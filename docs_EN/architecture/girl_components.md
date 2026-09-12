# Girl Component System Architecture

> Last updated: 2026-09-11 (after Phase 7 batches 1-14, verified against code)
> **Core files**: `game/core/framework/girlclass.rpy` (1,148 lines, formerly ~5,900 lines), `game/core/framework/girl/` (component package)
> **Phase**: Phase 2 (component-based decoupling) + Phase 7 (component migration completion — full method body migration)

---

## 1. System Responsibilities

The Girl class was originally a ~5,900-line god class. Phase 2 split it into **16 component classes** by domain; each component holds a reference to the Girl instance and is responsible for one focused domain. The `Girl` class itself (girlclass.rpy, `class Girl(EffectBearer)`) now keeps only `__init__` (state fields + component instantiation), delegation shells for migrated methods, a few intentionally retained micro-methods (such as the one-line `get_schedule`), and 24 live `_impl` aliases.

Key numbers (all verified via grep, after Phase 7):

- Component classes: **16** (`game/core/framework/girl/girl_*.rpy`, one class per file, init -2; includes the Phase 7 new file `girl_progression.rpy`).
- `_impl` aliases: **24** (only for methods whose real implementation still lives in girlclass, such as `get_schedule`/`is_unique`).
- The Girl class has ~212 methods (counted by `def `), almost all one-line delegation shells; all 2,000+ existing call sites work unchanged.

> Scope note: the older "15 components + host + factory = 17" figure has been updated to 16 components (new GirlProgression added).

## 2. Component Inventory

| Component class | File | Lines | Responsibility | Migrated implementation (★) |
|-----------------|------|------:|----------------|------------------------------|
| `GirlBase` | `girl_base.rpy` | 166 | Identity: naming, ini loading, post-acquire init | ★ `set_name` / `load_ini` / `init_after_acquire` |
| `GirlStats` | `girl_stats.rpy` | 389 | Stats, caps, spillover, tests | ★ `get_stat` / `change_stat` / `get_stat_minmax` / `stat_spillover` etc. |
| `GirlProgression` | `girl_progression.rpy` | 483 | Level/rank/job level, XP-JP-rep, Perks, stat upgrades | ★ all 28 methods (new in Phase 7 batch 6) |
| `GirlTraits` | `girl_traits.rpy` | 244 | Trait/perk management, shields, defense | ★ `generate_traits` / `add_trait` / `has_perk` / `test_shield` |
| `GirlItems` | `girl_items.rpy` | 170 | Equipment, item use, taking items | ★ `use_item` / `equip` / `take` |
| `GirlSchedule` | `girl_schedule.rpy` | 244 | Job assignment, workdays, schedule | ★ `set_job` / `will_do` / `get_status` |
| `GirlSex` | `girl_sex.rpy` | 784 | Sex acts, kinks, preferences, tastes | ★ 49 methods (inner+outer `generate_preferences` merged) |
| `GirlMood` | `girl_mood.rpy` | 610 | Mood, sanity, energy, health, fatigue | ★ mood cluster / `change_energy` / `heal` / `rest` / `tired_check` |
| `GirlRelationships` | `girl_relationships.rpy` | 372 | Love, fear, MC relationship, spoiling/intimidation | ★ `change_love/fear` / `receive_gift` / `update_relationships` |
| `GirlEconomy` | `girl_economy.rpy` | 489 | Price, upkeep, tips, reception capacity | ★ `get_price` / upkeep cluster / `whore_on_street` / `get_tip` |
| `GirlDialogue` | `girl_dialogue.rpy` | 497 | Dialogue, `say()`, personality, `is_`, descriptions | ★ `pick_dialogue` / `get_personality_description` / `is_` |
| `GirlPictures` | `girl_pictures.rpy` | 426 | Picture selection, refresh, evaluation | ★ `get_fix_pic` etc. (migrated earlier) |
| `GirlEffects` | `girl_effects.rpy` | 59 | Effect wrapper (delegates to EffectBearer) | — (pure delegation) |
| `GirlGeneration` | `girl_generation.rpy` | 116 | Randomization, personality, background orchestration | — (orchestration entry point, depends on other components) |
| `GirlLogging` | `girl_logging.rpy` | 253 | Logging, tracking, memory, recent events | ★ `add_log` / `track_event` / `remembers` and 9 more, 12 total |
| `GirlTraining` | `girl_training.rpy` | 316 | Farm training, obedience checks, build-up | ★ `will_do_farm_act` / `get_obedience_check_target` / `reset_build_up` |

The header of `girl/__init__.rpy` is now a full-★ table for all 16 components (only effects/generation are thin wrappers); the code is the source of truth.

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

## 6. Phase 7 migration lessons (2026-09-11, batches 1-14)

### 6.1 `generate_preferences` double-execution bug

**The most representative Phase 7 incident, fixed in `f027957`.**

The early migration had placed the **inner** body of `generate_preferences` (preference/fixation generation) into GirlSex while leaving the **outer wrapper** on the Girl side (calling the inner + generate_stats + virginity control + NGP settings) — correct at the time. In Phase 7 batch 8 the outer layer was merged into the component, but the outer wrapper in girlclass was **not shrunk to a pure shell in sync**, so `girl.generate_preferences()` executed the outer logic twice: sex stats regenerated (dice re-rolled), NGP preference settings applied twice (`change_preference` is not idempotent), virginity control run twice.

### Fix

The component holds the merged inner+outer implementation, and girlclass became a pure shell `self._sex.generate_preferences()` — matching the pre-migration semantics of "all logic in one method body".

### Lessons

- **When migrating wrapper-style methods, the component-side merge and the host-side shell shrink must be done as a pair**; doing only one side causes double execution. After migrating, grep the host method body to confirm no logic merged into the component remains.
- **Idempotency self-check**: if the merged logic contains random generation (dice) or non-idempotent changes (preference stacking), double execution shows up immediately; prioritize reviewing such methods.

### 6.2 Stale copies inside components

Phase 7 found several **old copies inside components whose semantics differed from the live girlclass versions**: `sanity_warning` (component's 3 branches vs the real 6 branches), `farm_beg_test` (inverted decision threshold), `use_item` (simplified version), `take`/`get_equipped` (different behavior), `get_stat_minmax` (a 5-line simplification vs the 63-line domain version).

### Lessons

- **A same-named method inside a component is not necessarily a shell**; before migrating, diff the girlclass original against the component copy line by line; the girlclass (live code) wins.
- The simplified `get_stat_minmax` copy had also degraded the `change_stat` skill cap from the baseline `max(rank*50+...)` to a constant 100 (fixed in batch 10 along with the migration, restoring baseline semantics) — **when two same-named implementations coexist, internal callers may already be using the wrong one**.

### 6.3 List comprehension variable shadowing

Component methods uniformly use `g = self.girl`, while the original code habitually used `g` as a comprehension/loop variable (`[g.name for g in self.friends]`). A mechanical `self→g` replacement would shadow the girl reference. All Phase 7 batches together fixed 20+ such sites, renaming the loop variable every time (`gf`/`gv`, etc.).

### Lessons

- After a mechanical `self→g` replacement, search the method body for `for g in` / `[g for` / `if g !=` and check each one.

---

## Related Documentation

- [services.md](services.md) — the service container (same batch of refactoring)
- [girl_pack.md](girl_pack.md) — girl packs and GirlFilesDict
- [trait_perk.md](trait_perk.md) — the Trait/Perk registries consumed by the GirlTraits component
- [ui_screens.md](ui_screens.md) — screens such as girl_profile were extracted in the same batch as componentization
