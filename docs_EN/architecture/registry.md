# Registry System Architecture

> Last updated: 2026-09-13 (verified against code)
> **Base class**: `game/core/systems/registry/registry.rpy` (init -10)
> **Phase**: Phase 6 (system decoupling and Mod support)

---

## 1. System Responsibilities

Registry is the unified registration center introduced in Phase 6, replacing scattered global dicts (`trait_dict`, `perk_dict`, `event_dict`, `dialogue_dict`, etc.). It provides:

- **Unified API**: `register` / `unregister` / `get` / `get_all` / `get_by_category` / `get_categories` / `clear` / `__contains__` / `__len__` (registry.rpy:37-100).
- **Category management**: the `category` parameter supports group retrieval (e.g. Traits grouped as positive/negative/background).
- **Override semantics**: re-registering logs in developer mode and then overrides — last registration wins, which is exactly the mechanism by which Mods override official content (registry.rpy:42-44).
- **Compatibility proxy**: `_RegistryProxy` (registry.rpy:103-144) wraps a Registry with a dict-like facade, so legacy code using `dict[key]` / `key in dict` / `.get()` works unmodified.
- **Singleton guarantee**: the base class `__new__` caches one instance per subclass (registry.rpy:14-20); every registry has exactly one instance game-wide.
- **No persistence**: all registries are rebuilt at init time and never enter save files.

## 2. Registry Inventory (10 files, all verified)

| Registry | File | Init level | Class definition line | Purpose |
|----------|------|-----------|----------------------|---------|
| `Registry` | `registry.rpy` | -10 | :7 | Abstract base class + `_RegistryProxy` |
| `UnlockRegistry` | `unlock_registry.rpy` | **-9** | :13 | Unlock condition registration |
| `TagRegistry` | `tag_registry.rpy` | -5 | :7 | Picture tag mapping |
| `TraitRegistry` | `trait_registry.rpy` | -5 | :7 | Trait definitions (see [trait_perk.md](trait_perk.md)) |
| `PerkRegistry` | `perk_registry.rpy` | -5 | :7 | Perk definitions |
| `DialogueRegistry` | `dialogue_registry.rpy` | -5 | :7 | Dialogue topic management |
| `EventRegistry` | `event_registry.rpy` | -5 | :7 | Event definitions + runtime queue (see [event.md](event.md)) |
| `NGPRegistry` | `ngp_registry.rpy` | -5 | :7 | NG+ settings |
| `MetaRegistry` | `meta_registry.rpy` | -5 | :7 | Meta-progression / unlocks |
| `QualityRegistry` | `quality_registry.rpy` | -5 | :78 (`QualityTier` value type at :13) | Item quality tiers (`register_quality`; data lives in the `data/quality.rpy` fallback + the "Item Quality" mod) |

Base class at init -10, UnlockRegistry at -9, all other subclasses at init -5. `QualityRegistry` is the only registry shipping its own value type (`QualityTier`); it is also the "framework in core, data in a mod" reference (see [../modding/MOD_API.md](../modding/MOD_API.md) §6.6).

## 3. Decoupling Approach

- **Decoupled from the global namespace**: the old global dicts are replaced by registry singletons, avoiding `KeyError` caused by init-order dependencies.
- **Decoupled from concrete classes**: the base class does not depend on concrete types such as Trait/Perk; it works through a generic interface.
- **Decoupled from legacy code**: `_RegistryProxy` provides a compatibility layer between old code and registries; legacy syntax like `trait_dict[id]` actually goes through the proxy to `TraitRegistry`, so old and new mix transparently.
- **Decoupled from Mods**: Mods only call `ModAPI.register_*()` (see [mod_system.md](mod_system.md)) and never touch registry implementations directly; override semantics naturally support Mods replacing official definitions.

## 4. Inter-System Relationships

```
Registry (base class, init -10)
    ├─→ TagRegistry ──────→ GirlPack / picture tagging / Room
    ├─→ TraitRegistry ────→ DataLoader.load_traits() / Girl (GirlTraits component) / girl_pack_editor
    ├─→ PerkRegistry ─────→ DataLoader.load_perks() / Girl / girl_pack_editor
    ├─→ EventRegistry ────→ DataLoader.load_story_events() / EventEngine / scenario_editor
    ├─→ DialogueRegistry ─→ GirlPack custom dialogue / ModAPI.register_dialogue
    ├─→ NGPRegistry ──────→ dev_console (ngp_editor.py)
    ├─→ MetaRegistry ─────→ dev_console (meta_editor.py)
    ├─→ QualityRegistry ──→ systems/items.rpy (generate_new_item / init_items) / "Item Quality" mod
    └─→ UnlockRegistry ───→ achievement/goal/unlock condition evaluation
```

Call chain: `game/core/data/*.json → DataLoader.load_*() → individual Registries → runtime game systems (Girl / EventEngine / Game / ...)`.

## 5. Editor Support

| Editor | Support | Notes |
|--------|---------|-------|
| Girl pack editor | ✅ | Traits/Perks directly manipulate TraitRegistry/PerkRegistry; tags resolved via TagRegistry |
| Scenario editor | ✅ | Directly manipulates EventRegistry |
| Dev console | ✅ | NGPRegistry, MetaRegistry, UnlockRegistry; `data_sync.py` validates consistency |

---

## Related Documentation

- [data_loader.md](data_loader.md) — the main populator of the registries
- [trait_perk.md](trait_perk.md) — consumers of the Trait/Perk registries
- [event.md](event.md) — the relationship between EventRegistry and EventEngine
- [mod_system.md](mod_system.md) — the targets of ModAPI registration wrappers
