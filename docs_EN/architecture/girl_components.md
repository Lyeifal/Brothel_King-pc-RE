# Girl Component System Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/framework/girlclass.rpy` (3,910 lines, formerly ~5,900 lines), `game/core/framework/girl/` (component package)
> **Phase**: Phase 2 (Girl system refactor — component-based decoupling)

---

## 1. System Responsibilities

The Girl class was originally a ~5,900-line god class. Phase 2 split it into **15 component classes** by domain; each component holds a reference to the Girl instance and is responsible for one focused domain. The `Girl` class itself (girlclass.rpy:26, `class Girl(EffectBearer)`) keeps the state fields, serialization, and not-yet-migrated methods, and delegates the migrated methods.

Key numbers (all verified via grep):

- Component classes: **15** (`game/core/framework/girl/girl_*.rpy`, one class per file, init -2).
- `_impl` aliases: **156** (class-body aliases of the form `_<method>_impl = <method>` inside girlclass.rpy).
- The Girl class retains ~215 methods (counted by `def `), so all 2,000+ existing call sites work unchanged.

> Scope note: if the task's figure "17" refers to the total number of girl subsystem files, that is 15 components + `girlclass.rpy` (host class) + `girl_factory.rpy` (factory functions) = 17; the component classes themselves number 15.

## 2. Component Inventory

| Component class | File | Lines | Responsibility | Migrated implementation (★) |
|-----------------|------|------:|----------------|------------------------------|
| `GirlBase` | `girl_base.rpy` | 34 | Identity: name, rank, serialization | — (lightweight wrapper) |
| `GirlStats` | `girl_stats.rpy` | 188 | Stats, caps, changes, spillover | ★ `get_stat` / `change_stat` / `set_stat` / `average_skills` |
| `GirlTraits` | `girl_traits.rpy` | 155 | Trait/perk management | ★ `generate_traits` |
| `GirlItems` | `girl_items.rpy` | 110 | Equipment, items, inventory | — |
| `GirlSchedule` | `girl_schedule.rpy` | 155 | Job assignment, workdays, schedule | ★ `get_status` |
| `GirlSex` | `girl_sex.rpy` | 415 | Sex acts, kinks, preferences | ★ `will_do_sex_act` / `refresh` / `activate` / `deactivate` etc., 30 total |
| `GirlMood` | `girl_mood.rpy` | 196 | Mood, sanity, energy, health | ★ `change_energy` / `heal` / `rest` |
| `GirlRelationships` | `girl_relationships.rpy` | 98 | Love, fear, obedience, MC relationship | ★ `change_love` / `change_fear` |
| `GirlEconomy` | `girl_economy.rpy` | 274 | Price, upkeep, tips, performance | ★ `get_price` / `get_xp` / `get_jp` / `get_rep` / `estimate_performance` |
| `GirlDialogue` | `girl_dialogue.rpy` | 217 | Dialogue selection, `say()`, personality | ★ `pick_dialogue` / `say` / `rand_say` |
| `GirlPictures` | `girl_pictures.rpy` | 431 | Picture selection, refresh, evaluation | ★ `get_fix_pic` |
| `GirlEffects` | `girl_effects.rpy` | 59 | Effect wrapper (delegates to EffectBearer) | — (pure delegation) |
| `GirlGeneration` | `girl_generation.rpy` | 116 | Randomization, personality, background, preferences | — (`randomize` entry point) |
| `GirlTraining` | `girl_training.rpy` | 177 | Training | Partial method bodies |
| `GirlLogging` | `girl_logging.rpy` | 32 | Logging, tracking, recent events | — (thin component) |

The header comment in `girl/__init__.rpy` ("Total: 11 components") is outdated — at that time only 10 components plus 1 stub were complete; there are now 15 component classes, so do not cite it.

## 3. Delegation Pattern

### 3.1 Component Instantiation

At the end of Girl.__init__ (girlclass.rpy:158-173), all components are created; components access any Girl state/method via `self.girl`:

```python
# girlclass.rpy:158-173 (excerpt)
# Phase 2.1: Component delegation (see game/core/framework/girl/)
self._base = GirlBase(self)
self._stats = GirlStats(self)
self._traits = GirlTraits(self)
# ... 15 in total
```

### 3.2 Method Delegation (Thin Wrappers)

The Girl class keeps the original method signatures; the method body is a one-line forward to the component, completely transparent to existing call sites:

```python
# girlclass.rpy:183-195 (GirlMood delegation example)
## Phase 2.1: Delegated to GirlMood component ##
def init_sanity(self):
    return self._mood.init_sanity()

def get_sanity(self):
    return self._mood.get_sanity()
```

### 3.3 The `_impl` Alias Convention

For domains claimed by a component whose method bodies still live inside the Girl class, the component calls the **unbound original implementation** on Girl via an `_impl` alias, bypassing the delegation layer to avoid infinite recursion:

```python
# girlclass.rpy:3713-3721 (Economy alias section, inside the class body)
# ── Phase 2.1: Economy delegation aliases ──
_get_price_impl = get_price
_get_med_upkeep_impl = get_med_upkeep
_adjust_upkeep_impl = adjust_upkeep
```

```python
# girl/girl_stats.rpy:127-129 — component-side call
def stat_spillover(self, stat, chg, job=None):
    '''Handle stat spillover between main and sex stats'''
    return self.girl._stat_spillover_impl(stat, chg, job)
```

Aliases bind as plain function objects (not bound methods) when the class body executes, so the component must pass `self.girl` explicitly when calling them. There are 156 such aliases in the class (counted precisely by `^\s+_[a-z_]+_impl = [a-z_]+$`).

## 4. Method Migration Pattern

Every migration commit follows the same four steps (see the Phase 2 series of commits in git log):

1. **Create the component file** (`girl_<domain>.rpy`, init -2); the class holds a `girl` reference.
2. **Move method bodies into the component**: implementation code moves from girlclass.rpy into component methods with unchanged semantics.
3. **Leave a delegation on the Girl side**: the original method becomes a one-liner `return self._<comp>.<method>(...)`.
4. **Add `_impl` aliases**: if the component needs to call back into other Girl methods, register aliases in the class body.

Unmigrated method bodies (such as `_stat_spillover_impl`, `_test_stats_impl`, `_get_xp_cap_impl`, which still remain in girlclass.rpy) are exposed to components via aliases, forming the transitional state of "components own the interface, the host retains the implementation."

## 5. Migration Lesson: the `get_stat` Double-Counting Bug

**This is the most representative incident of the component migration, fixed in commit `1c62fd1` (2026-09-11).**

### Symptoms

When migrating `get_stat` to `GirlStats`, the implementation applied the effect bonus twice:

```python
# Buggy version (historical version of girl_stats.rpy)
eff = g.get_effect("change", stat_name) + g.get_effect("change", "all skills")
# ... main/sex stat branches would also add "all main skills" / "all sex skills" ...
stat_obj = g.find_stat(stat_name)
if not stat_obj:
    return 0
val = stat_obj.value + eff
# Handle additional effects          ← duplicate accumulation
extra = (g.get_effect("change", stat_name) + g.get_effect("change", "all skills"))
return val + extra
```

`eff` already includes `change <stat>` and `change all skills`, and `extra` adds the same pair of effects once more — every effect bonus was counted twice, directly inflating girl stat evaluation, performance, and price.

### Fix (current code girl_stats.rpy:25-50)

1. Removed the duplicate `extra` accumulation, restoring baseline semantics: `result = stat_obj.value + eff`.
2. Restored the hard assertion on invalid stat names (`raise AssertionError(...)` listing valid names) — the buggy version had replaced the assertion with a silent `return 0`, masking callers passing wrong names.
3. Restored rounding and the lower bound: `round_int(result)`, negative values zeroed.
4. Tests updated in the same commit (`tools/test_runner.rpy`).

### Lessons

- **When migrating, compare the evaluation order of the original implementation line by line**, especially for "accumulation-style" code like effects/bonuses — it is the easiest place to "helpfully add it once more" while moving code.
- **Do not replace assertions with silent degradation.** For "robustness" the buggy version turned `AssertionError` into `return 0`, letting errors propagate into downstream numbers instead of surfacing at the source.
- Effect-bonus code must come with regression tests for the assertion semantics (this fix updated test_runner in the same commit).

---

## Related Documentation

- [services.md](services.md) — the service container (same batch of refactoring)
- [girl_pack.md](girl_pack.md) — girl packs and GirlFilesDict
- [trait_perk.md](trait_perk.md) — the Trait/Perk registries consumed by the GirlTraits component
- [ui_screens.md](ui_screens.md) — screens such as girl_profile were extracted in the same batch as componentization
