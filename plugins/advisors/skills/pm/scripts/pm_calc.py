#!/usr/bin/env python3
"""PM 고문의 계산 도구. 읽기만 하고 파일을 쓰지 않는다.

하위 명령
- capacity : 기간의 작업 가능 시간과 부하 비율
- cadence  : 정기 점검표(_state/pm-cadence.md)의 마지막 실행일과 다음 예정일
- risks    : 위험 목록(_state/pm-risks.md)의 점수 순서와 결정 시점 알림
- issues   : GitHub 마일스톤·이슈 현황 (gh CLI 읽기 명령만 쓴다)

결과는 표준 출력으로 낸다. --json 을 주면 JSON 으로 낸다.
"""

import argparse
import datetime as dt
import glob
import json
import os
import re
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def parse_date(text):
    m = DATE_RE.search(text or "")
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def today_of(args):
    return dt.date.fromisoformat(args.today) if getattr(args, "today", None) else dt.date.today()


def emit(args, data, lines):
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        print("\n".join(lines))


# ── capacity ─────────────────────────────────────────────

def cmd_capacity(args):
    start = dt.date.fromisoformat(args.start)
    end = dt.date.fromisoformat(args.end)
    if end < start:
        raise SystemExit("--to 가 --from 보다 앞이다")
    holidays = {dt.date.fromisoformat(d.strip()) for d in (args.holidays or "").split(",") if d.strip()}

    weekdays = holidays_n = 0
    day = start
    while day <= end:
        # 토·일과 지정한 공휴일은 휴일 시간으로 센다
        if day.weekday() >= 5 or day in holidays:
            holidays_n += 1
        else:
            weekdays += 1
        day += dt.timedelta(days=1)

    raw = weekdays * args.weekday + holidays_n * args.holiday
    planned = raw * args.plan_ratio
    data = {
        "from": start, "to": end, "days": (end - start).days + 1,
        "weekdays": weekdays, "holiday_days": holidays_n,
        "holidays_given": sorted(holidays),
        "raw_hours": round(raw, 2), "plan_ratio": args.plan_ratio, "planned_hours": round(planned, 2),
        "formula": "{}×{} + {}×{} = {} ; ×{} = {}".format(
            weekdays, args.weekday, holidays_n, args.holiday, round(raw, 2), args.plan_ratio, round(planned, 2)),
    }
    lines = [
        "기간: {} ~ {} ({}일, 평일 {}일, 휴일 {}일)".format(start, end, data["days"], weekdays, holidays_n),
        "작업 가능 시간: " + data["formula"],
    ]
    if not holidays:
        lines.append("주의: --holidays 가 비어 있어 공휴일을 평일로 셌다")
    if args.load is not None and planned > 0:
        ratio = args.load / planned
        data["load_hours"] = args.load
        data["load_ratio"] = round(ratio, 3)
        lines.append("부하: {} / {} = {:.0%}{}".format(args.load, round(planned, 2), ratio, " (초과)" if ratio > 1 else ""))
    if args.must is not None and planned > 0:
        ratio = args.must / planned
        data["must_hours"] = args.must
        data["must_ratio"] = round(ratio, 3)
        data["must_limit"] = args.must_limit
        over = ratio > args.must_limit
        data["must_over_limit"] = over
        lines.append("필수 작업 비율: {} / {} = {:.0%} (한도 {:.0%}){}".format(
            args.must, round(planned, 2), ratio, args.must_limit, " — 한도 초과, 범위를 줄일 대상" if over else ""))
    emit(args, data, lines)


# ── cadence ──────────────────────────────────────────────

def read_table(path):
    """마크다운 파일의 첫 표를 칸 이름 → 값 사전 목록으로 읽는다."""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            text = f.read()
    except OSError:
        return None, ""
    header, rows = None, []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if header and rows:
                break  # 첫 표가 끝났다
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue  # 구분선
        rows.append(dict(zip(header, cells)))
    return rows, text


def latest_report(report_dir, pattern):
    """기록 패턴에 맞는 리포트 가운데 파일 이름 앞 날짜가 가장 늦은 것. 파일 시각은 쓰지 않는다."""
    best = None
    for path in glob.glob(os.path.join(report_dir, pattern)):
        d = parse_date(os.path.basename(path))
        if d and (best is None or d > best[0]):
            best = (d, os.path.relpath(path, report_dir).replace("\\", "/"))
    return best


def cmd_cadence(args):
    report_dir = os.path.normpath(args.report_dir)
    path = os.path.join(report_dir, "_state", "pm-cadence.md")
    rows, _ = read_table(path)
    if rows is None:
        emit(args, {"error": "no-cadence-file", "path": path}, ["점검표 없음: " + path])
        return
    today = today_of(args)
    milestone = dt.date.fromisoformat(args.milestone_date) if args.milestone_date else None

    out = []
    for r in rows:
        rid = r.get("ID", "")
        if not rid:
            continue
        period = r.get("주기", "")
        pattern = r.get("기록 패턴", "").strip("` ")
        last, source = None, ""
        if pattern and pattern != "-":
            found = latest_report(report_dir, pattern)
            if found:
                last, source = found
        manual = parse_date(r.get("마지막 실행", ""))
        if manual and (last is None or manual > last):
            last, source = manual, "점검표 기록"

        due, note = None, ""
        m_days = re.match(r"^\s*(\d+)\s*일?\s*$", period)
        m_mile = re.search(r"마일스톤\s*(\d+)\s*일\s*전", period)
        if m_days:
            due = (last + dt.timedelta(days=int(m_days.group(1)))) if last else today
            if not last:
                note = "기록 없음 — 지금 해당"
        elif m_mile:
            if milestone:
                due = milestone - dt.timedelta(days=int(m_mile.group(1)))
                if last and last >= due:
                    due, note = None, "이번 마일스톤 몫은 이미 실행함"
            else:
                note = "마일스톤 날짜 없음"
        else:
            note = "날짜로 계산하지 않는 주기"

        if due is None:
            state = note or "-"
        elif due < today:
            state = "지남 {}일".format((today - due).days)
        elif due == today:
            state = "오늘"
        else:
            state = "남음 {}일".format((due - today).days)
        out.append({
            "id": rid, "check": r.get("점검", ""), "how": r.get("실행 방법", ""), "period": period,
            "last": last, "last_source": source, "due": due, "state": state, "note": note,
        })

    lines = ["오늘: {}".format(today), "| ID | 점검 | 주기 | 마지막 실행 | 근거 | 다음 예정 | 상태 |", "|---|---|---|---|---|---|---|"]
    for o in out:
        lines.append("| {id} | {check} | {period} | {last} | {src} | {due} | {state} |".format(
            id=o["id"], check=o["check"], period=o["period"], last=o["last"] or "-",
            src=o["last_source"] or "-", due=o["due"] or "-", state=o["state"]))
    dues = [o["due"] for o in out if o["due"] and o["due"] > today]
    nxt = min(dues) if dues else None
    lines.append("")
    lines.append("가장 이른 다음 예정일(오늘 이후): {}".format(nxt or "없음"))
    emit(args, {"today": today, "rows": out, "next_due_after_today": nxt}, lines)


# ── risks ────────────────────────────────────────────────

IMPACT = {"치명": 4, "심각": 3, "보통": 2, "가벼움": 1}
LIKELIHOOD = {"높음": 3, "중간": 2, "낮음": 1}


def level(text, table):
    # "중간~높음"처럼 두 값을 적었으면 높은 쪽을 쓴다
    hits = [v for k, v in table.items() if k in (text or "")]
    return max(hits) if hits else None


def cmd_risks(args):
    report_dir = os.path.normpath(args.report_dir)
    path = os.path.join(report_dir, "_state", "pm-risks.md")
    rows, _ = read_table(path)
    if rows is None:
        emit(args, {"error": "no-risk-file", "path": path}, ["위험 목록 없음: " + path])
        return
    today = today_of(args)
    soon = dt.timedelta(days=args.soon_days)
    milestone = dt.date.fromisoformat(args.milestone_date) if args.milestone_date else None

    out = []
    for r in rows:
        rid = r.get("ID", "")
        if not rid:
            continue
        i, l = level(r.get("영향", ""), IMPACT), level(r.get("가능성", ""), LIKELIHOOD)
        score = i * l if i and l else None
        when = r.get("결정 시점", "")
        due = parse_date(when)
        if due is None and "마일스톤" in when and milestone:
            due = milestone
        state = r.get("상태", "")
        flag = ""
        if state in ("해소", "폐기"):
            flag = state
        elif due is None:
            flag = "결정 시점 없음"
        elif due < today:
            flag = "결정 시점 지남 {}일".format((today - due).days)
        elif due - today <= soon:
            flag = "결정 시점 {}일 남음".format((due - today).days)
        out.append({"id": rid, "risk": r.get("위험", ""), "impact": r.get("영향", ""), "likelihood": r.get("가능성", ""),
                    "score": score, "decide_by": due, "state": state, "flag": flag})

    active = [o for o in out if o["state"] not in ("해소", "폐기")]
    active.sort(key=lambda o: (-(o["score"] or 0), o["decide_by"] or dt.date.max, o["id"]))
    lines = ["오늘: {} / 점수 = 영향(치명 4·심각 3·보통 2·가벼움 1) × 가능성(높음 3·중간 2·낮음 1)".format(today),
             "| 순서 | ID | 위험 | 영향 | 가능성 | 점수 | 결정 시점 | 알림 |", "|---|---|---|---|---|---|---|---|"]
    for n, o in enumerate(active, 1):
        lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            n, o["id"], o["risk"].replace("|", "/"), o["impact"], o["likelihood"],
            o["score"] if o["score"] is not None else "영향·가능성 미기재", o["decide_by"] or "-", o["flag"]))
    closed = len(out) - len(active)
    lines.append("")
    lines.append("관리 중 {}건, 해소·폐기 {}건".format(len(active), closed))
    emit(args, {"today": today, "active": active, "closed_count": closed}, lines)


# ── issues ───────────────────────────────────────────────

def gh_json(argv):
    exe = shutil.which("gh")
    if not exe:
        raise SystemExit("gh CLI 를 찾지 못했다")
    res = subprocess.run([exe] + argv, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise SystemExit("gh 실패: {}\n{}".format(" ".join(argv), res.stderr.strip()))
    return json.loads(res.stdout or "null")


def parse_map(text):
    out = {}
    for part in (text or "").split(","):
        if "=" in part:
            k, v = part.rsplit("=", 1)
            out[k.strip()] = float(v)
    return out


def cmd_issues(args):
    repo = args.repo
    size_hours = parse_map(args.size_hours)
    order = [s.strip() for s in (args.order_labels or "").split(",") if s.strip()]
    since = dt.date.fromisoformat(args.since) if args.since else None
    today = today_of(args)

    milestones = gh_json(["api", "repos/{}/milestones?state=open&per_page=100".format(repo)]) or []
    fields = "number,title,labels,milestone,updatedAt"
    open_issues = gh_json(["issue", "list", "--repo", repo, "--state", "open", "--limit", str(args.limit), "--json", fields]) or []
    closed = []
    if since:
        closed = gh_json(["issue", "list", "--repo", repo, "--state", "closed", "--limit", str(args.limit),
                          "--search", "closed:>={}".format(since), "--json", fields + ",closedAt"]) or []

    def labels(i):
        return [l.get("name", "") for l in i.get("labels", [])]

    def hours(i):
        hs = [size_hours[l] for l in labels(i) if l in size_hours]
        return hs[0] if hs else None

    def order_rank(i):
        ranks = [order.index(l) for l in labels(i) if l in order]
        return min(ranks) if ranks else len(order)

    ms_due = {}
    for m in milestones:
        ms_due[m["title"]] = parse_date(m.get("due_on") or "")

    def ms_key(i):
        title = (i.get("milestone") or {}).get("title")
        if not title:
            return (2, dt.date.max, "")
        due = ms_due.get(title)
        return (0 if due else 1, due or dt.date.max, title)

    rows = []
    for i in open_issues:
        ls = labels(i)
        rows.append({
            "number": i["number"], "title": i["title"],
            "milestone": (i.get("milestone") or {}).get("title") or "백로그",
            "must": args.must_label in ls if args.must_label else False,
            "blocked": args.blocked_label in ls if args.blocked_label else False,
            "in_progress": args.progress_label in ls if args.progress_label else False,
            "hours": hours(i), "labels": ls,
            "_key": ms_key(i) + (order_rank(i), 0 if (args.must_label in ls) else 1, i["number"]),
        })
    rows.sort(key=lambda r: r["_key"])

    summary = []
    for m in sorted(milestones, key=lambda m: (ms_due.get(m["title"]) or dt.date.max, m["title"])):
        title = m["title"]
        mine = [r for r in rows if r["milestone"] == title]
        known = [r["hours"] for r in mine if r["hours"] is not None]
        must_known = [r["hours"] for r in mine if r["must"] and r["hours"] is not None]
        due = ms_due.get(title)
        summary.append({
            "title": title, "due": due, "days_left": (due - today).days if due else None,
            "open": len(mine), "open_hours": round(sum(known), 2), "unsized": len(mine) - len(known),
            "must_open": sum(1 for r in mine if r["must"]), "must_hours": round(sum(must_known), 2),
            "blocked": sum(1 for r in mine if r["blocked"]),
            "closed_since": sum(1 for c in closed if (c.get("milestone") or {}).get("title") == title),
            "description": (m.get("description") or "").strip(),
        })

    lines = ["저장소: {} / 오늘: {}{}".format(repo, today, " / 완료 집계 기준일: {}".format(since) if since else "")]
    lines.append("")
    lines.append("## 열린 마일스톤")
    lines.append("| 마일스톤 | 마감 | 남은 날 | 열린 이슈 | 열린 규모(h) | 규모 없음 | 필수 | 필수 규모(h) | 대기 | 기준일 뒤 닫힘 |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for s in summary:
        lines.append("| {title} | {due} | {left} | {open} | {oh} | {un} | {mo} | {mh} | {bl} | {cs} |".format(
            title=s["title"], due=s["due"] or "-", left=s["days_left"] if s["days_left"] is not None else "-",
            open=s["open"], oh=s["open_hours"], un=s["unsized"], mo=s["must_open"], mh=s["must_hours"],
            bl=s["blocked"], cs=s["closed_since"] if since else "-"))
    lines.append("")
    lines.append("## 열린 이슈 (마일스톤 마감 → 순서 라벨 → 필수 → 번호)")
    lines.append("| # | 제목 | 마일스톤 | 규모(h) | 필수 | 대기 | 진행 중 |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows[: args.top]:
        lines.append("| {n} | {t} | {m} | {h} | {mu} | {b} | {p} |".format(
            n=r["number"], t=r["title"].replace("|", "/"), m=r["milestone"],
            h=r["hours"] if r["hours"] is not None else "-", mu="예" if r["must"] else "",
            b="예" if r["blocked"] else "", p="예" if r["in_progress"] else ""))
    if len(rows) > args.top:
        lines.append("(나머지 {}건 생략. --top 으로 늘린다)".format(len(rows) - args.top))
    if since:
        lines.append("")
        lines.append("## {} 이후 닫힌 이슈 ({}건)".format(since, len(closed)))
        for c in sorted(closed, key=lambda c: c.get("closedAt") or ""):
            lines.append("- #{} {} ({}, 닫힘 {})".format(
                c["number"], c["title"], (c.get("milestone") or {}).get("title") or "백로그", (c.get("closedAt") or "")[:10]))
    lines.append("")
    lines.append("주의: 이 순서는 라벨만 본 초안이다. 선행 관계(Blocked by)는 반영하지 않았다.")

    for r in rows:
        r.pop("_key", None)
    emit(args, {"today": today, "since": since, "milestones": summary, "open": rows, "closed_since": closed}, lines)


def main():
    ap = argparse.ArgumentParser(description="PM 고문 계산 도구 (읽기 전용)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("capacity", help="기간의 작업 가능 시간과 부하 비율")
    c.add_argument("--from", dest="start", required=True)
    c.add_argument("--to", dest="end", required=True)
    c.add_argument("--weekday", type=float, required=True, help="평일 하루 작업 시간")
    c.add_argument("--holiday", type=float, required=True, help="토·일·공휴일 하루 작업 시간")
    c.add_argument("--holidays", help="공휴일 날짜 목록. 쉼표로 구분")
    c.add_argument("--plan-ratio", type=float, default=1.0, help="계획에 쓰는 비율. 예: 0.7")
    c.add_argument("--load", type=float, help="이 기간에 잡은 작업 규모 합(시간)")
    c.add_argument("--must", type=float, help="그 가운데 필수 작업 규모 합(시간)")
    c.add_argument("--must-limit", type=float, default=0.6)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_capacity)

    k = sub.add_parser("cadence", help="정기 점검표의 다음 예정일")
    k.add_argument("report_dir")
    k.add_argument("--today")
    k.add_argument("--milestone-date", help="'마일스톤 N일 전' 주기에 쓸 마일스톤 날짜")
    k.add_argument("--json", action="store_true")
    k.set_defaults(func=cmd_cadence)

    r = sub.add_parser("risks", help="위험 목록(_state/pm-risks.md)의 점수와 결정 시점 알림")
    r.add_argument("report_dir")
    r.add_argument("--today")
    r.add_argument("--soon-days", type=int, default=14, help="결정 시점이 이 날수 안이면 알린다")
    r.add_argument("--milestone-date", help="결정 시점이 '마일스톤'으로만 적힌 위험에 쓸 날짜")
    r.add_argument("--json", action="store_true")
    r.set_defaults(func=cmd_risks)

    i = sub.add_parser("issues", help="GitHub 마일스톤·이슈 현황 (gh 읽기 명령만)")
    i.add_argument("--repo", required=True, help="owner/repo")
    i.add_argument("--since", help="이 날짜 이후 닫힌 이슈를 함께 센다")
    i.add_argument("--size-hours", help='규모 라벨=시간. 예: "size: S=1,size: M=2,size: L=5.5"')
    i.add_argument("--order-labels", help="앞에 올수록 먼저인 순서 라벨 목록. 쉼표로 구분")
    i.add_argument("--must-label")
    i.add_argument("--blocked-label")
    i.add_argument("--progress-label")
    i.add_argument("--limit", type=int, default=300)
    i.add_argument("--top", type=int, default=15)
    i.add_argument("--today")
    i.add_argument("--json", action="store_true")
    i.set_defaults(func=cmd_issues)

    args = ap.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
