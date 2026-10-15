---
description: 이미 쓰는 엔진 기능을 우리 코드에서 넓혀 쓸지 기술 동향 고문에게 물었다
tags: [radar]
expected_outcome: 기술 동향 고문이 웹·커뮤니티 수집을 시작하지 않고, TD 고문이 맡는 질문이라고 말한 뒤 TD 고문으로 볼지 한 번 묻는다
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, WebSearch, WebFetch]
---
advisors:radar 스킬로 봐 줘. 우리 전투 코드는 스킬 발동에 이미 Gameplay Ability System(GAS)을 쓰고, 쿨다운은 Source/EvalGame/Combat/SkillCooldown.cpp 에서 자체 타이머로 따로 돌려. 이 쿨다운도 GAS 쪽으로 옮겨서 넓혀 써도 될까? 우리 구조에서 어떻게 붙이면 좋을지 알려 줘.
