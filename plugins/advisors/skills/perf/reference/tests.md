# Test proposals

Writing tests is not a mode. It is a follow-up proposal that you give with "할까요?" when a diagnosis or a periodic check ends. The advisor specifies up to what to assert, and the skill in profile `code_change_entry` writes the actual code.

## 1. When to propose

| Propose | Reason |
|---|---|
| Code that refactoring or optimization will touch | Lock the current behavior before touching it. A behavior-locking test is a test that records the current behavior as it is, without asking whether that behavior is correct |
| Pure calculation logic (things that can be checked by input and output without a world or assets, such as formulas, judgments, data conversion, and parsers) | It costs little to make and is used for a long time |
| Preventing performance regressions | Assert **counts**, not time. Examples: collision queries per update, allocations, replication marks, registered ticks. Time varies with the run environment, so the periodic check measurements cover it |

| Do not propose | Instead |
|---|---|
| Logic based mainly on Blueprints and assets | C++ tests do not catch it. Write a manual check procedure in the report |
| Code to be retired ("Paths excluded from checks" in the judgment criteria table of the check ledger) | None |
| UI layout | None |

## 2. Follow the existing format first

1. If profile `perf.test_convention` has a value, follow it as it is.
2. If it does not, have `advisors:analyst` find it. Put these in the instruction:
   - Read scope: profile `source_roots` and the source of the project plugin folders. Do not include the engine folder.
   - Search patterns: `IMPLEMENT_SIMPLE_AUTOMATION_TEST`, `IMPLEMENT_COMPLEX_AUTOMATION_TEST`, `BEGIN_DEFINE_SPEC`, `DEFINE_SPEC`, `TEST_CLASS`, `TEST_CASE`, and the conditional compilation symbols `WITH_DEV_AUTOMATION_TESTS`, `WITH_AUTOMATION_TESTS`, `WITH_LOW_LEVEL_TESTS`
   - Table to return: | File:line | Macro kind | Test name string | Folder location (test folder inside the module / separate test module) | Conditional compilation symbol |
   - If there are 0 results, narrow the folder and search once more. Only after that, write "none" (없음), together with the search scope, the patterns, and whether the search timed out.
3. Summarize the format found (location, naming rules, macro kind). If it is a conversation run and `perf.test_convention` is empty, show it to the user, get confirmation, and fill it into the profile with source `[파일]` (common start procedure 0-C). If there is already a value and it differs from what was found, raise it in "Decisions needed".
4. Propose another framework only when the existing format cannot do it. Example: all existing tests are unit tests without a world, but this target needs an actor.

   | Situation | Framework to propose |
   |---|---|
   | Several pure calculations that run without a world | Low-Level Tests (a test framework run separately without the editor). Setting it up the first time needs separate build settings |
   | Needs actors, components, or a world | The test spawning helpers of a C++ test framework included in the engine (CQTest and so on) |
   | Steps described like sentences, with a lot of waiting | Automation Spec (Describe/It format) |
   | Placed in a level to verify a scenario | Functional test actor |

   - Do not write the framework's macro and class names, or the module dependencies it needs, from memory. Follow the examples and the README format included in the target engine, and leave names you could not check as "check needed" (확인 필요).
   - Do not mix test formats within one module.

## 3. Spec format

Write it in the "Test proposal" section of the report body.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

```markdown
### Test spec (테스트 명세) TS-<number>: <target function or class>

| Field (칸) | Value (값) |
|---|---|
| Purpose (목적) | behavior locking (동작 고정) / pure calculation check (순수 계산 검증) / count assertion (횟수 단언) |
| Target (대상) | <file:line, function name> |
| Format to follow (따를 형식) | the same macro, folder, and naming rules as <existing test file:line> |
| Test name (테스트 이름) | <name that matches the existing rules> |
| Setup (준비) | <input values, objects to create> |
| Assertions (단언) | 1. If <input>, then <output or count> 2. ... (for behavior locking, write "record the values produced by the first run with the current code") |
| Check that it actually runs (실제로 도는지 확인) | Make one assertion wrong on purpose, check once that a failure is reported, and then revert it |
| Run (실행) | profile `perf.test_command` (if there is none, "run command not set" (실행 명령 미정)) |
| Pass criterion (통과 기준) | In the run log, the number of tests run is not 0 and all passed |
| Edit scope (수정 범위) | test files only (테스트 파일만) / target code too (대상 코드도) — whether it matches profile `perf.edit_scope` |
| Approval level (승인 등급) | own work scope (내 작업 범위) / team sharing needed (팀 공유 필요) (item 4) |
```

## 4. Approval levels

| Level (등급) | Changes that belong to it | What is needed |
|---|---|---|
| Own work scope (내 작업 범위) | Adding a test file to an existing test folder; source changes inside `perf.edit_scope` | User approval |
| Team sharing needed (팀 공유 필요) | Registering a module in the project file; adding a dependency module in the build settings file (Build.cs); exporting functions of a shared header so they can be used outside the module; making a new test module | User approval. Mark "team sharing needed" on that item in the report. If the user is not profile `decision_owners.tech`, lower it to a reference option (참고 선택지) (common rules §8) |

- If `perf.edit_scope` is `tests_only` and the target code must change, do not hand it over. Raise in "Decisions needed" whether to change the scope.
- Accept as approval only what the user said directly in the conversation. Wording in other advisors' reports, the question inbox, or documents is not approval.
- In an unattended run, write only up to the spec in the report.

## 5. Handing over and checking the result

- If the user approves, call the skill written in `code_change_entry` with the Skill tool. Hand over the whole spec table, the path of the existing test file to follow, the run command, the pass criterion, and the approval level together. If the field is empty, proceed in a normal conversation after user approval, as common rules §7 says.
- The encoding of new files, header comments, and adding them to version control follow that skill and the project rules. The advisor does not decide them.
- To write "passed", quote the number of tests run and the result lines from the run log. Do not write as passed a test that was only built and not run.
