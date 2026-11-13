# Visual checklist

Run this before you show a mockup and when you review a capture. A still image cannot show everything: also check the screens before and after, the motion and the sound when you can, and say what you could not check. (B p.129)

## Nine checks

| # | Check | Why | Fix |
|---|---|---|---|
| 1 | Is it clear where to look first? Are the 2nd and 3rd steps led too? | The most important information must arrive first. Intuition beats detail | Size differences by priority; a frame or icon on the active item; a background gradient that leads the eye in the reading direction (B p.130–131) |
| 2 | Is the amount of information right? Does each piece show when it is needed? | People take in little at once. What the developer wants to show is not what the player needs | Remove what the decision does not need; numbers → chart; some text → icons; tabs for information not needed all the time. Agree on cuts with the game designer (B p.132–133) |
| 3 | Is it tiring for the eyes? | Players look at UI for a long time. Showiness grows easily | Weaken what does not need emphasis; fewer colors, lower saturation; stronger text contrast; gradients only for emphasis. Color and contrast alone often fix it (B p.134–135) |
| 4 | Can the player tell what is operable? | Players judge from experience whether something can be pressed | Depth on buttons; an arrow on rows that open a screen; a placeholder in inputs; matching style for an input and its button; a down arrow on dropdowns (B p.136–137) |
| 5 | Does it hold up after 10, 100, 10,000 uses? | Developers see a screen once; players see it every day | Skip or "result only" for long effects; a shorter version on repeat; short distances; a grid for d-pad selection. Agree early with design and engineering (B p.138–139) |
| 6 | Does it fit each target hardware and input device? | Each platform has its best input. Platform rules also govern glyphs | One glyph set per platform; generic d-pad images where possible; a fixed help area instead of hover tooltips for pad and touch; test the feel in play (B p.140–141) |
| 7 | Is it consistent in the screen and across the flow? | Inconsistency looks careless | One wording style; one number format (zero padding, digits); one icon style; same information, same color (B p.142–143) |
| 8 | Does it keep the world's tone? | World consistency matters as much as usability, most in licensed titles | Fonts and images in the world's style; follow the tone and manner the lead set (B p.144–145) |
| 9 | Is it release quality? | A failed check can block release | Spelling; key items inside the safe area; copyright line; image resolution; platform rules (B p.146–147) |

## What draws the eye

Use these to build the reading order, and to find what steals attention: large, bright, dark, high contrast with the background, warm colors, a known warning pair (yellow and black), complex shapes, the one item that differs in a row, text (next to a picture, the text is read first), and motion. (B p.106–108)

## Rough design check

A rough is ready for detailed design when all of these hold. Do not polish a rough; try more variations instead. (B p.105, p.113–114)

- You can tell which part must catch the eye first.
- The player can reach the information in the order of play.
- All text stays readable.
- The amount of information shown or read at once is right.
- Text in the real font fits its maximum length.
- Text in each localized language fits its maximum length.
- Buttons and the cursor are in easy positions.
- For multi-platform games, the layout works in each environment.
- Colors follow the color plan of the tone and manner.
- No extra colors were added.
- Color vision differences are covered.
- You can picture the size and the motion of the final design.

## Color order

1. Place colors from the project's color plan.
2. Set the colors of large areas.
3. Set contrast colors and small accent colors.
4. Turn the screen to grayscale. A good color screen still shows its contrast in grayscale. Repeat 2 to 4.

Check color vision with a simulation at this point if the project supports it. (B p.111–112, p.197–198)

## Finishing rules

- Avoid pure RGB primaries (#FF0000, #00FF00) and pure black (#000000) unless you mean them. Slightly shifted colors (navy, brown, carbon gray) look richer. (B p.117)
- Keep the corner ratio when you round a rectangle. When you nest rounded rectangles, the inner radius is smaller than the outer one. Scaling a finished shape breaks the ratio. (B p.117–118)
- Fix letter spacing by hand where it hurts readability. (B p.118)
- Do not add small English decoration under titles. (B p.118)
- Decide where anti-aliasing is allowed. Automatic anti-aliasing can spoil small text and pixel art. (B p.116)
- Texture and decoration: more is not better. Set a decoration level for the project and stay in it. (B p.116)
- Check at the minimum resolution that no text or image breaks. (B p.115, p.190)

## Motion check

- Frame rate: fixed, or the minimum and maximum if variable. (B p.126)
- Limits: objects that move at once, overlapping alpha textures, keyframes per object. (B p.126)
- Reuse: can one animation serve other objects? (B p.126)
- Speed: equal speeds feel orderly, mixed speeds feel rich. Use anticipation at the start and end of a change for a lively feel. (B p.126)
- Pivots for rotation and scale: can the designer set them? (B p.126)
- Alpha on stacked objects: does each fade alone or as one group? (B p.127)
- Sound: who sets the sound for each animation, and who hears about changes? (B p.127)
- Banned effects: strong flashing, sudden full-screen changes, regular patterns of different brightness. Check the platform rules. (B p.127)
