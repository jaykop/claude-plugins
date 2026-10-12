#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Steam 리뷰 수집·집계 도구 (advisors 시장 동향 고문용).

하위 명령
  count   <appid>... 게임마다 누적 리뷰 수·추천 수·비추천 수만 조회해 표로 낸다 (리뷰 본문은 받지 않음).
  fetch   <appid>  Steam 공식 리뷰 JSON 을 커서로 넘기며 받아 JSONL 로 저장한다.
  summary <jsonl>  언어 분포, 추천 비율, 월별 분포를 센다. --labels 를 주면 분류별 개수도 센다.
  sample  <jsonl>  분류 결과를 눈으로 대조할 수 있게 리뷰 몇 개를 무작위로 뽑아 보여 준다.

원칙
  - 표준 라이브러리만 쓴다. Python 3.8 이상, Windows/macOS/Linux 공용.
  - 결과는 --out 으로 받은 경로에만 쓴다. 없으면 표준 출력으로 낸다.
  - 작성자 계정 ID, 닉네임, 프로필 주소는 저장하지 않는다. 플레이 시간 숫자만 남긴다.
  - 리뷰 개수는 모델이 아니라 이 스크립트가 센다.
"""

import argparse
import csv
import json
import os
import random
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, OrderedDict
from datetime import date, datetime, timezone

API_URL = "https://store.steampowered.com/appreviews/{appid}"
HARD_MAX = 5000            # 한 번에 받을 수 있는 리뷰 개수의 절대 상한
HARD_TIME_LIMIT = 1800     # 초. 한 번 실행의 절대 시간 상한
MAX_FILE_BYTES = 200 * 1024 * 1024
USER_AGENT = "advisors-market-steam-reviews/1.0 (+https://github.com/jaykop/claude-plugins)"

EXIT_OK = 0
EXIT_NOTHING = 1     # 하나도 받지 못함 (조회 실패)
EXIT_PARTIAL = 2     # 일부만 받음 (시간 초과 또는 중간 조회 실패)
EXIT_USAGE = 3       # 입력 오류


def _reconfigure_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _fail(msg, code=EXIT_USAGE):
    sys.stderr.write("오류: " + msg + "\n")
    sys.exit(code)


def _parse_day(text, name):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        _fail("{} 은 YYYY-MM-DD 형식이어야 한다: {}".format(name, text))


def _ts_to_day(ts):
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
    except (TypeError, ValueError, OSError, OverflowError):
        return None


def _open_out(path):
    """--out 경로를 연다. 없으면 표준 출력."""
    if not path or path == "-":
        return sys.stdout, False
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    return open(path, "w", encoding="utf-8", newline="\n"), True


# ---------------------------------------------------------------- fetch

def _get_json(url, timeout, retries, base_wait):
    """JSON 한 쪽을 받는다. (데이터, 오류 설명) 을 돌려준다."""
    last_err = ""
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            return json.loads(raw.decode("utf-8")), ""
        except urllib.error.HTTPError as e:
            last_err = "HTTP {}".format(e.code)
            if e.code not in (429, 500, 502, 503, 504):
                return None, last_err
        except urllib.error.URLError as e:
            last_err = "연결 실패 ({})".format(getattr(e, "reason", e))
        except (TimeoutError, OSError) as e:
            last_err = "시간 초과 또는 연결 오류 ({})".format(e)
        except ValueError as e:
            last_err = "JSON 해석 실패 ({})".format(e)
            return None, last_err
        if attempt < retries:
            time.sleep(base_wait * (2 ** attempt))
    return None, last_err


def _slim(review):
    """저장할 칸만 남긴다. 작성자 식별 정보는 버린다."""
    author = review.get("author") or {}
    created = _ts_to_day(review.get("timestamp_created"))
    updated = _ts_to_day(review.get("timestamp_updated"))
    return OrderedDict([
        ("recommendationid", str(review.get("recommendationid", ""))),
        ("language", review.get("language", "")),
        ("voted_up", bool(review.get("voted_up"))),
        ("created", created.isoformat() if created else ""),
        ("updated", updated.isoformat() if updated else ""),
        ("timestamp_created", review.get("timestamp_created")),
        ("playtime_at_review_min", author.get("playtime_at_review")),
        ("votes_up", review.get("votes_up")),
        ("votes_funny", review.get("votes_funny")),
        ("comment_count", review.get("comment_count")),
        ("steam_purchase", review.get("steam_purchase")),
        ("received_for_free", review.get("received_for_free")),
        ("written_during_early_access", review.get("written_during_early_access")),
        ("primarily_steam_deck", review.get("primarily_steam_deck")),
        ("review", review.get("review", "")),
    ])


def cmd_count(args):
    appids = [str(a) for a in args.appids]
    bad = [a for a in appids if not a.isdigit()]
    if bad:
        _fail("appid 는 숫자여야 한다: {}".format(", ".join(bad)))
    if len(appids) > 100:
        _fail("한 번에 100개까지만 조회한다 (받은 개수 {})".format(len(appids)))
    started = time.monotonic()
    time_limit = min(args.time_limit, HARD_TIME_LIMIT)
    lines = [
        "| 앱 ID | 누적 리뷰 수 | 추천 | 비추천 | 추천 비율 | Steam 평가 문구 | 결과 |",
        "|---|---|---|---|---|---|---|",
    ]
    ok = failed = 0
    for i, appid in enumerate(appids):
        if time.monotonic() - started > time_limit:
            for rest in appids[i:]:
                lines.append("| {} | - | - | - | - | - | 조회 안 함 (시간 초과) |".format(rest))
                failed += 1
            break
        params = OrderedDict([
            ("json", "1"), ("filter", "recent"), ("language", args.language),
            ("review_type", "all"), ("purchase_type", args.purchase_type),
            ("num_per_page", "0"), ("cursor", "*"),
        ])
        url = API_URL.format(appid=appid) + "?" + urllib.parse.urlencode(params)
        data, err = _get_json(url, args.timeout, args.retries, max(args.delay, 1.0))
        if data is None or data.get("success") != 1:
            reason = err or "응답의 success 값이 1 이 아님"
            lines.append("| {} | - | - | - | - | - | 조회 실패: {} |".format(appid, reason))
            failed += 1
        else:
            qs = data.get("query_summary") or {}
            total = qs.get("total_reviews") or 0
            pos = qs.get("total_positive") or 0
            neg = qs.get("total_negative") or 0
            note = "열림" if total else "열림 — 리뷰 0개, 앱 ID 가 맞는지 스토어 페이지로 확인"
            lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                appid, total, pos, neg, _pct(pos, total), qs.get("review_score_desc", ""), note))
            ok += 1
        if i + 1 < len(appids):
            time.sleep(args.delay)
    lines.append("")
    lines.append("조회일: {} / 조건: language={} purchase_type={} / 출처: {}?json=1&num_per_page=0".format(
        date.today().isoformat(), args.language, args.purchase_type, API_URL.format(appid="<앱 ID>")))
    lines.append("추천 비율 = 추천 / 누적 리뷰 수 × 100 (이 스크립트가 계산). 누적 리뷰 수는 판매량이 아니다.")
    _emit(lines, args.out)
    if ok == 0:
        return EXIT_NOTHING
    return EXIT_PARTIAL if failed else EXIT_OK


def cmd_fetch(args):
    if not str(args.appid).isdigit():
        _fail("appid 는 숫자여야 한다: {}".format(args.appid))
    if args.max < 1:
        _fail("--max 는 1 이상이어야 한다")
    max_n = min(args.max, HARD_MAX)
    time_limit = min(args.time_limit, HARD_TIME_LIMIT)
    since_day = _parse_day(args.since, "--since") if args.since else None
    if since_day and args.filter != "recent":
        _fail("--since 는 --filter recent 일 때만 쓸 수 있다 (작성일 순서로 받을 때만 멈출 지점을 알 수 있다)")

    base_params = OrderedDict([
        ("json", "1"),
        ("filter", args.filter),
        ("language", args.language),
        ("review_type", args.review_type),
        ("purchase_type", args.purchase_type),
        ("num_per_page", "100"),
    ])
    url_base = API_URL.format(appid=args.appid)

    started = time.monotonic()
    cursor = "*"
    seen_cursors = set()
    seen_ids = set()
    records = []
    query_summary = None
    requests_made = 0
    stop_reason = ""
    partial = False
    reached_since = False

    while True:
        if len(records) >= max_n:
            stop_reason = "상한 도달 (--max {})".format(max_n)
            break
        if time.monotonic() - started > time_limit:
            stop_reason = "시간 초과로 중단 ({}초) — 일부만 받음".format(time_limit)
            partial = True
            break
        params = OrderedDict(base_params)
        params["cursor"] = cursor
        url = url_base + "?" + urllib.parse.urlencode(params)
        data, err = _get_json(url, args.timeout, args.retries, max(args.delay, 1.0))
        requests_made += 1
        if data is None:
            stop_reason = "조회 실패: {}".format(err)
            partial = bool(records)
            break
        if data.get("success") != 1:
            stop_reason = "조회 실패: 응답의 success 값이 1 이 아님 ({})".format(data.get("success"))
            partial = bool(records)
            break
        if query_summary is None:
            query_summary = data.get("query_summary")
        page = data.get("reviews") or []
        if not page:
            stop_reason = "끝 (더 받을 리뷰 없음)"
            break
        for review in page:
            rid = str(review.get("recommendationid", ""))
            if not rid or rid in seen_ids:
                continue
            if since_day:
                created = _ts_to_day(review.get("timestamp_created"))
                if created and created < since_day:
                    reached_since = True
                    continue
            seen_ids.add(rid)
            records.append(_slim(review))
            if len(records) >= max_n:
                break
        if reached_since:
            stop_reason = "기준일 {} 이전 리뷰에 도달".format(since_day.isoformat())
            break
        next_cursor = data.get("cursor")
        if not next_cursor or next_cursor in seen_cursors or next_cursor == cursor:
            stop_reason = "끝 (커서가 더 넘어가지 않음)"
            break
        seen_cursors.add(next_cursor)
        cursor = next_cursor
        time.sleep(args.delay)

    elapsed = round(time.monotonic() - started, 1)
    meta = OrderedDict([
        ("tool", "steam_reviews.py fetch"),
        ("appid", str(args.appid)),
        ("fetched_on", date.today().isoformat()),
        ("source", url_base),
        ("params", OrderedDict([
            ("filter", args.filter), ("language", args.language),
            ("review_type", args.review_type), ("purchase_type", args.purchase_type),
            ("max", max_n), ("since", args.since or ""),
        ])),
        ("query_summary", query_summary),
        ("count", len(records)),
        ("requests", requests_made),
        ("elapsed_sec", elapsed),
        ("stop_reason", stop_reason),
    ])

    if not records and not stop_reason.startswith("끝") and not reached_since:
        sys.stderr.write("받은 리뷰 0개 / 멈춘 이유: {}\n".format(stop_reason))
        sys.stderr.write("검색 실패로 기록할 것. 0개로 세지 않는다.\n")
        return EXIT_NOTHING

    out, is_file = _open_out(args.out)
    try:
        out.write(json.dumps({"_meta": meta}, ensure_ascii=False) + "\n")
        for rec in records:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
    finally:
        if is_file:
            out.close()

    status = sys.stdout if is_file else sys.stderr
    status.write("받은 리뷰 {}개 / 요청 {}회 / {}초 / 멈춘 이유: {}\n".format(
        len(records), requests_made, elapsed, stop_reason))
    if query_summary:
        status.write("조회 조건 전체 리뷰 수(query_summary): total_reviews={} total_positive={} total_negative={} ({})\n".format(
            query_summary.get("total_reviews"), query_summary.get("total_positive"),
            query_summary.get("total_negative"), query_summary.get("review_score_desc")))
    if is_file:
        status.write("저장: {}\n".format(os.path.abspath(args.out)))
    return EXIT_PARTIAL if partial else EXIT_OK


# ---------------------------------------------------------------- load

def _load_jsonl(path):
    if not os.path.isfile(path):
        _fail("파일이 없다: {}".format(path))
    if os.path.getsize(path) > MAX_FILE_BYTES:
        _fail("파일이 너무 크다 (상한 {} 바이트): {}".format(MAX_FILE_BYTES, path))
    meta = None
    reviews = []
    bad = 0
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                bad += 1
                continue
            if isinstance(obj, dict) and "_meta" in obj:
                meta = obj["_meta"]
                continue
            if isinstance(obj, dict) and obj.get("recommendationid"):
                reviews.append(obj)
            else:
                bad += 1
    return meta, reviews, bad


def _filter_reviews(reviews, args):
    from_day = _parse_day(args.date_from, "--from") if args.date_from else None
    to_day = _parse_day(args.date_to, "--to") if args.date_to else None
    langs = None
    if args.lang:
        langs = set(x.strip() for x in args.lang.split(",") if x.strip())
    picked = []
    for r in reviews:
        if langs is not None and r.get("language") not in langs:
            continue
        if from_day or to_day:
            try:
                d = datetime.strptime(r.get("created", ""), "%Y-%m-%d").date()
            except ValueError:
                continue
            if from_day and d < from_day:
                continue
            if to_day and d > to_day:
                continue
        picked.append(r)
    return picked


def _load_labels(path):
    """리뷰 ID → 분류 집합. 한 리뷰에 여러 줄(여러 분류)을 둘 수 있다."""
    if not os.path.isfile(path):
        _fail("분류 파일이 없다: {}".format(path))
    labels = {}
    rows = 0
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = None
        for row in reader:
            if not row or all(not c.strip() for c in row):
                continue
            if header is None:
                header = [c.strip().lower() for c in row]
                if "recommendationid" in header and "label" in header:
                    continue
                header = ["recommendationid", "label"]
            if len(row) < 2:
                continue
            rid, label = row[0].strip(), row[1].strip()
            if not rid or not label:
                continue
            labels.setdefault(rid, set()).add(label)
            rows += 1
    return labels, rows


def _pct(n, d):
    return "{:.1f}%".format(100.0 * n / d) if d else "-"


# ---------------------------------------------------------------- summary

def cmd_summary(args):
    meta, reviews, bad = _load_jsonl(args.jsonl)
    picked = _filter_reviews(reviews, args)
    n = len(picked)
    lines = []
    w = lines.append

    w("# Steam 리뷰 집계")
    w("")
    w("| 항목 | 값 |")
    w("|---|---|")
    w("| 원문 파일 | {} |".format(os.path.abspath(args.jsonl)))
    if meta:
        p = meta.get("params", {})
        w("| 앱 ID | {} |".format(meta.get("appid", "")))
        w("| 받은 날 | {} |".format(meta.get("fetched_on", "")))
        w("| 받은 조건 | filter={} language={} review_type={} purchase_type={} max={} since={} |".format(
            p.get("filter"), p.get("language"), p.get("review_type"), p.get("purchase_type"),
            p.get("max"), p.get("since") or "-"))
        w("| 받기를 멈춘 이유 | {} |".format(meta.get("stop_reason", "")))
        qs = meta.get("query_summary") or {}
        if qs:
            w("| 조회 조건 전체 리뷰 수 (Steam 이 돌려준 값) | 전체 {} / 추천 {} / 비추천 {} / 평가 문구 \"{}\" |".format(
                qs.get("total_reviews"), qs.get("total_positive"), qs.get("total_negative"), qs.get("review_score_desc")))
    else:
        w("| 앱 ID | 메타 줄 없음 (fetch 로 받은 파일이 아님) |")
    w("| 파일 안 리뷰 수 | {} |".format(len(reviews)))
    w("| 걸러 낸 조건 | 언어={} / 작성일 {} ~ {} |".format(args.lang or "전체", args.date_from or "처음", args.date_to or "끝"))
    w("| 집계한 리뷰 수 (표본) | {} |".format(n))
    if bad:
        w("| 읽지 못한 줄 | {} |".format(bad))
    w("")

    if n == 0:
        w("집계할 리뷰가 없다. 조건을 확인한다. 0개를 '불만 없음' 같은 결론으로 쓰지 않는다.")
        return _emit(lines, args.out)

    up = sum(1 for r in picked if r.get("voted_up"))
    w("## 추천 비율")
    w("")
    w("| 추천 | 비추천 | 추천 비율 |")
    w("|---|---|---|")
    w("| {} | {} | {} |".format(up, n - up, _pct(up, n)))
    w("")

    w("## 언어 분포")
    w("")
    w("| 언어 | 개수 | 비율 | 추천 비율 |")
    w("|---|---|---|---|")
    lang_count = Counter(r.get("language", "") for r in picked)
    for lang, c in lang_count.most_common():
        lang_up = sum(1 for r in picked if r.get("language", "") == lang and r.get("voted_up"))
        w("| {} | {} | {} | {} |".format(lang or "(빈 값)", c, _pct(c, n), _pct(lang_up, c)))
    w("")

    w("## 작성 월별 분포")
    w("")
    w("| 월 | 개수 | 추천 비율 |")
    w("|---|---|---|")
    month_count = Counter()
    month_up = Counter()
    for r in picked:
        m = (r.get("created") or "")[:7] or "(날짜 없음)"
        month_count[m] += 1
        if r.get("voted_up"):
            month_up[m] += 1
    for m in sorted(month_count):
        w("| {} | {} | {} |".format(m, month_count[m], _pct(month_up[m], month_count[m])))
    w("")

    w("## 구매 경로와 기타")
    w("")
    w("| 항목 | 개수 | 비율 |")
    w("|---|---|---|")
    for key, name in (("steam_purchase", "Steam 에서 구매"), ("received_for_free", "무료로 받음"),
                      ("written_during_early_access", "앞서 해보기 기간에 작성"),
                      ("primarily_steam_deck", "주로 Steam Deck 에서 플레이")):
        c = sum(1 for r in picked if r.get(key) is True)
        w("| {} | {} | {} |".format(name, c, _pct(c, n)))
    hours = [r.get("playtime_at_review_min") for r in picked if isinstance(r.get("playtime_at_review_min"), (int, float))]
    if hours:
        w("| 리뷰 작성 시점 플레이 시간 중앙값 | {:.1f}시간 | 값이 있는 리뷰 {}개 기준 |".format(
            statistics.median(hours) / 60.0, len(hours)))
    w("")

    if args.labels:
        labels, label_rows = _load_labels(args.labels)
        ids = set(r["recommendationid"] for r in picked)
        labeled = [r for r in picked if r["recommendationid"] in labels]
        unknown = sorted(set(labels) - set(r["recommendationid"] for r in reviews))
        outside = [rid for rid in labels if rid not in ids and rid not in unknown]
        m = len(labeled)
        w("## 분류별 개수")
        w("")
        w("| 항목 | 값 |")
        w("|---|---|")
        w("| 분류 파일 | {} |".format(os.path.abspath(args.labels)))
        w("| 분류 줄 수 | {} |".format(label_rows))
        w("| 표본 중 분류된 리뷰 | {} / {} |".format(m, n))
        w("| 표본 중 분류 안 된 리뷰 | {} |".format(n - m))
        w("| 원문 파일에 없는 리뷰 ID | {} |".format(len(unknown)))
        w("| 걸러 낸 조건 밖의 리뷰 ID | {} |".format(len(outside)))
        w("")
        if m:
            label_count = Counter()
            label_up = Counter()
            for r in labeled:
                for lab in labels[r["recommendationid"]]:
                    label_count[lab] += 1
                    if r.get("voted_up"):
                        label_up[lab] += 1
            w("한 리뷰가 여러 분류에 들 수 있으므로 비율의 합은 100% 를 넘을 수 있다. 비율의 분모는 분류된 리뷰 수 {}개다.".format(m))
            w("")
            w("| 분류 | 리뷰 수 | 분류된 리뷰 중 비율 | 그중 추천 | 그중 비추천 |")
            w("|---|---|---|---|---|")
            for lab, c in sorted(label_count.items(), key=lambda kv: (-kv[1], kv[0])):
                w("| {} | {} | {} | {} | {} |".format(lab, c, _pct(c, m), label_up[lab], c - label_up[lab]))
            w("")
        if unknown:
            w("원문 파일에 없는 리뷰 ID (앞 10개): " + ", ".join(unknown[:10]))
            w("")
    return _emit(lines, args.out)


def _emit(lines, out_path):
    out, is_file = _open_out(out_path)
    try:
        out.write("\n".join(lines) + "\n")
    finally:
        if is_file:
            out.close()
            sys.stdout.write("저장: {}\n".format(os.path.abspath(out_path)))
    return EXIT_OK


# ---------------------------------------------------------------- sample

def cmd_sample(args):
    meta, reviews, _ = _load_jsonl(args.jsonl)
    picked = _filter_reviews(reviews, args)
    labels = {}
    if args.labels:
        labels, _ = _load_labels(args.labels)
        if args.labeled_only:
            picked = [r for r in picked if r["recommendationid"] in labels]
    if not picked:
        return _emit(["뽑을 리뷰가 없다."], args.out)
    rng = random.Random(args.seed)
    k = min(args.n, len(picked))
    chosen = rng.sample(picked, k)
    lines = ["# 대조용 표본 — {}개 중 {}개 (seed={})".format(len(picked), k, args.seed), ""]
    for r in chosen:
        text = (r.get("review") or "").replace("\r", " ").replace("\n", " ").strip()
        if len(text) > args.chars:
            text = text[:args.chars] + " …"
        lab = ", ".join(sorted(labels.get(r["recommendationid"], []))) or "(분류 없음)"
        lines.append("- {} | {} | {} | {} | 분류: {}".format(
            r["recommendationid"], r.get("language", ""), "추천" if r.get("voted_up") else "비추천",
            r.get("created", ""), lab))
        lines.append("  > " + text)
    return _emit(lines, args.out)


# ---------------------------------------------------------------- main

def build_parser():
    p = argparse.ArgumentParser(
        prog="steam_reviews.py",
        description="Steam 공식 리뷰 JSON 을 받아 누적 수치를 조회하거나 JSONL 로 저장하고, 언어·추천·월별·분류별 개수를 센다.",
        epilog="종료 코드: 0 정상, 1 하나도 받지 못함(조회 실패), 2 일부만 받음, 3 입력 오류.",
    )
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("count", help="게임마다 누적 리뷰 수·추천 비율만 조회한다",
                       description="num_per_page=0 으로 요청해 Steam 이 돌려주는 누적 수치만 표로 낸다. 리뷰 본문은 받지 않는다.")
    c.add_argument("appids", nargs="+", help="Steam 앱 ID 들 (숫자, 최대 100개)")
    c.add_argument("--language", default="all", help="Steam 언어 코드 (기본 all)")
    c.add_argument("--purchase-type", choices=["all", "steam", "non_steam_purchase"], default="all",
                   help="구매 경로 거르기 (기본 all)")
    c.add_argument("--delay", type=float, default=1.5, help="요청 사이 대기 초 (기본 1.5, 최소 0.5)")
    c.add_argument("--timeout", type=float, default=30.0, help="요청 하나의 제한 시간 초 (기본 30)")
    c.add_argument("--retries", type=int, default=2, help="실패한 요청을 다시 시도할 횟수 (기본 2)")
    c.add_argument("--time-limit", type=int, default=300, help="전체 실행 제한 시간 초 (기본 300)")
    c.add_argument("--out", help="결과를 저장할 경로. 없으면 표준 출력")

    f = sub.add_parser("fetch", help="리뷰를 받아 JSONL 로 저장한다",
                       description="store.steampowered.com/appreviews/<appid>?json=1 을 커서로 넘기며 받는다. "
                                   "첫 줄은 받은 조건을 담은 메타 줄이다. 작성자 식별 정보는 저장하지 않는다.")
    f.add_argument("appid", help="Steam 앱 ID (숫자)")
    f.add_argument("--max", type=int, default=300, help="받을 리뷰 최대 개수 (기본 300, 절대 상한 {})".format(HARD_MAX))
    f.add_argument("--out", help="저장할 JSONL 경로. 없으면 표준 출력")
    f.add_argument("--filter", choices=["recent", "updated", "all"], default="recent",
                   help="정렬 방식. recent=작성일 최신순(기본), updated=수정일 최신순, all=도움됨 순")
    f.add_argument("--language", default="all", help="Steam 언어 코드. 예: all(기본), english, koreana, japanese, schinese")
    f.add_argument("--review-type", choices=["all", "positive", "negative"], default="all", help="추천/비추천 거르기 (기본 all)")
    f.add_argument("--purchase-type", choices=["all", "steam", "non_steam_purchase"], default="all",
                   help="구매 경로 거르기 (기본 all. 서버 쪽 기본값에 기대지 않도록 늘 명시해서 보낸다)")
    f.add_argument("--since", help="작성일이 이 날짜(YYYY-MM-DD, UTC 기준)보다 오래된 리뷰를 만나면 멈춘다. --filter recent 일 때만")
    f.add_argument("--delay", type=float, default=1.5, help="요청 사이 대기 초 (기본 1.5, 최소 0.5)")
    f.add_argument("--timeout", type=float, default=30.0, help="요청 하나의 제한 시간 초 (기본 30)")
    f.add_argument("--retries", type=int, default=2, help="실패한 요청을 다시 시도할 횟수 (기본 2)")
    f.add_argument("--time-limit", type=int, default=300,
                   help="전체 실행 제한 시간 초 (기본 300, 절대 상한 {}). 넘으면 받은 만큼 저장하고 '시간 초과'로 표시".format(HARD_TIME_LIMIT))

    for name, helptext in (("summary", "언어·추천·월별·분류별 개수를 센다"),
                           ("sample", "대조용으로 리뷰 몇 개를 무작위로 뽑는다")):
        s = sub.add_parser(name, help=helptext, description=helptext)
        s.add_argument("jsonl", help="fetch 로 저장한 JSONL 경로")
        s.add_argument("--labels", help="분류 CSV 경로. 칸: recommendationid,label (한 리뷰에 여러 줄 가능)")
        s.add_argument("--lang", help="이 언어만 센다. 쉼표로 여러 개. 예: english,koreana")
        s.add_argument("--from", dest="date_from", help="작성일(UTC 기준)이 이 날짜(YYYY-MM-DD) 이후인 리뷰만")
        s.add_argument("--to", dest="date_to", help="작성일(UTC 기준)이 이 날짜(YYYY-MM-DD) 이전인 리뷰만")
        s.add_argument("--out", help="결과를 저장할 경로. 없으면 표준 출력")
        if name == "sample":
            s.add_argument("--n", type=int, default=20, help="뽑을 개수 (기본 20)")
            s.add_argument("--seed", type=int, default=1, help="무작위 씨앗 값 (기본 1). 같은 값이면 같은 표본")
            s.add_argument("--chars", type=int, default=300, help="본문을 이 글자 수에서 자른다 (기본 300)")
            s.add_argument("--labeled-only", action="store_true", help="분류된 리뷰에서만 뽑는다")
    return p


def main(argv=None):
    _reconfigure_stdout()
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd in ("fetch", "count"):
        args.delay = max(args.delay, 0.5)
        return cmd_fetch(args) if args.cmd == "fetch" else cmd_count(args)
    if args.cmd == "summary":
        return cmd_summary(args)
    if args.cmd == "sample":
        return cmd_sample(args)
    parser.print_help()
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
