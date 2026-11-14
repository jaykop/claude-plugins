---
name: cli
description: "Run and check a Godot 4 project from the command line as an agent on Windows: import assets and refresh the class cache, boot smoke, script error scan, the headless test runner contract, automated screenshots, export with custom templates, and pitfalls of Windows and the Claude desktop app (console versus GUI executable exit codes, AppData virtualization, BOM, timeouts, vsync-throttled windows). Reads the Godot executables, project root, and project commands from .claude/godot-dev/profile.md. Use it after you change .gd, .tscn, .tres, or data files, and whenever you need to run Godot. Not for: code rules (godot-dev:code), clicking through the editor UI, judging feel or fun (a human plays)."
when_to_use: "When you need to run, test, capture, or export a Godot project, or after code or data changes in one. Examples: '테스트 돌려 줘', '스크립트 오류 확인해 줘', '스크린샷 찍어서 확인해 줘', '빌드 뽑아 줘', 'class_name이 안 보여', '내보내기 템플릿 설치', '/godot-dev:cli 점검'."
argument-hint: "[점검|테스트|촬영|내보내기] [args]"
---

# Running Godot from the command line

Godot project files are text, and the console executable reports errors and exit codes. That is enough to check most work without an editor MCP. A human still judges feel, art, and fun.

## Paths and profile

- This skill folder: `${CLAUDE_SKILL_DIR}`. If the variable is not expanded, it is the folder that holds this SKILL.md.
- Project profile: `.claude/godot-dev/profile.md`, with personal overrides in `profile.local.md`. Keys used: `version`, `godot`, `godot_console`, `project_root`, `export_templates`, and the `Commands` section (`import`, `boot_smoke`, `tests`, `validate`, `capture`, `run`). Template: `${CLAUDE_PLUGIN_ROOT}/shared/profile-template.md`.
- No profile: find `project.godot`, read the version from `config/features`, and look for the matching executable in the paths the project instructions name. If you cannot find the exact version, ask. Do not guess.

## Executables

- Use only the Godot version the project pins. Opening a project with another version can rewrite project files.
- Use the console executable (`*_console.exe`) for every run whose output or exit code you read. The GUI executable returns at once with exit code 0 while Godot keeps running, so its result means nothing. (OnceUponATime)
- Run one Godot process per project at a time. Parallel runs write the same import cache. (Catena)

## Check ladder

Run in this order and stop at the first failure. `<console>` is the console executable and `<root>` is the project root (usually `game`).

1. **Import and class cache.** `<console> --headless --path <root> --import`. Run it after you add a `class_name`, add or replace assets, or on a fresh clone. Until it runs, `-s` scripts cannot see new class names. (`--headless --editor --quit` also works.)
2. **Boot smoke.** `<console> --headless --path <root> --quit-after 60` (60 frames). Do not use `--check-only` alone: it only works together with `--script`.
3. **Tests.** The profile's `tests` command. The common form is `<console> --headless --path <root> -s res://tests/run_all.gd`, where the exit code is the number of failures. Runner contract: [reference/test-runner.md](reference/test-runner.md).
4. **Data validation.** The profile's `validate` command, if the project has one.
5. **Screenshots.** Only when the change is visual. See below.

Reading the output (OnceUponATime, Catena, Wraithbound):

- Strip ANSI color codes. A run fails if any line matches `^\s*(SCRIPT ERROR|ERROR:)`, `Parse Error`, or `Unable to convert`, even when the exit code is 0. Known noise goes in an allowlist file with a reason per pattern.
- Give each run a wall-clock limit. A runtime error stops only the function it happens in, so a script can hang instead of quitting. On timeout, kill the process tree (`taskkill /T /F /PID <pid>`) and report the first error line.

Report the commands you ran and their results. Name the checks you did not run and why. Never report an unrun check as passed.

## Screenshots

- Screenshots need a window. `--headless` uses a dummy renderer and gives empty images.
- Batch all window runs into one go and tell the user before you start, because windows will appear on their screen. (Jajang, Jamdok)
- Add `--disable-vsync` and a fixed `--resolution`. Windows opened from an agent session were throttled to about 4 fps by vsync. (Jajang)
- Capture inside the game after the frame is drawn:

  ```gdscript
  await RenderingServer.frame_post_draw
  get_viewport().get_texture().get_image().save_png(out_path)
  ```

  Projects usually wrap this in a capture script (`-s res://tools/capture/<name>.gd -- --out=<folder>`) or a `--capture` dev argument (`godot-dev:code` patterns, dev-args).
- Open and look at the images before you describe the result.

## Export

- Export templates go outside AppData. The Claude desktop app virtualizes AppData writes, so templates installed there may be invisible to Godot. Keep them in the profile's `export_templates` folder and set them as custom templates in each preset, or install them from that folder in the editor's export template manager. (Jajang, OnceUponATime)
- `<console> --headless --path <root> --export-release <preset> <output>` (or `--export-debug`). The preset must exist in `export_presets.cfg`.
- Exclude tools, tests, and test fixtures from release presets (`exclude_filter`). Run the release exe once with `--quit-after` and check its `godot.log`. (OnceUponATime)

## Windows and the desktop app

File encoding, PowerShell, AppData, Python, and git ownership notes: [reference/windows.md](reference/windows.md). Read it before you write files from PowerShell or set up a Python tool environment.
