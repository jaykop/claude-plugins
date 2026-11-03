# Judgment methods of the PM advisor

These are the basic methods that the PM advisor uses to judge schedule, scope, and risks. If the project keeps its own reference notes in profile `pm.knowledge_dir`, read those notes first. If they differ from this file, follow the notes. The notes can be private material, so do not copy their original text into reports. Quote only the note path and the item name.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. Priority

### 1-1. Three levels of necessity

| Level | Meaning | Judgment question |
|---|---|---|
| must (필수) (A) | Without it, this goal (milestone completion criteria, release) cannot be met | "Does it pass the completion criteria without this?" — if not, it is must |
| want (원함) (B) | Without it, the goal is still met, but the quality of the result drops a lot | "If it is left out, who loses what?" |
| spare (여유) (C) | Add it when there is spare capacity | The rest |

- Do not start a lower level before a higher level is finished. The only exception is while a must task waits for another person or an outside party. If you use the exception, record the reason.
- If you plan to make several of the same kind, split them and give each one its own level. Often only the first one is must. "As many as possible" is not a priority.
- Priorities keep changing. Review them at every weekly check. If they have not changed even once for several weeks, take it as a sign that the check is done only as a formality.
- Release preparation work (checking installation and launch, playtests, checking certification and submission requirements) is less visible than features, but it is usually must. Check whether it is missing.

### 1-2. Order draft — priority × effort

- Multiply priority 1–5 (1 is the highest) by effort 1–5 (1 is the easiest and shortest) to get a score from 1 to 25, and review from the smallest value.
- The score is an order **draft**. If you change the order after you look also at whether the task is must, prerequisites, the skills of the person who takes it, and urgent problems, write the reason.
- If the project uses its own grade system (for example, grade labels of importance × size), follow that system and do not use this score. If profile `pm.order_labels` exists, it is the project's system.

### 1-3. Estimation

- A rough time is enough. Do not chase exact times.
- **Relative estimation**: take one finished task as the reference, and measure "bigger than / about the same as / smaller than that one". Record the real time the reference task took.
- If you use size buckets (S·M·L·XL, or points such as 1·2·3·5·8·13), set a time range for each bucket. If tasks gather in one bucket, set the bucket boundaries again.
- **Timebox**: for a task whose duration is completely unknown, first set a "time to find out", and research and test within it. Estimate after the box ends. Count the box itself as one task.
- If the technology is new to you, or the result is hard to predict, take one size larger.
- A schedule always starts optimistic. In the plan, use only part of the available time (profile `pm.capacity.plan_ratio`).

## 2. Risks and responses

### 2-1. What a risk is

- A risk is a problem that has not happened yet but would shake completion or quality if it happens. A problem that already happened is not a risk but a task.
- Manage in the list only the risks that you can act on and that have a large impact. Keep risks with a small impact, or risks that you cannot act on, only as "watching".

### 2-2. Kinds

| Kind | Examples |
|---|---|
| people (사람) | Not enough people, conflict, slower pace, knowledge held by one person, burnout |
| project (프로젝트) | Not enough time or budget, scope growth, late design changes, work that piles up late (localization, certification and submission requirements) |
| production process (제작 과정) | Art and content pipeline bottlenecks, adopting new tools, deferred refactoring, build time |
| technology (기술) | Dependence on an engine version or experimental features, going over the performance budget, core technology that is not proven |

For solo development, read people risks as "not enough time, shaky priorities, decisions that only one person knows".

### 2-3. What to record

For each risk, write the following (format: `pm-risks.md` in `state-format.md`).

1. What can happen
2. Impact — what breaks if it happens. critical (치명) / severe (심각) / moderate (보통) / minor (가벼움)
3. Likelihood — high (높음) / medium (중간) / low (낮음). Attach evidence
4. 2 to 3 responses — things that can really be done. Separate **active** (능동: an action that reduces the risk itself) and **fallback** (대체: accepting another risk or cost to reduce the damage)
5. Decide by — "If it is not resolved by this date (or this milestone), confirm response X"
6. The cost and effect of each response, and how a decision now narrows later options

### 2-4. Order and updates

- Sort by Impact × Likelihood, largest first. If the order is the same, the one with the earlier Decide by comes first.
- Look first at the risks that harm the project's core principles (pillars). If the pillars are not decided, that itself is a risk.
- At every weekly check, review again the risks whose Decide by has passed or comes within 2 weeks. Do not delete a resolved risk. Change it to "resolved" and write how it was resolved.

## 3. Core principles (pillars) and scope

- Pillars are the core experiences or principles that this game must keep. There are no more than 4–5. Do not use a pillar that the whole team has not agreed to as a judgment criterion.
- Look at a new feature or change against the pillars. If pillars conflict, the pillar priority wins. Judging the pillars themselves (fun, interpreting the principles) is the design advisor's work. The PM looks at "can it be added with the current schedule, capacity, and risks".
- When you cut scope, remove want and spare first. If a must item has to be removed, the PM does not decide it: it is a decision that changes the goal. Raise it to the decision owner.

## 4. Milestones

### 4-1. Completion criteria as a grade table

When a milestone starts, first write the completion criteria by deliverable. Attach a grade and a check method to each criterion.

| Grade | Meaning |
|---|---|
| must (필수) | Without it, this milestone is not counted as complete |
| basic (기본) | Quality that must be there. Without it, the quality of the result drops |
| extra (추가) | Beyond expectations. Fill it in when there is spare capacity |

- Give each item a status (none (없음) / partial (일부) / done (완료) / excluded (제외) / not applicable (해당 없음)). If you decided to remove an item from the criteria, get it confirmed by the decision owner **before** the milestone ends, and record the reason.
- If the project uses its own evaluation table, use its grades and status values as they are.
- The check method must look at the deliverable, such as "try it directly in the build", "demo", or "playtest results". Someone saying "it is done" in a conversation or a messenger is not a check.

### 4-2. Splitting the remaining milestones into buckets

If several milestones remain, make one bucket for each milestone now, and split the work into the buckets. Split work that spans several milestones by milestone. This lets you look at the next milestone more realistically.

### 4-3. Capacity check

- If the project set a capacity for each milestone (a `capacity: Nh` (`용량: N시간`) line in the milestone description, and so on), that value is the basis of the must ratio.
- Time that can really be used in the remaining period = number of weekdays × weekday hours + number of holidays × holiday hours, multiplied by the plan ratio. Calculate it with `pm_calc.py capacity`. If the capacity that was set and this value differ a lot, write both.
- If the size sum of must tasks is over `pm.must_ratio_limit` (default 60%) of the available time, reduce the goal. The remaining 40% is for estimation error, bugs, and urgent work.
- Do not add issues without a size to the sum. Write them separately as "no size: N issues". Do not invent sizes to fill them in.

### 4-4. The last point to change the big direction

Before full production starts is the cheapest point to change the foundation of the game. As production goes on, the cost of a big change grows. In the milestone plan at this point, also do the "refit check" below, and check that you are not only adding features without cleaning up the base.

### 4-5. Refit check (at the start of a milestone)

| Axis | What to look at |
|---|---|
| Technology | Deferred technical debt and temporary code, how complete the core systems and tools are. For each technology, did you decide whether to keep it as it is, reinforce it, refactor it, rebuild it, or drop it |
| Game | Can the current design be built in the remaining period. Is there anything that you really changed because of playtest results |
| Team | Do the roles and the way of deciding fit the current number of people. Did you decide what to fix in the way of working of the last period |

Attach evidence (reports, issues, playtest records) to each axis. If there is no evidence, leave it as "not checked". For solo development, read the team axis as "time allocation and the record of decisions made alone".

## 5. Weekly check

- Do it on the same weekday every week. Compare the plan with the actual results, review priorities again, update risks, and decide next week's work.
- A weekly check plus handling urgent work on the day it comes up is better than gathering every day to hear progress orally. Read progress from the issue tracker.
- Record work instructions, owners, deadlines, and completion states in the issue tracker. Treat something decided only in a messenger or a conversation as not decided.
- For each meeting (for solo development, a check done alone), first write "what to decide or solve".

## 6. Retrospectives

### 6-1. Weekly retrospective (short)

- 1 to 3 items each for what went well / what went badly / what to change next week.
- For a task that was later than planned, write one cause: estimate was wrong (추정이 틀림) / scope grew (범위가 늘어남) / waiting for a prerequisite (선행 작업 대기) / urgent work cut in (급한 일 끼어듦) / not enough time (시간 부족) / cause unknown (원인 모름).

### 6-2. Milestone and project retrospective

- The purpose is to make the next project better. Do not blame. Focus on solutions.
- Questions: what to continue, what to stop, what to start, the most important thing learned this time.
- Look for what went well and what went wrong only in this project, rather than generic points that appear in every project. The "5 things that went well, 5 things that went wrong" format often used in game industry postmortems is useful.
- Leave the result as a document, and move 1 to 3 things to change into real tasks or rules in the next milestone plan.

## 7. Playtest plan (PD work)

### 7-1. What the test looks at

- A playtest here means that a few target players who see the game for the first time play it, to see whether it is worth playing, the flow, immersion, and whether they understand the controls and the tutorial. It is different from feature checks, load tests, automated tests, and betas.
- Decide first what you want to check. At the same time, accept unexpected reactions.

### 7-2. Procedure

1. Preparation: install the build on the test device and play it yourself several times. Fix problems that could block feedback, and block off broken parts.
2. Instructions: tell only the time limit and how to start. Do not explain the game. If an explanation is needed, that is a finding of this test.
3. Observation: watch and record. Help minimally only when the player is stuck for a long time and cannot progress, and record when and how you helped.
4. Wrap-up: write down reactions as they are, and do not overreact to one person's opinion. The same person is not a "first-time player" in the next test.
5. Frequency: regularly. Start in the prototype stage and continue until just before release. Manage the cycle in the periodic check table.

### 7-3. What to ask

- The most important thing is whether they want to keep playing. If they try to continue even when told to stop, that is the strongest signal.
- After the test, rather than abstract questions ("Was it fun?"), give sentences about specific scenes of the game and let them answer with the degree of agreement (Likert scale). Ask only about the experiences that this game aims for with its pillars.
- Write the questionnaire new, with this project's scene names. Sentence form example: "I felt <target experience> in <scene>".

### 7-4. Yes/no check items

Organize playtest results into yes/no items like "unit tests", and look at the same items again every time.

- Did everyone find <first goal> without help?
- Did anyone use <core control> without explanation?
- Did anyone say they wanted to quit at <a set section>?

The results of tests like these decide which features to add, what to fix, and what to keep. If you keep growing the plan only with meetings or documents without tests, the direction is wrong.

### 7-5. What to look at in the records

- Where players quit, where it takes the longest, where they die often (from logs and analytics records, if there are any).
- Whether players notice hidden information: controls, results of actions, states (health, buffs, and so on), location, goals and progress.

## 8. Team state diagnosis

Five conditions are commonly looked at for a team to perform well. Use them only as diagnosis criteria, not as enforced rules.

1. Psychological safety — do people feel it is fine to say a mistake or a disagreement
2. Dependability — do people do what they promised on time, at the expected level
3. Clear roles and goals — do people know who takes what and who decides
4. Meaning of the work — does each person accept why their work is needed
5. Impact of the work — do people believe this work matters

Adding too many rules and roles to a team whose trust is already high makes it slower. For a team with weak trust, clear roles and goals help. For solo development, look only at 2·4·5 (do you keep the promised scope, how does the current work connect to the goal, is motivation still there).

## 9. Learning fast

- Rather than planning for a long time, make something small, look at it, and fix it.
- The key is to shorten the time from one try to the next try. Tools, build time, and playtest frequency decide that time. Put work that makes this time longer (slow builds, manual repeated work) on the risk list or the improvement candidates.
