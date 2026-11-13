# Project format file

The skill writes in the project's script format. The project describes it in `.claude/story/format.md` at the project root. This file is the template for it, plus the default format the skill uses when a project has none.

## When the project has no format file

- If the user asks only for story documents (concept, plot, scene cards), the format file is not needed. Write the documents to `docs/story/` unless the project's instructions name another folder.
- If the user asks for script lines: look at how the project already stores dialogue (dialogue files, JSON, a dialogue plugin, design documents) and ask once whether to create `.claude/story/format.md` from the template below. Fill what you found and leave the rest empty. Until the user answers, write in the default format.
- Never guess check commands. An empty `Checks` section means no checks run, and the report says so.

## Template

Copy this into `.claude/story/format.md` and fill it. Remove sections that do not apply. The project's own documents (README, engine docs) stay the source of truth for grammar; this file summarizes and points to them.

```markdown
# Story format: <project>

## Language
<script language, e.g. ko>

## Source of truth
<files that define the script grammar. If this file and they differ, they win and this file gets fixed>

## Paths
- Story docs: <folder for concept.md, characters.md, plot.md, scenes.md, review-*.md>
- Scripts: <glob of script files>
- Data files: <speaker list file, variable defaults file>
- Images: <background folder, character folder layout>
- Where content may live: <e.g. only on work branches; main holds the engine>

## Line kinds
| Kind | Form | Rules |
|---|---|---|
| Narration | | |
| Spoken line | | |
| Line with pose | | |
| Pose only | | |
| Enter, exit | | |
| Scene change | | |
| Choice | | |
| Variable | | |
| Jump | | |
| Pause | | |
| Comment and intent comment | | |

## Inner voice
<how the protagonist's inner voice is written (narration line or its own speaker id) and the limits of each in this engine>

## Box
- One box: <what the player sees at once>
- Width: <about N characters per line in the UI, and how it was measured>
- Length rule: <keep the skill's rule (40 recommended, split above 60) or give other numbers with the reason>

## Data files
<format of the speaker list and the variable defaults, and what the checker requires (e.g. every speaker needs at least one pose image)>

## Blind spots
| Script line | What actually happens | What to do |
|---|---|---|

## Path limit
<maximum branch paths the checker follows, or "none">

## Checks
| Check | Command | Where it can run |
|---|---|---|

## Lint options
<arguments for story_lint.py, e.g. --command '<regex>' --speaker '<regex>'. Empty means the defaults>

## Placeholders
<how to stand in for images that do not exist yet, and where to record that they are placeholders>

## Related skills
<project skills to use alongside, e.g. a UI skill for mechanics that need a screen>
```

## Default format

Plain text, one line per box, in the style of Godot's Dialogue Manager. The lint defaults fit it.

| Kind | Form | Rules |
|---|---|---|
| Narration | a plain sentence | No `: ` inside. Does not start with `-`, `~`, `#`, `%`, `=>`. One tense for all narration |
| Spoken line | `<speaker id>: line` | Speaker ids are lowercase English, digits, underscore |
| Line with pose | `<speaker id>: line [#pose=<pose id>]` | Only on spoken lines |
| Stage commands | `do Stage.bg("<id>")`, `do Stage.enter("<id>", "<pose>", "<slot>")`, `do Stage.exit("<id>")`, `do Stage.pose("<id>", "<pose>")` | If the project has no stage, leave them out and write the place in narration |
| Choice | `- option text`, the reaction indented one tab below | 1–2 boxes of reaction. Conditional: `- text [if <condition> /]` |
| Variable | `set <name> = <value>`, `set <name> += 1` | English snake_case |
| Scene label, jump | `~ <scene id>`, `=> <scene id>`, `=> END` | Rejoin branches by jumping to a scene id |
| Pause | `[wait=0.5]` inside a line | Only for a swallowed breath |
| Comment | `# ...` | One-line card summary under each scene label. Intended expressions: `# 의도: ...` |

- Ids (speakers, backgrounds, poses, scene labels): lowercase English, digits, underscore. The script and the file names use the same string.
- Inner voice: a narration line by default; a separate speaker id (e.g. `hero_inner`) if the user prefers. Count it together with the protagonist as one speaker.
- Box: one line is one box. The skill's length rule applies.
- Checks: none beyond `story_lint.py` with its defaults. Say so in the report.
