# GameServices Service Container Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/systems/services/service_container.rpy`, `game/core/config/game_config.rpy`
> **Phase**: Phase 1 (service containerization, replacing scattered module-level global singletons)

---

## 1. System Responsibilities

`GameServices` is the game's Service Locator, consolidating singletons that originally existed as module-level global variables — such as `game`, `MC`, `brothel` — into a single container for unified management:

- **Unified registration/retrieval**: `register(key, service)` / `get(key, default)` / `has(key)` / `require(key)` (raises `RuntimeError` when not registered).
- **Typed property access**: IDE-friendly property accessors such as `services.game`, `services.mc`, `services.brothel`.
- **Dependency assertions**: `require_service(key)` (service_container.rpy:137, init -11) lets each init block perform dependency checks at its start.
- **Lifecycle**: `unregister(key)` cleans up on game reset.

Design goals (see file header comment service_container.rpy:6-13): build the container first (init -12); each service registers at its original init level; the old global variables are kept as aliases so existing code keeps working without modification, while new code gradually migrates to `services.xxx`.

## 2. The 11 Registered Services

All registration points below were verified one by one via grep:

| # | Key | Registration location | Timing | Notes |
|---|-----|----------------------|--------|-------|
| 1 | `config` | `game/core/config/game_config.rpy:121` | init -11 | `GameConfig` instance (see §4) |
| 2 | `i18n` | `game/core/systems/services/i18n_service.rpy:121` | init -10 | `I18nService`, wraps Ren'Py `__()` with plural/context/gender support |
| 3 | `event_engine` | `game/core/systems/events/event_engine.rpy:202` | init -4 | `EventEngine` singleton |
| 4 | `girl_files_dict` | `game/core/framework/girl_files_dict.rpy:412` | init -3 | `globalFilesDict` (`GirlFilesDict` instance) |
| 5 | `mod_api_v2` | `game/core/systems/mods/mod_api_v2.rpy:206` | init -3 | `ModAPIV2` singleton |
| 6 | `game` | `game/core/init/start.rpy:245` | Runtime (label start) | Registered after the `Game` instance is created |
| 7 | `calendar` | `game/core/init/start.rpy:246` | Runtime (label start) | `Calendar` instance |
| 8 | `mc` | `game/core/init/start.rpy:339` | Runtime (label start) | `MC` instance (noted `# Phase 1.1`) |
| 9 | `farm` | `game/core/init/start.rpy:557` | Runtime (label start) | `Farm` instance |
| 10 | `brothel` | `game/core/systems/events_dispatcher.rpy:753` | Runtime (brothel creation flow) | `Brothel` instance |
| 11 | `dev_console` | `game/core/tools/dev_console/console_commands.rpy:120` | Runtime (when dev console opens) | In-game developer console |

Note: the container also defines `mod_api` and `data_loader` properties (service_container.rpy:106-119), but **nothing anywhere calls `services.register("mod_api", ...)` or `services.register("data_loader", ...)`** (confirmed by grepping the whole codebase) — these two accessors currently always return `None`; they are interfaces reserved for future migration.

## 3. Init Priority Chain

Priority table (comment at service_container.rpy:152-159 + per-file verification):

```
init -12: GameServices singleton created (service_container.rpy:15) — before all game code
init -11: require_service() helper (service_container.rpy:135)
          GameConfig registers "config" (game_config.rpy:8)
          DataLoader class definition (data_loader.rpy:7)
          EventBridge singleton (event_bridge.rpy:18)
init -10: Registry base class (registry/registry.rpy:5)
          I18nService registers "i18n" (i18n_service.rpy, init -10)
          Goal / GameMode class definitions (framework/goal.rpy:2, systems/gamemodes/gamemode.rpy:6)
init -4:  HookManager (mods/mod_hooks.rpy:4)
          EventEngine registers "event_engine" (events/event_engine.rpy:7)
init -3:  ModAPI (mods/mod_api.rpy:4), ModAPIV2 registers "mod_api_v2" (mods/mod_api_v2.rpy:15)
          GirlFilesDict registers "girl_files_dict" (girl_files_dict.rpy:412)
init -2:  Girl class and its 15 components (framework/girlclass.rpy:7)
          v2 game_saved hook wired into Ren'Py save callbacks (mod_api_v2.rpy:209-219)
init -1:  DataLoader-driven difficulty table JSON override (data_loader.rpy:1309)
init (label start, runtime):
          game/calendar (start.rpy:245-246) → DataLoader.load_all() (start.rpy:258)
          → mc (start.rpy:339) → farm (start.rpy:557) → brothel (events_dispatcher.rpy:753)
```

The first five levels (-12 ~ -2) are the definition phase for classes and singletons; the real entities (game, MC, brothel, etc.) are only registered at runtime in `label start`. This is why the container's `require()` error message hints "Check init priority ordering" — dependencies must be registered in the order shown above.

## 4. GameConfig Centralized Configuration

`GameConfig` (game_config.rpy:10, init -11) is the single source of truth for all tunable parameters:

- **Defaults**: `_load_defaults()` (game_config.rpy:22) covers girl pack directories, image cache (144), auto-save (frequency 200, 12 slots), display (1920×1080), gameplay (difficulty, cheat toggles), i18n default language, performance thresholds, etc.
- **JSON overrides**: `_load_json_overrides()` (game_config.rpy:63) reads `game/custom/config/*.json` and layers them on top of the defaults (`dict.update`), which is Mod-friendly. Missing or invalid JSON is silently ignored (try/except pass).
- **Access**: `services.config.get(key, default)` / `.set(key, value)` / `.all()`, plus common properties (`girl_directories`, `image_cache_size`, `debug`, etc.).

## 5. Decoupling Approach

- **Decoupled from the global namespace**: new code takes dependencies via `services.xxx` instead of declaring `global` everywhere; old global variables are kept as compatibility aliases.
- **Decoupled from init ordering**: each service registers at its original init level; the container does not enforce a unified registration moment, only that the container itself is early enough (-12).
- **Decoupled from callers**: `get(key, default)` lets callers degrade gracefully on optional services (e.g. `dev_console`); `require(key)` is for mandatory services, so ordering mistakes fail loudly at init instead of silently at runtime.

## 6. Known Limitations

- The `mod_api` / `data_loader` properties are not wired (see §2).
- The service container is still a singleton (`GameServices._instance`) without interface abstraction; the interfaces/ directory (`i_event_service.rpy`, `i_girl_service.rpy`, `i_mod_service.rpy`) already contains abstract interface definitions and is the follow-up work for Phase 1.2.

---

## Related Documentation

- [registry.md](registry.md) — the registry system (several services depend on registries)
- [mod_system.md](mod_system.md) — both ModAPI v1/v2 are accessed through the service container
- [event.md](event.md) — registration of the event_engine service and the event bridge
- [girl_components.md](girl_components.md) — Girl componentization (same batch of Phase engineering as the service container)
