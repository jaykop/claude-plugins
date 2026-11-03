# Measurement conditions, measurement plans, and reading result files

## 1. Who measures, and when

- The advisor does not build, cook, run the editor, or change settings files (common rules §7). The measurer written in profile `perf.measured_by` does the measuring.
  - `사용자` or `빌드 머신`: the advisor hands over a measurement plan and waits for the result files to arrive in `perf.profiling_dir`.
  - `에디터 자동화`: the advisor sends console commands only when the session has a tool that operates the editor and the user answered "지금 재도 된다" in the conversation. These are play-in-editor values, so mark them as "editor-relative value" (에디터 상대값).
- An unattended run does not measure. It reads only measurement files that already exist.
- Make setting changes for measurement only with console commands or command-line arguments. Do not save them in settings files. Write what you changed in the "Temporarily changed settings" field of the measurement condition table, and when the measurement ends, ask the user whether it was reverted.

## 2. Measurement condition checklist

Fill in all the fields below for every measurement round. The evidence for filling the fields is the metadata of the result files (printed by `csv_profile_stat.py`), the measurement plan, and the user's answers. Do not register a round with an empty field as a baseline, and do not use it for round comparison either (for the unattended exception, see SKILL.md 2-2).

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

| Field (칸) | What to follow | If it deviates |
|---|---|---|
| Build configuration (빌드 구성) | A standalone run (a run outside the editor) of the Development or Test configuration. Do not use Debug configuration values | Use play-in-editor values only as "editor-relative value", and do not use them for over-budget judgments |
| Frame cap and vsync (프레임 상한·수직 동기화) | Turn both off (for example, `t.MaxFPS`, `r.VSync` — check the names in the target engine) | If the cap is hit, the bottleneck hides behind the waiting time. Do not judge the bottleneck |
| Frame throttling when the window is inactive (창 비활성 시 프레임 제한) | Make sure the frame rate does not drop even when the window goes to the back. For a standalone run, `t.IdleWhenNotForeground`; for the editor, the background CPU saving item in the preferences (setting name: check needed) | Ask the user whether the window was kept in front during the measurement. If you cannot confirm it, that round is "conditions unconfirmed" (조건 미확인) |
| Warm-up (워밍업) | Exclude the first entry and the shader compilation section. Discard the first run, or cut the early section with `--skip-frames` | Measure the first entry separately only when you look at hitch and loading items |
| Repeat count (반복 횟수) | 3 times or more under the same conditions | With 1 or 2 runs, the spread is unknown, so do not make a worsening judgment |
| Resolution and quality settings (해상도·화질 설정) | Write the resolution and the quality level (scalability: grouped quality settings) values | If they differ between rounds, "not comparable" (비교 불가) |
| Scene (장면) | A scenario ID of profile `perf.scenarios`. The reproduction steps and the measurement region (how the start and the end are marked) | A scene without an ID gives only a reference value for this round |
| Platform and hardware (플랫폼·하드웨어) | Platform, CPU, GPU, memory | If they differ, "not comparable" |
| Engine and build revision (엔진·빌드 리비전) | The engine version and the project revision (change number or commit) | If they differ, write the revision difference among the causes of the change. If the engine version changed, it is a new baseline candidate |
| Temporarily changed settings (임시로 바꾼 설정) | Console variables and arguments changed for the measurement, and whether they were reverted | If you do not know whether they were reverted, write it in the report |

## 3. Measure separately the region where the value actually does work

- First, find in the code the conditions under which the target code differs from its default behavior. Examples: branch conditions, the maximum headcount, bursts of spawning, the start and the end of an animation blend, level transitions, the start frame and the end frame of a feature.
- Write the evidence you found (file:line) in the measurement plan, and put that region in the measurement sample. To mark the region, use trace bookmarks and region commands (`Trace.Bookmark`, `Trace.RegionBegin` / `Trace.RegionEnd` — check them in the target engine).
- If you could not measure that region, leave it as "not checked" (확인 못 함). Do not measure only a convenient region and judge "it is always the same value, so it is meaningless".
- Do not look only at the average. Look at the average, p95 (the boundary value after excluding the slowest 5%), p99, the maximum, and the hitch count together.

## 4. Measurement plan format

This is the first deliverable of a diagnosis when there is no measurement. Write it in this format in the "Measurement plan" section of the report body. Write it so that the user can follow it exactly.

```markdown
### Measurement plan (측정 계획) MP-<number>: <what it tries to confirm>

| Field (칸) | Value (값) |
|---|---|
| Suspect to confirm (확인할 의심) | <number in the suspect list and item ID> |
| Scenario (시나리오) | <ID of perf.scenarios> — <reproduction steps in one line> |
| Measurement region (측정 구간) | <how the start and the end are marked>. Evidence for the region where the value does work: <file:line> |
| Build configuration (빌드 구성) | Development / Test standalone run (if inside the editor, "editor-relative value" (에디터 상대값)) |
| Command (명령) | <command-line arguments or console commands. For each name, the location where its existence was checked (file:line) or "check needed" (확인 필요)> |
| Repeats (반복) | discard 1 warm-up run + 3 runs |
| Compared with (비교 대상) | <baseline round / previous round / another setting of the same scene> |
| Result files (결과 파일) | Under <perf.profiling_dir>. Ask that the scenario ID be put in the file name or the subfolder by the "Measurement file naming rule" in the judgment criteria table of the check ledger. If the rule is empty, raise setting the rule in "Decisions needed" |
| Measurement condition table (측정 조건 표) | Ask that the fields of item 2 be filled in and handed over together |
| What the advisor does with the result (고문이 결과로 할 일) | <example: look at game thread time p95 with csv_profile_stat.py summary, and look at the inclusive time of the region of suspect 3 with an Insights export> |
```

- Reduce the plans to at most 3 per round. Follow the measurement order of the suspect list (largest call frequency and number of objects that have the code first).
- If another advisor requested the measurement (question inbox), use the scenario ID, platform, metric, and comparison method written in the request as they are. If the scenario ID is not in the profile, raise "a scenario must be added" in "Decisions needed" instead of a measurement plan.

## 5. Reading result files

Do not use numbers shown on screen as evidence. Use only values left in a log or a file. Do not scan large files by eye. Aggregate them with a script, and leave the commands you ran in the report.

### 5-1. CSV profiler results (.csv)

Aggregate them with `<스킬 폴더>/scripts/csv_profile_stat.py`. If `python` is not available, run it with `python3`.

```
# 1) Look at the stat names first. Do not guess a name and put it in --stats.
python "<스킬 폴더>/scripts/csv_profile_stat.py" list <파일.csv>

# 2) Aggregate one round (3 repetitions). Remove the warm-up part with --skip-frames.
python "<스킬 폴더>/scripts/csv_profile_stat.py" summary <r1.csv> <r2.csv> <r3.csv> --stats "<프레임 시간 열>,<게임 스레드 시간 열>,<렌더 스레드 시간 열>,<GPU 시간 열>" --budget-ms <예산 ms> --hitch-ms <히치 기준 ms> --skip-frames <N>

# 3) Compare two rounds (with the previous round and with the baseline round, each)
python "<스킬 폴더>/scripts/csv_profile_stat.py" compare --a <이전 r1> <이전 r2> <이전 r3> --b <이번 r1> <이번 r2> <이번 r3> --stats "<열 이름들>" --budget-ms <예산 ms> --hitch-ms <히치 기준 ms> --skip-frames <N>
```

- The frame time and per-thread time columns usually have names such as `FrameTime`, `GameThreadTime`, `RenderThreadTime`, `RHIThreadTime`, and `GPUTime`. Check the actual names with the result of 1). GPU-related columns may be missing depending on the measurement settings (check the argument that enables GPU statistics in the target engine).
- If you give `--budget-ms` and `--hitch-ms`, the script counts, for each chosen statistic, the frames over that value. Read the hitch count only from the frame time column, and read budget overruns only from time columns in ms. The same fields attached to columns such as counts and bytes have no meaning. If a value is missing, leave out that argument and write "no budget" (예산 없음) and "no hitch threshold" (히치 기준 없음) in the report.
- Copy the "메타데이터" (metadata) of the output (platform, build configuration, engine version, CPU, resolution, and so on) into the measurement condition table. If the metadata differs between files, the script shows it in a separate table.
- If the output has the "집계 중단" (aggregation stopped) mark, do not use that result. Raise the limit or narrow the scope, and run it again.
- A binary-format CSV cannot be read. Ask for it to be converted to a text CSV (the conversion tool name: check needed in the target engine).
- Do not use `--out`. Take the results from standard output, and copy the tables used for the judgment and the commands you ran into the report. If the output is long, reduce the statistics with `--stats` or cut it with `summary --sort p95 --top 20`. Save the report file only in Step Final.

### 5-2. Insights traces (.utrace)

A .utrace is a binary file, so do not read it directly. Make a CSV with the command-line export of Unreal Insights. The advisor does not run this command. It hands the user the form below.

```
UnrealInsights -OpenTraceFile="<파일>.utrace" -NoUI -AutoQuit -log -ExecOnAnalysisCompleteCmd="TimingInsights.ExportTimerStatistics <출력>.csv -region=<구간 이름> -threads=<스레드 이름>"
```

- These command-line arguments, the export command name, and the options (`-region=`, `-threads=`, `-timers=`, `-startTime=`, `-endTime=`, `-columns=`, `-sortBy=`, and so on) **must be checked in the target engine version**. If you search the engine source for `ExecOnAnalysisCompleteCmd` and `TimingInsights.Export`, you find the implementation of the export commands and functional test examples.
- The result of the timer statistics export is a table with one row per timer (measured region name). Its shape differs from CSV profiler results, which have one row per frame, so do not read it with `csv_profile_stat.py`. Check the column names in the header row, and then hand it to analyst with a defined reading scope, such as "the top 20 timers by inclusive time on the bottleneck thread".
- When you look at hitches, export cut to the time range of the hitch frames (`-startTime=`, `-endTime=`).

### 5-3. Other results

| Result | How to read it |
|---|---|
| Section frame statistics (logs and files from `StartFPSChart` / `StopFPSChart`) | Quote the log lines as they are. Write the per-thread averages and the hitch count together with the measurement conditions |
| Memory report (result file of `memreport`) | Hand it to analyst by heading in the report, and receive only the top items |
| Tick list (`dumpticks` log) | Group by class and count. If the log is long, hand it to analyst and receive a count table by class |
| Build and cook logs | Quote the total time line and the per-step time lines |

## 6. Bottleneck judgment

The bottleneck is the thread or resource that holds the frame time. Decide it separately for each scenario.

1. First check whether frame cap and vsync were off in the measurement. If they were on, do not judge.
2. Put the frame time and the per-thread times of the same round (game thread, render thread, RHI thread: the thread that passes graphics API calls to the driver, GPU) side by side with the same metrics (p50 and p95).
3. Treat the side closest to the frame time as the bottleneck. If two sides are similar (the difference is smaller than the spread of that metric), write "two bottlenecks: <A>, <B>" (병목 둘: <A>, <B>) and look at both.
4. Reducing a side that is not the bottleneck does not reduce the frame time. Write an improvement on a side that is not the bottleneck only as "headroom gained" (여유 확보).
5. Look at hitches separately from the average bottleneck. For each hitch frame, look at which side got longer.
6. Leave the table used for the judgment (metrics, values, files, commands) in the "Frame overview" of the report.

## 7. Old measurement files

- When you use a file measured at an earlier revision, write the file's revision and date, and mark it "measured at an earlier revision" (이전 리비전 측정).
- Decide the date of a measurement file not from the file system time but from the metadata of the result file, the date in the file name (treat it only as the date the file was made; common rules §3), or the date the user gave. If none of the three exists, it is "date unknown" (날짜 미상).
