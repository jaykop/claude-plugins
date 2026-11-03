# Report body format

Put this in the "Body" place of the shared format `shared/report-base.md`. The shared format handles the header table, Summary, Decisions needed, Changes since the previous report, Not checked, Questions passed to other advisors, and Next check condition. This file does not repeat them.

- The advisor name in the report title is "market advisor" (시장 동향 고문), and the mode is "Full review" (전면 평가) or "Change check" (변화 점검).
- In "Scope" of the header table, write the regions looked at, the groups looked at, the narrowed target (change check), and whether collection was done without agents.
- In the body, write the year and month (YYYY-MM) instead of words such as "this year", "these days", or "the last few months".
- Source numbers are the numbers of the "Sources" table at the end of the body. Attach one to every number.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## Full review body

```markdown
### Survey conditions (조사 조건)
| Item (항목) | Value (값) |
|---|---|
| 'Recent' window ('최근' 범위) | Releases YYYY-MM ~ YYYY-MM / metrics YYYY-MM ~ YYYY-MM (market_calc.py window) |
| Profile basis (프로필 기준) | Genre / play mode / platforms (from the first priority) / business model / regions / planned release (the profile value and the converted date range) / source IP |
| Competitor release period (condition e) (경쟁작 출시 기간 (조건 e)) | YYYY-MM-DD ~ YYYY-MM-DD (market_calc.py window·next) |
| Base tags (기준 태그) | 3~5 |
| Price bands (가격 구간) | Currency and bands. Our expected price (market.price_band) and its band |
| Performance metric (성과 지표) | The chosen metric and the reason |
| Assumed values (가정값) | Assumptions put in the profile's "undecided" fields. If none, "none" (없음) |
| Main platform restriction (주 플랫폼 제한) | none (없음) / no main-platform numbers (주 플랫폼 수치 없음) |
| Proposal label (제안 표기) | proposal (제안) / reference option (참고 선택지) (decision_owners.business: <value>) |

### 1. Axis evaluation summary (축별 평가 요약)
| Axis (축) | Grade (등급) | Confidence (확신도) | Restriction (제한) | Key evidence in one line (source number) (핵심 근거 한 줄 (출처 번호)) |
|---|---|---|---|---|
Unchecked cells (확인 못 한 칸 수): N (audience (이용자층) N, regions (지역) N, metrics (지표) N)

### 2. Competitors (경쟁작)
#### 2-1. Selected list (선정 목록)
| ID | Group (묶음) | Game (게임) | Identifier (식별자) | Release date (출시일) | Platforms (플랫폼) | Price and business model (가격·수익 모델) | Play mode (플레이 구성) | Conditions met (만족한 조건) | Reason chosen (고른 이유) |
|---|---|---|---|---|---|---|---|---|---|

#### 2-2. Public metrics (공개 지표)
| Game (게임) | Play mode (플레이 구성) | Months since release (출시 후 개월) | Performance metric value (성과 지표 값) | Review count / recommendation ratio (리뷰 수 / 추천 비율) | Average concurrent players, last 30 days (최근 30일 평균 동시 접속) | Official sales (metric kind) (공식 판매 (지표 종류)) | Estimated sales (tool, range) (추정 판매 (도구, 구간)) | Source number (출처 번호) |
|---|---|---|---|---|---|---|---|---|
Performance metric distribution (성과 지표 분포): (market_calc.py stats output table)

#### 2-3. Feature comparison (특징 비교) (write only has / does not have / not checked. Do not judge fun)
| Feature (특징) | Us (우리) | MC-001 | MC-002 | ... |
|---|---|---|---|---|

#### 2-4. Frequent topics in reviews (리뷰에서 자주 나온 말)
Classification scheme table (분류 체계 표) (name, what goes in / what does not go in, version)
| Game (게임) | Sample rule / actual period (표본 규칙 / 실제 기간) | Sample size / classified count (표본 수 / 분류된 수) | Top 3 praise (k of N) (칭찬 상위 3 (N개 중 k개)) | Top 3 complaints (k of N) (불만 상위 3 (N개 중 k개)) | Cross-check result (대조 결과) | Files (파일) |
|---|---|---|---|---|---|---|

### 3. Recent trends (최근 흐름)
#### 3-1. Trends (passed the judgment rule) (흐름 (판정 규칙 통과))
| Feature (특징) | Evidence games (3 or more) (근거 게임 (3개 이상)) | Metric and source (지표·출처) | Comparison points (비교 시점) | k of n at or above the median / j of m below (중앙값 이상 n개 중 k개 / 미만 m개 중 j개) | Until release (출시 때까지) | Confidence (확신도) |
|---|---|---|---|---|---|---|
#### 3-2. Cases (did not pass the rule, to watch) (사례 (규칙 미통과, 지켜볼 것))
#### 3-3. Declining trends (내려가는 흐름)

### 4. Audience (이용자층)
#### 4-1. Values at a confirmed unit (확인된 단위의 값)
| Region (지역) | Item (항목) | Value (값) | Data unit (자료 단위) | Sample and age range (표본·연령 범위) | Base period of the material (자료 기준 기간) | Source number (출처 번호) |
|---|---|---|---|---|---|---|
#### 4-2. Indirect signals (간접 신호)
| Signal (신호) | Value (값) | What it stands in for (무엇을 대신하는지) | Limits (한계) | Source number (출처 번호) |
|---|---|---|---|---|
#### 4-3. Comparison with the target player (목표 이용자와 비교): match (일치) / mismatch (어긋남) / judgment withheld (판단 보류) — evidence (근거)

### 5. By region (지역별) (profile regions only)
| Item (항목) | <region 1> | <region 2> | ... |
|---|---|---|---|
| Platform share (플랫폼 비중) | | | |
| Genre signals (장르 신호) | | | |
| Price and payment practices (가격·결제 관행) | | | |
| Age rating and release approval (연령 등급·출시 허가) | | | |
| Language and localization (언어·현지화) | | | |
| Data gaps (자료 공백) | | | |

### 6. Source IP audience and new game target (원작 이용자층과 새 게임 타깃) (only when ip_based is a source IP name)
| Item (항목) | Value (값) | Source number (출처 번호) | Confidence (확신도) |
|---|---|---|---|

### 7. Axis details (축별 상세)
(the axes-and-grades.md §6 format for each axis)

### 8. Launch conditions — proposals or reference options (출시 조건 — 제안 또는 참고 선택지)
#### <one-line title>
- Observation (관찰):
- Evidence (source numbers) (근거 (출처 번호)):
- 2~3 options and the market-side gains and losses of each (선택지 2~3개와 각각의 시장 쪽 득실):
- Decision owner (결정권자): the decision_owners.business value (if it is not the user, "reference option — what to pass to <decision owner>" (참고 선택지 — <결정권자>에게 전달할 내용))
- Metrics to watch at the next check (metric IDs) (다음 점검에서 볼 지표 (지표 ID)):

### 9. Observations on game content (passed to design as questions) (게임 내용 관련 관찰 (design 에 질문으로 넘김))
| Question inbox ID (질문함 ID) | Question ("A design judgment is needed on ~") (질문 ("~에 대해 기획 판단이 필요하다")) | Market evidence (source numbers) (시장 근거 (출처 번호)) | Evidence confidence (근거 확신도) |
|---|---|---|---|

### 10. Hardware share distribution (하드웨어 보급 분포) (only when platforms includes PC)
| Item (항목) | Values of the last 3 months (최근 3개월 값) | Average (평균) | Profile target_spec (프로필 target_spec) | Source number (출처 번호) |
|---|---|---|---|---|

### 11. Sources (출처)
| Number (번호) | Source (출처) | Kind (primary / secondary report / estimation tool / user-provided / script) (종류 (1차 / 2차 보도 / 추정 도구 / 사용자 제공 / 스크립트)) | Base period of the material (자료 기준 기간) | Publish date (발간일) | Accessed (조회일) | Sample and scope (표본·범위) | Link or file (링크 또는 파일) |
|---|---|---|---|---|---|---|---|

### 12. Search and calculation log (검색·계산 기록)
- Search queries used (the lists that web-scout returned, grouped) (사용한 검색어 (web-scout 가 돌려준 목록을 묶어서))
- Script commands run and their inputs (실행한 스크립트 명령과 입력)
```

## Change check body

```markdown
### Survey conditions (조사 조건)
| Item (항목) | Value (값) |
|---|---|
| Baseline full review (기준 전면 평가) | Path (the report that the survey conditions and the profile basis came from) |
| Comparison baseline (비교 기준) | The previous access date in market-snapshot.md |
| Narrowed scope (좁힌 범위) | all (전체) / <game ID, region, metric> (the request sentence or the question inbox ID) |
| Profile basis (프로필 기준) | The values of this run. The same cells as in the full review body (for the record. The mode decision compares with the same row of the baseline full review) |
| Profile basis change (프로필 기준 변화) | Compared with the baseline full review, none (없음) / <changed field> — full review needed (전면 평가 필요) |
| Sample rule and classification scheme (표본 규칙·분류 체계) | same as before (직전과 같음) / changed (not compared directly) (바뀜(직접 비교 안 함)) |

### 1. Metric changes (지표 변화)
(Add the two columns below to the market_calc.py snapshot --new output table. For a metric that had no previous record, the previous value is "none" (없음) and the difference is "first record" (첫 기록))
| Metric ID (지표 ID) | Game (게임) | Metric (지표) | Previous value (access date) (직전 값 (조회일)) | This value (이번 값) | Difference (차이) | Change rate (증감률) | Counts as a change (noise rule) (변화로 인정 (잡음 규칙)) | Same source (출처 같음) |
|---|---|---|---|---|---|---|---|---|

### 2. What is new (새로 생긴 것)
| Kind (new and announced games / new edition material / earnings release / regional condition change / method change) (종류 (신작·발표작 / 새 판 자료 / 실적 발표 / 지역 조건 변화 / 방법 변경)) | Content (내용) | Passed the selection rule (for new games) (선정 규칙 통과 (신작일 때)) | Source number (출처 번호) |
|---|---|---|---|

### 3. Axis grade changes (축 등급 변화) (only the axes whose evidence changed. If none, "no change" (변화 없음))
| Axis (축) | Previous grade (이전 등급) | New grade (새 등급) | Changed evidence (source numbers) (바뀐 근거 (출처 번호)) |
|---|---|---|---|

### 4. New observations on launch conditions (출시 조건 관련 새 관찰) (only when there are any, in the format of full review item 8)

### 5. Sources (출처)
### 6. Search and calculation log (검색·계산 기록)
```

In "Changes since the previous report" of the shared format, for a change check, write only "body items 1~3" (본문 1~3번 항목).
