#!/usr/bin/env python3
"""기획 영역 하나의 자료 목록을 만든다.

기획 고문(design)의 영역 진단 Step A1 에서 쓴다. 영역 폴더를 훑어
문서 파일을 읽는 순서대로 늘어놓고, 읽을 파일 수 상한을 넘는 것은
'못 읽은 자료'로, 폐기 표시가 있는 것은 '근거에서 뺀 자료'로 나눈다.
문서 머리(앞쪽 몇 줄)에 적힌 개정일도 함께 뽑는다. 머리에 날짜가 없으면
파일 이름에 든 날짜를 '작성일로 보임'으로 읽는다(회의록·플레이테스트 기록처럼
이름에 날짜를 붙이는 문서가 많기 때문). 파일 시스템의 수정 시각은 쓰지 않는다
(동기화 시각과 같아져 의미가 없기 때문).

프로젝트 파일은 읽기만 한다. 결과는 --out 경로에만 쓰고, 없으면 표준 출력으로 낸다.
Python 3.8 이상, 표준 라이브러리만 쓴다.
"""

import argparse
import datetime
import fnmatch
import json
import math
import os
import re
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# 들어가지 않는 폴더 이름. 점으로 시작하는 폴더도 들어가지 않는다.
SKIP_DIR_NAMES = {
    "node_modules", "__pycache__", "Intermediate", "Saved", "Binaries",
    "DerivedDataCache", "obj", "bin",
}

# 2026-03-04, 2026.3.4, 2026/03/04, 2026년 3월 4일
DATE_RE = re.compile(r"(?<!\d)((?:19|20)\d{2})\s*(?:[-./]|년)\s*(\d{1,2})\s*(?:[-./]|월)\s*(\d{1,2})(?!\d)")
# 파일 이름: 위 형식에 더해 2026_03_04, 20260304
NAME_DATE_RES = [
    re.compile(r"(?<!\d)((?:19|20)\d{2})\s*(?:[-./_]|년)\s*(\d{1,2})\s*(?:[-./_]|월)\s*(\d{1,2})(?!\d)"),
    re.compile(r"(?<!\d)((?:19|20)\d{2})(\d{2})(\d{2})(?!\d)"),
]

# 날짜 앞에 오는 이름. 앞쪽 무리일수록 '마지막으로 고친 날'에 가깝다.
LABELS_REVISED = [
    "개정", "갱신", "수정", "업데이트", "변경", "최종",
    "updated", "update", "last modified", "modified", "revised", "revision",
]
LABELS_WRITTEN = ["작성", "기준일", "created", "date", "날짜", "일시"]

FRONT_MATTER_REVISED = {"updated", "last_updated", "lastupdated", "modified", "revised", "revision_date"}
FRONT_MATTER_WRITTEN = {"date", "created"}


def parse_args():
    p = argparse.ArgumentParser(
        description="기획 영역 폴더의 자료 목록을 만든다. 읽을 순서, 상한 초과, 폐기 표시, 문서 머리의 개정일을 정리한다.",
    )
    p.add_argument("roots", nargs="+", help="영역 폴더. 여러 개 줄 수 있다")
    p.add_argument("--base", default=None,
                   help="결과에 경로를 이 폴더 기준 상대 경로로 적는다. 없으면 첫 영역 폴더의 상위 폴더")
    p.add_argument("--exclude", action="append", default=[],
                   help="빼는 폴더·파일 패턴(fnmatch). 이름 한 칸, 기준 폴더 상대 경로, 절대 경로, 또는 경로 끝부분에 맞춘다. 여러 번 줄 수 있다. 예: _archive, */old/*, Design/reference")
    p.add_argument("--include", action="append", default=[],
                   help="이 패턴(fnmatch)에 맞는 파일만 문서로 본다. 영역이 폴더로 나뉘어 있지 않을 때 쓴다. 파일 이름이나 기준 폴더 상대 경로에 맞춘다. 여러 번 줄 수 있다. 예: *전투*, 미션_*")
    p.add_argument("--summary", action="append", default=[],
                   help="요약 문서 패턴(fnmatch). 맞는 파일을 읽는 순서 맨 앞에 둔다. 예: *_summary.md")
    p.add_argument("--deprecated-marker", action="append", default=[],
                   help="폐기 표시 문자열. 파일 이름이나 문서 머리에 있으면 '근거에서 뺀 자료'로 보낸다. 예: [폐기]")
    p.add_argument("--ext", default=".md,.markdown,.txt",
                   help="문서로 볼 확장자, 쉼표로 구분 (기본 .md,.markdown,.txt)")
    p.add_argument("--read-limit", type=int, default=40, help="읽을 파일 수 상한 (기본 40)")
    p.add_argument("--batches", type=int, default=1,
                   help="읽을 파일을 크기가 비슷한 묶음 N개로 나눈다. 분석 작업자를 나눠 부를 때 쓴다. --batch-kb 와 함께 주면 묶음 수의 상한이 된다 (기본 1)")
    p.add_argument("--batch-kb", type=float, default=0,
                   help="읽을 파일 크기 합 N KB 마다 묶음 하나로 묶음 수를 정한다. 0 이면 쓰지 않는다 (기본 0)")
    p.add_argument("--order", choices=["default", "date"], default="default",
                   help="읽는 순서. default = 요약 문서 → 얕은 폴더 → 경로 순, date = 문서 날짜(머리, 없으면 파일 이름의 작성일)가 최근인 것부터(날짜 미상은 맨 뒤)")
    p.add_argument("--max-depth", type=int, default=8, help="들어갈 폴더 깊이 상한 (기본 8)")
    p.add_argument("--max-files", type=int, default=5000, help="훑을 파일 수 상한. 넘으면 멈춘다 (기본 5000)")
    p.add_argument("--time-limit", type=float, default=20.0, help="훑는 시간 상한, 초 (기본 20)")
    p.add_argument("--header-lines", type=int, default=40, help="날짜와 폐기 표시를 찾을 문서 앞쪽 줄 수 (기본 40)")
    p.add_argument("--since", default=None,
                   help="YYYY-MM-DD. 문서 날짜가 이 날짜보다 뒤인지 표시한다. 지난 리포트 이후 바뀐 문서를 고를 때 쓴다. "
                        "작성일(파일 이름의 날짜, '작성' 같은 이름이 붙은 날짜)만 있는 문서가 이 날짜와 같거나 앞이면 "
                        "그 뒤에 고쳤는지 알 수 없으므로 '작성일 이전·같음(수정 여부 모름)'으로 따로 표시한다")
    p.add_argument("--format", choices=["md", "json"], default="md", help="출력 형식 (기본 md)")
    p.add_argument("--out", default=None, help="결과를 쓸 파일 경로. 없으면 표준 출력")
    return p.parse_args()


def norm_date(m):
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        datetime.date(y, mo, d)
    except ValueError:
        return None
    return "%04d-%02d-%02d" % (y, mo, d)


def name_date(filename):
    """파일 이름에 든 날짜. 여러 개면 가장 늦은 것."""
    stem = os.path.splitext(filename)[0]
    found = []
    for rx in NAME_DATE_RES:
        for m in rx.finditer(stem):
            d = norm_date(m)
            if d:
                found.append(d)
    return max(found) if found else None


def read_header(path, n_lines):
    """앞쪽 n 줄을 읽는다. utf-8 이 안 되면 cp949, 그다음 latin-1 로 읽는다."""
    for enc in ("utf-8-sig", "cp949", "latin-1"):
        try:
            lines = []
            with open(path, "r", encoding=enc) as f:
                for i, line in enumerate(f):
                    if i >= n_lines:
                        break
                    lines.append(line.rstrip("\r\n"))
            return lines, None
        except UnicodeDecodeError:
            continue
        except OSError as e:
            return [], "읽기 실패(%s)" % e.__class__.__name__
    return [], "읽기 실패(인코딩)"


def header_info(lines, markers):
    """문서 머리에서 제목, 날짜, 날짜 종류(개정일·작성일), 날짜 근거, 폐기 표시를 뽑는다."""
    title = None
    revised = []   # (날짜, 이름, 줄 번호)
    written = []
    unlabeled = 0
    deprecated_hit = None

    in_fm = bool(lines) and lines[0].strip() == "---"
    for idx, raw in enumerate(lines):
        line_no = idx + 1
        line = raw.strip()
        if in_fm and idx > 0 and line == "---":
            in_fm = False
            continue
        if in_fm and ":" in line:
            key, _, val = line.partition(":")
            k = key.strip().lower()
            m = DATE_RE.search(val)
            if k == "title" and not title:
                title = val.strip().strip('"').strip("'")
            if m and norm_date(m):
                if k in FRONT_MATTER_REVISED:
                    revised.append((norm_date(m), key.strip(), line_no))
                elif k in FRONT_MATTER_WRITTEN:
                    written.append((norm_date(m), key.strip(), line_no))
        if not title and line.startswith("# "):
            title = line[2:].strip()
        for mk in markers:
            if mk and mk.lower() in line.lower() and not deprecated_hit:
                deprecated_hit = "%s (%d행)" % (mk, line_no)
        if in_fm:
            continue
        for m in DATE_RE.finditer(line):
            d = norm_date(m)
            if not d:
                continue
            before = line[:m.start()].lower()[-30:]
            label = None
            for lb in LABELS_REVISED:
                if lb in before:
                    label = ("rev", lb)
                    break
            if not label:
                for lb in LABELS_WRITTEN:
                    if lb in before:
                        label = ("wri", lb)
                        break
            if label and label[0] == "rev":
                revised.append((d, label[1], line_no))
            elif label:
                written.append((d, label[1], line_no))
            else:
                unlabeled += 1

    if revised:
        best = max(revised)
        date, kind, basis = best[0], "개정일", "머리 '%s' %d행" % (best[1], best[2])
    elif written:
        best = max(written)
        date, kind, basis = best[0], "작성일", "머리 '%s' %d행 (작성일로 보임)" % (best[1], best[2])
    else:
        date, kind = None, None
        basis = "날짜 미상" + (" (머리에 이름 없는 날짜 %d개)" % unlabeled if unlabeled else "")
    return title, date, kind, basis, deprecated_hit


def match_any(patterns, rel_posix, name, abs_posix=""):
    for pat in patterns:
        pp = pat.replace("\\", "/").rstrip("/")
        if not pp:
            continue
        if fnmatch.fnmatch(name, pp) or fnmatch.fnmatch(rel_posix, pp):
            return pat
        tail = pp[2:] if pp.startswith("./") else pp
        if abs_posix and (fnmatch.fnmatch(abs_posix, pp) or abs_posix.endswith("/" + tail)):
            return pat
    return None


def split_batches(items, n):
    """순서를 지키면서 크기 합이 비슷하게 n 묶음으로 자른다."""
    if n <= 1 or len(items) <= 1:
        return [items]
    n = min(n, len(items))
    total = sum(max(it["size"], 1) for it in items)
    target = total / float(n)
    batches, cur, acc = [], [], 0
    for i, it in enumerate(items):
        remaining_items = len(items) - i
        remaining_batches = n - len(batches)
        if cur and (acc >= target or remaining_items < remaining_batches) and len(batches) < n - 1:
            batches.append(cur)
            cur, acc = [], 0
        cur.append(it)
        acc += max(it["size"], 1)
    if cur:
        batches.append(cur)
    return batches


def main():
    a = parse_args()
    exts = {e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower()
            for e in a.ext.split(",") if e.strip()}
    roots = [os.path.abspath(r) for r in a.roots]
    base = os.path.abspath(a.base) if a.base else os.path.dirname(roots[0].rstrip("\\/"))

    def rel(p):
        try:
            r = os.path.relpath(p, base)
        except ValueError:
            return p.replace("\\", "/")
        if r.startswith(".."):
            return p.replace("\\", "/")
        return r.replace("\\", "/")

    t0 = time.monotonic()
    status = []           # 검색 상태 문구
    depth_cut = []        # 깊이 상한으로 안 본 폴더
    excluded_dirs = []    # 제외 규칙으로 뺀 폴더
    walk_errors = []
    include_skipped = 0
    docs = []
    other_types = {}
    scanned = 0
    stopped = None

    for root in roots:
        if not os.path.isdir(root):
            status.append("검색 실패(경로 없음): %s" % rel(root))
            continue
        root_depth = root.rstrip("\\/").count(os.sep)

        def onerror(err, _rel=rel):
            walk_errors.append("%s (%s)" % (_rel(getattr(err, "filename", "") or "?"), err.__class__.__name__))

        for dirpath, dirnames, filenames in os.walk(root, topdown=True, onerror=onerror, followlinks=False):
            if time.monotonic() - t0 > a.time_limit:
                stopped = "검색 실패(시간 초과 %g초)" % a.time_limit
                break
            depth = dirpath.rstrip("\\/").count(os.sep) - root_depth
            keep = []
            for d in sorted(dirnames):
                full = os.path.join(dirpath, d)
                r = rel(full)
                if d.startswith(".") or d in SKIP_DIR_NAMES:
                    continue
                pat = match_any(a.exclude, r, d, full.replace("\\", "/"))
                if pat:
                    excluded_dirs.append("%s (규칙 %s)" % (r, pat))
                    continue
                if depth + 1 > a.max_depth:
                    depth_cut.append(r)
                    continue
                keep.append(d)
            dirnames[:] = keep

            for fn in sorted(filenames):
                scanned += 1
                if scanned > a.max_files:
                    stopped = "검색 실패(파일 수 상한 %d)" % a.max_files
                    break
                if time.monotonic() - t0 > a.time_limit:
                    stopped = "검색 실패(시간 초과 %g초)" % a.time_limit
                    break
                full = os.path.join(dirpath, fn)
                r = rel(full)
                ext = os.path.splitext(fn)[1].lower()
                if match_any(a.exclude, r, fn, full.replace("\\", "/")):
                    continue
                if a.include and not match_any(a.include, r, fn):
                    include_skipped += 1
                    continue
                if ext not in exts:
                    key = ext or "(확장자 없음)"
                    other_types[key] = other_types.get(key, 0) + 1
                    continue
                try:
                    size = os.path.getsize(full)
                except OSError:
                    size = -1
                lines, err = read_header(full, a.header_lines)
                title, date, kind, basis, dep = header_info(lines, a.deprecated_marker)
                source = "머리" if date else None
                if not date and not err:
                    nd = name_date(fn)
                    if nd:
                        # 파일 이름의 날짜는 작성일로만 본다. 개정일로 쓰지 않는다.
                        date, kind, source = nd, "작성일", "파일 이름"
                        basis = "파일 이름 날짜 (작성일로 보임)"
                if not dep:
                    for mk in a.deprecated_marker:
                        if mk and mk.lower() in fn.lower():
                            dep = "%s (파일 이름)" % mk
                            break
                docs.append({
                    "path": r,
                    "folder": os.path.dirname(r) or ".",
                    "depth": r.count("/"),
                    "size": size,
                    "title": title,
                    "doc_date": date,
                    "date_kind": kind,
                    "date_source": source,
                    "date_basis": basis if not err else err,
                    "deprecated": dep,
                    "summary": bool(match_any(a.summary, r, fn)),
                })
            if stopped:
                break
        if stopped:
            break

    elapsed = time.monotonic() - t0
    if stopped:
        status.append(stopped)
    if depth_cut:
        status.append("일부만 검색(깊이 상한 %d, 들어가지 않은 폴더 %d개)" % (a.max_depth, len(depth_cut)))
    if walk_errors:
        status.append("일부만 검색(열지 못한 폴더 %d개)" % len(walk_errors))
    if not status:
        status.append("완료")
    partial = any(s.startswith("검색 실패") or s.startswith("일부만 검색") for s in status)

    kept = [d for d in docs if not d["deprecated"]]
    dropped = [d for d in docs if d["deprecated"]]
    if a.order == "date":
        dated = sorted([d for d in kept if d["doc_date"]], key=lambda d: (d["doc_date"], d["path"]), reverse=True)
        undated = sorted([d for d in kept if not d["doc_date"]], key=lambda d: d["path"])
        kept = dated + undated
    else:
        kept.sort(key=lambda d: (0 if d["summary"] else 1, d["depth"], d["path"]))
    selected = kept[: max(a.read_limit, 0)]
    over = kept[max(a.read_limit, 0):]
    n_batches = max(a.batches, 1)
    if a.batch_kb > 0:
        sel_kb = sum(max(d["size"], 0) for d in selected) / 1024.0
        n_batches = max(1, min(n_batches, int(math.ceil(sel_kb / a.batch_kb)) if sel_kb > 0 else 1))
    batches = split_batches(selected, n_batches)
    for bi, b in enumerate(batches, 1):
        for d in b:
            d["batch"] = bi

    if a.since:
        for d in docs:
            if not d["doc_date"]:
                d["since"] = "날짜 미상"
            elif d["doc_date"] > a.since:
                d["since"] = "이후"
            elif d["date_kind"] == "개정일":
                d["since"] = "이전·같음"
            else:
                # 작성일만 아는 문서는 그 뒤에 고쳤을 수 있다.
                d["since"] = "작성일 이전·같음(수정 여부 모름)"

    selected_ids = set(id(d) for d in selected)
    folders = {}
    for d in docs:
        f = folders.setdefault(d["folder"], {"docs": 0, "bytes": 0, "selected": 0, "deprecated": 0})
        f["docs"] += 1
        f["bytes"] += max(d["size"], 0)
        if id(d) in selected_ids:
            f["selected"] += 1
        if d["deprecated"]:
            f["deprecated"] += 1

    result = {
        "roots": [rel(r) for r in roots],
        "base": base.replace("\\", "/"),
        "status": status,
        "counts_are_minimum": partial,
        "limits": {"max_depth": a.max_depth, "max_files": a.max_files, "time_limit_s": a.time_limit,
                   "read_limit": a.read_limit, "header_lines": a.header_lines},
        "elapsed_s": round(elapsed, 2),
        "scanned_files": min(scanned, a.max_files),
        "doc_count": len(docs),
        "selected_count": len(selected),
        "over_limit_count": len(over),
        "deprecated_count": len(dropped),
        "selected_bytes": sum(max(d["size"], 0) for d in selected),
        "folders": folders,
        "selected": selected,
        "over_limit": over,
        "deprecated": dropped,
        "other_types": other_types,
        "include": a.include,
        "include_skipped": include_skipped,
        "depth_cut_dirs": depth_cut,
        "excluded_dirs": excluded_dirs,
        "walk_errors": walk_errors,
        "since": a.since,
        "order": a.order,
        "batches": len(batches) if selected else 0,
    }

    out = json.dumps(result, ensure_ascii=False, indent=1) if a.format == "json" else render_md(result)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
        print("저장함: %s" % a.out)
    else:
        print(out)


def kb(n):
    return "?" if n < 0 else "%.1f" % (n / 1024.0)


def cell(s, limit=60):
    """표 칸에 넣을 글자. 칸 구분자를 바꾸고, 너무 길면 자른다."""
    if not s:
        return ""
    s = str(s).replace("|", "/").replace("\n", " ")
    return s if len(s) <= limit else s[: limit - 1] + "…"


def render_md(r):
    L = []
    L.append("# 영역 자료 목록")
    L.append("")
    L.append("- 영역 폴더: " + ", ".join(r["roots"]))
    L.append("- 경로 기준: " + r["base"])
    L.append("- 검색 상태: " + " / ".join(r["status"]) +
             (" — 아래 개수는 끝까지 세지 못한 '최소' 값이다" if r["counts_are_minimum"] else ""))
    lim = r["limits"]
    L.append("- 상한: 깊이 %d, 훑을 파일 %d, 시간 %g초, 읽을 파일 %d (걸린 시간 %.2f초, 훑은 파일 %d)" % (
        lim["max_depth"], lim["max_files"], lim["time_limit_s"], lim["read_limit"], r["elapsed_s"], r["scanned_files"]))
    L.append("- 문서 %d개: 읽을 파일 %d (%s KB, 묶음 %d) / 상한 초과 %d / 폐기 표시 %d" % (
        r["doc_count"], r["selected_count"], kb(r["selected_bytes"]), r["batches"],
        r["over_limit_count"], r["deprecated_count"]))
    if r["include"]:
        L.append("- 포함 패턴: %s (패턴 밖 파일 %d개는 세지 않음)" % (", ".join(r["include"]), r["include_skipped"]))
    L.append("- 날짜: 문서 머리에 적힌 날짜를 읽고, 없으면 파일 이름의 날짜를 작성일로 읽었다. 작성일은 그 뒤에 고쳤는지를 가리는 데 쓰지 않는다. 파일 시스템 시각은 쓰지 않았다.")
    L.append("")

    L.append("## 하위 폴더별 개수")
    L.append("")
    L.append("| 폴더 | 문서 | 크기(KB) | 읽을 파일 | 폐기 표시 |")
    L.append("|---|---|---|---|---|")
    for k in sorted(r["folders"]):
        f = r["folders"][k]
        L.append("| %s | %d | %s | %d | %d |" % (k, f["docs"], kb(f["bytes"]), f["selected"], f["deprecated"]))
    L.append("")

    show_since = bool(r["since"])
    L.append("## 읽을 파일 (이 순서로 읽는다%s)" % (" — 문서 날짜가 최근인 것부터" if r.get("order") == "date" else ""))
    L.append("")
    head = "| # | 묶음 | 파일 | 제목 | 크기(KB) | 문서 날짜 | 날짜 근거 | 요약 문서 |"
    sep = "|---|---|---|---|---|---|---|---|"
    if show_since:
        head += " %s 이후 |" % r["since"]
        sep += "---|"
    L.append(head)
    L.append(sep)
    for i, d in enumerate(r["selected"], 1):
        row = "| %d | %d | %s | %s | %s | %s | %s | %s |" % (
            i, d.get("batch", 1), cell(d["path"], 200), cell(d["title"]), kb(d["size"]), d["doc_date"] or "-",
            cell(d["date_basis"]), "예" if d["summary"] else "")
        if show_since:
            row += " %s |" % d.get("since", "")
        L.append(row)
    if not r["selected"]:
        L.append("| - | - | 없음 | | | | | |" + (" |" if show_since else ""))
    L.append("")

    L.append("## 못 읽은 자료 (읽을 파일 수 상한 초과)")
    L.append("")
    if r["over_limit"]:
        L.append("이 파일에 걸린 시스템은 판정하지 않는다.")
        L.append("")
        for d in r["over_limit"]:
            L.append("- %s — %s (%s KB, %s)" % (d["path"], cell(d["title"]) or "제목 없음", kb(d["size"]), d["doc_date"] or d["date_basis"]))
    else:
        L.append("없음")
    L.append("")

    L.append("## 근거에서 뺀 자료 (폐기 표시)")
    L.append("")
    if r["deprecated"]:
        for d in r["deprecated"]:
            L.append("- %s — %s" % (d["path"], d["deprecated"]))
    else:
        L.append("없음")
    L.append("")

    L.append("## 다른 형식 파일 (내용을 읽지 않음)")
    L.append("")
    if r["other_types"]:
        for k in sorted(r["other_types"]):
            L.append("- %s: %d개" % (k, r["other_types"][k]))
    else:
        L.append("없음")
    L.append("")

    if r["excluded_dirs"]:
        L.append("## 제외 규칙으로 뺀 폴더")
        L.append("")
        for x in r["excluded_dirs"][:50]:
            L.append("- " + x)
        if len(r["excluded_dirs"]) > 50:
            L.append("- 외 %d개" % (len(r["excluded_dirs"]) - 50))
        L.append("")
    if r["depth_cut_dirs"]:
        L.append("## 깊이 상한으로 들어가지 않은 폴더")
        L.append("")
        for x in r["depth_cut_dirs"][:50]:
            L.append("- " + x)
        if len(r["depth_cut_dirs"]) > 50:
            L.append("- 외 %d개" % (len(r["depth_cut_dirs"]) - 50))
        L.append("")
    if r["walk_errors"]:
        L.append("## 열지 못한 폴더")
        L.append("")
        for x in r["walk_errors"][:50]:
            L.append("- " + x)
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
