# Choosing competitors and judging trends

Read this in the survey conditions (Step 1-1), competitor selection (Step 1-4), and trend judgment (Step 1-6) of a full review, and in setting the scope (Step 2-3) and maintaining the list (Step 2-5) of a change check.
Save the selection result in `<report_dir>/_state/market-competitors.md`. Its format follows the shared `shared/state-formats.md`.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. How to tell games apart

- Give each game its unique store identifier, and write it in the "identifier" column of `market-competitors.md`. For a Steam game, it is `steam:<앱 ID>`. Otherwise, it is the store product page URL (including console stores). If there is no store page (for example, a game that is only announced), leave it as "none", and write the official page address in the "Selection evidence" column. A change check queries again with the value in the identifier column.
- Do not mix remasters, region-specific titles, different games with the same name, demos, or free editions with the main game. If the identifiers differ, count them as different games.
- Once you give a list ID (`MC-001` …), do not change it. Even if you remove a game from the list, do not delete the row. Append `removed YYYY-MM-DD — <reason>` (`제외 YYYY-MM-DD — 이유`) to the end of the "Selection evidence" column.

## 2. Survey conditions (fixed in the report header)

Before you choose competitors, set the three items below and write them in "Survey conditions" at the top of the report. A change check uses the values of the most recent full review report as they are (a change check report does not have these three cells).

| Condition | How to set it |
|---|---|
| Base tags, 3~5 | Convert profile `genre` to store tags. In a conversation run, get them confirmed by the user together with the competitor list |
| Price bands | About four bands in the main region's currency. Example: "under USD 20 / 20~39.99 / 40~59.99 / 60 and over". Put free-to-play in one band, "free to start" (무료 시작) |
| Performance metric | Choose one in the order of §5 below |

## 3. Direct competitor conditions (six)

| Symbol | Condition | Judgment |
|---|---|---|
| a | Tags | The store tags (top user tags) overlap with the base tags by 3 or more |
| b | Platform | At least one of profile `platforms` is the same |
| c | Business model | The same as profile `business_model` |
| d | Price band | The same band in the price bands of §2. Set our band with profile `market.price_band`. If it is empty, d is not checked |
| e | Release period | Released, or announced as planned for release, between 36 months before our planned release start date and 12 months after the end date. The start date and the end date are `release_window` converted to dates (today if undecided), and get the range with `market_calc.py window`·`next` |
| f | Play mode | The same as profile `play_mode` (single / co-op / versus / mixed) |

- Count a condition that you could not check as not met. Write it in the "Selection evidence" column, as in "a·b·c·f met, d not checked".
- Call the games that meet four or more conditions the **comparison set**. Direct competitors and underperforming cases all come from the comparison set.

## 4. Five groups

| Group | Count | Condition to include | Where it is used | Where it is not used |
|---|---|---|---|---|
| direct competitor (직접 경쟁) | 5~8 | From the comparison set, among the rest after removing the ones chosen as underperforming cases, in order of the most conditions met | All axes, trend judgment, feature comparison | |
| benchmark title (기준작) | 2~3 | Successful titles that represent the genre. No release period limit. The company's previous titles go only in this group | To look at the upper end of this genre on the Genre demand axis | Sentences that compare directly with us |
| underperforming case (부진 사례) | 2~3, you must include them | From the comparison set, games whose performance metric is below the comparison set median, from the lowest | Survivorship bias check, trend judgment, feature comparison | Stating the cause of failure as settled |
| competitor for player time (이용자 시간 경쟁) | Usually 1~3 | Large live-service games that use the same players' time, even if the business model differs | Release timing axis, supporting evidence for the Competition density axis | Performance median, feature comparison |
| precedent only (선례 전용) | - | A mark that design attaches when the design advisor uses a game outside the list as a precedent | market does not use it | |

- Why you must include underperforming cases: to prevent the mistake of looking only at successful titles and reading what they share as the cause of success (survivorship bias, the error of drawing a conclusion only from the cases that survived). If the comparison set has no game below the median, collect candidates once more (§6). If there is still none, write "no underperforming case found" (부진 사례 찾지 못함) in Not checked.
- Include the games that the user named (`market.competitors_seed`) even if they do not meet the conditions. Write which group you put each one in and the conditions met in the "Selection evidence" column. If it meets fewer than four, do not put it in direct competitor; put it in benchmark title or competitor for player time.
- Do not attach evaluative words such as "failure" to a game that you put in underperforming case because of low performance. Write only the metric values.

## 5. Choosing the performance metric

Choose one metric that exists for all games in the comparison set **from the same source with the same definition**. The order is as follows.

1. Official sales announcements of the same kind (only when they exist for every game with the same metric kind. For metric kinds, see `metrics.md` §3)
2. The cumulative review count on the same store (for Steam, the cumulative review count that `steam_reviews.py count` returns). Do not convert it to sales; use it only to compare order
3. Values from the same estimation tool (write the tool name. The confidence is "estimated")

- Write the chosen metric and the reason in the survey conditions.
- Leave a game without a value as "not checked", and exclude it from the median calculation. Write the number excluded.
- Cumulative values lean toward games released long ago. Also write the months since release in the table, and write this difference as counter-evidence on the Genre demand axis.
- If the main platform is not Steam, metric 2 is a "supporting signal" (`axes-and-grades.md` §4).
- Get the median and the quartiles with `market_calc.py stats`.

## 6. What to keep in candidate collection

- Give candidate collection to web-scout. The search topics are only the base tags, platforms, the release period, and public game names. Do not hand over our game's feature list.
- Do not collect candidates only from articles that summarize successful titles, such as "the hits of the year". Also look at new release lists per tag, store search results, and release schedule summaries. This keeps underperforming cases from dropping out of the candidates.
- Look up the games that the user named separately, by name.

## 7. Maintaining the list (change check)

- Query the previous list again as it is. When you change the list, write the reason.
- Filter new and announced games with the same conditions that came out after the previous access date with §3, and write them in the report as "additional candidate" (추가 후보). In a conversation run, add them to the list if the user confirms. In an unattended run, do not add them to the list.
- When you move a game between groups (for example, direct competitor → underperforming case), keep the ID, and append the date of the move and the evidence metric to the "Selection evidence" column.

## 8. Trend judgment

### 8-1. "Trend" and "case"

Write "trend" (흐름) only when all three of the following are met.

1. There are 3 or more games with the same feature in the comparison set, and all of them were released within the 'recent' window (for releases).
2. Those 3 or more are at or above **the median of the direct competitor group** on the performance metric. The direct competitor group is chosen from the games other than the underperforming cases, so its median differs from the comparison set median. Use the comparison set median when you choose underperforming cases, and the median of the direct competitor group for trend judgment. In 8-1 and 8-2 below, "median" always means this value. Get it by putting only the values of the direct competitor group into `market_calc.py stats`.
3. That performance was confirmed at two or more points in time with the same metric from the same source. In the first full review, you can confirm it with past values that the same source gives (two quarterly results, a monthly review distribution, and so on). If there are no such values, leave it as "case (before the two-point check)" (사례(두 시점 확인 전)), and look again in the next change check.

If even one is missing, it is a "case" (사례). Do not count the number of times something was talked about in articles as evidence.

Judge a "declining trend" (내려가는 흐름) by the same rules. Write it only when 3 or more games with the same feature are below the median and this was confirmed at two or more points in time.

### 8-2. Survivorship bias check

If you extracted a common feature from the success side (at or above the median), you must also count how many games below the median (including underperforming cases) have the same feature. Write the two sides side by side in the trend table, as in "k of n at or above the median / j of m below the median" (중앙값 이상 n개 중 k개 / 중앙값 미만 m개 중 j개). Write it as a success-side feature only when the ratio on the at-or-above side (k/n) is higher than the ratio on the below side (j/m). If it is the same or lower, do not use it as a success factor. If there are fewer than 2 games below the median (m < 2), they cannot be compared, so leave it as a "case".

### 8-3. Whether it will last until release

- If 18 months or more remain until release and the trend appeared only in the last 12 months, mark it "may have passed by release" (출시 때 지나갔을 수 있음).
- Calculate release timing with `market_calc.py window` and `next`.

## 9. Feature comparison table

- The rows are our game's features (the list that the main agent made in Full review Step 1-2). The columns are the direct competitors and the underperforming cases.
- In the cells, write only "has (있음) / does not have (없음) / not checked (확인 못 함)" and the source number. The evidence is material whose original text web-scout quoted, such as store descriptions, official pages, and official announcements.
- Do not write how fun the feature is or how well it is made.
- Do not continue "only we have it" or "we do not have it" into "so let us add it / remove it". Pass anything about game content to design as a question.
- Do the comparison in the main agent after collection ends. Have web-scout only bring the competitors' feature lists in the original text.
