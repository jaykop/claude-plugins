<!-- ko-lint: ignore-file -->
# AI, world, items, UI and production

## AI

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 비헤이비어 트리, BT, 블랙보드, 블랙보드 키 | — | term | A | |
| 태스크, 데코레이터, 서비스 | — | term | 태스크 A 12 | BT nodes. |
| 스테이트 트리 | — | term | UE | |
| 퍼셉션, 센싱, 인지, 감지 | — | term | 인지 A 16; 감지 A 5.4; 센싱 A 4.7 | 인지 for an AI noticing a target; 센싱 for sensor sweeps; 퍼셉션 for the UE system. |
| 패트롤, 로밍 | 순찰, 배회 | term | 패트롤 A 0.9; 로밍 A 0.5 | |
| 추적 | 추격 | term | A 5.4 | 추적 거리, 추적 범위. |
| EQS | — | term | A | |

## Spawn and world

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 스폰, 리스폰, 디스폰 | — | term | 스폰 A 12 | |
| 스포너 | — | term | A 0.8 / K 19 | |
| 레벨, 맵, 필드, 던전 | — | term | 레벨 A 10; 맵 A 5.7 | |
| 체크포인트, 플레이어 스타트 | — | term | A | |
| 볼륨, 트리거 볼륨 | — | term | 볼륨 A raw 41 | |
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

## UI

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 위젯, 팝업, HUD | — | term | 위젯 A 15; 팝업 A 4.5 | |
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
