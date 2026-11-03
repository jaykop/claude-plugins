---
# advisors profile — one per project. Location: <project root>/.claude/advisors/profile.md
# In the comment next to a value, write its source tag: [사용자] confirmed by the user / [파일] read from a project file / [추정] estimated by the advisor, needs confirmation
# Each advisor has a knowledge_dir key: the team reference notes folder that the advisor follows first as its decision criteria. It can hold private material. Read index.md first
profile_version: 1
updated:                      # YYYY-MM-DD

# ── Common ───────────────────────────────────────────
project_name:
genre:                        # e.g. third-person action, co-op shooter
play_mode:                    # 싱글 / 협동 / 대전 / 혼합 (= single / co-op / versus / mixed)
ip_based:                     # false, or the name of the original work
platforms: []                 # Highest priority first. e.g. [PC-Steam, PS5]
target_spec:                  # Minimum spec and recommended spec
regions: []                   # Release regions. Highest priority first
business_model:               # 패키지 / 부분 유료 / 구독 / 미정 (= premium / free-to-play with paid items / subscription / undecided)
release_window:               # e.g. 2027 H2, 미정 (= undecided)
dev_stage:                    # 프리프로덕션 / 본 제작 / 알파 / 베타 / 라이브 (= preproduction / production / alpha / beta / live)
next_milestone:               # Name and date. e.g. 알파 2027-03-31 (date in YYYY-MM-DD)
team_size:                    # Number of developers and its source. e.g. about 40 people [사용자]. The technology trend advisor uses it to pick 'shipped cases of similar scale' (비슷한 규모의 출시 사례)
feature_cutoff:               # Feature addition deadline YYYY-MM-DD. If it has passed, the design advisor moves large addition proposals to 'next-stage candidate' (다음 단계 후보)
report_language: en           # en / ko. Language of reports and of new _state files (labels and the lines that scripts read, such as Next check: / 다음 점검:). The conversation with the user uses the conversation language

engine:
  kind:                       # unreal / godot. Advisor documents are written for Unreal. If godot, read them remapped as in shared/engine-godot.md
  name:                       # e.g. Unreal Engine, Godot Engine
  version:                    # e.g. 5.6.1, 4.3.0
  source_build:               # true means a source build (custom engine)
  run_wrapper:                # Godot only: the leading part of the project command that launches Godot (a locking and output-capturing wrapper, or the console executable). When the advisor writes a Godot command in a measurement plan or a test spec, it puts this in front. e.g. 'python tools/godot_run.py --timeout=300 --'
  root:                       # Engine folder path. For Unreal, fill it even if it is not a source build (launcher install). Used to check in the engine source that console command and setting names really exist. For Godot, only for a custom build: the engine source folder (where version.py is)

source_roots: []              # Game code folders (shared by design · radar · perf · td). Patterns such as `Plugins/*/Source` are allowed. For Godot, empty means the whole folder that contains project.godot. If that folder is a subfolder (e.g. game/), code outside it is out of scope, so to include that code, list both the project folder and the outside folders
project_file:                 # Project file. e.g. Game/MyGame.uproject, project.godot

vcs: git                      # git / p4 / 기타 (= other)
vcs_read_commands: []         # Read commands the advisor can use. e.g. [git log, git show] or [p4 filelog, p4 changes, p4 describe, p4 fstat]

decision_owners:              # Decision owner per area. If it is not the user, downgrade proposals to 'reference option' (참고 선택지)
  design:
  business:                   # Release timing, regions, price, business model
  tech:                       # Engine version upgrades, technology adoption (radar), code structure and design choices (td)
  schedule:                   # Milestone scope, task order, schedule (PM advisor)
user_role:                    # Role of the person who uses this profile. e.g. client programmer

report_dir: .claude/advisors/reports   # Path relative to the project root, or an absolute path
share_scope: personal         # personal / team
stale_after_days: 90          # When you cite another advisor's report older than this, mark it as 'outdated report' (오래된 리포트)
code_change_entry:            # Name of the skill to hand code changes to. Leave empty if there is none
search_banned_terms: []       # Words that must not go into search queries. Internal code names, names of unannounced features, and so on
search_banned_combos: []      # Combinations that reveal unannounced information when used together. e.g. ["<IP 이름> + 협동"]

# ── Design advisor ───────────────────────────────────
design:
  roots: []                   # Folders of the current design documents
  exclude: []                 # Folders that are reference material, so they do not count as the current design
  summaries:                  # Path pattern of area summary documents. Leave empty if there are none
  principles:                 # Document and location where the top principles / pillars / pillar priority / prohibition principles are written
  principles_status:          # 확정 / 가안 (= confirmed / draft)
  playtest_records: []        # Playtest record folders
  data_paths: []              # Balance data files
  data_status:                # 확정 / 임시값 (= confirmed / placeholder values). If 임시값, judge by rules only instead of numeric calculation
  principles_confirmed:       # Date and base revision when the principles were last confirmed. Format: "YYYY-MM-DD, 기준 리비전 <값>"
  archive_dirs: []            # Folders that keep proposals that were not adopted. Do not use them as evidence. Read them only to check whether a proposal was already rejected
  deprecated_marker: []       # Marker on deprecated documents. If there are several, use a list. e.g. ["[폐기]", "DEPRECATED"]
  glossary:                   # Location of the glossary document
  area_file_patterns: {}      # File name patterns per area, when the design documents are not split into folders per area. e.g. {전투: "combat_*.md"}
  existing_tools: []          # Design tools already in use. Item format "<role>: <tool name> — <output location>"
                              # The role is one of four: 문서 리뷰 / 관찰 포인트 게시 / 피드백 정리 / 수치 분석 (= document review / posting observation points / organizing feedback / numeric analysis)
  knowledge_dir:              # Folder of notes on design judgment criteria (review criteria the team set, lessons from past verdicts). Put principles (pillars) in principles. Reading rules: shared/rules.md §13

# ── Technology trend advisor ─────────────────────────
radar:
  engine_mod_marker:          # Marker of the start line of an engine modification block. By default it is read as a regular expression. It must match only the start line (if it also matches the end line, the block count doubles). e.g. '// MYGAME_BEGIN'
  engine_mod_end_marker:      # Marker of the end line of an engine modification block. td uses it when it lists the blocks. e.g. '// MYGAME_END'
  engine_mod_tag_re:          # Regular expression that extracts a topic tag from the text after the start marker. It must have one capture group (the part in parentheses). If empty, the text inside square brackets is used. e.g. '\[([^\]]+)\]'
  engine_mod_dirs: []         # Folders in which to count engine modification blocks. Relative paths are relative to engine.root. Narrow them so that the whole engine is not searched
  interests: []               # Areas to watch closely
  excluded: []                # Areas not to watch
  ai_tool_policy:             # Whether the company's AI tool policy has been checked. 미확인 / 허용 / 제한 (= unchecked / allowed / restricted)
  community_sources:          # Community channels for finding news. They are for finding 'what people are talking about', not evidence for verdicts
    auto: [qiita, geeknews, tencent-gameinstitute]   # Channels read automatically. Channel names are in the '10. Community channels' section of skills/radar/reference/sources.md
    manual: [reddit, zhihu]   # Channels where automatic access is blocked. Read them only when the user pastes posts or hands them over as files
  knowledge_dir:              # Folder of notes on technology adoption criteria (internal adoption process, kinds of technology to avoid, and so on). Reading rules: shared/rules.md §13

# ── Market advisor ───────────────────────────────────
market:
  competitors_seed: []        # Comparison games that the user named
  target_player:              # Target players that the team set (a decision. The market advisor looks at the gap between this and the confirmed player base)
  paid_data_files: []         # Paid data files that the user provided
  price_band:                 # Expected price band and currency. e.g. 39.99~49.99 USD
  check_interval: quarterly   # Change check interval. Also used as the default 'recheck date' (다시 확인할 날짜) of rows that market adds to source-checks.md
  knowledge_dir:              # Folder of notes on market judgment criteria (internal rules for reading metrics, regional conditions, and so on). Reading rules: shared/rules.md §13

# ── Optimization advisor ─────────────────────────────
perf:
  budgets: {}                 # Targets per platform. e.g. {PC-min: {fps: 60, frame_ms: 16.6, memory_gb: 8}}. For a game whose budget is processing time, write it like {PC: {day_ms: 300, match_ms: 30}}
  scenarios: []               # Representative measurement scenes. e.g. [{id: S01, map: ..., 설명: 적 20명 전투}]
  profiling_dir:              # Folder for measurement files (.utrace, .csv). A relative path is relative to the project root. For Godot, the folder where the measurement script saves CSV files
  measured_by:                # Who measures. 사용자 / 빌드 머신 / 에디터 자동화 (= user / build machine / editor automation)
  test_command:               # Command that runs the automated tests
  test_convention:            # Location and naming rules of the existing tests
  edit_scope: tests_only      # tests_only / source
  knowledge_dir:              # Folder of notes on performance judgment criteria (the team's measurement procedure, cautions per platform, and so on). Reading rules: shared/rules.md §13

# ── PM advisor ───────────────────────────────────────
pm:
  knowledge_dir:              # Folder of notes on schedule, risk, and retrospective criteria (it can hold private material). Reading rules: shared/rules.md §13
  tracker:                    # github / none
  tracker_repo:               # owner/repo
  size_hours: {}              # Size label → hours. e.g. {"size: S": 1, "size: M": 2, "size: L": 5.5}
  must_label:                 # Label for required tasks. e.g. "priority: must"
  blocked_label:              # Label for waiting tasks. e.g. "status: blocked"
  progress_label:             # Label for in-progress tasks
  order_labels: []            # Project order labels. Earlier labels come first. e.g. ["grade: A1", "grade: A2", "grade: B1"]
  next_task_entry:            # Skill to hand issue order confirmation and posting to. e.g. workflow:next-task
  capacity:                   # {weekday_hours: 2, holiday_hours: 4, plan_ratio: 0.7}. For personal values, use capacity_file below
  capacity_file:              # Another file (outside version control) that holds the daily work hours. Do not copy its values into this profile
  capacity_keys: {}           # Key names in capacity_file. e.g. {weekday_hours: time_budget_weekday, holiday_hours: time_budget_holiday}
  holidays: []                # List of public holidays YYYY-MM-DD. If empty, public holidays count as weekdays
  must_ratio_limit: 0.6       # Limit on the share of the plannable time that the size of required tasks can take
  week_start: 월              # Day of the week that weekly checks start from (월 = Monday)

# ── TD advisor ───────────────────────────────────────
td:
  rule_docs: []               # Team technical rule documents (paths or wildcard patterns. e.g. Docs/*.md). First-priority evidence. e.g. [Dev/Client/CLAUDE.md, Docs/CodingStandard.md]
  record_roots: []            # Folders of design records, incident records, and backlogs. Read the cause analyses in those documents as 'source document's estimate' (출처 문서의 추정)
  extra_roots: []             # Build, deploy, server, and tool folders outside source_roots to read
  vanilla_engine_root:        # Vanilla engine source folder (local). If set, compare engine modification blocks and per-version behavior locally
  engine_base_ref:            # Vanilla engine baseline on the version control server (p4 stream or git branch). Used to count the change history, on the vanilla engine side, of files that contain engine modification blocks
  knowledge_dir:              # Folder of notes on design judgment criteria (principles for structural choices, engine modification policy, and so on). Put coding rule documents in rule_docs. Reading rules: shared/rules.md §13
---

# Profile notes

Older profiles call this section "프로필 메모". Write here the circumstances that the values above cannot fully hold. Examples: why the data is provisional, areas with two decision owners, cautions about search terms.
