# TD advisor report body format

The whole report follows the head and the section order of `<플러그인 폴더>/shared/report-base.md`. This file sets what to put in the "## Body" place inside it, and how the TD advisor fills the common sections.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## File name and title

| Mode | File | Title |
|---|---|---|
| Design review | `<report_dir>/td/<YYYY-MM-DD>-decision.md` | `# TD advisor design review (<target>) — <YYYY-MM-DD>` (`ko`: `# TD 고문 설계 검토(<대상>) — <YYYY-MM-DD>`) |
| Structure audit | `<report_dir>/td/<YYYY-MM-DD>-audit.md` | `# TD advisor structure audit (<scope>) — <YYYY-MM-DD>` (`ko`: `# TD 고문 구조 점검(<범위>) — <YYYY-MM-DD>`) |

- For the mode part of the file name, use only the lowercase English words `decision` and `audit` (rules.md §12).
- The date is the writing date (system date). If you run the same mode twice on the same day, add `-2` at the end.
- The `<target>` in the title is a shortened form of the question and the decision record ID. Example: `design review (monster action selection structure, TD-D-003)` (`ko`: `설계 검토(몬스터 행동 선택 구조, TD-D-003)`). The next run tells the previous report apart by the ID when it looks for it.

## How to fill the common sections

- **Scope** (head table): the mode, the question kind or the audit scope, the target code scope (paths), the decision record ID, the number of materials read and not read, the needed marks ("no profile" (프로필 없음), "collected in the main agent without agents" (에이전트 없이 메인에서 수집함), "reference option" (참고 선택지)), and one line on outside material. Write the outside material line as one of the following.
  - `Outside material: not searched on the web (no condition applies)` (`ko`: `바깥 자료: 웹에서 찾지 않음(조건 해당 없음)`)
  - `Outside material: looked for primary sources once under the W2·W3 conditions` (`ko`: `바깥 자료: W2·W3 조건으로 1차 출처를 한 번 찾음`)
  - `Outside material: not searched on the web (W2 applies — banned search terms empty, passed to radar Q-xxxx | no profile — ask the technology trend advisor after making a profile)` (`ko`: `바깥 자료: 웹에서 찾지 않음(W2 걸림 — 검색 금지어 비어 있음, radar Q-xxxx 로 넘김 | 프로필 없음 — 프로필을 만든 뒤 기술 동향 고문에게 물을 것)`)
  - If you reused records, append them at the end, like `reused records SC-004 (checked 2026-10-13)` (`ko`: `재사용한 기록 SC-004(확인 2026-10-13)`).
- **Decisions needed**: at most three. For each item: "<what to decide> — <conclusion and condition> — <one-sentence evidence> — decision owner: <decision_owners.tech>" (`ko`: "<결정할 것> — <결론과 조건> — <한 문장 근거> — 결정권자: <decision_owners.tech>"). Also put here unconfirmed requirements, adding scenarios, confirming layer rules, waiting for outside checks, and team rule changes.
- **Changes since the previous report**: conclusions that changed and the evidence for the change (the location of the new fact), new options, options that are gone, and rows whose debt rank changed.
- **Not checked**: material not read (including Blueprint assets), failed searches and script exit code 3, empty profile values, modules not checked because their kind is unknown, modules whose includes cannot be counted, what remains as an execution order estimate or a connection estimate, and questions that wait for an answer. For each one, what would make it possible to check.
- **Next check condition**: for a design review and a module dependency audit, write the same value as the `Next check:` line at the top of td-ledger.md. For a technical debt audit, write the value at the top of td-debt.md. For an engine modification audit, write the value at the top of td-engine-mods.md. For a coding rule audit and an agent verifiability audit, it is "no schedule — when the user asks" (예약 없음 — 사용자가 요청할 때).

## Design review body

```markdown
### 1. Question (질문)
- Question (질문): <the user's question, copied without shortening it>
- Kind (종류): choice comparison (선택 비교) / new structure design (새 구조 설계) / structure problem (구조 문제) / feature feasibility (기능 타당성) / shift impact (전환 영향)
- Target code scope (대상 코드 범위): <path list>
- Decision record (결정 기록): TD-D-<number> (if you made it new, write so)

### 2. Requirements (요구)
| R | Requirement (요구) | Source (출처) | Grade (등급) |
|---|---|---|---|
| R-1 | <requirement sentence> | <design document path:line / ticket / team document / what the user said> | confirmed (확인함) / estimated (추정) / requirement not confirmed (요구 미확인) |

### 3. Current structure (지금 구조)
| # | Fact (사실) | Location (위치) | Static check (정적 확인) / execution order estimate (실행 순서 추정) / connection estimate (연결 추정) | Evidence (근거) |
|---|---|---|---|---|
(entry points, places that write the state, network role branches, mechanisms that set the execution order within the same frame. For new structure design, the existing structure to attach to)
- Related team rules (관련 팀 규칙): <rule sentence and location>
- Previous decision (지난 결정): <conclusion and status of TD-D-xxx; if there is none, "none" (없음)>
- Precedent (선례): <places that already solved the same problem, and how; if there is none, "none" (없음)>

### 4. Option comparison (선택지 비교)
| Column (칸) | Option 0 (안0) <keep the current approach (지금 방식 유지) / put it as is on the existing structure (기존 구조에 그대로 얹기)> | Option 1 (안1) <name> | Option 2 (안2) <name> (added by the advisor (고문이 더함)) |
|---|---|---|---|
| What it does (하는 일) | | | |
| Requirements met (요구 충족) | R-1 met [code] ... | | |
| Changed scope (바뀌는 범위) | none | files N, modules N (search pattern '...') | partly counted — <reason> |
| Engine behavior evidence (엔진 동작 근거) | | [engine] <path:line> | |
| Risk (위험) | | | |
| Performance (성능) | | not measured — perf Q-xxxx | |
| Reversal (되돌리기) | - | 2 | 4 |
| Ongoing cost (계속 드는 비용) | | | |
| Maturity risk (성숙도 위험) | | | |
| Team sharing needed (팀 공유 필요) | | | |

### 5. Conclusion (결론)
- Cause verdict (원인 판정; structure problem only) or feasibility verdict (가능성 판정; feature feasibility only): <value and evidence>
- Reason to change (바꿀 이유): <the item of choice-rules.md §5 and the evidence location; if there is none, "no confirmed reason to change" (확인된 바꿀 이유 없음). For new structure design, "not applicable — comparison of requirements met" (해당 없음 — 요구 충족 비교)>
- Conclusion (결론): **<recommend — if condition X, option A | decide after a trial | keep as is | judgment on hold — not enough confirmation (reason)>** — cap rules applied (걸린 상한 규칙): <list of T numbers, or "none" (없음)>
- If it is wrong, the reason (틀렸다면 그 이유): 1. <…> 2. <…> (rebuttal result (반박 결과): <rebutted with evidence (근거로 반박함) / could not rebut, lowered by one level (반박 못 해 한 단계 내림)>)
- Information that would reverse the judgment (판단을 뒤집을 정보): <…>
- Decision owner (결정권자): <decision_owners.tech> (if it is not the user, "reference option" (참고 선택지))

For a shift impact question, instead of the conclusion, write an "affected places table" (영향받는 곳 표) (| Affected place (영향받는 곳) | Changed scope (바뀌는 범위) | Risk (위험) | Evidence (근거) |), and put whether to do it in "Decisions needed".

### 6. Trial implementation spec (시험 구현 명세)
(Only when the conclusion is "decide after a trial". The columns of choice-rules.md §9)

### 7. Outside material (바깥 자료)
| Condition (조건) | Fact (사실) | Source (출처) | Check date (확인일) | Reused record or not (재사용한 기록인지) |
|---|---|---|---|---|
(If you did not look on the web, copy the outside material line of "Scope" in the head as it is)

### Appendix A. Search log (부록 A. 검색 기록)
(the scope, patterns, result counts, whether a search failed, and the search queries used, as returned by analyst and web-scout)

### Appendix B. Content from memory — not evidence (부록 B. 기억에서 나온 내용 — 근거 아님)
- <content>
```

## Structure audit body

After the head, write only the one section that matches the scope.

**Module dependencies**
```markdown
### 1. Basis (기준)
- N modules, N edges (N between project modules), N lines not parsed or only partly parsed, N excluded modules — module_graph.py <arguments>, exit code <0 | 3>
- Layer rules (층 규칙): final (확정) (<team document location>) / draft (초안) (--layer-draft)

### 2. Results by classification (분류별 결과)
| # | Classification (분류) | Depending module → depended-on module (의존하는 모듈 → 의존 대상 모듈) | Dependency kind and condition (의존 종류·조건) | Location (위치) | Where it is used (쓰는 곳; analyst) | Verdict (판정) |
|---|---|---|---|---|---|---|

### 3. Headers with the most includes (include 가 많은 헤더)
(top N of the module_graph.py result)

### 4. Layer rules (층 규칙)
| TD-L | Layer (층) | Modules (모듈) | Source (출처) | Status (상태) |
|---|---|---|---|---|
```

**Engine modifications**
```markdown
### 1. Basis (기준)
- The start and end marker rules, the folders counted, the block count per folder (by list), the number of blocks whose pairs do not match, skipped files — tech_inventory.py <arguments>
- The vanilla engine folder used for comparison and its version (Build.version), and its relation to our version (same (같음) / newer version (더 새 버전))

### 2. Group table (묶음 표)
| TD-E | Group (묶음) | Engine area (block count) (엔진 영역(블록 수)) | Block count (블록 수) | File count (파일 수) | Total line count (줄 수 합) | Classification (분류) | Evidence (근거) | Merge risk evidence (머지 위험 근거; only countable things) |
|---|---|---|---|---|---|---|---|---|

### 3. Block counts by classification and engine area (분류별·엔진 영역별 블록 수)
(count by the path of each block)
| Classification (분류) | Runtime (런타임) | Editor (에디터) | Tool program (도구 프로그램) | Plugin (플러그인) | Shader (셰이더) | Other (그 밖) |
|---|---|---|---|---|---|---|

### 4. Rule violation candidates (규칙 위반 후보)
| Rule (규칙; team document location) | Check method (검사 방법) | Blocks caught (걸린 블록 수) | Location (위치) |
|---|---|---|---|
```

**Technical debt**
```markdown
### 1. Where it was collected (모은 곳)
(count per source, and the places that could not be read)

### 2. Debt table (부채 표)
| Rank (순위) | TD-B | Kind (종류) | Location (위치) | Evidence numbers and command (근거 수치와 명령) | Payoff scope (갚는 범위) | Recommendation (권고) | Decide by (결정 시점) | Status (상태) |
|---|---|---|---|---|---|---|---|---|
```

**Coding rules**
```markdown
### 1. Area and collected material (영역과 모은 자료)

### 2. Rule candidates (규칙 후보)
| # | Rule (규칙) | Reason and evidence location (이유와 근거 위치) | Examples that follow / examples that break (따른 예 / 어긴 예) (file:line, count) | Automatic check (자동 검사) | In team documents (팀 문서에 있음) | Status (상태) |
|---|---|---|---|---|---|---|
| 1 | | | | search pattern '...' (검색식 '...') / a person must check (사람이 봐야 함) | yes (예) / no (아니오) | draft (초안) |
```

**Agent verifiability**
```markdown
### 1. Basis (기준)
- Target scope (paths), excluded paths, seeded random number path (the value in the criteria table / no set path (정한 경로 없음))
- Frame interval settings (reference) (프레임 간격 설정(참고)): <values and locations of bUseFixedFrameRate·FixedFrameRate·bSubstepping>
- Team rules on agent runs (에이전트 실행에 관한 팀 규칙): <clause and location / none (없음)>

### 2. Axis table (축 표)
| Axis (축) | Verdict (판정) | Evidence numbers and search patterns (근거 수치와 검색식) | Location (위치) | Not checked (확인 못 한 것) |
|---|---|---|---|---|
| 1. Random number path (난수 경로) | complete (갖춤) / partial (일부) / none (없음) / unknown (모름) | global random calls N (search pattern '...'), streams N (count per seed source) | | Blueprint random nodes |
| 2. State reproduction (상태 재현) | | | | |
| 3. Text output (텍스트 출력) | | | | |
| 4. Control without recompiling (재컴파일 없는 조작) | | | | |
| 5. Separation of numeric values into data (수치의 데이터 분리) | | | | |
| 6. Automated tests (자동 시험) | | | | |

### 3. Gap ranking (빈 곳 순위)
| Rank (순위) | Axis (축) | Gap (빈 곳) | Location (위치) | Changed scope (바뀌는 범위) | Recommendation (권고; if condition X, option A (조건 X 면 안 A) / accept (받아들임)) | Team rules (팀 규칙) |
|---|---|---|---|---|---|---|

### 4. Items for a person to check (사람이 볼 항목)
(things that search cannot tell apart, such as numbers written directly inside functions, Blueprint random nodes, and the impact when the frame interval is not fixed)
```

## Writing style

- Write in plain declarative sentences. In a Korean report, use the plain form (~한다), and do not use the polite form (해요체). Only the follow-up proposals given in the conversation end with "~할까요?" ("Shall I ...?").
- Explain the meaning of a technical term (in a Korean report, an English term) the first time it appears.
- Do not use a class or function name as the subject of an explanatory sentence. Write what that code actually does, and put the name in parentheses or in the evidence column.
