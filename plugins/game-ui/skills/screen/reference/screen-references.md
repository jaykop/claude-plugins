# Reference screen structures

Before you design a screen, find screens here that handle a similar decision. If none fits, confirm new ones and add them to the project file `.claude/game-ui/references.md`. "Confirmed" content comes from the listed sources. "Not confirmed" content is not evidence. Write down the screen structure (what is visible at once, how the player moves, how the player chooses), not the mechanic.

A screen database such as Game UI Database (gameuidatabase.com) is a quick way to look at real screens by genre and screen type. (B p.227)

## Genre starting points

The usual elements of a main screen, from the book. Use them as a start, then cut by the screen's decision. (B p.42–44, p.68–71)

| Screen | Usual elements |
|---|---|
| Adventure main | Speaking character, message box, choices, current status |
| RPG main | Controlled character, status, weapon and skill slots |
| First-person shooter | Aim, weapon slot, ammo count, status, minimap |
| Mobile "my page" hub | Menu, status, main character, banners |
| Settings | Category list on the left, item list on the right (step gauges, ON/OFF pairs), scroll bar, confirm and reset |
| Item list | List with thumbnails, detail of the selected item with stat gauges |
| Character select | Large character in the middle, name and stats panel at the top right, a row of candidates at the bottom with the selected one highlighted |
| Daily login bonus | Today's reward large in the middle, tomorrow's reward small in a corner, a skip button |

## Testimony and interrogation

| Game, screen | Screen structure | Use for | Caution |
|---|---|---|---|
| Ace Attorney cross-examination | One testimony line at a time. Arrows (left and right buttons on DS) move between lines. Press and Present buttons sit at the screen corners. Press draws more out of the current line; Present shows one piece of evidence against the current line. A wrong answer costs a penalty | Any screen that questions and refutes line by line | |
| Ace Attorney Psyche-Lock (2nd game) | The number of locks shows how many secrets a witness hides. Each piece of evidence opens one. Opening all restores part of the penalty gauge; there is no game over during the unlock | A marker for "how much is hidden" | |
| Ace Attorney Perceive (4th game) | The player finds a witness's nervous habit during testimony, links it to a line, and points it out like evidence | Non-verbal clues such as habits and faces | Criticized because habits are hard to see |
| Ace Attorney Investigations 2 Logic Chess | Talks with a character who refuses to speak. Each choice has a time limit; when time runs out the character ends the talk. Wrong answers deal damage | The idea of the other side's patience | A real-time timer clashes with VN reading speed and drew trial-and-error criticism |
| L.A. Noire interrogation | Ask one question from a list, hear the answer, then choose truth, doubt or lie. A lie must be proven with evidence from the notebook. A wrong call keeps the case going but loses that question's information | "Doubt without evidence, lie with evidence". Soft failure | |
| Danganronpa Nonstop Debate | Characters' lines flow across the screen one by one. The player shoots evidence (Truth Bullets) at a weak point. As the debate goes on, fewer bullets are available | Turning pointing into an action | Layout of the bullet choice screen not confirmed |
| Contradiction: Spot the Liar! | Collect statements in interviews, then set two contradicting statements against each other to catch a lie. The player can leave a witness and come back later | Statement vs statement, parallel conversations | Layout of the statement list not confirmed |

## Evidence and records

| Game, screen | Screen structure | Use for | Caution |
|---|---|---|---|
| Ace Attorney Court Record | One button switches between two categories, Evidence and Profiles. Selecting an item shows its description. 8 items per page, with page turns. Some items open a large view of a photo or document | Notebook, evidence view, evidence choice | In The Great Ace Attorney, the player turns evidence around to examine parts |
| Ace Attorney point-to-present | After presenting a photo or map, the player points at one spot in it with a cursor. Investigation also picks one spot, then shows an Examine button | Choosing part of a place or object | |
| Sherlock Holmes: Crimes & Punishments deduction board | Link two clues into a deduction, link deductions into a conclusion. Several conclusions are possible, and a wrong one can convict an innocent person | Organizing deductions, a judgment after the conclusion | |
| Return of the Obra Dinn logbook | Fill name, fate and killer for each crew member. Three correct entries lock in together | Group checks that stop guessing | |
| The Case of the Golden Idol thinking screen | Put words collected in the scene into blanks in a summary of the case. A section locks when all of it is right. The game says when two or fewer are wrong | Rebuilding a sentence with blanks | The "two or fewer wrong" hint makes brute force easy (criticized) |

## Space and time

| Game, screen | Screen structure | Use for | Caution |
|---|---|---|---|
| Unheard | Characters are circles on a floor plan. A time bar at the bottom rewinds and fast-forwards the scene. The player follows one character and listens. Answers assign names to circles; no penalty for mistakes | Character routes, finding positions by sound | |
| The Invisible Hours | Pick a room on the mansion map to move, rewind and fast-forward time, and follow any character. A 4D map shows who moved where and when | Routes of many characters moving at once | |
| Murdle | With the rule "the killer lies, the innocent tell the truth", the player crosses out cases in a suspect × place × weapon grid | An elimination grid that the player fills in | Official rule text not confirmed (confirmed from solution posts) |

## Raising and management hubs

| Game, screen | Screen structure | Use for | Caution |
|---|---|---|---|
| Hwalhyeopjeon (活俠傳) training map | One painted view of the sect, scrolled left and right; the player clicks places directly. The base screen shows only the date, action points, contribution, and status and save buttons. Some states show only when the mouse is over the hero's half-body portrait. The status window has 6 tabs (general, attributes, sect, bag, biography, relationships); relationships are star grades and unmet characters are silhouettes | A painted place map, states hidden behind hover | Place names and event marks were left out on purpose, which drew "add names" and "slow transitions" criticism. Place screen and monthly meeting layouts not confirmed |
| Princess Maker 2 main | The daughter's portrait in the middle, 9 icon menus on the right. Stats in a separate window (4 panels); relationship values hidden. Schedule has 3 slots per month. Each activity plays a short animation (success, failure, skipping) | A portrait-centered hub, activity result cuts | The remake was criticized for an old, complex UI |
| Umamusume training turn | Turn, goal, turns left, energy gauge, mood, 5 stats along the bottom, 6 action buttons. The training choice shows 5 facility cards with failure %, support faces with friendship gauges and a "!" hint; hold to preview the result | Large action cards, hold to preview | The stat row stays on screen because the decision is "which stat to raise". The "+N" preview format not confirmed |
| Persona 5 map and Confidants | Date and time of day at the top left. Confidant card icons and "UP" (rank up soon) on the map. Good answers show 1 to 3 musical notes over the other character. Social stats use 5 named levels instead of numbers. The menu previews the next rank reward | Character marks on the map, reactions without numbers | Rank-up effects and stat screen layout not confirmed |
| Long Live the Queen | 2 lessons a week plus a weekend activity. 42 skills listed as numbers | | Called confusing (a failure case). Criticized for having no log |

## Switching between story scenes and management

| Game, screen | Screen structure | Use for | Caution |
|---|---|---|---|
| Ren'Py default ADV screen | Full background, character slots, dialogue box at the bottom (about 26% of the height), name tag at the top left of the box, a small quick-menu row, choices stacked in the center. Notifications at the top left for about 3 seconds | The base layout for event scenes | Base resolution not confirmed |
| Persona 5, Fire Emblem: Three Houses, Hwalhyeopjeon, Umamusume, Princess Maker 2 | The hub shows scene triggers as icons (speech bubble in Three Houses, "!" in Umamusume). Entering a scene hides the hub completely. Results show as short icons in the scene and as value changes after returning | Hub and scene switching | Result display details per game not confirmed |

## Battle intent and matchups

| Game, screen | Screen structure | Use for | Caution |
|---|---|---|---|
| Hwalhyeopjeon 1:1 duel | Health and energy gauges and 5 commands with a rock-paper-scissors-style net of matchups. Enemy intent hints are two category sentences ("seems about to move", "seems to be guarding"); the insight stat and the duel length raise the chance to get one | Revealing intent by category | Intent is shown as sentences. Screen layout not confirmed |
| Slay the Spire intent | Intent icon over each enemy (attack icons by damage range with numbers), "?" when unknown. Some relics trade hidden intent for a benefit | Intent bubbles, an "unknown" marker | |
| Into the Breach | Testers did not understand text descriptions, so the team switched to animated tooltips that show the weapon's effect | Explain rules with moving tooltips | |
| Sekiro perilous attacks | Two layers of warning: a warning glyph and the body's wind-up | Icon plus wind-up pose | |
| Punch-Out!! | Stronger opponents shorten or remove their tells | Less intent detail for stronger enemies | |
| Monster Hunter Stories 2 | Three-color matchup: power, technical, speed | Matchup triangle | |
| Fire Emblem combat forecast | Weapon advantage ▲ and disadvantage ▼ arrows, a forecast window before attacking | ▲▼ on move cards | |

## Case reconstruction

| Game, screen | Screen structure | Caution |
|---|---|---|
| Danganronpa Closing Argument | Rebuild the case as comic panels. Pick the cut for each empty panel from candidates; solving some panels opens others. Fake cuts are mixed in | Panels were criticized as vague and fixed in later games. Add a reconstruction step only when the user asks for one |

## Sources

- Ace Attorney: [1 gameplay](https://strategywiki.org/wiki/Phoenix_Wright:_Ace_Attorney/Gameplay), [2 gameplay](https://strategywiki.org/wiki/Phoenix_Wright:_Ace_Attorney_-_Justice_For_All/Gameplay), [3 gameplay](https://strategywiki.org/wiki/Phoenix_Wright:_Ace_Attorney_-_Trials_and_Tribulations/Gameplay), [4 gameplay](https://strategywiki.org/wiki/Apollo_Justice:_Ace_Attorney/Gameplay), [5 gameplay](https://strategywiki.org/wiki/Phoenix_Wright:_Ace_Attorney_-_Dual_Destinies/Gameplay), [6 gameplay](https://strategywiki.org/wiki/Phoenix_Wright:_Ace_Attorney_-_Spirit_of_Justice/Gameplay), [The Great Ace Attorney evidence examination](https://twinfinite.net/guides/great-ace-attorney-chronicles-examine-evidence/), [3 speedrun notes (Evidence/Profiles switch)](https://www.speedrun.com/tat/guides/w0lxq)
- Ace Attorney Investigations 2: [Wikipedia](https://en.wikipedia.org/wiki/Ace_Attorney_Investigations_2:_Prosecutor%27s_Gambit), [StrategyWiki](https://strategywiki.org/wiki/Ace_Attorney_Investigations_2:_Prosecutor%27s_Gambit/Gameplay)
- L.A. Noire: [Engadget interrogation guide](https://www.engadget.com/2011-05-20-be-a-better-l-a-noire-interrogator.html), [Game Developer](https://www.gamedeveloper.com/design/l-a-noire-s-interrogation-system)
- Danganronpa: [System](https://danganronpa.us/danganronpa/system.html), [StrategyWiki](https://strategywiki.org/wiki/Danganronpa:_Trigger_Happy_Havoc/Gameplay), [V3 playthrough (Closing Argument)](https://lparchive.org/Danganronpa-V3-Killing-Harmony/Update%2033)
- Contradiction: [Giant Bomb](https://giantbomb.com/wiki/Games/Contradiction_Spot_The_Liar), [StrategyWiki](https://strategywiki.org/wiki/Contradiction:_Spot_The_Liar)
- Sherlock Holmes: Crimes & Punishments: [MobyGames](https://www.mobygames.com/game/68722), [Gamecritics review](https://gamecritics.com/jay-pullman/sherlock-holmes-crimes-punishments-review/)
- The Case of the Golden Idol: [TV Tropes](https://tvtropes.org/pmwiki/pmwiki.php/VideoGame/TheCaseOfTheGoldenIdol), [RPGFan review](https://www.rpgfan.com/review/the-case-of-the-golden-idol/)
- Unheard: [PC Gamer](https://www.pcgamer.com/this-new-detective-game-is-all-about-listening-to-solve-mysteries/), [Thumb Culture review](https://www.thumbculture.co.uk/unheard-voices-of-crime-edition-switch-review)
- The Invisible Hours: [GameSpot review](https://www.gamespot.com/reviews/the-invisible-hours-review-from-every-angle/1900-6416897/), [UploadVR preview](https://uploadvr.com/the-invisible-hours-preview)
- Murdle: [Daily Murdle solution post](https://fandomwire.com/daily-murdle-solution-for-today-july-19-2025/)
- Return of the Obra Dinn: no source link (a widely known rule; confirm before you use it as evidence)
- Hwalhyeopjeon: [Namuwiki status](https://namu.wiki/w/활협전/상태), [Namuwiki actions](https://namu.wiki/w/활협전/행동), [GCORES review](https://www.gcores.com/articles/183482), [Steam announcements feed](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1859910&count=100&feeds=steam_community_announcements), [Sohu duel guide (intent hints)](https://www.sohu.com/a/802079131_258858)
- Princess Maker 2: [Wikipedia](https://en.wikipedia.org/wiki/Princess_Maker_2), [CRPG Addict](https://crpgaddict.blogspot.com/2024/05/game-514-princess-maker-2-1993.html), [Anime News Network Regeneration review](https://animenewsnetwork.com/review/game/nintendo-switch/princess-maker-2-regeneration/.213316)
- Umamusume: [umamusu.wiki Career Mode](https://umamusu.wiki/Game:Career_Mode), [GameTora beginner's guide](https://gametora.com/umamusume/beginners-guide), [Game8 training guide](https://game8.co/games/Umamusume-Pretty-Derby/archives/536168)
- Persona 5: [itch.io Persona 5 UI study](https://itch.io/blog/533534/making-ui-come-to-life-study-of-persona-5), [ludo.guide Confidant overview](https://www.ludo.guide/guide/persona-5/extras/confidants/confidant-overview), [Wikipedia](https://en.wikipedia.org/wiki/Persona_5)
- Long Live the Queen: [Wikipedia](https://en.wikipedia.org/wiki/Long_Live_the_Queen_(video_game)), [Cubed3 review](https://cubed3.com/review/2166/1/long-live-the-queen-pc.html)
- VN screens: [Ren'Py GUI](https://www.renpy.org/doc/html/gui.html), [UI Design: An Anatomy of Visual Novels](https://towardstheendsky.blogspot.com/2024/08/ui-design-anatomy-of-visual-novels.html), [Three Houses support conversations](https://blog.hyperx.com/article/8149/how-to-view-support-conversations-in-fire-emblem-three-houses)
- Battle intent: [Slay the Spire Wiki Intent](https://slaythespire.wiki.gg/wiki/Intent), [Into the Breach UI interview](https://gamedeveloper.com/design/-i-into-the-breach-i-dev-on-ui-design-sacrifice-cool-ideas-for-the-sake-of-clarity-every-time-), [Sekiro perilous attacks](https://www.ludo.guide/guide/sekiro-shadows-die-twice/core-mechanics/perilous-attacks), [Punch-Out!!](https://en.wikipedia.org/wiki/Punch-Out!!_(1984_video_game)), [Monster Hunter Stories 2 combat](https://primagames.com/gaming/monster-hunter-stories-2-combat-explanation), [Fire Emblem Wiki combat forecast](https://www.fireemblemwiki.org/wiki/Combat_forecast)
- Book: 오타가키 사야코, 『플레이어를 생각하는 게임 UI 디자인 노하우』(김모세 옮김, 한빛미디어). Genre starting points from p.42–44 and p.68–71; Game UI Database from the reference list on p.227.
