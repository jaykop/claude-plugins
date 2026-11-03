# Which advisor to ask

The rules that divide work between the advisors are kept in this one file. The "does not do" (안 하는 일) table in each advisor's SKILL.md lists only where the work goes. If the dividing rule is unclear, look at this file.

When a question looks like another advisor's work:
- If it is a request that the user made in the conversation, ask once: "<고문>이 맡는 질문이에요. <고문>으로 볼까요?". If the user says yes, call that advisor's skill with the Skill tool (`advisors:<고문>`). If the user says no, do only the part that the current advisor can handle (for the technology trend advisor, the outside changes of that technology). If there is no part to handle, finish without a report.
- If the question came from the question inbox, do not ask the user. Pass it to the right advisor by the passing rules in inbox-format.md. This is the same in conversation runs and unattended runs.

## Word meanings

- **Our tree** (우리 트리): all the game code, project plugins, and local engine source in our repository.
- **Enabled technology** (켜져 있는 기술): the plugins in the technology trend advisor's technology list (`_state/radar-inventory.md`) whose status is "사용 중", "켜짐·사용 흔적 없음", or "엔진을 고쳐서 씀", and the engine features that project setting values turn on.
- **Technology not in our tree or turned off** (우리 트리에 없거나 꺼진 기술): all other technology. With a source build, a plugin that is in the engine folder but turned off also belongs here. For engine features that settings turn on (for example, renderer features), the project setting values decide whether they are on or off.

## Technical questions: td and radar

The rule is **where the answer is**.

| Where the answer is | Advisor | Example questions |
|---|---|---|
| Our code, local engine source, team documents | td | "이거 구조 어떻게 잡지?", "A 랑 B 중 뭐가 나아?", "이미 켜져 있는 <엔진 기능>으로 할까 직접 만들까?", "자체 시스템을 그 엔진 기능으로 옮길까?", "이미 쓰는 <기능>을 우리 코드에서 어떻게 쓸까? 더 넓혀 써도 돼?", "이 기능 기술적으로 돼?", "이 버그 왜 자꾸 다시 터져?", "모듈 의존 점검", "엔진 수정 블록 줄이기", "기술 부채 순서", "작성 규칙 초안" |
| Outside (new announcements, other engine versions, external products, industry news) | radar | "요즘 엔진 소식", "<우리 트리에 없거나 꺼진 기술> 써도 돼?", "<버전>으로 올려야 해?", "<외부 제품> 도입 검토", "써 본 사람들 평은?", "우리가 쓰는 <엔진 기능>에 알려진 버그 있어? 몇 버전에서 고쳐졌어?" |
| Both | td takes it | td compares the options with the facts on our side. For an outside fact that decides the verdict, td finds only primary sources under the conditions of td evidence.md §4 (W2 to W4). If the technology is not in our tree or is turned off (W1), td passes a question to radar |

- A technology name in the question does not by itself make it a radar question. How to use enabled technology in our code, and whether to replace our own implementation with that technology, are td.
- Whether to bring in technology that is not in our tree or is turned off, and what its maturity, supported platforms, and known problems are, are radar.
- A question that asks only about the known bugs and fix versions of an engine feature that we use (the engine developer's material answers it) is radar. A question that looks for the cause of that bug inside our code, or chooses how to fix it, is td. Inside that work, td finds only primary sources under condition W3.

## Other advisors

| Question | Advisor |
|---|---|
| Questions that measure cause and size (why the frame rate drops, how heavy it is, whether refactoring is needed) | perf |
| Questions that choose between options (which structure to fix it with, how to split modules) | td |
| Fun, game rules, whether the game needs this feature (add it or remove it) | design |
| Whether this feature can be built, which structure to build it with | td |
| Whether the code has a path for an AI agent to reproduce a state and check the result as text (agent verifiability). The format of performance measurement results and the measurement itself are perf | td |
| When to do it, whether to put it in this milestone or defer it, task order, schedule risks, retrospectives, when another advisor's periodic check is due | pm |
| Market, competing games, player base, hardware adoption | market |

- Three advisors split the review of one feature. Fun and principles are design. Whether it can be built and which structure to build it with are td. Whether to put it in this milestone and when to do it are pm. pm does not make the verdicts of the other two in their place. It asks them through the question inbox.
- Whether refactoring is needed is perf. Which way to fix it is td. When to do that check or that work is pm.
