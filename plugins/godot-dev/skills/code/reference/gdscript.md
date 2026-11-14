# GDScript rules

Read this when you write any `.gd` file. Rule ids continue from SKILL.md.

## Types (T)

- **T-1** Give every variable, parameter, and return value a type. Use `:=` only when the right side has a type the parser can infer. A non-inferable `:=` is a parse error. (VNTool, BeforeTheBell, Wraithbound)
- **T-2** Cast Variant results explicitly: `Dictionary.get()`, `ProjectSettings.get_setting()`, `JSON.parse_string()`, `Array` elements. Example: `var gravity: float = float(ProjectSettings.get_setting("physics/2d/default_gravity"))`. A changed setting type then fails at the cast, not later. (Wraithbound)
- **T-3** Compare floats to zero with `is_zero_approx()`, not `== 0.0`. Countdown timers clamp at zero: `t = maxf(t - delta, 0.0)`. (Wraithbound)

## Collections (pitfalls)

- **T-4** Do not put objects into `Array[Dictionary]`. Assigning or appending a typed object fails at runtime with `Unable to convert array index N from Object to Dictionary`, and the array ends up empty. Use `Array[ClassName]`, or a plain `Array` with a comment that states the element type. (Catena)
- **T-5** Nested typed collections are not supported: `Array[Array[int]]`, `Dictionary[String, Array[T]]`, `Dictionary[String, Dictionary]`. Use a plain container with a comment, or a small typed class that holds the inner collection. (Catena)
- **T-6** Typed dictionaries (`Dictionary[String, ClassName]`) exist from Godot 4.4. Where the value is a single class, use the typed form. For a fixed pair of keys (ally and enemy, left and right), two typed fields or a small wrapper class read better than a dictionary. (Catena)
- **T-7** When a type check looks wrong while debugging, find the cause. Do not weaken the annotation to make the error go away. A weakened type brings back silent defaults. (Catena)

## Classes and scripts (K)

- **K-1** If the target script has `class_name`, use the class name. Do not add a `preload` alias for it. Use `preload` only for scripts without `class_name`, and `load(path)` only for paths decided at runtime. (Catena)
- **K-2** After you add a `class_name`, refresh the class cache (`--headless --import`, see `godot-dev:cli`). Until then, `-s` scripts and other headless runs cannot see the name. (VNTool, BeforeTheBell, Jajang, OnceUponATime)
- **K-3** `class_name` only on classes other files use. (BeforeTheBell)
- **K-4** Typed data class shape: `_init` with a default for every argument, so an empty instance is valid. `to_dictionary` and `from_dictionary` only on classes that are saved or loaded. Named static constructors when kinds carry different fields (`RewardOffer.gold(...)`, `RewardOffer.equipment(...)`). A deep copy is `clone()`. Do not override `duplicate`, whose signature differs. (Catena)
- **K-5** Never give an exported Resource field a `.new()` default (`@export var stats: Stats = Stats.new()`). Instances can end up sharing one object. Leave it empty and set it from a `.tres` or explicit assignment. The same applies to nested Resource fields. (Wraithbound)
- **K-6** A Resource with five or more exported fields groups them with `@export_group`. (Wraithbound)

## Names and order (N)

- **N-1** Files `snake_case.gd`, classes `PascalCase`, signals in the past tense (`died`, `item_picked`). (BeforeTheBell)
- **N-2** Member order:
  1. File header and one-line responsibility comment
  2. `extends`, then `class_name`
  3. Signals
  4. Enums, constants, `preload`
  5. `@export` fields
  6. Public variables
  7. `@onready` references
  8. Private variables (`_name`)
  9. Lifecycle: `_init`, `_ready`, `_process`, `_physics_process`, input callbacks
  10. Public methods
  11. Signal handlers
  12. Private helpers

  (Catena, Wraithbound)

## Nodes and autoloads (A)

- **A-1** Reach sibling or distant nodes through `@export` references or `%UniqueName`. No `get_node("../..")` and no path-prefix constants. (BeforeTheBell, Catena, Wraithbound)
- **A-2** A required parent or child: `@onready` with a cast, a null check in `_ready` that calls `push_error`, and a guard (`if body == null: return`) in hot paths. (Wraithbound)
- **A-3** Only scene scripts call autoloads. Model classes and pure `RefCounted` classes do not, so tests can run them without the tree. (BeforeTheBell)
- **A-4** In a `-s` (`--script`) run, autoloads do not exist in `_init()`. In `_initialize()` the nodes are in the root but not ready. They are ready after one `await process_frame`. Code that must work in `-s` tools puts global helpers in static classes. (OnceUponATime, Jajang)

## Process functions (P)

- **P-1** Keep `_physics_process` and `_process` as a guard plus a list of helper calls, so the order reads at a glance. One helper per behavior. (Wraithbound)
- **P-2** A conditional action returns whether it happened: `_apply_jump_if_possible(on_floor) -> bool`. The caller uses the result for follow-up state. (Wraithbound)
- **P-3** Detect "just became X" by keeping last frame's value (`_was_on_floor`) and updating it at the end of the frame. (Wraithbound)
