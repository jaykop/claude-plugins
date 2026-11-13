# Genre: Mystery

For detective, crime, and mysteries mixed with ghost stories. Read it from step 1. Sources are in [sources.md](sources.md) under "Mystery".

## The genre's promise

- What it promises the player: the case has one truth, and every clue needed to solve it was in front of the player.
- Success: the player feels "I saw it but did not know what it meant", not "I never saw it".

Reader expectations by subgenre (pick one for the concept sheet's genre field):

| Subgenre | Expectation |
|---|---|
| Classic puzzle (본격) | A logic game. Closed space, a situation that looks impossible, fair clues |
| Social (사회파) | Motive and social background. The culprit's situation ties to a social problem |
| Cozy (코지) | Everyday cases, humor, character-driven. Little violence |
| Narrative trick (서술 트릭) | A deception only text can do. A VN has narration, so it is possible, but writing a lie in narration is cheating |
| Thriller | Pursuit and a deadline after the crime. The deadline must hold logically. Tension rises when the player knows a danger the protagonist does not (shown through narration or another character's scene). The object everyone chases can stay vague (a MacGuffin); hang the scenes on the chasers and the clock. A MacGuffin is never a clue the solution needs |

## Fairness

Four rules of fair play:

1. Show the player every clue needed for the solution before the solution.
2. The culprit appears early. A character who first appears late cannot be the culprit.
3. What the detective (or protagonist) learns also appears on the player's screen. Skipping the observation and stating only the result breaks the rule.
4. Do not build a twist on a hidden clue. Show the clue early and hide only its meaning.

Seven cheats (use as questions after the draft):

1. Contradiction: did you reverse an established fact for the story's convenience?
2. Ignoring the obvious question: did you skip, with no explanation, the "why did they do that?" the player will ask?
3. Ignoring logic: did a character do something they could not, because the plot needed it?
4. Misused red herring: did a person or object appear and vanish with no explanation?
5. Coincidence: is the case solved by too much coincidence? Use coincidence only as bad luck for the protagonist or good luck for the antagonist.
6. Acting for the reader: does a character keep up an act to fool the player even when alone? Narration in a scene where the character is alone must not contradict what that character knows.
7. Stale devices: a confession for no reason, a gun that jams, a secret passage first mentioned at the end.

First-person narrator rule: hiding from the player a clue the narrator knows is cheating. Build twists only from information the narrator did not have.

## Case design

1. Order of composing the crime: what kind of crime → the victim (why targeted) → relation to the culprit → motive (money, love, jealousy, revenge, social pressure) → the trick or alibi. The trick comes from the motive and the relation. Decide the weight of the incident (does the harm reach life, body, relationships, livelihood?) and record it in the concept sheet. A small theft made weak tension in a 5-minute scene (tested work).
2. Write a movement timeline for each suspect first. It is the raw data for contradictions in testimony.
3. Suspect sheet (added to the character sheet): surface motive / real motive / hidden past / lying habit (lines get shorter, answers a question with a question) / 2 clues that reveal the motive.
4. Culprit sheet (added): first appearance / cover image (friendly, helpless, authoritative) / reaction when accused (denial, keeping dignity, acceptance, silence) / self-defense logic / social background of the motive.
5. If there is a supernatural rule, fix it in 3 lines or fewer, and make every rule the deduction uses known to the player in advance.

## Clue card

```markdown
| id | 겉모습 | 숨은 의미 | 노출 방식 | 노출 문맥 | 노출 장면 | 회수 장면 | 오도 방향 | 플레이어가 볼 수 있었나 |
|---|---|---|---|---|---|---|---|---|
| clue_xxx | | | 대사 / 묘사 / 물건 / 부재 | 불평 / 농담 / 열거 / 감정 / 다툼 | | | | Y |
```

How to expose clues:

- Show the action, hide the meaning. The detective examining something is visible, but the reason stays unsaid until the solution.
- Put a decisive clue as one line among complaints, jokes, lists, or emotional lines. Do not stress it in narration. But do not bury it in an oversized lump of information.
- Expose the same clue 2 or more times in different contexts and flip its meaning at the end. It is fair and surprising.
- An absence clue (something that should be there and is not) goes in one inconspicuous narration line.
- An object too familiar to suspect is a good hiding place.
- Write values used in contradictions (time, quantity, position) as concrete values, not vague adverbs.

## Testimony card

```markdown
| 증인 | 한 말 | 확신도 | 유리한 해석 / 불리한 해석 | 말하지 않은 것 | 충돌하는 증거 |
|---|---|---|---|---|---|
| <id> | <요약> | 분명 / 기억 흐림 / 침묵 | | | clue_xxx |
```

Forms that become a "point out the contradiction" mechanic:

1. Direct lie: testimony and evidence clash head-on.
2. Two readings: the same testimony reads in the suspect's favor or against.
3. What was not said: a gap in the testimony. The gap itself is the target.
4. The use of a useless-looking object: an object or rule that looks meaningless was used in the crime. Add one box that asks "who benefits?"
5. Physical clash: position, time, distance do not fit.
6. Trap question: a question to watch the suspect's reaction. The reaction is the clue.

Rules for testimony scenes: plant the seed of the contradiction in chatter, then confirm it with repeated questions. A lying witness's text stays plausible; leak only 1–2 signals through the lying habit and pose. Do not make the player judge from the face alone. Signals have other causes too, so tie them to a line or a circumstance.

## Structure

Ten stages of a detective story: prologue → daily life → request → inquiry → impasse → consultation → adventure → truth → flashback (the culprit's story) → epilogue. Use it for the structure of a full story and for scene ids.

A 5-minute scene compresses to 4 parts.

| Part | Content | Share of boxes (estimate) |
|---|---|---|
| Request | Open with a strange situation in 3 steps (daily life → ordinary reaction → a fact that overturns it). No choices | 15–20% |
| Inquiry | Testimony and clues. One choice of where to investigate | 25–30% |
| Impasse | A contradiction found, the misdirection collapses, time or penalty pressure | 10–15% |
| Truth | 3–4 rounds of the player's accusations, the culprit's reaction and motive, a short aftertaste | about 40% |

Candidate numbers for a 5-minute scene (estimated from example works, adjusted by the playtest of the tested work): 50–75 boxes, 4–5 scenes, 3 decisive clues and 1–2 misdirections, 2 suspects or fewer (+1 witness).

- Three suspects in 5 minutes leave each with one statement and one accusation, and suspicion stays shallow (tested work). Give each suspect one "suspicion deepens" beat: one damaging piece of evidence + one line that presses them, or the suspect turning suspicion back on the protagonist.
- The ending choice (confirmation after the decisive accusation, and the ending branch) belongs to the truth part. With it, the truth part can approach 50%. If the truth part runs long, do not cut accusation rounds; cut repeated testimony in the inquiry.

## Resolution scene

Resolution round table:

```markdown
| 라운드 | 지적 대상(증언 또는 상황) | 필요한 증거 id | 오답 시 반론 | 정답 시 범인 반응 |
|---|---|---|---|---|
| 1 | | | | |
```

- Split rounds as accusation → rebuttal → correction. Not a detective's solo monologue. Every round has a point where the player judges.
- The culprit is present in the resolution scene and carries the reaction (denial, dignity, acceptance, silence) and the confession of motive. Confessing the moment evidence appears is a cliché. Give at least one rebuttal.
- A wrong-answer penalty is not just "wrong"; it is a reaction where a character's expectation breaks and their character shows.
- The culprit's motive makes the player feel sympathy and judgment at once. Social pressure or an unrecognized situation works well.
- After the decisive accusation, ask for confirmation once.
- If there is no screen to review past testimony and positions (a dialogue log, a notebook), always put a recap beat (2–3 boxes, two characters who disagree, rebuttal form) right before the resolution rounds (step 3 "Inside the scene").
- Keep the aftertaste short (3–6 boxes). Do not pile on explanation after the solution.

## Supernatural elements and a single truth

For mysteries mixed with folktales, ghost stories, or the supernatural. Attach a supernatural sheet to the concept sheet.

```markdown
- 괴이 규칙(3줄 이내):
- 역할: 분위기 / 힌트 제공 / 정체 폭로 / 해결 개입 중 하나
- 해결에 사용: Y / N (Y면 공개 장면과 방식)
- 잔여 현상: 해결에서 설명하지 않고 남길 현상 1개 (없으면 없음)
```

1. Pick one role. A single-truth mystery allows only the hint role. Intervening in the solution cancels the deduction.
2. A hint-role phenomenon gives direction only; the protagonist judges. Close the solution's evidence with physical evidence from the human world.
3. Show any supernatural rule the solution needs within the first 20%, through lines or events (rule shown → broken → oddity sensed).
4. Expose observation conditions (who, where, from which direction, in what light) with any phenomenon that looks supernatural. Then the solution can rebuild it as a human act.
5. Close the case's "who and how" as a single truth, and leave the supernatural only one doubt in the aftertaste. Put that doubt in the last 1–2 lines and do not use it in the logic that names the culprit.
6. One line where the detective limits the conclusion to "an interpretation based on the phenomena" is allowed. The ending treats the rational interpretation as correct.
7. "I saw a ghost" testimony is only atmosphere, not an evidence card, unless split into conditions like position, time, and light.
8. Do not pack folk settings into the first 5–8 boxes. Reveal them 3 or more times through ritual scenes, conflict lines, and places. Put explanatory lines in a context where a character scolds or argues.
9. On conflict: the case's who and how follow the single truth first; "why this place became like this" may stay unexplained.
10. If a supernatural rule decides how lines react (ears ringing at lies), compare every line the rule applies to with the rule. With two false sentences in one statement, the player cannot tell which one triggered it. If a core line that must be true is false, the solution collapses (step 5 pass A).

## Fairness checklist (step 5 pass A)

1. Did every clue the solution uses appear in a box at least once before the solution?
2. Did the culprit appear in an earlier scene?
3. Did what the detective learned at the scene appear on the player's screen?
4. Were clues that depend on outside knowledge only the detective has (a map, a record) given as evidence before the solution?
5. Is each decisive clue one line in a distracting context?
6. Is the misdirection one reasonable reading of the testimony?
7. Is testimony marked "not sure" actually checked against later evidence?
8. Is there no solution-intervening supernatural element?
9. Is there nothing that matches the 7 cheats?
10. Does one unresolved question remain at the end of the scene?
