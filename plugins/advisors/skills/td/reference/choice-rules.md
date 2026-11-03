# TD advisor verdict rules

Write a design review in the order of this file: requirements → option comparison → reason to change → cap rules → conclusion → self-rebuttal → decision owner. Do not use the adopt · trial · assess · hold verdicts of the technology trend advisor. The reason: so that the verdict terms of the two advisors do not get mixed.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. Evidence marks and grades

Attach a mark to every fact. Each mark maps to a common grade (confirmed / estimated / unknown in rules.md §1).

| Mark (표시) | What | Grade |
|---|---|---|
| [team doc] ([팀문서]) | path:line of team technical rules, design records, or incident records | The fact that a rule exists is confirmed. Cause analyses and effect claims in documents are estimated ("source document's estimate" (출처 문서의 추정)) |
| [code] ([코드]) | What you read or counted in our code in this run. path:line, the search pattern and the result count | A static check is confirmed. Execution order estimates and connection estimates are estimated |
| [engine] ([엔진]) | path:line of the local engine source | Calls and conditions written in the code are confirmed. The execution order and whether things happen in the same frame, when not run, are estimated |
| [measured] ([측정]) | A perf report or a measurement file | The original grade as it is |
| [history] ([이력]) | A `vcs_churn.py` result, an issue tracker query | Confirmed |
| [primary] ([1차]) | Official documents or release notes opened in this run, or a source-checks row that meets the reuse conditions of rules.md §3 (with the row ID and the original check date) | Confirmed only as far as "the document says so". Check with [engine] whether it also holds for our local engine source. If the two differ, write both and judge by the local side |
| [general] ([일반론]) | Design principles, technical articles by other developers (secondary) | Estimated |

What is not used as evidence:
- "It is the industry standard", "everyone does it this way", the majority opinion of a community, a competing game used it
- The behavior of a previous engine version from memory. Put content from memory only in the report appendix "Content from memory — not evidence"
- Reasons that are only "it is cleaner" or "it is easier to read"

When you cite another advisor's report or a previous record, copy the original grade, date, and caveats as they are. Example: if the "no change" line of a periodic check has "lines may be missing because a summarizing tool read the page" attached, copy that caveat too, and treat that line as estimated. If the date is older than `stale_after_days`, attach "outdated report".

## 2. Requirement list

- For each requirement R-n, write the requirement sentence, the source, and the grade. The source is a design document path:line, a ticket, a team document, an incident record, a perf · design · radar report, or what the user said.
- If the only source is what the user said, mark it "requirement not confirmed" (요구 미확인). You can recommend, but put the requirement check in "Decisions needed".
- Take requirements that touch game rules or fun only from design documents or design judgments. If there is no evidence, pass a question to design and keep the requirement as "requirement not confirmed".

## 3. Option comparison table

- Option 0 must be included. For a question that has a current implementation, it is "keep the current approach" (지금 방식 유지). For new structure design (a feature with no implementation yet), it is "put it as is on the closest existing structure" (가장 가까운 기존 구조에 그대로 얹기). If there is no existing structure to put it on either, option 0 is "the simplest implementation (one new class, no connection to existing systems)" (가장 단순한 구현(새 클래스 하나, 기존 시스템 연결 없음)).
- Fill the same columns for each option. If there is no evidence to fill a column, write "unknown". Do not leave it empty.

| Column (칸) | How to write it |
|---|---|
| What it does (하는 일) | One line |
| Requirements met (요구 충족) | For each R-n: met (충족) / partial (부분) / not met (불충족) / unknown (모름), with the evidence mark |
| Changed scope (바뀌는 범위) | The number of files, modules, call sites, new Build.cs dependencies, types exposed in public headers, the increase or decrease of engine modification blocks, the kinds of assets to save again. Write the search pattern and the result count with it. If the places used from Blueprints or assets cannot be counted, attach "partly counted" (일부만 셈) |
| Engine behavior evidence (엔진 동작 근거) | [engine] path:line or [primary] URL |
| Risk (위험) | Known failure modes (reentry, two places writing the same state in the same frame, a missing replication mark, loading order, and so on) and the evidence location |
| Performance (성능) | The [measured] value, and the maximum that can be saved (the time that section uses now). If there is none, "not measured — perf Q-xxxx" (미측정 — perf Q-xxxx) |
| Reversal (되돌리기) | The grade in §4 |
| Ongoing cost (계속 드는 비용) | The scope of code to maintain directly (file and line counts), the scope of dedicated editor code, the number of Experimental or Beta dependencies (technology inventory evidence), the number of places to check again at an engine version upgrade |
| Maturity risk (성숙도 위험) | Only when the option relies on an Experimental or Beta feature. Technology inventory, local .uplugin, radar-watchlist evidence |
| Team sharing needed (팀 공유 필요) | "Needed" (필요) if it registers a module, adds a Build.cs dependency, exports a shared header, or changes a format sent over the network |

- Do not give scores, and do not sum with weights. Only compare column by column.
- Do not have a duration (people · days) column. Write the size only in countable units (rules.md §2). Talk about the effect only up to the time that section uses now.

## 4. Reversal grades

| Grade (등급) | Meaning |
|---|---|
| 1 | Reverted by turning off a setting, a flag, or a plugin |
| 2 | Only the code is reverted. Assets and data formats stay as they are |
| 3 | Assets must be saved again, or data must be converted |
| 4 | Save data, a format sent over the network, or a format used by the server or other teams changes |

An option that is easy to reverse (1 · 2) can be tried even if less evidence has been collected. For an option that is hard to reverse (3 · 4), require measurement and decision owner confirmation first (T4). Handle engine modifications separately from how hard they are to reverse: as the cost paid at every engine version upgrade, in the "Ongoing cost" column and in T5.

## 5. Reason to change

In a choice comparison or a structure problem, to recommend an option other than option 0 ("keep the current approach"), one of the following must be confirmed.
- Recurring bug (되풀이된 버그): 2 or more bug tickets or incident records for the same place ([history]·[team doc])
- Blocked requirement (막힌 요구): a requirement that the current structure cannot meet (the source of the requirement and [code]·[engine] evidence). If the only source of the requirement is what the user said, recommend with this reason, but attach "requirement not confirmed"
- Measured cost (측정된 비용): perf's [measured]
- Deprecation with a deadline (기한 있는 폐기 예정): the removal version or date of an engine feature we use ([primary])
- Team rule violation (팀 규칙 위반): the rule clause in [team doc] and the [code] location that breaks it

If there is none, the conclusion is "keep as is" or "judgment on hold — not enough confirmation". Even if another option looks better, do not recommend moving if no reason to change is confirmed.

Do not use this section for new structure design, because there is no current implementation to change. Choose by comparing, for each option, the requirements met, the changed scope, and the ongoing cost. If the only source of a requirement is what the user said, give the recommendation, but put the requirement check in "Decisions needed".

If the user asked about an option that changes the way that team rules set, make the option that follows the rules option 0, and compare in the same columns. You can recommend, but attach "team rule change needed — decision owner <decision_owners.tech>" (팀 규칙 변경 필요 — 결정권자 <decision_owners.tech>) to the conclusion.

## 6. Conclusion

The conclusion is one of four.

| Conclusion (결론) | Condition |
|---|---|
| Recommend — if condition X, option A (권고 — 조건 X 면 안 A) | Write it in the form "if condition X, option A; if Y, option B". If §5 requires it, there is a reason to change; the evidence that the recommended option meets the requirements has at least one of [team doc]·[code]·[engine]·[measured]·[history]·[primary]; and no cap rule applies |
| Decide after a trial (시험 후 결정) | Two or more options remain, and only measurement or a trial implementation can tell them apart. Attach a trial implementation spec (§9) |
| Keep as is (현행 유지) | Option 0 meets all the requirements, or no reason to change was confirmed. This is a valid conclusion |
| Judgment on hold — not enough confirmation (판단 보류-확인 부족) | Write what must be checked to make a verdict, and whom to ask. Attach the reason in parentheses: (target not set) ((대상 미정)), (options not set) ((안 미정)), (waiting for outside check Q-ID) ((바깥 확인 대기 Q-ID)), (requirement not confirmed) ((요구 미확인)), and so on |

Verdicts written together, by question kind:
- Structure problem: write the cause verdict first.
  - Cause confirmed (원인 확인됨): analyst's static check has a call path that leads to the symptom, and the reproduction condition is in a ticket or a document
  - Cause candidate (원인 후보): there is a path, but it relies on an execution order estimate or a connection estimate, or there is no reproduction condition
  - Unknown (모름)
- Feature feasibility: write the feasibility verdict first. Possible with the current structure (지금 구조로 가능) / structure change needed (list of places to change) (구조 변경 필요(바꿀 곳 목록)) / not possible (blocking evidence) (불가(막는 근거)) / unknown (모름).
- Shift impact: instead of a conclusion, give an "affected places table" (영향받는 곳 표) (changed scope and risk), and put whether to do it in "Decisions needed". Do not conclude that it must be done or must not be done.

## 7. Cap rules

The order of conclusions from high to low is recommend > decide after a trial > keep as is · judgment on hold. If several rules apply, use the lowest one, and write all the numbers that apply.

| Number | Condition | Highest conclusion |
|---|---|---|
| T1 | The evidence that the requirements are met is only [general] or secondary | Decide after a trial |
| T2 | Performance decides between the options, but there is no measurement | Decide after a trial. A perf measurement request must be made |
| T3 | It is a source build, but the behavior of the engine feature was not checked in the local engine source and was seen only in web documents | Decide after a trial |
| T4 | An option with reversal 3 · 4 | If there is no measurement or trial implementation result, decide after a trial. Attach "decision owner confirmation needed" (결정권자 확인 필요) |
| T5 | An option that adds engine modification blocks | If there is no [code]·[engine] evidence that the options on the game code, tools, or settings side cannot meet the requirements, decide after a trial. If the team rule documents have engine modification rules, quote that clause |
| T6 | An option that relies on an Experimental or Beta feature | The maturity risk column must be filled. If the development stage is alpha or later, decide after a trial |
| T7 | The development stage is alpha, beta, or live, and it is a structure replacement that spreads across all content (global illumination method, shadow method, network replication method, animation system, material system, and so on) | Decide after a trial. Attach "lead agreement needed" (리드 합의 필요). If `dev_stage` is empty, do not recommend an option with reversal 3 · 4 |
| T8 | An outside fact that decides the verdict waits for radar's answer, or it could not be looked up on the web because there is no profile or no banned search terms | That option is "judgment on hold — not enough confirmation (waiting for outside check Q-ID)". If there is no profile, "judgment on hold — not enough confirmation (no profile)" ("판단 보류-확인 부족(프로필 없음)"). Compare only the remaining options with each other |
| T9 | The changed scope could not be counted to the end ("partly counted") | That option is decide after a trial |
| T10 | The execution order or whether things happen in the same frame decides the verdict, but the only evidence is an execution order estimate | Decide after a trial. Put the way to check (logs, debugger records, trial implementation) in the spec |

## 8. Self-rebuttal and decision owner

- For each recommended option, write two or more "if it is wrong, the reason" (틀렸다면 그 이유). If you cannot rebut them with evidence, lower the conclusion by one level.
- Write the "information that would reverse the judgment" (판단을 뒤집을 정보). Example: "if the perf measurement shows that this section is less than 10% of the budget, option 0".
- The decision owner is profile `decision_owners.tech`. If the user is not the decision owner, write it as a "reference option" (rules.md §8).
- Attach "team sharing needed" to options that change team-shared structure (the same criterion as item 4 of perf/reference/tests.md).

## 9. Trial implementation spec (only when the conclusion is "decide after a trial")

| Column (칸) | How to write it |
|---|---|
| Scope (범위) | A unit that can be turned off (a flag, a plugin, a separate map, a branch) |
| What to measure (잴 것) | For performance, a perf measurement request (scenario ID). For behavior, the phenomenon to check and the method (logs, debugger records) |
| Behavior-locking test (동작 고정 테스트) | A test that locks the current behavior before anything is touched. The form in item 3 of perf/reference/tests.md |
| How to turn it off and revert (끄고 되돌리는 방법) | Write only setting and file names that you confirmed |
| Duration (기간) | Keep it as "to be decided" (정할 것). The advisor does not decide it |

The advisor does not make the trial implementation itself. After user approval, pass it to `code_change_entry`.

## 10. Updating decision records

- Do not change a conclusion without a new fact. The reason: to prevent the verdict from going back and forth on the same facts.
- If you changed it, leave the previous conclusion, the new conclusion, and the evidence for the change (the location of the new fact) in the "Change log" of the TD ledger.
- Change the status of a decision record (proposed / in trial / adopted / rejected / on hold) only when the user stated a decision in the conversation, or when you can quote a document in which the decision is written.
