# radar-watchlist.md format

File: `<report_dir>/_state/radar-watchlist.md`. Only the technology trend advisor writes it. The TD advisor reads the status of the "Blockers when upgrading to the next version" table and the tracking rows (if you change the columns, also update the td documents as the head of shared/state-formats.md says). Update it at the end of every periodic check and single-technology diagnosis. In the "Written by:" field of the head, write `radar`, the same as the folder name, instead of the advisor name.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

```markdown
# Technology watchlist (기술 추적 목록)

Next check: YYYY-MM-DD
Written by: radar / Last updated: YYYY-MM-DD / Base revision: <CL or commit>

## Technologies being tracked (추적 중인 기술)
| ID | Technology (기술) | Area (분야) | Our state (우리 상태) | Announcement stage (발표 단계) | Current recommendation level (현재 추천도) | Cap rules applied (걸린 상한 규칙) | Related problem (관련 문제) | Condition to revisit (다시 볼 조건) | Last check date (마지막 확인일) | Evidence report (근거 리포트) |
|---|---|---|---|---|---|---|---|---|---|---|
| TW-001 | <public technology name> | graphics and animation (그래픽스·애니메이션) | none (없음) (per the technology inventory) | ④ "<short original quote>" | assess (검토) | L1, L4 | none (없음) | Beta or higher in the next engine release notes | YYYY-MM-DD | radar/YYYY-MM-DD-periodic.md |

## Blockers when upgrading to the next version (다음 버전으로 올릴 때 걸리는 것)
| ID | First recorded (처음 적은 날) | Ours → next version (우리 → 다음 버전) | Blocker (걸리는 것) | Kind (종류) | Evidence on our side (우리 쪽 근거) | Source (출처) | Status (상태) | Last check date (마지막 확인일) |
|---|---|---|---|---|---|---|---|---|
| UP-001 | YYYY-MM-DD | 5.a.b → 5.c | <API or feature that changes> | API change (API 변경) | TI-012, search expression '...' result N files | <release notes URL> | open (열림) | YYYY-MM-DD |

## Change log (바뀐 기록)
| Date (날짜) | ID | What changed (바뀐 것) | Evidence (근거) |
|---|---|---|---|
| YYYY-MM-DD | TW-001 | assess → trial (검토 → 시험) | perf measurement report <path>, primary source <URL> |

## Project plugins confirmed as public outside products (공개 외부 제품으로 확인된 프로젝트 플러그인)
| TI | Plugin (플러그인) | Vendor and public product name (공급사와 공개 제품 이름) | Confirmed by and how (확인한 사람·방법) | Check date (확인일) |
|---|---|---|---|---|
| TI-031 | <folder name> | <vendor> <product name> | confirmed by the user (conversation) (사용자 확인(대화)) | YYYY-MM-DD |
```

## Column rules

- **ID**: `TW-` followed by three digits for tracked technologies, and `UP-` followed by three digits for the next-version table. Do not reuse a number once it is given.
- **Technology**: the public name. If the name changes at the official release, write "new name (old name)" and keep the ID.
- **Our state**: one of the five states of the technology inventory. If the technology inventory has a row for it, write the TI-ID with it. If it is "in the engine but off" (엔진에 있으나 꺼짐) and you found the reason it was turned off, append "reason turned off: <one sentence> (<evidence location or 'confirmed by the user'>, YYYY-MM-DD)" (끈 이유: <한 문장> (<근거 위치 또는 '사용자 확인'>, YYYY-MM-DD)). The next run uses this reason without looking for it again. If the line of that plugin in the project file changed ("States changed from the previous inventory" (직전 목록과 달라진 상태) in the technology inventory), look for it again.
- **Public outside product table**: put in only the outside vendor products in the project Plugins folder that the user confirmed. Only products in this table can be searched on the web by vendor name (sources.md §9). If the user says it is not one, do not put it in. If you could not ask (unattended), do not put it in.
- **Announcement stage**: the number in verdict-rules.md §1 and a short original quote from a primary source.
- **Current recommendation level**: adopt (도입) / trial (시험) / assess (검토) / hold (보류) / already in use (이미 사용 중) / verdict withheld — not confirmed (판단 보류-확인 부족) / closed (종료). Do not delete it. When there is no longer a need to watch it, change it to "closed — <reason>" (종료 — <이유>).
- **Related problem**: the problem number in the report that gave that verdict, and its source (ticket, design document path, question inbox ID). If there is none, "none" (없음).
- **Condition to revisit**: write an event. Use a date only when there is no event.
- **Kind** (next-version table): planned deprecation or removal (폐기 예정·제거) / API change (API 변경) / maturity change (성숙도 변화) / engine modification block overlap (엔진 수정 블록 겹침) / platform (플랫폼) / outside vendor plugin (외부 공급사 플러그인).
- **Status** (next-version table): open (열림) / resolved (해소됨) / not applicable (해당 없음). Do not delete a row even when it is resolved.

## Update rules

- Change the recommendation level only when there is a new source or a new fact on our side, and when you change it, add one line to "Change log".
- In every periodic check, check each "Condition to revisit". If a condition is met, put that row in "Changes since the previous report" of the report and rate it again.
- The "next version" is the latest official engine version recorded in source-checks.md. If it is the same as our engine version, do not add new rows to the next-version table.
- Change the `Next check:` line in the head to today + the periodic check interval (default 30 days, or the schedule's interval if there is a schedule) only when a periodic check ends. A single-technology diagnosis does not change this line (only when the file is created for the first time, today + 30 days). Calculate dates with `date`.
