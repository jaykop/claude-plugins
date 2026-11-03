---
name: work-start
description: "Use at the start of a work session. Collect the in-progress issues assigned to me, the handoff notes, and the changes that are not committed or submitted yet. Give a short report and stop. After the user chooses a direction, align issue and note states, find design documents, change the issue state of the chosen work, and make a handoff note. Use for requests such as '작업 시작', '오늘 작업 시작', '어디까지 했지', '이어서 하자', '하던 일 뭐 있지'. It reads GitHub and Jira as issue trackers, and git and Perforce as version control. Not for: choosing new work by priority or making an issue (next-task), changing code (feature-impl), saving a handoff note (context-handoff)."
when_to_use: "When you open a session for the first time, when you return to work after some days, when several pieces of work are in progress and you must choose which one to continue."
argument-hint: "[issue number, issue key, or thread name]"
allowed-tools: Read, Glob, Grep, Bash(git status*), Bash(git branch*), Bash(git rev-parse*), Bash(gh issue list*), Bash(gh issue view*), Bash(p4 opened*)
---

# Work Start

This is the entry point that reports the work in progress at the start of a session. First give only a short briefing and stop. Do the follow-up steps (align states, find design documents, choose work) only after the user chooses a direction.

## Paths and profile

- Plugin folder: `${CLAUDE_PLUGIN_ROOT}`. If the value shows as the variable name, it is the folder two levels above this SKILL.md.
- Profile: `<project root>/.claude/workflow/profile.md`. Personal values are in `profile.local.md`. Keys used: `tracker`, `tracker_repo`, `tracker_project`, `tracker_site`, `tracker_query`, `status_labels`, `vcs`, `docs` (manual, plan), `threads_dir`, `archive_dir`.
- If there is no profile, ask whether to make one. Make it as "Paths and profile" of `feature-impl` describes. If the user says no, read only the version control state and give the briefing.

## Common rules

- The project instructions take priority over this skill.
- The briefing (steps 1 and 2) only reads. Do not change files, and do not write to the issue tracker.
- Changing an issue state, changing labels, and comments are publishing actions on the tracker. Show the content and do them only after confirmation.
- Read only the version control state. Do not run commands that change the working copy, such as `git pull` or `p4 sync`. If an update is necessary, only tell the user the command.

## Tracker tools

- `github`: use the logged-in `gh` CLI.
- `jira`: use the tools of the Atlassian MCP server. The prefix of the tool names (`mcp__<server name>__`) depends on the installation. Find the tools by the end of the name: `searchJiraIssuesUsingJql`, `getJiraIssue`, `getTransitionsForJiraIssue`, `transitionJiraIssue`, `getAccessibleAtlassianResources`.
  - If a tool is not in the tool list, load it with the tool search (ToolSearch) by this name. Do not write the server name in this skill or in the profile.
  - If a tool needs `cloudId`, get it with `getAccessibleAtlassianResources`. If there are several sites, choose the one whose address matches profile `tracker_site`. If the tool description says that it also accepts a site address, you can pass `tracker_site` directly.
  - If you cannot find the tools, skip the Jira query and write one line about it in the briefing.
- If the value is `none` or empty, skip the issue query.

## 1. Light query

Collect the three items below together. Do not read issue bodies or look for design documents here.

### 1-A. My issues

For `github`, read my open issues.

```bash
gh issue list --repo <tracker_repo> --assignee @me --state open --limit 20 --json number,title,labels,milestone,updatedAt
```

An issue with the `status_labels.in_progress` label is in progress. If no label is set, use all open issues in order of the latest change.

For `jira`, call `searchJiraIssuesUsingJql`.

- JQL: if profile `tracker_query` has a value, use it. If not, use `assignee = currentUser() AND statusCategory = "In Progress" ORDER BY priority DESC, updated DESC`. If `tracker_project` has a value, add `project = <tracker_project> AND` at the start.
- Fields: `summary`, `status`, `issuetype`, `priority`, `updated`, `parent`. Do not get the body or the comments.
- Get at most 20 issues.

### 1-B. Handoff notes

Find `<threads_dir>/*.md`. For each file, read only the `> Last updated` and `> Issue` lines of the header and the first item of "Next steps" (older notes: "다음에 할 일"). The time of the last activity is the file modification time. For the note format and the name rules, follow `context-handoff`.

### 1-C. Version control state

Read only the state, as profile `vcs` sets.

| `vcs` | Command | What to read |
|---|---|---|
| `git` | `git branch --show-current`, `git status --short` | Current branch, number of uncommitted files |
| `p4` | `p4 opened` | Number of open files, changelist numbers |

If the key is empty, check with `git rev-parse --is-inside-work-tree` whether the folder is a git repository. If it is not a git repository, skip this query.

## 2. Briefing

Give a short report of what you collected and stop. Do not ask a list of questions.

Write the briefing in the language of the conversation with the user. The examples below are in Korean.

If there are 4 handoff notes or fewer, use this format.

```
오늘 (YYYY-MM-DD)

이슈 N개
  · <이슈 키> [우선순위] <제목>
인계 메모 M개
  · <thread 이름> (<이슈 키 또는 "이슈 없음">) 마지막 활동 K일 전, 다음: <다음에 할 일 첫 항목>
미제출 변경 L개 (<브랜치 또는 체인지리스트>)

이어 갈 것: <대상> (<한 줄 이유>)
```

If there are 5 handoff notes or more, use the short format.

```
오늘 (YYYY-MM-DD)
이슈 N개: <키>, <키>   인계 메모 M개: <이름>, <이름>   미제출 변경 L개
이어 갈 것: <대상>
```

- Shorten the issue title of the tracker to one line. Do not include the body.
- Choose "이어 갈 것" (what to continue) in this order.
  1. The handoff note with the most recent activity
  2. If there is no handoff note, the in-progress issue with the highest priority. If priorities are equal, the issue that changed most recently
  3. If there is neither, and `tracker` is `github`, suggest choosing new work with `next-task`
- On the last line, give the choices in one line: "더 필요하면 상태 맞추기, 설계 문서 찾기, 이슈 상세, 바로 시작 가운데 말해 주세요."
- Stop here and wait for the user. Do not go to step 3 automatically.

## 3. After the user chooses a direction

Do only the items that the user asks for.

### 3-A. Align states

Compare the `> Issue` line of each handoff note with the tracker state. Read the state of each issue with `gh issue view <N> --json state,labels` or `getJiraIssue`.

Use these states.

- Done: a closed issue on GitHub, status category `done` on Jira
- In progress: the `status_labels.in_progress` label on GitHub, status category `indeterminate` on Jira
- To do: other open issues

| Handoff note | Issue state | Suggestion |
|---|---|---|
| Exists | In progress | Keep it |
| Exists | Done | Ask whether to archive the note (`context-handoff` Step 4) |
| Exists | To do | Ask whether to keep the note |
| None | In progress | Ask whether to make a note |
| Note without an issue | None | Ask whether to link it to an issue |

### 3-B. Find design documents

Look for the design documents of the chosen issue in this order.

1. Document links and paths in the issue body and comments
2. Documents in "Key files" (older notes: "주요 파일 및 경로") of the handoff note
3. The profile `docs.plan` and `docs.manual` folders. Search with the words of the issue title, and give only 1 to 3 candidates. For each candidate, write how well it matches: high, medium, or low. If no candidate is high, read the start of the candidate files and decide again.

Write only the documents that the user confirms in "Key files" of the handoff note. Do not write them in the tracker. If the user asks for it, show a comment draft and post it only after confirmation.

### 3-C. After the user chooses work

When the user chooses an issue or a handoff note, do these steps in order.

1. Read: read the issue body, the comments, and the whole handoff note. If you confirmed a design document in 3-B, read only the related items.
2. Issue state: if the issue is not in progress, ask whether to change it to in progress. Change it after approval.
   - `github`: add the `status_labels.in_progress` label. If no label is set, skip this step.
     ```bash
     gh issue edit <N> --repo <tracker_repo> --add-label "<label>"
     ```
   - `jira`: from the result of `getTransitionsForJiraIssue`, choose the transition whose target status category (`statusCategory.key`) is `indeterminate`. If there are several, show the names and ask. If no transition matches, do not change the state, and say so.
3. Handoff note:
   - If the chosen issue has a note, continue in that note.
   - If there is no note, look for a note without an issue whose topic matches. Use the words of the note name, the body, and the previous conversation. If there is a candidate, ask whether to link the issue to that note or to make a new note. If you link it, fill in the `> Issue` line and ask whether to rename the note.
   - If no note matches, make a new note with `<plugin folder>/shared/thread-template.md` and give its path. For the name, follow `context-handoff` Step 1.
4. Overlap check: if an uncommitted file is in "Key files" of another handoff note, write a one-line warning.
5. Hand over: code changes go to `feature-impl`, new issues go to `next-task`, and document-only changes go to the matching document skill.

## Cautions

- Do not delete or archive a handoff note only because time passed. Ask based on the tracker state, or clean up only when the user asks.
- Do not write credentials or secret values in the briefing or in handoff notes.
