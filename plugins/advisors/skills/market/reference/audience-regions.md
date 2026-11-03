# Audience, regions, and hardware share distribution

Read this in Full review Step 0-5 (first-run notice), Step 1-5 (collection), and Step 1-7 (Audience fit axis).

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. Limits to announce first on the first run

If this is a conversation run and there is no market report at all (first run), announce the content below before you start collection. If this is an unattended run, write the same content in the report's "Not checked" section.

> 시작 전에 한계부터 말씀드려요. 장르 단위로 나눈 연령·성별 공개 자료는 거의 없어요. 그래서 이용자층은 두 가지로만 채워요. 하나는 자료가 원래 조사한 단위(국가 전체, 플랫폼 전체 등)를 밝힌 값이고, 다른 하나는 리뷰 언어 분포나 커뮤니티 규모 같은 간접 신호예요. 또 일부 통계 사이트는 자동 조회를 막아서, 그 값이 필요하면 화면 캡처나 CSV 로 넘겨 주셔야 해요.

## 2. The audience has only two columns

| Column | What goes in it | Notation |
|---|---|---|
| Values at a confirmed unit (확인된 단위의 값) | Values that a public survey or official material measured directly | The value, **the original unit of the material** (all gamers in a country / platform users / genre players / players of a specific game), the sample, the age range, the base period of the material, the source number |
| Indirect signals that can stand in (대신 쓸 수 있는 간접 신호) | Review language distribution, community size (official community member count and so on), streaming viewership statistics, published game motivation surveys | `[indirect]` (`[간접]`) in front. What it stands in for, and its limits (for example: the sample of a motivation survey is people who came and answered by themselves, so it leans toward enthusiastic players) |

## 3. What not to do

- Do not write stereotype sentences without evidence. Example: "This genre is centered on men in their 20s and 30s". Find and delete such sentences in the self-check before saving.
- Do not carry a whole-country distribution over as if it were a genre player distribution. The same applies to a platform user distribution.
- Do not give "confirmed" to the Audience fit axis from material that is not at the genre level.
- Do not fill one region's cells with another region's material.
- If the survey methods (age range, sample, year) differ, only list the regional numbers side by side. Do not write comparison sentences such as "X is higher".
- Leave a cell that you could not check as "not checked". Write the number of unchecked cells in the report summary so that the gaps are visible.

## 4. Comparison with the target player

- `market.target_player` is a decision that the team made. market does not change this value.
- The comparison result is one of "match (일치) / mismatch (어긋남) / judgment withheld (판단 보류)". If `market.target_player` is empty, it is judgment withheld.
- If they do not match, write the difference and the evidence in the report's "Decisions needed", and leave it as a question to confirm with the person who set the target. The design advisor uses only the target in the profile, so a person decides whether to change the target.

## 5. Region table

- Handle only the regions in profile `regions`. Call one web-scout per region, in parallel, in one message.
- Fill the same six cells for each region.

| Cell | Content |
|---|---|
| Platform share (플랫폼 비중) | The usage or revenue share per platform in that region. Mark the data unit |
| Genre signals (장르 신호) | How visible this genre is in that region's public rankings and surveys |
| Price and payment practices (가격·결제 관행) | Regional pricing policy, the main payment methods, free-to-play practices |
| Age rating and release approval (연령 등급·출시 허가) | The rating body and its criteria, the government release approval system |
| Language and localization (언어·현지화) | The required languages, voice localization practices |
| Data gaps (자료 공백) | What you did not find in this region. You must fill it |

What to check in the original text for each region:

- For a region that requires government release approval, write official release and use through global stores separately.
- Check in the original text whether a sales ranking counts only packages or includes digital, and whether it is by revenue or by units.
- If the region counts the use of shared venues such as PC bangs (PC방) separately, also look at that material when the game is a PC online game.
- Check the age rating criteria and procedure in the original text of the rating body.
- Write amounts in that region's currency as they are.

### Sources to look at first per region

For each region, write the sources in the row below, in order, with names and addresses, into "Sources to look at first" of the web-scout "form D" brief (web-scout cannot read files). The addresses and the access check results at the time of writing are in `metrics.md` §7. This table is also a starting point, not the correct list. Choose the row that matches the region name in profile `regions`. If the region is not in the table, have web-scout find that region's public institutions, rating bodies, and regional media.

| Region | Sources to look at first (in order) | What was blocked or empty (at the time of writing) |
|---|---|---|
| Korea (한국) | 한국콘텐츠진흥원 (KOCCA) 게임이용자 실태조사 (game user survey) · 게임백서 (game white paper) → 게임물관리위원회 (GRAC, rating) → 인벤 (Inven, articles) | KOCCA report page address not checked. 디스이즈게임 (ThisIsGame) 403 (access denied) |
| Japan (일본) | Famitsu weekly sales ranking → CERO (rating) | A Japanese player survey source was not searched for at the time of writing |
| North America (북미) | ESA Essential Facts → Circana press releases → PlayStation Blog download rankings → ESRB (rating) → Game Developer (articles) | Circana address not checked (404). GamesIndustry.biz blocked by the tool |
| Europe (유럽) | PlayStation Blog download rankings → PEGI (rating) | A European player survey source was not searched for at the time of writing. GamesIndustry.biz blocked by the tool |
| China (중국) | NPPA (국가신문출판서) release approval notices | Chinese market and player sources were not searched for at the time of writing. Find them with form D on the first run |
| All regions (지역 공통) | Review language in the official Steam review JSON `[indirect]` → language share in the Steam Hardware & Software Survey `[indirect]` | SteamDB 403, Gamalytic table values not visible, Newzoo blocked by the tool, Quantic Foundry 403 |

A blocked source is "a person must export it" (`metrics.md` §6). Do not go around to open it through another address. If needed, get a capture or a CSV from the user.

## 6. Hardware share distribution

- Only market does this query. radar and perf read only the profile's `target_spec`.
- Query only when `platforms` includes PC. Collect the values of the last 3 months from the platform's official survey (for example, the Steam Hardware & Software Survey). Do not judge from the value of one month.
- Calculate averages and sums (for example, the sum of the shares at or above a certain memory size) with `market_calc.py stats`.
- This survey cannot tell specs per genre or sales shares per country. The language distribution of the survey is an `[indirect]` signal.
- Go only as far as a **proposal** to change `target_spec`. In the report's "Decisions needed", write the value to change, the evidence (source numbers, average over how many months), and the current value. If the user confirms it in a conversation run, write it to the profile at that time and change `updated` to today's date. In an unattended run, do not write the profile.
