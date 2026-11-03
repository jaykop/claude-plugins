# TD advisor `_state` file formats — td-ledger.md (TD ledger), td-debt.md (technical debt record)

These are the formats of the two `_state` files that only the TD advisor writes (they are in the skill reference, by the convention at the top of shared/state-formats.md). The PM advisor's periodic check calculation also reads the `Last updated:` line at the top of td-debt.md. The reason for splitting into two files is the session start notice. When the line has the "N days before milestone" format, the notice script (`scripts/due_check.py`) treats the file as already checked if its `Last updated:` date is on or after the notice start date. So that a design review does not turn off the technical debt notice, debts are kept in a separate file that changes only at a debt audit.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

| File | What it holds | When it changes | Head `Next check:` line (`다음 점검:`) |
|---|---|---|---|
| `td-ledger.md` (TD ledger (TD 기록)) | Criteria, decision records (TD-D), layer rules (TD-L), change log | Design review, module dependency audit, when criteria are set | Always `Condition — when a question addressed to td arrives in the question inbox or an awaited answer has arrived` (`조건 — 질문함에 td 앞 질문이 오거나 기다리던 답이 왔을 때`) |
| `td-debt.md` (technical debt record (기술 부채 기록)) | Technical debts (TD-B) | Adding debt rows or ranking them again happens only at a technical debt structure audit. If the user states a decision on one debt, in any run change only that row's status and decide-by date (leave `Last updated:` as is). When another run creates the file for the first time, create it with an empty table and `Last updated: not checked yet` (`마지막 갱신: 점검 전`) | Always `N days before milestone` (`마일스톤 N일 전`) (N is the value in the criteria table). If the profile has no milestone date, the notice script does not give a notice |

## td-ledger.md

```markdown
# TD advisor ledger (TD 고문 기록)

Next check: Condition — when a question addressed to td arrives in the question inbox or an awaited answer has arrived
Written by: td / Last updated: YYYY-MM-DD / Base revision: <CL or commit; if it could not be checked, "not checked">

## Criteria (판정 기준)
| Item (항목) | Value (값) | Set by (정한 사람) |
|---|---|---|
| Change history period (변경 이력 기간) | <example: 180 days> | user (사용자) / empty (비어 있음) |
| Ticket key prefix (티켓 키 접두사) | <example: ABC> | |
| Issue kinds and labels to count as bugs (버그로 셀 이슈 종류·라벨) | <example: Bug, label crash> | |
| Temporary marker comment pattern (임시 표시 주석 패턴) | <regex; if empty, the default TODO\|FIXME\|HACK> | |
| Excluded paths (점검 제외 경로) | <list of paths relative to the project root. External vendor plugins and so on> | |
| Days of notice before a milestone (마일스톤 전 알림 일수) | 30 | |
| Debt decision deadline days (부채 결정 기한 일수) | 7 | |
| Seeded random number path (시드 고정 난수 경로) | <the random function or subsystem name that the team set; if there is none, "none" (없음). Used in the agent verifiability audit> | |

## Decision records (결정 기록)
| ID | Question (질문) | Target paths (대상 경로) | Options (안) | Conclusion (결론) | Cap rules applied (걸린 상한) | Decision owner (결정권자) | Status (상태) | Waiting question (기다리는 질문) | Recheck condition (다시 볼 조건) | Evidence report (근거 리포트) |
|---|---|---|---|---|---|---|---|---|---|---|
| TD-D-001 | <shortened question> | <path> | keep option 0 / option 1 <name> / option 2 <name> | decide after a trial | T2, T10 | <name> | proposed | Q-0012 | <event> | td/2026-10-15-decision.md |

Status (상태): proposed (제안) / in trial (시험 중) / adopted (채택) / rejected (기각) / on hold (보류)
Comparison columns such as the changed scope are in the "4. Option comparison" table of the evidence report.

## Layer rules (층 규칙)
| ID | Layer (층) | Modules (모듈) | Source (출처) | Status (상태) |
|---|---|---|---|---|
| TD-L-001 | <layer name> | <module list> | <team document location / --layer-draft draft> | final (확정) / draft (초안) |

## Change log (바뀐 기록)
| Date (날짜) | ID | Before (이전) | After (이후) | Evidence for the change (location of the new fact) (바꾼 근거(새 사실의 위치)) |
|---|---|---|---|---|
```

## td-debt.md

```markdown
# TD advisor technical debt record (TD 고문 기술 부채 기록)

Next check: 30 days before milestone
Written by: td / Last updated: YYYY-MM-DD / Base revision: <CL or commit>

| ID | Kind (종류) | Location (위치) | Evidence numbers and command (근거 수치와 명령) | Rank (순위) | Payoff scope (갚는 범위) | Recommendation (권고) | Decide by (결정 시점) | Status (상태) | Last check date (마지막 확인일) |
|---|---|---|---|---|---|---|---|---|---|
| TD-B-001 | recurring bug | <path> | bug tickets 3 (vcs_churn.py …) | 2 | files 4 | pay off — issue in the next milestone | YYYY-MM-DD | open | YYYY-MM-DD |
```

Kind (종류): blocks release (출시 막음) / recurring bug (되풀이된 버그) / engine upgrade cost (엔진 버전 올리기 비용) / plugin on, no sign of use (켜짐·사용 흔적 없음 플러그인) / temporary marker comment (임시 표시 주석) / refactoring recommended (perf) (리팩터링 권장(perf))
Recommendation (권고): one of pay off (갚음) / accept (받아들임) / wait for condition (조건 대기), and a one-line reason. For pay off, write where to put it (current milestone (지금 마일스톤) / next milestone (다음 마일스톤) / backlog (백로그)). For wait for condition, write the recheck condition (when a certain issue starts, when a certain event happens). It is the advisor's proposal, and the user decides
Decide by (결정 시점): the date by which the user decides whether to accept the recommendation (`YYYY-MM-DD`). For a pay off or accept recommendation, it is the registration date + the "Debt decision deadline days" in the criteria table (default 7). For rank 1, set it no later than that, before the deadline of the next milestone. If the status is waiting for condition, it is `Condition — <recheck condition>` (`조건 — <다시 볼 조건>`). If the status is paying off, paid off, or accepted, it is `-`
Status (상태): open (열림) (before the decision) / waiting for condition (조건 대기) / paying off (갚는 중) (#issue) / paid off (갚음) / accepted (받아들임)

## Rules

- Do not reuse IDs. Do not give the number of a deleted row to the next row either.
- Change the status of decision records and debts only when the user stated a decision in the conversation, or when you can quote a document in which the decision is written. Do not change them in an unattended run.
- In the criteria table, write only values that the user answered in a conversation run. In an unattended run, only read it.
- A layer rule is "final" if it is in a team document. One extracted with `--layer-draft` is a "draft", and it changes to "final" when the user confirms it.
- If you changed a conclusion, you must leave one line in the "Change log" (choice-rules.md §10).
- Write the N at the top of td-debt.md as the value of "Days of notice before a milestone" in the criteria table. If you changed the value in the table, change the head line too at the next debt audit. Do not calculate the date directly.
- Do not leave the recommendation and the decide-by date empty in a new debt (TD-B) row. The reason: to prevent undecided debts from piling up and then being judged all at once. The PM advisor gives a notice in the weekly check about "open" debts whose decide-by date has passed or is near (`pm_calc.py debts`).
- If the user decides differently from the recommendation, change the status and the decide-by date to match that decision, and keep the recommendation column. If the condition of a debt that waits for a condition happens, change the decide-by date to that day and set the status back to "open".
- This file has only one table, the first one (PM's `debts` reads the first table). If you want more tables, such as a resolution log, put them after the debt table.
- Change the `Last updated:` of td-debt.md to a date only at a technical debt structure audit. If no audit has run yet, it is "not checked yet". If the notice script cannot read a date from this field, it does not treat the file as already checked.
- If the waiting question was closed as "dropped — passed to <advisor> Q-yyyy", change it to Q-yyyy (SKILL.md Step 0, item 2).
