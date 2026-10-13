"""Stop 훅: 세션의 턴 수가 정한 배수에 닿으면 context-handoff 를 권한다.

프로필(.claude/workflow/profile.md)이 있고 `handoff_reminder_turns` 가 1 이상인 프로젝트에서만 동작한다.
훅에서는 정확한 맥락 사용량을 알 수 없으므로 턴 수를 대신 쓴다.
턴 수는 ~/.claude/_hook_state/workflow/turn_<세션 id> 에 둔다.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import profile_reader  # noqa: E402


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    profile = profile_reader.load(profile_reader.project_root(data.get("cwd")))
    every = profile_reader.number(profile, "handoff_reminder_turns", 0)
    if every <= 0:
        return 0

    session = re.sub(r"[^\w.-]", "_", str(data.get("session_id") or "default"))
    state = Path.home() / ".claude" / "_hook_state" / "workflow"
    try:
        state.mkdir(parents=True, exist_ok=True)
        counter = state / ("turn_" + session)
        turns = int(counter.read_text(encoding="utf-8") or 0) if counter.is_file() else 0
        turns += 1
        counter.write_text(str(turns), encoding="utf-8")
    except (OSError, ValueError):
        return 0

    if turns % every:
        return 0
    json.dump(
        {
            "systemMessage": "세션 턴 {0}회 — context-handoff 로 인계 메모 갱신을 고려해 보세요.".format(turns),
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": (
                    "이번 세션이 길어졌다({0}턴). 사용자가 다음 작업으로 넘어가거나 마무리할 시점이면 "
                    "workflow 플러그인의 context-handoff 실행을 제안한다. 인계 메모를 갱신해 두면 다음 세션에서 "
                    "맥락을 잃지 않고 이어 갈 수 있다.".format(turns)
                ),
            },
        },
        sys.stdout,
        ensure_ascii=False,
    )
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
