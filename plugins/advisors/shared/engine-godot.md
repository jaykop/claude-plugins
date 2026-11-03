# Reading guide for Godot projects

The advisors' SKILL.md and reference files are written for Unreal. If the profile `engine.kind` is `godot`, the advisor must read this file first in Step 0, and read Unreal words and steps as mapped in the tables below.

- If an Unreal-only step is not in the tables (for example, cleaning up Build.cs dependencies, or finding the patch number of a launcher build), skip it and write "not applicable to Godot — <step>" (Godot 에 해당 없음 — <단계>) in the report's "Not checked". Do not read a skipped step as "no problem".
- The rule that you must not write command, setting, or class names from memory (perf `categories.md` §2, radar `sources.md` §7) still applies. A name marked "(확인 필요)" (check needed) in this file was uncertain even when this file was written. Before you put such a name in a report, check it in the official documentation or the engine source of the target version, and write where you checked it (URL and access date, or file:line).
- The design, market, and pm advisors have no steps tied to the engine. They have nothing to remap. However, Godot content data mixes `.tres` with JSON and CSV, and the tools that check that data are often outside res:// (for example, `tools/`). When design fills `design.data_paths` and `design.existing_tools`, it must look in both places.

## 1. Set engine.kind

- When you make the profile (start.md 0-D), fill it from the "엔진 종류 (engine.kind)" line of the `profile_scan.py` output, with the source `[파일]`. If the output says "둘 다", ask the user. In an unattended run, if the field is empty, follow the engine that the script detected, and write that in "Scope" in the report header.
- The three scripts detect the engine by themselves. `profile_scan.py` looks for both engines. `tech_inventory.py` and td's `module_graph.py` run their Godot versions (`tech_inventory_godot.py`, `godot_graph.py`) if `--project-file` is `project.godot`, or if there is no `.uproject` and there is only `project.godot`. So use the commands in SKILL.md as they are. To force the engine, add `--engine godot`.
- The other scripts (`csv_profile_stat.py`, `vcs_churn.py`, `due_check.py`, `pm_calc.py`, and the design and market scripts) do not depend on the engine.

### When you write the Godot run command

Advisors do not run Godot, builds, or the editor (rules.md §7). The rules below apply when you write a Godot command in a measurement plan, a test spec, `perf.test_command`, or the check conditions of a code change that you hand off.

- **Run wrapper**: If the project has a wrapper that launches Godot (locking, capturing output, time limit) or a build script, the command must go through it. Put the profile `engine.run_wrapper` in front of the command. If the field is empty, look for it in the "Godot 실행 래퍼 후보" lines of the `profile_scan.py` output and in the run instructions of the project's canonical documents, and get it confirmed in an conversation run. In an unattended run, add "run wrapper check needed" (실행 래퍼 확인 필요) next to the command.
- **Running at the same time**: If you launch two or more Godot instances in one project, the `.godot` import cache can get corrupted. Write Godot runs in sequence. Do not write them in parallel. In the measurement conditions table ("Measurement conditions" in the ledger), add a check item for whether another worktree or session uses the same folder. Do not write a step that kills processes by name, because that also kills processes of other sessions with the same name.
- **Headless and windowed**: Add `--headless` only to runs whose results you read from the console or a file. Screenshots, mouse input and hover, frame time, and rendering time need a window. In headless mode they fail or give wrong values. Group the runs that open a window together, and tell the user first. If the window is minimized, drawing stops and the run can end with a timeout.
- **Output**: On Windows, the GUI build executable may not print to the console (확인 필요). For a run whose output you must read, use the console executable or a wrapper that captures the output to a file.
- **A project opened for the first time**: Before any other run, run import (`--import` — 확인 필요) once in headless mode.
- **Document conflicts**: If project documents give different run commands, follow the document that the project defines as canonical (for example, `AGENTS.md`, or the canonical list in the document index), and record the other one in the report as "document conflict — <file:line>" (문서 충돌 — <파일:줄>).

## 2. Word mapping (all advisors)

| Unreal | Godot | Notes |
|---|---|---|
| Project file `.uproject` | `project.godot` | Write its path in the profile `project_file` |
| Engine version file `Engine/Build/Build.version` | For a custom build, `version.py` in the engine source. Otherwise `Godot.NET.Sdk/<version>` in the C# project file (`*.csproj`). If that is also missing, the version in `config/features` of `project.godot` | `config/features` has only up to the minor version (the patch number is unknown). The script reads them in this order |
| Source build or not (`EngineAssociation`) | Not written in the project file | Do not guess `engine.source_build`. Ask the user |
| `engine.root` (engine source or install folder) | Only for a custom build: the Godot engine source folder (where `version.py` is). Leave it empty for an official release | If it is empty, check engine class, setting, and command-line names in the official documentation of the target version and in that version's tag of the public source repository |
| Game code folders `Source`, `Plugins/*/Source` | The whole folder that contains `project.godot` (res://). For C#, projects outside res:// that the game project links with ProjectReference (for example, a pure simulation library) are also game code | To leave external add-ons (`addons/<name>`) out of the checks, pass them with `--exclude`. The module map and the technology inventory read C# projects outside res:// automatically, and `profile_scan.py` reports their paths. To include them in other code searches too, list them in `source_roots` |
| Plugin `.uplugin` | `addons/<name>/plugin.cfg` (editor plugin), `*.gdextension` (GDExtension), `addons/<name>` with neither (script add-on), NuGet packages of the C# project (PackageReference) | Features built into the engine (renderer, physics engine, and so on) are settings, not plugins. Packages of test projects are not part of the game, so leave them out of the technology inventory |
| Plugin enabled or disabled in the project file | `[editor_plugins] enabled` in `project.godot` | Even if an editor plugin is disabled, the add-on's runtime scripts can still be used. GDExtensions and script add-ons have no enable/disable field |
| Plugin maturity flags (`IsExperimentalVersion`, `IsBetaVersion`) | Not in add-on files | Check experimental flags of engine features in the original class descriptions of the target version's official documentation (in the engine source, the experimental flag in `doc/classes/*.xml` — 확인 필요) |
| Modules and `*.Build.cs` dependency declarations | None | td's module map counts folders as modules and references inside files as edges (§4) |
| Config files `Config/Default*.ini` | `project.godot` | Treat per-feature-tag values (a tag after a dot, as in `key.mobile`) as the same setting. A setting that is not written uses the engine default |
| Console variables (CVar), console commands | Project settings (ProjectSettings) keys, properties and methods of engine singletons (`Engine`, `Performance`, `RenderingServer`, and so on), command-line arguments | The way to control the game at run time is debug commands that the game builds itself, or a debug console add-on |
| Blueprint assets (`.uasset`, binary, so they cannot be read) | `.tscn` and `.tres` are text, so you can read them. You cannot read `.res` and `.scn` (binary) or things that are visible only in the editor | Use "Blueprints not checked" from the Unreal documents only for binary resources. Also count signal connections in scenes (`[connection]`) and script attachments from the text |
| Tick, tick groups | `_process`, `_physics_process`, node processing priority (`process_priority`, `process_physics_priority` — 확인 필요), scene tree order | These set the execution order within the same frame |
| Network replication, remote calls | High-level multiplayer (`MultiplayerAPI`, `@rpc`, `MultiplayerSynchronizer`, `MultiplayerSpawner` — 확인 필요) | For authority checks, look for calls such as `is_multiplayer_authority()` (확인 필요) |
| Cooking and packaging | Export (`export_presets.cfg`) | The target platform is `platform` in `export_presets.cfg` |
| Measurement file folder `Saved/Profiling` | No fixed location | Ask the user for `perf.profiling_dir` |
| Automated tests (Automation Spec and so on) | GUT, gdUnit4 (GDScript and C#), custom runners, .NET test projects (xUnit, NUnit, MSTest) | `profile_scan.py` reports these separately: known frameworks (`extends GutTest`, `extends GdUnitTestSuite`, `[TestSuite]`), custom runner candidates and the number of `test_` functions in them, and .NET test projects and their number of test attributes (`[Fact]`, `[Theory]`, `[Test]`, and so on). Tests of pure C# libraries that run without the engine are often in .NET test projects |

## 3. Technology trend advisor (radar)

- **Technology inventory** (SKILL.md Step 1): The command is the same. The Godot meaning of the five statuses is in the explanation at the end of the output. "In the engine but off" (엔진에 있으나 꺼짐) is an editor plugin that is in `addons` but is not written as enabled in `[editor_plugins]`.
  - There is no "엔진 폴더를 못 찾아" step. For Godot, the full inventory comes out without an engine folder. For an official release, do not ask for `engine.root`.
  - The input fingerprint for "변경 없음" is `version.py` (when you gave the engine folder), `project.godot`, `export_presets.cfg`, `*.csproj`, `plugin.cfg`, and `*.gdextension`. Game code is not part of the fingerprint, so a change only in usage traces is reflected only after `stale_after_days` has passed.
  - "켜짐·사용 흔적 없음" can be a plugin that adds only editor tools, or a GDExtension that is used only through the class names it registers. Do not conclude that it is "not used".
- **Primary evidence from our tree** (SKILL.md D2): Instead of `.uplugin`, read `plugin.cfg` (name, version, script) and `.gdextension` (`compatibility_minimum`, library paths). For a custom build, read that module's folder in the engine source.
- **Primary sources** (sources.md §1): The list below is where to start looking. At run time, open each one to check whether it is accessible and what its address is, and record that in `source-checks.md`.
  - The official blog and release announcements (the post list and the release pages on godotengine.org)
  - Official documentation per version (the versioned docs on docs.godotengine.org). If there is a migration guide (upgrade guide between minor versions), it is the primary evidence for a version check
  - Release tags, changelogs, and the issue tracker of the public source repository godotengine/godot (treat it as the official issue tracker)
  - The proposals repository godotengine/godot-proposals holds plans. Do not use it as evidence of a release (at most announcement stage ②)
  - Treat the Asset Library and add-on repositories as material from that add-on's vendor (the vendor rule in sources.md §1)
- **Community channels** (sources.md §10): Use the channel list as it is. For qiita tags, use public technology names (for example, `Godot` — 확인 필요).
- **Engine version checklist** (upgrade-checklist.md): Keep the item numbers, and read the items as follows.
  - 2: Compare against the add-ons, GDExtensions, and settings table in the technology inventory, and against the engine classes and methods that the game code uses. Have analyst count the files that use a changed API, with search patterns over `.gd`, `.cs`, `.tscn`, and `.tres`.
  - 3: Instead of Unreal maturity flags, check how the engine features we use that the official documentation marks as experimental change in the target version.
  - 4: Only for a custom build. If we use a modified add-on ("used with engine modifications" (엔진을 고쳐서 씀)), count that add-on here too.
  - 5: Record a version where `config_version` in `project.godot` changes (a major migration such as 3 → 4) separately as "blocked candidate" (막힘 후보), and use the migration guide as the primary evidence.
  - 7: For NuGet packages, check in the packages' public material whether they match the .NET version that the target version's `Godot.NET.Sdk` requires. For a C# project, treat installing a new major .NET runtime the same as an engine version check. If the editor and tools run on the newly installed runtime while the exported game stays on the target runtime, results can differ for the same input (compare `TargetFramework` and `RollForward`). For each add-on, check support for the target version in that add-on's repository or the Asset Library. `plugin.cfg` has no field for supported versions. For GDExtensions, check `compatibility_minimum` and `compatibility_maximum` (확인 필요) together with the vendor's material.
  - For a C# project, also put the `Godot.NET.Sdk` version and the .NET version that it requires in item 2.
  - Add to 10 (how to roll back): If the project has a procedure to confirm that the results are the same after the upgrade (determinism comparison, re-capturing the reference images for visual regression), write that procedure.

## 4. TD advisor (td)

- **Module map** (SKILL.md, audit-scopes.md §1): The command is the same. If the output header says "— Godot", it is the Godot version.
  - A module is a folder. `addons/<name>` is one add-on. Elsewhere, each folder directly under the project folder is one module. For finer modules, pass `--unit-depth 2`.
  - In a project where the code is concentrated in one folder such as `scripts/` (common in Godot), the modules collapse into one. If the output header has the warning "--unit-depth N 로 다시 돌릴 것", run again with that value, and use the output of the rerun in the report. Write the `--unit-depth` value you used in the criteria table ("Criteria") of the TD ledger, so that the next check runs with the same value.
  - Edges are grouped and counted by reference kind (preload, extends, class_name use, autoload use, scene and resource references, shader include, C# using, C# type use, dynamic load, path strings). Cycle and layer checks leave out dynamic loads, path strings, and `using` of namespaces that span several modules.
  - C# type use counts only the places where a type name declared in only one module is used as a type (declarations, `new`, `typeof`, static access, generic arguments). It counts only the types of the module's own C# project and of the projects linked with ProjectReference. If several modules declare a type with the same name, it is not counted, and the output header shows that number.
  - A module in a C# project folder outside res:// has "res:// 밖" in its membership column, and its name is the folder relative to the project root (for example, `core/Match`).
  - Do not use `--engine-root` or `--includes`. If they are passed, they are ignored and recorded as "주의".
  - Read the verdict table as follows:

    | Unreal classification | Godot |
    |---|---|
    | Layer rule violation | Same |
    | Runtime → editor dependency | The output's "에디터 전용 코드에 기대는 곳". If the condition column (`Engine.is_editor_hint()`, `#if TOOLS`) is empty, the grade is "confirmed". If it has a condition, record it only for reference. Record whether that condition is safe in an exported build as something to confirm with documentation or an export test |
    | Circular dependency | Same (based on references without dynamic loads and path strings) |
    | Removal candidate dependency, Undeclared include | Not applicable, because there are no dependency declarations |

  - In the deliverable, replace "the headers with the most includes" with "files that many other modules reference" (다른 모듈이 많이 참조하는 파일). Add to the deliverable the "autoload" table (global singletons and the number of modules that call each one by name) and "가리키는 파일이 없는 res:// 경로".
- **Current structure survey** (SKILL.md): In addition to entry points and the places that write state, look for the following: signal connections (`connect` in code and `[connection]` in `.tscn`); groups (`add_to_group`, `get_nodes_in_group`, `call_group`); node path strings (`$`, `get_node`, `%` unique names), which are references tied to the scene structure; scene inheritance and instances; and shared resources, where several places modify the same `.tres`.
- **Godot default checklist**: Use it only when `td.rule_docs` has no team rule on the same topic. If there is a team rule, the team rule wins. Cite the evidence as "Godot default checklist" (Godot 일반 점검표), and do not raise a recommendation grade on this checklist alone. Keep the search patterns and the counts.
  - Scenes: references whose node path within one scene goes deeper than 5 levels (the number of `/` in `get_node` and `$` — candidates for `%` unique names); `[sub_resource]` and `[ext_resource]` entries in a `.tscn` that nothing uses; automatically generated node names (`Node2D2`, names that contain `@`); places where several scenes define the same resource separately (candidates for a shared `.tres`)
  - Execution order: a child's `_ready` runs before the body of its parent's `_ready`. Look for places where a child's `_ready` reads state that the parent or an autoload fills in its own `_ready`
  - GDScript types: places that put a value of another type into a typed array (for example, an object into `Array[Dictionary]`); nested generics (`Array[Array[`); places that use Array or Dictionary as the values of a typed Dictionary (4.4 and later — 확인 필요). A runtime conversion error can leave the array empty
  - References: places that also call a script that has `class_name` through a `preload` alias (two names for the same target)
  - Files: write `.tres` and `.tscn` without a BOM. Add the `.uid` files of new scripts to version control together with the scripts (4.4 and later). The editor can change the indentation of C# files when it saves them. Write this as a condition when you hand off a code change (`code_change_entry`)
- **Engine modifications** (audit-scopes.md §2): Do this only for a custom build where `engine.root` is the Godot engine source. The vanilla engine (`td.vanilla_engine_root`) is the official source of the same version. Read the version from `version.py` instead of `Build/Build.version`. For an official release, engine modifications are "not applicable". If we use a modified add-on, give that add-on's folder as the folder to count, and treat the same version in the add-on's original repository as vanilla.
- **Agent verifiability** (axes 1–6 in audit-scopes.md): Use the search patterns below instead of the Unreal ones. The search patterns written here need no separate confirmation in an conversation run, and you can also use them in an unattended run. If you need to search for more, get confirmation in an conversation run.
  1. Random paths
     - GDScript global random: `(?<![\w.])(randi|randf|randi_range|randf_range|randfn|randomize|rand_from_seed|seed)\s*\(`
     - C# global random: `GD\.(Randi|Randf|RandRange|Randfn|Randomize|Seed)\b`, `new\s+(System\.)?Random\(`, `Random\.Shared`
     - Seeded streams: `RandomNumberGenerator`, seeded random types that the project made (`class\s+\w*(Rng|Random)\w*\b`). If the project made such a type, it is the precedent for the "set path"
     - Count random calls for presentation (effects, background shake, and so on) separately from random calls that affect game results. Do the first split by file name and folder (`fx`, `vfx`, `ambience`, and so on). For unclear cases, analyst checks whether the value goes into state or a judgment. Do not use global random calls for presentation as evidence for a "none" verdict
     - If the project documents declare determinism ("같은 시드면 같은 결과", "미리보기 = 실행", and so on) and there are tests that check it, record them as primary evidence
     - Frame interval (as a reference fact only): `physics/common/physics_ticks_per_second` in `project.godot`, the command-line option `--fixed-fps` (확인 필요)
     - C# runtime (as a reference fact only): differences in `TargetFramework` between the game project and the tool or test projects, `RollForward`, `Deterministic`. If the runtimes differ, floating-point results can differ even for the same input
  2. State reproduction
     - GDScript: `ResourceSaver\.save`, `FileAccess\.open`, `ConfigFile`, `JSON\.(stringify|parse)`, `(var_to_str|str_to_var|var_to_bytes|bytes_to_var)\s*\(`
     - C#: `ResourceSaver\.Save`, `FileAccess\.Open`, `ConfigFile`, `Json\.(Stringify|Parse)`, `File\.(WriteAll\w*|ReadAll\w*|Open\w*|Create)\b`, `JsonSerializer\.`
     - Input recording and replay: places that use `Input\.parse_input_event`, and structures that pass state-changing input only as command objects (`interface\s+I\w*Command\b` and its recorder and player). If there is a command structure, record it as a precedent for recording and replay
     - If there are session recording files (record and replay files under `user://`) and a tool that finds the first divergence by hash comparison, record them as evidence for "complete"
  3. Text output
     - GDScript: `(?<![\w.])(print|print_debug|print_rich|printerr|prints|printt|push_warning|push_error)\s*\(`
     - C#: `GD\.(Print|PrintRich|PrintErr|PrintS|PrintT|PushWarning|PushError)\b`, `Console\.Write(Line)?\b`, `Debug\.WriteLine\b`
     - File log settings: the file log entries in `project.godot` (확인 필요)
     - Screen only: debug `Label` and `draw_` calls, debug drawing add-ons
  4. Control without recompiling
     - Debug commands and cheats that the game made (an autoload with a table of command names, debug console add-ons)
     - GDScript: `OS\.get_cmdline_(user_)?args`, `OS\.is_debug_build`. C#: `OS\.GetCmdline(User)?Args`, `OS\.IsDebugBuild`
     - GDScript needs no rebuild after you edit a script, but do not count this as a control path
     - Remote control of the editor: `.mcp.json` and enabled remote control add-ons (technology inventory)
  5. Separating numbers into data
     - GDScript constants: `^\s*const\s+\w+\s*(:\s*(int|float))?\s*:?=\s*-?[0-9.]`. C# constants: `const\s+(float|double|int)\s+\w+\s*=\s*-?[0-9.]`
     - Ways already used to move numbers out (precedents): `@export`, `\[Export\]`, data classes that inherit `Resource` together with `.tres`, `ProjectSettings\.get_setting`, `.json` and `.csv` data files
  6. Automated tests
     - Number of tests: `func\s+test_` in files with `extends\s+(GutTest|GdUnitTestSuite)`, and `\[TestCase\]` in files with `\[TestSuite\]`
     - .NET test projects (from the `profile_scan.py` output): the count of `\[\s*(Fact|Theory|Test|TestCase|TestMethod|DataTestMethod)\s*[\](]` per project. The projects that a test project references (ProjectReference) are the modules that its tests cover
     - Custom test runners: runners built by hand without a known framework are common. They come in several shapes: an `extends Node` script and scene; an `extends SceneTree` runner script (run with `-s`); a base class that tests inherit (`extends RefCounted` and so on; the inheritance can span several levels); and, for C#, code that takes command-line check arguments and ends with `GetTree().Quit(n)`.
       - Pass to analyst the "자체 러너 후보" lines (test folders or names such as `test_*.gd` and `run_all.gd`, and the number of `test_` functions in them) and the "--headless 실행" lines of the `profile_scan.py` output.
       - For each runner, analyst collects: how it finds tests (file name rules, base class); the names of the assertion functions (the ones that the base class defines; do not fix the names to patterns such as `assert_*` or `check_*`) and the number of calls; whether it reports failure through the exit code (`(get_tree\(\)\.)?quit\(\s*[^)]` — a SceneTree runner calls `quit(` directly; for C#, `GetTree\(\)\.Quit\(`); and the number of tests that run separately (in a separate process, SKIP in the default run).
       - Quality signals: whether engine errors during tests (`push_error`, script errors) count as failures (`OS\.add_logger` and `Logger` subclasses — 확인 필요). If they do not count, a function that stopped on a GDScript runtime error can look like a pass. Whether there is a load-check test that loads every script.
       - Write the result split up, for example "N with known frameworks, M custom runners (N test_ functions, N that run separately)". If there is a custom runner, do not classify the axis as "none", even if the count for known frameworks is 0
     - Places where commands that run without a screen are written: project scripts and CI settings, the arguments of the run wrapper, and code blocks in canonical documents (README, handoff documents, architecture documents). Patterns: `--headless`, `--script` and `-s`, `--quit`, `--quit-after`, `--check-only` (확인 필요), GUT and gdUnit4 command-line run scripts (확인 필요), `extends\s+(SceneTree|MainLoop)` scripts, `dotnet test`. Do not run the commands
     - Count checks that need a screen (screenshot comparison and visual regression, UI hover checks) separately. If there is a scenario list file and a reference image folder, record their locations and the number of scenes. These checks must open a window, so do not count them as tests that can run unattended

## 5. Optimization advisor (perf)

- **Measurement files** (SKILL.md Step 0, measure.md §5):
  - The editor debugger's profiler, visual profiler, and monitors are screen tools. Do not use numbers shown on screen as evidence (measure.md §5). Use only values saved to files.
  - Per-frame CSV: If the game has a measurement script (usually an autoload) that writes `Performance.get_monitor()` values as one CSV row per frame, the file is a CSV with one header row followed by frame rows, so aggregate it with `csv_profile_stat.py` as it is. Check the unit of the time monitor values (seconds or ms) in the target version's documentation (확인 필요). To compare with `--budget-ms` and `--hitch-ms`, pick columns written in ms. If there is no such script, put a "measurement script spec" (측정용 스크립트 명세: the monitor names to record, column names, units, file location) in the measurement plan, and hand it to `code_change_entry` or to the user. The advisor does not write the script (rules.md §7).
  - Put rendering CPU and GPU time in the same CSV, using the viewport render time measurement feature of `RenderingServer` (확인 필요).
  - The default form of the measurement script spec is below. Copy it into the measurement plan as it is, and remove or add columns to fit the project. All monitor names, method names, and units are 확인 필요, so when you hand off the spec, also write "check the names and units in the target version's documentation" (대상 버전 문서로 이름과 단위를 확인할 것).

    | Column name | Value | Unit |
    |---|---|---|
    | `Frame` | Frame number since recording started | count |
    | `FrameTime` | `delta` of `_process` × 1000 | ms |
    | `ProcessTime` | `Performance.TIME_PROCESS` × 1000 | ms |
    | `PhysicsTime` | `Performance.TIME_PHYSICS_PROCESS` × 1000 | ms |
    | `RenderCpuTime` | The viewport's measured render CPU time | ms |
    | `RenderGpuTime` | The viewport's measured render GPU time | ms |
    | `DrawCalls` | `Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME` | count |
    | `Objects` | `Performance.OBJECT_COUNT` | count |
    | `Nodes` | `Performance.OBJECT_NODE_COUNT` | count |
    | `StaticMemMB` | `Performance.MEMORY_STATIC` ÷ 1048576 | MB |

    - Write one header row, then one row per frame. `csv_profile_stat.py` reads it as it is (`--stats "FrameTime,ProcessTime,PhysicsTime,RenderCpuTime,RenderGpuTime"`).
    - Put the scenario ID and the repetition number in the file name (for example, `S01_r1.csv`). The "Measurement file naming rule" in the check record reads this.
    - The save location is `perf.profiling_dir`. A game usually writes to `user://` while it runs, so also write in the spec how to move the files to that folder after the measurement.
    - Do not save the measurement conditions (vertical sync, frame cap, resolution, renderer, build type) at the end of the file. A person writes them in the measurement conditions table ("Measurement conditions" in the ledger). You do not need to match the metadata row format of `csv_profile_stat.py`.
    - Remove the warm-up frames after recording, with `--skip-frames`.
  - Command-line measurement conditions: turning off vertical sync, fixed frame rate (`--fixed-fps`), FPS output (`--print-fps`), startup time measurement (`--benchmark`, `--benchmark-file`) — all 확인 필요.
  - Do GPU captures with an external graphics debugger. Measure C# GC and allocations with .NET diagnostic tools.
  - The measurement file folder line of `profile_scan.py` shows "정해진 폴더가 없다". Only in that case, ask for `perf.profiling_dir`.
  - Measurements that are not per frame: for a game with heavy simulation or turn processing, the budget is processing time (for example, ms per processed day, ms per match), not frame time. You can use such keys in `perf.budgets`. The measurement files can be the output (console or file) of the project's headless bench tool, or a text summary from a .NET profiler. If the file is a CSV with one row per round or repetition, aggregate it with `csv_profile_stat.py`. Otherwise, quote the output lines as they are.
  - Measure C# only with Release builds. Do not use Debug measurements for verdicts, and write the build configuration in the build configuration column of the measurement conditions table ("Measurement conditions" in the ledger). For a metric whose results vary with the seed, use several seeds (3 or more if the project has no standard).
  - Time metrics differ between machines. Do not compare with measurements from other machines. Compare only with the previous round and the baseline round on the same machine. Measure when no other heavy work (builds or measurements in another worktree) runs on the same machine.
- **Category table** (categories.md): Do not change the item IDs. Remap only the following.
  - Game thread CPU is the main thread. Read 게임스레드-02 "Logic that runs every frame in Blueprints" as "logic that runs every frame in GDScript". Measure it with the processing time columns of the measurement file, and search the code in the bodies of `_process` and `_physics_process`.
  - The render thread can run on the main thread, depending on the rendering thread model setting (`project.godot`, 확인 필요). Judge by the measured rendering CPU time.
  - GC: GDScript uses reference counting, so it has no GC pauses. Check whether freeing piles up in one frame. For C#, check the .NET GC.
  - Build and cook time means export time and C# build time.
  - Do not use the Unreal commands in the table (`stat`, `dumpticks`, Insights channels). As Godot replacements, use only names that you confirmed in the target version's documentation or in the engine source.
- **Checking command names** (categories.md §2): If `engine.root` is set, find the names in the engine source (command-line arguments in the engine startup code, monitor names in the documentation file of the `Performance` class — 확인 필요). If it is not set, find them in the class reference and the command-line guide page of the target version's official documentation, and record the URL and access date.
- **Tests** (tests.md): Follow the format the project already uses (item 2 of `tests.md`). The order is: the project's own runner and base classes; then GUT and gdUnit4; then xUnit and NUnit if the logic is in a C# library without the engine. Specify logic tied to scenes and resources as tests that load and run the scene (the test framework's scene runner — 확인 필요). "Team sharing needed" applies to: changes to `project.godot` (adding an autoload, enabling an add-on, the input map), adding packages to `*.csproj`, changes to `Directory.Build.props`, `nuget.config`, or `dotnet-tools.json`, and installing a test add-on.

## 6. Profile keys

| Key | Godot value |
|---|---|
| `engine.kind` | `godot` |
| `engine.name` | Godot Engine (if the project uses C#, write that it is the .NET edition) |
| `engine.version` | The version that the script read. If the patch number is unknown, confirm it with the user |
| `engine.source_build` | Ask the user |
| `engine.root` | Only for a custom build: the engine source folder |
| `engine.run_wrapper` | The leading part of the project command that launches Godot. Examples: `python tools/godot_run.py --timeout=300 --`, `<console executable path>`. If it is empty, look for it as described in §1 "When you write the Godot run command" |
| `project_file` | The path of `project.godot` |
| `source_roots` | If empty, the whole folder that contains `project.godot`. To look only at game code folders, list those folders. If `project.godot` is in a subfolder (for example, `game/`), code outside it (tool scripts and so on) is out of scope. To include that code, list all the outside folders in `source_roots` (in that case, also list the project folder) |
| `radar.engine_mod_dirs` | For a custom build, folders under the engine source (relative paths are relative to `engine.root`). For a modified add-on, `addons/<name>` (relative to the project root) |
| `perf.budgets` | A frame budget (fps, frame_ms) or a processing time budget (for example, `{PC: {day_ms: 300, match_ms: 30, memory_gb: 2}}`) |
| `perf.profiling_dir` | The folder where the measurement script or the bench tool saves its results |
| `perf.test_command` | The run command that the project defines. If there is a run wrapper or a build script, write the command including it. Examples: `<run_wrapper> --headless --path game -s res://tests/run_all.gd`, `dotnet test <test project>` |
| `perf.test_convention` | Test folder and file name rules, base classes to inherit, fixture location |
