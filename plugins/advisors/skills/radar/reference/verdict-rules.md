# Technology trend advisor verdict rules

When you rate one technology, fill the columns in the order of this file: announcement stage → our state → applicability → necessity → recommendation level (apply the cap rules) → cost → condition to revisit.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. The seven announcement stages

| Stage (단계) | Name (이름) | Original wording that puts a technology at this stage |
|---|---|---|
| ① | paper/research (논문·연구) | Conference papers, preprints (papers published before conference review), blogs of research groups |
| ② | announcement/demo (발표·데모) | Keynotes (the first main presentation of an event), roadmaps, demo videos, wording such as "예정", "coming", "planned" |
| ③ | in source only (소스에만 있음) | Merged into a development branch of a public source repository, but not in the official release notes |
| ④ | Experimental release (Experimental 출시) | An Experimental mark (experimental stage: the API and the data format can change) in the release notes, the official documentation, or the plugin file |
| ⑤ | Beta | A Beta mark in the same places |
| ⑥ | production ready (정식(Production Ready)) | A production-ready mark in the same places |
| ⑦ | use in a shipped title confirmed (출시작 사용 사례 확인) | A source states that a shipped game used the technology. Write it together with ④~⑥ (for example "⑥ + ⑦") |

- Decide the stage by **quoting an original sentence of a primary source in quotation marks**. If there is no sentence to quote, the stage is "unknown" and the recommendation level is "verdict withheld — not confirmed".
- Do not drop wording that narrows the scope ("only certain platforms", "for licensees (outside companies that use the engine)", "editor only"). Copy it together with the quote.
- Demos and roadmaps do not go above ②. "Support planned in the next version" is not support.
- For a source-build engine, write both the plugin file mark in the local engine tree (`IsExperimentalVersion`, `IsBetaVersion`) and the mark in the release notes. For a feature that is not a plugin, write in that place the maturity text in the console variable description or the header comment of the local source (sources.md §1). If the two differ, write that they differ, and judge applicability by the local tree.
- Do not use the maturity wording of secondary reports. Reports often leave out the mark or remove the scope limit. The same applies to community posts (sources.md §10).

## 2. Look at our state first

The handling depends on the five states in `_state/radar-inventory.md`. The script (`tech_inventory.py`) decides the state by the criteria below.

| State in the technology inventory (기술 목록의 상태) | Meaning (the criterion the script used) | Handling |
|---|---|---|
| in use (사용 중) | It is on, and the build settings of the game code (`*.Build.cs`) or the dependency list of the project file use a module of that plugin, or a settings file has a section of that plugin | Do not report it as a new technology. Write "already in use" in the recommendation level column, and write only what changed since our version (planned deprecation, API changes, maturity changes) and the response deadline |
| on, no sign of use (켜짐·사용 흔적 없음) | It is on, but none of the signs above were found. Use only in assets or in the editor cannot be checked as text, so this does not mean "not used" | Same as above |
| used with engine modifications (엔진을 고쳐서 씀) | It is on, and there are engine modification blocks inside that plugin folder. If the modification blocks were not counted or the search failed, do not read the absence of this state as "not modified" | Same as above. Write the number of overlapping modification blocks in the cost column |
| in the engine but off (엔진에 있으나 꺼짐) | The plugin file exists (in the engine folder or the project Plugins folder), but it is off. If the engine folder was not found, a plugin that the project file marks as off is also put in this state, and the evidence column says so. If the evidence column has "on by engine default, but the project turned it off" (`엔진 기본은 켜짐인데 프로젝트가 끔` in the script output), it was turned off on purpose | First find the reason it was turned off. If a reason is written in the "Our state" column of radar-watchlist, use it. If you find it, write it on the first line of the item and rate the technology. If you do not find it, the result is "verdict withheld — not confirmed" |
| none (없음) | The project file marks it as off but the plugin file was not found, or it was in the previous inventory and is gone this time | Rate it |
| A feature not in the technology inventory (an engine feature turned on by a setting, an engine default plugin used only in assets, and so on) | The script adds, among the engine plugins not in the project file, only the ones that the game code depends on or that have modification blocks. Being absent from the inventory does not by itself mean "none" | For a feature turned on by a setting, write both the project setting value (ini path:line in Config) and the engine default (path:line of the console variable definition in the local source). If the settings table does not have that key, find it with Grep or run Step 1 again with `--extra-key`. If both are off, do not look for the reason it was turned off, and rate it like "none". If the engine default is on but the project turned it off, look for the reason like "in the engine but off", and in this case look at the history of that settings file. If it is on, handle it like "in use". For a plugin used only in assets, check again in the engine tree and the project settings |

If the technology inventory could not be checked, do not give a recommendation level to any technology. All of them are "verdict withheld — not confirmed".

Do not use these rules to judge how to use a technology we already use (the first three states in the table above) in our code, or whether to replace our own implementation with that technology. The td design review handles it (`shared/routing.md`). The technology trend advisor writes only the outside changes of that technology and the response deadline.

## 3. The three verdict columns

### 3-1. Applicability — possible / conditional / not possible

| Value (값) | Condition |
|---|---|
| possible (가능) | It actually exists in our engine tree (write the path). Support for every target platform in profile `platforms` was confirmed with a primary source. It does not conflict with company policy |
| conditional (조건부) | Write what is needed: engine upgrade / backport (moving a fix from a new version onto our engine) / custom engine merge / platform support check / company policy check |
| not possible (불가) | It is blocked by one of license, platform, or policy, and there is evidence for it |

- For a source build, write "possible" only after you confirm that the plugin or module folder exists in the local tree, even if the version number is the same.
- A launcher install (installed engine) has no backport option. Write only the upgrade.
- Do not interpret license clauses. Point out only the clauses to check and their sources, and leave it as "conditional — license check needed" (조건부 — 라이선스 확인 필요).

### 3-2. Necessity — problem confirmed / problem expected / no problem

| Value (값) | Condition |
|---|---|
| problem confirmed (문제 확인됨) | There is evidence that can be linked: a ticket, a requirement in a design document (path:line), a perf measured value (report path and scenario ID) |
| problem expected (문제 예상) | The only evidence is what the user said or an estimate |
| no problem (문제 없음) | All other cases |

- "It looks good", "the whole industry uses it", and "a competitor used it" are not evidence of necessity.
- For a technology that touches game features (new movement, presentation, systems), take necessity only from design documents or from design's judgment. If there is no evidence, pass a question to design and leave it as "problem expected".
- Profile `radar.interests` is only areas of interest, not problems. Candidates that come from it start at "no problem".

### 3-3. Recommendation level

| Value (값) | Meaning | Conditions that must all be met |
|---|---|---|
| adopt (도입) | Put it into the current schedule and use it | Announcement stage ⑥ or higher. Applicability "possible". Necessity "problem confirmed". There is our trial result or a shipped case of similar scale that discloses its team size. The owner who will maintain it is confirmed. The way to roll back is written. None of the cap rules below apply |
| trial (시험) | Try it briefly within a set scope | Announcement stage ④ or higher, and it can be tried within a scope that can be turned off. Necessity is "problem confirmed" or "problem expected" (if the latter, put "check whether the problem actually exists" in the trial goal). All the trial plan columns of §8 can be filled |
| assess (검토) | Do not touch it now, and watch it | A condition to revisit must be written |
| hold (보류) | Decide not to do it | One of: applicability "not possible", the cost is larger than the gain by countable evidence, a conflict with the development stage, a policy violation, or the same problem is already being solved with another technology. Write the reason and the condition to revisit |

Two marks that are not recommendation levels:
- **already in use (이미 사용 중)**: the first row of §2 applies.
- **verdict withheld — not confirmed (판단 보류-확인 부족)**: one of the technology inventory, the primary source, or the reason it was turned off could not be checked. Write what must be checked to rate it and whom to ask.

## 4. Cap rules

The order of recommendation levels from high to low is adopt > trial > assess > hold. If several rules apply, use **the lowest one**, and write **all** the numbers of the rules that apply.

| Number (번호) | Condition | Maximum recommendation level |
|---|---|---|
| L1 | Necessity "no problem" | assess |
| L2 | Applicability "not possible" | hold |
| L3 | Announcement stage ①~③ | assess |
| L4 | Announcement stage ④ | trial if within a scope that can be turned off (per plugin, editor only, a separate map or branch), otherwise assess |
| L5 | The shipped case does not disclose its team size (scale unknown), or our team size is unknown so a comparison is not possible | trial. Do not use that case as evidence for "adopt" |
| L6 | Not in our engine version | assess until an upgrade is decided. trial once the scope to backport (commits, files) is confirmed |
| L7 | There is no primary source, and the only evidence is secondary | assess |
| L8 | Support is unconfirmed for at least one target platform | assess for a technology that runs during gameplay. Not applicable to editor-only tools |
| L9 | The owner who will maintain it is unconfirmed | trial |
| L10 | Default by development stage (§5) | the value in §5 |
| L11 | AI for development tools, and profile `radar.ai_tool_policy` is unconfirmed or empty | Do not rate it. Group the whole area into one line, "policy check needed" (정책 확인 필요) |
| L12 | The only evidence for necessity, for shipped cases, or that it solves the problem is community posts (sources.md §10) | assess |

To judge "similar scale", our team size is needed. Read it from profile `team_size`. If it is empty (no answer was given in Step 0, or it is an unattended run), do not compare, and apply L5. The advisor does not decide how different the scale must be to count as "not similar". Write the scale of the case and our scale side by side. To give "adopt" only from a shipped case without our trial result, put that comparison in "Decisions needed" so that a person looks at it.

## 5. Defaults by development stage

Decide by profile `dev_stage`. If the team wrote a different criterion in the profile notes, follow it and write that in the report.

| Development stage (`dev_stage`) | Default |
|---|---|
| `프리프로덕션` (preproduction) | Use only the cap rules |
| `본 제작` (production) | A technology replacement that spreads across the content (global illumination method, shadow method, network replication method, animation system, material system, and so on) has a maximum of trial, with "lead agreement needed" (리드 합의 필요) attached |
| `알파`·`베타` (alpha, beta) | A new technology is hold by default. The only exception is when it solves a problem that blocks release (crashes, platform certification, missing the performance target) with measurement evidence, and even then the maximum is trial |
| `라이브` (live) | Engine upgrades and replacement of systems that run during gameplay have a maximum of trial. In the cost column, write the patch schedule and platform recertification as items to check |
| Empty | Do not give an "adopt" verdict (the maximum is trial). Write it in "Not checked" of the report |

## 6. Write cost in countable units

- Version difference: our version → the version that has the feature
- The engine folders that the feature touches and the number of engine modification blocks in them: the result of `tech_inventory.py --mod-only --mod-dirs <폴더>`
- Number of affected project files: write the search expression and the result count together
- Scope of assets that must be saved again: kind and folder. Write the count only when it can be counted
- Affected job roles
- Way to roll back: a setting that turns it off, turning off per plugin, a branch
- Write the duration (person-days) with "estimated" attached only when there is evidence. If there is no evidence, it is "unknown". Do not make it up.

## 7. AI for development tools and in-game AI

The two have different criteria, so do not mix them.

**AI for development tools** (coding assistants, asset generation tools, tools that connect to the editor)
- If profile `radar.ai_tool_policy` is `미확인` (unchecked) or empty, group every item of this area into one line in the report: "AI for development tools — policy check needed (N items held)" (개발 도구용 AI — 정책 확인 필요(N건 보류)). Do not write individual verdicts.
- If the policy is `허용` (allowed) or `제한` (restricted), check: whether the scope of material sent outside is within the policy, the commercial license, and whether it overlaps with the tools we use now (related plugins in the technology inventory and the project's AI tool settings files).
- Write prices only as "public price as of the check date" (확인일 기준 공개 가격), and do not use them in the recommendation level. Do not make purchase decisions.

**In-game AI** (models that run during gameplay: dialogue, behavior, animation generation, and so on)
- It touches features, so pass the fun judgment to design.
- In the technology columns, check: inference cost per player (public price and check date; calculate with Bash), response latency, offline behavior, platform certification, the way to filter inappropriate output, and the store's disclosure duty (only as a condition to meet). If even one of them is unconfirmed, the maximum is assess.
- For a recommendation tied to a specific model name, check the retirement schedule of that model and write it in "condition to revisit".

## 8. Trial plan (only when the recommendation level is "trial")

| Column (칸) | How to write it |
|---|---|
| Scope (범위) | A unit that can be turned off (plugin, editor only, separate map, branch) |
| Duration (기간) | A value that the user or the lead decides. The advisor leaves it as "to be decided" (정할 것) |
| Success criteria (성공 기준) | Metric and target. Hand performance metrics over as a perf measurement request (scenario ID, platform, metric, comparison before and after turning it on) |
| How to turn it off and roll back (끄고 되돌리는 방법) | The setting name or plugin name. Only confirmed names |
| Problem to check (확인할 문제) | If necessity is "problem expected", put in "check whether the problem actually exists" |

## 9. Conditions to revisit and changes to the recommendation level

- For each assess or hold item, write a condition to revisit. Write it as an event rather than a date. Examples: "when the release notes of the next engine version mark it Beta or higher", "when a perf measurement confirms that the shadow pass time exceeds the budget". Use a date only when there is no event to write.
- Do not change only the recommendation level without a new source or a new fact on our side. This prevents the verdict from going back and forth on the same facts. If you changed it, record the evidence for the change in "Change log" of `radar-watchlist.md`.
