# Spec and handoff

Use this when a screen goes to implementation, and when you check an implemented screen. Engineers need the dynamic parts, not a description of the still image. Do not expect an engineer to fill gaps on their own: the person who made the design knows the data best. (B p.165–166)

## Spec contents

Write one spec per screen or shared component. Any format is fine; keep it under version control, because it changes often. (B p.166–167)

1. Overview: the screen's purpose and decision (from the requirement card), and its variants (for a dialog: 1 button, 2 buttons, no button).
2. Layout image, with the focus marked.
3. Elements: in priority order, each with its text limit (for example 30 characters × 3 lines) or digit limit and number format (zero padding, digits, decimals).
4. Player input: touch, click, swipe, pinch, double-click, drag and drop, buttons, and which input devices.
5. Conditions: time, flags, parameters that change the screen.
6. Dynamic text and images: user-set text (player name in a sentence), state text, icons by state, avatar parts, box size by text length, result screen by win or loss.
7. States of each interactive element: default, hover, focus, pressed, released, cancel (pressed, moved out, released), disabled. (B p.123–124)
8. Motion: entry and exit animation, transition, effects, sound (see the motion list).
9. Open items: temporary parts, counts that may grow (text length, number of images or files), parts whose type may change (text → image).
10. Object hierarchy, if the engine uses one (for example Canvas > Dim > Dialog > ContentsWrapper > Message), with the role of each node.

Leave the implementation method to the engineer. (B p.166)

## Motion list

Share and update one list for the whole UI. (B p.82–87, p.123–127)

| Screen or element | Trigger | Animation or effect | Play mode | Owner | Sound |
|---|---|---|---|---|---|
| | on open, on press, on value change, on win | | once / N times until a condition / loop | UI, VFX, 3D, sound | |

- Transitions: choose the method per condition (fade, slide, wipe, white-out, black-out, spin) for in-game, out-game, story scenes, specific menus, entry and exit. Agree on it with the effects owner and the engineers. (B p.124–125)
- Owners: UI effects usually belong to UI (text effects, touch effects, effects that follow UI motion or cover the whole screen). Model and particle effects usually belong to VFX. When the owner is unclear, UI leads. (B p.83, p.86, p.127)
- Decide early whether a character on a UI screen is a 2D image or a 3D model. The implementation path differs a lot. (B p.80, p.86)
- Bring in sound early. It shapes the UI experience and gets forgotten after mid-development. (B p.87)

## Names

Files, objects and IDs are referenced by code. Do not rename or delete them on your own. Follow the engineers' naming document if one exists. (B p.155)

- Name by function, not by look: `Icon_Weapon`, `Window_Menu`, not `Icon_Red`, `Window_Left`. (B p.155)
- Treat case as significant, and keep one case style and one word separator (camel, snake or kebab). (B p.98, p.155)
- Use ASCII letters and digits in implementation files. Fix the number of serial digits, and start serials at 0 (`Image_000`). (B p.98, p.156)
- Avoid reserved words of the engine and the code. (B p.156)
- Use a UI prefix (`UI_`), agreed abbreviations (`bg`), and a maximum length; long paths can break builds. (B p.98–99)
- Under version control, do not use copy, final, or date suffixes. (B p.99)

## Draw layers

Define the draw order of UI layers early, with design and engineering. Moving an element to another layer late is hard. Example from the book, top first: (B p.103–104)

- In-game: special (chat input), system (errors, urgent notices), key effects (start, end), full-screen features (map, settings), important alerts (reload, near death), always-on (status, weapon, minimap), general (character info, score), effects (kill effects, damage numbers, cut-ins), 3D-attached info (names, status over characters).
- Out-game: system, transition effects (screen change, loading), always-on (current state, help), modal dialogs, general.

## Resolution, aspect, safe area

Write these in the project rules file and check every screen against them. (B p.100–101, p.115, p.189–191)

- Base resolution: the one most target players use. Review every design at this resolution so that reviewers see the same thing.
- Minimum resolution: text and key icons stay readable and do not break.
- Maximum resolution: 4K or 8K plan (vector-based scaling where possible).
- Aspect ratios: 16:9 and which others (ultrawide).
- Anchor of each element (top, bottom, left, right, center). Edge anchors drift far apart on ultrawide screens.
- Safe area: a common TV rule is title safe 95% and action safe 97.5% of width and height. Text that must be read goes inside title safe.
- Grid: positions and sizes in multiples of 4 px.
- Minimum hit size for touch and mouse: from the project rules file.

## Localization

Fix the release regions and languages at the requirements stage. Translation only, or content changes too? It changes cost and schedule. (B p.185–188)

- Text length: size each box for the longest language (German is often longest). One Korean word can become about 10 characters in another language.
- Direction: right-to-left languages, vertical text.
- Fonts: per-language fonts; some countries recommend specific fonts. Check the font license for embedding, atlases and server use. (B p.109–110)
- Confirm and cancel buttons: the meaning of ○ and × differs by region and platform.
- Colors, symbols, history, religion, politics: check for local meanings.
- Plan time for a native-speaker review and the fixes after it.

## Platforms

- Controller glyphs and button terms are swappable per platform, also in tutorials. (B p.140–141, p.192)
- Check the certification rules of each platform early (console makers, mobile stores). A failed check blocks release. (B p.119, p.192)
- Decide what to show during loading. (B p.119)
- Ask people with experience on a platform for its common bugs before you start. (B p.192)

## Assets

- Make textures no larger than needed. Pack parts into power-of-two atlases. Draw simple shapes with the engine instead of textures. Reduce colors where it does not hurt. (B p.156–159)
- Ask for the format, bit depth, size, count, and per-screen texture limits before you make data. (B p.156–157)
- An edited source file is not the game file. Ask when and how a change reaches the build. (B p.154)

## Verify the implemented screen

- Play it: check against the design with the game designer and the engineer, and list the fixes as tasks. (B p.169)
- Ask for a UI-only test scene, so the screen opens without a full playthrough. (B p.169)
- Ask for debug commands that force extreme and rare values (damage -9999, money at max, every icon state), and check every pattern. (B p.169–170)
- Later, play from start to end in order: some bugs exist only in the full flow. (B p.170)
- Check each input device and the longest language.
- Automate repeated manual checks (names, spelling, format conversion) or make the tools show errors. When a mistake repeats, fix the method, not the person. (B p.171)

## Status and reviews

- Keep a status for each screen, and show a "temporary" mark on screens in test builds. Example stages: layout → rough → final design → fixed. (B p.172–173)
- Completion level for reviews: A 80%+ (polish toward fixed), B 50%+ (colors, layout, main decoration, some animation), C 30%+ (rough layout, color direction, temporary images, minimal animation), D under 30% (function only, plain boxes). Share the level so feedback matches it. (B p.200)
- Review procedure: share the status and the checklist for that level; collect comments from play; sort them by category; mark each positive, negative or other; raise the priority of repeated comments; set the scope with the director; record the reason for every comment you act on and every one you do not. (B p.199)
- Common comments: "something is off" → ask where, then sort into function, visual, feel. "Tiring" → brightness, contrast, size and amount of text, strong effects. "Cluttered" → amount of elements (with the game designer), spacing, one shape, size and color system. "Make it like X" → find which part of X they mean. "Is this final?" → say the current level and take comments for that level. (B p.201)
- Read player feedback for the real problem behind it, not word for word. (B p.209)

## Engine notes

- Godot: `Control.tooltip_text` and `_make_custom_tooltip()` open on mouse hover only. For keyboard and pad focus and for touch long-press, open the same tooltip from the screen's focus and input signals, or use a fixed help area. (F)
