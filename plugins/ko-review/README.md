# ko-review — 한국어 문서·주석 교정과 설명 변경 부분 검토

한국어 기술 문서와 코드 주석을 관련 구현과 대조해 다듬는 플러그인이다. 한 AI 가 바꾼 설명을 목록에 남기면 다른 AI 가 그 항목의 문장만 교정하는 흐름도 함께 제공한다. 검토하는 AI 는 코드 기능을 검수하지 않는다. Claude Code 와 Codex 양쪽에서 같은 스킬을 쓴다.

| 스킬 | 명령 | 하는 일 |
|---|---|---|
| polish | `/ko-review:polish` | 문서·주석·설정 파일 설명을 관련 구현과 대조해 고친다. 에디터에 보이는 주석은 엔진별 기준을 함께 쓴다 |
| record | `/ko-review:record` | 작성 쪽. 수정 전 파일 상태를 남기고, 수정 뒤 바꾼 설명의 위치와 근거 구현을 등록한다 |
| review | `/ko-review:review` | 검토 쪽. 대기 항목만 읽고 교정한 뒤 결과를 기록한다 |

명령 이름을 외우지 않아도 된다. "이 설명서 문장 다듬어 줘", "이번 작업 설명 변경 기록해", "대기 중인 설명 검토해 줘" 같은 말로도 불린다. Codex 에서 스킬을 부르는 방식은 Codex 의 규칙을 따른다.

## 설치

Claude Code:

```
/plugin marketplace add jaykop/claude-plugins
/plugin install ko-review@jaykop
```

Codex:

```
codex plugin marketplace add jaykop/claude-plugins
```

그다음 Codex 앱의 플러그인 화면에서 `ko-review` 를 설치한다. 업데이트 방법은 [리포 README](../../README.md#업데이트) 를 따른다.

맞춤법·문체 전용 스킬이 필요하면 [DaleSeo/korean-skills](https://github.com/DaleSeo/korean-skills)(MIT)를 따로 설치한다. `polish` 는 이 스킬들이 있으면 필요한 참고만 읽는다.

```
/plugin marketplace add DaleSeo/korean-skills
/plugin install korean-skills@korean-skills
```

## 프로젝트 설정

프로필은 `<프로젝트 루트>/.claude/ko-review/profile.md` 하나다. 양식은 [shared/profile-template.md](shared/profile-template.md) 에 있다. `polish` 는 프로필 없이도 쓸 수 있고, `record` 는 처음 쓸 때 프로필을 만들지 묻는다.

| 칸 | 왜 필요한가 |
|---|---|
| `instructions` | 프로젝트 지침 파일. 이 플러그인의 규칙보다 우선한다 |
| `doc_roots`, `code_roots`, `exclude` | 넓은 범위를 요청받았을 때의 대상과 제외 범위 |
| `engine` | 에디터에 보이는 주석의 기준. 지금은 `unreal` 전용 기준만 있다 |
| `queue_dir` | 설명 변경 목록 폴더. 공개 저장소라면 git 에서 빠지는 폴더를 고른다 |
| `queue_scope` | 목록에 등록할 수 있는 설명 파일의 경로 패턴. 범위 밖 파일은 등록을 거절한다. 비우면 제한하지 않는다 |
| `queue_archive_dir` | `close` 로 닫은 목록을 옮길 폴더. `{year}`·`{quarter}` 를 쓸 수 있다. 비우면 닫은 목록을 제자리에 둔다 |
| `writer`, `reviewer` | 작성·검토를 맡는 쪽의 이름. 검토를 시작할 때 이름을 따로 주지 않으면 `reviewer` 값이 검토 기록에 남는다 |
| `check_runs` | `user` 면 빌드·테스트·lint 를 사용자가 요청할 때만 실행한다 |

프로젝트에서만 쓰는 금지어·표기 목록은 `.claude/ko-review/terms.json` 에 둔다. 형식은 [shared/terms-format.md](shared/terms-format.md) 에 있다.

## 설명 변경 목록

작성 쪽이 `record` 로 남긴 목록을 검토 쪽이 `review` 로 처리한다. 두 AI 는 같은 프로젝트 파일을 공유하고, 검토 요청은 사용자가 전달한다. 자동 호출이나 메시지 전송은 없다.

1. 작성 쪽: 수정 전 `start`, 수정 뒤 `capture` → `register`(바꾼 설명) / `no-impact`(영향 없는 변경)
2. 검토 쪽: `pending` → 항목마다 `begin` → 교정 → `finish`
3. 목록이 열려 있는 동안 설명이나 근거가 바뀌면 그 항목은 자동으로 다시 대기가 된다
4. 작성 쪽: 작업을 커밋한 뒤 사라진 설명은 `retire`, 목록은 `close` 로 닫는다. 닫힌 목록은 다시 대기가 생기지 않고, 이후 같은 설명을 바꾸는 작업은 자기 목록에 새로 등록한다

목록 형식, 명령, 위치 지정 방법은 [shared/queue-format.md](shared/queue-format.md) 에 있다.

## 구성

```
plugins/ko-review/
├─ .claude-plugin/plugin.json   Claude Code 매니페스트
├─ .codex-plugin/plugin.json    Codex 매니페스트 (같은 skills/ 를 쓴다)
├─ skills/
│  ├─ polish/    교정 기준 (reference/editor-comments.md, reference/unreal.md)
│  ├─ record/    작성 쪽 기록
│  └─ review/    검토 쪽 교정
├─ scripts/
│  ├─ review_queue.py   설명 변경 목록 기록 도구
│  └─ doc_check.py      링크·앵커·금지어·표기 갈림 검사 (읽기 전용)
└─ shared/       프로필 양식, 목록 형식, 낱말 목록 형식
```

## 필요한 것

- Claude Code 또는 Codex
- Python 3.8 이상 (표준 라이브러리만 쓴다)
- git (설명 변경 목록이 커밋과 diff 를 읽는다)

## 알려진 한계

- **문장 품질은 스크립트로 판정하지 않는다.** `doc_check.py` 는 판단이 필요 없는 후보만 찾는다. 통과해도 좋은 문장이라는 뜻은 아니다.
- **목록의 미등록 알림은 파일 단위다.** 같은 파일 안에서 등록하지 않은 변경 구간은 작성 쪽이 직접 확인해야 한다.
- **엔진별 기준은 언리얼만 있다.** 다른 엔진은 `editor-comments.md` 의 일반 기준만 쓴다.
- **Codex 는 버전이 같으면 새 사본을 받지 않는다.** 스킬이나 스크립트를 고치면 `.codex-plugin/plugin.json` 의 `version` 을 올려야 Codex 에 반영된다.
