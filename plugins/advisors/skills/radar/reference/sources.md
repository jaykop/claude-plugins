# Technology trend advisor source rules

This file holds only the rules for source kinds and reliability. Do not write here dated outside facts, such as the feature state of a specific version, event dates, or prices. Check such facts in every run and record them in `<report_dir>/_state/source-checks.md` with the check date.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 1. Source kinds

| Kind (종류) | What | Where it is used |
|---|---|---|
| primary (1차) | Material that the maker of the technology published directly. Official release notes (change history by version), official documentation, official blogs and news, original videos and slides of event presentations, public source repositories, papers | Evidence for the announcement stage, whether it is released, setting and class names, and supported platforms |
| primary (our tree) (1차(우리 트리)) | The plugin file marks and folder locations in the local engine tree. For a feature that is not a plugin (an engine feature turned on by a setting), the maturity text written in the console variable description or the header comment of the local source (path:line) | Evidence for "does it actually exist in our engine" in a source build. It takes priority over the release notes. Record the maturity text, but decide the announcement stage from the original wording of a primary source |
| secondary (2차) | Technical posts by other developers, event summary posts, reports in technical media, media that independently measured shipped games | Used to find shipped cases and actual measurement conditions. Compare summaries of facts against primary sources |
| tertiary (3차) | Forums, community boards (including the community channels in §10), social media, video tutorials, AI-generated summary sites, sites made for search exposure | Do not use them as evidence for verdicts. Use them only as leads to find what is a hot topic and what the known bugs or problems are, and confirm what you find again in primary and secondary sources |

Detailed rules:
- For papers, write separately whether it passed conference review or is a preprint. Also write whether the code is public and the license (whether it can be used only for research). If papers are the only evidence, the announcement stage is ①.
- Material that a hardware or SDK vendor published about its own product counts as primary only for release facts. Mark performance numbers as "vendor measurement" (공급사 측정).
- Official documentation of an AI model company (whether released, price, usage limits, retirement schedule) counts as primary. Mark benchmarks as "company's own measurement" (회사 자체 측정).
- An official forum answer marked as from staff of the engine developer counts as primary, but if it talks about a plan and not a release, the announcement stage does not go above ②.
- A roadmap page is a plan. Do not use it as evidence of release.

## 2. Reliability of shipped cases

For a shipped case from a secondary source, write three things separately.
1. Whether the presenter actually shipped a game with that technology
2. Whether the measurement conditions (hardware, resolution, scene) were disclosed
3. Whether the team size and the engine version were disclosed

If the team size was not disclosed, write "scale unknown" (규모 미상). A scale-unknown case gives at most "trial" as the recommendation level (verdict rule L5).

## 3. Dates

| Date (날짜) | Meaning | Caution |
|---|---|---|
| Announcement date (발표일) | The day it was first made public. The day the keynote or session was held | Do not mix it with the video upload date, the article date, or the document revision date. If unknown, "announcement date unknown" (발표일 미상) |
| Release (출시) | The released version and date | Read it from the release notes. If not released, "not released" (미출시) |
| Check date (확인일) | The day that source was opened in this run | System date (`date +%F`) |

- Write dates as YYYY-MM-DD. Do not write "recently", "a while ago", or "this year".
- Event schedules change every year. If you need an event date, check it on that year's official page and put it in source-checks.md.

## 4. How to write source-checks.md

Follow the source-checks.md part of `<플러그인 폴더>/shared/state-formats.md` for the format.

- **External facts table**: put in dated outside facts. Examples: the latest official engine version and its release date, the maturity mark of a feature used in a current verdict, model retirement schedules, public prices, event schedules.
- **Source access table**: write the access results of sources that failed to open and of community channels, with the method, the result, the check date, and the recheck date. The result is one of open (열림) / blocked (code) (막힘(코드)) / partial (부분) / blocked by the tool (도구가 막음). "Blocked by the tool" is the case where not the site but the web tool of Claude Code did not open that address, and the method column becomes "a person must export it" (사람이 내보내 줘야 함). Instruct the next run to look for the same fact in another primary source instead of the blocked source.
- Default **recheck date**: check date + 30 days. For an event schedule, the day after the event ends. For a retirement schedule, the earlier of 30 days before the retirement date and check date + 30 days. Rows of the access table are also check date + 30 days. Calculate dates with `date`.
- Write only one source in one row. If sources say different things, split the rows and write "disagrees with SC-xxx" (SC-xxx 와 어긋남) in the value column.
- For a fact that decides the announcement stage or supported platforms (a maturity mark such as Experimental, Beta, or production ready), copy the original sentence of the primary source into the value column in quotation marks, and also write the version and the wording that narrows the scope. If the original has no scope limit, write "no scope limit" (범위 한정 없음). This is so that the next run can still keep the original quote rule of verdict-rules.md §1 when it reuses this row.
- If you looked for a primary source but in the end there was none, write the source kind as "no primary source (not found)" (1차 없음(찾지 못함)), and write the places you looked in the value column. Until the recheck date, use it only as the fact that "there is no primary source" (the verdict is L7 or "verdict withheld — not confirmed").
- Reuse: use a row that meets the three conditions of rules.md §3 as evidence without opening the web again. Write the row ID and the original check date with it. Do not use rows that do not meet the conditions (secondary and tertiary, rows with mixed sources, rows where primary sources disagree, summaries without the original wording) as evidence. Pass them on as facts to recheck.
- A periodic check always opens again the "current latest official engine version and its release date" of R1 and the release notes since our version. It does not reuse them. This is so that a new version is not missed.
- A fact whose recheck date is today or earlier must be checked again before it is used as evidence. Put it in the collection instructions of the periodic check as a "fact to recheck". Put a channel whose date has passed in as a "channel to recheck".
- **Written by** column: this file is written together with market and td. Write radar for the rows the technology trend advisor newly writes. Do not delete rows that another advisor added. If you checked a row again, you can update the value, the source URL, the source kind, the check date, and the recheck date, and keep only "written by" as the advisor that first added the row (state-formats.md). The ID of a new row is the number after the largest number in the table.
- The `Next check:` line at the top is the earliest "recheck date" among all rows of the two tables (including other advisors' rows).

## 5. When the original cannot be opened

- If the original could not be opened because of 403, a login requirement, or a timeout, write "failed to open" (열기 실패). Do not fill in the content with search result summaries.
- If the web tool refused the address itself (errors such as "unable to fetch" or "not accessible"), write "blocked by the tool" (도구가 막음). Do not open the same site again through another address, a script, search result summaries, or a cache.
- Look for the same fact in another primary source. If it is not found in the end, that item is verdict rule L7 (only secondary evidence) or "verdict withheld — not confirmed".
- If sources say different things, write both and follow the primary source, but mark that they differ.

## 6. Content from memory

- Collect content that comes from training memory (for example, "I believe this feature was still experimental") separately in the report appendix "Content from memory — not evidence", and do not use it in verdicts.
- Use words such as "latest version", "currently supported", or "still experimental" only from a primary source opened in this run, or from a source-checks row that meets the reuse conditions of rules.md §3. When you use that row, write the row ID and the original check date with it.

## 7. Name confirmation

Write only setting names (CVars, console variables that change engine behavior), class, plugin, and module names whose existence you confirmed with a link to the official documentation or a path in the local engine source. If you could not confirm a name, write "name unconfirmed" (이름 미확인). Do not make up plausible names.

## 8. Performance numbers

Write performance numbers from the announcer with the source and the measurement conditions (hardware, resolution, scene), and mark them as "announcer's numbers" (발표 측 수치). Do not turn them into "it improves this much in our game". Write the effect on our side only as "not measured — perf measurement request Q-xxxx" (미측정 — perf 측정 요청 Q-xxxx).

## 9. Collection topics and search queries

**The five topics** — call web-scout once for each topic, in parallel. Leave out the areas in profile `radar.excluded`.

| Topic (주제) | What it covers |
|---|---|
| engine (엔진) | Engine release notes, version policy, build and tools, changes in the public source repository |
| graphics and animation (그래픽스·애니메이션) | Rendering, lighting, shadows, geometry, animation, physics presentation |
| network (네트워크) | Replication (state synchronization between server and client), online service integration, netcode |
| development tools and AI (개발 도구·AI) | Development tools, editor extensions, AI for development tools, in-game AI |
| platform (플랫폼) | Public SDKs, policies, and certification requirements of the target platforms (only what is public) |

**Search query rules**
- Build queries only from names of public technologies, products, and companies, official feature names of the engine, and general technical terms.
- Do not put in: profile `search_banned_terms`, the combinations in `search_banned_combos`, the project name, the names of plugins and modules whose location in the technology inventory is "project" (프로젝트), internal code names, sentences from design documents, ticket titles.
- Use engine plugin names only when the location in the evidence column of the technology inventory is "engine" (엔진) (these are names the engine published).
- Among the plugins whose location is "project", search for public products of outside vendors by the name the vendor published, only for the ones in the "Project plugins confirmed as public outside products" table of `radar-watchlist.md`. If a plugin is not in the table, do not search for it. Do not decide that a plugin is an outside product only from the creator name written in the plugin file (.uplugin). Put a plugin in the table only when the user confirmed it.
- Rewrite problems to solve into general technical terms before searching. Example: "넓은 숲 지역에서 그림자가 무겁다" (shadows are heavy in a wide forest area) in a design document → "shadow rendering cost dense foliage". If you turn a symptom into a specific technology name, you will find only that technology, so get technology names from the search results. Check once more that the rewritten query does not reveal internal matters.
- The words you put in the search queries, tags, and addresses of community channels (§10) follow these rules as they are. This is because the search conditions in tags and addresses are also sent to outside services.

## 10. Community channels

**Role**: the place to find what is a hot topic, and the experience and bug reports of people who actually used a technology. The source grade is tertiary (§1). Do not use them as evidence for verdicts, and confirm release and maturity again with primary sources. Do not raise the recommendation level above "assess" with content that comes only from communities (verdict-rules.md L12).

**When to read**: in a periodic check, read all auto channels. In a single-technology diagnosis, read them only when conditions C1~C3 of SKILL.md D3 apply, and only after D3 (primary source collection) returns. The TD advisor does not read community posts.

**Channels** — use the channel names below in profile `radar.community_sources`. auto is a channel read automatically, and manual is a channel read only when the user pastes posts or gives them as files.

| Channel name | Language of posts | How to read (address format) | Address for the access check | Access result checked once at writing time |
|---|---|---|---|---|
| qiita | Japanese | Public API `https://qiita.com/api/v2/items?query=tag:<태그>&per_page=<N>`. It returns the latest posts for each tag with the post date (`created_at`). Use public technology names as tags (for example `UnrealEngine`). `<N>` is the number of posts to get at once. Filter the target period with `created_at` | The address on the left with one tag | open |
| geeknews | Korean | The post list and item pages of `https://news.hada.io/`. It is a collection that introduces other posts, so each item has a link to the original. Follow the link and open the original, and quote from the original. To search by technology name, narrow the web search scope to this site | `https://news.hada.io/` | open |
| tencent-gameinstitute | Chinese | The latest post list of Tencent Game Institute `https://gameinstitute.qq.com/`. To search by technology name, narrow the web search scope to this site | `https://gameinstitute.qq.com/` | open |
| reddit | English | Do not read it automatically. Read it only when the user pastes posts or gives them as files | `https://www.reddit.com/` | blocked by the tool (both WebFetch and WebSearch refuse this site) |
| zhihu | Chinese | Do not read it automatically. Same as above | `https://www.zhihu.com/` | blocked (403) |

- The "Access result checked once at writing time" column is a value checked once when this file was written. It is not evidence for verdicts, and the value to follow in each run is the access table of `source-checks.md`. In the first run, open each channel again and write it in the access table (written by radar). For auto channels, the collection itself is the check. For manual channels, open the address for the access check once.
- At writing time, GameLook, a Chinese-language game development medium, was also tested, but the connection was refused (on the PC used for the test), so it was not added as a channel. If it opens in another environment, you can add a row to this table and use it.
- If the profile has a channel name that is not in this table, do not read it, and write it in "Not checked" of the report as "unknown channel name" (모르는 채널 이름).

**Reading rules**
- Treat posts found in channels as tertiary even if they are technical posts. If you opened the original that a post links, write that original separately by its own kind (primary if it is official documentation, secondary if it is a technical post by another developer).
- For Japanese and Chinese posts, write the original quote together with a translation into the report language. The translation helps reading. Keep numbers, versions, and announcement stages on the original side as evidence.
- Do not open a channel whose automatic lookup is blocked (access result "blocked" or "blocked by the tool") through another address, a script, search result summaries, or a cache. This is because the site or the tool blocked automatic collection. Use that channel only as manual. When the recheck date comes, open the address for the access check once with the same tool. Even if it opens, the user decides whether to move it to auto (in an unattended run, only write it in the report).
- For manual channels, read only the posts that the user pasted into the conversation or whose file path the user gave. In the source column, write "provided by the user (<channel name>)" (사용자 제공(<채널 이름>)), and the URL if the user gave one. Do not read them in an unattended run.
- For the post date of a post, use the date written on the page or in the API. Do not mix it with the access date.

**Where posts go in a periodic check**

| Content of the post | Where it goes | Primary confirmation |
|---|---|---|
| Problem and bug reports about a technology in the technology inventory (a technology we use now), problems that appeared after a version upgrade | ① a lead for changes to technologies we use now | Known issues in the release notes, the official issue tracker, official forum answers by staff of the engine developer. If confirmed, put it in the ① table with the primary source |
| A technology or user experience that connects to a problem to solve (P-n) | ② a candidate for technologies that fit the problems | Confirm the announcement stage and supported platforms with primary sources, then rate it by the verdict rules |
| Other topics | ③ one line of news that connects to no problem | Not done. Do not rate it |

Do not put leads and candidates not confirmed with a primary source into ① or ②. Keep them only in the "Community leads" table of the report, as "not confirmed with a primary source" (1차 확인 못 함).
