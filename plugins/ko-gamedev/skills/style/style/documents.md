<!-- ko-lint: ignore-file -->
# Design and technical document style

Based on corpus D: Korean design documents a game team wrote about its animation system. The same rules fit system design notes, tech docs, manuals and dev logs. Player-facing text and localization are out of scope.

## Reader

- Before you write, name the reader and what the reader already knows. This decides which terms you explain and how much background you give.
- Usual readers of a framework or tool project: a developer who uses the system in another project (knows the engine, not the system internals), a later maintainer who traces why something changed, and the person who makes a decision.
- When one document serves readers with different backgrounds, say at the top which sections each reader needs.

## Register

- Write plain declarative sentences: ~이다, ~한다. D has no ~니다 lines.
- Explanatory docs may talk to the reader the way D does: `~라고 생각하면 된다`, `~를 염두에 두자`, `~를 살펴보자`. Specs and reference pages state facts without them.
- The benefactive ~해 준다 is normal in Korean dev docs (D 22 for 해주). Do not remove it for style.
- Use glossary words. Write engine type names in English, as in comments: State Machine, Transition, Blend Space, Cached Pose, Montage, Actor. D writes them as loanwords (스테이트, 트랜지션, 블렌드 스페이스); this skill does not. Keep the concept words that D uses: 애디티브, 커브, 블렌드, 포즈. Do not write 상태 기계 or 전이.

## Structure

1. 개요: one short paragraph on what this part handles, then a list of its sub-parts with one line each.
2. One section per sub-part: what it does, how it is built, the values or curves that drive it.
3. Point at figures and code explicitly: `위 그림처럼`, `아래 코드에서`, `빨간색으로 표시한 부분`.
4. Close with what is left or what to watch: `나머지 작업`, `주의할 점`.

Inside each section:

- Open with the conclusion or result. Reasons, evidence and history follow it.
- A heading says what the section does or concludes. Add the verb or particle that it needs: `락온 타겟 전환하기`, `스폰 위치를 NavMesh에 맞추기`. Do not stack nouns: `타겟 및 전환 정보`.
- Introduce a figure, table, list or code block with one sentence before it that says what it shows. Markdown documents need no numbered captions.

## Terms

- At first use, give the Korean loanword or the Korean meaning together with the English: `보폭(Stride)`, `스트레이핑(Strafing)`, `마지막 타격(막타)`. After that, use one form.
- Write asset, node, class, curve and variable names exactly as in the project, in English: `YawOffset_FB 커브`, `bPivot 변수`.
- Short codes are fine once defined: `F, B, LF, RB` for directions.
- Expand an abbreviation at its first use, with the meaning it has in this document: `EQS(Environment Query System)`. Skip the expansion only for abbreviations that every reader of the document knows (UE, BP, AI). The same abbreviation can mean different things in different fields.

## Sentences and lists

- Parallel conditions or reasons: a list, or `첫째, 둘째`.
- Comparisons: a table.
- Steps a reader follows: a numbered list, in the order the reader performs them. A prerequisite comes before the step that needs it.
- 때문에 is the usual connective in D (56 per 1,000 lines against 32 for ~므로). Avoid long ~므로 chains.
- Do not list with the middle dot `·`. Use commas, `와/과`, or `/` (D writes `전/후/좌/우`).
- Keep facts and numbers exact. A design doc is read by people who will tune the values.
