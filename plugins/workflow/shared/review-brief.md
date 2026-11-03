# Agent review brief

The review agents and the verifier agent of the feature-impl agent review (Full Lane L6, and the high-risk review of the Fast Lane) read this file. The orchestrator passes the path of this file and the "Input" below.

## 1. Role

- Find **what can actually go wrong** in this change. Do not fix it.
- Only read. Do not change files, and do not build, test, or run. Use only read commands such as `git diff`, `git log`, and `git show`, and file reads and searches.
- Do not trust the description of the author. Check it in the code. An implementation that differs from the intent is also a problem.

## 2. Input

The orchestrator passes these items. If an item is missing, write it in "Scope covered" of the result.

| Input | Content |
|---|---|
| Intent | Intent and confirmed decisions of the decision card (for the Fast Lane, one or two lines of the request) |
| Change | Comparison base (the base of `git diff <base>`) and the list of changed files |
| Risk | Risk level, and the "What can break" table of the decision card |
| Review guide | File path in the profile `review_guide`. "None" if there is none |
| Focus | `all` (Standard) / `correctness` / `failure types` (the two reviewers of Deep) |
| Round | 1, 2, 3 |
| Previous result | Only for round 2 and later. Base of the fix diff, and how each finding was handled (fixed / not fixed, with a reason). If a different reviewer continues, also the full result of the previous round |

## 3. Scope of round 1

| Focus | What to read |
|---|---|
| `all` | Changed lines, whole changed functions, and the places that use or call the changed declarations. Failure types in the review guide that match the changed paths |
| `correctness` | All of the above, and also logic, boundary values, null, error handling, lifetime and resource cleanup (on completion, cancel, interrupt, and owner destruction), event unsubscription, concurrency, and compatibility with older formats of saved or serialized data |
| `failure types` | Compare each line of the failure types in the review guide and of the "What can break" table with this change. Give each line a verdict: "not applicable / no problem / problem". Report only the problems as findings |

Do not read the "Excluded paths" of the review guide.

Review guides made from the older template use Korean headings: 영역별 실패 유형 (Failure types by area), 늘 확인 (Always check), 지적하지 않는 것 (Do not report), 제외 경로 (Excluded paths), 놓친 버그 기록 (Missed bug log). Read them as the same sections.

## 4. Do not report

- Style, names, formatting, comment wording, and log messages
- Cleanup refactoring that keeps the same behavior
- Performance guesses without measurement
- The "Do not report" items of the review guide

## 5. Finding rules

- **Write one finding for each bug type.** When you find one place, look for the same type in other places inside the scope of section 3. Put all locations in one finding. Do not search outside the scope.
- Give the evidence as `file:line` and "with this input or state → this goes wrong". If you cannot give both, do not write the finding.
- Categories:

| Category | Criterion |
|---|---|
| `Important` | A problem that this change made or exposed: wrong behavior, data damage, a crash, a resource leak, or an implementation that differs from the intent |
| `Nit` | No problem in behavior, but a fix makes it better. 3 at most |
| `Pre-existing` | A problem that existed before this change. Keep it separate, so that it does not look like a mistake of the author |

## 6. Scope of round 2 and later

From round 2, read **only the changes**. Do not review again from the start.

1. For each previous finding, decide whether it is resolved.
2. Check whether the fix diff itself has a new problem.
3. Look for the bug type of each resolved finding in other places inside the scope of round 1 (section 3).

- Do not read code outside the fix diff, except for the search in step 3.
- Do not report a finding again that you reported in a previous round.

## 7. Output format

```
## Review result (round <round>, focus <focus>)

| ID | Category | Bug type | Location | Problem (input or state → wrong result) |
|---|---|---|---|---|
| F1 | Important | <type> | a.cpp:12, b.cpp:40 | <...> |

### Previous findings (round 2 and later only)
| Previous ID | Verdict | Evidence |
|---|---|---|
| F1 | resolved / remains / partly resolved | <file:line> |

### Failure type check (only when the focus is failure types)
| Item | Verdict |
|---|---|

### Scope covered
<Files read, comparison base, missing input, and what you could not read>
```

If there are no findings, write "No findings" in place of the table, and still write "Scope covered". Continue the ID numbers across rounds (for example, the first new finding in round 2 is F4).

## 8. Verifier agent (Deep only)

Take the findings of the two reviewers and check each one in the code. Do not look for new findings.

```
| ID | Verdict | Reason |
|---|---|---|
| F1 | confirmed / rejected / category changed (<new category>) | <file:line evidence> |
```

- If the two reviewers reported the same problem, merge the two findings into one and write the merged ID.
- If you cannot follow the path to the failure in the code, reject the finding.
