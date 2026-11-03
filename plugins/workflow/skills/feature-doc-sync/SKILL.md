---
name: feature-doc-sync
description: "After you develop or change a feature, update the documents that it affects (usage manual, change record devlog, design plan), and write a draft of the result record for the linked issue. Not for: the missing-document check just before a commit (commit-doc-review)."
when_to_use: "After the user chooses documentation in Step Final of feature-impl, or when the user says '문서 정리해' or '매뉴얼 갱신해'."
argument-hint: "[#issue number or work scope]"
---

# Feature document sync

The project instructions and the request of the user take priority. After the implementation, put the current usage in the related documents. This procedure gives no permission to run builds, tests, or separate code checks.

The profile is `<project root>/.claude/workflow/profile.md`. Keys used: `docs` (index, manual, devlog, plan, templates), `tracker`, `tracker_public`, `status_labels`, `threads_dir`. If there is no profile, read the project instructions and the `docs/` layout, and get the document locations confirmed.

## 1. Effect and work state

Keep these items separate: the linked issue, the scope of this implementation, the result of user confirmation, and the remaining work. The work state goes in the issue, the current usage and limits go in the manual, and the reasons for important decisions go in the devlog. Before you post to an issue, prepare a draft and get confirmation from the user. Personal trial and error, local settings, and session notes go in the handoff note (`threads_dir`).

If a public API, UI, setting, run procedure, or the handling of existing data changes, update the related manual in the same work. Do not make a document that summarizes the whole state. Also decide whether an internal implementation change affects an existing description.

## 2. Update the related documents

The language and style of the documents follow the project instructions.

Before you change a document, read the actual template of its category (`docs.templates`). Do not copy templates into this skill.

- Current usage: manual template
- Change, decision, diagnosis: devlog template
- Design of an issue: plan template. Do not write undecided items as the current specification

Update the existing document of the same topic first. If you make a new document or change a document path, update the document index (`docs.index`) and the related links. Do not add a devlog for each simple typo. Keep the judgment of that time and the scope of user confirmation in past records, and link later changes.

## 3. Technical check

Read the paragraphs that you wrote or changed and the items next to them. Check that the configured target, conditions, units, results, and limits match the actual implementation. Do not guess behavior that you do not know. Report it as an open question.

## Completion report

Report briefly: the paths of the related documents, items that need a decision, the result of user confirmation, and the checks that did not run. If there is an issue, prepare a draft of the result record and the document links, and ask the user whether to post it. If only the implementation is done and the user has not confirmed it, suggest the `status_labels.needs_verification` label.
