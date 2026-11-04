---
name: style
description: "Write and correct Korean code comments and technical documents in game projects with the vocabulary and register Korean game developers use. A glossary split by area (core verbs, spelling, Unreal, combat, animation, AI and systems) maps AI-style Korean (쓴다, 돌려준다, 고른다, 편집기, 시각, 피해, 가운뎃점 나열, ~므로) and common misspellings to industry words (사용한다, 반환한다, 선택한다, 에디터, 시점, 대미지), and style guides set the register for comments and documents. A lint script finds candidates in comments only. Not for: English text, player-facing UI or localization strings, general prose outside game development, code logic changes."
when_to_use: "When you are about to write Korean comments or documents in a game project, and when the user asks things like '주석 한국어 다듬어 줘', '업계 용어로 고쳐 줘', 'AI 말투 같은 주석 정리해 줘', '이 설계 문서 문체 교정해 줘', '게임 용어 맞게 썼는지 봐 줘', '/ko-gamedev:style Source/ 검토만'."
argument-hint: "[files or folders] [검토만|수정]"
allowed-tools: Read, Glob, Grep, Edit, Bash(python *ko_lint.py*), Bash(python3 *ko_lint.py*), Bash(git status *), Bash(git diff *), Bash(p4 opened*)
---
<!-- ko-lint: ignore-file -->

# Korean game-dev style

Korean game developers write comments with Sino-Korean and loanword verbs (사용, 반환, 세팅, 체크, 스폰), English engine names, and short noun-ending notes. AI-written Korean leans the other way: purified native verbs (쓴다, 돌려준다, 고른다), translated engine words (편집기, 저작), full ~다 sentences everywhere, middle-dot lists and ~므로 chains. This skill moves Korean text toward the industry register while keeping grammar and spelling clean.

The rules come from measured corpora: a commercial UE5 project written by people (A), public game projects by Korean developers from before 2022 (O), an AI-written UE5 project (K), and a team's design pages (D). See [glossary/README.md](glossary/README.md#evidence).

## Paths and priority

- This skill folder: `${CLAUDE_SKILL_DIR}`. If the variable is not expanded, it is the folder that holds this SKILL.md.
- Project terms file: `.claude/ko-gamedev/terms.md` in the project root, if it exists.

Follow, in order: the user's current request, the project's instructions (CLAUDE.md, AGENTS.md) and project terms file, then this skill.

Check the project's instructions for the comment language before you start. If they require English comments:

- New comments: write them in English. This skill does not apply.
- A request to correct existing Korean text: if the user did not say whether to polish the Korean or translate it to English, ask once. In `검토만` mode, state the conflict at the top of the report and continue the review.

## What to read

Read once per session, not per comment. Read only the area files the text touches.

| Always | When |
|---|---|
| [glossary/core.md](glossary/core.md), [glossary/spelling.md](glossary/spelling.md) | Any Korean comment or document |
| [style/comments.md](style/comments.md) | Code comments, tooltips, tag descriptions |
| [style/documents.md](style/documents.md) | Design docs, tech docs, manuals, dev logs |
| [glossary/unreal.md](glossary/unreal.md) | Unreal projects |
| [glossary/combat.md](glossary/combat.md) | Targeting, damage, hits, reactions, defense, skills |
| [glossary/animation.md](glossary/animation.md) | Anim assets, blending, locomotion, root motion, IK |
| [glossary/systems.md](glossary/systems.md) | AI, spawn, world, items, quests, UI, production words |
| [style/ai-tells.md](style/ai-tells.md) | Correcting AI-written text, or when you need the reasons behind a rule |

## Writing new text

Apply the files above while you write. Before you hand over more than a few lines, run the lint on the changed files and fix the `replace` hits.

## Correcting existing text

1. Scope. Use the files the user named. Check `git status --short` (or `p4 opened`) and keep other people's changes. For a wide scope, size it first with `--summary`.
2. Candidates. Run the lint on the scope:

   ```
   python "${CLAUDE_SKILL_DIR}/scripts/ko_lint.py" <files or folders>
   python "${CLAUDE_SKILL_DIR}/scripts/ko_lint.py" --summary <folder>
   ```

   Use `python3` if `python` is missing. The lint reads only comments (C++, C#, Python, GDScript, ini `DevComment`) and document text (Markdown outside code). A hit is a candidate, not a verdict. Density marks (`·`, ~므로, bare 대상) are counted per file; add `--kind replace,review,density` to list their lines.
3. Read each candidate in its full comment block or paragraph. Decide by meaning: 쓴다 can mean write, 본다 can mean look, 가운데 can mean the center. Then fix the whole block: words from the glossary, register from the style file. Also fix what the lint cannot see: other inflections of a listed verb, 대상 that means a combat target, comment kind and register, metaphors, overlong explanations.
4. Edit only Korean comment and document text. Keep identifiers, string literals, log and UI strings, `UPROPERTY` metadata (`DisplayName`, `ToolTip`, `Category`), code, encoding (BOM) and line endings.
5. Keep the facts: conditions, negations, numbers, units, defaults, lifetime, failure handling. Do not add a fact you did not check in code. If a comment contradicts the code, report it instead of rewriting it to match either side.
6. Run the lint again on the changed files.

In `검토만` mode, do not edit. Report a table: `file:line`, before, after, reason. Put repeats of the same change in one row and list their line numbers. Report the lint totals once, since nothing changes.

For a scope over about 20 files, work in batches by folder. You can give each batch to a subagent: pass this skill folder path, the batch's file list, and steps 3 to 6.

## Report

State what you read and changed (files, lines), the lint totals before and after (`검토만`: once), the hits you left on purpose with the reason, and any comment that contradicts the code. Say which parts you did not read.

## Do not

- Copy the flaws of human comments: typos, 일단, 그냥, `...`, mixed ~다 and ~니다.
- Rewrite a clear, correct sentence only to change its ending.
- Translate class, function, property or tag names.
- Touch player-facing text; its wording belongs to the design and localization team.
- Quote comments from corpus A in files you write.

## Project words without a terms file

When a word the glossary flags is the project's own defined term (a graph system's 전이, an action system's 부위), leave it, list it in the report under hits left on purpose, and offer to create `.claude/ko-gamedev/terms.md` with an `Allow` row for it.

## Extending the glossary

Add project words to the project terms file, with an `Allow` table for words the project defines differently. Add general words to the area file in `glossary/`. Row format and evidence rules: [glossary/README.md](glossary/README.md).
