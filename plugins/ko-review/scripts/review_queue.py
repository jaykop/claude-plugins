#!/usr/bin/env python3
"""작업별 설명 변경 목록과 내용 스냅샷을 기록한다. Python 표준 라이브러리만 쓴다.

작성하는 AI 는 start · scope · capture · register · no-impact 로 바꾼 설명과 근거 구현을 남기고,
검토하는 AI 는 pending · begin · snapshot · finish 로 대기 항목을 교정한 결과를 남긴다.
작업을 커밋한 뒤에는 작성하는 AI 가 retire 로 사라진 설명을 폐기하고 close 로 목록을 닫는다.
목록 형식은 플러그인의 shared/queue-format.md 를 따른다.

프로젝트 루트: --root, 환경 변수 CLAUDE_PROJECT_DIR, 현재 폴더의 git 최상위, 현재 폴더 순으로 정한다.
버전 관리: 프로필의 vcs(git, p4, none)를 쓴다. 없으면 git 저장소인지 본다. git 이 아니면 파일 사본과 비교해 변경 구간을 찾는다.
목록 폴더: --queue-dir, 프로필(.claude/ko-review/profile.md)의 queue_dir, 기본값 순으로 정한다.
등록 범위: 프로필의 queue_scope 패턴에 맞고 exclude 에 걸리지 않는 설명 파일만 등록한다. queue_scope 가 비면 제한하지 않는다.
보관 폴더: --archive-dir, 프로필의 queue_archive_dir 순으로 정한다. 없으면 닫은 목록을 제자리에 둔다.
"""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import difflib
from fnmatch import fnmatchcase
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PROFILE = ".claude/ko-review/profile.md"
DEFAULT_QUEUE_DIR = ".claude/ko-review/queue"
KINDS = ("comment", "doc", "data-comment")
# 이전 형식의 kind 이름. 기존 목록을 그대로 읽고, 새로 등록할 때만 바꾼다.
LEGACY_KINDS = {"manual": "doc", "tag-devcomment": "data-comment"}

ROOT = Path.cwd()
QUEUES = ROOT / DEFAULT_QUEUE_DIR
QUEUE_SCOPE = []
EXCLUDE = []
VCS = "git"


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def find_root(explicit):
    if explicit:
        return Path(explicit).resolve()
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and Path(env).is_dir():
        return Path(env).resolve()
    try:
        top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                      encoding="utf-8", stderr=subprocess.DEVNULL).strip()
        if top:
            return Path(top).resolve()
    except (OSError, subprocess.CalledProcessError):
        pass
    return Path.cwd().resolve()


def profile_value(root, key):
    """프로필 머리(--- 사이)의 최상위 `key: value` 한 줄만 읽는다. 없으면 None."""
    path = root / PROFILE
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^" + re.escape(key) + r":\s*(.*)$", line)
        if match:
            value = re.sub(r"\s+#.*$", "", match.group(1)).strip().strip("'\"")
            return value or None
    return None


def profile_list(root, key):
    """`key: [a, b]` 한 줄을 목록으로 읽는다. 괄호가 없으면 값 하나짜리 목록, 칸이 없으면 빈 목록이다."""
    value = profile_value(root, key)
    if not value:
        return []
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip().strip("'\"")]


def matches(path, patterns):
    # 패턴이 폴더 이름이면 그 아래 파일도 맞는 것으로 본다. fnmatch 의 * 는 / 도 넘는다.
    return any(fnmatchcase(path, p) or fnmatchcase(path, p.rstrip("/") + "/*") for p in patterns)


def in_queue_scope(path):
    """queue_scope 가 비면 모든 경로를 받는다. exclude 는 queue_scope 가 있을 때만 적용한다."""
    if not QUEUE_SCOPE:
        return True
    return matches(path, QUEUE_SCOPE) and not matches(path, EXCLUDE)


def project_path(value):
    path = (ROOT / value).resolve()
    path.relative_to(ROOT)
    return path


def relative(value):
    return project_path(value).relative_to(ROOT).as_posix()


def git(*args):
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, encoding="utf-8", errors="strict"
    ).strip()


def vcs_kind():
    """버전 관리 종류. 프로필 vcs 가 있으면 그 값이고, 없으면 git 저장소인지 본다."""
    value = profile_value(ROOT, "vcs")
    if value:
        if value not in ("git", "p4", "none"):
            raise ValueError("Unknown profile vcs; use git, p4 or none")
        return value
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], cwd=ROOT, stderr=subprocess.DEVNULL)
        return "git"
    except (OSError, subprocess.CalledProcessError):
        return "none"


def p4_opened(*paths):
    """p4 opened 출력. 상태를 남기는 용도라 실패해도 작업을 막지 않고 빈 글을 돌려준다."""
    try:
        return subprocess.run(["p4", "opened", *paths], cwd=ROOT, capture_output=True, encoding="utf-8",
                              errors="replace", timeout=30).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def head_ref():
    return git("rev-parse", "HEAD") if VCS == "git" else None


def initial_changes():
    if VCS == "git":
        return git("status", "--short")
    return p4_opened() if VCS == "p4" else ""


def initially_dirty(path):
    if VCS == "git":
        return bool(git("status", "--short", "--", path))
    return bool(p4_opened(str(project_path(path)))) if VCS == "p4" else False


def base_folder(task):
    return QUEUES / f"{task}.base"


def save_base(task, path):
    """git 이 아니면 시작 상태를 되찾을 곳이 없으므로 수정 전 파일을 목록 폴더에 복사해 둔다."""
    source = project_path(path)
    if source.is_file():
        target = base_folder(task) / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def text_lines(path):
    return path.read_text(encoding="utf-8-sig", errors="replace").splitlines() if path.is_file() else []


def base_hunks(task, path):
    """시작 상태의 사본과 지금 파일을 비교한 diff 구간."""
    diff = difflib.unified_diff(text_lines(base_folder(task) / path), text_lines(project_path(path)), n=0, lineterm="")
    return [line for line in diff if line.startswith("@@")]


def file_hash(value):
    path = project_path(value)
    return digest(path.read_bytes()) if path.is_file() else None


def queue_path(task):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", task):
        raise ValueError("Task ID must use lowercase letters, digits and hyphens")
    path = (QUEUES / f"{task}.descriptions.json").resolve()
    path.relative_to(ROOT)
    return path


@contextmanager
def edit_queue(task, create=False):
    path = queue_path(task)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(path.suffix + ".lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        original = path.read_bytes() if path.exists() else None
        if create and original is not None:
            if json.loads(original.decode("utf-8")).get("closed"):
                raise ValueError("Queue for this task is closed; use a new task ID, "
                                 "or set queue_archive_dir so closed queues move out")
            raise ValueError("Queue already exists; reuse it instead of resetting")
        if not create and original is None:
            raise ValueError("Queue does not exist; run start first")
        data = json.loads(original.decode("utf-8")) if original else {}
        if original and data.get("schemaVersion") != 1:
            raise ValueError("Unsupported queue schema version")
        yield data
        # 잠금을 쓰지 않는 편집기의 수정도 덮어쓰지 않는다.
        current = path.read_bytes() if path.exists() else None
        if current != original:
            raise ValueError("Queue changed during this operation; retry after reading it")
        data["updatedAt"] = now()
        temp.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        # Windows 에서 동기화·읽기 도중 잠깐 파일 교체를 막으면 제한적으로 재시도한다.
        for attempt in range(4):
            latest = path.read_bytes() if path.exists() else None
            if latest != original:
                raise ValueError("Queue changed before replacement; read it again")
            try:
                os.replace(temp, path)
                break
            except PermissionError:
                if attempt == 3:
                    raise
                time.sleep(0.1 * (attempt + 1))
    finally:
        os.close(fd)
        lock.unlink()
        if temp.exists():
            temp.unlink()


def block(selector):
    lines = project_path(selector["path"]).read_text(encoding="utf-8-sig").splitlines()
    matches = [i for i, line in enumerate(lines) if selector["anchor"] in line]
    if len(matches) != 1:
        raise ValueError(f"Anchor must match one line: {selector['path']} / {selector['anchor']}")
    index = matches[0]
    start = index - selector.get("before", 0)
    end = index + 1 + selector.get("after", 0)
    mode = selector.get("mode", "lines")
    if mode == "heading":
        heading = re.match(r"^(#{1,6})\s", lines[index])
        if not heading:
            raise ValueError("Heading selector must point to a Markdown heading")
        level = len(heading.group(1))
        end = len(lines)
        for i in range(index + 1, len(lines)):
            other = re.match(r"^(#{1,6})\s", lines[i])
            if other and len(other.group(1)) <= level:
                end = i
                break
    elif mode == "span":
        ends = [i for i in range(index + 1, len(lines)) if selector["endAnchor"] in lines[i]]
        if len(ends) != 1:
            raise ValueError("End anchor must match one later line")
        end = ends[0] + (1 if selector.get("includeEnd", False) else 0)
    elif mode != "lines":
        raise ValueError("Unknown selector mode")
    if start < 0 or end > len(lines) or start >= end:
        raise ValueError("Selected block is outside the file")
    text = "\n".join(lines[start:end]) + "\n"
    return {"sha256": digest(text.encode("utf-8")), "lineHint": start + 1, "endLineHint": end}


def normalize_selector(selector):
    selector = dict(selector)
    selector["path"] = relative(selector["path"])
    if not isinstance(selector.get("anchor"), str) or not selector["anchor"]:
        raise ValueError("Selector requires a literal anchor")
    for key in ("before", "after"):
        if not isinstance(selector.get(key, 0), int) or selector.get(key, 0) < 0:
            raise ValueError("before/after must be nonnegative line counts")
    return selector


def snapshot(entry):
    return {"description": block(entry["selector"]),
            "evidence": [block(item) for item in entry["evidence"]]}


def fingerprints(value):
    # 줄 위치만 바뀌었을 때는 검토를 유지하고, 선택한 내용의 변화를 비교한다.
    return [value["description"]["sha256"], *[item["sha256"] for item in value["evidence"]]]


def refresh(data):
    for entry in data["entries"]:
        # 폐기한 항목은 설명이 사라졌거나 다른 작업으로 넘어간 것이므로 다시 대기로 돌리지 않는다.
        if entry["status"] == "retired":
            continue
        try:
            current = snapshot(entry)
            entry.pop("locationError", None)
            reference = entry.get("review", {}).get("snapshot", entry["snapshot"])
            if fingerprints(current) != fingerprints(reference):
                entry["status"] = "pending"
                entry.pop("ticket", None)
            entry["snapshot"] = current
        except (OSError, ValueError, KeyError) as error:
            entry["status"] = "pending"
            entry["locationError"] = str(error)
            entry.pop("ticket", None)


def get_entry(data, entry_id):
    for entry in data["entries"]:
        if entry["id"] == entry_id:
            return entry
    raise ValueError("Entry not found")


def capture(data):
    data["headCommit"] = head_ref()
    changes = []
    for path in data["taskPaths"]:
        current = file_hash(path)
        initial = data["initialFiles"][path]
        if current == initial["sha256"]:
            continue
        if VCS == "git":
            patch = git("diff", "--no-ext-diff", "--no-textconv", "--unified=0",
                        data["baseCommit"], "--", path)
            hunks = re.findall(r"^@@.*@@.*$", patch, flags=re.MULTILINE)
        else:
            hunks = base_hunks(data["taskId"], path)
        changes.append({"path": path, "sha256": current, "hunks": hunks,
                        "initiallyDirty": initial["dirty"],
                        "changeType": "deleted" if current is None else "modified-or-added"})
    data["changes"] = changes
    data["capturedAt"] = now()
    refresh(data)


def ensure_open(data):
    # 닫힌 목록은 그 작업의 커밋으로 끝난 기록이다. 이후의 변경은 새 작업의 목록이 맡는다.
    if data.get("closed"):
        raise ValueError("Queue is closed; record later changes in a new task queue")


def archive_folder(explicit):
    """보관 폴더를 정한다. {year}·{quarter} 는 닫는 날의 연도와 분기(예: 2026-Q4)다. 없으면 None."""
    pattern = explicit or profile_value(ROOT, "queue_archive_dir")
    if not pattern:
        return None
    today = datetime.now().astimezone()
    quarter = f"{today.year}-Q{(today.month - 1) // 3 + 1}"
    return project_path(pattern.format(year=today.year, quarter=quarter))


def remove_item_files(task):
    """닫은 작업의 등록 입력 파일(<task>.items*.json)을 지우고 지운 경로를 돌려준다."""
    # register 가 항목 내용을 목록에 모두 옮기고, 닫은 작업은 다시 등록하지 않으므로 입력 파일은 남길 이유가 없다.
    removed = sorted(QUEUES.glob(f"{task}.items*.json"))
    for path in removed:
        path.unlink()
    # 닫은 작업은 다시 capture 하지 않으므로 시작 상태의 사본도 남길 이유가 없다.
    base = base_folder(task)
    if base.is_dir():
        shutil.rmtree(base)
        removed.append(base)
    return removed


def archive_queue(task, folder):
    """닫은 목록을 보관 폴더로 옮기고 새 경로를 돌려준다."""
    source = queue_path(task)
    lock = source.with_suffix(source.suffix + ".lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        # 같은 작업을 여러 번 닫으면 보관 폴더에 앞선 목록이 있으므로 번호를 붙여 덮어쓰지 않는다.
        number, target = 1, folder / source.name
        while target.exists():
            number += 1
            target = folder / f"{task}.{number}{source.name[len(task):]}"
        folder.mkdir(parents=True, exist_ok=True)
        os.replace(source, target)
        return target
    finally:
        os.close(fd)
        lock.unlink()


def issue_ref(value):
    # 기존 목록과 맞추려고 숫자만 있으면 정수로 둔다. 다른 트래커의 키(ABC-12)는 문자열로 둔다.
    if value is None:
        return None
    return int(value) if value.isdigit() else value


def main():
    global ROOT, QUEUES, QUEUE_SCOPE, EXCLUDE, VCS
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=("start", "scope", "capture", "register", "no-impact",
                                            "pending", "snapshot", "begin", "finish", "retire", "close"))
    parser.add_argument("task")
    parser.add_argument("--root", help="Project root (default: CLAUDE_PROJECT_DIR or git top level)")
    parser.add_argument("--queue-dir", help="Queue folder relative to the root (default: profile queue_dir)")
    parser.add_argument("--paths", nargs="+")
    parser.add_argument("--issue", help="Issue number or tracker key linked to this task")
    parser.add_argument("--items", help="Project-relative JSON array of review entries")
    parser.add_argument("--path", help="Task file whose descriptions are unaffected")
    parser.add_argument("--id")
    parser.add_argument("--token")
    parser.add_argument("--reviewer", help="Reviewer name recorded by begin (default: profile reviewer, then 'reviewer')")
    parser.add_argument("--status", choices=("reviewed", "needs-decision"), default="reviewed")
    parser.add_argument("--note")
    parser.add_argument("--description-hash", help="Expected hash of the final, edited description block")
    parser.add_argument("--allow-unresolved", action="store_true",
                        help="Let close keep entries that are not reviewed or retired")
    parser.add_argument("--archive-dir", help="Folder for closed queues, {year}/{quarter} allowed (default: profile queue_archive_dir)")
    args = parser.parse_args()

    ROOT = find_root(args.root)
    QUEUES = ROOT / (args.queue_dir or profile_value(ROOT, "queue_dir") or DEFAULT_QUEUE_DIR)
    QUEUE_SCOPE = profile_list(ROOT, "queue_scope")
    EXCLUDE = profile_list(ROOT, "exclude")
    VCS = vcs_kind()

    closed_queue = False
    with edit_queue(args.task, create=args.command == "start") as data:
        # 닫힌 목록에서는 읽기 명령만 받는다.
        if args.command not in ("start", "pending", "snapshot"):
            ensure_open(data)
        if args.command == "start":
            if not args.paths:
                raise ValueError("start requires explicit file paths")
            data.update(schemaVersion=1, taskId=args.task, issue=issue_ref(args.issue),
                        baseCommit=head_ref(), headCommit=head_ref(),
                        startedAt=now(), initialChanges=initial_changes(),
                        taskPaths=[], initialFiles={}, changes=[], entries=[], noImpact=[])
        if args.command in ("start", "scope"):
            if not args.paths:
                raise ValueError("scope requires explicit file paths")
            for value in args.paths:
                path = relative(value)
                if project_path(path).is_dir():
                    raise ValueError("Use explicit files, not directories")
                if path not in data["taskPaths"]:
                    data["taskPaths"].append(path)
                    data["initialFiles"][path] = {
                        "sha256": file_hash(path), "capturedAt": now(),
                        "dirty": initially_dirty(path)}
                    if VCS != "git":
                        save_base(args.task, path)
        elif args.command == "capture":
            capture(data)
        elif args.command == "register":
            if not args.items:
                raise ValueError("register requires --items")
            items = json.loads(project_path(args.items).read_text(encoding="utf-8-sig"))
            for item in items:
                if not item.get("id") or not item.get("reason"):
                    raise ValueError("Entry requires id and reason")
                item["kind"] = LEGACY_KINDS.get(item.get("kind"), item.get("kind"))
                if item["kind"] not in KINDS:
                    raise ValueError("Unknown entry kind; use one of " + ", ".join(KINDS))
                item["selector"] = normalize_selector(item["selector"])
                # 근거 경로는 제한하지 않는다. 검토 대상인 설명 파일만 범위를 확인한다.
                if not in_queue_scope(item["selector"]["path"]):
                    raise ValueError("Description file is outside profile queue_scope; record it with no-impact")
                if item["selector"]["path"] not in data["taskPaths"]:
                    raise ValueError("Description file must be in taskPaths; add it before editing")
                item["evidence"] = [normalize_selector(s) for s in item.get("evidence", [])]
                if not item["evidence"]:
                    raise ValueError("Entry requires implementation or contract evidence")
                item["snapshot"] = snapshot(item)
                item["status"] = "pending"
                item["registeredAt"] = now()
                existing = next((e for e in data["entries"] if e["id"] == item["id"]), None)
                if existing:
                    if existing.get("review"):
                        item["review"] = existing["review"]
                    data["entries"][data["entries"].index(existing)] = item
                else:
                    data["entries"].append(item)
        elif args.command == "pending" and data.get("closed"):
            # 닫힌 목록은 현재 내용과 다시 맞추지 않는다. 맞추면 이후 작업의 변경으로 항목이 다시 대기가 된다.
            print(json.dumps({"taskId": data["taskId"], "closed": data["closed"], "entries": [],
                              "outOfScopeEntries": []}, ensure_ascii=False, indent=2))
        elif args.command == "pending":
            capture(data)
            covered = {e["selector"]["path"] for e in data["entries"]}
            covered.update(s["path"] for e in data["entries"] for s in e["evidence"])
            covered.update(n["path"] for n in data["noImpact"] if n["sha256"] == file_hash(n["path"]))
            waiting = [e for e in data["entries"] if e["status"] not in ("reviewed", "retired")]
            # 범위가 생기기 전에 등록된 항목은 지우지 않고 따로 알린다. 정리는 사람이 정한다.
            print(json.dumps({"taskId": data["taskId"], "changes": data["changes"],
                              "unassignedChanges": [c for c in data["changes"] if c["path"] not in covered],
                              "noImpact": data["noImpact"],
                              "entries": [e for e in waiting if in_queue_scope(e["selector"]["path"])],
                              "outOfScopeEntries": [e for e in waiting
                                                    if not in_queue_scope(e["selector"]["path"])]},
                             ensure_ascii=False, indent=2))
        elif args.command == "no-impact":
            if not args.path or not args.note:
                raise ValueError("no-impact requires --path and --note")
            path = relative(args.path)
            if path not in data["taskPaths"]:
                raise ValueError("File must be in taskPaths")
            data["noImpact"] = [n for n in data["noImpact"] if n["path"] != path]
            data["noImpact"].append({"path": path, "sha256": file_hash(path), "reason": args.note,
                                     "recordedAt": now()})
        elif args.command == "snapshot":
            entry = get_entry(data, args.id)
            print(json.dumps(snapshot(entry), ensure_ascii=False, indent=2))
        elif args.command == "begin":
            refresh(data)
            entry = get_entry(data, args.id)
            if entry["status"] == "retired":
                raise ValueError("Entry is retired; it is no longer reviewed")
            if entry.get("locationError"):
                raise ValueError(entry["locationError"])
            # 이름을 주지 않으면 프로필의 검토 담당 이름을 쓴다. 검토 스킬이 인자를 빠뜨려도 기록이 익명이 되지 않게 한다.
            reviewer = args.reviewer or profile_value(ROOT, "reviewer") or "reviewer"
            entry["ticket"] = {"token": uuid.uuid4().hex, "snapshot": entry["snapshot"],
                               "reviewer": reviewer, "startedAt": now()}
            print(json.dumps(entry["ticket"], ensure_ascii=False, indent=2))
        elif args.command == "finish":
            entry = get_entry(data, args.id)
            ticket = entry.get("ticket", {})
            if not args.token or ticket.get("token") != args.token:
                raise ValueError("finish requires the token returned by begin")
            if not args.note:
                raise ValueError("finish requires a review result note")
            current = snapshot(entry)
            previous = ticket["snapshot"]
            if fingerprints(current)[1:] != fingerprints(previous)[1:]:
                raise ValueError("Implementation evidence changed during review; begin again")
            expected = args.description_hash or previous["description"]["sha256"]
            if current["description"]["sha256"] != expected:
                raise ValueError("Description changed; provide its final hash after reading it")
            entry["status"] = args.status
            entry["snapshot"] = current
            entry["review"] = {"reviewer": ticket["reviewer"], "finishedAt": now(),
                               "snapshot": current, "note": args.note, "status": args.status}
            entry.pop("ticket")
        elif args.command == "retire":
            if not args.id or not args.note:
                raise ValueError("retire requires --id and --note")
            entry = get_entry(data, args.id)
            if entry.get("ticket"):
                raise ValueError("Entry is under review; finish it before retiring")
            # 지난 상태와 위치 오류를 남겨 왜 폐기했는지 나중에 따라갈 수 있게 한다.
            entry["retired"] = {"at": now(), "note": args.note, "previousStatus": entry["status"],
                                "locationError": entry.pop("locationError", None)}
            entry["status"] = "retired"
        elif args.command == "close":
            if not args.note:
                raise ValueError("close requires --note")
            busy = [e["id"] for e in data["entries"] if e.get("ticket")]
            if busy:
                raise ValueError("Entries are under review; finish them before closing: " + ", ".join(busy))
            capture(data)
            unresolved = [{"id": e["id"], "status": e["status"],
                           **({"locationError": e["locationError"]} if e.get("locationError") else {})}
                          for e in data["entries"] if e["status"] not in ("reviewed", "retired")]
            if unresolved and not args.allow_unresolved:
                # 이 경우 목록을 저장하지 않는다. 남은 항목을 보여 주고 처리하거나 확인받게 한다.
                print(json.dumps({"taskId": data["taskId"], "unresolved": unresolved},
                                 ensure_ascii=False, indent=2))
                raise ValueError("Unresolved entries remain; review or retire them, or pass --allow-unresolved")
            data["closed"] = {"at": now(), "commit": data["headCommit"], "note": args.note,
                              "unresolved": unresolved}
            closed_queue = True
    if closed_queue:
        for path in remove_item_files(args.task):
            print(f"Removed input: {path.relative_to(ROOT).as_posix()}")
        folder = archive_folder(args.archive_dir)
        if folder is not None:
            moved = archive_queue(args.task, folder)
            print(f"Closed and archived: {moved.relative_to(ROOT).as_posix()}")
            return
    if args.command != "pending":
        print(f"Saved: {queue_path(args.task).relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"review_queue: {error}", file=sys.stderr)
        sys.exit(1)
