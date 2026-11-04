<!-- ko-lint: ignore-file -->
# Unreal Engine

Engine and editor words. When you mean the exact class, function or property, write the English name as in code (`UCharacterMovementComponent`, `BeginPlay`). Use the Korean word for the concept in prose.

## Editor and assets

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 에디터 | 편집기 | replace | 에디터 A 7.4 / K 20; 편집기 A 0 / K 18 | 에디터 모듈, 에디터 전용, 에디터 프리뷰. |
| 디테일 패널, 뷰포트, 아웃라이너, 콘텐츠 브라우저 | — | term | UE | If the team runs the English editor, write the English label: Details 패널. |
| 블루프린트, BP | — | term | A 3.3 | |
| 데이터 테이블, 데이터 에셋 | — | term | UE | |
| Row, 로우 | `re:(?<![가-힣])행(?=[을의이은에 ])` | review | Row A 3.5, 로우 A 0.5; 행 K raw 165 / A 0 | For DataTable rows. 표의 행 in a document table stays. |
| 프로퍼티, 변수 | 속성 | review | 프로퍼티 A 0.6 / K 9.4; 속성 A 1.7 / K 4.0; 변수 A raw 55 | UPROPERTY members: 프로퍼티. 속성 also means element type (ElementalType), so avoid it for properties. |
| PIE, 에디터 프리뷰 | — | term | A | |
| 쿠킹, 패키징, 빌드 | — | term | common | |

## Gameplay framework

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 액터, 컴포넌트, 폰, 캐릭터, 컨트롤러 | — | term | 액터 A raw 197 | |
| 게임 모드, 게임 스테이트, 플레이어 스테이트, 게임 인스턴스, 서브시스템 | — | term | UE | |
| 스폰한다 | — | term | 스폰 A 12 / K 3.8; 생성 A 21 / K 52 | Actors are 스폰. UObjects, widgets and data may be 생성. The lint does not check this; read for it. |
| Owner, 오너 | 소유 액터, 소유 폰, 소유 캐릭터, 소유 컨트롤러, 소유자 | review | Owner A 5.3, 오너 A 0.6; 소유 액터 A 0 / K 11; 소유자 A 0.2 / K 8.9 | Owner 액터, Owner 폰. Memory ownership (TUniquePtr owns a buffer) may keep 소유한다. |
| 틱, Tick | — | term | 틱 A 6.8 | 틱마다 and 매 프레임 are both fine. |
| 월드, 레벨, 맵 | — | term | 레벨 A 10, 맵 A 5.7 | |
| 로컬 플레이어, 로컬 컨트롤 | — | term | 로컬 A 11 | |

## Networking

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 서버, 클라이언트, 클라 | — | term | 서버 A 9.1 / K 0; 클라 A 3.5 | 클라 is an accepted short form in comments. |
| 리슨 서버, 데디 서버 | — | term | A | |
| 리플리케이트, 동기화 | — | term | 동기화 A 6.3; 복제 A 1.4 / K 11 | For network state never write 복제; it reads as copy. |
| 오소리티, 서버 권한 | — | term | UE | |
| RPC, 멀티캐스트 | — | term | common | |
| 서버 주도, 클라 주도 | — | term | A | Who drives movement or state. |

## Collision and queries

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 콜리전, 충돌 | — | term | 콜리전 A 4.8; 충돌 A 6.3 | 콜리전 for settings (프로파일, 채널, 프리셋). 충돌 for the event. |
| 트레이스, 라인 트레이스, 스윕 | — | term | A 1.2 | |
| 오버랩 | 겹침, 겹치면, 겹친 | review | 오버랩 A 1.7; 겹침 A 0.6 / K 9.8 | Overlap events and checks: 오버랩. Two ranges that overlap may stay 겹친다. |
| 벗어나면, EndOverlap | 이탈 | review | 이탈 A 0 / K 10 | |
| 콜리전 프로파일, 트레이스 채널 | — | term | 프로파일 A | |
| 캡슐 | — | term | A 8.0 | |

## Gameplay Ability System and tags

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 어빌리티, GA | — | term | GA A 14 / K 0.8; 어빌리티 A 7.5 / K 0 | AI text keeps the English word Ability in Korean prose; people write 어빌리티 or GA. |
| GE, 게임플레이 이펙트 | 효과 클래스, 효과를 적용, 효과를 제거 | review | GE A 5.1 / K 11; 효과 A 1.4 / K 16 | 이펙트 alone usually means VFX in comments, so say GE for gameplay effects. |
| 어트리뷰트, 어트리뷰트 세트 | — | term | Attribute A 3.0 | |
| 게임플레이 큐, GameplayCue | — | term | UE | GC also means garbage collection; spell out 게임플레이 큐 when it could be read either way. |
| 게임플레이 태그, 태그 | — | term | A | |
| ASC, 어빌리티 태스크 | — | term | A | |

## VFX and UI

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 이펙트, VFX, 나이아가라 | — | term | 이펙트 A 8.3; 나이아가라 A raw 16 | 이펙트를 출력, 이펙트 재생. |
| 위젯, UMG, HUD, 뷰모델 | — | term | 위젯 A 15 | |
| 카메라 셰이크 | 흔들림 (카메라) | term | common | Camera Shake assets and tasks. |

## Engine internals

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 가비지 컬렉션, GC, CDO, 리플렉션, UHT | — | term | UE | |
| 로드, 로딩, 비동기 로드 | — | term | 로딩 A 3.3 / K 0.1; 로드 A 4.1 / K 17 | |
| 소프트 레퍼런스, 하드 레퍼런스 | — | term | 레퍼런스 A raw 12 | |
| 델리게이트, 바인딩, 콜백 | — | term | 바인딩 A 5.9 | |
| 풀링, 액터 풀 | — | term | A | |
| 트랜스폼, 위치, 회전, 스케일, 오프셋 | — | term | 위치 A 32; 회전 A 15; 트랜스폼 A 2.1 | Prose may use 위치 and 회전 or 로케이션 and 로테이션; keep one pair per file. |
| 월드 좌표, 로컬 좌표, 컴포넌트 스페이스 | — | term | A | |
| 노멀, 포워드 벡터, 전방 | — | term | 노멀 A 4.1 | |
| 네비메시, NavMesh | — | term | A | |
| CVar, 콘솔 명령, 치트 | — | term | A | |
| 오버라이드 | — | term | A raw 16 | Override할 (the English verb) is also common in A. |
