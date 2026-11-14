# godot-dev profile

Copy this file to `.claude/godot-dev/profile.md` in the project root and fill in the values. Keep it in version control. Paths that differ per PC can go in `.claude/godot-dev/profile.local.md` (add it to `.gitignore`), which overrides the same keys.

## Engine

- version: 4.7.2
- godot: C:\Users\<user>\Documents\Godot\Godot_v4.7.2-stable_win64.exe
- godot_console: C:\Users\<user>\Documents\Godot\Godot_v4.7.2-stable_win64_console.exe
- project_root: game
- renderer: GL Compatibility  # GL Compatibility | Forward Plus | Mobile
- language: GDScript  # GDScript | C#
- export_templates: C:\Users\<user>\Documents\Godot\export_templates\4.7.2.stable\

## Commands

`<godot>` and `<godot_console>` stand for the paths above. Add the project's own commands below the common ones.

- import: <godot_console> --headless --path game --import
- boot_smoke: <godot_console> --headless --path game --quit-after 60
- tests: <godot_console> --headless --path game -s res://tests/run_all.gd
- validate: (none)
- capture: (none)
- run: <godot> --path game

## Code rules

- error_policy: strict  # strict | lenient (godot-dev:code E-1, E-2)
- comment_language: ko
- file_header: "# <프로젝트 이름> — <이 파일의 책임 한 줄>"
- length_review: 500
- data_format: json  # json | csv | tres | none
- patterns: []  # any of: data-driven, deterministic-sim, preview, save, editor-tools, dev-args
- project_code_manual: (none)  # a project document that overrides these rules, e.g. docs/manual/coding-standards.md
