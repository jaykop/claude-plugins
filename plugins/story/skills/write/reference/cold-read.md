# Cold read

A writer cannot see the gaps in their own story: they know every reason, so the missing ones do not show. A reader who knows nothing but the pitch finds them. Run this before every human checkpoint that shows a story, plot, twist, or scene list, and again after any large change to the event chain. Do not show the human a story that has not been through it.

The mystery solve test (genre-mystery.md, fairness checklist 12) is a different, later check on the text the player sees. This one checks the story itself.

## Steps

1. Write the pitch as [presenting.md](presenting.md) says. That text is the only input. Do not give the reader the concept sheet, the chain table, notes, source documents, or the conversation.
2. Add one line on the form and genre, e.g. "선택지 없는 2~3시간 비주얼 노벨, 주인공 1인칭, 범죄 스릴러".
3. Give it to a new subagent (Agent tool, general-purpose). Use a fresh agent every round; an agent that has seen an earlier version fills gaps from memory.
4. Prompt (Korean, since the pitch is Korean):

   ```
   아래 이야기 소개만 읽고 답한다. 다른 파일은 열지 않는다. 작가의 의도를 짐작해서 채우지 않는다. 소개에 적힌 것만 근거로 삼는다.

   1. 이 이야기를 처음 듣는 사람에게 일어난 순서대로 5~8문장으로 다시 말한다.
   2. 읽다가 막힌 곳: 소개 없이 나온 이름이나 말, 앞뒤가 이어지지 않는 곳, 무슨 일이 일어나는지 알 수 없는 문장.
   3. 사건마다 묻는다: 그 인물이 왜 그것을 하는가, 왜 하필 지금인가, 왜 더 쉬운 방법을 쓰지 않는가. 답이 소개 안에 없는 것을 모두 적는다.
   4. 상대(적대자, 조직, 권력자)가 바보처럼 구는 곳: 그가 아는 것으로 보아 더 쉽게 할 수 있는 일을 하지 않는 곳.
   5. 서로 기대어 사는 무리끼리 이유 없이 싸우는 곳.
   6. 빼도 사건이 바뀌지 않는 인물, 사건, 설정.
   7. 반전이 있으면: 숨겨진 쪽의 행동도 이유가 이어지는가. 반전을 빼도 이야기가 서는가.

   답 형식:
   - 다시 말하기(1번)
   - 표: 번호 | 소개 속 구절 | 문제 | 심각도(막힘 / 의문 / 사소)
   ```

5. Compare the retelling with the story you meant. Any difference is a failure of the pitch or the chain, not of the reader.
6. Fix the chain first, then the pitch. "막힘": something cannot be followed at all. "의문": a reason is missing. "사소": wording.
7. If you fixed any 막힘 or 의문, run again with a new agent. At most 3 rounds.
8. At the checkpoint, list the 의문 items still open, in plain sentences. Do not say the story passed when items remain.

Without a subagent tool, do it yourself in a separate pass that reads only the pitch, and tell the human the check was self-run and weaker.

## Reading the result

- The reader's retelling drops or reorders an event: the pitch skipped a cause or used an undefined term there.
- The reader asks "why not just …": the opponent's easy move is unanswered. Add a row that makes the move impossible, or let the opponent make it and follow the consequences.
- The reader cannot tell who someone is: introduce them at first mention (presenting.md rule 3).
- The reader says a character could be cut: cut them, or give them a chain row that matters.
