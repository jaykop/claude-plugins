#!/usr/bin/env bash
# workflow 훅 실행기 — 쓸 수 있는 파이썬을 찾아 주어진 스크립트에 표준 입력을 그대로 넘긴다.
# 파이썬이 없으면 아무것도 하지 않는다. 훅이 실패해서 작업을 막는 일이 없게 하려는 것이다.

script="$1"
shift
[ -f "$script" ] || exit 0

for py in python3 python; do
  # Windows 의 python3 바로 가기는 실행돼도 스토어 안내만 띄우므로 실제로 돌아가는지 확인한다.
  if command -v "$py" >/dev/null 2>&1 && "$py" -c "import sys" >/dev/null 2>&1; then
    exec "$py" "$script" "$@"
  fi
done
exit 0
