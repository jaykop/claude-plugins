#!/usr/bin/env bash
# 시험용 프로젝트: TD 고문이 Step 0 에서 묻지 않도록 필요한 프로필 칸과 팀 규칙 문서를 두고,
# Niagara 가 "사용 중"인 기술 목록과 컴포넌트를 다시 쓰는 코드를 둔다.
set -eu

mkdir -p .claude/advisors/reports/_state Source/EvalGame/Combat Docs

cat > .claude/advisors/profile.md <<'EOF'
---
profile_version: 1
updated: 2026-10-01

project_name: EvalGame          # [사용자] 시험용 이름
genre: 3인칭 액션               # [사용자]
play_mode: 싱글                 # [사용자]
platforms: [PC-Steam]           # [사용자]
target_spec: 최저 GTX 1660, 권장 RTX 3070   # [사용자]
dev_stage: 본 제작              # [사용자]
next_milestone: 알파 2027-03-31 # [사용자]
team_size: 약 20명 [사용자]

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
  tech: 클라이언트 프로그래머(이 프로필을 쓰는 사람)   # [사용자]
user_role: 클라이언트 프로그래머   # [사용자]

report_dir: .claude/advisors/reports
share_scope: personal
stale_after_days: 90
code_change_entry:              # [사용자] 모름
search_banned_terms: []         # [사용자] 없음
search_banned_combos: []        # [사용자] 없음

td:
  rule_docs: [Docs/CodingRules.md]   # [사용자]
  record_roots: []              # [사용자] 없음
  extra_roots: []               # [사용자] 없음
  vanilla_engine_root:          # [사용자] 모름
  engine_base_ref:              # [사용자] 모름
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
| TI-001 | Niagara | 사용 중 | EvalGame.uproject 의 Plugins, Source/EvalGame/EvalGame.Build.cs |

## 만든 방법과 검색 기록
시험용으로 손으로 적은 목록이다.
EOF

cat > Docs/CodingRules.md <<'EOF'
# 코드 작성 규칙

1. 게임 코드에서 엔진 소스를 고치지 않는다. 엔진 기능으로 안 되면 게임 모듈에서 감싼다.
2. 전투 중 매 프레임 새 컴포넌트를 만들지 않는다. 미리 만들어 두고 다시 쓴다.
EOF

cat > EvalGame.uproject <<'EOF'
{
	"FileVersion": 3,
	"EngineAssociation": "5.6",
	"Modules": [
		{ "Name": "EvalGame", "Type": "Runtime", "LoadingPhase": "Default" }
	],
	"Plugins": [
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
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "Niagara" });
	}
}
EOF

cat > Source/EvalGame/Combat/HitEffect.cpp <<'EOF'
// 맞은 자리 이펙트. Niagara 컴포넌트를 미리 만들어 두고 돌려 쓴다.
#include "HitEffect.h"
#include "NiagaraComponent.h"

void UHitEffectPool::Init(UNiagaraSystem* System, int32 Count)
{
	for (int32 i = 0; i < Count; ++i)
	{
		UNiagaraComponent* Comp = NewObject<UNiagaraComponent>(GetOwner());
		Comp->SetAsset(System);
		Comp->RegisterComponent();
		Free.Add(Comp);
	}
}

UNiagaraComponent* UHitEffectPool::Spawn(const FVector& Location)
{
	if (Free.Num() == 0)
	{
		return nullptr;
	}
	UNiagaraComponent* Comp = Free.Pop();
	Comp->SetWorldLocation(Location);
	Comp->Activate(true);
	return Comp;
}
EOF
