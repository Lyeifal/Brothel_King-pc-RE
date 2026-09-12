# BK Evolution — Master Roadmap

> Last updated: 2026-09-11 (verified against code)
> **Project**: Brothel King Evolution (data-driven transformation + game architecture refactoring + visual editors)
> **Branch**: `bk-evolution`
> **Tech stack**: Ren'Py 8.2.0, Python 3.9, tkinter (zero third-party dependencies)

This document merges two older roadmaps (`docs/archive/pre-reorg-2026-09/ROADMAP.md`, `BK_EVOLUTION_ROADMAP.md`); every item has been verified against the current code. Commit-by-commit details are tracked in [REFACTORING_PROGRESS.md](REFACTORING_PROGRESS.md) as the source of truth (65 commits accumulated after baseline `b09f55e`, verified via `git log` on 2026-09-11).

**Project goal**: transform BK from a purely code-driven Ren'Py visual novel into a **data-driven, mod-friendly** framework — JSON carries game data, Registry/DataLoader layering, a service container decouples global state, and visual editors lower the barrier to modding.

---

## 1. Overall Progress

| Phase | Content | Status |
|------|------|------|
| Data-driven Phase A–G | Infrastructure, editor GUI, exporting hardcoded data to JSON, girl pack tools, scenario editor, de-hardcoding | ✅ Completed |
| Data-driven Phase H | Full i18n adaptation (`_i18n` suffix convention) | ✅ Completed |
| Data-driven Phase I | System decoupling (UnlockRegistry + Farm/Location separation) | ✅ Completed |
| Refactoring Phase 0 | Emergency fixes (I18N + performance) | ✅ Completed |
| Refactoring Phase 1 | Core architecture: service container + event bridge | ✅ Completed |
| Refactoring Phase 2 | Girl component decomposition (girlclass 5,900 → 3,910 lines) | ✅ Completed |
| Refactoring Phase 7 | Girl component migration completion (3,910 → 1,148 lines, 16 components) | ✅ Done |
| Refactoring Phase 3 | UI architecture: screen extraction (screens.rpy 8,886 → 620 lines) | ✅ Completed |
| Refactoring Phase 4 | I18N system (I18nService) | ✅ Completed |
| Refactoring Phase 5–6 | Mod API v2 + dev tools (Dev Console / Test Runner) | ✅ Completed |
| Follow-up increments | Mod v2 hook wiring + UI integration, auction system mod-ification | ✅ Completed |

---

## 2. Completed (✅)

### 2.1 Data-Driven Phase A–G (2026-06)

- ✅ **Phase A Infrastructure** — `tools/bk_editor/` package structure, `game/core/data/` directory system, JSON Schemas (`_schemas/`), `DataLoader` (`game/core/systems/data_loader.rpy`, 1,319 lines)
- ✅ **Phase B/C Editor GUI** — story event editor (StoryEvent CRUD), origin editor, Trait/Perk CRUD + Effect visualization
- ✅ **Phase D Hardcoded Export** — 131 Traits, 53 Perks, etc. exported to JSON
- ✅ **Phase E Girl Pack Tools** — `_BK.ini` visual editor (8 tabs)
- ✅ **Phase F Scenario Editor** — full Scenario CRUD + JSON Schema validation
- ✅ **Phase G De-hardcoding** — Origin/Trait/Perk/Powers/Challenges/Contracts/Resources/Achievements/Goals/Difficulty and 50+ other domains migrated to `game/core/data/` JSON (full inventory in [migration/DATA_MIGRATION.md](../migration/DATA_MIGRATION.md))
- ✅ **Phase H i18n Adaptation** — 105 JSON data files adapted with `_i18n`; `json_i18n.rpy` switched to a pure `_i18n` suffix scan (whitelist removed)
- ✅ **Phase I System Decoupling** — `UnlockRegistry` (`systems/registry/unlock_registry.rpy`); `Farm.active` became a property that auto-syncs unlock state; `farm.action` mixing fixed

### 2.2 Refactoring Phase 0–3 (2026-09; see REFACTORING_PROGRESS.md for details)

- ✅ **Phase 0 Emergency Fixes** — I18N fixes + performance (image caching, lazy tag parsing, AutoRepair throttling)
- ✅ **Phase 1 Core Architecture**
  - Service container `GameServices` (`systems/services/service_container.rpy`, init -12); 11 services registered (see PROJECT_GUIDE §5)
  - Event bridge EventBridge (`systems/events/event_bridge.rpy`) bridging the legacy event system with the new EventEngine
  - Centralized configuration GameConfig (`config/game_config.rpy`), supporting JSON override via `custom/config/`
  - Init dependency assertions (`init/dependency_graph.rpy` + `require_service()`)
- ✅ **Phase 2 Girl Component Decomposition**
  - `girlclass.rpy` 5,900 → **3,910 lines** (-34%); 15 `girl_*.rpy` components under `framework/girl/` + `__init__.rpy` (16 files)
  - 33 large block methods migrated (stats/mood/economy/sex/dialogue/traits/items/schedule/training/effects/generation/pictures/relationships); migration pattern: implement in component → delegate from the Girl class
- ✅ **Phase 7 Girl component migration completion** (2026-09-11, batches 1-14, 15 commits)
  - `girlclass.rpy` 3,910 → **1,148 lines** (cumulative -81%); 16 components (new `girl_progression.rpy` progression component)
  - Another ~120 methods migrated; fixed the `generate_preferences` double execution and the change_stat skill cap regression; cleaned up 6 stale component copies and 3 duplicate-definition dead shells
  - Lint passed on every batch; the delegation-shell pattern kept all 2,000+ existing call sites unchanged throughout
- ✅ **Phase 3 UI Architecture**
  - `ui/screens.rpy` 8,886 → **620 lines**; 108 screens extracted into 16 files under `ui/screens/`, verified word-for-word identical against the baseline via `temp/verify_extract.py`; currently 112 screen declarations (4 added later, including `mods`)
  - ViewModel layer (`ui/view_models/`)
- ✅ **Phase 4 I18N System**
  - `I18nService` (`systems/services/i18n_service.rpy`): `t()` / `tn()` / `tc()` / `pronoun()` / `possessive()`
  - `plural()` / `article()` are language-aware; language extension via `custom/config/languages.json`
  - JSON `_i18n` migration complete; Chinese covers 27,933/29,367 dialogue blocks
- ✅ **Phase 5–6 Mod API v2 + Dev Tools**
  - `ModAPIV2` (`systems/mods/mod_api_v2.rpy`, 219 lines): versioned manifest, `register_hook`/`execute_hook`/`cancel_hook`
  - **All 16 hook points wired** (2026-09-11, `c6b3fa2`): girl_generated/acquired/sold/runaway, day_starting/ending, night_starting/finished, week_starting, event_triggering/finished, chapter_starting/finished, security_event, game_saved/loaded — 16 `execute_hook` call sites verified by grep
  - **UI integration** (`1788c04`): manifest supports `home_rightmenu_add_buttons`; `get_menu_buttons()`/`get_mod_info()`; the Mods screen shows v2 mods read-only (always-active semantics)
  - Dev Console (`game/core/tools/dev_console/`, Shift+O, developer mode only); Test Runner (`game/core/tools/test_runner.rpy`, Tests button on the main menu, component smoke tests + ModAPIV2 tests)
  - Auction system extracted from `systems/auction` as a sample mod: `game/custom/mods/Auction House/` (converted to v2)

### 2.3 Verification Records

- ✅ Lint passes (historical warnings only); game launches normally to the main menu (baseline verification 2026-09-10)
- ✅ `tools/verify_mod_api.py` static assertions + full stubbed-environment simulation all pass; a bug was found and fixed where `cancel_hook` going through `execute_hook` lost its cancellation semantics
- ✅ Screen extraction verified word-for-word identical (`temp/verify_extract.py`)

---

## 3. In Progress (🚧)

| Item | Description |
|------|------|
| 🚧 Machine translation quality audit | Large batches of machine translations have been re-imported (dialogue and strings); manual spot-checks needed for semantics, tone, and placeholder correctness; tools: `tools/audit_placeholders.py`, `tools/check_excel*.py` |
| 🚧 Story text polish | Readability and name/terminology consistency polish for the Chinese story text |
| 🚧 Legacy save compatibility watch | Post-refactor save format relies on AutoRepair auto-fixing; keep watching player feedback on loading old saves (related to legacy backlog item 6 below) |

---

## 4. Legacy Backlog (⏳, sorted by value)

| # | Item | Current status (verified) | Value / rationale |
|---|------|----------------|-----------|
| 1 | ⏳ Mod v2 `cancel_hook` consumers | All 16 hook points are wired but **purely notification-style**; there is no `cancel_hook` call site anywhere in game flow (only `test_runner.rpy:352` for testing) | Let mods actually intercept/cancel events, closing the loop on v2 hook semantics |
| 2 | ⏳ Fallback dictionary cleanup | `_fallback_*` hardcoded fallbacks still remain in `start.rpy`, `settings.rpy`, and various registries | Remove them once the JSON migration passes 100% regression-free verification, eliminating duplicate data sources |
| 3 | ⏳ `Girl.__init__` split | ~120 lines, attribute initialization + component instantiation, deliberately left as-is | Splitting into per-component `init_*` carries save compatibility risk; low cost-benefit, deferred |
| 4 | ✅ Grouping ~800 lines of small methods — done (Phase 7, 2026-09-11): batches 1-14 migrated all of them by group; girlclass left with only __init__ + delegation shells + 24 live aliases | — |
| 5 | ✅ `change_mood` vs GirlMood ownership — done (Phase 7 batch 1): all 5 mood-cluster method implementations moved into GirlMood; boundaries are now clean | — |
| 6 | ⏳ Legacy save compatibility watch | AutoRepair handles old save fixes; no large-scale negative feedback yet | Long-term watch item; add repair rules if problems surface |

Other known minor issues (track opportunistically, no separate items):
- The `girls` screen in `ui/screens/` has two definitions (`screen_girl_list.rpy:9` and `screen_misc.rpy:80`); confirm whether the override is intentional
- `events_dispatcher.rpy` at 8,611 lines is still the largest legacy file; it can be gradually broken down as the event system evolves

---

## 5. Future Directions (⏳ Aspirational, not committed)

| Direction | Description |
|------|------|
| New language onboarding | The language extension mechanism is ready (`custom/config/languages.json` + font mappings in `translations.rpy`); adding a language only requires translation files + font config |
| Editor enhancements | Scenario editor support for JSON-ifying District/Location/NPC/Shop (currently still hardcoded in `start.rpy`; the editor only offers a read-only viewer); more editor tabs for `core/data/` domains |
| Event system evolution | Once EventEngine fully takes over the legacy `city_events`/`daily_events` paths, retire EventBridge and the event bridge compatibility layer |
| Mod ecosystem | More official sample mods (see `Auction House`); evaluation for retiring the v1 Mod API |

> This section is directional thinking, not committed scheduling; before starting work, append commit records to [REFACTORING_PROGRESS.md](REFACTORING_PROGRESS.md).

---

## 6. Related Documents

| Document | Description |
|------|------|
| [PROJECT_GUIDE.md](PROJECT_GUIDE.md) | Project guide: directory standards, init chain, service access, data-driven architecture |
| [REFACTORING_PROGRESS.md](REFACTORING_PROGRESS.md) | Source of truth for refactoring progress (commit-by-commit chain, component migration details) |
| [../README.md](../README.md) | Documentation hub |
| [../migration/DATA_MIGRATION.md](../migration/DATA_MIGRATION.md) | Full hardcoded → JSON migration inventory |
| [../architecture/README.md](../architecture/README.md) | Index of subsystem architecture docs |
| [../i18n/I18N_ROADMAP.md](../i18n/I18N_ROADMAP.md) | i18n status, conventions, and toolchain |
| [../modding/CUSTOM_DIRECTORIES.md](../modding/CUSTOM_DIRECTORIES.md) | `custom/` vs `core/` directory boundaries |
