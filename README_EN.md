# Brothel King PC — Evolution (Refactored)

> Branch: `bk-evolution` · Ren'Py 8.2.0 / Python 3.9 · Chinese localization complete
>
> [🇨🇳 中文](README.md) | 🇬🇧 English

**Brothel King Evolution** is a data-driven transformation and architecture refactoring of the Ren'Py adult management game *Brothel King*: game data lives in JSON, a Registry + DataLoader layering loads it, a service container decouples global state, and visual editors plus a Mod API lower the barrier for modding and derivative development.

⚠️ **This repository contains only code, documentation, and translations** — no game assets (images/audio), no Ren'Py engine binaries, no girl packs. To run the game, copy this repository into a full game installation.

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
└── renpy/ lib/          # Ren'Py engine & runtime (untracked)
```

## 🚀 Running

Requires a full game installation (with `game/resources/`, `lib/`, Ren'Py engine). Overlay this repository onto the game directory, then:

```powershell
# Lint check
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint

# Launch
.\Brothel_King.exe
```

## 🌐 Translation Workflow

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
