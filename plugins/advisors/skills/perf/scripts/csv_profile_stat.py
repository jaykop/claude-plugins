#!/usr/bin/env python3
"""언리얼 CSV 프로파일러 결과 파일을 집계한다.

읽기만 한다. 결과는 --out 으로 받은 경로에만 쓰고, 없으면 표준 출력으로 낸다.

파일 형식(엔진 버전에 따라 조금씩 다르므로 아래를 모두 견딘다):
  - 첫 줄은 통계 이름 머리 행이다. 이벤트 이름처럼 글자가 든 열이 앞이나 뒤에 있을 수 있다(숫자가 없는 열은 뺀다).
  - 그 뒤로 프레임마다 한 행이 온다. 기록 도중 새 통계가 생기면 앞쪽 행은 열이 모자랄 수 있다.
  - 끝에 머리 행이 한 번 더 붙을 수 있다. 이때는 이 행이 열을 모두 담고 있으므로 이 행을 쓴다.
  - 맨 끝에 '[키],값,[키],값,...' 꼴의 메타데이터 행이 붙을 수 있다.

하위 명령:
  list     파일의 통계 이름(열 이름)만 출력한다. --stats 에 넣을 이름을 고를 때 먼저 쓴다.
  summary  통계별 평균·p50·p95·p99·최대·예산 초과 프레임 수를 낸다. 파일을 여러 개 주면
           파일별 값과 함께 지표별 중앙값과 흩어짐(최대-최소)을 낸다. 하위 명령을 생략하면 summary 다.
  compare  두 회차의 같은 통계를 비교한다. 'compare a.csv b.csv' 또는
           'compare --a a1.csv a2.csv --b b1.csv b2.csv' (반복 측정 파일 여러 개).
"""

import argparse
import csv
import fnmatch
import gzip
import json
import math
import os
import sys
import time
from array import array

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 사람이나 장치를 가리키는 메타데이터는 출력하지 않는다.
# 엔진은 메타데이터 키를 소문자로 바꿔 쓰는 경우가 있으므로 키 비교는 모두 소문자로 한다.
HIDDEN_META = {"loginid", "devicetag"}
# 명령줄은 경로가 섞이므로 --show-commandline 을 줄 때만 낸다.
COMMANDLINE_KEY = "commandline"

METRICS = ["mean", "p50", "p95", "p99", "max"]
METRIC_LABEL = {
    "n": "표본 수",
    "mean": "평균",
    "p50": "p50",
    "p95": "p95",
    "p99": "p99",
    "max": "최대",
    "over_budget": "예산 초과 프레임",
    "hitches": "히치 프레임",
}


class ScriptError(Exception):
    pass


class Limits:
    """행 수와 시간 상한."""

    def __init__(self, max_rows, seconds):
        self.max_rows = max_rows
        self.deadline = time.monotonic() + seconds
        self.hit = None

    def check(self, rows_read):
        """읽기를 계속해도 되면 True. 상한에 걸리면 이유를 남기고 False."""
        if rows_read > self.max_rows:
            self.hit = "행 상한({0}행)".format(self.max_rows)
            return False
        if rows_read % 2000 == 0 and time.monotonic() > self.deadline:
            self.hit = "시간 초과"
            return False
        return True


def to_float(cell):
    cell = cell.strip()
    if not cell:
        return None
    try:
        v = float(cell)
    except ValueError:
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v


def open_text(path):
    if not os.path.isfile(path):
        raise ScriptError("파일 없음: {0}".format(path))
    if path.lower().endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="")
    with open(path, "rb") as f:
        head = f.read(4096)
    if b"\x00" in head or path.lower().endswith(".bin"):
        raise ScriptError(
            "이진 형식으로 보임: {0} — 텍스트 CSV 로 바꾼 뒤 다시 실행한다 "
            "(변환 도구 이름은 대상 엔진에서 확인 필요)".format(path)
        )
    return open(path, "r", encoding="utf-8-sig", errors="replace", newline="")


def is_header_like(row):
    cells = [c.strip() for c in row if c.strip()]
    if len(cells) < 2:
        return False
    return all(to_float(c) is None for c in cells)


def parse_metadata(row, show_commandline):
    meta = {}
    i = 0
    while i < len(row):
        key = row[i].strip()
        if key.startswith("[") and key.endswith("]"):
            name = key[1:-1]
            if name.lower() == COMMANDLINE_KEY:
                # 명령줄은 늘 마지막이고 쉼표가 섞일 수 있으므로 나머지를 다시 잇는다.
                value = ",".join(row[i + 1:]).strip()
                if show_commandline:
                    meta[name] = value
                break
            value = row[i + 1].strip() if i + 1 < len(row) else ""
            if name.lower() not in HIDDEN_META:
                meta[name] = value
            i += 2
        else:
            i += 1
    return meta


def classify_rows(path, limits):
    """1차 읽기: 머리 행, 데이터 행 수, 메타데이터 행 위치를 정한다."""
    header = None
    final_header = None
    data_rows = 0
    meta_row = None
    rows_read = 0
    with open_text(path) as f:
        reader = csv.reader(f)
        for row in reader:
            rows_read += 1
            if not limits.check(rows_read):
                break
            if header is None:
                if not row:
                    continue
                if not is_header_like(row):
                    raise ScriptError("첫 줄이 통계 이름 머리 행이 아님: {0}".format(path))
                header = [c.strip() for c in row]
                continue
            if not row or not any(c.strip() for c in row):
                continue
            if row[0].strip().startswith("["):
                meta_row = row
                break
            if is_header_like(row):
                cells = [c.strip() for c in row]
                if len(cells) >= len(header) and cells[: len(header)] == header:
                    final_header = cells
                continue
            data_rows += 1
    if header is None:
        raise ScriptError("빈 파일: {0}".format(path))
    return header, final_header, data_rows, meta_row


def select_columns(names, patterns):
    wanted = []
    for idx, name in enumerate(names):
        if not name:
            continue
        if patterns and not any(fnmatch.fnmatchcase(name, p) for p in patterns):
            continue
        wanted.append(idx)
    return wanted


def load_profile(path, patterns, skip_frames, limits, show_commandline):
    header, final_header, data_rows, meta_row = classify_rows(path, limits)
    names = final_header if final_header else header
    wanted = select_columns(names, patterns)
    values = {idx: array("d") for idx in wanted}
    bad_cells = {idx: 0 for idx in wanted}
    used_rows = 0
    seen_data = 0
    rows_read = 0
    long_rows = 0
    started = False
    with open_text(path) as f:
        reader = csv.reader(f)
        for row in reader:
            rows_read += 1
            if not limits.check(rows_read):
                break
            if not started:
                if row and is_header_like(row):
                    started = True
                continue
            if not row or not any(c.strip() for c in row):
                continue
            if row[0].strip().startswith("["):
                break
            if is_header_like(row):
                continue
            seen_data += 1
            if len(row) > len(names):
                long_rows += 1
            if seen_data <= skip_frames:
                continue
            used_rows += 1
            for idx in wanted:
                if idx >= len(row):
                    continue
                v = to_float(row[idx])
                if v is None:
                    bad_cells[idx] += 1
                else:
                    values[idx].append(v)
    numeric = {}
    for idx in wanted:
        if len(values[idx]) > 0:
            numeric[names[idx]] = values[idx]
    text_columns = [names[idx] for idx in wanted if len(values[idx]) == 0]
    return {
        "path": path,
        "header_source": "끝에 다시 적힌 머리 행" if final_header else "첫 줄",
        "extra_columns_in_final_header": (len(final_header) - len(header)) if final_header else 0,
        "data_rows": data_rows,
        "used_rows": used_rows,
        "skipped_frames": min(skip_frames, data_rows),
        "metadata": parse_metadata(meta_row, show_commandline) if meta_row else {},
        "values": numeric,
        "text_columns": text_columns,
        "bad_cells": {names[idx]: n for idx, n in bad_cells.items() if n and len(values[idx]) > 0},
        "rows_longer_than_header": long_rows,
        "limit_hit": limits.hit,
    }


def percentile(sorted_vals, q):
    """정렬된 값에서 선형 보간으로 백분위를 구한다 (q 는 0~100)."""
    n = len(sorted_vals)
    if n == 0:
        return None
    if n == 1:
        return sorted_vals[0]
    pos = (n - 1) * q / 100.0
    lo = int(math.floor(pos))
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac


def stat_metrics(vals, budget, hitch):
    s = sorted(vals)
    out = {
        "n": len(s),
        "mean": sum(s) / len(s),
        "p50": percentile(s, 50),
        "p95": percentile(s, 95),
        "p99": percentile(s, 99),
        "max": s[-1],
    }
    if budget is not None:
        out["over_budget"] = sum(1 for v in s if v > budget)
    if hitch is not None:
        out["hitches"] = sum(1 for v in s if v > hitch)
    return out


def median(vals):
    s = sorted(vals)
    n = len(s)
    if n == 0:
        return None
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def fmt(v, digits=3):
    if v is None:
        return "-"
    if isinstance(v, int):
        return str(v)
    if abs(v - round(v)) < 1e-9 and abs(v) >= 1000:
        return str(int(round(v)))
    return "{0:.{1}f}".format(v, digits)


def metric_keys(budget, hitch):
    keys = list(METRICS)
    if budget is not None:
        keys.append("over_budget")
    if hitch is not None:
        keys.append("hitches")
    return keys


def run_metrics(profile, budget, hitch):
    return {name: stat_metrics(vals, budget, hitch) for name, vals in profile["values"].items()}


def aggregate_runs(per_run, keys):
    """파일(반복 측정)마다의 지표에서 지표별 중앙값과 흩어짐(최대-최소)을 낸다."""
    names = []
    for m in per_run:
        for name in m:
            if name not in names:
                names.append(name)
    agg = {}
    for name in names:
        present = [m[name] for m in per_run if name in m]
        entry = {"runs": len(present)}
        for k in keys:
            vals = [p[k] for p in present if p.get(k) is not None]
            entry[k] = median(vals) if vals else None
            entry[k + "_spread"] = (max(vals) - min(vals)) if len(vals) >= 2 else None
        agg[name] = entry
    return agg


def sort_names(names, metrics, sort_key):
    if sort_key == "name":
        return sorted(names)
    return sorted(names, key=lambda n: (metrics[n].get(sort_key) is None, -(metrics[n].get(sort_key) or 0)))


def command_text():
    return "python " + " ".join(
        ('"{0}"'.format(a) if (" " in a or not a) else a) for a in [os.path.basename(sys.argv[0])] + sys.argv[1:]
    )


def file_info_rows(profile):
    rows = [
        ("파일", profile["path"]),
        ("데이터 행", str(profile["data_rows"])),
        ("집계에 쓴 행", "{0} (앞 {1}행 제외)".format(profile["used_rows"], profile["skipped_frames"])),
        ("머리 행", profile["header_source"]
         + (" (첫 줄보다 열 {0}개 많음)".format(profile["extra_columns_in_final_header"])
            if profile["extra_columns_in_final_header"] else "")),
    ]
    if profile["metadata"]:
        rows.append(("메타데이터", ", ".join("{0}={1}".format(k, v) for k, v in profile["metadata"].items())))
    else:
        rows.append(("메타데이터", "없음"))
    if profile["text_columns"]:
        rows.append(("숫자가 없는 열(제외)", ", ".join(profile["text_columns"][:10])
                     + (" 외 {0}개".format(len(profile["text_columns"]) - 10) if len(profile["text_columns"]) > 10 else "")))
    if profile["bad_cells"]:
        rows.append(("숫자 아닌 칸을 건너뛴 통계", ", ".join(
            "{0}({1})".format(k, v) for k, v in list(profile["bad_cells"].items())[:10])))
    if profile["rows_longer_than_header"]:
        rows.append(("머리 행보다 칸이 많은 행", "{0}행 — 이름이 없는 칸은 버렸다".format(profile["rows_longer_than_header"])))
    if profile["limit_hit"]:
        rows.append(("집계 중단", "{0} — 앞부분만 집계함. 전체 결과로 쓰지 않는다".format(profile["limit_hit"])))
    return rows


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(lines)


def cmd_list(args):
    out = []
    data = []
    for path in args.files:
        # 상한은 파일마다 새로 센다. 앞 파일의 중단 표시가 뒤 파일에 남지 않게 한다.
        limits = Limits(args.max_rows, args.timeout)
        header, final_header, data_rows, _ = classify_rows(path, limits)
        names = final_header if final_header else header
        names = [n for n in names if n]
        if args.stats:
            names = [n for n in names if any(fnmatch.fnmatchcase(n, p) for p in args.stats)]
        data.append({"path": path, "data_rows": data_rows, "stats": names, "limit_hit": limits.hit})
        out.append("## 통계 이름 — {0}\n".format(path))
        out.append("데이터 행 {0}, 열 {1}개{2}\n".format(
            data_rows, len(names), " — 읽기 중단: " + limits.hit if limits.hit else ""))
        out.append("\n".join("- " + n for n in names))
        out.append("")
    if args.format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    return "\n".join(out)


def cmd_summary(args):
    keys = metric_keys(args.budget_ms, args.hitch_ms)
    profiles, per_run = [], []
    for path in args.files:
        limits = Limits(args.max_rows, args.timeout)
        p = load_profile(path, args.stats, args.skip_frames, limits, args.show_commandline)
        profiles.append(p)
        per_run.append(run_metrics(p, args.budget_ms, args.hitch_ms))

    if args.format == "json":
        result = {
            "command": command_text(),
            "percentile_method": "linear",
            "budget_ms": args.budget_ms,
            "hitch_ms": args.hitch_ms,
            "files": [{k: v for k, v in p.items() if k != "values"} for p in profiles],
            "per_file": per_run,
        }
        if len(profiles) > 1:
            result["aggregate"] = aggregate_runs(per_run, keys)
        return json.dumps(result, ensure_ascii=False, indent=2)

    out = ["## CSV 프로파일러 집계\n"]
    out.append(md_table(["항목", "값"], [
        ("명령", "`" + command_text() + "`"),
        ("백분위 계산", "값을 정렬한 뒤 선형 보간"),
        ("예산", "{0} ms 초과 프레임을 셈 (ms 단위 통계에만 뜻이 있음)".format(fmt(args.budget_ms)) if args.budget_ms is not None else "주지 않음"),
        ("히치 기준", "{0} ms 초과 프레임을 셈 (프레임 시간 통계에서 읽음)".format(fmt(args.hitch_ms)) if args.hitch_ms is not None else "주지 않음"),
        ("통계 필터", ", ".join(args.stats) if args.stats else "없음(모든 숫자 열)"),
    ]))
    out.append("")
    headers = ["통계"] + [METRIC_LABEL[k] for k in ["n"] + keys]
    for p, m in zip(profiles, per_run):
        out.append("### 파일: {0}\n".format(os.path.basename(p["path"])))
        out.append(md_table(["항목", "값"], file_info_rows(p)))
        out.append("")
        if not m:
            out.append("집계할 숫자 열이 없음. 'list' 로 통계 이름을 확인한다.\n")
            continue
        names = sort_names(list(m.keys()), m, args.sort)
        if args.top:
            names = names[: args.top]
        out.append(md_table(headers, [[n] + [fmt(m[n].get(k)) for k in ["n"] + keys] for n in names]))
        out.append("")

    if len(profiles) > 1:
        agg = aggregate_runs(per_run, keys)
        out.append("### 반복 측정 묶음 ({0}개 파일): 지표별 중앙값과 흩어짐(최대-최소)\n".format(len(profiles)))
        hdr = ["통계", "파일 수"]
        for k in keys:
            hdr += [METRIC_LABEL[k] + " 중앙값", METRIC_LABEL[k] + " 흩어짐"]
        names = sort_names(list(agg.keys()), agg, args.sort)
        if args.top:
            names = names[: args.top]
        rows = []
        for n in names:
            row = [n, agg[n]["runs"]]
            for k in keys:
                row += [fmt(agg[n][k]), fmt(agg[n][k + "_spread"])]
            rows.append(row)
        out.append(md_table(hdr, rows))
        out.append("")
        meta_diff = metadata_differences([p["metadata"] for p in profiles])
        if meta_diff:
            out.append("### 파일끼리 다른 메타데이터 (같은 조건의 반복 측정이 아닐 수 있음)\n")
            out.append(md_table(["키"] + [os.path.basename(p["path"]) for p in profiles], meta_diff))
            out.append("")
    return "\n".join(out)


def metadata_differences(metas):
    keys = []
    for m in metas:
        for k in m:
            if k not in keys:
                keys.append(k)
    rows = []
    for k in keys:
        vals = [m.get(k, "(없음)") for m in metas]
        if len(set(vals)) > 1:
            rows.append([k] + vals)
    return rows


def cmd_compare(args):
    if args.a or args.b:
        if not (args.a and args.b) or args.files:
            raise ScriptError("--a 와 --b 를 함께 주거나, 파일 두 개만 순서대로 준다")
        files_a, files_b = args.a, args.b
    else:
        if len(args.files) != 2:
            raise ScriptError("비교할 파일 두 개가 필요하다: compare <a.csv> <b.csv>")
        files_a, files_b = [args.files[0]], [args.files[1]]

    keys = metric_keys(args.budget_ms, args.hitch_ms)
    sides = {}
    for label, files in (("A", files_a), ("B", files_b)):
        profiles, per_run = [], []
        for path in files:
            limits = Limits(args.max_rows, args.timeout)
            p = load_profile(path, args.stats, args.skip_frames, limits, args.show_commandline)
            profiles.append(p)
            per_run.append(run_metrics(p, args.budget_ms, args.hitch_ms))
        sides[label] = {"profiles": profiles, "agg": aggregate_runs(per_run, keys)}

    agg_a, agg_b = sides["A"]["agg"], sides["B"]["agg"]
    common = [n for n in agg_a if n in agg_b]
    only_a = sorted(n for n in agg_a if n not in agg_b)
    only_b = sorted(n for n in agg_b if n not in agg_a)

    rows, json_rows = [], []
    for n in sorted(common):
        for k in keys:
            va, vb = agg_a[n][k], agg_b[n][k]
            sa, sb = agg_a[n][k + "_spread"], agg_b[n][k + "_spread"]
            diff = (vb - va) if (va is not None and vb is not None) else None
            if diff is None or va is None or abs(va) < 1e-12:
                rate = None
            else:
                rate = diff / va * 100.0
            spreads = [s for s in (sa, sb) if s is not None]
            if diff is None:
                beyond = "계산 불가"
            elif not spreads:
                beyond = "판정 재료 없음(반복 1회)"
            else:
                beyond = "예" if abs(diff) > max(spreads) else "아니오"
            rows.append([n, METRIC_LABEL[k], fmt(va), fmt(sa), fmt(vb), fmt(sb), fmt(diff),
                         ("{0:+.1f}%".format(rate) if rate is not None else "계산 불가"), beyond])
            json_rows.append({"stat": n, "metric": k, "a": va, "a_spread": sa, "b": vb, "b_spread": sb,
                              "diff": diff, "change_pct": rate, "diff_exceeds_spread": beyond})

    meta_a = sides["A"]["profiles"][0]["metadata"]
    meta_b = sides["B"]["profiles"][0]["metadata"]
    meta_diff = metadata_differences([meta_a, meta_b])
    inner_diff = {
        label: metadata_differences([p["metadata"] for p in sides[label]["profiles"]])
        for label in ("A", "B") if len(sides[label]["profiles"]) > 1
    }

    if args.format == "json":
        return json.dumps({
            "command": command_text(),
            "files_a": files_a, "files_b": files_b,
            "budget_ms": args.budget_ms, "hitch_ms": args.hitch_ms,
            "rows": json_rows, "only_in_a": only_a, "only_in_b": only_b,
            "metadata_differences": meta_diff, "metadata_differences_within_side": inner_diff,
            "limit_hits": [p["limit_hit"] for s in sides.values() for p in s["profiles"] if p["limit_hit"]],
        }, ensure_ascii=False, indent=2)

    out = ["## CSV 프로파일러 비교\n"]
    out.append(md_table(["항목", "값"], [
        ("명령", "`" + command_text() + "`"),
        ("A", ", ".join(files_a)),
        ("B", ", ".join(files_b)),
        ("값", "파일이 여럿이면 파일별 지표의 중앙값. 흩어짐은 그 지표의 최대-최소"),
        ("변화", "B − A. 변화율 = (B − A) / A × 100. A 가 0 이면 계산 불가"),
        ("'변화 > 흩어짐'", "변화의 크기가 두 쪽 흩어짐 중 큰 값보다 큰지. 나빠짐 판정은 이것과 최소 변화폭, 측정 조건 일치를 함께 보고 사람이 한다"),
        ("백분위 계산", "값을 정렬한 뒤 선형 보간"),
    ]))
    out.append("")
    hits = [p for s in sides.values() for p in s["profiles"] if p["limit_hit"]]
    if hits:
        out.append("**집계 중단된 파일이 있음 — 이 비교를 결과로 쓰지 않는다:** "
                   + ", ".join("{0}({1})".format(p["path"], p["limit_hit"]) for p in hits) + "\n")
    if meta_diff:
        out.append("### A 와 B 의 메타데이터 차이 (측정 조건이 다를 수 있음)\n")
        out.append(md_table(["키", "A (첫 파일)", "B (첫 파일)"], meta_diff))
        out.append("")
    for label, diff in inner_diff.items():
        if diff:
            out.append("### {0} 묶음 안에서 다른 메타데이터\n".format(label))
            out.append(md_table(["키"] + [os.path.basename(p["path"]) for p in sides[label]["profiles"]], diff))
            out.append("")
    out.append("### 통계 비교\n")
    if rows:
        out.append(md_table(["통계", "지표", "A", "A 흩어짐", "B", "B 흩어짐", "변화", "변화율", "변화 > 흩어짐"], rows))
    else:
        out.append("두 쪽에 함께 있는 통계가 없음.")
    out.append("")
    if only_a or only_b:
        out.append("### 한쪽에만 있는 통계\n")
        out.append("- A 에만: " + (", ".join(only_a) if only_a else "없음"))
        out.append("- B 에만: " + (", ".join(only_b) if only_b else "없음"))
        out.append("")
    return "\n".join(out)


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--stats", action="append", metavar="이름들",
                        help="집계할 통계 이름. 쉼표로 여러 개, 와일드카드(*, ?) 가능. 여러 번 줄 수 있다. "
                             "예: --stats \"FrameTime,GameThreadTime\" --stats \"Exclusive/GameThread/*\"")
    common.add_argument("--skip-frames", type=int, default=0, metavar="N",
                        help="앞쪽 데이터 행 N개를 버린다(워밍업 구간 제외). 기본 0")
    common.add_argument("--budget-ms", type=float, metavar="MS",
                        help="프레임 시간 예산. 통계마다 이 값을 넘은 프레임 수를 센다(ms 단위 통계에만 뜻이 있다)")
    common.add_argument("--hitch-ms", type=float, metavar="MS",
                        help="히치 기준. 통계마다 이 값을 넘은 프레임 수를 센다")
    common.add_argument("--format", choices=["md", "json"], default="md", help="출력 형식. 기본 md(마크다운 표)")
    common.add_argument("--out", metavar="경로", help="결과를 쓸 파일. 없으면 표준 출력")
    common.add_argument("--max-rows", type=int, default=2000000, metavar="N",
                        help="파일마다 읽을 최대 행 수. 넘으면 '집계 중단'으로 표시한다. 기본 2000000")
    common.add_argument("--timeout", type=float, default=120.0, metavar="초",
                        help="파일마다 읽기 시간 상한(초). 넘으면 '집계 중단(시간 초과)'으로 표시한다. 기본 120")
    common.add_argument("--show-commandline", action="store_true",
                        help="메타데이터의 명령줄도 출력한다(경로가 섞일 수 있어 기본은 숨김)")

    parser = argparse.ArgumentParser(
        description="언리얼 CSV 프로파일러 결과 파일을 집계한다. 하위 명령: list / summary(기본) / compare",
        epilog="예: python csv_profile_stat.py list run1.csv\n"
               "    python csv_profile_stat.py summary run1.csv run2.csv run3.csv --stats \"FrameTime,GameThreadTime\" --budget-ms 16.6 --skip-frames 300\n"
               "    python csv_profile_stat.py compare before.csv after.csv --stats FrameTime\n"
               "    python csv_profile_stat.py compare --a b1.csv b2.csv b3.csv --b n1.csv n2.csv n3.csv --stats FrameTime",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")
    p_list = sub.add_parser("list", parents=[common], help="통계 이름만 출력")
    p_list.add_argument("files", nargs="+", metavar="CSV", help="CSV 프로파일러 결과 파일")
    p_sum = sub.add_parser("summary", parents=[common], help="통계별 지표 집계")
    p_sum.add_argument("files", nargs="+", metavar="CSV", help="CSV 파일. 여러 개면 반복 측정으로 보고 중앙값과 흩어짐도 낸다")
    p_sum.add_argument("--sort", choices=["name", "mean", "p95", "p99", "max"], default="name",
                       help="표 정렬 기준. 기본 name")
    p_sum.add_argument("--top", type=int, metavar="N", help="정렬 뒤 위에서 N개만 낸다")
    p_cmp = sub.add_parser("compare", parents=[common], help="두 회차 비교")
    p_cmp.add_argument("files", nargs="*", metavar="CSV", help="비교할 두 파일: A B")
    p_cmp.add_argument("--a", nargs="+", metavar="CSV", help="A 쪽 반복 측정 파일들")
    p_cmp.add_argument("--b", nargs="+", metavar="CSV", help="B 쪽 반복 측정 파일들")
    return parser


def main(argv):
    if argv and argv[0] not in ("list", "summary", "compare", "-h", "--help"):
        argv = ["summary"] + argv
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 2
    if args.skip_frames < 0:
        parser.error("--skip-frames 는 0 이상이어야 한다")
    if args.stats:
        args.stats = [p.strip() for chunk in args.stats for p in chunk.split(",") if p.strip()]
    try:
        if args.command == "list":
            text = cmd_list(args)
        elif args.command == "summary":
            text = cmd_summary(args)
        else:
            text = cmd_compare(args)
    except ScriptError as e:
        print("오류: {0}".format(e), file=sys.stderr)
        return 2
    except OSError as e:
        print("오류: 파일을 읽지 못함 — {0}".format(e), file=sys.stderr)
        return 2
    if args.out:
        out_dir = os.path.dirname(os.path.abspath(args.out))
        if not os.path.isdir(out_dir):
            print("오류: 출력 폴더가 없음 — {0}".format(out_dir), file=sys.stderr)
            return 2
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
        print("저장함: {0}".format(args.out))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
