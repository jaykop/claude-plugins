# Evaluation axes and grades

Read this in Full review Step 1-7 and Change check Step 2-7.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. Axis list

Use the six basic axes. If profile `ip_based` is a source IP name, add a seventh axis (Source IP match).

| Axis | What it asks | Main evidence | Condition for judgment withheld |
|---|---|---|---|
| Genre demand (장르 수요) | How much games under these conditions sell and are used recently | The performance distribution of the comparison set (median, quartiles), recent metrics of benchmark titles, trend judgment results | The performance metric exists for fewer than half of the games in the comparison set |
| Competition density (경쟁 밀도) | How many games share the same conditions, and whether our differentiators already exist | The number of released and announced games with the same conditions in the 'recent' window, the number of competitors in the feature comparison table that have our differentiators, competitor-for-player-time games | The comparison set could not be made. If there is no feature list, grade only up to Neutral from the number of released games |
| Platform (플랫폼) | Whether the chosen platforms reach players of this genre in the chosen regions | The platform share in the region table (mark the data unit), the platform mix of direct competitors and their public results per platform | `platforms` or `regions` is empty |
| Price and business model (가격·수익 모델) | Where our price and business model sit in the competitor distribution | The position of our expected price (`market.price_band`) in the competitor list price distribution (`market_calc.py position`), the performance of competitors with the same business model, the count of price and monetization complaints in reviews | `business_model` is empty. If `market.price_band` is empty, show only the distribution, and the position is judgment withheld |
| Release timing (출시 시점) | Whether big releases aiming at the same players cluster before and after the planned release | Announced games within 3 months before and after the planned release, planned releases of direct competitors, large update announcements of competitor-for-player-time games, how long trends stay valid | `release_window` is undecided |
| Audience fit (이용자층 적합) | Whether the target that the team set (`market.target_player`) matches the confirmed audience | Values at a confirmed unit, indirect signals (`audience-regions.md`) | `market.target_player` is empty |
| Source IP match (원작 일치) (only when IP-based) | Whether the source IP's audience overlaps with the new game's target | §5 | Fewer than two countable items |

## 2. Favorable-side signals and unfavorable-side signals

| Axis | Favorable-side signals | Unfavorable-side signals |
|---|---|---|
| Genre demand | A feature judged as a rising trend overlaps with our conditions. Games at or above the median keep coming out among the 'recent' releases. Recent metrics of benchmark titles hold | It was judged a declining trend. Most 'recent' releases are below the median |
| Competition density | Few released and announced games share the same conditions. No or few direct competitors have our differentiators | Many released games share the same conditions, and most of them already have our differentiators. There are competitor-for-player-time games that hold the same players |
| Platform | It is confirmed that the chosen platform has a large share in the chosen regions. Direct competitors produced public results on the same platform | It is confirmed that the platform has a small share in the chosen regions. Most direct competitors center on other platforms |
| Price and business model | Competitors in the same price band with the same business model performed at or above the median. Their reviews have few price complaints | The expected price is at the upper end of the distribution, and the reviews of games in the same band have many price complaints. Most games with the same business model are underperforming cases |
| Release timing | No large announced game aiming at the same players within 3 months before and after | Benchmark-title-level announced games or direct competitors cluster within 3 months before and after. The trend that we rely on is "may have passed by release" |
| Audience fit | The target and the confirmed values and indirect signals point the same way | They do not match |
| Source IP match | Reviews of the source IP that request elements of the new game appear in the sample. The main review languages of the source IP overlap with `regions`. The source IP produced results on the main platform of the new game | The play modes of the source IP and the new game differ, and there are almost no requesting reviews. The languages and platforms used for the source IP do not overlap with our `regions` and `platforms` |

Signals only give a direction for choosing evidence. Grade only by the rules in §3.

## 3. Axis grades

| Grade | Condition |
|---|---|
| Favorable (유리) | There are two or more pieces of evidence that point to the favorable side, and at least one of them has confidence "confirmed". You wrote the counter-evidence, and it is weaker |
| Unfavorable (불리) | There are two or more pieces of unfavorable-side evidence, and at least one is "confirmed". Also write what would make it better if it changed |
| Neutral (중립) | There are two or more pieces of evidence, but the directions are mixed, or they point the same way but the effect is small (for example: the expected price is in the middle of the competitor distribution) |
| Judgment withheld (판단 보류) | There is one piece of evidence or none, or all are "hypothesis", or a needed profile field is empty, or it leans to the favorable or unfavorable side but has no "confirmed" evidence at all (whether because of the restrictions in §4 or because the material is only "estimated"). If it leans to a side, write it together, as in "judgment withheld (favorable side)" (판단 보류(유리 쪽)), and write what would make a judgment possible |

- Apply the rules mechanically. This keeps the grade from leaning toward seeing the project favorably, and from pessimism without evidence.
- Count evidence separately only for different metrics or different primary sources. Two articles that cite the same original source count as one.
- In a change check, re-grade only the axes whose evidence changed. If you change a grade, write the previous grade, the new grade, and the changed evidence side by side.

## 4. Confidence and restrictions

### 4-1. Confidence

| Confidence | Meaning | Common level (rules.md §1) |
|---|---|---|
| confirmed (확인) | In this run you saw primary material directly (official platform material, official publisher announcements, the original text of an official survey, original data received with a script this time), and you confirmed the number from an original sentence or script output | confirmed (확인함) |
| estimated (추정) | Estimation tool values, press citations of paid material whose original you did not see, numbers from secondary articles whose original source you did not find, indirect signals, summary numbers for which you could not quote the original sentence | estimated (추정) |
| hypothesis (가설) | An interpretation that rests on only one piece of evidence or on one indirect signal. Also write what to look at to confirm it | estimated (추정) (the weakest) |
| not checked (확인 못 함) / query failed (조회 실패) | There is no material, or it did not open | unknown (모름) |

- At the end of each judgment sentence, attach one of confirmed / estimated / hypothesis.
- Write the confidence of an axis as the strongest of the evidence that supports the grade, but if a restriction below applies, do not go over its upper limit.

### 4-2. Restrictions

| Restriction | Condition to apply it | Effect |
|---|---|---|
| No main-platform numbers (주 플랫폼 수치 없음) | The first item of `platforms` is not Steam (console, mobile, another PC store) | Mark Steam metrics as "supporting signal" (보조 신호), and do not count them as "confirmed" evidence. If there are no separate primary numbers for the main platform, the upper limit of that axis's confidence is "estimated" |
| Indirect signal (간접 신호) | The evidence is a metric marked `[indirect]` | That evidence is "estimated" or lower |
| Not genre-level (장르 단위 아님) | The audience evidence is at the whole-country or whole-platform unit | The upper limit of the Audience fit axis's confidence is "estimated" |
| Old data (오래된 자료) | The base period of a market metric (sales, reviews, concurrent players, rankings, interest metrics) is older than 12 months before the access date. For player surveys and industry reports that come out every year, do not apply this restriction if it is the latest edition; write only the edition year (`metrics.md` §4) | Attach the "data from YYYY" (YYYY년 자료) warning, and do not use it as evidence that changes a grade |
| Assumed values (가정값) | You put assumed values in the profile's "undecided" fields and evaluated | For each axis, write which assumption it is based on |
| Citing another advisor's report (다른 고문 리포트 인용) | rules.md §1 | Use the original grade as it is. If it is older than the reference period, mark it "outdated report" |

## 5. Source IP match axis

Use it only when profile `ip_based` is a source IP name.

- Fill it only with items that can be counted from public material.
  - Public results of the source IP: numbers announced by the publisher. Write the metric kind in the original wording (`metrics.md` §3).
  - Release timing of the source IP per platform.
  - The number of reviews of the source IP that request a specific element (for example, the play mode that the new game adds). If the source IP is on Steam, fetch them with `steam_reviews.py`, classify them, and write "k of N". If it is not on Steam, it is "not checked".
  - The language distribution of the source IP's reviews compared with `regions` `[indirect]`.
- If the play mode of the source IP (single / co-op / versus) differs from the new game's `play_mode`, do not assume that the audiences overlap. It goes to Favorable only if two or more pieces of evidence of overlap come from the items above.
- You can use the source IP name as a search term. But do not put the source IP name in a search term together with the new game's genre, play mode, or features. Use the source IP name alone, or only with words that look for facts about the source IP itself (sales, release, platform, reviews). Keep `search_banned_combos`.

## 6. Axis detail format

```markdown
### <axis name>
- Grade / Confidence / Restriction (등급 / 확신도 / 제한):
- Evidence (source numbers) (근거 (출처 번호)): one line per piece of evidence, ending with confirmed / estimated / hypothesis
- Counter-evidence (반대 근거):
- The grade changes if this information appears (이 정보가 생기면 등급이 바뀐다):
```
