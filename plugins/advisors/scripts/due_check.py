#!/usr/bin/env python3
"""고문 점검 가운데 때가 된 것과 열린 질문을 찾아 한 줄로 알린다.

읽기만 한다. 프로젝트에 고문 프로필이 없거나 알릴 것이 없으면 아무것도 출력하지 않는다.

- 기본 출력: 사람이 읽는 목록
- --hook: Claude Code SessionStart 훅 형식(JSON) — 알릴 것이 있을 때만
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 고문 목록은 이 플러그인의 skills/ 아래 폴더 이름이다. 고문을 더해도 이 파일은 고치지 않는다.
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEXT_RE = re.compile(r"^\s*다음 점검:\s*(\d{4}-\d{2}-\d{2})", re.M)
# 마일스톤 기준 형식: "다음 점검: 마일스톤 14일 전" — 프로필 next_milestone 의 날짜에서 뺀다
MILESTONE_RE = re.compile(r"^\s*다음 점검:\s*마일스톤\s*(\d+)\s*일\s*전", re.M)
MILESTONE_DATE_RE = re.compile(r"^next_milestone:[^#\n]*?(\d{4}-\d{2}-\d{2})", re.M)  # 주석(#) 속 예시 날짜는 읽지 않는다
LAST_UPDATE_RE = re.compile(r"마지막 갱신:\s*(\d{4}-\d{2}-\d{2})")
REPORT_DIR_RE = re.compile(r"^report_dir:\s*(.*?)\s*(#.*)?$", re.M)


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except OSError:
        return None


def resolve_report_dir(project_root, profile_text):
    m = REPORT_DIR_RE.search(profile_text)
    value = (m.group(1).strip().strip("'\"") if m else "") or ".claude/advisors/reports"
    if not os.path.isabs(value):
        value = os.path.join(project_root, value)
    return os.path.normpath(value)


def advisor_keys():
    skills = os.path.join(PLUGIN_ROOT, "skills")
    try:
        names = os.listdir(skills)
    except OSError:
        return set()
    return {n for n in names if os.path.isfile(os.path.join(skills, n, "SKILL.md"))}


def plugin_name():
    try:
        with open(os.path.join(PLUGIN_ROOT, ".claude-plugin", "plugin.json"), "r", encoding="utf-8") as f:
            return json.load(f).get("name") or "advisors"
    except (OSError, ValueError):
        return "advisors"


def owner_of(state_file, keys):
    """파일 이름이 '<고문>-' 으로 시작하는 _state 파일만 그 고문의 점검 파일이다(source-checks 같은 공용 파일은 빠진다)."""
    name = os.path.basename(state_file)
    # 이름이 겹치면(design, design-review) 가장 긴 이름이 주인이다
    return max((k for k in keys if name.startswith(k + "-")), key=len, default=None)


def open_questions(inbox_text):
    """받는 고문별 '열림' 질문 수."""
    counts = {}
    for line in inbox_text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8 or not cells[0].startswith("Q-"):
            continue
        receiver, status = cells[3], cells[7]
        if status == "열림":
            counts[receiver] = counts.get(receiver, 0) + 1
    return counts


def main():
    ap = argparse.ArgumentParser(description="때가 된 고문 점검과 열린 질문을 알린다 (읽기 전용).")
    ap.add_argument("project_root", nargs="?", help="프로젝트 루트. 없으면 CLAUDE_PROJECT_DIR 또는 현재 폴더")
    ap.add_argument("--today", help="오늘 날짜 YYYY-MM-DD (시험용)")
    ap.add_argument("--hook", action="store_true", help="SessionStart 훅 JSON 으로 출력")
    args = ap.parse_args()

    root = args.project_root or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    profile = os.path.join(root, ".claude", "advisors", "profile.md")
    profile_text = read_text(profile)
    if profile_text is None:
        return 0  # 고문을 쓰지 않는 프로젝트 — 조용히 끝낸다

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    keys = advisor_keys()
    plugin = plugin_name()

    def label(key):
        return "/{}:{}".format(plugin, key) if key in keys else key

    state_dir = os.path.join(resolve_report_dir(root, profile_text), "_state")
    items = []

    try:
        names = sorted(os.listdir(state_dir))
    except OSError:
        names = []
    for name in names:
        if not name.endswith(".md") or name == "inbox.md":
            continue
        text = read_text(os.path.join(state_dir, name)) or ""
        key = owner_of(name, keys)
        if not key:
            continue
        m = NEXT_RE.search(text)
        due = None
        if m:
            try:
                due = dt.date.fromisoformat(m.group(1))
            except ValueError:
                due = None
        else:
            mm = MILESTONE_RE.search(text)
            md = MILESTONE_DATE_RE.search(profile_text)
            if mm and md:
                try:
                    due = dt.date.fromisoformat(md.group(1)) - dt.timedelta(days=int(mm.group(1)))
                except ValueError:
                    due = None
                # 알림 시작일 이후에 이미 갱신(점검)했으면 다시 알리지 않는다
                lu = LAST_UPDATE_RE.search(text)
                if due is not None and lu:
                    try:
                        if dt.date.fromisoformat(lu.group(1)) >= due:
                            due = None
                    except ValueError:
                        pass
        if due is None:
            continue
        if due <= today:
            items.append("{} 점검 예정일 {} 지남 ({})".format(label(key), due.isoformat(), name))

    inbox = read_text(os.path.join(state_dir, "inbox.md"))
    if inbox:
        for receiver, n in sorted(open_questions(inbox).items()):
            items.append("{} 앞으로 열린 질문 {}건".format(label(receiver), n))

    # 같은 고문의 _state 파일이 여러 개면 중복 알림을 줄인다
    seen, unique = set(), []
    for it in items:
        head = it.split(" 점검 예정일")[0]
        if " 점검 예정일" in it and head in seen:
            continue
        seen.add(head)
        unique.append(it)

    if not unique:
        return 0

    if args.hook:
        msg = (
            "## advisors 알림\n\n"
            "고문 점검 가운데 때가 된 것이 있다: " + "; ".join(unique) + ".\n\n"
            "사용자의 첫 요청을 먼저 처리한다. 적당한 때 이 내용을 한 줄로만 알리고, 할지 묻는다. "
            "같은 세션에서 다시 꺼내지 않는다. 사용자가 원하지 않으면 그대로 둔다."
        )
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": msg}}, ensure_ascii=False))
    else:
        for it in unique:
            print("- " + it)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # 훅이 세션 시작을 막지 않게 한다
        if "--hook" not in sys.argv:
            print("오류: " + str(e), file=sys.stderr)
        sys.exit(0)
