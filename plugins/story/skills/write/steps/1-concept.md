# Step 1: World, cause, and concept

Build the story from the world's order and the characters' wants. Twists, clues, and the logline come after the causes hold. A story whose events have no reason fails no matter how good the twist is. Output: `concept.md` (world, chain, logline, concept sheet) and `characters.md` in the story docs folder (format file `Paths`).

## Order

1. Take down the user's idea as given. Separate the genre, the length, the format (choices or not, endings), and the settings that are already decided.
2. Adapting a source (folktale, novel, webtoon, true events, an existing design doc): fill the adaptation sheet in [../reference/adaptation.md](../reference/adaptation.md) now. Read the source's earliest documents too; a later revision may contradict the original intent. Do not assume the human remembers the source, even one they wrote: everything you present takes its world, cast, and terms from what you write here, not from the source.
3. Write the world and the cause ("World and cause" below): world order → the crack → the cast → the event chain. No twist, clue, or logline yet.
4. Run the chain check on your own draft ("Chain check"). Then run the cold read in [../reference/cold-read.md](../reference/cold-read.md) on the pitch. Fix the chain until no blocking item is left.
5. Human checkpoint 1: present the world, the crack, the cast, and the story in time order as [../reference/presenting.md](../reference/presenting.md) says, with what the cold read still questions. Stop.
6. After approval:
   - If the genre or the user wants a twist, design it now ("Twist").
   - Mystery: write "Case design" in [../reference/genre-mystery.md](../reference/genre-mystery.md) from the chain. The culprit is one of the chain's actors and the crime is one of its events.
   - Romance or faction: read the genre file ([../reference/genre-romance.md](../reference/genre-romance.md), [../reference/genre-faction.md](../reference/genre-faction.md)). Each adds a design card.
   - Not a straight line in time (two timelines, a frame, the same event from two viewpoints): pick the pattern in [../reference/structures.md](../reference/structures.md). It changes the viewpoint declaration and step 2.
7. Write logline candidates from the chain ("Logline"). 3 by default, 1 if the user asks.
8. When the human picks a logline, fill the story part of the concept sheet and the core part of each character sheet.
9. Run the cold read again on the full pitch, twist included. Human checkpoint 2: present it as presenting.md says and stop.

In the short mode, steps 3–8 go in one pass, but the chain check and the cold read still run before the single checkpoint, and the presentation still starts from the world, the crack, and the cast.

## World and cause

Write this part at the top of `concept.md`. Use the format's language (Korean by default) for everything you write into it.

### World order

Write how the groups and people live off each other before anything goes wrong.

```markdown
| 무리 또는 인물 | 누구에게서 무엇을 얻나 | 그 대가로 무엇을 주나 | 이 질서가 깨지면 잃는 것 |
|---|---|---|---|
```

- Write it as an exchange. Every row gets something and gives something.
- Groups that depend on each other do not turn on each other unless what they get changes. The crack below is that change.
- Name the world's terms here (an organization, a code, a nickname) with one plain sentence each. Use them later only as defined.

### The crack (why now)

- One change in what someone gets, made by someone who wants something. Write the actor, what they want, and what they do. "갑자기", "어느 날" with no actor is not a crack. An accident or a disaster may only be the protagonist's bad luck, never what solves the story.
- Who gains and who loses from the crack, by name.
- Why now: the date or deadline, and what caused it.

### Cast

- Take only the people the chain needs. Each character causes, blocks, or is hit by at least one chain event. Cut anyone who does none, even a well-loved character from the source.
- One line each: who they are, what they want in this story, which chain rows they act in.

### Event chain

```markdown
| # | 언제 | 누가 | 무엇을 한다 | 원하는 것 | 왜 지금 | 왜 이 방법(더 쉬운 길은 왜 안 되나) | 결과(다음 사건의 원인) |
|---|---|---|---|---|---|---|---|
```

- Rows go in the order things happen, not the order the player learns them.
- Each row's result causes the next row or someone's reaction. If a row follows only by "그리고", a cause is missing.
- Opponents act like capable people. At each row ask what the opponent knows now and what the easiest, smartest move would be (evict, fire, call the police, hide the evidence, simply ask). Either they make that move, or the row says why they cannot.
- No row exists only to plant a clue, set up a twist, or bring a character on stage.
- The protagonist's own choices cause the turning rows. A protagonist who is only carried along is a defect.
- Size: 4–8 rows for a 5-minute scene, about 10–25 rows for a 2–3 hour story.

A worked example (world order, crack, cast, chain, twist, and a bad and a good pitch) is in [../examples/story-chain.md](../examples/story-chain.md).

### Chain check

Run this on your own draft before the cold read. Fix the chain, not the wording.

For every row:

- Who does it, what do they want, why now, why this way? Is each answer written in the row?
- What do the other parties do in response? Is that in a later row, or does the chain say why they do nothing?
- Does it follow from an earlier row? Does a later row need it? A row nothing needs is a cut candidate.

For the whole chain:

- Does the protagonist want something from the first rows?
- Is what the protagonist can lose visible early?
- Does the ending follow from choices, not from luck?
- Is there any group whose behavior goes against what it gets in the world order without a crack to explain it?

## Twist

Design it only after checkpoint 1, on top of an approved chain.

- A twist is a second reading of events that already happened for their own reasons. It is not a new event.
- Write the hidden side's own chain (their wants, why now, why this way) in the same table. It must pass the chain check too.
- Fill this and keep it in `concept.md`:

```markdown
| 플레이어가 믿는 것 | 실제로 일어난 것 | 알게 되는 장면 | 다르게 읽히는 앞 장면 |
|---|---|---|---|
```

- Remove the twist in your head: does the story still stand as a story of causes? If not, rebuild the chain, not the twist.
- The facts that reveal the truth come from the world (a record, a habit, a rule) that existed before the twist needed them.

## Logline

Form: `[주인공의 특징]이 [뜻밖의 조건]에서 [목표]를 하려 한다. 그런데 [장애물].` One or two sentences, with a word that names the genre.

- Build it from the chain: the condition comes from the crack, the obstacle from the opponent's want.
- Every term in it is defined in the world order. Do not put an undefined name or code word in a logline.
- With 3 candidates, use different hook types: situation hook (the setup is fresh), mechanic hook (the game mechanic is fresh, e.g. a case that opens only when you point out a contradiction in testimony), character hook (the protagonist is fresh).
- Attach to each candidate one line: the question the player will have in mind. Drop a candidate that raises no question.
- If a candidate ends in an abstract word ("받아들이는 이야기", "성장하는 이야기"), rewrite it as action. An action sentence with two or more verbs makes a scene appear.
- When you twist a folktale or a classic, write one line for the core of the source and one line for the twist. Do not reuse the source's own scenes and sentences.

A logline alone does not show what happens. Under each candidate, write a synopsis of about 4–7 lines so the human can compare candidates from the text alone:

- What this candidate changes in the approved chain (a different twist, a different protagonist choice, a different ending). Candidates share the world and the cast.
- Opening: the first event on screen.
- One line per part: the event that turns it, with who does it and why.
- Twist, if any: where it lands and what it overturns, written in full. The human is the author, not a player.
- Ending: who gets or loses what.

No abstract lines ("갈등이 깊어진다", "진실에 다가간다"). Every name and term is one the world order or the cast list already defined.

## Concept sheet

Two parts. Fill "이야기" now. Fill "대본 설정" before step 4; it decides how the script looks, not what happens.

```markdown
# 기획 시트: <작품 또는 장면 이름>

## 이야기

- 분량 예산: 대사창 <N>개, 장면 <N>개 (5분 ≈ 대사창 50~75개, 장면 4~5개)
- 장르: <주 장르, 하위 장르>
- 섞는 장르와 이유: <없음, 또는 장르와 그것이 보강하는 감정. 결말 약속은 주 장르 하나만 정한다. 둘이 필요하면 사용자와 합의한다>
- 장르의 약속: <이 장르가 플레이어에게 약속하는 것 한 줄. 마지막 리뷰에서 지켰는지 확인한다>
- 관습과 변주: <지키는 관습 3개 이상 / 크게 비트는 것 1개. 플레이어가 아는 형태를 먼저 주고 한 군데에서 어긋난다>
- 로그라인: <선택한 로그라인>
- 중심 질문: 주인공은 <목표>를 할 수 있을까? (장면이 진행될수록 선명해지고 마지막에 답한다)
- 주인공: <누구, 시작 상태>
- 목표: <얻는 것 또는 벗어나는 것, 구체적 행동으로. "사흘 안에 증인을 찾는다"처럼 성공 조건이 보여야 한다>
- 대결: <누가 또는 무엇이 막는가, 그가 원하는 것. 주인공보다 약하면 안 된다>
- 잃을 것: <실패하면 잃는 것. 돈, 성공 같은 추상 보상이 아니라 사람, 관계, 정체성, 평판. 첫 장면 대사창에 한 번 이상 나와야 한다>
- 사건의 무게: <피해 종류(생명, 신체, 관계, 생계)와 그 피해가 화면에 처음 보이는 대사창>
- 결말 유형: 얻음 / 못 얻음 / 일부 얻음
- 왜 지금: <균열에서 가져온다>
- 시점 선언: <인칭, 시제, 시점 인물, 시점 인물이 모르는 것. 시간대나 시점이 둘 이상이면 structures.md 패턴 이름과 각 구간의 시점>
- 괴이/초자연 요소: 없음 / 있음(역할: 분위기, 힌트 제공, 정체 폭로, 해결 개입 중 하나)
- 이야기가 묻는 것 / 답 한 줄: <이 이야기가 던지는 질문 하나와 작품이 내놓는 답. 장면 삭제 여부를 판단할 때 기준으로 사용한다>
- 하지 않을 이야기: <이 작품이 피하는 방향 한 줄. 예: 노력하면 반드시 성공한다는 설교>

## 대본 설정 (4단계 전에 채운다)

- 장면당 화자 수 제한: <작품 결정, 예: 2명. 속말은 주인공과 합쳐 1명으로 센다>
- 속말 표기: <형식 파일 "Inner voice"의 표기 중 하나. 형식 파일이 없으면 기본 형식의 표기>
  - 역할 분담: 지문은 바깥(행동, 감각, 사실), 속말은 안(판단, 추측, 감정)
  - 형식 파일에 적힌 속말 표기의 한계가 있으면 사람에게 알린다
- 지문 문말: <현재형 또는 과거형 중 하나. structures.md 패턴을 쓰면 층이나 스레드마다 하나씩 정한다>
- 핵심 한마디 후보: <클라이맥스에서 인물이 할 대사 1~2개. 장면 카드 단계에서 위치를 결정한다>
- 취재·관찰 메모: <실제 직업이나 장소가 나오면. 지식이 아니라 소리, 습관, 소품, 용어, 사소한 사건, 실제로 들은 말 한마디. 없으면 없음>
```

The 5-minute numbers are estimates from example-work analysis and one playtest (sources.md "Tested in a work"). For a game that is not a VN, replace 대사창 with the unit the format file defines.

## Character sheet

Write one for the protagonist and for every character who appears in 2 or more scenes. Fill the core part now and the voice part before step 4. Decide what the character wants and hides first; decide the job or role last. A job chosen first brings its stereotype with it and the character turns thin.

```markdown
## <화자 id> (<표시 이름>)

### 핵심

- 역할: 주인공 / 적대자 / 조력자 / 증여자(단서나 힘을 주는 인물) / 증인 / 기타
- 사건 사슬에서 하는 일: <행 번호와 한 줄>
- 원하는 것(의식): <이 이야기에서>
- 필요한 것(무의식): <원하는 것과 충돌하면 기록>
- 말하는 것 / 숨기는 마음: <겉으로 내세우는 이유와 그 밑의 진짜 마음. 이 틈이 인물을 입체로 만든다>
- 결함 있는 신념: <한 문장>
  - 빈칸 질문 중 하나 이상에 답한다: 내가 안전한 때는 __이다 / 가장 중요한 것은 __이다 / 사람들의 가장 나쁜 점은 __이다 / 남들은 모르는 세상의 진실은 __이다
- 신념이 준 것 / 신념을 거스르면 잃는 것: <구체적으로>
- 기본 정서: <자기 처지를 받아들이는 태도 한 줄. 첫 장면에 이 정서가 보여야 이야기가 움직인다>
- 욕망 목록과 충돌 쌍: <3~5개 중 서로 부딪치는 쌍>
- 겉 감정 / 속 감정: <다르면 둘 다. 대사와 행동은 겉, 신체 반응과 속말은 속을 보여 준다>
- 좌절 반응: <원하는 것을 못 얻을 때 이 인물이 하는 행동 1순위>

### 목소리 (4단계 전에 채운다)

- 말투:
  - 길이 경향: <짧다 / 보통 / 길다. 주인공을 주변 인물보다 짧게 말하게 하면 성격이 드러난다>
  - 어미 층위: <합쇼체 / 해요체 / 반말>
  - 입버릇 2개, 쓰지 않는 표현 1개 이상
  - 평소 말하기 규칙: <음량, 길이, 어미 중 하나. 감정 정점에서 이 규칙을 처음 어기게 한다>
- 자리·소품: <이력을 보여 주는 물건이나 자리 하나. 대사 대신 이것으로 오래 있었는지, 막 왔는지를 보여 준다>
- 상대별 말투 표:

  | 상대 | 호칭 | 어미 | 거리감 |
  |---|---|---|---|
  | <id> | | | |

- 첫 등장: 외모 1개 + 습관 행동 1개 (캐릭터 그림이 있으면 외모는 생략)
- 그림 id: <형식 파일 규칙의 포즈·표정 id. 있는 것과 새로 필요한 것>
```

A minor character gets a three-line sheet: role and the one feeling they bring to the story, one line of speech habit, one prop. Give each supporting character a different feeling; two characters bringing the same feeling is a merge candidate.

Add these fields for an antagonist or a culprit:

- Type: one main and one secondary from shadow (the same wound as the protagonist), close enemy (someone the protagonist trusted), mask (outside and inside differ), conviction (keeps a principle to the end), recognition hunger (never acknowledged), jealousy, system.
- One principle the character keeps, and a word the character repeats. The principle does not change with the situation.
- Why the character believes they are right: the ground for self-defense lines.
- Why the character cannot part from the protagonist: duty, the same place, the scene of the case.
- One reason the player cannot beat them easily: information advantage, rank, a way to destroy evidence.

## Check

- Did the chain check and the cold read run before each checkpoint, and are the remaining items shown to the human?
- Does the logline have the protagonist, the condition, the goal, and the obstacle, all from the chain?
- Is the goal concrete enough that a success condition and obstacles follow from it?
- Is what can be lost something the player will care about?
- Is the weight of the incident enough to make tension within the length budget? A light case (a small theft) needs a bigger loss or a different harm. A stolen envelope of cash made weak tension in a 5-minute mystery (sources.md "Tested in a work").
- Do all main characters want different things? Even allies need different intentions, or their talk has no conflict.
- Does the viewpoint declaration list what the viewpoint character does not know? In a mystery, twists come only from this list.
- A protagonist with no chosen goal yet (someone just enduring): do not force a goal into the opening. Show their situation densely, with one point of sympathy, so the player asks what happens next; let the goal form later. What can be lost still appears in the first scene, and a game still needs a goal for the player before the first meaningful choice.
- Is the job doing the work that the character should do (a stereotype standing in for a person)?
