# agent-playtest — 에이전트 기능 확인

Unreal 프로젝트에서 에이전트가 이슈의 완료 조건이나 테스트 가이드를 PIE에서 직접 확인하는 절차다. 게임 안 동작은 엔진 플러그인 `AgentPlaytest`의 MCP 도구가 담당한다. 이 도구는 이름 있는 동작(Verb)을 플레이어 입력으로 주입하고, 게임 상태를 JSON으로 읽고, JSON 시나리오를 프레임 단위로 실행한다. 이 스킬은 그 앞뒤를 담당한다. 확인 항목을 나누고, 시나리오를 실행하고, 근거를 붙여 판정하고, 리포트와 댓글 초안을 작성한다.

```
/plugin install agent-playtest@jaykop
```

| 스킬 | 명령 | 하는 일 |
|---|---|---|
| check | `/agent-playtest:check` | 이슈 완료 조건·테스트 가이드 → 시나리오 → 실행 → 판정 → 리포트와 댓글 초안 |

```
/agent-playtest:check #308
/agent-playtest:check #308 1 2 5
```

## 필요한 것

- 프로젝트에 엔진 플러그인 `AgentPlaytest`가 있고 Editor 타겟에서 활성화되어 있다. 동작 목록(Verb Set) Data Asset과 관찰할 Attribute를 프로젝트 설정에 지정한다. 이 플러그인의 사용법은 그 프로젝트의 매뉴얼을 따른다.
- 엔진 Experimental 플러그인 `ModelContextProtocol`, `ToolsetRegistry`가 활성화되어 있고, Claude Code가 에디터의 MCP 서버에 연결되어 있다.
- 시나리오 작성법과 판정 기준은 엔진 플러그인 안의 Agent Skill(`/Script/AgentPlaytestEditor.AgentPlaytestSkill`)에 있다. 이 스킬은 실행 전에 그 내용을 읽는다. 그래서 MCP 클라이언트가 Claude Code가 아니어도 같은 작성법을 사용할 수 있다.

## 판정

항목마다 통과, 실패, 판단 불가 중 하나로 판정하고, 통과에는 이번 실행의 근거(관찰 값, 로그 줄, 캡처)를 붙인다. 조작감, 연출, 재미는 판정하지 않고 사람이 확인할 목록으로 분류한다. 에이전트의 확인은 사용자 확인을 대신하지 않는다.

## 이 플러그인에 없는 것

- **게임 코드 수정과 테스트 코드 작성.** 실패한 항목은 리포트에 기록한다. 구현은 `workflow`의 `feature-impl`이 담당한다.
- **게시.** 이슈 댓글은 초안까지만 작성하고, 사용자가 확인한 후 게시한다.
- **자율 플레이.** 목표만 받아 스스로 플레이하는 테스트는 다루지 않는다.

## 프로젝트 프로필

프로젝트마다 다른 값은 `.claude/agent-playtest/profile.md`에 둔다. 양식은 [shared/profile-template.md](shared/profile-template.md)다.

| 키 | 내용 |
|---|---|
| `test_level` | 에이전트 확인에 사용하는 레벨 |
| `report_dir` | 리포트 위치. 인계 메모 폴더(`threads_dir`)에는 두지 않는다. 다른 스킬이 그 폴더의 모든 파일을 인계 메모로 읽기 때문이다 |
| `language` | 리포트와 댓글 초안의 언어 |
| `tracker_public` | true면 댓글 초안에서 로컬 경로를 뺀다 |
| `Project notes` 절 | 도구로 알 수 없는 게임 사실: 디버그 로그 명령, 치트와 사전 조건, 입력 기준, 테스트 레벨 정보 |
