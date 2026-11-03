# Engine version checklist

Use it when the target of a single-technology diagnosis is **one engine version**. Use it only when the user named a version ("5.x 로 올려야 해?") or when such a question came to the technology trend advisor (radar) in the question inbox. A periodic check does not run this checklist. It only accumulates, each run, rows in the "Blockers when upgrading to the next version" table of `radar-watchlist.md`.

The procedure is the same as the single-technology diagnosis (D1~D5). This file decides what to look at in D2 and D3, and what to rate in D4.

## Starting point

1. From the "Blockers when upgrading to the next version" table of `radar-watchlist.md`, take all rows whose status is "open". Do not investigate again what has already accumulated. Check again only the rows whose "Last check date" is more than 30 days ago.
2. Check the decision owner. An engine upgrade is the job of profile `decision_owners.tech`. If the user is not the decision owner, write the whole report as a "reference option" (rules.md §8).
3. The advisor does not conclude whether to upgrade or not. Organize what blocks and what is gained in countable units, and put the decision in "Decisions needed" with the decision owner.

## Check items

| # | Item | Where to check | Who does it |
|---|---|---|---|
| 1 | Version difference and the list of versions in between | Our version: technology inventory. Target version and versions in between: list of primary release notes | web-scout |
| 2 | Among planned deprecations, removals, and API changes in the versions in between, the ones that affect what we use | Primary release notes. Compare against the engine plugins in the technology inventory whose state is "in use", "on, no sign of use", or "used with engine modifications", and the features in the settings table | web-scout (in parallel, one per version) + comparison by the main agent |
| 3 | How the Experimental and Beta plugins we turned on change in the target version | `IsExperimentalVersion`, `IsBetaVersion` in the evidence column of the technology inventory → release notes of the target version | web-scout |
| 4 | Engine modification blocks (source build only) | Total count and distribution by folder: technology inventory. The engine area of each group (runtime / editor / tool program / plugin / shader / other) and its classification (candidate to move out of the engine / can be removed after an engine upgrade / check needed whether the engine developer fixed it / must be kept / unknown), and the merge risk evidence: if `_state/td-engine-mods.md` exists, quote it as is (if it does not exist, "before the TD advisor structure check" (TD 고문 구조 점검 전)). If it differs from the block count in the technology inventory, use the one counted later, as the rule in shared/state-formats.md says. Whether that folder changed a lot in the target version: change descriptions in primary sources or a comparison of the public source. If it cannot be checked, "unknown". If the team has a procedure document for engine upgrades (profile `td.rule_docs`), quote that procedure as the way to check actual merge conflicts. The advisor does not run it | main agent (script) + web-scout |
| 5 | Project settings whose name or default value changed in the target version | Settings table of the technology inventory → primary sources | web-scout |
| 6 | Support mark of the target version for each target platform | Public material only. For private console information, "the platform's private documents must be checked" (플랫폼 비공개 문서 확인 필요) | web-scout |
| 7 | Whether outside vendor plugins (public products) support the target version | Vendor's public material. Search only the ones in the "Project plugins confirmed as public outside products" table of radar-watchlist. For a project plugin not in the table, in a conversation run ask whether it is an outside product, and if the answer is yes, put it in the table and then search. Do not search plugins that the project made itself; for those, write only "check whether code work is needed" (코드 작업 필요 여부 확인) (unattended: do not ask, and write it in "Not checked") | web-scout |
| 8 | Whether it overlaps with the next milestone | Profile `next_milestone`. Calculate the remaining days with `date`. If there is no evidence for the work duration, "unknown" | main agent |
| 9 | What is gained | New features of the target version that connect to the problem list (Step 2). For each feature, the three verdict columns of verdict-rules.md | main agent |
| 10 | Way to roll back | Whether there is a branch that keeps the previous engine, and so on. Write it as an item to confirm with the user | main agent |

- Items 2, 3, and 5 are not "copy the whole change list". Keep only the lines that touch what is in the technology inventory.
- For the impact on project files (the number of files that use a changed API), give analyst the search expression and count. Write the search expression and the result count together.

## Table to put in the report

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

```markdown
| # | Check item (점검 항목) | Result (결과) | Blocking level (걸리는 정도) | Evidence (근거) |
|---|---|---|---|---|
| 2 | <API that changes> | used in N of our files (search expression '...') | work needed (작업 필요) | <release notes URL>, checked YYYY-MM-DD |
```

The blocking level is one of four: blocked (막힘) / work needed (작업 필요) / no impact (영향 없음) / unknown (모름).

## Relation to the accumulated table of the periodic check

- Step R5 of the periodic check adds, among the findings of ① (changes to technologies we use now), only the ones that block the next version, as `UP-` rows. In effect, part of check items 2, 3, and 4 above accumulates each run.
- After running this checklist, add the newly found blockers as `UP-` rows, and change the status of resolved rows to "resolved".
