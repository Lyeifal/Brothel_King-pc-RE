# Trait / Perk System Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/framework/character.rpy` (`Trait` class :207, `Perk` class :303)
> **Data**: `game/core/data/traits/traits.json` (**131 entries**, measured), `game/core/data/perks/perks.json` (**53 entries**, measured)
> **Registries**: `game/core/systems/registry/trait_registry.rpy`, `perk_registry.rpy` (both init -5)

---

## 1. System Responsibilities

### Trait

Defines passive attributes of girls/customers, influencing behavior, dialogue, and interactions:

- **Effect mounting**: a Trait carries a list of `Effect`s (`framework/effects.rpy`) of types `change` (value add/subtract) / `boost` (multiplier) / `special`, evaluated uniformly by `EffectBearer` (one of Girl's base classes).
- **Tags**: the `tags` field is used for picture tag mapping (e.g. hair color → corresponding pictures).
- **Mutual exclusion**: the `opposite` field declares mutually exclusive traits, preventing conflicting coexistence at generation time.
- **Categories**: positive / negative / background, etc., written to the category at registration to support grouped retrieval.

### Perk

Active/passive enhancements for MC and girls:

- **Cost and unlock**: usually consumes skill points/perk points; some have prerequisites.
- **Effect system**: shares the `Effect` mechanism with Traits, applying globally to MC or to an individual girl.

## 2. Class Structure (character.rpy)

| Class | Line | Key capabilities |
|-------|-----:|------------------|
| `Trait` | :207 | `from_dict()` JSON construction, effect list, tags, opposite groups |
| `Perk` | :303 | `from_dict()` JSON construction, cost/unlock, effect list |

Both are batch-constructed from JSON by `DataLoader.load_traits()` / `load_perks()` and registered into `TraitRegistry` / `PerkRegistry` (override semantics: last registration wins, so Mods can override official definitions).

## 3. Runtime Consumers

- **Girl**: the `GirlTraits` component (`girl/girl_traits.rpy`) manages a girl's trait additions/removals; `get_effect()` aggregates effect values along the Girl → equipment → traits chain. `generate_traits` was moved into the component in Phase 2.
- **MC**: perks are selected in the `perks` screen of `screen_progress.rpy`; effects are evaluated through the same Effect system.
- **Data generation**: at girl generation, traits are drawn randomly from the positive/negative trait pools of `traits.json` (exactly one negative trait drawn).

## 4. Inter-System Relationships

```
game/core/data/traits/traits.json (131)
    └─→ DataLoader.load_traits() → TraitRegistry (init -5 registry)
           ├─→ GirlTraits component (generation/add/remove/query)
           ├─→ EffectBearer.get_effect() effect aggregation
           └─→ ModAPI.register_trait() (Mod override/addition)

game/core/data/perks/perks.json (53)
    └─→ DataLoader.load_perks() → PerkRegistry
           ├─→ screen_progress (perks screen)
           └─→ ModAPI.register_perk()
```

## 5. Editor Support

| Editor | Support | Notes |
|--------|---------|-------|
| Girl pack editor `trait_creator.py` | ✅ | Reads/writes traits.json / perks.json with field validation (validators.py) |
| Dev console | ✅ View | Trait/Perk data consistency validated via data_sync |

After modifying the JSON, the game must be restarted for changes to take effect (registries are rebuilt at init time, see [registry.md](registry.md)).

---

## Related Documentation

- [registry.md](registry.md) — the base-class mechanics of TraitRegistry / PerkRegistry
- [data_loader.md](data_loader.md) — JSON loading and fallback
- [girl_components.md](girl_components.md) — the GirlTraits component
- [mod_system.md](mod_system.md) — the API by which Mods register Traits/Perks
