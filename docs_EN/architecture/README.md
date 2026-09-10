# BK Evolution System Architecture Documentation

> Last updated: 2026-09-11 (verified against code, bk-evolution branch)

This directory contains the architecture documentation for the core systems of the BK Evolution branch. All paths, class names, line numbers, and hook call sites have been verified one by one against the current code via grep; the pre-reorg snapshots of the old versions are available at `../../docs/archive/pre-reorg-2026-09/architecture/` for comparison.

> **Note**: `classes.rpy` / `functions.rpy` were split long ago into multiple smaller files under `framework/`; any documentation referencing these two file names is outdated.

---

## Subsystem Status Matrix

| Subsystem | Status | Core files | Notes |
|-----------|--------|-----------|-------|
| GameServices service container | 🚧 In progress | `systems/services/`, `config/game_config.rpy` | 11 services registered (init -12 container); `mod_api`/`data_loader` properties not wired; interface abstraction (interfaces/) pending |
| Girl componentization | 🚧 In progress | `framework/girlclass.rpy` (3,910 lines, formerly ~5,900), `framework/girl/` (15 components) | 15/15 component classes in place, 156 `_impl` aliases; some method bodies still in the host class (transitional state) |
| UI screen extraction | ✅ Done | `ui/screens.rpy` (620 lines, formerly 8,886), `ui/screens/` (16 files) | screens.rpy has no screen left, only image/style/label; 16 files split by domain |
| Mod system | 🚧 In progress | `framework/challenges.rpy` (v1 Mod), `systems/mods/` | v1/v2 coexist; all 16 v2 hooks wired (pure notification); `cancel_hook` interception semantics have no call site; the two hook stores are not unified |
| DataLoader / JSON-ification | 🚧 In progress | `systems/data_loader.rpy` (1,319 lines) | ~45 load_* methods; fallback mode deliberately kept (two data sources coexist) |
| Registry | ✅ Done | `systems/registry/` (10 files) | Base class + 8 subclasses + UnlockRegistry; override semantics support Mod replacement |
| Trait / Perk | ✅ Done | `framework/character.rpy`, `data/traits/` (131), `data/perks/` (53) | JSON-driven + GirlTraits component consumption |
| Event system | 🚧 In progress | `framework/interactions.rpy` (StoryEvent), `systems/events_dispatcher.rpy` (8,611 lines), `systems/events/` | EventEngine/EventRegistry in place; **EventBridge old→new sync silently broken because it calls a nonexistent method** (see event.md §2.4) |
| Game / GameMode | ✅ Done | `framework/core_entities.rpy` (Game :19), `systems/gamemodes/` | story/sandbox/scenario modes all registered; modes filtering applied throughout event enqueueing |
| Goal | ✅ Done | `framework/goal.rpy`, `data/goals/chapter_goals.json` (7 chapters) | Loaded independently by settings.rpy (with fallback); 5 goal types gate chapter progression |
| CustomerAffix | ✅ Done | `systems/customer/customer_affixes.rpy`, `data/customers/customer_affixes.json` | Three-dimension affixes + 8 color tiers; self-loaded JSON + hardcoded fallback |
| Girl Pack | ✅ Done | `framework/girl_files_dict.rpy`, `framework/girl_factory.rpy`, `custom/girls/` (102 packs) | GirlFilesDict service-ified; three-layer pack validation |
| Editor suite | ✅ Done | `tools/bk_editor/` (three editors) | Girl pack / scenario / dev console; JSON contracts via DataLoader |
| I18N | 🚧 In progress | `systems/services/i18n_service.rpy`, `i18n/json_i18n.rpy`, `tl/` | I18nService service-ified; translation coverage continuously expanding |

## Document Index

### Infrastructure (new in this batch)

| Document | Content |
|----------|---------|
| [services.md](services.md) | GameServices container, table of 11 registered services, GameConfig, init priority chain |
| [girl_components.md](girl_components.md) | Girl component system: list of 15 components, delegation pattern, `_impl` aliases, lessons from the get_stat double-counting bug |
| [ui_screens.md](ui_screens.md) | UI screen architecture: what remains in screens.rpy + per-file screen inventory of the 16 files in ui/screens/ |
| [mod_system.md](mod_system.md) | v1 Mod class and v2 ModAPIV2 coexistence architecture, registration flow, full table of 18 hook points (call sites verified one by one), HookManager relationship |

### Subsystems (refreshed in this batch)

| Document | System | Core files |
|----------|--------|-----------|
| [data_loader.md](data_loader.md) | DataLoader + fallback mode | `systems/data_loader.rpy` |
| [registry.md](registry.md) | Registry system | `systems/registry/` |
| [trait_perk.md](trait_perk.md) | Trait / Perk | `framework/character.rpy`, `data/traits/`, `data/perks/` |
| [event.md](event.md) | StoryEvent / EventEngine / EventBridge | `framework/interactions.rpy`, `systems/events/`, `events_dispatcher.rpy` |
| [gamemode.md](gamemode.md) | Game / GameMode | `framework/core_entities.rpy`, `systems/gamemodes/` |
| [goal.md](goal.md) | Goal chapter objectives | `framework/goal.rpy`, `data/goals/` |
| [customer_affix.md](customer_affix.md) | CustomerAffix affixes | `systems/customer/`, `data/customers/` |
| [girl_pack.md](girl_pack.md) | Girl pack system | `framework/girl_files_dict.rpy`, `girl_factory.rpy`, `custom/girls/` |
| [editor_suite.md](editor_suite.md) | Editor suite (condensed) | `tools/bk_editor/` |

## Suggested Reading Order

1. Read [services.md](services.md) first to understand the init priority chain — the registration timing of every system depends on it.
2. Then read subsystem docs as your interest dictates; for cross-system topics (Mod, data flow) read [mod_system.md](mod_system.md) and [data_loader.md](data_loader.md).
3. Directory-level file responsibilities are also described in `game/core/README.md`.

---

## Related Documentation

- `game/core/README.md` — game/core directory structure guide
- `tools/bk_editor/README.md` — editor suite usage documentation
- `docs/i18n/` — internationalization documentation
- `docs/tools/` — toolchain documentation
- Old snapshots: `../../docs/archive/pre-reorg-2026-09/architecture/`
