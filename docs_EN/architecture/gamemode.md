# Game / GameMode System Architecture

> Last updated: 2026-09-11 (game mode implementations extracted into the "Game Modes" mod)
> **Core files**: `game/core/framework/core_entities.rpy` (`Game` class :19), `game/core/framework/game_systems.rpy` (1,325 lines), `game/core/systems/gamemodes/gamemode.rpy` (framework: base class + registry)
> **Mod files**: `game/custom/mods/Game Modes/` (story/sandbox/scenario mode classes, origin/scenario registries, start-of-game selection screens)
> **Editor support**: ✅ Scenario editor (scenario portion)

---

## 1. System Responsibilities

- **`Game`** (core_entities.rpy:19, `class Game(EffectBearer, Trackable)`): the top-level container of run state — chapters, goals (`self.goals`, initially `chapter_goals[1]`, :34), active Mods (`active_mods`), game mode (`game_mode`), merchants/seen events, etc. Registered at runtime as the service `services.game` (start.rpy:245).
- **`GameMode`** (systems/gamemodes/gamemode.rpy:9, init -10): the mode base class. Each mode defines its rule set, victory conditions, goal channels, and start-of-game behavior (overridable methods such as `on_game_start`, `can_advance_chapter`). It also carries the optional `ui_color` / `ui_icon` card metadata fields consumed by the mode-selection screen.
- **`GameModeRegistry`** (gamemode.rpy:128): the mode registry; `register(mode)` stores by `mode_id`, `get()` / `list_modes()` / `list_mode_instances()` query. The three built-in modes are registered by the "Game Modes" mod (mod.rpy, init -1; the classes live in that mod's `*_mode.rpy` files, init -9).

## 2. The Three Game Modes

The three built-in mode implementations live in `game/custom/mods/Game Modes/` (formerly `game/core/systems/gamemodes/`, extracted 2026-09-11):

| Mode ID | Constant | Registration location | Responsibility |
|---------|----------|----------------------|----------------|
| `story` | `MODE_STORY` | `Game Modes/story_mode.rpy` (registered in mod.rpy) | Main story, 7 chapters of linear progression, gated by chapter goals |
| `sandbox` | `MODE_SANDBOX` | `Game Modes/sandbox_mode.rpy` (registered in mod.rpy) | Sandbox free management; includes `OriginRegistry` (sandbox_mode.rpy:150) providing player origin choices |
| `scenario` | `MODE_SCENARIO` | `Game Modes/scenario_mode.rpy` (registered in mod.rpy) | Custom scenario; includes `ScenarioRegistry` (scenario_mode.rpy:165); scenarios define victory conditions and event sets |

The core `systems/gamemodes/` directory now only holds the framework (`gamemode.rpy`) plus two unrelated systems: `kidnap_system.rpy`, `special_girl_npc.rpy`.

**Fallback when the mod is absent**: `select_game_mode` in start.rpy probes `renpy.has_screen("game_mode_select")`; without the mod it silently sets `game_mode = "story"` and `story_mode = True` (plain story mode). `select_origin` / `select_scenario` are likewise skipped based on screen availability. `Game.game_mode` stays `None` in that case, and `Game.is_story_mode()` returns `True` for `None` (including old saves missing the attribute, protected via getattr) as the backward-compatible default.

## 3. Collaboration with Game

```
label start (init/start.rpy)
  ├─→ services.register("game", game) (:245)
  ├─→ select_game_mode: renpy.has_screen("game_mode_select") probe (mod absent → default story)
  ├─→ mode selection screen (Game Modes Mod/screen_gamemode.rpy, registry-driven cards) → gamemode_registry.get(mode_id)
  ├─→ game.game_mode = <mode instance>; game_mode.on_game_start(game) (stays None if registry lookup fails)
  ├─→ game.goals = chapter_goals[1] (core_entities.rpy:34, story mode)
  └─→ Game.update_mods() (core_entities.rpy:201) handles Mod activation prompts

Chapter progression (events_dispatcher.rpy:1015):
  game.set_goals(chapter_goals[chapter]) → Goal.reached() must all be satisfied before proceeding (see goal.md)
```

Mode filtering runs through the event system: EventEngine compares `event.modes` against `game.game_mode.mode_id` at enqueue time (event_engine.rpy:78-83).

## 4. The Role of game_systems.rpy

`framework/game_systems.rpy` (1,325 lines) is the **function layer** (not a class) related to Game: persistence cleanup in `update_mods` (:158-172, removing deleted Mods from `detected_mods` and syncing `persistent.mods`), `load_quest_pics` (:227), etc. Mod lifecycle management spans two files — core_entities.rpy (activate/deactivate/update) and game_systems.rpy (persistence cleanup) — keep that distinction in mind when reading.

## 5. Mod Integration

- `Game.activate_mod` / `deactivate_mod` / `update_mods` (core_entities.rpy:201-298): per-save Mod lifecycle (see [mod_system.md](mod_system.md) for details).
- The v2 capabilities `game_modes` / `origin` / `scenario` let Mods register new modes/origins/scenarios (`ModAPI.register_game_mode/register_origin/register_scenario` → the corresponding registries).

## 6. Editor Support

| Editor | Support | Notes |
|--------|---------|-------|
| Scenario editor `scenario_editor_tab.py` | ✅ | Reads/writes `core/data/scenarios/scenarios.json` → `DataLoader.load_scenarios()` → ScenarioRegistry |
| Start-of-game mode screen | — | `Game Modes/screen_gamemode.rpy`, registry-driven (`gamemode_registry.list_mode_instances()`), embedded in the game |

---

## Related Documentation

- [goal.md](goal.md) — chapter goals and mode progression gating
- [event.md](event.md) — modes filtering of events
- [mod_system.md](mod_system.md) — Mod lifecycle and new-mode registration
- [services.md](services.md) — the registration timing of the game service
