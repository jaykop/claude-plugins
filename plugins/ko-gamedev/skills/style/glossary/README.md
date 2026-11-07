<!-- ko-lint: ignore-file -->
# Glossary format and sources

The glossary is split by area. Each file is a set of Markdown tables. `scripts/ko_lint.py` reads every table that has `Use` and `Avoid` columns, so the tables are both the reference and the lint rules.

| File | Area |
|---|---|
| [core.md](core.md) | Verbs, conditions, nouns, connectives and casual words used in every area |
| [spelling.md](spelling.md) | One spelling per loanword |
| [unreal.md](unreal.md) | Engine, editor, gameplay framework, networking, collision, GAS, engine internals |
| [combat.md](combat.md) | Targets, lock-on, damage, hit and hurt, reactions, defense, skills |
| [animation.md](animation.md) | Anim assets, blending, state machines, locomotion, root motion, IK |
| [systems.md](systems.md) | AI, spawn and world, items and progression, UI, production words |

## Columns

| Column | Meaning |
|---|---|
| Use | The word to write. Several words separated by commas are all acceptable; pick by context. |
| Avoid | Surface forms to replace. Comma-separated. A plain form matches only when no Hangul syllable is right before it, so 쓴다 does not match 덮어쓴다. A plain form also matches as a prefix, so write stems (돌려주 matches 돌려주고 and 돌려주므로). A form written as `` `re:...` `` is a Python regex; write a pipe inside it as `\|`. `—` means nothing to avoid. |
| Kind | `replace`: almost always wrong in a code comment or tech doc. `review`: often an AI habit, but correct in some contexts; read the sentence. `density`: fine once, a problem when it repeats; the lint counts it per file and lists the lines only with `--kind density`. `term`: reference only, not linted. In a `term` row, Avoid names words to avoid in that sense; the lint skips them because they are correct in other senses. |
| Evidence | Where the choice comes from. See below. |
| Note | When the row does not apply, and how to choose between the Use words. |

## Evidence

Counts are the number of comments (or document lines) that contain the form, per 1,000. Snapshot taken 2026-11-04.

| Code | Corpus |
|---|---|
| A | Korean comments in the C++ source of a commercial Unreal Engine 5 game, written by people. About 6,600 comments. Not public; do not quote its comments in shared files. |
| K | Korean comments in an Unreal Engine 5 project written mostly by AI agents. About 7,400 comments. This is the comparison group: it shows what AI-written Korean looks like. `K docs` means that project's Markdown documents (about 78,000 Korean lines). |
| D | Korean design documents about an animation system, written by a game team. About 500 Korean lines. |
| O | Korean comments in public game projects by Korean developers, at their last commit before 2022-01-01 (written before AI coding tools were common): planetarium/NineChronicles (377), G0DCH/Unity-HexaTile-CasualStrategy (619), ncsoft/Unreal.js and Unreal.js-core (5). 1,001 comments, mostly Unity C#. gorisanson/pikachu-volleyball, pikachu-volleyball-p2p-online and utilForever/RosettaStone have English comments and gave only README lines. |
| raw | Total occurrences instead of a per-1,000 rate. |
| common | Common in Korean game teams but not measured in A or D. Check the team's usage before you enforce it. |
| UE | Matches the spelling of the Korean Unreal Engine documentation, from memory. Not cross-checked in this snapshot. |
| style | A style decision of this skill, not a corpus count: engine type names stay in English in Korean text (2026-11-06). The counts next to it show what people write. |
| W | 유영경, 『개발자를 위한 글쓰기 가이드』(로드북, 2021), a Korean technical writing guide; `§nn` is its principle number. A style source, not a corpus count. |
| KR | Listed in the retired ko-review checker (claude-plugins, removed 2026-11-03), which recorded forms it had seen in AI-written docs. K counts for these are low because that checker already removed most of them from the comparison project; A shows whether people use the form. |

Example: `A 0.3 / K 78` means 0.3 of every 1,000 human comments and 78 of every 1,000 AI comments contain the form.

### Cross-check with O

O is a second, independent set of human comments (different teams, Unity instead of Unreal). It confirms the main rows:

| Form | A | O | K |
|---|---|---|---|
| 쓴다 and its forms | 0.9 | 2 | 121 |
| 돌려주다 | 0.3 | 0 | 25 |
| 고르다 | 0.3 | 3 | 35 |
| 바꾸다 | 2.7 | 7 | 63 |
| 남긴다 | 0 | 0 | 30 |
| 켜다, 끄다 | 2.3 | 0 | 32 |
| 시각 | 0 | 0 | 37 |
| ~한 뒤 | 2.1 | 1 | 62 |
| 대상 | 12 | 6 | 106 |
| · | 0 | 0 | 103 |
| ~므로 | 18 | 1 | 200 |
| 반환, 리턴 | 15 | 15 | 46 |
| 변경 | 35 | 34 | 21 |

Where O disagrees with A, the rows were relaxed: 갱신 (O 16) is no longer flagged, 구독 (O 4, Rx and MVVM) became `review`, and 세팅 and 체크 stay `term` because O uses them less (8 and 3) than A (38 and 58).

## Spelling policy

1. A term the team uses every day wins over the standard Korean spelling when they differ. Example: 타겟, not 타깃 (A 43 / 0.8).
2. Where the team is split, use the standard spelling. Example: 대미지 over 데미지, 메시지 over 메세지.
3. Where A and the UE documentation differ and neither dominates, pick one per project and record it in the project terms file. Example: 에셋 or 애셋.
4. Class, function, property, tag and asset names stay in English exactly as in code. Engine type names (Actor, Component, Mesh, Tick) stay in English in prose too; see [../style/comments.md](../style/comments.md#words). A Korean loanword is for concepts and actions (콜리전, 스폰).

## Project terms file

A project can add rows and silence built-in rows. Create `.claude/ko-gamedev/terms.md` in the project root. The lint loads it automatically when run from the project root, or with `--terms <file>`.

```markdown
# Project terms

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 락온 | 하드락 | replace | team | This project calls the player's explicit lock 락온. |
| 애셋 | 에셋 | replace | team | Follows the UE Korean docs. |

| Allow | Note |
|---|---|
| 전이 | The action graph defines 전이 as its own term. |
```

The project file wins over this glossary when they conflict. `Allow` forms are never reported, even when a built-in row matches inside them.

## Adding a row

- Add a row only with evidence: a corpus count, a team decision, or a UE documentation spelling. Write the evidence code.
- Prefer `review` unless you have seen the form be wrong in every sentence you checked.
- Keep forms narrow. A form that matches inside common words floods the lint; use `re:` with a lookahead, as 시각 does in core.md.
- A suffix such as 므로 always follows a Hangul syllable, so a plain form never matches it. Use `re:(?<=[가-힣])므로`.
- After a change, run the lint on a folder you know (an AI-written one and a human-written one) and compare the totals.
- Do not copy comments from corpus A into this folder. Write your own examples.
