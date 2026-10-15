#!/usr/bin/env bash
# 시험용 프로젝트: PM 고문이 Step 0 에서 묻지 않도록 필요한 프로필 칸을 채우고,
# 정기 점검표와 "점검 전"인 기술 부채 기록을 둔다. 트래커는 쓰지 않는다.
set -eu

mkdir -p .claude/advisors/reports/_state

cat > .claude/advisors/profile.md <<'EOF'
---
profile_version: 1
updated: 2026-10-01

project_name: EvalGame          # [사용자] 시험용 이름
genre: 3인칭 액션               # [사용자]
play_mode: 싱글                 # [사용자]
platforms: [PC-Steam]           # [사용자]
dev_stage: 본 제작              # [사용자]
next_milestone: 알파 2027-03-31 # [사용자]
team_size: 1명 [사용자]
feature_cutoff: 2027-02-01      # [사용자]

source_roots: [Source]          # [사용자]
vcs: git                        # [사용자]
vcs_read_commands: []           # [사용자] 없음

decision_owners:
  design: 클라이언트 프로그래머(이 프로필을 쓰는 사람)   # [사용자]
  tech: 클라이언트 프로그래머(이 프로필을 쓰는 사람)     # [사용자]
  schedule: 클라이언트 프로그래머(이 프로필을 쓰는 사람) # [사용자]
user_role: 클라이언트 프로그래머   # [사용자]

report_dir: .claude/advisors/reports
share_scope: personal
stale_after_days: 90
code_change_entry:              # [사용자] 모름
search_banned_terms: []         # [사용자] 없음
search_banned_combos: []        # [사용자] 없음

design:
  principles:                   # [사용자] 모름
  playtest_records: []          # [사용자] 없음

pm:
  knowledge_dir:                # [사용자] 없음
  tracker: none                 # [사용자]
  tracker_repo:                 # [사용자] 없음
  size_hours: {}                # [사용자] 없음
  must_label:                   # [사용자] 없음
  blocked_label:                # [사용자] 없음
  progress_label:               # [사용자] 없음
  order_labels: []              # [사용자] 없음
  next_task_entry:              # [사용자] 없음
  capacity: {weekday_hours: 2, holiday_hours: 4, plan_ratio: 0.7}   # [사용자]
  holidays: []                  # [사용자] 없음
  must_ratio_limit: 0.6
  week_start: 월
---
EOF

cat > .claude/advisors/reports/_state/pm-cadence.md <<'EOF'
# PM 정기 점검표

다음 점검: 2026-10-08
작성: pm / 마지막 갱신: 2026-10-01 / 기준 리비전: 확인 못 함

| ID | 점검 | 실행 방법 | 주기 | 기록 패턴 | 마지막 실행 | 메모 |
|---|---|---|---|---|---|---|
| PC-001 | 주간 점검 | /advisors:pm 주간 점검 | 7 | pm/*-weekly*.md | - | |
| PC-009 | 기술 부채 점검 | /advisors:td 구조 점검 기술 부채 | 마일스톤 30일 전 | 갱신:_state/td-debt.md | - | 구조 점검 리포트는 범위가 섞이므로 기술 부채 기록의 마지막 갱신으로 본다 |
EOF

cat > .claude/advisors/reports/_state/td-debt.md <<'EOF'
# TD 고문 기술 부채 기록

다음 점검: 마일스톤 30일 전
작성: td / 마지막 갱신: 점검 전 / 기준 리비전: 확인 못 함

| ID | 종류 | 위치 | 근거 수치와 명령 | 순위 | 갚는 범위 | 상태 | 마지막 확인일 |
|---|---|---|---|---|---|---|---|
EOF
