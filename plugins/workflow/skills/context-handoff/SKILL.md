---
name: context-handoff
description: "Use when the session context is near its limit or when the session ends. Save or update the state of the work in progress as a handoff note file for each thread, so that the next session can continue. Use it when the context limit, the end of a session, continuing later, or an intermediate save is mentioned. Not for: writing public documents (usage, change records), or only posting to an issue."
when_to_use: "When the handoff hook suggests it in a long session, before you move to other work, when the user says '저장해 둬' or '다음에 이어서', and in Step Final of feature-impl."
argument-hint: "[thread name]"
---

# Context Handoff

Save the context of the work before the session ends. Save it **per thread**: one piece of work is one file. Always update the same file for the same thread.

## Profile and save location

The profile is `<project root>/.claude/workflow/profile.md`. The plugin folder is `${CLAUDE_PLUGIN_ROOT}`. If the value shows as the variable name, the plugin folder is two levels above this SKILL.md.

- Notes in progress: profile `threads_dir` (default `.claude/workflow/threads`)
- Notes of finished work: `<YYYY-QN>/` under profile `archive_dir`
- If there is no profile, ask for the save location. For a public repository, it must be a folder that is not in version control.

**Division of roles.** If the profile has `tracker`, the issue is the reference for work in progress. The handoff note is a **local session record** that supports the issue. It holds trial and error, local paths, and steps for the next session that do not go into a public issue. Write the shared progress, completion, and waiting-for-confirmation state in the issue, the current usage in the manual, and the reasons for important decisions in the devlog. For how notes are shared or backed up (for example, in another version control system), follow the project instructions.

Write the note in the language that the project instructions set for handoff notes. If they set none, use the language of the existing note.

## Workflow

When new work starts, make its note, or read and update the existing file. First write the goal, the current situation, the linked issue, and the next action. During the work, add important decisions, and update the note when the work ends.

### Step 1 — Thread name

1. **If an issue is linked**: `<issue number>-<slug>` (example: `12-preview-gizmo-fix`). For Jira, use the issue key (example: `ABC-12-preview-gizmo-fix`). If an existing note has no issue number, suggest a rename.
2. **If the work branch is not the default branch**: use the branch name in kebab-case.
3. **If you work on the default branch**: take the topic from the conversation. Use lowercase English kebab-case.
4. **If it is not clear, ask the user**: "What name do you want for this thread? (example: `timeline-editor-polish`)"

### Step 2 — File path

`<threads_dir>/<thread-name>.md`

### Step 3 — Write the note (merge)

**If the file exists**, read it, then update it as follows.

- **Done**: cumulative (add new items)
- **In progress**: update to the current state (move finished items to "Done")
- **Next steps**: sort again (remove finished items, add new items)
- **Notes**: cumulative (add new decisions and context)
- **Key files**: update to the current state
- **Risks and checks**: keep the items and update only the state (mark "checked" only for what was actually checked)
- **Review log**: cumulative (do not delete the rows that feature-impl wrote for each round)
- **Version control state**: replace with the current state
- **Last updated**: the current time

Older notes use Korean section headings: 현재 작업 목표 (Goal), 완료된 것 (Done), 진행 중인 것 (In progress), 다음에 할 일 (Next steps), 구현 계획 (Implementation plan), 위험과 검증 (Risks and checks), 리뷰 기록 (Review log), 주요 파일 및 경로 (Key files), 버전 관리 상태 (Version control state), 빌드·검증 상태 (Build and check state), 참고 사항 (Notes). Read them as the same sections. When you update an older note, keep its headings.

**If the file is new**, use `<plugin folder>/shared/thread-template.md`.

### Step 3.5 (optional) — Issue status comment

If an issue is linked and this session has progress to share (confirmed decisions, finished items, blockers), show a draft of a **public summary** comment and ask whether to post it. Do not post without confirmation.

- Include: finished items, confirmed decisions, remaining work, links to related commits and documents
- Do not include (especially if `tracker_public` is true): local paths, details of trial and error, guesses that are not decided, build or check results that were not checked

```bash
gh issue comment <N> --body-file <temporary draft file>
```

### Step 4 (optional) — Finish a thread

Do this only when the user asks for it, for example "thread 마무리" or "보관으로 옮겨". Do not move the note automatically.

- `<threads_dir>/<name>.md` → `<archive_dir>/<YYYY-QN>/<name>.md`
- Quarters: January to March Q1, April to June Q2, July to September Q3, October to December Q4

**Before you move the note**, move the trial and error in "Notes" that is worth keeping to the related devlog or the linked issue. The note is a record that can disappear.

## Writing rules

- Write **specifically**, so that the agent of the next session can continue from this note alone.
- Focus on **what to do next** more than on how far the work went.
- Copy incomplete code, commands, and error messages as they are.
- When you update a note, do not cut the core context (decisions, trial and error).
- Do not guess build or check results that were not checked.
- Do not write credentials or secret values.

## Cautions

- Do not put a date in the file name.
- If you hand off the same thread more than once, always update the same file.
- For different work, make a **new file**. Do not mix several pieces of work in one file.
- Always keep notes in `threads_dir`. Do not mix them with the shared document folders.
