# Optimization report body format

The whole report follows the header and the section order of `<플러그인 폴더>/shared/report-base.md`. Below is what goes in the "Body" (본문) place of that format. If a section has no content, do not leave only the heading. Write one line: "not applicable" (해당 없음).

- File name: `<report_dir>/perf/<YYYY-MM-DD>-diagnosis.md` (diagnosis) or `<report_dir>/perf/<YYYY-MM-DD>-periodic.md` (periodic check). The date is the date written, and the mode part is written only in lowercase English (common rules §12).
- In the "Scope" (범위) row of the header, write the target (symptom, system, file, question ID), the scenario ID, and the number of measurement files used. If the main conversation read them without a subagent, add "collected by the main conversation without an agent" (에이전트 없이 메인에서 수집함).
- Define an English term the first time it appears (common rules §11). Examples: p95 (the boundary value after excluding the slowest 5%), inclusive time (the time including child calls).

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## Diagnosis

```markdown
### 1. Scope and criteria (범위와 기준)
| Item (항목) | Value (값) |
|---|---|
| Target (대상) | <symptom / system path / file / question inbox ID> |
| Scenario (시나리오) | <ID and a one-line description> |
| Budget basis (예산 기준) | <value of perf.budgets / "no budget — fallback ranking rule" (예산 없음 — 대체 순위 규칙)> |
| Measured by (측정 주체) | <perf.measured_by> |
| Measurement data (측정 자료) | <list of files used / "no measurement — this run's deliverable is a measurement plan" (측정 없음 — 이번 결과물은 측정 계획)> |

### 2. Measurement conditions (측정 조건)
<the table of measure.md item 2 for each round. If there is no measurement, "not applicable" (해당 없음)>

### 3. Frame overview (bottleneck judgment) (프레임 개요 (병목 판정))
| Scenario (시나리오) | Metric (지표) | Frame (프레임) | Game thread (게임 스레드) | Render thread (렌더 스레드) | RHI thread (RHI 스레드) | GPU | Bottleneck (병목) | Budget (예산) | Hitch frames (히치 프레임) | Source (출처) |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 | p50 / p95 / max (최대) (ms) | | | | | | | | | <file, command> |

### 4. Confirmed problems [confirmed] (확인된 문제 [확인])
#### 4.1 <item ID> <title> — <Priority 1 (1순위) / Priority 2 (2순위) / Priority 3 (3순위)>
- Measured value (측정값): <value> (file: <path>, command or channel: <...>, region: <...>, repeats: <N times, spread>)
- Cause code (원인 코드): <file:line> (call path: <file:function → file:function>)
- Improvement proposal (개선안): <what and how. Look at the game code and settings side first>
- Effect ceiling (효과 상한): <inclusive time of this region>. <if it is the bottleneck, "frame time can drop by at most ..." / if not, "<thread> gains at most ... of headroom">
- Re-measurement method (재측정 방법): <same conditions, same region>
- Approval level (승인 등급): <own work scope (내 작업 범위) / team sharing needed (팀 공유 필요)>

### 5. Suspect list [suspected] (before measurement, at most 10) (의심 목록 [의심] (측정 전, 10건까지))
| Measurement order (측정 순서) | Item ID (항목 ID) | Location (file:line) (위치 (파일:줄)) | Pattern (패턴) | Call frequency and evidence (file:function path) (호출 빈도와 근거 (파일:함수 경로)) | Evidence for the number of objects that have this code (그 코드를 가진 객체 수 근거) | Measurement to confirm (확인할 측정) |
|---|---|---|---|---|---|---|

- Suspects cut (잘린 의심): <N — cut by call frequency and object count>
- Excluded search results (제외한 검색 결과): <things called only once and so on, with file:line and the reason>
- Search log (검색 기록): <scope, patterns, result count, whether it failed>

### 6. Measurement plan (측정 계획)
<the format of measure.md item 4. At most 3. If the measurements are enough, "not applicable" (해당 없음)>

### 7. Refactoring judgment (리팩터링 판단)
<the table of refactor.md item 4. If no judgment was made, "not applicable" (해당 없음)>

### 8. Test proposal (테스트 제안)
<the spec of tests.md item 3. If there is none, "not applicable" (해당 없음)>

### 9. Evidence check log (근거 확인 기록)
- Console commands, console variables, and command-line arguments used, and the location (file:line) where their existence was checked, or "check needed" (확인 필요)
- Script commands that were run, and the tables from their output that were used for the judgment
```

## Periodic check

```markdown
### 1. Round information (회차 정보)
| Item (항목) | Value (값) |
|---|---|
| This round (이번 회차) | R-<number> (<date>) |
| New measurement files (새 측정 파일) | <list of paths relative to profiling_dir, and scenario IDs. Write the files left out as "scenario unknown" (시나리오 미상) separately> |
| Measurement conditions (측정 조건) | C-<number> — <summary of the fields of measure.md item 2>, user confirmed <yes (예) / no (unattended) (아니오(무인))> |
| Compared rounds (비교한 회차) | previous R-<number> (conditions match / different fields: ...), baseline R-<number> (conditions match / different fields: ...). If it is the first round, "none (first round)" (없음(첫 회차)). If there is no baseline, "no baseline" (기준선 없음) |

### 2. Scope looked at this time and why it was chosen (이번에 본 범위와 고른 이유)
| Category or item (부문 또는 항목) | Reason chosen (고른 이유) |
|---|---|
| | ① got worse in the last round (지난 회차에서 나빠짐) / ② touched by changes in this period (이 기간 변경이 건드림) (N changes. If the read command was not allowed or the lookup failed, "not looked up" (조회 안 함)) / ③ category not looked at for the longest (가장 오래 안 본 부문) (last check date) / question inbox request (질문함 요청) (Q-number) |

### 3. Changes (변화)
| Item ID (항목 ID) | Scenario (시나리오) | Metric (지표) | Baseline (기준선) | Previous (직전) | This round (median) (이번 (중앙값)) | Spread (흩어짐) | vs. previous (직전 대비) | vs. baseline (기준선 대비) | Judgment (판정) | Candidate cause changes (원인 후보 변경) |
|---|---|---|---|---|---|---|---|---|---|---|

- Judgment: pass (통과) / caution (주의) / over budget (초과) / not measured (측정 못 함) / not comparable (비교 불가). Add "cumulative worsening" (누적 악화) to the judgment field.
- A cause candidate is only a candidate. To confirm it, propose a measurement that splits the range between the two revisions.

### 4. Details of items that got worse (나빠진 항목 상세)
#### 4.1 <item ID> <title>
- Change (변화): <formula and values, comparison command>
- Cause candidates (원인 후보): <change numbers and the paths they touched>
- Suspect code (의심 코드): <result of running that category's patterns only on the changed paths, at most 10>
- Next measurement (다음 측정): <measurement plan number>

### 5. Baseline (기준선)
<"baseline candidate: R-<number> — user confirmation needed" (기준선 후보: R-<번호> — 사용자 확인 필요) / "no baseline change" (기준선 변경 없음)>

### 6. Evidence check log (근거 확인 기록)
<the same as item 9 of the diagnosis format>
```

## What to show in the conversation

Keep the full report only in the file. In the conversation, show only what common rules §9 says: a three-line summary, the decisions needed, the report path, and 1 to 3 follow-up proposals.
