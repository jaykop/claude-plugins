# Question inbox format between advisors

File: `<report_dir>/_state/inbox.md`

One advisor stacks the questions that it passes to another advisor, one row per question. When each advisor starts a run, it first reads the "열림" questions addressed to it, and proposes to the user: "<고문> 앞으로 미해결 질문이 N건 있는데 같이 볼까요?".

```markdown
# 고문 질문함

다음 점검: 조건 — 열린 질문이 있을 때 받는 고문 실행 시작 시

| ID | 날짜 | 보낸 고문 | 받는 고문 | 질문 | 관련 ID | 필요한 답의 형태 | 상태 |
|---|---|---|---|---|---|---|---|
| Q-0001 | 2026-01-15 | radar | perf | 새 그림자 방식 시험의 성공 기준 측정 | TW-003 | 시나리오 S01, PC-min, GPU 프레임 시간 p95, 켜기 전후 비교 | 열림 |
```

## Rules

- The ID is `Q-` followed by a four-digit number. Do not delete rows. Change only the status (열림 / 답함 / 폐기).
- Write the "필요한 답의 형태" (form of the answer needed) column so that the receiving advisor can work right away.
  - When you request a measurement from perf: the scenario ID (only one that is in profile perf.scenarios), the platform, the metric, and the comparison method. If no scenario fits, write "알맞은 시나리오 없음" and a description of the scene that is needed, and put adding a scenario in "Decisions needed" (결정이 필요한 것) of the sending advisor's report.
  - When you request a review from design: one paragraph of input (what the player does) → rule (how the game processes it) → result (what the player gets), and the evidence. If the rule is not decided, write "규칙 미정".
  - When you request a check from market: the target game or metric, the region, and the period.
  - When you request a check from radar: the problem to solve, the related measurements or tickets, the public technology name (if there is one), the kind of outside fact that is needed (발표 단계 = announcement stage / 우리 버전 이후 변화 = changes after our version / 지원 플랫폼 = supported platforms / 알려진 문제 = known problems / 다른 엔진 버전의 동작 = behavior in other engine versions), and the ID of the decision record that waits for it (if there is one).
  - When you request radar to write or update the technology list (radar-inventory.md): the reason (목록 없음 = no list / 마지막 갱신이 오래됨 = the last update is old / 엔진 버전이 다름 = the engine version is different).
  - When you request a schedule judgment from pm: the target (one proposal, refactoring, structure change, debt payoff, or technology to adopt), the expected size or "모름", and the cost of doing it late with its evidence. pm answers with one of 지금 넣기 (add now) / 다음 마일스톤 (next milestone) / 백로그 (backlog) / 넣지 않기 (do not add).
  - When you request a refactoring judgment from perf (pm sends it): the area path, the issue numbers that gather in that area, and the item ID in the periodic check table.
  - When you request a review from td: the target system (code path or design document path), the options to compare (if there are any), the requirements and their evidence, and the related measurements and tickets.
- If a received question is not the work of the receiving advisor (`shared/routing.md`), pass it on.
  - Change the status of the original row to "폐기 — <고문>으로 넘김 Q-xxxx", and post the same content to the right advisor with a new ID (Q-xxxx).
  - In the new row, keep "보낸 고문" (sending advisor) as the advisor that sent the question first. Write the original question ID in the "관련 ID" (related ID) column.
  - In the "필요한 답의 형태" of the receiving advisor, fill each field that the original question does not have with "모름 — 처음 보낸 고문 확인 필요".
  - If the advisor that received the passed question cannot reach a verdict because of a "모름 — 처음 보낸 고문 확인 필요" field, it posts a question to the first sender that asks it to fill that field, and writes that Q-ID in its own record (for td, the "기다리는 질문" column of the decision record).
  - Do not pass a question again if it was already passed once (a question whose 관련 ID has a passing record). The receiving advisor answers as far as it can, and puts which advisor must handle it in "Decisions needed" (결정이 필요한 것) of its report.
  - Do not ask the user. This is the same in conversation runs and unattended runs.
- When you answer, change the status to "답함", and append the path of the report that has the answer to the end of the question column.
