# Priority grade scheme (priority_scheme: grade)

Multiply the importance and the size of an issue to get its grade. Pass grades along blocking relations. Then set the work order for each milestone. `<plugin folder>/scripts/issue_priority.py` does the calculation. If the project instructions set other rules, the instructions take priority.

## Labels

| Kind | Label | Score |
|---|---|---|
| Importance a | `priority: must` / `priority: should` / `priority: could` | 3 / 2 / 1 |
| Size b | `size: S` / `size: M` / `size: L` / `size: XL` | 3 / 2 / 1 / no grade |
| Grade record | `grade: A1` … `grade: C2` | Own grade |

- Set **a** against the goal of the milestone that holds the issue. For the backlog, use the profile `backlog_goal`. Must (3) is work without which the completion criteria cannot be met, and bugs that block progress. Should (2) is work that greatly changes the quality of the result or the cost of rework. Could (1) is convenience and cleanup work.
- **b** is the time the user spends hands-on (build and check, editor work, decisions). S is 1 hour or less, M is 3 hours or less, and L is 8 hours or less. XL (over 8 hours) gets no grade. Split it into sub-issues, and use the parent issue only as a bundle. If you are not sure, use the next larger size.
- The **own grade** is a×b: 9 A1, 6 A2, 4 B1, 3 B2, 2 C1, 1 C2. In the same grade, the issue with the higher a comes first.
- The **effective grade** is the highest grade among the open issues that this issue blocks (Blocked by). It is never lower than the own grade. It changes each time a blocking relation changes, so do not record it as a label.
- Do not keep a C grade issue in a milestone. Split it or move it to the backlog.
- If the milestone description has a line `capacity: Nh` (or `용량: N시간`), the script compares the planned amount with it. The size total uses the middle value of each size (S 1, M 2, L 5.5 hours). If the must issues use more than 60% of the capacity, reduce the milestone goal instead of removing issues.

## Run

```
python "<plugin folder>/scripts/issue_priority.py"
python "<plugin folder>/scripts/issue_priority.py" --milestone M1
python "<plugin folder>/scripts/issue_priority.py" --apply
```

You need a logged-in `gh` CLI and Python 3.8 or later. The script uses `--repo`, then the profile `tracker_repo`, then the gh repository of the current folder. `--apply` changes grade labels. It is a publishing action, so use it only after the user confirms. If characters break in the Windows console, add `PYTHONIOENCODING=utf-8`.

## How to read the output

| Output | Meaning |
|---|---|
| `due` | Milestone due date. Milestones are in due date order. Issues without a milestone are under `Backlog` |
| `capacity`, `planned`, `must` | Value of the capacity line, size total, and size total of must issues |
| `ord` | Order of the issues that you can work on now. If a blocking issue is open, `-` and `[blocked by #N]` |
| `own`, `eff` | Own grade and effective grade. `XL` for XL. `-` if a label is missing |
| `bundles` | Parent issues that have sub-issues. They get no score |

The sort order is: workable or not, effective grade, own importance, issue number.

| Warning | Action |
|---|---|
| `missing priority or size label` | Add the label |
| `multiple priority or size labels` | Keep only one |
| `size XL in milestone` | Split it into sub-issues |
| `grade C… in milestone` | Split it to B or higher, or move it to the backlog |
| `blocker #N is in later …` | Move the blocking issue to the same milestone or an earlier one |
| `dependency cycle detected` | Remove one relation |
| `grade label mismatch` | Fix it with `--apply` |
| `must share over 60%` (header line) | Reduce the milestone goal |

## Limits

- For each issue, the script reads at most 50 labels and at most 50 blocking issues. For sub-issues, it reads only the count, to know whether an issue is a parent.
- `--milestone` only limits the output. Warnings use all open issues.
- A milestone without issues does not appear.
