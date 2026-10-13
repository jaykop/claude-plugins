# 설명 변경 목록 형식

<!-- ko-review: ignore -->

작업마다 바꾼 설명과 로직 변경에 영향을 받는 기존 설명을 목록 하나에 남긴다. 작성하는 쪽(`record` 스킬)이 기록하고 검토하는 쪽(`review` 스킬)이 대기 항목을 읽어 교정한다. 전체 프로젝트를 매번 읽는 대신 해당 문단·주석과 직접 관련된 구현만 대조한다.

목록 파일: `<queue_dir>/<task>.descriptions.json`. `queue_dir` 는 프로필 값이고, 없으면 `.claude/ko-review/queue` 다. 기록 도구는 `<플러그인 폴더>/scripts/review_queue.py` 다. Python 3.8 이상과 git 이 필요하고, 프로젝트 루트에서 실행한다.

작업 ID 는 영어 소문자·숫자·하이픈이다. 이슈가 있으면 `<번호>-<slug>`, 없으면 `<slug>` 로 정한다.

## 명령

| 명령 | 쓰는 쪽 | 하는 일 |
|---|---|---|
| `start <task> --paths <파일들> [--issue <번호>]` | 작성 | 수정 전 파일 상태를 기록하고 목록을 만든다. 이미 있으면 거절한다 |
| `scope <task> --paths <파일들>` | 작성 | 작업 중 새로 손댈 파일을 수정 전에 더한다 |
| `capture <task>` | 작성 | 시작 상태와 다른 파일, git diff 구간, 현재 HEAD 를 기록한다 |
| `register <task> --items <JSON 파일>` | 작성 | 설명 항목을 등록한다. 같은 id 를 다시 등록하면 대기로 돌린다 |
| `no-impact <task> --path <파일> --note "이유"` | 작성 | 설명에 영향이 없는 변경을 기록한다. 파일 내용이 바뀌면 기록이 무효가 된다 |
| `pending <task>` | 둘 다 | 현재 내용과 맞춰 본 뒤 대기 항목, 미등록 변경 파일을 출력한다 |
| `begin <task> --id <항목> --reviewer <이름>` | 검토 | 현재 스냅샷과 token 을 기록한다 |
| `snapshot <task> --id <항목>` | 검토 | 현재 설명·근거의 해시를 출력한다. 완료 기록은 하지 않는다 |
| `finish <task> --id <항목> --token <token> --note "결과" [--status needs-decision] [--description-hash <해시>]` | 검토 | 검토 결과를 기록한다 |

공통 인자: `--root <프로젝트 루트>`, `--queue-dir <목록 폴더>`. 보통은 생략한다.

## 항목 JSON

`register` 에 넘기는 파일은 항목 배열이다. 같은 `queue_dir` 아래에 두면 정리하기 쉽다.

```json
[
  {
    "id": "retry-limit-comment",
    "kind": "comment",
    "reason": "재시도 횟수 설정이 0일 때의 동작을 설명한다",
    "selector": {
      "path": "Source/Net/RetryPolicy.h",
      "anchor": "int32 MaxRetryCount",
      "before": 3
    },
    "evidence": [
      {
        "path": "Source/Net/RetryPolicy.cpp",
        "anchor": "bool FRetryPolicy::ShouldRetry",
        "mode": "span",
        "endAnchor": "return false;",
        "includeEnd": true
      }
    ]
  }
]
```

| 칸 | 뜻 |
|---|---|
| `id` | 작업 안에서 유지하는 이름 |
| `kind` | `comment`(코드 주석), `doc`(문서), `data-comment`(설정·데이터 파일의 설명 칸). 이전 이름 `manual`, `tag-devcomment` 도 받아서 각각 `doc`, `data-comment` 로 바꾼다 |
| `reason` | 무엇을 설명하는지, 왜 바꿨는지 |
| `selector` | 설명의 위치. 파일은 `start`·`scope` 로 등록한 작업 파일이어야 한다 |
| `evidence` | 설명을 뒷받침하는 구현·계약의 위치. 하나 이상 필요하다. 작업 파일이 아니어도 된다 |

## 위치 지정

`anchor` 는 **파일 안의 한 줄에만 맞는 문자열**이다. 타입·함수 이름만 쓰면 여러 호출과 맞을 수 있으므로 선언이나 제목처럼 구별되는 내용을 쓴다.

| mode | 선택 범위 |
|---|---|
| `lines`(기본) | anchor 한 줄. `before`·`after` 로 앞뒤 줄 수를 더한다. 한 줄 설명이나 짧은 주석 |
| `heading` | Markdown 제목부터 다음 같은 수준·상위 제목 직전까지. 문서의 한 단락 |
| `span` | anchor 부터 뒤쪽에서 한 번만 나오는 `endAnchor` 직전까지. `includeEnd: true` 면 끝 줄도 포함. 주석·구현 블록 |

무관한 줄 이동만 있으면 검토 결과를 유지한다. 설명이나 근거 내용이 바뀌면 다음 `pending`·`capture`·`begin` 에서 대기로 돌아간다.

## 목록 파일의 주요 칸

| 칸 | 뜻 |
|---|---|
| `schemaVersion`, `taskId`, `issue` | 현재 형식은 1. 이슈가 없으면 null |
| `baseCommit`, `headCommit` | 시작·캡처 시점의 커밋 |
| `taskPaths`, `initialChanges`, `initialFiles` | 명시적 파일 범위, 시작 시 git 상태와 파일 해시 |
| `changes`, `noImpact` | 시작 상태와 다른 파일·diff 구간, 영향 없음 기록 |
| `entries[].snapshot`, `review`, `ticket` | 내용 SHA-256 과 줄 위치 힌트, 검토 결과, 검토 시작 token |
| `entries[].status` | `pending`·`reviewed`·`needs-decision` |

## 제한

- 자동 캡처는 작업 파일의 변경과 diff 구간까지만 찾는다. 주석 문법이나 의미상의 영향은 판정하지 않는다. `unassignedChanges` 는 항목·근거·영향 없음 기록이 없는 **파일 단위** 알림이다. 같은 파일 안의 미등록 구간은 작성하는 쪽이 직접 대응시킨다.
- 시작 전에 이미 수정돼 있던 파일은 해시와 상태만 남는다(`initiallyDirty`). diff 에 이전 변경이 섞일 수 있으므로 사람이 구분한다.
- anchor 가 사라지거나 여러 줄과 맞으면 `locationError` 를 남기고 대기로 둔다.
- 목록을 쓰는 동안 `.lock` 파일로 잠근다. 다른 쓰기나 내용 변경이 있으면 덮어쓰지 않고 멈춘다. Windows 의 일시적인 파일 교체 거절은 최대 4번 다시 시도한다. 비정상 종료로 `.lock` 이 남았으면 다른 처리가 돌고 있지 않은지 확인한 뒤 그 잠금 파일만 지운다.
- 해시가 같다는 것은 문장이 바뀌지 않았다는 뜻일 뿐, 문장의 품질을 판정하지 않는다.
- Windows 콘솔에서 `UnicodeEncodeError` 가 나면 `python -X utf8 ...` 으로 실행한다.
