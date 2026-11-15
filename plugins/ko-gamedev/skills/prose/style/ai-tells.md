<!-- ko-lint: ignore-file, prose-lint: ignore-file -->
# Signs of AI-written Korean story prose

What separates the AI-written planning documents (K1, K2) from Korean books (N, E) and professional story introductions (P). Corpus codes: [../glossary/README.md](../glossary/README.md#evidence). The K1 numbers come from its pitch, the document its reader called unreadable: world section (19 sentences), cast list (15), events (96). Small samples; read them as directions.

The short version: AI Korean states facts one after another in the same flat form, hides whose reasoning each sentence is, and names everything with a few native words that each carry several meanings. A reader cannot tell what follows from what, and the words feel like a children's book written by a lawyer.

## Linking

Two kinds of numbers: P and K1 come from morphological analysis (kiwipiepy) of the professional introductions and the K1 pitch; "lint" numbers come from `prose_lint.py` itself, on all of N and E and on the K1 pitch, so they match what the lint prints. Do not compare across the two kinds.

| Sign | Books and P | AI | Fix |
|---|---|---|---|
| Sentences that open with a connective (그런데, 하지만, 그래서, 그러던 어느 날) | P 5 to 14% of sentences. Lint: N 51, E 85 per 1,000 | K1 events 1%. Lint: K1 pitch 17, K2 16 per 1,000 | Mark the turns. [sentences.md](sentences.md) S2 |
| Turn connectives at the start (그런데, 하지만, 그러나, 그러던) | P 1.4 to 8.5% | K1 0% | The reader cannot see which event turns the story |
| 하지만 or 그러나 anywhere | N 805, E 1030 per 1M syllables | K 318 | |
| Reason and purpose markers (때문, 위해, 려고, 탓, 덕분) | P 9 to 15 per 100 sentences | K1 5.2; 0 in the cast list | Attach the reason to the person who has it. S3 |
| A present-tense rule built on ~라야 or two -면 conditions, with no thinking verb or reason marker (lint `owner`) | Lint: N 1.1, E 7.6 per 1,000 (how-to books state rules in their own voice) | Lint: K1 pitch 25 per 1,000; the three hits are the sentences a fresh reader could not place | Give the reasoning an owner. S3 |
| Conditional -면 | P 3.5 to 6.2 per 100 sentences. Lint: N 6.2, E 13.6 | K1 16 to 18. Lint: K1 pitch 16 | Plot logic proven by bare conditions. S3 |
| -고 joins | P 21 to 50 per 100 sentences. Lint: N 33, E 29 | K1 55 to 74. Lint: K1 pitch 57 | -고 joins facts with no relation. S2 |
| Sentences that open with a date or a weekday | P about 1%. Lint: N 0.3%, E 0.8% | K1 21%. Lint: K1 pitch 14% | A police log. Mark time only where the story turns. S6 |
| Sentences whose first word is the subject | P 13 to 27% | K1 42 to 47% | Every sentence starts a new actor. Take up the last sentence's new information. S4 |
| Paragraph length | P 4 to 7.7 sentences | K1 8.7 on average, up to 14 | One point per paragraph. S1 |
| Linked sentences in paragraphs of 4+ sentences (lint `linked`) | Lint: N 0.33, E 0.44 | Lint: K1 0.27, K2 0.38 | A weak sign: K2 is in the book range. S2 |

Adding a connective to every sentence is the opposite AI habit. Three of the writing guides tell writers to cut connective adverbs. The fix is the relation, written with a connective ending (-아서, -니까, -려고, -지만, -는데) or a reason predicate (때문이다); a connective adverb only at the turns.

## Words

| Sign | Books and P | AI | Fix |
|---|---|---|---|
| Verb variety (verb types / verb tokens, same length) | P 0.51 to 0.55 | K1 0.39 | A few verbs carry many meanings: 넘기다 for assign, hand over, sacrifice, report and get through. [../glossary/words.md](../glossary/words.md) |
| Noun variety, and the top 10 nouns' share of all nouns | P 0.56 to 0.57; 11 to 12% | K1 0.30; 26% | The same few names repeat in every sentence because nothing is described |
| 하다 verbs and adjectives (조사하다, 누설하다, 정중하다) | P 5.7 to 9.1 per 100 eojeol | K1 2.3 to 3.2 | AI avoids the precise Sino-Korean action verb and reaches for a native verb with five meanings. [words.md](words.md) W2 |
| Adjectives in character introductions | P 3.7 to 5.2 per 100 eojeol | K1 cast list 0 | A character line with a job and a goal, and nothing about the person. [introductions.md](introductions.md) I3 |
| Adverbs | P 4.4 to 8.6 per 100 eojeol | K1 2.3 | |
| Catch-all verbs (넘기다, 안다, 본다, 둔다, 원하다, 잃다) | N and E rates in words.md | 6 to 30 times the book rate, in both K1 and K2 | words.md, catch-all verbs |
| Metaphor verbs for plot logic (무너지다, 남다, 드러나다, 이어지다, 흘리다, 기대다) | | 5 to 70 times | words.md, metaphor verbs |
| Short nouns with several meanings (자리, 일, 몫, 줄, 손, 철, 셈) | per 1,000 sentences: 자리 6 to 10, 몫 0 to 1, 셈 1 to 3 | K pitches: 자리 34, 몫 29, 셈 15 | words.md, vague nouns |
| Quotation marks around coined terms | P 6 to 9 per 100 sentences | K1 world section 52.6 | Too many invented names before the reader has a person to follow. I4 |
| Registers mixed in one paragraph | P keeps one register per piece | K1 puts 감찰, 진술 조서, 연대보증인 next to 분다, 샜다, 손이 없으니 | Pick one register. W5 |

## Reasoning with no owner

The clearest sign, and the one the user could not read. A planning document explains why each character acts. AI writes those reasons as general present-tense statements between the events, with no person attached:

- 진짜 장부가 있는 조직이라야 검찰에서 무너지지 않는다.
- 증인을 겁주면 서장이 바로 의심한다.
- 기한 직전이라야 서장이 캐 볼 틈이 없다.

Each is one character's calculation. Read without the author's head, it is the narrator stating a law of the world, and the reader cannot tell whose plan is being described or whether it is true. Fix: [sentences.md](sentences.md) S3.

## What not to over-correct

- The target is not Sino-Korean. Replacing every native word with a Sino-Korean one gives 공문서체, the opposite failure. The test is whether the word narrows to one meaning and whether people in that field use it ([words.md](words.md) W1).
- Idioms stay: 단속을 넘긴다 (get through), 몫을 나눠 준다 (split shares), 정보를 흘린다 (once), 몸을 사린다, 눈감아 준다, 남의 손을 빌린다.
- Do not announce every reason with a frame (이렇게 따진다, ~라는 것이 X의 계산이다). Fixing "no owner" this way swaps one mechanical pattern for another ([sentences.md](sentences.md) S3).
- Do not add a connective to every sentence. Do not turn every short sentence into a long one: short sentences are fine when they are related, and P uses many.
- Present tense for the story's now is the norm in synopses and pitches. Only the time before the story starts goes to the past tense.
- A character's quoted line keeps the character's words, wrong pairings and all, if the character would say it. The lint skips quoted text for this reason.
- Do not add literary color (비유, 꾸밈말) to a planning document. Plain and exact is the register.
