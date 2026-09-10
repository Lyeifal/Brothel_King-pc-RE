# BK Evolution — Data-Driven Migration Records

> Last updated: 2026-09-11 (verified against code)
>
> **Status: migration concluded ✅ (the original 12 core domains and all additional domains have been fully converted to JSON); fallbacks retained.**
> **This document is a historical record + current data inventory** and no longer tracks new tasks; entries not marked ✅ in the remaining inventory below are intentionally kept (runtime dynamic data, hardcoded fallbacks, or low-value inline mappings).
>
> Created on: 2026-06-08
> Original current phase: Phase 7.5 (comprehensive hardcoded audit) — completed
>
> ## Post-migration architecture quick reference (verified against code 2026-09-11)
>
> | Layer | Location | Description |
> |----|------|------|
> | Authoritative data | `game/core/data/<domain>/*.json` | 36 subdirectories total (including `_schemas/`); load points see `DataLoader` (`game/core/systems/data_loader.rpy`) |
> | Schema validation | `game/core/data/_schemas/*.schema.json` | One JSON Schema per domain |
> | Loader | `game/core/systems/data_loader.rpy` | All `load_*()` class methods, JSON preferred |
> | Registries | `game/core/systems/registry/` | `registry.rpy` base class + nine Registries: trait/perk/tag/dialogue/event/meta/ngp/unlock |
> | Hardcoded fallback | `game/core/data/*.rpy` (`items.rpy`, `jobs.rpy`, `perks.rpy`, `powers.rpy`, `settings.rpy`, `spells.rpy`) and `_fallback_*` inside various .rpy files | Ensures the game can start when JSON is missing; **do not delete** |
> | Data export | `game/core/systems/data_exporter.rpy` | `export_*()` symmetric with DataLoader |
> | Visual editing | `tools/bk_editor/` | Editor suite; mapping see `tools/bk_editor/README.md` |
>
> ⚠️ The only deviation from the original plan: the target path `data/assets/*.json` in overview row #14 "Picture/audio lists" was **not adopted** — that content was actually split into `settings/audio_registry.json` (audio registry) and `settings/picture_mappings.json` (picture mappings); the `data/assets/` directory does not exist.

---

## Migration principles

1. **JSON first, .rpy fallback** — new JSON is the preferred data source; keep hardcoded `.rpy` as fallback
2. **Schema first** — every JSON must have a `.schema.json` defining its structure first
3. **Unified loading via DataLoader** — all JSON loads through `DataLoader.load_*()` methods
4. **`from_dict()` deserialization** — every class must have a `from_dict()` class method
5. **Test after removing scripts** — run `tools/clean_runtime.ps1` after each migration and verify by actually playing

---

## Overall progress

> i18n status: 🌐 complete | ⏳ pending | ⚠️ N/A (identifiers/picture paths/keys)

| # | Domain | Priority | Source file | Target JSON | Migration status | i18n status | Completion date |
|------|------|--------|--------|-----------|----------|-----------|----------|
| 1 | Item system | ⭐⭐⭐ | `data/items.rpy` | `data/items/items.json` | ✅ Complete | 🌐 Complete | 2026-06-10 |
| 2 | Jobs/performances | ⭐⭐⭐ | `data/jobs.rpy` | `data/jobs/perform_job_dict.json` | ✅ Complete | ⚠️ N/A (pure data structure) | 2026-06-08 |
| 3 | Brothel parameters | ⭐⭐⭐ | `init/settings.rpy` | `data/economy/brothel_params.json` | ✅ Complete | ⚠️ N/A | 2026-06-08 |
| 4 | Shop system (phases 1-4) | ⭐⭐⭐ | `init/settings.rpy` + `core_entities.rpy` + `economy.rpy` | `data/shops/*.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| 5 | Tax system | ⭐⭐⭐ | `init/settings.rpy` | `data/economy/tax_params.json` | ✅ Complete | ⚠️ N/A | 2026-06-08 |
| 6 | Minion | ⭐⭐ | `init/variables.rpy` | `data/minions/minions.json` | ✅ Complete | 🌐 Complete (value-level) | 2026-06-08 |
| 7 | Farm installations | ⭐⭐ | `init/variables.rpy` | `data/farm/installations.json` | ✅ Complete | ⚠️ N/A | 2026-06-08 |
| 8 | Rooms/buildings | ⭐⭐ | `init/variables.rpy` | `data/rooms/rooms.json` | ✅ Complete | ⚠️ N/A | 2026-06-08 |
| 9 | Powers/spells (Powers) | ⭐⭐ | `data/powers.rpy` | `data/powers/powers.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| 10 | Spells/moon phases (Spells + Moons) | ⭐⭐ | `data/spells.rpy` | `data/spells/spells.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| 11 | MC classes/spellbooks (MC Classes) | ⭐⭐ | `data/spells.rpy` | `data/classes/mc_classes.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| 12 | Difficulty parameters | ⭐⭐ | `init/settings.rpy` | `data/difficulty/difficulty.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| 13 | Goal system UI | ⭐ | `init/variables.rpy` | `data/goals/goal_ui.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| 14 | Picture/audio lists | ⭐ | `init/settings.rpy` | ~~`data/assets/images.json` + `data/assets/audio.json`~~ → actually split into `settings/picture_mappings.json` + `settings/audio_registry.json` | ✅ Complete (paths adjusted, see header note) | 🌐/⚠️ Mixed | 2026-06-08 |
| — | Fixations | ⭐⭐ | `init/variables.rpy` | `data/fixations/fixations.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Interaction menu tree | ⭐⭐ | `init/variables.rpy` | `data/interactions/*.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Traits | ⭐⭐ | `data/traits.rpy` | `data/traits/traits.json` | ✅ Complete | 🌐 Complete (limited) | 2026-06-08 |
| — | Perks | ⭐⭐ | `data/perks.rpy` | `data/perks/perks.json` | ✅ Complete | 🌐 Complete (limited) | 2026-06-08 |
| — | Achievements | ⭐ | `systems/achievements.rpy` | `data/achievements/achievements.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Challenges | ⭐ | `framework/functions.rpy` | `data/challenges/challenges.json` | ✅ Complete | ⚠️ N/A | 2026-06-08 |
| — | Contracts | ⭐ | `framework/functions.rpy` | `data/contracts/contracts.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Resources | ⭐ | `framework/functions.rpy` | `data/resources/resources.json` | ✅ Complete | ⚠️ N/A | 2026-06-08 |
| — | Customers | ⭐ | `systems/customer/` | `data/customers/customer_affixes.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Cleanliness | ⭐ | `init/start.rpy` | `data/settings/cleanliness_penalties.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Treasure | ⭐ | `init/start.rpy` | `data/settings/treasure_thresholds.json` | ✅ Complete | ⚠️ N/A | 2026-06-08 |
| — | Meta Progression | ⭐ | `systems/registry/` | `data/meta/meta_progression.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | NGP Settings | ⭐ | `systems/registry/` | `data/ngp/ngp_settings.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Stats | ⭐ | `init/variables.rpy` | `data/stats/stats.json` | ✅ Complete | 🌐 Complete (value-level) | 2026-06-08 |
| — | Ranks | ⭐ | `init/variables.rpy` | `data/ranks/ranks.json` | ✅ Complete | 🌐 Complete (value-level) | 2026-06-08 |
| — | Personalities | ⭐ | `init/variables.rpy` | `data/personalities/personalities.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Origins | ⭐ | `systems/gamemodes/` | `data/sandbox/origins.json` | ✅ Complete | 🌐 Complete | 2026-06-08 |
| — | Scenarios | ⭐ | `systems/gamemodes/` | `data/scenarios/scenarios.json` | ✅ Complete | ⚠️ N/A (empty) | 2026-06-08 |

---

## Newly completed in this session (2026-06-08)

| Domain | Source file | Target JSON | Completion date | Notes |
|------|--------|-----------|----------|------|
| Item system | `data/items.rpy` | `data/items/items.json` | 2026-06-08 | 90 template + 103 regular items; `Item.from_dict()` / `Item.to_dict()`; Schema created |
| Jobs/performances | `data/jobs.rpy` | `data/jobs/perform_job_dict.json` | 2026-06-08 | 170 dictionary entries; pure dict structure needs no `from_dict()`; `_fallback_perform_job_dict` fallback |
| Brothel parameters | `init/settings.rpy` | `data/economy/brothel_params.json` | 2026-06-08 | 5 parameter groups (capacity, helpers, reputation_cap, cost, pics); string keys auto-converted to int keys |
| Shop system (phases 1-4 + A+B) | `init/settings.rpy` + `core_entities.rpy` + `economy.rpy` | `data/shops/*.json` | 2026-06-08 | 11 shops + 10 upgrades + unlock batches + district bindings + chapter price multipliers/stock growth/time pressure + `item_type_weights` probability weights; `NPC.restock()` fully data-driven; `ItemInstance._price_multiplier` |
| Tax system | `init/settings.rpy` | `data/economy/tax_params.json` | 2026-06-08 | `tax_brackets` + `tax_chapter_penalty` + `tax_time_pressure_maximum` + `tax_random_range`; string keys auto-converted to int keys |
| Minion | `init/variables.rpy` | `data/minions/minions.json` | 2026-06-08 | `all_minion_types` + `minion_description` + `minion_xp_to_level` + `minion_price` + `farm_pics`; string keys auto-converted to int keys |
| Farm installations | `init/variables.rpy` | `data/farm/installations.json` | 2026-06-08 | `installation_price` + `farm_type_list` + `farm_inst_list` + `farm_installations_dict`; string keys auto-converted to int keys |
| Rooms/buildings | `init/variables.rpy` | `data/rooms/rooms.json` | 2026-06-08 | `room_pics` + `room_dict` + `common_room_dict` + `master_bedrooms` + `job_room_dict` + `room_capacity`; string keys auto-converted to int keys |
| Powers/spells | `data/powers.rpy` | `data/powers/powers.json` | 2026-06-08 | 61 normal + 61 super EvilPower; `EvilPower.from_dict()`; hardcoded fallback retained |
| Spells/moon phases | `data/spells.rpy` | `data/spells/spells.json` | 2026-06-08 | `shield_effect` + `bshield_effect` + `bshield_spell` + `moons` (12 moon phases); fallback retained |
| MC classes/spellbooks | `data/spells.rpy` | `data/classes/mc_classes.json` | 2026-06-08 | 3 classes (Warrior/Trader/Wizard) + spellbooks + `modes` + `icon` + `description`; origin `available_classes` restrictions; dynamic UI filtering |
| Difficulty parameters | `data/settings.rpy` + `init/settings.rpy` | `data/difficulty/difficulty.json` | 2026-06-08 | 5 difficulty levels + `name_i18n` / `description_i18n` for 13 settings; loaded with override at `init/settings.rpy` `init 1`; hardcoded fallback in `data/settings.rpy` retained |
| Goal system UI | `init/variables.rpy` | `data/goals/goal_ui.json` | 2026-06-08 | 8 channels + 4 non-story channels + 8 category mappings + 8 tooltip buttons + 4 color constants; loaded with override at `init/settings.rpy` `init 1`; hardcoded fallback in `variables.rpy` retained |
| Fixations (癖好/执念) | `init/variables.rpy` | `data/fixations/fixations.json` | 2026-06-08 | 55 Fixation definitions + 275 `_i18n` texts (description/action/intro/pos_reaction/neg_reaction); `Fixation.from_dict()`; rebuilds `fix_dict` + `fix_description` at `init/settings.rpy` `init 1`; hardcoded fallback in `variables.rpy` retained |
| Interaction menu tree | `init/variables.rpy` | `data/interactions/interact_dict.json` + `free_interact_dict.json` | 2026-06-08 | 22 slave menus (5 submenus + 64 topics) + 14 free-girl menus (4 submenus + 42 topics); `GirlInteractionTopic.from_dict()`; override at `init/settings.rpy` `init 1`; hardcoded fallback in `variables.rpy` retained |
| Tag dictionary | `init/settings.rpy` | `settings/tags.json` | 2026-06-08 | 180 tag mappings; code tags (non-`_i18n`); loaded at `init -10`; `tag_registry.register_tags_bulk()` |
| Picture mappings | `init/settings.rpy` | `settings/picture_mappings.json` | 2026-06-08 | 7 picture mapping groups (advertising/pony/security/arson/violent/treasure/no_girls); loaded at `init -10` |
| Help text | `systems/help.rpy` | `settings/help_texts.json` | 2026-06-08 | 109 help texts + 16 picture mappings; `_i18n` texts + post-processing with `__()`; hyperlink compilation logic retained |
| City encounters | `init/variables.rpy` | `settings/encounters.json` | 2026-06-08 | `pop_name_dict` + `encounters` + `encounter_pics`; tuple structures auto-restored; loaded at `init 1` |
| Security parameters | `init/variables.rpy` | `settings/security_params.json` | 2026-06-08 | `security_events` + `alert_limits1` + `alert_limits2`; int keys auto-converted; tuples auto-restored; loaded at `init 1` |
| Training tests | `init/variables.rpy` | `settings/training_tests.json` | 2026-06-08 | `training_test_dict` + `magic_training_test_dict`; loaded at `init 1` |
| Quest parameters | `init/variables.rpy` | `settings/quest_params.json` | 2026-06-08 | `quest_base_gold` + `class_prices`; int keys auto-converted; loaded at `init 1` |
| Inventory sorting/filtering | `init/variables.rpy` | `settings/inventory_sorters.json` | 2026-06-08 | `inventory_filters` + `filter_list` + `sorter_dict` (20 sorters + 9 filters + 6 filter lists); `caption_i18n`/`tooltip_i18n` translatable; loaded at `init -3` to keep screens usable |
| Sex training parameters | `init/variables.rpy` | `settings/sex_training_params.json` | 2026-06-08 | `base_reluctance` + `preference_modifier` + `preference_limit` + `experienced_modifiers` + `experienced_color` + `sexual_training_value`; colors as hex values; loaded at `init -3` |
| Girl background random pools | `init/variables.rpy` | `settings/girl_background_pools.json` | 2026-06-08 | `slave_stories` + `homes` + `guardians` + `hobbies` + `colors` + `food` + `drinks` (~69 entries); loaded at `init -3` |
| Audio registry | `init/settings.rpy` | `settings/audio_registry.json` | 2026-06-08 | `playlist` (12 tracks) + `music_shortcuts` (41) + `sound_shortcuts` (102); loaded at `init -10`; `setattr(store, key, value)` keeps the variable interface |
| Contract parameters | `init/variables.rpy` | `settings/contract_params.json` | 2026-06-08 | `contract_level` + `contract_value` + `contract_skill_limit` + `contract_sex_limit` + `contract_stage_modifier` + `contract_specials`; tuples auto-restored; loaded at `init -2`/`init` |
| Building resources | `init/variables.rpy` | `settings/resource_params.json` | 2026-06-08 | `build_resources` + `resource_gold_value` + `resource_sell_discount` + `resource_base_exchange_rate`; `Fraction` arrays restored; loaded at `init -3` |
| Perk archetypes | `init/variables.rpy` | `settings/archetype_data.json` | 2026-06-08 | `archetype_list` + `archetype_description`; `description_i18n` translatable; loaded at `init -4` |
| Game constants | `init/settings.rpy` + `init/variables.rpy` | `settings/game_constants.json` | 2026-06-08 | `weekdays` + `workshift_color` + `MC_class_index` + `roman_numbers` + `playerclass_pics` + `god_pics` + `alignment_pics` + `frequency_tags` + `night_pics` + `fix_pic_balance_*` + `tip_base` + `maximum_tip_modifier` + `starting_gold` + `class_discount` + `nsfw` + `stock_picture_threshold` + `mood_runaway_limit` + `free_girls_per_district`; loaded at `init -10`/`init -4` |
| Job and sex act parameters | `init/variables.rpy` | `settings/job_params.json` | 2026-06-08 | `all_jobs` + `all_sex_acts` + `extended_sex_acts` + `farm_hardcore_acts` + `opposite_sex_acts` + `job_sort_value` + `job_color` + `normal_tags` + `all_farm_tags`; colors as hex values; `null` keys mapped to `None`; loaded at `init -3` |
| XP/rank/class point parameters | `init/variables.rpy` | `settings/xp_rank_params.json` | 2026-06-08 | `xp_to_levelup` (25 levels) + `MC_xp_to_levelup` (26 levels) + `rank_cost` + `rank_stat_step` + `jp_*_modifier`; int keys auto-converted; loaded at `init python` |
| Economy modifier parameters | `init/variables.rpy` | `settings/economy_modifiers.json` | 2026-06-08 | `price_modifiers` + `stat_bonus` + `roll_modifier` + `helper_cost`; loaded at `init -4` |
| Customer and advertising parameters | `init/settings.rpy` | `settings/customer_params.json` | 2026-06-08 | `customer_base_preference` + `advertising_settings` + `reputation_decay` + `tip_*_modifier` + `xp_bonus_dict`; loaded at `init -10` |
| Unlock/cheat/license parameters | `init/settings.rpy` + `init/variables.rpy` | `settings/unlock_params.json` | 2026-06-08 | `sex_act_test` + `chapter_district_unlocks` + `cheat_modifier` + `license_dict`; tuples auto-restored; `license_dict` `name_i18n` translatable; loaded at `init -10`/`init -3` |
| Location tooltips | `init/variables.rpy` | `settings/location_tooltips.json` | 2026-06-08 | `location_tb` + `papa_location`; `papa_location` `name_i18n` translatable; loaded at `init -4` |
| Personality/gift parameters | `init/variables.rpy` | `settings/personality_gift_params.json` | 2026-06-08 | `alignment_bonus` + `personality_attributes` + `attribute_score_dict` + `gpersonalities_likes` + `gpersonalities_comment`; `comments_i18n` translatable; loaded at `init -3` |

## Newly completed in this i18n-adaptation round (2026-06-10)

| Domain | Source file | Target JSON | Completion date | Notes |
|------|--------|-----------|----------|------|
| Item i18n | `core/systems/items.rpy` | `data/items/items.json` | 2026-06-10 | All 193 items gained `name_i18n` + `description_i18n`; `Item` class gained a `name_i18n` attribute; `from_dict()` reads `name_i18n`; UI display switched to `__(it.name_i18n)` |
| Chapter title i18n | `core/systems/events_dispatcher.rpy` | `data/chapters/chapter_titles.json` | 2026-06-10 | 8 chapters: `title`→`title_i18n`, `subtitle`→`subtitle_i18n`; loading code translates with `__()`; hardcoded fallback texts wrapped with `__()` |
| Help text runtime translation | `core/systems/help.rpy` | `settings/help_texts.json` | 2026-06-10 | All return paths of `get_help_text()` wrapped with `__()`; help text supports runtime language switching |
| i18n scanner enhancement | `core/i18n/json_i18n.rpy` | — | 2026-06-10 | `_scan_i18n_strings` supports collecting dictionary values when `parent_key.endswith("_i18n")`; nested dictionary texts such as `help_dict_i18n` can be collected by `generate translations` |

## Completed migrations (Phase 5-7)

| Domain | Source file | Target JSON | Completion date | Notes |
|------|--------|-----------|----------|------|
| Traits | `data/traits.rpy` | `data/traits/traits.json` | Phase 5 | 130+ definitions |
| Perks | `data/perks.rpy` | `data/perks/perks.json` | Phase 5 | 50+ definitions + 5 special |
| Achievements | `systems/achievements.rpy` | `data/achievements/achievements.json` | Phase 7 | 231 achievements |
| Challenges | `framework/functions.rpy` | `data/challenges/challenges.json` | Phase 7 | MC challenges |
| Resources | `framework/functions.rpy` | `data/resources/resources.json` | Phase 7 | Building resources |
| Contracts | `framework/functions.rpy` | `data/contracts/contracts.json` | Phase 7 | 8 contract templates |
| Goals | `framework/goal.rpy` | `data/goals/chapter_goals.json` | Phase 7 | Chapter goals |
| Chapter Titles | `init/start.rpy` | `data/chapters/chapter_titles.json` | Phase 7 | Chapter titles |
| Stats | `init/variables.rpy` | `data/stats/stats.json` | Phase 7 | 12 stat definitions |
| Personalities | `init/variables.rpy` | `data/personalities/personalities.json` | Phase 7 | Personality archetypes |
| Ranks | `init/variables.rpy` | `data/ranks/ranks.json` | Phase 7 | Rank names |
| Scenarios | `systems/gamemodes/` | `data/scenarios/scenarios.json` | Phase 7 | Scenario definitions |
| Origins | `systems/gamemodes/` | `data/sandbox/origins.json` | Phase 7 | Origin definitions |
| Difficulty | `init/settings.rpy` | `data/difficulty/difficulty.json` | Phase 7 | Difficulty parameters |
| Customer Affixes | `systems/customer/` | `data/customers/customer_affixes.json` | Phase 7 | Customer affixes |
| Cleanliness Penalties | `init/start.rpy` | `data/settings/cleanliness_penalties.json` | Phase 7 | Cleanliness penalties |
| Treasure Thresholds | `init/start.rpy` | `data/settings/treasure_thresholds.json` | Phase 7 | Treasure thresholds |
| Meta Progression | `systems/registry/` | `data/meta/meta_progression.json` | Phase 7 | Meta upgrades |
| NGP Settings | `systems/registry/` | `data/ngp/ngp_settings.json` | Phase 7 | NG+ settings |

---

## Technical debt and known issues

| Issue | Impact | Status |
|------|------|------|
| Ren'Py `dict` → `RevertableDict` replacement | `isinstance(x, dict)` fails on JSON data | ✅ Fixed (uses `__import__('builtins').dict`) |
| `functions.rpy` split missed functions | `generate_name` etc. missing | ✅ Fixed |
| `stats.json` key case mismatch | `gstats_dict` KeyError | ✅ Fixed |
| `with open` file handle leak | Pickle fails when saving | ✅ Fixed (all 7 sites got `del _f`) |
| `settings.rpy` indentation error | Startup error | ✅ Fixed |
| `crazy_customer()` double `%` formatting | Runtime TypeError | ✅ Fixed (removed the extra `%`) |
| `unlock_trainer()` using translated name as key | Achievement system crashes in non-English locales | ⚠️ Temporary fix (extracts English name from `portrait`); needs system-level `key`/`id` attribute decoupling |

---

## Migration checklist (generic for every domain)

- [ ] 1. Analyze the data structures in the source `.rpy`
- [ ] 2. Design the JSON Schema (`data/_schemas/xxx.schema.json`)
- [ ] 3. Write the `DataLoader.load_xxx()` method
- [ ] 4. Implement `from_dict()` / `to_dict()` on the target class
- [ ] 5. Create the JSON data file
- [ ] 6. Add a `_fallback_xxx` fallback in `start.rpy`
- [ ] 7. Modify the original `.rpy` code to prefer loading JSON
- [ ] 8. Run `tools/clean_runtime.ps1`
- [ ] 9. Run `--lint` verification
- [ ] 10. Verify by actually playing (at least one full interaction loop)
- [ ] 11. Update the status in this document

---

## Remaining hardcoded data inventory (Phase 7.5 comprehensive audit)

> The groups below are ordered by priority and impact, listing only hardcoded data structures not yet migrated to JSON.
> Already-migrated items (items, jobs, brothel_params, shops, tax_params, minions, installations, rooms, powers, spells, mc_classes, traits, perks, achievements, challenges, resources, contracts, goals, chapter_titles, stats, personalities, ranks, scenarios, origins, difficulty, customer_affixes, cleanliness_penalties, treasure_thresholds, meta_progression, ngp_settings) are not listed again.

### 🔴 High priority (large datasets, migrate first)

| # | File | Variable name | Type | Entries | Description |
|---|------|--------|------|--------|------|
| 1 | `variables.rpy` | `fix_description` + `fix_dict` | dict | ~200 | All Fixation definitions and description text ✅ migrated to `fixations.json` |
| 2 | `variables.rpy` | `interact_dict` + `free_interact_dict` | dict | ~110 | Slave/free-girl interaction menu tree ✅ migrated to `interactions/*.json` |
| 3 | `variables.rpy` | `farm_perform_dict` | dict | 100+ | Farm performance text and mechanics (locations, intros, stories, reactions, cum texts) ✅ migrated to `farm/farm_perform_dict.json` |
| 4 | `variables.rpy` | `generic_gossip` + `chapter_gossip` + `district_gossip` | list/dict | ~150 | City gossip text library (generic + chapter + district) ✅ migrated to `settings/gossip.json` |
| 5 | `variables.rpy` | `recent_event_templates` | dict | 28 | Recent event templates (28 event types) ✅ migrated to `settings/recent_events.json` |
| 6 | `variables.rpy` | `contract_tasks` + `contract_description` + related | list/dict | ~60 | Contract task system (40 ContractTasks + descriptions + parameters) ✅ migrated to `settings/contracts.json` |
| 7 | `settings.rpy` | `_tag_dict_data` | dict | ~180 | Tag dictionary: filename substring → in-game tag mapping ✅ migrated to `settings/tags.json` |
| 8 | `settings.rpy` | `security_pics` + `advertising_pics` + `treasure_pics` + `pony_pics` + `arson_pics` + `violent_pics` + `no_girls_pics` | dict/list | ~50 | Security/advertising/treasure/pony/arson/violent/no-girls picture mappings ✅ migrated to `settings/picture_mappings.json` |
| 9 | `variables.rpy` | `mood_description` + `love_description` + `fear_description` | dict | 54 | Mood/love/fear level description text ✅ migrated to `settings/girl_descriptions.json` |
| 10 | `variables.rpy` | `merchant_greetings` + `merchant_title` + `merchant_dict` | dict | 51 | Merchant dialogue data (greetings + titles + type mappings) ✅ migrated to `settings/merchants.json` |

### 🟡 Medium priority (medium datasets, high standalone migration value)

| # | File | Variable name | Type | Entries | Description |
|---|------|--------|------|--------|------|
| 11 | `variables.rpy` | `brothel_ranking_reputations` | dict | 40 | Brothel reputation rank names (40 ranking titles) ✅ migrated to `settings/rankings.json` |
| 12 | `variables.rpy` | `quality_prefix` + `quality_modifier` | dict | 57 | Item quality prefixes + price multiplier system ✅ migrated to `settings/quality.json` |
| 13 | `variables.rpy` | `encounters` + `encounter_pics` + `pop_name_dict` | tuple/dict | ~60 | City encounter types + pictures + population random names ✅ migrated to `settings/encounters.json` |
| 14 | `variables.rpy` | `jokes` + `compliments` | dict | ~20 | Social interaction text library (jokes + compliments) ✅ migrated to `settings/dialogue_texts.json` |
| 15 | `variables.rpy` | `help_dict` + `help_pic_dict` + `help_center_pic_dict` | dict | 120+ | Brokipedia help text system (100+ entries) ✅ migrated to `settings/help_texts.json` |
| 16 | `settings.rpy` | `playlist` + `m_*` music shortcuts + `s_*` sound shortcuts | list/string | ~155 | Audio asset registry (BGM + SFX) ✅ migrated to `settings/audio_registry.json` |
| 17 | `variables.rpy`/`settings.rpy` | `customer_base_preference` + `advertising_settings` + `reputation_decay` + `tip_*_modifier` + `xp_bonus_dict` | dict | ~60 | Customer preference/advertising/reputation decay/tips/XP multipliers ✅ migrated to `settings/customer_params.json` |
| 18 | `variables.rpy` | `security_events` + `alert_limits1` + `alert_limits2` | dict | 17 | Security event types + alert thresholds ✅ migrated to `settings/security_events.json` |
| 19 | `start.rpy` | `blist` + `district_dict` + `location_dict` + location instantiation + population instantiation | dict/object | ~90 | World map: brothel definitions + districts + locations + populations ✅ migrated to `worlds/default_world.json` (including UI layout + scenario mode interface) |
| 20 | `variables.rpy` | `xp_to_levelup` + `MC_xp_to_levelup` + `rank_cost` + `rank_stat_step` + `jp_*_modifier` | dict | ~70 | XP/rank/promotion/job point system ✅ migrated to `settings/xp_rank_params.json` |
| 21 | `variables.rpy` | `base_reluctance` + `preference_modifier` + `preference_limit` + `experienced_*` + `sexual_training_value` | dict | ~40 | Sex training/experience/preference system ✅ migrated to `settings/sex_training_params.json` |
| 22 | `variables.rpy` | `slave_stories` + `homes` + `guardians` + `hobbies` + `colors` + `food` + `drinks` | list | ~63 | Girl background generation random pools ✅ migrated to `settings/girl_background_pools.json` |
| 23 | `variables.rpy` | `training_test_dict` + `magic_training_test_dict` + `long_act_description` | dict | ~28 | Training prerequisites + long sex act descriptions. `long_act_description` + `pref_response` + `experienced_description` ✅ migrated to `settings/sex_descriptions.json` |
| 24 | `variables.rpy` | `sorter_dict` + `inventory_filters` + `filter_list` | dict | ~33 | UI sorting/filtering/inventory system ✅ migrated to `settings/inventory_sorters.json` |
| 25 | `variables.rpy` | `special_quest_description` + `quest_base_gold` + `class_prices` + `class_prefixes` | dict | ~21 | Quest/class prices and descriptions. `class_prefixes` + `special_quest_description` ✅ migrated to `settings/small_texts.json` |
| 26 | `settings.rpy` | `sex_act_test` + `chapter_district_unlocks` + `cheat_modifier` | dict | 13 | Sex act unlock thresholds + chapter district unlocks + cheat multipliers ✅ migrated to `settings/unlock_params.json` |
| 27 | `variables.rpy` | `alignment_bonus` + `personality_attributes` + `attribute_score_dict` + `gpersonalities_likes` + `gpersonalities_comment` + `gift_description` | dict/list | ~50 | Personality/attribute/gift system. `gift_description` ✅ migrated to `settings/misc_texts.json`, the rest ✅ migrated to `settings/personality_gift_params.json` |
| 28 | `variables.rpy` | `event_sounds` + `roll_dict` + `result_dict` + `result_colors` + `result_star_dict` + `result_reference` | dict | ~25 | Result resolution/dice/sound system. `roll_dict` + `result_dict` + `result_reference` ✅ migrated to `settings/roll_results.json`, `event_sounds` ✅ migrated to `settings/threat_params.json` |
| 29 | `variables.rpy` | `stat_increase_dict` + `maintenance_desc` + `log_event_dict` + `attraction_dict` + `gold_threat_*` | dict | ~30 | Maintenance/cleanliness/attraction/threat system. `stat_increase_dict` ✅ migrated to `settings/stat_increase_dict.json`, `maintenance_desc` ✅ migrated to `settings/maintenance_desc.json`, `log_event_dict` + `attraction_dict` ✅ migrated to `settings/event_texts.json`, `gold_threat_amount` + `gold_threat_max` ✅ migrated to `settings/threat_params.json` |
| 30 | `variables.rpy` | `price_modifiers` + `stat_bonus` + `roll_modifier` + `helper_cost` | dict | ~16 | Price/bonus/dice/helper cost ✅ migrated to `settings/economy_modifiers.json` |
| 31 | `variables.rpy` | `MC_inventory_slots` + `girl_inventory_slots` + `all_MC_stats` + `MC_stat_description` + `MC_playerclass_description` + `god_description` + `alignment_description` | list/dict | ~20 | MC/girl inventory slots + stat/class/god/alignment descriptions. `MC_stat_description` + `MC_playerclass_description` + `god_description` + `alignment_description` ✅ migrated to `settings/mc_descriptions.json` |
| 32 | `variables.rpy` | `license_dict` + `location_tb` + `papa_location` | dict | ~24 | Licenses/location tooltips/district aliases ✅ migrated to `settings/unlock_params.json` + `settings/location_tooltips.json` |
| 33 | `variables.rpy` | `archetype_list` + `archetype_description` | list/dict | 16 | Perk archetype names and descriptions ✅ migrated to `settings/archetype_data.json` |
| 34 | `variables.rpy` | `contract_level` + `contract_value` + `contract_skill_limit` + `contract_sex_limit` + `contract_stage_modifier` + `contract_specials` + `contract_task_types_order` + `contract_task_types_description` | dict/list | ~40 | Contract system parameters. `contract_task_types_order` + `contract_task_types_description` ✅ migrated with `contracts.json`, the rest ✅ migrated to `settings/contract_params.json` |
| 35 | `variables.rpy` | `goal_channels` + `goal_channels_no_story` + `goal_categories` + `goal_tb` + `goal_colors` | tuple/dict | ~32 | Goal system UI constants ✅ migrated to `goal_ui.json` |
| 36 | `settings.rpy` | `frequency_tags` | dict | 4 | Tag frequency weight modifiers ✅ migrated to `settings/game_constants.json` |
| 37 | `variables.rpy` | `weekdays` + `workshift_dict` + `workshift_color` + `MC_class_index` + `roman_numbers` | tuple/dict | ~23 | Calendar/workshifts/class index/Roman numerals. `workshift_dict` ✅ migrated to `settings/small_texts.json`, the rest ✅ migrated to `settings/game_constants.json` |
| 38 | `variables.rpy` | `all_jobs` + `all_sex_acts` + `extended_sex_acts` + `farm_hardcore_acts` + `opposite_sex_acts` + `job_sort_value` + `job_color` | list/dict | ~35 | Job/sex act IDs and sorting/colors ✅ migrated to `settings/job_params.json` |
| 39 | `variables.rpy` | `normal_tags` + `all_farm_tags` | tuple | 12 | Picture tag classifications |
| 40 | `variables.rpy` | `customer_rank_dict` + `attract_pop_dict` | dict | 11 | Customer ranks/population attractiveness. `attract_pop_dict` ✅ migrated to `settings/small_texts.json` |
| 41 | `settings.rpy` | `playerclass_pics` + `god_pics` + `alignment_pics` | dict | 9 | Class/god/alignment icon paths ✅ migrated to `settings/game_constants.json` |
| 42 | `variables.rpy` | `build_resources` + `resource_gold_value` + `resource_sell_discount` + `resource_base_exchange_rate` | list/dict | ~20 | Building resource prices and exchange rates ✅ migrated to `settings/resource_params.json` |
| 43 | `settings.rpy` | `night_pics` | list | 1 | Night background picture ✅ migrated to `settings/game_constants.json` |
| 44 | `settings.rpy` | `fix_pic_balance_variety` + `fix_pic_balance_accuracy` | dict | 4 | Picture balance mode weights ✅ migrated to `settings/game_constants.json` |
| 45 | `settings.rpy` | `tip_base` + `maximum_tip_modifier` + `sell_girl_preference_boost` + `starting_gold` + `class_discount` + `nsfw` + `stock_picture_threshold` + `mood_runaway_limit` + `free_girls_per_district` | constant | ~9 | Standalone numeric constants (except `sell_girl_preference_boost`) ✅ migrated to `settings/game_constants.json` |

### 🟢 Low priority (small datasets or inline mappings)

| # | File | Variable name | Type | Entries | Description |
|---|------|--------|------|--------|------|
| 46 | `framework/economy.rpy` | `s_des` | dict | 5 | Short sex act descriptions ✅ migrated to `settings/sex_act_descriptions.json` |
| 47 | `framework/economy.rpy` | `rank_lookup_dict` + `order` + `check_order` | dict/list | 11 | Customer matching priority ✅ `rank_lookup_dict` migrated to `settings/rank_lookup.json` (`order`/`check_order` are dynamic variables, kept in place) |
| 48 | `framework/world.rpy` | `pronoun` | dict | 2 | Gender pronouns ✅ migrated to `settings/pronoun.json` |
| 49 | `framework/world.rpy` | `rank_factor` | dict | 5 | District rank → cleaning fee coefficient ✅ migrated to `settings/rank_factor.json` |
| 50 | `framework/progression.rpy` | `first`/`second`/`third`/`names`/`fourth` | tuple | ~160 | Brothel name generation word pools ✅ migrated to `settings/brothel_name_pools.json` |
| 51 | `framework/character.rpy` | `weight_dict` + `weight` + `pref_dict` | dict | ~25 | Preference weights and ranges |
| 52 | `framework/core_entities.rpy` | `god_dict` + `name_map` + `all_qualities` | dict/list | 9 | Gods/name mappings/quality tiers ✅ migrated to `settings/entity_lookups.json` |
| 53 | `framework/challenges.rpy` | inline opposed-chance table | list | 11 | Opposed dice difference table ✅ migrated to `settings/opposed_chance_table.json` |
| 54 | `framework/progression.rpy` | `_rank_dict` + `pace` | dict | 12 | Rank → number mapping + XP pace |
| 55 | `framework/girlclass.rpy` | `_wd_dict` (×2) + `base_value` + `step` (×2) | dict | ~30 | Weekday mappings + preference base values + mood step sizes |
| 56 | `systems/game_systems.rpy` | inline challenge pics + `_batch` (×4) | dict/list | 10 | Challenge pictures + unlock batch NPC lists |
| 57 | `systems/customer/customer_affixes.rpy` | `CUSTOMER_COLOR_TIERS` | dict | 8 | Customer color tiers (JSON fallback already exists) |
| 58 | `systems/security.rpy` | `siege_enemy_scaling` | dict | 4 | Siege enemy scaling config ✅ migrated to `settings/security_scaling.json` |
| 59 | `systems/postings.rpy` | `quest_templates` + `class_templates` | list | 26 | Quest templates + class templates ✅ migrated to `settings/quest_templates.json` |
| 60 | `systems/items.rpy` | `item_type_by_name` + `all_equipement_types` + `furniture_types` + `extractor_items` + `all_furniture` | dict/list | ~40 | Item type mappings + equipment slots + furniture |
| 61 | `systems/minigame.rpy` | `house_templates` + inline ninja effects | list/dict | 11 | Ninja minigame house templates |
| 62 | `systems/endday.rpy` | `latest_ent_match` + `latest_wh_match` | dict | 8 | Entertainment/whoring match result structures |
| 63 | `systems/events_dispatcher.rpy` | `_bbcr` + `_neg_stats` + inline prep maps | list/dict | ~10 | Inline constants in the event dispatcher |
| 64 | `systems/farm.rpy` | `imgfiles` + `available_acts` | list | dynamic | Farm picture scanning + available acts |
| 65 | `systems/courtyard/courtyard.rpy` | `upgrade_cost` (×3) | dict | 6 | Courtyard upgrade costs |
| 66 | `systems/powers.rpy` | `evpower_color` + `evil_card_size` | dict/int | 3 | Power rarity colors + card size ✅ migrated to `settings/power_ui.json` |
| 67 | `systems/achievements.rpy` | `tracked_achievements` | list | 36 | Tracked achievement targets ✅ migrated to `settings/tracked_achievements.json` |
| 68 | `systems/traits.rpy` | `gold_traits` + `pos_traits` + `neg_traits` | list | 127 | Hardcoded trait definitions (traits.json migrated; this is the fallback) |
| 69 | `content/declarations.rpy` | `y_ratio` + `UI_elements_colors` + `ev_gallery_list` | dict/list | 14 | Picture ratios + UI theme + gallery categories ✅ `UI_elements_colors` + `ev_gallery_list` migrated to `settings/ui_element_colors.json` / `settings/ev_gallery_list.json` |
| 70 | `content/interactions.rpy` | inline cumshot tags + `diff` | dict | ~20 | Sex act cumshot tags + training difficulty |
| 71 | `content/interactions_free.rpy` | `limit` | dict | 6 | Free-girl interaction count limits |
| 72 | `content/story_events/story_events.rpy` | `loandict` + `loans` | dict/list | 14 | Loan tiers and loan objects ✅ migrated to `settings/loans.json` |
| 73 | `data/settings.rpy` | `diff_name` + `diff_description` + `diff_settings` + `diff_setting_name` + `diff_setting_description` + `stat_name_dict` | dict/list | ~50 | Difficulty UI text + stat names (difficulty.json migrated; this is the UI layer) |
| 74 | `data/perks.rpy` | `archetype_dict` + `perk_description` + `perk_dict` | dict | 103 | Hardcoded perks (perks.json migrated; this is the fallback) |
| 75 | `data/items.rpy` | `_fallback_template_items` + `_fallback_all_items` | list | 131 | Hardcoded item fallback |
| 76 | `data/jobs.rpy` | `_fallback_perform_job_dict` | dict | ~100 | Job performance fallback |
| 77 | `start.rpy` | `extras_dict` | dict | 6 | Unlockable extra feature flags ✅ migrated to `settings/extras_dict.json` |
| 78 | `start.rpy` | `town_locations` + `beach_locations` + `nature_locations` + `court_locations` + `all_locations` | list | ~23 | Location category lists |
| 79 | `start.rpy` | `endless_district` + `all_districts` | object/list | 7 | Endless-mode district + district list |

### Suggested migration roadmap

**Short term (1-2 sessions):**
- ✅ Fixation system — migrated to `fixations.json`
- ✅ Interaction menus — migrated to `interactions/*.json`
- ✅ Farm performance text — migrated to `farm/farm_perform_dict.json`
- ✅ City gossip — migrated to `settings/gossip.json`
- ✅ Tag dictionary — migrated to `settings/tags.json`
- ✅ Picture mappings — migrated to `settings/picture_mappings.json`
- ✅ Help system — migrated to `settings/help_texts.json`
- ✅ Audio asset registry — migrated to `settings/audio_registry.json`
- ✅ Inventory sorting/filtering — migrated to `settings/inventory_sorters.json`
- World map (`blist` + `district_dict` + `location_dict` + instantiation) — 90+ entries, complex (needs `from_dict()`)

**Medium term (3-5 sessions):**
- ✅ Contract task system — migrated to `settings/contracts.json`
- ✅ XP/rank/promotion system — migrated to `settings/xp_rank_params.json`
- ✅ Quality system — migrated to `settings/quality.json`
- ✅ Training/preference system — migrated to `settings/sex_training_params.json`
- ✅ Background generation pools — migrated to `settings/girl_background_pools.json`
- ✅ Result resolution system — migrated to `settings/roll_results.json` / `settings/threat_params.json`
- Contract system parameters (`contract_level` + `contract_value` + `contract_specials`, etc.)
- Building resources (`build_resources` + `resource_gold_value` + `resource_base_exchange_rate`)

**Long term (optional / higher complexity):**
- Full world map object system (`Population`/`Location`/`District`/`Brothel` `from_dict()`)
- Brothel name generation word pools (`progression.rpy` pools, ~160 entries)
- Item type system (`systems/items.rpy` mappings)
- Achievement tracking (`systems/achievements.rpy` `tracked_achievements`)
- Courtyard/minigame inline data

---

## Appendix: removed hardcoded data

The following data has been completely removed from `.rpy` (only JSON + fallback retained):

| Domain | Original hardcoded location | Removal method |
|------|-------------|----------|
| Items | `data/items.rpy` | Fully removed, only `_fallback_*` retained |
| Jobs | `data/jobs.rpy` | Fully removed, only `_fallback_*` retained |
| Brothel params | `init/settings.rpy` | Fully removed, only `_fallback_*` retained |
| Shops | `init/settings.rpy` + `core_entities.rpy` + `economy.rpy` | Dynamically loaded, no fallback |
| Tax | `init/settings.rpy` | Fully removed, only `_fallback_*` retained |
| Minions | `init/variables.rpy` | Fully removed, only `_fallback_*` retained |
| Farm installations | `init/variables.rpy` | Fully removed, only `_fallback_*` retained |
| Rooms | `init/variables.rpy` | Fully removed, only `_fallback_*` retained |
| Powers | `data/powers.rpy` | Fully removed, only `_fallback_*` retained |
| Spells | `data/spells.rpy` | Fully removed, only `_fallback_*` + `moons` fallback retained |
| MC Classes | `data/spells.rpy` | `spellbook` migrated to `mc_classes.json`; original hardcoded data turned into fallback |

---

## Related documents

- [`../modding/CUSTOM_DIRECTORIES.md`](../modding/CUSTOM_DIRECTORIES.md) — full subdirectory inventory of `core/data/` and editor correspondence
- [`../tools/TOOLS.md`](../tools/TOOLS.md) — inventory of migration history scripts (`export_*`, `migrate_variables`, `split_*`)
- [`../i18n/I18N_ROADMAP.md`](../i18n/I18N_ROADMAP.md) — JSON `_i18n` migration and translation status
- [`../i18n/BEST_PRACTICES.md`](../i18n/BEST_PRACTICES.md) — translatable field conventions for new JSON data
- [`../../game/core/systems/data_loader.rpy`](../../game/core/systems/data_loader.rpy) — DataLoader implementation
- [`../../tools/bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md) — checklist for adding new JSON data sources
