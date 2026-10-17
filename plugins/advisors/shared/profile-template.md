---
# advisors 프로필 — 프로젝트마다 하나. 위치: <프로젝트 루트>/.claude/advisors/profile.md
# 값 옆 주석에 출처를 적는다: [사용자] 사용자가 확정 / [파일] 프로젝트 파일에서 읽음 / [추정] 고문이 추정, 확인 필요
# 고문마다 knowledge_dir 칸이 있다: 그 고문이 판정 기준으로 먼저 따를 팀 기준 노트 폴더. 비공개 자료여도 된다. index.md 부터 읽는다
profile_version: 1
updated:                      # YYYY-MM-DD

# ── 공통 ─────────────────────────────────────────────
project_name:
genre:                        # 예: 3인칭 액션, 협동 슈터
play_mode:                    # 싱글 / 협동 / 대전 / 혼합
ip_based:                     # false, 또는 원작 이름
platforms: []                 # 1순위부터. 예: [PC-Steam, PS5]
target_spec:                  # 최저 사양과 권장 사양
regions: []                   # 출시 지역. 1순위부터
business_model:               # 패키지 / 부분 유료 / 구독 / 미정
release_window:               # 예: 2027 하반기, 미정
dev_stage:                    # 프리프로덕션 / 본 제작 / 알파 / 베타 / 라이브
next_milestone:               # 이름과 날짜. 예: 알파 2027-03-31 (날짜는 YYYY-MM-DD)
team_size:                    # 개발 인원과 출처. 예: 약 40명 [사용자]. 기술 동향 고문이 '비슷한 규모의 출시 사례'를 가릴 때 쓴다
feature_cutoff:               # 기능 추가 마감일 YYYY-MM-DD. 지났으면 기획 고문이 큰 추가 제안을 '다음 단계 후보'로 돌린다

engine:
  name:                       # 예: Unreal Engine
  version:                    # 예: 5.6.1
  source_build:               # true 면 소스 빌드(커스텀 엔진)
  root:                       # 엔진 폴더 경로. 소스 빌드가 아니어도(런처 설치본) 적는다. 콘솔 명령·설정 이름이 실제로 있는지 엔진 소스에서 확인할 때 쓴다

source_roots: []              # 게임 코드 폴더 (design · radar · perf · td 공용). `Plugins/*/Source` 같은 패턴을 쓸 수 있다
project_file:                 # 프로젝트 파일. 예: Game/MyGame.uproject

vcs: git                      # git / p4 / 기타
vcs_read_commands: []         # 고문이 써도 되는 읽기 명령. 예: [git log, git show] 또는 [p4 filelog, p4 changes, p4 describe, p4 fstat]

decision_owners:              # 영역별 결정권자. 사용자가 아니면 제안을 '참고 선택지'로 낮춘다
  design:
  business:                   # 출시 시점, 지역, 가격, 수익 모델
  tech:                       # 엔진 버전 올리기, 기술 도입(radar), 코드 구조·설계 선택(td)
  schedule:                   # 마일스톤 범위, 작업 순서, 일정 (PM 고문)
user_role:                    # 이 프로필을 쓰는 사람의 역할. 예: 클라이언트 프로그래머

report_dir: .claude/advisors/reports   # 프로젝트 루트 기준 상대 경로 또는 절대 경로
share_scope: personal         # personal / team
stale_after_days: 90          # 다른 고문 리포트를 인용할 때 이보다 오래되면 '오래된 리포트'로 표시
code_change_entry:            # 코드 수정을 맡길 스킬 이름. 없으면 비움
search_banned_terms: []       # 검색어에 넣으면 안 되는 말. 내부 코드 이름, 미발표 기능 이름 등
search_banned_combos: []      # 함께 넣으면 미발표 정보가 되는 조합. 예: ["<IP 이름> + 협동"]

# ── 기획 고문 ─────────────────────────────────────────
design:
  roots: []                   # 현재 기획서 폴더
  exclude: []                 # 참고 자료라서 현재 기획으로 보지 않을 폴더
  summaries:                  # 영역 요약 문서의 경로 패턴. 없으면 비움
  principles:                 # 최상위 원칙 / 필러 / 필러 우선순위 / 금지 원칙이 적힌 문서와 위치
  principles_status:          # 확정 / 가안
  playtest_records: []        # 플레이테스트 기록 폴더
  data_paths: []              # 밸런스 데이터 파일
  data_status:                # 확정 / 임시값 (임시값이면 수치 계산 대신 규칙만 보고 판단)
  principles_confirmed:       # 원칙을 마지막으로 확인한 날짜와 기준 리비전. 형식: "YYYY-MM-DD, 기준 리비전 <값>"
  archive_dirs: []            # 채택되지 않은 안을 보관하는 폴더. 근거로 쓰지 않고, 이미 기각된 안인지 확인할 때만 읽는다
  deprecated_marker: []       # 폐기된 문서에 붙는 표시. 여러 개면 목록으로. 예: ["[폐기]", "DEPRECATED"]
  glossary:                   # 용어집 문서 위치
  area_file_patterns: {}      # 기획서가 영역별 폴더로 나뉘지 않았을 때 영역별 파일 이름 패턴. 예: {전투: "combat_*.md"}
  existing_tools: []          # 이미 쓰는 기획 도구. 항목 형식 "<역할>: <도구 이름> — <산출물 위치>"
                              # 역할은 넷 중 하나: 문서 리뷰 / 관찰 포인트 게시 / 피드백 정리 / 수치 분석
  knowledge_dir:              # 기획 판단 기준 노트 폴더(팀이 정한 심사 기준, 지난 판정에서 배운 것). 원칙(필러)은 principles 에 둔다. 읽는 규칙은 shared/rules.md §13

# ── 기술 동향 고문 ─────────────────────────────────────
radar:
  engine_mod_marker:          # 엔진 수정 블록의 시작 줄 표시. 기본은 정규식으로 읽는다. 시작 줄에만 걸려야 한다(끝 줄에도 걸리면 블록 수가 두 배가 된다). 예: '// MYGAME_BEGIN'
  engine_mod_end_marker:      # 엔진 수정 블록의 끝 줄 표시. td 가 블록 목록을 낼 때 쓴다. 예: '// MYGAME_END'
  engine_mod_tag_re:          # 시작 표시 뒤 글에서 주제 태그를 뽑는 정규식. 캡처 그룹(괄호로 묶은 부분)이 하나 있어야 한다. 비면 대괄호 안 글을 쓴다. 예: '\[([^\]]+)\]'
  engine_mod_dirs: []         # 엔진 수정 블록을 셀 폴더. 상대 경로는 engine.root 기준. 엔진 전체를 검색하지 않도록 좁힌다
  interests: []               # 특히 볼 분야
  excluded: []                # 보지 않을 분야
  ai_tool_policy:             # 회사의 AI 도구 정책 확인 여부. 미확인 / 허용 / 제한
  community_sources:          # 소식을 찾는 커뮤니티 채널. 판정 근거가 아니라 '무엇이 화제인지' 찾는 곳이다
    auto: [qiita, geeknews, tencent-gameinstitute]   # 자동으로 읽는 곳. 채널 이름은 skills/radar/reference/sources.md 의 '커뮤니티 채널' 항목
    manual: [reddit, zhihu]   # 자동 조회가 막힌 곳. 사용자가 글을 붙여 넣거나 파일로 넘겨 줄 때만 읽는다
  knowledge_dir:              # 기술 도입 판단 기준 노트 폴더(사내 도입 절차, 피하는 기술 종류 등). 읽는 규칙은 shared/rules.md §13

# ── 시장 동향 고문 ─────────────────────────────────────
market:
  competitors_seed: []        # 사용자가 지정한 비교 게임
  target_player:              # 팀이 정한 타깃 이용자 (결정. 시장 고문은 이것과 확인된 이용자층의 차이를 본다)
  paid_data_files: []         # 사용자가 넣어 준 유료 데이터 파일
  price_band:                 # 예상 가격대와 통화. 예: 39.99~49.99 USD
  check_interval: quarterly   # 변화 점검 주기. source-checks.md 에서 market 이 넣은 행의 '다시 확인할 날짜' 기본값으로도 쓴다
  knowledge_dir:              # 시장 판단 기준 노트 폴더(사내 지표 해석 기준, 지역별 사정 등). 읽는 규칙은 shared/rules.md §13

# ── 최적화 고문 ───────────────────────────────────────
perf:
  budgets: {}                 # 플랫폼별 목표. 예: {PC-min: {fps: 60, frame_ms: 16.6, memory_gb: 8}}
  scenarios: []               # 대표 측정 장면. 예: [{id: S01, map: ..., 설명: 적 20명 전투}]
  profiling_dir:              # 측정 파일(.utrace, .csv)을 두는 폴더. 상대 경로면 프로젝트 루트 기준
  measured_by:                # 측정 주체. 사용자 / 빌드 머신 / 에디터 자동화
  test_command:               # 자동화 테스트 실행 명령
  test_convention:            # 기존 테스트의 위치·이름 규칙
  edit_scope: tests_only      # tests_only / source
  knowledge_dir:              # 성능 판단 기준 노트 폴더(팀의 측정 절차, 플랫폼별 주의점 등). 읽는 규칙은 shared/rules.md §13

# ── PM 고문 ───────────────────────────────────────────
pm:
  knowledge_dir:              # 일정·위험·회고 기준 노트 폴더(비공개 자료여도 된다). 읽는 규칙은 shared/rules.md §13
  tracker:                    # github / none
  tracker_repo:               # owner/repo
  size_hours: {}              # 규모 라벨 → 시간. 예: {"size: S": 1, "size: M": 2, "size: L": 5.5}
  must_label:                 # 필수 작업 라벨. 예: "priority: must"
  blocked_label:              # 대기 라벨. 예: "status: blocked"
  progress_label:             # 진행 중 라벨
  order_labels: []            # 프로젝트 순서 라벨, 앞일수록 먼저. 예: ["grade: A1", "grade: A2", "grade: B1"]
  next_task_entry:            # 이슈 순서 확정·게시를 맡길 스킬. 예: workflow:next-task
  capacity:                   # {weekday_hours: 2, holiday_hours: 4, plan_ratio: 0.7}. 개인 값이면 아래 capacity_file 을 쓴다
  capacity_file:              # 하루 작업 시간을 적어 둔 다른 파일(버전 관리 밖). 값은 이 프로필에 옮겨 적지 않는다
  capacity_keys: {}           # capacity_file 의 키 이름. 예: {weekday_hours: time_budget_weekday, holiday_hours: time_budget_holiday}
  holidays: []                # 공휴일 YYYY-MM-DD 목록. 비우면 공휴일을 평일로 센다
  must_ratio_limit: 0.6       # 필수 작업 규모가 계획 가능 시간에서 차지할 수 있는 한도
  week_start: 월              # 주간 점검 기준 요일

# ── TD 고문 ─────────────────────────────────────────
td:
  rule_docs: []               # 팀 기술 규칙 문서(경로나 와일드카드 패턴. 예: Docs/*.md). 근거 1순위. 예: [Dev/Client/CLAUDE.md, Docs/CodingStandard.md]
  record_roots: []            # 설계 기록·사고 기록·백로그 폴더. 그 문서 속 원인 분석은 '출처 문서의 추정'으로 읽는다
  extra_roots: []             # source_roots 밖에서 읽을 빌드·배포·서버·도구 폴더
  vanilla_engine_root:        # 순정 엔진 소스 폴더(로컬). 있으면 엔진 수정 블록과 버전별 동작을 로컬에서 비교한다
  engine_base_ref:            # 버전 관리 서버에 있는 순정 엔진 기준(p4 스트림·git 브랜치). 엔진 수정 블록이 든 파일이 순정 엔진 쪽에서 바뀐 이력을 셀 때 쓴다
  knowledge_dir:              # 설계 판단 기준 노트 폴더(구조 선택 원칙, 엔진 수정 방침 등). 코드 작성 규칙 문서는 rule_docs 에 둔다. 읽는 규칙은 shared/rules.md §13
---

# 프로필 메모

위 값으로 다 담지 못한 사정을 적는다. 예: 데이터가 임시값인 이유, 결정권자가 둘인 영역, 검색어 주의 사항.
