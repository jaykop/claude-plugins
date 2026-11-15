<!-- ko-lint: ignore-file, prose-lint: ignore-file -->
# Glossary format and evidence

The glossary is a set of Markdown tables. `scripts/prose_lint.py` reads every table that has `Use` and `Avoid` columns, so the tables are both the reference and the lint rules. The format is the same as ko-gamedev:style's glossary, with one more column, `Base`.

| File | Area |
|---|---|
| [words.md](words.md) | Catch-all verbs, metaphor verbs for plot logic, vague nouns, childish or wrongly paired verb phrases |

## Columns

| Column | Meaning |
|---|---|
| Use | The words to write. Several words separated by commas are all acceptable; pick by meaning. The note says which meaning takes which word. |
| Avoid | Surface forms to find. A plain form matches only when no Hangul syllable is right before it, and matches as a prefix, so write stems (넘기 matches 넘기고, 넘기면). A form written as `` `re:...` `` is a Python regex; write a pipe inside it as `\|`. |
| Kind | `review`: often an AI habit, sometimes right; read the sentence. `density`: fine once, a problem when it repeats; the lint lists the lines only when the file's rate is 3 times `Base` or more, with at least 3 hits. `replace`: almost always wrong in story prose (no row uses it yet). `term`: reference only, not linted. |
| Base | The book rate for the Avoid forms: the higher of N and E below, per 1,000,000 Hangul syllables, measured with the lint's own matching (quoted text skipped). `—` when the books have no hit. |
| Evidence | Rates per 1,000,000 Hangul syllables in the AI documents (K1, K2, K3) and the books (N, E). `K1 3 hits` gives a raw count where the rate would mislead. |
| Note | Which meaning takes which Use word, and what not to change. |

## Evidence

Snapshot taken 2026-11-15. Counts are outside quotation marks, because quoted text in a story document is usually a character's line or a coined term.

| Code | Corpus |
|---|---|
| K1 | Planning documents for a Korean crime-thriller visual novel, written by an AI agent (Claude) in November 2026: a pitch and a concept document in two versions. About 23,000 Hangul syllables. The user who asked for this skill judged them unreadable. Not public; do not quote. |
| K2 | Planning documents for a short mystery visual novel by the same kind of agent: concept, characters, plot, scenes, clues, story bible. About 20,000 Hangul syllables. Not public. |
| K3 | Two AI-written game design documents for a shop-management game. About 5,000 Hangul syllables. Not public. |
| N | 31 novels written in Korean, 1990s to 2020s, literary and genre: 김영하 (3), 정유정 (5), 박완서, 한강 (2), 김훈 (3), 천명관 (2), 황석영, 이영도, 김호연, 손원평, 김려령, 이미예, 김금희, 신경숙, 은희경, 공한K, 김초엽, 천선란, and three anthologies of Korean thriller and horror short stories. About 4.0 million Hangul syllables outside quotes. |
| E | Nonfiction written in Korean: 33 writing, editing and story-craft books by Korean authors (among them 김정선 『동사의 맛』, 박일환 『어휘 늘리는 법』, 정희모·이재성 『글쓰기의 전략』, 홍지운 『시나리오 레시피』, 이진희 『게임 시나리오 기획자의 생각법』, the 웹소설 작가를 위한 장르 가이드 series) and four books of Korean film writing (오기환 『스토리 흥행하는 글쓰기』, 『혼자서 본 영화』, 『영화가 내 몸을 지나간 후』, 『한국사 영화관』). About 2.9 million Hangul syllables outside quotes. Translated books are left out of N and E, because translation has its own habits. |
| P | Professional story introductions, measured by sentence features rather than words: the character introductions in 『나의 아저씨 1』 and 『미생 1』, the writers' notes in 『박쥐』 and 『친절한 금자씨』 screenplay books, and plot summaries in three books of Korean film criticism. |
| G | Rule sources, cited by book and chapter: 『동사의 맛』, 『어휘 늘리는 법』, 『우리말 어휘력 사전』(박영수), 『맹랑한 국어사전 탐방기』, 『문장의 조건』, 『글쓰기의 전략』, 『위반하는 글쓰기』, 『10일 안에 쓰고 100일 동안 고친다』, 『쓰기의 공식, 프렙』, 『프로작가의 탐나는 글쓰기』, 『스토리 흥행하는 글쓰기』, 『마음을 낚는 이야기꾼 웹소설 작가되기』, 『웹소설 작가를 위한 장르 가이드』 3, 5, 10, 『편집자처럼 책을 보고 책을 쓰다』, 『작가를 위한 집필 안내서』, 『서사 패턴 959』. |

K is small. A rate built on 3 to 10 hits shows a direction, not a precise ratio. A row was added only when the form is several times more frequent in K than in both N and E, in both K1 and K2 where the note does not say otherwise, and when the books show what writers use instead.

No sentence from any book is copied into this skill. Examples are written for the skill.

## Project terms file

A project can add rows and silence built-in rows in `.claude/ko-gamedev/prose-terms.md` at the project root. The lint loads it automatically when run from the project root, or with `--terms <file>`. It is a separate file from ko-gamedev:style's `terms.md`, because the two skills pull words in different directions: style turns 넘긴다 into 전달한다 for code, while prose asks which of five meanings 넘긴다 has in a story.

```markdown
# Project prose terms

| Use | Avoid | Kind | Base | Evidence | Note |
|---|---|---|---|---|---|
| 의뢰 | 주문 | review | — | team | In this story an "order" is always a disguised job request. |

| Allow | Note |
|---|---|
| 몫 | The gang's cut is called 몫 in the story's own slang. |
```

The project file wins over this glossary when they conflict. `Allow` forms are never reported.

## Adding a row

- Measure first: the form's rate in an AI-written story document and in books, with the same matching. Write both in Evidence and the book rate in Base.
- Prefer `review` and `density`. Most of these words are right somewhere.
- Keep forms narrow. A form that matches inside common words floods the lint; use `re:` with a lookahead.
- Run the lint on an AI-written document and on a book chapter before and after, and compare the totals.
