# Goal System Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/framework/goal.rpy` (`Goal` class :4, init -10)
> **Data**: `game/core/data/goals/chapter_goals.json` (**7 chapters**, measured) + `goal_ui.json`
> **Load point**: `game/core/init/settings.rpy:101-123` (loaded independently, not via DataLoader)

---

## 1. System Responsibilities

Goals are the phased objectives driving chapter progression:

- **Types** (`type`): `gold` (gold held), `ranked` (N girls reaching a given rank), `reputation` (brothel reputation), `prestige` (MC prestige), `story` (story flag, the value being a label).
- **Gating semantics**: `reached()` (goal.rpy:52) — when `blocking=True` and unmet, chapter progression is blocked; `max_chapter` declares the highest chapter the goal applies to; non-blocking goals are always reached.
- **Channels**: `channel="advance"` is the main progression channel; other channels are used for optional side quests.
- **Description**: `get_description()` (goal.rpy:34) generates the text per type (or takes the text value for the story type).

## 2. Data Flow

```
game/core/data/goals/chapter_goals.json (7 chapters, each a list of Goal dicts)
    └─→ init/settings.rpy:101-123
           ├─ JSON present: Goal.from_dict(g) constructed one by one → chapter_goals[int(ch)]
           └─ JSON missing: chapter_goals = _chapter_goals_fallback (hardcoded fallback at settings.rpy:101)
    └─→ Game.goals = chapter_goals[1]          (core_entities.rpy:34, at game start)
    └─→ game.set_goals(chapter_goals[chapter]) (events_dispatcher.rpy:1015, switched per chapter)

goal_ui.json ─→ DataLoader.load_goal_ui() ─→ settings.rpy:520 (display config for the goals UI)
```

Note: the Goal type only accepts the 5 types listed above; the types mentioned in the old documentation (`bedrooms/girls/customers/districts/mc_level/free`) have **no implemented branch** in `reached()` (they fall into `return False` and block permanently) — they are historical leftovers in the description; do not rely on them.

## 3. Decoupling Approach

- **Decoupled from Game**: Goal only reads the global `MC`/`brothel`/`game`/`story_flags` and does not hold a Game reference.
- **Decoupled from save files**: Goals are rebuilt from JSON at every init and never enter save files; progress checks always evaluate current actual values (gold, reputation, etc.).
- **Decoupled from DataLoader**: for historical reasons it is self-loaded by settings.rpy (with its own fallback); it is one of the two self-load paths (the other being customer_affixes).

## 4. Inter-System Relationships

- **Chapter progression**: `events_dispatcher.rpy:1015` calls `set_goals` on chapter switch; the progression check calls `Goal.reached()`.
- **Mode gating**: story mode is goal-gated; sandbox mode can advance freely (see `can_advance_chapter` in [gamemode.md](gamemode.md)).
- **Goals UI**: `goal_ttip` in `screen_resources.rpy` and friends display current goals; `goal_ui.json` provides the UI config.

## 5. Editor Support

| Editor | Support | Notes |
|--------|---------|-------|
| Dev console | ✅ View | chapter_goals.json format validated via data_sync |
| Direct JSON editing | ✅ | Simple structure (a list of dicts per chapter); restart to take effect |

---

## Related Documentation

- [gamemode.md](gamemode.md) — chapter progression and mode rules
- [data_loader.md](data_loader.md) — goal_ui.json as the counterexample to the DataLoader path
- [event.md](event.md) — story-type Goals and their relationship to story_flags
