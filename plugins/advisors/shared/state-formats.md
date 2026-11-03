# Record file formats that advisors share

Of the files in `<report_dir>/_state/`, this file fixes the format of only **the files that other advisors read** and **the files that several advisors write together** (source-checks, feedback). The format of the question inbox (inbox) is in `shared/inbox-format.md`. The formats of the files that only one advisor writes and reads (design-proposals, market-snapshot, perf-ledger, pm-cadence, pm-risks, pm-plan, td-ledger, td-debt) are in the reference files of each skill. But for td-debt, the periodic check calculation of the PM advisor (`pm_calc.py cadence`) reads the `Last updated` date at the top. Only the technology trend advisor writes radar-watchlist, but the TD advisor reads the status of "Blockers when upgrading to the next version" (UP rows) and the tracking rows. Its format is in radar/reference/watchlist-format.md. If you change the columns of that table, also update evidence.md §3 and audit-scopes.md §3 of td to match.

The format blocks below write each label in English with the Korean name in parentheses. Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko` (rules.md §11). When you update an existing file, keep the language that the file already uses.

The first part of every `_state` file is the same.

```markdown
# <file title>

Next check: YYYY-MM-DD        (or "N days before milestone", "Condition — <description>". rules.md §12)
Written by: <advisor> / Last updated: YYYY-MM-DD / Base revision: <CL or commit>
```

When `report_language` is `ko`:

```markdown
# <파일 제목>

다음 점검: YYYY-MM-DD        (또는 "마일스톤 N일 전", "조건 — <조건 설명>". rules.md §12)
작성: <고문> / 마지막 갱신: YYYY-MM-DD / 기준 리비전: <CL 또는 커밋>
```

## Literal tokens that scripts read

Scripts read both forms of each token. Write the form of `report_language` exactly as below: `en` writes the English column, and `ko` writes the Korean column. Old files written in Korean keep working.

| English (`en`) | Korean (`ko`) | Where | Read by |
|---|---|---|---|
| `Next check:` | `다음 점검:` | head of every `_state` file | `scripts/due_check.py` |
| `Next check: N days before milestone` | `다음 점검: 마일스톤 N일 전` | head | `due_check.py` |
| `Next check: Condition — <description>` | `다음 점검: 조건 — <조건 설명>` | head | (advisors; scripts skip it) |
| `Written by:` | `작성:` | head | (advisors) |
| `Last updated:` | `마지막 갱신:` | head | `due_check.py`, `pm_calc.py cadence`, `tech_inventory.py` |
| `Base revision:` | `기준 리비전:` | head | (advisors) |
| `not checked yet` (value of `Last updated` before the first check) | `점검 전` | head | `pm_calc.py` (any value that is not a date counts as "no run yet") |
| `not checked` | `확인 못 함` | any value | (advisors) |
| `open` / `answered` / `dropped` | `열림` / `답함` / `폐기` | status of `inbox.md` | `due_check.py` (counts `open`) |
| `dropped — passed to <advisor> Q-xxxx` | `폐기 — <고문>으로 넘김 Q-xxxx` | status of `inbox.md` | (advisors) |
| `\| Input fingerprint \|` row | `\| 입력 지문 \|` row | `radar-inventory.md` | `tech_inventory.py` |
| columns `ID`, `Check`, `How to run`, `Period`, `Record pattern`, `Last run`, `Note` | `ID`, `점검`, `실행 방법`, `주기`, `기록 패턴`, `마지막 실행`, `메모` | `pm-cadence.md` | `pm_calc.py cadence` |
| period `N` or `N days` / `N days before milestone` / `Condition — <description>` | `N` or `N일` / `마일스톤 N일 전` / `조건 — <설명>` | `pm-cadence.md` | `pm_calc.py cadence` |
| record pattern `updated:<path>` | `갱신:<경로>` | `pm-cadence.md` | `pm_calc.py cadence` |
| columns `Risk`, `Kind`, `Impact`, `Likelihood`, `Response`, `Decide by`, `Status`, `Evidence`, `Last checked` | `위험`, `종류`, `영향`, `가능성`, `대응책`, `결정 시점`, `상태`, `근거`, `마지막 확인` | `pm-risks.md` | `pm_calc.py risks` |
| impact `critical` / `severe` / `moderate` / `minor` | `치명` / `심각` / `보통` / `가벼움` | `pm-risks.md` | `pm_calc.py risks` |
| likelihood `high` / `medium` / `low` | `높음` / `중간` / `낮음` | `pm-risks.md` | `pm_calc.py risks` |
| status `watching` / `responding` / `resolved` / `dropped` | `관찰` / `대응 중` / `해소` / `폐기` | `pm-risks.md` | `pm_calc.py risks` (`resolved` and `dropped` are closed) |
| decide-by cell that names a milestone contains `milestone` | contains `마일스톤` | `pm-risks.md` | `pm_calc.py risks` |
| columns `Kind`, `Location`, `Evidence numbers and command`, `Rank`, `Payoff scope`, `Recommendation`, `Decide by`, `Status`, `Last check date` | `종류`, `위치`, `근거 수치와 명령`, `순위`, `갚는 범위`, `권고`, `결정 시점`, `상태`, `마지막 확인일` | `td-debt.md` | `pm_calc.py debts` |
| status `open` / `paying off` / `paid off` / `accepted` / `waiting for condition` | `열림` / `갚는 중` / `갚음` / `받아들임` / `조건 대기` | `td-debt.md` | `pm_calc.py debts` |
| decide-by `Condition — <condition>` | `조건 — <조건>` | `td-debt.md` | `pm_calc.py debts` |
| columns `Metric ID`, `Game`, `Metric`, `Value`, `Source`, `Base period`, `Accessed`, `Note` | `지표 ID`, `게임`, `지표`, `값`, `출처`, `기준 기간`, `조회일`, `메모` | `market-snapshot.md` | `market_calc.py snapshot` |
| `capacity: Nh` | `용량: N시간` | PM capacity notes | `pm_calc.py` |

- English values are read without regard to upper and lower case. A column name written with both names, such as `Period (주기)`, is also read, but do not write it that way.
- The scripts print their own output in Korean. `tech_inventory.py` writes `radar-inventory.md` itself, so that file is in Korean in every `report_language`.

## radar-inventory.md — Project technology list

- Made by: radar. Read by: perf, design (as support for implementation checks), td (technologies already in use and maturity marks).
- `tech_inventory.py` writes this file in Korean. The block below shows its Korean labels, and the English names are in the list after the block.
- Conditions for making it again: when the engine version file, the project file (.uproject and so on), the Config folder, or the build settings of the game code (Build.cs) changed, or when the last update is older than profile `stale_after_days`. If neither is true, do not make it again; only check the date. For Godot, the conditions are when the engine version.py (custom build), project.godot, export_presets.cfg, C# project files, plugin.cfg, or .gdextension changed.
- The Godot version also has the same tables and the same five statuses. The engine table has the "엔진: Godot" (engine: Godot) row at the top, and the plugin rows are for the addons folder (editor plugins·GDExtension·script add-ons) and for .gdextension files outside addons. The Godot meaning of the statuses is in the explanation at the end of the list.
- You can add rows to the tables below (for example, "프로젝트 모듈" (project modules), "프로젝트 파일의 대상 플랫폼" (target platforms in the project file), "입력 지문" (input fingerprint)). At the end, put `## 만든 방법과 검색 기록` (how it was made and search log), and write in it the search scope, the limits, whether a search failed, and what changed from the previous list.

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

English names of the labels above: sections 엔진 (Engine), 플러그인·기능 (Plugins and features), 주요 렌더링·네트워크 설정 (Main rendering and network settings). Columns 항목 (Item), 값 (Value), 근거 위치 (Evidence location), 이름 (Name), 상태 (Status), 설정 (Setting). Rows 엔진 버전 (engine version), 소스 빌드 여부 (source build or not; 예 = yes, 아니오 = no), 엔진 수정 블록 수 (engine modification block count; "검색 실패" = search failed).
The status is one of five: none (없음) / in the engine but off (엔진에 있으나 꺼짐) / on, no sign of use (켜짐·사용 흔적 없음) / in use (사용 중) / used with engine modifications (엔진을 고쳐서 씀). "In the engine but off" is also used for a plugin that is in the project folder but turned off. Some uses cannot be checked in text (use only in assets), so do not say "none" only because a technology is not in the list.

## market-competitors.md — Competitor list

- Made by: market. Read by: design (looks at it first when choosing precedents).
- When design uses a game outside this list as a precedent, mark it "precedent only" (선례 전용) in the report.

```markdown
| ID | Game (게임) | Identifier (식별자) | Group (묶음) | Platform (플랫폼) | Release date (출시일) | Revenue model (수익 모델) | Selection evidence (선정 근거) | Last check date (마지막 확인일) |
|---|---|---|---|---|---|---|---|---|
| MC-001 | ... | steam:<app ID> | direct competitor (직접 경쟁) | ... | ... | ... | ... | ... |
```

The identifier is the value used to look the game up again. For a Steam game, use `steam:<app ID>` (`steam:<앱 ID>`); for other games, use the store page URL. If there is none, write "none" (없음).

The group is one of five: direct competitor (직접 경쟁) / benchmark title: a successful title that represents the genre (기준작(장르를 대표하는 성공작)) / underperforming case (부진 사례) / competitor for player time: a game that uses the same players' time even if its monetization differs (이용자 시간 경쟁(과금은 달라도 같은 이용자의 시간을 쓰는 게임)) / precedent only (선례 전용)

## source-checks.md — External facts and source check log

- Written by: radar, market, td (external facts found under the W2~W4 conditions of td/reference/evidence.md §4, "no primary source (not found)" rows, and the access results of the sources opened at that time; evidence.md §8). Read by: all advisors.
- The reuse conditions are in rules.md §3.
- Write only one source in one row. If sources say different things, split them into separate rows and write "disagrees with SC-xxx" (SC-xxx 와 어긋남) in the value column.
- For a fact that decides an announcement stage·supported platforms, copy the original sentence into the value column in quotation marks, and write with it the wording that narrows the version and the scope it applies to. If the original has no scope limit, write "no scope limit" (범위 한정 없음).
- The source kind is one of primary (1차) / secondary (2차) / tertiary (3차) / no primary source (not found) (1차 없음(찾지 못함)). "No primary source (not found)" is a record that you looked for a primary source but there was none; write the places you looked in the value column.
- Several advisors write this file together, so fill in the "written by" column in every row. Do not delete rows that another advisor added. If you checked a row again, you can update the value, the source URL, the source kind, the check date, and the recheck date. In this case, only the "written by" column stays unchanged: keep the advisor that first added the row.
- Set the `Next check:` at the top to the earliest "recheck date" among all rows of the two tables. This is the same rule whichever advisor writes the file.
- Do not hard-code external facts that have dates (the latest engine version, event schedules, the maturity of features, and so on) in the instruction text. Keep such facts in this file with the check date, and check them again when the recheck date has passed.

```markdown
## External facts (바깥 사실)
| ID | Fact (사실) | Value (값) | Source URL (출처 URL) | Source kind (출처 종류) | Written by (쓴 고문) | Check date (확인일) | Recheck date (다시 확인할 날짜) |
|---|---|---|---|---|---|---|---|
| SC-001 | latest official engine version (최신 엔진 정식 버전) | 5.x | ... | primary (1차) | radar | YYYY-MM-DD | YYYY-MM-DD |

## Source access (출처 접근 가능 여부)
| Source (출처) | Method (방식) | Result (결과) | Written by (쓴 고문) | Check date (확인일) | Recheck date (다시 확인할 날짜) | Note (메모) |
|---|---|---|---|---|---|---|
| ... | automatic lookup (WebFetch) (자동 조회(WebFetch)) / script (스크립트) / a person must export it (사람이 내보내 줘야 함) | open (열림) / blocked (code) (막힘(코드)) / partial (부분) / blocked by the tool (도구가 막음) | market | YYYY-MM-DD | YYYY-MM-DD | |
```

The result "blocked by the tool" is the case where Claude Code's web tool, not the site, does not open that address (errors such as "unable to fetch", "not accessible"). In this case, do not go around it with another method; classify it as "a person must export it".

## td-engine-mods.md — Classification of engine modification block groups

- Made by: td (the "engine modifications" (엔진 수정) scope of the structure audit). Read by: radar (item 4 of the engine version checklist).
- The next check at the top is a condition sentence: `Next check: Condition — when it is decided to upgrade the engine version or the block count changed` (`다음 점검: 조건 — 엔진 버전을 올리기로 했거나 블록 수가 바뀌었을 때`). It does not give date notices.
- Write the block count with the base revision and the date it was counted. If it differs from the block count in radar-inventory, write both values with the dates they were counted, and use the one counted later. This is because the technology list may not be made again even when the engine source changes (the engine source is not in the conditions for making the technology list again).
- Group names and modification reasons are internal project information. No advisor puts them in search queries.

```markdown
| ID | Group (topic tag or file) (묶음(주제 태그 또는 파일)) | Engine area (block count) (엔진 영역(블록 수)) | Folder (폴더) | Block count (블록 수) | File count (파일 수) | Total line count (줄 수 합) | Classification (분류) | Evidence (근거) | Merge risk evidence (머지 위험 근거) | Base revision (기준 리비전) | Last check date (마지막 확인일) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TD-E-001 | [<tag>] | runtime 3, editor 1 | <path from the engine folder> | 4 | 2 | 21 | check needed whether the engine developer fixed it | <path:line> | 2 blocks per file, 3 changes on the stock engine side | <CL> | YYYY-MM-DD |
```

The engine area is one of runtime (런타임) / editor (에디터) / tool program (도구 프로그램) / plugin (its module kind) (플러그인(그 모듈 종류)) / shader (셰이더) / other (path) (그 밖(경로)). If a group spans two or more areas, write the block count of each area together. The classification is one of five: candidate to move out of the engine: it can move to game code·tools·settings (엔진 밖으로 옮길 후보(게임 코드·도구·설정으로 옮길 수 있음)) / can be removed after an engine upgrade: the fixed version and the evidence (엔진 버전을 올리면 지울 수 있음(수정 버전과 근거)) / check needed whether the engine developer fixed it (엔진 개발사가 고쳤는지 확인 필요) / must be kept (유지 필요) / unknown (모름). In the merge risk evidence, write only things that can be counted (blocks per file, total line count, number of changes on the stock engine side). Do not write modifier IDs.

## feedback.md — Result feedback log

This file collects the marks that the user put on report items. In the next run, each advisor reads the rows for itself and avoids the same mistake (start.md 0-F). Advisors do not change plugin files. They only go as far as proposing a place to fix (rules.md §13).

- Writers: the user (who can edit the file directly), and every advisor in a conversation run (start.md "Receive result feedback"). In an unattended run, no advisor writes it. Readers: all advisors. Each advisor reads only the rows whose advisor column is itself.
- The `Next check:` at the top is a condition sentence: `Next check: Condition — at the start of a run of that row's advisor, when there are rows not applied yet` (`다음 점검: 조건 — 반영 전 행이 있을 때 그 행의 고문 실행 시작 시`). It does not give date notices. The file name does not start with an advisor name, so it is also not a target of the session start notice. In the `Written by:` field at the top, write the last writer (the advisor name or "user" (사용자)).
- Do not delete rows. Change only the status.

```markdown
# Result feedback log (결과 표시 기록)

Next check: Condition — at the start of a run of that row's advisor, when there are rows not applied yet
Written by: <the advisor that wrote last, or "user"> / Last updated: YYYY-MM-DD / Base revision: <CL or commit; if not checked, "not checked">

| ID | Date (날짜) | Advisor (고문) | Report (리포트) | Item (항목) | Mark (표시) | Description (설명) | Cause (원인) | Fixed in (고친 곳) | Status (상태) |
|---|---|---|---|---|---|---|---|---|---|
| FB-0001 | 2026-10-15 | radar | radar/2026-10-14-single.md | verdict table row 2 (판정 표 2행) | wrong (틀림) | 우리 코드에서 어떻게 쓸지 물었는데 커뮤니티 글부터 모았다 | another advisor's work (다른 고문 몫) | | not applied yet (반영 전) |
```

| Column | What to write |
|---|---|
| ID | `FB-` followed by a four-digit number. The number after the last number in the table |
| Date (날짜) | The day of the mark, YYYY-MM-DD |
| Advisor (고문) | The advisor that wrote that report (design · radar · market · perf · pm · td). Even if the advisor wrongly took work that belongs to another advisor, this is the advisor that wrote that report |
| Report (리포트) | The report path relative to `report_dir` |
| Item (항목) | The location in the report: a heading, a table name and row, a proposal ID, and so on. If the mark is about the whole report, "whole report" (전체) |
| Mark (표시) | One of three. **wrong** (틀림): a fact or a judgment is wrong. **generic** (일반론): it is true anywhere, even for a project other than this one, so it cannot be used for a judgment. **missed** (놓침): the advisor did not look at material or a risk that it needed to look at |
| Description (설명) | What the user said, in one line. The advisor does not rephrase it |
| Cause (원인) | One of five. See the "Where to fix by cause" table below. If the cause was not found, "unknown" (모름) |
| Fixed in (고친 곳) | Where the fix was applied: a file path (the plugin's reference·script·SKILL.md, team reference notes, a profile field) or a commit. Leave it empty while the status is "not applied yet" |
| Status (상태) | not applied yet (반영 전) / applied (반영함) / not applied — <reason> (반영 안 함 — <이유>) |

- When the user writes a row directly, the user can fill in only ID, Date, Advisor, Report, Item, Mark, and Description. Read an empty Cause as "unknown" and an empty Status as "not applied yet". Skip a row whose column count does not match, and the advisor that read it writes the ID of that row (if there is none, the start of the line) in the report's "Not checked" section.
- A person changes the status to "applied" or "not applied". In a conversation run, if the user says "고쳤어(<곳>)" or "반영 안 해도 돼(<이유>)", the advisor writes it down as it is. The advisor does not change the status by its own judgment. If the status is "applied", the Fixed in column must be filled.

### Where to fix by cause

Advisors only use this table to propose candidate places to fix. People change plugin files, and the team writes team reference notes.

| Cause | Meaning | Candidate places to fix |
|---|---|---|
| evidence not read (근거를 못 읽음) | Material needed for the judgment existed, but the advisor did not read it or could not read it (no path in the profile, a read command was blocked, a search failed) | The path fields of the profile (the "Required profile values" table of that advisor's SKILL.md), `vcs_read_commands`, the step in that advisor's SKILL.md that reads the material |
| no judgment criterion (판정 기준 없음) | The advisor read the material, but neither the instructions nor the team reference notes have a criterion that decides that case | If the criterion fits only this project, the team reference notes of that advisor (profile `<고문>.knowledge_dir`). If the criterion fits any project, the reference files of that advisor |
| wrong criterion (기준이 틀림) | A criterion existed and the advisor followed it, but the criterion was wrong | The place where that criterion is written (the reference file and line, the script, the item in the team reference notes) |
| another advisor's work (다른 고문 몫) | This advisor took work that it must not take | `shared/routing.md`, the mode selection and the "what it does not do" table of that advisor's SKILL.md |
| unknown (모름) | The cause is not found yet | Do not decide one. Propose to make the same question into a test question (plugin `evals/`) and run it again |

For a row that became "applied", propose to move it into a test question that checks that the mistake does not happen again (plugin `evals/`, "시험 질문" (test questions) in the README). People also do the moving.

## Values to put in the profile

Values that several advisors use go in the profile, not in `_state`. Examples: target spec (`target_spec`), target player (`market.target_player`), measurement scenes (`perf.scenarios`).

- When an advisor wants to change one of these values, it does not change it directly. It writes the value to change and the evidence in the report's "Decisions needed" section, and writes the value in the profile only when the user confirms it.
- Only market looks up the hardware adoption distribution. radar and perf read only the profile's `target_spec`.
