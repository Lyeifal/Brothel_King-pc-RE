# `game/custom/` and `game/core/` Directory Boundaries

> Last updated: 2026-09-11 (verified against code)
>
> **Design principle**:
> - `game/core/` ← **official core content**: core code logic + official JSON data + official templates
> - `game/custom/` ← **user/community content**: girl packs and community mods

---

## Quick overview

```
game/
├── core/                        ← Official core (updated with each release)
│   ├── config/                  ← Core configuration (including screens.rpy, etc.)
│   ├── content/                 ← Official content scripts
│   │   ├── city_events/         ← City events
│   │   ├── day_events/          ← Daily events
│   │   ├── events/              ← Custom event entry point (registered in __init__.rpy)
│   │   ├── main_story/          ← Main story
│   │   ├── scenarios/           ← Scenario pack scripts
│   │   ├── side_stories/        ← Side stories
│   │   └── story_events/        ← Story events
│   ├── data/                    ← Official JSON data repository (with a few fallback .rpy files)
│   ├── framework/               ← Core classes and functions (including the Mod() class, Game/GameServices, etc.)
│   ├── i18n/                    ← Internationalization registration (json_i18n.rpy)
│   ├── init/                    ← Initialization scripts (variables.rpy / settings.rpy / start.rpy)
│   ├── systems/                 ← Subsystems (Registry, DataLoader, services, mods, etc.)
│   ├── templates/               ← Blank templates
│   │   ├── event_template.rpy
│   │   ├── scenario_template.rpy
│   │   ├── girl_template/
│   │   └── mod_template/        ← v2 mod template (register_mod + manifest)
│   ├── tools/                   ← In-game tools (test_runner, dev_console)
│   └── ui/                      ← UI-related (screen_home.rpy, main.rpy, etc.)
│
└── custom/                      ← User/community content (update-safe)
    ├── girls/                   ← Girl packs
    └── mods/                    ← Community mods (v1 and v2 coexist)
```

---

## `game/core/` — Official core

### `core/data/` — Official JSON data repository

This is the core directory of BK Evolution's data-driven architecture. All JSON files are loaded at the `init` phase by `DataLoader` (`game/core/systems/data_loader.rpy`) into the various Registries (`game/core/systems/registry/`).

| Subdirectory | Content | Corresponding editor |
|--------|------|-----------|
| `_schemas/` | JSON Schemas, validating all data files | All |
| `achievements/` | Achievement definitions | `dev_console` |
| `archetypes/` | Jobs/archetypes | `girl_pack_editor` |
| `challenges/` | MC challenges | `dev_console` |
| `chapters/` | Chapter titles and metadata | `dev_console` |
| `classes/` | MC classes/spellbooks | `dev_console` |
| `contracts/` | Contract templates | `dev_console` |
| `customers/` | Customer affixes (color/personality/mood) | `dev_console` |
| `difficulty/` | Difficulty settings | `dev_console` |
| `economy/` | Brothel parameters/taxes and other economy parameters | `dev_console` |
| `events/` | StoryEvent JSON (event_dict.json, 69 events) | `scenario_editor` |
| `farm/` | Farm descriptions/performance text | `scenario_editor` / `dev_console` |
| `fixations/` | Fixations | `girl_pack_editor` |
| `goals/` | Chapter goals | `dev_console` |
| `interactions/` | Interaction menu configuration | `scenario_editor` |
| `items/` | Item definitions | `dev_console` |
| `jobs/` | Job performance data | `dev_console` |
| `meta/` | Meta progression | `dev_console` |
| `minions/` | Minion definitions | `dev_console` |
| `ngp/` | NG+ settings | `dev_console` |
| `perks/` | Perks | `girl_pack_editor` |
| `personalities/` | Girl personalities | `girl_pack_editor` |
| `powers/` | Powers/abilities | `dev_console` |
| `ranks/` | Ranks | `dev_console` |
| `resources/` | Building resources | `dev_console` |
| `rooms/` | Rooms | `dev_console` |
| `sandbox/` | Sandbox origins + sandbox events | `scenario_editor` |
| `scenarios/` | Scenario registry | `scenario_editor` |
| `settings/` | Global settings/text dictionaries/audio registry/picture mappings | `dev_console` |
| `shops/` | Shops (shops.json + shop_economy.json) | `dev_console` |
| `spells/` | Spells + moon phases | `dev_console` |
| `stats/` | Stats | `dev_console` |
| `stories/` | Story event manifest (story_events.json) | `scenario_editor` |
| `traits/` | Traits | `girl_pack_editor` |
| `worlds/` | World/district configuration | `dev_console` |

> **Note**: Some `.rpy` files (`data/items.rpy`, `data/jobs.rpy`, `data/perks.rpy`, `data/powers.rpy`, `data/settings.rpy`, `data/spells.rpy`, `data/quality.rpy`) are still kept as hardcoded fallbacks — the game can still start when JSON is missing. The authoritative data is always the JSON in the subdirectory of the same name. `data/quality.rpy` is a special case: its authoritative data has **moved out of core** and is now provided by the `custom/mods/Item Quality/` mod (this file is the fallback when that mod is disabled or uninstalled). See [`../migration/DATA_MIGRATION.md`](../migration/DATA_MIGRATION.md) for details.

### `core/content/events/` — Custom event script entry point

Put event scripts in `.rpy` format here, suitable for complex logic (multiple branches, custom screens, special animations).

- `__init__.rpy` — registers the events in this directory into `EventRegistry`.
- Mod authors who want to add custom `.rpy` events should load them through the mod system; example events for the core framework can go here.

### `core/content/scenarios/` — Scenario pack scripts

`.rpy` resources for scenario mode (`GameMode.MODE_SCENARIO`). Used together with the `core/data/scenarios/scenarios.json` registry.

### `core/systems/mods/` — Mod mechanism implementation

| File | Description |
|------|------|
| `mod_api.rpy` | v1 `ModAPI` (Registry wrapper + HookManager wrapper) |
| `mod_api_v2.rpy` | v2 `ModAPIV2` (register_mod / manifest / 19 standardized hooks) |
| `mod_hooks.rpy` | Phase 6 `HookManager` (v1 compatibility-layer hook dispatcher) |

See [`MOD_API.md`](MOD_API.md) for details.

### `core/templates/` — Blank templates

Starting points for mod/girl pack authors to copy:

| File/Directory | Purpose |
|----------|------|
| `event_template.rpy` | `.rpy` template for a single event |
| `scenario_template.rpy` | `.rpy` template for a single scenario pack |
| `girl_template/` | Minimal girl pack template, including a sample `_BK.ini` |
| `mod_template/mod_template.rpy` | v2 mod template: `register_mod` + full manifest fields + `register_hook` example |

---

## `game/custom/` — User/community content

Only two kinds of content should appear in this directory: **girl packs** and **mods**. Its design goals:

1. **Update-safe**: not overwritten when the game is updated.
2. **Community-friendly**: players and mod authors only need to care about this layer.
3. **Isolated from core**: official data, code, and templates in `core/` can be refactored freely without affecting `custom/` content.

### `custom/girls/` — Girl packs

Each subdirectory is an independent girl pack:

```
custom/girls/
└── <author>_<work>_<character name>/
    ├── _BK.ini
    ├── portrait/
    ├── profile/
    ├── act/
    └── ...
```

> **Corresponding editor**: Girl Pack Editor (`girl_pack_editor`)

### `custom/mods/` — Community mods

Each subdirectory is an independent mod:

```
custom/mods/
├── Auction House/            ← v2 mod example (auction house, authoritative reference implementation)
│   ├── mod.rpy               # register_mod entry + home menu button screen
│   ├── auction.rpy           # Auction core classes (AuctionLot/AuctionSession/AuctionHouse)
│   └── auction_screens.rpy   # UI screens
├── Item Quality/             ← v2 data-driven mod example (item quality tiers, ex core settings/quality.json)
│   ├── mod.rpy               # register_mod entry (requires: ["items"])
│   ├── quality.rpy           # load_quality_tiers() (init -9, reads JSON and registers tiers)
│   ├── quality.json          # 7 tiers of data (prefixes / price multipliers)
│   ├── tl/chinese_simplified/  # mod-owned translations (prefix entries + manifest strings)
│   └── README.txt            # disable/uninstall semantics and extension how-to
└── Goldo's cool mod/         ← v1 mod tutorial example (includes title.png)
    └── goldo's cool mod.rpy  # Mod(...) construction + events + help_prompts + labels
```

Mods can:

- Register via v1 `Mod()` or v2 `services.mod_api_v2.register_mod()` (both mechanisms coexist, see [`MOD_API.md`](MOD_API.md));
- Register hooks (v2 standardized hooks or the v1 HookManager);
- Add custom traits, perks, events, game modes, origins, scenarios, item quality tiers (`register_quality`);
- Ship their own translations under `<mod>/tl/chinese_simplified/` (see [`MOD_API.md`](MOD_API.md) §7);
- Declare home right-side menu buttons (`home_rightmenu_add_buttons`).

> **Note**: A scenario mod is also a mod; keep it under `custom/mods/` uniformly. Do not create a separate `custom/scenarios/` directory.

---

## Correspondence with the editor suite

The editor suite is located at `tools/bk_editor/` (see [`../tools/TOOLS.md`](../tools/TOOLS.md) and `tools/bk_editor/README.md`).

| Editor | Read path | Write path |
|--------|---------|---------|
| Girl Pack Editor | `custom/girls/*` | `custom/girls/*` |
| Scenario Editor - Events | `core/data/stories/story_events.json`, `core/data/sandbox/events.json` | Same as read path |
| Scenario Editor - Scenarios | `core/data/scenarios/scenarios.json` | `core/data/scenarios/scenarios.json` |
| Dev Console - Achievements | `core/data/achievements/achievements.json` | `core/data/achievements/achievements.json` |
| Dev Console - Difficulty | `core/data/difficulty/difficulty.json` | `core/data/difficulty/difficulty.json` |
| Dev Console - NG+ | `core/data/ngp/ngp_settings.json` | `core/data/ngp/ngp_settings.json` |
| Dev Console - Meta progression | `core/data/meta/meta_progression.json` | `core/data/meta/meta_progression.json` |
| Girl Pack Editor - Trait/Perk | `core/data/traits/traits.json`, `core/data/perks/perks.json` | Same as read path |

---

## Usage advice

### If you are a player

- Girl packs → extract to `custom/girls/`
- Mods → extract to `custom/mods/`
- v1 mods are toggled in the main-menu Mods screen; v2 mods take effect as soon as installed, and deleting the folder deactivates them.
- Don't edit the JSON under `core/data/` by hand; using the editors is safer.

### If you are a mod author

1. **Use v2 for new mods**: copy `core/templates/mod_template/`, and follow the three-file structure of `custom/mods/Auction House/`; only use v1 `Mod()` when you need a "per-save toggle" (refer to Goldo's cool mod).
2. **Modifying official data**: use the editors to change JSON under `core/data/` (validated by Schemas).
3. **Making a girl pack**: copy `core/templates/girl_template/`, rename it, and put it in `custom/girls/`.
4. **Making a scenario mod**: copy `core/templates/scenario_template.rpy` and register it via `core/data/scenarios/scenarios.json`; put the mod scripts in `custom/mods/<your mod>/`.

### If you are a core developer

- When adding a new data category, create a subdirectory under `core/data/`.
- You must add a JSON Schema in `core/data/_schemas/`.
- Add a corresponding `load_xxx()` method in `DataLoader` (`game/core/systems/data_loader.rpy`).
- **Keep the hardcoded fallback**, ensuring the game can still start when JSON files are missing.
- Never put new official JSON data in `custom/data/` (that directory is deprecated and does not exist).

---

## Historical changes

Early in BK Evolution, JSON data was placed in `game/custom/data/`, which conflicted with `custom/` being the "user content" layer. Everything has now been migrated:

| Original location | New location |
|--------|--------|
| `game/custom/data/` | `game/core/data/` |
| `game/custom/events/` | `game/core/content/events/` |
| `game/custom/scenarios/` | `game/core/content/scenarios/` |
| `game/custom/templates/` | `game/core/templates/` |

`game/custom/` now strictly keeps only the `girls/` and `mods/` subdirectories (confirmed against code on 2026-09-11; no other subdirectories such as `custom/config/` exist).

---

## Related documents

- [`MOD_API.md`](MOD_API.md) — complete v1/v2 mod mechanism reference (including the Auction House example walkthrough)
- [`../migration/DATA_MIGRATION.md`](../migration/DATA_MIGRATION.md) — JSON data migration records and fallback inventory
- [`../tools/TOOLS.md`](../tools/TOOLS.md) — tool inventory including the editor suite
- [`../../game/core/templates/mod_template/mod_template.rpy`](../../game/core/templates/mod_template/mod_template.rpy) — v2 mod template
