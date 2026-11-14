# Scene rules

Read this when you create or edit a `.tscn` file or a UI layout.

## Structure (S)

- **S-1** Author core UI layout in `.tscn` files. Build UI in code only for repeated items (list rows, cards, debug rows), and instance them from an exported `PackedScene` template. (Wraithbound)
- **S-2** One `.tscn` owns one UI area. The main scene instances sub-scenes and keeps only the top-level layout (background, margins, root container). A prototype with one area may stay in one file; split when the second area arrives. Repeated structure used three or more times becomes a sub-scene. (Catena, VNTool)
- **S-3** Node names state their role (`TitleLabel`, `RewardList`). No `Container2` or `Label3`. Generic names are fine for plain spacers. (Catena, VNTool)
- **S-4** Remove dead nodes, unused `sub_resource` and `ext_resource` blocks, and commented-out node blocks. (Catena)
- **S-5** Values that change with game state or language (text, enabled state, modulate, localized strings) are set by the script. The scene keeps an empty or obvious placeholder, so the value does not live in two places. Truly static, non-localized values may stay in the scene. (Catena, VNTool)
- **S-6** Paths deeper than four levels use `unique_name_in_owner` and `%Name`, or a sub-scene split. (Catena, VNTool, Wraithbound)
- **S-7** A swappable scene gets required nodes with `%Name` and optional nodes with `get_node_or_null()`. Write the required nodes down (a scene contract in the project docs or the script header). A missing required node reports with `push_error`. The script never builds a substitute. (VNTool, Wraithbound)

## Styles (Y)

- **Y-1** Colors, font sizes, and StyleBoxes come from a Theme with type variations, not `theme_override_*`. Overrides beat the theme, so a later reskin cannot change them. Positions, sizes, and spacing stay in the scene. (VNTool)
- **Y-2** A resource shared by several nodes in one scene is one `sub_resource`. A resource shared by two or more scenes is a `.tres` file. (Catena)

## Pitfalls

- **S-8** A Container with `anchors_preset = 15` (full rect) gets `grow_horizontal = 2` and `grow_vertical = 2` from the editor. When its content is larger than the anchors, it grows both ways, its top moves above the anchor line, and the parent's clip cuts the top. Set `grow_horizontal = 1` and `grow_vertical = 1` unless you want centered growth, and say so when you do. (Catena)
- **S-9** Children run `_ready` before their parent. A sub-scene's `_ready` must not depend on state the parent loads in its own `_ready` (for example the translation table). Raw keys such as `ui.result` on screen are the symptom. Fix it one of three ways: the parent sets the text after it loads, the state moves to an autoload, or the sub-scene evaluates lazily at first show. (Catena)
