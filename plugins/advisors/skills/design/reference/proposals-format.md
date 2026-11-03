# Proposal record format — `_state/design-proposals.md`

Only the design advisor writes and reads this record. It exists to track the status of the proposals that the advisor made, and to avoid proposing an already rejected idea again.
Read it in Step 0, and update it in Step Final.

## Principle of not making a new ledger

If the project has design tools that it already uses (profile `design.existing_tools`), do not write here again the work that those tools take.

| Role of the existing tool | What to write in this file | What not to write |
|---|---|---|
| 관찰 포인트 게시 (observation point posting) | The proposal ID and the mark "passed on as a verification candidate" (검증 후보로 넘김) | The verification plan body (keep it in the report only as candidates in that tool's format) |
| 피드백 정리 (feedback summary) | A one-line summary of the verification result and the location of that output | The original feedback text, and the cause analysis, effort, and effect estimates of the summary document |
| 수치 분석 (numeric analysis) | The location of the quoted result | Reproducing the calculation |

If there is no such tool, put the verification method directly in the "Verification plan" entry.

## File format

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

```markdown
# Design proposal record (기획 제안 기록)

Next check: 14 days before milestone        (or: Next check: Condition — a new playtest record appears or the next milestone date is set)
Written by: design / Last updated: YYYY-MM-DD / Base revision: <CL or commit>

## Proposals (제안)
| ID | First proposed (처음 낸 날) | Kind (종류) | Area / target (영역·대상) | One-line summary (input → rule → result) (한 줄 요약 (입력 → 규칙 → 결과)) | Status (상태) | Status changed (상태 바뀐 날) | Status evidence (상태 근거) | Revival condition (되살릴 조건) | Report (리포트) |
|---|---|---|---|---|---|---|---|---|---|
| DP-0001 | YYYY-MM-DD | on hold | Missions / supply crate | … | on hold | YYYY-MM-DD | user confirmed (conversation) | if … is observed in 3-player co-op records | design/YYYY-MM-DD-area.md |

## Verification results (검증 결과)
| Proposal ID (제안 ID) | Checked (확인한 날) | Success and failure directions written in advance (미리 적은 성공·실패 방향) | Observation (관찰) | Result (결과) | Evidence grade (근거 등급) | Source (출처) |
|---|---|---|---|---|---|---|

## Prediction hit record (예측 적중 기록)
| Period (기간) | Right (맞음) | Wrong (틀림) | Cannot judge (판단 불가) | Evidence grade that the wrong proposals relied on (틀린 제안이 기댄 근거 등급) |
|---|---|---|---|---|

## Verification plan (only when there is no existing observation tool) (검증 계획 (기존 관찰 도구가 없을 때만))
### DP-0003
- Observation scene (관찰 장면):
- Observation signal (관찰 신호):
- Success / failure (성공 / 실패):
- Conditions (조건):
- Measurement means (측정 수단):

## Idea notes (not raised as proposals because they did not meet the minimum conditions) (아이디어 메모 (최소 조건을 채우지 못해 제안으로 올리지 않은 것))
| Date (날짜) | Idea (input → rule → result) (아이디어 (입력 → 규칙 → 결과)) | Condition not met (못 채운 조건) | Source (출처) |
|---|---|---|---|
```

## Column rules

- **ID**: `DP-` followed by a four-digit number. Never delete or reuse an ID once it is given. If the name changes, keep the ID.
- **Kind (종류)**: add (추가) / modify numbers (수정(수치)) / modify structure (수정(구조)) / on hold (보류) / recommend removal (제거 권고) / merge (통합)
- **Status (상태)**: one of five.

  | Status (상태) | Meaning |
  |---|---|
  | proposed (제안) | The advisor made it and it is not decided yet |
  | adopted (채택) | The decision owner decided to proceed |
  | rejected (기각) | The decision owner decided not to do it. Write the rejection reason in "Status evidence" as the original text |
  | on hold (보류) | The decision owner decided to postpone it. "Revival condition" is required |
  | in verification (검증 중) | After adoption, it is being checked with playtests |

- **Status evidence (상태 근거)**: who decided it and where. Write it like `user confirmed (conversation)` (`사용자 확인(대화)`) or `decision owner record <document location>` (`결정권자 기록 <문서 위치>`).

## Update rules

1. Always add a new proposal with the "proposed" status.
2. Change the status to "adopted", "rejected", "on hold", or "in verification" only in the following two cases.
   - The user said in this conversation that they decided so. If the user is not the decision owner, write "decision owner's decision heard secondhand" (결정권자 결정을 전해 들음).
   - You can quote a document that records the decision owner's decision.
   The advisor does not change a status by its own judgment.
3. In an unattended run, do not change statuses. Only add new proposals, record verification results, and add idea notes.
4. Record a verification result as right / wrong / cannot judge by comparing the observation with the success and failure directions written in advance. If the observation is only [observed-opinion], "cannot judge" is the default, and write right or wrong only when it was repeated in different builds.
5. For a wrong proposal, write in "Prediction hit record" which evidence grade the wrong judgment relied on. In the next verdicts, use evidence of that grade more carefully.
6. If an idea that is the same as or similar to a rejected idea comes in again, do not propose it again unless you quote the rejection reason and write what changed since then.
7. Set the `Next check:` line (`다음 점검:` in a Korean file) of the head as described in "The Next check line of the head" below. The design advisor does not do scheduled checks, so only the session start notice reads this line.

## The Next check line of the head

The session start notice script (`scripts/due_check.py`) turns `Next check: N days before milestone` (`다음 점검: 마일스톤 N일 전`) into the date that is N days before the date in profile `next_milestone`, and notifies from that day. The condition form does not do a date comparison.

| Case | Line to write |
|---|---|
| `next_milestone` has a date (YYYY-MM-DD) | `Next check: 14 days before milestone` (`다음 점검: 마일스톤 14일 전`) |
| `next_milestone` has no date | `Next check: Condition — a new playtest record appears or the next milestone date is set` (`다음 점검: 조건 — 새 플레이테스트 기록이 생기거나 다음 마일스톤 날짜가 정해졌을 때`) |

- If the milestone date has already passed, write "the date in profile next_milestone has passed" (프로필 next_milestone 의 날짜가 지났음) in "Not checked" of the report.
- The notice script notifies from the day that is 14 days before the milestone date. But if the `Last updated` in the head is on or after that day, it does not notify. So even if today is already on or after that day, use the milestone form, and this run is handled as the check before that milestone. Do not calculate the date yourself.
