# workflow — 이슈 기반 작업 흐름

작업을 고르는 것부터 구현, 문서 반영, 커밋 전 확인, 세션 인계까지 한 흐름으로 잇는 플러그인이다. 프로젝트마다 다른 값(이슈 저장소, 문서 폴더, 빌드 명령, 검증 담당)은 프로필에서 읽는다. Claude Code 와 Codex 양쪽에서 같은 스킬을 쓴다(훅은 Claude Code 전용).

| 스킬 | 명령 | 하는 일 |
|---|---|---|
| next-task | `/workflow:next-task` | 오늘 시간에 맞는 다음 이슈 고르기, 새 이슈 초안·게시, 다시 채점 |
| feature-impl | `/workflow:feature-impl` | 규모(Small/Large), 종류(feature/improvement/bug), 위험 등급(low/mid/high)을 판별해 구현하고, 에이전트 리뷰와 체크포인트로 마무리 |
| feature-doc-sync | `/workflow:feature-doc-sync` | 영향받는 manual·devlog·plan 갱신(또는 문서 지시서 작성과 쓴 결과 대조), 이슈 결과 초안, 설명 변경 목록 정리 |
| doc-draft | `/workflow:doc-draft` | 문서 지시서의 사실만으로 manual·devlog·plan 을 쓰고, 대조에서 지적받은 문단을 다시 쓰기 |
| commit-doc-review | `/workflow:commit-doc-review` | 커밋 직전 빠진 문서 확인, `Docs-Reviewed:` 트레일러(feature-impl 작업이면 `Risk:`·`Tested:` 도) |
| context-handoff | `/workflow:context-handoff` | 작업별 인계 메모 저장·갱신 |

명령 이름을 외우지 않아도 된다. "다음 뭐 해", "이거 고쳐 줘", "문서 정리해", "커밋해", "여기까지 저장해 둬" 같은 말로도 불린다.

## 흐름

1. `next-task` 로 이슈를 고르거나 만든다.
2. `feature-impl` 이 구현한다. Small 은 바로 고치고, Large 는 요구 정리 → 탐색 → 계획(결정 카드) → 결정 확정 → 구현 → 에이전트 리뷰 → 테스트 가이드 순서다.
3. 끝나면 체크포인트가 문서화(`feature-doc-sync`), 커밋(`commit-doc-review`), 이슈 상태, 인계(`context-handoff`)를 차례로 제안한다.

빌드·테스트·검사는 기본적으로 사용자가 맡는다(프로필 `verification: user`). 스킬은 요청이 있을 때만 실행한다. 코드를 읽기만 하는 에이전트 리뷰는 이와 별개로 `agent_review` 칸을 따른다. 커밋, 이슈 게시, 라벨 변경은 언제나 초안을 보여 주고 확인받은 뒤에 한다.

### 리뷰 방식

사람이 모든 줄을 읽는 대신, 무엇이 깨질 수 있고 무엇이 그걸 잡는지를 기준으로 사람이 볼 범위를 줄인다.

- **위험 등급**: 변경 자체로 정한다. 프로필 `risk_paths` 의 `high`·`low` 경로와, 경로와 무관한 기준(저장 데이터 형식, 빌드·CI, 데이터 삭제, 공용 구조 신설)으로 판별하고 나머지 코드는 mid 다.
- **결정 카드**: Large 계획은 의도, 사용자가 답할 결정, 깨질 수 있는 것과 확인 방법, 테스트 후보, 조각만 대화에 낸다. 파일 표는 인계 메모에 둔다. 테스트 후보는 프로필 `test_candidates` 기준에 드는 코드만 올리고, 테스트 코드는 사용자가 고른 것만 쓴다. 결정이 많거나 카드가 한 화면을 넘으면 따로 빌드·테스트·커밋할 수 있는 조각으로 나눈다.
- **에이전트 리뷰**: 사람보다 먼저 맥락 없는 서브에이전트가 본다. low 는 생략, mid 는 리뷰어 1명, high 는 2명 병렬과 검증자 1명이다. `verification: user` 면 빌드 요청 전에 리뷰해서 빌드 한 번으로 확인한다. 2차 이후는 변경분만 보고, 3차 뒤에도 문제가 남으면 멈추고 묻는다. 절차는 [shared/review-brief.md](shared/review-brief.md).
- **리뷰 패킷**: 리뷰가 끝나면 볼 곳(파일:줄), 리뷰가 찾은 것과 처리, 검사로 못 잡는 것만 보여 준다.
- **커밋 증거**: 커밋 메시지에 `Risk:`, `Tested:`(확인하지 않은 것 포함), 필요하면 `Revert:` 를 남긴다.

프로젝트의 실패 유형을 적은 리뷰 지침(`REVIEW.md` 등, 양식 [shared/review-guide-template.md](shared/review-guide-template.md))을 프로필 `review_guide` 에 연결하면 리뷰가 그 항목을 하나씩 대조한다. 리뷰를 통과한 코드에서 버그가 나오면 지침의 "놓친 버그 기록"에 적고 실패 유형에 반영한다.

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

그다음 Codex 앱의 플러그인 화면에서 `workflow` 를 설치한다. 업데이트 방법은 [리포 README](../../README.md#업데이트) 를 따른다.

주석·문서 설명의 교차 검토까지 쓰려면 [ko-review](../ko-review/README.md) 도 설치하고 프로필에서 `description_review: true` 로 켠다.

### 문서를 다른 AI 에게 쓰게 하기

프로필 `doc_writer: codex` 로 두면 문서 작성을 나눈다. 구현한 AI 는 대화와 구현을 알기 때문에 사실을 모으고, 다른 AI 는 문장을 쓴다.

1. 구현한 쪽이 `feature-doc-sync` 에서 문서 대신 지시서(`<threads_dir>/<작업 ID>.docbrief.md`, 양식 [shared/docbrief-template.md](shared/docbrief-template.md))를 쓴다. 지시서에는 사실·결정·확인 상태·미확정 사항만 근거와 함께 적고, 문장은 쓰지 않는다.
2. 쓰는 쪽이 `doc-draft` 로 지시서의 사실만 써서 문서를 만든다. 지시서에 없는 동작·한계는 쓰지 않는다.
3. 구현한 쪽이 쓴 결과를 지시서·코드와 대조한다. 문장은 고치지 않고 틀린 위치만 적어 한 번 다시 쓰게 한다. 그 뒤에도 남은 문제는 사용자에게 보여 준다.

언제, 어떤 명령으로 다른 AI 에게 넘길지는 플러그인이 정하지 않는다. 프로젝트 지침에 적는다.

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

### 리뷰와 테스트를 맞추는 값

비워 둬도 동작한다. 비우면 경로와 무관한 기본 기준으로만 위험 등급을 정하고, 리뷰 지침 없이 리뷰하고, 테스트 후보를 내지 않는다.

| 칸 | 내용 |
|---|---|
| `risk_paths.high`, `risk_paths.low` | 위험 등급을 정하는 경로(glob). 어디에도 걸리지 않는 코드는 mid |
| `agent_review` | false 면 에이전트 리뷰를 끈다. 칸이 없으면 켜진 것으로 본다 |
| `review_guide` | 리뷰가 대조할 실패 유형 문서 |
| `test_candidates` | 결정 카드에 자동화 테스트 후보로 올릴 코드의 기준. 비우면 후보 절을 뺀다 |

## 훅 (Claude Code)

두 훅 모두 **프로필이 있는 프로젝트에서, 프로필로 켰을 때만** 동작한다. 플러그인을 설치했다고 다른 프로젝트의 커밋이 막히지 않는다. 프로필이 없는 프로젝트에서는 `run-py.sh` 가 파이썬을 띄우기 전에 끝내고, 커밋 검사 훅은 `git` 명령에만 실행된다(훅 정의의 `if` 필터). 그래서 셸 명령마다 드는 지연이 거의 없다.

| 훅 | 켜는 칸 | 동작 |
|---|---|---|
| PreToolUse (Bash·PowerShell) | `commit_gate: true` | `git commit` 명령에 `commit_trailer`(기본 `Docs-Reviewed:`)가 없으면 막고 `commit-doc-review` 를 거치게 한다. 에이전트의 커밋에만 적용되고 사용자가 터미널에서 직접 하는 커밋에는 영향이 없다 |
| Stop | `handoff_reminder_turns: N` (1 이상) | 세션 턴이 N 의 배수가 될 때 `context-handoff` 를 권한다. 턴 수는 `~/.claude/_hook_state/workflow/` 에 둔다 |

Codex 에서 같은 동작이 필요하면 프로젝트의 `.codex/hooks.json` 에서 Claude Code 마켓플레이스 사본의 스크립트(`~/.claude/plugins/marketplaces/jaykop/plugins/workflow/hooks/commit_gate.py`, `handoff_reminder.py`)를 `python` 으로 실행하게 연결한다. Codex 플러그인 사본은 버전마다 경로가 바뀌므로 쓰지 않는다. 훅 정의를 바꾸면 Codex 의 `/hooks` 에서 다시 승인해야 한다.

## 우선순위 등급

`next-task` 는 중요도(`priority: must/should/could`)와 규모(`size: S/M/L/XL`) 라벨의 곱으로 등급을 매기고, Blocked by 관계로 등급을 물려준 뒤 마일스톤별 순서를 낸다. 규칙과 출력 읽는 법은 [shared/priority-scheme.md](shared/priority-scheme.md) 에 있다. 계산은 `scripts/issue_priority.py` 가 한다.

## 구성

```
plugins/workflow/
├─ .claude-plugin/plugin.json   Claude Code 매니페스트
├─ .codex-plugin/plugin.json    Codex 매니페스트 (같은 skills/ 를 쓴다)
├─ skills/        next-task, feature-impl, feature-doc-sync, doc-draft, commit-doc-review, context-handoff
├─ hooks/         hooks.json, run-py.sh, commit_gate.py, handoff_reminder.py
├─ scripts/       issue_priority.py, profile_reader.py
└─ shared/        프로필 양식, 개인 프로필 양식, 등급 체계, 인계 메모 양식, 문서 지시서 양식, 리뷰 지시서, 리뷰 지침 양식
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
- **에이전트 리뷰는 코드를 읽기만 한다.** 실행해야 드러나는 문제는 빌드·테스트 가이드의 몫이다. 서브에이전트를 쓸 수 없는 환경에서는 구현한 에이전트가 직접 리뷰하고, 리뷰 패킷에 그 사실을 적는다.
- **리뷰 결과가 나빠져도 위험 기준이 자동으로 엄격해지지 않는다.** 놓친 버그 기록을 보고 `risk_paths` 와 리뷰 지침을 사람이 고친다.
- **Codex 플러그인 훅은 쓰지 않는다.** Codex 에서는 위 훅 단락처럼 프로젝트의 `.codex/hooks.json` 으로 연결한다. 이 연결은 같은 PC 의 Claude Code 에 이 마켓플레이스가 추가돼 있어야 동작한다.
