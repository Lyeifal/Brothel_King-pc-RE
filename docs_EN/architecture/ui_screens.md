# UI Screen Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/ui/screens.rpy` (620 lines, formerly 8,886 lines), `game/core/ui/screens/` (16 files, 9,240 lines total)
> **Phase**: Phase 2/3 (screens extracted by domain)

---

## 1. System Responsibilities

All in-game screens in BK were extracted from the monolithic `screens.rpy` into separate files under `ui/screens/` by business domain. After extraction:

- `screens.rpy` keeps only **image declarations** (`image` statements, starting around line 11), **custom styles** (styles inside the `init:` block, starting around line 133), **transforms** (starting around line 180), and **5 labels**; it contains **no screens at all** (`^screen ` count is 0).
- `ui/screens/` holds all ~90+ screen definitions, split by domain into 15 `screen_*.rpy` files + 1 `__init__.rpy`.
- Every extracted block in the original file carries a migration comment (e.g. screens.rpy:325-343) noting the destination file and Phase, usable as an index.

## 2. What Remains in screens.rpy (620 lines)

| Category | Location | Content |
|----------|----------|---------|
| Image declarations | Around lines 11-63 | UI icons (`img_AP`, `img_gold`, `filter_*`, etc.), thumbnail buttons (`tb_*`), background images |
| Custom styles | `init:` block at line 133 | Global style definitions kept after extraction |
| Transforms | From line 180 | Common transforms (including Dexell's updated versions) |
| Labels | Lines 474 / 497 / 536 / 547 / 566 | `girlpack_menu`, `girlpack_menu_restart`, `pic_test`, `farm_pic_test`, `packstates_menu` — entry points for girl pack management and picture test flows |

## 3. File Inventory of `ui/screens/` (16 files)

Screen lists were verified per file via grep:

| File | Lines | Screen list |
|------|------:|-------------|
| `__init__.rpy` | — | Package description comment |
| `screen_common.rpy` | — | See §4 (shared screens) |
| `screen_brothel.rpy` | — | `brothel`, `furniture` |
| `screen_districts.rpy` | — | `districts`, `district_button`, `visit_district`, `visit_location`, `matchmaking`, `customer_satisfaction` |
| `screen_farm.rpy` | — | `farm_menu`, `farm_tab`, `minion_button`, `fshow_init` |
| `screen_girl_list.rpy` | — | `girls` |
| `screen_girl_log.rpy` | — | `girl_log`, `previous_night_log` |
| `screen_girl_profile.rpy` | — | `girl_profile` |
| `screen_girl_stats.rpy` | — | `stat_bar`, `custom_bar`, `girl_stats`, `assign_job`, `girl_stats_light`, `trait_details`, `perk_details` |
| `screen_home.rpy` | — | `home`, `brothel_report` |
| `screen_misc.rpy` | — | `tax_tooltip`, `tax_tab`, `adv_tooltip`, `girls`, `girl_tab`, `girl_pick_badge`, `badge_button`, `girl_button`, `girl_fast_actions`, `button_overlay`, `rank_level_details` |
| `screen_misc2.rpy` | — | `suzume_hints`, `restock_button`, `inventory_filter`, `girl_select`, `main_character`, `personality_screen`, `notebook`, `fshow_screen`, `farm_show_gold`, `generic_event_screen`, `mood_details`, `love_button`, `fear_button`, `sex_details` |
| `screen_powers.rpy` | — | `mojo_bar`, `power_detail`, `power_draw`, `power_hand`, `power_card`, `power_card_content`, `power_target`, `girl_vp_selector`, `mojo_payment`, `mojo_trade`, `micro_transac`, `brothel_ranking`, `scroll_list`, `brothel_ranking_button`, `harem_button` |
| `screen_progress.rpy` | — | `autorest`, `level`, `perks` |
| `screen_quest.rpy` | — | `active_spells`, `spellbook`, `postings`, `challenge_menu`, `challenge`, `letter`, `modal`, `invisible_button`, `mods`, `free_girl_interact`, `girl_interact`, `free_girl_stats`, `debug_pics`, `girl_mix`, `pic_tester` |
| `screen_resources.rpy` | — | `resource_tab`, `resource_gain`, `resource_exchange`, `achievement_notification`, `crystal_display`, `achievements`, `contracts`, `contract_tab`, `pick_girl`, `contract_result`, `increment_counter`, `increment_display`, `auction_brothel`, `goal_ttip` |
| `screen_schedule.rpy` | — | `schedule`, `save_schedule`, `load_schedule` |

Note: the table lists only `screen` statements; each file also contains companion python utility functions and styles.

## 4. Shared Screens: screen_common.rpy

Foundational screens reused across domains, referenced by other screen files via `use` or `call screen`:

`tool`, `overlay`, `quick_start`, `dark_filter`, `yes_no`, `OK_screen`, `show_img`, `show_event`, `show_sex_event`, `shortcuts`, `close`, `receive_item`

One of the extraction rules is "generic widgets referenced by 3+ domains go into `screen_common.rpy`."

## 5. Extraction Rules

1. **Cluster by business domain**: screens of the same functional domain move together with their private python utility functions, keeping files cohesive (e.g. the schedule trio, the powers fifteen-piece set).
2. **Shared sinks down**: cross-domain widgets go into `screen_common.rpy`; global styles/images/transforms stay in `screens.rpy`.
3. **Leave a comment index**: the original location gets an `## EXTRACTED to ui/screens/xxx.rpy (Phase N)##` comment for traceability.
4. **Do not change call sites**: Ren'Py screens resolve by name, so `call screen xxx` / `use xxx` need no modification when files move.
5. **Coordinate with componentization**: extraction of screens such as `girl_profile` (Phase 3.1) proceeded in the same batch of work as Girl componentization.

## 6. Other UI-Layer Files (Boundary Notes)

- `game/core/ui/main.rpy` — main interaction loop (contains call sites such as the girl_sold hook).
- `game/core/ui/notify.rpy`, `content_menu.rpy`, `screen_home.rpy` (another copy at the ui/ root) — notifications and content menu.
- `game/core/config/screens.rpy` — engine-level Ren'Py screens (say/choice/nvl/file, etc.), layered separately from game screens and not part of this extraction.

---

## Related Documentation

- [girl_components.md](girl_components.md) — Girl componentization (contemporary work)
- [mod_system.md](mod_system.md) — the v2 Mod `home_rightmenu_add_buttons` points at screens in this layer
- [editor_suite.md](editor_suite.md) — girl pack/scenario editors related to screens
