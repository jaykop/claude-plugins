# Check ledger format (`_state/perf-ledger.md`)

This is a record that only the optimization advisor writes and reads. Its location is `<report_dir>/_state/perf-ledger.md`. Append to it every round, and do not delete earlier rows. If another advisor wants measured values, it cites the report, not this file.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## Header

Use the same header as every `_state` file (`<플러그인 폴더>/shared/state-formats.md`).

```markdown
# Optimization check ledger (최적화 점검 기록)

Next check: YYYY-MM-DD
Written by: perf / Last updated: YYYY-MM-DD / Base revision: <change number or commit>
```

- `Next check:` (`다음 점검:` in a Korean file) is the last run date plus the default period (7 days). Calculate the date with `date -d "+7 days" +%F` (GNU) or `date -v+7d +%F` (macOS). If the user set a different period, use that value.
- A run that made no report because there were no new measurement files also updates this line.

## 1. Judgment criteria

These are optimization-only values that have no field in the profile. Write only values that the user set, with source `[사용자]`. Do not make up values to fill empty ones. Write values used only in this run, such as the temporary criteria in `refactor.md` item 3, only in the report, not here.

```markdown
## Judgment criteria (판정 기준)
| Value (값) | Setting (설정) | Source (출처) |
|---|---|---|
| Measurement file naming rule (측정 파일 이름 규칙) | <rule that reads the scenario ID from the file name or the subfolder. Example: starts with `<시나리오 ID>_` / subfolder named after the scenario ID> | |
| Hitch threshold (ms) (히치 기준(ms)) | | |
| Minimum change (최소 변화폭) | <value and unit (ms or %). If it differs by metric, split the rows> | |
| Refactoring history period (days) (리팩터링 이력 기간(일)) | | |
| Ticket key prefix (티켓 키 접두사) | | |
| Issue types and labels counted as bugs (버그로 셀 이슈 종류·라벨) | | |
| Change cost criterion (변경 비용 기준) | | |
| Bug frequency criterion (버그 빈도 기준) | | |
| Paths excluded from checks (code to be retired) (점검 제외 경로(폐기 예정 코드)) | | |
| Baseline round (기준선 회차) | R-<number> | |
```

## 2. Paths by category

The periodic check uses this table to choose "the categories that the changes in that period touched", and as the scope in which it runs that category's suspect code patterns. Put in only values that the user checked.

- The code and settings paths are analyst's code search scope. Write them as globs relative to the project root.
- The version control path is passed as it is to `vcs_churn.py --path`. For git, write a folder path relative to the project root. For p4, write a depot path (a form that starts with `//` and ends with `/...`). If you give p4 any other form, the script cannot filter files by path.

```markdown
## Paths by category (부문별 경로)
| Category (부문) | Code and settings paths (glob) (코드·설정 경로 (glob)) | Version control path (버전 관리 경로) | Check date (확인일) |
|---|---|---|---|
| Game thread CPU — AI (게임 스레드 CPU — AI) | Source/<모듈>/AI/** | git: Source/<모듈>/AI/ or p4: //<depot>/<경로>/Source/<모듈>/AI/... | YYYY-MM-DD |
```

## 3. Measurement conditions

Use the fields of the measurement condition checklist (`measure.md` item 2) as they are. A condition ID is `C-` followed by a three-digit number. Rounds with the same conditions use the same condition ID.

```markdown
## Measurement conditions (측정 조건)
| Condition ID (조건 ID) | Build configuration (빌드 구성) | Frame cap and vsync (프레임 상한·수직 동기화) | Inactive-window throttling (창 비활성 제한) | Warm-up (워밍업) | Repeats (반복) | Resolution and quality (해상도·화질) | Platform and hardware (플랫폼·하드웨어) | Engine and build revision (엔진·빌드 리비전) | Temporarily changed settings (임시로 바꾼 설정) | User confirmed (사용자 확인) |
|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | | | | | | | | | | yes (예) / no (아니오) |
```

## 4. Rounds

A round ID is `R-` followed by a three-digit number.

```markdown
## Rounds (회차)
| Round (회차) | Date (날짜) | Run mode (실행 방식) | Condition ID (조건 ID) | Scenario (시나리오) | Measurement files (측정 파일) | Compared rounds (비교한 회차) | Baseline status (기준선 여부) | Report (리포트) |
|---|---|---|---|---|---|---|---|---|
| R-001 | YYYY-MM-DD | conversation (대화) | C-001 | S01 | <list of paths relative to profiling_dir> | none (first round) (없음(첫 회차)) | baseline (기준선) | perf/YYYY-MM-DD-periodic.md |
```

- The "Measurement files" column is the basis for picking out new measurement files. If `perf.profiling_dir` has a file that has never been written here, it is a new file. Do not use file system modification times.
- In "Baseline status", only a round whose measurement condition fields are all filled and that the user confirmed can be "baseline". A round from an unattended run can only go as far as "baseline candidate" (기준선 후보).
- If you change the baseline, change "Baseline round" in the judgment criteria table, and leave one line under the rounds table with the date of the change and the reason.

## 5. Items

Use the IDs of the category and item table (`categories.md`). If one item is measured with several scenarios or metrics, split the rows.

```markdown
## Items (항목)
| Item ID (항목 ID) | Scenario (시나리오) | Metric (지표) | Last check date (마지막 점검일) | Check method (점검 방법) | Baseline value (round) (기준선 값 (회차)) | Previous value (round) (직전 값 (회차)) | Judgment (판정) | Evidence mark (근거 표시) | Measurement files (측정 파일) |
|---|---|---|---|---|---|---|---|---|---|
| 게임스레드-01 | S01 | Game thread time p95 (ms) | YYYY-MM-DD | CSV profiler, csv_profile_stat.py compare | 12.4 (R-001) | 12.9 (R-003) | caution (주의) | [confirmed] ([확인]) | <path> |
```

- "Last check date" is used to choose ③ of the periodic check (the one category not looked at for the longest). Leave a category that has never been looked at as "none" (없음), and choose it first. If there are several candidates, choose the earlier one in the table order of `categories.md` item 3.
- "Judgment" is one of pass (통과) / caution (주의) / over budget (초과) / not measured (측정 못 함) / not comparable (비교 불가). Set "-" only when it is the first round and there is also no budget (`grades.md` item 6).
- Do not change the values of items not measured this time. Do not copy the previous value as if it were this round's value.

## 6. Project-specific items

```markdown
## Project-specific items (프로젝트 추가 항목)
| Item ID (항목 ID) | Category (부문) | Item (항목) | Main values to look at (주로 보는 값) | Date added (추가일) |
|---|---|---|---|---|
| 게임스레드-P01 | Game thread CPU (게임 스레드 CPU) | | | YYYY-MM-DD |
```

## 7. No-measurement log

Leave one line for each run that made no report because there were no new measurement files.

```markdown
## No-measurement log (측정 없음 기록)
| Date (날짜) | Run mode (실행 방식) | Requested measurement (요청한 측정) |
|---|---|---|
| YYYY-MM-DD | unattended (무인) | none (not requested because it is an unattended run) (없음 (무인 실행이라 요청하지 않음)) |
| YYYY-MM-DD | conversation (대화) | asked to measure S01 by measurement plan MP-002 (S01 을 측정 계획 MP-002 대로 재 달라고 요청) |
```
