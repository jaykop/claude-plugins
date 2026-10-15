"""PreToolUse 훅: 문서 검토 트레일러가 없는 git commit 을 막는다.

프로필(.claude/workflow/profile.md)이 있고 `commit_gate: true` 인 프로젝트에서만 동작한다.
Bash·PowerShell 명령에 `git commit` 이 들어 있고 트레일러(기본 `Docs-Reviewed:`)가 없으면
커밋을 거부하고 commit-doc-review 스킬을 거치라고 알린다. 훅은 트레일러가 있는지만 본다.
실제 검토는 스킬이 맡는다.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import profile_reader  # noqa: E402

COMMIT_RE = re.compile(r"\bgit(?:\s+-[cC]\s+\S+)*\s+commit\b")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    command = (data.get("tool_input") or {}).get("command") or ""
    if not COMMIT_RE.search(command):
        return 0

    profile = profile_reader.load(profile_reader.project_root(data.get("cwd")))
    if not profile_reader.flag(profile, "commit_gate"):
        return 0
    trailer = profile.get("commit_trailer") or "Docs-Reviewed:"
    if trailer in command:
        return 0

    reason = (
        "커밋 전 문서 검토가 필요하다. workflow 플러그인의 commit-doc-review 스킬로 이번 커밋과 관련된 문서의 "
        "반영 여부를 검토하고 사용자에게 보고한 뒤, 커밋 메시지 트레일러에 '{0} <검토 결과 요약>' 한 줄을 넣어 "
        "다시 커밋한다. 검토 없이 트레일러만 붙이지 않는다.".format(trailer)
    )
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
        ensure_ascii=False,
    )
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
