# Step 4: Write the script

Convert the approved scene cards into script lines in the project's format. The grammar, the line kinds, and the lines the project's checker cannot catch are in the format file (`.claude/story/format.md`, sections `Line kinds` and `Blind spots`). Read it before you write.

## Order

1. Write the spoken lines first. Use the verbs in the card's "speakers and wants" so the characters push and pull.
2. Add narration, stage commands (background, enter, exit, pose), choices, and variables in the format's syntax.
3. Split and trim. Split boxes to the length rule, then cut about 10% of the draft's boxes. Cut first the lines whose removal keeps the information, the emotion, and the clues.
4. Update the project's data files (speaker list, variable defaults) and write the list of image ids the script uses. The format file's `Data files` says which files.
5. Go to step 5.

## Box length

- Rule: 1–2 sentences per box, 40 characters or fewer recommended, split above 60. The format file's `Box` section may set other numbers for its UI; it wins.
- Evidence: in Korean TV drama scripts (나의 아저씨 1–16화, 미생 1화와 7–20화) one spoken turn has a median of 15–19 characters; 76–85% of turns are 1–2 sentences, about 80% are 40 characters or fewer, and 88–94% are 60 or fewer. Later, more emotional episodes keep the median and grow only the long tail (90th percentile 47–57 in the first episodes, 60–70 later). Film screenplays (친절한 금자씨, 박쥐) break lines at breath units; one such line has a median of 20 and a 90th percentile of 32–34 (sources.md "Dialogue analysis").
- Three or more sentences from one speaker in a row: only for a tirade, a revelation, or a drunken scene. Even then, split them into boxes of 1–2 sentences.
- Split points: a breath, the other person's reaction, a glance or an action line. Splitting one speaker into two boxes creates a pause; in the drama scripts 12–15% of turns continue the same speaker.
- Split long monologues by box too. If one character speaks 3 or more boxes in a row, check whether a reaction or action can go between them. After a long line, the other side's short reply (silence, or 4 characters or fewer) is normal.

## Dialogue

- Exchanges where every question gets an exact answer are dull. In real scripts, 17–29% of replies right after a question are counter-questions, and in TV scripts 35–47% of replies right after a question are 6 characters or fewer (counted over all turns, only about 21% are that short). Counter-questions plus silence or trailing off make 36–53% of replies to a question. Twist 1 or more of every 3 question–answer pairs: counter-question, short answer, silence, topic change, or answering with an action. Keep twisted replies to 3 in a row or fewer.
- Key lines: short (about 10–15 characters), everyday words, with a silent or reaction box before or after. No narration that stresses them, no emotion words around them. The situation gives the line its weight.
- A mentor or senior who only comforts rings false. Mix in one line of reality.
- Lines from research (something a person in that job actually said) beat generic lines. A stock phrase reads as false at once.
- Silence is not an empty box. Write it as `……` from the speaker, a one-word reply, or one action line.
- Follow the character sheet for speech: length tendency, register, verbal tics, the address table for each listener. Keep titles and forms of address that show rank.
- Suggest dialect and nonstandard spelling with a few words only. Limit a minor character to 1–2 turns.
- Do not put words that describe the tone in the line ("화난 목소리로"). The speaker label and the pose do that.
- Do not write moral lines that state the theme, except the key line at the climax.
- Numbers: write times, minutes, distances, money, floors, and room numbers in Arabic numerals in both lines and narration ("9시 4분", "8분", "3층 302호"). Keep counts of times and people in native Korean (스무 번, 세 분). Times written in Korean words were hard to read in the playtest.
- Guide text: text that is not a character's action, line, or thought (how to use a screen, a goal reminder) goes to a separate guide speaker id in the speaker list, so the screen can show it in its own color. Do not write it as narration in parentheses like "(안내)". The playtester asked for guide text to look different from narration, lines, and inner voice.

## Emotion

- Order of expression: the line's tone → pose or expression → one action line → inner voice.
- Do not name emotions in narration (슬펐다, 화가 났다, 불안했다). Do not explain again in narration an emotion that the line or the pose already showed.
- In first-person narration, do not describe your own face from outside. Write a body sensation instead: "손끝이 차가워졌다", not "얼굴이 하얗게 질렸다". Do not assert another character's thoughts; write visible signs or a guess.
- Cut first-person filter verbs (느꼈다, 보였다, 생각했다, 깨달았다) by writing what was perceived directly.
- Outside emotional peaks, short summary narration is fine. Showing is for key scenes and emotional peaks.
- When first-person listing narration reveals what happened before the story without a flashback, keep the list to facts and move judgment and guesses into the inner voice.

## Example

One scene card converted, in the default format (format-template.md). The skill wrote this example; it is not from a book. Real ids come from the project's speaker list and image folders.

```text
~ shop_visit
# 의도: 의뢰인이 숨기는 것이 있다 | 목표: 경위 듣기 / 결과: 진술에 빈칸이 생김
do Stage.bg("bg_shop_night")
셔터가 반쯤 내려진 가게 안에 형광등 하나만 켜져 있다.
do Stage.enter("client", "neutral", "right")
client: 오셨어요? 문 닫으려던 참인데.
hero: 전화로 말씀하신 장부, 보여 주시죠.
client: ……그게, 찾아봐야 해서요. [#pose=nervous]
client: 차라도 드릴까요?
- 장부부터 찾아 달라고 한다
	set pressed_client = true
	client: 지금요? 아, 네. 잠깐만요.
- 차를 받는다
	client: 금방 끓일게요. [#pose=smile]
	그가 등을 돌린 사이, 계산대 아래 서랍이 반쯤 열려 있다.
=> shop_ledger
```

This example needs a `pressed_client` default of `false` in the variable file, and the images `bg_shop_night`, `client/neutral`, `nervous`, `smile`.

## Data files

- Speaker list: every speaker id with its display name. Use the format's id rule (lowercase English, digits, underscore by default).
- Variable defaults: every variable the script sets or tests. Name flags so the meaning shows (`heard_testimony_a`, `trust_client`).
- Image id list: backgrounds and character poses, split into "existing" and "new". Handle new ids with the format file's placeholder rule.

## Bad and fixed examples

Common mistakes are in [../examples/lines.md](../examples/lines.md).
