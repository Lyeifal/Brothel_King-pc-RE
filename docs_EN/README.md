# Brothel King — Documentation Hub

> Last updated: 2026-09-11 (verified against code)
> Branch: `bk-evolution` (Brothel King Evolution / Ren'Py 8.2.0)

This directory is the **single active documentation repository** for the BK Evolution project. All documents reflect the current codebase; outdated document snapshots are kept in [archive/](../docs/archive/) — their content is obsolete, **do not cite them**.

---

## Navigate by Role

### 🎮 Players

Game instructions and FAQs are not in `docs/`; they live in the project root:

- [`../README.html`](../README.html) — Project introduction (HTML)
- [`../faq.txt`](../faq.txt) — Frequently asked questions

### 🧩 Mod Authors

| Document | Description |
|------|------|
| [modding/CUSTOM_DIRECTORIES.md](modding/CUSTOM_DIRECTORIES.md) | Directory boundaries between `game/custom/` and `game/core/`: girl packs go in `custom/girls/`, community mods in `custom/mods/` |
| [architecture/girl_pack.md](architecture/girl_pack.md) | Girl pack system architecture (`_BK.ini` format, loading flow) |
| [architecture/event.md](architecture/event.md) | StoryEvent / EventEngine event system architecture |
| [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) | Data-driven architecture and JSON data conventions (must-read for mod data extensions) |
| [`../tools/bk_editor/README.md`](../tools/bk_editor/README.md) | Editor suite usage (girl pack / scenario / data editing) |

Status of the mod interfaces: v1 `Mod()` (`game/core/framework/challenges.rpy`) and v2 `ModAPIV2` (`game/core/systems/mods/mod_api_v2.rpy`, 19 hook points wired) coexist; the v2 template is in `game/core/templates/mod_template/`, and sample mods are `game/custom/mods/Auction House/` (UI-style) and `game/custom/mods/Item Quality/` (data-style, with its own `tl/` translations).

### 🌐 Translators

| Document | Description |
|------|------|
| [i18n/I18N_ROADMAP.md](i18n/I18N_ROADMAP.md) | The single active i18n reference: current status, `_i18n` suffix convention, roadmap |
| [i18n/BEST_PRACTICES.md](i18n/BEST_PRACTICES.md) | i18n coding standards (`__()` / `_()` wrapping rules, placeholder constraints) |
| [i18n/TRANSLATION_STATUS.md](i18n/TRANSLATION_STATUS.md) | Chinese translation completion plan and coverage snapshot (2026-06; some figures have since been refreshed by machine translation) |
| [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) § Translation Workflow | The standard translation pipeline (extract → xlsx → re-import → lint) |

### 🏗️ Core Developers

| Document | Description |
|------|------|
| [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) | **The single active project guide**: directory standards, init priority chain, service container, data-driven architecture |
| [project/ROADMAP.md](project/ROADMAP.md) | Master roadmap: completed / in progress / legacy backlog / future directions |
| [project/REFACTORING_PROGRESS.md](project/REFACTORING_PROGRESS.md) | Source of truth for refactoring progress: commit-by-commit chain (60+ commits after baseline `b09f55e`), component migration details |
| [architecture/README.md](architecture/README.md) | Index of subsystem architecture docs (DataLoader, events, girl packs, registries, etc.) |
| [migration/DATA_MIGRATION.md](migration/DATA_MIGRATION.md) | Full inventory of the hardcoded → JSON data migration |

### 🛠️ Tool Users

| Document | Description |
|------|------|
| [architecture/editor_suite.md](architecture/editor_suite.md) | Editor suite (three-part architecture) design and data file mapping |
| [`../tools/bk_editor/README.md`](../tools/bk_editor/README.md) | Editor suite (tkinter GUI) usage |
| [`../tools/bk_editor/AGENTS.md`](../tools/bk_editor/AGENTS.md) | Editor development conventions (for those maintaining editor code) |

`tools/` also contains many translation/audit scripts (`audit_placeholders.py`, `export_empty_to_xlsx.py`, `i18n_lint.py`, `verify_mod_api.py`, etc.); see [i18n/I18N_ROADMAP.md](i18n/I18N_ROADMAP.md) and [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) for usage.

---

## Full Document Index

### Project Level (project/)

| Document | Description |
|------|------|
| [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) | Project guide: directory standards, core file quick reference, init chain, service access, data-driven architecture, editor suite, naming conventions, cache hygiene |
| [project/ROADMAP.md](project/ROADMAP.md) | Master roadmap (merged from two older roadmaps, refreshed against current code) |
| [project/REFACTORING_PROGRESS.md](project/REFACTORING_PROGRESS.md) | Source of truth for refactoring progress: Phase 0–6 commit-by-commit chain, Girl component migration details, screen extraction records |

### Architecture (architecture/)

| Document | Description |
|------|------|
| [architecture/README.md](architecture/README.md) | Architecture doc index and core file cross-reference |
| [architecture/data_loader.md](architecture/data_loader.md) | DataLoader: JSON loading, fallback mode, each load_* method |
| [architecture/registry.md](architecture/registry.md) | Registry layer: Trait/Perk/Tag/Dialogue/Event/NGP/Meta/Unlock registries |
| [architecture/event.md](architecture/event.md) | StoryEvent / EventEngine / EventRegistry event system |
| [architecture/gamemode.md](architecture/gamemode.md) | GameMode / GameModeRegistry (story / sandbox / scenario) |
| [architecture/girl_pack.md](architecture/girl_pack.md) | Girl pack system: `_BK.ini`, picture tags, loading and validation |
| [architecture/goal.md](architecture/goal.md) | Goal / chapter objective system |
| [architecture/trait_perk.md](architecture/trait_perk.md) | Trait / Perk / Effect system |
| [architecture/customer_affix.md](architecture/customer_affix.md) | Customer / CustomerAffixes / PreferenceMatrix |
| [architecture/editor_suite.md](architecture/editor_suite.md) | Editor suite three-part architecture (girl_pack / scenario / dev_console) |

### Internationalization (i18n/)

| Document | Description |
|------|------|
| [i18n/I18N_ROADMAP.md](i18n/I18N_ROADMAP.md) | The single active i18n reference: status, `_i18n` convention, toolchain |
| [i18n/BEST_PRACTICES.md](i18n/BEST_PRACTICES.md) | i18n coding best practices |
| [i18n/TRANSLATION_STATUS.md](i18n/TRANSLATION_STATUS.md) | Chinese translation completion plan (2026-06 snapshot) |

### Modding (modding/)

| Document | Description |
|------|------|
| [modding/CUSTOM_DIRECTORIES.md](modding/CUSTOM_DIRECTORIES.md) | Directory boundary notes for `game/custom/` and `game/core/` |

### Migration (migration/)

| Document | Description |
|------|------|
| [migration/DATA_MIGRATION.md](migration/DATA_MIGRATION.md) | Hardcoded data → JSON migration inventory (source files, target paths, status) |

### Tools (tools/)

> This directory is currently empty, reserved for tool script documentation. For the editor suite docs see [`../tools/bk_editor/README.md`](../tools/bk_editor/README.md).

### Archive (archive/) — ⚠️ Outdated, do not cite

| Entry | Description |
|------|------|
| [archive/pre-reorg-2026-09/](../docs/archive/pre-reorg-2026-09/) | Snapshot of old docs from before the 2026-09 documentation reorganization (old PROJECT_GUIDE / ROADMAP / BK_EVOLUTION_ROADMAP / I18N series, etc.), kept for historical reference only |
| [archive/PROJECT_GUIDE_V3.md](../docs/archive/PROJECT_GUIDE_V3.md) | An even earlier project guide (Phase 6 era) |
| [archive/I18N_PLAN.md](../docs/archive/I18N_PLAN.md), [archive/I18N_REFACTOR_PLAN.md](../docs/archive/I18N_REFACTOR_PLAN.md), [archive/i18n_progress.md](../docs/archive/i18n_progress.md) | Old i18n plans and progress (content now consolidated into [i18n/I18N_ROADMAP.md](i18n/I18N_ROADMAP.md)) |

---

## Related Documents

- [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) — Project guide (recommended first read)
- [project/ROADMAP.md](project/ROADMAP.md) — Master roadmap
- [project/REFACTORING_PROGRESS.md](project/REFACTORING_PROGRESS.md) — Source of truth for refactoring progress
