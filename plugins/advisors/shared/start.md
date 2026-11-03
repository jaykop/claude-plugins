# Common start and finish procedure for advisors

Step 0 and Step Final of each advisor skill follow this file. This file also has the procedure for when the user says during the conversation that a report is wrong ("Receive result feedback"). Below, `<고문>` is one of the folder names under the plugin's `skills/` folder (design · radar · market · perf · pm · td). If a question looks like the work of another advisor, see `shared/routing.md`.

This file is read with Read, so the path variables in it are not replaced. Replace `<플러그인 폴더>` (plugin folder) and `<프로젝트 루트>` (project root) with the actual paths written in the SKILL.md section "Paths and arguments".

## Step 0 — Start

### 0-A. Decide the run mode
- If the arguments of this call, written in the SKILL.md section "Paths and arguments", include `--unattended`, this is an unattended run. In all later steps, follow `rules.md` §10 (no questions; only up to saving the report).
- Do not decide by the words of the request. A request that contains the word '무인' (unattended), such as "무인도 생존 게임 시장성 봐 줘", is also a conversation run.
- In all other cases, it is a conversation run.

### 0-B. Read the common rules
Read `<플러그인 폴더>/shared/rules.md`. These rules take priority over the instructions of each advisor.

### 0-C. Check the profile
The profile has only one location: `<프로젝트 루트>/.claude/advisors/profile.md`.

**If it exists**, read it. If fields that this advisor needs (the "Required profile values" of each SKILL.md; include a field even if it belongs to another advisor's section) are empty:
- Conversation run: ask about only those fields, all at once. But do not ask about the following fields.
  - Fields that the SKILL.md marks "not asked in Step 0". If the mark is on a table title, this means all fields of that table (that skill checks them separately in a later step).
  - Fields for which the user already answered "모름" (don't know) or "아직 안 정함" (not decided yet). For such an answer, leave the value empty and write `[사용자] 모름` in the comment, and do not ask again from then on. If the user enters a value directly, use it from then on.
  - List fields for which the user answered "없음" (none) (for example, search banned terms). Write an empty list `[]` with the comment `[사용자] 없음`, and treat the field as filled. Do not ask again from then on.
  - Fields that can be found in files. Do not ask; fill them with the script in 0-D.

  When you get the answers, write them into the profile and change `updated` to today's date. In the comment next to each value, add the source (`[사용자]`, `[파일]`, `[추정]`).
- Unattended run: do not ask. Write the empty fields in the report's "확인 못 한 것" (not checked) section, and skip the steps that strictly need such a field.

**If it does not exist**:
- Conversation run: ask "이 프로젝트에 고문 프로필이 없어요. 만들까요?". If the user agrees, do 0-D. If the user refuses, do only the scope that the "When there is no profile" section of that SKILL.md defines. If the advisor has no such paragraph, do only what can be done without a profile (web research and similar). In this case, an advisor that uses the web must ask once about search banned terms and banned combinations before it searches, and must use the answer only for this run. In either case, write that fact at the top of the report.
- Unattended run: `report_dir` cannot be known, so do not write anything. Leave only "프로필 없음 — 대화 세션에서 먼저 프로필을 만들어 주세요" in the final response and stop.

### 0-D. Make the profile
1. Read the template `<플러그인 폴더>/shared/profile-template.md`.
2. Collect the values that can be found in files with the script.
   ```
   python "<플러그인 폴더>/scripts/profile_scan.py" "<프로젝트 루트>"
   ```
   If `python` is not available, run it with `python3`. Fill in the results (version control kind, engine kind, project file, engine version, folders with many documents, and so on) with the source `[파일]`. If the engine kind comes out as "둘 다" (both), ask. If it is Godot, the value to put in each field is in `<플러그인 폴더>/shared/engine-godot.md` §6.
   - Before you fill in the document folder fields (`design.roots`, `design.exclude`, `design.archive_dirs`, `td.rule_docs`, `td.record_roots`), check whether the project has a document index (for example `docs/README.md`, `AGENTS.md`) that separates canonical documents from legacy documents. If it does, follow that list. The index wins over the status mark at the top of a file (for example "확정" (final)). Send legacy documents to `design.exclude` or `design.archive_dirs`. If a document is in the canonical list but its body points to a path that does not exist now, write "일부 낡음" (partly outdated) in the profile notes. If canonical documents differ from each other in run commands or rules, follow the document that the index says to read first.
3. Of the remaining fields, ask about **only the common fields and the fields written in the "Required profile values" of the advisor that was called now** (the "not asked in Step 0" exception from 0-C is the same). Ask about the other fields the first time an advisor that needs them is called. Ask everything at once, and tell the user that unknown values can be left empty.
4. In particular, do not fill in the following by guessing: `decision_owners`, `user_role`, `team_size`, `search_banned_terms`, `search_banned_combos`, `design.principles_status`, `perf.budgets`.
5. The save location is `<프로젝트 루트>/.claude/advisors/profile.md`. Leave it to the user whether to put it in version control. If it is a git project and `share_scope` is personal, ask whether to add it to `.gitignore`.

### 0-E. Report folder and past records
The mode must be decided before you can choose the previous report. If the request does not decide the mode, first do the mode selection of the SKILL.md, and then come to 0-E.

1. Decide `report_dir`. If it is a relative path, it is relative to the project root. If the folder does not exist, create it.
2. In `<report_dir>/<고문>/`, find the most recent report of **the same mode as this run** (tell the modes apart by the mode part of the file name; `rules.md` §12). If the SKILL.md says that the target must also be the same (for example, an area diagnosis must be for the same area), match that condition too. If you find one, use it as the "직전 리포트" (previous report).
3. In `<report_dir>/_state/inbox.md`, find the questions whose receiving advisor (받는 고문) is `<고문>` and whose status is "열림".
   - Conversation run: ask "<고문> 앞으로 미해결 질문이 N건 있는데 이번에 같이 볼까요?". If the user chooses to look at them together, first finish the requested work, and then handle each question with one run of this advisor's "mode that looks at one target" (see the mode selection of the SKILL.md).
   - Unattended run: include only the questions that fit the scope of the requested mode. Write the others in the report's "확인 못 한 것" (not checked) section as "다음 대화 실행에서 처리" (handle in the next conversation run).
   - Exception: for a question that is not the work of the receiving advisor (`shared/routing.md`), do not ask the user, in both conversation and unattended runs. Pass it to the right advisor by the passing rules in inbox-format.md.
4. Decide today's date with `date +%F`.
5. Read the base revision. Read it only if the command is allowed in profile `vcs_read_commands`. This is the same for conversation and unattended runs (`rules.md` §7). For git, use `git rev-parse --short=12 HEAD`. For p4, use `p4 changes -m1 ...#have` in the project root. If the command is not allowed or it fails, write "확인 못 함".

### 0-F. Team reference notes and result feedback
Read the two kinds of material that fit the judgment criteria to this project. The rules for reading and writing them are in `rules.md` §13. Read them in both conversation and unattended runs.

1. **Team reference notes**: if profile `<고문>.knowledge_dir` is empty, skip this (do not ask about it in Step 0). If it has a value, first read `index.md` in that folder, and then read the notes listed there that apply to this mode and target. If there is no `index.md`, read all .md files in the folder. If the folder does not exist or cannot be read, write that in the report's "확인 못 한 것" (not checked) section.
2. **Result feedback**: in `<report_dir>/_state/feedback.md`, read the rows whose advisor column (고문) is `<고문>` and whose status is "반영 전" (including an empty status) (format: `shared/state-formats.md`). If the file does not exist, skip this.
   - For each row, open that item of that report. If the report file does not exist, look only at the description column (설명).
   - Do not make the same mistake in this run's judgment. In places where the same mistake can occur again (the same kind of question, the same material, the same judgment), write the row ID at that place in the report, and write one line on what you did this time.
   - If a mark does not seem to match the evidence (if the evidence file:line or source contradicts the mark), do not change this run's judgment to match the mark. Write the row ID and that evidence in the report's "결정이 필요한 것" (decisions needed) section, and get the user to confirm it again.
   - In the "범위" (scope) row at the top of the report, write the row IDs you read (for example "결과 표시 FB-0003, FB-0007 읽음"). If there are no rows to read, write "결과 표시 없음".
   - For a row whose cause is empty or "모름": in a conversation run, look at the report item again and find the cause. Write it in that column in Step Final. If you cannot find it, leave it as "모름". In an unattended run, leave it as it is.
   - If you read 10 or more rows, propose a cleanup. In a conversation run, add "반영 전 표시가 N건 쌓였어요. 원인별로 고칠 곳을 정리해 드릴까요?" to the follow-up proposals in Step Final. If the user agrees, give groups by cause in the conversation (row IDs, and the candidates from the state-formats.md table "Where to fix by cause"), and do not change files. In an unattended run, write "반영 전 N건 — 정리 필요" in the "범위" (scope) row at the top of the report.

### 0-G. Engine kind
The advisor documents are written for Unreal. If profile `engine.kind` is `godot`, read `<플러그인 폴더>/shared/engine-godot.md`, and read the advisor documents as changed by the sections of that file that the SKILL.md points to. design·market·pm have no steps tied to the engine, so they do not need to read it.
- If `engine.kind` is empty, treat the project as Godot when `project_file` is `project.godot`, or when, down to depth 3 under the project root, there is no `.uproject` and there is a `project.godot` (Glob). In a conversation run, write that value in the profile with the source `[파일]`.
- In all other cases, treat it as Unreal (`unreal`).

## Step Final — Finish

1. Save the report as `<report_dir>/<고문>/<YYYY-MM-DD>-<모드>.md`. The format is `<플러그인 폴더>/shared/report-base.md`.
2. Update the `_state` files of this advisor. Change `마지막 갱신` at the top to today's date, and also update the `다음 점검:` line. The session start notice uses these two values to decide whether to notify. If the SKILL.md defines when each file is changed (for example, td's td-debt.md only during a technical debt check), change that file only at that time.
   - Write the result feedback log (`_state/feedback.md`) only in a conversation run. Write the marks received in this run ("Receive result feedback" below) and the causes found in 0-F. If the file does not exist, create it with the header in `shared/state-formats.md`. In an unattended run, do not write it.
3. If there are questions to pass to another advisor, add them to `_state/inbox.md` (format: `<플러그인 폴더>/shared/inbox-format.md`). For the questions answered in this run, change the status to "답함".
4. In a conversation run, give only the following in the conversation.
   - A three-line summary
   - Decisions needed
   - The report path
   - 1 to 3 follow-up proposals. Examples:
     - "<다른 고문>에게 넘긴 질문 N건을 지금 볼까요?"
     - "<항목>을 코드 수정으로 넘길까요?" (if profile `code_change_entry` is set, use that skill name)
     - If this advisor ran for the first time, the default cycle in the SKILL.md is not "예약 없음" (no schedule), and no check is scheduled: "다음 점검을 <주기>로 예약할까요?"
     - If 0-F read 10 or more "반영 전" rows: "반영 전 표시가 N건 쌓였어요. 원인별로 고칠 곳을 정리해 드릴까요?"
5. In an unattended run, end the final response with the report path and a three-line summary.

### File write approval
The allowed-tools of each SKILL.md allow in advance only writes under the project's `.claude/advisors/` (the default `report_dir` and the profile location). If `report_dir` is set to another place, ask for write approval for each file in a conversation run. In an unattended run, follow the last item of `rules.md` §10.

## Receive result feedback

During a conversation run, if the user says that a report is wrong ("이 리포트 X 틀렸어", "이건 어디에나 맞는 말이야", "Y 는 안 봤네"), add one line to the result feedback log. This is the same after the report is given and during the work. Do not write it in an unattended run. The format is feedback.md in `shared/state-formats.md`.

1. Classify the mark as one of 틀림 (wrong) / 일반론 (generic) / 놓침 (missed). If the user's words do not decide it, show the three and ask once.
2. Decide the report and the item. If the user did not point to them, find the matching item in the most recent report, show it, and get confirmation that it is the right one. If the user's words are about another advisor's report, the advisor column is the advisor that wrote that report.
3. In the description column (설명), put the user's words in one line. Do not rephrase them.
4. Find the cause. Look at the report item, the material read at that time (the report's "범위" (scope)), and that advisor's instructions, and choose one of the five in the state-formats.md table "Where to fix by cause". Do not ask the user questions that require domain knowledge. If you cannot find the cause, write "모름".
5. Set the status to "반영 전" and leave the "fixed in" column (고친 곳) empty. Writing the file is the same as item 2 of Step Final. If the report was already given, write it right away.
6. In the conversation, report only the row ID, the cause, and the candidate places to fix, in one line. Do not change reference files, scripts, SKILL.md, or team reference notes (`rules.md` §13). If the place to fix is a profile field, write it in the profile after the user confirms the value, as in 0-C.
7. If the user tells you where it was fixed ("고쳤어, 커밋 abc") or decides not to apply it ("반영 안 해도 돼, <이유>"), change the "fixed in" column and the status of that row as the user says.

## Make a scheduled check

Make one only if the user agreed to the schedule.

- If the session has a scheduled task tool (Claude Desktop scheduled-tasks `create_scheduled_task`), make it with that tool.
  - A scheduled run does not remember this conversation. Put all of the following in the instruction text.
    - First line: the skill and mode to call, and the `--unattended` argument. Example: `/advisors:radar 정기 점검 --unattended`. An unattended run is identified only by this argument (0-A). Put this line first so that it is read as a slash command
    - The absolute path of the project root, and an instruction to work in that folder
    - "질문하지 말고 리포트 저장까지만 할 것" (do not ask questions; only go as far as saving the report). This is an explanation for people to read; the identification is done by the argument on the first line
    - The absolute path of `report_dir`. Tell the user to allow writes to this folder in the permission settings of the scheduled task. The allowed-tools of each SKILL.md allow in advance only writes under `.claude/advisors/` and a few git·p4 read commands. If `report_dir` is in another place, or if `vcs_read_commands` has other commands, tell the user to allow those too. If the `knowledge_dir` of that advisor is outside the project, tell the user to allow reads of that folder too
  - For the cycle, propose the "Default cycle" of each SKILL.md, and use the value that the user decides.
  - Tell the user that it runs while the Claude Desktop app is on, and that if the app was off, it runs the next time the app is turned on.
- If there is no scheduled task tool, do not make it yourself. Tell the user how to make it with the instruction text above in the scheduled task screen of Claude Desktop. Do not recommend cloud schedules (routines), because they cannot see local files.
