<!-- ko-lint: ignore-file -->
# Animation

Animation words come mostly from corpus D (the animation design pages) and A. In AnimGraph talk, Korean teams keep the UE node and asset names as loanwords: 스테이트, 트랜지션, 블렌드 스페이스.

## Assets and notifies

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 애님 시퀀스, 애님 커브, 애님 그래프, 애님 BP, 애님 인스턴스 | — | term | 애님 A 10 / K 0; D 101 | 애님 is the usual prefix in compounds. The standalone noun is 애니메이션. |
| 몽타주, 몽타주 섹션, 슬롯 | — | term | 몽타주 A 6.3 / D 16 | 몽타주 재생, 블렌드 아웃. |
| 애님 시퀀스, 모션 | 클립 | review | 클립 A 0 / O 0 / K 9.4; 모션, 시퀀스, 애니메이션 A 36 | A Unity AnimationClip may keep 클립. |
| 노티파이, 노티, 노티파이 스테이트 | 애니메이션 알림, 애님 알림 | replace | 노티파이 A 4.1, 노티 A 4.5; 알림 A 1.5 / K 20 | AnimNotify is never 알림 in a game team. |
| 커브, 커브값 | 곡선 | replace | 커브 A 11 / D 139; 곡선 A 0 / K 4.4 | |
| 싱크 마커 | — | term | D raw 14 | |
| 루트 모션 | — | term | A 7.5 | 루트 모션 몽타주. |
| 본, 소켓, 스켈레톤, 스켈레탈 메시 | 뼈 | term | 소켓 A 4.8 | |
| 프레임, 키프레임 | — | term | A | |
| 플레이 레이트, 재생 속도 | — | term | D PlayRate | |

## Blending and state machines

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 블렌드한다, 블렌딩 | 섞는다, 섞고, 섞은, 섞어 | review | 블렌드 A 1.2 / D 64; 블렌딩 A 4.5; 섞 A 0 / K 7.4 / D 4.0 | D uses 섞다 twice in explanations; comments use 블렌드. Mixing items that are not poses (tasks in a Preset, sounds) stays 섞다. |
| 블렌드 인, 블렌드 아웃, 블렌드 타임 | — | term | A | |
| 블렌드 스페이스 | — | term | D raw 14 | |
| 스테이트, 스테이트 머신 | 상태 기계 | term | 스테이트 D 107 / A 2.3 | In AnimGraph talk, 스테이트. A generic state elsewhere is 상태. |
| 트랜지션, 트랜지션 룰 | 전이 | review | 트랜지션 D 48; 전이 A 2.1 / K 24 | A graph system that defines its own 전이 can allow it in the project terms file. |
| 애디티브 | 가산 | term | D raw 13 | 애디티브 포즈, 애디티브로 추가한다. |
| 포즈, 포즈 캐시 | — | term | D raw 99 | |
| 레이어 블렌딩, 오버레이 레이어, Layered Blend per Bone | — | term | D | |
| 링크드 애님 레이어 | — | term | D | |

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
| 에임 오프셋, 스파인 로테이션 | — | term | D | |

## Motion and IK

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 모션 워핑, 모션 매칭 | — | term | A | |
| 풋 IK, 풋락, 풋스텝 | — | term | A | |
| 파쿠르, 볼트, 월런, 클라이밍 | — | term | A | Vault is 볼트 in a parkour system. |
