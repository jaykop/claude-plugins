---
name: write
description: "Draft and review Korean story scripts for visual novels and other story-driven games, from the concept to the script lines. Runs concept sheet → scene list → scene cards → script → self-review in five passes (structure, scenes, dialogue, sentences, format), with genre references (mystery, romance, faction), non-linear structure patterns, an adaptation sheet for folktales and novels, and a cliché check. The project's script format (line kinds, paths, check commands) comes from the project's .claude/story/format.md. A lint script marks sentence candidates. Not for: engine code, image or sound generation, menu and UI text, localization strings, Korean code comments (ko-gamedev)."
when_to_use: "When you write or revise a game's story, plot, characters, scenes, or script lines, or review a script. Examples: '5분 장면 대본 작성해 줘', '이 기획으로 대본 초안', '장면 카드 만들어 줘', '대본 리뷰해 줘', '이 장면 대사 다듬어 줘', '이 설화를 VN으로 각색해 줘', '/story:write 리뷰만 game/content/dialogue/main.dialogue'."
argument-hint: "[전체|축약|리뷰만|수정] [target file or scene]"
---

# Story script writing

Claude drafts the script and a human edits it in a text editor. The human makes the final call. The procedure and review criteria come from writing guides, Korean drama and film scripts, film criticism, and one tested work, condensed into steps. Sources: [reference/sources.md](reference/sources.md).

## Paths and priority

- This skill folder: `${CLAUDE_SKILL_DIR}`. If the variable is not expanded, it is the folder that holds this SKILL.md.
- Project format file: `.claude/story/format.md` at the project root. It says how this project writes scripts: language, paths, line kinds, box size, blind spots of its checker, check commands, lint options. Template and default format: [reference/format-template.md](reference/format-template.md).

Follow, in order: the user's current request; the project's instructions (CLAUDE.md, AGENTS.md), the format file and the documents it names as the source of truth; then this skill. If the project has its own story skill, that skill wins where they differ.

## Before you start

1. Check `git status --short` (or `p4 opened`) and the current branch. Do not overwrite a script someone is editing. If the format file says where content may live (e.g. only on work branches), check that first.
2. Read the format file. If there is none, follow "When the project has no format file" in format-template.md.
3. Read what exists: story documents, the speaker list, the variable defaults, the image ids. Reuse existing ids first.
4. If input is missing, ask once, all together: mode ("Modes" below), genre, length (5 minutes ≈ 50–75 boxes), speakers per scene, viewpoint (person, viewpoint character), how inner voice is written, settings already decided, and whether there is a source to adapt.

## Modes

| Mode | Runs | Human checkpoints |
|---|---|---|
| 전체 (full) | Steps 1–5 | After step 1 (concept sheet), after step 3 (scene cards) |
| 축약 (short) | Steps 1–3 written in one go, then 4–5 | Once, after step 3. For about one 5-minute scene |
| 리뷰만 (review only) | Step 5 only. Do not edit the script; write the report | Report delivered |
| 수정 (revise) | Only the named passes, on a script a human edited | Report delivered |

At a checkpoint, show the output and stop. Do not go on without approval.

## Steps

| Step | File | Output |
|---|---|---|
| 1 Concept | [steps/1-concept.md](steps/1-concept.md) | 3 logline candidates, concept sheet, character sheets |
| 2 Plot | [steps/2-plot.md](steps/2-plot.md) | Scene list, setting and clue reveal table |
| 3 Scenes | [steps/3-scene.md](steps/3-scene.md) | Scene cards |
| 4 Script | [steps/4-write.md](steps/4-write.md) | Script files, data files, image id list |
| 5 Self-review | [steps/5-review.md](steps/5-review.md) | Fixes per pass, items for the human, check results |

Reference files, read when needed:

| File | When |
|---|---|
| [reference/format-template.md](reference/format-template.md) | No format file yet, or creating one; the default format |
| [reference/genre-mystery.md](reference/genre-mystery.md) | Mystery, detective, crime, ghost-story mysteries. From step 1 |
| [reference/genre-romance.md](reference/genre-romance.md) | Romance as the main line or mixed in. From step 1 |
| [reference/genre-faction.md](reference/genre-faction.md) | Real history, period drama, real people. From step 1 |
| [reference/structures.md](reference/structures.md) | Two timelines, a frame story, the same events from another viewpoint, routes per viewpoint. From step 1 |
| [reference/adaptation.md](reference/adaptation.md) | Adapting a folktale, classic, novel, webtoon, true events, or a design document. From step 1 |
| [reference/cliche-check.md](reference/cliche-check.md) | Step 5 pass D |
| [examples/lines.md](examples/lines.md) | Steps 4 and 5. Bad and fixed examples |
| [reference/sources.md](reference/sources.md) | To check where a technique comes from, or to explain it to the human |

A genre with no file (horror, fantasy, SF, and others): if a work in that genre is written, analyze 2–3 example works the user agrees on and add `reference/genre-<genre>.md` in the same form as the existing genre files.

## Always

- Never copy sentences or lines from books and works. Use the techniques only.
- Speakers use only the ids in the project's speaker list. Follow the format file's rules for narration (the default format: no `: ` in narration, narration does not start with `-`).
- One box holds 1–2 sentences, 40 characters or fewer recommended; split above 60. These are provisional numbers; the format file may set others. Evidence is in step 4.
- Do not name emotions in narration. Show emotion through the line's tone, the pose, an action line, then the inner voice, in that order.
- Do not settle by yourself things judged by feel: style, a character's voice, rhythm. Put them under "items for the human" in the report.
- Do not change again what a human kept on purpose (an intent comment, a cliché judged "keep" in a review).

## Checks

After writing or revising a script, run the format file's `Checks` commands and the lint in step 5 pass D. A check that could not run goes in the report with the reason; never report it as passed.

## Report

Report briefly at the end of each step. The step 5 report form is in [steps/5-review.md](steps/5-review.md). In the conversation give the conclusion and a few key lines; details go in the story documents or the report file.
