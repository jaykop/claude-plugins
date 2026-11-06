<!-- ko-lint: ignore-file -->
# Animation

Animation words come mostly from corpus D (the animation design pages) and A. Korean teams write the UE node and asset names as loanwords (D: 스테이트, 트랜지션, 블렌드 스페이스). This skill writes engine type names in English (State, Transition, Blend Space) and keeps the concept words that D uses: 블렌드, 커브, 포즈, 애디티브, 루트 모션.

## Assets and notifies

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| Anim Sequence, AnimGraph, Anim Blueprint, ABP, Anim Instance | 애님 시퀀스, 애님 그래프, 애님 BP, 애님 블루프린트, 애님 인스턴스 | replace | style; 애님 A 10 / K 0; D 101 | Engine type names. A curve inside an animation is 커브, a concept. The standalone noun 애니메이션 stays. |
| Montage, Montage Section, Slot | 몽타주 | replace | style; 몽타주 A 6.3 / D 16 | Engine type names. Montage 재생, 블렌드 아웃. An inventory 슬롯 stays (systems.md). |
| Anim Sequence, 모션 | 클립 | review | 클립 A 0 / O 0 / K 9.4; 모션, 시퀀스, 애니메이션 A 36 | A Unity AnimationClip may keep 클립. |
| Notify, Notify State | 노티, 애니메이션 알림, 애님 알림 | replace | style; 노티파이 A 4.1, 노티 A 4.5; 알림 A 1.5 / K 20 | Engine type names (AnimNotify, AnimNotifyState). Never 알림. |
| 커브, 커브값 | 곡선 | replace | 커브 A 11 / D 139; 곡선 A 0 / K 4.4 | |
| Sync Marker | 싱크 마커 | replace | style; D raw 14 | Engine type name. |
| 루트 모션 | — | term | A 7.5 | 루트 모션 몽타주. |
| 본 | 뼈 | term | A | A concept word, so it stays Korean. |
| Socket, Skeleton, Skeletal Mesh | 소켓, 스켈레톤 | replace | style; 소켓 A 4.8 | Engine type names. The Mesh row in unreal.md matches 스켈레탈 메시. |
| 프레임, 키프레임 | — | term | A | |
| 플레이 레이트, 재생 속도 | — | term | D PlayRate | |

## Blending and state machines

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 블렌드한다, 블렌딩 | 섞는다, 섞고, 섞은, 섞어 | review | 블렌드 A 1.2 / D 64; 블렌딩 A 4.5; 섞 A 0 / K 7.4 / D 4.0 | D uses 섞다 twice in explanations; comments use 블렌드. Mixing items that are not poses (tasks in a Preset, sounds) stays 섞다. |
| 블렌드 인, 블렌드 아웃, 블렌드 타임 | — | term | A | |
| Blend Space | 블렌드 스페이스 | replace | style; D raw 14 | Engine type name. |
| State, State Machine | 상태 기계, `re:(?<![가-힣])(?<!게임 )(?<!플레이어 )(?<!노티파이 )스테이트(?! ?트리)( ?머신)?` | replace | style; 스테이트 D 107 / A 2.3 | Engine node type names in an AnimGraph. A generic state elsewhere is 상태. Game State and Player State are in unreal.md, StateTree in systems.md, Notify State in the Notify row. |
| Transition, Transition Rule | 트랜지션 | replace | style; 트랜지션 D 48 | Engine node type names. |
| Transition, Transition Rule | 전이 | review | 전이 A 2.1 / K 24 | A graph system that defines its own 전이 can allow it in the project terms file. |
| 애디티브 | 가산 | term | D raw 13 | 애디티브 포즈, 애디티브로 추가한다. |
| 포즈 | — | term | D raw 99 | A concept word, so it stays Korean. |
| Cached Pose | 포즈 캐시 | replace | style; D | Engine node type name. |
| 레이어 블렌딩, 오버레이 레이어, Layered Blend per Bone | — | term | D | |
| Linked Anim Layer | 링크드 애님 레이어 | replace | style; D | Engine node type name. |

## Locomotion

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 로코모션 | 이동 애니메이션 | term | D raw 13 | |
| 스프린트, 대시 | 질주 | replace | 스프린트 A 2.0 / D 6.0; 질주 A 0 / K 4.8 | |
| 걷기, 달리기, Gait | — | term | A | Walk, Run and Sprint gaits. |
| 스트레이핑 | 게걸음 | term | D | |
| 피벗 | — | term | D 22 | Direction change while strafing. |
| 런스타트, 런스탑 | — | term | D | |
| 턴 인 플레이스, 제자리 회전 | — | term | D title; 제자리 A raw 14 | |
| 보폭, Stride | — | term | D | Write 보폭(Stride) at first use. |
| 착지, 랜드 | — | term | D raw 21 | |
| Aim Offset, 스파인 로테이션 | 에임 오프셋 | replace | style; D | Aim Offset is an asset type. 스파인 로테이션 is a concept and stays. |

## Motion and IK

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 모션 워핑, 모션 매칭 | — | term | A | |
| 풋 IK, 풋락, 풋스텝 | — | term | A | |
| 파쿠르, 볼트, 월런, 클라이밍 | — | term | A | Vault is 볼트 in a parkour system. |
