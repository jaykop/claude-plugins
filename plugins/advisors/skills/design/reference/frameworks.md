# Analysis frameworks

These are the frameworks that the design advisor uses when it checks systems. Read this file in area diagnosis Step A3 and in single review Step B3. The analyst that collects material reads only the items that the caller named.

A framework is not a tool that gives the right answer. It is **a tool that makes check questions**. So each framework has the steps where it is used.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

- If the principle document has the project's own verification checklist, use it as the first column of the per-system check. Passing the checklist only means that the direction is right. It is not evidence of fun.
- Do not run a framework that has no input material. Leave its column out of the report entirely, and write only one line in body "0. Basis": "<framework name>: no input material (needed: …)" (`<틀 이름>: 입력 자료 없음(필요한 것: …)`). Do not make a table filled only with "no material".

| # | Framework (틀) | Area diagnosis | Single review | Input material |
|---|---|---|---|---|
| 1 | Core loop map (핵심 반복 구조 고리 지도) | A3-2 | Check the loop it attaches to | Design documents, implementation check |
| 2 | MDA chain (MDA 사슬) | Proposal card | B3-2 | Rules of the target |
| 3 | Meaningful choice (의미 있는 선택) | A3-4 | B3-3 | Systems that have options, data |
| 4 | Risk-reward (위험-보상) | A3-4 | B3-3 | Actions that take a risk, data |
| 5 | Role overlap (역할 중복) | A3-4 | Similar existing systems | System list, loop map |
| 6 | Player motivation (플레이어 동기) | A3-4 (when there is a target) | When there is a target | Profile `market.target_player` |
| 7 | Tension curve (긴장 곡선) | A3-4 (when there is placement data) | Not used | Content placement data |
| 8 | Learning order (학습 순서) | A3-4 (when there is placement or tutorial material) | When a new rule is added | Content order, tutorial documents |
| 9 | Interpreting play that differs from the intent (의도와 다른 플레이의 해석) | A3-5 | B3-1 | Playtest observations |

---

## 1. Core loop map

**What it is** — Draw the loop that the player repeats, "action → feedback → reward → reason for the next action" (the core loop), split into three time units.

| Unit (단위) | Range |
|---|---|
| moment (순간) | A few seconds to a few tens of seconds. One exchange in combat, one move in a puzzle |
| one round (한 판) | One mission, stage, or match |
| long term (장기) | Growth, collection, and unlocks across several rounds |

**How to do it**
1. From the design documents, extract the loop for each unit. Leave a cell that is not in the documents as "not in the documents" (문서에 없음). Do not fill it with genre common sense.
2. Attach the implementation check stage to show whether each cell of the loop is implemented.
3. For each system, mark which cell of which loop it is attached to.

**Output** — The loop map table, "broken loops" (loops whose feedback or reward is empty), and "systems not attached to any loop".
- Start looking for on hold and removal candidates in the systems not attached to any loop.
- Start looking for add candidates in the broken loops.

**Common mistake** — Filling the loop by looking only at summary documents. Use summary documents only to choose what to read, and quote the evidence for the loop from the main documents.

## 2. MDA chain

**What it is** — An analysis framework that assumes that rules (Mechanics) create behavior patterns during play (Dynamics), and that those patterns create the player's emotions (Aesthetics). Its purpose is to stop you from jumping straight from rules to emotions, by making you always write the "behavior pattern" in the middle.

**How to do it** — For each proposal card, write in this order.

```
rule → expected play pattern → target emotion → linked pillar
```

- The behavior pattern is a prediction, so it is [estimated].
- Write the patterns separately for each player type: a player who only cares about efficiency / a first-time player / an expert.
- If profile `play_mode` is `협동`, `대전`, or `혼합`, add three more: a team with a large skill gap, the case where one player solves everything alone, and the case where one player leaves or goes down.

**Output** — Take the "observation signal" of the verification method from these behavior patterns. If a pattern is not observed, that link of the chain is wrong.

**Common mistake** — Imagining only good patterns. Write first the dominant strategies and exploits that a player who only cares about efficiency builds.

## 3. Meaningful choice

**What it is** — A framework that checks whether what the player chooses (weapons, skills, builds, routes, rewards) is actually worth thinking about.

**Three checks**
1. Is the difference in results visible to the player?
2. Does the answer change with the situation?
3. Is the information needed to choose given?

**Calculation for the second check** — For each situation in which the choice actually happens (kind of enemy faced, stage, number of players), make a table of the efficiency of the options, and check the dominance relations with `choice_calc.py dominance`.
- An option that is first in every situation → a dominant option candidate. The hypothesis is that there is no reason to choose the other options.
- An option dominated by another option → a candidate for an option with no reason to be chosen.
- Do not judge with one easy condition, such as the average against a practice target. The situation columns must be scenes where the choice actually happens.
- If the data is placeholder values, do not calculate, and make a judgment that looks only at rules (grades-and-rubric §5).

## 4. Risk-reward

**What it is** — A framework that checks whether actions in which the player takes a risk (precise timing defense, keeping close range, waiting while gathering resources, and so on) are rewarded as much as the risk taken.

**How to do it** — Put the gain on success of the risky action, the loss on failure, and the gain of the safe action into the same unit, and get the break-even success rate with `choice_calc.py breakeven`. If the actions take different amounts of time, also put in the time.
- The break-even success rate is over 100% → even on success, it is not better than the safe side. Make the hypothesis "players drift to the safe side", and pass it to the verification method.
- 0 or below → failure loses nothing. The risk is not a risk.
- In between → whether players actually exceed that success rate in a playtest becomes an observation item.
- If the units cannot be matched (for example, damage dealt and health lost), do not calculate, and write "not calculated: units differ" (단위가 달라 계산 안 함). If the design documents have a rule that converts one to the other, quote that rule and use it.

## 5. Role overlap

**What it is** — A framework that checks whether two systems do the same job.

**How to do it** — For each pair of systems, check three things: Do they attach to the same cell of the same loop? Do they fill the same motivation? Do they ask the player for the same choice? If all three overlap, it is a merge or on hold candidate. When you judge that they overlap, quote the evidence of both systems.

## 6. Player motivation

**What it is** — A framework that checks why the player cares about a system. Use the two models in different places.

- **Self-determination theory**: It sees basic human needs as three: competence, autonomy, and relatedness. Use it when you ask "why would the player care about this?" about one system.
- **Gamer motivation model** (for example, the 12 motivations that Quantic Foundry published — destruction·excitement, competition·community, challenge·strategy, completion·power, fantasy·story, design·discovery): Use it when you compare the target player with systems. Use only the published definitions, and do not use numbers from paid reports. When you move the definition of a motivation into the report, write "source checked" only if you opened the public original in this run. If you did not, leave it as [estimated].

**Input** — This advisor does not decide the main motivations of the target player. Use only profile `market.target_player`. If a market advisor report shows a player base different from the profile, do not use it for verdicts; raise it only as a "question for the user".

**Output** — A mark of the motivations that each system fills. A main motivation of the target that no system fills is an add candidate. A system that fills only motivations outside the target has its fun contribution lowered by one grade.

**If there is no input** — If the target is empty, leave this check out and write only one line in body "0. Basis".

## 7. Tension curve

**What it is** — Estimate from the content placement the shape of the rise and fall of tension and relief during play, and how well the challenge difficulty matches the player's skill.

**Input** — Content placement data (encounter composition, enemy appearances, mission sections). If there is none, do not use it.

**How to do it** — For each section, take pressure indicators from the data (number of enemies faced at the same time, enemy attack frequency, whether recovery means exist, and so on), and line up the intensity. Mark three kinds of sections.
1. Sections where tension continues without a break
2. Sections where a new rule appears directly in real play without first being introduced in a safe situation
3. Sections where the difficulty jumps suddenly

**Caution** — This curve is an estimate ([estimated] or [calculated]). Check the actual feel with a playtest.

## 8. Learning order

**What it is** — Check whether a new rule appears in the order "introduction → safe practice → combination with other rules → test under pressure".

**Input** — Content order, tutorial and onboarding documents. If there are none, do not use it.

**How to do it** — For each rule, find where it first appears and the first scene where that rule must be used. Mark the rules that appear as a test without an introduction, and the places where two or more new rules first appear in the same scene.

## 9. Interpreting play that differs from the intent

If a playtest shows play that differs from the design intent, check it in the following order.

1. Start from the premise that players move toward the larger reward, and suspect **the reward structure first**. Check the calculations of §3 and §4 again.
2. Review both "teaching (tutorials, on-screen guidance)" and "changing the rules or rewards", and write the cost of each. Do not give adding a tutorial as the first answer.
3. Separate observation from interpretation. "Who did what in which situation" is observation. "Why they did it" is interpretation ([estimated]).
4. Treat one person's opinion only as one person's opinion. Write the number of people who said the same thing and the sample kind.
