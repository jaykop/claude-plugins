---
name: next-task
description: "Use for requests such as '다음 뭐 해', '오늘 뭐 하지', '다음 작업', '새 이슈', '이슈 만들어', '이거 이슈로 남겨', '우선순위 다시 매겨'. Using GitHub milestones and the importance x size grade, choose the next work that fits the time available today, post a new issue draft with importance, size, blocking issues, and milestone, or score issues again. It does not implement. It hands over to feature-impl. Not for: reporting and continuing the work in progress (work-start), changing code, or projects whose issue tracker is not GitHub."
when_to_use: "When you choose what to do before you start work, when you record new work as an issue, and when you start or move a milestone or the scope changes and issues need a new score."
argument-hint: "[next work|new issue|score again] [time available today]"
allowed-tools: Read, Glob, Grep, Bash(python *issue_priority.py), Bash(python3 *issue_priority.py), Bash(python *issue_priority.py --milestone *), Bash(python3 *issue_priority.py --milestone *), Bash(gh issue view *), Bash(gh issue list *), Bash(gh api repos/*/milestones*)
---

# Next Task

This is the entry point that chooses work and makes issues. It has three modes.

| Mode | Example requests |
|---|---|
| A. Choose the next work | "다음 뭐 해", "오늘 1시간 있어", "휴일인데 뭐 하지" |
| B. Make a new issue | "이거 이슈로 만들어", "이런 기능 필요해", or feature-impl reports that there is no issue |
| C. Score again | Start of a milestone, an issue moves to another milestone, a scope change, or a large direction decision |

## Paths and profile

- Plugin folder: `${CLAUDE_PLUGIN_ROOT}`. If the value shows as the variable name, it is the folder two levels above this SKILL.md.
- Profile: `<project root>/.claude/workflow/profile.md`. Personal values are in `profile.local.md`. Keys used: `tracker`, `tracker_repo`, `tracker_public`, `issue_template`, `status_labels`, `priority_scheme`, `backlog_goal`, `milestone_view_url`, `threads_dir`, `time_budget_weekday` and `time_budget_holiday` (personal).
- If there is no profile, or `tracker` is not `github`, say that this skill cannot be used and stop. You need a logged-in `gh` CLI.

## Common rules

- The source of the rules is the project instructions. If they conflict with this skill, the instructions win. If `priority_scheme` is `grade`, the grade rules follow `<plugin folder>/shared/priority-scheme.md`.
- Creating an issue, comments, label changes, closing, and `--apply` are publishing actions on the repository. Run them **only after you show a draft and get confirmation**.
- Write issue titles, bodies, and comments in the language that the project instructions set for issues. Write the output to the user in the language of the conversation. The output examples below are in Korean.
- This skill does not implement. After work is chosen, code changes go to `feature-impl`, and document work goes to the matching document skill.
- Run the order calculation as read-only. If characters break in the Windows console, add `PYTHONIOENCODING=utf-8` at the start.
  ```bash
  python "<plugin folder>/scripts/issue_priority.py"
  ```
  If `python` is not available, use `python3`. If the script ends with an error, report it with the output. Do not make up an order without the script.

---

## A. Choose the next work

### A1. Time today

If the user gave a time, use it. If not, check whether today is a weekday or a weekend day or holiday, and use `time_budget_weekday` or `time_budget_holiday` of the personal profile. If there is no value, ask. Say in one line which value you used. If the user corrects it, choose again with the new value.

### A2. Read the order

Run the script. Read the order table, the waiting list, and the warnings of the milestone with the earliest due date. If issues have the `status_labels.in_progress` label, check them too.

### A3. Choose

1. Go through the workable issues in order, and find the first issue that fits the time today. S fits 1 hour, and M fits 3 hours. L does not finish in one session, so set the slice to finish today.
2. If the first issue is larger than the time today, recommend one of these two.
   - The first issue, if its effective grade is higher than the next issue that fits the time, and it has a slice that can finish today (one decision, one check, one set of assets).
   - If not, the next issue that fits the time.
   Write the option you did not recommend in one line.
3. Do not move an in-progress issue to the front if it is later in the order. But if the handoff note gives a reason to continue it (a half-made result, a postponed decision), write it as an alternative with the reason.

### A4. Set the scope

Read the body of the chosen issue (`gh issue view <N>`) and its handoff note (`<threads_dir>/<N>-*.md`). Of the design documents that the body links, read only the related items.

### A5. Output

```
## 오늘 할 일: #N <제목>
등급 <자체>/<유효> · 규모 <b> · 오늘 <시간> 기준

- 오늘 범위: <오늘 끝낼 것. 조각이면 조각만>
- 끝났다고 볼 기준: <확인 방법 하나>
- 필요한 것: <빌드 / 에디터 작업 / 결정 / 없음>

참고
- 대안: <추천하지 않은 쪽 한 줄>
- 대기 중인 A 등급: #x (선행 #y)
- 진행 중: #z
- 경고: <스크립트 경고. 없으면 생략>
```

At the end, ask whether to start ("시작할까요?"). If the user starts, code changes go to `feature-impl`, design decisions go to a discussion of the design document, and editor work goes to step-by-step guidance.

---

## B. Make a new issue

### B1. Duplicate check

```bash
gh issue list --state all --search "<keywords>" --limit 10
```

If an issue overlaps, do not make a new one. First ask whether to continue that issue or to make its scope larger.

### B2. Classify

- Kind and area labels follow the label rules of the project instructions.
- Milestone: read the descriptions.
  ```bash
  gh api repos/<owner/repo>/milestones --jq '.[] | "\(.title)\t\(.due_on)\n\(.description)\n"'
  ```
  Put the issue in a milestone only if a milestone in progress requires this work. "Requires" means that you can name, in one line, which completion criterion of the milestone description needs it. If you cannot, the backlog is the default. If the user still wants it in the milestone, write the user's reason as the basis.
- a: set it against the completion criteria of the target milestone. For the backlog, set it against profile `backlog_goal`.
- b: set it by the time that the user spends hands-on. If the technology is new or the result is hard to predict, use the next larger size.
- Blocking: find the issues that this work must wait for, and the issues that this work will block.
- For XL, also make a plan that splits the issue into sub-issues. Give each sub-issue an a and a b, and give the parent issue only `size: XL`.

### B3. Rule check

- If the issue goes into a milestone and its grade is C, suggest a split to B or higher, or the backlog.
- If a must issue goes into a milestone, add the size of this issue (S 1, M 2, L 5.5 hours) to the `must` share of the script output, and check whether it goes over 60%.
- If an issue that is not must goes into a milestone, show the open size total of that milestone plus the size of this issue, next to the capacity in the milestone description. If the total is over the capacity, also suggest the backlog.
- If a blocking issue is in a later milestone or in the backlog, suggest moving it too.

### B4. Draft

The body follows the profile `issue_template` format. If there is none, write the goal, scope, completion conditions, related documents, and confirmed decisions. If `tracker_public` is true, do not include local paths, personal settings, session notes, or trial and error, and use a design document link in place of design details.

Show the following metadata together with the body.

```
제목: <제목>
라벨: type: … · priority: … · size: … · grade: … (프로젝트 라벨 규칙에 따라 영역 라벨 추가)
마일스톤: <제목 또는 백로그>
마일스톤 근거: <넣으면 필요한 완료 기준 한 줄과 열린 규모 합/용량, 백로그면 그 이유 한 줄>
선행: #… / 막음: #… / 상위: #…
a 근거: <한 줄>
b 근거: <한 줄>
```

### B5. Post (after confirmation)

```bash
gh issue create --repo <owner/repo> --title "<title>" --body-file <temporary draft file> \
  --label "type: …" --label "priority: …" --label "size: …" --label "grade: …" --milestone "<milestone title>"
```

Link blocking relations and sub-issues with the REST API. `issue_id` and `sub_issue_id` are database ids, not issue numbers.

```bash
gh api repos/<owner/repo>/issues/<N> --jq .id
gh api -X POST repos/<owner/repo>/issues/<blocked issue>/dependencies/blocked_by -F issue_id=<id of the blocking issue>
gh api -X POST repos/<owner/repo>/issues/<parent issue>/sub_issues -F sub_issue_id=<id of the sub-issue>
```

After posting, run the script again. Report the position of the new issue in the order, and any new warning.

---

## C. Score again

### C1. Target

- Start of a milestone: all issues of that milestone
- Move to another milestone: the moved issues (set a again against the goal of the new milestone)
- Scope change: the changed issues and the issues that they block
- Large direction decision: scan the whole backlog for candidates to move into a milestone

### C2. Suggestion

Read the script output and the issue bodies. Show only the issues to change, in a table.

```
| 이슈 | 현재 a·b·등급 | 제안 a·b·등급 | 이유 |
```

### C3. Apply (after confirmation)

```bash
gh issue edit <N> --repo <owner/repo> --add-label "priority: …" --remove-label "priority: …"
python "<plugin folder>/scripts/issue_priority.py" --apply
```

`--apply` sets the grade labels to the own grade. Include it in the approval request for the label changes.

When a milestone starts and profile `milestone_view_url` has a value, tell the user to change the search term (`milestone:"…"`) of that issue view to the new milestone name. GitHub search has no "current milestone" filter.

When a milestone ends, suggest comparing the actual time of the closed issues with their sizes. If work collects in one size, move the time limits between sizes instead of adding more sizes.
