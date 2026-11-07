<!-- ko-lint: ignore-file -->
# Core words

Words that appear in every area. Most rows map a native Korean verb that AI text prefers to the Sino-Korean or loanword verb that Korean game developers write. Columns and kinds: [README.md](README.md).

Avoid forms are stems where possible: 돌려주 matches 돌려주고, 돌려주며 and 돌려주므로. The lint prints the whole word it matched.

## Verbs

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 사용한다 | 쓴다, 쓰는, 쓰고, 쓰면, 쓰지, 쓰므로, 쓰며, 쓰도록, 쓰려, 써서, 써야, 썼, `re:(?<![가-힣])쓸 ` | replace | 사용 A 64 / K 45; 쓴다 A 0.3 / K 78 | If 쓰다 means write, use 기록한다, 작성한다 or 저장한다. 덮어쓴다 is not matched. |
| 반환한다, 리턴한다 | 돌려주, 돌려준, 돌려줄, 돌려줘 | replace | 반환 A 9.5, 리턴 A 5.4; 돌려준 A 0 / K 19 | 되돌려준다 is not matched; see 복구한다. |
| 호출한다 | 부른다, 부르고, 부르면, 부르지, 부르므로, 부르는, 부를 | replace | 호출 A 14 / K 55; 부른다 A 0 / K 6.3 | 불러온다 (load) is a different verb. |
| 선택한다 | 고른, 고르, 고를, 골라, 골랐 | replace | 선택 A 19; 고른다 A 0 / K 13 | 고르게 (evenly) also matches; skip it. |
| 변경한다 | 바꾼, 바꾸, 바꿀, 바꿨 | replace | 변경 A 35; 바꾼다 A 0 / K 17 | A casual 바꿔 준다 is not matched. |
| 전달한다 | 넘긴, 넘기고, 넘기며, 넘기면, 넘기는, 넘길 | replace | 전달 A 3.3; 넘긴다 A 0 / K 6.6 | 대사 넘기기 (skip a line of dialogue) is a UI action and is not matched. |
| 수집한다 | 모은, 모으, 모아, 모았 | replace | 수집 A 2.3; 모은다 A 0 / K 4.7 | |
| 담당한다, 처리한다 | 맡는, 맡고, 맡긴, 맡기, 맡아 | replace | 처리 A 42; 맡는다 A 0 / K 4.8 | |
| 삭제한다, 제거한다 | 지운, 지우, 지워, 지울 | replace | 삭제 A 15; 지운다 A 0.5 / K 12 | 삭제 for data, files and actors. 제거 for list entries, effects and tags. |
| 유지한다 | 그대로 둔, 그대로 두, 그대로 둬 | replace | 유지 A 14; 둔다 A 1.8 / K 33 | The auxiliary -어 둔다 (저장해 둔다) is fine. |
| 추가한다, 제거한다, 부착한다 | 뗀다, 떼고, 떼어, 뗄, 붙인, 붙이고, 붙이며 | review | 붙인 A 0.2 / K 7.4; 뗀다 A 0 / K 0.9 | Tags: 추가한다, 제거한다. Components: 부착한다 or Attach한다. |
| 초기화한다, 리셋한다, 클리어한다 | 비운다, 비우고, 비운 | review | 비운 A 0.3 / K 12 | A pointer or target: nullptr로 리셋한다. A container: 비운다 is acceptable, or Empty()로 초기화한다. |
| 전송한다 | 보낸, 보내고, 보내며, 보내는 | review | 전송 A 2.3; 보낸다 A 0.2 / K 10 | Packets, RPCs and messages: 전송. 이벤트를 보낸다 is acceptable when the file already says it. |
| 이동한다, 옮겨 준다 | 옮긴, 옮기고, 옮기며, 옮기는 | review | 이동 A 26; 옮긴다 A 0 / K 7.1 | People write 옮겨 준다 for moving entries between lists. |
| 가져온다, 참조한다 | 읽는다, 읽고, 읽으며, 읽어 | review | 가져오 A 6.6; 읽는다 A 0 / K 11 | Reading a file, stream or config stays 읽는다. |
| 결정한다, 지정한다, 설정한다 | 정한다, 정하고, 정하는, 정할 | review | 결정 A 11, 지정 A 11, 정한다 A 6 / K 52 | 정한다 is not wrong. Fix it when it repeats through a file. 정해진 (fixed) is not matched. |
| 출력한다 (로그); 유지한다 (값, 후보) | 남긴다, 남기고, 남기지, 남기며 | review | 출력 A 14; 남긴다 A 0 / K 16 | 경고를 남긴다 → 경고 로그를 출력한다. If it means keep a value or a candidate, use 유지한다. |
| 스킵한다, 무시한다 | 건너뛴, 건너뛰, 건너뛸 | review | 스킵 A 2.7, 무시 A 5.6; 건너뛴 A 0 / K 8.5 | |
| 카운트한다 | 센다, 세고, 세는, `re:(?<![가-힣])세지 않` | review | 카운트 A raw 11; 센다 A 0 / K 4.3 | |
| 복구한다, 리셋한다, 원래대로 돌린다 | 되돌린, 되돌리, 되돌려 | review | 복구 A 5.1, 리셋 A 3.2; 되돌린다 A 0 / K 9.7 | |
| 종료한다 | 끝낸, 끝내 | review | 종료 A 22; 끝나 A 5.6 / K 24 | Intransitive 끝난다 is common in human comments and is not matched. |
| 판단한다, 체크한다 | 판정한, 판정하, 판정할, 판정해 | review | 판단 A 8.1, 체크 A 58; 판정 A 1.4 / K 54 | Combat 히트 판정 and 공격 판정 are correct; see combat.md. |
| 간주한다, 판단한다, 체크한다 | `re:(?<![가-힣])본다(?![가-힣])`, 보지 않 | review | raw A 1 / K 89 | 통과로 본다 → 통과로 간주한다. Looking at a screen stays 본다. |
| ~ 값을 사용한다, ~에 따라 결정된다 | `re:(?<![가-힣])따른다(?![가-힣])` | review | raw A 0 / K 90 | 설정을 따른다 is fine in docs. In a comment, name what decides the value. |
| 업데이트, 갱신 | — | term | 업데이트 A 17 / O 12 / K 0.7; 갱신 A 4.7 / O 16 / K 29 | Both are normal; O writes 점수 갱신, 보너스 갱신. Keep the file's word. |
| 확장한다, 분리한다 | 펼친, 펼치, 펼쳐 | review | 펼친 A 0 / K 2.2 | 부위별로 펼친다 → 부위별로 분리한다. |
| 생성한다 | 만든다, 만들고, 만들지, 만들어 | review | A 10 / O 3 / K 51; 생성 A 21 / O 57 / K 52 | People also write 만든다, mostly for setting a value (0으로 만든다 → 0으로 설정); fix it when it repeats. |
| 변경된다 | 바뀐, 바뀌, 바뀔 | review | A 3.0 / O 4 / K 39; 변경되 A 4.7 / O 2 | |
| 브로드캐스트한다, 이벤트를 호출한다, 로그를 출력한다 | 알린다, 알리고, 알리지, 알리는, 알린 | review | A 1.8 / O 1 / K 21 | Name the mechanism. 알림 (a player notification) is not matched. |
| 일치시킨다, 동기화한다, 맞춰 준다 | 맞춘다, 맞추고, 맞춘, `re:(?<![가-힣])맞지\s*않` | review | 맞추 A 5.4 / O 1 / K 21; 맞지 않 A 0.2 / O 0 / K 6.1 | 맞지 않으면 → 일치하지 않으면. Hitting a target is 히트 (combat.md). |
| 정지한다, 중단한다 | 멈춘, 멈추, 멈춰 | review | A 1.8 / O 0 / K 23; 정지, 중단 A 4.1 | |
| 저장한다, 캐싱한다 | 보관 | review | A 1.1 / O 0 / K 19; 저장, 캐싱 A 23 / O 13 | |
| 유지된다 | 남는다, 남지, `re:(?<![가-힣])남아\s*있` | review | A 1.8 / O 0 / K 18 | |
| 할당한다, 세팅한다 | 채운, 채우, 채워 | review | A 1.4 / O 5 / K 16; 할당 A 6.9 / O 22 / K 1.3 | |
| 참조한다 | 가리킨, 가리키 | review | A 0.2 / O 0 / K 11 | A pointer pointing at memory may keep 가리킨다. |
| 대기한다 | 기다린, 기다리, 기다려 | review | A 0.6 / O 1 / K 13; 대기 A 1.7 / O 2 | |
| 무시한다, 바로 리턴한다 | 아무것도 하지 않, 아무것도 안 | review | A 0 / O 0 / K 13; 무시, 리턴 A 16 / O 28 | does nothing |
| 필터링한다 | 거른, 거르, 걸러 | review | A 0.5 / O 1 / K 9.8; 필터 A 1.7 / O 7 | |
| 제외한다 | 뺀다, 빼고, 빼면, 뺀, 빼지 | review | A 0.5 / O 3 / K 12; 제외 A 6.2 | Arithmetic subtraction (값을 뺀다) stays. |
| 기록한다 | 적는다, 적고, 적은, 적어 | review | A 0.9 / O 0 / K 3.5 | 적은 (few) also matches; skip it. |
| 계산한다, 측정한다 | 잰다, 재고, 재서 | review | A 0 / O 0 / K 3.4; 계산 A 15 / O 21 | |
| 조준한다, 에임 | 겨누, 겨눈, 겨눌 | review | A 0 / O 0 / K 2.3; 조준, 에임 A 2.7 | |
| 접근한다 | 다가가, 다가간, 다가갈 | review | A 0 / O 0 / K 1.5 | |

## Conditions and values

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| true면, false면, 활성화, 비활성화 | 켜면, 끄면, 켜져, 꺼져, 켜지, 꺼지, 켜졌, 꺼졌, 켠다, 끈다, 켜고, 끄고, 켜 두, 꺼 두 | review | 활성화 A 27; 켜면 A 0 / K 9.8 | For bool properties write true면 and false면. Features and Tick: 활성화, 비활성화. A light or a physical switch keeps 켜다. |
| 설정하지 않으면, 지정하지 않으면, None이면 | 비우면, 비워 두면, 비워두면 | replace | 비우면 A 0 / K 11 | 배열이 비어 있으면 (an empty container) is correct and is not matched. |
| 설정하지 않으면, None이면 | `re:비어\s*있으면` | review | A 0.9 / O 0 / K 21 | For an unset tag, query or reference property. A container (배열이 비어 있으면) stays. |
| 시점, 타이밍, 시간 | `re:(?<![가-힣])시각(?![적화])` | replace | 시점 A 12, 타이밍 A 4.8; 시각 A 0 / K 37 | A world time value is 시간(초). 시각적 and 시각화 are not matched. In camera and line-of-sight code 시점 also means viewpoint; use 타이밍 or 월드 시간 there. |
| 현재 | `re:(?<![가-힣])이번(?! ?프레임)` | review | 현재 A 30; 이번 A 0.3 / K 19 | 이번 프레임 is fine and is not matched. |
| 바로, 즉시, ~한 뒤 바로 | 직후 | review | 바로 A 5.6; 직후 A 0 / K 8.2 | |
| 중 | 가운데 | review | 가운데 A 0 / K 6.3 | ~ 가운데 하나 → ~ 중 하나. 화면 가운데 (the center) stays. |
| 임계값 | 문턱 | replace | 임계값 A 0.3; 문턱 A 0 / K 1.5 | |
| ~ 후, ~ 이후, ~한 다음 | `re:(?<=[가-힣]) 뒤(?=에\|[\s,.]\|$)` | review | ~ 뒤 A 2.1 / O 1 / K 62; ~ 후 A 34 / O 18 / K 25 | One of the strongest AI signs. 캐릭터 뒤에 (behind) is a direction and stays. |
| 시점, 타이밍, 때 | 순간 | review | A 0.3 / O 0 / K 15 | |
| ~ 여부 | — | term | 여부 A raw 259 | Name of a bool: 락온 가능 여부. |

## Nouns

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 세팅, 설정 | — | term | 세팅 A 37 / K 0; 설정 A 24 / K 64 | Both are normal. 세팅 for filling in values and preparing state (카메라 세팅, 초기 세팅). 설정 for options and property names. AI text never writes 세팅; it is not slang. |
| 체크 | — | term | 체크 A 58 / K 4.8 | ~인지 체크 and ~ 체크 are the most common verb nouns in human comments. |
| 타겟, or name the thing | `re:(?<![가-힣])대상` | density | 대상 A 12 / K 106 | AI text calls every receiver 대상. A file with many is worth a read; combat.md lists the forms that should be 타겟. |
| 오브젝트 | 객체 | review | 오브젝트 A 8.9 / K 5.0; 객체 A 1.5 / K 26 | UObjects and things in the world: 오브젝트. General C++ object talk may keep 객체. |
| 복사본 | 사본 | replace | 복사 A 3.0; 사본 A 0 / K 20 | |
| 상속, 자식 클래스 | 파생 | review | 상속 A 2.1; 파생 A 0 / K 8.7 | 파생 클래스 is textbook Korean but rare in game code comments. |
| 부모 구현, Super 구현 (override); 기본 구현 (base class) | 기반 구현 | review | A 0 / K 1.5 | In the base class's own header the default behavior is 기본 구현. In an override, the inherited behavior is 부모 구현. |
| 베이스 클래스, 부모 클래스 | 기반 클래스 | review | A 0 / O 0 / K 1.6 | |
| 바인딩 | 구독 | review | 바인딩 A 5.9 / O 0; 구독 A 0.3 / O 4 / K 20 | UE delegates and events are bound (바인딩). Rx observables and MVVM view models are subscribed; O writes 뷰 모델을 구독합니다, so 구독 stays there. |
| 필드, 항목, 슬롯 | `re:(?<![가-힣])칸(?![가-힣]{2})` | replace | 칸 A 0 / K 9.1 | 대상 칸 → Target 필드. |
| 셰이프, Shape | 도형 | replace | Shape A 4.4; 도형 A 0 / K 8.2 | |
| 샘플 | 표본 | replace | 샘플 A 0.2 / K 9.8; 표본 A 0 / K 3.0 | Audio: 512샘플. |
| 에디터용, 편집용 | 저작 | replace | 저작 A 0 / K 7.5 | 저작 그래프 → 에디터 그래프 or 편집용 그래프. |
| 이유, 원인 | 사유 | review | A 0 / O 0 / K 9.1 | |
| 핸들러 | 처리기 | replace | A 0 / O 0 / K 7.4 | |
| 리스트, 배열 | 목록 | review | 목록 A 4.4 / O 1 / K 39; 리스트, 배열 A 15 / O 5 | People write 목록 for a named data list (PathPoint 목록, A 3.9); fix it when it repeats. 목록 in document prose is fine. |
| Warning 로그, 에러 로그 | 경고 | review | A 0.2 / O 0 / K 28 | 경고를 남긴다 → Warning 로그를 출력한다. A warning shown to the player stays. |
| 변경된 값, 델타 | 변경분 | review | A 0 / O 0 / K 5.6 | |
| 리포트 | 보고서 | review | A 0 / O 0 / K 6.7 | HID and crash reports. |
| 로그, 이력 | — | term | 로그 A 3.0 | 실행 기록 is fine. 기록을 남긴다 → 로그를 출력한다. |

## Connectives and marks

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 때문에, ~라서, or split the sentence | `re:(?<=[가-힣])므로` | density | A 18 / K 200 / D 32 | One or two per file is fine. A file where most comments end in ~므로 reads machine-made. |
| 쉼표, 와/과, 및, 슬래시 | `re:(?<=[가-힣A-Za-z0-9)])·(?=[가-힣A-Za-z0-9(])` | density | A 0 / K 103 / D 0 | People list with commas or slashes: 전투/비전투, 서버와 클라. |

## 자리

AI text uses 자리 for seven different things. A writes the specific word for each. Bare 자리 is A 0 / K 5.4 (K docs 3.4).

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 즉시, 바로, 이 시점에 (time); 해당 지점에서, 제자리에서 (place) | 그 자리에서, 이 자리에서 | review | 그 자리에서 A 0 / K 0.8; 바로 A 5.6, 즉시 A 3.9 | 그 자리에서 비운다 → 즉시 비운다. 탄이 그 자리에서 멈춘다 → 탄이 해당 지점에서 멈춘다. 그 자리에서 돈다 → 제자리에서 회전한다. |
| 위치, 지점 (world); 인덱스, 순서 (list); 필드 (type slot); 오프셋 (bytes); 공간, 슬롯, 버퍼 (capacity) | `re:(?<![가-힣])(?<!그 )(?<!이 )자리(?![잡표])(?!에서)(?! ?수)` | review | 자리 A 0 / K 5.4; 위치 A 32, 지점 A 14, 인덱스 A 13, 슬롯 A 6.8, 오프셋 A 2.9, 공간 A 1.8 | 마지막 자리에 남는다 → 마지막 위치에 남는다. 그 자리를 교체한다 → 해당 인덱스의 항목을 교체한다. 자리를 바꾼다 → 순서를 바꾼다. 아이템 ID 자리에 → 아이템 ID 필드에. 헤더와 같은 자리 → 헤더와 같은 오프셋. 자리가 모자라면 → 버퍼 공간이 모자라면. 제자리 and a digit count (열아홉 자리 수) stay. |
| 플레이스홀더, 임시값, 더미 값 | 자리표시 | replace | K only; 더미 A 0.3 | |

## Calques and metaphors

English idioms translated word by word, and metaphors that make the reader guess the technical action. Most rows come from the retired ko-review checker (evidence `KR`); people do not write them (A about 0).

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 에러 없이, 로그 없이, 알림 없이 | 조용히 | review | A 0 / K 1.7 | 조용히 실패한다 → 에러나 로그 없이 실패한다. |
| 나중에 문제가 될 것 같다, 허술하다, 의심된다 | 냄새가 난, 냄새나는 | replace | KR; A 0 | code smell |
| 빠진 경우, 처리하지 않는 경우 | 논리 구멍 | replace | KR; A 0 | |
| 빠진 경우 | `re:(규칙\|논리\|로직\|조건\|설계\|검사\|처리)[에의]?\s*구멍` | review | KR; 구멍 A 0.3 (all geometry) | A hole in geometry (구멍 체크) is not matched. |
| 대체 값, 대체 경로, 대신 | 폴백 | review | KR; 폴백 A 0, 대체 A 2.9 | A Fallback field name in the editor stays in English. |
| (say what it guards) | 센티넬 | replace | KR; A 0 | 잘못된 값이 넘어가지 않게 막는 값. |
| 오래된, 업데이트되지 않은 | 스테일 | replace | KR; A 0 | stale |
| 실제 코드, 런타임 코드 | 제품 코드 | replace | KR; A 0 | production code |
| 조건, 단계 | 관문 | review | KR; A 0 | gate. A gate in the game world stays. |
| 규격, 규정, 지켜야 하는 조건 | 계약 | review | KR; A 0 / K 1.9, K docs 8.9 | contract. A project that defines API 계약 as a term can allow it. |
| 말단, 끝단 | 리프 | review | KR; A 0 | 리프 노드 of a tree structure stays. |
| 남은, 참조가 끊긴 | 고아 | review | KR; A 0 | orphan |
| 활성인, 지금 그리는 | `re:화면\s*(을\s*)?(소유\|쥐)` | replace | KR; A 0 | 하드락이 화면을 소유 중이면 → 하드락이 활성이면. |
| 시작한다 | `re:기동(?!력\|성\|대\|전)` | replace | KR; A 0 | 보간을 기동한다 → 보간을 시작한다. |
| 비활성, 동작하지 않는, 사용하지 않는; 활성, 동작 중 | `re:죽은\s*(코드\|함수\|변수\|분기\|경로\|값\|설정\|기능\|참조\|포인터\|핸들)`, `re:살아\s?있는\s*(참조\|포인터\|객체\|오브젝트\|핸들\|구독\|바인딩\|타이머)` | review | KR; 죽다 A 2.6 / K 7.9, all character deaths in A | dead and alive code. Only code nouns are matched; characters, monsters and dummies dying are not. |
| 아직 정하지 않은, 나중을 위해 남겨 둔 | 열려 있, 열어 둔, 열어 두, 열어 놓 | review | KR; A 0.2 / K 3.2 | open question. Doors, windows, UI panels and files stay. |
| 요청한다, 허용한다 | `re:(전이\|입력)(를\|을\|가\|이)?\s*(연다\|여는\|열어)` | review | KR; A 0 / K 0.8 | 전이를 여는 트리거 → 전이를 요청하는 트리거. |
| 지운다, 그리지 않는다 | `re:(?<!체력이 )(?<!체력을 )(?<!게이지가 )(?<!HP가 )(?<!HP를 )깎(는\|아\|여\|인\|을)` | review | KR; A 0.2 | Surface or pixel subject. 체력이 깎인다 and 게이지가 깎인다 are normal industry speech and are not matched. |
| 지연 시간이 지나면 | 지연이 지나 | replace | KR; A 0 | |
| 나뉘지 않는다, 결과가 같다 | 가르지 않 | replace | KR; A 0 | |
| 넣는다, 전달한다, 사용한다 | `re:먹이(는\|지\|고\|면\|기\|던\|게)`, 먹여 | replace | KR; A 0 | feed |
| 감쇠가 크다, (say the effect) | `re:(감쇠\|값\|입력)(를\|을)\s*([가-힣]+\s+)?먹` | replace | KR; A 0 | 감쇠를 과하게 먹는다 → 감쇠가 너무 커서 회전 변화가 작아진다. |
| (say how the value changes) | `re:(값\|수치\|각도\|알파\|파라미터\|피치\|입력\|스틱\|축)(을\|를)\s*(민다\|미는\|밀어\|밀고\|밀면)` | review | KR; A 0 | push. Pushing an object stays. |
| 장착 해제한다 | `re:무기를\s*벗` | replace | KR; A 0 | |
| (name what decides the value) | 노리는, 노린다, 노리고 | review | KR; A 0 / K 0.8 | 입력이 노리는 단계 → 현재 입력에 해당하는 단계. A monster aiming at the player stays. |
| 해제한다, 참조를 유지한다 | 붙잡 | review | KR; A 0 / K 0.5 | |
| 선택한다 | `re:(?<![가-힣])(쥔\|쥐고\|쥐는)` | review | KR; A 0 | A weapon held in a hand stays. |
| ~로 쓰여 있다 | `re:(한국어\|영어\|한글)로\s*갈(려\|린\|리)` | replace | KR; A 0 | |
| (say what splits) | `re:손이\s*갈(리\|린\|립\|려\|렸)` | replace | KR; A 0 | A made-up idiom. |
| (Korean) | `re:[぀-ゟ゠-ヿ]` | replace | KR | Japanese kana mixed into Korean text. |

## Translationese

Patterns of translated Korean that a Korean technical writing guide lists (evidence `W`). They are grammatical, so people write them too; A and O are not counted yet. That is why the rows are `review` or `density`, not `replace`.

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| ~로, ~에서, 사용해, 호출해 | 통해, 통한 | review | W §36, §37 | Name the means: `Interface로 읽는다`, `콘솔에서 설정한다`, `API를 호출해 전송한다`. Keep 통해 only when no verb names the means. |
| 있다, 포함한다 | `re:[을를] 가지고 있`, `re:[을를] 가진다` | review | W §36 | A thing that has a value or tag: `ASC에 태그가 있고`. A class that holds a member may keep 가진다, or write 포함한다. |
| ~할 수 있다 | 가능하다 | review | W §36 | `빌드 후 가능하다` → `빌드한 뒤에 생성할 수 있다`. Name the action. 불가능하다 is not matched. |
| ~을, ~를 | `re:에 대해` | density | W §36 | `성능에 대해 알아본다` → `성능을 알아본다`. 에 대한 is normal Korean and is not matched. |
| (rewrite with a verb) | `re:(으로\|로)의 ` | density | W §40 | `노드 중심 흐름으로의 변경` → `노드 중심 흐름으로 변경`. |
| (rewrite with a verb) | `re:에서의` | density | W §40 | `PIE에서의 동작` → `PIE에서 동작할 때`. |
| ~하면 | `re:(?<!밖)의 경우` | review | W §36 | `호출의 경우` → `호출하면`. 그 밖의 경우 is not matched. |
| 보이는, 나타나는, ~되는 | 보여지, `re:되어지` | review | W §35 | Double passive: `보여지는` → `보이는`, `변경되어진` → `변경된`. |

## Casual words

People write these, but they carry no information. Remove them from comments and docs you write or correct. Inside a TODO they are fine.

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| (delete), 우선, 임시로 | 일단 | review | A 16 / K 0 | |
| (delete) | 그냥 | review | A 4.4 | |
| 등 | 등등 | review | A 2.1 | |
| 확인 필요, ~로 추정 | `re:(?<=[할될는인] )듯(?![가-힣])` | review | A 2.0 | State the uncertainty plainly. |
| (say what decides it) | 알아서 | review | A 2.1 | |
| (delete) | `re:(?<=[가-힣])\s*\.{3,}` | review | A 11 / K 0.8 | Trailing ... after Korean text. |

## Document references

References that the reader cannot follow from inside the document.

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| (name the section or link it) | `re:§\s*\d` | review | KR | Fine only if the document numbers its sections. |
| (say what the earlier state was) | 기존과 동일 | review | KR | |
