<!-- ko-lint: ignore-file -->
# Code comment style

How Korean game developers write comments, measured on corpora A and O (people) against corpus K (AI). Codes are explained in [../glossary/README.md](../glossary/README.md#evidence).

| Line ending | A (people) | O (people) | K (AI) |
|---|---|---|---|
| Noun (개조식: ~ 체크, ~ 여부, ~ 처리) | 58% | 55% | 7% |
| ~다 (해라체 sentence) | 15% | 8% | 89% |
| ~함, ~음, ~됨 | 5.5% | 6% | 0% |
| ~니다 | 4% | 15% | 0.1% |

People write short noun-ending notes and switch to full sentences only to explain. AI writes every comment as a full sentence. In O, ~니다 comes from one team that writes its C# `///` doc comments in 합쇼체; that is a team convention, so follow the file. Match the people, but keep the grammar and spelling clean: A also contains typos and casual words that you should not copy.

## Register by comment kind

| Comment kind | Write | Example |
|---|---|---|
| Property, field, enum value, parameter | A noun phrase. Add a short clause for the condition or the special value. | `/** 하드락 해제 거리. 0이면 거리로는 해제하지 않음 */` |
| Bool property | `~ 여부`, or `true면 ~` | `/** true면 이동 중에도 회전 허용 */` |
| Inline note in a function body | 개조식 with a noun ending | `// 서버에서만 실행` `// 타겟이 없으면 스킵` |
| Function or class header | First line: what it does, as a ~한다 sentence or a noun phrase. Then conditions and results as short lines or `-` items. | see below |
| Why, order of steps, an engine quirk | ~한다 sentences, or a numbered list | `// 1. 타겟 후보 수집` `// 2. 각도 가중치로 정렬` |
| TODO, NOTE | Follow the project. If it has none: `TODO(이름): 내용` | `// TODO(이름): 임시 처리. 서버 동기화 방식 확정 후 제거` |

Rules:

- Keep one register inside one declaration's comment block. Noun endings and ~함 endings can share a block; ~다 and ~니다 cannot.
- Use ~니다 only when the file already uses it throughout.
- Register is consistent per comment kind within a file: all property comments as noun phrases, all function headers in one style.
- When correcting, a property, field or enum comment you rewrite for words becomes a noun phrase. Count that kind in the file: if you rewrite at least half of them anyway, convert the rest too; otherwise leave the clear ones alone. The user can ask for a full register pass.
- Function and class headers are not converted for register. Keep ~한다 sentences there, or the noun style if the file already uses it, and only fix words.
- Put units in parentheses: (초), (cm), (도), (0~1). Add a unit only if you checked it in code.
- Say what 0, None and an empty value do when they behave differently: `0이면 무제한`, `None이면 루트 컴포넌트 사용`.

## Words

- Use the glossary words. Run `scripts/ko_lint.py` on what you wrote when it is more than a few lines.
- Write class, function, property, tag and asset names in English exactly as in code. Attach the Korean particle the way the name is read aloud: `Tick은`, `Owner가`, `Actor를`, `Socket을`, `GE를`, `BeginPlay에서`.
- An English engine verb with a Korean ending is normal when it names the exact API: `Tick하지 않음`, `EndPlay되면`, `Override할` (A 9.2 / K 6.0). For general actions use the Korean verb: `Set되는` → `세팅되는`, `Valid하지 않은` → `유효하지 않은`.
- List with commas or slashes (`전투/비전투`), not the middle dot `·`.
- `->` is fine for a flow inside a comment: `Idle -> Run -> Stop`.
- Use 때문에, ~라서, or two short lines instead of chaining ~므로.

## Content

- Write what a reader of this line needs: the role of the value, the condition, what happens at the edge values. Leave history and reasoning chains to commit messages and docs.
- One fact per line. If a sentence holds a condition, an exception and a reason, split it.
- No personification or metaphor: not 입력이 노리는 단계, but 현재 이동 입력에 해당하는 Gait.
- Keep facts exact when you rewrite: conditions, negations, numbers, units, defaults, lifetime, failure handling. Do not add a fact you did not check.

## Before and after

Examples written in the style of corpus K. They show the patterns, not real comments.

| Before | After | Why |
|---|---|---|
| `/** 비우면 무기 기본 이펙트를 그대로 쓴다. */` | `/** 설정하지 않으면 무기 기본 이펙트 사용 */` | 비우면, 쓴다 |
| `/** 타겟과의 거리가 이 값을 넘으면 추적을 멈춘다. 0이면 거리로는 멈추지 않는다. */` | `/** 추적 중단 거리. 타겟과의 거리가 이 값을 넘으면 추적 중단, 0이면 거리 제한 없음 */` | Property comment starts with what the value is |
| `// 난수는 [0, 1) 값을 내므로 확률보다 작을 때 성공으로 본다.` | `// 난수는 [0, 1) 범위 값을 반환하기 때문에 확률보다 작으면 성공으로 간주` | 내다, ~므로, 본다 |
| `/** 피격 방향을 앞·뒤·왼쪽·오른쪽 가운데 하나로 고른 값. */` | `/** 피격 방향을 전/후/좌/우 중 하나로 구분한 값 */` | Middle dot, 가운데, 고르다 |
| `/** 마지막으로 공격한 월드 시각(초). */` | `/** 마지막 공격 시점의 월드 시간(초) */` | 시각 |
| `// 레벨 언로드 순서에 따라 매니저가 먼저 내려갈 수 있으므로 살아 있을 때만 해제한다.` | `// 레벨 언로드 순서에 따라 매니저가 먼저 파괴될 수 있기 때문에 유효한 경우에만 해제` | 내려가다 and 살아 있다 are metaphors; ~므로 |
| `// 화살 하나는 대상 하나만 맞히고 사라진다. 걸러진 대상은 지나쳐 계속 날아간다.` | `// 화살 하나는 타겟 하나만 히트하고 소멸. 필터링된 타겟은 통과해서 계속 비행` | 대상, 맞히다, 걸러지다 |
| `/** 무한 흔들림을 루프로 지정하면 경고한다. */` | `/** 무한 카메라 셰이크를 루프로 지정하면 경고 */` | 흔들림 for a Camera Shake asset |
| `/** 무기의 스태틱 메시를 찾고, 없으면 루트 컴포넌트를 반환한다. */` | (no change) | Already clear. Not every sentence needs a rewrite. |

A header with several facts:

```cpp
// Before
/**
 * 요청을 복사하고 한 번의 보상 지급을 시작한다.
 * 요청을 받으면 true다. 설정 오류, 인벤토리 부재, 중복 요청은 false와 로그로 알린다.
 * 지급할 아이템이 0개면 완료 이벤트를 즉시 부른다. 그 외에는 각 지급 결과 뒤 완료 이벤트를 부른다.
 */

// After
/**
 * 요청을 복사해서 보상 지급을 한 번 시작한다.
 * @return 요청을 수락하면 true. 설정 오류, 인벤토리 없음, 중복 요청이면 false 반환 후 로그 출력
 * - 지급할 아이템이 0개면 완료 이벤트 즉시 호출
 * - 그 외에는 각 지급 결과가 나온 뒤 완료 이벤트 호출
 */
```
