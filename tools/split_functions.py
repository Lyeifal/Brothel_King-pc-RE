"""Split game/core/framework/functions.rpy into focused modules.

Groups:
  - utils.rpy        : display, math, string, list, file helpers
  - girl_factory.rpy : girl generation, packs, init files
  - game_systems.rpy : turns, events, quests, UI
  - economy.rpy      : money, customers, items, tax, matchmaking
  - effects.rpy      : effect system, picture system
  - dialogue.rpy     : descriptions, dialogue, preferences, minions
"""

import re
from pathlib import Path

SRC = Path("game/core/framework/functions.rpy")
OUT_DIR = Path("game/core/framework")

with open(SRC, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract header + python early block + init block start
# Header is lines 0-5 (comments)
# python early is lines 6-25
# init -3 starts at line 26 (0-indexed)
header_lines = lines[:6]  # includes "#### FUNCTIONS..." comments
early_lines = lines[6:26]  # python early block
init_start_line = 26
init_header = lines[init_start_line]  # "init -3 python:\n"

# Find all top-level definitions in init block
def find_definitions(block_lines, global_offset):
    defs = []
    for i, line in enumerate(block_lines):
        m = re.match(r"^(    )(def |class )(\w+)", line)
        if m:
            defs.append((i + global_offset, m.group(3), m.group(2).strip(), len(m.group(1))))
    return defs

init_defs = find_definitions(lines[init_start_line+1:], init_start_line+1)

# Build ranges for each definition
ranges = []
for i, (start, name, kind, indent) in enumerate(init_defs):
    if i + 1 < len(init_defs):
        end = init_defs[i+1][0]
    else:
        end = len(lines)
    ranges.append((name, start, end, kind))

print(f"Found {len(ranges)} definitions in init block")

# Group assignments
groups = {
    "utils": [
        "xres", "yres", "res_font", "res_tb", "fast_portrait", "predict_next_img",
        "dice", "rand_choice", "weighted_choice", "round_int", "str_int", "str_dec",
        "round_down", "round_up", "round_best", "mean", "mean_int", "clamp",
        "get_change_min_max", "is_string", "make_list", "reverse_if",
        "plus_text", "gold_text", "and_text", "list_text", "plural", "article",
        "season_text", "capitalize", "uncapitalize",
        "cycle_list", "move_up_list", "move_down_list",
        "is_imgfile", "is_videofile", "list_imgfiles", "get_current_folder",
        "count_lines", "girl_object_count", "girl_gc", "debug_sorting_girls",
        "is_renpy_8_1", "norollback", "are_different",
    ],
    "girl_factory": [
        "get_girl_path", "get_selected_girlpacks", "change_template",
        "generate_girls", "create_girl", "get_name", "get_girl", "get_girls",
        "read_init_file_generate_as", "read_init_file_field", "read_init_file",
        "register_custom_tags_for_pack", "register_custom_dialogue_for_pack",
        "clone_init_dict", "can_generate", "can_spawn",
        "get_girlpack_rating", "get_plus_rating", "randomize_girl_level",
    ],
    "game_systems": [
        "update_slaves", "update_free_girls", "refresh_available_locations",
        "reset_girl_jobs", "cycle_free_girls", "update_market", "update_shops",
        "weekly_updates", "update_mods", "register_mod", "reset_updated_games",
        "load_quest_pics", "update_quests", "refresh_quest_girls",
        "add_event", "story_add_event", "story_remove_event", "clear_event",
        "story_set_condition", "get_events", "toggle_skip",
        "get_vp_bounds", "focus_vp", "select_previous_girl", "get_previous",
        "get_next", "select_next_girl", "can_interact", "get_act_menu",
        "get_fix_menu", "get_fix_list", "multiple_choice_menu", "long_menu",
        "shake_mouse",
        "commit_start_settings", "unlocking_extras", "update_available_mixes",
        "get_day_report", "get_next_day_report", "get_warnings",
        "get_resting_girls", "get_known_free_girls", "compile_girl_log",
        "set_girls_workdays", "change_district", "get_starting_furniture",
        "build_all_furniture", "create_enemy_brothels", "list_stat_changes",
        "MU_jobgirl_event_test", "farm_can_perform_act",
    ],
    "economy": [
        "can_pay", "transact", "get_exchange_rate", "search_items",
        "cust_diff_description", "get_entertainment_bonus", "perform",
        "get_customer_population_count", "reset_alerts",
        "generate_customers", "count_customers", "get_available_populations",
        "job_matchmaking", "wh_matchmaking",
        "make_match_list_from_ent_dict", "make_match_list_from_wh_list",
        "init_tax", "calculate_tax", "pay_tax",
        "init_items", "list_district_items", "get_rand_item",
        "update_NPC_items",
    ],
    "effects": [
        "get_effect", "add_effects", "remove_effects",
        "get_scale_factor", "update_effects",
        "get_pic_list", "get_pic",
    ],
    "dialogue": [
        "say_name", "get_description", "get_log_changes",
        "describe_leveled_stats", "get_change_text", "help", "get_gossip",
        "relinquish_girl", "have_fight",
        "compare_preference", "get_preference_limit",
        "get_act_weakness_symbol", "get_fix_weakness_symbol",
        "this_is_a_hentai_game_so_why_are_you_trying_to_act_classy_all_of_a_sudden",
        "get_rand_minion", "can_use_minion_item",
        "return_ddict_list", "add_mix", "add_all_to_mix", "remove_all_from_mix",
        "delete_mix", "prepare_not_tags",
        "parse_dice_formula", "factor", "term", "plus_minus",
        "is_censored", "load_girl_status", "update_girl_status",
        "change_autorest", "reset_autorest",
        "get_opposite_attribute", "print_ignore_list", "toggle_ignore_pic",
        "_event_mode_allowed",
    ],
}

# Build output files
for group_name, func_names in groups.items():
    out_path = OUT_DIR / f"{group_name}.rpy"
    content = f"#### {group_name.replace('_', ' ').title()} functions ####\n\n"
    content += init_header
    
    for name in func_names:
        for fname, fstart, fend, fkind in ranges:
            if fname == name:
                func_lines = lines[fstart:fend]
                content += "".join(func_lines)
                break
        else:
            print(f"WARNING: Function {name} not found!")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written {out_path} ({len(content.splitlines())} lines)")

print("\nDone. Remember to delete the old functions.rpy after testing!")
