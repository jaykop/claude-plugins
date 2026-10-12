#!/usr/bin/env bash
# SessionStart 훅 — 이 프로젝트에 고문 프로필이 있고 때가 된 점검이나 열린 질문이 있을 때만 한 줄 알림을 넣는다.
# 프로필이 없거나 파이썬이 없으면 아무것도 하지 않는다.

script="$1"
[ -f "$script" ] || exit 0

root="${CLAUDE_PROJECT_DIR:-$PWD}"
[ -f "$root/.claude/advisors/profile.md" ] || exit 0

for py in python3 python; do
  if command -v "$py" >/dev/null 2>&1 && "$py" -c "import sys" >/dev/null 2>&1; then
    "$py" "$script" "$root" --hook 2>/dev/null
    exit 0
  fi
done
exit 0
