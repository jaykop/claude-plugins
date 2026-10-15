---
# ko-review 프로필 — 프로젝트마다 하나. 위치: <프로젝트 루트>/.claude/ko-review/profile.md
# 값 옆 주석에 출처를 적는다: [사용자] 사용자가 확정 / [파일] 프로젝트 파일에서 읽음 / [추정] 확인 필요
# 스크립트는 이 머리 부분의 최상위 `키: 값` 한 줄만 읽는다. 목록과 하위 항목은 스킬이 읽는다.
profile_version: 1
updated:                      # YYYY-MM-DD

instructions: [AGENTS.md]     # 프로젝트 지침 파일. 이 플러그인의 규칙보다 우선한다
doc_roots: []                 # 다듬을 문서 폴더. 예: [docs/manual, docs/devlog]
doc_templates: []             # 문서 템플릿. 예: [docs/manual/_Template.md]
code_roots: []                # 주석을 다듬을 코드 폴더. 예: [Source, Plugins]
exclude: []                   # 손대지 않을 폴더. 벤더 코드, 생성 파일
engine:                       # unreal / godot / unity / none — 에디터에 보이는 주석 기준을 고른다
comment_language: ko          # 설명 주석의 언어
code_text_language: en        # 식별자·메타데이터·로그 문자열의 언어. 주석을 다듬을 때 바꾸지 않는다
data_comment_files: []        # 사람이 읽는 설명 칸이 있는 설정·데이터 파일. 예: [Config/Tags/*.ini]

queue_dir: .claude/ko-review/queue   # 설명 변경 목록 폴더. 공개 저장소면 git 에서 빼는 폴더를 고른다
writer: Claude                # 설명을 작성하고 목록에 남기는 쪽
reviewer: Codex               # 대기 항목을 검토하는 쪽
terms_file: .claude/ko-review/terms.json   # 프로젝트 전용 금지어·표기 목록. 없으면 비움
check_runs: user              # user: 빌드·테스트·lint 는 사용자 담당, 요청이 있을 때만 실행 / agent: 스킬이 필요하면 실행
---

# 메모

<!-- 프로젝트 고유의 문체 결정을 짧게 적는다. 예: "UI 이름은 영어 원문 표기", "경어체 대신 평서체" -->
