# 우선순위 등급 체계 (priority_scheme: grade)

이슈의 중요도와 규모를 곱해 등급을 매기고, 선행 관계를 따라 등급을 물려준 뒤 마일스톤별 작업 순서를 정한다. 계산은 `<플러그인 폴더>/scripts/issue_priority.py` 가 한다. 프로젝트 지침이 다른 규칙을 정했으면 지침이 우선한다.

## 라벨

| 종류 | 라벨 | 점수 |
|---|---|---|
| 중요도 a | `priority: must` / `priority: should` / `priority: could` | 3 / 2 / 1 |
| 규모 b | `size: S` / `size: M` / `size: L` / `size: XL` | 3 / 2 / 1 / 등급 없음 |
| 등급 기록 | `grade: A1` … `grade: C2` | 자체 등급 |

- **a** 는 이슈가 속한 마일스톤의 목표를 기준으로 매긴다. 백로그는 프로필 `backlog_goal` 을 기준으로 한다. 필수 3 은 없으면 완료 기준을 채울 수 없는 작업과 진행을 막는 버그, 중요 2 는 결과의 질이나 재작업 비용을 크게 바꾸는 작업, 선택 1 은 편의·정리 작업이다.
- **b** 는 사용자가 직접 손대는 시간(빌드·확인, 에디터 작업, 결정)이다. S 는 1시간 이하, M 은 3시간 이하, L 은 8시간 이하다. 8시간을 넘는 XL 은 등급 없이 하위 이슈로 나누고, 상위 이슈는 묶음으로만 쓴다. 불확실하면 한 단계 크게 잡는다.
- **자체 등급** 은 a×b 다. 9 A1, 6 A2, 4 B1, 3 B2, 2 C1, 1 C2. 같은 등급이면 a 가 높은 쪽이 먼저다.
- **유효 등급** 은 이 이슈가 Blocked by 로 막고 있는 열린 이슈 중 가장 높은 등급이다. 자체 등급보다 낮아지지 않는다. 선행 관계가 바뀔 때마다 달라지므로 라벨로 남기지 않는다.
- C 등급은 마일스톤에 두지 않고 쪼개거나 백로그로 보낸다.
- 마일스톤 설명에 `용량: N시간`(또는 `capacity: Nh`) 줄을 두면 계획량을 견준다. 규모 합은 칸의 가운데 값(S 1, M 2, L 5.5시간)으로 더한다. 필수 이슈의 합이 용량의 60% 를 넘으면 이슈를 빼기보다 마일스톤 목표를 줄인다.

## 실행

```
python "<플러그인 폴더>/scripts/issue_priority.py"
python "<플러그인 폴더>/scripts/issue_priority.py" --milestone M1
python "<플러그인 폴더>/scripts/issue_priority.py" --apply
```

로그인된 `gh` CLI 와 Python 3.8 이상이 필요하다. 저장소는 `--repo`, 프로필 `tracker_repo`, 현재 폴더의 gh 저장소 순으로 정한다. `--apply` 는 grade 라벨을 바꾸는 게시 작업이므로 사용자 확인 뒤에만 쓴다. Windows 콘솔에서 글자가 깨지면 `PYTHONIOENCODING=utf-8` 을 붙여 실행한다.

## 출력 읽는 법

| 출력 | 의미 |
|---|---|
| `due` | 마일스톤 마감일. 마일스톤은 마감일 순, 마일스톤 없는 이슈는 `Backlog` |
| `capacity`, `planned`, `must` | 용량 줄의 값, 규모 합, 필수 이슈 규모 합 |
| `ord` | 지금 작업할 수 있는 이슈의 순서. 선행 작업이 열려 있으면 `-` 와 `[blocked by #N]` |
| `own`, `eff` | 자체 등급과 유효 등급. XL 은 `XL`, 라벨이 없으면 `-` |
| `bundles` | 하위 이슈를 가진 상위 이슈. 채점하지 않는다 |

정렬은 작업 가능 여부, 유효 등급, 자체 중요도, 이슈 번호 순이다.

| 경고 | 할 일 |
|---|---|
| `missing priority or size label` | 라벨을 붙인다 |
| `multiple priority or size labels` | 하나만 남긴다 |
| `size XL in milestone` | 하위 이슈로 나눈다 |
| `grade C… in milestone` | 쪼개서 B 이상으로 만들거나 백로그로 보낸다 |
| `blocker #N is in later …` | 선행 작업을 같은 마일스톤이나 앞 마일스톤으로 옮긴다 |
| `dependency cycle detected` | 관계 하나를 끊는다 |
| `grade label mismatch` | `--apply` 로 맞춘다 |
| `must share over 60%` (머리줄) | 마일스톤 목표를 줄인다 |

## 제한

- 이슈 하나에서 라벨과 선행 이슈는 각각 50개까지만 읽는다. 하위 이슈는 개수만 읽어 상위 이슈인지 가린다.
- `--milestone` 은 출력 범위만 줄인다. 경고는 전체 열린 이슈를 기준으로 낸다.
- 이슈가 없는 마일스톤은 보이지 않는다.
