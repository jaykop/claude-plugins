# Step 5: Self-review

Check the script in 5 passes and fix it. If a pass finds a defect, hold the later passes. Polishing sentences in a script whose structure does not stand wastes time. If pass A or B finds a defect, go back to the step 3 scene cards.

In the review-only mode, do not edit the script. Write the report only.

## Pass A: Structure

- Does every scene still show its event chain rows (step 1)? Did the script add an event, an attack, or a character with no row and no cause? Every action someone takes on screen has a want and a reason it happens now.
- Do opponents still act like capable people, or did a scene make one wait or blunder so the plot could go on?
- Do the card's goal, obstacle, result, new information, and start state → end state actually happen in the script?
- Do the concept sheet's goal, what can be lost, why now, and the weight of the incident appear in boxes of the first scene? If they are only in the concept sheet and not on screen, the player does not know them. In the tested work, "what can be lost" never appeared in a box, and the review missed it.
- Does every scene link hold as 그리하여 or 하지만?
- Are the odd detail, prop, and question shown in the first scene paid off at the end?
- Did every setting and clue used in the resolution appear on the player's screen (in a box) at least once before the resolution?
- Reread the concept sheet's question, answer, and "what this story will not do". Did the draft arrive where it meant to, and did any line drift into the story it should not be (a success sermon, a lecture)?
- Do supporting characters each bring a different feeling? Does anyone get moved around like a piece, for the plot's convenience?
- Mystery: check the fairness checklist and the 7 cheats in [../reference/genre-mystery.md](../reference/genre-mystery.md).
- Romance or faction: check the checklist at the end of the genre file.
- More than one timeline or viewpoint: check the pattern's questions in [../reference/structures.md](../reference/structures.md).
- An adaptation: check the review questions in [../reference/adaptation.md](../reference/adaptation.md).
- If a supernatural rule decides how lines react (e.g. ears ring when someone lies), find every line the rule applies to and compare it with the rule. Two false sentences in one statement, or a core line that must be true but is false, is a violation. The tested work found 6 violations this way.

## Pass B: Scenes

- First 5 lines: no start on explanatory narration; 2 or more of speaker, place, situation shown; a question raised.
- Last 3 lines: one of the last-line types; no line explaining the emotion after a shocking line; strong endings not back to back.
- Does every scene have conflict? Do allies have different intentions?
- Do two characters react to the same event with the same verb?
- Emotional peak: is it one of the two shapes in step 3 "Inside the scene"? Does it end on a look or an action, not an explanation? Does a character break their usual way of speaking for the first time here?
- Does each chapter end on narration?
- Choices: different values at stake; an immediate reaction for each option; a reaction beat (emotion → analysis → decision) just before; at least 1 option with no condition.
- Do 2 or more open questions remain at the end of each scene?
- Is there no stretch of 20 or more boxes without tension?

## Pass C: Dialogue

- Function tag: does each line do at least one of plot progress, new information, obstacle, tension, theme, character change, goal exposure, relationship and background? A line that does none is a cut candidate. Decide by "does the story still flow if this line is cut?"
- Explanatory lines: does this speaker have a reason inside the scene to tell this listener this now? If characters recite what both know, change it to one of the alternatives in step 3 "Information".
- Question and answer: are there no runs of pairs where each question gets an exact answer?
- Cover the speaker label: can you still tell who speaks? Record the ground as one of length, register, or form of address. If there is none, apply the character sheet's speech again.
- Shown, then said: does a line repeat what the narration, the pose, or the background has already shown? Cut one side by the information grade: for essential information keep the line, otherwise keep the showing.
- Does a character explain the meaning of their own symbol? Cut the explanation.
- Key lines: short, without stressing narration or emotion words around them?
- Does a line sound like something a person in that job or place would actually say, or like a generality?
- Three ways of reading. Read the script (1) in full, (2) spoken lines only, ignoring narration, poses, and backgrounds, (3) skimming: each scene's first box, last box, and choice texts only. Pass: in (2) you can tell what happened in each scene and every essential item appears; in (3) each scene's start and end states differ. Players skip, use auto mode, and come back after a break.
- Remove the second layer (subtext, foreshadowing) in your head. Can you still retell the plot correctly from the first layer?
- Does each scene leave the player one thing to work out alone? A scene where characters say everything secures understanding but leaves nothing to guess.
- 10 viewpoint violations (first person, limited third):
  1. Narrating what the viewpoint character cannot see or know
  2. Describing what the viewpoint character would not care about
  3. Narrating what the viewpoint character has not realized
  4. Describing one's own looks without a mirror
  5. Describing one's own face as if from outside
  6. Asserting another character's thoughts and intentions
  7. Calling someone by a description when the name is known ("안경 쓴 남자")
  8. Narrating an event before it happens
  9. Vocabulary that does not fit the viewpoint character
  10. The viewpoint character not clear at the top of the scene

### Lenses

For a full story or a revision after a playtest, also read once through each lens. Report only what the passes above did not already cover.

- Character: where does the character pay the biggest price for a choice, and does that choice happen as an action (a choice) or only in words? Is one thing about them left unexplained? Do they keep a rule of their own, and is there a moment it breaks?
- Space: do places and props do more than set the scene? Does a motif return with a changed meaning? Are characters paired with props or places? Does the mood ever contrast with the scene's feeling on purpose?
- Narrative: can the reason for showing events in this order be written in one sentence? Read again knowing the ending: does any earlier scene contradict it?
- Technique: who narrates, with what feeling, and what does that bias? Is a skipped stretch of time paid off later? Does each noticeable effect (branch style, screen effect) connect to the scene's meaning?

## Pass D: Sentences

Mark candidates with the lint, then judge each line. A hit is a candidate only. Keep it if it is the character's speech or an intended expression, and record why.

```
python "${CLAUDE_SKILL_DIR}/scripts/story_lint.py" <lint options from the format file> <script files>
```

Use `python3` if `python` is missing. The format file's `Lint options` gives the regexes for its line kinds; with no options the defaults fit the default format. The checks: emotion names and filter verbs in narration, double passive and translationese in spoken lines, narration, and choice text, clock times and minutes written in Korean words, boxes over the length limit, `: ` in narration, choice lines, and the distribution of narration endings (to see mixed tense).

Rules for judging:

- Cut test: cut adjectives, adverbs, conjunctions, "나는", and "것 같다" if the information, emotion, and clues survive. Keep them if something is lost. In spoken lines, "것 같다" can be evasion or a habit, so do not cut it automatically.
- Cut adverbs that explain emotion (쓸쓸하게, 화난 듯).
- Is the narration ending unified to the concept sheet's tense (per layer or thread when a structures.md pattern is used)?
- Are forms of address, proper nouns, and prop names spelled the same across scenes?
- No noun or ending repeated 3 or more times in 2–3 adjacent lines. Intended repetition (an interrogation) is an exception.
- A device sentence (the same sentence repeated as a signal, e.g. the same line every time a supernatural event happens) is exempt from the repetition check. Mark its first appearance with an intent comment (`# 의도: 장치 문장` in the default format) and keep it. Players named this repetition as the most memorable part of the tested work ([../examples/lines.md](../examples/lines.md) 11).
- Write times, amounts, and distances used in testimony and clues as values, not vague adverbs ("사흘 전에", not "꽤 전에"). Times, minutes, distances, money, floors, and rooms in Arabic numerals (step 4 "Dialogue").
- If the story has a period setting, no objects, words, or loanwords that did not exist then. Faction: also [../reference/genre-faction.md](../reference/genre-faction.md).
- Cut stock metaphors in narration. Stock phrases in spoken lines are fine if they are the character's speech.
- Clichés: mark candidates with [../reference/cliche-check.md](../reference/cliche-check.md) and judge each one: keep, change, or cut.
- Do not auto-correct inversion, intended repetition, or exceptions in sentence length. Record them as items for the human to judge.

## Pass E: Format

1. Search for the format's blind spots: the `Blind spots` table in the format file. The lint's `colon` and `choices` checks cover the common ones (a `: ` that splits narration into a speaker; a line that the format reads as a choice).
2. Then check:
   - Is every new variable in the variable defaults? Is every new speaker in the speaker list?
   - Does every new id in the image id list have an image file or a placeholder?
   - Is the number of branch paths under the format file's path limit?
   - Run the format file's `Checks` commands. If they cannot run where you are (wrong branch, no engine), record it in the report. Do not report it as passed.

## Report

Write it to `review-<scene id or file>.md` in the story docs folder, and give only 3–5 summary lines in the conversation.

```markdown
# 리뷰 리포트: <파일>

- 실행한 검사: <형식 파일 검사마다 이름과 결과(통과 / 오류 N개, 경로 검사면 경로 N개, 끝 도달 N개)>, story_lint <항목별 건수>
- 실행하지 못한 검사: <검사와 이유>

## 패스별 수정
| 패스 | 줄 | 수정 전 요약 | 수정 후 요약 | 이유 |
|---|---|---|---|---|

## 사람이 판단할 항목
| 줄 | 질문 |
|---|---|
| | 이 침묵이 너무 긴가 / 이 말투가 인물답나 / 이 반전이 공정한가 |

## 클리셰 판정
| 클리셰 | 줄 | 판정(유지 / 변형 / 삭제) | 이유 |
|---|---|---|---|

## 열린 질문(플레이어 관점)
- <장면 끝에서 플레이어가 궁금해할 것>
```

## After a human playtest

After a human plays it, ask these four and use the answers as input for the next revision: where it was confusing or dull, where they were most absorbed, how they would describe it to a friend in one line, and the most memorable line or scene.
