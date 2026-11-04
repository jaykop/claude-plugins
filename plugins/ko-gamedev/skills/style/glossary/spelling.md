<!-- ko-lint: ignore-file -->
# Loanword spelling

One spelling per word. The policy for choosing is in [README.md](README.md#spelling-policy): team usage first, then the standard spelling, then a per-project choice.

## Fixed spellings

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 타겟 | 타깃 | replace | A 43 / 0.8; K 5.4 / 2.6 | Industry spelling. Standard Korean is 타깃; use it only where the publisher requires standard spelling (player-facing text, official documents). |
| 대미지 | 데미지 | replace | A 7.4 / 3.6 | Both are common. 대미지 is standard and more frequent in A. |
| 세팅 | 셋팅 | replace | A 37 / 0.5 | |
| 메시 | 메쉬 | replace | A 9.8 / 2.1 | UE: 스태틱 메시, 스켈레탈 메시. |
| 이펙트 | 이팩트 | replace | A 8.3 / 0.2 | |
| 애니메이션 | 애니매이션, 에니메이션 | replace | A 13 / 3.2 | A frequent typo in human comments. |
| 메시지 | 메세지 | replace | A 5.0 / 3.5 | |
| 액세서리 | 악세서리, 악세사리 | replace | A 0 / 2.8 | Standard spelling; people often miss it. |
| 태스크 | 테스크 | replace | A 12 / 2.4 | |
| 파라미터 | 파라메터 | replace | A 3.0 / 0.8 | |
| 노멀 | 노말 | replace | A 4.1 / 0.3 | Normal vector. 노멀 공격 (a basic attack) is 일반 공격 or 기본 공격. |
| 텍스처 | 텍스쳐 | replace | A 0 / 1.1 | UE |
| 셰이더 | 쉐이더 | replace | A 0 / 0.2 | UE |
| 머티리얼 | 메테리얼, 매터리얼, 머터리얼 | replace | A 0 / 1.1; K 2.7 / 0 | UE |
| 콘텐츠 | 컨텐츠 | replace | common | UE: 콘텐츠 브라우저. |
| 스태미나 | 스테미나 | replace | A 0.6 / 0 | |
| 스탯 | 스텟 | replace | A 2.9 / 0 | |
| 컴포넌트 | 콤포넌트 | replace | A 12 / 0 | |
| 리플리케이션, 리플리케이트 | 레플리케이션, 레플리케이트 | replace | A 0.3 / 0 | UE |
| 커스터마이징 | 커스터마이즈 | review | A 1.7 / 0 | As a noun. The verb 커스터마이즈한다 is fine. |
| 나이아가라 | `re:(?<![가-힣])니아가라` | replace | KR | |
| 셰이프 | 쉐이프 | replace | KR; Shape A 4.4 | |
| 블루프린트, BP | 블프 | review | KR; A 0 | Casual short form; fine in chat, not in comments or docs. |

## Pick one per project

Record the choice in the project terms file. Until then, keep whatever the file already uses.

| Use | Avoid | Kind | Evidence | Note |
|---|---|---|---|---|
| 에셋, 애셋 | — | term | 에셋 A 7.7 / 애셋 A 3.3; D 2.0 / 15.9; K 37 / 0 | Code comments lean 에셋. The UE Korean docs and D write 애셋. |
| 타게팅, 타겟팅 | — | term | A 3.0 / 0.8 | Follow the project's targeting system name. |
| 셋업, 세팅 | — | term | 셋업 A 2.9 | 셋업 for a one-time setup step, 세팅 for values. |
| 캐싱, 캐시 | — | term | 캐싱 A 2.9; 캐시 A 1.2 / D 24 | 캐싱 for the act, 캐시 for the stored data (포즈 캐시). |
