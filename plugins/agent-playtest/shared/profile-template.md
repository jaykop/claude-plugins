# agent-playtest profile

Copy this file to `.claude/agent-playtest/profile.md` in the project root and fill in the values. Keep it in version control.

## Values

- test_level: /Game/Maps/LV_Test  # level for agent checks; a test guide that names another level asks first
- report_dir: docs/agent-check  # where reports go; not the handoff note folder itself, because other skills read every file there as a handoff note. Reports hold absolute local paths of run records: in a public repository, use a folder that version control ignores
- language: ko  # language of the report and the comment draft
- tracker_public: true  # true leaves local paths out of comment drafts

## Project notes

Facts about this game that the agent cannot learn from the tools. Keep each line short and current.

- Debug log commands for the features you check often, e.g. `log LogMyGame Verbose`.
- Cheats for preconditions (kill, god mode, apply an effect), and what they need first (for example: open the effect asset in the editor before applying it by name).
- Input notes, for example whether movement is relative to the camera.
- Anything in the test level the agent should know, for example where the player starts and which actors are test fixtures.
