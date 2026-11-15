<!-- ko-lint: ignore-file, prose-lint: ignore-file -->
# Words

Words that AI-written Korean story documents use far more often than Korean books, and what to write instead. Columns, kinds, `Base` and the corpus codes K1, K2, K3, N, E: [README.md](README.md). Rates are per 1,000,000 Hangul syllables outside quotation marks, measured with the lint's own matching.

Choose by the three questions in [../style/words.md](../style/words.md): does the word narrow to one meaning here, does a person in that field call it this, does it fit an adult reader of a planning document. Native Korean or Sino-Korean is not the test.

## Catch-all verbs

One verb carries five meanings in one document. Give each meaning its own verb. These rows are `density`: the lint lists them only when a file uses the form at 3 times `Base` or more, at least 3 times.

| Use | Avoid | Kind | Base | Evidence | Note |
|---|---|---|---|---|---|
| 맡긴다, 건넨다, 넘겨준다 (사람), 내준다 (희생양), 고발한다, 제보한다, 버틴다 (기간) | 넘긴, 넘기, `re:(?<![가-힣])넘겨(?!주\|준\|줄\|줬)`, 넘길 | density | 68 | K1 2153, K2 395 / N 68, E 52 | Split by meaning: assign work 맡긴다; hand over an object 건넨다; hand a person to the police 넘겨준다; offer a scapegoat as an arrest record 내준다; report a crime 고발한다; get through a period 버틴다. 단속을 무사히 넘긴다 is idiomatic and can stay once. |
| 알고 있다, 전해 듣는다, 눈치챈다, 확인한다, 짐작한다 | `re:(?<![가-힣])안다(?![가-힣])` | density | 27 | K1 835, K2 346 / N 15, E 27 | Name how the person knows: heard, saw, guessed, was told. In a plot, the path of knowing is the point. |
| 확인한다, 목격한다, 판단한다, 여긴다, ~에 끌린다 | `re:(?<![가-힣])본다(?![가-힣])`, `re:(?<![가-힣])보고도(?![가-힣])` | density | 65 | K1 615, K2 445 / N 28, E 65 | 본다 stands in for check, witness, judge and be tempted by. In a script's narration, 본다 for a look on screen can stay. |
| 놓는다, 보관한다, 숨긴다, 맡겨 둔다 | `re:(?<![가-힣])둔다(?![가-힣])`, 두고 간, 두기로 | density | 9 | K1 264, K2 297 / N 4, E 9 | The auxiliary -어 둔다 (적어 둔다) is not matched. |
| 바란다, 노린다, ~고 싶어 한다 | 원하는, 원한다, 원하 | density | 224 | K1 439, K2 1976 / N 104, E 224 | 원하는 것 is the "want" column of a character sheet. In prose, say what the person is after: 노린다 for a target, 바란다 for a hope. |
| 노린다, 바란다, 목표다 | `re:(?<=[가-힣])려\s?(고\s)?한다` | density | 30 | see note | Fine once. Four characters in a row who each ~하려 한다 read like a template: 20 per 100 sentences in K1's character list, 0 to 2.6 in the professional introductions measured in [../style/ai-tells.md](../style/ai-tells.md). |
| 담당한다, 처리한다, 책임진다 | 맡는, 맡는다, 맡아 | density | 25 | K1 308, K2 99 / N 25, E 17 | 맡긴다 (assign a job) is the recommended word for one meaning of 넘긴다 and is not matched. |
| 위태로워진다, 빼앗긴다, 날린다, 걸려 있다 | 잃는, 잃는다, 잃을 | density | 20 | K1 439, K2 642 / N 16, E 20 | 잃을 것 is the English "stakes". Write what is at risk and how: 어머니의 전세 보증금이 날아간다. |

## Metaphor verbs for plot logic

AI explains why a plan works with body and building verbs: a case collapses, a trace remains, a line connects. Korean writers name the legal or practical result.

| Use | Avoid | Kind | Base | Evidence | Note |
|---|---|---|---|---|---|
| 기소가 어렵다, 혐의가 입증되지 않는다, 들통난다, 실패한다 | 무너지, 무너진, 무너뜨 | density | 39 | K1 703, K2 49 / N 39, E 29 | A wall or a person collapsing stays. |
| 기록된다, 의심을 산다, 흔적이 남는다 (once) | `re:(?<![가-힣])남는다`, 남지 않 | density | 27 | K1 571, K2 99 / N 13, E 27 | 빚만 남는다 (only the debt is left) is natural and can stay. |
| 밝혀진다, 알려진다, 탄로 난다, 들통난다 | 드러난, 드러나 | density | 69 | K1 571, K2 346 / N 46, E 69 | 들통난다 is colloquial: fine once in a crime story, but three in a page read as slang. |
| 연결된다, 관련이 밝혀진다, 수사가 ~까지 미친다 | 이어지, 잇는, 잇고 | density | 56 | K1 264, K2 247 / N 34, E 56 | |
| 누설한다 (처음 한 번), 알려 준다, 귀띔한다, 유출된다 | 흘린, 흘리, 흘려, 샜다 | density | 65 | K1 615 / N 65, E 28 | 정보를 흘린다 is a real idiom. The problem is repetition, and a light word for a crime: call it 수사 정보 누설 once. |
| ~에 달려 있다, ~에 의존한다 | 기댄다, `re:기대고(?= 있)` | review | 2.5 | K1 176 / N 2.5, E 0.7 | 결말이 이 지점에 기댄다 → 결말은 이 덫이 통하느냐에 달려 있다. A person leaning on a wall stays. |

## Vague nouns

Short nouns with several meanings. Pin the meaning with a compound or a modifier, or use the concept word. If the document already uses the word in another sense (자리 in 자릿세), change it.

| Use | Avoid | Kind | Base | Evidence | Note |
|---|---|---|---|---|---|
| 위치, 둔 곳, 장소; 직위 | `re:(?<![가-힣])자리(?!세\|잡\|에서 일어)` | density | 370 | K1 1318, K2 494 / N 370, E 164 | 돈궤 자리 → 돈궤를 둔 곳. 물건을 두고 갈 자리 → 물건을 넘겨받을 장소. |
| 의뢰, 범행, 작업, 사건 (name which) | `re:(?<![가-힣])일(?=[을이은도과])` | density | 879 | K1 1890, K2 939 / N 879, E 835 | One 일 is fine. Ten in a page hide which job is meant. |
| 의뢰, 일거리, 청부 | 일감 | density | 2.2 | K1 439, K3 214 / N 2.2, E 0 | |
| 상납금, 배당, 수당, 일당, 수수료 | 몫 | density | 24 | K1 791, K3 1925 / N 18, E 24 | 몫을 나눠 준다 (shares split among people) is correct. A cut paid to a gang is 상납금. |
| 연줄, 연고, 연결고리, 관련 | `re:(?<![가-힣])줄(도\|이\|은)\s*(없\|있)` | review | 1.4 | K1 88 / N 0.5, E 1.4 | 조직과 아무 줄도 없는 → 조직과 아무 연결고리도 없는. |
| 부릴 사람, 쓸 수단, 일손 | 손이 없 | review | 0.5 | K1 132 / N 0.5, E 0 | 남의 손을 빌린다 is an idiom and is not matched. |

## Reasoning frames

Frames that announce a calculation instead of attaching it to an action. They show up when a corrector gives reasons their owners mechanically. The books have almost none. Fold the reason into the action ([../style/sentences.md](../style/sentences.md) S3).

| Use | Avoid | Kind | Base | Evidence | Note |
|---|---|---|---|---|---|
| -려고, -니까, ~할까 봐, ~을 노리고 (in the action sentence) | 계산이다, 계산으로는, 계산이 있다 | review | 0.2 | N 0.2, E 0; first corrected test text 3 | 계산 as arithmetic stays. |
| (the reason itself, in the action sentence) | `re:(?<![가-힣])이렇게 (따진\|계산한\|판단한)`, `re:데는 (계산\|이유\|까닭)이 있다` | review | 0 | N 0, E 0 | |
| 그런데 ~할 길이 없다, ~가 걸린다 | `re:(?<![가-힣])남은 문제는` | review | 0 | N 0, E 0 | |
| 믿는다, 짐작한다, 여긴다 (vary), or fold | `re:[다라]고 판단한다` | density | 0.9 | N 0, E 0.9 | Fine once or twice. In every paragraph it reads like a report. |

## Third-person feelings

| Use | Avoid | Kind | Base | Evidence | Note |
|---|---|---|---|---|---|
| 싶어 한다, 두려워한다, 무서워한다, 싫어한다 | `re:(?<=[가-힣]) 싶다(?=[.,])`, `re:(?<![가-힣])(두렵\|무섭\|싫)다(?=[.,])` | review | — | both corrected test texts | Only in third-person documents. First-person narration and dialogue keep the bare form ([../style/sentences.md](../style/sentences.md) S12). |

## Childish or wrongly paired verb phrases

| Use | Avoid | Kind | Base | Evidence | Note |
|---|---|---|---|---|---|
| 따져 본다, 저울질한다, 계산한다 | 셈한, 셈하, 셈해 | review | 1.0 | K1 176 / N 1.0, E 0.3; 따지다 N 18, E 30 | 셈한다 is counting money. Weighing options is 저울질한다 or 따져 본다. A character's own line may keep it. |
| 빼돌린다, 훔쳐 온다, 절도 | 빼 오, 빼오 | review | 0 | K1 308 / N 0, E 0; 빼돌리다, 훔치다 N 33, E 30 | 물건 빼 오기 → 절도, 물건 빼돌리기. |
| 추궁한다, 조사한다, 뒤를 캔다, 탐문한다 | 캐묻, 캐물, `re:(?<![가-힣])캔다`, `re:(?<![가-힣])캐 ` | review | 9.4 | K1 308, K2 148 / N 9.4, E 1.0 | 캐묻다 takes a matter (사정, 행적), not a person: 보라를 캐묻는다 → 보라를 추궁한다. 캐다 takes 뒤, 정체, 비밀. |
| 물색한다, 점찍는다, 택한다 | 고른, 고르, 고를, 골라, 골랐 | review | 95 | K1 176, K2 198, K3 428 / N 54, E 95 | Finding a person who fits a plan is 물색한다. 고르게 (evenly) also matches; skip it. |
| 미끼를 던진다, 미끼를 놓는다 | `re:미끼를\s*(낸\|내)` | review | — | K1 3 hits / N 0, E 0 | 미끼 pairs with 던지다, 놓다, 물다. |
| 회선을 유지한다, 해지하지 않는다 | `re:(번호\|회선\|전화)[가를이을]?\s*(살려\|살아\|살린)` | review | — | K1 3 hits / N 0, E 0 | |
