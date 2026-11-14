# Patterns

Optional. Use a section when the profile's `patterns` list names it, or when the task clearly needs it. These are not rules for every game: a short prototype may skip all of them.

## data-driven — content in JSON or CSV

For games with many items, enemies, events, or tuning values. (Catena, BeforeTheBell, OnceUponATime, Jajang, Jamdok)

- Every data file carries `schema_version`. One loader per file kind (D-5). Errors name the file, the line or key, and the item.
- A validator runs outside the game (a `-s` script or a Node/Python tool) and checks references, types, ranges, and duplicate ids before the game runs. Give each rule a negative fixture and make the validator's self-test fail when a rule has none. (OnceUponATime)
- Godot imports `.csv` files as translations by default. Data CSVs must use the Keep File import (`importer="keep"` in the `.import` file). Check this in the validator. (BeforeTheBell)
- Player-visible text lives in a translation CSV and code uses keys. A lint pass rejects Korean string literals in `.gd` and scene properties, with log calls as the exception. (OnceUponATime, BeforeTheBell)
- Optional: hot reload of data with a key (BeforeTheBell used F5), followed by a `data_reloaded` signal that subscribers use to refresh.

## deterministic-sim — rules you can replay

For combat simulations, tactics, auto-battlers, and anything you balance with batch runs. (Jamdok, BeforeTheBell, Jajang)

- The rule core has no `Node`, physics, `Timer`, or wall-clock time. It advances by ticks or frames.
- Random numbers come from named `RandomNumberGenerator` streams with a fixed seed. No global `randi()`, no `Time`, no `_process` delta in decisions. Camera and UI effects are exempt.
- A headless batch runner plays the simulation N times and prints win rates, durations, and event counts (for example `-s res://tools/cli/battle_batch.gd -- --n=100`).
- Rule tests use fixed fixtures. Tests against the real data check invariants only, so tuning the data does not break rule tests. (BeforeTheBell)

## preview — show the result before committing

For turn-based and tactical games that show a forecast. (Catena)

- Run the same resolver on a `clone()` of the state (R-3). Do not write a second "preview" version of the rule.
- Data for two fixed sides (ally, enemy) lives in a small wrapper with two typed fields and `for_side(side_id)`, not in `Dictionary[String, T]`.
- When building Y from X piles up helper functions in a facade, move them to a static factory on Y (`CombatUnitView.make_ally(...)`). Pass dependencies as arguments. Y never holds a reference to the game state.

## save — save files and migration

For anything with progress that survives a restart. (BeforeTheBell, BootRoom, Catena)

- Write atomically: write `*.tmp`, then rename.
- The file carries `version`. A migrator raises old files one step at a time (`_migrate_1_to_2`), with a unit test per step.
- Fix the save folder with `application/config/use_custom_user_dir` and `custom_user_dir_name`. Otherwise `user://` follows the project name and moves when the title changes.
- Validate on load and repair broken references to known-good values. Test the round trip and a forced quit.

## editor-tools — tools inside the editor and the game

For games that need hand-tuned data: levels, motions, sounds, pieces. (Jajang, Jamdok)

- A tool screen is one `@tool` Control scene under `game/tools/`. It has two hosts: an EditorPlugin that puts it in a main-screen tab, and a dev menu in the running game (debug builds only). Edit, save, and reload without leaving the game.
- Tools save through the same loader and validator as the game (D-5).
- For agent checks, a tool can take an environment variable that makes it capture its own screen and run scripted edits (Jajang: `MOTION_EDITOR_SNAPSHOT=<folder> <godot> --editor --path game`).

## dev-args — developer launch arguments

For any game you test often. (Jamdok, BeforeTheBell, OnceUponATime)

- Arguments after `--` are read from `OS.get_cmdline_user_args()` by one dev script or autoload.
- Common set: `--scene=<path>`, `--battle=<a>:<b>`, `--seed=<n>`, `--speed=<n>`, `--capture=<folder>[,seconds]`, `--quit-after=<seconds>`, `--tools`, `--pause-at=<seconds>`.
- Dev-only features are disabled in release builds. Gate them with a debug build check or a custom export feature tag (OnceUponATime used `test_hooks`).
