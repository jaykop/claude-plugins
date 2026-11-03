# Technology trend advisor report body format

The whole report follows the head and the section order of `<플러그인 폴더>/shared/report-base.md`. This file decides what goes in the "## Body" place in it, and how the technology trend advisor fills the common sections.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## File name and title

| Mode | File | Title |
|---|---|---|
| Periodic check (`정기 점검`) | `<report_dir>/radar/<YYYY-MM-DD>-periodic.md` | `# Technology trend advisor periodic check — <YYYY-MM-DD>` (ko: `# 기술 동향 고문 정기 점검 — <YYYY-MM-DD>`) |
| Single-technology diagnosis (`단일 기술 진단`) | `<report_dir>/radar/<YYYY-MM-DD>-single.md` | `# Technology trend advisor single-technology diagnosis (<target>) — <YYYY-MM-DD>` (ko: `# 기술 동향 고문 단일 기술 진단(<대상>) — <YYYY-MM-DD>`) |

- In the mode part of the file name, use only the lowercase English `periodic` and `single`. Do not put in a Korean mode name (rules.md §12).
- The date is the writing date (system date). Do not put in the end of the target period or the dates of the posts covered.
- If the same mode runs twice on the same day, add `-2` to the end of the name.
- The `<target>` in the title of a single-technology diagnosis is used when the next diagnosis looks for the previous report. For the same technology, use the same name (the public name).

## How to fill the common sections

- **Scope** (head table): the mode, the target period (for a periodic check, from the date of the previous periodic check to today; for a single-technology diagnosis, item 4 of SKILL.md Step 0), the number of sources opened and the number that failed to open, whether the technology inventory was rebuilt or the existing inventory was used as is (if rebuilt, the reason the script gave), and the community channels (the auto channels read and the number of posts, failures to open and "blocked by the tool", and whether there were manual channel posts that the user gave). If collection was done in the main agent without subagents, write "collected by the main agent without agents" (에이전트 없이 메인에서 수집함).
- A single-technology diagnosis adds one "Collection" line to the scope. Format: `Collection: web primary sources <looked for — items not filled from records: … | not looked for — all filled from records> / community <read — conditions met C1·C2·C3 | not read (no condition met)> / records reused <SC-ID and original check date, report path:line | none>` (ko: `수집: 웹 1차 출처 <찾음 — 기록으로 채우지 못한 항목: …| 찾지 않음 — 기록으로 모두 채움> / 커뮤니티 <읽음 — 걸린 조건 C1·C2·C3 | 읽지 않음(조건 해당 없음)> / 재사용한 기록 <SC-ID 와 원래 확인일, 리포트 경로:줄 | 없음>`). From this line alone, a reader must be able to tell why the web was searched or community posts were read, or why not.
- **Previous report** (head table): the previous report of the same mode. For a single-technology diagnosis, the previous report whose title also has the same target. If there is none, "none".
- **Decisions needed**: in a periodic check, raise items only from body item 2 (changes to technologies we use now) and item 3 (technologies that fit the problems). Do not raise news in item 6 or community leads in item 7 (raise only leads that were confirmed with a primary source and moved to items 2 and 3). At most three. Each item: "<technology> — <recommendation level or response deadline> — <one-sentence reason> — Decision owner: <decision_owners.tech>" (ko: "<기술> — <추천도 또는 대응 기한> — <한 문장 이유> — 결정권자: <decision_owners.tech>"). If the user is not the decision owner, write it as a "reference option".
- **Changes since the previous report**: split into five kinds. Newly added items / items whose announcement stage went up / items whose recommendation level changed and the evidence for the change / items whose condition to revisit was met / items withdrawn, dropped, or renamed. Also write here the changes in technology inventory states ("States changed from the previous inventory" (직전 목록과 달라진 상태) that the script printed).
- **Not checked**: sources that failed to open, failed searches, empty profile values, turn-off reasons that could not be checked, an engine modification block count that is "search failed", the number of community leads that could not be confirmed with a primary source, and unknown channel names. For each, what would make it possible to check.
- **Questions passed to other advisors**: the list of Q-IDs posted to the question inbox (`_state/inbox.md`).
- **Next check condition**: write the same value as the `Next check:` value in the head of `radar-watchlist.md`. Do not write the value of source-checks.md (the earliest recheck date) here.

## Periodic check body

```markdown
### 1. Baseline (기준)
- Our engine (우리 엔진): <version>, <source build or not>, engine modification blocks (엔진 수정 블록) <N or "search failed" (검색 실패)> (radar-inventory.md, updated (갱신) YYYY-MM-DD)
- Latest official engine version checked (확인한 최신 정식 엔진 버전): <version> (SC-xxx, <source URL>, checked (확인) YYYY-MM-DD)
- Development stage (개발 단계): <dev_stage> / Next milestone (다음 마일스톤): <next_milestone> / Target platforms (대상 플랫폼): <platforms> (profile updated (프로필 갱신) YYYY-MM-DD)

### 2. Changes to technologies we use now (지금 쓰는 기술의 변화)
| TI | Technology (기술) | Our state (우리 상태) | What changed (바뀐 점) | Original quote (원문 인용) | Impact on us (우리 영향) | Response deadline (대응 기한) | Source (출처) |
|---|---|---|---|---|---|---|---|
| TI-012 | <name> | in use (사용 중) | planned deprecation (폐기 예정) | "<original>" | N files (search expression '...') | <removal version stated by the source; if none, "no stated deadline" (밝힌 기한 없음)> | <URL>, checked YYYY-MM-DD |

If there is no change, write "No change in the checked scope — N sources checked" (확인한 범위에서 변화 없음 — 확인한 출처 N개) (the source list is in Appendix A).

### 3. Technologies that fit the problems (문제에 맞는 기술)
#### 3.<n> <technology name> (<explanation of the English term at first use>)
- Problem (문제): P-<n> <one-line problem> (Source (출처): <ticket, design document path, question inbox ID, what the user said>)
- Area (분야): <engine | graphics and animation | network | development tools and AI | platform>
- What it is (무엇인가): <two or three sentences>
- Announcement stage (발표 단계): <①~⑦> — "<primary original quote>" (<URL>)
- Dates (날짜): announced (발표) <YYYY-MM-DD | announcement date unknown> / released (출시) <version, date | not released> / checked (확인) <YYYY-MM-DD>
- Our state (우리 상태): <one of the five> (<TI-ID or search evidence>)
- Applicability (적용 가능성): <possible | conditional | not possible> — <reason and the conditions needed>
- Necessity (필요성): <problem confirmed | problem expected | no problem> — <evidence link>
- Community leads (커뮤니티 실마리): <# list from item 7; if none, "none">. This is the path by which the candidate was found, not evidence for the verdict
- Cost (비용): version difference (버전 차이) <>, overlapping engine modification blocks (겹치는 엔진 수정 블록) <N>(<folder>), affected files (영향 파일) <N>(<search expression>), assets to save again (다시 저장할 에셋) <scope>, affected job roles (영향 직군) <>, way to roll back (되돌리는 방법) <>
- Recommendation level (추천도): **<adopt | trial | assess | hold | already in use | verdict withheld — not confirmed>** — cap rules applied (걸린 상한 규칙): <list of L numbers or "none">
- Trial plan (시험 계획) (only for trial): scope (범위) <>, duration (기간) <to be decided>, success criteria (성공 기준) <metric and target — perf Q-xxxx>, how to turn it off (끄는 방법) <>
- Condition to revisit (다시 볼 조건): <event | date>
- Questions passed (넘긴 질문): <Q-ID, receiving advisor>

If the problem list is empty, write "No problem to solve is registered" (풀어야 할 문제가 등록되지 않음), and give one line on how to register problems (profile radar.interests, other advisors' reports, the question inbox, a user request).

### 4. Blockers when upgrading to the next version (다음 버전으로 올릴 때 걸리는 것)
Show only the rows added or whose status changed in this run, and write that the full table is in radar-watchlist.md.
| UP | Ours → next version (우리 → 다음 버전) | Blocker (걸리는 것) | Kind (종류) | Evidence on our side (우리 쪽 근거) | Source (출처) | Status (상태) |
|---|---|---|---|---|---|---|
If the next version is the same as our version, "not applicable — we are on the latest official version (SC-xxx)" (해당 없음 — 우리가 최신 정식 버전(SC-xxx)).

### 5. AI for development tools (개발 도구용 AI)
If the policy (radar.ai_tool_policy) is unchecked, one line: "AI for development tools — policy check needed (N items held)" (개발 도구용 AI — 정책 확인 필요(N건 보류)). If it is confirmed, write in the format of item 3, and write prices only as "public price as of the check date" (확인일 기준 공개 가격).

### 6. News that connects to no problem (문제와 이어지지 않는 소식)
- <technology> — <announcement stage and a short quote> — <URL>, published (발행) <YYYY-MM-DD>
- <post title> — <channel name>, community post (커뮤니티 글) — <URL>, posted (작성) <YYYY-MM-DD>
(One line each. Do not rate them.)

### 7. Community leads (커뮤니티에서 찾은 실마리)
| # | Channel (채널) | Post title (글 제목) | URL | Date (날짜) | Original quote (원문 인용) | Primary confirmation result (1차 확인 결과) | Sent to (보낸 곳) |
|---|---|---|---|---|---|---|---|
| 1 | qiita | <title> | <URL> | posted (작성) YYYY-MM-DD | "<original>" (translation (번역): <in the report language>) | confirmed (확인함) — <primary source URL>, checked YYYY-MM-DD | ① TI-012 |
| 2 | provided by the user (reddit) (ko: 사용자 제공(reddit)) | <title> | <URL the user gave, or "none"> | posted (작성) YYYY-MM-DD | "<original>" | not checked (확인 못 함) — <primary sources looked at and the result> | kept as a lead only (실마리로만 둠) |

- Put only leads for ① and candidates for ② in this table. A post sent to ③ needs only one line in item 6.
- If the original quote is Japanese or Chinese, add a translation into the report language after the original. For Korean and English posts, write only the original.
- The primary confirmation result is one of four: confirmed (확인함) (primary source and check date) / disagrees (어긋남) (the primary source says something different; write both) / not checked (확인 못 함) (places looked at and the result) / original is primary (원문이 1차) (the original that the post linked was official material).
- Sent to is one of ① TI-ID, ② 3.<n>, or "kept as a lead only" (실마리로만 둠). What could not be confirmed with a primary source is "kept as a lead only".
- If there were no community posts at all, write "N channels read, no relevant posts" (읽은 채널 N개, 해당 글 없음). If a channel could not be opened, write that in "Not checked".

### Appendix A. Source list (부록 A. 출처 목록)
| # | Title (제목) | URL | Source kind (출처 종류) | Publish date (발행일) | Check date (확인일) | Opened (열림) |
|---|---|---|---|---|---|---|

### Appendix B. Content from memory — not evidence (부록 B. 기억에서 나온 내용 — 근거 아님)
- <content>
```

## Single-technology diagnosis body

```markdown
### 1. Question (질문)
- Question (질문): "Can <technology> solve our <problem>?" or "If we upgrade to <version>, what blocks us and what do we gain?" (ko: "<기술>로 우리의 <문제>를 풀 수 있는가" or "<버전>으로 올리면 무엇이 걸리고 무엇을 얻는가")
- Target type (대상 종류): technology (기술) | engine version (엔진 버전)
- Problem source (문제 출처): <ticket, design document, perf report, question inbox ID, what the user said | no problem (문제 없음)>
- Tracking ID (추적 ID): <TW-xxx; if newly created, write so>

### 2. Facts on our side (우리 쪽 사실)
| # | Fact (사실) | Location (위치) | Evidence type (근거 종류) |
|---|---|---|---|
(technology inventory state, reason turned off, related code scope and search expression, modification block count of the related engine folders)

### 3. The technology according to primary sources (1차 출처로 본 기술)
| Version (버전) | What changed (바뀐 점) | Original quote of the announcement stage (발표 단계 원문 인용) | Scope-limiting wording (범위 한정 문구) | Source (출처) |
|---|---|---|---|---|
- Supported platforms (지원 플랫폼): <mark and source for each platform; unconfirmed ones as "unconfirmed" (미확인)>
- Shipped cases (출시 사례): <game, source, whether shipped, measurement conditions, whether the team size is disclosed>
- Known problems (알려진 문제): <only what was checked again with primary or secondary sources. What was seen only in communities goes to Appendix C>

### 4. Verdict (판정)
| Column (칸) | Value (값) | Evidence (근거) |
|---|---|---|
| Announcement stage (발표 단계) | | |
| Applicability (적용 가능성) | | |
| Necessity (필요성) | | |
| Recommendation level (추천도) | | Cap rules applied (걸린 상한 규칙): |

### 5. Cost and risk (비용과 위험)
(in the units of verdict-rules.md §6)

### 6. Trial plan (시험 계획)
(only when the recommendation level is trial. verdict-rules.md §8)

### 7. Engine version checklist result (엔진 버전 점검표 결과)
(only when the target type is engine version. The table in upgrade-checklist.md)

### 8. Condition to revisit (다시 볼 조건)

### Appendix A. Source list (부록 A. 출처 목록)
### Appendix B. Content from memory — not evidence (부록 B. 기억에서 나온 내용 — 근거 아님)
### Appendix C. Community leads (부록 C. 커뮤니티에서 찾은 실마리)
(The same table as item 7 of the periodic check body. The sent-to column is "raised as a known problem" (알려진 문제로 올림) or "kept as a lead only" (실마리로만 둠). If community posts were not read, one line: "not read (no condition met)" (읽지 않음(조건 해당 없음)))
```

## Writing style

- Write declarative sentences (in a Korean report, the plain ~한다 form). Do not use the polite 해요체 form. Only follow-up proposals given in the conversation end as a question ("~할까요?").
- Explain the meaning of an English term the first time it appears.
- Do not use a setting name or a class name as the subject of an explanatory sentence. Write what that setting actually changes, and put the name in parentheses or in the evidence column.
