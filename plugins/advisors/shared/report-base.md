# Common report format

Every advisor report follows the header and the section order below. In the "Body" (본문) place, put the body format of each skill.

A report uses the English names and fixed values below when profile `report_language` is `en` (the default), and the Korean ones in parentheses when it is `ko`.

```markdown
# <advisor name> <mode> — <YYYY-MM-DD>

| Item (항목) | Value (값) |
|---|---|
| Written (작성일) | YYYY-MM-DD (system date) |
| Run mode (실행 방식) | conversation (대화) / unattended (무인) |
| Base revision (기준 리비전) | P4 CL number, or the first 12 characters of the git commit. If it could not be checked, "not checked" (확인 못 함) |
| Profile updated (프로필 갱신일) | the updated value of profile.md |
| Previous report (직전 리포트) | path of the most recent report of the same mode. If there is none, "none" (없음) |
| Baseline report (기준 리포트) | (optional) the report that is the baseline for the comparison. Example: the full review that a change check uses as its baseline. If there is none, delete the row |
| Scope (범위) | what this run looked at. Also write the team reference notes that were read (paths) and the result feedback row IDs (start.md 0-F) |

## Summary (요약)
At most three lines. Only the conclusion and the most important evidence.

## Decisions needed (결정이 필요한 것)
Only what a person must decide. For each item, write the decision owner (profile decision_owners). If there is nothing, "none" (없음).

## Body (본문)
<format of each advisor>

## Changes since the previous report (지난 리포트와 달라진 것)
Only when there is a previous report. New items / items that are gone / items whose grade changed.

## Not checked (확인 못 한 것)
Material that could not be read, failed searches, empty profile values. For each one, what would make it possible to check.

## Questions passed to other advisors (다른 고문에게 넘긴 질문)
The list of IDs of the questions posted to _state/inbox.md.

## Next check condition (다음 점검 조건)
A date or a condition. It must be the same value as the `Next check:` line (`다음 점검:` in a Korean file) of the _state file. Write that line exactly in one of the two forms (rules.md §11, state-formats.md "Literal tokens that scripts read").
```

## Evidence notation examples

- File: `Docs/Combat/dodge.md:42` — path and line number
- Web: `<title> (<URL>, published YYYY-MM-DD, accessed YYYY-MM-DD)` — when `report_language` is `ko`: `<title> (<URL>, 발행 YYYY-MM-DD, 조회 YYYY-MM-DD)`. If the publish date was not found, "publish date unknown" (발행일 미상)
- Measurement: `<file path> — <scenario ID>, <build configuration>, <measurement count>`
- Calculation: the formula, the input file and rows, the command that was run
