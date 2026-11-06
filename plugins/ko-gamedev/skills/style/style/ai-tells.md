<!-- ko-lint: ignore-file -->
# Signs of AI-written Korean

What separates corpus K (AI) from corpus A (people) and D (design docs). AI Korean leans toward purified native verbs, complete sentences, middle-dot lists and ~므로. It reads like a translated textbook, not like a team's code. Numbers are per 1,000 comments.

| Sign | A | K | Fix |
|---|---|---|---|
| Middle-dot lists (`앞·뒤`, `비용·쿨다운`) | 0 | 103 | Commas, `와/과`, `/` |
| `~므로` | 18 | 200 | `때문에`, `~라서`, or two lines |
| Every comment is a `~다` sentence | 15% of lines | 89% of lines | Noun-ending notes for fields and inline comments (style/comments.md) |
| Native verbs where the industry uses Sino-Korean or loanword verbs: 쓴다, 돌려준다, 고른다, 부른다, 바꾼다, 넘긴다, 보낸다, 모은다, 맡는다, 지운다, 남긴다, 센다 | about 0 each | 4 to 78 each | glossary/core.md |
| Engine concepts translated into Korean: 편집기, 저작, 표본, 사본, 도형, 칸, 구독, 이탈, 소유 액터, 곡선, 질주 | 0 | 3 to 44 each | 에디터, 에디터용, 샘플, 복사본, 셰이프, 필드, 바인딩, EndOverlap, Owner, 커브, 스프린트 |
| 대상 for every target, object and receiver | 12 | 106 | 타겟 for combat targets; name the thing elsewhere |
| 시각 for a point in time | 0 | 37 | 시점, 타이밍, 시간 |
| 켜면, 끄면 for bool values | 0 | 10 | true면, false면, 활성화하면 |
| 비우면, 비워 두면 for unset values | 0 | 11 | 설정하지 않으면, None이면 |
| 판정 for any evaluation | 1.4 | 54 | 판단, 체크. Keep 판정 for hit detection. |
| Industry words absent: 세팅, 체크, 업데이트, 스폰, 어빌리티, 스킬, 하드락, 기획 | 4 to 58 | 0 to 5 | Use them where they fit. For an ability, write Ability or GA, because engine type names stay English (style/comments.md). |
| Personification and metaphor: 입력이 노린다, 몫, 기댄다, 흉내 낸다, 내려간다 (for unload) | rare | frequent | Say the technical action |
| English idioms translated word by word: 조용히 실패한다, 냄새가 난다, 계약, 죽은 코드, 열려 있는 질문, 스테일 | about 0 | 0 to 8 | glossary/core.md, Calques and metaphors |
| 자리 for a position, list slot, field, byte offset or capacity | 0 | 5.4 | 위치, 지점, 인덱스, 필드, 오프셋, 공간 (glossary/core.md) |
| A whole design rationale in one doc comment | rare | frequent | Keep the fact the reader needs; move the reasoning to docs or the commit |

## What not to over-correct

- Human comments in A also have flaws: typos (애니매이션, 악세서리, 이팩트), casual words (일단, 그냥, ...), mixed ~다 and ~니다. Do not copy them. The target is the industry's vocabulary and register with clean grammar.
- Do not rewrite a clear, correct sentence only because it ends in ~다.
- Do not force loanwords where plain Korean is the industry habit too: 위치, 회전, 이동, 입력, 상태 are normal in A.
