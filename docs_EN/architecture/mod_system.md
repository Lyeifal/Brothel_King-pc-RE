# Mod System Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/framework/challenges.rpy` (v1 Mod class), `game/core/systems/mods/mod_api.rpy` (v1 API), `game/core/systems/mods/mod_api_v2.rpy` (v2 API), `game/core/systems/mods/mod_hooks.rpy` (HookManager)
> **Phase**: Phase 5/6 (Mod support)

---

## 1. System Responsibilities

The Mod system lets third-party content coexist via two mechanisms:

- **v1 (Mod class)**: traditional Mods. The author declares a `Mod(...)` instance in their own `.rpy`; it automatically enters `detected_mods` and is enabled/disabled per save by the player in-game, with lifecycle labels (early/init/night/update/load/remove) and persistence via `persistent.mods`.
- **v2 (ModAPIV2)**: declarative manifest registration. The Mod calls `ModAPIV2.instance().register_mod(mod_id, manifest)`, declaring capability requirements, hook tables, dependencies, and UI buttons; installation means permanently active, with no per-save toggle.

The two APIs each have **independent** hook storage (see §5) and do not interfere with each other; v1 remains usable via a compatibility layer.

## 2. The v1 Mod Class

Defined at `game/core/framework/challenges.rpy:370` (`class Mod(object)`).

### 2.1 Constructor Parameters (challenges.rpy:374)

- `name` / `folder` / `creator` / `version` / `pic` / `description` — metadata; `self.path = "mods/" + folder + "/"`.
- Lifecycle labels: `early_label` (game start, before district/brothel setup), `init_label` (after setup), `night_label` (every night event), `update_label`, `load_label` (on save load), `remove_label` (cleanup on disable).
- `chapter_labels` — a table of labels triggered per chapter (1-7).
- `events` — the Mod's event dictionary (all declared events get `ev.mod = self`).
- `home_rightmenu_add_buttons` — buttons for the home right-side menu.
- `help_prompts` — help menu entries.

### 2.2 State Persistence Trick

`__setattr__` / `__getattribute__` overrides (challenges.rpy:441-465): attribute assignments made after the init phase write to the global `mod_settings` (a defaultdict(dict) saved with the save file); reads prefer `mod_settings[self.name]` — this keeps Mod custom attributes across save sessions, while metadata declared during init is not overwritten by every init.

### 2.3 Registration Flow

```
In the Mod author's rpy: Mod(name=..., folder=..., ...) instantiation
        │  end of __init__: detected_mods[self.name] = self   (challenges.rpy:432)
        ▼
detected_mods global dict (initialized empty at init/variables.rpy:2389, filled at declaration time)
        ▼
Game.update_mods() on game start (core_entities.rpy:201):
  - New save: pops a yes_no asking for per-save activation (core_entities.rpy:233-237)
  - Old save: calls activate_mod for Mods already active in persistent.mods (core_entities.rpy:225)
  - game_systems.rpy:158-172 cleans up Mods in detected_mods that no longer exist
        ▼
Game.activate_mod(mod, early=False) (core_entities.rpy:243):
  1. early=True: only calls early_label, then returns
  2. Bulk-registers mod.hooks into HookManager (core_entities.rpy:255-257)
  3. Registers mod.events into EventRegistry (category="mod") (core_entities.rpy:260-262)
  4. Wraps night_label as a daily StoryEvent and appends it (core_entities.rpy:264-265)
  5. Calls init_label
Game.deactivate_mod(mod) (core_entities.rpy:277):
  - Removes from active_mods, hook_manager.unregister_mod(mod), removes the night event, calls remove_label
```

Mod management UI: `screen mods` (ui/screens/screen_quest.rpy:564 onwards) lists `detected_mods`; players activate/deactivate Mods there.

## 3. v2 ModAPIV2

Defined at `game/core/systems/mods/mod_api_v2.rpy:17` (`class ModAPIV2(ModAPI)`, init -3); the singleton `mod_api_v2` is registered as a service (mod_api_v2.rpy:205-206).

- **Capabilities** (mod_api_v2.rpy:30-41): `girl_stats`, `girl_traits`, `economy`, `events`, `dialogue`, `pictures`, `game_modes`, `origin`, `scenario`, `ngp_settings` — validated at registration; unknown capabilities raise `ValueError` outright.
- **`register_mod(mod_id, manifest)`** (:50): the manifest contains `name/version/api_version(must=2)/min_game_version/author/description/requires/hooks/dependencies/home_rightmenu_add_buttons`. Duplicate registration raises an error.
- **Permanently active**: no per-save toggle; disabling = removing the files from `game/custom/mods/`.
- **UI integration**: `get_menu_buttons()` feeds the home right-side menu rendering; `get_mod_info()` feeds the mods screen display.
- **v1 inheritance**: v2 inherits `ModAPI`, so registration wrappers such as `register_trait/perk/tag/dialogue/event/ngp_setting/scenario/origin/game_mode` are likewise available to v2 Mods.

## 4. The 18 v2 Hook Points (all wired, each verified via grep)

Naming convention `<domain>_<action>_<tense>`. Hook constants are defined at mod_api_v2.rpy:187-204. Except for the last two destination hooks, **all are pure notification hooks** — call sites discard the return value via `$ mod_api_v2.execute_hook(...)`, so Mods can only observe, not intercept, game logic (the `cancel_hook` mechanism exists but no in-game call site currently uses it). `girl_destination_list`/`girl_destination_accept` are the exception: return values/arguments wire mod-registered girl destinations into the acquisition flow (see rows 17/18 and the "Courtyard" mod reference implementation).

| # | Constant | Hook name | Call site (file:line) | Context keys |
|---|----------|-----------|-----------------------|--------------|
| 1 | `HOOK_GIRL_GENERATED` | `girl_generated` | `framework/girl_factory.rpy:278` | `girl` |
| 2 | `HOOK_GIRL_ACQUIRED` | `girl_acquired` | `systems/events_dispatcher.rpy:8465` | `girl`, `price`, `context` |
| 3 | `HOOK_GIRL_SOLD` | `girl_sold` | `ui/main.rpy:839`, `ui/main.rpy:1452` | `girl`, `price` |
| 4 | `HOOK_GIRL_RUNAWAY` | `girl_runaway` | `systems/events_dispatcher.rpy:1173` | `girl` |
| 5 | `HOOK_DAY_STARTING` | `day_starting` | `systems/endday.rpy:1498` | `time` |
| 6 | `HOOK_DAY_ENDING` | `day_ending` | `systems/endday.rpy:340` | `time` |
| 7 | `HOOK_NIGHT_STARTING` | `night_starting` | `systems/endday.rpy:403` | `time` |
| 8 | `HOOK_NIGHT_FINISHED` | `night_finished` | `systems/endday.rpy:1431` | `time` |
| 9 | `HOOK_WEEK_STARTING` | `week_starting` | `framework/core_entities.rpy:1937` | `week`, `time` |
| 10 | `HOOK_EVENT_TRIGGERING` | `event_triggering` | `systems/events_dispatcher.rpy:1084` | `event`, `event_type`, `label` |
| 11 | `HOOK_EVENT_FINISHED` | `event_finished` | `systems/events_dispatcher.rpy:1087` | `event`, `event_type`, `label` |
| 12 | `HOOK_SECURITY_EVENT` | `security_event` | `systems/security.rpy:62` | `event_type`, `alert_level` |
| 13 | `HOOK_CHAPTER_STARTING` | `chapter_starting` | `systems/events_dispatcher.rpy:661` | `chapter` |
| 14 | `HOOK_CHAPTER_FINISHED` | `chapter_finished` | `systems/events_dispatcher.rpy:1053` | `chapter` |
| 15 | `HOOK_GAME_SAVED` | `game_saved` | `mods/mod_api_v2.rpy:215` (via `renpy.config.save_json_callbacks`, registered at :209-219) | — |
| 16 | `HOOK_GAME_LOADED` | `game_loaded` | `systems/events_dispatcher.rpy:191` | — |
| 17 | `HOOK_GIRL_DESTINATION_LIST` | `girl_destination_list` | `systems/events_dispatcher.rpy:8403` | `girl`, `at_working_cap`; callbacks return `[{"id", "text", "available"}]` |
| 18 | `HOOK_GIRL_DESTINATION_ACCEPT` | `girl_destination_accept` | `systems/events_dispatcher.rpy:8497` | `girl`, `destination` |

For Mod-side usage see the template `game/core/templates/mod_template/mod_template.rpy:47-53`: `api.register_hook(api.HOOK_GIRL_GENERATED, on_girl_generated)`, with callback signature `callback(context: dict)`.

## 5. HookManager (mod_hooks.rpy) and Its Relationship to v2 Hooks

`HookManager` (mod_hooks.rpy:6, init -4, singleton `hook_manager`) is the **central dispatcher of the v1 era**:

- Stores `{hook_name: [(callback, mod), ...]}`, invokes in registration order, logs exceptions in developer mode.
- v1 Mods bulk-register via the `mod.hooks` dict on activation (core_entities.rpy:255-257); `ModAPI.hook()` (mod_api.rpy:66-68) also points at it.
- On Mod deactivation, `hook_manager.unregister_mod(mod)` cleans up everything.

**Current v1 hook call sites** (verified via grep):

| Hook name | Call site | Scenario |
|-----------|-----------|----------|
| `on_day_end` | `systems/endday.rpy:337` | Day-end settlement_ctx |
| `on_settlement_girls_ready` | `systems/endday.rpy:555` | Girl phase ready |
| `on_settlement_end` | `systems/endday.rpy:1587`, `systems/settlement/settlement_pipeline.rpy:104` | Settlement finished |
| `on_day_start` | `systems/endday.rpy:1588` | New day starts |
| `pre_settlement_phase` / `pre_settlement_<phase>` | `systems/settlement/settlement_pipeline.rpy:76-77` | Before each phase |
| `post_settlement_<phase>` / `post_settlement_phase` | `systems/settlement/settlement_pipeline.rpy:84-85` | After each phase |
| `on_settlement_start` | `systems/settlement/settlement_pipeline.rpy:97` | Settlement start |
| `on_event_trigger` | `systems/events/event_engine.rpy:183` (EventEngine.on_event_trigger) | Event trigger |

How the two coexisting systems relate:

```
v1 Mod (challenges.rpy)
  └─ mod.hooks ──→ HookManager (mod_hooks.rpy) ──→ on_day_end / on_settlement_* / on_event_trigger
v2 Mod (manifest hooks + register_hook)
  └─ _mod_hooks (mod_api_v2.rpy:46, independent storage!) ──→ the 18 hooks such as girl_generated (girl_destination_list/accept are interactive)
```

Two things to note:

1. **Fully separate storage**: v2's `register_mod` writes manifest hooks into `ModAPIV2._mod_hooks` (mod_api_v2.rpy:88-89) without going through HookManager; conversely, v1 hooks like `on_day_end` have no corresponding constants on the v2 side.
2. **HookManager's `invoke_first` supports overriding default behavior** (mod_hooks.rpy:67), but all current v1 call sites use `invoke`, so in practice it likewise degrades to pure notification.

## 6. Backward Compatibility and Known Limitations

- v1 Mods keep their original behavior entirely; the `ModAPI` (v1) and `ModAPIV2` singletons are independent of each other.
- v2 hook naming (`girl_generated`) is stylistically inconsistent with v1 (`on_girl_generate`) — a historical leftover; new Mods should use the v2 constants.
- The `game_saved` hook is implemented via `renpy.config.save_json_callbacks` with a duplicate-registration guard (mod_api_v2.rpy:218).
- v1 hook points are few and concentrated in the settlement pipeline; v2 hook points cover the girl/event/chapter/day-night/save full lifecycle.

---

## Related Documentation

- [services.md](services.md) — mod_api_v2 service registration
- [registry.md](registry.md) — the targets of content registered by Mods via the API
- [event.md](event.md) — event-system context for the on_event_trigger / event_triggering hooks
- [gamemode.md](gamemode.md) — game_modes / scenario / origin among the v2 capabilities
