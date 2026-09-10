# Game / GameMode System Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/framework/core_entities.rpy` (`Game` class :19), `game/core/framework/game_systems.rpy` (1,325 lines), `game/core/systems/gamemodes/` (7 files)
> **Editor support**: ✅ Scenario editor (scenario portion)

---

## 1. System Responsibilities

- **`Game`** (core_entities.rpy:19, `class Game(EffectBearer, Trackable)`): the top-level container of run state — chapters, goals (`self.goals`, initially `chapter_goals[1]`, :34), active Mods (`active_mods`), game mode (`game_mode`), merchants/seen events, etc. Registered at runtime as the service `services.game` (start.rpy:245).
- **`GameMode`** (systems/gamemodes/gamemode.rpy:9, init -10): the mode base class. Each mode defines its rule set, victory conditions, goal channels, and start-of-game behavior (overridable methods such as `on_game_start`, `can_advance_chapter`).
- **`GameModeRegistry`** (gamemode.rpy:128): the mode registry; `register(mode)` stores by `mode_id`, `get()` / `list_modes()` query. The three built-in mode registration points: `story_mode.rpy:63`, `sandbox_mode.rpy:227`, `scenario_mode.rpy:246`.

## 2. The Three Game Modes

| Mode ID | Constant | Registration location | Responsibility |
|---------|----------|----------------------|----------------|
| `story` | `MODE_STORY` | `story_mode.rpy:63` | Main story, 7 chapters of linear progression, gated by chapter goals |
| `sandbox` | `MODE_SANDBOX` | `sandbox_mode.rpy:227` | Sandbox free management; includes `OriginRegistry` (sandbox_mode.rpy:150) providing player origin choices |
| `scenario` | `MODE_SCENARIO` | `scenario_mode.rpy:246` | Custom scenario; includes `ScenarioRegistry` (scenario_mode.rpy:165); scenarios define victory conditions and event sets |

Auxiliary modules: under gamemodes/ there are also `kidnap_system.rpy`, `special_girl_npc.rpy`, and `screen_gamemode.rpy` (mode-selection screen at game start).

## 3. Collaboration with Game

```
label start (init/start.rpy)
  ├─→ services.register("game", game) (:245)
  ├─→ mode selection screen (screen_gamemode.rpy) → gamemode_registry.get(mode_id)
  ├─→ game.game_mode = <mode instance>; game_mode.on_game_start(game)
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
| Start-of-game mode screen | — | `screen_gamemode.rpy` is embedded in the game |

---

## Related Documentation

- [goal.md](goal.md) — chapter goals and mode progression gating
- [event.md](event.md) — modes filtering of events
- [mod_system.md](mod_system.md) — Mod lifecycle and new-mode registration
- [services.md](services.md) — the registration timing of the game service
