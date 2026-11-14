# Adaptation

For turning a source (a folktale, a classic, a novel, a webtoon, true events, an existing design document) into a game script. Fill the adaptation sheet in step 1 before the logline. Sources are in [sources.md](sources.md) under "Adaptation". Rules marked "estimate" are design choices for games, not findings from the sources.

## Two stages

1. Reduce the source to a medium-neutral summary: the list of events, the relationships between characters, the order in which information is revealed. No sentences or signature scenes from the source.
2. Design the game on top of it: choices, variables, images, box length, inner voice. Look for what the game can do that the source could not; do not just transcribe.

What moves from source to script is the structure (events, relations, reveal order), not the sentences.

## Adaptation sheet (step 1)

```markdown
# 각색 시트: <원작>

- 원작 종류와 권리: 설화·고전(공유 재료) / 현대 소설·웹툰(권리 필요: 허락 여부) / 실화 / 기획 문서
- 대상 독자: 원작을 아는 플레이어 / 처음 보는 플레이어
- 가져올 인물: <1단계 사건 사슬이 필요로 하는 인물만. 원작 인물을 모두 넣지 않는다. 빼는 인물과 이유>
- 원작의 핵심 한 줄: <사건과 관계 한 문장. 원작 문장 없이>
- 유지할 것 3개: <독자가 기억하는 사건, 관계, 장면의 기능. 이름이나 설정이 아니라 기능으로. 예: 세 번 반복되는 선택의 순간>
- 바꿀 것: | 무엇을 | 주제 / 인물 / 가치관 / 원인 중 | 이유 한 줄 |
- 지향점 한 줄: <원작의 무엇을 게임의 강점(속말, 선택지, 반복 플레이, 그림)으로 키우는가>
- 옮기는 구간과 시점 수: <긴 원작이면 어느 구간, 시점이 여럿이면 몇 개를 쓰는가>
- 이식 조건: <시대나 장소를 바꾸면 원작 갈등에 필요한 사회 조건(계급, 금기, 압박)이 새 배경에도 있는가>
- 게임이 못 하는 것 1개 이상 / 원작보다 잘하는 것 1개 이상:
- 장(章)을 장면으로: 원작 순서 유지 / 사건 시간순 재배열 (둘 중 하나)
- 원작 형식 장치(일기 날짜, 편지, 일지): 숨긴다(장면 id, 배경) / 드러낸다(날짜 지문, 편지 화면)
```

- For a long source (a serial, a webtoon, a design document with many episodes): list every episode in a table (length, characters, emotional function), rearrange it around the protagonist's arc (pull forward, enlarge, cut), then fill the empty cells (a character with nothing to do in a chapter) with new episodes. Write the concept and the scene list only after this.
- Keep: the ending points, the big turning events, the tone. Raising the stakes of the setting to give the protagonist a goal can kill the source's tone.
- Change freely: the reasons that link events and the characters' motives (make them come from character), new relationships grown from a one-line setting in the source, the opening (avoid a first scene that makes players expect the wrong genre), episodes whose weight pulls the story away from the protagonist (shrink them).
- Spend the box budget on the 3 things to keep first.
- If the ending type differs from the source, write the reason and how the theme changes. With branches, the source's ending can survive as one ending and the changed one as another (estimate).
- "I did not like the source's ending" is an allowed reason. If you change who performs an action, write how the meaning of the action changes.
- Do not assume the player read the source. Introduce the characters and their relationships in the first scene, unless the sheet says the target is source readers.
- Either keep the source's chapter order or rebuild in time order. A half-and-half version loses both the source's appeal and a new one.
- Changing the period or place: find the social condition the conflict needs first, then a period and place where it holds, then filter by production limits. Swapping only props and place names keeps nothing.
- A device dropped because it is dated (a birth secret) did a job (a twist, a motive, a spark of conflict). Write the job and give it to another device.
- Compressing a long source weakens motives that were built over many pages. Add one motive device if needed, and record whether it changes the ending or the theme.
- A source with several viewpoints: decide separately whether to keep the number of viewpoints and how to redistribute length. A section that revisits events from another viewpoint must bring new information. Switch viewpoints only at section boundaries and update the viewpoint declaration each time (estimate).

## Conversion rules

| Source element | In the game | Check |
|---|---|---|
| Inner narration | One narration line of action, prop, or sensation; if impossible, one inner-voice line | One line per paragraph of source? Inner voice not piled at the start of the scene? |
| A chapter | A scene | Order rule declared on the sheet |
| Long description of a place or person | Background image + one narration line | The line must not repeat what the image already shows. One line of what the image cannot show (sound, smell, time, a judgment) passes (estimate) |
| Narrator's commentary, satire, diary voice | Inner-voice lines, viewpoint declaration kept | Not turned into a direct sermon |
| Too many characters | Merge or cut | A merged character keeps one way of speaking; per-scene speaker limit |
| A long chain of events | Compress into one day or one place | Motive device added if compression weakened the motive |
| Heavy explanatory knowledge (science, institutions) | Only what the story needs, in one narration line | Only what the story cannot do without |
| A coincidence in the source | A character's motive, or the player's investigation or choice (estimate) | If every option leads to the same result, it is not a choice. Write why the source's inevitability was given up |
| Activities that are not visual (reading, writing letters, thinking) | Usable as they are; a VN is a text medium | The activity's value (power, voyeurism) shows in one scene, and it does not swell to 100 boxes |

Things a film solved with acting, camera, or a star's image must be redesigned in text and images in a VN.

## Failure patterns

1. Substitution: only props and place names change; the period's feeling, urgency, and events stay foreign.
2. Servility: the source's order and scenes are followed step for step; text is merely turned into pictures.
3. Halfway: neither keeps the source's form nor breaks it.
4. Lost spine: the few decisive events that moved readers were cut or shortened.
5. Assumed readers: gaps only source readers can follow; missing introductions.
6. Partial transplant without identity: the core (satire, tragedy) is dropped, the easy part kept, the source's name kept.
7. Against the aim: satire or metaphor covered over with direct statements and satisfying punishment, or strong material stacked with strong staging until the feeling hardens.
8. The fidelity shield: "faithful to the source" used in place of a reason for a change.
9. Compression without a new motive.
10. A device removed and its job left empty.
11. Copied sentences and signature scenes from the source.
12. Stock replacement: the source's specifics replaced with stock settings.

## Review questions (step 5 pass A, adaptations only)

1. Does each of the 3 things to keep survive in boxes? Which lines?
2. Does every change have a one-line reason, and can the reason be read in the script?
3. Does someone who does not know the source understand the relationships in the first scene?
4. Are there boxes written against the one-line aim?
5. If the viewpoint character changed from the source, was the viewpoint declaration updated? Does every revisiting section bring new information?
6. Could any inner-voice line taken from inner narration become one action line instead?
7. How many lines copy the source's sentences? (The target is zero for a source under copyright; a few at most for shared material.)
8. Does narration repeat what the background image already shows?
9. If a source coincidence became a choice, does each branch lead somewhere different?
10. If the ending type differs from the source, are the reason and the change of theme written?
11. Do the links between events come from the characters' natures, not from the plot's need?
12. Does any kept episode pull weight away from the protagonist's story?
13. Does the opening set the right genre expectation?

## By kind of source

- Folktale, classic: short and shared. Separate what to keep (the one-line theme) from what to overturn (relationships, values, causes). If the twist is large, do not lead with the source's name. Supernatural leftovers: cliche-check.md 9.
- Novel: inner life and time. The first two conversion rules carry most of the work.
- Webtoon, comic: metaphor, symbol, and omission are its language, and it has pictures. Where the source has few words, leave the empty space with one narration line and an image id; do not fill it with sermons (estimate).
- True events: the pressure to keep facts makes a halfway result likely. Write the line between fact and fiction on the sheet. Historical events: [genre-faction.md](genre-faction.md).
- An existing design document of the project: the sources say nothing direct. Use the sheet's first part only (core line, things to keep, things to change).
- Rights: a modern novel or webtoon needs permission. This is a production fact from the sources, not legal advice.
