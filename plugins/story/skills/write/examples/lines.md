# Bad and fixed examples

Used in steps 4 and 5. The skill wrote every example; none comes from a book or a work. The examples use the default format (reference/format-template.md). Speaker ids are examples: `hero` protagonist, `aunt` aunt, `client` client, `clerk` clerk.

## 1. Lines that explain what both know

Bad: both know it; it is said for the player.

```text
aunt: 너도 알다시피 우리 가게는 할아버지 때부터 삼십 년째 하는 국숫집이잖니.
```

Fixed: let it slip inside an argument.

```text
aunt: 삼십 년 버틴 가게를 네가 한 달 만에 닫겠다고?
hero: 버틴 거지, 잘된 건 아니잖아요.
```

## 2. Emotion names in narration

Bad:

```text
그 말을 듣자 나는 몹시 불안해졌다.
```

Fixed: an action or a body sensation; the face goes to the pose.

```text
do Stage.pose("hero", "tense")
컵을 내려놓으려다 두 번 만에 겨우 받침에 올렸다.
```

## 3. Question and exact answer, every time

Bad:

```text
hero: 어젯밤 몇 시에 들어오셨어요?
client: 열한 시쯤 들어왔어요.
hero: 그때 가게에 누가 있었나요?
client: 아무도 없었어요.
```

Fixed: mix counter-questions, short answers, and topic changes. The evasion itself becomes a clue.

```text
hero: 어젯밤 몇 시에 들어오셨어요?
client: 그게 중요해요?
hero: 몇 시요.
client: ……11시. 11시 조금 넘어서.
client: 근데 경찰도 아닌데 왜 자꾸 물어요?
```

## 4. First person: own face from outside, another's thoughts asserted

Bad:

```text
내 얼굴이 하얗게 질렸다.
그녀는 내가 눈치챌까 봐 겁을 먹고 있었다.
```

Fixed: own body as sensation, others as visible signs and guesses.

```text
손끝이 차가워졌다.
그녀는 내 쪽을 보지 않고 영수증만 접었다 폈다 했다.
```

## 5. A long box

Bad: three facts and an emotion in one box (over 70 characters).

```text
clerk: 그 손님은 매주 화요일마다 와서 늘 같은 자리에 앉았는데 지난주에는 안 왔고 오늘은 웬 남자랑 같이 와서 계속 시계만 보더라고요.
```

Fixed: split at breaths and reactions.

```text
clerk: 매주 화요일에 와요. 늘 창가 자리.
clerk: 지난주엔 안 왔고요.
hero: 오늘은요?
clerk: 남자랑 같이요. 계속 시계만 보던데.
```

## 6. Lines that pass the checker but misbehave

Bad (in the default format):

```text
오후 세 시: 가게 앞.
이모: 왔니?
- 그때 문이 열렸다.
```

Fixed: no `: ` in narration, speaker ids only, narration does not start with `-`.

```text
do Stage.bg("bg_shop_front")
오후 3시, 가게 앞.
aunt: 왔니?
그때 문이 열렸다.
```

## 7. A choice with no reaction

Bad: every option goes straight to the same line.

```text
- 믿는다
- 의심한다
=> next_day
```

Fixed: react to each option, record the result, then rejoin.

```text
- 믿는다
	set trust_client += 1
	client: ……고마워요. 진짜로. [#pose=relieved]
- 의심한다
	client: 그럴 줄 알았어요. [#pose=cold]
	그녀는 가방을 챙겨 일어섰다.
=> next_day
```

## 8. A clue exposed with emphasis

Bad: the narration says it matters.

```text
나는 그때 중요한 것을 발견했다. 달력의 13일에만 빨간 동그라미가 없었다.
```

Fixed: one line inside a complaint.

```text
aunt: 달력 좀 봐라. 장날마다 동그라미 쳐 놨더니 누가 13일 것만 지워 놨어.
aunt: 그나저나 너 밥은 먹었니?
```

## 9. Explaining the emotion after a shocking line

Bad:

```text
client: 그날 밤, 언니는 가게에 없었어요.
그 말은 모든 것을 뒤집는 충격적인 고백이었다.
```

Fixed: cut with one action line or a scene change.

```text
client: 그날 밤, 언니는 가게에 없었어요.
선풍기 돌아가는 소리만 남았다.
```

## 10. A scene that starts with explanation

Bad:

```text
~ start
1994년 여름, 서울. 나는 서른두 살의 전직 형사로, 지금은 이모의 국숫집을 돕고 있다.
```

Fixed: start on an incident or an odd detail and let the setting slip.

```text
~ start
do Stage.bg("bg_shop_front")
셔터 열쇠 구멍이 껌으로 막혀 있었다. 어제는 없던 것이다.
do Stage.enter("aunt", "neutral", "right")
aunt: 형사 그만두더니 열쇠 구멍 구경이 취미가 됐니?
```

## 11. A repeated device sentence (a good example)

The repetition check flags it, but it stays. Repeating the same sentence as a signal lets the player learn the rule by feel. Players named this kind of repetition as the most memorable part of the tested work.

```text
# 의도: 장치 문장. 거짓말을 들을 때마다 같은 한 줄로 반복한다
landlord: 그 시간엔 방에서 텔레비전 보고 있었어.
창밖 신호등이 한 번 깜빡였다.
tenant: 저는 그 계단, 오늘 처음 올라와 봤어요.
창밖 신호등이 한 번 깜빡였다.
```

- Do not vary the sentence. Variants like "또 깜빡였다" or "다시 신호등이" blur the signal.
- Put an intent comment above the first one. Step 5 pass D's repetition check and the review report judge it as keep.
- If the solution uses the signal, also compare it with the supernatural rule (step 5 pass A).
