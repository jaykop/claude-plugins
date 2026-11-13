# Anti-patterns and check questions

Check a screen plan or mockup with these questions before you show it to the user. Source marks are explained in [SKILL.md](../SKILL.md#sources). Cases marked `F` come from two visual novel prototypes that a user reviewed.

## Check questions

### Structure

1. How many large blocks of information does this screen show at once? If more than one, keep one as the focus and move the others to small markers or a hidden layer. (F; B p.130)
2. Can you name what the eye reads 1st, 2nd and 3rd? Do size, color, contrast and motion lead the eye in that order? (B p.106–108, p.130)
3. Are all the targets the player chooses from spread on the screen at once? If so, change to a category snap and one-at-a-time browsing. (F)
4. Does each choice start from the context (the line being read, the place where the player stands)? (F)
5. Is there a table that the game sorted for the player? If the sorting is part of the play, let the player record it. (F)
6. Is space shown on a map, or in a table or text? (F)
7. Does a number counter create the tension? Can a gauge with a meaning in the story replace it? (F)
8. Does the same information (a speaker's name, a value) appear in two places? (F)
9. Can you name a reference screen, with a source, for this screen structure? If you took only the mechanic, check the screen structure again. (F)
10. Did you add a step or screen that the user did not ask for? (F)
11. Is this a decision screen or a reading screen? Does a decision screen hold information that does not affect the decision (all stats, all relationships, logs)? (F; B p.132)
12. Can any text or number on the screen move to the detail layer? Did anything the decision needs move there by mistake? (F)
13. In a story scene, is any pixel of the management screen visible? Does every line have a background and a speaker image (or a planned no-speaker shot)? (F)
14. Is a value change shown with the same icon in the scene, on the result card, and on the hub gauge? Can the player read one turn's result without a log? (F)
15. In battle, is intent or a matchup explained with sentences? Can the intent display give false information? (F)

### Text, input, repetition

16. Does every text field have a length limit, and was the layout tried with the real text at that limit in the longest target language? (B p.67, p.109–110, p.186–187)
17. Can the player use this screen for the 100th time without pain: a skip for long effects, short distances between targets, a grid a d-pad can walk? (B p.138–139)
18. Does the screen work with each target input device (touch, mouse, pad)? Is any information reachable only by mouse hover? (F; B p.110–111, p.140–141)
19. Does any meaning depend on color alone? (B p.197–198)
20. Does the mockup state its focus and its completion level (D, C, B, A)? (B p.200)

## Patterns

| Pattern | Why it fails | Do instead | Case |
|---|---|---|---|
| A list or table of information presented as the UI | It is reading material with no act of choosing or comparing. Text grows | One item large, the rest as position markers | F: a notebook tab that listed every statement and its result as text |
| All targets and all evidence on one screen for matching | When the player sees everything, the player scans instead of thinking. The screen becomes a table | From the line being read, [Present] → browse evidence one by one | F: a pointing screen with 3 statement cards and 7 clue cards at once |
| Two-step choice where each step is a full list | 9 choice buttons pile up on one screen | Same as above | F: 6 sentences → 9 clues as choice buttons |
| Remaining tries shown as a number | Tension turns into arithmetic and loses the story | A gauge per character (patience) or a shared one (trust) | F: HUD "questions left 4, wrong 0/3" |
| A time × place table instead of a route | A route is movement through a building. A table is only an alibi sheet | The route of one character on a floor map, time one segment at a time | F: a route board as a grid |
| The game sorts the alibis | The game does the deduction for the player | A blank form that the player fills with stickers and notes | F: a board that marked claim, confirmed and lie |
| Speaker name twice, "X's testimony" title | The eye splits and space is lost | Name at the top left of the dialogue box, small reference info to its right | F: name tag at top left plus a box title |
| Only the reference game's mechanic | The screen falls back to a familiar list | Check the reference's screen structure (what is visible, how to move, how to choose) and keep the source | F: an analysis of mystery games that covered only their rules |
| An unrequested step | The plan grows and the user must cut it | Propose with a reason and ask | F: a final reconstruction puzzle the user removed |
| Route and time told only in narration | The player cannot look again | Map, time bar, player's own recording tool | F: a 5-minute sample scene |
| Reading material on a decision screen | The decision gets buried and the player scans the same data every turn | Keep what affects the decision, move the rest to a sub-screen | F: a schedule screen with 6 stat bars, 3 gauges, a map, a relationship chart, slots and a log |
| Every explanation and number always visible | Text covers the screen. Markers and explanations look equal | Markers on screen, reasons and numbers in the detail layer | F: a relationship panel that showed multipliers, next-scene conditions and change reasons for every character |
| A dialogue box over the dimmed hub as a "scene" | No background or characters, so it reads as a notice | Hide the hub in scenes and use the standard scene layout | F: an event shown as the engine dialogue box over the schedule screen |
| A change shown only as a corner toast | Easy to miss, and the reason is lost | Icon in the scene, result card, gauge animation | F: "+2 strength" toasts stacking on the map |
| Battle intent as sentences, results as a log | Reading the enemy becomes reading text | The enemy's wind-up pose plus an intent icon, short hit text in the middle | F: hint sentences, a read % bar, a 6-line log, a help paragraph |
| Intent display that gives false information | The player stops trusting it and loses the basis for decisions | Give less detail, never wrong detail | F: low insight showed the hint sentence of a different move |
| All menu items with the same size and weight | Nothing tells the player where to start | Make the first item larger, add a frame or icon to the active item, let the background lead the eye | B p.130–131 |
| Stats as rows of numbers | Hard to read at a glance | A radar or bar chart, icons for some text, tabs for information not needed all the time | B p.132–133 |
| Everything emphasized: many saturated colors, weak text contrast, heavy gradients | Tiring to look at for long | Fewer colors, lower saturation, stronger text contrast, gradients only for emphasis | B p.134–135 |
| Buttons and inputs that do not look operable | The player does not know the control exists | Depth on buttons, arrows on rows, placeholders in inputs, a down arrow on dropdowns | B p.136–137 |
| An unskippable long effect, targets far apart, a one-axis carousel for many items | Painful on the 100th use | Skip or "result only", shorter repeat version, short distances, grid layout | B p.138–139 |
| Mixed controller glyphs, hover-only help on a pad | Wrong for the device and may break platform rules | One glyph set per platform, a fixed help area for the selection | B p.140–141 |
| Wording, number format (01 vs 1), icon style or color differ for the same information | Looks careless and harms the game's image | One wording style, one number format, one icon style, same info same color | B p.142–143 |
| Fonts or images outside the world's tone | Breaks the world, worst in licensed titles | Fonts and images in the style of the world | B p.144–145 |
| Spelling errors, key items outside the safe area, missing copyright line, low-resolution background | Can block release | Fix before review; see the release checks | B p.146–147 |
| Small English decoration under every title | More text to check, and it doubles after localization | Remove it or keep it to one place | B p.118 |
| A text box sized to the Korean string only | No room after translation | Size to the longest language | B p.110, p.186–187 |
| A spec handed over as images only | States, limits and conditions get lost in implementation | A spec with dynamic parts, text limits and object hierarchy | B p.165–167 |
