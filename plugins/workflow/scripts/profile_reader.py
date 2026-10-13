"""workflow 프로필의 최상위 `키: 값` 한 줄을 읽는다. 훅과 스크립트가 함께 쓴다.

프로필은 <프로젝트 루트>/.claude/workflow/profile.md, 개인 값은 같은 폴더의 profile.local.md 다.
머리(--- 사이)의 들여쓰지 않은 줄만 읽고, 목록·하위 항목은 해석하지 않는다(스킬이 직접 읽는다).
"""

import os
import re
import subprocess
from pathlib import Path

PROFILE = Path(".claude/workflow/profile.md")
LOCAL_PROFILE = Path(".claude/workflow/profile.local.md")


def project_root(hint=None):
    """훅 입력의 cwd, CLAUDE_PROJECT_DIR, git 최상위, 현재 폴더 순으로 프로젝트 루트를 정한다."""
    for candidate in (os.environ.get("CLAUDE_PROJECT_DIR"), hint):
        if candidate and Path(candidate).is_dir():
            return Path(candidate).resolve()
    try:
        top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                      encoding="utf-8", stderr=subprocess.DEVNULL).strip()
        if top:
            return Path(top).resolve()
    except (OSError, subprocess.CalledProcessError):
        pass
    return Path.cwd().resolve()


def read_front(path):
    values = {}
    if not path.is_file():
        return values
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return values
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z_][\w.-]*):\s*(.*)$", line)
        if match:
            value = re.sub(r"\s+#.*$", "", match.group(2)).strip().strip("'\"")
            values[match.group(1)] = value
    return values


def load(root):
    """프로필이 없으면 None. 있으면 개인 값을 덮어쓴 dict."""
    shared = root / PROFILE
    if not shared.is_file():
        return None
    values = read_front(shared)
    values.update({k: v for k, v in read_front(root / LOCAL_PROFILE).items() if v != ""})
    return values


def flag(values, key, default=False):
    if not values or values.get(key, "") == "":
        return default
    return values[key].lower() in ("true", "yes", "on", "1")


def number(values, key, default=0):
    try:
        return int(values.get(key, "")) if values else default
    except ValueError:
        return default
