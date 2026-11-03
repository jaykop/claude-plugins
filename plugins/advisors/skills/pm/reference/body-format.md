# PM advisor report body formats

The report head and the common sections follow `shared/report-base.md`. Below are the formats for each mode that go in the "Body" place. Attach the calculation command or the source next to every number.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## next — Next task

```markdown
### Time available today (오늘 쓸 수 있는 시간)
<value> — source (user (사용자) / profile pm.capacity (프로필 pm.capacity) / pm.capacity_file)

### Candidates (후보)
| Kind (종류) | Candidate (후보) | Why now (왜 지금인가) | Size (규모) | Evidence (근거) |
|---|---|---|---|---|
| Issue (이슈) | #N title | order rank 1, must | M | pm_calc issues output |
| Due check (때가 된 점검) | PC-002 Performance periodic check | 3 days overdue | - | pm_calc cadence |
| Risk decision (위험 결정) | PR-003 | 2 days left to Decide by | - | pm_calc risks |
| Debt decision (부채 결정) | TD-B-004 | Decide by passed 1 day ago, td recommendation "pay off — next milestone" | - | pm_calc debts |
| Retrospective·plan (회고·계획) | Weekly check | last weekly check 8 days ago | - | |

### Recommendation (추천)
- Recommendation (추천): <one>. One or two lines of reason.
- Alternative (대안): <one>. Why it was not recommended.
- Hand off to (넘길 곳): for issue work, profile `pm.next_task_entry` (scope and today's slice decision); for an advisor check, that advisor's command.
```

The issue order is the label-based draft of `pm_calc.py issues`. Write that the order with prerequisites included and today's slice follow the result of the `pm.next_task_entry` skill.

## weekly — Weekly check

```markdown
### Against last week's plan (지난주 계획 대비)
| Planned work (계획한 일) | Result (결과) | Cause of delay (늦어진 원인) |
|---|---|---|

- Issues closed after the base date: N (pm_calc issues --since <last check date>)
- New issues: N

#### Issues that came in without a scope decision (범위 판단 없이 들어온 이슈)
| # | Title (제목) | Milestone (마일스톤) | Size (규모) | Must (필수) | Proposal (제안) |
|---|---|---|---|---|---|
| | | | | no (아니오) | confirm whether to keep it (그대로 둘지 확인) / candidate to move to the backlog (백로그로 옮길 후보) |
(If there are none, "none". Look for decision records in the Order change record of pm-plan.md and in scope reports)

### Milestone state (마일스톤 상태)
| Milestone (마일스톤) | Days left (남은 날) | Open must (열린 필수) | Must size (h) (필수 규모(h)) | Capacity in description (h) (설명의 용량(h)) | Plannable time in remaining period (h) (남은 기간 계획 가능 시간(h)) | Must ratio (필수 비율) | Verdict (판정) |
|---|---|---|---|---|---|---|---|
Verdict (판정): room (여유) / tight (빠듯함) (80% of the limit or more) / over (초과) — present scope reduction candidates

### Risks (위험)
- Risks whose Decide by has passed or is within 14 days: (pm_calc risks)
- New risk candidates: (found in this week's facts. Evidence required)

### Technical debt decision points (기술 부채 결정 시점)
| ID | Rank (순위) | Location (위치) | td recommendation (td 권고) | Decide by (결정 시점) | Alert (알림) |
|---|---|---|---|---|---|
(pm_calc debts. If N debts have an empty Decide by, propose the technical debt check)

### Periodic checks (정기 점검)
| ID | Check (점검) | State (상태) | Proposal (제안) |
|---|---|---|---|

### Short retrospective (짧은 회고)
- What went well (잘된 것):
- What went badly (안된 것):
- What to change next week (다음 주에 바꿀 것):

### Next week's plan (다음 주 계획)
| Order (순서) | Work (일) | Size (규모) | Why (왜) |
|---|---|---|---|
Total size <h> / next week's plannable time <h> (pm_calc capacity)
```

## milestone — Milestone plan

```markdown
### Goal and period (목표와 기간)
### Completion criteria (grade table) (완료 기준 (등급표))
| ID | Criterion (기준) | Grade (등급) | Check method (확인 방법) |
|---|---|---|---|

### Work to include (담을 일)
| Necessity (필수성) | Issue·task (이슈·작업) | Size (규모) | Prerequisite (선행) |
|---|---|---|---|
| A must (A 필수) | | | |
| B want (B 원함) | | | |
| C spare (C 여유) | | | |

### Capacity (용량)
Command, plannable time, must size sum, must ratio, verdict. If it is over the limit, the candidates to remove (from want and spare first) and the hours that each removal saves.

### Buckets by remaining milestone (남은 마일스톤별 통)
### Refit check (재정비 점검) (methods.md 4-5)
| Axis (축) | Level (수준) | Evidence (근거) | Work to add in this milestone (이번 마일스톤에 넣을 일) |
|---|---|---|---|

### Risks (top 3) (위험 (상위 3개))
For each risk, 2 to 3 responses and the Decide by.

### Periodic check schedule (정기 점검 일정)
The checks that run during this milestone, and their dates.
```

## retro — Milestone retrospective

```markdown
### Results against the plan (계획 대비 결과)
| Completion criterion (완료 기준) | Grade (등급) | Result (결과) | Evidence (근거) |
|---|---|---|---|

### Estimate against actual (추정 대비 실제)
| Size bucket (규모 칸) | Issue count (이슈 수) | Evidence of real time spent (실제 걸린 시간 근거) | Judgment (판단) |
|---|---|---|---|
If there is no data on real time, leave it as "no data" (자료 없음) and do not invent it.

### 5 things that went well / 5 things that went wrong (잘된 것 5 / 잘못된 것 5)
Mainly things that apply only to this project. Evidence for each item.

### Risk retrospective (위험 회고)
Resolved risks, risks that really happened (whether they were on the list or not), missed risks.

### What to carry into the next milestone (1 to 3) (다음 마일스톤에 옮길 것 (1~3개))
| What to change (바꿀 것) | Form moved into real work·rules (실제 작업·규칙으로 옮긴 형태) | Check method (확인 방법) |
|---|---|---|
```

## scope — Scope decision

```markdown
### Target (대상)
One sentence. What is to be added (or removed, or deferred).

### Schedule view judgment (일정 관점 판단)
| Question (질문) | Answer (답) | Evidence (근거) |
|---|---|---|
| Necessity (필수성) | A / B / C | milestone completion criterion MC-... |
| Size (규모) | S / M / L / unknown (timebox proposal) (모름(시간 상자 제안)) | |
| Must ratio if added (넣으면 필수 비율) | x% → y% | pm_calc capacity |
| Work pushed out (밀려나는 일) | | |
| New risks (새로 생기는 위험) | | |
| Cost of doing it later (늦게 하면 생기는 비용) | | |

### Proposal (제안)
One of add now (지금 넣기) / next milestone bucket (다음 마일스톤 통) / backlog (백로그) / do not add (넣지 않기), with its condition.

### Parts that need a design judgment (기획 판단이 필요한 부분)
Principle and fun judgments are the design advisor's work. The question IDs posted to the question inbox.

### Parts that need a technical judgment (기술 판단이 필요한 부분)
Feasibility and structure judgments are the td advisor's work. The question IDs posted to the question inbox. If there are none, "none".
```

## playtest — Playtest plan

```markdown
### What this test checks (이번 테스트로 확인할 것)
3 to 7 yes/no check items (methods.md 7-4). Include the items of the last test that must be looked at again.

### Participants and procedure (대상과 진행)
- Participants: who, how many, whether they see the game for the first time
- Build·device preparation check: installation, how many times you played it yourself, broken parts to block off
- Instruction sentences: one or two sentences
- Time: minutes
- Observation sheet columns: time (시각) / scene (장면) / what they did (한 일) / where they got stuck (막힘) / what they said (말한 것)

### After-test sentences (agreement scale) (끝난 뒤 문장 (동의 척도))
Only the experiences that this game aims for with its pillars. Sentences that include scene names.

### Where results go (결과를 받을 곳)
Location of the record files (profile design.playtest_records). When results come in, hand the interpretation to the design advisor and the schedule update to the next weekly check.
```
