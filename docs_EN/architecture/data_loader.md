# DataLoader System Architecture

> Last updated: 2026-09-11 (verified against code)
> **File**: `game/core/systems/data_loader.rpy` (1,319 lines)
> **Invocation timing**: class defined at `init -11` (data_loader.rpy:7); `DataLoader.load_all()` is called at runtime in `label start` (`game/core/init/start.rpy:258`)
> **Data directory**: `game/core/data/`

---

## 1. System Responsibilities

DataLoader is the unified loading entry point for all JSON-driven content in BK Evolution:

- **Load once per session**: each JSON file is parsed only once per session (`cls._loaded` cache set, data_loader.rpy:18).
- **Safe degradation**: `_load_json_file()` (:41) reads via `renpy.loadable()` / `renpy.open_file()`; when a file is missing or invalid it shows a `renpy.notify()` message and returns `None`, without blocking game startup.
- **Multi-category support**: ~45 `load_*` class methods (:27-1308), covering Trait, Perk, Origin, StoryEvent, SandboxEvent, Scenario, Achievement, Challenge, Difficulty, NGP, Meta, Item, Power, Shop, Spell, MC classes, Minion, Installation, Gossip, dialogue text, recent events, cleaning penalties, treasure thresholds, tax rates, upkeep descriptions, goal UI, security events, event colors, etc.
- **Runtime overrides**: the `init -1` block at the end of the file (data_loader.rpy:1309-1319) uses `load_difficulty()` to override the global difficulty table from JSON.

Core methods:

| Method | Description |
|--------|-------------|
| `DataLoader.load_all()` (:27) | Loads all core categories (traits/perks/origins/story+sandbox events/scenarios/achievements/challenges/difficulty/ngp/meta) |
| `DataLoader.reset_cache()` (:34) | Clears the cache, supporting runtime reload (debugging) |
| `DataLoader._load_json_file(rel_path)` (:41) | Unified safe read; `DATA_DIR = "core/data"` |

## 2. Fallback Mode (still present, not cleaned up)

**DataLoader itself only returns data or None — it never falls back**; fallback logic is scattered across call sites, uniformly following the "JSON first, hardcoded fallback" pattern. Verified fallback points:

| Call site | File:line | Notes |
|-----------|-----------|-------|
| Template/all items | `game/core/data/items.rpy:98-99` | `load_items() or _fallback_template_items / _fallback_all_items` |
| Job performance dict | `game/core/data/jobs.rpy:227` | `perform_job_dict = _fallback_perform_job_dict` |
| Challenge odds | `framework/challenges.rpy:36` | falls back to a hardcoded table when JSON is missing |
| Core entity lookup | `framework/core_entities.rpy:7` | entity lookup table |
| Customer rank/sex act blurbs | `framework/economy.rpy:1894, 1902` | customer rank order, sex act short descriptions |
| UI color mapping / EV gallery | `content/declarations.rpy:292, 1494` | |
| Free girl interaction favor cap | `content/interactions_free.rpy:6` | |
| Loan parameters | `content/story_events/story_events.rpy:14312` | |
| Chapter goals | `init/settings.rpy:101-123` | `_chapter_goals_fallback` + `Goal.from_dict` |
| Security events | `init/settings.rpy:231-240` | `load_security_events()` failure yields `{}` |

**Current assessment**: fallback is a deliberate compatibility strategy rather than a temporary measure (`tools/bk_editor/AGENTS.md` explicitly requires "keep the hardcoded fallback so the game can still start when JSON files are missing"); there is no cleanup plan for now. Calling it "not cleaned up" refers to two copies of the data source coexisting long-term — when modifying data you must be aware of both places.

## 3. Decoupling Approach

- **Decoupled from game logic**: DataLoader only reads JSON and constructs objects; it does not interfere with runtime logic.
- **Decoupled from registries**: the loader knows the registry interface (e.g. `trait_registry.register_trait()`) but does not depend on registry internals; constructed products are handed to registries for management (see [registry.md](registry.md)).
- **Decoupled from the filesystem**: uses Ren'Py `renpy.loadable()` / `renpy.open_file()` instead of native Python IO, so it keeps working in packaged releases (Android/Steam). Exceptions: a few spots such as `customer_affixes.rpy:18` and the chapter goals in `settings.rpy` still use `os.path` + native open — a known inconsistency.

## 4. Inter-System Relationships

```
game/core/data/
    ├─→ traits/traits.json (131 entries)      → load_traits()        → TraitRegistry
    ├─→ perks/perks.json (53 entries)         → load_perks()         → PerkRegistry
    ├─→ sandbox/origins.json                  → load_origins()       → sandbox OriginRegistry
    ├─→ stories/story_events.json             → load_story_events()  → EventRegistry
    ├─→ sandbox/events.json                   → load_sandbox_events()→ EventRegistry
    ├─→ scenarios/scenarios.json              → load_scenarios()     → ScenarioRegistry
    ├─→ achievements/achievements.json        → load_achievements()  → achievement system
    ├─→ difficulty/difficulty.json            → load_difficulty()    → init -1 override of diff_list etc.
    ├─→ ngp/ngp_settings.json                 → load_ngp_settings()  → NGPRegistry
    ├─→ meta/meta_progression.json            → load_meta_progression() → MetaRegistry
    ├─→ goals/goal_ui.json                    → load_goal_ui()       → settings.rpy:520
    ├─→ settings/security_events.json         → load_security_events() → settings.rpy:231
    ├─→ customers/customer_affixes.json       → (does NOT go through DataLoader; customer_affixes.rpy self-loads)
    └─→ other settings/*.json (cleaning/treasure/tax/event colors etc.) → corresponding load_* methods
```

Note the two "exceptions": goals/chapter_goals.json is loaded by `init/settings.rpy` itself (with fallback, see [goal.md](goal.md)); customers/customer_affixes.json is loaded by `systems/customer/customer_affixes.rpy:18` itself (see [customer_affix.md](customer_affix.md)).

## 5. Editor Support

| Editor | Support | Notes |
|--------|---------|-------|
| All editors | ✅ Indirect | Editor-produced JSON → loaded by DataLoader → takes effect in game |
| Dev console `data_sync.py` | ✅ | Batch validation of JSON format/schema |

---

## Related Documentation

- [registry.md](registry.md) — the load targets of DataLoader
- [trait_perk.md](trait_perk.md) — consumers of the traits/perks JSON
- [goal.md](goal.md) — the independent loading path of chapter_goals.json
- [customer_affix.md](customer_affix.md) — another example of self-loaded JSON
- [editor_suite.md](editor_suite.md) — the JSON contract between editors and DataLoader
