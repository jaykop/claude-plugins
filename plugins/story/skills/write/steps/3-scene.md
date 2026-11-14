# Step 3: Scene cards

Write a card for each scene in the scene list. The card is the blueprint just before the lines. Step 4 converts cards into lines. Output: `scenes.md` in the story docs folder.

## Scene card

```markdown
### <장면 id>

- 유형: <아래 장면 유형 중 하나> / 기능: 행동 | 반응 | 설정 | 심화
- 극적 의문: <이 장면이 묻는 것 하나. 장면 안에서 제기 → 숙고 → 답 순서로 다룬다>
- 의도: 이 장면은 <무엇을 보여 주거나 변경하기> 위해 있다
- 시작 상태 → 끝 상태: <두 문장이 달라야 한다>
- 목표 / 장애물 / 결과: <누구의 목표인가, 무엇이 막는가(다른 인물, 내적 결함, 환경), 결과(대개 실패하거나 더 큰 곤경)>
- 앞 장면에서 이어지는 원인: <한 줄>
- 새 정보: <비면 삭제 후보>
- 화자와 원하는 것: <id>: <능동 동사(떠보다, 숨기다, 몰아세우다, 달래다)> / <id>: <다른 동사>
- 사건에 대한 반응: <id>: <반응 동사(감내하다, 버티다, 헤매다)> / <id>: <다른 동사>. 같은 사건에 두 인물이 같은 동사로 반응하면 하나를 바꾼다. 차이는 각자 아는 것에서 나온다
- 이 인물에게 왜 큰일인가: <사건이 작아도 당사자에게 큰일인 이유 한 줄. 규모를 키우지 않고 초점을 좁힌다>
- 첫 층 한 줄: <누가 무엇을 원하고 지금 무엇을 하는지, 누가 막는지. 대사만 읽어도 이 줄이 서야 한다>
- 필수 정보: <등급이 필수인 항목과 그것이 나오는 대사창 위치>
- 서브텍스트(둘째 층): 사건 / 속뜻 / 전달 수단(포즈, 행동 지문, 소품, 반복되는 사물, 선택지 문구의 어긋남)
- 반복 모티프: <소품, 색, 장소 중 하나. 나올 때마다 맥락이 바뀐다. 없으면 없음>
- 첫 줄 유형: <아래 목록>
- 끝 줄 유형: <아래 목록>
- 선택지: <위치, 걸린 가치, 선택별 즉시 반응, 합류 장면 id>
- 배경 id / 그림 id: <기존 id 우선. 새 id는 표시>
- 대사창 예산: <N>
```

Scene types (15): opening, situation, conversation, urgency, escape, chase, crisis, realization, reversal, reflection, renewed resolve, transition, resolution, climax, final. Do not use the same type 3 times in a row. Mystery mapping: hearing testimony = conversation, finding a contradiction = realization or reversal, wrong-answer penalty = crisis, moving to a new place = transition.

## First lines of a scene

- Do not start with explanatory narration. Start with an incident, an action, a question, or an odd detail.
- Within the first 5 lines, show 2 or more of: speaker, place, situation. Handle the place with the format's background command and one narration line.
- Do not start by waking from a dream, an alarm, or getting up (except when the dream ties directly into the story).
- Write 3 first-line candidates, each with "the question the player will have". Drop a candidate that raises no question.
- In the opening scene, put something that breaks daily life within the first 5 lines.

## Inside the scene

- Go goal → obstacle → result. Fail the easiest attempt first and raise the intensity.
- If 20 or more boxes pass without tension, add a small obstacle (a phone call, someone cutting in, a sound, a discovery). It works best when the player knows before the character does.
- Redesign a scene where allies only talk without any friction. Give them at least a small disagreement or something hidden.
- Before a choice, put a reaction beat: emotion → analysis → decision. 1–3 lines are enough. The beat makes the player accept the choice.
- In the scene with the strongest emotion, stop the roundabout talk and have the character say the core once, exactly. Before that, talk around it: change the topic, answer with a question, blame the past.
- An emotional peak takes one of two shapes. (a) Short turns: one side speaks in short lines, the other answers with short replies, silence, and actions; the scene ends on a look or a gesture, not an explanation. (b) A long speech: one character talks at length, the other answers each part with silence or 4 characters or fewer. In Korean drama scripts, a reply right after a turn over 80 characters is silence or 4 characters or fewer 36–45% of the time, against 28–34% after a turn of 20 or fewer.
- Just before a peak, 3–5 callback boxes can replay earlier lines one at a time (in a VN, lines the player chose or heard), then the peak line. The callbacks build the feeling's ground on the spot.
- A long meeting, presentation, or confrontation scene: split it in two with a narration box between.
- If a recap scene is needed, have two characters with different opinions recap by rebutting each other.
- If the game has no screen to review past testimony and clues (a dialogue log, a notebook), put a recap beat (2–3 boxes, two characters who disagree, rebuttal form) right before the resolution or accusation round. In the tested work, players could not see testimony, places, and room numbers again and got confused.
- Show spatial information (who is on which floor and room, who saw what where) 2 or more times if the resolution uses it.

## Last lines of a scene

Last-line types: just before a key decision, just after something terrible, an ominous sign, a revealed secret, an unanswered question, a shocking statement, a new character arrives.

- End by pulling into the next scene, not by resolving. But cutting every scene on a crisis dulls the player. Use a strong ending in 1–2 of every 3 scenes.
- Do not follow a shocking line with a line that explains the emotion. One action line, or a direct scene change, is fine.
- Do not end on a goodbye ("다음에 봐").
- End a chapter on narration: an action, a look, a view. In Korean drama scripts 21 of 22 episode endings were narration, more than scene endings (about half).
- A chapter can open by replaying the last moment of the previous chapter in a few boxes. It brings back a player who paused.
- Designing the first and last image as a pair gives a return ending (the same place looks different).

## Choices

- Two or more options stake different values (loyalty and truth, survival and protection). At least once per story, give a dilemma where both options cost something.
- Each option gets 1–2 boxes of immediate reaction. An option with no reaction is a defect.
- After a decisive choice (naming the culprit), ask once for confirmation or withdrawal.
- Every question has at least 1 option with no condition.
- Write option text as something the protagonist would actually say or do, short. Differences in character (bold, careful, evasive) show, but every option is still in character.
- One option may postpone action. Show the cost of postponing in the reaction.
- Record the outer reward (a clue, affection) and the inner meaning (the protagonist's change of attitude) of each option separately.

## Information

Two layers. The first layer is what the player must follow: what the protagonist wants, what they are doing now, who is in the way. The second layer is foreshadowing, hidden settings, subtext, and wider meaning. The story must stand when the second layer is missed. Clues the resolution uses belong to the first layer.

- Do not write lines whose purpose is to recite, for the player, what both characters know. Instead: a character who does not know asks, an argument where interests clash carries it, a prop or the background shows it, or it waits.
- A restatement is fine when the character has a purpose of their own: to rebut, confirm, correct a misunderstanding, make an excuse, threaten, doubt. The player who missed it the first time catches up. Judge twice: does the speaker have a reason to say it to this listener now (the character layer), and does the player have this information yet (the player layer)?
- In a VN, the text box carries most of the information. A prop or the background can carry important or decorative information, not essential information. Essential information goes in box text, disguised as a conflict line, a question from someone who does not know, or a rebuttal recap.
- If setting explanation runs for more than 2 lines, it is a lump. Break it into events or reactions.
- Reveal a character's past only as much as the current scene needs, briefly, over several times.
- Return line: at a chapter start, right after a scene change, and right after a long choice, let one line show what the protagonist is trying to do now. It is a muttered plan, a plan said aloud, or someone's checking question, not a recital. Players come back from a pause, from auto mode, or days later.
- A silence or a one-line reaction is easy to skip. Plant its reason in the line before, so the silence raises a question, and let the line after answer it or twist it.
- A character does not explain the meaning of their own symbol. Leave the object's name and the reactions; cut the explanation.

## Human checkpoint

Write a plain summary of the scene list (one or two sentences per scene: who does what, and why) and run the cold read on it ([../reference/cold-read.md](../reference/cold-read.md)). Then present the summary as [../reference/presenting.md](../reference/presenting.md) says, point to the scene cards in the file, and stop. In the short mode, the presentation starts from the world order, the crack, and the cast, and includes the concept.
