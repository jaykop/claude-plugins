# workflow — 이슈 기반 작업 흐름

작업을 고르는 것부터 구현, 문서 반영, 커밋 전 확인, 세션 인계까지 한 흐름으로 잇는 플러그인이다. 프로젝트마다 다른 값(이슈 저장소, 문서 폴더, 빌드 명령, 검증 담당)은 프로필에서 읽는다. Claude Code 와 Codex 양쪽에서 같은 스킬을 쓴다(훅은 Claude Code 전용).

| 스킬 | 명령 | 하는 일 |
|---|---|---|
| next-task | `/workflow:next-task` | 오늘 시간에 맞는 다음 이슈 고르기, 새 이슈 초안·게시, 다시 채점 |
| feature-impl | `/workflow:feature-impl` | 규모(Small/Large)와 종류(feature/improvement/bug)를 판별해 구현하고 체크포인트로 마무리 |
| feature-doc-sync | `/workflow:feature-doc-sync` | 영향받는 manual·devlog·plan 갱신, 이슈 결과 초안, 설명 변경 목록 정리 |
| commit-doc-review | `/workflow:commit-doc-review` | 커밋 직전 빠진 문서 확인, `Docs-Reviewed:` 트레일러 |
| context-handoff | `/workflow:context-handoff` | 작업별 인계 메모 저장·갱신 |

명령 이름을 외우지 않아도 된다. "다음 뭐 해", "이거 고쳐 줘", "문서 정리해", "커밋해", "여기까지 저장해 둬" 같은 말로도 불린다.

## 흐름

1. `next-task` 로 이슈를 고르거나 만든다.
2. `feature-impl` 이 구현한다. Small 은 바로 고치고, Large 는 요구 정리 → 탐색 → 계획 → 피드백 → 구현 → 테스트 가이드 순서다.
3. 끝나면 체크포인트가 문서화(`feature-doc-sync`), 커밋(`commit-doc-review`), 이슈 상태, 인계(`context-handoff`)를 차례로 제안한다.

빌드·테스트·검사는 기본적으로 사용자가 맡는다(프로필 `verification: user`). 스킬은 요청이 있을 때만 실행한다. 커밋, 이슈 게시, 라벨 변경은 언제나 초안을 보여 주고 확인받은 뒤에 한다.

## 설치

Claude Code:

```
/plugin marketplace add jaykop/claude-plugins
/plugin install workflow@jaykop
```

Codex:

```
codex plugin marketplace add jaykop/claude-plugins
```

그다음 Codex 의 플러그인 화면에서 `workflow` 를 설치한다. Codex 쪽 설치 절차는 아직 실제로 확인하지 않았다.

주석·문서 설명의 교차 검토까지 쓰려면 [ko-review](../ko-review/README.md) 도 설치하고 프로필에서 `description_review: true` 로 켠다.

## 프로젝트 설정

| 파일 | 내용 | 버전 관리 |
|---|---|---|
| `.claude/workflow/profile.md` | 팀과 공유하는 값. 양식 [shared/profile-template.md](shared/profile-template.md) | 올린다 |
| `.claude/workflow/profile.local.md` | 개인 값(하루 작업 가능 시간 등). 양식 [shared/profile-local-template.md](shared/profile-local-template.md) | 올리지 않는다 |

`feature-impl` 이나 `context-handoff` 를 처음 부르면 프로필이 없을 때 만들지 묻는다. 프로젝트 지침(`AGENTS.md` 등)에서 알 수 있는 값은 채우고 모르는 값만 묻는다.

### 꼭 직접 정해야 하는 값

| 칸 | 왜 필요한가 |
|---|---|
| `instructions`, `scope_sections`, `coding_rules` | 스킬이 규칙을 복사하지 않고 매번 지침의 해당 위치를 읽는다 |
| `tracker`, `tracker_repo`, `tracker_public` | 이슈 연동 여부와 공개 저장소 주의 사항. `next-task` 는 `github` 일 때만 동작한다 |
| `threads_dir` | 인계 메모 위치. 공개 저장소면 버전 관리에서 빠지는 폴더여야 한다 |
| `verification` | `user` 면 빌드·테스트를 사용자가 맡는다 |
| 본문 "변경 → 문서 대응표" | 커밋 전 검토할 문서를 고르는 표 |

## 훅 (Claude Code)

두 훅 모두 **프로필이 있는 프로젝트에서, 프로필로 켰을 때만** 동작한다. 플러그인을 설치했다고 다른 프로젝트의 커밋이 막히지 않는다.

| 훅 | 켜는 칸 | 동작 |
|---|---|---|
| PreToolUse (Bash·PowerShell) | `commit_gate: true` | `git commit` 명령에 `commit_trailer`(기본 `Docs-Reviewed:`)가 없으면 막고 `commit-doc-review` 를 거치게 한다. 에이전트의 커밋에만 적용되고 사용자가 터미널에서 직접 하는 커밋에는 영향이 없다 |
| Stop | `handoff_reminder_turns: N` (1 이상) | 세션 턴이 N 의 배수가 될 때 `context-handoff` 를 권한다. 턴 수는 `~/.claude/_hook_state/workflow/` 에 둔다 |

Codex 에서 같은 동작이 필요하면 프로젝트의 `.codex/hooks.json` 에 직접 연결한다. Codex 플러그인 훅은 아직 다루지 않는다.

## 우선순위 등급

`next-task` 는 중요도(`priority: must/should/could`)와 규모(`size: S/M/L/XL`) 라벨의 곱으로 등급을 매기고, Blocked by 관계로 등급을 물려준 뒤 마일스톤별 순서를 낸다. 규칙과 출력 읽는 법은 [shared/priority-scheme.md](shared/priority-scheme.md) 에 있다. 계산은 `scripts/issue_priority.py` 가 한다.

## 구성

```
plugins/workflow/
├─ .claude-plugin/plugin.json   Claude Code 매니페스트
├─ .codex-plugin/plugin.json    Codex 매니페스트 (같은 skills/ 를 쓴다)
├─ skills/        next-task, feature-impl, feature-doc-sync, commit-doc-review, context-handoff
├─ hooks/         hooks.json, run-py.sh, commit_gate.py, handoff_reminder.py
├─ scripts/       issue_priority.py, profile_reader.py
└─ shared/        프로필 양식, 개인 프로필 양식, 등급 체계, 인계 메모 양식
```

## 필요한 것

- Claude Code 또는 Codex
- Python 3.8 이상 (표준 라이브러리만 쓴다)
- git
- `next-task` 와 이슈 연동: 로그인된 `gh` CLI
- 훅: bash. Windows 에서는 Git Bash 가 필요하다

## 알려진 한계

- **이슈 트래커는 GitHub 만 다룬다.** 다른 트래커는 `tracker: none` 으로 두면 이슈 단계를 건너뛴다.
- **훅은 맥락 사용량을 모른다.** 인계 권유는 턴 수를 대신 쓴다.
- **Codex 설치와 훅은 아직 확인 전이다.** 스킬은 같은 파일을 쓰지만, 이 리포를 Codex 마켓플레이스로 추가해 설치하는 과정과 Codex 플러그인 훅은 시험하지 않았다.
