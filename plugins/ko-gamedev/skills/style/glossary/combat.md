<!-- ko-lint: ignore-file -->
# Combat

Combat words are shared by code, design documents and conversation. Keep the team's own pair when it differs (for example 하드락 against 락온) and record it in the project terms file.

## Targets and lock-on

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 타겟 | 락온 대상, 공격 대상, 대상 액터, 타게팅 대상, 대상 후보 | review | 타겟 A 43 / K 5.4; 대상 액터 A 0.2 / K 11; 락온 대상 A 0 / K 3.1 | The actor being attacked, tracked or locked is 타겟. 적용 대상 and 검사 대상 stay 대상. Bare 대상 is counted per file by core.md; read those lines too. |
| 하드락, 락온 | — | term | 하드락 A 10 / K 0; 락온 A 1.5 / K 22 | The target the player fixed on purpose. 하드락 해제, 락온 유지 거리. |
| 소프트 타겟, 소프트락 | — | term | A 1.2 | A target picked automatically from input direction and distance. |
| 타게팅 | — | term | A 3.0 | Choosing a target. Also the UE Targeting System. |
| 어그로 | — | term | A 1.4 | Who the monster attacks next. |

## Damage and hits

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 대미지 | 피해 | review | 대미지 A 7.4, 데미지 A 3.6; 피해 A 0 / K 16 | Player-facing text follows the design team's word; this row is for code and tech docs. |
| 피격, 피격자, 피격 반응 | — | term | 피격 A 12 / K 12 | 피격 판정, 피격 이펙트, 피격 반응 GA. |
| 히트, 적중 | 명중 | review | 히트 A 4.2; 명중 A 0.2 / K 0.7 | 히트 판정, 히트 이펙트, 다단 히트. |
| 히트한다, 피격된다 | 맞힌, 맞히고, 맞히면, 맞힐 | review | 맞히 A 0 / K 1.2 | 투사체가 타겟 하나만 히트한다. |
| 공격자 | — | term | A 2.4 | |
| 판정 | — | term | | 공격 판정, 히트 판정, 판정 프레임, 판정 범위. For general evaluation use 판단 or 체크 (core.md). |
| 히트박스, 허트박스 | — | term | K HurtBox 12 | Attack-side and hit-side areas. Keep the project's class names in English. |
| 다단 히트 | — | term | 다단 A 1.5 | |
| 막타 | — | term | A 1.4 | The last hit. In a document, write 마지막 타격(막타) at first use. |
| 약점, 파츠, 파츠 브레이크, 부위, 부위 파괴 | — | term | 파츠 A 2.6; 부위 A 2.3 | Keep the project's own word. |
| 투사체, 프로젝타일 | 발사체 | term | 투사체 A 3.5; 프로젝타일 A 1.1 | |

## Reactions and status

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 경직 | — | term | A 0.9 | Short stun on hit. |
| 그로기 | — | term | A 1.8 | |
| 넉, 넉백, 넉다운, 다운 | — | term | 넉 A 2.7 | |
| 스턴 | 기절 | term | A 2.3 | |
| 슈퍼아머 | — | term | common | No hit reaction while active. |
| 포이즈 | — | term | Poise A 1.5 / K 3.4 | The stagger gauge behind 경직 and 그로기. |
| 버프, 디버프 | — | term | A 0.8 | |
| 부활 | — | term | A 3.5 | Revive on the spot. Respawn at a point is 리스폰 (systems.md). |

## Defense and timing

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 가드, 가드 브레이크, 가드 게이지 | 방어 붕괴 | term | 가드 A 3.6 | |
| 패링 | 튕겨내기 | term | common | |
| 회피, 닷지, 구르기 | — | term | 회피 A 0.9; 닷지 A 0.5; 구르기 D 4.0 | |
| 저스트 회피, 저스트 가드 | — | term | common | |
| 딜레이, 선딜, 후딜 | — | term | 딜레이 A 3.0 | 선딜 is the wind-up before the hit; 후딜 is the recovery after it. |
| 캔슬 | — | term | A 2.3 / K 4.2 | 캔슬 가능 구간. |
| 콤보 | 연계 | term | A 3.9 | |
| 쿨타임, 쿨다운 | 재사용 대기시간 | term | A 0.8 / 0.8 | GAS Cooldown GE: 쿨다운. Design talk: 쿨타임. |

## Skills and stats

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 스킬 | 기술 | term | 스킬 A 17 / K 0 | The player-facing name of an ability. The code class stays an ability (GA). |
| 패시브, 액티브 | — | term | A | |
| 스탯, 어트리뷰트 | 능력치 | term | 스탯 A 2.9 | |
| 체력, HP | 생명력 | term | 체력 A 1.1; HP A 1.2 | |
| 게이지 | — | term | A | |
