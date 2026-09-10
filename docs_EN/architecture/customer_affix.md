# Customer Affix System Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core file**: `game/core/systems/customer/customer_affixes.rpy` (405 lines, init -1)
> **Data**: `game/core/data/customers/customer_affixes.json` (load point customer_affixes.rpy:18)
> **Consumer**: `framework/world.rpy:418` (`Customer.__init__` calls `generate_customer_affixes`)

---

## 1. System Responsibilities

CustomerAffix attaches a three-dimension affix to each customer, making their behavior, budget, and rating feedback more differentiated:

### Three-Dimension Affixes

| Dimension | Class | Effect |
|-----------|-------|--------|
| Personality prefix | `CustomerPersonality` (customer_affixes.rpy, prefix section) | Behavior and difficulty modifiers |
| Wealth/budget | Color tier | Budget multiplier |
| Mood | mood affix | Satisfaction tendency |

### Color Tiers (8 levels)

`CUSTOMER_COLOR_TIERS` (customer_affixes.rpy:26-41): white(1.0×) → green(1.2×) → blue(1.5×) → purple(2.0×) → gold(2.8×) → orange(4.0×) → red(6.0×) → iridescent(10.0×). The JSON definition lives in the `color_tiers` array of `customer_affixes.json` (id/color/budget_multiplier/name_i18n).

### Core Classes

- `CustomerAffixes` (:298): the complete affix combination for a single customer; methods include `get_color()`, `get_tier_name()`, `get_budget_multiplier()`, `get_full_title()`, `apply_to_customer(customer)`, `to_dict()` / `from_dict()` (save serialization).
- `generate_customer_affixes(pop_rank=1, forced_tier=None)` (:380): randomly generates affixes by crowd rank; `forced_tier` can force a color tier.

## 2. State After Data Migration

- **JSON first**: `_ca_path = gamedir/core/data/customers/customer_affixes.json` (:18), self-loaded with native `os.path` + `json.load` (**not via DataLoader**; one of the two self-load paths).
- **Hardcoded fallback kept**: when the JSON is missing or `color_tiers` is empty, it falls back to the hardcoded 8-tier table inside the file (:31-41). The fallback is a deliberately kept compatibility strategy.
- Affix data enters save files: what is stored per customer is a `CustomerAffixes.to_dict()` snapshot, restored via `from_dict()` on load, unaffected by later JSON modifications.

## 3. Decoupling Approach

- **Decoupled from generation logic**: `generate_customer_affixes()` is a pure functional generator that does not depend on a Customer instance.
- **Decoupled from application logic**: `apply_to_customer()` one-way writes affix effects (budget multipliers, etc.) into the customer; the customer itself (the `Customer` in `world.rpy`) is unaware of the affix internals.
- **Decoupled from the crowd system**: it only takes `pop_rank`; the caller (district crowd) decides the generation parameters.

## 4. Inter-System Relationships

```
customer_affixes.json ──(self-loaded, :18)──→ CUSTOMER_COLOR_TIERS + affix definitions
                                                  │
world.rpy:418 Customer.__init__ ──→ generate_customer_affixes(pop_rank=self.pop.rank)
                                                  │
                                                  ▼
                                       CustomerAffixes ──→ apply_to_customer(customer)
                                                  │
                                                  ▼
                          Budget multiplier/behavior modifiers → nightly settlement rating feedback
```

## 5. Editor Support

| Editor | Support | Notes |
|--------|---------|-------|
| Direct JSON editing | ✅ | customer_affixes.json has a simple structure (color_tiers array + affix tables); restart to take effect |
| Dev console | ✅ View | Validated via data_sync |

There is no dedicated visual editor tab yet; the scale is still small.

---

## Related Documentation

- [data_loader.md](data_loader.md) — comparison of self-loaded JSON vs. the DataLoader path
- [girl_components.md](girl_components.md) — interaction between customer ratings and girl performance (GirlEconomy)
- [event.md](event.md) — customer satisfaction events
