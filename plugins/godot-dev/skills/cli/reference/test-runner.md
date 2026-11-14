# Headless test runner contract

Use this when you write or fix a project's test runner (usually `res://tests/run_all.gd`). It comes from spikes run on Godot 4.6.2 on Windows (OnceUponATime §9.2 and §11) and from runners in Jajang, Jamdok, and ROKA.

## Runner

1. The runner `extends SceneTree` and is started with `-s`. Autoloads are not ready in `_init()`. In `_initialize()`, `await process_frame` once before you use any autoload. The alternative is a test scene passed as the main scene, where autoloads are ready before the scene's `_ready`.
2. The runner calls each test function. Each test sets a completion mark as its last statement. If a test returns without the mark, a runtime error stopped it: count it as a failure. A `quit(1)` inside a function that hit a runtime error never runs, so the process would hang.
3. Failure reports with `push_error` and the runner ends with `quit(<failure count>)`. All passing ends with `quit(0)`. A `SCRIPT ERROR` line in the output is a failure even when the exit code is 0.
4. Keep the runner free of project autoload assumptions where possible (A-3, A-4 in `godot-dev:code`), so rule classes run without the scene tree.

## Tests

- Rule tests use fixed fixtures, not the live data files. Separate tests check invariants of the live data (every attack has a tell, every reference resolves). Tuning the data then never breaks a rule test. (BeforeTheBell)
- Seeded randomness only (deterministic-sim pattern).
- Input injection: `Input.parse_input_event` changes action state on the next frame, not the same frame. GUI focus and clicks work headless with `Viewport.push_input`; send press and release on different frames. (OnceUponATime)
- Text fitting: `Font.get_string_size()` and `TextParagraph` give the same sizes headless and windowed. Measure with fonts bundled in the project, not system fonts, which differ per PC. (OnceUponATime)
- Gamepad connection changes cannot be simulated for real. Drive that code through its signal and leave real unplugging to a human. (OnceUponATime)
