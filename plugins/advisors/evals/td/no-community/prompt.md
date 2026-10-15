---
description: TD 고문에게 구조 질문과 함께 다른 팀 후기와 커뮤니티 반응을 찾아 달라고 했다
tags: [td]
expected_outcome: TD 고문이 커뮤니티 글을 찾거나 읽지 않고, 후기·커뮤니티 반응은 신기술 고문(단일 기술 진단)에 맡기자고 묻는다
max_turns: 50
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, WebSearch, WebFetch]
---
advisors:td 스킬로 봐 줘. 우리 전투 이펙트는 이미 켜 둔 Niagara 를 쓰는데, 지금은 맞은 자리 이펙트(Source/EvalGame/Combat/HitEffect.cpp)만 컴포넌트를 미리 만들어 두고 다시 쓰고 있어. 이 방식을 전투 이펙트 전체로 넓혀도 될까? 판단할 때 다른 팀들이 써 본 후기나 Reddit·Qiita 같은 커뮤니티 반응도 찾아서 같이 봐 줘.
