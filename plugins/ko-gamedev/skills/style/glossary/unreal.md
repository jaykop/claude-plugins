<!-- ko-lint: ignore-file -->
# Unreal Engine

Engine and editor words. When you mean the exact class, function or property, write the English name as in code (`UCharacterMovementComponent`, `BeginPlay`). Engine type names stay in English in prose too: Actor, Component, Mesh, Tick, Ability, Widget. The rule is in [../style/comments.md](../style/comments.md#words). Concept and action words keep their Korean loanwords: 콜리전, 트레이스, 스폰, 바인딩.

## Editor and assets

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 에디터 | 편집기 | replace | 에디터 A 7.4 / K 20; 편집기 A 0 / K 18 | 에디터 모듈, 에디터 전용, 에디터 프리뷰. |
| 디테일 패널, 뷰포트, 아웃라이너, 콘텐츠 브라우저 | — | term | UE | If the team runs the English editor, write the English label: Details 패널. |
| Blueprint, BP | 블루프린트 | replace | style; 블루프린트 A 3.3; B raw 33 / 15 | Engine type name. 블프 is in spelling.md. |
| Data Table, Data Asset | 데이터 테이블, 데이터 에셋 | replace | style | Engine type names. A balance sheet in design talk stays 테이블 (systems.md). |
| Mesh, Static Mesh, Skeletal Mesh | `re:(?<![가-힣])(스태틱 \|스켈레탈 )?메(시\|쉬)(?!지)` | replace | style; 메시 A 9.8, 메쉬 A 2.1 | Engine type names. 메시지 is not matched. |
| Material, Material Instance | 머티리얼, 메테리얼, 매터리얼, 머터리얼, 마테리얼 | replace | style; UE; B | Engine type names. 마테리얼 is a variant that B's own post checker watches for. |
| Texture | 텍스처, 텍스쳐 | replace | style; UE | Engine type name. |
| Row, 로우 | `re:(?<![가-힣])행(?=[을의이은에 ])` | review | Row A 3.5, 로우 A 0.5; 행 K raw 165 / A 0 | For DataTable rows. 표의 행 in a document table stays. |
| 프로퍼티, 변수 | 속성 | review | 프로퍼티 A 0.6 / K 9.4; 속성 A 1.7 / K 4.0; 변수 A raw 55 | UPROPERTY members: 프로퍼티. 속성 also means element type (ElementalType), so avoid it for properties. |
| PIE, 에디터 프리뷰 | — | term | A | |
| 쿠킹, 패키징, 빌드 | — | term | common | |

## Gameplay framework

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| Actor, Component, Pawn | 액터, 컴포넌트, 콤포넌트, `re:(?<![가-힣])폰(?!트)` | replace | style; 액터 A raw 197, 컴포넌트 A 12; B raw Actor 76 / 액터 51, Component 84 / 컴포넌트 16 | Engine type names. People write 액터 and 컴포넌트 (A); this skill writes the English name. Attach the particle by the English sound: Actor를, Component가. 폰트 is not matched. |
| Character, Player Controller, AI Controller | 캐릭터, 컨트롤러 | term | style | Write the English name when you mean the engine class or its instance (ACharacter, APlayerController, AAIController). A game character in design talk stays 캐릭터, and a gamepad stays 컨트롤러. The lint does not check this; read for it. |
| Game Mode, Game State, Player State, Game Instance, Subsystem | 게임 모드, 게임 스테이트, 플레이어 스테이트, 게임 인스턴스, 서브시스템 | replace | style; UE | Engine type names. |
| 스폰한다 | — | term | 스폰 A 12 / K 3.8; 생성 A 21 / K 52 | Actors are 스폰. UObjects, widgets and data may be 생성. The lint does not check this; read for it. |
| Owner, 오너 | 소유 액터, 소유 폰, 소유 캐릭터, 소유 컨트롤러, 소유자 | review | Owner A 5.3, 오너 A 0.6; 소유 액터 A 0 / K 11; 소유자 A 0.2 / K 8.9 | Owner Actor, Owner Pawn. Memory ownership (TUniquePtr owns a buffer) may keep 소유한다. |
| Tick | 틱 | replace | style; 틱 A 6.8 | Engine function name. Tick마다 and 매 프레임 are both fine. |
| 월드, 레벨, 맵 | — | term | 레벨 A 10, 맵 A 5.7 | Ordinary game words, so they stay Korean. Write World or Level only when you name the UWorld or ULevel object. |
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

## Input

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 입력, 인풋 | — | term | B raw 35 / 18 | Both are normal. 인풋 랙 and 인풋 버퍼 are fixed compounds. Otherwise keep one word per file. |
| Enhanced Input, Input Action, Input Mapping Context, IMC, Input Trigger, Input Modifier | 인풋 액션, 입력 액션, 인풋 매핑 컨텍스트, 입력 매핑 컨텍스트, 인풋 트리거, 입력 트리거 | replace | style; B IMC raw 6 | Engine type names. B writes InputAction, IMC and Input Trigger in English. Trigger types (Hold, Release, Tap) stay English too; the act is 트리거링 (spelling.md). |

## Gameplay Ability System and tags

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| Ability, GA | 어빌리티 | replace | style; GA A 14 / K 0.8; 어빌리티 A 7.5 / K 0 | Engine type name, also in Ability Task. People write 어빌리티 or GA (A); this skill writes Ability or GA. |
| Gameplay Effect, GE | 게임플레이 이펙트 | replace | style | Engine type name. |
| GE, Gameplay Effect | 효과 클래스, 효과를 적용, 효과를 제거 | review | GE A 5.1 / K 11; 효과 A 1.4 / K 16 | 이펙트 alone usually means VFX in comments, so say GE for gameplay effects. |
| Attribute, Attribute Set | 어트리뷰트 | replace | style; Attribute A 3.0 | Engine type names. |
| Gameplay Cue, GameplayCue | 게임플레이 큐 | replace | style; UE | Engine type name. GC also means garbage collection; spell out Gameplay Cue when it could be read either way. |
| Gameplay Tag, 태그 | 게임플레이 태그 | replace | style; A | Engine type name. 태그 alone is an ordinary word and stays. |
| ASC, Ability Task | — | term | A | The Ability row matches 어빌리티 태스크. |

## VFX and UI

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 이펙트, VFX | — | term | 이펙트 A 8.3 | A concept word, so it stays Korean. 이펙트를 출력, 이펙트 재생. |
| Niagara, Niagara System | 나이아가라, `re:(?<![가-힣])니아가라` | replace | style; 나이아가라 A raw 16 | Engine type names. |
| Widget, UMG, HUD, ViewModel | 위젯, 뷰모델 | replace | style; 위젯 A 15; B raw 13 / 2 | Engine type names. |
| Camera Shake | 카메라 셰이크, 카메라 쉐이크 | replace | style; common | Engine type name, for Camera Shake assets and tasks. Not 흔들림 either. |

## Rendering and performance

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| Nanite, Lumen | 나나이트, 루멘 | replace | style; B 나나이트 raw 4 | Engine feature names, written in English like Niagara. Nanite Mesh. |
| 드로우콜, Draw Call | — | term | B raw 12 | B writes both. Keep one per file. |
| PSO, PSO 캐시 | — | term | B | Pipeline State Object. PSO 캐시 수집, 미리 컴파일. |
| LOD | — | term | B raw 7 | LOD 세팅, LOD 교체. |
| 성능, 퍼포먼스 | — | term | B raw 33 / 23 | Both are normal. Keep one per file. |
| 최적화, 오버헤드, 프로파일링 | — | term | B raw 23, 19, 2 | |
| 라이팅 | — | term | B raw 18 / 조명 0 | Rendering light. A light Actor placed in a level is a Light. |
| 트라이앵글, 폴리곤 | — | term | B raw 3, 4 | Mesh density. |
| 컬링, 오클루전 컬링 | — | term | common | Rendering. Fading an object in front of the camera is a camera job (systems.md, Camera). |

## Engine internals

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 가비지 컬렉션, GC, CDO, 리플렉션, UHT | — | term | UE | |
| 로드, 로딩, 비동기 로드 | — | term | 로딩 A 3.3 / K 0.1; 로드 A 4.1 / K 17 | |
| 소프트 레퍼런스, 하드 레퍼런스 | — | term | 레퍼런스 A raw 12 | |
| Delegate, 바인딩, 콜백 | 델리게이트 | replace | style; 바인딩 A 5.9 | Delegate is an engine type name. 바인딩 and 콜백 are concepts and stay. |
| 풀링, Actor 풀 | — | term | A | |
| 트랜스폼, 위치, 회전, 스케일, 오프셋 | — | term | 위치 A 32; 회전 A 15; 트랜스폼 A 2.1 | Prose may use 위치 and 회전 or 로케이션 and 로테이션; keep one pair per file. |
| 월드 좌표, 로컬 좌표, Component Space | — | term | A | |
| 노멀, 포워드 벡터, 전방 | — | term | 노멀 A 4.1 | |
| NavMesh | 네비메시, 내비메시 | replace | style; A | Engine type name. |
| CVar, 콘솔 명령, 치트 | — | term | A | |
| 오버라이드 | — | term | A raw 16 | Override할 (the English verb) is also common in A. |
