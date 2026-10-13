# Brothel King PC — Evolution (Refactored)

> Branch: `bk-evolution` · Ren'Py 8.2.0 / Python 3.9 · Full Chinese localization
>
> [🇨🇳 中文](README.md) | 🇬🇧 English

**Brothel King Evolution** is a data-driven transformation and architecture refactoring of the Ren'Py adult management game *Brothel King*: game data lives in JSON, a Registry + DataLoader layering loads it, a service container decouples global state, and visual editors plus Mod API v2 lower the barrier for modding and derivative development.

⚠️ **This repository contains only code, documentation, and translations** — no game assets (images/audio), no Ren'Py engine binaries, no girl packs. To run the game, copy this repository into a full game installation.

---

## 🎯 Latest Update (2026-10-13)

This update completes the project's testing, documentation, and example code, making it truly "community-ready":

### ✅ New Content

- 📋 **Complete Testing System**
  - Manual testing guide (60+ test items)
  - Integration test suite (8 automated tests)
  - CI/CD scripts (cross-platform)
  - Girl pack validation tool

- 📚 **Comprehensive Developer Documentation**
  - Complete Mod Development Guide (8000+ words)
  - Girl Pack Compatibility Guide
  - Save Format & Migration Documentation
  - CI/CD Setup Guide

- 🎯 **Full-Featured Example Mod**
  - Advanced Pricing System (380 lines, complete implementation)
  - Demonstrates all Mod API core features
  - Detailed comments and learning documentation

**See Details**: [`DELIVERY_DOCUMENT.md`](DELIVERY_DOCUMENT.md) - Complete delivery documentation

---

## ✨ Key Features

| Feature | Description |
|------|------|
| 📦 Data-driven architecture | 131 Traits, 53 Perks, items, achievements, contracts, origins, spells and 50+ other domains migrated from hardcoded Python to `game/core/data/` JSON (with Schema validation) |
| 🧩 Service container | `GameServices` manages 11 core services; EventBridge bridges the legacy and new event systems |
| 👧 Girl componentization | `girlclass.rpy` slimmed from 5,900 to 1,148 lines across 16 component files — all 2,000+ call sites unchanged |
| 🖥️ UI architecture | 108 screens extracted from a single 8,886-line file into 16 files, verified character-for-character identical |
| 🌐 Full Chinese localization | Simplified Chinese at 100% coverage (0 missing dialogue / 0 missing strings); I18nService provides `t()`/`tn()`/`tc()`/`plural()` APIs — adding a language needs only translation files + font config |
| 🔧 Mod API v2 | Versioned manifest, 19 wired hook points (register/execute), UI button injection; two official sample mods: [Auction House](game/custom/mods/Auction%20House/) (UI-style) and [Item Quality](game/custom/mods/Item%20Quality/) (data-style, with its own `tl/`) |
| 🛠️ Dev tools | Dev Console (Shift+O, developer mode), Test Runner (Tests button on main menu), 30+ audit/translation/verification scripts under `tools/` |
| 📝 Visual editors | tkinter editor suite (zero third-party dependencies): girl pack editor (8 tabs), scenario/story event editor, Trait/Perk CRUD |

## 📁 Repository Layout

```
├── game/
│   ├── core/            # Core framework: service container, data loading, events, UI, i18n, mod system, dev tools
│   │   ├── data/        # JSON game data (with _schemas/ validation)
│   │   ├── framework/   # Componentized Girl framework (16 components under girl/)
│   │   ├── systems/     # Systems: auction, items, traits, security, registries…
│   │   ├── ui/          # Screens (16 extracted files) + ViewModels
│   │   └── tl/          # In-game translations (chinese_simplified)
│   ├── custom/          # User content: girls/ girl packs, mods/ community mods (untracked)
│   ├── resources/       # Game assets (untracked — provide your own)
│   └── tl/              # Ren'Py translation directory (strings.rpy etc.)
├── docs/                # Chinese documentation
├── docs_EN/             # English documentation (mirror of docs/)
├── tools/               # Translation/audit/verification scripts + bk_editor suite
├── renpy/               # Ren'Py engine (untracked— provide your own) 
└── lib/                 # runtime (untracked— provide your own)
```

## 🚀 Quick Start

### Running the Game

Requires a full game installation (with `game/resources/`, `lib/`, Ren'Py engine). Overlay this repository onto the game directory, then:

```powershell
# Launch the game
.\Brothel_King.exe

# Or use Python launcher
python Brothel_King.py
```

### Developer Quick Validation

```powershell
# 1. Run automated test suite
.\tools\ci\run_tests.ps1  # Windows
./tools/ci/run_tests.sh    # Linux/macOS

# 2. Lint check
python Brothel_King.py . lint

# 3. Verify girl pack compatibility
python tools/test_girl_packs.py

# 4. In-game testing (developer mode)
# Main menu → Tests button
```

### User Guide

1. **Players**: Just launch the game, Chinese translation is complete
2. **Mod Developers**: Read [`docs/modding/MOD_DEVELOPMENT_GUIDE.md`](docs/modding/MOD_DEVELOPMENT_GUIDE.md)
3. **Girl Pack Authors**: Read [`docs/modding/GIRL_PACK_COMPATIBILITY.md`](docs/modding/GIRL_PACK_COMPATIBILITY.md)
4. **Contributors**: Read [`docs/project/PROJECT_GUIDE.md`](docs/project/PROJECT_GUIDE.md)

---

## 🔧 Mod API v2 | Complete Mod Ecosystem

### 19 Standardized Hooks

Allows mods to intercept game logic at the following points:

| Category | Hooks |
|------|------|
| Girl-related | girl_generated, girl_acquired, girl_sold, girl_runaway |
| Time cycle | day_starting, day_ending, night_starting, night_finished, week_starting |
| Events | event_triggering, event_finished, security_event |
| Chapter | chapter_starting, chapter_finished |
| System | game_saved, game_loaded, item_generated |
| Interaction | girl_destination_list, girl_destination_accept |

### Example Mods

| Mod | Type | Description |
|-----|------|------|
| **Example - Price Override** | Full-featured | Custom pricing system (380 lines, fully commented) |
| Item Quality | Data-driven | Item quality system (with translations) |
| Auction House | UI-driven | Auction system |
| Game Modes | Complex | Game mode framework |

### Create Your First Mod in 5 Minutes

```python
## game/custom/mods/My Mod/mod.rpy

init -1 python:
    api = ModAPIV2.instance()
    
    api.register_mod("my_mod", {
        "name": "My First Mod",
        "version": "1.0.0",
        "api_version": 2,
        "description": __("My first mod"),
    })
    
    def on_day_start(context):
        renpy.notify("A new day begins!")
    
    api.register_hook(api.HOOK_DAY_STARTING, on_day_start)
```

**Complete Tutorial**: [`docs/modding/MOD_DEVELOPMENT_GUIDE.md`](docs/modding/MOD_DEVELOPMENT_GUIDE.md)

---

## 🧪 Testing & Quality Assurance

### Automated Tests

```powershell
# Run full test suite (recommended)
.\tools\ci\run_tests.ps1  # Windows
./tools/ci/run_tests.sh    # Linux/macOS

# Run individual tests
python Brothel_King.py . lint                 # Syntax check
python tools/verify_mod_api.py                 # Mod API validation
python tools/test_girl_packs.py                # Girl pack compatibility
```

### In-Game Testing

Developer mode:
- Main menu → **Tests** button
- Run component and integration tests
- Press `Shift+O` for developer console

### Test Coverage

- ✅ Syntax check (Ren'Py Lint)
- ✅ Translation coverage check (95%+)
- ✅ Mod API validation (19 hooks)
- ✅ Girl pack format validation (102 packs)
- ✅ Component unit tests (5 components)
- ✅ Integration tests (8 workflows)

**Complete Testing Guide**: [`docs/testing/MANUAL_TEST_GUIDE.md`](docs/testing/MANUAL_TEST_GUIDE.md)

---

## 📚 Documentation Navigator

### 🚀 Quick Start
| Document | Description |
|------|------|
| [HANDOVER_CHECKLIST.md](HANDOVER_CHECKLIST.md) | **Start here!** Testing and release checklist |
| [DELIVERY_DOCUMENT.md](DELIVERY_DOCUMENT.md) | Complete project delivery documentation |

### 👨‍💻 Developer Documentation
| Document | Description |
|------|------|
| [docs/modding/MOD_DEVELOPMENT_GUIDE.md](docs/modding/MOD_DEVELOPMENT_GUIDE.md) | Complete Mod development guide (must-read) |
| [docs/modding/GIRL_PACK_COMPATIBILITY.md](docs/modding/GIRL_PACK_COMPATIBILITY.md) | Girl pack format and compatibility |
| [docs/architecture/SAVE_FORMAT.md](docs/architecture/SAVE_FORMAT.md) | Save format and migration |
| [docs/modding/MOD_API.md](docs/modding/MOD_API.md) | Mod API reference |

### 🧪 Testing Documentation
| Document | Description |
|------|------|
| [docs/testing/MANUAL_TEST_GUIDE.md](docs/testing/MANUAL_TEST_GUIDE.md) | Complete manual testing guide |
| [docs/testing/CI_SETUP.md](docs/testing/CI_SETUP.md) | CI/CD setup and usage |

### 📖 Project Documentation
| Document | Description |
|------|------|
| [docs/project/PROJECT_GUIDE.md](docs/project/PROJECT_GUIDE.md) | Project guide: directory standards, service access |
| [docs/project/ROADMAP.md](docs/project/ROADMAP.md) | Development roadmap |
| [docs/project/CURRENT_STATUS_SUMMARY.md](docs/project/CURRENT_STATUS_SUMMARY.md) | Current project status |

### 🏗️ Architecture Documentation
| Document | Description |
|------|------|
| [docs/architecture/](docs/architecture/) | Subsystem architecture documentation |
| [docs/migration/DATA_MIGRATION.md](docs/migration/DATA_MIGRATION.md) | Data migration checklist |
| [docs/i18n/I18N_ROADMAP.md](docs/i18n/I18N_ROADMAP.md) | Internationalization roadmap |

---

```powershell
# After adding JSON _i18n fields, sync them into strings.rpy first
python tools/import_json_i18n.py

# Extract empty translations → export to Excel → translate → import
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --empty chinese_simplified
python tools/export_empty_to_xlsx.py
python tools/import_translated_empty.py

# Audit & regression
python tools/audit_json_i18n.py      # JSON _i18n coverage
python tools/audit_placeholders.py   # placeholder consistency
python tools/verify_i18n.py          # missing regression (baseline: 0 missing)
```

## 📚 Documentation

| Document | Description |
|------|------|
| [docs_EN/project/ROADMAP.md](docs_EN/project/ROADMAP.md) | Master roadmap (completed / in progress / backlog) |
| [docs_EN/project/PROJECT_GUIDE.md](docs_EN/project/PROJECT_GUIDE.md) | Project guide: directory standards, init chain, service access, data conventions |
| [docs_EN/architecture/](docs_EN/architecture/) | Subsystem architecture (DataLoader, events, girl packs, registries…) |
| [docs_EN/i18n/I18N_ROADMAP.md](docs_EN/i18n/I18N_ROADMAP.md) | Single active i18n reference |
| [docs_EN/modding/MOD_API.md](docs_EN/modding/MOD_API.md) | Full Mod API documentation |
| [docs_EN/migration/DATA_MIGRATION.md](docs_EN/migration/DATA_MIGRATION.md) | Hardcoded → JSON migration inventory |

## ⚠️ Disclaimer

- This project is **adult content (18+)**, containing nudity and sexual material — for adult players only, for study and research purposes
- This repository contains no game assets or commercial material; original game content remains the property of its developers
- Do not use this project for any commercial purpose

## 📄 License

Code is provided under the license file in this repository (if any). Original game assets remain the property of their developers and are not distributed here.
