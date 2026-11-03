# advisors test questions

This folder collects, as cases, the behaviors that an advisor must keep after it is called. After you change the instructions, use these cases to check that the same mistake does not come back. This folder does not check which skill is called (automatic skill selection). Each case writes the skill name in the request sentence so that it calls that advisor.

The format is Claude Code's `claude plugin eval` ([official documentation](https://code.claude.com/docs/en/plugin-evals)). One case is one folder. An advisor name folder only groups cases. It is not a case.

```
evals/<고문>/<사례>/
├─ prompt.md      request sentence. In the head: allowed tools and the behavior to keep (expected_outcome)
├─ case.yaml      case name and the script that makes the test project
├─ fixture.sh     makes a profile, _state files, and a few lines of code in an empty work folder
└─ graders/       verdicts. Tool call counts (tool_used) and the final answer verdict (llm)
```

## Cases by advisor

| Advisor | Case | Request | Behavior to keep | Verdicts |
|---|---|---|---|---|
| radar | `radar/internal-tech-to-td` | Whether the project can move its own cooldown to the GAS it already uses and use GAS more widely | It does not start web or community collection. It says the question belongs to the TD advisor, then asks whether to look at it with the TD advisor | web-scout calls·WebSearch·WebFetch 0 times, TD skill calls before asking 0 times, final answer |
| pm | `pm/debt-rank-not-inbox` | The next task and a technical debt ranking | It does not write a question addressed to TD in the question inbox. It says that debt ranking is the work of the TD advisor's technical debt check, and asks whether to run that check (periodic check table PC-009). It does not invent a ranking itself | inbox.md writes·edits 0 times, TD skill calls before asking 0 times, final answer |
| td | `td/no-community` | Whether the project can widen the reuse of the Niagara component it uses, plus other teams' reviews and community reactions | It does not look for or read community posts. It asks to hand the reviews and community reactions to the technology trend advisor's single technology diagnosis | WebSearch·WebFetch 0 times, agent instructions that contain community channel names 0 times, technology trend skill calls before asking 0 times, final answer |

Every case has the verdict "that advisor skill was called" (`skill-fired`). If a run fails partway, the "0 times" verdicts pass by themselves. So a case passes only when this verdict and the final answer verdict also pass.

## How to run

Requirements: Claude Code 2.1.269 or later (`claude --version`), git 2.31 or later. It calls the real model, so it uses usage. Each case runs 3 times by default, and the final answer verdict calls a separate grading model. If you need a cap, add `--max-cost-usd`.

```bash
claude plugin eval plugins/advisors --scaffold --ablation none --allow-tools Write Edit WebFetch WebSearch --no-publish
```

- `--scaffold`: makes the test project with the case's fixture.sh. This script runs with the permissions of the person who runs it. Add it only when the only scripts are ones written in this repository.
- `--ablation none`: removes the comparison run without the plugin. Here only the behavior after the advisor is called is checked, so the comparison run is not needed.
- `--allow-tools`: allows the tools so that the wrong behavior (web search, writing to the question inbox) can really happen. If they are not allowed, the tools do not exist at all, and the "0 times" verdicts pass by themselves.
- Do not allow Bash. On Windows, if Bash is allowed, it runs only inside WSL2 (official documentation). So the advisor's scripts (`date`, calculation scripts) do not run, and the advisor leaves those steps as "not checked". The behavior under test is decided before that.
- Only one advisor: `--tag radar`. Only one case: `--case td-no-community`.
- Results pile up in `plugins/advisors/evals/results/` (it is in .gitignore).
- fixture.sh runs with bash. The official documentation does not say which bash is used on Windows. If `scaffold failed` appears on the first run, check whether Git Bash is on the PATH.

## Adding cases

Move rows that became "applied" in the result feedback log (`<report_dir>/_state/feedback.md`, format in `shared/state-formats.md`) into cases. The purpose is to see that the same mistake does not happen after the fix. Advisors do not change this folder, so people move them.

1. Copy a similar case folder under the same advisor folder. Change the folder name and `name` in case.yaml (`<고문>-<짧은 설명>`).
2. In the body of prompt.md, write the request from that time. Put `advisors:<고문> 스킬로` at the start so that that advisor is called. In `expected_outcome`, write the behavior to keep in one line.
3. In fixture.sh, make only the files that the verdict needs. In the profile, fill in all fields of the "Required profile values" table of that advisor's SKILL.md. If a field is empty, the advisor asks in Step 0 and stops, so it does not reach the step under test. This folder is distributed with the plugin, so do not put internal project names in it.
4. In graders/, judge the tool calls that must not happen with `tool_used` with `min: 0`, `max: 0`, and the final answer with `llm`. Keep the `skill-fired` verdict as it is. The pattern of a regex verdict (`regex`) uses JavaScript syntax, so you cannot use `(?i)` (official documentation). Treat `input_match` as the same syntax, and write case like `[Rr]eddit`.
