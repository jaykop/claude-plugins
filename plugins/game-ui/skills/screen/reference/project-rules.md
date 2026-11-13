# Project UI rules

Mode `규칙` creates or updates `.claude/game-ui/rules.md` in the project root. The file keeps every screen in the project on the same rules, so screens do not drift apart. It is a guide, not a law: it may change during development, but tell the people it affects (design, engineering, art) every time it changes. (B p.52, p.60)

## How to fill it

1. Read what the project already states: design docs, engine settings (base resolution, stretch mode), existing UI scenes or widgets, fonts in the tree, an existing terms file.
2. Fill what the files show, with the source next to each value.
3. Ask the user for the rest, a few items at a time. Leave unknown values blank with `unknown`.
4. Tone and manner: propose candidates, do not decide. Give 2 or 3 keyword pairs, each with OK and NO examples. The user chooses.
5. Before you finish, run the sensitive-expression check on the motifs and words.

## Tone and manner

Decide it early. It sets the visual direction, the brand, and the difference from other games, and later screens get much easier. (B p.30)

- Keywords: two words that name the mood together ("toy" + "pop"), each with a 1 to 2 line explanation. Mixing genres or making a new word is fine. (B p.31)
- OK and NO examples: collect both. People picture different things for the same keyword. The NO examples matter most; they stop rework. (B p.32)
- Color plan: define only the roles the game needs, then do not add colors. More colors blur the roles and clutter the screen. (B p.34–35)
- Fonts: three roles, each chosen separately: title, body, parameter (numbers). A strong title font can contrast with a plain body font. All of them must stay readable in quick decisions. (B p.36–38)
- Motifs: a few decorations that keep the world and repeat well: icon marks, background patterns, frames, border lines, bullets. In a licensed title, study the original's decoration. Prefer motifs that suggest the action (press, pull). (B p.39–40)
- Example screen: make it for the main flow, the screen the player uses longest. If characters fill that screen and the UI is small, use a UI-heavy screen (settings, items, character select) instead. The example checks the tone; it is not a spec. (B p.42–44)

## Sensitive-expression check

Check motifs, symbols and words before you fix them, above all for overseas release: race, religion, politics, drugs, alcohol and tobacco, gambling, sexual content, violence, rating marks, the Red Cross emblem, and flags with historical weight. Ask the legal or quality team when unsure. Blood amount and color can raise the age rating. Events in the news can turn a fine word into a bad one. (B p.33, p.40, p.188, p.213)

## Template

Copy this into `.claude/game-ui/rules.md` and fill it.

```markdown
# UI rules

Last updated: YYYY-MM-DD

## Project story
- For whom: (age range, games they like, play time and frequency)
- Experience: (what the player should feel; one line)
- Pitch: (who it is for, what is different, what fun it gives; three lines at most)

## Requirements
- Platforms:
- Input devices: (touch / mouse and keyboard / pad)
- Base resolution:
- Minimum / maximum resolution:
- Aspect ratios: (16:9, ultrawide?)
- Anchor rule: (which elements stick to which edge)
- Safe area: (for example title 95%, action 97.5%)
- Grid: (for example multiples of 4 px)
- Minimum hit size:
- Review capture size:
- Languages: (longest language:)
- Color vision support:
- Target fps:

## Tone and manner
- Keywords:
- OK examples:
- NO examples:
- Motifs:

## Color roles
| Role | Color | Used for |
|---|---|---|
| Base | | backgrounds |
| Key | | accent |
| Progress | | buttons, active state |
| Important | | irreversible actions (delete, sell) |
| Positive | | |
| Negative | | |
| Danger | | directly tied to game over |
| Rarity | | item grades |

## Fonts
| Role | Font | Min size | Max size | License scope |
|---|---|---|---|---|
| Title | | | | |
| Body | | | | |
| Parameter | | | | |

## Text rules
- UI labels: (noun form: 결정, 취소, not 결정한다)
- System messages: (polite form)
- Punctuation: (for example no periods in labels)
- Date and time: (for example yyyy/MM/dd HH:mm)
- Numbers: (zero padding, digits, separators)
- Terms: (link to the terms list)

## Components
- Frame, dialog (close button position), buttons by color role, tabs, scroll bar, dropdown, text box (one line, multi-line), group decoration
```

## Notes on the sections

- Requirements: these are the items the book asks for at the start (release date, milestones, update rhythm, platforms, languages, minimum and maximum resolution, color vision support, target fps). A live-service game should also estimate update size and staffing. (B p.28)
- Color roles: the book's full list also has paid currency, ally, enemy, and one color per character. Add only what the game uses. Map buttons to roles: confirm in the progress color, delete in the important color, cancel in a small gray button. (B p.34–35, p.58)
- Fonts: set a minimum and maximum size per device or resolution. Check that the font has every character you need (digits, symbols, proper nouns of the world) and what its license allows. (B p.55, p.109)
- Text rules: decide them with the game designer. Automatic line-break rules (no punctuation at line start) change text length in dynamic text; check with the engineers that they can do it. Keep a terms list so that every screen spells a word the same way. (B p.56–57)
- Components: build the shared components first and assemble prototypes from them. (B p.57–59, p.80)
