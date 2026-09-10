# Editor Suite Architecture

> Last updated: 2026-09-11 (verified against code)
> **Directory**: `tools/bk_editor/`
> **Detailed documentation**: [tools/bk_editor/README.md](../../tools/bk_editor/README.md) (this article is only a condensed architecture-level introduction; for details, defer to that README and `tools/bk_editor/AGENTS.md`)
> **Tech stack**: Python 3.9+, tkinter (Pillow optional, installed by default)

---

## 1. System Responsibilities

The Editor Suite is BK Evolution's visual data-editing toolchain, letting non-programmers create Mod content. It follows a **three-independent-editors** architecture:

| Editor | Directory | Target users | Core responsibilities |
|--------|-----------|--------------|----------------------|
| **Girl pack editor** | `girl_pack_editor/` | Mod authors | Batch picture tagging, `_BK.ini` editing, custom Traits/Perks, pack validation |
| **Scenario editor** | `scenario_editor/` | Story/event authors | StoryEvent CRUD, scenario management, map/NPC/shop references, dialogue tag scanning |
| **Dev console** | `dev_console/` | Core developers | Achievements, difficulty, NG+, meta-progression, I18n, data sync |

## 2. Key Conventions

- **No cross-directory imports**: each editor may only import its own `tabs/` submodules, the `bk_editor.shared` shared library, the standard library, and tkinter.
- **Shared library `shared/`**: `paths.py` (project path constants), `json_io.py` (JSON read/write), `widgets.py` (`LabeledEntry`/`EffectEditor`/`JsonTreeview`, etc.), `validators.py` (field validation), `renpy_ref.py` (function-level lazy references to in-game data; **module-level `import renpy` is forbidden**).
- **Unified entry point**: `tools/bk_editor.py`, or each editor's `main.py` for standalone launch.
- **JSON contract**: editors produce JSON → the game-side `DataLoader.load_*()` loads it → registries take effect. After modifying JSON, the game must be restarted (registries are rebuilt at init time).

## 3. Editor ↔ Game Data Mapping (verified against AGENTS.md)

| Editor module | JSON file | Game load point |
|---------------|-----------|-----------------|
| `dev_console/achievement_editor` | `core/data/achievements/achievements.json` | `DataLoader.load_achievements()` |
| `dev_console/difficulty_editor` | `core/data/difficulty/difficulty.json` | `DataLoader.load_difficulty()` |
| `dev_console/ngp_editor` | `core/data/ngp/ngp_settings.json` | `DataLoader.load_ngp_settings()` |
| `dev_console/meta_editor` | `core/data/meta/meta_progression.json` | `DataLoader.load_meta_progression()` |
| `scenario_editor/event_editor` | `core/data/stories/story_events.json`, `core/data/sandbox/events.json` | `load_story_events()` / `load_sandbox_events()` |
| `scenario_editor/scenario_editor_tab` | `core/data/scenarios/scenarios.json` | `DataLoader.load_scenarios()` |
| `girl_pack_editor/trait_creator` | `core/data/traits/traits.json`, `core/data/perks/perks.json` | `load_traits()` / `load_perks()` |

## 4. Known Limitations

- The `_BK.ini` editor strips all comments on save (configparser limitation).
- tkinter PhotoImage cannot preview WebP/AVIF without Pillow (Pillow is installed by default).
- District/Location/NPC/Shop have no JSON (still hardcoded in `start.rpy`); the editors only offer reference viewing and code-snippet generation.
- The Windows console may fail to display non-ASCII filenames correctly (file operations work fine).

---

## Related Documentation

- [tools/bk_editor/README.md](../../tools/bk_editor/README.md) — full usage documentation for the three editors
- [data_loader.md](data_loader.md) — game-side loading of editor JSON
- [registry.md](registry.md) — the registries targeted by editors
- [girl_pack.md](girl_pack.md) — validation logic of the girl pack editor
