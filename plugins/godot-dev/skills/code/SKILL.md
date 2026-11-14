---
name: code
description: "Code and scene rules for Godot 4 GDScript game projects. Use it when you write, change, or review .gd, .tscn, or .tres files, data loading, save files, or rule and simulation code in a Godot project. Covers data shape (typed classes, Dictionary only at boundaries), one owner for constants and helpers, mutation naming, file length review points, UI that does not own rules, one code path for game, preview, and checks, data-driven content referenced by id, the error policy, comments, GDScript pitfalls, and scene structure, plus optional genre patterns (data-driven content, deterministic simulation, saves, editor tools, dev launch arguments). The rules come from the user's own Godot projects. Project values come from .claude/godot-dev/profile.md. Not for: running Godot or reading results (godot-dev:cli), comment wording and terms (ko-gamedev:style), screen design (game-ui:screen), general Godot tutorials."
when_to_use: "Before you write or review GDScript or scenes in a Godot project, also inside a larger feature task. Examples: '이 기능 구현해 줘'(Godot 프로젝트에서), '이 스크립트 리뷰해 줘', '씬 구조 정리해 줘', '데이터 로더 만들어 줘', '세이브 구조 짜 줘', '전투 시뮬 분리해 줘', '/godot-dev:code 리뷰만 game/scripts/battle/'."
argument-hint: "[작성|리뷰만] [file or folder]"
---

# Godot code rules

Follow these rules when you write or review GDScript and scenes. They were collected from the user's own Godot projects. Most appeared in two or more of them. The project names after a rule are its sources, so a reader can check the original.

## Paths and priority

- This skill folder: `${CLAUDE_SKILL_DIR}`. If the variable is not expanded, it is the folder that holds this SKILL.md.
- Project profile: `.claude/godot-dev/profile.md` in the project root. It holds the values this skill does not guess: error policy, comment language, file header, length review point, data format, which patterns apply. Personal values (local paths) can go in `profile.local.md` next to it, which is not version controlled. Template: `${CLAUDE_PLUGIN_ROOT}/shared/profile-template.md` (the plugin folder is two levels above this file).
- If there is no profile, use the defaults written here and say once that the project has no profile.

Follow, in order: the user's current request, the project's instructions (AGENTS.md, CLAUDE.md) and the project's own code manual, the profile, then this skill.

## Modes

| Mode | When | Do |
|---|---|---|
| 작성 (default) | You add or change code or scenes | Before you write, name in one line the rule groups that apply. Write. Run the checklist below. Then run the checks in `godot-dev:cli`. |
| 리뷰만 | The user asks for a review | Read the target and report findings. Do not edit. |

Reference files, read when the task touches them:

| File | Read when |
|---|---|
| [reference/gdscript.md](reference/gdscript.md) | You write any `.gd` file. Typing, pitfalls, member order, node references. |
| [reference/scenes.md](reference/scenes.md) | You create or edit a `.tscn` file or UI layout. |
| [reference/patterns.md](reference/patterns.md) | The profile lists a pattern, or the task loads data, saves, simulates rules, builds an editor tool, or adds dev launch arguments. |

## Rules

C# projects: the rules in this file apply. The GDScript reference does not.

### Data (D)

- **D-1** Runtime data is a typed class (`class_name` on a `RefCounted` or `Resource`). Use `Dictionary` only at boundaries: raw JSON before validation, save files, third-party state (for example Dialogue Manager variables), debug output, editor metadata. A Dictionary shape passed through two or more functions becomes a class. (Catena, VNTool, Wraithbound)
- **D-2** One value, one place. Do not store the same value under two keys. Compute display values with a function. (Catena, VNTool)
- **D-3** Content and tuning live in data files (JSON, CSV, `.tres`), not in code. No magic numbers except 0, 1, -1, and 2. Player-visible text uses translation keys. (BeforeTheBell, Jajang, Jamdok, OnceUponATime, Wraithbound)
- **D-4** Refer to content by id. Keep the id, the display name, and the file path apart. Code resolves paths from a folder convention and never hard-codes a content path. (VNTool, OnceUponATime, Jajang, Jamdok)
- **D-5** One loader per file kind. Existence check, parse, `schema_version` check, and shape check happen in that one owner. Old keys, aliases, and fallback values are allowed only inside that loader or `from_dictionary`. The rest of the code sees only normalized data. (Catena, VNTool)
- **D-6** No hidden defaults. Code does not invent a missing character, background, stat, or speaker. A needed default is written in a data file or project setting. (Catena, VNTool)
- **D-7** Placeholder and final assets live in separate folders. Never infer a rule from an asset's name, color, or size. Hand-edited outputs of a generator go in an `override/` folder that the generator does not overwrite. (VNTool, Jajang, Jamdok, OnceUponATime)

### Responsibility (R)

- **R-1** UI shows data and forwards input. Rules (what is allowed, what a tag means, how a value is computed) live in model or service classes. (VNTool, BeforeTheBell, Wraithbound)
- **R-2** Rule calculation (movement rules, vision, combat simulation, damage) lives in classes without `Node`, apart from drawing, and is testable headless. These classes do not call autoloads. (Jajang, Jamdok, BeforeTheBell)
- **R-3** The game, the preview, and the check tools call the same function. If a preview and the real action follow the same rule, they share one code path. (VNTool, Catena, Jajang)
- **R-4** A function that changes state says so in its name: `set_`, `apply_`, `add_`, `remove_`, `reset_`, `enter_`, `exit_`, `commit_`. `get_`, `find_`, `resolve_`, `list_`, `is_`, `has_`, and `*_path` are read-only. A resolver returns a result. The change happens at an explicit apply step. (Catena, VNTool)
- **R-5** A constant or helper used by two files has one owner. When the same lookup, path rule, or text conversion appears a second time, move it to the owner. Reuse an existing typed class by composition. Do not copy its fields into a new class. (Catena, VNTool)
- **R-6** Load, parse, and check functions are read-only. Files are written only by functions whose name and target are explicit: save, settings, screenshot. (VNTool)
- **R-7** Add an abstraction only for a real boundary: a rule repeated twice, data that needs an owner, a boundary you can test. No empty managers, generic payload routers, or catch-all registries for future features. (VNTool)
- **R-8** File length is a review point. At the profile's `length_review` (default 500 lines), check that the file has one responsibility. Over 1000 lines, split it or write down why. Split an over-limit file before you add features to it. "It is the main scene" is not a reason to keep unrelated state and functions together. (Catena, VNTool, BeforeTheBell)

### Errors (E)

- **E-1** The default policy is `strict`. A missing file or reference reports the file and the item with `push_error`. The runtime never guesses or patches a value. A validator or test catches content errors before the game runs, and the runtime only reports. (VNTool, Wraithbound)
- **E-2** With `error_policy: lenient` in the profile, a loader may skip a bad row of hand-edited tuning data. It still collects a warning for every skipped row and prints them together. Nothing fails silently. (BeforeTheBell)
- **E-3** A missing asset may show a visible placeholder with one warning in debug builds. A release check fails if any placeholder remains. (BeforeTheBell, OnceUponATime)
- **E-4** A required node that is missing reports with `push_error` in `_ready` and leaves the script inert. Never create a substitute node silently. (Wraithbound)

### Comments and files (C)

- **C-1** Comments use the profile's `comment_language` (default Korean). Identifiers, Godot API names, and data keys stay English. Comments explain why, intent, invariants, and removal conditions. They do not repeat what the line does. For word choice, follow `ko-gamedev:style` when it is installed. (Catena, BeforeTheBell, VNTool, and six AGENTS.md files)
- **C-2** Fields of data classes, enums, and static catalogs always get a comment: meaning, unit, allowed values, whether the value is saved or runtime only. Functions get a comment only when the contract, side effect, call timing, or order is not visible in the code. (Catena)
- **C-3** Comments are maintained with the code. A stale comment is worse than none. A `TODO` states why it is left and the condition that resolves it. Temporary compatibility code states its removal condition. (Catena)
- **C-4** New files start with the profile's `file_header` and a one-line responsibility comment. No verdict comments such as "reviewed" or "검토 통과". (Catena, VNTool, BeforeTheBell)
- **C-5** `.gd`, `.tscn`, `.tres`, `.json`, `.gdshader`, and `.cfg` files are UTF-8 without BOM, with LF line ends. How to avoid a BOM on Windows: `godot-dev:cli`. (Jajang, Jamdok, OnceUponATime, FirstBlade)

## Checklist before you report

- Which rule groups applied?
- New Dictionary used as runtime data? New magic value? Hidden default?
- id, display name, and path mixed anywhere?
- Does UI code decide a rule? Do preview, game, and check run different code for one rule?
- Does a load or check function write a file or change outside state?
- Is any error swallowed without a report?
- Do new data fields and enums have comments? Is a file past the review point?
- Did you run the `godot-dev:cli` checks? Name the checks you did not run and why. Never report an unrun check as passed.

## Review output

One line per finding, most severe first:

```
path:line — rule id — problem — fix
```

Group findings that share a cause. Mark a finding as uncertain when you could not confirm it by reading the code.
