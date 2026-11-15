---
name: prose
description: "Write and correct Korean story prose in game projects (synopses, pitches, loglines, 기획의도, world and character introductions, concept documents, scene summaries, narration) so that a Korean reader can follow it and it does not read as AI-written. Rules come from 31 Korean novels, 37 Korean writing and film books, professional drama and film introductions, and AI-written story documents that a reader could not follow. It fixes reasoning with no owner (a character's calculation written as a general rule), facts stacked with -고 and periods and no relation, missing turn markers, date-log sentences, catch-all verbs (넘긴다, 안다, 본다, 둔다), metaphor verbs for plot logic (무너진다, 남는다, 드러난다, 이어진다), vague nouns (자리, 일, 몫, 줄, 손, 셈), wrong pairings (보라를 캐묻는다, 미끼를 낸다), mixed registers, and thin character lines. A lint script marks word candidates, long sentences and parenthesis chains, and compares the linking rate with books. Not for: code comments and technical documents (ko-gamedev:style), story structure, dialogue voice and script format (story:write), English text, UI strings."
when_to_use: "When you write or correct a Korean story document or narration in a game project, and when the user says things like '시놉시스 문장 다듬어 줘', '소개문이 AI가 쓴 것 같아', '무슨 말인지 모르겠어', '어휘 수준이 낮아', '기획서 문체 교정해 줘', '인물 소개 다시 써 줘', '/ko-gamedev:prose game/content/story/pitch.md 검토만'. Also before you show a story pitch to a human."
argument-hint: "[files or folders] [검토만|수정]"
allowed-tools: Read, Glob, Grep, Edit, Bash(python *prose_lint.py*), Bash(python3 *prose_lint.py*), Bash(git status *), Bash(git diff *), Bash(p4 opened*)
---
<!-- ko-lint: ignore-file, prose-lint: ignore-file -->

# Korean story prose

AI-written Korean story documents fail in a way a reader feels before they can name it. Sentence after sentence states a fact in the same flat form, so nothing follows from anything. A character's calculation sits between events as if it were a law of the world. One native verb carries five meanings, and short nouns like 자리, 일, 몫 stand for whatever the writer had in mind. The reader has to rebuild the author's head to understand the plot.

This skill fixes that with rules measured on Korean books and on AI documents a reader could not follow. Evidence and corpora: [glossary/README.md](glossary/README.md#evidence).

## Paths and priority

- This skill folder: `${CLAUDE_SKILL_DIR}`. If the variable is not expanded, it is the folder that holds this SKILL.md.
- Project prose terms: `.claude/ko-gamedev/prose-terms.md` at the project root, if it exists. It is separate from ko-gamedev:style's `terms.md`.

Follow, in order: the user's current request; the project's instructions (CLAUDE.md, AGENTS.md); story:write and the project's story format file (`.claude/story/format.md`) where they apply; then this skill.

Boundaries:

- ko-gamedev:style is for code comments and technical documents, and pushes verbs the other way (넘긴다 → 전달한다). Do not apply its verb rows to story prose. In a document that mixes a system spec and a story, use style for the spec sections and this skill for the story sections.
- story:write owns the story itself: the event chain, the twist, scene structure, dialogue voice and the script format. Its `reference/presenting.md` decides the order of a checkpoint pitch. This skill owns the Korean of the sentences. If a fix would change what happens or why, it is a story question: report it, do not decide it.

## What to read

Read once per session, not per paragraph.

| Always | When |
|---|---|
| [style/ai-tells.md](style/ai-tells.md), [style/sentences.md](style/sentences.md), [style/words.md](style/words.md), [glossary/words.md](glossary/words.md) | Any Korean story document or narration |
| [style/introductions.md](style/introductions.md) | Logline, 기획의도, synopsis, pitch, world or character introductions |
| [style/examples.md](style/examples.md) | Before your first correction in a session, to see a whole fix |

## Writing new text

Apply the files above while you write. Before you hand over more than a paragraph, run the lint and the checks at the end of [style/sentences.md](style/sentences.md) (first sentences only; 왜? 누구 생각?). Before a human reads a pitch or a synopsis, also run the fresh reader check (step 8 below), unless story:write's cold read already covers the same text.

## Correcting existing text

1. Scope. Use the files the user named. Check `git status --short` (or `p4 opened`) and keep other people's changes.
2. Read the whole document before you change anything. Write for yourself a five-line retelling: who wants what, what happens, and why. Mark every point where the retelling needed something the text does not say. Those are the missing links, and they matter more than any word. A sibling document (concept, event table) can tell you what the author meant; use it to understand, not to import new facts.
3. Mark candidates:

   ```
   python "${CLAUDE_SKILL_DIR}/scripts/prose_lint.py" <files or folders>
   python "${CLAUDE_SKILL_DIR}/scripts/prose_lint.py" --summary <folder>
   python "${CLAUDE_SKILL_DIR}/scripts/prose_lint.py" --kind density <file>
   ```

   Use `python3` if `python` is missing. The lint reads Markdown and text outside code and quotation marks. It lists `review` words; `owner`, a present-tense sentence built on an "only if" (~라야, ~해야) or two -면 conditions with no thinking verb or reason marker (S3); sentences over 25 eojeol (`long`); and sentences with two or more parentheses (`paren`). It lists `density` words only when the file uses them at 3 times the book rate. Per file it also prints five sentence measures next to the book values: sentences opening with a connective, linked sentences in long paragraphs, -면 conditions, sentences opening with a date, -고 joins. A hit is a candidate; decide by meaning. The measures show direction: do not chase the book numbers by adding connectives (S2).

   The `owner` check finds only the plainest cases (3 of the 9 in the pitch it was tested on). Read every sentence that sounds like a reason for its owner yourself.
4. Fix in the order of [style/sentences.md](style/sentences.md#revision-order): paragraphs, then relations and owners of reasons, then sentence size, then subjects, names and words. Words come last because restructuring removes many of them.
5. Keep the facts: every event, person, number, date, cause, condition and negation. Add no fact, motive or event. When you cannot tell what a sentence means (whose plan this is, which 일 is meant, who 그 is), do not guess: list it as a question. When a reason needs an owner the text does not name, take it from the source document, or ask.
   - Reordering is allowed: you may move a fact to the paragraph that uses it, or a reason next to its action. Dropping is not.
   - A fuller character line (I3) may use only facts from the same document or its source document. What is missing is a question for the author.
   - Writing out an owner or a purpose that the source document states is not adding a motive. List each one in the report under "taken from the source", so the author can check it.
   - Do not delete a coined term the document defines, even when there are more than I4 allows. List the terms and ask which to keep.
6. Keep what is not prose: quoted character lines, coined terms the document defines, tables, ids, headings, Markdown structure, encoding and line endings. A table cell is prose only if it is a sentence. One exception: draft numbers and review notes in the title line move to a status line under it (I9).
7. Run the lint again on the changed files, then the checks at the end of [style/sentences.md](style/sentences.md#checks). Compare the length: giving reasons their owners and paragraphs their points makes a text longer, and up to about a quarter more is normal. Beyond that, look for the same frame sentence repeated (~라는 계산이다, ~고 판단한다 in every paragraph) and merge.
8. Fresh reader, for a pitch or synopsis a human will judge, or whenever the user said they could not follow the text: give a new agent only the corrected text, no conversation and no source files. Ask it to retell who wants what, what happens and why, and to list every sentence it had to read twice. Compare with what the author meant, fix, and repeat at most once more. Report what the reader still got wrong.

In `검토만` mode, do not edit. Report a table: `file:line`, original, correction, rule code (S, W, I, or the glossary row). Put repeats of one change in one row with their line numbers. Report the lint results once.

For a long document, work section by section. You may hand sections to subagents with this skill's folder path, the section, and steps 4 to 7. Run steps 2 and 8 on the whole document yourself.

## Report

Write the report in the project's language. State:

- What you read and changed (files, sections), and one representative paragraph before and after.
- Lint before and after: hits by kind, the connective and linking rates against the book values.
- Questions you could not settle without guessing (step 5), and story problems you found but did not touch (a motive missing from the source, an event with no cause).
- Hits left on purpose, with the reason (an idiom, a character's line).
- The fresh reader's result, if you ran it; say so if you did not.

## Do not

- Turn the text into Sino-Korean officialese or literary prose. Plain and exact is the target ([style/ai-tells.md](style/ai-tells.md#what-not-to-over-correct)).
- Put a connective on every sentence, or break every long sentence into fragments.
- Change a character's quoted line, voice or deliberate slang.
- Fix plot logic by inventing reasons. Reasons come from the author or the source document.
- Copy sentences from the books cited in this skill. Write new examples.

## Extending

Project words go in `.claude/ko-gamedev/prose-terms.md`, with an `Allow` table for words the story defines (a gang's own slang). General rows go in [glossary/words.md](glossary/words.md) with measured evidence; row format and rules: [glossary/README.md](glossary/README.md).
