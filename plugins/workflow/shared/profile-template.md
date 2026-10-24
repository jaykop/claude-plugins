---
# workflow 프로필 — 프로젝트마다 하나. 위치: <프로젝트 루트>/.claude/workflow/profile.md
# 팀과 공유할 값만 둔다. 개인 값(작업 가능 시간 등)은 같은 폴더의 profile.local.md 에 두고 버전 관리에서 뺀다.
# 값 옆 주석에 출처를 적는다: [사용자] 사용자가 확정 / [파일] 프로젝트 파일에서 읽음 / [추정] 확인 필요
# 훅과 스크립트는 이 머리 부분의 최상위 `키: 값` 한 줄만 읽는다. 목록과 하위 항목은 스킬이 읽는다.
profile_version: 1
updated:                      # YYYY-MM-DD
project_name:

# ── 지침과 범위 ─────────────────────────────────────
instructions: [AGENTS.md]     # 프로젝트 지침 파일. 이 플러그인의 스킬보다 우선한다
scope_sections: []            # 범위·구조·모듈 경계가 적힌 지침의 위치. 예: ["AGENTS.md 프로젝트와 현재 범위", "AGENTS.md 모듈 경계"]
coding_rules: []              # 코딩 규칙이 적힌 위치. 스킬은 규칙을 복사하지 않고 매번 이 위치를 읽는다
source_roots: []              # 코드 탐색 범위. 예: [Plugins/*/Source, Source]
risk_paths:                   # 위험 등급을 정하는 경로(glob). 어디에도 걸리지 않는 코드 변경은 mid. 경로와 무관한 기준은 feature-impl Step 0-C
  high: []                    # 예: [Source/**/Save*/**, .github/workflows/**, Config/Default*.ini]
  low: []                     # 예: [Docs/**, Tools/Scripts/**]

# ── 이슈 트래커 ─────────────────────────────────────
tracker: github               # github / none
tracker_repo:                 # owner/repo
tracker_public: true          # 공개 저장소면 이슈·커밋에 로컬 경로, 개인 설정, 시행착오를 쓰지 않는다
issue_template:               # 이슈 본문 양식. 예: .github/ISSUE_TEMPLATE/work.md
status_labels:                # 상태 라벨 이름. 비우면 상태 라벨 제안을 건너뛴다
  in_progress: "status: in-progress"
  needs_verification: "status: needs-verification"
  blocked: "status: blocked"
priority_scheme: grade        # grade(중요도×규모, shared/priority-scheme.md) / none
backlog_goal:                 # 마일스톤 없는 이슈의 중요도를 매기는 기준 목표
milestone_view_url:           # 마일스톤을 시작할 때 갱신을 안내할 이슈 뷰 주소. 없으면 비움

# ── 버전 관리와 커밋 ────────────────────────────────
vcs: git
commit_policy:                # 커밋 범위·대상 규칙이 적힌 위치. 예: "AGENTS.md 커밋과 저장소별 추적 범위"
commit_gate: false            # true 면 트레일러 없는 git commit 을 훅이 막는다
commit_trailer: "Docs-Reviewed:"

# ── 문서 ────────────────────────────────────────────
docs:
  index:                      # 문서 목록. 예: docs/README.md
  manual:                     # 현재 사용법 폴더
  devlog:                     # 변경·결정 기록 폴더
  plan:                       # 설계 문서 폴더
  templates: []               # 카테고리별 템플릿 경로
threads_dir: .claude/workflow/threads   # 로컬 인계 메모 폴더. 공개 저장소면 버전 관리에서 빠지는 폴더를 고른다
archive_dir: .claude/workflow/archive   # 완료한 인계 메모 보관 폴더

# ── 검증 ────────────────────────────────────────────
verification: user            # user: 빌드·테스트·검사는 사용자 담당 / agent: 스킬이 필요하면 실행
build_commands: []            # 사용자가 직접 쓰는 빌드 명령 (안내용)
test_setup_mcp:               # 테스트 셋업을 대신할 수 있는 MCP 서버 이름. 예: unreal-mcp. 없으면 비움
test_candidates: []           # feature-impl 결정 카드에 올릴 자동화 테스트 후보의 기준. 비우면 후보 절을 뺀다. 예: ["입출력으로 확인할 수 있는 로직"]
agent_review: true            # false 면 feature-impl 의 에이전트 리뷰(읽기 전용)를 건너뛴다. 칸이 없으면 켜진 것으로 본다
review_guide:                 # 에이전트 리뷰가 읽는 리뷰 지침(프로젝트의 실패 유형). 예: REVIEW.md. 양식 shared/review-guide-template.md

# ── 연동 ────────────────────────────────────────────
description_review: false     # true 면 ko-review 플러그인의 설명 변경 기록(record)을 작업 흐름에 넣는다
doc_writer: claude            # claude / codex. codex 면 feature-doc-sync 가 manual·devlog·plan 대신 문서 지시서를 쓰고, 다른 AI 가 doc-draft 로 쓴 결과를 대조한다
handoff_reminder_turns: 25    # 이 턴 수마다 context-handoff 를 권한다. 0 이면 끈다
---

# 변경 → 문서 대응표

commit-doc-review 가 커밋 파일마다 검토할 문서를 고를 때 쓴다. 해당하는 줄만 본다.

| 변경 경로 | 검토할 문서 |
|---|---|
| 코드 전체 | 연결 이슈의 구현·확인 상태와 변경에 영향을 받는 manual·devlog |
| 문서 추가·삭제·이름 변경 | 문서 목록, 그 문서를 가리키는 링크 |
| 공개 API·UI·설정·실행 방법 변경 | 관련 manual |
| 설계 결정, 반복될 수 있는 문제의 해결 | 주제별 devlog 필요 여부 |

# 설계 점검 항목

feature-impl 이 구현 계획에서 반드시 확인할 프로젝트 설계 원칙. 지침에 이미 있으면 위치만 적는다.

-

# 메모

<!-- 프로젝트 고유의 작업 흐름 결정을 짧게 적는다 -->
