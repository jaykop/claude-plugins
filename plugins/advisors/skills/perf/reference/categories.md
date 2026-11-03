# Category and item table

This file sets the names and IDs that the optimization advisor uses for its check targets. Diagnosis reports, periodic check reports, and the check ledger (`_state/perf-ledger.md`) all use these IDs.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. ID rules

- Do not change item IDs. Even if you change an item name, keep the ID as it is.
- When you add an item to this file, use the number after the last number of that category. Do not reuse deleted numbers.
- Do not put items that exist in only one project (such as a system unique to that game) in this file. Put them in the "Project-specific items" table of the check ledger, and add `P` before the number (`게임스레드-P01`) so that they do not overlap with the numbers of this file.
- If you need a category that is not in the table, such as audio, add it as a project-specific item together with the category name.
- When you find the cause of a hitch (a moment when one or two frames suddenly take long, a stutter), also write it in the item of the cause category. Example: write a hitch caused by garbage collection in both `히치-01` and `GC-01`.

## 2. Before you use a command name

The console commands, console variables (engine setting values that can be changed while running), command-line arguments, and trace channel names in the table below are widely used names written down for reference. Names and behavior change with each engine version.

1. Before you put a name in a measurement plan or a report, search for the name in the target engine source (profile `engine.root`; for a launcher install, its install folder) to check that it exists, and write the location found (file:line) in the "Evidence check log" of the report.
   - Narrow the search scope to `*.cpp` and `*.h` in `Engine/Source`, and ignore case. Searching the whole engine folder at once easily times out. If there are many names, hand analyst the name list and the search scope, and receive a location table.
   - Console commands and console variables: search for the name string as it is.
   - `stat <이름>`: if it is a stat group, search for `STATGROUP_<이름>`. For subcommands that are not groups, such as `stat unit` and `stat dumphitches`, search for the subcommand string (for example, `dumphitches`).
   - Trace channel groups (presets): read the `[Trace.ChannelPresets]` part of `Engine/Config/BaseEngine.ini`.
   - If the search ended with a timeout or an error, it is "search failed" (검색 실패). It does not mean that the name does not exist. In this case too, add "check needed" (확인 필요).
2. If you cannot see the engine source, add "check needed" next to the name. When you request a measurement, tell the user that fact too.
3. Names marked "(check needed)" in the table were not certain even when this file was written. Check them before the other names.
4. Do not make up names that are not in the table from memory. If you need one, find it in the engine source.
5. Do not write from memory what an engine feature supports or what its default value is either. Check it with the target engine's source and `Engine/Config/Base*.ini`. If outside material such as release notes is needed, ask radar through the question inbox. Do not write such constraints in this file either.

## 3. Categories and items

| Category (부문) | Item ID (항목 ID) | Item (항목) | Main values to look at (주로 보는 값) |
|---|---|---|---|
| Game thread CPU (게임 스레드 CPU) | 게임스레드-01 | Number and cost of ticks (update functions called every frame): enabled ticks, tick interval, ticks with an empty body | Inclusive time of the tick region (the time including the time of the child functions that the function called), number of registered ticks |
| | 게임스레드-02 | Logic that runs every frame in Blueprints | Inclusive time of the Blueprint function region |
| | 게임스레드-03 | AI: perception, pathfinding, behavior tree and state tree updates | AI region time, number of pathfinding requests |
| | 게임스레드-04 | Animation update: anim graph evaluation, updates of off-screen characters, anim logic left on the game thread | Anim region time, number of characters updated |
| | 게임스레드-05 | Physics: number of collision queries (traces, sweeps, overlap tests), number of simulated bodies, overlap events | Physics region time, queries per frame |
| | 게임스레드-06 | Frequency of actor and object creation and destruction | Creations and destructions per frame, time of that region |
| | 게임스레드-07 | UI update: property bindings evaluated every frame, number of widgets | UI region time |
| Render thread (렌더 스레드) | 렌더스레드-01 | Draw calls and number of mesh batches | Number of draw calls, render thread time |
| | 렌더스레드-02 | Cost of visibility determination (choosing the visible objects) | Visibility region time, number of objects tested |
| | 렌더스레드-03 | Number of shadow-casting lights and objects | Shadow setup region time |
| | 렌더스레드-04 | Code that rebuilds the render state every frame | Time and call count of that region |
| GPU | GPU-01 | Global illumination and reflections | Time per GPU pass |
| | GPU-02 | Shadows | Time per GPU pass |
| | GPU-03 | Mesh throughput: virtualized geometry meshes and other high-poly meshes | Geometry pass time, triangle count |
| | GPU-04 | Translucency, post-processing, particles | Time per GPU pass |
| | GPU-05 | Resolution, upscaling, quality level settings | GPU frame time per quality level |
| Memory (메모리) | 메모리-01 | Texture streaming pool | Pool usage, whether the pool is exceeded |
| | 메모리-02 | Assets pulled in by hard references (references that are loaded together when the referencing asset is loaded) | Resident memory per map and per character |
| | 메모리-03 | Growth trend during long play (suspected leak) | Memory difference between the start and the end of the same scenario |
| | 메모리-04 | Peak compared with the platform limit | Peak usage |
| Loading and streaming (로딩·스트리밍) | 로딩-01 | Map loading time | Time from the start of loading until the player can control |
| | 로딩-02 | Streaming waits during play: world partition cells, async load waits | Number and length of waits |
| | 로딩-03 | Synchronous loads during the game (loads that stop the game thread until everything is read) | Number and time of synchronous loads |
| Network and replication (네트워크·복제) | 네트워크-01 | Server replication processing time | Replication region time within the server frame |
| | 네트워크-02 | Send and receive bandwidth per connection | Bytes per second |
| | 네트워크-03 | Frequency of remote calls (RPC) and use of reliable calls | Calls per second |
| | 네트워크-04 | Movement replication and number of position corrections | Corrections per second |
| Garbage collection and object count (가비지 컬렉션·오브젝트 수) | GC-01 | Pause time and frequency of garbage collection (the process that collects and deletes unused engine objects) | Time per run, runs per minute |
| | GC-02 | Trend of the number of engine objects (UObject) remaining in memory | Count at the start and the end of the scenario |
| | GC-03 | Top object counts by class | Count per class |
| Hitches (momentary stutters) (히치(순간 끊김)) | 히치-01 | Number of hitches and maximum length | Number of frames over the hitch threshold, maximum frame time |
| | 히치-02 | Compilation of shaders and pipeline state objects (PSO: a bundle of drawing settings that is created at first use and causes a stutter) | Number of hitches at first appearance |
| | 히치-03 | Hitches whose cause is not known yet | List of hitch frames |
| Build and cook time (빌드·쿡 시간) | 빌드-01 | Full build time | Build time |
| | 빌드-02 | Incremental build time and number of recompiled files after changing one shared header | Time, number of files |
| | 빌드-03 | Cook (the process that converts editor assets into platform data) time and number of shaders | Time, number of shaders |
| | 빌드-04 | Package size | Bytes |
| Code health (코드 건강도) | 코드-01 | Files where changes concentrate | Number of changes in the period |
| | 코드-02 | Groups of files that always change together (coupling) | Number of times changed together |
| | 코드-03 | Files where bug fixes recur | Number of changes linked to bug tickets |
| | 코드-04 | Pure calculation logic without tests | Whether tests exist (file:line) |

The [confirmed] items of the code health category are not frame measurements. They are numbers counted directly from the version control history and the issue tracker (`refactor.md` in the same reference folder).

## 4. Measurement methods and suspect code patterns by category

A "quick check" is a command that shows values directly on screen or in a log. Numbers shown on screen are averages or instant values, so do not use them as evidence in a report. Use as evidence only values left in a log or a file (`measure.md` item 5).
Run the "suspect code patterns" only after measurement has decided that the category is the bottleneck. If there is no measurement, run them only inside the system path that the user named.

### Game thread CPU

- Quick check: `stat unit`, `stat game`, `dumpticks` (writes the list of registered ticks to the log), `StartFPSChart` / `StopFPSChart` (writes frame statistics of a section to a file)
- Quick check of sub-items: AI `stat ai`, animation `stat anim`, physics `stat physics`, collision queries `stat collision`
- Deep measurement: the cpu channel of an Insights trace (Unreal Insights: the engine's tool for recording and analyzing profiles). To see Blueprint function names too, the command-line argument `-statnamedevents`. `CsvProfile Start` / `CsvProfile Stop` of the CSV profiler (a feature that writes one row of statistics per frame to a CSV)
- Suspect code patterns:
  - Full searches inside tick functions: calling `GetAllActorsOfClass`, `TActorIterator`, or component searches (`GetComponents`, `FindComponentByClass`) every frame
  - Creation and destruction inside tick functions: `SpawnActor`, `NewObject`, `Destroy`
  - Logging and string building inside tick functions: `UE_LOG`, `FString::Printf`
  - Tick overrides whose body is empty or only calls the parent function; classes with many ticks enabled with a tick interval of 0
  - Collision queries inside loops (`LineTrace*`, `Sweep*`, `Overlap*`)
  - Heavy searches inside the update function of an anim instance; settings that always update even off screen (the `VisibilityBasedAnimTickOption` value)
  - Classes with many components that have overlap events enabled (`bGenerateOverlapEvents`)
  - UI: property bindings evaluated every frame, text updates inside widget ticks
- Blueprints are asset files (.uasset) in a binary format, so do not judge them by text search. Look at them only through `dumpticks` logs, `-statnamedevents` traces, and checks inside the editor. If you could not look, it is "not checked" (확인 못 함).

### Render thread

- Quick check: `stat scenerendering`, `stat rhi`, `stat initviews`
- Deep measurement: the cpu, gpu, and frame channels of an Insights trace (the rendering preset if there is one)
- Suspect code patterns:
  - Placing many copies of the same mesh as individual components (not using instanced components)
  - Calls that rebuild the render state every frame (`MarkRenderStateDirty`, component re-registration)
  - Creating dynamic material instances every frame (calling `CreateDynamicMaterialInstance` in a tick)
  - Classes with many small lights that have dynamic shadows enabled

### GPU

- Quick check: `stat gpu`, `ProfileGPU` (writes the time per GPU pass of one frame to the log)
- Deep measurement: the gpu channel of an Insights trace. GPU statistics of the CSV profiler can have a separate argument that enables them (for example, `-csvGpuStats`). GPU analysis tools of the platform makers
- Code is weak evidence here. Read the settings files (lighting, shadow, and quality level values in `Config/Default*.ini`) and the "주요 렌더링·네트워크 설정" (main rendering and network settings; the script writes this table name in Korean) table of `_state/radar-inventory.md`, and judge by measurement.

### Memory

- Quick check: `memreport -full` (writes a memory report to a file), `obj list` (object count per class), `stat llm` (in a build with LLM enabled)
- Deep measurement: Memory Insights (the memory channel of a trace), LLM (Low-Level Memory Tracker: a feature that counts memory split by tag) with the command-line argument `-llm`, and `-LLMCSV` to write it as CSV
- Suspect code patterns:
  - A chain of members that hard-reference large assets (class references, object pointers). Check whether they can be soft references (`TSoftObjectPtr`, `TSoftClassPtr`)
  - Cache containers that are never emptied, pools that never shrink
  - `AddToRoot` without `RemoveFromRoot`

### Loading and streaming

- Quick check: `stat streaming`, `stat levels`
- Deep measurement: the loading-related channels of an Insights trace (the loading preset if there is one)
- Suspect code patterns:
  - Synchronous loads during the game: `LoadObject`, `StaticLoadObject`, `LoadSynchronous`, `LoadClass`
  - Calls that stop and wait for async loads (`FlushAsyncLoading`)
  - A structure that loads everything at once at level transitions

### Network and replication

- Quick check: `stat net`
- Deep measurement: Network Insights (the net channel of a trace; the recording detail level is `NetTrace.SetTraceVerbosity`), traces recorded separately in the server process
- Suspect code patterns:
  - Remote calls made inside a tick; reliable remote calls made every frame
  - Many actors that leave the replication frequency (`NetUpdateFrequency`) at the default value
  - Replicating a large array as a whole
  - Not using dormancy (a setting that stops replication when nothing will change)
  - Properties missing from the push model (a method that marks a property for replication only at the moment its value changes) when the project uses it

### Garbage collection and object count

- Quick check: `obj list`, the garbage collection time lines in the log (log category name: check needed)
- Deep measurement: the garbage collection regions in an Insights trace, the related statistics of the CSV profiler (check the names in the header row of the result file)
- Suspect code patterns:
  - Creating many short-lived engine objects every frame (calling `NewObject` in a tick)
  - Accumulating `AddToRoot`

### Hitches (momentary stutters)

- Quick check: `stat dumphitches` (writes hitch frames to the log), the hitch threshold console variable `t.HitchFrameTimeThreshold`
- Deep measurement: choose the hitch frames from the frame time column of the CSV profiler, and then look at that frame range in the Insights trace of the same round. Point to the cause of a hitch with the frames where the hitch happened, not with the average
- Suspect code patterns: settings that build shaders and pipeline state objects in advance (setting name: check needed), synchronous loads during the game, garbage collection

### Build and cook time

- Quick check: the total time in the build log, the statistics in the cook log
- Deep measurement: the build tool's options that record compiler and linker time (option names: check needed)
- Suspect code patterns: heavy includes in public headers, includes that a forward declaration can replace, shared headers that change often (`vcs_churn.py` result)
- A clean build (a build that deletes intermediate results and starts from the beginning) and a cook take a long time, and other work on that PC is hard during them. The advisor does not run them itself. It reads only the logs that the user ran.

### Code health

- Measurement: count the change counts, the files changed together, and the ticket keys with `<플러그인 폴더>/scripts/vcs_churn.py`. Decide whether a change is a bug by looking up the issue tracker.
- The judgment criteria are in `refactor.md` in the same reference folder.

## 5. Linking categories and code paths

To choose "the categories that the changes in that period touched" in the periodic check, each category must have code paths and version control paths. Paths differ by project, so do not write them in this file. Keep them in the "Paths by category" table of the check ledger (`ledger-format.md`) with values that the user checked. If the table is empty, skip that step and write it in "Not checked" in the report.
