# BK Evolution — Mod API Reference (v1 + v2)

> Last updated: 2026-09-11 (persistent enable mechanism + main-menu Mod Manager screen, verified against code)
>
> This document is the authoritative reference for Brothel King Evolution's Mod mechanisms, covering both the legacy v1 `Mod()` class and the new `ModAPIV2`.
> All line numbers, parameters, and behavior reflect the current code (branch `bk-evolution`).

---

## 0. Quick choice: v1 or v2?

| | v1 (`Mod()`) | v2 (`ModAPIV2`) |
|---|---|---|
| Entry point | Instantiate the `Mod(...)` class | `services.mod_api_v2.register_mod(mod_id, manifest)` |
| Registration | Automatically added to `detected_mods` at construction | Explicit manifest registration, with validation |
| Activation semantics | **Per-save toggle**: can be activated/deactivated in the main-menu Mods screen; state stored in `persistent.mods` | **Enabled by default, persistently disableable**: flag stored in `persistent._bk_v2_mod_states`, toggled in the main-menu Mod Manager screen |
| How to deactivate | Deactivate in the Mods screen | Toggle off in the main-menu "Mods" (Mod Manager screen); or delete the entire `game/custom/mods/<Mod>/` folder |
| Lifecycle labels | `early/init/night/update/load/remove_label` + `chapter_labels` | No label mechanism; use hooks (`game_saved`/`game_loaded`, etc.) |
| Home right-menu buttons | `home_rightmenu_add_buttons` | Manifest `home_rightmenu_add_buttons` (new support in v2) |
| Event registration | `events={...}` + `add_event()` | Inherited `ModAPI.register_event()` and other Registry wrappers |
| Hook system | `mod.hooks` dict → `HookManager` (Phase 6 compatibility layer) | Manifest `hooks` or `register_hook()` → standardized hooks |
| Dependencies | None | Manifest `dependencies` (enforced: mod stays inactive until every dependency is active) |
| Template | `game/custom/mods/Goldo's cool mod/` (tutorial example) | `game/core/templates/mod_template/mod_template.rpy` |
| Full example | Same as above (v1) | `game/custom/mods/Auction House/` (authoritative example, see §6) |

**Recommendations**:

- **Use v2 for all new mods** — it has version declarations, capability validation, standardized hooks, and new UI integrations such as home menu buttons are only guaranteed ongoing maintenance for v2.
- v1 remains fully usable and suits scenarios requiring "per-save toggle" semantics (players may want to disable a mod on some saves). Tutorial-style event mods like Goldo's cool mod continue to work via v1.
- Both mechanisms can coexist without interfering with each other (v2 has its own singleton and hook table).

---

## 1. v1 Mod mechanism

### 1.1 Full parameter list of the `Mod()` class

Definition: `game/core/framework/challenges.rpy:370` (`init -2 python`). Construction **automatically registers** the mod into the global `detected_mods` dict (`challenges.rpy:432`).

```python
Mod(
    name,                     # Required. Display name of the mod; also the key of detected_mods / persistent.mods
    folder,                   # Required. Mod folder name, used to build the resource path "mods/" + folder + "/"
    creator="Unknown",        # Author name
    version=1.0,              # Version number. Used by check_for_updates() to detect updates
    pic=None,                 # Title image filename (relative to mod path), shown in the Mods screen
    description=__("This is a mod for Brothel King."),  # Description text
    help_prompts=None,        # [(button text, label), ...] see §1.3
    init_label="",            # Called after activation, after the brothel is established (call_in_new_context)
    night_label="",           # Called every night after activation (added to daily_events, type="night")
    update_label="",          # Called when a version change is detected while loading a save
    home_rightmenu_add_buttons=None,  # [screen names, ...] see §1.4
    events=None,              # {event name: StoryEvent, ...} see §1.3
    early_label="",           # Called early in a new game (before districts/the brothel are set up)
    load_label="",            # Called when loading a save (no arguments)
    remove_label="",          # Called on deactivation (for cleanup)
)
```

Attributes computed automatically after construction:

| Attribute | Description | Code location |
|------|------|----------|
| `path` | `"mods/" + folder + "/"`, the resource lookup path | `challenges.rpy:380` |
| `full_name` | `name + " v" + version + ", from " + creator` | `challenges.rpy:388` |
| `pic` | `Picture(pic, path+pic)` or `None` | `challenges.rpy:383-386` |
| `help_prompts` | Each prompt automatically prefixed with `[Mod name] ` | `challenges.rpy:393-397` |
| `chapter_labels` | `{1: None, ..., 7: None}`, labels callable at chapter start (**not a constructor parameter**; assign after init) | `challenges.rpy:406` |
| `hooks` | `{}`, Phase 6 hook table `{hook_name: callback}` (**not a constructor parameter**; assign after init) | `challenges.rpy:425` |
| `api_version` | Always `1` | `challenges.rpy:426` |
| `active` / `seen` | Active state / whether the mod has been viewed in the Mods screen | `challenges.rpy:433-434` |

**Persisting custom attributes**: `Mod` overrides `__setattr__`/`__getattribute__` (`challenges.rpy:441-465`). Custom attributes assigned after the init phase are written to the global `mod_settings` (`defaultdict(dict)`), **saved with the save file**, and restored from `mod_settings` when init reruns instead of being overwritten by defaults. Note the exceptions: the `name` and `init` attributes are excluded.

### 1.2 Automatic registration and activation flow

Relevant global variables (`game/core/init/variables.rpy:2389-2395`): `detected_mods = {}`, `persistent.mods = {}` (initialized on first run), `mod_traceback`, `updated_games`.

Structure of `persistent.mods[name]` (`game/core/framework/game_systems.rpy:205`):

```python
{"version": mod.version, "check": mod.get_check(), "active": mod.active}
```

`get_check()` returns `(version, path, init_label, len(events))` for detecting version changes (`challenges.rpy:468-469`).

Flow (in call order):

1. **Init phase**: the mod's `.rpy` instantiates `Mod(...)` at `init -1` (by convention) → automatically enters `detected_mods`.
2. **New game** (`label start`, `game/core/systems/events_dispatcher.rpy:94`) → calls `update_mods()` (`game/core/framework/game_systems.rpy:150`):
   - Present in `persistent.mods` but missing from `detected_mods` → delete the record and report "has been removed";
   - New mod (no record in `persistent.mods`) → `register_mod(mod)` writes to persistent, reports "has been added";
   - `check_for_updates()` differs → re-register, report "has been updated" and set `active=True`;
   - Already recorded and `persistent.mods[name]["active"]` → set `mod.active = True`.
3. **Early activation** (`events_dispatcher.rpy:671`) → `game.start_mods(early=True)`: for active mods in `detected_mods`, calls `activate_mod(mod, early=True)`, which triggers only `early_label`.
4. **Full activation** (`events_dispatcher.rpy:968`) → `game.start_mods()`: `game.activate_mod(mod)` (`game/core/framework/core_entities.rpy:243`) does the following in order:
   - Registers `mod.hooks` to `hook_manager` (Phase 6 compatibility layer, `:254-257`);
   - Registers `mod.events` to `event_registry` (category="mod", `:260-262`);
   - If `night_label` is non-empty → appends `StoryEvent(label=night_label, type="night", once=False)` to `daily_events` (`:264-265`);
   - `renpy.call_in_new_context(mod.init_label)` (`:270-272`).
5. **Mods screen toggle** (`screen mods`, starting at `game/core/ui/screens/screen_quest.rpy:564`):
   - `mod.activate()` (`challenges.rpy:480`): yes_no confirmation → `active=True` + write `persistent.mods` → `game.activate_mod(self)`;
   - `mod.deactivate()` (`challenges.rpy:495`): yes_no confirmation → `active=False` + write persistent → `game.deactivate_mod(self)` (calls `remove_label` for cleanup, `core_entities.rpy:291-292`).
   - Note: the in-game "Mods" button (`screen navigation`, `game/core/config/screens.rpy:815`) opens this same screen; the main-menu `screen main_menu()` "Mods" button (`screens.rpy:997`) instead opens the v2 Mod Manager screen (§2.5).
6. **On loading a save** (`label after_load`, starting at `events_dispatcher.rpy:186`): refreshes the mod instance references in `game.active_mods`, collects and `call`s each active mod's `load_label`; then (`game/core/ui/main.rpy:907`) `game.update_mods()` handles three cases — "mod removed / version changed / newly activated" — and may return a list of `update_label`s to call.
7. **Chapter start** (`events_dispatcher.rpy:974-978`): for each active mod, checks `mod.chapter_labels[game.chapter]`; if non-empty and the label exists, it is queued for a chapter-label call (if it doesn't exist, an `AssertionError` is raised).

### 1.3 events and help_prompts

**events**: the value of the constructor parameter `events={...}` must be `StoryEvent` objects (`ev.mod = self` is linked automatically at construction, `challenges.rpy:429-430`). On activation all are registered to `event_registry` (step 4 in §1.2), and afterwards scheduled via `mod.add_event(event_name, type=..., date=..., delay=1, call_args=None)` (`challenges.rpy:508`):

- `type="alarm"` → `calendar.set_alarm(date, ev)` (default `date = calendar.time + delay`);
- `type in ("morning", "day", "night")` → added to `daily_events`;
- `type="city"` → added to `city_events` (triggered when the MC visits the corresponding location).

**help_prompts**: `[(button text, label), ...]`. The in-game Help ("?") menu merges the help_prompts of all active mods into its option list (`game/core/systems/help.rpy:374-375`); button text automatically gets a `[Mod name] ` prefix. The target label is invoked with `call` and can be a mod's option menu (Goldo's cool mod's "Surprise me tomorrow" uses this mechanism).

**Label overview** (all are invoked via `call_in_new_context` or `call` with no arguments, inside `game.activate_mod` / save loading / chapter flow):

| label | When it triggers |
|-------|----------|
| `early_label` | Early in a new game, **before** districts/the brothel are established (`activate_mod(early=True)`, `core_entities.rpy:247-252`) |
| `init_label` | When the mod is activated (after the brothel is established) |
| `night_label` | Every night (via daily_events) |
| `update_label` | When a version change is detected on load; falls back to the reset flow if this label is absent |
| `load_label` | Every save load (`after_load`, `events_dispatcher.rpy:203-210`) |
| `remove_label` | Cleanup on deactivation (`core_entities.rpy:291-292`) |
| `chapter_labels[n]` | Start of chapter n (1-7, `events_dispatcher.rpy:974`) |

### 1.4 home_rightmenu_add_buttons (v1)

Constructor parameter; the value is a **list of no-argument screen names**. The home right-side menu (`game/core/ui/screen_home.rpy`):

- `:59-61` iterates `game.active_mods`, collecting v1 mods that declare buttons;
- `:73-74` adds a row to the menu whenever any v1/v2 mod button exists;
- When expanded, `screen mod_menu_display(mod_menu, v2_buttons)` (`screen_home.rpy:382`) renders each via `use expression <screen name>` (`:390-394`), grouped by mod and showing the mod name.

Inside the button screen there is usually a `textbutton` whose `action` navigates to the mod's own UI (Goldo's cool mod's `test_mod_but` and Auction House's `right_menu_auction` both follow this pattern).

---

## 2. v2 Mod mechanism (ModAPIV2)

Implementation: `game/core/systems/mods/mod_api_v2.rpy` (`init -3 python`), class `ModAPIV2(ModAPI)`.
Singleton: `mod_api_v2 = ModAPIV2()` (`:385`), registered into the service container `services.register("mod_api_v2", mod_api_v2)` (`:386`), accessible as `services.mod_api_v2` (attribute defined at `game/core/systems/services/service_container.rpy:109-111`). Because it inherits `ModAPI`, v1's `register_trait` / `register_event` and other Registry wrapper methods are also available on v2 (`game/core/systems/mods/mod_api.rpy`).

### 2.1 `register_mod(mod_id, manifest)` and full manifest fields

Signature: `game/core/systems/mods/mod_api_v2.rpy:80`.

```python
services.mod_api_v2.register_mod("my_mod", {
    "name": "My Mod",                # Display name (Mods screen, home menu group title)
    "version": "1.0",                # Mod version (display only; no comparison/validation currently)
    "api_version": 2,                # Must be 2, otherwise ValueError
    "min_game_version": "0.3",       # Minimum game version (declarative; not enforced currently)
    "author": "Your Name",           # Author
    "description": __("..."),        # Description (shown in Mods screen)
    "requires": ["girl_traits"],     # Capability flag list, see §2.2
    "hooks": {"girl_generated": my_callback},  # {hook name: callback}, see §3
    "dependencies": ["game_modes"],  # Prerequisite mod_id list (enforced semantics, see §2.2)
    "always_on": False,              # True = cannot be disabled (default False), see §2.2
    "home_rightmenu_add_buttons": ["my_screen"],  # Home right-menu button screen list, see §2.3
})
```

Field-by-field explanation:

| Field | Type | Required | Validation/behavior |
|------|------|------|-----------|
| `name` | str | Recommended | Display name for `get_menu_buttons()` / `get_mod_info()`; falls back to `mod_id` when missing |
| `version` | str | Recommended | Display only. The code does not parse or compare it |
| `api_version` | int | **Yes** | Must `== 2`, otherwise `ValueError` (`mod_api_v2.rpy:115-117`) |
| `min_game_version` | str | No | Recorded only. **Not enforced in current code** |
| `author` | str | Recommended | Display only |
| `description` | str | Recommended | Display only (Mods screen) |
| `requires` | [str] | No | Each item must be in the `CAPABILITIES` set, otherwise `ValueError` (`:118-120`), see §2.2 |
| `hooks` | {str: callable} | No | Each callback is registered into `_mod_hooks` as `(mod_id, callback, 0)` (`:131-132`); callbacks of a disabled mod are skipped at fire time (§2.2) |
| `dependencies` | [str] | No | **Enforced** (`:219-242`): the mod activates only when every dependency is active; an uninstalled (unregistered) or disabled dependency counts as missing, the mod stays inactive and the Mod Manager shows 缺少前置 (missing prerequisite) |
| `always_on` | bool | No | Defaults to `False`. When `True` the persistent flag is ignored and the mod is always active (the Mod Manager shows 常驻 (pinned) with no toggle button) |
| `home_rightmenu_add_buttons` | [str] | No | List of no-argument screen names, see §2.3 |

Registration-time validation summary (`:113-123`):

1. `api_version != 2` → `ValueError`;
2. `requires` contains an unknown capability flag → `ValueError`;
3. **Registering the same `mod_id` twice → `ValueError`** (`:122-123`, checked against `_registered_mods`) — avoid double registration when init reruns.

Right after registration the active set is recomputed from the persistent flags + dependencies (`_rebuild_active_mods()`, `:138`); when `renpy.config.developer` is true, successful registration logs output via `renpy.log` (`:140-145`).

### 2.2 Persistent enable mechanism, always_on and capability flags

**Enable semantics** (BK Evolution persistent toggle, replacing the old "active once installed"):

- Each v2 mod's enable flag lives in `persistent._bk_v2_mod_states` (`mod_id -> bool`; **unrecorded ids default to enabled**). Field-name constant: `ModAPIV2.PERSISTENT_STATES_ATTR` (`:49`).
- A mod is **active iff**: registered AND (`always_on` OR persistently enabled) AND every manifest `dependencies` entry is active. The active set is recomputed globally by `_rebuild_active_mods()` (`:219-242`): dependencies resolve before their dependents (topological pass); a mod whose dependency is uninstalled (unregistered), disabled or part of a cycle stays inactive.
- Ren'Py binds `persistent` **before** init code runs (`renpy/main.py` calls `renpy.persistent.init()` before executing init), so `register_mod` (init -1) reads the flag immediately and **a disabled mod is not activated in the current boot**; `apply_startup_states()` (`:203-217`) re-syncs idempotently from `before_main_menu` (`events_dispatcher.rpy:100`) as a safety net.
- A disabled mod's hooks stay in `_mod_hooks`, but `execute_hook`/`cancel_hook` skip callbacks attributed to inactive mods (`:321-322`, `:352-353`); `"_direct"` callbacks (registered via `register_hook()`) are not attributable and always run.
- **Convention for mod authors**: init-time registrations with side effects (e.g. registering modes/origins into core registries) should be guarded by `if services.mod_api_v2.is_mod_active("your_mod_id"):` — see `game/custom/mods/Game Modes/mod.rpy:50-57`.

**`always_on`**: optional manifest boolean, defaults to `False`. When `True` the mod is always active and `set_mod_enabled` has no effect on it (the flag value is still recorded); the Mod Manager shows 常驻 (pinned) with no toggle. Suitable for core-gameplay mods that other mods can depend on while players cannot switch them off.

**`dependencies`**: optional list of mod_ids, enforced — the mod stays inactive until every dependency is active (see above). Example: `"dependencies": ["game_modes"]` declares a dependency on the "Game Modes" mod (§6.5).

**Capability flags** (`CAPABILITIES`, `mod_api_v2.rpy:52-64`) — declare which capability surfaces a mod needs; currently used for registration-time validation and documentation semantics:

```python
"girl_stats"    # Modify girl stats
"girl_traits"   # Register custom traits/perks
"economy"       # Modify economy calculations
"items"         # Register custom item quality tiers / affect item generation
"events"        # Register/dispatch events
"dialogue"      # Custom dialogue lines
"pictures"      # Custom picture tags
"game_modes"    # Register custom game modes
"origin"        # Register player origins
"scenario"      # Register scenarios
"ngp_settings"  # NG+ settings
```

### 2.3 Main-menu Mod Manager screen (screen mod_manager)

`game/core/ui/screens/screen_mod_manager.rpy`, opened by the "Mods" button of the main-menu `screen main_menu()` (`game/core/config/screens.rpy:997`, `action Show("mod_manager")`).

- Lists **every registered** mod returned by `list_registered_mods()`: name, version, author and state (已启用/enabled, 已禁用/disabled, 缺少前置/missing prerequisite + ids, 常驻/pinned).
- Each non-`always_on` mod gets a toggle button whose action is `[Function(set_mod_enabled, ...), Function(renpy.save_persistent), SetScreenVariable("show_restart_hint", True)]` — writes persistent + re-syncs memory + shows "changes take full effect after a restart" (no hot reload).
- A "返回" (Back) button at the bottom (`Return()`; `tag menu` makes the screen replace the main-menu screen, and the main-menu interaction loop re-shows it afterwards).
- In-game, the "Mods" button (`screen navigation`, `screens.rpy:815`) still opens the legacy `screen mods()` (v1 per-save toggles + read-only v2 list).

### 2.4 home_rightmenu_add_buttons (v2)

Manifest field; the value is a **list of no-argument screen names**. `get_menu_buttons()` (`:271-281`) returns `[(mod_id, display name, [button screen names])]` — containing only **active** mods that declare buttons (disabled mods are excluded). The home right-side menu fetches the list at `screen_home.rpy:65-69` via `services.mod_api_v2.get_menu_buttons()` and renders it through the `v2_buttons` parameter of `screen mod_menu_display` (`screen_home.rpy:395-401`), displayed alongside v1 mod buttons and grouped by mod.

### 2.5 Lifecycle hooks

v2 has no v1 label mechanism; lifecycle events are covered via hooks:

- `game_saved`: triggered on every save via `renpy.config.save_json_callbacks` (`mod_api_v2.rpy:389-399`, with duplicate-registration protection);
- `game_loaded`: triggered in `label after_load` (`events_dispatcher.rpy:189-191`, guarded by `hasattr` for compatibility with old saves).
- Startup activation safety net: `apply_startup_states()` is called in `before_main_menu` (`events_dispatcher.rpy:100`); it is idempotent.

---

## 3. Complete hook point reference (19)

Constant definitions: `game/core/systems/mods/mod_api_v2.rpy:365-383`. Naming convention: `<domain>_<action>_<tense>` (five names — `girl_sold`, `girl_runaway`, `security_event`, `girl_destination_list`, `girl_destination_accept` — lack `_<tense>`; `tools/verify_mod_api.py` emits a naming-convention warning for these, which is a known item).

All callback signatures are uniformly `callback(context: dict)`; `execute_hook` packs the keyword arguments into a context dict and passes it in (`mod_api_v2.rpy:308-331`), skipping callbacks of inactive mods.

| # | Constant | String value | Call site (file:line) | context keys |
|---|------|----------|---------------------|-----------|
| 1 | `HOOK_GIRL_GENERATED` | `girl_generated` | `game/core/framework/girl_factory.rpy:278` | `girl` |
| 2 | `HOOK_GIRL_ACQUIRED` | `girl_acquired` | `game/core/systems/events_dispatcher.rpy:8465` | `girl`, `price`, `context` |
| 3 | `HOOK_GIRL_SOLD` | `girl_sold` | `game/core/ui/main.rpy:839`, `game/core/ui/main.rpy:1452` | `girl`, `price` |
| 4 | `HOOK_GIRL_RUNAWAY` | `girl_runaway` | `game/core/systems/events_dispatcher.rpy:1173` | `girl` |
| 5 | `HOOK_DAY_STARTING` | `day_starting` | `game/core/systems/endday.rpy:1498` | `time` |
| 6 | `HOOK_DAY_ENDING` | `day_ending` | `game/core/systems/endday.rpy:340` | `time` |
| 7 | `HOOK_NIGHT_STARTING` | `night_starting` | `game/core/systems/endday.rpy:403` | `time` |
| 8 | `HOOK_NIGHT_FINISHED` | `night_finished` | `game/core/systems/endday.rpy:1431` | `time` |
| 9 | `HOOK_WEEK_STARTING` | `week_starting` | `game/core/framework/core_entities.rpy:1937` | `week`, `time` |
| 10 | `HOOK_EVENT_TRIGGERING` | `event_triggering` | `game/core/systems/events_dispatcher.rpy:1084` | `event`, `event_type`, `label` |
| 11 | `HOOK_EVENT_FINISHED` | `event_finished` | `game/core/systems/events_dispatcher.rpy:1087` | `event`, `event_type`, `label` |
| 12 | `HOOK_SECURITY_EVENT` | `security_event` | `game/core/systems/security.rpy:62` | `event_type`, `alert_level` |
| 13 | `HOOK_CHAPTER_STARTING` | `chapter_starting` | `game/core/systems/events_dispatcher.rpy:661` | `chapter` |
| 14 | `HOOK_CHAPTER_FINISHED` | `chapter_finished` | `game/core/systems/events_dispatcher.rpy:1053` | `chapter` |
| 15 | `HOOK_GAME_SAVED` | `game_saved` | `game/core/systems/mods/mod_api_v2.rpy:215` (save_json_callbacks) | none |
| 16 | `HOOK_GAME_LOADED` | `game_loaded` | `game/core/systems/events_dispatcher.rpy:191` (after_load) | none |
| 17 | `HOOK_GIRL_DESTINATION_LIST` | `girl_destination_list` | `game/core/systems/events_dispatcher.rpy:8403` | `girl`, `at_working_cap` |
| 18 | `HOOK_GIRL_DESTINATION_ACCEPT` | `girl_destination_accept` | `game/core/systems/events_dispatcher.rpy:8497` | `girl`, `destination` |
| 19 | `HOOK_ITEM_GENERATED` | `item_generated` | `game/core/systems/items.rpy:239` (`Item.generate_new_item`) | `item`, `template`, `tier` |

Notes:

- `event_triggering` fires before event dispatch and `event_finished` after it finishes; both carry the same context;
- `girl_sold` has two call sites (the two UI entry points for selling a girl);
- `game_saved`/`game_loaded` have no context keys (invoked without arguments);
- **No point in the current game code calls `cancel_hook()`** (§4); it is covered by tests (`game/core/tools/test_runner.rpy:352-353`) and is meant for mod authors to `call` themselves.
- `girl_destination_list` fires when acquiring a girl while the brothel is full: mod callbacks return a list of destinations `[{"id", "text", "available"}]`, which the core adds to the placement menu; if the player picks one, `girl_destination_accept` fires (`destination` = the destination id). Reference implementation: `game/custom/mods/Courtyard/mod.rpy` (the "Courtyard" mod).
- `item_generated` (**notification-only**, no return-value contract) fires **every time a template item is cooked into a concrete item** — roughly 400 times per new game during `init_items` (90 templates × their 4-5 applicable tiers). Context: `item` is the finished new item (`name`/`name_i18n`/`price`/`rarity`/`rank`/`base_effects` are already written; callbacks may mutate it in place and the change lands in that new game's item pool), `template` is the source template item, `tier` is the `QualityTier` used. Reference implementation: `game/custom/mods/Item Quality/` (the "Item Quality" mod).

---

## 4. API quick reference

All defined in `game/core/systems/mods/mod_api_v2.rpy`; there is also a service interface abstraction `game/core/systems/services/interfaces/i_mod_service.rpy`.

### Mod lifecycle

| Method | Line | Description |
|------|------|------|
| `register_mod(mod_id, manifest)` | `:80` | Register a v2 mod and immediately recompute the active set from persistent flags + dependencies, see §2.1 |
| `unregister_mod(mod_id)` | `:147` | Remove the mod (registry + active set) and clean up all its hooks |
| `is_mod_active(mod_id)` | `:263` | `mod_id in _active_mods` |
| `list_active_mods()` | `:266` | Returns the list of active mod_ids |
| `list_registered_mods()` | `:244` | Returns **all registered** mod_ids (including inactive) — used by the Mod Manager screen |
| `is_mod_enabled(mod_id)` | `:178` | Read the persistent enable flag; unrecorded ids default to `True` |
| `set_mod_enabled(mod_id, enabled)` | `:190` | Write the persistent flag and re-sync the in-memory active set (`ValueError` for unknown ids) |
| `apply_startup_states()` | `:203` | Idempotent rebuild of the active set; called from `before_main_menu` as a safety net |
| `missing_dependencies(mod_id)` | `:251` | Returns the dependency ids that are not currently active (for the 缺少前置 display) |

### UI integration

| Method | Line | Description |
|------|------|------|
| `get_menu_buttons()` | `:271` | `[(mod_id, display name, [button screen names])]`, only **active** mods declaring home menu buttons |
| `get_mod_info(mod_id)` | `:283` | Copy of the manifest for a registered mod (including inactive); returns `None` for unknown ids |

### Hooks

| Method | Line | Description |
|------|------|------|
| `register_hook(hook_name, callback, priority=0)` | `:297` | Register callback `callback(context)` (attributed `"_direct"`, not filtered by disable); higher priority runs first, sorted immediately at registration |
| `execute_hook(hook_name, **context)` | `:308` | Execute all callbacks of the hook (**skipping callbacks of inactive mods**, `:321-322`); returns `{mod_id: result}` (callbacks returning `None` are filtered; mod_id `"_direct"` means registered directly via `register_hook`); callback exceptions are swallowed with `renpy.notify` (developer mode), **never crashing the game** |
| `cancel_hook(hook_name)` | `:333` | Creates a `{"cancel": False}` context and invokes callbacks one by one (same inactive-mod skip at `:352-353`); returns `True` if any callback sets `context["cancel"] = True`. **Cannot be routed through `execute_hook`** (comment `:339-345`: `execute_hook` rebuilds the context with `**kwargs`, losing the cancel signal — a historical bug, now fixed) |

### Others (inherited from `ModAPI`, `mod_api.rpy`)

`register_trait` / `register_perk` / `register_tag` / `register_dialogue` / `register_event` / `register_ngp_setting` / `register_scenario` / `register_origin` / `register_game_mode` / `register_quality`, plus the v1-compatible `get_mod_path` / `is_mod_active` / `get_active_mods` (note the latter two operate on v1 `detected_mods`).

`register_quality(tier)` (`mod_api.rpy`) registers a `QualityTier` into `quality_registry` keyed by its `rank`; **same rank overwrites** (last registration wins), so a mod can both retune the default 0-6 tiers and extend beyond 7 (`Item.generate_new_item` caps `rank` at `quality_registry.get_max_rank()`, and `init_items` iterates `get_tiers()`). See §6.6.

### Verification tool

`python tools/verify_mod_api.py` — pure-Python static assertions + simulated execution (no Ren'Py runtime required):

- Asserts the 19 `HOOK_*` constants exist with unique values (`EXPECTED_HOOK_COUNT = 19`);
- Asserts `register_mod`/`unregister_mod`/`register_hook`/`execute_hook`/`cancel_hook`/`set_mod_enabled`/`is_mod_enabled`/`apply_startup_states`/`list_registered_mods`/`missing_dependencies` exist;
- Asserts the v1 base wrappers `register_trait`/`register_perk`/`register_event`/`register_quality`/`register_game_mode` exist and that `CAPABILITIES` includes `"items"`;
- Asserts every `api.HOOK_*` referenced by `mod_template.rpy` really exists;
- Simulates registration, duplicate-registration rejection, unknown-capability rejection, priority ordering, exception swallowing, the cancel flow, `get_menu_buttons`/`get_mod_info` behavior, persistent enable/disable (with a stubbed `persistent`), hook skipping for disabled mods, `always_on`, dependency resolution and `apply_startup_states` idempotence;
- Current result: **all passing**, with 5 naming-convention warnings (`girl_sold`/`girl_runaway`/`security_event`/`girl_destination_list`/`girl_destination_accept` lack the `_<tense>` suffix).

---

## 5. v1 compatibility layer (HookManager)

`game/core/systems/mods/mod_hooks.rpy` (`init -4 python`) is the Phase 6 centralized hook dispatcher; a v1 mod's `mod.hooks` dict is registered via `hook_manager.register(...)` at activation (`core_entities.rpy:254-257`).

- `hook_manager.register(hook_name, callback, mod=None)` / `unregister` / `unregister_mod`;
- `invoke(hook_name, *args, **kwargs)` returns a list of all callback results; `invoke_first` takes the first non-`None` result (used to override default behavior);
- Global convenience function `register_hook(hook_name, callback, mod=None)` (`mod_hooks.rpy:101`).

Note: this is a separate hook table independent of v2's `_mod_hooks`; same names but different storage. The v2 standardized hooks are the forward-looking interface for mod authors.

---

## 6. Full example: Auction House (authoritative v2 example)

Location: `game/custom/mods/Auction House/`, with three clearly separated files — the best sample to model a v2 mod on.

### 6.1 `mod.rpy` (44 lines) — registration entry + menu button

```renpy
init -1 python:
    services.mod_api_v2.register_mod("auction_house", {
        "name": __("Auction House"),
        "version": "2.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("..."),
        "requires": [],
        "hooks": {},
        "dependencies": [],
        "home_rightmenu_add_buttons": ["right_menu_auction"],
    })

screen right_menu_auction():
    hbox xalign 1.0 spacing 20:
        text ""
        textbutton _("Auction") style_group "rm":
            action Show("auction_house")
            tooltip __("访问拍卖行买卖女孩。")
```

Notes:

- **Standalone registration block**: registration lives in a separate `mod.rpy` at `init -1` (later than ModAPIV2's `init -3`, ensuring the service is registered);
- **mod_id decoupled from folder name**: `"auction_house"` is a stable id, unrelated to the folder name "Auction House";
- This mod needs no capabilities or hooks, so `requires`/`hooks`/`dependencies` are all empty — full fields make future extension easy;
- `home_rightmenu_add_buttons` points to the `right_menu_auction` screen defined in the same file: the home right-side menu "Mods" row embeds it via `use expression`; the button style follows `style_group "rm"` (right-menu button group) for a consistent look;
- The button action is `Show("auction_house")` — opening the mod's main screen.

### 6.2 `auction.rpy` (277 lines) — core business logic

Pure Python (`init -1 python`), fully separated from the UI. Four classes:

| Class | Responsibility |
|----|------|
| `AuctionBid` | A single bid: `bidder_name`, `amount`, `is_player`, `timestamp` |
| `AuctionLot` | A single lot (girl): state machine `pending/active/sold/unsold/cancelled`; `place_bid()` validates the minimum increment; `npc_bid()` simulates NPC bids based on enthusiasm (capped at the girl's buy price ×(0.8+0.7×enthusiasm)); `finalize()` closes the lot and returns `(status, winner, price)` |
| `AuctionSession` | One auction session: `start_bidding()` opens all lots; `advance_lot()` closes lots one by one; `auto_resolve()` simulates NPC bidding for all lots in the background; `player_buy_lot()` buys at reserve price; `player_sell_girl()` lists a girl from the MC's team as a lot |
| `AuctionHouse` | Persistent global instance (module-level `auction_house = AuctionHouse()` at the end): `history`, scheduling via `next_auction_day` + `frequency=30`, `generate_npc_lots()` generates random girls from the city |

Key points:

- **Reuses core APIs directly**: `girl.get_price("sell"/"buy", raw=True)`, `get_girls(count)`, `MC.gold`/`MC.girls`, `calendar.day` — v2 mods run in the same process as core code, so all of these are available;
- **All player-visible text wrapped in `__()`**, including status text `get_status_text()` and NPC names, ensuring it enters the translation system;
- **Module-level global instance** `auction_house` is the mod's runtime state (v2 has no v1-style `mod_settings` auto-persistence; if you need cross-save persistence, handle it yourself, e.g. via the `game_saved`/`game_loaded` hooks);
- This file has zero UI and zero registration, so it can be safely imported by the screen file.

### 6.3 `auction_screens.rpy` (331 lines) — UI layer

Two screens:

- `screen auction_house()`: main screen. `tag menu` + `modal True`; screen-local variables (`current_session`/`selected_lot`/`bid_amount`) manage interaction state; lot list on the left, details and bidding on the right (`-`/`+` adjustment, `出价` (Bid) button with `sensitive` validation of gold and increment, `立即购买` (Buy Now) only for NPC lots); bottom bar with `下一个拍品` (Next lot) / `自动结拍` (Auto-resolve) / `出售我的一个女孩` (Sell one of my girls) (`Show("auction_sell_girl", session=current_session)`) / `关闭` (Close).
- `screen auction_sell_girl(session)`: picks a girl from `MC.girls` to list; `Function(session.player_sell_girl, girl)` calls the core logic directly.

Key points:

- **Bridges UI events to Python methods via `Function(...)`**, connecting to the class methods in `auction.rpy`;
- Chinese UI text is written in Chinese directly and wrapped in `__()` (the project's target language), demonstrating that v2 mod text also enters the translation system;
- Migration fix record: the original `auction_sell_girl` referenced a nonexistent global `auction_house_session`; when moved into the mod it was changed to take an explicit `session` parameter — mods should avoid relying on implicit global session state.

### 6.4 Why this is the authoritative example

1. The three-way file split (registration/logic/UI) is the recommended structure for v2 mods;
2. It demonstrates the full chain of `home_rightmenu_add_buttons` from manifest to screen;
3. It demonstrates safe interaction with core global objects (`MC`, `calendar`, `get_girls`);
4. It demonstrates combining v2 with the i18n conventions (`__()`/`_()`).

### 6.5 Dependency example: Game Modes

`game/custom/mods/Game Modes/` (mod_id `"game_modes"`) demonstrates the persistent enable semantics and prerequisite dependencies:

```renpy
init -1 python:
    services.mod_api_v2.register_mod("game_modes", {
        ...
        "dependencies": [],
        "always_on": False,   # player-disableable; other mods can depend on it
    })

    ## EN: register modes only while active (disabled → empty registry →
    ##     the start flow falls back to plain story mode).
    ## ZH: 仅激活时注册模式；被禁用时注册表为空，开局回退剧情模式。
    if services.mod_api_v2.is_mod_active("game_modes"):
        gamemode_registry.register(StoryMode())
        gamemode_registry.register(SandboxMode())
        gamemode_registry.register(ScenarioMode())
```

How another mod declares the dependency:

```python
"dependencies": ["game_modes"]   # this mod activates only while game_modes is active
```

The mod folder's `README.txt` documents this convention (the Ren'Py launcher ignores non-`.rpy` files).

### 6.6 Data-driven extension example: Item Quality

`game/custom/mods/Item Quality/` (mod_id `"item_quality"`) is the reference for a **data-driven mod**: the core keeps the registry framework plus a hardcoded fallback, and the mod supplies hot-swappable data. It demonstrates `register_quality`, the `"items"` capability flag, the `item_generated` hook and a mod-owned translation directory all at once.

**Core-side framework** (`game/core/systems/registry/quality_registry.rpy`, `init -5`):

- `QualityTier(rank, price_modifier, prefixes, rarity_keep)` — `prefixes` maps adjective category → English prefix (missing keys fall back to `"misc"`); `rarity_keep` defaults to `("S","U","M")` (those rarities do not scale with the tier);
- `QualityRegistry` (extends `Registry`) — `register_quality(tier)` keyed by `str(rank)`, `get_tier(rank)`, `get_tiers()`, `get_max_rank()`;
- Hardcoded fallback `game/core/data/quality.rpy` (`init -4`, **do not delete**, identical to the mod's data so disabling the mod is invisible to players).

**Mod side** (three-way split: registration / logic / data):

```renpy
## mod.rpy — registration entry (init -1)
init -1 python:
    services.mod_api_v2.register_mod("item_quality", {
        "name": __("Item Quality"),
        "api_version": 2,
        "requires": ["items"],
        "always_on": False,
    })
    ## EN: Register tiers only while active; disabled -> core fallback stays.
    ## ZH: 仅激活时注册档位；禁用时保留核心兜底（数据一致）。
    if services.mod_api_v2.is_mod_active("item_quality"):
        load_quality_tiers()
```

```renpy
## quality.rpy — data loading (init -9, called by the init -1 block above)
init -9 python:
    import json
    QUALITY_JSON_PATH = "custom/mods/Item Quality/quality.json"

    def load_quality_tiers():
        ## EN: mod-local JSON via renpy.loader (Ren'Py archives included).
        ## ZH: 经 renpy.loader 读取 Mod 自带 JSON（兼容打包进归档）。
        try:
            with renpy.loader.load(QUALITY_JSON_PATH) as _f:
                _data = json.load(_f)
        except Exception as _e:
            renpy.notify(__("Item Quality mod: could not load quality.json (%s)") % _e)
            return   ## core fallback tiers stay in place; the game keeps running
        for _tier_data in _data.get("tiers", []):
            quality_registry.register_quality(QualityTier.from_dict(_tier_data))
```

How another mod overrides quality (same rank overwrites; new ranks extend the range):

```python
init -1 python:
    if services.mod_api_v2.is_mod_active("my_mod"):
        quality_registry.register_quality(QualityTier(
            rank=3, price_modifier=12.0,
            prefixes={"dress": "Gilded", "misc": "Gilded"},
        ))
```

Key takeaways:

1. **Framework in core, data in the mod**: `QualityRegistry` and `QualityTier` are core registries (`init -5`); the mod only feeds data — the game still starts with the mod disabled or deleted;
2. **init layering**: mod classes/functions must be defined before the registration entry point (`init -9` defines, `init -1` registers), same shape as Game Modes' `story_mode.rpy`;
3. **Mod-owned translation**: prefix entries live in `tl/chinese_simplified/quality.rpy`, and each `old` string must be **byte-identical** to the source (including trailing spaces such as `"Cheap "`); Ren'Py loads `tl/` unconditionally, so Chinese prefixes still apply while the mod is disabled;
4. **Uninstall degradation**: after deleting the folder, `__()` misses the entries and falls back to the English source text (acceptable degradation; see the mod's `README.txt`).

For comparison, the v1 tutorial example: `game/custom/mods/Goldo's cool mod/goldo's cool mod.rpy` (209 lines) demonstrates the full v1 flow — `Mod(...)` construction, `help_prompts` option menu, `early_label`/`init_label` labels, `events` + `add_event()` scheduling (alarm/morning/city types), `set_condition` conditional events, custom `register_trait`, and a `home_rightmenu_add_buttons` button screen.

---

## 7. Legacy items and known issues

| Item | Status | Description |
|----|------|------|
| v2 `min_game_version` validation | 📝 Known limitation | Recorded but not enforced (declarative semantics) |
| v2 `dependencies` validation | ✅ Implemented | Enforced: the mod stays inactive until every dependency is active (`_rebuild_active_mods`, `mod_api_v2.rpy:219-242`) |
| manifest `hooks` registration priority always 0 | 📝 By design | When priority is needed, register separately via `register_hook(..., priority=N)` |
| `register_hook()` callbacks are not filtered by disable | 📝 By design | `"_direct"` callbacks cannot be attributed to a mod; use manifest `hooks` if the callback must stop with a disabled mod |
| `cancel_hook` has no in-game call site | 📝 Known | Covered only by tests; meant for mods/scripts to call themselves |
| 5 hook names don't follow `<domain>_<action>_<tense>` | 📝 Known | `girl_sold` / `girl_runaway` / `security_event` / `girl_destination_list` / `girl_destination_accept`; verify_mod_api emits warnings; renaming would break registered callbacks, so left as-is |
| v2 enable-state persistence | ✅ Implemented | Enable/disable flags stored in `persistent._bk_v2_mod_states` (toggled in the main-menu Mod Manager screen); custom mod content data still needs manual persistence via the `game_saved`/`game_loaded` hooks |
| Mod content translation | ✅ Available (mod-owned) | Each mod ships its own translations in `<mod>/tl/chinese_simplified/*.rpy` (the `old` string must be byte-identical to the source, trailing spaces included); Ren'Py loads `tl/` unconditionally, so entries still apply while the mod is disabled, and deleting the mod falls back to the English source. Example: `game/custom/mods/Item Quality/tl/chinese_simplified/` |

---

## Related documents

- [`CUSTOM_DIRECTORIES.md`](CUSTOM_DIRECTORIES.md) — directory boundaries of `game/custom/` and `game/core/`
- [`../tools/TOOLS.md`](../tools/TOOLS.md) — tool inventory including `tools/verify_mod_api.py`
- [`../../game/core/templates/mod_template/mod_template.rpy`](../../game/core/templates/mod_template/mod_template.rpy) — blank v2 mod template
- [`../../game/custom/mods/Auction House/mod.rpy`](../../game/custom/mods/Auction%20House/mod.rpy) — v2 example entry
- [`../../game/custom/mods/Item Quality/README.txt`](../../game/custom/mods/Item%20Quality/README.txt) — data-driven mod example (`register_quality` + mod-owned translations)
- [`../../game/custom/mods/Goldo's cool mod/goldo's cool mod.rpy`](../../game/custom/mods/Goldo's%20cool%20mod/goldo's%20cool%20mod.rpy) — v1 tutorial example
