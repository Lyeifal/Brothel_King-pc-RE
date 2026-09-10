# Brothel King Project Guide

> Last updated: 2026-09-11 (verified against code)
> This document is the **single active project guide** for BK Evolution, superseding all old project guides under `docs/archive/`.
> Branch: `bk-evolution`

---

## 1. Project Overview

**Brothel King** is an adult business simulation / visual novel game built on the Ren'Py engine. The player runs a brothel, manages girls, serves customers, upgrades facilities, and explores the story.

- **Engine**: Ren'Py 8.2.0 / Python 3.9
- **Version**: Brothel King Evolution
- **Languages**: English original + Simplified Chinese (`chinese_simplified`)
- **Platforms**: Windows / Linux / macOS
- **Branch**: `bk-evolution`

---

## 2. Root Directory Structure

```
Brothel_King-pc/
├── Brothel_King.exe      # Windows launcher
├── Brothel_King.py       # Python launch script (Ren'Py launcher)
├── Brothel_King.sh       # Linux/macOS launch script
├── lib/                  # Platform Python runtimes (py3-windows-x86_64/ etc.)
├── renpy/                # Ren'Py engine source
├── game/                 # Game scripts and assets (the only game code directory)
├── tools/                # Translation, audit, migration scripts + bk_editor/ editor suite
├── docs/                 # Project documentation (this file's home)
├── temp/                 # Logs, translation temp files, backups
├── README.html           # Project readme (for players)
└── faq.txt               # FAQ (for players)
```

> Runtime logs (`errors.txt`, `log.txt`, `traceback.txt`) are generated in the root after the game runs; tool output is written to `temp/`.

The `game/` root keeps only standard Ren'Py directories and entry assets:

```
game/
├── core/                 # All official code and data (see Section 3)
├── cache/                # Ren'Py compile cache (*.rpyb)
├── custom/               # User/community content: girls/ (girl packs), mods/ (community mods)
├── resources/            # Resources directory
├── saves/                # Save files
├── tl/                   # Translations (chinese_simplified/ etc.)
└── presplash_*.png       # Launch splash images
```

---

## 3. `game/core/` Directory Standard

`game/core/` is the **single canonical location** for official code, data, and content. No `.rpy` scripts live directly in the `game/` root.

`game/core/` currently has 10 directories (plus one `README.md`):

```
game/core/
├── config/        # Ren'Py config and centralized configuration: gui.rpy, options.rpy, screens.rpy,
│                  #   translations.rpy, game_config.rpy (GameConfig service)
├── content/       # Narrative content: dialogue.rpy, interactions.rpy, intro.rpy, declarations.rpy,
│                  #   main_story/, side_stories/, story_events/, city_events/, day_events/,
│                  #   scenarios/, events/
├── data/          # Data-driven JSON repository (40+ domain subdirectories) + a few .rpy data definitions
│                  #   (items.rpy, jobs.rpy, perks.rpy, powers.rpy, settings.rpy)
│                  #   _schemas/ holds JSON Schemas; HARDCODED_DATA_AUDIT.md is the audit record
├── framework/     # Base classes and core entities: girlclass.rpy, character.rpy, core_entities.rpy,
│                  #   world.rpy, interactions.rpy, challenges.rpy, utils.rpy,
│                  #   girl/ (16 Girl component files), pythonlib/ (vendored libraries)
├── i18n/          # json_i18n.rpy — registers JSON `_i18n` fields into the Ren'Py translation system
├── init/          # Startup: start.rpy (game instance creation/service registration), settings.rpy,
│                  #   variables.rpy, dependency_graph.rpy (init dependency assertions)
├── systems/       # Game systems: endday.rpy, events_dispatcher.rpy, data_loader.rpy,
│                  #   data_exporter.rpy, farm.rpy, security.rpy, traits.rpy, perks.rpy,
│                  #   items.rpy, mods/ (mod_api, mod_api_v2, mod_hooks),
│                  #   events/ (event_engine, event_bridge), registry/ (9 registries),
│                  #   services/ (service_container, i18n_service),
│                  #   gamemodes/, customer/, auction/, courtyard/, settlement/
├── templates/     # Developer/mod templates: event_template.rpy, scenario_template.rpy,
│                  #   girl_template/ (_BK.ini template), mod_template/ (v2 mod example)
├── tools/         # In-game tools: dev_console/ (Shift+O console),
│                  #   girl_pack_editor/, test_runner.rpy (bk_test_runner entry)
└── ui/            # UI: screens.rpy (620 lines, only image/style/label declarations remain),
                     screens/ (16 screen files, 112 screen declarations),
                     screen_home.rpy, main.rpy, content_menu.rpy, notify.rpy,
                     view_models/
```

### 3.1 Where Does Code Go — Decision Table

| If it is... | Put it in... | Current examples |
|-------------|---------|----------|
| Character definitions, image declarations, transitions | `content/` | `declarations.rpy`, `intro.rpy` |
| Dialogue strings, interaction menus, story content | `content/` | `dialogue.rpy`, `interactions.rpy`, `main_story/` |
| JSON data files | `data/<domain>/` | `traits/traits.json`, `perks/perks.json`, `achievements/achievements.json` |
| Base classes and core entities | `framework/` | `character.rpy`, `core_entities.rpy`, `girlclass.rpy` |
| Girl component methods | `framework/girl/` | `girl_stats.rpy`, `girl_economy.rpy`, etc. — 15 `girl_*.rpy` files |
| Vendored/backported standard libraries | `framework/pythonlib/` | — |
| Game startup, difficulty selection, game instance creation | `init/` | `start.rpy` |
| Global variables, persistent defaults | `init/` | `variables.rpy`, `settings.rpy` |
| Settlement, event dispatch, end-of-day | `systems/` | `endday.rpy`, `events_dispatcher.rpy` |
| Registries, DataLoader, Mod API | `systems/` | `registry/`, `data_loader.rpy`, `mods/` |
| Service container, translation service | `systems/services/` | `service_container.rpy`, `i18n_service.rpy` |
| UI screens | `ui/screens/` | `screen_home.rpy`, `screen_girl_stats.rpy`, etc. |
| Mod/scenario templates | `templates/` | `mod_template/`, `scenario_template.rpy` |
| In-game debugging tools | `tools/` | `dev_console/`, `test_runner.rpy` |
| Standalone GUI editor (not in-game) | `tools/bk_editor/` (under the project-root `tools/`) | `girl_pack_editor/`, `scenario_editor/`, `dev_console/` |

### 3.2 Core File Quick Reference

| Domain | Core files | Size |
|------|----------|------|
| Girl class (post-refactor) | `game/core/framework/girlclass.rpy` | 3,910 lines (5,900 pre-refactor) |
| Girl components | `game/core/framework/girl/girl_*.rpy` × 15 + `__init__.rpy` | 16 files |
| Trait/Perk/Effect base classes | `game/core/framework/character.rpy`, `effects.rpy` | — |
| Core entities (Game/MC/Calendar etc.) | `game/core/framework/core_entities.rpy` | — |
| Service container | `game/core/systems/services/service_container.rpy` | 159 lines, init -12 |
| Translation service | `game/core/systems/services/i18n_service.rpy` | 121 lines, init -10 |
| Centralized configuration | `game/core/config/game_config.rpy` | 121 lines, init -11 |
| DataLoader | `game/core/systems/data_loader.rpy` | 1,319 lines, init -11 |
| Event engine | `game/core/systems/events/event_engine.rpy` | — |
| Event dispatch | `game/core/systems/events_dispatcher.rpy` | 8,611 lines (legacy large file) |
| End-of-day settlement | `game/core/systems/endday.rpy` | 1,603 lines |
| Mod API v2 | `game/core/systems/mods/mod_api_v2.rpy` | 219 lines |
| Main screen file (post-extraction) | `game/core/ui/screens.rpy` | 620 lines (was 8,886) |
| Screens directory | `game/core/ui/screens/` | 16 files, 112 screen declarations |
| Girl files dictionary | `game/core/framework/girl_files_dict.rpy` | 416 lines, registers a service at init -2 |
| Game startup | `game/core/init/start.rpy` | 1,081 lines |
| Test framework | `game/core/tools/test_runner.rpy` | 379 lines, `label bk_test_runner` |
| i18n JSON registration | `game/core/i18n/json_i18n.rpy` | 274 lines |

---

## 4. Init Priority Chain

Authoritative sources: `game/core/init/dependency_graph.rpy` and the actual `init` declarations in code (grep-verified 2026-09-11):

```
init -12   service_container.rpy    GameServices singleton (services = GameServices())
init -11   game_config.rpy          GameConfig class + registers "config"
init -11   data_loader.rpy          DataLoader class definition
init -11   variables.rpy            early variables
init -10   settings.rpy             girl_directories, config adjustments
init -10   translations.rpy         bk_language_map, font mappings
init -10   i18n_service.rpy         I18nService (registers "i18n" in its later section)
init -5    tag_registry.rpy         Tag registry initialization
init -4    variables.rpy            tag_dict (JSON-loaded), persistent variables
init -4    event_engine.rpy         EventEngine class + registers "event_engine"
init -3    utils.rpy/effects.rpy/dialogue.rpy/economy.rpy/game_systems.rpy
init -3    girl_factory.rpy         get_girl_path, create_girl
init -3    mod_api_v2.rpy           ModAPIV2 class + instantiation + registers "mod_api_v2"
init -2    core_entities.rpy        Game, Main, NPC, Calendar classes
init -2    world.rpy                Brothel, District, Population, etc.
init -2    character.rpy            Trait, Perk, Effect, ItemType, etc.
init -2    girlclass.rpy            Girl class (delegates to components)
init -2    girl_files_dict.rpy      GirlFilesDict instantiation + registers "girl_files_dict"
init -2    challenges.rpy           Spell, MC_challenge, Mod (v1)
init -2    mod_api_v2.rpy           game_saved hook attached to save_json_callbacks
init -1    test_runner.rpy          TestRunner class
init -1    console_commands.rpy     registers "dev_console"
init 0     start.rpy label          creates game / calendar / MC / farm and registers services
           events_dispatcher.rpy    registers "brothel" (where the Brothel instance is created)
```

Dependency assertions: call `require_service("key")` at the top of an init block (defined at `service_container.rpy:137`) to surface ordering errors at startup rather than at runtime.

---

## 5. Service Access (Service Container)

The service container `GameServices` is a global singleton (`service_container.rpy`, init -12). Usage:

```python
services = GameServices.instance()   # or just use the global services
services.register("key", obj)        # register (re-registering overwrites; hot-reload friendly)
services.get("key", default)         # keyed access
services.require("key")              # raises RuntimeError if missing
services.game                        # typed property access
```

Currently **actually registered** keys (verified by grepping `services.register(`; 11 total):

| key | Service object | Registration site | Notes |
|-----|----------|----------|------|
| `config` | GameConfig | `config/game_config.rpy:121` (init -11) | Centralized configuration; supports JSON override via `custom/config/` |
| `girl_files_dict` | GirlFilesDict | `framework/girl_files_dict.rpy:412` (init -2) | Inverted index of girl files + lazy loading |
| `game` | Game | `init/start.rpy:245` | Game instance |
| `calendar` | Calendar | `init/start.rpy:246` | Calendar |
| `mc` | Main | `init/start.rpy:339` | Protagonist |
| `farm` | Farm | `init/start.rpy:557` | Farm |
| `brothel` | Brothel | `systems/events_dispatcher.rpy:753` | Brothel |
| `event_engine` | EventEngine | `systems/events/event_engine.rpy:202` (init -4) | Event engine |
| `i18n` | I18nService | `systems/services/i18n_service.rpy:121` (init -10) | Translation service |
| `dev_console` | DevConsole | `tools/dev_console/console_commands.rpy:120` (init -1) | Debug console |
| `mod_api_v2` | ModAPIV2 | `systems/mods/mod_api_v2.rpy:206` (init -3) | Mod API v2 |

Note: the container also defines `services.mod_api` and `services.data_loader` property accessors, but there are **no corresponding `register` calls** in the code (access returns `None`) — use the actually registered keys above.

Common quick reference:

```python
services.game          # Game instance
services.mc            # Main protagonist
services.brothel       # Brothel
services.farm          # Farm
services.calendar      # Calendar
services.i18n          # I18nService: t() / tn() / tc() / pronoun() / possessive()
services.config        # GameConfig
services.mod_api_v2    # Mod API v2 (16 HOOK_* constants)
services.dev_console   # Dev Console
services.event_engine  # EventEngine
services.girl_files_dict  # Girl files dictionary
```

---

## 6. Data-Driven Architecture

### 6.1 The `from_dict()` / `to_dict()` Contract

Every entity definable from JSON must implement:

```python
@classmethod
def from_dict(cls, d, **resolvers):
    """Build an instance from a JSON-compatible dict."""

def to_dict(self):
    """Serialize to a JSON-compatible dict."""
```

### 6.2 DataLoader + Fallback Pattern

All JSON loading goes through `DataLoader` (`systems/data_loader.rpy`, class defined at init -11):

```python
resource_dict = DataLoader.load_resources(location_resolver=lambda name: globals().get(name)) \
                or _fallback_resource_dict
```

Rules:
1. When JSON is missing or invalid, `load_*` returns `None` and the caller falls back to a hardcoded `_fallback_*` dict/list.
2. **Fallbacks are still kept** today (the JSON migration has not yet passed 100% regression-free verification); cleanup is a legacy backlog item (see ROADMAP).
3. The standard steps for adding a new JSON data source are in [`../tools/bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md): create a subdirectory under `data/` → `DataLoader.load_xxx()` → `DataExporter.export_xxx()` → add a schema under `_schemas/` → add an editor tab in dev_console.

### 6.3 Runtime Resolver Pattern

JSON stores only **string names**; `from_dict()` accepts optional resolvers that resolve them to objects at runtime:

```python
# JSON: {"wood": {"location": "shipyard", ...}}
location = location_resolver("shipyard")   # → shipyard Location object
```

### 6.4 Data Migration Status

The full migration inventory is in [migration/DATA_MIGRATION.md](../migration/DATA_MIGRATION.md) and [architecture/data_loader.md](../architecture/data_loader.md). Covered domains include: traits, perks, achievements, challenges, contracts, resources, difficulty, ngp, meta, goals, scenarios, story_events, sandbox events, etc. Editor data mapping is in the table in [`../tools/bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md).

---

## 7. Editor Suite

Three standalone tkinter editors (zero third-party dependencies; standard library + tkinter + Pillow only), located in `tools/bk_editor/`:

| Editor | Launch command | Audience | Main outputs |
|--------|----------|------|---------|
| Girl pack editor | `python tools/bk_editor/girl_pack_editor/main.py` | Mod authors | `game/custom/girls/`, `core/data/traits/`, `core/data/perks/` |
| Scenario editor | `python tools/bk_editor/scenario_editor/main.py` | Story authors | `core/data/scenarios/`, `core/data/stories/`, `core/data/sandbox/` |
| Dev console (GUI) | `python tools/bk_editor/dev_console/main.py` | Core developers | `core/data/achievements/`, `difficulty/`, `ngp/`, `meta/` |

Architecture convention: the three editors must not reference each other's directories; shared capabilities go through `bk_editor/shared/` uniformly. Details in [`../tools/bk_editor/README.md`](../../tools/bk_editor/README.md) and [`../tools/bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md), plus [architecture/editor_suite.md](../architecture/editor_suite.md).

The game also ships separate in-game tools (not part of the editor suite): Dev Console (`game/core/tools/dev_console/`, Shift+O, developer mode only), in-game girl pack editor (`game/core/tools/girl_pack_editor/`), and Test Runner (`game/core/tools/test_runner.rpy`, Tests button on the main menu, developer mode only).

---

## 8. Naming Conventions

| Convention | Examples | Applies to |
|------|------|----------|
| `PascalCase` | `Achievement`, `Resource`, `DataLoader`, `GameServices` | Class names |
| `snake_case` | `load_challenges()`, `resource_dict` | Functions, variables |
| `UPPER_SNAKE` | `HOOK_GIRL_GENERATED` | Constants, hook names |
| `_fallback_*` | `_fallback_resource_dict` | Hardcoded fallback data |
| `girl_<domain>.rpy` | `girl_stats.rpy`, `girl_mood.rpy` | Girl component files |
| `screen_<domain>.rpy` | `screen_quest.rpy`, `screen_farm.rpy` | Screen files |
| `core/data/<domain>/` | `core/data/traits/`, `core/data/achievements/` | JSON data directories |
| `<domain>_<action>_<tense>` | `girl_generated`, `day_starting` | Mod v2 hook naming |

---

## 9. Cache & Build Hygiene

After modifying any `.rpy` or `.json`, clean the compile cache:

```powershell
# Delete compiled scripts
Get-ChildItem -Path "game" -Filter "*.rpyc" -Recurse | Remove-Item -Force

# Delete bytecode cache
Get-ChildItem -Path "game\cache" -Filter "*.rpyb" | Remove-Item -Force
```

Ren'Py recompiles on next launch. **Never rely on the freshness of `.rpyc` files after changing init block contents or moving files.**

Common verification commands (Windows, via the bundled Python in lib):

```powershell
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --count chinese_simplified
```

---

## 10. Related Documents

| Document | Description |
|------|------|
| [../README.md](../README.md) | Documentation hub (role-based navigation + full index) |
| [ROADMAP.md](ROADMAP.md) | Master roadmap |
| [REFACTORING_PROGRESS.md](REFACTORING_PROGRESS.md) | Source of truth for refactoring progress (commit-by-commit chain) |
| [../architecture/README.md](../architecture/README.md) | Index of subsystem architecture docs |
| [../migration/DATA_MIGRATION.md](../migration/DATA_MIGRATION.md) | Full data migration inventory |
| [../i18n/I18N_ROADMAP.md](../i18n/I18N_ROADMAP.md) | i18n status and toolchain |
| [../modding/CUSTOM_DIRECTORIES.md](../modding/CUSTOM_DIRECTORIES.md) | `custom/` vs `core/` directory boundaries |
| [`../../tools/bk_editor/README.md`](../../tools/bk_editor/README.md) | Editor suite documentation |
