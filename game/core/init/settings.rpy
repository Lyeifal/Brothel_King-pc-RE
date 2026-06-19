####         SETTINGS           ####################################################
##    Those are the settings      ##################################################
##    that can be easily edited   ##################################################
##    by players in Bro King      ##################################################


init -10 python:

#### GIRLS FOLDER/GIRL PACKS ####

    girl_directories = ["custom/girls/", ] # You can specify one or more directories containing girl packs. The 'game' folder is the root folder

#### CONFIG & PERFORMANCE ####

    ## Picture caching. Set lower values if you have memory problems. Use only one setting, comment the other out with the # symbol.

    config.image_cache_size = 144 # Set this higher for better performance (will use more RAM)
#     config.image_cache_size_mb = 500 # You may use this instead of config.image_cache_size. Set this higher for better performance (will use more RAM)

    refresh_memory_on_home_screen = False # Change to True if you want more frequent memory refresh. May help on lower-end computers

    ## Auto-save.

    config.has_autosave = True # Auto-save is enabled by default. The game will save every night before pressing end-day.
    config.autosave_frequency = 200 # The game will also auto-save after n messages have been shown (during long events)
    save_every_x_days = 2 # The frequency with which an end-day save is done (1=every day, 2=every 2 days, and so on)
    config.autosave_slots = 12
    config.autosave_on_choice = False
    config.autosave_on_quit = False

    config.developer = True

    # Maximum number of items shown (change this if you are having performance issues with large inventories)
    max_item_shown = 30

#### TRANSLATION OPTIONS ####

    ## Edit this dictionary to change the stat names that are displayed (change the right-hand text)

    # <MIGRATED: see data/settings.rpy>

#### BALANCE / CHEATS ####

    debug = False # Replace this with 'True' for additional cheats and information (recommended for testing)

    # EN: Load unlock parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载解锁参数（BK Evolution）。
    _unlock_json = DataLoader.load_unlock_params()
    if _unlock_json:
        cheat_modifier = _unlock_json.get("cheat_modifier", {})
        _sat = _unlock_json.get("sex_act_test", {})
        sex_act_test = {k: [tuple(x) for x in v] for k, v in _sat.items()}
        chapter_district_unlocks = {int(k): v for k, v in _unlock_json.get("chapter_district_unlocks", {}).items()}
    else:
        cheat_modifier = {}
        sex_act_test = {}
        chapter_district_unlocks = {}

    ## STARTING TRAITS

    prefer_original_girls = False # Set this to True to always generate original (gold-trait) girls first. Default is False.

    use_ini_skills = True # If set to True, this will use values specified in _BK.ini files to generate skill values.
    use_ini_traits = True # If set to True, this will use values specified in _BK.ini files to generate trait values.
    use_ini_personality = True # If set to True, this will use values specified in _BK.ini files to generate personality values.
    use_ini_sex = True # If set to True, this will use values specified in _BK.ini files to generate sexual preferences values.

    starting_traits_gold = 0 # Original girls will receive this plus 1 gold trait(s)
    starting_traits_positive = 2 # Number of positive traits, except gold traits
    starting_traits_negative = 1

    ## SEX ACTS

    whore_test = 50 ## Minimum value of Obedience + Libido to become a whore

    bis_chance = 0.5 # This is the base chance for Bisexual to trigger, if active
    group_chance = 0.5 # This is the base chance for Group to trigger, if active

    ## BROTHEL SETTINGS
    # For each chapter: the first number between brackets is the minimum number of bedrooms (and therefore girls), the second number is max.
    bro_capacity = {1 : [1, 4], 2 : [4, 8], 3: [8, 12], 4 : [12, 16], 5 : [16, 20], 6 : [20, 24], 7 : [24, 32]}

    # For each chapter: the maximum number of helpers (for advertising, security, and maintenance)
    bro_helpers = {1 : 8, 2 : 16, 3 : 24, 4 : 32, 5 : 40, 6 : 48, 7 : 64}

    # Reputation cap affects the maximum number of customers that can come before advertising and special effects. Each customer costs 10 pts of reputation * rank
    bro_reputation_cap = {1 : 80, 2 : 320, 3 : 480, 4 : 1200, 5 : 1560, 6 : 3040, 7 : 5800}

    ## EN: Maximum chapter number (used for validation and loop bounds).
    ## ZH: 最大章节数（用于验证和循环边界）。
    MAX_CHAPTER = 7

    ## CHAPTER GOALS

    # Goal types can be: __('gold'), 'ranked', 'reputation', 'prestige'

    bro_cost = {1 : 0, 2 : 1000, 3: 5000, 4 : 7500, 5 : 15000, 6 : 25000, 7 : 100000}

    ## EN: Fallback hardcoded chapter goals (used if JSON file is missing or invalid).
    ## ZH: 硬编码回退章节目标（JSON 文件缺失或无效时使用）。
    _chapter_goals_fallback = {
                    1 : [Goal("gold", bro_cost[2])],
                    2 : [Goal("gold", bro_cost[3])],
                    3 : [Goal("ranked", 2, 6), Goal("gold", bro_cost[4])],
                    4 : [Goal("ranked", 3, 8), Goal("gold", bro_cost[5])],
                    5 : [Goal("ranked", 3, 12), Goal("gold", bro_cost[6])],
                    6 : [Goal("ranked", 4, 12), Goal("gold", bro_cost[7])],
                    7 : [Goal(None, channel="other")],
                    }

    ## EN: Try loading chapter goals from JSON (BK Evolution data-driven goals).
    ## ZH: 尝试从 JSON 加载章节目标（BK Evolution 数据驱动目标）。
    chapter_goals = _chapter_goals_fallback
    try:
        import json, os
        _goals_json_path = os.path.join(config.gamedir, "core", "data", "goals", "chapter_goals.json")
        if os.path.exists(_goals_json_path):
            with open(_goals_json_path, "r", encoding="utf-8") as _f:
                _goals_data = json.load(_f)
            del _f
            chapter_goals = {}
            for _ch_str, _goal_list in _goals_data.items():
                chapter_goals[int(_ch_str)] = [Goal.from_dict(g) for g in _goal_list]
    except Exception:
        pass

    ## CUSTOMER CAPACITY

    # The formula for calculating customer capacity is: base_customer + (main_stat + constitution) // customer_points
    # Main stat is: Beauty, Body, Charm or Refinement for jobs, Libido for whores
    # This values are halved if the girl works half-time
    # You can edit those values here.

    job_base_customer = 2
    job_customer_points = 50

    whore_base_customer = 1
    whore_customer_points = 100


    ## CUSTOMER PREFERENCES

    customer_cap_multiplier = 3 # Multiplies customer difficulty to calculate customer max money (base modifier, advertising improves it)

    # EN: Load customer and advertising parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载顾客与广告参数（BK Evolution）。
    _cust_json = DataLoader.load_customer_params()
    if _cust_json:
        customer_base_preference = _cust_json.get("customer_base_preference", {})
        advertising_settings = {int(k): v for k, v in _cust_json.get("advertising_settings", {}).items()}
        reputation_decay = {int(k): v for k, v in _cust_json.get("reputation_decay", {}).items()}
        tip_result_modifier = _cust_json.get("tip_result_modifier", {})
        tip_advertising_modifier = _cust_json.get("tip_advertising_modifier", {})
        tip_act_modifier = _cust_json.get("tip_act_modifier", {})
        xp_bonus_dict = _cust_json.get("xp_bonus_dict", {})
    else:
        customer_base_preference = {}
        advertising_settings = {}
        reputation_decay = {}
        tip_result_modifier = {}
        tip_advertising_modifier = {}
        tip_act_modifier = {}
        xp_bonus_dict = {}

    ## GOLD / BALANCE CONSTANTS ##
    # EN: Loaded from JSON (BK Evolution).
    # ZH: 从 JSON 加载杂项常量（BK Evolution）。
    _gc_json = DataLoader.load_game_constants()
    if _gc_json:
        starting_gold = _gc_json.get("starting_gold", 500)
        tip_base = _gc_json.get("tip_base", 10)
        maximum_tip_modifier = _gc_json.get("maximum_tip_modifier", 5.0)
        class_discount = _gc_json.get("class_discount", 0.15)
        nsfw = _gc_json.get("nsfw", True)
        stock_picture_threshold = _gc_json.get("stock_picture_threshold", 4)
        fix_pic_balance_variety = _gc_json.get("fix_pic_balance_variety", {})
        fix_pic_balance_accuracy = _gc_json.get("fix_pic_balance_accuracy", {})
        night_pics = _gc_json.get("night_pics", [])
        playerclass_pics = _gc_json.get("playerclass_pics", {})
        _gp = _gc_json.get("god_pics", {})
        god_pics = {(None if k == "null" else k): v for k, v in _gp.items()}
        alignment_pics = _gc_json.get("alignment_pics", {})
        frequency_tags = _gc_json.get("frequency_tags", {})
        mood_runaway_limit = _gc_json.get("mood_runaway_limit", 10)
        free_girls_per_district = _gc_json.get("free_girls_per_district", 12)
    else:
        starting_gold = 500
        tip_base = 10
        maximum_tip_modifier = 5.0
        class_discount = 0.15
        nsfw = True
        stock_picture_threshold = 4
        fix_pic_balance_variety = {}
        fix_pic_balance_accuracy = {}
        night_pics = []
        playerclass_pics = {}
        god_pics = {}
        alignment_pics = {}
        frequency_tags = {}
        mood_runaway_limit = 10
        free_girls_per_district = 12

    sell_girl_preference_boost = 0.01 / 100 # Girl sell price increases or decreases by 1% for every +/- 100 points of preference

    ## GUILD TAX ##
    # Fallback values; JSON override applied in init 1 below

    tax_brackets = [(500, 0), (1000, 0.1), (2000, 0.15), (4000, 0.2), (8000, 0.25), (16000, 0.3), (32000, 0.35), (64000, 0.4), (128000, 0.45), (10**12, 0.5)] # For each (x, y): Up to x average daily net income, raw tax rate is y.

    tax_chapter_penalty = {1 : 0, 2 : 0.05, 3 : 0.075, 4 : 0.1,5 : 0.125, 6 : 0.15, 7 : 0.2} # Raw percentage is increased by this for each tax bracket except 0

    tax_time_pressure_maximum = 0.2 # The maximum time pressure tax modifier

    tax_random_range = 0.25 # The expected lump sum of money may vary by +/- this much every month

    ## XP ##

    # xp_bonus_dict = {
    #         "very bad" : 0.5,
    #         "bad" : 0.75, #7.5,
    #         "average" : 1.0, #10,
    #         "good" : 1.25, #15,
    #         "very good" : 1.5, #20,
    #         "perfect" : 1.75 #35
    #         }


    ## SECURITY ##
    # Loaded from JSON (BK Evolution)

    _sec_json = DataLoader.load_security_events()
    if _sec_json:
        if "security_events" in _sec_json:
            security_events = {int(k): [tuple(x) for x in v] for k, v in _sec_json["security_events"].items()}
        if "alert_limits1" in _sec_json:
            alert_limits1 = {int(k): tuple(v) for k, v in _sec_json["alert_limits1"].items()}
        if "alert_limits2" in _sec_json:
            alert_limits2 = {int(k): tuple(v) for k, v in _sec_json["alert_limits2"].items()}
    else:
        security_events = {}
        alert_limits1 = {}
        alert_limits2 = {}

    # mood_runaway_limit / free_girls_per_district loaded from JSON (BK Evolution).


    ## SHOPS ##

    # Weekly shop item number is partly randomized. Shop inventory level can be improved with resources.

    ## SHOPS ##
    ## Fallback values; JSON override applied below.
    shop_item_number = {
                        "shop" : {"junk" : __("d3 + 3"), "common" : __("d6"), "rare" : __("d3"), "exceptional" : __("d3 + -2")},
                        "city" : {"junk" : __("d6"), "common" : __("d6 + 2"), "rare" : __("d3 + 1"), "exceptional" : __("d3 + -1")},
                        "minion" : {"minion" : __("d5"), "item" : __("d4 + -1")},
                        }

    shop_chapter_modifiers = {
                        1 : {"junk" : 0, "common" : 0, "rare" : 0, "exceptional" : 0, "minion" : 0, "item" : 0},
                        2 : {"junk" : 1, "common" : 1, "rare" : 0, "exceptional" : 0, "minion" : 0, "item" : 0},
                        3 : {"junk" : 1, "common" : 2, "rare" : 0, "exceptional" : 0, "minion" : 0, "item" : 0},
                        4 : {"junk" : 1, "common" : 2, "rare" : 1, "exceptional" : 0, "minion" : 0, "item" : 1},
                        5 : {"junk" : 2, "common" : 2, "rare" : 2, "exceptional" : 0, "minion" : 1, "item" : 1},
                        6 : {"junk" : 3, "common" : 2, "rare" : 2, "exceptional" : 1, "minion" : 1, "item" : 1},
                        7 : {"junk" : 3, "common" : 3, "rare" : 2, "exceptional" : 1, "minion" : 1, "item" : 2},
                        }

    shop_restock_cost = {
                        "shop" : {2 : 500, 3 : 1000, 4 : 2000, 5 : 4000, 6 : 8000, 7 : 15000},
                        "city_merchant" : {2 : 400, 3 : 800, 4 : 1600, 5 : 3200, 6 : 6400, 7 : 12000},
                        "minion_merchant" : {2 : 400, 3 : 800, 4 : 1600, 5 : 3200, 6 : 6400, 7 : 12000},
                        }

    shop_upgrades = {
                    1 : [2, ("wood", 5), ("junk", 2)],
                    2 : [2, ("dye", 10), ("common", 1)],
                    3 : [2, ("leather", 15), ("junk", 3)],
                    4 : [4, ("ore", 10), ("common", 2)],
                    5 : [3, ("dye", 20), ("rare", 1)],
                    6 : [4, ("silk", 15), ("common", 3)],
                    7 : [4, ("marble", 20), ("rare", 1)],
                    8 : [5, ("silk", 30), ("exceptional", 1)],
                    9 : [6, ("diamond", 5), ("rare", 2)],
                    10 : [7, ("diamond", 15), ("exceptional", 2)]
                    }

    shop_chapter_price_multiplier = {1: 1.0, 2: 1.05, 3: 1.1, 4: 1.2, 5: 1.35, 6: 1.5, 7: 1.75}
    shop_chapter_stock_bonus = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3}
    shop_time_pressure_settings = {"price_growth_per_month": 0.02, "max_price_multiplier": 2.0, "stock_decay_per_month": 0.0, "min_stock_multiplier": 1.0}

    ## EN: Load shop parameters from JSON (BK Evolution).
    ## ZH: 从 JSON 加载商店参数（BK Evolution）。
    _sp_json = DataLoader.load_shop_params()
    if _sp_json:
        if "shop_item_number_i18n" in _sp_json:
            shop_item_number = {k: {kk: __(vv) for kk, vv in v.items()} for k, v in _sp_json["shop_item_number_i18n"].items()}
        if "shop_chapter_modifiers" in _sp_json:
            shop_chapter_modifiers = {int(k): v for k, v in _sp_json["shop_chapter_modifiers"].items()}
        if "shop_restock_cost" in _sp_json:
            shop_restock_cost = {k: {int(kk): vv for kk, vv in v.items()} for k, v in _sp_json["shop_restock_cost"].items()}
        if "shop_upgrades" in _sp_json:
            def _to_tuple(x):
                return tuple(x) if isinstance(x, list) else x
            shop_upgrades = {}
            for k, v in _sp_json["shop_upgrades"].items():
                shop_upgrades[int(k)] = [_to_tuple(x) for x in v]
        if "shop_chapter_price_multiplier" in _sp_json:
            shop_chapter_price_multiplier = {int(k): v for k, v in _sp_json["shop_chapter_price_multiplier"].items()}
        if "shop_chapter_stock_bonus" in _sp_json:
            shop_chapter_stock_bonus = {int(k): v for k, v in _sp_json["shop_chapter_stock_bonus"].items()}
        if "shop_time_pressure_settings" in _sp_json:
            shop_time_pressure_settings = _sp_json["shop_time_pressure_settings"]
    shop_time_pressure = 0.0 # Time pressure modifier for shop prices (grows monthly)

    ## CLASSES ##

#### PICTURES #### Feel free to edit or add more

    brothel_pics = {1 : "1 slum brothel.webp",
                    2 : "2 town brothel.webp",
                    3 : "3 town brothel.webp",
                    4 : "4 rich brothel.webp",
                    5 : "5 rich brothel.webp",
                    6 : "6 king brothel.webp",
                    7 : "7 endless brothel.webp"
                    }

    room_pics = {
                # Common rooms
                "tavern" : "tavern.webp",
                "strip club" : "strip club.webp",
                "onsen" : "onsen.webp",
                "okiya" : "okiya.webp",
                # Bedrooms
                "Basic room" : "basic room1.webp",
                "+Basic room+" : "basic room2.webp",
                "*Basic room*" : "basic room3.webp",
                "Standard room" : "standard room1.webp",
                "+Standard room+" : "standard room2.webp",
                "*Standard room*" : "standard room3.webp",
                "Elegant room" : "rich room1.webp",
                "+Elegant room+" : "rich room2.webp",
                "*Elegant room*" : "rich room3.webp",
                "Noble suite" : "noble room1.webp",
                "+Royal suite+" : "noble room2.webp",
                "*Imperial suite*" : "noble room3.webp",
                # Master bedroom
                "Single room" : "master/master0.webp",
                "Double room" : "master/master1.webp",
                "Small suite" : "master/master2.webp",
                "Luxury suite" : "master/master3.webp",
                "Royal suite" : "master/master4.webp",
                "Royal harem" : "master/master5.webp",
                }

    # Picture mappings loaded from JSON (BK Evolution).
    # Must stay in init -10 because declarations.rpy (init -2) references these variables.
    _pics_data = DataLoader.load_picture_mappings()
    if _pics_data:
        advertising_pics = {int(k): v for k, v in _pics_data.get("advertising_pics", {}).items()}
        pony_pics = _pics_data.get("pony_pics", [])
        security_pics = _pics_data.get("security_pics", {})
        arson_pics = _pics_data.get("arson_pics", [])
        violent_pics = _pics_data.get("violent_pics", [])
        treasure_pics = _pics_data.get("treasure_pics", {})
        no_girls_pics = _pics_data.get("no_girls_pics", [])
    else:
        advertising_pics = {}
        pony_pics = []
        security_pics = {}
        arson_pics = []
        violent_pics = []
        treasure_pics = {}
        no_girls_pics = []

    # Tag dict loaded from JSON (BK Evolution).
    # Must stay in init -10 because tag_registry.register_tags_bulk runs at init -4,
    # and tag_list_dict is built at init -3 before girl_files_dict (init -2).
    _tags_data = DataLoader.load_tags()
    if _tags_data:
        _tag_dict_data = _tags_data.get("tag_dict", {})
    else:
        _tag_dict_data = {}

    # playerclass_pics / god_pics / alignment_pics loaded from JSON (BK Evolution).


#### SOUND & MUSIC CHANNELS #### Defines music and sound directories

    ## Channel declaration

    renpy.music.register_channel("music", mixer = "music", file_prefix = "resources/music/")
    renpy.music.register_channel("sound", mixer = "sfx", file_prefix = "resources/sounds/", loop = False)
    renpy.music.register_channel("sound2", mixer = "sfx", file_prefix = "resources/sounds/", loop = False)
    renpy.music.register_channel("sound3", mixer = "sfx", file_prefix = "resources/sounds/", loop = False)
    renpy.music.register_channel("video", mixer = "sfx")

    # EN: Load audio registry from JSON (BK Evolution).
    # ZH: 从 JSON 加载音频注册表（BK Evolution）。
    _audio_json = DataLoader.load_audio_registry()
    if _audio_json:
        playlist = _audio_json.get("playlist", [])
        for _mkey, _mval in _audio_json.get("music_shortcuts", {}).items():
            setattr(store, _mkey, _mval)
        for _skey, _sval in _audio_json.get("sound_shortcuts", {}).items():
            setattr(store, _skey, _sval)
    else:
        playlist = []
        # Music and sound shortcuts will be missing if JSON fails to load


#### TAG DICTIONARY : Converts old tag (strings found in picture filename) to new tag(s) (used in game)
    ## The old tag is discarded. Only the new tags are kept.
    ## All tags should be lower case (for performance reasons) and two characters or more.

    frequency_tags = {"freq_highest" : 900, "freq_high" : 300, "freq_low" : 30, "freq_lowest" : 10} # Base frequency is 100

    ## TAG REGISTRY (Phase 6)
    ## Tags are now registered via TagRegistry for runtime extensibility.
    ## The dictionary below is auto-loaded into tag_registry at init.

    # Tag data is loaded from JSON in variables.rpy (init 1).

init -4 python:
    # Phase 6: Register tags to TagRegistry (must run after registry init at -5, before variables.rpy init at -3)
    tag_registry.register_tags_bulk(_tag_dict_data)
    del _tag_dict_data

    # Pictures with NSFW tags will be ignored when nsfw is set to False.
    # Warning: Turning nsfw off is for debugging only; many pictures will remain uncensored, so watch out.

    nsfw_tags = ["naked", "service", "oral", "blowjob", "handjob", "titjob", "mast", "sex", "anal", "fetish", "bisexual", "group", "beast", "machine", "monster", "big"]

    # Pictures with forbidden tags will be completely ignored. Use this to disable unwanted content.

    forbidden_tags = ["unused"]


#### SUPPORT/CONTACT ####

    ## For feedback, bug report, constructive criticism, etc. Appears in help messages

    URL = "{a=https://www.henthighschool.net/brothel-king/}{color=#9933FF}https://www.henthighschool.net/brothel-king/{/color}{/a}"

#### END OF BK SETTINGS ####


init 1 python:

    # EN: Load brothel parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载青楼参数（BK Evolution）。
    _brothel_params_json = DataLoader.load_brothel_params()
    if _brothel_params_json:
        if "bro_capacity" in _brothel_params_json:
            bro_capacity = _brothel_params_json["bro_capacity"]
        if "bro_helpers" in _brothel_params_json:
            bro_helpers = _brothel_params_json["bro_helpers"]
        if "bro_reputation_cap" in _brothel_params_json:
            bro_reputation_cap = _brothel_params_json["bro_reputation_cap"]
        if "bro_cost" in _brothel_params_json:
            bro_cost = _brothel_params_json["bro_cost"]
        if "brothel_pics" in _brothel_params_json:
            brothel_pics = _brothel_params_json["brothel_pics"]

    # EN: Load shop economy parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载商店经济参数（BK Evolution）。
    _shop_economy_json = DataLoader.load_shop_economy()
    if _shop_economy_json:
        if "chapter_price_multiplier" in _shop_economy_json:
            shop_chapter_price_multiplier = _shop_economy_json["chapter_price_multiplier"]
        if "chapter_stock_bonus" in _shop_economy_json:
            shop_chapter_stock_bonus = _shop_economy_json["chapter_stock_bonus"]
        if "time_pressure" in _shop_economy_json:
            shop_time_pressure_settings = _shop_economy_json["time_pressure"]

    # EN: Load tax parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载税收参数（BK Evolution）。
    _tax_params_json = DataLoader.load_tax_params()
    if _tax_params_json:
        if "tax_brackets" in _tax_params_json:
            tax_brackets = _tax_params_json["tax_brackets"]
        if "tax_chapter_penalty" in _tax_params_json:
            tax_chapter_penalty = _tax_params_json["tax_chapter_penalty"]
        if "tax_time_pressure_maximum" in _tax_params_json:
            tax_time_pressure_maximum = _tax_params_json["tax_time_pressure_maximum"]
        if "tax_random_range" in _tax_params_json:
            tax_random_range = _tax_params_json["tax_random_range"]

    # EN: Load difficulty display text from JSON (BK Evolution).
    #     Uses _i18n suffixed fields for translatable text.
    # ZH: 从 JSON 加载难度显示文本（BK Evolution）。
    #     使用 _i18n 后缀字段标记可翻译文本。
    _diff_text_json = None
    try:
        import json as _json_diff
        _diff_text_path = os.path.join(config.gamedir, "core", "data", "difficulty", "difficulty.json")
        with open(_diff_text_path, "r", encoding="utf-8") as _f_diff:
            _diff_text_json = _json_diff.load(_f_diff)
            del _f_diff
    except Exception:
        pass

    if _diff_text_json:
        if "difficulties" in _diff_text_json:
            for _dk, _dd in _diff_text_json["difficulties"].items():
                if "name_i18n" in _dd:
                    diff_name[_dk] = __(_dd["name_i18n"])
                if "description_i18n" in _dd:
                    diff_description[_dk] = __(_dd["description_i18n"])
        if "settings" in _diff_text_json:
            for _sk, _sd in _diff_text_json["settings"].items():
                if "name_i18n" in _sd:
                    diff_setting_name[_sk] = __(_sd["name_i18n"])
                if "description_i18n" in _sd:
                    diff_setting_description[_sk] = __(_sd["description_i18n"])

    # EN: Load goal UI constants from JSON (BK Evolution).
    # ZH: 从 JSON 加载目标 UI 常量（BK Evolution）。
    _goal_ui_json = DataLoader.load_goal_ui()
    if _goal_ui_json:
        if "channels" in _goal_ui_json:
            goal_channels = tuple(_goal_ui_json["channels"])
        if "channels_no_story" in _goal_ui_json:
            goal_channels_no_story = tuple(_goal_ui_json["channels_no_story"])
        if "categories" in _goal_ui_json:
            goal_categories = _goal_ui_json["categories"]
        if "tb" in _goal_ui_json:
            goal_tb = _goal_ui_json["tb"]
        if "colors" in _goal_ui_json:
            goal_colors = _goal_ui_json["colors"]

    # EN: Load fixations from JSON (BK Evolution).
    #     Rebuilds both fix_dict (Fixation objects) and fix_description (translatable text).
    # ZH: 从 JSON 加载癖好/执念定义（BK Evolution）。
    #     重建 fix_dict（Fixation 对象）和 fix_description（可翻译文本）。
    _fixations_raw = None
    try:
        import json as _json_fix
        _fix_path = os.path.join(config.gamedir, "core", "data", "fixations", "fixations.json")
        with open(_fix_path, "r", encoding="utf-8") as _f_fix:
            _fixations_raw = _json_fix.load(_f_fix)
            del _f_fix
    except Exception:
        pass

    if _fixations_raw and "fixations" in _fixations_raw:
        _new_fix_dict = {}
        _new_fix_description = {}
        for _fk, _fd in _fixations_raw["fixations"].items():
            # Build Fixation object
            try:
                _new_fix_dict[_fk] = Fixation.from_dict(_fd)
            except Exception:
                pass
            # Build fix_description entries with runtime translation
            for _field in ("description", "action", "intro", "pos_reaction", "neg_reaction"):
                _i18n_key = _field + "_i18n"
                if _i18n_key in _fd:
                    _new_fix_description[_fk + " " + _field] = __(_fd[_i18n_key])
        if _new_fix_dict:
            fix_dict = _new_fix_dict
        if _new_fix_description:
            fix_description = _new_fix_description

    # EN: Load interaction menus from JSON (BK Evolution).
    # ZH: 从 JSON 加载交互菜单（BK Evolution）。
    _interact_json = DataLoader.load_interact_dict()
    if _interact_json:
        interact_dict = _interact_json

    _free_interact_json = DataLoader.load_free_interact_dict()
    if _free_interact_json:
        free_interact_dict = _free_interact_json
