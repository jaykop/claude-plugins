# 설명 변경 목록 형식

<!-- ko-review: ignore -->

작업마다 바꾼 설명과 로직 변경에 영향을 받는 기존 설명을 목록 하나에 남긴다. 작성하는 쪽(`record` 스킬)이 기록하고 요청서를 만들면, 검토하는 쪽(`review` 스킬)은 요청서만 읽고 교정문을 결과 파일에 쓴다. 작성하는 쪽이 도구로 교정문을 반영한다. 검토하는 쪽은 코드 기능을 검수하지 않는다. 요청서의 근거 구현은 교정이 원래 뜻을 바꾸지 않았는지 확인하는 데만 읽는다.

목록 파일: `<queue_dir>/<task>.descriptions.json`. `queue_dir` 는 프로필 값이고, 없으면 `.claude/ko-review/queue` 다. 기록 도구는 `<플러그인 폴더>/scripts/review_queue.py` 다. Python 3.8 이상이 필요하다. 프로젝트 루트에서 실행하며, 버전 관리는 프로필의 `vcs` 값을 따른다.

작업 ID 는 영어 소문자·숫자·하이픈이다. 이슈가 있으면 `<번호>-<slug>`, 없으면 `<slug>` 로 정한다.

## 명령

| 명령 | 쓰는 쪽 | 하는 일 |
|---|---|---|
| `start <task> --paths <파일들> [--issue <번호>]` | 작성 | 수정 전 파일 상태를 기록하고 목록을 만든다. 이미 있으면 거절한다 |
| `scope <task> --paths <파일들>` | 작성 | 작업 중 새로 손댈 파일을 수정 전에 더한다 |
| `capture <task>` | 작성 | 시작 상태와 다른 파일, diff 구간을 기록한다. git 을 쓰면 현재 HEAD 도 기록한다 |
| `register <task> --items <JSON 파일>` | 작성 | 설명 항목을 등록한다. 같은 id 를 다시 등록하면 대기로 돌린다. 설명 파일이 프로필 `queue_scope` 밖이면 거절한다 |
| `no-impact <task> --path <파일> --note "이유"` | 작성 | 설명에 영향이 없는 변경을 기록한다. 파일 내용이 바뀌면 기록이 무효가 된다 |
| `pending <task>` | 작성 | 현재 내용과 맞춰 본 뒤 대기 항목, 미등록 변경 파일을 출력한다. `queue_scope` 밖의 대기 항목은 `outOfScopeEntries` 로 따로 출력한다. 항목은 해시 스냅샷을 빼고 설명의 현재 줄 범위(`lines`)를 붙여 출력한다. 닫힌 목록이면 맞춰 보지 않고 닫힘 정보만 출력한다 |
| `prepare <task> [--limit <수>] [--reviewer <이름>]` | 작성 | 대기 항목으로 요청서를 만들고 항목마다 검토 시작 token 을 기록한다 |
| `apply <task> [--results <파일>]` | 작성 | 결과 파일의 교정문을 반영하고 검토 결과를 목록에 기록한다 |
| `begin <task> --id <항목> [--reviewer <이름>]` | 수동 | 사람이 검토 결과를 직접 기록할 때만 쓴다. 현재 스냅샷과 token 을 기록한다. 이름을 생략하면 프로필 `reviewer` 값, 그것도 없으면 `reviewer` 로 기록한다 |
| `snapshot <task> --id <항목>` | 수동 | 사람이 검토 결과를 직접 기록할 때만 쓴다. 현재 설명·근거의 해시와 설명 본문(`descriptionText`)을 출력한다. 본문은 목록에 저장하지 않는다. 완료 기록은 하지 않는다 |
| `finish <task> --id <항목> --token <token> --note "결과" [--status needs-decision] [--description-hash <해시>]` | 수동 | 사람이 검토 결과를 직접 기록할 때만 쓴다. 검토 결과를 기록한다 |
| `retire <task> --id <항목> --note "이유"` | 작성 | 설명이 지워졌거나 다른 작업으로 넘어간 항목을 `retired` 로 둔다. 이후 다시 대기가 되지 않는다. 검토 중인 항목은 거절한다 |
| `close <task> --note "이유" [--allow-unresolved] [--archive-dir <폴더>]` | 작성 | 작업을 커밋·제출한 뒤 목록을 닫는다. 아래 "목록 수명"을 따른다 |

공통 인자: `--root <프로젝트 루트>`, `--queue-dir <목록 폴더>`. 보통은 생략한다.

## 목록 수명

목록은 한 작업의 커밋·제출 전 검토를 위한 기록이다. 그 작업을 커밋·제출하고 검토 넘기기를 마치면 작성 쪽이 `close` 로 닫는다. 닫지 않고 두면 이후 다른 작업이 같은 설명이나 근거를 바꿀 때마다 항목이 다시 대기가 되고, 설명이 지워지면 위치 오류로 남는다.

- `close` 는 검토 중(`begin` 뒤 `finish` 전)인 항목이나 요청서를 만든 뒤 반영하지 않은 항목이 있으면 거절한다. 요청서를 만든 뒤에는 `apply` 하거나 다시 `prepare` 한다. 먼저 `capture` 로 현재 상태를 맞춘다.
- `reviewed`·`retired` 가 아닌 항목이 남아 있으면 그 항목을 출력하고 거절한다. 남긴 채 닫으려면 `--allow-unresolved` 를 붙인다. 남은 항목은 `closed.unresolved` 에 그대로 기록된다.
- 닫힌 목록은 `scope`·`capture`·`register`·`no-impact`·`prepare`·`apply`·`begin`·`finish`·`retire`·`close` 를 거절한다. `pending`·`snapshot` 만 받는다. 같은 작업 ID 로 `start` 하려면 닫힌 목록이 보관 폴더로 옮겨져 있어야 한다.
- 다시 열지 않는다. 이후 같은 설명을 바꾸는 작업은 자기 목록에 새로 등록한다. 오래 가는 작업은 커밋·제출마다 닫고, 다음 단계에서 같은 ID 로 새로 `start` 한다.
- 보관 폴더는 `--archive-dir`, 프로필 `queue_archive_dir` 순으로 정한다. 둘 다 없으면 닫힌 목록을 제자리에 둔다. 폴더 이름에는 닫는 날을 기준으로 `{year}`(예: `2026`), `{quarter}`(예: `2026-Q4`)를 쓸 수 있다. 보관 폴더에 같은 이름이 있으면 `<task>.2.descriptions.json` 처럼 번호를 붙인다.
- 같은 작업의 등록 입력 파일(`<task>.items*.json`)과 수정 전 파일을 복사해 둔 폴더(`<queue_dir>/<task>.base/`), 남은 요청서·결과 파일은 닫을 때 지운다. `register` 가 항목 내용을 목록에 모두 옮겼고, 닫은 작업은 다시 등록하지 않기 때문이다. 보관 폴더를 쓰지 않아도 지운다.
- 닫기 전에 위치 오류 항목은 anchor 를 바로잡아 검토를 받거나, 설명이 사라졌으면 `retire` 한다. 판단을 기다리는 항목(`needs-decision`)은 프로젝트의 이슈나 작업 메모로 옮긴다.

## 등록 범위

프로필의 `queue_scope` 는 목록에 등록할 수 있는 설명 파일의 경로 패턴이다. 프로젝트 루트 기준 `/` 경로에 fnmatch 로 맞춘다. `*` 는 `/` 도 넘으므로 `Source/*` 는 `Source` 아래 모든 파일과 맞는다. 패턴이 폴더 이름이면 그 아래 파일도 맞는다.

- `queue_scope` 가 비었거나 없으면 제한하지 않는다. 이때는 `exclude` 도 적용하지 않는다.
- `queue_scope` 가 있으면 `register` 는 `selector.path` 가 패턴에 하나도 맞지 않거나 `exclude` 에 걸리는 항목을 `Description file is outside profile queue_scope; record it with no-impact` 로 거절한다. 항목 하나라도 거절되면 같은 `--items` 파일의 항목은 하나도 등록하지 않는다. 범위 밖 파일은 `no-impact` 로 남긴다.
- `evidence` 경로는 제한하지 않는다.
- `pending` 은 범위 밖 대기 항목(범위를 정하기 전에 등록된 항목 등)을 `entries` 에서 빼고 `outOfScopeEntries` 로 따로 출력한다. 자동으로 지우지 않는다. 정리는 사용자가 정한다.

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

무관한 줄 이동만 있으면 검토 결과를 유지한다. 설명이나 근거 내용이 바뀌면 다음 `pending`·`capture`·`begin` 에서 대기로 돌아간다. `retired` 항목과 닫힌 목록은 돌아가지 않는다.

설명은 한 설정의 완결된 주석 블록·문단·표의 행을 선택한다. 바뀐 줄만 골라 빈 값이나 예외 설명이 빠지지 않게 한다. 선택 범위는 작성 쪽이 정하고 고친다. 검토 쪽은 목록 파일과 소스 파일을 읽거나 고치지 않는다. 교정으로 anchor 줄이 바뀌면 `apply` 가 바뀐 구간에서 파일 안에 한 번만 나오는 줄로 selector 를 다시 잡는다. 원래 anchor 가 남아 있으면 그대로 쓴다. 다시 잡지 못하면 파일을 되돌리고 거절한다. 근거를 읽는 범위와 기술 판단 제한은 `review` 스킬을 따른다.

## 요청서와 결과 파일

작성 쪽은 `register` 와 `pending` 대조를 마친 뒤 `prepare <task>` 로 요청서를 만든다. 요청서는 `<queue_dir>/<task>.request.md`, 결과 파일의 기본 위치는 `<queue_dir>/<task>.result.json` 이다. `prepare` 는 결과 파일을 `items` 가 빈 형식으로 미리 만들고, 검토 쪽은 그 파일의 내용만 바꾼다. Windows 의 Codex 샌드박스가 새로 만든 파일은 작성 쪽 계정이 읽지 못할 수 있기 때문이다.

### 요청서에 넣는 내용

- 요청 ID, 결과 파일 경로, 결과 파일 형식을 넣는다.
- 항목마다 종류·위치·등록 이유·고칠 글·앞뒤 6줄·근거 구간을 넣는다. 근거가 한 줄만 고른 구간이면 그 아래 줄을 더해 40줄까지 보여 준다. 앞 항목과 같은 근거 구간은 다시 싣지 않고 그 항목 번호만 적는다.
- 프로젝트 낱말 목록의 확정 금지 표현(`banned`, `banned_patterns`)을 넣는다.
- `polish` 의 "문장 기준", "사실과 수정 권한", "교정 완료 판단" 세 절을 넣는다. `comment`·`data-comment` 는 `editor-comments.md`, 프로필 `engine` 이 `unreal` 이면 `unreal.md`, `doc` 은 `manual.md` 를 함께 넣고, `word-choice.md` 는 언제나 넣는다.

상태가 `pending` 인 항목만 넣는다. `needs-decision` 항목은 사용자가 정할 때까지 넣지 않는다. 위치 오류 항목과 `queue_scope` 밖 항목은 넣지 않고 출력의 `skipped` 에 적는다. 한 번에 40개까지 넣으며, `--limit` 로 수를 바꿀 수 있다. 넣지 못한 대기 항목 수는 출력의 `notIncluded` 다.

넣은 항목마다 검토 시작 token 을 기록한다. 검토자 이름은 `--reviewer`, 없으면 프로필 `reviewer`, 그것도 없으면 `reviewer` 다. 다시 `prepare` 하면 이전 요청은 무효가 되고, 이전 요청의 결과 파일은 `apply` 가 거절한다.

### 결과 파일 형식

검토 쪽은 요청서의 결과 파일 경로에 다음 형식으로 쓴다. 요청서의 모든 항목을 넣고, `status` 는 `reviewed` 또는 `needs-decision` 으로 쓴다.

`{"requestId": "<요청 ID>", "items": [{"id": "...", "status": "reviewed", "text": "...", "note": "..."}]}`

- `text` 는 "고칠 글" 전체를 대신할 글이다. 설명 밖의 줄과 글자(코드, 설정 키, 들여쓰기, 주석 기호)는 그대로 둔다. 줄 수는 바뀌어도 된다. 고칠 것이 없으면 원문 그대로 둔다.
- 설명과 근거가 어긋나 보이거나 원래 뜻을 알 수 없을 때, 사용 제약인지 불명확한 내용을 지워야 할 때는 `needs-decision` 으로 남긴다. 이때 `text` 는 원문 그대로 두고 `note` 에 어긋난 설명 위치와 근거 위치만 적는다.
- `note` 는 한 줄이다. 어떤 모호함을 없앴는지 쓰고, 그대로 뒀으면 판단 근거를 쓴다. "뜻이 분명하므로 유지했다"만으로 끝내지 않는다.

### 반영과 거절

작성 쪽은 검토 쪽이 결과 파일에 항목을 채우면 `apply <task>` 를 실행한다. `items` 가 비어 있으면 거절하고 요청을 그대로 둔다. 다른 위치의 결과 파일은 `--results <파일>` 로 지정한다.

도구가 교정문을 선택 구간에 쓴다. 파일의 BOM 과 줄바꿈 문자는 원래대로 두고, 같은 파일의 여러 항목은 아래쪽부터 바꾼다. anchor 줄이 바뀌면 위 "위치 지정"의 규칙으로 selector 를 다시 잡는다. 검토자, 시각, 메모, 상태를 목록에 기록하고, 반영한 뒤 요청서와 기본 위치의 결과 파일을 지운다. 기록하는 해시는 모든 항목을 쓴 뒤의 내용이다. 반영 전에 기록과 같던 다른 항목도, 이번 반영으로 근거만 바뀌었으면 해시를 새로 잡아 다시 대기가 되지 않게 한다. 설명이 바뀐 항목은 그대로 두어 대기로 돌린다.

다음 경우에는 거절한다. 거절한 항목은 파일을 바꾸지 않고 대기로 남긴다.

- `comment` 에서 주석 밖의 코드가 달라졌다.
- `data-comment` 에서 설명 값 밖이 달라졌다. 키 이름에 `comment`·`description`·`desc`·`tooltip` 이 들어간 값만 설명으로 본다.
- `doc` 에서 코드 블록이 달라졌다.
- C 계열 파일에서 원문에 없던 블록 주석 안의 `/*` 나 `\` 로 끝나는 `//` 주석이 생겼다. `\` 로 끝나는 `//` 주석은 다음 줄까지 주석으로 만든다.
- 요청 뒤에 설명이나 근거가 바뀌었다. `apply` 는 파일을 쓰기 전에 모든 항목을 확인하므로, 같은 요청의 다른 항목을 반영해 근거가 바뀐 것은 여기에 해당하지 않는다.
- 설명 구간이 겹치는 다른 항목을 이번 `apply` 에서 먼저 반영했다.
- 교정문을 쓰고 나니 근거의 anchor 를 찾을 수 없다. 파일은 되돌린다.
- 결과가 없다.
- 요청에 없는 항목이다.
- 파일이 읽기 전용이라 쓸 수 없다. 체크아웃하지 않은 Perforce 파일이 여기에 해당한다.

### 출력 칸

| 칸 | 뜻 |
|---|---|
| `applied` | 반영한 항목 |
| `unchanged` | 그대로 둔 항목 |
| `unchecked` | 주석 문법을 모르는 파일이라 코드 보호를 확인하지 못하고 반영한 항목 |
| `needsDecision` | 판단이 필요한 항목 |
| `failed` | 거절한 항목과 이유 |
| `remaining` | 남은 대기·판단 필요 항목 수 |

### 주석 문법과 반영 뒤 확인

주석 문법을 아는 파일은 C 계열(c, cpp, h, cs, java, js, ts, go, rs, swift, kt 등), `#` 주석을 쓰는 파일(py, rb, sh, ps1, yaml, toml 등), `--` 주석을 쓰는 파일(lua, sql), `;`·`#` 줄 주석을 쓰는 ini·cfg 다. 파이썬 docstring 처럼 문자열 안에 있는 설명은 `comment` 로 반영하지 못한다. 코드가 달라진 것으로 거절한다.

작성 쪽은 반영된 교정문을 다시 고치지 않는다. 고쳐야 하면 고친 뒤 같은 id 로 다시 `register` 한다. `unchecked` 항목은 작성 쪽이 바뀐 구간을 직접 확인하고, `needsDecision` 항목은 사용자에게 보인다. `remaining` 이 0 이 아니면 다시 `prepare` 한다.

## 목록 파일의 주요 칸

| 칸 | 뜻 |
|---|---|
| `schemaVersion`, `taskId`, `issue` | 현재 형식은 1. 이슈가 없으면 null |
| `baseCommit`, `headCommit` | 시작·캡처 시점의 커밋. git 을 쓰지 않으면 null |
| `taskPaths`, `initialChanges`, `initialFiles` | 명시적 파일 범위, 시작 시 버전 관리 상태(`git status` 또는 `p4 opened`), 시작 시 파일 해시 |
| `changes`, `noImpact` | 시작 상태와 다른 파일·diff 구간, 영향 없음 기록 |
| `request` | 지금 요청의 ID, 항목, 요청서·결과 파일 경로 |
| `entries[].snapshot`, `review`, `ticket` | 내용 SHA-256 과 줄 위치 힌트, 검토 결과, 검토 시작 token(prepare 또는 begin) |
| `entries[].status` | `pending`·`reviewed`·`needs-decision`·`retired` |
| `entries[].retired` | 폐기한 시각, 이유, 폐기 전 상태와 위치 오류 |
| `closed` | 닫은 시각, 그때의 `headCommit`, 이유, 남긴 항목(`unresolved`). 열린 목록에는 없다 |

## 제한

- git 을 쓰지 않으면 `start`·`scope` 때 수정 전 파일을 `<queue_dir>/<task>.base/` 에 복사한다. 이 사본과 비교해 diff 구간을 찾고, `close` 때 사본을 지운다. `queue_dir` 은 버전 관리에서 제외되는 폴더여야 한다.
- 자동 캡처는 작업 파일의 변경과 diff 구간까지만 찾는다. 주석 문법이나 의미상의 영향은 판정하지 않는다. `unassignedChanges` 는 항목·근거·영향 없음 기록이 없는 **파일 단위** 알림이다. 같은 파일 안의 미등록 구간은 작성하는 쪽이 직접 대응시킨다.
- 시작 전에 이미 수정돼 있던 파일은 해시와 상태만 남는다(`initiallyDirty`). diff 에 이전 변경이 섞일 수 있으므로 사람이 구분한다.
- anchor 가 사라지거나 여러 줄과 맞으면 `locationError` 를 남기고 대기로 둔다. 파일 이름 변경은 따라가지 않는다. 작성 쪽이 경로·anchor 를 고치거나 `retire` 한다.
- 목록을 쓰는 동안 `.lock` 파일로 잠근다. 다른 쓰기나 내용 변경이 있으면 덮어쓰지 않고 멈춘다. Windows 의 일시적인 파일 교체 거절은 최대 4번 다시 시도한다. 비정상 종료로 `.lock` 이 남았으면 다른 처리가 돌고 있지 않은지 확인한 뒤 그 잠금 파일만 지운다.
- 해시가 같다는 것은 문장이 바뀌지 않았다는 뜻일 뿐, 문장의 품질을 판정하지 않는다.
- `reviewed`는 선택한 설명과 근거의 검토 기록이다. 파일 전체를 읽었다는 뜻도, 앞으로 그 문장을 고칠 필요가 없다는 뜻도 아니다. 문장 품질은 `polish`의 완료 판단으로 정하고, 전수 교정의 읽은 범위와 남은 범위는 별도로 기록한다.
- Windows 콘솔에서 `UnicodeEncodeError` 가 나면 `python -X utf8 ...` 으로 실행한다.
