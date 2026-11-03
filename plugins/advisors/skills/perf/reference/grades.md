# Evidence marks, grades, and worsening judgment

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. Evidence marks

Attach one of the marks below to every finding in the report. Do not write a judgment sentence without a mark.

| Mark (표시) | Meaning | Must be written with it | Level in common rules §1 |
|---|---|---|---|
| [confirmed] ([확인]) | The cost was confirmed by measurement. It can be called a bottleneck or a cost | Measurement file path, command or channel, scenario ID, region, value, repeat count and spread | confirmed (확인함) |
| [suspected] ([의심]) | Found by reading code only. It is only a candidate | file:line, and the call path (file:function → file:function) that shows the code is called every frame or often | estimated (추정) |
| [not measured] ([측정 못 함]) | It could not be measured because there was no means, scenario, permission, or environment to measure it | What would make it possible to measure | unknown (모름) |

- The only way to raise [suspected] to [confirmed] is measurement. Do not raise it by reading more code or by citing similar cases.
- For a claim taken from another advisor's report, use the original grade as it is, and write the date of that report (common rules §1).
- In the code health category, use as [confirmed] the numbers counted directly from the version control history and the issue tracker. Write the command that produced the numbers with them.

## 2. Prohibitions about numbers

- Do not predict the improvement effect as a number. Do not write "fixing this makes it 2ms faster".
- Do not use generic multipliers. A sentence such as "Blueprints are 10 times slower than C++" is not evidence. If two approaches must be compared, measure both in this project.
- Use ms, MB, and counts in the report only if they come from the measurement results of this project. Do not use numbers from memory, numbers from other projects, or numbers from web articles.
- Calculate with a script or Bash, and leave the formula and the inputs (common rules §2).

## 3. Effect ceiling

- In an improvement proposal, write only the "effect ceiling" (효과 상한). The effect ceiling is the inclusive time that the region uses now (the time including the time of the child functions that the function called). An improvement cannot reduce more than that.
- Only when that thread is the bottleneck, write "frame time can drop by at most <ceiling>". If it is not the bottleneck, write "<thread> gains at most <ceiling> of headroom (the frame time can stay the same)".
- The effect is confirmed only when you measure again under the same conditions after the improvement and compare. Attach the re-measurement method to the improvement proposal.

## 4. Grades

Rank only [confirmed] items. The budget used for the judgment is the value of profile `perf.budgets`.

| Grade (등급) | Condition | What to attach in the report |
|---|---|---|
| Priority 1 — recommended to handle now (1순위 — 바로 처리 권장) | [confirmed], it exceeds the budget in a representative scenario, and that category is the bottleneck of that scenario. Or it was confirmed as the cause of a recurring hitch | Cause code (file:line), improvement proposal, effect ceiling, re-measurement method |
| Priority 2 — put in the plan (2순위 — 계획에 넣기) | [confirmed] and within the budget now, but one of these: it got a worsening judgment / it exceeded the budget in a minimum-spec measurement / it is not the bottleneck but it has the largest cost share in that category | Cause code, improvement proposal, effect ceiling |
| Priority 3 — record only (3순위 — 기록만) | [confirmed] and the cost is small (it is not the bottleneck and it did not get worse). Recommend not touching it | Only the measured value. Even if the code looks bad, it belongs here as far as performance evidence goes |
| Suspected — needs measurement (의심 — 측정 필요) | [suspected]. Do not rank it | Measurement order and measurement plan |
| Not measured (측정 못 함) | It could not be measured | What would make it possible to measure. Do not recommend changing or removing this item |
| Not comparable (periodic check only) (비교 불가 (주기 점검 전용)) | The measurement conditions differ from the earlier round, so the change cannot be judged | The fields that differ. If it is an intended change such as an engine upgrade, "new baseline candidate" (새 기준선 후보) |

### When there is no budget

If `perf.budgets` is empty, do not give Priority 1 for exceeding the budget. Instead, use the rules below, and write "no budget — fallback ranking rule" (예산 없음 — 대체 순위 규칙) at the top of the report.

- Put the top 5 regions by inclusive time inside the bottleneck thread at Priority 2. Group regions whose order shifts between repeated measurements (regions whose difference is smaller than the spread) at the same rank.
  - Read the inclusive time of each region from the Insights timer statistics export (`measure.md` 5-2). If you only have CSV profiler results, you know only the thread totals. So do not rank regions, and put the export in the measurement plan.
  - In the CSV profiler, a statistic with `Exclusive` in its name can be exclusive time (the time excluding child calls). Until you check its definition in the engine source, do not use it as inclusive time or as an effect ceiling.
- What was confirmed as the cause of a recurring hitch is Priority 1 even without a budget. But the hitch threshold (ms) must be set in the judgment criteria table of the ledger. If it is not set, put it at Priority 2 and ask for the hitch threshold to be set.
- The remaining [confirmed] items are Priority 3.
- Raise "Please set the budget (target fps or frame time per platform, memory limit)" in "Decisions needed". The decision owner sets the budget, so the advisor does not set it.

## 5. Suspect list rules

- Run the pattern search only after measurement has decided the bottleneck category, and run only that category's patterns. If there is no measurement, run it only inside the system path that the user named. Do not run all patterns on the whole source.
- When a pattern matches, do not raise it as a suspect right away. Follow the call path, and write with file:line which of the following it is.
  - Every frame (매 프레임): tick functions, short-interval timers, delegates (event bindings) called every frame
  - Frequent event (잦은 이벤트): events that can happen several times per second, such as hits, shots, and input
  - Once (한 번): at start (BeginPlay and so on), at loading, at settings changes
  - Unknown (모름): the call path is broken, or it is called from a Blueprint
- Leave "once" out of the suspect list, and keep it with the reason in "Excluded search results".
- The suspect list has at most 10 items per round. If there are more, cut it by call frequency (every frame > frequent event > unknown) and by the number of objects that have that code (whether it runs for every character or for only one), largest first, and write the number cut.
- Attach only a measurement order to suspects, not a rank.

## 6. Worsening judgment (periodic check)

1. **Conditions match**: Compare only if the measurement condition tables (`measure.md` item 2) of this round and the compared round are all the same. If even one differs, set "not comparable" and write the field that differs. If it is an intended change such as an engine version change, mark it "new baseline candidate". For the exception when an unattended run cannot fill the user confirmation field, follow SKILL.md 2-2, and add "some conditions unconfirmed" (조건 일부 미확인) to that comparison result.
2. **Repeats**: Both rounds must have been measured 3 times or more. For each metric, use the median and the spread (maximum − minimum) (the output of `csv_profile_stat.py compare --a ... --b ...`).
3. **Judgment**: Treat it as "worse" (나빠짐) or "better" (좋아짐) only when the median difference is larger than the larger of "the larger spread of the two rounds" and "the minimum change". The minimum change is the value in the judgment criteria table of the ledger. If it is not there, use only the spread, and raise "Please set the minimum change" in "Decisions needed". For time, memory, and count metrics, larger is worse.
4. **Comparison with two rounds**: Compare with both the previous round and the baseline round. If the comparison with the previous round gives no judgment but the comparison with the baseline shows a worsening, mark it "cumulative worsening" (누적 악화). This is to catch cases that get worse little by little.
5. **Budget**: Separately from worsening, if it exceeds the budget, it is "over budget" (초과). If it is within the budget and got worse, it is "caution" (주의).
6. **Cause candidates**: For each item that got worse, attach as "cause candidates" (원인 후보) the changes between the two rounds' revisions that touched that category's paths. Write that they are only candidates. Only propose how to confirm them: a measurement that splits the range between the two revisions (measure the middle revision and halve the range each time). If profile `vcs_read_commands` does not have the needed read commands, or the lookup failed and there is no change list, the cause candidate field is "not checked" (확인 못 함) (the same in conversation and unattended runs). Do not fill it by guessing without a change list.
7. **Items without a measurement**: For an item not measured this time, keep the previous value as it is and mark it "not measured this round" (이번 측정 없음). Do not copy the previous value as if it were this round's value.

The judgment value is one of five: pass (통과) / caution (주의) / over budget (초과) / not measured (측정 못 함) / not comparable (비교 불가). As an exception, if it is the first round of that scenario and there is also no budget, there is nothing to compare with, so set "-" (no judgment) (판정 없음). In this case, do not write "pass".
