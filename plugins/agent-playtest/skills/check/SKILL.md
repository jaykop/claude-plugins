---
name: check
description: "Check the completion conditions or the test guide of one issue in Unreal Play In Editor through MCP, with the AgentPlaytest engine plugin. Split the items into what game state can show and what a person must judge, write JSON scenarios, run them with RunScenario, give each item a verdict (passed, failed, cannot judge) with evidence, and write a report draft and an issue comment draft. Reads the test level and project notes from .claude/agent-playtest/profile.md. Not for: writing automation test code, judging feel or visuals, changing game code or assets, posting without approval."
when_to_use: "When the user asks the agent to run the in-game checks of an issue or a test guide itself. Examples: '#308 테스트 가이드 직접 돌려 봐', '이 이슈 완료 조건 PIE로 확인해 줘', '에이전트로 기능 테스트해', '/agent-playtest:check #308'."
argument-hint: "<issue number | test guide path> [item numbers]"
---

# Agent feature check in Play In Editor

The engine plugin `AgentPlaytest` gives the agent MCP tools that inject player input and read game state as JSON. This skill is the procedure around those tools: from an issue to a verdict report. How to write a scenario and how to read a result are in the engine skill, which you read in Step 2.

## Paths and profile

- This skill folder: `${CLAUDE_SKILL_DIR}`. If the variable is not expanded, it is the folder that holds this SKILL.md.
- Project profile: `.claude/agent-playtest/profile.md`. Template: `${CLAUDE_PLUGIN_ROOT}/shared/profile-template.md`. Keys used: `test_level`, `report_dir`, `language`, `tracker_public`, and the `Project notes` section.
- If the project also has a `workflow` profile (`.claude/workflow/profile.md`), use its `tracker`, `tracker_repo`, and `threads_dir` when this profile does not set them.
- No profile, or no `report_dir`: ask for the test level and where to write the report. Do not guess a level. Do not put reports in `threads_dir` itself: other skills read every file there as a handoff note.

## Rules

- Calling this skill is the user's request to run play checks. It does not allow builds, code changes, or test code. If an item needs a code change to pass, report it; do not fix it here.
- The project instructions win over this skill, for example rules about who runs checks and what may be posted.
- Do not save levels or assets. Before you place, change, or remove anything in the editor for a check, show the list and get a yes. Undo those changes when the checks end.
- Do not post to the issue tracker. Write drafts and ask.
- Never report an item as passed without evidence from this run. Results from earlier sessions are background, not evidence.

## Step 1 — Read the items

1. Read the issue (`gh issue view <N>` for GitHub) and its completion conditions. Then look for a test guide: the handoff note of the issue in `threads_dir`, documents linked from the issue, or the path the user gave. A test guide is often more concrete than the completion conditions; when both exist, check the guide and map each guide row to the condition it covers.
2. Classify each item.

| Class | Meaning | Example |
|---|---|---|
| Play | Game state can show it: tags, location, rotation, speed, attributes, log lines | "stands 80 cm in front of the plate and faces it" |
| Editor | Outside Play In Editor: asset editors, previews, build output | "the action editor preview plays without errors" |
| Person | Feel, smoothness, visuals, sound, fun | "the 0.2 s blend looks natural" |

Only Play items run here. Editor items go to the report as not run unless an editor tool can read the result directly. Person items always go to the person list.

3. Write the setup the Play items need: level, actors to place, cheats, debug commands, project settings. Show the user one table with the items, their class, and the setup changes, and wait for a yes before Step 2. If the guide names a level other than `test_level`, ask which to use.

## Step 2 — Preflight

1. Check that the MCP server is connected and lists the toolset `AgentPlaytestEditor.AgentPlaytestToolset`. If not, stop and tell the user what is missing (editor not running, plugin not enabled, MCP server off).
2. Read the engine skill with `ToolsetRegistry.AgentSkillToolset.GetSkills` for `/Script/AgentPlaytestEditor.AgentPlaytestSkill`, and follow it while you write and judge scenarios. Read `Project notes` of the profile too.
3. Call `ListVerbs`. If an item needs input that no verb covers, mark it cannot judge and name the missing verb.
4. Open the level, make the approved setup changes, and start Play In Editor (`EditorToolset.EditorAppToolset.StartPIE`). Call `GetObservation` and read the start state.
5. Read the transforms of the actors the items refer to, and compute the expected values before you write any scenario.

## Step 3 — Run

1. Write one scenario per item, following the engine skill. Keep each scenario JSON; the report needs it.
2. Run each with `RunScenario`. The call blocks until the scenario ends, so run them one at a time.
3. A failed or surprising result runs a second time. If the scenario itself was wrong (wrong expected value, wrong verb), fix the scenario and say so in the report; do not count the first run as a failure of the feature.
4. Reset between scenarios when a run leaves the player dead, far away, or in a lasting state.
5. Stop Play In Editor at the end, and undo the setup changes.

## Step 4 — Report

Write the report to `<report_dir>/<N>-<YYYYMMDD>.md` in `language`. Contents:

- Environment: level, setup changes and whether they were undone, date, and the frame time seen in the step times. The build state is what the user reported; do not claim a build you did not see.
- Item table: item (with the guide row or condition it covers), class, verdict, evidence (observed values, log lines, capture paths whose result says the file exists), scenario name.
- For each failure: the failed step, the observation, and the second run.
- Person list: items for a person, with what to look at.
- Not covered: cases the scenarios did not run, and items that could not run, with the reason.
- The scenarios (JSON), and the paths of the run records (`run.json`).

Then add an issue comment draft as the last section of the report: the item table and the person list, without local paths when `tracker_public` is true. Show the draft and ask whether to post it. Checks by the agent do not replace the user's check; do not suggest closing the issue on agent results alone.

## Pitfalls

- The editor window in the background runs the game at a few frames per second, and input timing is rounded to whole frames. A short window or a tight distance after held movement is a scenario problem: widen it as the engine skill says and run again (Step 3.3). Only a check that depends on input timing finer than a few frames is cannot judge at a low frame rate; ask the user to keep the editor window in front and run it again.
- The MCP client sends one tool call at a time. A running scenario cannot be stopped from the same client; give it a timeout instead.
- A cheat with a wrong argument, or a cheat that takes a class name that is not loaded, does nothing and its console step still passes. Expect the effect of each setup step before the feature steps.
- Actors placed in the editor level reach Play In Editor only when they are placed before the session starts.
