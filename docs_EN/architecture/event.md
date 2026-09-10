# Event / StoryEvent System Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/framework/interactions.rpy` (`StoryEvent` class :55), `game/core/systems/events_dispatcher.rpy` (8,611 lines, runtime dispatch), `game/core/systems/events/event_engine.rpy` (202 lines), `game/core/systems/events/event_bridge.rpy` (68 lines)
> **Editor support**: ✅ Scenario editor (`scenario_editor`)

---

## 1. System Responsibilities

StoryEvent is the unified encapsulation of all story/random/city/daily events in the game (note: the class is defined at `framework/interactions.rpy:55`, **not** in core_entities.rpy — the old documentation was wrong on this point):

- **Trigger conditions**: multi-dimensional filtering by `chapter`, `rank`, `date`, `location`, `seasons`, `condition_func`, etc.
- **Lifecycle**: `once=True` one-shot / `once=False` repeatable.
- **Mode filtering** (BK Evolution): the `modes` field declares the GameModes the event applies to (`None` all modes / `str` single mode / `list` multiple modes), checked at enqueue time in EventEngine.
- **Type queues**: two global queues, `city` (city events) and `daily` (morning/day/night), plus alarm for precise calendar alarms.

## 2. Four Key Components

### 2.1 StoryEvent (interactions.rpy:55)

Low-level data class: a label points to a Ren'Py label, with priority `order`, trigger conditions, and call arguments. A Mod's `night_label` is also wrapped into a StoryEvent triggered every night (core_entities.rpy:265).

### 2.2 events_dispatcher.rpy (8,611 lines)

Runtime dispatch hub: daily screening, triggering, and execution (`call` of the corresponding label) for the `city_events` / `daily_events` queues. It also hosts the v2 hook call sites `event_triggering`/`event_finished` (:1084/:1087), `chapter_starting`/`chapter_finished` (:661/:1053), `girl_runaway` (:1173), `girl_acquired` (:8440), and `game_loaded` (:191).

### 2.3 EventEngine (systems/events/event_engine.rpy)

init -4 singleton, registered as the service `services.event_engine` (:202). High-level management interface:

- `register_story_event()` / `register_event_from_dict()` — register into EventRegistry, optionally enqueueing at the same time.
- `add_event_to_queue()` / `remove_event_from_queue()` — runtime queue management; **modes filtering** (:78-83) and forced city semantics for locations (:86) are applied before enqueueing.
- `scan_custom_events()` / `load_event_pack()` — scan `core/content/events/` and load event packs at runtime with `renpy.load_string()`.
- `on_event_trigger()` — fires the v1 `on_event_trigger` hook via HookManager (:183).

### 2.4 EventBridge (systems/events/event_bridge.rpy)

init -11 singleton. Positioned as a bridge between old and new systems: when events are added via the old API (`add_event()` / `story_add_event()`), they are synced to EventEngine so both systems see the same set of events.

**⚠ Known issue (found during code verification)**: `EventBridge.sync_to_engine()` (event_bridge.rpy:52) calls `engine.register_runtime_event(event, event_type)`, but that method **does not exist** on `EventEngine` (what exists is `add_event_to_queue` / `remove_event_from_queue`; grepping the whole codebase finds no `register_runtime_event` definition). Because the bridge code wraps everything in try/except that silently swallows exceptions, the old→new sync is currently a **silent no-op**; the reverse direction (New→Old, event_dict proxy) is handled normally by the proxy in `event_registry.rpy:65`. Fix direction: change the bridge to call the existing enqueue API.

## 3. Inter-System Relationships

```
story_events.json / sandbox/events.json / scenarios.json
    └─→ DataLoader.load_story_events() / load_sandbox_events()
           └─→ EventRegistry (init -5)  ←── ModAPI.register_event (category="mod")
                  ├─→ event_dict proxy (New→Old compatibility)
                  └─→ EventEngine ──→ city_events / daily_events global queues
                                         └─→ events_dispatcher.rpy daily screening/triggering
                                                ├─→ v1 hook on_event_trigger (HookManager)
                                                └─→ v2 hooks event_triggering / event_finished

Old API add_event()/story_add_event() ──→ EventBridge.sync_to_engine() (currently a no-op, see §2.4)
```

## 4. Mod and Hook Integration

- When a v1 Mod is activated, its events are automatically registered into EventRegistry (core_entities.rpy:260-262), and `night_label` becomes a nightly StoryEvent.
- The v2 hooks `event_triggering` / `event_finished` fire at dispatcher :1084/:1087 with context containing `event`, `event_type`, `label`.

## 5. Editor Support

| Editor | Support | Notes |
|--------|---------|-------|
| Scenario editor `event_editor.py` | ✅ | CRUD for story_events.json / sandbox events.json, going through the EventRegistry contract |
| Event pack hot-reload | ✅ | `EventEngine.load_event_pack()` supports runtime `.rpy` event packs |

---

## Related Documentation

- [registry.md](registry.md) — the base-class mechanics of EventRegistry
- [data_loader.md](data_loader.md) — event JSON loading
- [mod_system.md](mod_system.md) — v1/v2 event hook comparison
- [gamemode.md](gamemode.md) — the relationship between modes filtering and GameMode
