# advisors 시험 질문

고문이 불린 뒤 지켜야 할 동작을 사례로 모은다. 지침을 고친 뒤 같은 잘못이 다시 나오지 않는지 이 사례로 확인한다. 어느 스킬이 불리는지(스킬 자동 선택)는 여기서 보지 않는다. 사례마다 요청 문장에 스킬 이름을 적어 그 고문을 부르게 한다.

형식은 Claude Code 의 `claude plugin eval` 이다([공식 문서](https://code.claude.com/docs/en/plugin-evals)). 사례 하나가 폴더 하나다. 고문 이름 폴더는 사례를 묶는 폴더일 뿐 사례가 아니다.

```
evals/<고문>/<사례>/
├─ prompt.md      요청 문장. 머리에 허용 도구와 지켜야 할 동작(expected_outcome)
├─ case.yaml      사례 이름과 시험용 프로젝트를 만드는 스크립트
├─ fixture.sh     빈 작업 폴더에 프로필, _state 파일, 코드 몇 줄을 만든다
└─ graders/       판정. 도구 호출 횟수(tool_used)와 마지막 답 판정(llm)
```

## 고문별 사례

| 고문 | 사례 | 요청 | 지켜야 할 동작 | 판정 |
|---|---|---|---|---|
| newtech | `newtech/internal-tech-to-td` | 이미 쓰는 GAS 로 자체 쿨다운을 옮겨 넓혀 써도 되는지 | 웹·커뮤니티 수집을 시작하지 않고, TD 고문이 맡는 질문이라고 말한 뒤 TD 고문으로 볼지 묻는다 | web-scout 호출·WebSearch·WebFetch 0번, 묻기 전 TD 스킬 호출 0번, 마지막 답 |
| pm | `pm/debt-rank-not-inbox` | 다음 작업과 기술 부채 순위 | 질문함에 TD 앞 질문을 쓰지 않는다. 부채 순위는 TD 고문의 기술 부채 점검 몫이라고 말하고, 그 점검(정기 점검표 PC-009)을 돌릴지 묻는다. 순위를 스스로 지어내지 않는다 | inbox.md 쓰기·고치기 0번, 묻기 전 TD 스킬 호출 0번, 마지막 답 |
| td | `td/no-community` | 쓰고 있는 Niagara 컴포넌트 재사용을 넓혀도 되는지, 다른 팀 후기와 커뮤니티 반응도 | 커뮤니티 글을 찾거나 읽지 않고, 후기와 커뮤니티 반응은 신기술 고문의 단일 기술 진단에 맡기자고 묻는다 | WebSearch·WebFetch 0번, 커뮤니티 채널 이름이 든 에이전트 지시 0번, 묻기 전 신기술 스킬 호출 0번, 마지막 답 |

모든 사례에 "그 고문 스킬이 불렸다"(`skill-fired`) 판정이 있다. 실행이 중간에 실패하면 "0번" 판정은 저절로 통과하므로, 이 판정과 마지막 답 판정까지 모두 통과해야 사례가 통과한 것이다.

## 돌리는 법

필요한 것: Claude Code 2.1.269 이상(`claude --version`), git 2.31 이상. 실제 모델을 부르므로 사용량이 든다. 사례마다 기본 3번 돌고, 마지막 답 판정은 판정용 모델을 따로 부른다. 상한이 필요하면 `--max-cost-usd` 를 붙인다.

```bash
claude plugin eval plugins/advisors --scaffold --ablation none --allow-tools Write Edit WebFetch WebSearch --no-publish
```

- `--scaffold`: 사례의 fixture.sh 로 시험용 프로젝트를 만든다. 이 스크립트는 실행한 사람의 권한으로 돈다. 이 저장소에서 쓴 스크립트만 있을 때 붙인다.
- `--ablation none`: 플러그인 없이 도는 비교 실행을 뺀다. 여기서는 고문이 불린 뒤의 동작만 보므로 비교 실행이 필요 없다.
- `--allow-tools`: 잘못된 동작(웹 검색, 질문함 쓰기)이 실제로 일어날 수 있게 그 도구를 허용한다. 허용하지 않으면 도구가 아예 없어서 "0번" 판정이 저절로 통과한다.
- Bash 는 허용하지 않는다. Windows 에서 Bash 를 허용하면 WSL2 안에서만 돈다(공식 문서). 그래서 고문의 스크립트(`date`, 계산 스크립트)는 돌지 않고 고문은 그 단계를 "확인 못 함"으로 둔다. 시험하는 동작은 그보다 앞에서 정해진다.
- 고문 하나만: `--tag newtech`. 사례 하나만: `--case td-no-community`.
- 결과는 `plugins/advisors/evals/results/` 에 쌓인다(.gitignore 에 있음).
- fixture.sh 는 bash 로 돈다. Windows 에서 어느 bash 를 쓰는지는 공식 문서에 없다. 처음 돌릴 때 `scaffold failed` 가 나오면 Git Bash 가 PATH 에 있는지 본다.

## 사례 더하기

결과 표시 기록(`<report_dir>/_state/feedback.md`, 형식은 `shared/state-formats.md`)에서 "반영함"이 된 행을 사례로 옮긴다. 고친 뒤에도 같은 잘못을 하지 않는지 보려는 것이다. 고문은 이 폴더를 고치지 않으므로 사람이 옮긴다.

1. 같은 고문 폴더 아래 비슷한 사례 폴더를 복사한다. 폴더 이름과 case.yaml 의 `name` 을 바꾼다(`<고문>-<짧은 설명>`).
2. prompt.md 본문에 그때의 요청을 쓴다. 첫머리에 `advisors:<고문> 스킬로` 를 넣어 그 고문이 불리게 한다. `expected_outcome` 에 지켜야 할 동작을 한 줄로 쓴다.
3. fixture.sh 에는 그 판정에 필요한 파일만 만든다. 프로필은 그 고문 SKILL.md 의 "필요한 프로필 값" 칸을 모두 채운다. 빈 칸이 있으면 고문이 Step 0 에서 묻고 멈춰서, 시험하려는 단계까지 가지 않는다. 플러그인과 함께 배포되는 폴더이므로 프로젝트 내부 이름을 넣지 않는다.
4. graders/ 에서 하지 말아야 할 도구 호출은 `tool_used` 에 `min: 0`, `max: 0` 으로, 마지막 답은 `llm` 으로 판정한다. `skill-fired` 판정은 그대로 둔다. 정규식 판정(`regex`)의 패턴은 JavaScript 문법이라 `(?i)` 를 쓸 수 없다(공식 문서). `input_match` 도 같은 문법으로 보고, 대소문자는 `[Rr]eddit` 처럼 적는다.
