<!-- ko-lint: ignore-file -->
# Design and technical document style

Based on corpus D: Korean design documents a game team wrote about its animation system. The same rules fit system design notes, tech docs, manuals and dev logs. Player-facing text and localization are out of scope.

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

## Terms

- At first use, give the Korean loanword or the Korean meaning together with the English: `보폭(Stride)`, `스트레이핑(Strafing)`, `마지막 타격(막타)`. After that, use one form.
- Write asset, node, class, curve and variable names exactly as in the project, in English: `YawOffset_FB 커브`, `bPivot 변수`.
- Short codes are fine once defined: `F, B, LF, RB` for directions.

## Sentences and lists

- Parallel conditions or reasons: a list, or `첫째, 둘째`.
- Comparisons: a table.
- Steps a reader follows: a numbered list.
- 때문에 is the usual connective in D (56 per 1,000 lines against 32 for ~므로). Avoid long ~므로 chains.
- Do not list with the middle dot `·`. Use commas, `와/과`, or `/` (D writes `전/후/좌/우`).
- Keep facts and numbers exact. A design doc is read by people who will tune the values.
