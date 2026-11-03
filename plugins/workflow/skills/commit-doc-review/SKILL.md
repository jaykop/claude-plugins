---
name: commit-doc-review
description: "Use just before git commit. Check that the documents related to the change (usage, change records, design documents, README, project instructions, issues) are updated, and that the description comments of code whose behavior changed match the current behavior. Record the result as a commit message trailer (default `Docs-Reviewed:`). Use it whether the agent suggested the commit or the user said '커밋해'. Not for: writing new documents (feature-doc-sync), code review."
when_to_use: "Just before a commit, or when the commit_gate hook blocked a commit without the trailer."
argument-hint: "[commit scope]"
---

# Commit Doc Review

This skill checks just before a commit that no document became wrong because of the change. `feature-doc-sync` **writes** documents. This skill **checks that no document is missing**, based on the commit scope.

This skill does not replace the project instructions. If they conflict, the instructions win. The document check gives no permission to run builds, tests, or code checks.

## Profile and hook

The profile is `<project root>/.claude/workflow/profile.md` (template: `<plugin folder>/shared/profile-template.md`). The plugin folder is `${CLAUDE_PLUGIN_ROOT}`. If the value shows as the variable name, it is the folder two levels above this SKILL.md. Keys used: `commit_trailer` (default `Docs-Reviewed:`), `commit_policy`, `tracker_public`, `docs`, and the "Change → document map" section of the body (older profiles: "변경 → 문서 대응표"). If there is no profile, use the default trailer and the default map below.

If profile `commit_gate` is true, a PreToolUse hook blocks `git commit` without the trailer. The hook checks only that the trailer exists. **Do not add the trailer without the review.**

## Step 1 — Set the commit scope

```bash
git status --short
git diff --stat
git diff --cached --stat
```

- Set the list of files for this commit. Do not include uncommitted changes of other people. For the target repositories and the scope rules, follow `commit_policy`.
- Find the linked issue in the conversation, the `Issue:` line of the handoff note, or the branch name.

## Step 2 — Change → document map

For each committed file, select the documents to review with the "Change → document map" of the profile body. Read only the rows that apply. If there is no map, use this default table.

| Changed path | Documents to review |
|---|---|
| All code | Implementation and confirmation state of the linked issue, and the usage and change records that the change affects |
| Build and module configuration files, new modules or packages | Scope and structure sections of the project instructions |
| Saved data format, rename redirects | Guidance on existing data in the usage documents, and the related change records |
| Added, removed, or renamed documents | Document index (`docs.index`), and the links that point to the document |
| Every change with a linked issue | Confirmed and open items of the design documents that the issue links, and the issue checklist |
| Change to a public API, UI, setting, or run procedure | Related usage documents |
| Design decision, or fix for a problem that can happen again | Whether a topic change record is necessary |

Folders outside version control (local notes, agent settings, and similar) are not in the commit, so do not review them.

## Step 3 — Verdict for each document

Read **only the related sections** of the selected documents, and compare them with the change. Do not read whole documents again or check widely.

| Verdict | Criterion |
|---|---|
| Updated | The commit already contains the correct change |
| Needs update | A statement became wrong or is missing because of this change |
| No effect | The map selected it, but the change does not affect the statements (one-line reason) |

- Also check that no document claims a build or run result that was not checked. Keep implementation done and user confirmation separate.
- If the commit has Markdown documents, check the relative links and the in-document anchors of the changed documents yourself.

## Step 3b — Description comment check

Always do this step when the commit has code changes, separately from the map.

1. In each `git diff` hunk, find the functions, properties, types, and tags whose behavior changed. Include renames, default value changes, and changes to conditions, return values, and failure handling.
2. Read the description comment of each such declaration. If only an implementation file changed, read the comment in the header or the file that has the declaration. Include comments that show as editor tooltips, and tag descriptions (such as `DevComment`).
3. Decide whether each comment matches the current behavior. Put the verdict in the same table as Step 3 (Updated, Needs update, No effect), as a row "Description comment: <file>". If no declaration changed its behavior, write one row with "No effect" and the reason.

Read only the comments of the declarations in the diff. If a comment in another file or a document describes the same behavior, the map of Step 2 covers it. If you do not know the behavior, do not guess and change the comment. Report it as "Needs update".

## Step 4 — Report and apply

Report to the user with a table. Write the report in the language of the conversation.

```
## Pre-commit document review

| Document | Verdict | Details |
|---|---|---|
```

- **If an item needs an update**, show the fix and ask whether to apply it. If the user agrees, put it in the same commit. If the user says "documents later", commit as is. Write the documents that are not updated in the trailer, and if there is a linked issue, suggest an issue comment draft for the remaining document work.
- If all items are Updated or No effect, say so in one line and commit at once. If the user already asked for the commit, do not ask again.

## Step 5 — Commit message trailer

Add one line to the last trailer block of the commit message (above `Co-Authored-By`). Write it in the language of the commit message.

```
Docs-Reviewed: usage and related change records updated, editor guide not affected
Docs-Reviewed: 2 description comments updated, usage not affected
Docs-Reviewed: documents only, README links checked
Docs-Reviewed: editor guide not updated (handled in #12)
```

- If `tracker_public` is true, do not include local paths or session notes.
- If `feature-impl` implemented the change in this conversation, also put its evidence lines (`Risk:`, `Tested:`, and `Revert:` when necessary) in the same block. The format follows feature-impl Step Final "2) Commit preparation". Do not add them to other commits. The hook does not check these lines.
- If there is a linked issue, write `#N` in the title or the body. Use a keyword that closes the issue automatically only after the user confirms completion.
