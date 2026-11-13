---
name: screen
description: "Game UI screen design guide. Use it when you plan, mock up, review, or hand off game screens: menus, HUD, dialogue windows, notebooks and evidence screens, maps, management and raising hubs, event scenes, battle screens, settings, shops, result screens. It first fixes who the screen is for and the one decision the player makes on it, checks the real screen structure of 2 to 3 reference games, splits each screen into focus, support, detail (tooltip or help area) and sub-screen layers, and checks the result against an anti-pattern list and a visual checklist. It also sets up a project's UI rules file (requirements, tone and manner, color roles, fonts, text rules) and writes implementation specs for engineers (states, motion list, text limits, naming, draw layers, resolution and safe area, localization, platforms). Sources: a Korean game UI design book (page cites) and user feedback on two visual novel prototypes. Not for: engine code, image generation, story or dialogue writing, sound design, marketing banners."
when_to_use: "When a task plans or reviews a game screen or UI, also inside a larger design task, and before you design a mechanic that needs a new screen. Examples: '인벤토리 화면 설계해 줘', '이 HUD 리뷰해 줘', '상점 UI 시안 만들어 줘', '설정 화면 기획', '툴팁 어떻게 넣지', '전투 화면 정보가 너무 많아', 'UI 규칙 문서 만들어 줘', '톤 앤 매너 정해 줘', 'UI 기획서 엔지니어용으로 써 줘', '구현된 화면 캡처 검수해 줘', '/game-ui:screen 리뷰만 docs/ui/shop.md'."
argument-hint: "[설계|리뷰만|규칙|인계] [screen name, document, or capture]"
---

# Game UI screen design

Follow this when you design or review game screens. A person makes the final decision.

## Sources

Rules carry a source mark so that a reader can check them.

- `B p.N`: 오타가키 사야코, 『플레이어를 생각하는 게임 UI 디자인 노하우』(김모세 옮김, 한빛미디어), page N. The rules here are paraphrased. The book has the figures and the full examples.
- `F`: feedback a user gave on two visual novel prototypes (a mystery VN and a raising sim, 2026-11). The same mistakes came back in both, so they became rules.

## Paths and priority

- This skill folder: `${CLAUDE_SKILL_DIR}`. If the variable is not expanded, it is the folder that holds this SKILL.md.
- Project UI rules: `.claude/game-ui/rules.md` in the project root, if it exists. It holds the values this skill does not guess: platforms and input devices, base resolution, safe area, minimum hit size, languages, color roles, fonts, text rules.
- Project references: `.claude/game-ui/references.md`, if it exists. Add reference screens you confirm in a project there, not in this skill folder. An update of the plugin overwrites this folder.

Follow, in order: the user's current request, the project's instructions (CLAUDE.md, AGENTS.md), the project UI rules file, a project skill for its own screens (for example a VN skill), then this skill.

## Modes

| Mode | When | Read |
|---|---|---|
| `설계` (default) | Plan or mock up screens | [reference/anti-patterns.md](reference/anti-patterns.md), [reference/screen-references.md](reference/screen-references.md), and [reference/visual-checklist.md](reference/visual-checklist.md) before you show a mockup |
| `리뷰만` | Review a design doc, mockup, or capture. Do not edit | [reference/anti-patterns.md](reference/anti-patterns.md), [reference/visual-checklist.md](reference/visual-checklist.md) |
| `규칙` | Create or update the project UI rules file | [reference/project-rules.md](reference/project-rules.md) |
| `인계` | Write the implementation spec for engineers, or check an implemented screen | [reference/spec-and-handoff.md](reference/spec-and-handoff.md) |

## Principles (always)

### Screen structure

1. One focus per screen. Show one thing large: one statement, one item, one character, one decision. Then plan what the eye reads 2nd and 3rd, with size, position, contrast and motion. When all elements have the same weight, the player does not know where to start. (F; B p.106, p.130)
2. Split decision screens from reading screens. A decision screen holds only the information that changes that decision. Full stats, all relationships and logs go to a reading screen that the player opens. A hub may show a stat row all the time only when the decision is "which stat to raise". (F; B p.132)
3. Move between categories with a snap (left and right, or tabs). Inside a category, show a small position marker (thumbnail row, dots) and the selected item's information only. Do not spread the content of all items on one screen. (F)
4. Start a choice from the context: the line the player reads, the place where the player stands. Do not make the player match a full target list against a full item list on one screen. (F)
5. When sorting the information is part of the puzzle, do not give a table that the game sorted. Give a recording tool: a blank form, stickers, notes. (F)
6. Show space on a map, and time one segment at a time. A time × place table does not replace a route in a building. (F)
7. Show a tension resource as a gauge with a meaning in the story (patience, trust), not as a number counter. (F; B p.23)
8. Show new information when it appears, one piece at a time. Do not drop it all when the player opens the notebook. (F)
9. Use pictures, icons and position before blocks of text. Decoration must not be louder than information. Use only the few motifs that the project's tone and manner defines. (F; B p.39, p.133)
10. Put reasons and exact numbers in a detail layer: a tooltip, or a fixed help area for the selected item. The screen keeps the marker (icon, gauge, stage name). Information that the decision needs stays on the screen; the detail layer only adds to it. Detail text is 1 to 3 lines. If it needs more, move it to a sub-screen. (F; B p.141)
    - Open it with mouse hover, keyboard or pad focus, and touch long-press. Support all three.
    - On pad-first or touch-first platforms, prefer a fixed help area (usually at the bottom) that follows the selection. A hover-only tooltip fails there.
11. Prefer the layouts that players know from similar games. Use a new pattern only when the known one fails the screen's decision, and say why. (B p.76)
12. Do not add screens or screen steps that the user did not ask for. Propose them with a reason and wait for a yes. A dead end or a missing back path that a flow check finds is a finding to report, not a reason to add a screen. A control inside the requested screen (a tab, a skip button) is not a new step. (F; B p.75)

### Feedback, scenes, battle

13. Show a value change three times with the same icon: at the moment it happens (an icon over the character who reacted: ♪ for relationship, ▲▼ for stats), on a result card at the end of the scene (5 lines at most, before → after bars), and as a gauge animation when the player is back on the hub. A corner toast alone is not enough. (F)
14. When a story scene starts, hide the management screen completely and use the standard scene layout: background, character sprites, dialogue box. Do not dim the hub and float a dialogue box over it. (F)
15. Mark where a scene or event can open with an icon on the map or on the place ("UP", "!"). Without the mark, players hunt for conditions. (F)
16. In battle, show the enemy's intent as an icon over the enemy, not as a sentence. The intent display never lies. It only gives less detail: "?" → category → two candidates → exact. Show matchups with a small triangle diagram and ▲▼ on move cards. Hide the log by default. Put the two fighters large, face to face, with each bar next to its fighter. (F)
17. In a dialogue box, put the speaker's name at the top left and small reference information (room, status gauge) to its right. Do not show the name in a second place, and do not add titles such as "X's testimony". (F)

### Repeated use and visuals

18. Design for the 100th use. A long effect gets a skip or a "result only" button, and later plays get a shorter version. Keep the elements that the player moves between close together. Put selectable items in a grid that a d-pad can walk. Check the layout for each input device (touch, mouse, pad). (B p.110–111, p.138–139)
19. Subtract. Use few colors, low saturation, strong contrast between text and background, and gradients only where you emphasize. (B p.134–135)
20. A color has one role from the project rules (progress and active, important for irreversible actions, danger, positive, negative, rarity). The same information has the same color on every screen. Do not carry a meaning with color alone; add a shape, icon or text. (B p.34–35, p.142, p.197–198)
21. What the player can operate looks operable: buttons have depth, a row that opens another screen has an arrow, an input field has a placeholder, a dropdown has a down arrow. (B p.136–137)

## Procedure (`설계`)

0. Context. Read the project UI rules file. If it is missing, check only what this screen needs: who plays and what experience the game gives (one line), platforms and input devices, base resolution, languages, color vision support. Mark the rest "unknown". Offer to make the rules file with mode `규칙`. (B p.26–28)
1. Flow. List the screens of the flow the user asked about, and link them: main cycle, sub-screens, back paths. Check for dead ends, screens with no way in or out, and the in-game and out-game split. Report gaps; do not add screens (principle 12). (B p.73–75)
2. Requirement card for each screen. (B p.65–72; F)
   - Purpose: the real aim, not the means. A daily login bonus exists so that the player wants to come back tomorrow, not to hand out an item.
   - Decision: the one decision the player makes here, in one sentence. Two decisions → split the screen. No decision → it is a reading screen; do not mix it with a decision screen.
   - Functions: verbs (list, select, confirm, show result).
   - Elements: in priority order, each with its text length or digit limit (name 2–8 characters, attack 3 digits).
   - Notes: what may change later.
3. References. For each decision, check the real screen structure of 2 to 3 reference games. (F)
   - Check: what is visible at once, how the player moves to the next item, how the player chooses, what shows after a wrong choice.
   - Do not judge from a description of the mechanic. Confirm with a wiki, a review, a playthrough, or a screen database, and keep the source. Write "확인 못 함" for what you could not confirm, and do not use it as evidence.
   - Start with [reference/screen-references.md](reference/screen-references.md), then the project references file.
4. Layers. Give each screen four layers. If the focus has two things, go back to step 2.
   - Focus: large, one.
   - Support: small; position and state (icon, gauge, stage name).
   - Detail: tooltip or help area; reasons and numbers (principle 10).
   - Sub-screen: a reading screen that a button or key opens.
5. Layout and states. (B p.76, p.80, p.108–110, p.123–124)
   - Place rectangles first: higher priority, larger and more visible. Place every navigation button now.
   - Put real text at its maximum length, in the longest target language. Then decorate.
   - List the states of each interactive element (default, hover, focus, pressed, released, cancel, disabled) and each dynamic case (icon by state, gauge by value, box size by text length, result by win or loss).
6. Checks. Answer the questions in [reference/anti-patterns.md](reference/anti-patterns.md). Before you show a mockup, run [reference/visual-checklist.md](reference/visual-checklist.md).
7. Mockup, only when the user asks for one. Add one line to each mockup with its focus and its completion level (D: layout boxes, C: rough, B: colors and main decoration, A: near final), so that reviewers judge at that level. Put small feedback on a mockup into the design doc; do not rebuild the mockup for it. (F; B p.200)
8. Handoff. When the screen goes to implementation, write the spec with [reference/spec-and-handoff.md](reference/spec-and-handoff.md).

## `리뷰만`

Do not edit. For each screen, report: the player's decision, the focus (or "none"), layer problems, anti-pattern hits, visual checklist hits, and what to confirm with the user. Rank by the effect on the player's decision. For a capture of an implemented screen, also check the verification items in [reference/spec-and-handoff.md](reference/spec-and-handoff.md#verify-the-implemented-screen) (extreme values, longest text, each input device). Say what you could not check from a still image: motion, sound, the screens before and after. (B p.129)

## `규칙`

Use [reference/project-rules.md](reference/project-rules.md) to create or update `.claude/game-ui/rules.md`. Fill what the project files show. Ask for the rest. Leave unknown values blank and marked. Do not invent tone keywords or colors on your own: propose candidates with OK and NO examples and let the user choose. (B p.30–59)

## Report

Keep it short for each screen: the player's decision / reference screens and sources / focus, support, detail, sub-screen / anti-pattern and checklist results / completion level / what to confirm. The conversation gets the conclusion and the questions. The details go to the project's design doc.

## Do not

- Present a list or table of information as the UI.
- Take a reference game's mechanic without checking its screen structure.
- Show a mockup with no stated focus.
- Lay out with placeholder text that is shorter than the real text.
- Put a hover-only tooltip on a pad or touch screen.
- Add a screen, step, or phase that the user did not ask for.
