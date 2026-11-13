# story — 게임 대본 기획·작성·검토

비주얼 노벨과 이야기 중심 게임의 한국어 대본을 기획부터 대사까지 쓰고 검토하는 플러그인이다. Claude 가 초안을 쓰고 사람이 텍스트 에디터로 고친다. 최종 판단은 사람이 한다.

```
/plugin install story@jaykop
```

| 스킬 | 명령 | 하는 일 |
|---|---|---|
| write | `/story:write` | 기획 시트 → 장면 목록 → 장면 카드 → 대본 → 자체 리뷰. 리뷰만 하거나 지정한 패스만 다시 돌릴 수도 있다 |

명령 이름을 외우지 않아도 된다. "5분 장면 대본 작성해 줘", "장면 카드 만들어 줘", "대본 리뷰해 줘", "이 장면 대사 다듬어 줘", "이 설화를 VN으로 각색해 줘" 같은 말로도 불린다.

```
/story:write 축약 첫 장면
/story:write 리뷰만 game/content/dialogue/main.dialogue
/story:write 수정 패스 C,D scene_02
```

| 모드 | 진행 | 사람 확인 |
|---|---|---|
| 전체 | 1~5단계 | 기획 시트 후, 장면 카드 후 |
| 축약 | 1~3단계를 한 번에, 그다음 4~5단계 | 장면 카드 후 1회 |
| 리뷰만 | 5단계만. 대본은 고치지 않고 리포트만 | 리포트 |
| 수정 | 사람이 고친 대본에 지정한 패스만 | 리포트 |

## 프로젝트 형식 파일

대본 형식은 프로젝트마다 다르다. 각 프로젝트의 `.claude/story/format.md` 에 적는다.

- 대본 언어, 기획 문서와 대본 파일 위치, 데이터 파일(화자 목록, 변수 기본값)
- 줄 종류(지문, 대사, 선택지, 명령)와 쓰는 법, 속말 표기
- 대사창 폭과 길이 기준
- 검사 도구가 잡지 못하는 줄, 분기 경로 수 제한
- 검사 명령과 실행 가능한 곳, 문장 검사 스크립트 옵션

양식은 [skills/write/reference/format-template.md](skills/write/reference/format-template.md) 에 있다. 형식 파일이 없으면 기획 문서(기획, 플롯, 장면 카드)는 그대로 쓰고, 대본을 쓸 때 형식 파일을 만들지 한 번 묻는다. 답을 받기 전에는 기본 형식(Godot Dialogue Manager 와 같은 한 줄 한 대사창 텍스트)으로 쓴다. 검사 명령은 추측하지 않는다. 형식 파일에 없으면 검사를 실행하지 않았다고 리포트에 적는다.

## 구성

```
skills/write/
  SKILL.md                 절차: 시작 전 확인, 모드, 단계, 참조, 지킬 것, 검사, 보고
  steps/
    1-concept.md           로그라인, 기획 시트, 인물 시트
    2-plot.md              3점 선구상, 골격, 장면 목록, 설정·단서 공개 표(정보 등급), 분기
    3-scene.md             장면 카드, 첫 줄과 끝 줄, 선택지, 정보 전달(두 층, 복귀 줄), 감정 정점
    4-write.md             대사창 길이와 근거 통계, 대사, 감정, 데이터 파일
    5-review.md            패스 A 구조, B 장면, C 대사(읽기 모드 3종, 관점별 읽기), D 문장, E 형식, 리포트 양식
  reference/
    format-template.md     프로젝트 형식 파일 양식과 기본 형식
    genre-mystery.md       공정성, 속임수 7종, 사건 설계, 단서·증언 카드, 해결 장면, 괴이 요소
    genre-romance.md       장애물 4종, 관계 진행 신호, 오해와 재회, 엔딩 직전 대안
    genre-faction.md       역사 변형 7종, 경계 규칙, 사실·허구 목록
    structures.md          시점 교체 재방문, 호출형 액자, 현재 쪽 수수께끼, 이중 스레드, 겹겹 액자
    adaptation.md          각색 시트, 변환 규칙, 실패 패턴, 리뷰 질문
    cliche-check.md        클리셰 25개와 판정 절차
    sources.md             기법별 출처
  examples/lines.md        나쁜 예와 고친 예 11쌍(직접 쓴 예문)
  scripts/story_lint.py    문장 후보 검사: 지문의 감정 이름·필터 동사, 이중 피동, 번역투, 한글 시각, 긴 대사창, 지문 속 ": ", 선택지 목록, 지문 문말 분포
```

## 출처

작법서, 한국 드라마·영화 대본(대사 길이 통계 포함), 영화 비평서와 이론서, 그리고 VNTool 에서 이 스킬로 쓴 5분 장면의 테스트 플레이 결과다. 책과 작품의 문장은 옮기지 않았고 기법만 요약했다. 책별 출처는 [sources.md](skills/write/reference/sources.md) 에 있다.

## 문장 검사 스크립트

```
python skills/write/scripts/story_lint.py <대본 파일>
python skills/write/scripts/story_lint.py --summary --checks length,colon <대본 파일>
```

표준 라이브러리만 쓴다. 기본 정규식은 Dialogue Manager 형식에 맞춰져 있고, 다른 형식은 `--command`, `--speaker`, `--tag`, `--choice` 로 바꾼다(형식 파일의 "Lint options"). 검출은 후보일 뿐이고 판단은 줄마다 한다.

## 다른 플러그인과의 경계

- 한국어 코드 주석과 기술 문서는 `ko-gamedev`.
- 메뉴, UI 문구, 현지화 문자열은 이 플러그인의 범위가 아니다.
