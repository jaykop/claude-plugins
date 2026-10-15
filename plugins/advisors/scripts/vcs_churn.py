#!/usr/bin/env python3
"""버전 관리 이력에서 파일별 변경 횟수와 티켓 키를 모은다. 리팩터링 판단 자료로 쓴다.

읽기 명령만 쓴다.
  git: git log, git rev-parse
  p4 : p4 changes, p4 describe, p4 fstat (--sizes 일 때만)
프로젝트 파일은 읽기만 하고, 결과는 --out 으로 받은 경로에만 쓴다(없으면 표준 출력).
변경 설명 원문과 작성자 이름은 출력하지 않는다. 설명에서 뽑은 티켓 키만 낸다.

티켓 종류(버그인지 등)는 조회하지 않는다. 결과의 키 목록으로 이슈 트래커를 한 번에 조회한다.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ALLOWED = {
    "git": {"log", "rev-parse"},
    "p4": {"changes", "describe", "fstat"},
}
DEFAULT_TICKET_RE = r"\b([A-Z][A-Z0-9]+)-(\d+)\b"
DEFAULT_EXCLUDE_PREFIX = ["UTF", "ISO", "SHA", "RFC"]
DESCRIBE_CHUNK = 20
FSTAT_CHUNK = 50
MAX_SIZE_BYTES = 20 * 1024 * 1024


class VcsError(Exception):
    pass


class TimeBudget:
    def __init__(self, seconds):
        self.deadline = time.monotonic() + seconds

    def left(self):
        return self.deadline - time.monotonic()


def decode_lines(raw):
    """줄마다 UTF-8 로 읽고, 안 되면 cp949, 그래도 안 되면 latin-1 로 읽는다."""
    out = []
    for line in raw.split(b"\n"):
        line = line.rstrip(b"\r")
        for enc in ("utf-8", "cp949", "latin-1"):
            try:
                out.append(line.decode(enc))
                break
            except (UnicodeDecodeError, LookupError):
                continue
    return out


def run(cmd, kind, sub, cwd, budget, allow_fail=False):
    if sub not in ALLOWED[kind]:
        raise VcsError("허용하지 않은 명령: {0} {1}".format(kind, sub))
    left = budget.left()
    if left <= 0:
        raise subprocess.TimeoutExpired(cmd, 0)
    try:
        proc = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=left)
    except FileNotFoundError:
        raise VcsError("'{0}' 명령을 찾지 못함".format(cmd[0]))
    except OSError as e:  # 작업 폴더가 없거나 경로 형식이 잘못된 경우 등
        raise VcsError("'{0}' 를 실행하지 못함(작업 폴더: {1}): {2}".format(cmd[0], cwd or "현재 폴더", e))
    if proc.returncode != 0 and not allow_fail:
        err = "\n".join(decode_lines(proc.stderr)).strip() or "(오류 문구 없음)"
        raise VcsError("{0} 실패(종료 코드 {1}): {2}".format(" ".join(cmd[:3]), proc.returncode, err[:500]))
    return proc.stdout, proc.stderr


# ---------------------------------------------------------------- git

def collect_git(args, budget, notes):
    repo = args.repo or "."
    # 날짜는 커밋 날짜(%cd)다. --since/--until 이 커밋 날짜로 거르므로 같은 기준을 쓴다.
    fmt = "%x1eC%x1f%H%x1f%cd%x1f%B%x1f"
    cmd = ["git", "-C", repo, "log", "--no-merges", "--no-renames", "--name-only", "--date=short",
           "--since=" + args.since, "-n", str(args.max_changes + 1), "--pretty=format:" + fmt]
    if args.until:
        cmd.append("--until=" + args.until + " 23:59:59")
    cmd.append("--")
    cmd.extend(args.path or [])
    raw, _ = run(cmd, "git", "log", None, budget)
    text = "\n".join(decode_lines(raw))
    changes = []
    for chunk in text.split("\x1e"):
        if not chunk.strip():
            continue
        parts = chunk.split("\x1f")
        if len(parts) < 5 or parts[0] != "C":
            continue
        files = [ln.strip() for ln in parts[4].splitlines() if ln.strip()]
        changes.append({"id": parts[1][:12], "date": parts[2].strip(), "desc": parts[3], "files": files})
    root = None
    if args.sizes:
        try:
            out, _ = run(["git", "-C", repo, "rev-parse", "--show-toplevel"], "git", "rev-parse", None, budget)
            root = decode_lines(out)[0].strip()
        except VcsError as e:
            notes.append("저장소 최상위 폴더를 못 찾아 줄 수를 세지 못함: {0}".format(e))
    commands = [" ".join(cmd[:1] + cmd[3:4]) + " (기간·경로 조건)"]
    return changes, root, commands


# ---------------------------------------------------------------- p4

def parse_ztag(lines):
    """p4 -ztag 출력을 레코드 목록으로 바꾼다. 새 'change' 필드가 나오면 새 레코드다."""
    records = []
    cur = None
    last_key = None
    for line in lines:
        if line.startswith("... "):
            body = line[4:]
            key, _, value = body.partition(" ")
            if key == "change" or cur is None:
                if cur is not None:
                    records.append(cur)
                cur = {}
            cur[key] = value
            last_key = key
        elif cur is not None and last_key == "desc":
            cur["desc"] = cur.get("desc", "") + "\n" + line
    if cur is not None:
        records.append(cur)
    return records


def p4_date(value):
    return value.replace("-", "/")


def collect_p4(args, budget, notes):
    if not args.path:
        raise VcsError("p4 는 --path 가 필요하다. 예: --path //depot/Game/...")
    base = ["p4"]
    if args.p4_charset:
        base += ["-C", args.p4_charset]
    end = "@" + p4_date(args.until) + ":23:59:59" if args.until else "@now"
    changes_cmds = []
    numbers = []
    for path in args.path:
        spec = "{0}@{1},{2}".format(path, p4_date(args.since), end)
        cmd = base + ["-ztag", "changes", "-s", "submitted", "-m", str(args.max_changes + 1), spec]
        changes_cmds.append(" ".join(cmd))
        raw, _ = run(cmd, "p4", "changes", args.cwd, budget)
        for rec in parse_ztag(decode_lines(raw)):
            if rec.get("change", "").isdigit():
                numbers.append(int(rec["change"]))
    numbers = sorted(set(numbers), reverse=True)
    prefixes = []
    for path in args.path:
        if path.startswith("//") and path.endswith("/..."):
            prefixes.append(path[:-3].casefold())
        else:
            prefixes = None
            notes.append("depot 경로('//.../...' 꼴)가 아닌 경로가 있어 파일을 경로로 거르지 않음: {0}".format(path))
            break

    def in_scope(depot_file):
        return prefixes is None or any(depot_file.casefold().startswith(p) for p in prefixes)

    changes = []
    failed = []
    described = 0
    for i in range(0, min(len(numbers), args.max_changes + 1), DESCRIBE_CHUNK):
        chunk = numbers[i:i + DESCRIBE_CHUNK]
        cmd = base + ["-ztag", "describe", "-s"] + [str(n) for n in chunk]
        try:
            raw, err = run(cmd, "p4", "describe", args.cwd, budget, allow_fail=True)
        except subprocess.TimeoutExpired:
            notes.append("describe 중 시간 초과 — 앞의 {0}개 변경만 집계함".format(described))
            raise PartialResult(changes)
        recs = {int(r["change"]): r for r in parse_ztag(decode_lines(raw)) if r.get("change", "").isdigit()}
        for n in chunk:
            rec = recs.get(n)
            if rec is None:
                failed.append(n)
                continue
            files = [v for k, v in sorted(rec.items()) if re.match(r"depotFile\d+$", k) and in_scope(v)]
            date = ""
            if rec.get("time", "").isdigit():
                date = datetime.fromtimestamp(int(rec["time"])).strftime("%Y-%m-%d")
            changes.append({"id": str(n), "date": date, "desc": rec.get("desc", ""), "files": files})
            described += 1
    if failed:
        notes.append("describe 결과가 없는 변경 {0}개(권한·삭제 등): {1}".format(
            len(failed), ", ".join(str(n) for n in failed[:20])))
    cmds = [c for c in changes_cmds] + ["p4 -ztag describe -s <변경 번호 {0}개씩> × {1}회".format(
        DESCRIBE_CHUNK, (min(len(numbers), args.max_changes + 1) + DESCRIBE_CHUNK - 1) // DESCRIBE_CHUNK)]
    return changes, None, cmds


class PartialResult(Exception):
    def __init__(self, changes):
        super().__init__("partial")
        self.changes = changes


# ---------------------------------------------------------------- 집계

def ticket_finder(args):
    if args.ticket_prefix:
        prefixes = [p.strip() for chunk in args.ticket_prefix for p in chunk.split(",") if p.strip()]
        pattern = r"\b(" + "|".join(re.escape(p) for p in prefixes) + r")-(\d+)\b"
    else:
        pattern = args.ticket_regex or DEFAULT_TICKET_RE
    regex = re.compile(pattern)
    exclude = set(p.strip() for chunk in (args.exclude_prefix or [",".join(DEFAULT_EXCLUDE_PREFIX)])
                  for p in chunk.split(",") if p.strip())

    def find(text):
        keys = set()
        for m in regex.finditer(text or ""):
            if m.lastindex and m.lastindex >= 2 and m.group(2) and m.group(2).isdigit():
                prefix, num = m.group(1), m.group(2)
                if prefix in exclude:
                    continue
                keys.add("{0}-{1}".format(prefix, int(num)))
            else:
                whole = m.group(0)
                if whole.partition("-")[0] in exclude:
                    continue
                keys.add(whole)
        return keys

    return find, pattern, sorted(exclude)


def count_lines(path):
    try:
        if os.path.getsize(path) > MAX_SIZE_BYTES:
            return "크기 상한 초과"
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return "읽기 실패"
    if b"\x00" in data[:8192]:
        return "이진 파일"
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def sizes_git(root, files):
    out = {}
    for f in files:
        local = os.path.join(root, f)
        out[f] = count_lines(local) if os.path.isfile(local) else "로컬에 없음"
    return out


def sizes_p4(args, files, budget, notes):
    base = ["p4"] + (["-C", args.p4_charset] if args.p4_charset else [])
    out = {}
    for i in range(0, len(files), FSTAT_CHUNK):
        chunk = files[i:i + FSTAT_CHUNK]
        try:
            raw, _ = run(base + ["-ztag", "fstat", "-T", "depotFile,clientFile"] + chunk,
                         "p4", "fstat", args.cwd, budget, allow_fail=True)
        except subprocess.TimeoutExpired:
            notes.append("fstat 중 시간 초과 — 줄 수 일부만 셈")
            break
        cur = {}
        for line in decode_lines(raw) + [""]:
            if line.startswith("... "):
                key, _, value = line[4:].partition(" ")
                cur[key] = value
            elif cur:
                if "depotFile" in cur and "clientFile" in cur:
                    local = cur["clientFile"]
                    out[cur["depotFile"]] = count_lines(local) if os.path.isfile(local) else "로컬에 없음"
                cur = {}
    for f in files:
        out.setdefault(f, "확인 못 함")
    return out


def aggregate(changes, args, find_keys):
    files = {}
    pair_counts = {}
    ticket_changes = {}
    bulk = 0
    excludes = [e.replace("\\", "/").rstrip("/").rstrip(".").rstrip("/").casefold() for e in (args.exclude_path or [])]
    for ch in changes:
        if excludes:
            # 점검 제외 경로 아래 파일은 세지 않는다(외부 공급사 플러그인 등)
            ch["files"] = [f for f in ch["files"]
                           if not any(f.replace("\\", "/").casefold().startswith(e + "/") for e in excludes)]
        keys = find_keys(ch["desc"])
        ch["keys"] = keys
        for k in keys:
            ticket_changes[k] = ticket_changes.get(k, 0) + 1
        nfiles = len(ch["files"])
        is_bulk = nfiles > args.bulk_files
        if is_bulk:
            bulk += 1
        for f in ch["files"]:
            e = files.setdefault(f, {"changes": 0, "tickets": set(), "co_sum": 0, "co_n": 0, "last": ""})
            e["changes"] += 1
            e["tickets"].update(keys)
            if not is_bulk:
                e["co_sum"] += nfiles - 1
                e["co_n"] += 1
            if ch["date"] > e["last"]:
                e["last"] = ch["date"]
        if not is_bulk and nfiles > 1:
            uniq = sorted(set(ch["files"]))
            for i in range(len(uniq)):
                for j in range(i + 1, len(uniq)):
                    pair = (uniq[i], uniq[j])
                    pair_counts[pair] = pair_counts.get(pair, 0) + 1
    return files, pair_counts, ticket_changes, bulk


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(lines)


def command_text():
    return "python " + " ".join(
        ('"{0}"'.format(a) if (" " in a or not a) else a) for a in [os.path.basename(sys.argv[0])] + sys.argv[1:]
    )


def render(args, changes, cap_hit, partial, files, pairs, tickets, bulk, sizes, notes, pattern, exclude, vcs_cmds):
    ranked = sorted(files.items(), key=lambda kv: (-kv[1]["changes"], kv[0]))
    top = ranked[: args.top]
    top_pairs = sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0]))[: args.pairs]
    ticket_list = sorted(tickets.items(), key=lambda kv: (-kv[1], kv[0]))
    change_rows = []
    if args.changes:
        ordered = sorted(changes, key=lambda c: (c["date"], c["id"]), reverse=True)[: args.changes]
        change_rows = [{"id": c["id"], "date": c["date"], "files": len(c["files"]),
                        "ticket_keys": sorted(c.get("keys", []))} for c in ordered]

    if args.format == "json":
        return json.dumps({
            "command": command_text(),
            "vcs": args.vcs, "paths": args.path, "since": args.since, "until": args.until,
            "vcs_commands": vcs_cmds,
            "changes": len(changes), "change_cap": args.max_changes, "cap_hit": cap_hit, "partial": partial,
            "bulk_threshold": args.bulk_files, "bulk_changes": bulk,
            "files": [{
                "file": f, "changes": e["changes"], "ticket_keys": sorted(e["tickets"]),
                "avg_cochanged_files": (e["co_sum"] / e["co_n"]) if e["co_n"] else None,
                "last_change": e["last"], "lines": sizes.get(f) if sizes else None,
            } for f, e in top],
            "file_count": len(files),
            "pairs": [{"a": a, "b": b, "count": n} for (a, b), n in top_pairs],
            "ticket_keys": [{"key": k, "changes": n} for k, n in ticket_list],
            "ticket_pattern": pattern, "ticket_excluded_prefixes": exclude,
            "change_list": change_rows,
            "notes": notes,
        }, ensure_ascii=False, indent=2)

    out = ["## 버전 관리 변경 집계\n"]
    period = "{0} ~ {1}".format(args.since, args.until or "오늘")
    cap = "{0}개".format(len(changes))
    if cap_hit:
        cap += " — 상한 {0}개에 걸림. 기간 안 변경이 더 있을 수 있다".format(args.max_changes)
    if partial:
        cap += " — 일부만 집계함(아래 '확인 못 한 것')"
    out.append(md_table(["항목", "값"], [
        ("명령", "`" + command_text() + "`"),
        ("버전 관리", args.vcs),
        ("대상 경로", ", ".join(args.path) if args.path else "저장소 전체"),
        ("제외한 경로", ", ".join(args.exclude_path) if args.exclude_path else "없음"),
        ("기간", period),
        ("실행한 읽기 명령", "; ".join(vcs_cmds)),
        ("변경 수", cap),
        ("파일 수", "{0}개".format(len(files))),
        ("함께 바뀐 파일", "대상 경로 안의 파일만 센다"),
        ("묶음 변경", "파일 {0}개 넘게 바꾼 변경 {1}개 — 변경 횟수에는 넣고, 함께 바뀐 파일 계산에서는 뺐다".format(
            args.bulk_files, bulk)),
        ("티켓 키 규칙", "`{0}` (제외 접두사: {1}). 번호 앞자리 0 은 떼어 맞췄다".format(
            pattern, ", ".join(exclude) if exclude else "없음")),
    ]))
    out.append("")
    out.append("### 파일별 변경 횟수 (상위 {0}개)\n".format(len(top)))
    if top:
        hdr = ["순위", "파일", "변경 횟수", "티켓 키 수", "함께 바뀐 파일 수 평균", "마지막 변경일"]
        if sizes is not None:
            hdr.append("줄 수(로컬 사본)")
        rows = []
        for i, (f, e) in enumerate(top, 1):
            avg = "{0:.1f}".format(e["co_sum"] / e["co_n"]) if e["co_n"] else "-"
            row = [i, f, e["changes"], len(e["tickets"]), avg, e["last"] or "-"]
            if sizes is not None:
                row.append(sizes.get(f, "-"))
            rows.append(row)
        out.append(md_table(hdr, rows))
    else:
        out.append("기간 안 변경이 없음. 경로와 기간을 확인한 뒤, 좁힌 조건으로 한 번 더 조회해서 '없음'을 확정한다.")
    out.append("")
    if top_pairs:
        out.append("### 함께 자주 바뀐 파일 쌍 (상위 {0}개, 묶음 변경 제외)\n".format(len(top_pairs)))
        out.append(md_table(["파일 1", "파일 2", "함께 바뀐 횟수"], [[a, b, n] for (a, b), n in top_pairs]))
        out.append("")
    out.append("### 티켓 키 ({0}개)\n".format(len(ticket_list)))
    if ticket_list:
        out.append(md_table(["키", "등장한 변경 수"], [[k, n] for k, n in ticket_list[:200]]))
        if len(ticket_list) > 200:
            out.append("\n표는 200개까지만 보였다. 전체 목록은 아래 한 줄에 있다.")
        out.append("\n이슈 트래커 조회용 한 줄 목록:\n")
        out.append("```\n" + ", ".join(k for k, _ in ticket_list) + "\n```")
    else:
        out.append("설명에서 찾은 티켓 키가 없음.")
    out.append("")
    if args.changes:
        out.append("### 변경 목록 (최근 {0}개)\n".format(len(change_rows)))
        if change_rows:
            out.append(md_table(["변경", "날짜", "대상 경로 안 파일 수", "티켓 키"],
                                [[c["id"], c["date"] or "-", c["files"], ", ".join(c["ticket_keys"]) or "-"]
                                 for c in change_rows]))
        else:
            out.append("변경 없음.")
        out.append("")
    if notes:
        out.append("### 확인 못 한 것\n")
        out.extend("- " + n for n in notes)
        out.append("")
    return "\n".join(out)


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--since", required=True, metavar="YYYY-MM-DD", help="기간 시작일(이 날 포함)")
    common.add_argument("--until", metavar="YYYY-MM-DD", help="기간 끝날(이 날 포함). 없으면 오늘까지")
    common.add_argument("--path", action="append", metavar="경로",
                        help="대상 경로. git 은 저장소 안 경로, p4 는 depot 경로(예: //depot/Game/...). 여러 번 줄 수 있다")
    common.add_argument("--max-changes", type=int, default=500, metavar="N",
                        help="읽을 최대 변경 수. 넘으면 최근 것부터 이만큼만 읽고 '상한에 걸림'으로 표시한다. 기본 500")
    common.add_argument("--top", type=int, default=30, metavar="N", help="파일 표에 낼 개수. 기본 30")
    common.add_argument("--pairs", type=int, default=10, metavar="N", help="함께 바뀐 파일 쌍 표에 낼 개수. 기본 10, 0 이면 안 냄")
    common.add_argument("--changes", type=int, default=0, metavar="N",
                        help="최근 변경 N개를 번호·날짜·파일 수·티켓 키로 나열한다(원인 후보 찾기용). 기본 0(안 냄)")
    common.add_argument("--bulk-files", type=int, default=50, metavar="N",
                        help="이보다 많은 파일을 바꾼 변경은 함께 바뀐 파일 계산에서 뺀다(일괄 정리 등). 기본 50")
    common.add_argument("--ticket-prefix", action="append", metavar="접두사",
                        help="티켓 키 접두사. 쉼표로 여러 개. 주면 이 접두사만 찾는다. 예: --ticket-prefix ABC,XYZ")
    common.add_argument("--ticket-regex", metavar="정규식",
                        help="티켓 키 정규식. 기본 '[A-Z][A-Z0-9]+-숫자'. 그룹 1=접두사, 그룹 2=번호로 짜면 번호를 맞춰 준다")
    common.add_argument("--exclude-path", action="append", metavar="경로",
                        help="이 경로 아래 파일은 세지 않는다. 여러 번 줄 수 있다. git 은 저장소 기준 경로, p4 는 depot 경로(//.../...)")
    common.add_argument("--exclude-prefix", action="append", metavar="접두사",
                        help="키로 치지 않을 접두사. 쉼표로 여러 개. 기본 UTF,ISO,SHA,RFC (UTF-8 같은 글자를 키로 오인하지 않게)")
    common.add_argument("--sizes", action="store_true",
                        help="상위 파일의 로컬 사본 줄 수를 센다. p4 는 fstat 으로 로컬 경로를 찾는다")
    common.add_argument("--format", choices=["md", "json"], default="md", help="출력 형식. 기본 md")
    common.add_argument("--out", metavar="경로", help="결과를 쓸 파일. 없으면 표준 출력")
    common.add_argument("--timeout", type=float, default=120.0, metavar="초",
                        help="전체 시간 상한(초). 넘으면 '검색 실패(시간 초과)' 또는 '일부만 집계'로 표시한다. 기본 120")

    parser = argparse.ArgumentParser(
        description="버전 관리 이력에서 파일별 변경 횟수, 함께 바뀐 파일, 티켓 키를 모은다(읽기 전용).",
        epilog="예: python vcs_churn.py git --repo . --since 2026-01-01 --path Source/\n"
               "    python vcs_churn.py p4 --path //depot/Game/Source/... --since 2026-01-01 --max-changes 300 --ticket-prefix ABC\n"
               "종료 코드: 0 정상, 2 오류(명령 실패·인자 오류), 3 시간 초과로 실패하거나 일부만 집계",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="vcs")
    p_git = sub.add_parser("git", parents=[common], help="git 저장소")
    p_git.add_argument("--repo", metavar="폴더", help="저장소 폴더. 기본 현재 폴더")
    p_p4 = sub.add_parser("p4", parents=[common], help="Perforce")
    p_p4.add_argument("--cwd", metavar="폴더", help="p4 를 실행할 폴더(P4CONFIG 를 이 폴더 기준으로 찾음)")
    p_p4.add_argument("--p4-charset", metavar="이름", help="p4 -C 로 넘길 문자 집합. 서버가 유니코드 모드인데 환경에 없을 때만")
    return parser


def valid_date(text):
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.vcs:
        parser.print_help()
        return 2
    if args.vcs == "p4" and not args.cwd:
        args.cwd = None  # 빈 문자열이 오면 현재 폴더에서 실행한다
    if args.vcs == "p4" and args.cwd and not os.path.isdir(args.cwd):
        parser.error("--cwd 폴더가 없다: {0}".format(args.cwd))
    if not valid_date(args.since) or (args.until and not valid_date(args.until)):
        parser.error("날짜는 YYYY-MM-DD 형식이어야 한다")
    if args.max_changes < 1:
        parser.error("--max-changes 는 1 이상이어야 한다")
    for p in args.path or []:
        if not p or p.startswith("-"):
            parser.error("--path 값이 비었거나 '-' 로 시작한다(명령 옵션으로 읽힐 수 있음): {0}".format(p))

    budget = TimeBudget(args.timeout)
    notes = []
    partial = False
    vcs_cmds = []
    try:
        if args.vcs == "git":
            changes, root, vcs_cmds = collect_git(args, budget, notes)
        else:
            changes, root, vcs_cmds = collect_p4(args, budget, notes)
    except PartialResult as pr:
        changes, root, partial = pr.changes, None, True
        vcs_cmds = ["p4 changes / p4 describe (도중 시간 초과)"]
    except subprocess.TimeoutExpired:
        print("검색 실패(시간 초과): 변경 목록을 {0}초 안에 받지 못함. 0건이 아니다. "
              "경로나 기간을 좁혀 다시 실행한다.".format(int(args.timeout)), file=sys.stderr)
        return 3
    except VcsError as e:
        print("오류: {0}".format(e), file=sys.stderr)
        return 2

    cap_hit = len(changes) > args.max_changes
    if cap_hit:
        changes = changes[: args.max_changes]
    find_keys, pattern, exclude = ticket_finder(args)
    files, pairs, tickets, bulk = aggregate(changes, args, find_keys)

    sizes = None
    if args.sizes:
        top_files = [f for f, _ in sorted(files.items(), key=lambda kv: (-kv[1]["changes"], kv[0]))[: args.top]]
        if args.vcs == "git" and root:
            sizes = sizes_git(root, top_files)
        elif args.vcs == "p4":
            sizes = sizes_p4(args, top_files, budget, notes)
        else:
            sizes = {}

    text = render(args, changes, cap_hit, partial, files, pairs, tickets, bulk, sizes, notes, pattern, exclude, vcs_cmds)
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
    return 3 if partial else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
