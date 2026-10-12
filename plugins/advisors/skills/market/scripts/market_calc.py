#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""시장 동향 고문의 계산 도구. 머릿속 계산 대신 이 스크립트를 쓴다.

하위 명령
  stats    값 여러 개의 개수·최소·사분위·중앙값·최대·평균·합계
  change   직전 값과 이번 값의 차이와 증감률
  position 한 값이 값 묶음 안에서 놓이는 위치 (아래·같음·위 개수, 백분위 순위)
  window   오늘부터 거꾸로 N개월 범위 ('최근' 범위 고정용)
  next     기준일에서 주기만큼 지난 날짜 ('다음 점검:' 줄용)
  snapshot market-snapshot.md 를 읽어 지표별 최근 값을 보여 주고, --new 로 준 이번 값과 비교

원칙
  - 표준 라이브러리만 쓴다. Python 3.8 이상, Windows/macOS/Linux 공용.
  - 파일은 읽기만 한다. 결과는 --out 경로에만 쓰고, 없으면 표준 출력으로 낸다.
  - 출력에 계산식을 함께 적는다. 리포트에 그대로 옮겨 근거로 남긴다.
"""

import argparse
import calendar
import os
import re
import statistics
import sys
from datetime import date, datetime, timedelta

MAX_FILE_BYTES = 5 * 1024 * 1024
EXIT_OK = 0
EXIT_USAGE = 3

_STRIP = re.compile(r"[,\s$€£¥₩%]")


def _reconfigure_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _fail(msg):
    sys.stderr.write("오류: " + msg + "\n")
    sys.exit(EXIT_USAGE)


def _num(text):
    """'12,340' '$29.99' '87.2%' 같은 값을 숫자로 읽는다. 단위 추측(k, 만 등)은 하지 않는다."""
    raw = str(text).strip()
    cleaned = _STRIP.sub("", raw)
    try:
        return float(cleaned)
    except ValueError:
        return None


def _nums(values):
    out = []
    for v in values:
        x = _num(v)
        if x is None:
            _fail("숫자로 읽을 수 없는 값: {} (천 단위 쉼표, 통화 기호, % 만 지울 수 있다)".format(v))
        out.append(x)
    return out


def _fmt(x):
    if x is None:
        return "-"
    if abs(x - round(x)) < 1e-9 and abs(x) < 1e15:
        return "{:,}".format(int(round(x)))
    return "{:,.4f}".format(x).rstrip("0").rstrip(".")


def _day(text, name):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        _fail("{} 은 YYYY-MM-DD 형식이어야 한다: {}".format(name, text))


def _add_months(d, months):
    total = d.year * 12 + (d.month - 1) + months
    y, m = divmod(total, 12)
    m += 1
    last = calendar.monthrange(y, m)[1]
    return date(y, m, min(d.day, last))


def _emit(lines, out_path):
    text = "\n".join(lines) + "\n"
    if not out_path or out_path == "-":
        sys.stdout.write(text)
        return
    parent = os.path.dirname(os.path.abspath(out_path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    sys.stdout.write("저장: {}\n".format(os.path.abspath(out_path)))


# ---------------------------------------------------------------- stats

def cmd_stats(args):
    xs = _nums(args.values)
    if not xs:
        _fail("값이 하나도 없다")
    xs_sorted = sorted(xs)
    n = len(xs)
    lines = ["입력 {}개 (정렬): {}".format(n, ", ".join(_fmt(x) for x in xs_sorted)), ""]
    lines.append("| 개수 | 최소 | 1사분위 | 중앙값 | 3사분위 | 최대 | 평균 | 합계 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    if n >= 2:
        q = statistics.quantiles(xs, n=4, method="inclusive")
        q1, q3 = q[0], q[2]
    else:
        q1 = q3 = None
    lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
        n, _fmt(xs_sorted[0]), _fmt(q1) if q1 is not None else "계산 불가(값 1개)",
        _fmt(statistics.median(xs)), _fmt(q3) if q3 is not None else "계산 불가(값 1개)",
        _fmt(xs_sorted[-1]), _fmt(statistics.mean(xs)), _fmt(sum(xs))))
    lines.append("")
    lines.append("식: 중앙값 = statistics.median, 사분위 = statistics.quantiles(n=4, method='inclusive')")
    if n < 5:
        lines.append("주의: 값이 {}개뿐이라 사분위는 참고만 한다.".format(n))
    _emit(lines, args.out)
    return EXIT_OK


# ---------------------------------------------------------------- change

def _change_row(old, new, percent=False):
    diff = new - old
    if old == 0:
        rate = "계산 불가(직전 값 0)"
    else:
        rate = "{:+.1f}%".format(diff / abs(old) * 100.0)
    text = _fmt(diff) if diff < 0 else "+" + _fmt(diff)
    if percent:
        text += "%p"
    return text, rate


def cmd_change(args):
    old, new = _nums([args.old, args.new])
    diff, rate = _change_row(old, new, "%" in args.old or "%" in args.new)
    lines = [
        "| 직전 값 | 이번 값 | 차이 | 증감률 |",
        "|---|---|---|---|",
        "| {} | {} | {} | {} |".format(_fmt(old), _fmt(new), diff, rate),
        "",
        "식: 차이 = 이번 - 직전, 증감률 = (이번 - 직전) / |직전| × 100. % 값의 차이는 %p(퍼센트포인트)",
    ]
    _emit(lines, args.out)
    return EXIT_OK


# ---------------------------------------------------------------- position

def cmd_position(args):
    x = _nums([args.value])[0]
    xs = _nums(args.values)
    if not xs:
        _fail("비교할 값 묶음이 비어 있다")
    below = sum(1 for v in xs if v < x)
    same = sum(1 for v in xs if v == x)
    above = sum(1 for v in xs if v > x)
    n = len(xs)
    pct = (below + 0.5 * same) / n * 100.0
    med = statistics.median(xs)
    lines = [
        "대상 값: {} / 묶음 {}개: {}".format(_fmt(x), n, ", ".join(_fmt(v) for v in sorted(xs))),
        "",
        "| 아래 | 같음 | 위 | 백분위 순위 | 묶음 중앙값 | 중앙값 대비 |",
        "|---|---|---|---|---|---|",
        "| {} | {} | {} | {:.1f} | {} | {} |".format(
            below, same, above, pct, _fmt(med),
            "위" if x > med else ("같음" if x == med else "아래")),
        "",
        "식: 백분위 순위 = (아래 개수 + 0.5 × 같은 개수) / 묶음 개수 × 100",
    ]
    _emit(lines, args.out)
    return EXIT_OK


# ---------------------------------------------------------------- window / next

def cmd_window(args):
    today = _day(args.today, "--today") if args.today else date.today()
    lines = ["| 범위 | 시작일 | 끝일 | 연월 표기 |", "|---|---|---|---|"]
    for m in args.months:
        if m < 1 or m > 240:
            _fail("--months 는 1~240 사이여야 한다: {}".format(m))
        start = _add_months(today, -m)
        lines.append("| 최근 {}개월 | {} | {} | {} ~ {} |".format(
            m, start.isoformat(), today.isoformat(), start.strftime("%Y-%m"), today.strftime("%Y-%m")))
    lines.append("")
    lines.append("기준일: {} ({})".format(today.isoformat(), "--today 로 받음" if args.today else "시스템 날짜"))
    _emit(lines, args.out)
    return EXIT_OK


_INTERVALS = {"monthly": ("m", 1), "quarterly": ("m", 3), "semiannual": ("m", 6),
              "half-yearly": ("m", 6), "yearly": ("m", 12), "annual": ("m", 12)}


def _parse_interval(text):
    t = text.strip().lower()
    if t in _INTERVALS:
        return _INTERVALS[t]
    m = re.fullmatch(r"(\d+)\s*([dwm])", t)
    if not m:
        _fail("주기 표기를 읽을 수 없다: {} (monthly, quarterly, semiannual, yearly, 또는 14d·2w·3m)".format(text))
    n = int(m.group(1))
    if n < 1 or n > 3650:
        _fail("주기 값이 너무 크거나 작다: {}".format(text))
    return m.group(2), n


def cmd_next(args):
    base = _day(args.base, "--from") if args.base else date.today()
    lines = ["| 기준일 | 주기 | 다음 날짜 |", "|---|---|---|"]
    for spec in args.interval:
        unit, n = _parse_interval(spec)
        if unit == "d":
            nxt = base + timedelta(days=n)
        elif unit == "w":
            nxt = base + timedelta(weeks=n)
        else:
            nxt = _add_months(base, n)
        lines.append("| {} | {} | {} |".format(base.isoformat(), spec, nxt.isoformat()))
    _emit(lines, args.out)
    return EXIT_OK


# ---------------------------------------------------------------- snapshot

def _split_row(line):
    cells = line.strip()
    if cells.startswith("|"):
        cells = cells[1:]
    if cells.endswith("|"):
        cells = cells[:-1]
    return [c.strip() for c in cells.split("|")]


def _read_snapshot(path):
    if not os.path.isfile(path):
        _fail("파일이 없다: {}".format(path))
    if os.path.getsize(path) > MAX_FILE_BYTES:
        _fail("파일이 너무 크다 (상한 {} 바이트): {}".format(MAX_FILE_BYTES, path))
    rows = []
    header = None
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            s = line.strip()
            if not s.startswith("|"):
                header = None
                continue
            cells = _split_row(s)
            if header is None:
                if "지표 ID" in cells:
                    header = cells
                continue
            if all(re.fullmatch(r":?-{2,}:?", c or "--") for c in cells):
                continue
            if len(cells) < len(header):
                cells += [""] * (len(header) - len(cells))
            row = dict(zip(header, cells))
            if row.get("지표 ID", "").startswith("MS-"):
                rows.append(row)
    return rows


def _latest(rows):
    """ID 별 (가장 늦은 줄, 숫자 값이 있는 가장 늦은 줄, 전체 줄 수, 숫자 줄 수)."""
    by_id = {}
    by_id_num = {}
    count = {}
    count_num = {}
    for r in rows:
        rid = r["지표 ID"]
        count[rid] = count.get(rid, 0) + 1
        prev = by_id.get(rid)
        if prev is None or r.get("조회일", "") >= prev.get("조회일", ""):
            by_id[rid] = r
        if _num(r.get("값", "")) is not None:
            count_num[rid] = count_num.get(rid, 0) + 1
            prev = by_id_num.get(rid)
            if prev is None or r.get("조회일", "") >= prev.get("조회일", ""):
                by_id_num[rid] = r
    return by_id, by_id_num, count, count_num


def cmd_snapshot(args):
    rows = _read_snapshot(args.file)
    if not rows:
        _fail("'지표 ID' 칸이 있는 표에서 MS- 로 시작하는 줄을 찾지 못했다: {}".format(args.file))
    latest, latest_num, count, count_num = _latest(rows)
    lines = []
    if not args.new:
        lines.append("| 지표 ID | 게임 | 지표 | 가장 늦은 값 | 조회일 | 기록 수 (숫자 값) | 마지막 숫자 값 (조회일) | 출처 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for rid in sorted(latest):
            r = latest[rid]
            rn = latest_num.get(rid)
            last_num = "{} ({})".format(rn.get("값", ""), rn.get("조회일", "")) if rn else "없음"
            lines.append("| {} | {} | {} | {} | {} | {} ({}) | {} | {} |".format(
                rid, r.get("게임", ""), r.get("지표", ""), r.get("값", ""), r.get("조회일", ""),
                count[rid], count_num.get(rid, 0), last_num, r.get("출처", "")))
        lines.append("")
        lines.append("숫자 값 기록이 2 이상인 지표만 두 시점 비교에 쓸 수 있다.")
        _emit(lines, args.out)
        return EXIT_OK

    lines.append("| 지표 ID | 게임 | 지표 | 직전 값 (조회일) | 이번 값 | 차이 | 증감률 | 메모 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for item in args.new:
        if "=" not in item:
            _fail("--new 는 ID=값 형식이어야 한다: {}".format(item))
        rid, val = item.split("=", 1)
        rid = rid.strip()
        new = _num(val)
        r_any = latest.get(rid)
        if r_any is None:
            lines.append("| {} | - | - | 없음 | {} | 첫 기록 | - | 기록에 없는 ID |".format(rid, val))
            continue
        r = latest_num.get(rid)
        memo = ""
        if r is not None and r is not r_any:
            memo = "가장 늦은 줄({}, {})이 숫자가 아니라 그 전 숫자 값과 비교".format(
                r_any.get("값", ""), r_any.get("조회일", ""))
        if r is None or new is None:
            why = "이번 값이 숫자가 아니라 비교 안 함" if new is None else "숫자 값 기록이 없어 비교 안 함"
            lines.append("| {} | {} | {} | {} ({}) | {} | - | - | {} |".format(
                rid, r_any.get("게임", ""), r_any.get("지표", ""), r_any.get("값", ""),
                r_any.get("조회일", ""), val, why))
            continue
        old = _num(r.get("값", ""))
        diff, rate = _change_row(old, new, "%" in r.get("값", "") or "%" in val)
        lines.append("| {} | {} | {} | {} ({}) | {} | {} | {} | {} |".format(
            rid, r.get("게임", ""), r.get("지표", ""), r.get("값", ""), r.get("조회일", ""),
            _fmt(new), diff, rate, memo))
    lines.append("")
    lines.append("식: 차이 = 이번 - 직전, 증감률 = (이번 - 직전) / |직전| × 100. 직전 값은 같은 ID 에서 숫자 값이 있는 가장 늦은 조회일 줄.")
    lines.append("같은 ID 는 같은 정의·같은 출처라는 전제다. 출처나 정의가 바뀌었으면 이 표의 비교를 쓰지 않는다.")
    _emit(lines, args.out)
    return EXIT_OK


# ---------------------------------------------------------------- main

def build_parser():
    p = argparse.ArgumentParser(
        prog="market_calc.py",
        description="시장 동향 고문의 계산 도구. 중앙값·증감률·위치·날짜 범위를 계산하고 식을 함께 출력한다.",
        epilog="값에서 천 단위 쉼표, 통화 기호($ € £ ¥ ₩), % 는 지우고 읽는다. % 값의 차이는 %p(퍼센트포인트)로 표시한다. 'k', '만' 같은 단위는 읽지 않는다. "
               "음수 값이 있으면 하위 명령 뒤에 -- 를 넣는다. 예: market_calc.py change -- -5 10. "
               "셸에서 값은 작은따옴표로 감싼다. 예: '$29.99' (감싸지 않으면 셸이 $2 를 변수로 읽어 9.99 로 바뀐다)",
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--out", help="결과를 저장할 경로. 없으면 표준 출력")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("stats", parents=[common], help="개수·최소·사분위·중앙값·최대·평균·합계")
    s.add_argument("values", nargs="+", help="숫자 값들")

    c = sub.add_parser("change", parents=[common], help="직전 값과 이번 값의 차이와 증감률")
    c.add_argument("old", help="직전 값")
    c.add_argument("new", help="이번 값")

    po = sub.add_parser("position", parents=[common], help="한 값이 값 묶음 안에서 놓이는 위치")
    po.add_argument("value", help="위치를 볼 값 (예: 우리 예상 가격)")
    po.add_argument("values", nargs="+", help="비교할 값 묶음 (예: 직접 경쟁작 가격들)")

    w = sub.add_parser("window", parents=[common], help="오늘부터 거꾸로 N개월 범위")
    w.add_argument("--months", type=int, nargs="+", default=[24, 12], help="개월 수 (기본 24 12)")
    w.add_argument("--today", help="기준일 YYYY-MM-DD (기본: 시스템 날짜)")

    n = sub.add_parser("next", parents=[common], help="기준일에서 주기만큼 지난 날짜")
    n.add_argument("--interval", nargs="+", default=["quarterly"],
                   help="주기. monthly, quarterly, semiannual, yearly, 또는 14d·2w·3m (기본 quarterly)")
    n.add_argument("--from", dest="base", help="기준일 YYYY-MM-DD (기본: 시스템 날짜)")

    sn = sub.add_parser("snapshot", parents=[common], help="market-snapshot.md 의 최근 값 보기, 이번 값과 비교")
    sn.add_argument("file", help="market-snapshot.md 경로")
    sn.add_argument("--new", nargs="*", help="이번 값. ID=값 형식으로 여러 개. 예: --new 'MS-001=1520' 'MS-004=88.1%%'")
    return p


def main(argv=None):
    _reconfigure_stdout()
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {"stats": cmd_stats, "change": cmd_change, "position": cmd_position,
                "window": cmd_window, "next": cmd_next, "snapshot": cmd_snapshot}
    if args.cmd not in handlers:
        parser.print_help()
        return EXIT_USAGE
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
