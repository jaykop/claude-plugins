<!-- ko-lint: ignore-file -->
# AI, world, items, camera, UI and production

## AI

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| Behavior Tree, BT, Blackboard, Blackboard Key | 비헤이비어 트리, 블랙보드 | replace | style; A | Engine type names. |
| Task, Decorator, Service | 데코레이터 | replace | style; 태스크 A 12 | BT and StateTree node types. 태스크 and 서비스 are also ordinary words; write Task and Service when you mean the node type. |
| StateTree | 스테이트 트리 | replace | style; UE | Engine type name. |
| Perception, 센싱, 인지, 감지 | 퍼셉션 | replace | style; 인지 A 16; 감지 A 5.4; 센싱 A 4.7 | 인지 for an AI noticing a target; 센싱 for sensor sweeps; Perception for the UE system (AIPerception). |
| 패트롤, 로밍 | 순찰, 배회 | term | 패트롤 A 0.9; 로밍 A 0.5 | |
| 추적 | 추격 | term | A 5.4 | 추적 거리, 추적 범위. |
| EQS | — | term | A | |
| 자극, Stimulus | — | term | B raw 10 | What AI Perception senses: 시각 자극, 청각 자극. The component is AI Perception Stimuli Source; write its name in English. |
| 감각, Sense | — | term | B raw 2 | Sight, Hearing and Damage senses of AI Perception. Config classes stay English (AISense_Sight). |
| 길찾기, 경로 탐색 | — | term | B raw 3 | NavMesh is in unreal.md. |

## Spawn and world

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 스폰, 리스폰, 디스폰 | — | term | 스폰 A 12 | |
| 스포너 | — | term | A 0.8 / K 19 | |
| 레벨, 맵, 필드, 던전 | — | term | 레벨 A 10; 맵 A 5.7 | |
| 체크포인트, Player Start | 플레이어 스타트 | replace | style; A | Player Start is an engine type name. 체크포인트 is a game word. Projects often give checkpoints their own name (B: 캠프); record it in the project terms file. |
| 탈것, 탑승, Vehicle | `re:(?<![가-힣])탈 것(?!이)` | review | B raw 6 / 17 (탈것 / 탈 것); K docs 탈것 raw 4 | 탈것 is one word. Write Vehicle when you mean the engine class (Chaos Vehicle). 탈 것이다 (will ride) is not matched, and neither is 탈 것이 as a subject; read for those. |
| 볼륨, Trigger Volume | 트리거 볼륨 | replace | style; 볼륨 A raw 41 | Trigger Volume is an engine type name. |
| 레벨 이벤트, 연출 | — | term | 연출 A 3.5 | |

## Items and progression

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 아이템, 장비, 무기, 방어구 | — | term | 아이템 A raw 168 | |
| 장착, 장착 해제 | 착용 해제 | term | 장착 A 9.7; 착용 A 2.4 | Weapons are 장착. 착용 is fine for clothes and armor. |
| 인벤토리, 스토리지, 슬롯, 퀵슬롯 | — | term | 인벤토리 A 4.8 | |
| 재료, 제작 | 크래프팅 | term | 제작 A 11 | 아이템 제작. |
| 보상, 드롭 | — | term | 보상 A 5.0 | |
| 상점, 구매, 판매, 재화 | — | term | A | |
| 퀘스트, 스텝, 목표, 저널 | — | term | 퀘스트 A 8.6 | |
| 세이브, 로드, 세이브 슬롯 | — | term | 세이브 A raw 33 | |
| 커스터마이징 | — | term | A 1.7 | |

## Camera

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 구도 | — | term | B raw 14 | Camera framing for a state: 전투 구도, 비전투 구도. A base 구도 plus offsets per state. |
| Spring Arm, Camera Component | 스프링 암, 스프링암 | replace | style; UE | Engine type names. The Component row in unreal.md matches 카메라 컴포넌트. Camera Shake is in unreal.md. |
| 장애물 투명화 | — | term | B raw 4 | Fading the object between the camera and the character. Occlusion culling is a rendering term (unreal.md). |
| 하이라이트, 아웃라인 | — | term | B raw 12 | Drawing a character hidden behind an obstacle, usually with Custom Depth and Stencil. |

## UI

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| Widget, 팝업, HUD | — | term | 위젯 A 15; 팝업 A 4.5 | The Widget row in unreal.md matches 위젯. |
| 인디케이터, 미니맵, 툴팁 | — | term | 인디케이터 A 2.9 | |
| 포커스, 셀렉션, 노드 | — | term | A | Skill tree and menu navigation. |
| 표기, 표시 | — | term | 표기 A raw 44 | 쿨타임 표기, 대미지 표시. |

## Production

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 기획, 기획자, 기획 의도 | 게임 설계 | term | 기획 A 4.4 / K 0.1 | 기획 확인 필요. |
| 연출, 컷신, 시네마틱 | — | term | 연출 A 3.5 | |
| 리소스, 아트, TA | — | term | common | |
| 코어 테스트, FGT, CBT, QA, TF | — | term | A | |
| 밸런스, 수치, 테이블 | — | term | 수치 A raw 34 | |
| 임시 코드, TODO | — | term | TODO A 26 / K 0.1 | Format: style/comments.md. |
