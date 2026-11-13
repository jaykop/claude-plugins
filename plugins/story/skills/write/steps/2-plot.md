# Step 2: Plot

Write the scene list and the setting and clue reveal table. This step fixes cause and effect between scenes and the order of information before any line. Output: `plot.md` in the story docs folder (mystery clues go in `clues.md`).

## Order

1. Three-point preplan: decide the last scene, then the key scene, then the first scene, then the middle.
   - Pick one of 5 last-scene types: inner change, wider understanding, twist, return (overlaps the first scene with a different meaning), open.
   - The key scene is where a choice or an accusation happens. The last-scene type decides it (inner change: the event that causes the change; twist: the scene that betrays the prediction).
   - Pick one of 9 first-scene types. Welcoming types: setting, daily life, character, flashback, whole-story compression. Pulling types: incident, habitual action, contrasting symbol, question. A 5-minute scene and a mystery start from incident or question. Do not start with a flashback.
   - What the first scene shows (an odd detail, a prop, a question) is paid off at the end. If it is not paid off, cut it.
2. Lay out the skeleton ("Skeleton").
3. Write the scene list table and check the causes.
4. Write the setting and clue reveal table.
5. Design the branches and count the paths.

## Skeleton

Lay out one 5-minute scene with the four opening points.

| Point | Content | Share of boxes (estimate) |
|---|---|---|
| Daily life | Short. The protagonist's small goal and usual self. 8 boxes or fewer | 15% |
| Upheaval | An event that shakes the protagonist's world. It happens in front of the player (not reported, not a flashback). Inside the first 20–30% | 20% |
| Reaction and refusal | The protagonist's emotional reaction and hesitation. Put the first choice here. A reaction true to character that backfires is good | 35% |
| Point of no return | The protagonist chooses, and cannot go back to before the event. Record it in a variable | 30% |

The shares are estimates, not from the books. A 5-minute mystery uses the "request → inquiry → impasse → truth" skeleton in [../reference/genre-mystery.md](../reference/genre-mystery.md). It has 2 suspects (+1 witness) by default, with a "suspicion deepens" beat for each suspect in the scene list ("Structure" in the same file).

A full story uses 4 turning points: point of no return (about 1/4), renewed resolve (middle), darkest moment (about 3/4), victory (ending). Each turning point's result is the next one's cause.

A story with more than one timeline or viewpoint follows the pattern's skeleton in [../reference/structures.md](../reference/structures.md). Write which timeline or viewpoint each scene belongs to in the scene list.

## Scene list

```markdown
| # | 장면 id | 장면 한 줄 | 앞 장면과의 연결 | 강도(1~10) | 새 정보 |
|---|---|---|---|---|---|
| 1 | start | <동사 2개 이상의 행동 문장> | - | 3 | <무엇이 새로 드러나는가> |
| 2 | <id> | | 그리하여 / 하지만 | | |
```

- Write the scene line as action ("찾아가서 추궁한다"), not a state ("깨닫는다", "고민한다").
- Write the link only as 그리하여 (so) or 하지만 (but). If scenes link only by 그리고 (and), the cause is broken. Redesign or merge the scenes.
- If "new information" is empty, cut the scene or merge it into another.
- Intensity: mostly starts low and rises. Change one if three scenes in a row have the same intensity. 10 appears once or twice per story.
- Side-branch test: does the scene or investigation point (1) affect the ending, (2) serve a main character's change, or (3) reveal a new fact? If none, cut it.
- Check that each scene moves one step toward the central question (a new clue, a contradiction, a change in a relationship).

## Setting and clue reveal table

```markdown
| id | 내용 | 등급 | 공개 장면 | 노출 방식 | 재노출 장면 | 회수 장면 | 해결에 사용 |
|---|---|---|---|---|---|---|---|
| set_xxx | <설정> | 필수 / 중요 / 장식 | <장면 id> | 갈등 대사 / 인물 약점 / 소품, 배경(필수면 대사창 텍스트도) | <장면 id 또는 -> | <장면 id 또는 -> | Y / N |
```

- Grade every item. Essential (필수): missing it, the player cannot follow the next scene or the resolution. Important (중요): needed to understand relationships and feelings. Decoration (장식): the story holds without it.
- Essential information is written in box text at least once; an image, a pose, or a prop alone is not enough, because the player's eyes are on the text box. Show it at least twice, in different scenes or forms. Put the second showing at the nearest decision point that needs it (just before a choice, before the resolution, at a chapter start), not right after the first in the same scene. Warn when an essential row has no re-exposure scene.
- If a side scene reveals something the resolution uses, show it again in a main-path scene. Players skip side content.
- Keep the order things happened and the order they are revealed apart. When the plot reveals out of time order, write a timeline of events once and give each difference from it a one-line purpose.
- By default, a setting not used in the resolution stays out of the script. If the writer wants it anyway, attach it to an emotional beat in one line.
- Reveal 2 new settings or fewer in a 5-minute scene. Move the rest to later scenes.
- Do not reveal a setting as plain explanation. Use one of three disguises: an argument where interests clash, a question from a character who does not know, a prop or the background.
- Curiosity peaks when the player knows part of the whole. Keep 2 or more open questions and 1 or more closed questions at the end of each scene.
- Record foreshadowing as a pair: reveal and payoff. Warn if one side is missing.

## Branches

- Branches split briefly and rejoin the main line. Each choice needs an immediate reaction, but the whole scene does not need to split.
- Record a choice whose outcome differs in a variable, and reflect it later with a condition or a conditional choice.
- Paths multiply: 8 two-way choices in a row make 256 paths. Stay under the format file's path limit; paths beyond it are never checked. Rejoin choices with the same play result at once to cut paths.
- With several endings, give each ending a last-scene type.
- Decide how wrong answers work first.
  - Rebuttal then continue: a wrong answer also hears a rebuttal and moves on. Paths multiply by the number of choices (7 choices made 128 paths in the tested work).
  - Choose again: record the wrong choice in a variable, hide it with a condition, and return to the same question. If it is not hidden, the path never ends.

## Check

- Are the last-scene type and the key scene decided?
- Does the upheaval happen in front of the player inside the first 20–30%?
- Is every scene link 그리하여 or 하지만?
- Are all settings and clues used in the resolution revealed in scenes before the resolution?
- Does every essential item have a re-exposure scene?
- At the end of each scene, is there at least one fact the player knows, one the player can only guess at, and one the player does not know? No guesses means no curiosity; only known facts means over-explanation.
