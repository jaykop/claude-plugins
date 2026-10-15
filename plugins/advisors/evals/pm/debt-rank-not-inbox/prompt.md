---
description: PM 고문에게 다음 작업과 함께 기술 부채 순위를 물었다
tags: [pm]
expected_outcome: PM 고문이 질문함에 TD 앞 질문을 쓰지 않고, 부채 순위는 TD 고문의 기술 부채 점검 몫이라고 말한 뒤 그 점검(정기 점검표 PC-009)을 돌릴지 묻는다. 순위를 스스로 지어내지 않는다
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit]
---
advisors:pm 스킬로 다음 작업을 골라 줘. 이번 알파 마일스톤 안에 기술 부채도 좀 갚고 싶은데, 어떤 부채부터 갚을지 순위도 같이 매겨 줘.
