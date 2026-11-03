# Judging whether refactoring is needed

Refactoring is not a mode. When a diagnosis or a periodic check has decided a target, judge it with these criteria. After user approval, hand the actual change to the skill in profile `code_change_entry`. This file decides only whether refactoring is needed. How to fix it (structure choices, module splitting) is the work of the TD advisor's design review.

## 1. Three axes

| Axis | What to look at | Source of the numbers |
|---|---|---|
| Performance (성능) | Does that code have Priority 1 or Priority 2 [confirmed] items? Is their cause a structural problem for which local fixes (storing results, calling less often, returning early) cannot reach the effect ceiling? Examples: a structure that scans everything every frame, scattered data layout | Measurement results ([confirmed] only) |
| Change cost (변경 비용) | Number of changes in the period and its rank, average number of files changed together, file pairs that often change together, file line count, number of existing files (besides new files) that must be changed to add one new kind (an entry such as a weapon or a skill) | `vcs_churn.py`, code reading |
| Bug frequency (버그 빈도) | Among the changes to that file, the number linked to bug tickets; the number of times the same function was fixed again | Ticket keys from `vcs_churn.py` + issue tracker lookup |

## 2. Collecting the numbers

Conversation runs and unattended runs follow the same order. An unattended run does not ask (1) and does not query the issue tracker (5).

1. **Period**: Use "Refactoring history period" in the judgment criteria table of the check ledger. If it is empty, a conversation run asks the user. An unattended run skips 2 to 5, and leaves the fields where those numbers go as "no data (period not set)" (자료 없음(기간 미정)).
2. **Check that read commands are allowed**: Profile `vcs_read_commands` must have `git log` for git (also `git rev-parse` if you count lines), and `p4 changes` and `p4 describe` for p4 (also `p4 fstat` if you count lines). This is the same in conversation and unattended runs (common rules §7). If they are not there, do not run it, and write it in "Not checked".
3. **Comparison scope**: A rank has meaning only if there are other files to compare with. In `--path`, give not only the target file but the module folder that contains the target, or `source_roots`, and read the target's rank within it. If you give only the target path, the target always comes out first, and it cannot be used for the judgment. Write the comparison scope in the report.
4. **Run** (if `python` is not available, `python3`):

   ```
   python "<플러그인 폴더>/scripts/vcs_churn.py" git --repo "<프로젝트 루트>" --since <시작일> --path <비교 범위> --sizes
   python "<플러그인 폴더>/scripts/vcs_churn.py" p4 --cwd "<프로젝트 루트>" --path <비교 범위 depot 경로>/... --since <시작일> --sizes
   ```

   - If the target file is not in the file table (top 30 by default), increase `--top` and run it again. If it is still not there, write "outside the top N" (상위 N위 밖).
   - If you know the ticket key prefix (judgment criteria table of the check ledger), give `--ticket-prefix <접두사>`. If you do not know it, a person filters out the non-keys from the resulting key list.
   - If "상한에 걸림" (limit reached) appears, shorten the period or increase `--max-changes`, and run it again.
   - "검색 실패(시간 초과)" (search failed (timeout)) is not 0 results (common rules §4). Narrow the path or the period and run it again.
5. **Whether it is a bug**: The script does not look up ticket types. If the session has an issue tracker tool, query **all the collected keys at once** and receive only the issue types (if there are many keys, you can split them into groups of 100, but do not ask separately for each file). For the issue types and labels counted as bugs, use the value in the judgment criteria table. If it is not there, ask the user. If there is no tool, or it is an unattended run, leave only the key list in the report and set the bug frequency axis to "no data" (자료 없음). Even in this case, judge the change cost axis with the numbers from 1 to 4 and 6.
6. **Number of files to change to add one new kind**: Have `advisors:analyst` find the places in the target system that branch by kind (list registration, branch statements, data tables), and count them. In the instruction, put "file:line and whether that place must be changed for each kind" as a field to return.

## 3. Judgment

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

- Do not make up absolute threshold values. If the judgment criteria table has no criterion, use the temporary criteria below, write "(temporary criterion)" ((임시 기준)), and raise setting the criterion in "Decisions needed".
  - Change cost axis: the rank of the number of changes within the comparison scope is in the top 10
  - Bug frequency axis: 2 or more changes linked to bug tickets (bug fixes recurred)
- Write an axis without numbers as "no data". Do not count it as "not applicable" (해당 없음). Even if no axis applies, if there is a "no data" axis, set it to on hold instead of not recommended, and write the missing data.

| Judgment (판정) | Condition |
|---|---|
| Recommended (권장) | Two or more axes apply. Or the performance axis is Priority 1 and it is a structural problem |
| On hold (보류) | Only one axis applies. Look again in the next check |
| Not recommended (비권장) | No axis applies. It is code to be retired ("Paths excluded from checks" in the judgment criteria table). It is engine code (look at solutions on the game code and settings side first; cleaning up engine-modification blocks is the 'engine modifications' scope of the TD advisor's structure audit) |

- Do not recommend for the reason "it is hard to read" alone.
- Even if performance is good, you can recommend based on the two axes of change cost and bug frequency. In this case, write "not a performance reason" (성능 근거 아님) in that row of the report, and do not mix it with the performance grade judgment.
- When you recommend, first propose a behavior-locking test (`tests.md`). If a test cannot be set up, reduce the refactoring scope, or write a measurement or manual check procedure instead.
- The judgment is a proposal. Hand the actual refactoring to `code_change_entry` after user approval, and mark the approval level (`tests.md` item 4) with it.

## 4. Report table

```markdown
| Target (대상) | Performance (성능) | Change cost (변경 비용) | Bug frequency (버그 빈도) | Judgment (판정) | Command that produced the numbers (수치를 낸 명령) |
|---|---|---|---|---|---|
| <file or system> | <grade, measured value, whether it is a structural problem / no data (자료 없음)> | <N changes (rank N within comparison scope <path>), average N files changed together, N lines> | <N bug tickets / N ticket keys / no data (자료 없음)> | recommended (권장) / on hold (보류) / not recommended (비권장) (not a performance reason (성능 근거 아님)) | <script command, issue tracker query> |
```
