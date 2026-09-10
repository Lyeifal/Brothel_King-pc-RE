# BK Evolution — Mod API Reference (v1 + v2)

> Last updated: 2026-09-11 (verified against code)
>
> This document is the authoritative reference for Brothel King Evolution's Mod mechanisms, covering both the legacy v1 `Mod()` class and the new `ModAPIV2`.
> All line numbers, parameters, and behavior reflect the current code (branch `bk-evolution`).

---

## 0. Quick choice: v1 or v2?

| | v1 (`Mod()`) | v2 (`ModAPIV2`) |
|---|---|---|
| Entry point | Instantiate the `Mod(...)` class | `services.mod_api_v2.register_mod(mod_id, manifest)` |
| Registration | Automatically added to `detected_mods` at construction | Explicit manifest registration, with validation |
| Activation semantics | **Per-save toggle**: can be activated/deactivated in the main-menu Mods screen; state stored in `persistent.mods` | **Always active**: dropping the folder into `game/custom/mods/` is enough; no toggle |
| How to deactivate | Deactivate in the Mods screen | Delete the entire `game/custom/mods/<Mod>/` folder |
| Lifecycle labels | `early/init/night/update/load/remove_label` + `chapter_labels` | No label mechanism; use hooks (`game_saved`/`game_loaded`, etc.) |
| Home right-menu buttons | `home_rightmenu_add_buttons` | Manifest `home_rightmenu_add_buttons` (new support in v2) |
| Event registration | `events={...}` + `add_event()` | Inherited `ModAPI.register_event()` and other Registry wrappers |
| Hook system | `mod.hooks` dict → `HookManager` (Phase 6 compatibility layer) | Manifest `hooks` or `register_hook()` → standardized hooks |
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
   - Note: the main-menu "Mods" button is only shown when `detected_mods` is non-empty (`game/core/config/screens.rpy:999`); all v1 toggling happens in this screen.
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
Singleton: `mod_api_v2 = ModAPIV2()` (`:205`), registered into the service container `services.register("mod_api_v2", mod_api_v2)` (`:206`), accessible as `services.mod_api_v2` (attribute defined at `game/core/systems/services/service_container.rpy:109-111`). Because it inherits `ModAPI`, v1's `register_trait` / `register_event` and other Registry wrapper methods are also available on v2 (`game/core/systems/mods/mod_api.rpy`).

### 2.1 `register_mod(mod_id, manifest)` and full manifest fields

Signature: `game/core/systems/mods/mod_api_v2.rpy:50`.

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
    "dependencies": ["other_mod"],   # List of mod_ids this mod depends on (declarative; not enforced currently)
    "home_rightmenu_add_buttons": ["my_screen"],  # Home right-menu button screen list, see §2.3
})
```

Field-by-field explanation:

| Field | Type | Required | Validation/behavior |
|------|------|------|-----------|
| `name` | str | Recommended | Display name for `get_menu_buttons()` / `get_mod_info()`; falls back to `mod_id` when missing |
| `version` | str | Recommended | Display only. The code does not parse or compare it |
| `api_version` | int | **Yes** | Must `== 2`, otherwise `ValueError` (`mod_api_v2.rpy:74-76`) |
| `min_game_version` | str | No | Recorded only. **Not enforced in current code** |
| `author` | str | Recommended | Display only |
| `description` | str | Recommended | Display only (Mods screen) |
| `requires` | [str] | No | Each item must be in the `CAPABILITIES` set, otherwise `ValueError` (`:78-80`), see §2.2 |
| `hooks` | {str: callable} | No | Each callback is registered into `_mod_hooks` as `(mod_id, callback, 0)` (`:88-89`) |
| `dependencies` | [str] | No | Recorded only. **Current code does not check** whether dependencies are registered |
| `home_rightmenu_add_buttons` | [str] | No | List of no-argument screen names, see §2.3 |

Registration-time validation summary (`:73-83`):

1. `api_version != 2` → `ValueError`;
2. `requires` contains an unknown capability flag → `ValueError`;
3. **Registering the same `mod_id` twice → `ValueError`** (`:82-83`) — avoid double registration when init reruns.

When `renpy.config.developer` is true, successful registration logs output via `renpy.log` (`:91-93`).

### 2.2 Always-active semantics and capability flags

**Always active** (explicitly commented at `mod_api_v2.rpy:67-71`):

- v2 mods are **active as soon as installed** — dropping the folder into `game/custom/mods/` gets it loaded by Ren'Py and executes the registration block; there is no per-save toggle;
- **Deactivation = deleting the files**: just remove the mod folder from `game/custom/mods/`;
- State is not written to `persistent.mods` (that's the v1 mechanism); v2's `_active_mods` is an in-memory registration table built at init time;
- `unregister_mod(mod_id)` (`:95-99`) exists but is mainly for testing/hot-reload scenarios; normal mods don't need to call it.

**Capability flags** (`CAPABILITIES`, `mod_api_v2.rpy:30-41`) — declare which capability surfaces a mod needs; currently used for registration-time validation and documentation semantics:

```python
"girl_stats"    # Modify girl stats
"girl_traits"   # Register custom traits/perks
"economy"       # Modify economy calculations
"events"        # Register/dispatch events
"dialogue"      # Custom dialogue lines
"pictures"      # Custom picture tags
"game_modes"    # Register custom game modes
"origin"        # Register player origins
"scenario"      # Register scenarios
"ngp_settings"  # NG+ settings
```

### 2.3 home_rightmenu_add_buttons (v2)

Manifest field; the value is a **list of no-argument screen names**. `get_menu_buttons()` (`:109-119`) returns `[(mod_id, display name, [button screen names])]` — containing only active mods that declare buttons. The home right-side menu fetches the list at `screen_home.rpy:65-69` via `services.mod_api_v2.get_menu_buttons()` and renders it through the `v2_buttons` parameter of `screen mod_menu_display` (`screen_home.rpy:395-401`), displayed alongside v1 mod buttons and grouped by mod.

### 2.4 Lifecycle hooks

v2 has no v1 label mechanism; lifecycle events are covered via hooks:

- `game_saved`: triggered on every save via `renpy.config.save_json_callbacks` (`mod_api_v2.rpy:214-218`, with duplicate-registration protection);
- `game_loaded`: triggered in `label after_load` (`events_dispatcher.rpy:189-191`, guarded by `hasattr` for compatibility with old saves).

---

## 3. Complete hook point reference (18)

Constant definitions: `game/core/systems/mods/mod_api_v2.rpy:187-204`. Naming convention: `<domain>_<action>_<tense>` (three names — `girl_runaway`, `girl_sold`, `security_event` — lack `_<tense>`; `tools/verify_mod_api.py` emits a naming-convention warning for these, which is a known item).

All callback signatures are uniformly `callback(context: dict)`; `execute_hook` packs the keyword arguments into a context dict and passes it in (`mod_api_v2.rpy:143-159`).

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

Notes:

- `event_triggering` fires before event dispatch and `event_finished` after it finishes; both carry the same context;
- `girl_sold` has two call sites (the two UI entry points for selling a girl);
- `game_saved`/`game_loaded` have no context keys (invoked without arguments);
- **No point in the current game code calls `cancel_hook()`** (§4); it is covered by tests (`game/core/tools/test_runner.rpy:352-353`) and is meant for mod authors to `call` themselves.
- `girl_destination_list` fires when acquiring a girl while the brothel is full: mod callbacks return a list of destinations `[{"id", "text", "available"}]`, which the core adds to the placement menu; if the player picks one, `girl_destination_accept` fires (`destination` = the destination id). Reference implementation: `game/custom/mods/Courtyard/mod.rpy` (the "Courtyard" mod).

---

## 4. API quick reference

All defined in `game/core/systems/mods/mod_api_v2.rpy`; there is also a service interface abstraction `game/core/systems/services/interfaces/i_mod_service.rpy`.

### Mod lifecycle

| Method | Line | Description |
|------|------|------|
| `register_mod(mod_id, manifest)` | `:50` | Register a v2 mod, see §2.1 |
| `unregister_mod(mod_id)` | `:95` | Remove the mod and clean up all its hooks |
| `is_mod_active(mod_id)` | `:101` | `mod_id in _active_mods` |
| `list_active_mods()` | `:104` | Returns the list of active mod_ids |

### UI integration

| Method | Line | Description |
|------|------|------|
| `get_menu_buttons()` | `:109` | `[(mod_id, display name, [button screen names])]`, only mods declaring home menu buttons |
| `get_mod_info(mod_id)` | `:121` | Copy of the manifest (for display in the Mods screen); returns `None` for unknown ids |

### Hooks

| Method | Line | Description |
|------|------|------|
| `register_hook(hook_name, callback, priority=0)` | `:132` | Register callback `callback(context)`; higher priority runs first, sorted immediately at registration |
| `execute_hook(hook_name, **context)` | `:143` | Execute all callbacks of the hook; returns `{mod_id: result}` (callbacks returning `None` are filtered; mod_id `"_direct"` means registered directly via `register_hook`); callback exceptions are swallowed with `renpy.notify` (developer mode), **never crashing the game** |
| `cancel_hook(hook_name)` | `:161` | Creates a `{"cancel": False}` context and invokes callbacks one by one; returns `True` if any callback sets `context["cancel"] = True`. **Cannot be routed through `execute_hook`** (comment `:167-173`: `execute_hook` rebuilds the context with `**kwargs`, losing the cancel signal — a historical bug, now fixed) |

### Others (inherited from `ModAPI`, `mod_api.rpy`)

`register_trait` / `register_perk` / `register_tag` / `register_dialogue` / `register_event` / `register_ngp_setting` / `register_scenario` / `register_origin` / `register_game_mode`, plus the v1-compatible `get_mod_path` / `is_mod_active` / `get_active_mods` (note the latter two operate on v1 `detected_mods`).

### Verification tool

`python tools/verify_mod_api.py` — pure-Python static assertions + simulated execution (no Ren'Py runtime required):

- Asserts the 16 `HOOK_*` constants exist with unique values (`EXPECTED_HOOK_COUNT = 16`);
- Asserts `register_mod`/`unregister_mod`/`register_hook`/`execute_hook`/`cancel_hook` exist;
- Asserts every `api.HOOK_*` referenced by `mod_template.rpy` really exists;
- Simulates registration, duplicate-registration rejection, unknown-capability rejection, priority ordering, exception swallowing, the cancel flow, and `get_menu_buttons`/`get_mod_info` behavior;
- Current result: **all passing**, with 3 naming-convention warnings (`girl_sold`/`girl_runaway`/`security_event` lack the `_<tense>` suffix).

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

For comparison, the v1 tutorial example: `game/custom/mods/Goldo's cool mod/goldo's cool mod.rpy` (209 lines) demonstrates the full v1 flow — `Mod(...)` construction, `help_prompts` option menu, `early_label`/`init_label` labels, `events` + `add_event()` scheduling (alarm/morning/city types), `set_condition` conditional events, custom `register_trait`, and a `home_rightmenu_add_buttons` button screen.

---

## 7. Legacy items and known issues

| Item | Status | Description |
|----|------|------|
| v2 `min_game_version` / `dependencies` validation | 📝 Known limitation | Recorded but not enforced (comment at `mod_api_v2.rpy:50` declares the semantics) |
| manifest `hooks` registration priority always 0 | 📝 By design | When priority is needed, register separately via `register_hook(..., priority=N)` |
| `cancel_hook` has no in-game call site | 📝 Known | Covered only by tests; meant for mods/scripts to call themselves |
| 3 hook names don't follow `<domain>_<action>_<tense>` | 📝 Known | `girl_sold` / `girl_runaway` / `security_event`; verify_mod_api emits warnings; renaming would break registered callbacks, so left as-is |
| v2 state persistence | 🚧 To be planned | v1's `mod_settings` auto-saves with the save file; v2 mods must implement it themselves via the `game_saved`/`game_loaded` hooks |
| Mod content translation | ⏳ To be planned | `game/custom/` content stays in its original language by default; may be supported in the future via a unified string table |

---

## Related documents

- [`CUSTOM_DIRECTORIES.md`](CUSTOM_DIRECTORIES.md) — directory boundaries of `game/custom/` and `game/core/`
- [`../tools/TOOLS.md`](../tools/TOOLS.md) — tool inventory including `tools/verify_mod_api.py`
- [`../../game/core/templates/mod_template/mod_template.rpy`](../../game/core/templates/mod_template/mod_template.rpy) — blank v2 mod template
- [`../../game/custom/mods/Auction House/mod.rpy`](../../game/custom/mods/Auction%20House/mod.rpy) — v2 example entry
- [`../../game/custom/mods/Goldo's cool mod/goldo's cool mod.rpy`](../../game/custom/mods/Goldo's%20cool%20mod/goldo's%20cool%20mod.rpy) — v1 tutorial example
