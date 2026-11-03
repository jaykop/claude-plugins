# Evidence grades and verdict criteria

These are the criteria that the design advisor uses for verdicts. Read this file in area diagnosis Step A3 and in single review Step B3. The analyst that collects material also reads §1 and §2 of this file first.
If this file conflicts with the common rules (`shared/rules.md`), the common rules win.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. Evidence grades

Attach one of the grades below to every claim. The grade follows the **weakest link** of that claim.

| Grade (등급) | Meaning | Where it can be used | Common level (공통 단계) |
|---|---|---|---|
| [observed-behavior] ([관찰-행동]) | Player behavior confirmed in logs, video captures, or observation notes. It must say who did what in which situation | The only grade with which a fun judgment can be written as "confirmed". Evidence for recommend removal | confirmed (확인함) |
| [observed-opinion] ([관찰-의견]) | What a tester said. Always write with it the sample kind (internal developer / external tester) and the number of people who said the same thing | The fact that such an opinion existed is confirmed. As evidence that something is fun or not fun, it is estimated | confirmed (확인함) (the fact that it was said) / estimated (추정) (the fun conclusion) |
| [calculated] ([계산]) | A result calculated from data or code values. Show the formula, the input location, and the command that was run | Structure judgments such as a dominant option or a break-even point | confirmed (확인함) |
| [document] ([문서]) | Content that is only in the design documents and was not confirmed by the implementation or by observation | The fact that the design decided so. Do not use it as evidence that the game actually is so | confirmed (확인함) (document content) / estimated (추정) (game state) |
| [document-intent] ([문서-의도]) | An intent sentence in a design document, such as "the player feels ~" | Use it only as a goal. It is not evidence that something is fun | confirmed (확인함) (the intent is written) |
| [estimated] ([추정]) | A hypothesis built from theory, precedents from other games, or analogy | Supporting evidence for additional proposals. It alone cannot produce on hold or removal | estimated (추정) |

If there is no material and you cannot attach a grade, do not make the claim, and leave it as "judgment withheld" (common level "unknown").

## 2. Marks attached to evidence

| Mark (표시) | When |
|---|---|
| source document's estimate (출처 문서의 추정) | Cause analysis, effort estimates, and effect estimates contained in a document that another person or an AI summarized (a feedback summary, meeting minutes, and so on). The grade is [estimated], and do not use it to calculate fun contribution, cost, or priority. Do not move the numbers in it into the report |
| original not checked (원문 미확인) | A statement in a summary document whose original (original note, recording, raw survey data, public post) you could not open and check. Do not raise it to [observed-opinion]; leave it as [estimated]. If the original is a project file, the analyst opens it. If it is a public web page, the web-scout opens it. If it is in a place that cannot be opened, such as an internal messenger, do not pass it to web collection; leave it as "original not checked" |
| implementation stage N (구현 N단계) | The result of the implementation check (0–3). Stage 1 = the name is in the code, stage 2 = the call path connects to the game flow, stage 3 = the data and asset connections were also confirmed. Claims about a system below stage 2 have the [document] grade |
| written before principle revision (원칙 개정 이전 작성) | A design document dated before the last revision date of the principle document. Read the date only from the version control history or the revision date in the document head |
| file name date (파일 이름 날짜) | The document head has no date, so the date in the file name was read. Treat it only as the writing date and do not use it as a revision date. So it is not a reason to attach "written before principle revision" |
| date unknown (날짜 미상) | The document head and the file name have no date, and the version control history could not be checked either |
| precedent: source checked (선례: 출처 확인) / precedent: memory (선례: 기억) | An example from another game. Only a source (official developer material, patch notes, developer talk) that you opened this time is "source checked". Do not use "memory" as sole evidence. For a talk where you saw only the title and the abstract, add "abstract only" (초록 기준) |
| precedent only (선례 전용) | A game outside the market advisor's competitor list (`_state/market-competitors.md`) |
| outdated report (오래된 리포트) | Another advisor's report is older than profile `stale_after_days` |

## 3. Sentences about fun

- If a conclusion about fun or emotion ("boring", "frustrating", "thrilling", "tense", and so on) has no [observed-behavior] evidence, start it with `Hypothesis:` (`가설:` when `report_language` is `ko`), and on the same line write the ID of the proposal that has the verification method to check that hypothesis.
- Do not judge hand feel, hit impact, or control feel. Write only whether the data contains the mechanisms that produce such feel (hit stop — an effect that briefly freezes the screen at the moment of a hit, hit sounds, screen shake, and so on), and how skills use those mechanisms differently.
- You cannot play videos directly. Use as evidence only what is in the captures or visual notes that the user gave, and do not guess the content of a video.

## 4. Verdict kinds

### Existing systems

| Verdict (판정) | Meaning |
|---|---|
| keep (유지) | It contributes to the principles, it is attached to a loop, and no structure problem was found. Write a reason for keep too |
| modify numbers (수정(수치)) | A problem that goes away if only the numbers change. Give only a `[PLACEHOLDER]` starting value and the reason. Do not give it in the no-numeric-evidence stage |
| modify structure (수정(구조)) | A rule problem that remains whatever numbers you put in. Propose changing the rule and keeping the system |
| on hold (보류) | Stop progress and attach a revival condition. It must meet the minimum conditions of 6-2 |
| recommend removal (제거 권고) | Only when all minimum conditions of 6-3 are met |
| merge (통합) | A proposal to combine two systems whose roles overlap into one. It uses the same minimum conditions as recommend removal (judged for the side that disappears) |
| judgment withheld (판단 보류) | No verdict could be made because there is no material or the principles are not confirmed. Write the material needed |

### New ideas

| Verdict (판정) | Meaning |
|---|---|
| recommend (추천) | All minimum conditions of 6-1 are met |
| conditional recommend (조건부 추천) | The minimum conditions are met, but there are conditions for it to hold (for example: an implementation check, a performance measurement, a change to another system). Write the conditions |
| shelve (보관) | Do not proceed now. Write the revival condition and keep it only in the proposal record |
| do not recommend (비추천) | It conflicts with the principles or the prohibition principles, or the failure scenarios could not be rebutted. Write the reason |

### When to lower a verdict

- If the principles are "draft" (가안), write "based on draft principles" in the report head and give the verdicts as they are.
- If the principles are not confirmed (none, or the user refused), do not give verdicts, and leave all of them as "judgment withheld (principles not confirmed)" (판단 보류(원칙 미확정)).
- If the user is not the design decision owner, write every proposal as "reference option", and organize it in a form to pass to the decision owner.

## 5. Structure problems and numeric problems

- There is one question that separates them: **Does this problem remain whatever numbers you put in?**
  - If it remains, it is a structure problem. It becomes a target of modify structure, on hold, or removal.
  - If it goes away when the numbers change, it is a numeric problem. Give only modify numbers. Do not propose on hold or removal for a numeric problem alone.
- **Judgment that looks only at rules** — If the data is placeholder values (`design.data_status: 임시값`), do not do numeric calculations, and look only at the rules. Examples:
  - Does the rule of option A include all effects of B and add more? → Whatever the numbers, A is always equal to or better than B (dominance).
  - Does a risky action lose nothing by the rules even when it fails? → The risk is not a risk.
  - Do two systems give the same result for the same input? → Role overlap.
  This judgment rests on rules of the [document] grade, so its grade is [document]. Write "no-numeric-evidence stage" in the report head.

## 6. Minimum conditions

For each verdict, fill in the table below and attach it to the report. If even one condition is not met, you cannot give that verdict.

```markdown
| Condition (조건) | Met (충족) | Evidence location (근거 위치) |
|---|---|---|
```

### 6-1. Add (recommend, conditional recommend)

1. The pillar it strengthens, and a quote of that pillar's definition sentence or experience goal sentence. The result of checking the top-level principle and the prohibition principles.
2. Evidence that it is missing from the current design: at least one fact confirmed in this project's material ([document] grade or higher, with the location). "It is common in the genre" and "a competitor has it" are not evidence.
3. The loop it attaches to. If there is no place to attach it, why a new loop is needed.
4. The MDA chain and the scenario of a player who only cares about efficiency (for co-op or versus, also team scenarios).
5. History check: the result of looking for rejection records of the same idea in the proposal record and in the unadopted drafts folder. If it was rejected before, what changed since then.
6. Opportunity cost (what doing this postpones), the fun contribution and cost grades, and the evidence for each.
7. Verification method: the observation scene, and the direction that separates success from failure.

If they are not met, do not put it in the report proposals. Leave it in "Idea notes" of the proposal record.

### 6-2. On hold

1. Current state: the design document location and the implementation check stage.
2. At least one piece of problem evidence: one of [calculated], [observed-behavior], or [observed-opinion]. If it is the [document] grade, there must be a quote showing that it explicitly conflicts with the top-level principle, a pillar, or a prohibition principle. [estimated] alone is not enough.
3. Revival condition: what must be confirmed to proceed again, in a form that can be checked.
4. The other systems affected while it is on hold.
5. The design intent confirmation question was attached before the verdict.

### 6-3. Recommend removal (also the side that disappears in a merge)

It is hard to undo, so the bar is higher than on hold.

1. All five conditions of 6-2 are met.
2. Observation evidence: at least one [observed-behavior], or [observed-opinion] repeated in **at least two different builds**. Write the sample kind and the number of people with it. If neither exists, give at most "on hold" as the verdict, and give with it the observation items to use for checking.
3. Evidence of no pillar contribution or of a conflict. Show at least one of the three below, with evidence.
   - No pillar contribution: compare with the principle table of Step 1 and show that it does not reach any pillar's definition or experience goal sentence. An option that is dominated by another option and has no reason to be chosen ([calculated] or judgment that looks only at rules) also belongs here.
   - Conflict with the principles or the prohibition principles: quote the conflicting principle sentence and the system sentence together.
   - (The side that disappears in a merge) The remaining side already takes over that contribution: quote the evidence of both systems.
   "Its contribution is low compared to the maintenance cost" does not meet this condition. If only the cost is the problem, give at most on hold.
4. It was shown to be a structure problem (§5). If numbers solve it, it is not removal but modify.
5. Explanation of the gap: what takes over the loop that the system was attached to and the motivation it filled, or why it can stay empty. And the dependency scope — the list of code, data, and content that refers to this system. If you could not count all of them, give at most on hold.
6. The result of first writing the reasons to keep it as strongly as possible.

## 7. Fun contribution

| Grade (등급) | Condition |
|---|---|
| high (상) | It quotes which definition or experience goal sentence of which pillar it answers, and it changes the player's behavior in the scene where that goal applies, or it solves a structure problem that blocks that goal. The evidence must have at least one grade that is not [estimated] |
| medium (중) | It connects to a pillar, but the sentence to quote is indirect. Or it meets the conditions of "high", but its only evidence is [estimated] |
| low (하) | It connects to a pillar only indirectly (convenience features, long-term collection, and so on). Or it is outside the main motivations of the target player in the profile (only when there is a target) |

- Use the pillar priority only to decide the order within the same grade. Do not give "high" only because it reaches a pillar with high priority.
- Do not write effect sizes (predictions such as "churn down 20%"). Express the effect only as the success criterion of the verification method.

## 8. Cost

| Grade (등급) | Condition |
|---|---|
| S | Only existing data or settings values change. No new code and no new assets |
| M | An existing system is extended with some code, or a small amount of new assets from one discipline is needed |
| L | New system code is needed, or new assets from several disciplines are needed, or a change to another core system follows |

- **Raise one grade**: If new network synchronization is needed (check when profile `play_mode` is `협동`, `대전`, or `혼합`), or if existing content must be made again, raise it one grade. If you raise it from L, write "L+", and also give whether it can be split into smaller pieces.
- Write four pieces of evidence: the systems that change and their code locations (implementation stage), the kinds of new assets needed and the disciplines, whether network synchronization is needed, and whether existing content must be reworked. Cost is a rough estimate, so attach "responsible programmer must confirm". If the implementation scope or structure decides the grade, pass a question to td. If the "4. Option comparison" table of the td design review report (`td/<날짜>-decision.md`) has a "Changed scope" column, quote that value, its evidence mark, and qualifiers such as "partly counted" as they are.
- Do not write work days or headcount.
- **Performance cost**: For a proposal that increases the number of enemies on screen, the number of effects that go off at the same time, or the number of objects to synchronize over the network, attach "performance not checked" (성능 미확인) to the cost and request a measurement from perf. Do not remove this mark until the answer comes.

## 9. Priority

| Fun contribution \ Cost | S | M | L | L+ |
|---|---|---|---|---|
| high (상) | 1 | 1 | 2 (with a way to split) | 3 (a way to split is required) |
| medium (중) | 2 | 3 | shelve (보관) | shelve (보관) |
| low (하) | 3 | shelve (보관) | shelve (보관) | shelve (보관) |

- 1 = a candidate to check right away in the next playtest. Shelve = keep it only in the proposal record and do not put it in the report summary.
- If profile `dev_stage` is `알파`, `베타`, or `라이브`, or if the profile `feature_cutoff` date is before today, lower an **add** proposal with cost L or higher to "next-stage candidate" (다음 단계 후보) (shelve).
- **Self-rebuttal**: For each priority 1 or 2 proposal, write at least two "reasons this proposal could be wrong". If you cannot rebut them with evidence, lower the fun contribution by one grade and set the priority again.

## 10. Numbers that can be used in a report

There are only three kinds.

1. Project values with a location (data file:row, design document:line)
2. Calculated values whose formula, inputs, and command are shown
3. `[PLACEHOLDER]` proposed values with a reason

Do not use example numbers in manuals or design documents, test data, estimated numbers from source documents, industry statistics, or work days.
