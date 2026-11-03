# market-snapshot.md format

File: `<report_dir>/_state/market-snapshot.md`. Only market writes and reads it. It is the comparison baseline of a change check, and the history used for the "comparison at two points in time" of trend judgment. Update it in Step Final.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

```markdown
# Market numbers record (시장 수치 기록)

Next check: YYYY-MM-DD
Written by: market / Last updated: YYYY-MM-DD / Base revision: <CL or commit; if none, not checked>

## Metrics (지표)

| Metric ID (지표 ID) | Game (게임) | Metric (지표) | Value (값) | Source (출처) | Base period (기준 기간) | Accessed (조회일) | Note (메모) |
|---|---|---|---|---|---|---|---|
| MS-001 | MC-003 <game name> | Steam cumulative review count (all languages, all purchase types) | 12,340 | Steam review JSON, steam_reviews.py count | Cumulative from release to the access date | YYYY-MM-DD | |
| MS-002 | MC-003 <game name> | Steam cumulative review recommendation ratio | 87.2% | Steam review JSON, steam_reviews.py count | Cumulative from release to the access date | YYYY-MM-DD | supporting signal |
| MS-003 | MC-005 <game name> | Official sales announcement (units sold) | 1,000,000 | <publisher> earnings material <URL> | Cumulative to YYYY-MM-DD | YYYY-MM-DD | Original: "sold" |
| MS-004 | MC-006 <game name> | Average concurrent players over the last 30 days | query failed | <statistics site> | - | YYYY-MM-DD | Automatic lookup blocked, no user material |

## Axis grades (축 등급)

| Axis (축) | Grade (등급) | Confidence (확신도) | Restriction (제한) | Report (리포트) |
|---|---|---|---|---|
| Genre demand | Neutral | estimated | No main-platform numbers | market/YYYY-MM-DD-full.md |

## Review sample (리뷰 표본)

| Game (게임) | Sample rule (표본 규칙) | Original file (원문 파일) | Classification file (분류 파일) | Classification scheme (분류 체계) | Accessed (조회일) |
|---|---|---|---|---|---|
| MC-003 <game name> | recent, all languages, all purchase types, last 3 months, max 300 | market/data/YYYY-MM-DD/reviews-<앱 ID>.jsonl | market/data/YYYY-MM-DD/labels-<앱 ID>.csv | v1 | YYYY-MM-DD |
```

## Rules

- **The same metric ID means the same game, the same definition, and the same source.** If the definition or the source changes, make a new ID. In the note of the last row of the old ID, write "replaced by MS-0xx — not compared directly" (MS-0xx 로 대체 — 직접 비교 안 함).
- **Do not delete; add up.** Every time you query, add a new row with the same ID below. This makes the comparison at two points in time possible. `market_calc.py snapshot` reads, for each ID, the row with the latest access date among the rows that have a numeric value as the previous value.
- In the value column, write only the number and unit symbols (%, currency symbols, thousands separators). Put words such as "about" or "or more" in the note column. Write non-numeric values ("query failed" (조회 실패), "not checked" (확인 못 함)) as they are. The script does not use such rows as the previous value; it compares with the numeric row before them, and writes in the note column that it did so.
- Keep query failures as rows too. This lets the next check try the same source again.
- In the game column, write the ID and the name from `market-competitors.md` together. For a game outside the list, write "outside the list" (목록 밖).
- If the main platform is not Steam, write "supporting signal" (보조 신호) in the note of the Steam metric rows.
- Overwrite the "Axis grades" table with the current values after every report. The history stays in the report files.
- Keep only one row, the last sample, per game in the "Review sample" table. A change check uses the sample rule and the classification scheme of this row as they are. Do not change this row with a sample whose classification was not finished (for example, one that was only fetched in an unattended run). Write the paths of the fetched files only in the report.
- Write paths relative to `report_dir`.
