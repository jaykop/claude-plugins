#!/usr/bin/env bash
# 시험용 프로젝트: 기술 동향 고문이 Step 0 에서 묻지 않도록 필요한 프로필 칸을 채우고,
# GAS 가 "사용 중"인 기술 목록과 자체 쿨다운 코드를 둔다.
set -eu

mkdir -p .claude/advisors/reports/_state Source/EvalGame/Combat

cat > .claude/advisors/profile.md <<'EOF'
---
profile_version: 1
updated: 2026-10-01

project_name: EvalGame          # [사용자] 시험용 이름
genre: 3인칭 액션               # [사용자]
play_mode: 싱글                 # [사용자]
ip_based: false                 # [사용자]
platforms: [PC-Steam]           # [사용자]
target_spec: 최저 GTX 1660, 권장 RTX 3070   # [사용자]
regions: [KR, NA]               # [사용자]
business_model: 패키지          # [사용자]
release_window: 미정            # [사용자]
dev_stage: 본 제작              # [사용자]
next_milestone: 알파 2027-03-31 # [사용자]
team_size: 약 20명 [사용자]
feature_cutoff: 2027-02-01      # [사용자]

engine:
  name: Unreal Engine           # [사용자]
  version: 5.6.1                # [사용자]
  source_build: false           # [사용자]
  root:                         # [사용자] 모름

source_roots: [Source]          # [사용자]
project_file: EvalGame.uproject # [사용자]

vcs: git                        # [사용자]
vcs_read_commands: []           # [사용자] 없음

decision_owners:
  design: 기획 리드             # [사용자]
  business: PD                  # [사용자]
  tech: 클라이언트 프로그래머(이 프로필을 쓰는 사람)   # [사용자]
  schedule: 클라이언트 프로그래머(이 프로필을 쓰는 사람)   # [사용자]
user_role: 클라이언트 프로그래머   # [사용자]

report_dir: .claude/advisors/reports
share_scope: personal
stale_after_days: 90
code_change_entry:              # [사용자] 모름
search_banned_terms: []         # [사용자] 없음
search_banned_combos: []        # [사용자] 없음

radar:
  engine_mod_marker:            # [사용자] 모름
  engine_mod_dirs: []           # [사용자] 없음
  interests: []                 # [사용자] 없음
  excluded: []                  # [사용자] 없음
  ai_tool_policy: 미확인        # [사용자]
  knowledge_dir:                # [사용자] 없음
---
EOF

cat > .claude/advisors/reports/_state/radar-inventory.md <<'EOF'
# 프로젝트 기술 목록

다음 점검: 2026-12-31
작성: radar / 마지막 갱신: 2026-10-01 / 기준 리비전: 확인 못 함

## 엔진
| 항목 | 값 | 근거 위치 |
|---|---|---|
| 엔진 버전 | 5.6.1 | 프로필 engine.version |
| 소스 빌드 여부 | 아니오 | EvalGame.uproject 의 EngineAssociation |
| 엔진 수정 블록 수 | 세지 않음 | 프로필 radar.engine_mod_dirs 비어 있음 |

## 플러그인·기능
| ID | 이름 | 상태 | 근거 위치 |
|---|---|---|---|
| TI-001 | GameplayAbilities | 사용 중 | EvalGame.uproject 의 Plugins, Source/EvalGame/EvalGame.Build.cs |
| TI-002 | Niagara | 사용 중 | EvalGame.uproject 의 Plugins |

## 만든 방법과 검색 기록
시험용으로 손으로 적은 목록이다.
EOF

cat > EvalGame.uproject <<'EOF'
{
	"FileVersion": 3,
	"EngineAssociation": "5.6",
	"Modules": [
		{ "Name": "EvalGame", "Type": "Runtime", "LoadingPhase": "Default" }
	],
	"Plugins": [
		{ "Name": "GameplayAbilities", "Enabled": true },
		{ "Name": "Niagara", "Enabled": true }
	]
}
EOF

cat > Source/EvalGame/EvalGame.Build.cs <<'EOF'
using UnrealBuildTool;

public class EvalGame : ModuleRules
{
	public EvalGame(ReadOnlyTargetRules Target) : base(Target)
	{
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "GameplayAbilities", "GameplayTags", "GameplayTasks" });
	}
}
EOF

cat > Source/EvalGame/Combat/SkillCooldown.cpp <<'EOF'
// 스킬 쿨다운을 자체 타이머로 처리한다. 스킬 발동은 GAS 의 능력(GameplayAbility)으로 한다.
#include "SkillCooldown.h"

void USkillCooldownComponent::StartCooldown(FName SkillId, float Seconds)
{
	CooldownEnds.Add(SkillId, GetWorld()->GetTimeSeconds() + Seconds);
}

bool USkillCooldownComponent::IsReady(FName SkillId) const
{
	const float* End = CooldownEnds.Find(SkillId);
	return End == nullptr || GetWorld()->GetTimeSeconds() >= *End;
}
EOF
