# TD advisor structure audit scopes

A structure audit looks at only one scope at a time. For each scope, this file sets the collection, what to count, the verdict, and the output. Ranking and classification use fixed rules. Do not use weights or score sums. Evidence marks and grades follow choice-rules.md §1.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

Take script output only on standard output, without `--out`. If a section has exit code 3 of `module_graph.py`, "검색 실패" (search failed) in the `module_graph.py` result, or "검색 실패" or "건너뛴 파일" (skipped files) in the `tech_inventory.py` result, read the counts in that section as minimum values. Do not write them as 0 or "none".

## 1. Module dependencies

**Collection**
1. Set the excluded paths. They are external vendor plugins (the plugins in the "Project plugins confirmed as public outside products" table of radar-watchlist, and the plugins that the user said are external products) and the "Excluded paths" in the criteria table of the TD ledger. If this is the first structure audit and the table is empty, in a conversation run show the list of folders under the project's Plugins, ask which folders to exclude, and write the answer in the table. In an unattended run, exclude only what is in the table.
2. Make the module map (if `python` is not available, use `python3`).
   ```
   python "<스킬 폴더>/scripts/module_graph.py" "<프로젝트 루트>" --project-file "<project_file>" [--source-roots "<폴더1>" "<폴더2>"] [--extra-roots "<폴더1>" "<폴더2>"] [--engine-root "<engine.root>"] [--exclude "<제외 경로1>" "<제외 경로2>"] --includes [--layer "<층 이름>=<모듈1>,<모듈2>" ...] [--layer-draft]
   ```
   - Give `--layer` the layer rule (TD-L) rows of the TD ledger in order, starting from the lowest layer. If there are no rows, leave it out and give `--layer-draft`.
   - For Godot, if the result head has the caution "--unit-depth N 로 다시 돌릴 것" (run again with --unit-depth N), run it again with that value (engine-godot.md §4).
   - An edge is one dependency declaration written in Build.cs or the project file. Even for the same two modules, if a Public dependency and a dynamic load are written separately, count them as two.
   - Without `--engine-root`, the kinds of engine modules are unknown, so the runtime → editor dependency check runs only between project modules. Move the count of "종류를 몰라 검사하지 못한 의존 대상 모듈" (depended-on modules not checked because their kind is unknown) in the result to "Not checked".
   - Dependencies caught in "해석 못 한 줄" (lines not parsed) at the end of the result (including partly parsed lines) are not in the table. Read the edge count of that module as a minimum value.
   - Edges to a "헤더가 하나도 없어 include 를 셀 수 없는 모듈" (module whose includes cannot be counted because it has no headers) are left out of the include check. Write that fact under "Not checked".
3. Set the layer rules.
   - If `td.rule_docs` has a rule on layers or on the dependency direction between modules and plugins, that rule is "final". Move the rule sentence and its location to a TD-L row.
   - If not, keep the `--layer-draft` result (a draft of layers counted by depth along the dependencies) as "draft — not the target structure". Do not calculate layers by hand (rules.md §2). In a conversation run, show it. If the user fixes it and confirms it, write the status of the TD-L row as "final".
4. Call analyst (for each violating edge and each removal candidate): which file of the depending module uses what of the depended-on module (include, class and function names, reflection strings, module load calls). Get static checks and connection estimates separately. If there are more than 10 targets, look at only up to 10, in order of most includes, and write only the count for the rest.

**Verdict**

| Classification (분류) | Condition (조건) |
|---|---|
| Layer rule violation (층 규칙 위반) | The layer rules are "final", and a module in a lower layer depends on a module in an upper layer. If the layer rules are a draft, write only "differs from the draft" (초안과 다름) |
| Runtime → editor dependency (런타임 → 에디터 의존) | A runtime-kind module depends on an editor-kind module without an if condition. The link can break in a shipping build. The grade is confirmed. Write a dependency inside a condition only for reference |
| Circular dependency (순환 의존) | A group of modules that depend on each other through edges other than dynamic loads |
| Removal candidate dependency (지울 후보 의존) | A Public or Private dependency in Build.cs for which no include was found. Write "candidate" (후보) only when analyst confirmed that it is not used through reflection or module loading either. If that was not confirmed, write "unknown" |
| Undeclared include (선언 없는 include) | It includes a header of another module without a dependency declaration. It builds through a Public dependency of another module, so if that Public dependency changes, the build breaks |

**Output**: the module count and the edge count, a table for each classification, the top list of the headers with the most includes, and the update of the TD-L layer rules. Attach "team sharing needed" to proposals that move or remove a dependency.

## 2. Engine modifications

Do this only if the project is a source build and the engine folder (`engine.root`) exists. If not, end with "not applicable".

**Collection**
1. Set the modification marker rules. Use profile `radar.engine_mod_marker` (start line), `radar.engine_mod_end_marker` (end line), `radar.engine_mod_tag_re` (topic tag), and `radar.engine_mod_dirs` (folders to count).
   - The start marker must match only start lines. If the value also matches end lines (for example `X_(BEGIN|END)`), the block count inflates. In that case, in a conversation run, get confirmation to change it to a value that matches only start lines.
   - If the fields are empty, look for the start and end marker rules and the topic tag rule in `td.rule_docs` and in the guide documents (`*.md`) right under the engine folder. In a conversation run, get confirmation of the rules you found. If there is a profile, write them with the `[파일]` source. If there is no profile, use them only for this run.
   - In an unattended run, if any one of the start marker, the end marker, or the folders to count is empty, do not do this scope, and write it under "Not checked". The reason: without an end marker, you cannot tell whether the start marker also matches end lines, so the block count can inflate. In a conversation run, if the end marker is empty, find it as described in item 1 and get confirmation.
2. Extract the block list. Give `--engine-root` and `--literal` the same way as the technology trend advisor gives them when it makes the technology inventory.
   ```
   python "<플러그인 폴더>/scripts/tech_inventory.py" "<프로젝트 루트>" --project-file "<project_file>" --engine-root "<engine.root>" --mod-only --mod-list --mod-marker "<시작 표시>" [--mod-end "<끝 표시>"] [--literal] [--mod-tag-re "<태그 정규식>"] --mod-dirs "<폴더1>" "<폴더2>"
   ```
   - For the block count, use "폴더별 블록 수 (목록 기준)" (block count per folder, by list) in the result. If that line has "위의 개수와 다르다" (differs from the count above), it is the start marker problem of item 1.
   - "태그별 묶음" (groups by tag) in the result is the classification unit. Blocks without a tag are grouped by file.
   - Modification reasons are internal project information. Do not put them in search queries. The script does not put the start marker (it can contain a modifier ID) in its result. The advisor also does not copy modifier IDs into the report, the question inbox, or `_state`.
3. For each block, set the engine area: runtime (런타임; Engine/Source/Runtime) / editor (에디터; Engine/Source/Editor, Developer) / tool program (도구 프로그램; Engine/Source/Programs) / plugin (플러그인; Engine/Plugins, with the module kind of that plugin) / shader (셰이더; Engine/Shaders) / other (그 밖; write the path. Example: Engine/Source/ThirdParty, Config). If the blocks of a group span two or more areas, write the block count of each area together in the engine area column of the group (example: runtime 46, editor 6). Count the table of block counts by classification and by engine area by the path of each block.
4. Call analyst for each group (if there are many groups, up to 10, in order of block count, largest first): the engine function that was changed and its file, the places where game code or tools rely on that modification (search with the names of the functions, fields, and console variables that the modification added), and the public extension points on the same path (delegates, virtual functions, console variables, subsystems, plugin hooks, settings file values).
5. If `td.vanilla_engine_root` is empty, ask once in a conversation run. If it is set, read `Build/Build.version` in that folder and write the version in the report. If it is the same version as our engine, use it only to open the vanilla engine side of the same file and check the original code that the block changed. If it is a newer version than ours, use it only to check whether the engine developer already fixed the problem. If it is a lower version than ours, do not use it. If `td.engine_base_ref` is set and `vcs_read_commands` allows it, count from the history the number of times that file changed on the vanilla engine side.

**Verdict** — Classify each group as one of five.

| Classification (분류) | Condition (조건) |
|---|---|
| Candidate to move out of the engine (엔진 밖으로 옮길 후보) | A public extension point to do the same work on the game code, tools, or settings side exists, as [engine] path:line. Write the scope to move (file count) with it |
| Can be removed after an engine upgrade (엔진 버전을 올리면 지울 수 있음) | The block fixes a bug, and you confirmed the version in which the engine developer fixed the same bug, with a [primary] source or with the vanilla engine source of a newer version. Write the fixed version and the evidence |
| Check needed whether the engine developer fixed it (엔진 개발사가 고쳤는지 확인 필요) | The block fixes a bug, and it is not yet known whether the engine developer already fixed it. If the vanilla engine source of a newer version is local, look with it. If not, look for primary sources (hotfix notes, the official issue tracker) under the W3·W4 conditions, using only public feature names and general symptom terms (evidence.md §4·§7). Look only for up to 10 groups with the largest block counts, and write only the count for the rest. If you find it, move the group to "can be removed after an engine upgrade". If you do not find it, keep the group in this classification |
| Must be kept (유지 필요) | There is no extension point, and there is [code]·[engine] evidence that game code or tools rely on the modification |
| Unknown (모름) | There is no evidence to tell among the four above |

- For merge risk, write only countable things: blocks per file, the total line count of the group, the number of changes on the vanilla engine side (when there is history). Do not make up a risk grade and attach it.
- If the team rules have modification rules (start and end markers, writing the reason, grouping by tag, keeping modifications minimal, and so on), make a countable check for each rule. Example: the number of blocks whose pairs do not match, the number of blocks without a modification reason. The blocks that the check catches are "rule violation candidates" (규칙 위반 후보).
- Write the rules that cannot be counted separately, as "items for a person to check" (사람이 볼 항목). Example: whether one modification without a tag spans several files (the script groups untagged blocks by file). Compare the modification reasons of untagged blocks across files, raise the ones that look like the same work as candidates, and get the user's confirmation whether they are the same modification.
- If the user asked for "ways to reduce", give the block counts by classification and by engine area together.

**Output**: the update of `_state/td-engine-mods.md` (format: shared/state-formats.md), and the group table and the rule violation candidates in the report. The engine version checklist of the technology trend advisor (item 4 of upgrade-checklist.md) reads this file.

## 3. Technical debt

**Where to collect** — Merge everything into one list. If the same target comes from several places, combine it into one row and write all the evidence.
- Technology inventory: among the plugins whose location is the engine, the ones that have an Experimental or Beta marker and are "사용 중" (in use), and the plugins that are "켜짐·사용 흔적 없음" (on, no sign of use). Write separately the Experimental or Beta markers that project plugins put on themselves, and do not put them in the ranking
- Among the "Blockers when upgrading to the next version" (UP rows) of radar-watchlist, the ones whose status is "open"
- Among the groups of td-engine-mods, the ones whose classification is "candidate to move out of the engine", "can be removed after an engine upgrade", or "check needed whether the engine developer fixed it"
- The backlog and incident records in `td.record_roots`
- The count of temporary marker comments. The pattern is the value in the criteria table of the TD ledger. If there is no value, use `TODO|FIXME|HACK` and write "(default pattern)" ("(기본 패턴)"). Count only per folder
- Recurring bugs: files with 2 or more bug fixes, counted with `vcs_churn.py` and the issue tracker. The period, the prefix, and the bug kinds are the values in the criteria table of the TD ledger (SKILL.md V2)
- Rows of perf reports whose refactoring verdict is "Recommended" (with the original grade unchanged)

**Ranking rules** — A fixed order from the top.
1. There is evidence that it blocks release: our crash reports and incident records (path:line), platform requirements, Experimental features that go into the shipping build (read the .uplugin: it has a Runtime-kind module, and its target restriction is not editor only), a conflict with a feature of the next milestone (design document path:line). A crash fix in the engine release notes is rank 3, not rank 1
2. There are 2 or more bug tickets or incident records for the same place (the same as the temporary criterion of perf refactor.md)
3. It blocks the next engine version upgrade or raises its cost: UP rows, engine modification block groups
4. Others: plugins that are on with no sign of use, temporary marker comments

- Within the same rank, order by the number of affected files, largest first.
- Show the payoff scope (the number of files and modules that change) only as a column, and do not mix it into the ranking. A person decides whether to pay it off before the feature schedule.
- Whether a plugin that is "켜짐·사용 흔적 없음" (on, no sign of use) can actually be turned off cannot be known from text (it can be used only from assets). Do not recommend turning it off. Write it as an item that asks the user to check its references in the editor.

**Recommendation and decide-by date** — Attach both to each debt. The rank answers "how urgent is it". The recommendation answers "where to send it".
- Pay off (갚음): rank 1, or rank 2 when a feature of the next milestone changes the same location (design document or issue path). Write where to put it as one of current milestone (지금 마일스톤) / next milestone (다음 마일스톤) / backlog (백로그). When to do it is the PM's work, so do not assert a milestone. Write it as a candidate
- Wait for condition (조건 대기): when the trigger to fix it is tied to a specific issue or event (example: when an issue that changes that file starts). Write the condition as an issue number or as an event that can be checked
- Accept (받아들임): rank 4, and nothing is blocked even if it is not fixed. Leave a one-line reason
- Write the decide-by date by the rules in ledger-format.md. If an existing "open" debt has an empty recommendation or decide-by date, fill it in this audit

**Output**: the debt table, and the update of the debts (TD-B) in `_state/td-debt.md`. Change the status (open / waiting for condition / paying off / paid off / accepted) only when the user stated a decision. In a conversation run, put the debts whose decide-by date is today or has passed into "Decisions needed", with the recommendation. For a debt that was decided to be paid off, propose to pass an issue draft to the skill in profile `pm.next_task_entry`. If that field is empty, the user makes the issue directly. Posting happens only after user confirmation.

## 4. Coding rules

**Set the area**: one area at a time. Examples: writing abilities, the tasks of a specific plugin, replicated properties, UI binding. If the request does not have one, ask in a conversation run. In an unattended run, if there is no area, do not do this scope, and end with "no target".

**What to collect**
- The rules that are already in team documents (`td.rule_docs`) and their locations
- The patterns that repeat in the code of that area and their counts (analyst). If some places do the same work in two or more ways, get the count and examples for each way
- The mistakes in that area and their causes, from incident records (tickets, design records)
- Constraints on the engine side (path:line in the local engine source). Example: a certain function must be called only on the server

**Columns of the rule candidate table**: rule (규칙) / reason (이유; the location of the evidence in incident records or engine behavior) / examples that follow it and examples that break it (따른 예와 어긴 예; file:line and count) / whether it can be checked automatically (자동 검사 가능 여부; a search pattern, or "a person must check" (사람이 봐야 함)) / whether it is already in team documents (이미 팀 문서에 있는지) / status (상태; always "draft" (초안))

- If there is a separate format check tool that runs before submit (encoding, brackets, include order, and so on), do not handle format. Handle only design rules.
- The advisor does not put rules in team documents. A person decides whether to put them in, and a person does that work.
- For a rule with many breaking examples, attach "does not match the current code — before deciding, a decision is needed on what to do with the existing code" (지금 코드와 맞지 않음 — 정하기 전에 기존 코드를 어떻게 할지 결정 필요).

## 5. Agent verifiability

Check whether the code has a path through which an AI agent can do, without a person, the check "change it, recreate the same state, and read the result as text". This scope judges only whether the path exists. Team rules and people decide whether an agent actually runs that path. The format of performance measurement results and running measurements are perf's work.

**Set the target**: by default, `source_roots` minus the "Excluded paths" in the criteria table of the TD ledger. If the user named a system, look only at that folder. Count test folders (for example `Private/Tests`) only in axis 6.

**Collection** — Collect six axes. For each axis, leave the search pattern, the result count, and whether the search failed in the search log. The search patterns below are for Unreal C++. For Godot, use the search patterns in `<플러그인 폴더>/shared/engine-godot.md` §4 (in both conversation and unattended runs). For other engines, in a conversation run, get confirmation of search patterns with the same meaning. In an unattended run, do not do this scope, and write it under "Not checked".

1. Random number path — Do random numbers go through one path whose seed can be set?
   - Read the "Seeded random number path" (the random function or subsystem name that the team set) in the criteria table of the TD ledger. If it is empty, ask once in a conversation run and write the answer in the table. In an unattended run, if it is empty, treat it as "no set path" (정한 경로 없음).
   - Count global random calls per folder: `FMath::(Rand|Rand32|FRand|RandRange|FRandRange|RandBool|VRand|VRandCone|RandPointInBox|RandHelper)\b`, `\bstd::(rand|random_device)\b`, `(^|[^:\w])rand\(\)`. Count the calls inside the implementation files of the set path separately.
   - Count the streams that have a seed (`FRandomStream`). Get from analyst where the seed of each stream comes from: fixed value or setting value / the set path / global random / time / unknown.
   - Read `bUseFixedFrameRate`, `FixedFrameRate`, and `bSubstepping` in the project Config. If the frame interval is not fixed, the same input can give different results. Write these values only as reference facts. Do not use them for the classification.
   - Random nodes in Blueprints cannot be counted from text. Write them under "Not checked".
2. State reproduction — Is there code that returns to the same game state?
   - Save and load: `USaveGame`, `SaveGameToSlot`, `LoadGameFromSlot`, `FObjectAndNameAsStringProxyArchive`.
   - Record and replay: code that records input or commands and feeds them in again, engine replay (`UDemoNetDriver`, `UReplaySubsystem`). Get from analyst what it records and what it leaves out.
   - Cheats and console commands that move the game to a specific state (spawn, move position, set the time, set stats). From the list of axis 4, choose only the ones that set state.
3. Text output — Can the state be taken out as text that the agent reads?
   - Collect console commands and cheats (`FAutoConsoleCommand`, `FAutoConsoleCommandWithWorld`, `FAutoConsoleCommandWithWorldAndArgs`, `UFUNCTION\(\s*Exec`, `UCheatManagerExtension`), state log buffers, and log categories (`DECLARE_LOG_CATEGORY_EXTERN`).
   - Get from analyst where the output of each command and buffer goes: log or console text (`UE_LOG`, `Ar.Logf`, `FOutputDevice`) / screen only (`AddOnScreenDebugMessage`, `DrawDebug`, GameplayDebugger categories) / no output.
   - Group the results by whether each module has at least one text output path.
4. Control without recompiling — Can state or values change without building again?
   - Use the command list of axis 3 too, and split the commands that change state from the commands that only read. Add console variables (`TAutoConsoleVariable`, `FAutoConsoleVariableRef`).
   - Find settings through which an agent operates the editor remotely: `.mcp.json` in the project root, and remote control and scripting plugins that are enabled in the project file. For the list of enabled plugins, use the technology inventory (`_state/radar-inventory.md`) if it exists.
5. Separation of numeric values into data — Are balance values outside the code?
   - Count code constants per folder: `(constexpr|static\s+const)\s+(float|double|int32|int|uint8)\s+\w+\s*=\s*-?[0-9.]`, `#define\s+\w+\s+-?[0-9.]`.
   - For up to 10 files with the most constants, analyst splits each constant into a balance value (speed, damage, time, probability, distance) or a technical constant (buffer size, tolerance, bit count). Count only balance values as gaps. Write only the count for the remaining files.
   - For the ways that already moved values into data (editable `UPROPERTY`, DataAsset, DataTable, `UDeveloperSettings`, `Config=`), write only the location, as precedents.
   - Numbers written directly inside functions (magic numbers) cannot be told apart by search. Keep them as "items for a person to check".
6. Automated tests — Can logic be checked without a person playing?
   - Count the automation tests per module: `IMPLEMENT_SIMPLE_AUTOMATION_TEST`, `IMPLEMENT_COMPLEX_AUTOMATION_TEST`, `IMPLEMENT_CUSTOM_SIMPLE_AUTOMATION_TEST`, `BEGIN_DEFINE_SPEC`, classes derived from `AFunctionalTest`.
   - Find where commands that run without a screen are written: `-nullrhi`, `-unattended`, `-ExecCmds=`, `Automation RunTests` in project scripts and CI settings, and commandlets (classes derived from `UCommandlet`). Do not run the commands.

Also look in `td.rule_docs` for clauses that restrict an agent's build, test, or editor runs. If there are any, write the clause and its location in the "Basis" section of the report.

**Verdict** — Classify each axis as one value.

| Axis (축) | Complete (갖춤) | Partial (일부) | None (없음) |
|---|---|---|---|
| 1. Random number path (난수 경로) | Global random calls outside the set path are 0, and the seeds of all streams come from fixed values, setting values, or the set path | There is a set path, but there are global random calls that do not go through it, or there are streams whose seed is set by global random or by time | There is no set path, and there are global random calls |
| 2. State reproduction (상태 재현) | There is [code] evidence that save and load, or record and replay, returns to the same state | Cheats make only a similar state | None of the three exists |
| 3. Text output (텍스트 출력) | All target modules have a text output path | Only some modules have one | There is only screen output, or there is no output |
| 4. Control without recompiling (재컴파일 없는 조작) | There are commands or variables that change state, and there are also remote control settings | Only one of the two exists | Neither exists |
| 5. Separation of numeric values into data (수치의 데이터 분리) | The balance-value code constants in the sample are 0 | There are balance-value code constants in the sample, and there are also precedents of moving values into data | There is no precedent of moving values into data |
| 6. Automated tests (자동 시험) | All target modules have tests, and commands that run without a screen are written | Only some modules have tests, or there are no commands that run without a screen | There are no tests |

- If there is no evidence to decide, the value is "unknown". Write an axis whose search failed as "unknown", not "none".
- For an axis where material that cannot be counted remains, such as Blueprints, attach "Blueprints not checked" (블루프린트 확인 못 함) even if the axis is complete.

**Ranking rule**: Put the partial and none axes in axis number order. The reason: if an earlier axis has a gap, the results checked with a later axis cannot be recreated under the same conditions. Within the same axis, order by the number of files caught, largest first.

**Recommendation** — For each gap, write it in the form "if condition X, option A".
- Write the condition as work to give to an agent. Example: "if you plan to give an agent changes to AI branches and their rechecks". If there is no such plan, or if the scale is small enough that a person checking directly costs little, also write "accept".
- For the option, first use the way of a module in the same project that already has that axis. Example: if there is a set random path, move the calls that do not go through it into the path.
- In this scope, do not recommend options that change the current structure a lot, such as gathering all targets into one type or separating the simulation into a library outside the engine. If needed, open them separately as a design review question.
- For an axis where team rules block agent runs, write options only up to making the path. Do not write options that give the runs to an agent. Quote that clause.
- Write the changed scope as the number of files and call sites.

**Output**: the axis table, the gap rank table, and the items for a person to check. Do not change `_state`, except the "Seeded random number path" in the criteria table. Put high-ranked gaps in "Decisions needed". If it is decided to fix them, propose to pass them to profile `code_change_entry`.
