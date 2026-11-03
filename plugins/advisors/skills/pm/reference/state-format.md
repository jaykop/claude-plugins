# Record file formats of the PM advisor

`<report_dir>/_state/` holds three files that only the PM advisor writes. The head format is the same as in `shared/state-formats.md`. The file names start with `pm-`, so the session start notice (`scripts/due_check.py`) reads the `Next check:` line. When that date comes for pm-cadence.md, the notice also finds the check names of the due rows with `pm_calc.py cadence` and announces them together.

`pm_calc.py` reads the tables by column name. Do not change the column names or their order. If you add a column, add it at the end.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## pm-cadence.md — Periodic check table

This file manages in one place the work that has a cycle, such as the other advisors' periodic checks, refactoring judgments, and playtests. With this table, the PM announces the work that is due, and if the user agrees, it calls that advisor or proposes a scheduled task. The PM does not write another advisor's report in its place.

```markdown
# PM periodic check table (PM 정기 점검표)

Next check: YYYY-MM-DD
Written by: pm / Last updated: YYYY-MM-DD / Base revision: <commit>

| ID | Check (점검) | How to run (실행 방법) | Period (주기) | Record pattern (기록 패턴) | Last run (마지막 실행) | Note (메모) |
|---|---|---|---|---|---|---|
| PC-001 | Weekly check (주간 점검) | /advisors:pm 주간 점검 | 7 | pm/*-weekly*.md | - | |
| PC-002 | Performance periodic check (성능 주기 점검) | /advisors:perf 주기 점검 | 7 | perf/*-periodic*.md | - | A report is made only when there is a new measurement file |
| PC-003 | Refactoring judgment (리팩터링 판단) | /advisors:perf 진단 <영역> 리팩터링 필요성 | 28 | - | YYYY-MM-DD | Diagnosis reports mix with other purposes, so write the last run directly |
| PC-004 | Technology trend periodic check (기술 동향 정기 점검) | /advisors:radar 정기 점검 | 30 | radar/*-periodic*.md | - | |
| PC-005 | Market change check (시장 변화 점검) | /advisors:market 변화 점검 | 90 | market/*-check*.md | - | |
| PC-006 | Design area check (기획 영역 점검) | /advisors:design 영역 진단 <영역> | 14 days before milestone | design/*-area*.md | - | |
| PC-007 | Playtest (플레이테스트) | Run by people. For the plan: /advisors:pm 플레이테스트 계획 | 14 | - | - | |
| PC-008 | Milestone retrospective (마일스톤 회고) | /advisors:pm 마일스톤 회고 | Condition — milestone ends | pm/*-retro*.md | - | |
| PC-009 | Technical debt check (기술 부채 점검) | /advisors:td 구조 점검 기술 부채 | 30 days before milestone | updated:_state/td-debt.md | - | Structure audit reports mix scopes, so use the last update of the technical debt record. Match the number of days of the period to "Days of notice before a milestone" in the Criteria table of the TD ledger |
```

- **How to run** (실행 방법): a slash command or a task for a person. You can also add checks specific to the project (rule check scripts, backup checks, and so on). Call a command only when the user agreed.
- **Period** (주기): one of a number of days (integer), `N days before milestone` (`마일스톤 N일 전`), or `Condition — <description>` (`조건 — <설명>`). For a period that is not a number of days, `pm_calc.py cadence` does not calculate a date (condition), or it calculates the date from the profile `next_milestone` date.
- **Record pattern** (기록 패턴): a glob relative to `report_dir`. The latest of the dates at the start of the matching file names is the last run. Do not use file system times (common rules §3). For work that leaves no report, write `-` and write the date in the Last run column.
- If you write the record pattern as `updated:<path relative to report_dir>` (`갱신:<path>`), the `Last updated` date at the head of that file is the last run. Use it when reports mix several purposes so that file names cannot tell them apart, and there is a record file that the advisor changes only when it checks (example: `updated:_state/td-debt.md`). If the value is not a date (for example, "not checked yet" (점검 전)), treat it as no run record.
- If both values exist, use the later one.
- **`Next check:` in the head** is the "가장 이른 다음 예정일(오늘 이후)" (earliest next due date after today) line of the `pm_calc.py cadence` output. If past items remain, write today's date (so that the next session start announces them again).
- When you make the file for the first time, keep only the rows of this example that fit the project. Do not add rows for advisors that are not turned on. For each period, propose the default cycle in that advisor's SKILL.md, and write the value that the user decided.

## pm-risks.md — Risk list

The judgment method is item 2 of `methods.md`.

```markdown
# PM risk list (PM 위험 목록)

Next check: Condition — check together at the weekly check
Written by: pm / Last updated: YYYY-MM-DD / Base revision: <commit>

| ID | Risk (위험) | Kind (종류) | Impact (영향) | Likelihood (가능성) | Response (대응책) | Decide by (결정 시점) | Status (상태) | Evidence (근거) | Last checked (마지막 확인) |
|---|---|---|---|---|---|---|---|---|---|
| PR-001 | <what can happen> | people (사람) / project (프로젝트) / production process (제작 과정) / technology (기술) | critical (치명) / severe (심각) / moderate (보통) / minor (가벼움) | high (높음) / medium (중간) / low (낮음) | a) active (능동): ... b) fallback (대체): ... | YYYY-MM-DD or "<milestone name>" | watching (관찰) / responding (대응 중) / resolved (해소) / dropped (폐기) | file:line, issue, report | YYYY-MM-DD |

## Resolution record (해소 기록)
| ID | Resolved on (해소일) | How it was resolved (어떻게 해소했나) |
|---|---|---|
```

- `pm_calc.py risks` calculates the score and the order as Impact × Likelihood. Do not put a score column in the table (so that a handwritten score and the calculation do not disagree).
- If the Decide by value is `<milestone name>`, pass the date of that milestone with `--milestone-date`. For another milestone, write the date directly.
- Do not delete rows. When a risk is resolved, change the status to "resolved" and add one line to the Resolution record table.
- Do not write the likelihood as "high" without evidence. If the evidence is an estimate, add "estimated" (추정) in the Evidence column.

## pm-plan.md — Milestone plan and weekly log

```markdown
# PM milestone plan (PM 마일스톤 계획)

Next check: 7 days before milestone
Written by: pm / Last updated: YYYY-MM-DD / Base revision: <commit>

## Current milestone (현재 마일스톤)
| Item (항목) | Value (값) |
|---|---|
| Name (이름) | ... |
| Date range (기간) | YYYY-MM-DD ~ YYYY-MM-DD |
| Goal (목표) | one sentence |
| Source (출처) | tracker milestone description (트래커 마일스톤 설명) / profile next_milestone (프로필 next_milestone) / user (사용자) |

## Completion criteria (완료 기준)
| ID | Criterion (기준) | Grade (등급) | Check method (확인 방법) | Status (상태) | Check date (확인일) | Evidence (근거) |
|---|---|---|---|---|---|---|
| MC-001 | ... | must (필수) / basic (기본) / extra (추가) | try it directly in the build (빌드에서 직접 해 보기) / demo (시연) / playtest (플레이테스트) | none (없음) / partial (일부) / done (완료) / excluded (제외) / not applicable (해당 없음) | YYYY-MM-DD | issue·report |

## Buckets by remaining milestone (남은 마일스톤별 통)
| Milestone (마일스톤) | Work to include (issue numbers or short names) (담을 일 (이슈 번호나 짧은 이름)) | Must size sum (h) (필수 규모 합(h)) | Note (메모) |
|---|---|---|---|

## Capacity record (용량 기록)
| Calculated on (계산일) | Date range (기간) | Plannable time (h) (계획 가능 시간(h)) | Must size (h) (필수 규모(h)) | Must ratio (필수 비율) | Command (명령) |
|---|---|---|---|---|---|

## Order change record (순서를 바꾼 기록)
| Date (날짜) | What changed (바꾼 것) | Reason (이유) |
|---|---|---|

## Weekly log (주간 기록)
| Week (start date) (주(시작일)) | Planned work (계획한 일) | Finished work (끝낸 일) | Delayed work and cause (늦어진 일과 원인) | What to change (바꿀 것) |
|---|---|---|---|---|
```

- In the cause column, write one of the cause words of `methods.md` 6-1.
- In a project with a tracker, if the completion criteria and the issue states differ, treat the tracker as the fact, and raise the difference in "Decisions needed" of the report. The PM does not change the tracker.
- When a milestone ends, do not delete this file. After you write the retrospective report, replace "Current milestone" and "Completion criteria" with the values of the new milestone. The previous values stay in the retrospective report.
