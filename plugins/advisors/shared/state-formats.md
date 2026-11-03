# Record file formats that advisors share

Of the files in `<report_dir>/_state/`, this file fixes the format of only **the files that other advisors read** and **the files that several advisors write together** (source-checks, feedback). The format of the question inbox (inbox) is in `shared/inbox-format.md`. The formats of the files that only one advisor writes and reads (design-proposals, market-snapshot, perf-ledger, pm-cadence, pm-risks, pm-plan, td-ledger, td-debt) are in the reference files of each skill. But for td-debt, the periodic check calculation of the PM advisor (`pm_calc.py cadence`) reads the `마지막 갱신` date at the top. Only the technology trend advisor writes radar-watchlist, but the TD advisor reads the status of "다음 버전으로 올릴 때 걸리는 것" (blockers when upgrading to the next version) (UP rows) and the tracking rows. Its format is in radar/reference/watchlist-format.md. If you change the columns of that table, also update evidence.md §3 and audit-scopes.md §3 of td to match.

The first part of every `_state` file is the same.

```markdown
# <파일 제목>

다음 점검: YYYY-MM-DD        (또는 "마일스톤 N일 전", "조건 — <조건 설명>". rules.md §12)
작성: <고문> / 마지막 갱신: YYYY-MM-DD / 기준 리비전: <CL 또는 커밋>
```

## radar-inventory.md — Project technology list

- Made by: radar. Read by: perf, design (as support for implementation checks), td (technologies already in use and maturity marks).
- Conditions for making it again: when the engine version file, the project file (.uproject and so on), the Config folder, or the build settings of the game code (Build.cs) changed, or when the last update is older than profile `stale_after_days`. If neither is true, do not make it again; only check the date. For Godot, the conditions are when the engine version.py (custom build), project.godot, export_presets.cfg, C# project files, plugin.cfg, or .gdextension changed.
- The Godot version also has the same tables and the same five statuses. The engine table has the "엔진: Godot" row at the top, and the plugin rows are for the addons folder (editor plugins·GDExtension·script add-ons) and for .gdextension files outside addons. The Godot meaning of the statuses is in the explanation at the end of the list.
- You can add rows to the tables below (for example, "프로젝트 모듈" (project modules), "프로젝트 파일의 대상 플랫폼" (target platforms in the project file), "입력 지문" (input fingerprint)). At the end, put `## 만든 방법과 검색 기록`, and write in it the search scope, the limits, whether a search failed, and what changed from the previous list.

```markdown
## 엔진
| 항목 | 값 | 근거 위치 |
|---|---|---|
| 엔진 버전 | 5.x.y | Engine/Build/Build.version |
| 소스 빌드 여부 | 예 / 아니오 | 프로젝트 파일의 EngineAssociation |
| 엔진 수정 블록 수 | N (폴더별) 또는 "검색 실패" | 프로필 radar.engine_mod_dirs, 검색 패턴 |

## 플러그인·기능
| ID | 이름 | 상태 | 근거 위치 |
|---|---|---|---|
| TI-001 | ... | 사용 중 | ... |

상태는 다섯 가지 중 하나: 없음 / 엔진에 있으나 꺼짐 / 켜짐·사용 흔적 없음 / 사용 중 / 엔진을 고쳐서 씀

"엔진에 있으나 꺼짐"은 프로젝트 폴더에 있지만 꺼 둔 플러그인에도 쓴다. 텍스트로 확인할 수 없는 사용(에셋에서만 쓰는 경우)이 있으므로, 목록에 없다는 것만으로 "없음"이라고 하지 않는다.

## 주요 렌더링·네트워크 설정
| 설정 | 값 | 근거 위치 |
|---|---|---|
```

## market-competitors.md — Competitor list

- Made by: market. Read by: design (looks at it first when choosing precedents).
- When design uses a game outside this list as a precedent, mark it "선례 전용" in the report.

```markdown
| ID | 게임 | 식별자 | 묶음 | 플랫폼 | 출시일 | 수익 모델 | 선정 근거 | 마지막 확인일 |
|---|---|---|---|---|---|---|---|---|
| MC-001 | ... | steam:<앱 ID> | 직접 경쟁 | ... | ... | ... | ... | ... |
```

The identifier (식별자) is the value used to look the game up again. For a Steam game, use `steam:<앱 ID>`; for other games, use the store page URL. If there is none, write "없음".

The group (묶음) is one of five: 직접 경쟁 (direct competitor) / 기준작(장르를 대표하는 성공작) (benchmark title: a successful title that represents the genre) / 부진 사례 (underperforming case) / 이용자 시간 경쟁(과금은 달라도 같은 이용자의 시간을 쓰는 게임) (competitor for player time: a game that uses the same players' time even if its monetization differs) / 선례 전용 (precedent only)

## source-checks.md — External facts and source check log

- Written by: radar, market, td (external facts found under the W2~W4 conditions of td/reference/evidence.md §4, "1차 없음(찾지 못함)" rows, and the access results of the sources opened at that time; evidence.md §8). Read by: all advisors.
- The reuse conditions are in rules.md §3.
- Write only one source in one row. If sources say different things, split them into separate rows and write "SC-xxx 와 어긋남" in the value column (값).
- For a fact that decides an announcement stage·supported platforms, copy the original sentence into the value column in quotation marks, and write with it the wording that narrows the version and the scope it applies to. If the original has no scope limit, write "범위 한정 없음".
- The source kind (출처 종류) is one of 1차 / 2차 / 3차 / 1차 없음(찾지 못함) (primary / secondary / tertiary / no primary source (not found)). "1차 없음(찾지 못함)" is a record that you looked for a primary source but there was none; write the places you looked in the value column.
- Several advisors write this file together, so fill in the "쓴 고문" (written by) column in every row. Do not delete rows that another advisor added. If you checked a row again, you can update the value, the source URL, the source kind, the check date, and the recheck date. In this case, only the "쓴 고문" column stays unchanged: keep the advisor that first added the row.
- Set the `다음 점검:` at the top to the earliest "다시 확인할 날짜" (recheck date) among all rows of the two tables. This is the same rule whichever advisor writes the file.
- Do not hard-code external facts that have dates (the latest engine version, event schedules, the maturity of features, and so on) in the instruction text. Keep such facts in this file with the check date, and check them again when the recheck date has passed.

```markdown
## 바깥 사실
| ID | 사실 | 값 | 출처 URL | 출처 종류 | 쓴 고문 | 확인일 | 다시 확인할 날짜 |
|---|---|---|---|---|---|---|---|
| SC-001 | 최신 엔진 정식 버전 | 5.x | ... | 1차 | radar | YYYY-MM-DD | YYYY-MM-DD |

## 출처 접근 가능 여부
| 출처 | 방식 | 결과 | 쓴 고문 | 확인일 | 다시 확인할 날짜 | 메모 |
|---|---|---|---|---|---|---|
| ... | 자동 조회(WebFetch) / 스크립트 / 사람이 내보내 줘야 함 | 열림 / 막힘(코드) / 부분 / 도구가 막음 | market | YYYY-MM-DD | YYYY-MM-DD | |

결과의 "도구가 막음"은 사이트가 아니라 Claude Code 의 웹 도구가 그 주소를 열지 않는 경우다("unable to fetch", "not accessible" 같은 오류). 이 경우 다른 방법으로 돌아가지 않고 "사람이 내보내 줘야 함"으로 분류한다.
```

## td-engine-mods.md — Classification of engine modification block groups

- Made by: td (the '엔진 수정' (engine modification) scope of the structure audit). Read by: radar (item 4 of the engine version checklist).
- The next check at the top is a condition sentence: `다음 점검: 조건 — 엔진 버전을 올리기로 했거나 블록 수가 바뀌었을 때`. It does not give date notices.
- Write the block count with the base revision and the date it was counted. If it differs from the block count in radar-inventory, write both values with the dates they were counted, and use the one counted later. This is because the technology list may not be made again even when the engine source changes (the engine source is not in the conditions for making the technology list again).
- Group names and modification reasons are internal project information. No advisor puts them in search queries.

```markdown
| ID | 묶음(주제 태그 또는 파일) | 엔진 영역(블록 수) | 폴더 | 블록 수 | 파일 수 | 줄 수 합 | 분류 | 근거 | 머지 위험 근거 | 기준 리비전 | 마지막 확인일 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TD-E-001 | [<태그>] | 런타임 3, 에디터 1 | <엔진 폴더 기준 경로> | 4 | 2 | 21 | 엔진 개발사가 고쳤는지 확인 필요 | <경로:줄> | 파일당 블록 2, 순정 엔진 쪽 변경 3회 | <CL> | YYYY-MM-DD |
```

The engine area (엔진 영역) is one of 런타임 / 에디터 / 도구 프로그램 / 플러그인(그 모듈 종류) / 셰이더 / 그 밖(경로) (runtime / editor / tool program / plugin (its module kind) / shader / other (path)). If a group spans two or more areas, write the block count of each area together. The classification (분류) is one of five: 엔진 밖으로 옮길 후보(게임 코드·도구·설정으로 옮길 수 있음) (candidate to move out of the engine: it can move to game code·tools·settings) / 엔진 버전을 올리면 지울 수 있음(수정 버전과 근거) (can be removed after an engine upgrade: the fixed version and the evidence) / 엔진 개발사가 고쳤는지 확인 필요 (check needed whether the engine developer fixed it) / 유지 필요 (must be kept) / 모름 (unknown). In the merge risk evidence (머지 위험 근거), write only things that can be counted (blocks per file, total line count, number of changes on the stock engine side). Do not write modifier IDs.

## feedback.md — Result feedback log

This file collects the marks that the user put on report items. In the next run, each advisor reads the rows for itself and avoids the same mistake (start.md 0-F). Advisors do not change plugin files. They only go as far as proposing a place to fix (rules.md §13).

- Writers: the user (who can edit the file directly), and every advisor in a conversation run (start.md "Receive result feedback"). In an unattended run, no advisor writes it. Readers: all advisors. Each advisor reads only the rows whose advisor column (고문) is itself.
- The `다음 점검:` at the top is a condition sentence: `다음 점검: 조건 — 반영 전 행이 있을 때 그 행의 고문 실행 시작 시`. It does not give date notices. The file name does not start with an advisor name, so it is also not a target of the session start notice. In the `작성:` field at the top, write the last writer (the advisor name or "사용자").
- Do not delete rows. Change only the status.

```markdown
# 결과 표시 기록

다음 점검: 조건 — 반영 전 행이 있을 때 그 행의 고문 실행 시작 시
작성: <마지막으로 쓴 고문 또는 "사용자"> / 마지막 갱신: YYYY-MM-DD / 기준 리비전: <CL 또는 커밋, 확인 못 했으면 "확인 못 함">

| ID | 날짜 | 고문 | 리포트 | 항목 | 표시 | 설명 | 원인 | 고친 곳 | 상태 |
|---|---|---|---|---|---|---|---|---|---|
| FB-0001 | 2026-10-15 | radar | radar/2026-10-14-single.md | 판정 표 2행 | 틀림 | 우리 코드에서 어떻게 쓸지 물었는데 커뮤니티 글부터 모았다 | 다른 고문 몫 | | 반영 전 |
```

| Column | What to write |
|---|---|
| ID | `FB-` followed by a four-digit number. The number after the last number in the table |
| 날짜 | The day of the mark, YYYY-MM-DD |
| 고문 | The advisor that wrote that report (design · radar · market · perf · pm · td). Even if the advisor wrongly took work that belongs to another advisor, this is the advisor that wrote that report |
| 리포트 | The report path relative to `report_dir` |
| 항목 | The location in the report: a heading, a table name and row, a proposal ID, and so on. If the mark is about the whole report, "전체" |
| 표시 | One of three. **틀림** (wrong): a fact or a judgment is wrong. **일반론** (generic): it is true anywhere, even for a project other than this one, so it cannot be used for a judgment. **놓침** (missed): the advisor did not look at material or a risk that it needed to look at |
| 설명 | What the user said, in one line. The advisor does not rephrase it |
| 원인 | One of five. See the "Where to fix by cause" table below. If the cause was not found, "모름" |
| 고친 곳 | Where the fix was applied: a file path (the plugin's reference·script·SKILL.md, team reference notes, a profile field) or a commit. Leave it empty while the status is "반영 전" |
| 상태 | 반영 전 (not applied yet) / 반영함 (applied) / 반영 안 함 — <이유> (not applied — <reason>) |

- When the user writes a row directly, the user can fill in only ID, 날짜, 고문, 리포트, 항목, 표시, and 설명. Read an empty 원인 as "모름" and an empty 상태 as "반영 전". Skip a row whose column count does not match, and the advisor that read it writes the ID of that row (if there is none, the start of the line) in the report's "확인 못 한 것" (not checked) section.
- A person changes the status to "반영함" or "반영 안 함". In a conversation run, if the user says "고쳤어(<곳>)" or "반영 안 해도 돼(<이유>)", the advisor writes it down as it is. The advisor does not change the status by its own judgment. If the status is "반영함", the 고친 곳 column must be filled.

### Where to fix by cause

Advisors only use this table to propose candidate places to fix. People change plugin files, and the team writes team reference notes.

| Cause | Meaning | Candidate places to fix |
|---|---|---|
| 근거를 못 읽음 (evidence not read) | Material needed for the judgment existed, but the advisor did not read it or could not read it (no path in the profile, a read command was blocked, a search failed) | The path fields of the profile (the "Required profile values" table of that advisor's SKILL.md), `vcs_read_commands`, the step in that advisor's SKILL.md that reads the material |
| 판정 기준 없음 (no judgment criterion) | The advisor read the material, but neither the instructions nor the team reference notes have a criterion that decides that case | If the criterion fits only this project, the team reference notes of that advisor (profile `<고문>.knowledge_dir`). If the criterion fits any project, the reference files of that advisor |
| 기준이 틀림 (wrong criterion) | A criterion existed and the advisor followed it, but the criterion was wrong | The place where that criterion is written (the reference file and line, the script, the item in the team reference notes) |
| 다른 고문 몫 (another advisor's work) | This advisor took work that it must not take | `shared/routing.md`, the mode selection and the "what it does not do" table of that advisor's SKILL.md |
| 모름 (unknown) | The cause is not found yet | Do not decide one. Propose to make the same question into a test question (plugin `evals/`) and run it again |

For a row that became "반영함", propose to move it into a test question that checks that the mistake does not happen again (plugin `evals/`, '시험 질문' in the README). People also do the moving.

## Values to put in the profile

Values that several advisors use go in the profile, not in `_state`. Examples: target spec (`target_spec`), target player (`market.target_player`), measurement scenes (`perf.scenarios`).

- When an advisor wants to change one of these values, it does not change it directly. It writes the value to change and the evidence in the report's "결정이 필요한 것" (decisions needed) section, and writes the value in the profile only when the user confirms it.
- Only market looks up the hardware adoption distribution. radar and perf read only the profile's `target_spec`.
