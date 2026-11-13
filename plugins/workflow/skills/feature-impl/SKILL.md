---
name: feature-impl
description: "The single entry point for requests to implement or change code. First decide the size (Small / Large), the work type (feature / improvement / bug), and the risk level (low / mid / high). Then go through the Fast Lane or the Full Lane, and finish with a checkpoint that suggests documents, commit, issue, and handoff note. Use it for every code change request: new features, bug fixes, value tuning, variable renames, and requests with '살짝', '간단히', '수치만', '빠르게', '조금만'. Not for: choosing the next work and making issues (next-task), document-only changes, code review only."
when_to_use: "When you get a request to change code in a project that has a workflow profile. It also works without a profile. Then it first asks whether to make a profile."
argument-hint: "[#issue number] <request>"
---

# Feature Implementation (path by size)

This is the combined skill for requests to implement or change code. Step 0 decides the size and goes to the **Fast Lane (Small)** or the **Full Lane (Large)**. Both paths end with the **Step Final checkpoint**.

This skill does not replace the project instructions. If they conflict, **the project instructions win.**

## Paths and profile

- Plugin folder: `${CLAUDE_PLUGIN_ROOT}`
- Project root: `${CLAUDE_PROJECT_DIR}`

If the values show as variable names, the plugin folder is two levels above this SKILL.md, and the project root is the folder where the session started.

The profile is `<project root>/.claude/workflow/profile.md`. Personal values are in `profile.local.md` in the same folder. The templates are `<plugin folder>/shared/profile-template.md` and `profile-local-template.md`.

- **If the profile exists**, read it. Keys used in this skill: `instructions`, `scope_sections`, `coding_rules`, `source_roots`, `risk_paths`, `tracker`, `tracker_repo`, `tracker_public`, `status_labels`, `threads_dir`, `verification`, `build_commands`, `test_setup_mcp`, `test_candidates`, `agent_review`, `review_guide`, and the "Design checklist" section of the body (older profiles: "설계 점검 항목").
- **If there is no profile**, ask: "이 프로젝트에 workflow 프로필이 없어요. 만들까요?" If the user agrees, fill in the values that the project instructions (`AGENTS.md`, `CLAUDE.md`, `README.md`) and the folder layout show, marked `[file]`, and ask for the unknown values in one message. If the user says no, continue with these defaults: no issue tracker, no handoff note, the user does verification.

Speak to the user in the language of the conversation. The quoted messages below are examples in Korean. Write handoff notes, code comments, and commit messages in the languages that the project instructions set.

---

## Common rules (both paths)

### Scope

- Do not copy the scope, structure, or module boundaries into this skill. Each time, use the instructions that profile `scope_sections` points to.
- The priority of evidence follows the project instructions. If the instructions do not set it, use this order.
  1. The current request of the user and decisions that the user confirmed explicitly
  2. The structure and boundaries in the project instructions, and the documents that describe current usage
  3. Open issues and the design documents that they link
- Do not use a discarded pre-implementation design document as the current specification. **Do not implement a feature that the user did not ask for, or a design that is not decided.**

### Coding rules

- Follow the rules that profile `coding_rules` points to. Do not copy the rules into this skill.
- If there are no rules, follow the surrounding code for naming, comment density and language, indentation, encoding (with or without BOM), and line endings.
- When the behavior of a function, property, type, or tag changes, update the description comment of that declaration in the same edit to match the current behavior. Include comments that show as editor tooltips, and tag descriptions (such as `DevComment`). When a name changes, also update the comments that mention that name.

### Version control rules

- **Before you start, check the current state with `git status --short`.** Do not overwrite or revert uncommitted changes of other people.
- Make only the changes that the request needs. If you see work in progress on the same file, check its current state, then continue.
- **Commit and push only when the user asks.** Do not commit automatically because the implementation is done. The commit scope and targets follow profile `commit_policy`.

### Verification owner

- If profile `verification` is `user`, or there is no profile, **the user does builds, tests, lint, and static analysis.** Run them only when the user asks explicitly.
- The agent review (L6) only reads code, so it is separate from this rule. Follow profile `agent_review`. If the key is missing or there is no profile, the review is on. The review agents also do not run builds or tests.
- Do not add or extend test code only because of a feature request. Write only the tests that the user chose from the "Test candidates" of the decision card. Do not make a copy of the project or a separate test environment for verification.
- Do not force-quit the editor or user processes.
- When you ask the user to build, give the profile `build_commands` if they exist.
- **In the completion report, write only what was actually verified.** Do not report a check that did not run as successful.

### Step header

At the start of each step, print a header line.

```
[Fast F2/3] Fix
```
```
[Full L3/7] Implementation plan + thread save
```

### Trial and error log

Collect error fixes, non-obvious decisions, and avoided traps **in "Notes" of the handoff note** (`<threads_dir>/<thread-name>.md`; older notes: "참고 사항"). For the other Korean headings of older notes, see `context-handoff` Step 3. Later, `feature-doc-sync` moves the items worth keeping to a devlog.

---

## Step 0 — Entry, and decide size, type, and risk level

> **Done by: the orchestrator (directly)**

Analyze the request of the user and decide three axes: **size + work_type + risk level**. The three are independent.

### A. Size

| Size | Criterion | Path |
|---|---|---|
| **Small** | Value tuning, variable rename, a 1 to 2 line fix, a simple bug fix in one file | → Fast Lane |
| **Large** | New feature, several files, crosses a module boundary, needs a design decision | → Full Lane |

If it is not clear, ask briefly.

> "이거 Fast lane (소규모) 갈까요, Full lane (큰 작업) 갈까요?"

Medium work goes to the Full Lane. If the user says "여기서 끊자" during the work, go to Step Final at once.

### B. work_type

Guess it from the conversation. If it is not clear, give candidates and get confirmation.

| work_type | Effect |
|---|---|
| **`feature`** (new feature) | Full Lane standard. L1 strongly recommended. Strongly suggest a manual update in Step Final |
| **`improvement`** (improve existing behavior) | Depends on size. The test guide stresses regression checks. Suggest a manual **update** in Step Final |
| **`bug`** (bug fix) | Skip L1 automatically, with a safety message. Focus on the reproduction scenario. A manual update is usually not necessary |

### C. Risk level

The change itself sets the level. Size and author (user or agent) do not matter. A one-line fix that changes a saved data format is high.

Use the first level that matches, from the top.

| Level | Criterion |
|---|---|
| **high** | The change touches a file that matches profile `risk_paths.high`. Or, independent of the path: a change to a saved data format or to the name of a serialized type, a change to build, CI, or release settings, code that deletes or overwrites user data, or a new shared structure that later code will copy |
| **low** | All changed files match `risk_paths.low`. Or the change is only documents, comments, or UI text, only test code, or only code behind a feature flag that is off by default |
| **mid** | All other code changes |

- Give each file a level, and use the highest one. If it is not clear, use the higher level.
- If the planning or the implementation adds files to change, decide again. If the level goes up, tell the user.

The level sets the depth of the agent review (L6) and what a person must read.

| Level | Agent review | What a person reads |
|---|---|---|
| low | Skipped | Evidence such as build and test results |
| mid | Standard: 1 reviewer | Evidence + code parts that contain judgment |
| high | Deep: 2 reviewers in parallel + verifier | Evidence + the whole change (with a reading order) |

Report the result in one line.

```
Large · feature · risk high (Source/Save/SaveGame.cpp: saved data format)
```

### D. Issue link

If profile `tracker` is not `github`, skip this step (`jira` is read only by `work-start` now). If it is `github`, the issue is the reference for work in progress. **An issue is required for Large and optional for Small.**

1. If the user gives an issue number, read it with `gh issue view <N>` and continue that issue.
2. If there is no number, look for an open issue with a matching topic.
   ```bash
   gh issue list --state open --search "<keywords>" --limit 10
   ```
   If there is a candidate, confirm: "#N `<제목>` 이어서 할까요?"
3. If no issue matches, make a draft with **B. Make a new issue** of the `next-task` skill. Show the draft and post it after confirmation.
4. If the user says "이슈 없이", continue without an issue. If the user later says "이슈로 만들어", go to 3.

When the work starts, ask whether to add the profile `status_labels.in_progress` label (only if the label is set).

### E. Handoff note

The handoff note is a **local session record** that supports the issue. Its name is `<threads_dir>/<issue number>-<slug>.md` (`<slug>.md` if there is no issue). If there is no profile, do not write a handoff note.

- If a matching file exists, continue it. If an existing file has no issue number, suggest a rename.
- If there is none, the Full Lane makes it in L3. The Fast Lane does not make one.
- If the work has neither an issue nor a handoff note, skip the handoff and issue suggestions of Step Final.

---

# Fast Lane (Small)

Finish quickly in 3 steps. Skip the planning, design, and test guide steps. Do the agent review only for risk high (at the end of F2).

## Step F1 — Find the change location

> **Done by: the orchestrator (directly)**

- Read the files and lines that the user pointed to.
- Confirm the intent of the change. If it is not clear, ask 1 or 2 questions, then continue.

## Step F2 — Fix

> **Done by: the orchestrator (directly)**

- First check with `git status --short` whether the file has uncommitted changes.
- Make the fix with the coding rules. Do not touch anything outside the request.
- For risk high, do a Deep review with the procedure of Full Lane L6. The order with the build also follows L6. The intent input is one or two lines of the request. Do not review low or mid.

## Step F3 — Ask for a build check

> **Done by: the orchestrator (directly)**

If the user does verification:

> "수정 완료. 빌드 결과 알려주세요."

**Do not build yourself.** If the user reports an error: analyze → fix → ask for a new build. "통과" or "에러 없음" → **Step Final**. If profile `verification` is `agent`, check with `build_commands` yourself and report the result as it is.

---

# Full Lane (Large)

## Agent strategy

A subagent starts without context. So by default, use subagents only for exploration that reads widely and returns only the result. The orchestrator does the planning and the implementation directly, because they need the decisions confirmed in the conversation and the detailed rules of the instructions. Use of this skill is itself a request to use subagents as the table below shows. If the user does not want subagents, or the environment cannot use them, do L2 and L6 directly too.

| Step | Done by | Reason |
|------|-----------|------|
| L1. Requirements | Orchestrator | Conversation with the user |
| L2. Codebase exploration | Exploration agent (fast model; Explore for Claude). Directly, if only a few named files are necessary | Receive only the result of a wide search, and save the main context |
| L3. Implementation plan + save | Orchestrator | Confirmed decisions, instructions, and conversation context set the quality of the plan. A planning agent that receives only a summary loses this context |
| L4. Confirm decisions and feedback | Orchestrator | Conversation with the user |
| L5. Implementation | Orchestrator, in implementation order. Parallel implementation agents only under the condition below | Files that depend on each other (declaration and implementation, includes, generated code macros) easily go out of sync when written separately, and the user pays for that with build time |
| L6. Agent review | Review agents (general-purpose subagents that start without context) × the number for the depth. The orchestrator handles the findings | A reviewer that is not pulled by the implementation context reads the change. Fixing needs the conversation context |
| L7. Error fixes + test guide | Orchestrator | Conversation with the user, run environment |

Condition for parallel implementation agents: the "Parallel implementation groups" of the plan contain several files that do not reference each other, and the plan gives complete implementation instructions for each file (for example, independent data files, or unrelated tool scripts). Even then, give a declaration and implementation pair of the same module to one agent.

## Step L1 — Requirements

> **Done by: the orchestrator (directly)**

### When work_type is `bug`: skip automatically, with a safety message

> "bug 타입 — 요구 정리는 건너뛰고 재현 시나리오부터 갑니다. 필요하면 알려주세요."

If the user says nothing else, go to L2.

### Standard L1

Follow the priority of evidence in the common rules.

```
## Requirement summary: [feature name]

### Purpose
### Core behavior
### Data / parameters
### Exceptions / edge cases
### Open or unclear items
```

After the summary, ask for confirmation. After confirmation, go to L2.

## Step L2 — Codebase exploration

> **Done by: the exploration agent**

Give the exploration agent:

- The full L1 requirement summary
- Search targets: related classes, components, and subsystems, dependent systems, and existing patterns to reuse
- Search scope: profile `source_roots` (if empty, the whole repository without generated and vendor folders)
- Boundary check: which module or area this change belongs to, and whether it breaks the dependency direction of the project instructions
- Design questions: the open items of L1 and the choices you already see (for example, which framework draws a UI, which system owns a state). For each, the base that the project already has (base classes, frameworks, managers, conventions) and the files that show how it is used
- Thoroughness: the most thorough

Result format:

```
## Codebase exploration result

### Related files
### Existing structures to reuse
### Existing bases for each design question
### Dependencies to watch (including module boundaries)
```

Go to L3 automatically.

## Step L3 — Implementation plan + thread save

> **Done by: the orchestrator (directly)**

Write the plan from the L1 requirement summary, the L2 exploration result, the coding rules, and the "Design checklist" of the profile body. If an exploration result looks wrong, read the file yourself and check. Before you recommend an option for a decision, read yourself the files and documents behind its reasons ("Evidence for a recommendation" below).

The plan has two layers. **Show the user only the decision card.** Keep the detailed plan, such as the file tables and the implementation order, in the handoff note. The user must judge decisions and risks. A file list is not material for that judgment.

### Decision card (show it in the conversation)

Write the card in the language of the conversation, and translate the labels.

```
## Implementation plan: [feature name]
Large · <work_type> · risk <level> (<files and reason>)

### Intent
<3 lines or fewer. What changes, and how>

### Decisions
**D1. <question for the user>**
- Recommended: <option>: <result>
  - Why: <the deciding reason> [<source>]
- Alternative: <option>: <result>
  - Better if: <the condition under which this option wins>

### What can break, and how to check
| # | What can break | How to check |
|---|---|---|
| R1 | | |

### Test candidates
| # | Target | Criterion | What to assert | Recommendation |
|---|---|---|---|---|
| T1 | | | | |

### Slices
| # | Content | How to check |
|---|---|---|
```

- Fit the card on one screen. If it does not fit, there are too many decisions, or the slices are too large.
- **Decisions**: write only items that have real alternatives with different results. Items that the instructions or the existing code already set are not decisions. Write each question with behavior and results, in words that the user can answer, not with file or function names. If there are no decisions, write "No decisions". Each recommendation needs a `Why` line with a source, and each alternative a `Better if` line. Follow "Evidence for a recommendation" below.
- **What can break**: items found while you check "What the plan must check" below, and places where this change can break existing behavior. In "How to check", write a means that actually finds the problem, such as the build or an item of the test guide. If there is no such means, write "Person checks: <what>". Use the same R numbers in the test guide and in the handoff note.
- **Test candidates**: if profile `test_candidates` is empty, leave out this section. If it has values, list only code that is new or changes behavior in this work and that matches those criteria. Write the matching criterion in the `Criterion` column. If nothing matches, write "No test candidates". `What to assert` is what the test checks, such as the input and the expected result, or a resource that must not remain after repetition. `Recommendation` is one of `this work`, `follow-up issue`, or `none`. Do only what the user chooses. `this work` goes into the implementation order of the detailed plan. `follow-up issue` goes to the follow-up issue draft of Step Final 3). Do not write a candidate that the user did not answer.
- **Slices**: follow "Slicing" below. If there is only one slice, write "One implementation" in place of the table.

### Evidence for a recommendation

A recommendation is only as good as the reasons behind it. If the reasons are not written down, a later question cannot be checked against them, and the recommendation changes with the mood of the conversation.

Tag each reason with its source:

| Tag | Meaning |
|---|---|
| `[code <file:line>]` | Code that you read yourself in this session. An exploration summary is not a source; the file it points to is |
| `[doc <path or URL>]` | A project document, engine documentation, or another document that you read |
| `[profile]`, `[instructions]` | The workflow profile or the project instructions |
| `[user <date>]` | A decision that the user confirmed |
| `[assumption]` | Not checked |
| `[agent convenience]` | Helps the agent, not the product: no assets needed, can be checked without the editor, fewer files to write |

Before you show the card:

1. Read the code or document behind each reason of each recommendation yourself.
2. Check whether the project already has a base for the decision area: a base class, a framework, a manager, a convention. An option that ignores an existing base needs a reason for that.
3. An `[assumption]` cannot silently be the deciding reason. Check it first. If you cannot, make it a question for the user (a decision of its own, or an open item). If a later decision settles it, write in the `Why` line that the recommendation depends on it: `Why: ... [assumption: 결투에서 빙의하지 않음. U2에서 결정]`.
4. An `[agent convenience]` reason cannot be the only reason. If it is one of the reasons, say what it costs the product.
5. If the evidence does not separate the options, say so in the `Why` line, and recommend the option that is cheaper to change later.

Save every reason with its source in "Design decisions" of the detailed plan.

### Slicing

Split the work into slices if there are more than 5 decisions, more than 6 items that can break, or the decision card does not fit on one screen.

- You must be able to build, test, and commit each slice separately. With only one slice applied, the project builds and the existing behavior stays.
- Order the slices so that each one is the base for the next (for example, data structure → behavior → UI).
- Get the decisions once for the whole work. Implement each slice through L5 → L6 → L7 → the commit suggestion of Step Final, then go to the next slice.

### Detailed plan (keep it in the handoff note)

If there are slices, split the file tables and the implementation order by slice.

```
## Implementation plan: [feature name]

### New files
| File path | Module or area | Role |

### Changed files
| File path | Module or area | Change |

### Implementation order
### Parallel implementation groups
### Design decisions
### Lifetime and resource cleanup review
### Open questions
```

In "Design decisions", write for each decision: the options, the recommendation, every reason with its source tag, and the `Better if` condition of each alternative. After L4, add the confirmed option. If a recommendation changes, keep the old one, and write the reason that failed and the evidence that replaced it.

What the plan must check:

- Each line of the profile "Design checklist".
- Shared settings and assets are separate from runtime state. Shared objects do not store runtime time, target records, or handles.
- Condition checks have no side effects.
- Running work releases acquired resources and event subscriptions on completion, cancel, interrupt, and owner destruction. Reference lifetime and memory management (GC, reference counts, and similar) are reviewed.
- If a path, module name, or serialized type name changes, saved data and redirects from the old name are checked.

Put each problem found in these checks in "What can break" of the decision card.

### Save to the thread file

When the plan is written, save the full detailed plan in the `## Implementation plan` section of the handoff note, and the "What can break" table in the `## Risks and checks` section (older notes: `## 구현 계획`, `## 위험과 검증`). If the file does not exist, make it with `<plugin folder>/shared/thread-template.md`. If you do not write a handoff note (no profile), show the detailed plan when the user asks for it.

> "구현 계획을 `<threads_dir>/<name>.md` 에 저장했습니다."

If there is an issue, after the decisions are confirmed, show a **summary** of the plan (scope, confirmed decisions, completion conditions) as an issue comment draft, and ask whether to post it. For design details, only link the design document if there is one. If `tracker_public` is true, do not include local paths or trial and error.

### End of the plan output

> "결정 D1~Dn 에 답해 주세요. 추천안대로면 **'추천대로'** 라고 하셔도 됩니다."

If there are test candidates:

> "결정 D1~Dn 과 테스트 후보 T1~Tn 에 답해 주세요. 테스트 후보는 `이번 작업`·`후속 이슈`·`안 함` 가운데 고르시면 됩니다. 모두 추천안대로면 **'추천대로'** 라고 하셔도 됩니다."

If there are no decisions:

> "결정할 것은 없습니다. 위험과 조각을 보시고 괜찮으면 **'구현 시작'** 이라고 말씀해 주세요."

If there are no decisions but there are test candidates:

> "결정할 것은 없습니다. 테스트 후보 T1~Tn 을 `이번 작업`·`후속 이슈`·`안 함` 가운데 골라 주세요. 추천안대로면 **'추천대로'**, 테스트 없이 구현하려면 **'구현 시작'** 이라고 말씀해 주세요."

## Step L4 — Confirm decisions and feedback

> **Done by: the orchestrator (directly)**

- When you get the answers, write the confirmed result of each decision (`D1: recommended option confirmed`, `D2: alternative confirmed: <reason>`). Also write the result for the test candidates (`T1: this work`, `T2: none`).
- If the answers change the plan, show the whole decision card again. Mark the changed items with `*`. If nothing changed, report only the confirmed results in one line.
- Put the feedback in the matching part of the decision card or the detailed plan.
- Also update the `## Implementation plan` and `## Risks and checks` sections of the handoff note (older notes: `## 구현 계획`, `## 위험과 검증`).
- If decisions or test candidates are still not answered, ask only about those.

### Questions and pushback on a recommendation

A question about a recommendation is not an answer to the decision, and it is not disagreement.

- **"왜 이걸 추천했어?", "근거가 뭐야?"**: answer with the saved reasons and their sources. Do not change the recommendation in that reply. If you find that a reason was not checked, name it, check it, and then say whether the recommendation stands.
- **A counterargument**: decide its kind before you answer.

| Kind | Example | Handling |
|---|---|---|
| New fact | "그 클래스는 다음 달에 없어져", "결투에서는 빙의 안 해" | Check it if you can (code, document, issue). If it holds, change the recommendation. If you cannot check it, say so, and ask whether to use it as a premise |
| Different priority | "디자이너가 에디터에서 고칠 수 있어야 해" | The user decides priorities. Confirm the alternative, and record `D1: alternative confirmed: user priority <X>` |
| Misunderstanding of an option | The user reads the option as something it is not | Correct the description with the evidence. Keep the recommendation, and ask again |
| No new fact | "그래도 B가 낫지 않아?" | Keep the recommendation. Give the deciding reason in one line, and say what evidence would change it. If the user still chooses B, that is a decision: record `user choice` |

- When you change a recommendation, name the reason that failed and why: `근거 2(결투에서 빙의)는 확인하지 않은 가정이었고, U2에서 정할 일이라 근거로 쓸 수 없다`. Do not write only "근거가 약했다".
- When you keep a recommendation, say why the counterargument does not change the conclusion.
- Record each change in "Design decisions" of the handoff note: the old recommendation, the reason that failed, the new recommendation and its evidence.

When all decisions are confirmed and the user says **"구현 시작"** or **"추천대로"** → L5. "추천대로" confirms all decisions and test candidates with the recommended options. If you get "구현 시작" while answers are missing, say in one line that the remaining decisions take the recommended options and the remaining test candidates take `none`, then go to L5.

## Step L5 — Implementation

> **Done by: the orchestrator (directly). Implementation agents × N only for the groups that meet the condition**

- By default, implement directly in the implementation order of the plan. When you change a declaration, update the implementations and the call sites that use it in the same flow.
- Give only the groups that meet the parallel condition of "Agent strategy" to implementation agents. Files in a group run at the same time. Groups run one after another. Give each agent the implementation instructions for its files, the contents of the dependent files, and the coding rules. When you get the result, read it yourself and check that it fits the neighboring files.
- **No changes outside the plan.** If you find something outside the plan, put it in the result and report it to the user.
- If the work has slices, implement only the current slice.
- If the files to change are more than the plan says, decide the risk level again with Step 0-C. If the level goes up, stop and tell the user.

When you finish, go to L6 at once. The build request follows the order of L6.

## Step L6 — Agent review

> **Done by: review agents × the number for the depth. The orchestrator handles the findings and the review packet**

Before a person reads the change, review agents without context read it. The review procedure and the output format are in `<plugin folder>/shared/review-brief.md`. If profile `agent_review` is false or the risk is low, skip the review, and write that on the first line of the review packet.

### L6-1. Order with the build

| `verification` | Order | Reason |
|---|---|---|
| `user` (or no profile) | Review → handle findings → ask for a build together with the review packet | One build also checks the fixes from the review. The number of user builds does not go up |
| `agent` | Build and test with `build_commands` → if they pass, review → handle findings → build and test again only for the changed parts | The expensive review does not look for problems that a cheap and deterministic check finds |

### L6-2. Depth and reviewers

Step 0-C risk level sets the depth.

| Depth | Reviewers | Check of findings |
|---|---|---|
| Standard (mid) | 1 reviewer with focus `all` | The orchestrator reads the `file:line` of each finding and checks it before handling it |
| Deep (high) | 2 reviewers with focus `correctness` and `failure types`, in parallel in one message | 1 verifier agent merges the two results and checks each finding (review-brief.md section 8) |

Give each reviewer the path of review-brief.md and the input of its section 2. If profile `review_guide` has a value, give that path.

If subagents cannot be used, the orchestrator reviews directly with review-brief.md, and writes "not a review without context" in the review packet.

### L6-3. Handle findings

Close every finding. Fix it, or write the reason.

| Category | Handling |
|---|---|
| `Important` | Fix it. If you decide that the reviewer is wrong, do not fix it and write the reason. If the fix needs a large change outside the plan, do not fix it and ask the user |
| `Nit` | Fix only what you can fix at once inside the changed lines. Close the rest as "Nit: skipped". If you fixed only Nits, do not run another round |
| `Pre-existing` | Do not fix it in this change. Write it in the review packet, and if there is an issue tracker, suggest a follow-up issue |

If a finding covers a bug type, fix all its locations at once.

### L6-4. Next round

If you fixed at least one `Important`, run the next round. **From round 2, the review reads only the changes** (review-brief.md section 6).

- **Send the next round to the reviewer of the previous round** (SendMessage for Claude). This keeps the reviewer from reading the same code again. For Deep, continue each of the two reviewers and the verifier agent.
- The input is the base of the fix diff and the handling of each finding (fixed / not fixed, with a reason).
- If you cannot continue the reviewer (the environment does not support it, or the previous reviewer cannot be called again), start a new reviewer with the same depth and focus, and also give it the full result of the previous round.

If one of these is true, read the round 1 scope again even in round 2 or later. Write the reason in the review packet.

- The fix changed the design (a decision of the decision card changed, or a new structure came in).
- The fix touched a file that was not in round 1.
- The fix diff is half of the original diff or larger.

**If an `Important` remains after round 3, stop the review.** Tell the user that the approach needs a new look, with the remaining findings, and ask whether to continue.

### L6-5. Record

For each round, write one row in the `## Review log` table of the handoff note (older notes: `## 리뷰 기록`): round, scope, depth, number of new problems, handling. If there is no handoff note, write it only in the review packet.

### L6-6. Review packet

After the review, give the packet to the user. In place of diagrams or a description of the whole change, show only the places where a person must judge. Write the packet in the language of the conversation, and translate the labels.

```
## Review packet: [feature name]
risk <level> · review <depth / skipped (reason)> · <N> rounds · new problems per round <round 1 a, round 2 b>

### Intent
<Intent of the decision card. One line for each confirmed decision>

### Where to look
| # | file:line | Why to look | Related |
|---|---|---|---|

### What the review found
| ID | Category | Bug type | Location | Handling |
|---|---|---|---|---|

### What checks cannot find
- <What neither the review nor builds and tests can check, so a person must judge>
```

- **Where to look**: for mid, 2 to 5 code parts that contain judgment (where a decision is implemented, where a risk R item applies). For high, list the whole change in reading order. For low, write "None: check the evidence only". Write the D and R numbers in the "Related" column.
- **What checks cannot find**: do not leave it empty. If there really is nothing, write the reason in one line.

Closing message:

> "구현과 리뷰 완료. 빌드 후 에러 있으면 알려주세요."

For a slice, say `구현과 리뷰 완료 (조각 N/M)`. If `verification` is `agent`, add the build and test results and go to L7-2.

## Step L7 — Error fixes + test guide

> **Done by: the orchestrator (directly)**

### L7-1. Error fixes

If the user reports a build error: analyze the cause → explain the fix → fix → ask for a check. If the user does verification, **do not build yourself.**

Do not review build error fixes again. If a fix changes behavior (more than a fix to make it compile), review only that fix as the next round of L6-4. This round also counts toward the limit of 3 rounds.

### L7-2. Test environment setup (when MCP is available)

If profile `test_setup_mcp` is empty, skip this step. If it has a value, check **before** you give the test guide whether you can do part of the setup for the user.

1. Check whether that MCP server is connected and what it can do. If it is not connected or has no related function, skip this step.
2. Choose the items that you can do, and **ask**.
   > "MCP 로 이런 셋업을 대신 할 수 있어요: (예) 테스트 맵 로드 / 오브젝트 생성 / 실행 시작. 해드릴까요?"
3. If the user approves, run it and report the result. If the user says no, keep that step in the manual guide.

Always keep real operation and visual checks in the manual guide.

### L7-3. Test guide

| work_type | Core checks |
|---|---|
| `feature` | Feature check + edge cases + data flow (all) |
| `improvement` | The above + **regression check** (the behavior before the change stays) |
| `bug` | **Reproduction scenario → try to reproduce after the fix → check normal behavior** first |

Include every item of "What can break" in the decision card whose check is a test, and write its number in the `R` column.
For each test candidate of the decision card that this work wrote, add the test name and how to run it to the test guide, and write its `T` number in the `R` column.

Write the guide in the language of the conversation, and translate the labels.

```
## Test guide: [feature name]

### Test environment
### Normal behavior checks
| # | Check | Test condition | Expected result | R |

### Edge case checks
| # | Situation | How to test | Expected result | R |

### Data flow checks
| # | Check point | Expected value or range | Log needed | R |
```

If a log is necessary, add a temporary log after the user approves. When the check ends, ask whether to remove it.

> "위 항목을 테스트해 주세요. 결과 알려주시면 수정하겠습니다."

**"테스트 완료"** or **"통과"** → set the state of the matching R items in `## Risks and checks` of the handoff note (older notes: `## 위험과 검증`) to "checked", and go to **Step Final**.

---

# Step Final — Checkpoint (both paths)

If the work has slices, go through this checkpoint for each slice. After the commit, if slices remain, go to L5 of the next slice. You can do the documentation and the handoff once, in the last slice.

### Description comment check: first, when the implementation ends or before you wait for confirmation

Before you ask the user for a build or run check, read the description comment of each declaration whose behavior changed in this work, and check that it matches the current behavior. If it does not match, fix it in the same work. Then a comment fix does not need another build. Just before the commit, `commit-doc-review` checks the same comments again.

If a public API, UI, setting, or run procedure changed, update the related manual in the same work. Do not postpone a document update that the user already asked for until a follow-up question.

At the end of the work, suggest the four items below. When the user answers, call the matching skill or skip it.

### 1) Documentation

> "이번 변경에 영향을 받는 manual·devlog 를 정리할까요?"

- Do not make a document that summarizes the whole state. Update only the affected documents. `feature-doc-sync` does the actual work.
- `feature` → devlog + manual strongly recommended
- `improvement` → manual **update** recommended
- `bug` → only the reproduction, fix, and confirmation state of the linked issue, and the affected documents. If the fixed bug was in code that passed the agent review, suggest a line for the "Missed bug log" of `review_guide` and a change to its "Failure types by area" table (older guides: "놓친 버그 기록", "영역별 실패 유형")

### 2) Commit preparation

> "커밋할까요? 원하시면 변경 이유와 검증 상태를 담은 커밋 메시지를 먼저 보여드립니다."

- **Ask first. Do not commit automatically.**
- Just before the commit, check with `commit-doc-review` that the related documents are updated, and add the profile `commit_trailer` trailer to the message. If `commit_gate` is true, the hook blocks a commit without the trailer.
- Write the reason for the change and the **actual** verification result in the message. Do not write an unchecked item as passed.
- Add the evidence lines to the trailer block (above `Co-Authored-By`). Always add `Risk:` and `Tested:`. Add `Revert:` only when `git revert` alone cannot undo the change.

  ```
  Risk: high: saved data format change (SaveGame version 3 → 4)
  Tested: build passed (user), test guide R1, R2, R4 checked (user), agent review Deep round 2 / not checked: R3 loading an old save
  Revert: a build after the revert cannot read saves written with version 4. Apply the version 3 conversion tool before the revert
  ```

  - `Risk:` is the level from Step 0-C and one line of reason.
  - `Tested:` says what was checked and by whom, and also what was not checked (`not checked:`). If the review was skipped, write it, for example "agent review skipped (low)".
  - If `tracker_public` is true, do not include local paths.
- If there is an issue, write `#N` in the message. Use a keyword that closes the issue automatically (`Closes #N`) only after the user confirms completion.
- Check with `git status --short` that no unintended file is included.

### 3) Issue state

Suggest this only if there is an issue. For each item, show a draft and post it after confirmation.

| Situation | Suggestion |
|---|---|
| Implementation done, before user confirmation | Result summary comment + `status_labels.needs_verification` label |
| The user confirmed the build and run | Result summary comment (document links, commits) + close the issue |
| Work remains | Comment with the remaining items. For separate work, a follow-up issue draft |

### 4) End of session

> "여기서 마무리하시면 `context-handoff` 로 인계 메모를 갱신할까요?"

- If the work continues, skip it. If the user moves to other work or ends the session, recommend it.
- If the work had neither an issue nor a handoff note, skip it.

---

## Cautions

- If the size is hard to decide, ask the user. Do not guess.
- Do not change a recommendation only because the user asked about it. Change it when a reason fails or a new fact holds, and say which.
- Save the handoff note **at the moment the plan is confirmed**, and update it with each feedback.
- If the work becomes smaller during the Full Lane, you can move to Fast Lane Step F2.
- No step of this skill goes around the verification owner rules of the project instructions.
