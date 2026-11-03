---
# workflow profile. One per project, at <project root>/.claude/workflow/profile.md
# Keep only the values the team shares. Put personal values (such as available hours) in profile.local.md in the same folder, and keep that file out of version control.
# Write the source next to each value: [user] the user confirmed it / [file] read from a project file / [guess] must be confirmed
# Hooks and scripts read only the top-level `key: value` lines of this header. Skills read the lists and nested items.
profile_version: 1
updated:                      # YYYY-MM-DD
project_name:

# ── Instructions and scope ──────────────────────────
instructions: [AGENTS.md]     # Project instruction files. They take priority over the skills of this plugin
scope_sections: []            # Where the instructions describe scope, structure, and module boundaries. Example: ["AGENTS.md Project and current scope", "AGENTS.md Module boundaries"]
coding_rules: []              # Where the coding rules are. Skills do not copy the rules. They read this location each time
source_roots: []              # Code search scope. Example: [Plugins/*/Source, Source]
risk_paths:                   # Path globs that set the risk level. A code change that matches no glob is mid. For criteria that do not depend on the path, see feature-impl Step 0-C
  high: []                    # Example: [Source/**/Save*/**, .github/workflows/**, Config/Default*.ini]
  low: []                     # Example: [Docs/**, Tools/Scripts/**]

# ── Issue tracker ───────────────────────────────────
tracker: github               # github / jira / none. Only work-start reads jira now
tracker_repo:                 # github: owner/repo
tracker_project:              # jira: project key. Example: ABC
tracker_site:                 # jira: site address. Example: example.atlassian.net. Leave empty if there is only one site
tracker_query:                # jira: JQL that finds issues in progress. If empty, work-start uses its default condition
tracker_public: true          # If the repository is public, do not write local paths, personal settings, or trial and error in issues and commits
issue_template:               # Issue body template. Example: .github/ISSUE_TEMPLATE/work.md
status_labels:                # Status label names. If empty, the skills do not suggest status labels
  in_progress: "status: in-progress"
  needs_verification: "status: needs-verification"
  blocked: "status: blocked"
priority_scheme: grade        # grade (importance x size, shared/priority-scheme.md) / none
backlog_goal:                 # The goal that sets the importance of issues without a milestone
milestone_view_url:           # Address of the issue view to update when a milestone starts. Leave empty if there is none

# ── Version control and commits ─────────────────────
vcs: git                      # git / p4. For p4, only the status query of work-start works now
commit_policy:                # Where the rules for commit scope and targets are. Example: "AGENTS.md Commits and tracking scope"
commit_gate: false            # If true, the hook blocks git commit without the trailer
commit_trailer: "Docs-Reviewed:"

# ── Documents ───────────────────────────────────────
docs:
  index:                      # Document index. Example: docs/README.md
  manual:                     # Folder for current usage documents
  devlog:                     # Folder for change and decision records
  plan:                       # Folder for design documents
  templates: []               # Template path for each category
threads_dir: .claude/workflow/threads   # Folder for local handoff notes. For a public repository, choose a folder that is not in version control
archive_dir: .claude/workflow/archive   # Folder for handoff notes of finished work

# ── Verification ────────────────────────────────────
verification: user            # user: the user runs builds, tests, and checks / agent: skills run them when necessary
build_commands: []            # Build commands that the user runs (for guidance only)
test_setup_mcp:               # Name of an MCP server that can do the test setup. Example: unreal-mcp. Leave empty if there is none
test_candidates: []           # Criteria for automated test candidates on the feature-impl decision card. If empty, the card has no candidate section. Example: ["Logic that you can check through input and output"]
agent_review: true            # If false, feature-impl skips the read-only agent review. If the key is missing, the review is on
review_guide:                 # Review guide that the agent review reads (the failure types of the project). Example: REVIEW.md. Template: shared/review-guide-template.md

# ── Integration ─────────────────────────────────────
handoff_reminder_turns: 25    # Suggest context-handoff each time the session reaches a multiple of this many turns. 0 turns it off
---

# Change → document map

commit-doc-review uses this map to select the documents to review for each committed file. It reads only the rows that apply. Older profiles call this section "변경 → 문서 대응표".

| Changed path | Documents to review |
|---|---|
| All code | Implementation and confirmation state of the linked issue, and the manual and devlog that the change affects |
| Added, removed, or renamed documents | Document index, and the links that point to the document |
| Change to a public API, UI, setting, or run procedure | Related manual |
| Design decision, or fix for a problem that can happen again | Whether a topic devlog is necessary |

# Design checklist

Project design principles that feature-impl must check in the implementation plan. If the instructions already contain a principle, write only its location. Older profiles call this section "설계 점검 항목".

-

# Notes

<!-- Write short decisions about the work process of this project -->
