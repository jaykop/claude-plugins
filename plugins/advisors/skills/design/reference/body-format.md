# Design advisor report body format

The common head and section order follow `shared/report-base.md`. This file decides what goes in the "## Body" (본문) place of that format, and what to write in the "Scope" (범위) field of the head.
Read it in area diagnosis Step A4 and in single review Step B4.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## The "Scope" field of the head

Write each of the following on its own line, only when it applies.

- Mode and target: `Area diagnosis — <area name> (<area folder or area file pattern>)` (`영역 진단 — <영역 이름> (<영역 폴더 또는 영역 파일 패턴>)`) or `Single review — <target in one line>` (`단건 심사 — <대상 한 줄>`)
- Design documents read / limit: `Design documents read 32 / limit 40, over the limit 12` (`읽은 기획서 32 / 상한 40, 상한 초과 12`)
- `based on draft principles` (`가안 기준`) — when the principles are a draft
- `principles not confirmed — no verdicts` (`원칙 미확정 — 판정 없음`) — when there are no principles or they were not confirmed
- `no-numeric-evidence stage` (`수치 근거 없음 단계`) — when the data is placeholder values
- `reference option` (`참고 선택지`) — when the user is not the design decision owner
- `collected in the main conversation without agents` (`에이전트 없이 메인에서 수집함`) — when subagents could not be called

The report title is `# Design advisor area diagnosis — YYYY-MM-DD` (`# 기획 고문 영역 진단 — YYYY-MM-DD`) or `# Design advisor single review — YYYY-MM-DD` (`# 기획 고문 단건 심사 — YYYY-MM-DD`).

---

## Area diagnosis body

```markdown
## Body (본문)

### 0. Basis (기준)
- Principles (원칙): <document:paragraph> / status confirmed (확정) · draft (가안) / confirmation record <the date and revision in profile design.principles_confirmed. If empty, "none" (없음)> / principle document changes after that <yes (있음) · no (없음) · not checked (확인 못 함)>
- Data status (데이터 상태): confirmed (확정) / placeholder values (임시값)
- Evidence grade marks (근거 등급 표시): [observed-behavior] ([관찰-행동]) [observed-opinion] ([관찰-의견]) [calculated] ([계산]) [document] ([문서]) [document-intent] ([문서-의도]) [estimated] ([추정])
- Checks not run (돌리지 않은 점검): <framework name>: no input material (needed: …) (<틀 이름>: 입력 자료 없음(필요한 것: …))   ← only when it applies, one line each

### 1. At a glance (한눈에 보기)
| Rank (순위) | Proposal ID (제안 ID) | Kind (종류) | One-line summary (한 줄 요약) | Fun contribution (재미 기여도) | Cost (비용) | Strongest evidence grade (가장 강한 근거 등급) |
|---|---|---|---|---|---|---|
(At most 5 rows. If the conclusion is "no change" (변경 없음), write that)

### 2. Material list (자료 목록)
| Category (구분) | Material (자료) | Location (위치) | Date (evidence) (날짜(근거)) | Mark (표시) |
|---|---|---|---|---|
Category: read (읽음) / not read (over the limit, format) (못 읽음(상한 초과·형식)) / left out of evidence (deprecated mark, reference material) (근거에서 뺌(폐기 표시·참고 자료))
Mark: written before principle revision (원칙 개정 이전 작성), date unknown (날짜 미상), summary document (요약 문서), and so on

### 3. Core loop map (핵심 반복 구조 지도)
| Unit (단위) | Action (행동) | Feedback (피드백) | Reward (보상) | Reason for the next action (다음 행동의 이유) | Implementation stage (구현 단계) | Evidence (근거) |
|---|---|---|---|---|---|---|
| moment (순간) | | | | | | |
| one round (한 판) | | | | | | |
| long term (장기) | | | | | | |
#### Broken loops (끊긴 고리)
#### Systems not attached to any loop (어느 고리에도 붙지 않은 시스템)

### 4. Differences between the design documents and the implementation (facts only, no verdicts) (기획서와 구현의 차이 (사실만, 판정 없음))
| Item (항목) | Design document (기획서) | Implementation (code, data) (구현(코드·데이터)) | Location (위치) | Question for the user (사용자 확인 질문) |
|---|---|---|---|---|
Difference kinds (차이 종류): only in the documents (문서에만 있음) / only in the implementation (구현에만 있음) / different values (값이 다름)

### 5. Per-system diagnosis (시스템별 진단)
| System (시스템) | Linked principle (연결 원칙) | Attached loop (붙은 고리) | Checklist (체크리스트) | Choice (선택) | Risk-reward (위험-보상) | Role overlap (역할 중복) | Mechanisms (메카닉) | Implementation stage (구현 단계) | Evidence grade (근거 등급) | Verdict (판정) |
|---|---|---|---|---|---|---|---|---|---|---|
(Leave the columns of checks that were not run out of the table)

### 6. Removal, merge, on hold, and modify proposals (제거·통합·보류·수정 제안)
Proposal cards (format below) in this order: removal and merge → on hold → modify structure → modify numbers

### 7. Additional proposals (추가 제안)
Proposal cards (format below)

### 8. Judgment withheld (판단 보류)
| Item (항목) | Why it could not be judged (판단하지 못한 이유) | Material needed (필요한 자료) |
|---|---|---|

### 9. Check of past proposals (지난 제안 확인) (when the proposal record has "adopted" or "in verification" entries)
| Proposal ID (제안 ID) | Status (상태) | Success and failure directions written in advance (미리 적은 성공·실패 방향) | Observation this time (이번 관찰) | Result (right / wrong / cannot judge) (결과(맞음/틀림/판단 불가)) | Evidence grade (근거 등급) |
|---|---|---|---|---|---|
On hold items that met their revival condition (되살릴 조건을 채운 보류 항목):

### 10. Verification candidates (검증 후보)
If there is an existing "관찰 포인트 게시" (observation point posting) tool, a candidate list in that tool's entry format. Do not write that the tool should be run.
If there is none, the "Verification method" form below.

### 11. Questions for the user (사용자 확인 질문)
Design intent confirmation questions, questions from "4. Differences between the design documents and the implementation", and principle interpretation questions.

### Appendix (부록)
#### Calculations — commands run, input locations, full output (계산 — 실행한 명령, 입력 위치, 출력 전문)
#### Citation list — locations and dates (인용 목록 — 위치와 날짜)
```

---

## Single review body

```markdown
## Body (본문)

### 0. Basis (기준)
(Same as "0. Basis" of area diagnosis)

### 1. Target (대상)
- Input → rule → result (입력 → 규칙 → 결과): <one paragraph, without expressions of expectation>
- Source (출처): user request (사용자 요청) / another advisor's question (다른 고문 질문) <Q-ID> / proposal record (제안 기록) <DP-ID>
- For a review of an existing system (기존 시스템 심사면): design document (기획서) <location> / implementation (구현) <stage, location> / data (데이터) <location>

### 2. Verdict (판정)
- Verdict (판정): <recommend (추천) · conditional recommend (조건부 추천) · shelve (보관) · do not recommend (비추천)> or <keep (유지) · modify numbers (수정(수치)) · modify structure (수정(구조)) · on hold (보류) · recommend removal (제거 권고) · merge (통합) · judgment withheld (판단 보류)>
- One-line reason (한 줄 이유):
- Minimum condition check (최소 조건 점검):
| Condition (조건) | Met (충족) | Evidence location (근거 위치) |
|---|---|---|

### 3. History (이력)
- Similar existing systems (비슷한 기존 시스템): <name, overlap, location>
- Rejection and on hold records (기각·보류 기록): <proposal ID or unadopted draft document, quoted reason, what changed since then>

### 4. Counter-evidence (written before the verdict) (반대 근거 (판정보다 먼저 쓴 것))
1. Dominant strategy that a player who only cares about efficiency builds (효율만 따지는 플레이어가 만드는 지배 전략):
2. Conflict with the principles or the prohibition principles (원칙·금지 원칙과의 충돌):
3. Cases where the effect is small compared to the cost (비용에 비해 효과가 작은 경우):

### 5. MDA chain (MDA 사슬)
rule → expected play pattern → target emotion → linked pillar (규칙 → 예상 플레이 양상 → 목표 감정 → 연결 필러)
- Player who only cares about efficiency (효율만 따지는 플레이어):
- First-time player / expert (처음 하는 플레이어 / 숙련자):
- (Co-op, versus) team with a large skill gap / one player solves everything / one player is missing ((협동·대전) 실력 차이가 큰 팀 / 한 명이 다 해결 / 한 명이 빠짐):

### 6. Calculation or judgment that looks only at rules (계산 또는 규칙만 보는 판단)
(When frameworks §10 applies, add the mechanism rows the target touches)
| Catalog ID (카탈로그 ID) | State now (지금 상태) | Location or search log (위치 또는 검색 기록) | Change by this target (이 대상이 바꾸는 것) | Linked pillar (연결 필러) |
|---|---|---|---|---|

### 7. Proposal card (제안 카드)
(One card in the format below)

### 8. Questions for the user (사용자 확인 질문)

### Appendix (부록)
#### Calculations — commands, inputs, outputs (계산 — 명령, 입력, 출력)
#### Citation list (인용 목록)
```

If the idea was already rejected and nothing changed, write only items 1 to 3 and stop. In the verdict field, write `already rejected (<proposal ID>), nothing changed` (`이미 기각됨(<제안 ID>), 달라진 점 없음`).

---

## Proposal card

Both modes use the same format. Do not leave a field empty. If it does not apply, write "not applicable" (해당 없음) and the reason.

```markdown
#### <proposal ID> <title>
- Kind (종류): add (추가) / modify numbers (수정(수치)) / modify structure (수정(구조)) / on hold (보류) / recommend removal (제거 권고) / merge (통합)
- Principles (원칙): contributes to <layer, name, quote location> / harms <…> / prohibition principle check result (기여하는 것 / 해치는 것 / 금지 원칙 점검 결과)
- Scene the player goes through (플레이어가 겪는 장면): <one line. Who, when, while doing what, goes through what>
- Input → rule → result (입력 → 규칙 → 결과): <for add and modify structure>
- Evidence (근거): <content> [grade] <location> (several lines)
- Counter-evidence (반대 근거): <content> [grade] <location>
- Reasons to keep it (written first for on hold, removal, and merge) (남겨야 하는 이유 (보류·제거·통합일 때 먼저 쓴 것)):
- Revival condition (for on hold) (되살릴 조건 (보류일 때)):
- Dependency scope (for removal and merge) (의존 범위 (제거·통합일 때)): <list of code, data, and content that refers to it, search scope and pattern>
- Numbers (for modify numbers) (수치 (수정(수치)일 때)): <actual meaning of the value> = [PLACEHOLDER] <starting value>, reason:
- Opportunity cost (for add) (기회비용 (추가일 때)): <what doing this postpones>
- Fun contribution (재미 기여도): high (상) · medium (중) · low (하) — reason
- Cost (비용): S · M · L · L+ — systems that change and their locations / new assets / network synchronization / rework of existing content. Responsible programmer must confirm (담당 프로그래머 확인 필요)
- Performance cost (성능 부담): none (없음) / yes (있음) — performance not checked (성능 미확인), question <Q-ID>
- Priority (우선순위): 1 · 2 · 3 · shelve (보관) — reason
- Reasons it could be wrong (priority 1 and 2) (틀렸다면 그 이유 (우선순위 1·2)): 1) … 2) … — rebuttal result
- Verification method (검증 방법): (the form below, or candidates in the existing tool's format)
- Questions passed on (넘긴 질문): <list of Q-IDs>
- Minimum condition check (최소 조건 점검): | Condition (조건) | Met (충족) | Evidence location (근거 위치) |
```

## Verification method

```markdown
- Observation scene (관찰 장면): <the moment when that mechanic is actually used. Not a session average or a practice range>
- Observation signal (관찰 신호): <behavior first. Number of attempts, choice ratio, whether players try again, and so on>
- Success / failure (성공 / 실패): <the direction is fixed, the threshold number is [PLACEHOLDER]>. Write it before the test
- Conditions (조건): <number of players, skill mix, number of rounds>
- Measurement means (측정 수단): observation notes (관찰 메모) / play logs (플레이 로그) (the result of checking whether that log exists in the code; if not, "log must be added" (로그 추가 필요)) / survey (설문) (including the original question text)
```

A plan that can be called right whatever is observed is not verification. Write it again.

---

## Whole-game index

Make it only when the target is "the whole game". It makes no new verdicts. It collects and shows the latest area diagnosis report of each area. In an unattended run, no new area diagnosis is run, so make it only from the reports that already exist.
File: `<report_dir>/design/<YYYY-MM-DD>-area-index.md`. Use the common head, but the body is only the following.

```markdown
## Body (본문)

| Area (영역) | Latest report (최근 리포트) | Written (작성일) | Base revision (기준 리비전) | Principle status (원칙 상태) | Top proposals (at most 3) (상위 제안(최대 3)) | Outdated (오래됨) |
|---|---|---|---|---|---|---|
| <area> | <path> | YYYY-MM-DD | <value> | confirmed (확정) · draft (가안) | DP-…, DP-… | yes (예) / no (아니오) |
| <area> | not diagnosed (진단 안 함) | - | - | - | - | - |

- Proposals that span areas (when the same system appears in the reports of two areas) (영역 사이에 걸친 제안(두 영역 리포트에 같은 시스템이 나온 경우)): <proposal ID, areas>
- Outdated (오래됨): a report older than profile stale_after_days
```
