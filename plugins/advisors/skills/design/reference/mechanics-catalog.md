# Mechanism catalog

This file lists the mechanisms that produce control feel, combat readability, and the level and camera experience in 3D action games. The design advisor does not judge hand feel, hit impact, or control feel. It checks only whether the project has the mechanisms that produce the feel its pillars ask for, whether they fit the principles, and whether their values agree with each other. Read this file in area diagnosis Step A3-4 and in single review Step B3 (frameworks §10). The analyst that collects material reads only the sections and rows that the caller names.

Write the English names when profile `report_language` is `en`, and the Korean names in parentheses when it is `ko`.

## 0. How to use

- A row is a question, not a requirement. Many games leave a mechanism out on purpose (for example, no guard in a game that wants nonstop offense, or no jump in a game built on one-to-one sword duels). A missing mechanism is a finding only when a pillar needs the feel that the mechanism produces.
- For each row that applies, record one of four states:

  | State (상태) | Meaning |
  |---|---|
  | present (있음) | Found in documents, data, or code. Write the location and the implementation stage |
  | deliberately left out (의도적으로 뺌) | A design document says it was left out. Write that location |
  | not found (찾지 못함) | Not found in the searched scope. Write the scope and the pattern |
  | cannot check (확인 불가) | The logic or values are in assets that cannot be read as text (Blueprint graphs, binary scenes, animation notifies). Write which assets |

- "Not found" in a text search is not "absent". Values often live in assets that cannot be read as text. Write "not found" with the search log, and do not make it a verdict on its own. In a conversation run, turn it into a question for the user.
- Evidence grades: presence only in design documents is [document]. Presence in code or data follows the implementation stage. A comparison between the project's own values is [calculated]. What the player feels stays a hypothesis (`Hypothesis:`), with a verification method.
- This file has no target numbers. Do not bring target values from memory or from outside material. The only number checks are the "Consistency" questions, which compare the project's own values with each other (for example, whether attacks that deal more damage also have longer anticipation). Sort the values, mark the places where the order breaks, and show the table.
- Engine words follow Unreal. In a Godot project, use the Godot names in the search term lines.

## 1. Control response (조작 응답)

| ID | Mechanism (메카닉) | Where it shows (흔적) | Check question (점검 질문) | Failure shape (실패 모양) |
|---|---|---|---|---|
| move-01 | Acceleration and stopping (가속·정지) | Acceleration, deceleration, braking friction, skid on direction reversal | Does stop precision fit the pillar? A game about exact positioning wants short stops. A game whose challenge is momentum can want longer ones | Long stops in a precision game feel unfair. Instant stops in a momentum game flatten the challenge |
| move-02 | Variable jump and air control (가변 점프·공중 제어) | Jump height by hold time, air acceleration, max fall speed | Can the player correct a jump in the air? | Without air control, the player walks back and retries the run-up again and again |
| move-03 | Near-miss forgiveness (아슬아슬한 실패 보정) | Late jump after leaving a ledge, ledge grab, rising on wall contact during a jump, edge snap | When a jump is just short, does it still succeed in places where the pillar does not want punishing precision? | Failures that look like success on screen read as bugs |
| move-04 | Turn and turnaround (선회·돌아보기) | Turn rate, turn in place or turn radius, turnaround animation length by direction, whether the turnaround can be canceled | Is the turnaround fast where response matters (combat) and slow only where realism matters? | Slow turns in fights against many enemies |
| move-05 | Stats change ability, not response (스탯은 능력만 바꾼다) | Which values equipment, weight, or growth changes | Do stats change turn rate, jump distance, or input delay? | Players cannot tell whether a failure came from their skill or their stats. Jumps that the level needs become impossible with some builds |
| move-06 | Input buffer (선행 입력) | Buffer window length, number of slots, the states that accept a buffered input | Does the buffer length fit the intended weight of attacks? Is there a way out of a buffered move that the player did not want (guard cancel)? | A long buffer makes moves come out late, feel light, or come out by accident. No buffer makes every link a timing test |
| move-07 | Cancel windows (캔슬 구간) | State transition table: attack to dodge, recovery to guard, and in which frames | If the pillar wants offense to keep flowing, can the player dodge out of an attack and keep the combo? | Defense resets the combo and breaks the flow. Cancels everywhere remove commitment |
| move-08 | Press or hold (누름·길게 누름 구분) | Hold threshold, a shared first motion while press or hold is still undecided | Does deciding press or hold delay the response? Where in a combo can a hold branch start? | Every press feels slow |
| move-09 | Context action (상황 액션) | Object or state tag to action table, one button with several meanings | Does each context action have a visible cue? Does a button keep the same verb in every state? | The same button does unrelated things. Players trigger actions they did not want |
| move-10 | Targeting assist (조준·타깃 보조) | Lock-on target selection (angle, distance, priority), release conditions, retarget after a kill, per-attack homing range, angle, and speed, aim snap strength and duration, option toggle | Does homing differ by attack and weapon? Does the assist stop after the first moment, so skill still matters? | Strong homing on every attack removes weapon identity and skill. Homing that pulls the player over ledges |
| move-11 | Edge and fall rules (가장자리·낙하 규칙) | Edge guard angle, auto-jump volumes, which falls kill and which do not | Are the fall rules consistent enough to learn? | Players cannot predict which drops are safe |
| move-12 | Failure that keeps the character (캐릭터다운 실패) | Special states for wall bumps, water exits, and glide collisions, a list of motions the character must not do | When the player fails, does the character still act like the character the pillars describe? | A hero who flails or dies in a silly way breaks the fantasy |

Search terms: `Accel|Decel|Friction|Braking`, `Coyote|LedgeGrab|AirControl`, `TurnRate|RotationRate`, `InputBuffer|Buffer`, `Cancel`, `Hold|Charge`, `Interact|Context`, `LockOn|Target|Homing|Magnet|AimAssist`.

## 2. Attack, defense, and being hit (공격·방어·피격)

| ID | Mechanism (메카닉) | Where it shows (흔적) | Check question (점검 질문) | Failure shape (실패 모양) |
|---|---|---|---|---|
| atk-01 | Attack phases (공격 단계) | Per attack: anticipation, active, and recovery length, the active window of the attack volume, cancel flags | Are the phases data, not only baked into animations? Consistency: do attacks that deal more damage have longer anticipation or recovery? | Strong attacks that are also fast leave no reason to use weak ones |
| atk-02 | Hit feedback (타격 피드백) | Hit stop length and timing (at contact or just after), hit sound, camera shake, hit effects, damage numbers | Do light and heavy attacks use different amounts of feedback? When the target does not react, is the hit still shown (effect, gauge drop)? | Hits on armored enemies that look like misses. The same feedback on every attack |
| atk-03 | Hit reaction mapping (피격 리액션 대응) | Reaction classes (flinch, knockdown, launch, stagger, stun), an attack-to-reaction column, the number of directions | Does each reaction open a next action (combo, finisher, counter)? Motion budget: reaction sizes × directions × body types | Reactions that do not match the attack look random. Direction sets that multiply animation cost |
| atk-04 | Poise and super armor (강인도·슈퍼 아머) | Poise value, stagger value per attack, decay time, armor windows | Do large enemies react to every hit (and look weak), or only after enough damage? Is armor shown before it matters? | Bosses that never get to attack because every hit interrupts them. Armor that the player cannot read |
| atk-05 | Knockback and combo limits (넉백·콤보 제한) | Knockback distance per attack, scaling by combo count, gravity scaling for airborne targets | Is there a guard against infinite combos? | Loops that kill from full health |
| atk-06 | Invulnerability and getting up (무적·기상) | Invulnerable windows by state (dodge, knockdown, getup, special move), protection after getup, enemy rules while the player is down | Can the player be hit until death with no chance to act? Does the way invulnerability is shown fit the art style? | Hit-lock deaths. Blinking that looks out of place in a realistic game |
| atk-07 | Cost of defense (방어의 대가) | Guard stamina or durability, guard break, parry window and its punishment, dodge recovery, penalty for repeated dodges | Does any defense option win with no risk? | Camping: guarding or dodging forever |
| atk-08 | Option triangle (선택지 상성) | A matrix of attack, throw or grab, guard, and dodge | Does one option beat all the others? (`choice_calc.py dominance` on the matrix) | One answer to every situation |
| atk-09 | Advantage on block (가드 시 유불리) | Per attack: recovery against guard stun, a punishable flag | Is it clear which attacks are safe on block and which are punishable? Consistency: is each safe attack paid for with another weakness (slow start, short reach)? | Attacks that are both safe and strong. Or every attack punishable, so offense stops |
| atk-10 | End of an offense (공격 흐름의 끝) | Large recovery on the last hit, resource cost, cooldown | Does continuous offense stop somewhere, so the other side gets a turn? | One-sided fights |
| atk-11 | Just-timing reward (저스트 타이밍 보상) | Window length, reward (slow motion, score multiplier, reflect), anti-spam rule | Does the reward match the risk? (`choice_calc.py breakeven`) | Spamming gets the reward without the risk |
| atk-12 | Stamina (스태미나) | Cost per action, regeneration conditions, what is blocked at zero, whether the gauge is visible | Does managing the resource add a decision, or only a delay? | A hidden gauge. A zero state that blocks defense with no warning |
| atk-13 | Readable cause of death (사망 원인 가독성) | Distinct reactions and effects per damage source, a warning before lethal states, a hit-direction marker | Can the player tell who hit them, when, and with what (in shooting games, from which direction)? | Deaths that look random lower the will to try again |

Search terms: `Anticipation|Startup|Active|Recovery|WindUp`, `HitStop|Hitstop|TimeDilation`, `HitReact|Flinch|Knockdown|Launch`, `Poise|Stagger|SuperArmor|Armor`, `Knockback`, `Invincib|Invulner|IFrame`, `Guard|Block|Parry|Dodge`, `Stamina`.

## 3. Enemies and AI (적·AI)

| ID | Mechanism (메카닉) | Where it shows (흔적) | Check question (점검 질문) | Failure shape (실패 모양) |
|---|---|---|---|---|
| enemy-01 | Rules you can read from the look (외형으로 읽히는 규칙) | Visual spec per enemy type, state-to-visual changes (stunned, armored, open), a visible attack origin | Does the look match the rule (what can be touched, what flies, what is open)? Can it be read from every camera angle? | A look that promises one rule and a hit volume that follows another |
| enemy-02 | Telegraph (공격 전조) | Anticipation length per enemy attack, a distinct animation, effect, and sound, an on-screen indicator | Can every enemy attack be read before it lands? Consistency: do stronger attacks, or attacks that close distance fast, have longer or clearer telegraphs? | "Why did that hit me?" Difficulty that comes from unreadable attacks, not from skill |
| enemy-03 | Attack permission (공격 허가) | Central attack slots or tokens, slots per difficulty, a pause while the player is in a combo, positions around the player | Without central control, can several enemies hit at the same moment? | Damage spikes and hit-lock in groups. Groups that clump in one spot |
| enemy-04 | Spacing and speed (간격·속도) | Enemy speed against player speed, distance bands (run when far, walk when near), approach, strafe, and circle patterns, limits on vertical movement | Can the player outrun enemies and choose the next target? Do enemies stop at distances that the player's attacks reach? | Enemies that hover just out of reach. Fast circling enemies that the camera cannot follow |
| enemy-05 | Perception (인지) | Sight cones, hearing radius, time to recognize, alert spread to other enemies, alert states | Is there a gradual zone between unseen and seen, so stealth takes skill? | Instant detection with no warning |
| enemy-06 | Leash (추적 범위) | Aggro radius, leash radius or time, home position, reset rules | Does running away pile up pursuers? | Trains of enemies. Encounter layouts that break after a chase |
| enemy-07 | Roles and mixes (역할·조합) | Size, behavior, and role columns in the enemy table, the role mix per encounter | Do encounters mix roles, so the player must choose an order? | Single-type groups with one fixed solution |
| enemy-08 | Answers to player verbs (플레이어 동작에 대한 적의 반응) | Enemy type × player action matrix (works, blocked, special reaction), how a blocked action is shown | Does each player verb have enemies that make it useful? Is "this does not work" shown? | Player verbs that nothing needs. Blocked actions with no feedback |
| enemy-09 | Showing before telling (적이 먼저 보여 주기) | Placement of enemies that use an ability the player just got | Is a new ability first shown by an enemy or by terrain, before text? | Abilities taught only by text |
| enemy-10 | Boss pattern mix (보스 패턴 구성) | Pattern table (counterable melee, area attack that must be dodged, ranged attack, opening window), phases by health, a weak-point visual code, hints placed before the fight | Is the boss hard because of contrast and tempo, or only because of health and damage? Is the weak-point code the same across the game? | Damage sponges. Secrets with no hint that block progress |
| enemy-11 | Feints that keep a tell (전조가 남는 속임수) | Attacks with similar wind-ups, variable combo counts, variation in attack order | Does each feint keep some tell? | Feints with no tell feel unfair |
| enemy-12 | Ranged accuracy (원거리 명중) | Accuracy by distance, a movement penalty, an accuracy ramp after leaving cover, difficulty multipliers | Can an enemy hit with certainty in the moment it appears? | Perfect accuracy reads as cheating |
| enemy-13 | Target choice (타깃 선택) | Score terms (distance, visibility, threat, state), a penalty for a target that is already chosen, scripted weights | Do enemies spread their attention, or do all of them pick the nearest target? | Everyone attacks one character. No room for decoy tactics |
| enemy-14 | Level data for AI (AI 가 쓰는 레벨 데이터) | Navigation, cover points with direction and height, combat zones, runtime updates for destroyed or moving geometry | Does the level give the AI the information it needs to look smart? | Smart logic with no data looks stupid |
| enemy-15 | Pacing control (긴장 조절) | An intensity value per player, spawn scaling by recent damage and health, rest phases | Is there a rest after a peak? | Endless peaks tire players. Endless calm bores them |
| enemy-16 | Defeat as reward (처치 연출 보상) | Defeat reactions by method and enemy rank, the rule for removing bodies (out of camera view) | Is the strongest feedback given at the moment of a kill? | Bodies that vanish on screen in a realistic game |

Search terms: `Telegraph|Indicator|WindUp`, `AttackToken|AttackSlot|Ticket|Director`, `Perception|Sight|Hearing|Alert`, `Leash|Aggro|Home`, `Formation|Squad`, `Accuracy|Spread`, `Cover`, `EQS|Query`, `Intensity|Spawner|Wave`.

## 4. Level (레벨)

| ID | Mechanism (메카닉) | Where it shows (흔적) | Check question (점검 질문) | Failure shape (실패 모양) |
|---|---|---|---|---|
| level-01 | Player metrics first (플레이어 메트릭 선확정) | A metrics table (speed, jump height and distance, step height, walkable slope, aerial combo height), level gaps and heights derived from it, a reachability check after a metric change | Were level sizes built from fixed metrics? Did a metric change after levels were built? | Gaps that cannot be crossed after tuning. Levels built again |
| level-02 | Safe first appearance (안전한 첫 등장) | The first place each gimmick, enemy, or verb appears, and the failure cost there | Is the first appearance low-risk, before a test under pressure? (frameworks §8) | The first contact is a lethal test |
| level-03 | Failure cost steps (실패 비용 단계) | Results of falls and traps (respawn, damage, death), checkpoint spacing, recovery supply per section, states that cannot be recovered | Does the failure cost rise with progress? Is there never a state that cannot be finished? | Soft-locks. Early sections that punish like late ones |
| level-04 | Optional skill ceiling (선택형 숙련 보상) | Required verbs and optional advanced verbs per section, shortcuts and secrets that need the advanced ones | Can a basic player finish while a skilled player finds faster routes? | Advanced verbs forced early feel like chores |
| level-05 | Hazard rhythm (장애물 리듬) | Hazard period and phase, rest spots between hard parts, the number of things the player must do at once per section | Do hazards have a rhythm that can be learned? Does the number of simultaneous demands rise over the game? | Hazards that look random and must be memorized |
| level-06 | Orientation (방향 감각) | One unique landmark per area, symmetry and repetition, a hierarchy of path widths, the destination visible from entrances, places to look back | Can the player tell where they are and where to go without a map? | Symmetric or repeated spaces. Dependence on signs and text |
| level-07 | Reward trust (보상의 신뢰) | Reward placement next to lethal hazards, lines of rewards that guide the route, reward value against the effort to reach it | Do rewards ever lead into unfair deaths? Is the reward worth the detour? | Trust lost after one bait trap. A chest worth less than the trail that led to it |
| level-08 | Branch functions (분기의 기능) | Each branch tagged as dead end with a reward, gate, shortcut, or full branch, the number of branches in a row | Does every branch have a function, and a cue that tells the options apart? | Identical forks that turn choice into guessing |
| level-09 | Boundaries (경계) | Boundaries that cannot be crossed and boundaries an action can cross, feedback at the ones that cannot be crossed, invisible walls, space only the camera can enter | Does the player get a clear answer when they cannot go somewhere? | Invisible walls with no visible reason |
| level-10 | Arenas (전장) | Closed or open, shape against enemy count, ceiling height against aerial combo height, obstacles that block the camera, wave condition (all defeated, count, time) | Do the arena shape and wave rules fit the tempo the pillar wants? | Arenas you can leave at any time lose tension. Scattered enemies slow the tempo |
| level-11 | Fair hazards (공정한 함정) | Whether a hazard is visible before it triggers, an escape window, damage against the expected health at that point, whether enemies can trigger it too | Can a careful player see each hazard coming? | Deaths that only luck avoids |
| level-12 | Hint ladder (단계별 힌트) | Puzzle hints in steps, information placed near the puzzle | Is there a second and a third hint for players who are stuck? | Puzzles that stop progress |
| level-13 | Beat plan (비트 계획) | A beat chart, encounter length, rest after peaks, the order in which enemy weapons escalate, closing the way back | Is there a plan of peaks and rests across a section? Does play end at the right tension for the next cutscene? | Flat sections. Tension that drops right before a scene that needs it |
| level-14 | Map data layers (맵 데이터 층) | Collision, triggers, navigation, restart points, ground material sounds, and camera data per map | Does each map have every layer that the systems above need? | A mechanic that is designed, with no data to drive it |

Search terms: `Metric|JumpHeight|StepHeight|WalkableFloor`, `Checkpoint|Respawn|Restart`, `KillZ|KillVolume|DeathVolume`, `Landmark`, `Wave|Spawn|Encounter`, `Hint`, `Beat`.

## 5. Collision (충돌 판정)

| ID | Mechanism (메카닉) | Where it shows (흔적) | Check question (점검 질문) | Failure shape (실패 모양) |
|---|---|---|---|---|
| coll-01 | Separate volumes (판정 분리) | Movement capsule, hurt volumes, attack volumes, guard volumes, collision channels or profiles | Are movement, hurt, attack, and guard volumes separate? | One volume doing every job |
| coll-02 | What you see is what is judged (화면과 판정 일치) | Attack volume size against visual size for the camera distance, a generous guard angle, the movement capsule anchor, the foot shape on stairs and ledges | When something looks like a hit, a block, or a step on screen, is it one? | Hits you see that miss. Blocks that still take damage |
| coll-03 | Tunneling at high speed (고속 이동 관통) | Sweeps or traces for projectiles and weapon swings, continuous collision flags, physics substeps, physics rate lowered under load | Can a fast object pass through a thin target in one frame? | Bullets and blades that pass through |
| coll-04 | Map safety (맵 안전장치) | Rules for minimum wall thickness and angle, a kill volume under the map, blocking volumes higher than jump plus aerial combo height | Can a player leave the map or get stuck? | Falling through the world. Leaving arenas with aerial combos |
| coll-05 | Camera-only collision (카메라 전용 충돌) | Camera channel responses (the camera ignores fences and cliffs, and is blocked in narrow corridors) | Can the camera go where the player cannot, where that helps framing? | A camera stuck behind fences |
| coll-06 | Trigger rules (트리거 규칙) | Filters (player only, enemy only, direction), removal after one use | Does each trigger fire only for the right actor and the right number of times? | Events that fire twice or for the wrong actor |

Search terms: `Capsule|Hitbox|Hurtbox|CollisionProfile|Channel`, `Sweep|Trace|CCD|Substep`, `KillZ|BlockingVolume`, `Trigger`.

## 6. Camera (카메라)

| ID | Mechanism (메카닉) | Where it shows (흔적) | Check question (점검 질문) | Failure shape (실패 모양) |
|---|---|---|---|---|
| cam-01 | What success needs is in view (필요한 것이 화면 안에) | Default framing against landing spots, shadows, key interactables, and active attackers, a rule for attacks from off screen | Is everything needed to succeed visible with the default camera? | Sections that are unfair or cannot be cleared only because of the camera |
| cam-02 | Height cues (높이 단서) | A blob or drop shadow under the player and under objects in the air, side or high views in jump sections | Can the player judge height and distance for jumps? | Missed jumps that looked right |
| cam-03 | Lock-on framing (락온 구도) | Shoulder offset by weapon, both characters in frame, rotation blend time (no instant snap over a large angle), release by distance or height, camera settings per target, weak-point priority | Does lock-on keep the target in view without a disorienting cut? | Losing direction when locking onto an enemy behind the player |
| cam-04 | Camera-relative input (카메라 기준 입력) | An input direction latch when the camera cuts or flips, auto recenter, priority of manual input, run and look on the same hand | When the camera changes, does the stick keep moving the character the same way until it is released? | Running back through the door you just came through |
| cam-05 | Context cameras (상황별 카메라) | Camera zone volumes, rails or splines, blend times, tilt hints on slopes and ledges, combat distance by enemy count and distance | Do context cameras show the next goal and the threats? | Camera changes in the middle of a jump |
| cam-06 | Occlusion (가림 처리) | Spring arm probe, character or wall fade, a camera mode for narrow zones | What happens when walls or the character fill the screen? | A camera inside a wall. A hidden character |
| cam-07 | Comfort (멀미·광과민 대응) | Head bob and shake options, rotation speed caps, pitch clamp, no upside-down flips, flash rate limits, field-of-view options | Is there an option for each motion that makes some players sick? | Nausea. Flashing hazards |
| cam-08 | Blind side of an offset camera (오프셋 카메라의 사각) | Shoulder offset side, shoulder swap, threat directions in the level layout | Does the level layout account for the side that the camera hides? | Threats always placed on the blind side |

Search terms: `SpringArm|CameraBoom|SpringArm3D`, `LockOn|Target`, `CameraShake|HeadBob`, `FOV|FieldOfView`, `CameraVolume|CameraZone|Rail|Spline|Blend`, `Fade|Occlu`.

## 7. Common questions (공통 질문)

Use these when no row above settles the question.

1. Experience first: which pillar does this mechanism serve? A mechanism that serves no pillar is an on hold or removal candidate. A pillar that no mechanism serves is an add candidate.
2. Leaving out is a design choice: when the documents say a mechanism was left out on purpose, check that the reason still holds. Do not propose adding it only because other games have it.
3. Every strong option has a price: invulnerability, homing, armor, and parries each need a cost or a limited window.
4. Readable before realistic: when the two conflict, reactions, damage sources, and boundaries must be readable first.
5. More reactions than actions: a verb that gets the same response everywhere is not worth trying. Positive or neutral feedback should come more often than negative feedback.
6. Combine, do not only add: a new element that works together with existing ones (a fight on a moving platform) gives more than a separate new element.
7. Seen before read: information given by space, light, and motion works better than signs and text.
