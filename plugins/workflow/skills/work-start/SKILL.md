---
name: work-start
description: "작업 세션을 시작할 때 쓴다. 나에게 배정된 진행 중 이슈, 인계 메모, 아직 커밋·제출하지 않은 변경을 가볍게 모아 짧게 알려 주고 멈춘다. 사용자가 방향을 정하면 이슈와 인계 메모의 상태 맞추기, 설계 문서 찾기, 고른 작업의 이슈 상태 전환과 인계 메모 만들기를 한다. '작업 시작', '오늘 작업 시작', '어디까지 했지', '이어서 하자', '하던 일 뭐 있지' 같은 요청에 쓴다. 이슈 트래커는 GitHub·Jira, 버전 관리는 git·Perforce 를 읽는다. 해당하지 않는 경우 — 새로 할 작업을 우선순위로 고르거나 이슈를 만드는 일(next-task), 코드 수정(feature-impl), 인계 메모 저장(context-handoff)."
when_to_use: "세션을 처음 열었을 때, 며칠 쉬었다가 하던 작업으로 돌아올 때, 진행 중인 작업이 여럿이라 무엇부터 이어 갈지 정할 때."
argument-hint: "[이슈 번호·이슈 키 또는 thread 이름]"
allowed-tools: Read, Glob, Grep, Bash(git status*), Bash(git branch*), Bash(git rev-parse*), Bash(gh issue list*), Bash(gh issue view*), Bash(p4 opened*)
---

# Work Start

세션 첫머리에 하던 일을 알려 주는 진입점이다. 먼저 짧은 브리핑만 주고 멈춘다. 상태 맞추기, 설계 문서 찾기, 작업 고르기의 후속 처리는 사용자가 방향을 정한 뒤에만 한다.

## 경로와 프로필

- 플러그인 폴더: `${CLAUDE_PLUGIN_ROOT}`. 값이 변수 이름 그대로 보이면 이 SKILL.md 의 두 단계 위 폴더다.
- 프로필: `<프로젝트 루트>/.claude/workflow/profile.md`, 개인 값은 `profile.local.md`. 쓰는 칸: `tracker`·`tracker_repo`·`tracker_project`·`tracker_site`·`tracker_query`, `status_labels`, `vcs`, `docs`(manual·plan), `threads_dir`·`archive_dir`.
- 프로필이 없으면 만들지 묻는다. 만드는 방법은 `feature-impl` 의 "경로와 프로필" 과 같다. 거절하면 버전 관리 상태만 읽고 브리핑한다.

## 공통 규칙

- 프로젝트 지침이 이 스킬보다 앞선다.
- 브리핑(1·2단계)은 읽기만 한다. 파일을 고치지 않고 이슈 트래커에 쓰지 않는다.
- 이슈 상태 전환, 라벨 변경, 댓글은 트래커에 게시하는 작업이다. 내용을 보여 주고 확인받은 뒤에만 한다.
- 버전 관리는 상태만 읽는다. `git pull`, `p4 sync` 처럼 작업 사본을 바꾸는 명령은 실행하지 않는다. 받아 와야 하면 명령만 알려 준다.

## 트래커 도구

- `github`: 로그인된 `gh` CLI 를 쓴다.
- `jira`: Atlassian MCP 서버의 도구를 쓴다. 도구 이름 앞부분(`mcp__<서버 이름>__`)은 설치 방식마다 다르다. 그래서 이름 뒷부분으로 찾는다: `searchJiraIssuesUsingJql`, `getJiraIssue`, `getTransitionsForJiraIssue`, `transitionJiraIssue`, `getAccessibleAtlassianResources`.
  - 도구 목록에 없으면 도구 검색(ToolSearch)에 이 이름을 넣어 불러온다. 서버 이름은 이 스킬과 프로필에 적지 않는다.
  - 도구가 `cloudId` 를 요구하면 `getAccessibleAtlassianResources` 로 얻는다. 사이트가 여럿이면 프로필 `tracker_site` 와 주소가 같은 것을 고른다. 도구 설명에 사이트 주소도 받는다고 적혀 있으면 `tracker_site` 를 바로 넣어도 된다.
  - 도구를 찾지 못하면 Jira 조회를 건너뛰고 브리핑에 그 사실을 한 줄로 적는다.
- `none` 이거나 비었으면 이슈 조회를 건너뛴다.

## 1. 가벼운 조회

아래 셋을 함께 모은다. 이슈마다 본문을 읽거나 설계 문서를 찾는 일은 여기서 하지 않는다.

### 1-A. 내 이슈

`github` 면 내 열린 이슈를 읽는다.

```bash
gh issue list --repo <tracker_repo> --assignee @me --state open --limit 20 --json number,title,labels,milestone,updatedAt
```

`status_labels.in_progress` 라벨이 붙은 이슈를 진행 중으로 본다. 라벨을 정하지 않았으면 열린 이슈 전체를 최근에 바뀐 순서로 본다.

`jira` 면 `searchJiraIssuesUsingJql` 을 부른다.

- JQL: 프로필 `tracker_query` 가 있으면 그 값을 쓴다. 없으면 `assignee = currentUser() AND statusCategory = "In Progress" ORDER BY priority DESC, updated DESC` 를 쓴다. `tracker_project` 가 있으면 앞에 `project = <tracker_project> AND` 를 붙인다.
- 필드: `summary`, `status`, `issuetype`, `priority`, `updated`, `parent`. 본문과 댓글은 받지 않는다.
- 최대 20건만 받는다.

### 1-B. 인계 메모

`<threads_dir>/*.md` 를 찾는다. 파일마다 머리의 `> Last updated`, `> Issue` 줄과 "다음에 할 일" 의 첫 항목만 읽는다. 마지막 활동 시각은 파일 수정 시각으로 정한다. 인계 메모의 양식과 이름 규칙은 `context-handoff` 를 따른다.

### 1-C. 버전 관리 상태

프로필 `vcs` 에 맞춰 상태만 읽는다.

| `vcs` | 명령 | 읽는 것 |
|---|---|---|
| `git` | `git branch --show-current`, `git status --short` | 현재 브랜치, 커밋하지 않은 파일 수 |
| `p4` | `p4 opened` | 열린 파일 수, 체인지리스트 번호 |

칸이 비었으면 `git rev-parse --is-inside-work-tree` 로 git 저장소인지 본다. git 저장소가 아니면 이 조회를 건너뛴다.

## 2. 브리핑

모은 것을 짧게 알려 주고 멈춘다. 질문을 늘어놓지 않는다.

인계 메모가 4개 이하면 이 형식으로 쓴다.

```
오늘 (YYYY-MM-DD)

이슈 N개
  · <이슈 키> [우선순위] <제목>
인계 메모 M개
  · <thread 이름> (<이슈 키 또는 "이슈 없음">) 마지막 활동 K일 전, 다음: <다음에 할 일 첫 항목>
미제출 변경 L개 (<브랜치 또는 체인지리스트>)

이어 갈 것: <대상> (<한 줄 이유>)
```

인계 메모가 5개 이상이면 줄여서 쓴다.

```
오늘 (YYYY-MM-DD)
이슈 N개: <키>, <키>   인계 메모 M개: <이름>, <이름>   미제출 변경 L개
이어 갈 것: <대상>
```

- 이슈 제목은 트래커의 제목을 한 줄로 줄인다. 본문은 넣지 않는다.
- "이어 갈 것" 은 이 순서로 고른다.
  1. 마지막 활동이 가장 최근인 인계 메모
  2. 인계 메모가 없으면 진행 중 이슈 가운데 우선순위가 가장 높은 것. 우선순위가 같으면 최근에 바뀐 것
  3. 둘 다 없고 `tracker` 가 `github` 면 `next-task` 로 새 작업을 고르자고 적는다
- 마지막 줄에 선택지를 한 줄로 적는다: "더 필요하면 상태 맞추기, 설계 문서 찾기, 이슈 상세, 바로 시작 가운데 말해 주세요."
- 여기서 멈추고 사용자의 말을 기다린다. 3단계로 저절로 넘어가지 않는다.

## 3. 사용자가 방향을 정한 뒤

요청받은 항목만 한다.

### 3-A. 상태 맞추기

인계 메모의 `> Issue` 줄과 트래커 상태를 비교한다. 이슈마다 `gh issue view <N> --json state,labels` 또는 `getJiraIssue` 로 상태를 읽는다.

상태는 이렇게 나눈다.

- 완료: GitHub 는 닫힌 이슈, Jira 는 상태 분류 `done`
- 진행 중: GitHub 는 `status_labels.in_progress` 라벨, Jira 는 상태 분류 `indeterminate`
- 할 일: 그 밖의 열린 이슈

| 인계 메모 | 이슈 상태 | 제안 |
|---|---|---|
| 있음 | 진행 중 | 그대로 둔다 |
| 있음 | 완료 | 메모를 보관할지 묻는다(`context-handoff` Step 4) |
| 있음 | 할 일 | 메모를 그대로 둘지 묻는다 |
| 없음 | 진행 중 | 메모를 만들지 묻는다 |
| 이슈가 적히지 않은 메모 | 없음 | 이슈와 연결할지 묻는다 |

### 3-B. 설계 문서 찾기

고른 이슈의 설계 문서를 이 순서로 찾는다.

1. 이슈 본문과 댓글에 있는 문서 링크와 경로
2. 인계 메모의 "주요 파일 및 경로" 에 적힌 문서
3. 프로필 `docs.plan` 과 `docs.manual` 폴더. 이슈 제목의 낱말로 찾고, 후보를 1~3개만 낸다. 후보마다 맞는 정도를 높음·중간·낮음으로 적는다. 높음이 없으면 후보 파일의 앞부분을 읽어 다시 판단한다.

사용자가 확정한 문서만 인계 메모의 "주요 파일 및 경로" 에 적는다. 트래커에는 적지 않는다. 사용자가 요청하면 댓글 초안을 보여 주고 확인받은 뒤에 게시한다.

### 3-C. 작업을 고른 뒤

사용자가 이슈나 인계 메모를 고르면 차례로 한다.

1. 읽기: 이슈 본문·댓글과 인계 메모 전체를 읽는다. 3-B 에서 확정한 설계 문서가 있으면 관련 항목만 읽는다.
2. 이슈 상태: 이슈가 진행 중이 아니면 진행 중으로 바꿀지 묻는다. 승인을 받으면 바꾼다.
   - `github`: `status_labels.in_progress` 라벨을 붙인다. 라벨을 정하지 않았으면 이 단계를 건너뛴다.
     ```bash
     gh issue edit <N> --repo <tracker_repo> --add-label "<라벨>"
     ```
   - `jira`: `getTransitionsForJiraIssue` 결과에서 도착 상태의 분류(`statusCategory.key`)가 `indeterminate` 인 전환을 고른다. 여럿이면 이름을 보여 주고 묻는다. 맞는 전환이 없으면 바꾸지 않고 그 사실을 알린다.
3. 인계 메모:
   - 고른 이슈의 메모가 있으면 그대로 이어 쓴다.
   - 메모가 없으면 이슈가 적히지 않은 메모 가운데 주제가 맞는 것을 찾는다. 메모 이름의 낱말, 본문, 직전 대화를 본다. 후보가 있으면 그 메모에 이슈를 연결할지 따로 만들지 묻는다. 연결하면 `> Issue` 줄을 채우고 이름을 바꿀지 묻는다.
   - 맞는 메모가 없으면 `<플러그인 폴더>/shared/thread-template.md` 로 새 메모를 만들고 경로를 알린다. 이름은 `context-handoff` Step 1 을 따른다.
4. 겹침 확인: 미제출 변경 파일이 다른 인계 메모의 "주요 파일 및 경로" 에 있으면 경고를 한 줄 적는다.
5. 넘기기: 코드를 바꾸는 일은 `feature-impl`, 새 이슈는 `next-task`, 문서만 고치는 일은 해당 문서 스킬로 넘긴다.

## 주의

- 시간이 지났다는 이유로 인계 메모를 지우거나 보관하지 않는다. 트래커 상태를 근거로 묻거나, 사용자가 요청할 때만 정리한다.
- 인증 정보와 비밀 값은 브리핑과 인계 메모에 적지 않는다.
