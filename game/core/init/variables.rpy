####         INIT VARIABLES FOR B KING          ####################################################
##    Those are the init variables and lists      ##################################################
##    for B King                                  ##################################################
##                                                ##################################################

init -11:
    define persistent.screen_width = 1920
    define persistent.screen_height = 1080

    define persistent.new_game_plus = False
    define persistent.last_difficulty = "normal" # Either stores a stock difficulty name or a custom difficulty dictionary
    define persistent.seen_list = []

    define persistent.cheats = False # Tracks if cheats are on in general (but the main setting is within the 'game' object)
    define persistent.girl_packs = []
    define persistent.girl_mix = {"default" : []}
    define persistent.active_mix = "default"
    define persistent.game_mixes = ["default"]

    define persistent.achievements = {} # Stores achievement levels with the following format: {target : level}. Workaround because Objects cannot be saved as persistent.
    define selected_achievement = None
    define latest_achievements = []

    define persistent.debug_pic_counter_dict = defaultdict(int) # Dictionary containing (pictures : count) when debug_pic_counter is on
    define persistent.debug_pic_counter = False

    define persistent.seen_intro = False
    define persistent.seen_tax_intro = False
    define persistent.seen_ignore_intro = False

    define persistent.pic_ignore_list = [] # Lists all picture paths that have been set to 'ignore' by the player

    default persistent.NGPsettings = {}
    default persistent.meta_upgrades = {} # EN: Stores cross-run meta upgrade ranks. ZH: 存储跨周目局外养成升级等级。

    define _greedy_rollback = False # Experimental (solves loading problems where a save rolls back too far)

    # Init variables for the 'Game Settings' screen are located in the BK_content_menu.rpy file #


init -4 python:

## STORY GIRLS ##
    girl_directories += ["resources/characters/npc/Kunoichi/narika", "resources/characters/npc/Kunoichi/haruka", "resources/characters/npc/Kunoichi/mizuki", "resources/characters/npc/Homura/"] # girl_directories is initiated in BKsettings. Declare story girl paths here

init -3 python:

#### SYSTEM ####

    version_number = 0.2

    VIDEOFORMATS = (".webm", ".mkv", ".avi", ".mpg", ".mpeg") # Took out ".mp4" because of missing codecs
    IMGFORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".avif") # animated gifs and .webp do not work in Ren'py for now

    config.layers.append("myoverlay")

    ## Change native ren'py keymap behavior ##

    try:
        config.keymap['game_menu'].remove('mouseup_3')
    except:
        pass
    # config.keymap['game_menu'].append('o')

    try:
        config.keymap['screenshot'].remove('noshift_K_s')
    except:
        pass
    config.keymap['screenshot'].append('shift_K_s')

    try:
        config.keymap['toggle_fullscreen'].remove('f')
    except:
        pass
    config.keymap['toggle_fullscreen'].append('shift_F')

    try:
        config.keymap['toggle_music'].remove('m')
    except:
        pass
    config.keymap['toggle_music'].append('shift_M') # This doesn't work for reasons unclear

    try:
        config.keymap['hide_windows'].remove('h')
    except:
        pass
    config.keymap['hide_windows'].append('shift_H')

    try:
        config.keymap['self_voicing'].remove('v')
    except:
        pass

    config.keymap['self_voicing'].append('shift_V')

    # config.keymap['inspector'].remove('i')
    # config.keymap['inspector'].append('shift_I')

    config.keymap['viewport_up'] += ('K_PAGEUP', 'repeat_K_PAGEUP')
    config.keymap['viewport_down'] += ('K_PAGEDOWN', 'repeat_K_PAGEDOWN')

    gallery_type = "ev"

    untagged_pics = []
    rating_dict = defaultdict(dict)

    test_event_name = ""

    choice_menu_girl_interact = False
    last_interact_menu = "chat"
    last_free_interact_menu = "chat"

    selected_view_mode = "Auto"

    read_ini_log = ""

#### RESOLUTION ####

    # This is used as the base for the resolution calculations (native BK resolution)
    RES_BASE_X = 1024
    RES_BASE_Y = 768
    res_xy_ratio = 1.0 # WIP - Not working as intended - Default (1.0) is 4:3. Set this aspect ratio to 1.2 for 16:10, 1.334 for 16:9.

    new_res_ratio = config.screen_height/RES_BASE_Y # Used to scale factored images and tooltips

    res_dict = {}

    res_event_width = xres(800) # Base 800
    res_event_height = yres(600) # Base 600

    res_portrait_size = int(config.screen_height*0.2)

#### GOALS ####

    goal_channels = ("story", "story2", "story3", "advance", "advance2", "papa", "contract", "other")
    goal_channels_no_story = ("advance", "advance2", "contract", "other")
    goal_categories = {"story" : "STORY", "story2" : "STORY", "story3" : "STORY", "advance" : "ADVANCE", "advance2" : "ADVANCE", "contract" : "CONTRACT", "other" : "MISC", "papa" : "MISC"}
    goal_tb = {"story" : "tb story", "story2" : "tb story", "story3" : "tb story", "advance" : "tb advance", "advance2" : "tb advance", "contract" : "tb contract", "other" : "tb other", "papa" : "tb papa"}
    goal_colors = {"STORY" : c_softpurple, "ADVANCE" : c_magenta, "CONTRACT" : c_firered, "MISC" : c_yellow}

#### TAG LIST ####

    #<Chris12>
    for tag in tag_dict:
        if tag != tag.lower(): raise Exception("Illegal Tag " + tag + " in tag_dict! Only lowercase allowed.")
        if len(tag) <= 1: raise Exception("Illegal Tag " + tag + " in tag_dict! Tags must be at least 2 characters long.")
    tag_list_dict = {tag : make_list(tag_dict[tag]) for tag in tag_dict}
    sorted_tag_dict_keys = sorted(tag_dict.keys(), key = lambda x : len(x), reverse=True)
    sorted_tags_with_separator = [tag for tag in sorted_tag_dict_keys if " " in tag]
    ending_pattern = re.compile(r"(\(\d*\))?(\.\w{3,4})+$") # can match (and remove) the last part of a filename '(00001).webp'.
    #</Chris12>

#### BADGES ####

    badge_pics = [f for f in renpy.list_files() if f.startswith("resources/ui/badges/") and is_imgfile(f)]

#### DIFFICULTY ####

    diff_list = ["very easy", "easy", "normal", "hard", "insane"] # A list is needed to show the values in order

    diff_settings_range = {
                        "gold" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "budget" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "rewards" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "resources" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "stats" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "pref" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "xp" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "jp" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "rep" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "prestige" : {"min" : 0.1, "max" : 5.0,  "pace" : 0.05},
                        "tax rate" : {"min" : -0.3, "max" :  0.3, "pace" :  0.05},
                        "satisfaction" : {"min" : -3, "max" : 3, "pace" : 1},
                        "security" : {"min" : 0, "max" : 5, "pace" : 1},
                        }

    diff_dict = {
                "very easy" : {"gold" : 1.5,
                            "budget" : 1.25,
                            "rewards" : 1.5,
                            "resources" : 1.5,
                            "stats" : 1.5,
                            "pref" : 1.5,
                            "xp" : 1.5,
                            "jp" : 1.5,
                            "rep" : 1.5,
                            "prestige" : 1.5,
                            "tax rate" : -0.2,
                            "satisfaction" : 2,
                            "security" : 5,
                        },

                "easy" :  {"gold" : 1.25,
                            "budget" : 1.1,
                            "rewards" : 1.25,
                            "resources" : 1.5,
                            "stats" : 1.25,
                            "pref" : 1.25,
                            "xp" : 1.25,
                            "jp" : 1.25,
                            "rep" : 1.25,
                            "prestige" : 1.25,
                            "tax rate" : -0.1,
                            "satisfaction" : 1,
                            "security" : 3,
                        },
                "normal" : {"gold" : 1.0,
                            "budget" : 1.0,
                            "rewards" : 1.0,
                            "resources" : 1.0,
                            "stats" : 1.0,
                            "pref" : 1.0,
                            "xp" : 1.0,
                            "jp" : 1.0,
                            "rep" : 1.0,
                            "prestige" : 1.0,
                            "tax rate" : 0.0,
                            "satisfaction" : 0,
                            "security" : 1,
                        },

                "hard" :  {"gold" : 0.8,
                            "budget" : 0.9,
                            "rewards" : 0.85,
                            "resources" : 0.85,
                            "stats" : 0.75,
                            "pref" : 0.75,
                            "xp" : 0.75,
                            "jp" : 0.75,
                            "rep" : 1.0,
                            "prestige" : 1.0,
                            "tax rate" : 0.1,
                            "satisfaction" : -1,
                            "security" : 0,
                        },
                "insane" : {"gold" : 0.6,
                            "budget" : 0.75,
                            "rewards" : 0.6,
                            "resources" : 0.6,
                            "stats" : 0.5,
                            "pref" : 0.5,
                            "xp" : 0.5,
                            "jp" : 0.5,
                            "rep" : 0.75,
                            "prestige" : 0.75,
                            "tax rate" : 0.2,
                            "satisfaction" : -2,
                            "security" : 0,
                        },
    }

#### CHEATS ####

    always_show_personality = defaultdict(bool)


#### STARTING GAME VARIABLES AND OBJECTS ####

    ## INIT VARIABLES ##

#    global selected_girl
    selected_girl = None
    selected_sex_act = None
#    global selected_quest
    selected_item = None
    selected_quest = None
    selected_district = None
    selected_location = None
    selected_destination = None
    show_spellbook = False
    pers_showing = "personality"
#    vp_value = 0
    vp_adj = ui.adjustment()
    sched_adj = ui.adjustment()

    adjust_vp = True
    shake_count = 0
    always_show_brothel_report = False

    last_contract_result = None

#### RANDOM TIPS ####

    random_tips = [
                    __("Zan is an exciting place... Make sure to explore the city regularly!"),
                    __("Did you know the brothel has many shortcuts? You need to find the right key..."),
                    __("Beautiful girls make the best masseuses."),
                    __("Masseuses should be {b}beautiful{/b} and {b}sensitive{/b}. A good {b}body{/b} and {b}refinement{/b} are also important."),
                    __("A girl with a good Body makes a great dancer."),
                    __("Dancers should have a good {b}body{/b} and high {b}libido{/b}. {b}Refinement{/b} and {b}charm{/b} also help."),
                    __("Charming girls will do better as waitresses."),
                    __("Waitresses need {b}charm{/b} and {b}constitution{/b}. It cannot hurt if they are {b}beautiful{/b}, and have a good {b}body{/b} as well."),
                    __("Geishas should be refined girls to achieve the best results."),
                    __("Geishas should be {b}refined{/b} and {b}obedient{/b}. {b}Beauty{/b} and {b}charm{/b} also help make a perfect geisha."),
                    __("Higher-class customers are harder to satisfy, but they tip better."),
                    __("Don't forget to pay for the brothel's security. Things can escalate quickly."),
                    __("Your brothel gets dirty every time girls interact with customers. Your maintenance team should keep up, otherwise you'll end up spending a lot more to repair the damage later."),
                    __("Advertising girls are good if you want to bring more customers to the brothel. Don't bring more than you can handle, however: unsatisfied customers will lower your reputation."),
                    __("Disobedient girls are less likely to accept working or training."),
                    __("Girls with high Libido are more likely to agree to and enjoy sex, and can serve multiple customers too."),
                    __("Sensitive girls are good at making customers happy, regardless of the act."),
                    __("Constitution determines how much energy a girl has, and how many customers she can serve."),
                    __("Charm and Sensitivity make your girls better at handjobs, blowjobs and other service sex acts."),
                    __("A good {b}service{/b} skill is required to perform Service, of course, as well as {b}sensitivity{/b}. {b}Charm{/b} and the {b}fetish{/b} skill also help."),
                    __("Beauty and Libido are important for regular Sex acts."),
                    __("For regular Sex, high {b}sex{/b} and {b}libido{/b} skills give the best results. {b}Beauty{/b} and {b}service{/b} also boost sex."),
                    __("Girls with a good Body and Constitution can handle Anal sex well."),
                    __("Anal sex requires a high {b}anal{/b} skill and a good {b}constitution{/b}. {b}Body{/b} and {b}sex{/b} skills also help."),
                    __("Refinement and Obedience are good for Fetish sex acts."),
                    __("A girl needs a good {b}fetish{/b} and {b}obedience{/b} skills for Fetish sex acts. {b}Refinement{/b} and {b}anal{/b} skills also factor."),
                    __("The brothel report has lots of useful information about the brothel. If you want information about a given girl, check out her statistics in the girl tab."),
                    __("When working, girls receive both XP and JP. XP allow a girl to level up their stats and earn perks, JP allow a girl to get better at a given job or sex act. Both max out depending on her rank."),
                    __("Customers' tastes are different in the kind of entertainment and sex acts they like. Variety is key to keep all customers satisfied."),
                    __("Every satisfied customer increases your reputation. But unhappy customers will diss your brothel and your girls, so watch out."),
                    __("Overall, customer satisfaction stems from two factors: the quality of entertainment they receive, and the quality of your whores."),
                    __("Girls may become Bisexual, allowing two of them to service the same customer."),
                    __("Girls may learn how to have Group sex, allowing them to serve two or three customers at the same time."),
                    __("Bisexual and Group sex are always satisfying for the customers."),
                    __("Upkeep is important to keep your girls in the mood. Although happy girls may work for you for little upkeep, their mood will drop dramatically if their upkeep gets too low."),
                    __("Although your security will take care of most problems, your girls will need some personal defense if a crazy customer targets them directly. Beware, though, any weapon you give them could be used against you..."),
                    __("The most effective way to train your girls for sex acts is to do it yourself, but it's time-consuming. Maybe you can find someone who will train them for you?"),
                    __("Some of the people you meet can become trainers for your girls. Make sure to pick the one with the best ability for your management style."),
                    __("In Zan, a reputation for good or evil can make a lot of difference. Every good or bad deed has consequences. Of course, not everything is black and white. Some people like to walk the line between both..."),
                    __("I hear there are girls with very loose morals hanging out in the various districts of the city. You wouldn't happen to know anything about that, would you?"),
                    __("The girl from the shop is always acting flirtatious and bitchy,... I don't like her. I wish we could find other places to shop in town."),
                    __("You can buy girls that have already been trained at the slave market. This can save you some time, although you can never be 100% sure about the quality of the training they received."),
                    __("By talking with your girls, you can get to know them, and they might even tell you their personal stories."),
                    __("Girls will love you if you act kindly towards them and let them do what they like."),
                    __("Girls will fear you if you act harshly towards them or force them to do things they don't want."),
                    __("When all else fails, you can lecture your girls in order to start their training. Being Charismatic helps."),
                    __("Your Strength determines how good you are in a fight, or at pulling off various physical feats."),
                    __("Your Spirit determines how good you are with using, detecting and resisting magic."),
                    __("Charisma is important for all kinds of interactions, both with your girls and in the outside world."),
                    __("Your Speed determines how many actions you can take every day. It is rarely used for anything else."),
                    __("Unhappy girls may run away from you. If you cannot afford to hire bounty hunters, your last chance to get them back will be to explore the city on your own."),
                    __("Don't forget to upgrade the brothel bedrooms. Girls and customers alike will see their mood deteriorate if the bedrooms are below par, especially at higher ranks."),
                    __("Common rooms can host a limited number of customers. Make sure you have enough room to entertain everyone."),
                    __("When a girl joins your brothel, you must have a room ready for her. Otherwise, you might have to wait until you expand to receive her."),
                    __("Some people sell curious things around in the city, even monsters or animals. I'm not sure what you'd need them for."),
                    __("Sex skills cannot be improved by levelling. One needs first-hand experience to learn them."),
                    __("Classes are useful to improve a girl's inferior skills more quickly."),
                    __("Every girl has her own reputation, separate from your brothel's. Reputation is key for a girl to reach higher ranks."),
                    __("The best way to improve a girl's reputation is for her to succeed in Quests."),
                    __("Sex slaves receive ranks from the Slavers guild. Ranks determines many things, including max level and max skills."),
                    __("At the lowest rank, a girl's Skills are limited to 50. Every additional Rank improves the Skill maximum by 50 more."),
                    __("When a girl levels up, she receives Skill points, depending on her current Rank. Also, she receives a perk point every level."),
                    __("Every five levels, a girl will receive an extra perk point."),
                    __("No matter what, a girl cannot go above level 25."),
                    __("I've heard a rumor about a secret Rank at the Slaver guild, higher even than Rank 'S'."),
                    __("Please, Master, never ever let your money fall under zero denars! I've heard some people will try to tempt you with shady deals if you're in debt, but they just mean even more trouble."),
                    __("Never trust an Elf. Don't come here saying I didn't warn you."),
                    __("At higher ranks, integrating new girls can be tough. Make sure to use Classes, Items, Perks and other bonuses to help the new girl get ahead."),
                    __("When you feel like you've seen it all, you can disable some night events in the Game Settings menu."),
                    __("Don't like the random name generation? You can disable it in the Game Settings menu."),
                    __("Not into some of the more hardcore acts? Disable them in the Game Settings menu."),
                    __("Hit 'Ctrl' to skip night events, or any dialog you've already seen."),
                    __("A right click will take you back one step. Right-clicking on the main menu will bring out the Options menu."),
                    __("During the day, come back to the Home screen at any time with the 'H' key."),
                    __("Press 'E' to end the day and move on the the night's events."),
                    __("Spells can be auto-cast, using any leftover mana points you have left at the end of the day."),
                    __("Pressing the 'Esc' key will bring out the game menu"),
                    __("You can come back to the latest visited location simply by using the 'L' key."),
                    __("Prestige is earned whenever you or your girls have sex. Earning prestige will allow you to level up."),
                    __("Your skills cannot naturally go over 10, but Items and Magic can help."),
                    __("Virgin girls receive a new trait after they are deflowered, depending on the conditions under which it happened."),
                    __("If your girls are in a bad mood, make sure you pay them enough, and that their accommodations are comfortable enough."),
                    __("Advertising increases the maximum amount of money per customer. Make sure they bring a fat purse!"),
                    __("Classes may cause a girl's skills to exceed their level cap. Handy if you have the cash for them."),
                    __("After a while, higher skills become harder to increase for experienced girls. Classes can help you get around that."),
                    __("Although jobs and sex acts rely on a couple of major skills, having other high skills can often give a little boost to a girl's results."),
                    __("Even though recognizing a naked girl should be easy, people can never agree on what 'nudity' is, exactly! Can you believe it?"),
                    __("Public acts are confusing. Is it public because it's outside, or because other people can see you? I can never tell."),
                    __("You can quick-save with F5 and quick-load with F9 (when shortcuts are active). What does it mean? I have no idea!"),
                    __("Be careful not to let your girls fall sick or hurt! Hurt girls will recover energy half as fast as other girls."),
                    __("Are notifications flying by too fast for you? You can review the latest notifications by clicking on the '?' button."),
                    __("Game settings give you various options to tweak the game's content and UI to your liking."),
                    __("Brokipedia in the '?' menu will help you grasp some finer details about the game. It doesn't hold everything yet, but will be improved over time."),
                    __("Mind the special effects from this month's moon. They may give extra rewards for some specific activities you wouldn't normally do."),
                    __("If you put fear in your girls' heart, Evil powers may become accessible from the Farm. I shiver to think about what you could do with these."),
                    __("Evil brothel owners use up slave girls until their sanity is gone, then throw them out on the street. You wouldn't do that, would you?"),
                    __("I heard that if you summon a magical pet 15 times, something special happens... How cute."),
                    __("Tired of the story? Reach the end of the game at least once to unlock 'No story' mode."),
                    __("I've heard of something called 'NewGame+' if you reach the end of the game. Whatever could that mean?"),
                ]

    ## EN: Load loading tips from JSON (BK Evolution).
    ## ZH: 从 JSON 加载加载画面提示（BK Evolution）。
    _lt_json = DataLoader.load_loading_tips()
    if _lt_json and "random_tips_i18n" in _lt_json:
        random_tips = [__(s) for s in _lt_json["random_tips_i18n"]]


    ## MC ##

    all_MC_stats = ["strength", "spirit", "charisma", "speed"]

    ## INVENTORY ##

    MC_inventory_slots = ["hands", "accessory", "misc"]
    girl_inventory_slots = ["hands", "body", "neck", "finger", "accessory"]
    # EN: Load inventory filters, filter lists, and sorters from JSON (BK Evolution).
    # ZH: 从 JSON 加载库存过滤器、过滤列表和排序器（BK Evolution）。
    _inv_json = DataLoader.load_inventory_sorters()
    if _inv_json:
        inventory_filters = _inv_json.get("inventory_filters", {})
        filter_list = {(None if k == "null" else k): v for k, v in _inv_json.get("filter_list", {}).items()}
        _sorters = _inv_json.get("sorter_dict", {})
        sorter_dict = {k: [__(v.get("caption_i18n", "")), v.get("attribute", ""), __(v.get("tooltip_i18n", "")), v.get("reverse", False)] for k, v in _sorters.items()}
    else:
        inventory_filters = {}
        filter_list = {}
        sorter_dict = {}

    ## RESOURCES ##
    # EN: Loaded from JSON (BK Evolution).
    # ZH: 从 JSON 加载建筑资源参数（BK Evolution）。
    _res_json = DataLoader.load_resource_params()
    if _res_json:
        build_resources = _res_json.get("build_resources", [])
        resource_gold_value = {int(k): Fraction(*v) for k, v in _res_json.get("resource_gold_value", {}).items()}
        resource_sell_discount = _res_json.get("resource_sell_discount", 0.1)
        _rber = _res_json.get("resource_base_exchange_rate", {})
        resource_base_exchange_rate = {int(outer_k): {int(inner_k): Fraction(*inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in _rber.items()}
    else:
        build_resources = []
        resource_gold_value = {}
        resource_sell_discount = 0.1
        resource_base_exchange_rate = {}



    ## ALERTS ##

    seen_alerts = defaultdict(bool)


    ## LICENCES ##
    # EN: Loaded from JSON (BK Evolution).
    # ZH: 从 JSON 加载（BK Evolution）。
    _unlock_json = DataLoader.load_unlock_params()
    if _unlock_json and "license_dict" in _unlock_json:
        license_dict = {int(k): (__(v["name_i18n"]), v["pic"]) for k, v in _unlock_json["license_dict"].items()}
    else:
        license_dict = {}



    ## BROTHEL PICS AND ROOMS ##

init python:

    brothel_images = {
                        1 : renpy.image("brothel1", im.Scale("resources/brothels/" + brothel_pics[1], config.screen_width, config.screen_height)),
                        2 : renpy.image("brothel2", im.Scale("resources/brothels/" + brothel_pics[2], config.screen_width, config.screen_height)),
                        3 : renpy.image("brothel3", im.Scale("resources/brothels/" + brothel_pics[3], config.screen_width, config.screen_height)),
                        4 : renpy.image("brothel4", im.Scale("resources/brothels/" + brothel_pics[4], config.screen_width, config.screen_height)),
                        5 : renpy.image("brothel5", im.Scale("resources/brothels/" + brothel_pics[5], config.screen_width, config.screen_height)),
                        6 : renpy.image("brothel6", im.Scale("resources/brothels/" + brothel_pics[6], config.screen_width, config.screen_height)),
                        7 : renpy.image("brothel7", im.Scale("resources/brothels/" + brothel_pics[7], config.screen_width, config.screen_height)),
                    }

init 1 python:
    # EN: Load room data from JSON (BK Evolution).
    # ZH: 从 JSON 加载房间数据（BK Evolution）。
    _rooms_json = DataLoader.load_rooms()

    if _rooms_json and "room_pics" in _rooms_json:
        room_pics = _rooms_json["room_pics"]

    # ROOMS #

    if _rooms_json and "bedrooms" in _rooms_json:
        room_dict = {int(k): Room(v["name"], v["level"], v.get("type", "bedroom"), v.get("job"), v.get("cost", 0))
                     for k, v in _rooms_json["bedrooms"].items()}
    else:
        room_dict = {
                    1 : Room("Basic room", 1),
                    2 : Room("+Basic room+", 2),
                    3 : Room("*Basic room*", 3),
                    4 : Room("Standard room", 4),
                    5 : Room("+Standard room+", 5),
                    6 : Room("*Standard room*", 6),
                    7 : Room("Elegant room", 7),
                    8 : Room("+Elegant room+", 8),
                    9 : Room("*Elegant room*", 9),
                    10 : Room("Noble suite", 10),
                    11 : Room("+Royal suite+", 11),
                    12 : Room("*Imperial suite*", 12)
                    }

    if _rooms_json and "common_rooms" in _rooms_json:
        common_room_dict = {k: Room(v["name"], v["level"], v["type"], v.get("job"), v.get("cost", 0))
                            for k, v in _rooms_json["common_rooms"].items()}
    else:
        common_room_dict = {
                            "tavern" : Room("tavern", 0, "special", job = "waitress"),
                            "strip club" : Room("strip club", 0, "special", job = "dancer"),
                            "onsen" : Room("onsen", 0, "special", job = "masseuse"),
                            "okiya" : Room("okiya", 0, "special", job = "geisha"),
                            }

    for room in common_room_dict:
        for dirt_state in ("clean enough", "dusty", "dirty", "disgusting", "fire"):
            path = "resources/brothels/rooms/" + room + {"clean enough" : "", "dusty" : __("_dusty"), "dirty" : __("_dirty"), "disgusting" : __("_verydirty"), "fire" : __("_verydirty")}[dirt_state] + ".webp"
            renpy.image(room + " " + dirt_state, ProportionalScale(path, config.screen_width, config.screen_height))

    if _rooms_json and "master_bedrooms" in _rooms_json:
        master_bedrooms = {int(k): Room(v["name"], v["level"], v["type"], v.get("job"), v.get("cost", 0))
                           for k, v in _rooms_json["master_bedrooms"].items()}
    else:
        master_bedrooms = {
                            0 : Room("Single room", level=0, type="master", cost=0),
                            1 : Room("Double room", level=1, type="master", cost=750),
                            2 : Room("Small suite", level=2, type="master", cost=2500),
                            3 : Room("Luxury suite", level=3, type="master", cost=7500),
                            4 : Room("Royal suite", level=4, type="master", cost=25000),
                            5 : Room("Royal harem", level=5, type="master", cost=75000),
                            }

    if _rooms_json and "common_room_keys" in _rooms_json:
        all_common_rooms = _rooms_json["common_room_keys"]
    else:
        all_common_rooms = ["tavern", "strip club", "onsen", "okiya"]

    if _rooms_json and "job_room_map" in _rooms_json:
        _jrm = _rooms_json["job_room_map"]
        job_room_dict = {k: v for k, v in _jrm.items()}
    else:
        job_room_dict = {"waitress" : "tavern",
                        "dancer" : "strip club",
                        "masseuse" : "onsen",
                        "geisha" : "okiya",
                        "whore" : "bedroom"
                        }

    if _rooms_json and "job_room_display_name_i18n" in _rooms_json:
        job_room_display_name = {k: __(v) for k, v in _rooms_json["job_room_display_name_i18n"].items()}
    else:
        job_room_display_name = {"waitress" : __("Tavern"),
                                "dancer" : __("Strip club"),
                                "masseuse" : __("Onsen"),
                                "geisha" : __("Okiya"),
                                "whore" : __("Bedroom")
                                }

    if _rooms_json and "room_capacity" in _rooms_json:
        room_capacity_dict = _rooms_json["room_capacity"]
    else:
        room_capacity_dict = {0 : 4, 1 : 4, 2 : 6, 3 : 8, 4 : 10, 5 : 12, 6 : 14, 7 : 16}

init -4 python:

    ## CITY BUTTONS
    # EN: Loaded from JSON (BK Evolution).
    # ZH: 从 JSON 加载（BK Evolution）。
    _loc_tb_json = DataLoader.load_location_tooltips()
    if _loc_tb_json:
        location_tb = _loc_tb_json.get("location_tb", {})
        _papa = _loc_tb_json.get("papa_location", {})
        papa_location = {k: __(v["name_i18n"]) for k, v in _papa.items()}
    else:
        location_tb = {}
        papa_location = {}

    suzume_hints_active = False

    ## FARM
    # Fallback values; JSON override applied in init 1 below

    installation_price = {
                        0: 100,
                        1: 250,
                        2: 500,
                        3: 1000,
                        4: 1750
                    }

    farm_type_list = ["machine", "beast", "monster", "stallion"]
    farm_inst_list = ["stables", "pig stall", "monster den", "workshop"]
    farm_installations_dict = {"machine" : __("workshop"), "beast" : __("pig stall"), "monster" : __("monster den"), "stallion" : __("stables")}

    minion_xp_to_level = {
                        0: 0,
                        1: 10,
                        2: 25,
                        3: 50,
                        4: 100,
                        5: 250
                    }

    minion_price = {
                    0: 100,
                    1: 200,
                    2: 300,
                    3: 400,
                    4: 500,
                    5: 750
                }

    minion_description = {"stallion" : __("Stallions are male sex slaves from the Blood Islands, magically brainwashed and bred selectively for their abnormally large dicks...."),
                        "beast" : __("Beasts are all sorts of animals that Gizel keeps around at the farm. More like a zoo, really."),
                        "monster" : __("Monsters are unnatural fiends crawling inside the darkest caves of Xeros. They come in many forms, but the ones with tentacles are the most sought after."),
                        "machine" : __("Machines or artefacts have many uses, but in Gizel's workshop, they really only seem to be designed for one thing: sex.")
                        }

    all_minion_types = ["stallion", "beast", "monster", "machine"]

    farm_pics = {
                "stallion" : ["big"],
                "beast" : ["beast"],
                "monster" : ["monster"],
                "machine" : ["machine", "toy"],
                }

    farm_holding_dict = {
                        "libido" : __("Tending to minions (Lib)"),
                        "sensitivity" : __("Tending to Gizel (Sen)"),
                        "obedience" : __("Cleaning up the farm (Ob)"),
                        "constitution" : __("Working outside (Con)"),
                        "rest": __("Resting"),
                        }

    farm_ttip =         {
                        "libido" : __("She will tend to the farm creatures (boosts libido, costs energy)."),
                        "sensitivity" : __("She will tend to Gizel personally (boosts sensitivity, costs energy)."),
                        "obedience" : __("She will clean up the farm (boosts obedience, costs energy)."),
                        "constitution" : __("She will work-out in the backyard (boosts constitution, costs energy)."),
                        "rest": __("She will be resting in her cell."),
                        "gentle": __("In {b}gentle{/b} mode, she won't be forced to do something she doesn't want to. This training will not generate fear."),
                        "tough": __("In {b}tough{/b} mode, Gizel will overcome moderate resistance on her part. This training will generate fear."),
                        "hardcore": __("In {b}hardcore{/b} mode, Gizel will ignore all red lines and force her to do anything. This training will generate massive fear."),
                        }

    farm_description = {"stallion intro" : __("%s spent the night in the stables with a well-hung stallion."),
                        "beast intro" : __("%s spent the night in the pig stalls with a horny, filthy animal."),
                        "monster intro" : __("%s spent the night in the monster den with a lewd, disgusting creature."),
                        "machine intro" : __("%s spent the night in the workshop attached to a large and strange machine."),
                        "stallion intro plural" : __("%s spent the night in the stables with %s well-hung stallions."),
                        "beast intro plural" : __("%s spent the night in the pig stalls with %s drooling, horny beasts."),
                        "monster intro plural" : __("%s spent the night in the monster den, harassed by %s lewd and disgusting creatures."),
                        "machine intro plural" : __("%s spent the night in the workshop strapped to an array of %s arcane machines."),
                        "naked intro" : __("Gizel paraded %s naked in front of %s."),
                        "service intro" : __("Gizel pushed %s to her knees and made her service %s."),
                        "sex intro" : __("Gizel told %s to fuck %s."),
                        "anal intro" : __("Gizel told %s to let %s fuck her ass."),
                        "fetish intro" : __("Gizel showed %s the chains on the wall and told her she'd watch %s have its way with her."),
                        "bisexual intro" : __("Gizel decided to join %s for a little fun with a %s."),
                        "group intro" : __("Gizel told %s to get ready to have sex with a group of %ss."),

                        "stallion good" : __(" %s couldn't take her eyes off the stallion's rock-hard cock. {color=[c_green]}Her training went well.{/color}"),
                        "stallion average" : __(" %s was impressed and a little worried upon seeing the size of the stallion's hard cock. {color=[c_white]}Her training went normally.{/color}"),
                        "stallion bad" : __(" The stallion's large dick scared %s and she recoiled fearfully. {color=[c_red]}Her training went poorly.{/color}"),
                        "beast good" : __(" %s was curious and aroused by the weird shape and smell of the beast's genitals. {color=[c_green]}Her training went well.{/color}"),
                        "beast average" : __(" %s felt uncomfortable around the animals and their weird bodies. {color=[c_white]}Her training went normally.{/color}"),
                        "beast bad" : __(" %s couldn't believe she was being treated like a farm animal and stood as far as she could from the beasts. {color=[c_red]}Her training went poorly.{/color}"),
                        "monster good" : __(" %s felt incredibly aroused by the pheromones emanating from the monster. {color=[c_green]}Her training went well.{/color}"),
                        "monster average" : __(" %s felt weakened and confused by the monster's strange musk. {color=[c_white]}Her training went normally.{/color}"),
                        "monster bad" : __(" %s felt disgusted and nauseated because of the monster's icky smell. {color=[c_red]}Her training went poorly.{/color}"),
                        "machine good" : __(" The cold touch of metal and the elastic feel of rubber against her skin sent %s over the top. {color=[c_green]}Her training went well.{/color}"),
                        "machine average" : __(" %s felt very odd attached to a strange, vibrating artefact in the middle of a workshop full of bizarre sex toys. {color=[c_white]}Her training went normally.{/color}"),
                        "machine bad" : __(" %s was scared by the spiky, threatening look of the machine and couldn't relax. {color=[c_red]}Her training went poorly.{/color}"),

#                        "naked result good" : __("{color=[c_green]}%s was aroused by having her body on display before the %s, her nipples becoming visibly erect.{/color} Gizel pinched them hard, teasing her mercilessly."),
#                        "naked result average" : __("{color=[c_white]}%s felt confused and ashamed, standing naked and exposed.{/color} She blushed as Gizel made her display every part of her body to the %s."),
#                        "naked result bad" : __("{color=[c_lightred]}%s cowered and cried as she was made to stand naked in front of the %s.{/color}.Gizel commented harshly on her poor performance."),
#                        "service result good" : __("{color=[c_green]}%s kneeled and starting working on the %s. She did her best to frown and hide her enjoyment, but Gizel could see she was getting wet.{/color}"),
#                        "service result average" : __("{color=[c_white]}%s did what she was asked, polishing the %s's strange dick with her lips and tongue.{/color}"),
#                        "service result bad" : __("{color=[c_lightred]}Tears ran down %s's cheeks as the %s forcefully fucked her throat.{/color}"),
#                        "sex result good" : __("{color=[c_green]}%s could hardly hide her sighs and screams of pleasure as the %s started fucking her mercilessly.{/color}"),
#                        "sex result average" : __("{color=[c_white]}%s shivered and moaned as the %s pumped its large, strange dick back and forth inside her tight pussy.{/color}"),
#                        "sex result bad" : __("{color=[c_lightred]}%s screamed in pain and fought weakly as the %s violently fucked her.{/color}"),
#                        "anal result good" : __("{color=[c_green]}%s yelled with pleasure as her ass got ravaged by the %s's large cock.{/color}"),
#                        "anal result average" : __("{color=[c_white]}%s moaned with a mix of pain and shameful pleasure as the %s violated her asshole.{/color}"),
#                        "anal result bad" : __("{color=[c_lightred]}%s screamed in pain and cried bitterly as the %s forced its large cock inside her tight asshole.{/color}"),
#                        "fetish result good" : __("{color=[c_green]}%s squirmed with confusion and pleasure, and quickly reached climax as the %s relentlessly violated her bound body.{/color}"),
#                        "fetish result average" : __("{color=[c_white]}%s screamed and moaned as the %s inflicted a strange mix of pain and pleasure on her weak body.{/color}"),
#                        "fetish result bad" : __("{color=[c_lightred]}%s shrieked with pain as the %s ruthlessly defiled her defenseless body.{/color}"),
#                        "bisexual result good" : __("{color=[c_green]}%s and Gizel strated licking and fingering each other's pussy, and soon forgot the %s as they passionately brought each other to climax.{/color} Gizel was very satisfied."),
#                        "bisexual result average" : __("{color=[c_white]}Gizel forced %s to service both her and the %s.{/color} They both came forcefully on the poor girl's face. She was left confused by the whole ordeal."),
#                        "bisexual result bad" : __("{color=[c_lightred]}%s was disgusted and tried to let out muffled screams as Gizel forcefully buried her pussy into her face, nearly choking her, while the %s tended to her other holes.{/color}"),
#                        "group result good" : __("{color=[c_green]}As %s and the %ss fucked in a variety of positions, she started enjoying herself and taking the lead, showing the minions which holes to use invitingly.{/color}"),
#                        "group result average" : __("{color=[c_white]}Grumbling, %s followed orders and used all of her holes to pleasure the %ss. However, she didn't seem to hate it as much as she was pretending to.{/color}"),
#                        "group result bad" : __("{color=[c_lightred]}%s cried and screamed as the %ss took turns violating her body.{/color} Gizel kept tauting her during the whole ordeal as she sobbed silently."),
                        "pen obedience": __("%s reflected on her unfortunate circumstances and misdeeds that brought her to the farm. {color=[c_green]}She thinks that perhaps, if she was more obedient, she wouldn't get in trouble.{/color}"),
                        "pen constitution": __("Even though she was locked in, %s was determined to stay in shape. {color=[c_green]}She did some abs crunches and push ups and has become fitter.{/color}"),
                        "pen sensitivity": __("%s was bored and started thinking about the weird creatures in the farm and their more 'unusual' features. {color=[c_green]}Soon, she was feeling flushed and strangely aroused.{/color}"),
                        "pen libido": __("%s was feeling bored and horny, so she decided to masturbate a little, listening to the strange noises of the farm. {color=[c_green]}She enjoyed herself.{/color}"),

                        "holding gentle obedience" : __("Gizel sent %s to clean up the farm, telling her to scrub every corner of the barn and wash the multiple stains on the floor. %s sighed and got to work."),
                        "holding gentle constitution" : __("Gizel made %s run laps around the back on the horsetrack, stopping and yelling at %s to go faster from time to time to keep her on edge."),
                        "holding gentle sensitivity" : __("Gizel used %s as her personal servant to pursue her perverted fantasies with a variety of strange toys. Gizel didn't push %s too much, but she still discovered new things."),
                        "holding gentle libido" : __("Gizel asked %s to tend to the minions: feeding them, cleaning them, and helping them 'release their stress'. %s learnt a good deal about the minions' peculiar anatomy as she worked."),
                        "holding tough obedience" : __("Gizel sent %s to clean up the farm, telling her to scrub every corner of the barn and wash the multiple stains on the floor. %s did what she was asked, rather than face the threat of Gizel's magical lash."),
                        "holding tough constitution" : __("Gizel made %s run laps around the back on the horsetrack, giving %s vicious swats with a riding crop whenever she caught her slowing down."),
                        "holding tough sensitivity" : __("Gizel used %s as her personal servant to pursue her perverted fantasies, forcing her to lick her body and use various toys on her hungry holes. It was tough, but %s learnt new things."),
                        "holding tough libido" : __("Gizel asked %s to tend to the minions: feeding them, cleaning them, and helping them 'release their stress'. Gizel forced her to touch parts of their anatomy she wasn't comfortable around, arousing some strange feelings in %s."),
                        "holding hardcore obedience" : __("Gizel sent %s to clean up the farm, telling her to scrub every corner of the barn and wash the multiple stains on the floor. %s got a taste of her whip mercilessly if any dirt was left."),
                        "holding hardcore constitution" : __("Gizel made %s run laps around the back on the horsetrack, wearing various punishment instruments like a wooden collar, shackles or nipple clamps. %s had to suffer through it to get stronger."),
                        "holding hardcore sensitivity" : __("Gizel used %s as her personal servant to pursue her perverted fantasies, forcing her to lick her body and use various toys on her hungry holes. She made sure %s helped with {i}everything{/i}, especially what she was most uncomfortable with."),
                        "holding hardcore libido" : __("Gizel asked %s to tend to the minions: feeding them, cleaning them, and helping them 'release their stress'. Gizel told %s she was not allowed to use her hands unless she would get a beating, forcing her to get creative."),

                        "holding obedience good": __(" As an added challenge, Gizel made %s wear tight ropes bound across her body as she went on with her work. {color=[c_green]}The rough ropes rubbed against her body in a way both uncomfortable and oddly arousing.{/color}"),
                        "holding obedience bad": __(" {color=[c_lightred]}%s was disgusted by all the filth and bodily fluids left over by Gizel's minions.{/color}"),
                        "holding constitution good": __(" Gizel thought it would drive %s wilder to roam outside free of clothes, so she made her run naked alongside the horses. {color=[c_green]}Being naked outdoors with the animals made her more comfortable with her body.{/color}"),
                        "holding constitution bad": __(" {color=[c_lightred]}As %s completed her laps in record timing, she gave Gizel a contemptuous and defiant look.{/color}"),
                        "holding sensitivity good": __(" %s gives Gizel a wonderful orgasm as she licks her erect clit with a skillful tongue. {color=[c_green]}She is now more familiar with ways to pleasure a woman.{/color}"),
                        "holding sensitivity bad": __(" Gizel worked %s too hard, leaving her exhausted and panting on the floor. {color=[c_lightred]}Her constitution has suffered.{/color}"),
                        "holding libido good": __(" {color=[c_green]}Several hours spent working with the minions have allowed %s to increase her technique.{/color}"),
                        "holding libido bad": __(" {color=[c_lightred]}As a result of spending too many hours jerking off minions, %s's technique has become more mechanical.{/color}"),
                        }

    ## EN: Load farm description texts from JSON (BK Evolution), fallback to hardcoded above.
    ## ZH: 从 JSON 加载农场描述文本（BK Evolution），否则使用上方硬编码。
    _fd_json = DataLoader.load_farm_descriptions()
    if _fd_json and "farm_descriptions_i18n" in _fd_json:
        farm_description = {k: __(v) for k, v in _fd_json["farm_descriptions_i18n"].items()}

    farm_holding_stats = {"constitution" : ("naked", "obedience"), "obedience" : ("fetish", "libido"), "sensitivity" : ("bisexual", "constitution"), "libido" : ("service", "sensitivity")}

    farm_holding_tags = {"constitution" : ["run", "constitution"], "obedience" : ["obedience", "maid"], "sensitivity" : ["sensitivity"], "libido" : ["libido"]}

    minion_adjectives = {
                        "stallion" : ["erect", "drooling", "horny", "well-built", "snorting", "bulky", "nickering", "sleazy"],
                        "beast" : ["drooling", "horny", "filthy", "dirty", "rowdy", "excited", "fat"],
                        "monster" : ["horny", "gooey", "filthy", "dirty", "large", "wiggly", "weird-looking", "strange", "sleazy"],
                        "machine" : ["buzzing", "strange", "weird-looking", "bizarre", "enchanted", "convoluted", "protruding"],
                        }

    minion_name_dict = {
                        "consonants" : ["q", "w", "r", "t", "p", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"],
                        "vowels" : ["a", "e", "i", "o", "u", "y"],
                        "monster1" : ["gr", "kr", "le", "ry", "shr", "dr", "kz", "gz", "th", "bl", "kl", "wr", "qr", "mr", "sh"],
                        "monster2" : ["ck", "k", "rk", "rz", "rm", "xx", "uz", "oo", "hu", "qq", "tz", "zt", "rh", "th"],
                        }

    ## EN: Load farm holding parameters from JSON (BK Evolution).
    ## ZH: 从 JSON 加载农场持有参数（BK Evolution）。
    _fhp_json = DataLoader.load_farm_holding_params()
    if _fhp_json:
        if "farm_holding_dict_i18n" in _fhp_json:
            farm_holding_dict = {k: __(v) for k, v in _fhp_json["farm_holding_dict_i18n"].items()}
        if "farm_ttip_i18n" in _fhp_json:
            farm_ttip = {k: __(v) for k, v in _fhp_json["farm_ttip_i18n"].items()}
        if "farm_holding_stats" in _fhp_json:
            farm_holding_stats = {k: tuple(v) for k, v in _fhp_json["farm_holding_stats"].items()}
        if "farm_holding_tags" in _fhp_json:
            farm_holding_tags = _fhp_json["farm_holding_tags"]

    ## EN: Load minion parameters from JSON (BK Evolution).
    ## ZH: 从 JSON 加载仆从参数（BK Evolution）。
    _mp_json = DataLoader.load_minion_params()
    if _mp_json:
        if "minion_adjectives" in _mp_json:
            minion_adjectives = _mp_json["minion_adjectives"]
        if "minion_name_dict" in _mp_json:
            minion_name_dict = _mp_json["minion_name_dict"]

    girl_name_dict = {"syllabs" : ["sha", "she", "shee", "shi", "wa", "ri", "ree", "ra", "ru", "ti", "ta", "ty", "ya", "yu", "sa", "so", "su", "se", "sy", "da", "de", "di", "do", "dy", "fa", "fe", "fio", "fia", "gi", "hu", "ha", "hyu", "ja", "ju", "ji", "ka", "ky", "ki", "kyo", "kyu", "la", "li", "le", "lo", "lu", "lyu", "lia", "lya", "lee", "loo", "za", "zi", "zu", "ze", "zee", "xa", "xy", "xe", "ca", "ce", "chi", "chu", "va", "vi", "vy", "ve", "bu", "be", "na", "ne", "ni", "nya", "nyu", "nee", "ma", "mu", "me", "mi", "myu", "mia", "mya"],
                      "fillers" : ["n", "r", "l", "s", "'", "", "", ""],
                      "enders" : ["n", "l", "nn", "a", "ya", "na", "ly", "", "", ""],
                      "last_syllabs" : ["jo", "sho", "to", "ya", "ma", "mi", "yo", "ko", "na", "ye", "yu", "ka", "ta", "fu", "ro", "sa", "shi", "ki", "no", "ra", "re", "tsu", "chi", "shi", "se", "n", "mu", "ne", "kyo", "ku"],
                      }

    ## EN: Load girl name pools from JSON (BK Evolution).
    ## ZH: 从 JSON 加载女孩名字池（BK Evolution）。
    _gnp_json = DataLoader.load_girl_name_pools()
    if _gnp_json and "girl_name_dict" in _gnp_json:
        girl_name_dict = _gnp_json["girl_name_dict"]


    ## FEAR POWERS AND MOJO

    NORMAL_MOJO_VALUE = 7.5 # Gain 1 purple mojo for each x amounts of fear raised (regular interactions)
    FARM_MOJO_VALUE = 2.5 # Gain 1 coloured mojo for each x amounts of fear raised (farm interactions)

    mojo_act_dict = {
                "naked": ("green",),
                "service": ("green",),
                "sex": ("blue",),
                "anal": ("red",),
                "fetish": ("yellow",),
                "group": ("blue", "red"),
                "bisexual": ("yellow",),
                "sensitivity": ("green",),
                "libido": ("blue",),
                "constitution": ("red",),
                "obedience": ("yellow",),
                }

    ## CITY MERCHANTS

    ## POPULATIONS & ENCOUNTERS ##
    # Loaded from JSON (BK Evolution)

    _enc_json = DataLoader.load_encounters()
    if _enc_json:
        if "pop_name_dict_i18n" in _enc_json:
            pop_name_dict = {k: tuple(__(v) for v in vals) for k, vals in _enc_json["pop_name_dict_i18n"].items()}
        if "encounters" in _enc_json:
            def _to_tuple(val):
                if isinstance(val, list):
                    return tuple(_to_tuple(v) for v in val)
                return val
            encounters = tuple(_to_tuple(v) for v in _enc_json["encounters"])
        if "encounter_pics" in _enc_json:
            def _to_tuple(val):
                if isinstance(val, list):
                    return tuple(_to_tuple(v) for v in val)
                return val
            encounter_pics = {k: _to_tuple(v) for k, v in _enc_json["encounter_pics"].items()}
    else:
        pop_name_dict = {}
        encounters = ()
        encounter_pics = {}


    ## WEEK DAYS / CALENDAR / COLORS
    # EN: Loaded from JSON (BK Evolution).
    # ZH: 从 JSON 加载日历与颜色常量（BK Evolution）。
    _gc_json = DataLoader.load_game_constants()
    if _gc_json:
        weekdays = tuple(_gc_json.get("weekdays", []))
        workshift_color = {int(k): v for k, v in _gc_json.get("workshift_color", {}).items()}
        MC_class_index = _gc_json.get("MC_class_index", {})
        roman_numbers = {int(k): v for k, v in _gc_json.get("roman_numbers", {}).items()}
    else:
        weekdays = ()
        workshift_color = {}
        MC_class_index = {}
        roman_numbers = {}

    ## JOBS and SEX ACTS
    # EN: Loaded from JSON (BK Evolution).
    # ZH: 从 JSON 加载（BK Evolution）。
    _job_json = DataLoader.load_job_params()
    if _job_json:
        all_jobs = _job_json.get("all_jobs", [])
        all_sex_acts = _job_json.get("all_sex_acts", [])
        extended_sex_acts = _job_json.get("extended_sex_acts", [])
        farm_hardcore_acts = _job_json.get("farm_hardcore_acts", [])
        opposite_sex_acts = {(None if k == "null" else k): v for k, v in _job_json.get("opposite_sex_acts", {}).items()}
        normal_tags = tuple(_job_json.get("normal_tags", []))
        all_farm_tags = tuple(_job_json.get("all_farm_tags", []))
        job_sort_value = {(None if k == "null" else k): v for k, v in _job_json.get("job_sort_value", {}).items()}
        job_color = {(None if k == "null" else k): v for k, v in _job_json.get("job_color", {}).items()}
    else:
        all_jobs = []
        all_sex_acts = []
        extended_sex_acts = []
        farm_hardcore_acts = []
        opposite_sex_acts = {}
        normal_tags = ()
        all_farm_tags = ()
        job_sort_value = {}
        job_color = {}


    ## STAT NAMES (SKILLS) — JSON-driven (BK Evolution) ##
    import json as _json, os as _os
    _stats_path = _os.path.join(renpy.config.gamedir, "core", "data", "stats", "stats.json")
    _stats_data = {}
    if _os.path.exists(_stats_path):
        with open(_stats_path, 'r', encoding='utf-8') as _f:
            _stats_data = _json.load(_f)
        del _f

    gstats_main = [__(s) for s in _stats_data.get("main_stats", ["Charm", "Beauty", "Body", "Refinement", "Sensitivity", "Libido", "Constitution", "Obedience"])]
    gstats_sex = [__(s) for s in _stats_data.get("sex_stats", ["Service", "Sex", "Anal", "Fetish"])]
    all_skills = [s.lower() for s in gstats_main + gstats_sex]

    ## STAT DESCRIPTION ##
    _sd = _stats_data.get("stat_descriptions", {})
    gstats_dict = {k: __(v) for k, v in _sd.items()}

    _ssd = _stats_data.get("stat_short_descriptions", {})
    gstats_descript = {k: __(v) for k, v in _ssd.items()}

    _sjs = _stats_data.get("stat_job_skills", {})
    gstat_job_skill = {k: __(v) for k, v in _sjs.items()}

    _msc = _stats_data.get("mc_stat_colors", {})
    MC_stat_color = {k: v for k, v in _msc.items()}

    _pc = _stats_data.get("preference_colors", {})
    preference_color = {k: v for k, v in _pc.items()}
    preference_color[None] = _pc.get(None, "%s")


    ## WORLD MAP (BK Evolution) ##
    active_world_map = None

    ## GIRL PERSONALITIES ##
    # EN: Load personality and gift parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载人格与礼物参数（BK Evolution）。
    _pers_gift_json = DataLoader.load_personality_gift_params()
    if _pers_gift_json:
        alignment_bonus = _pers_gift_json.get("alignment_bonus", {})
        personality_attributes = [tuple(x) for x in _pers_gift_json.get("personality_attributes", [])]
        attribute_score_dict = _pers_gift_json.get("attribute_score_dict", {})
        gpersonalities_likes = _pers_gift_json.get("gpersonalities_likes", {})
        _gc = _pers_gift_json.get("gpersonalities_comment", {})
        gpersonalities_comment = {k: tuple(__(x) for x in v.get("comments_i18n", [])) for k, v in _gc.items()}
    else:
        alignment_bonus = {}
        personality_attributes = []
        attribute_score_dict = {}
        gpersonalities_likes = {}
        gpersonalities_comment = {}

init python:
    ## GIRL PERSONALITIES — JSON-driven (BK Evolution) ##
    _pers_path = _os.path.join(renpy.config.gamedir, "core", "data", "personalities", "personalities.json")
    _pers_data = []
    if _os.path.exists(_pers_path):
        with open(_pers_path, 'r', encoding='utf-8') as _f:
            _pers_data = _json.load(_f)
        del _f

    gpersonalities = {}
    for _pers_item in _pers_data:
        _pid = _pers_item.get("id")
        if not _pid:
            continue
        gpersonalities[_pid] = Personality(
            name=get_i18n(_pers_item, "name", _pid),
            attributes=tuple(_pers_item.get("attributes", [])),
            description=get_i18n(_pers_item, "description", ""),
            often_stories=_pers_item.get("often_stories", []),
            rarely_stories=_pers_item.get("rarely_stories", []),
            never_stories=_pers_item.get("never_stories", []),
            dialogue_personality_weight=_pers_item.get("dialogue_personality_weight", 3),
            dialogue_attribute_weight=_pers_item.get("dialogue_attribute_weight", 1),
        )

    reserved_personality_names = gpersonalities.keys()

    # EN: Load sex training parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载性训练参数（BK Evolution）。
    _sex_train_json = DataLoader.load_sex_training_params()
    if _sex_train_json:
        base_reluctance = _sex_train_json.get("base_reluctance", {})
        preference_modifier = _sex_train_json.get("preference_modifier", {})
        preference_limit = _sex_train_json.get("preference_limit", {})
        experienced_modifiers = _sex_train_json.get("experienced_modifiers", {})
        experienced_color = _sex_train_json.get("experienced_color", {})
        sexual_training_value = _sex_train_json.get("sexual_training_value", {})
    else:
        base_reluctance = {}
        preference_modifier = {}
        preference_limit = {}
        experienced_modifiers = {}
        experienced_color = {}
        sexual_training_value = {}

    # Training prerequisites loaded from JSON (BK Evolution)

    _train_json = DataLoader.load_training_tests()
    if _train_json:
        def _to_tuples(val):
            if isinstance(val, list):
                return [tuple(x) for x in val]
            return val
        if "training_test_dict" in _train_json:
            training_test_dict = {k: _to_tuples(v) for k, v in _train_json["training_test_dict"].items()}
        if "magic_training_test_dict" in _train_json:
            magic_training_test_dict = {k: _to_tuples(v) for k, v in _train_json["magic_training_test_dict"].items()}
    else:
        training_test_dict = {}
        magic_training_test_dict = {}

    ## MC interactions
    # The dictionary uses nested lists to retain choices order

    interact_dict = {
                    "chat" : ["GENERAL TOPICS", "PERSONAL TOPICS", "STORY"],
                    "GENERAL TOPICS" : [GirlInteractionTopic("chat", "chat", __("Life as a slave"), "slave_chat_slave_life"),
                                        GirlInteractionTopic("chat", "chat", __("Life in the brothel"), "slave_chat_brothel", condition="has_worked"),
                                        GirlInteractionTopic("chat", "chat", __("Getting along with customers"), "slave_chat_customers", condition="has_worked"),
                                        GirlInteractionTopic("chat", "chat", __("Getting along with other girls"), "slave_chat_other_girls", condition="other_girls"),
                                        ],
                    "PERSONAL TOPICS" : [
                                        GirlInteractionTopic("chat", "chat", __("Her well-being"), "slave_chat_well_being"),
                                        GirlInteractionTopic("chat", "chat", __("Her feelings about you"), "slave_chat_feelings"),
                                        GirlInteractionTopic("chat", "chat", __("Her tastes"), "slave_chat_tastes"),
                                        GirlInteractionTopic("chat", "chat", __("Her origins"), "slave_chat_origins"),
                                    ],
                    "STORY" : [GirlInteractionTopic("chat", "story", __("Hear her story again"), "slave_chat_story", AP_cost=0, condition="story")],

                    "train" : ["SKILL TRAINING", "SEXUAL TRAINING", "SPECIAL TRAINING"],
                    "SKILL TRAINING" : [GirlInteractionTopic("train", "train", __("Obedience training"), "slave_train_obedience", act="obedience"),
                                        GirlInteractionTopic("train", "train", __("Constitution training"), "slave_train_constitution", act="constitution")],
                    "SEXUAL TRAINING" : [
                                        GirlInteractionTopic("train", "train", __("Naked"), "slave_train_sex_acts", act="naked", advanced=True),
                                        GirlInteractionTopic("train", "train", __("Service"), "slave_train_sex_acts", act="service", advanced=True),
                                        GirlInteractionTopic("train", "train", __("Sex"), "slave_train_sex_acts", act="sex", advanced=True),
                                        GirlInteractionTopic("train", "train", __("Anal"), "slave_train_sex_acts", act="anal", advanced=True),
                                        GirlInteractionTopic("train", "train", __("Fetish"), "slave_train_sex_acts", act="fetish", advanced=True),
                                        GirlInteractionTopic("train", "train", __("Bisexual"), "slave_train_sex_acts", act="bisexual", advanced=True),
                                        GirlInteractionTopic("train", "train", __("Group"), "slave_train_sex_acts", act="group", advanced=True),
                                    ],
                    "SPECIAL TRAINING" : [GirlInteractionTopic("train", "train", __("Free-form training"), "slave_train_free_form", condition="free-form"),
                                          GirlInteractionTopic("train", "train", __("Remove negative fixation"), "slave_remove_fixation", condition="neg_fix")],

                    "magic" : ["MAGIC SKILL TRAINING {image=img_gold}", "MAGIC SEXUAL TRAINING {image=img_gold}", "MAGIC SKILL TRAINING {image=img_MP}", "MAGIC SEXUAL TRAINING {image=img_MP}", "CHOOSE METHOD"],

                    "CHOOSE METHOD" : [GirlInteractionTopic("magic", None, __("Current method"), "slave_hypnotize_method", AP_cost=0), GirlInteractionTopic("magic", None, "Spend", "slave_hypnotize_driver", AP_cost=0)], # None type excludes it from girl interaction count

                    "MAGIC SKILL TRAINING {image=img_gold}" : [
                                                GirlInteractionTopic("magic", "train", __("Obedience training"), "slave_magic", act="obedience", gold_cost=20, condition="gold_driver"),
                                                GirlInteractionTopic("magic", "train", __("Sensitivity training"), "slave_magic", act="sensitivity", gold_cost=20, condition="gold_driver"),
                                                GirlInteractionTopic("magic", "train", __("Libido training"), "slave_magic", act="libido", gold_cost=20, condition="gold_driver"),
                                                ],
                    "MAGIC SEXUAL TRAINING {image=img_gold}" : [
                                                GirlInteractionTopic("magic", "train", __("Naked"), "slave_magic", act="naked", advanced=True, gold_cost=20, condition="gold_driver"),
                                                GirlInteractionTopic("magic", "train", __("Service"), "slave_magic", act="service", advanced=True, gold_cost=40, condition="gold_driver"),
                                                GirlInteractionTopic("magic", "train", __("Sex"), "slave_magic", act="sex", advanced=True, gold_cost=50, condition="gold_driver"),
                                                GirlInteractionTopic("magic", "train", __("Anal"), "slave_magic", act="anal", advanced=True, gold_cost=60, condition="gold_driver"),
                                                GirlInteractionTopic("magic", "train", __("Fetish"), "slave_magic", act="fetish", advanced=True, gold_cost=70, condition="gold_driver"),
                                                GirlInteractionTopic("magic", "train", __("Bisexual"), "slave_magic", act="bisexual", advanced=True, gold_cost=80, condition="gold_driver"),
                                                GirlInteractionTopic("magic", "train", __("Group"), "slave_magic", act="group", advanced=True, gold_cost=100, condition="gold_driver"),
                                                ],

                    "MAGIC SKILL TRAINING {image=img_MP}" : [
                                                GirlInteractionTopic("magic", "train", __("Obedience training"), "slave_magic", act="obedience", MP_cost=1, condition="mana_driver"),
                                                GirlInteractionTopic("magic", "train", __("Sensitivity training"), "slave_magic", act="sensitivity", MP_cost=1, condition="mana_driver"),
                                                GirlInteractionTopic("magic", "train", __("Libido training"), "slave_magic", act="libido", MP_cost=1, condition="mana_driver"),
                                                ],
                    "MAGIC SEXUAL TRAINING {image=img_MP}" : [
                                                GirlInteractionTopic("magic", "train", __("Naked"), "slave_magic", act="naked", advanced=True, MP_cost=1, condition="mana_driver"),
                                                GirlInteractionTopic("magic", "train", __("Service"), "slave_magic", act="service", advanced=True, MP_cost=2, condition="mana_driver"),
                                                GirlInteractionTopic("magic", "train", __("Sex"), "slave_magic", act="sex", advanced=True, MP_cost=3, condition="mana_driver"),
                                                GirlInteractionTopic("magic", "train", __("Anal"), "slave_magic", act="anal", advanced=True, MP_cost=3, condition="mana_driver"),
                                                GirlInteractionTopic("magic", "train", __("Fetish"), "slave_magic", act="fetish", advanced=True, MP_cost=4, condition="mana_driver"),
                                                GirlInteractionTopic("magic", "train", __("Bisexual"), "slave_magic", act="bisexual", advanced=True, MP_cost=4, condition="mana_driver"),
                                                GirlInteractionTopic("magic", "train", __("Group"), "slave_magic", act="group", advanced=True, MP_cost=5, condition="mana_driver"),
                                                ],

                    "react" : ["ENCOURAGE", "DISCIPLINE"],
                    "ENCOURAGE" : [
                                    GirlInteractionTopic("react", "reward", __("Praise her"), "slave_reward_praise"),
                                    GirlInteractionTopic("react", "reward", __("Give her gold"), "slave_reward_gold"),
                                    GirlInteractionTopic("react", "reward", __("Give her a gift"), "slave_reward_gift"),
                                    GirlInteractionTopic("react", "reward", __("Pet her"), "slave_reward_pet"),
                                    GirlInteractionTopic("react", "reward", __("Give her a day off"), "slave_reward_day"),
                                    GirlInteractionTopic("react", "reward", __("Have sex with her"), "slave_reward_sex"),
                                    ],
                    "DISCIPLINE" : [
                                    GirlInteractionTopic("react", "discipline", __("Scold her"), "slave_punish_scold"),
                                    GirlInteractionTopic("react", "discipline", __("Remove upkeep"), "slave_punish_upkeep"),
                                    GirlInteractionTopic("react", "discipline", __("Force her to go naked"), "slave_punish_naked", condition="dressed"),
                                    GirlInteractionTopic("react", "discipline", __("Beat her"), "slave_punish_beat"),
                                    GirlInteractionTopic("react", "discipline", __("Rape her"), "slave_punish_rape"),
                                    GirlInteractionTopic("react", "discipline", __("Send her to the farm"), "slave_punish_farm", condition="farm"),
                                    ],
                    "misc" : ["CLOTHING", "CUSTOMERS", "MASTER BEDROOM", "DEBUG"],
                    "CLOTHING" : [
                                    GirlInteractionTopic("misc", None, __("Tell her to go naked"), "slave_clothing_naked", AP_cost=0, condition="can_undress"),
                                    GirlInteractionTopic("misc", None, __("Tell her to get dressed"), "slave_clothing_dressed", AP_cost=0, condition="naked"),
                                    ],
                    "CUSTOMERS" : [
                                    GirlInteractionTopic("misc", None, __("Forbid sex acts during job"), "slave_forbid_cust_events", AP_cost=0, condition="!forbid customer sex"),
                                    GirlInteractionTopic("misc", None, __("Allow sex acts during job"), "slave_allow_cust_events", AP_cost=0, condition="forbid customer sex"),
                                    ],
                    "MASTER BEDROOM" : [
                                        GirlInteractionTopic("misc", None, __("Send her to your bedroom"), "slave_master_bedroom_add", AP_cost=0, condition="master_bedroom_add"),
                                        GirlInteractionTopic("misc", None, __("Remove her from your bedroom"), "slave_master_bedroom_remove", AP_cost=0, condition="master_bedroom_remove")
                                        ],
                    "DEBUG" : [GirlInteractionTopic("misc", None, __("Cheat"), "interaction_cheat_menu", AP_cost=0, condition="debug_mode"),
                        GirlInteractionTopic("misc", None, __("Reset girl interactions"), "interaction_cheat_girl", AP_cost=0, condition="debug_mode"),
                        GirlInteractionTopic("misc", None, __("Reset MC interactions"), "interaction_cheat_MC", AP_cost=0, condition="debug_mode"),
                        GirlInteractionTopic("misc", None, __("Reveal Personality"), "interaction_cheat_personality", AP_cost=0, condition="debug_mode"),
                        ],
                    }


    free_interact_dict = {
                            "chat" : ["GENERAL TOPICS", "PERSONAL TOPICS", "DEBUG"],
                            "GENERAL TOPICS" : [GirlInteractionTopic("chat", "chat", __("Small talk"), "free_chat_small_talk"),
                                                GirlInteractionTopic("chat", "chat", __("Gossip"), "free_chat_gossip"),
                                                GirlInteractionTopic("chat", "chat", __("Life"), "free_chat_life"),# love_test=5),
                                                GirlInteractionTopic("chat", "chat", __("Love"), "free_chat_love"),# love_test=5),
                                                ],
                            "PERSONAL TOPICS" : [
                                                GirlInteractionTopic("chat", "chat", __("Her origins"), "free_chat_origins", love_test=10),
                                                GirlInteractionTopic("chat", "chat", __("Her hobbies"), "free_chat_hobbies", love_test=10),
                                                GirlInteractionTopic("chat", "chat", __("Likes"), "free_chat_likes", love_test=10),
                                                GirlInteractionTopic("chat", "chat", __("Dislikes"), "free_chat_dislikes", love_test=10),
                                                ],
                            "fun" : ["JOKE", "TOUCH", "PLAY"],
                            "JOKE" : [
                                        GirlInteractionTopic("fun", "joke", __("Harmless"), "free_joke_harmless", love_test=15),
                                        GirlInteractionTopic("fun", "joke", __("Adult"), "free_joke_adult", love_test=15),
                                        GirlInteractionTopic("fun", "joke", __("Dark"), "free_joke_dark", love_test=15),
                                        GirlInteractionTopic("fun", "joke", __("Mean"), "free_joke_mean", love_test=15),
                                        ],
                            "TOUCH" : [
                                        GirlInteractionTopic("fun", "touch", __("Hold her hand"), "free_touch_hand", love_test=40),
                                        GirlInteractionTopic("fun", "touch", __("Kiss"), "free_touch_kiss", relationship_level=2),
                                        GirlInteractionTopic("fun", "touch", __("Slap her ass"), "free_touch_ass", love_test=55, relationship_level=3),
                                        GirlInteractionTopic("fun", "touch", __("Touch her breasts"), "free_touch_breasts", love_test=60, relationship_level=3),
                                        GirlInteractionTopic("fun", "touch", __("Touch her pussy"), "free_touch_pussy", love_test=65, relationship_level=3),
                                        ],
                            "PLAY" : [
                                        GirlInteractionTopic("fun", "play", __("Get her naked"), "free_play", act="naked", relationship_level=4),
                                        GirlInteractionTopic("fun", "play", __("Ask for service"), "free_play", act="service", relationship_level=4),
                                        GirlInteractionTopic("fun", "play", __("Ask for sex"), "free_play", act="sex", relationship_level=4),
                                        GirlInteractionTopic("fun", "play", __("Ask for anal sex"), "free_play", act="anal", relationship_level=4),
                                        GirlInteractionTopic("fun", "play", __("Ask for fetish"), "free_play", act="fetish", relationship_level=4),
                                        ],
                            "flirt" : ["COMPLIMENT", "SEXUAL TOPICS"],

                            "COMPLIMENT" : [
                                        GirlInteractionTopic("flirt", "compliment", __("Compliment her beauty"), "free_flirt_beauty", relationship_level=1),
                                        GirlInteractionTopic("flirt", "compliment", __("Compliment her body"), "free_flirt_body", relationship_level=1),
                                        GirlInteractionTopic("flirt", "compliment", __("Compliment her mind"), "free_flirt_mind", relationship_level=1),
                                        GirlInteractionTopic("flirt", "compliment", __("Compliment her spirit"), "free_flirt_spirit", relationship_level=1),
                                        ],
                            "SEXUAL TOPICS" : [
                                                GirlInteractionTopic("flirt", "chat about sex", __("Her sexual experience"), "free_flirt_sex_experience", love_test=55),
                                                GirlInteractionTopic("flirt", "chat about sex", __("Her sexual tastes"), "free_flirt_sex_tastes", love_test=55),
                                                GirlInteractionTopic("flirt", "chat about sex", __("Nudity"), "free_flirt_sex_act", act="naked", love_test=55),
                                                GirlInteractionTopic("flirt", "chat about sex", __("Service"), "free_flirt_sex_act", act="service", love_test=55),
                                                GirlInteractionTopic("flirt", "chat about sex", __("Sex"), "free_flirt_sex_act", act="sex", love_test=55),
                                                GirlInteractionTopic("flirt", "chat about sex", __("Anal sex"), "free_flirt_sex_act", act="anal", love_test=55),
                                                GirlInteractionTopic("flirt", "chat about sex", __("Fetish acts"), "free_flirt_sex_act", act="fetish", love_test=55),
                                                GirlInteractionTopic("flirt", "chat about sex", __("Bisexuality"), "free_flirt_sex_act", act="bisexual", love_test=55),
                                                GirlInteractionTopic("flirt", "chat about sex", __("Group sex"), "free_flirt_sex_act", act="group", love_test=55),
                                                ],
                            "give" : ["GIVE", "OFFER"],
                            "GIVE" : [
                                        GirlInteractionTopic("give", "gift", __("Give her a present"), "free_give_gift", love_test=20),
                                        GirlInteractionTopic("give", "gold", __("Give her money"), "free_give_gold", love_test=20),
                                        ],
                            "OFFER" : [GirlInteractionTopic("give", "offer", __("Offer her a job"), "free_offer_job", love_test=90, relationship_level=5),],
                            "DEBUG" : [GirlInteractionTopic("give", None, __("Change love"), "interaction_cheat_love", AP_cost=0, condition="debug_mode"),
                                        GirlInteractionTopic("give", None, __("Reset girl interactions"), "interaction_cheat_girl", AP_cost=0, condition="debug_mode"),
                                        GirlInteractionTopic("give", None, __("Reset MC interactions"), "interaction_cheat_MC", AP_cost=0, condition="debug_mode"),
                                        GirlInteractionTopic("give", None, __("Reveal Personality"), "interaction_cheat_personality", AP_cost=0, condition="debug_mode"),
                                        ],
                    }

    fix_description = {
                    "public acts description" : __("doing it in public."),
                    "public acts action" : __("Do it in public"),
                    "public acts intro" : __("You call in everyone from the brothel: girls, helpers, passersby... You tell %s that she must do it in public."),
                    "public acts pos_reaction" : __("She blushes and you can see her nipples perking under her blouse. She is aroused by the thought of doing it in public."),
                    "public acts neg_reaction" : __("She is indignant and complains that she can't do anything when people are watching. You ignore her."),

                    "cosplay description" : __("wearing sexy and revealing outfits."),
                    "cosplay action" : __("Wear a sexy outfit"),
                    "cosplay intro" : __("You give %s a choice of uniforms she can wear."),
                    "cosplay pos_reaction" : __("She bites her lip, looking playful. She chooses a kinky uniform with holes for her tits, pussy and asshole."),
                    "cosplay neg_reaction" : __("She chooses a rather conservative and boring uniform. She doesn't enjoy having to wear it."),

                    "dildos description" : __("using sex toys while fucking."),
                    "dildos action" : __("Use a dildo"),
                    "dildos intro" : __("You tell %s to use a dildo in her other hole while you're fucking her."),
                    "dildos pos_reaction" : __("She easily slips the dildo in place. It looks like something she is used to doing a lot."),
                    "dildos neg_reaction" : __("She hates it as she has to painfully force the dildo in. She doesn't enjoy it at all."),

                    "vibrators description" : __("vibrators."),
                    "vibrators action" : __("Use a vibrator"),
                    "vibrators intro" : __("You tell %s to use a vibrating egg while doing it."),
                    "vibrators pos_reaction" : __("She wastes no time in using the egg on her ready clit, bringing herself to a state of heavy arousal."),
                    "vibrators neg_reaction" : __("She is sensitive and uncomfortable using the egg, and complains that it feels weird."),

                    "dirty sex description" : __("dirty sex"),
                    "dirty sex action" : __("Get down and dirty"),
                    "dirty sex intro" : __("You tell %s to get down in the dirt and get ready to be abused."),
                    "dirty sex pos_reaction" : __("She seems happy to be on the ground, like a dirty bitch she is."),
                    "dirty sex neg_reaction" : __("She hates dirt and complains that it is unhealthy."),

                    "penis worship description" : __("worshiping dicks, especially large ones."),
                    "penis worship action" : __("Make her rub your dick"),
                    "penis worship intro" : __("You tell %s that she has to rub oil on your dick and pay it proper respect."),
                    "penis worship pos_reaction" : __("She takes a good look at your large, throbbing cock and seems happy and aroused that she can play with it. She plants a wet kiss right on the tip."),
                    "penis worship neg_reaction" : __("She looks away from your erect dick, still uncomfortable around a man's cock."),

                    "bondage description" : __("being tied up."),
                    "bondage action" : __("Tie her up"),
                    "bondage intro" : __("Using tight ropes and your expert knowledge of bondage as a slave master, you tie %s up in an uncomfortable and embarrassing position."),
                    "bondage pos_reaction" : __("She moans with pleasure as you tie her up, loving the feel of the ropes biting her skin."),
                    "bondage neg_reaction" : __("She cries and squirms as you tie her up, feeling extremely uncomfortable."),

                    "oil description" : __("being oiled-up."),
                    "oil action" : __("Oil her up"),
                    "oil intro" : __("You give %s a bottle of body oil, insisting that she spreads it all over her naked body."),
                    "oil pos_reaction" : __("She oils up every nook and cranny of her body for your pleasure, playfully massaging her glistening skin while you watch."),
                    "oil neg_reaction" : __("She isn't comfortable with slippery and oily stuff, complaining that it stinks and feels revolting."),

                    "wet description" : __("being wet."),
                    "wet action" : __("Get her wet"),
                    "wet intro" : __("You ask Sill to fetch you a bucket of cold water, which you pour straight on %s's body."),
                    "wet pos_reaction" : __("She loves being wet and moist, moaning as she slips her hands all over her body."),
                    "wet neg_reaction" : __("She looks upset and miserable like a wet kitty. She hates water."),

                    "submission description" : __("taking a humiliating pose."),
                    "submission action" : __("Humiliate her"),
                    "submission intro" : __("You tell %s to get on her knees and beg for what's going to happen."),
                    "submission pos_reaction" : __("She eagerly obeys your order, taking perverse pleasure in begging for you to abuse her."),
                    "submission neg_reaction" : __("She refuses to beg and complains that it is beneath her."),

                    "femdom description" : __("dominating her partner."),
                    "femdom action" : __("Let her dominate"),
                    "femdom intro" : __("You tell %s to take the lead and dominate this encounter."),
                    "femdom pos_reaction" : __("She is pleased to be given the leading role. She perversely enjoys giving orders and dominating her partner."),
                    "femdom neg_reaction" : __("She hesitates, then awkwardly tries to give an order in an unconvincing voice. She almost immediately reverses herself and apologises. She doesn't enjoy taking the lead at all."),

                    "gags description" : __("being gagged while having sex."),
                    "gags action" : __("Gag her"),
                    "gags intro" : __("You order %s to wear a large ball gag, which leaves her mouth open at all times and makes it hard to talk."),
                    "gags pos_reaction" : __("She seems oddly happy and excited as she puts on the gag and gives you a sheepish look."),
                    "gags neg_reaction" : __("Unable to control her drooling and hardly able to talk, she gives you a furious look. She seems to hate it."),

                    "strap-ons description" : __("fucking girls with a strap-on."),
                    "strap-ons action" : __("Use a strap-on"),
                    "strap-ons intro" : __("You tell %s to fuck Sill using a strap-on dildo."),
                    "strap-ons pos_reaction" : __("She looks triumphant as she puts on a huge black strap-on dildo, with one end up in her pussy and the other dangling in front of her. Sill gasps."),
                    "strap-ons neg_reaction" : __("She grumbles as she puts it on, complaining that she isn't a man."),

                    "roleplay description" : __("playing a role while fucking."),
                    "roleplay action" : __("Make her play a role"),
                    "roleplay intro" : __("You tell %s that you are going to play roles: you are the city guard and she is a captured thief."),
                    "roleplay pos_reaction" : __("She enjoys the idea of role-playing and makes a great show of being a repentant horny thief."),
                    "roleplay neg_reaction" : __("She thinks it's stupid and distracting and doesn't get into it at all."),

                    "plugs description" : __("wearing a plug inside her ass."),
                    "plugs action" : __("Use anal plug"),
                    "plugs intro" : __("Taking out a large, glistening rubber plug, you tell %s to insert it in her ass."),
                    "plugs pos_reaction" : __("She pushes the plug deep inside her ready asshole with delight, moaning seductively."),
                    "plugs neg_reaction" : __("She inserts the plug with great difficulty, ashamed and in pain. It makes her very uncomfortable."),

                    "enemas description" : __("getting an enema."),
                    "enemas action" : __("Use an enema"),
                    "enemas intro" : __("You tell %s it's time to clean up."),
                    "enemas pos_reaction" : __("As you insert the enema into her asshole and start filling her up with water, she begs you to go further and further. Soon, her belly is inflated and rounded like a balloon."),
                    "enemas neg_reaction" : __("She cries with shame and horror as you fill her insides with cleansing water. She begs you to stop."),

                    "beads description" : __("wearing anal beads."),
                    "beads action" : __("Use anal beads"),
                    "beads intro" : __("You give %s a bead necklace and explain what she should do with it."),
                    "beads pos_reaction" : __("She pushes the beads into her asshole one by one, clearly enjoying it and moaning as you watch."),
                    "beads neg_reaction" : __("She cringes and whines as she painfully pushes one or two beads inside her ass. She tells you she hates it."),

                    "masturbation description" : __("masturbating."),
                    "masturbation action" : __("Make her masturbate"),
                    "masturbation intro" : __("You tell %s to play with herself while doing it."),
                    "masturbation pos_reaction" : __("She enthusiastically starts playing with her clit and fingering her pussy while you watch her."),
                    "masturbation neg_reaction" : __("She pretends to masturbate but isn't doing anything. She doesn't enjoy it at all."),

                    "fingering description" : __("being fingered."),
                    "fingering action" : __("Slide a finger inside her"),
                    "fingering intro" : __("You tell %s you will put your fingers inside her."),
                    "fingering pos_reaction" : __("Her pussy welcomes you as you slide, one, then two, then three fingers inside her with ease. She moans with pleasure as you increase your pace, covering your fingers with her love juices."),
                    "fingering neg_reaction" : __("Her pussy contracts and resists you as you push a single finger inside with great difficulty. Tears run down her face: she isn't enjoying this at all."),

                    "handjobs description" : __("giving handjobs."),
                    "handjobs action" : __("Give a handjob"),
                    "handjobs intro" : __("You order %s to give you a good handjob."),
                    "handjobs pos_reaction" : __("She loves rubbing her hands up and down your dick, watching your throbbing, hard cock with fascination."),
                    "handjobs neg_reaction" : __("She is mechanical and unenthusiastic. She doesn't like handjobs."),

                    "cunnilingus description" : __("cunnilingus."),
                    "cunnilingus action" : __("Cunnilingus"),
                    "cunnilingus intro" : __("You go down between %s's legs and spread her pussy lips."),
                    "cunnilingus pos_reaction" : __("She moans wildly as you move your tongue deep inside her. Her love juices splash out, betraying her pleasure."),
                    "cunnilingus neg_reaction" : __("She frowns and tries to close her legs, not feeling it. It seems like cunnilingus is not her thing."),

                    "oral description" : __("giving oral."),
                    "oral action" : __("Oral sex"),
                    "oral intro" : __("You tell %s to use her tongue and mouth to increase the pleasure."),
                    "oral pos_reaction" : __("She loves licking and sucking her partner, and she makes sure to make eye contact with you as she does it."),
                    "oral neg_reaction" : __("She gags at the taste and looks annoyed. She doesn't like giving oral."),

                    "irrumatio description" : __("irrumatio."),
                    "irrumatio action" : __("Irrumatio"),
                    "irrumatio intro" : __("Ordering %s to lay flat with her head hanging from the bed, you decide to fuck her mouth hard."),
                    "irrumatio pos_reaction" : __("You shove your dick as deep and hard as you can into her mouth-pussy, and she takes it all in, seemingly enjoying having her throat raped."),
                    "irrumatio neg_reaction" : __("She gags and coughs and cries and squirms, hating it, but you force-fuck her throat anyway."),

                    "deep throat description" : __("deep throat."),
                    "deep throat action" : __("Deep-throat"),
                    "deep throat intro" : __("You tell %s to get ready to deep-throat you."),
                    "deep throat pos_reaction" : __("She has no gag reflexes and enjoys sucking your dick as far down her throat as she can."),
                    "deep throat neg_reaction" : __("She gags and almost throws up, begging you to stop. You ignore her."),

                    "titjobs description" : __("giving titjobs."),
                    "titjobs action" : __("Give a titjob"),
                    "titjobs intro" : __("You order %s to use her tits to pleasure you."),
                    "titjobs pos_reaction" : __("She wraps your dick completely between her gorgeous tits, licking the tip as she slides her soft mounds up and down your cock."),
                    "titjobs neg_reaction" : __("She awkwardly tries to use her tits to rub your dick, but she is clumsy and uninterested."),

                    "footjobs description" : __("giving footjobs."),
                    "footjobs action" : __("Give a foot job"),
                    "footjobs intro" : __("You order %s to use her legs and feet to rub your dick."),
                    "footjobs pos_reaction" : __("She loves playing with your dick with her feet, giving you a good upskirt view as she brings you to your limit."),
                    "footjobs neg_reaction" : __("She hates it, only managing to crush your cock with her clumsy feet. You tell her to stop."),

                    "double penetration description" : __("being fucked in both holes."),
                    "double penetration action" : __("Double penetration"),
                    "double penetration intro" : __("You ask one of your security guys to join you and %s, telling him to fuck her ass as you take the front."),
                    "double penetration pos_reaction" : __("She screams wildly as she gets both her front and back holes raped by fat dicks. She loves it."),
                    "double penetration neg_reaction" : __("She is upset and bothered that two dicks are in her at the same time. It seems to be too much for her."),

                    "fisting description" : __("being fisted."),
                    "fisting action" : __("Fist her"),
                    "fisting intro" : __("Telling %s not to move, you decide to play around with her pussy using your bare fist."),
                    "fisting pos_reaction" : __("She squeals with pleasure as you rape her wet pussy with your fist, eventually sending her into a massive squirting orgasm."),
                    "fisting neg_reaction" : __("She screams with pain and begs you to stop as your fist bends her pussy in unnatural ways. She hates it."),

                    "insults description" : __("being insulted."),
                    "insults action" : __("Insult her"),
                    "insults intro" : __("You call %s names as you force her to perform, using language that would make a harbor whore blush."),
                    "insults pos_reaction" : __("She seems to love being trashed and insulted, and after only a minute, you notice that she has got completely wet."),
                    "insults neg_reaction" : __("She is shocked and unnerved by your words, unable to concentrate on what she's doing. It isn't helping."),

                    "69 description" : __("69."),
                    "69 action" : __("Do a 69"),
                    "69 intro" : __("You tell %s to get into a 69 position."),
                    "69 pos_reaction" : __("She loves 69 and enjoys herself tremendously as she tends to her partner while her pussy gets licks."),
                    "69 neg_reaction" : __("She looks unhappy as she seems to despise that position. In the end, it isn't enjoyable for anyone."),

                    "watersports description" : __("watersports."),
                    "watersports action" : __("Play watersports"),
                    "watersports intro" : __("You tell %s to get ready for some 'watersports'."),
                    "watersports pos_reaction" : __("She loves peeing in front of people and being peed on. She doesn't find it shameful."),
                    "watersports neg_reaction" : __("She is disgusted by bodily fluids and recoils with horror at the thought."),

                    "ass-to-mouth description" : __("ass-to-mouth."),
                    "ass-to-mouth action" : __("Go ass-to-mouth"),
                    "ass-to-mouth intro" : __("You decide to fuck %s in the ass before moving to her mouth."),
                    "ass-to-mouth pos_reaction" : __("She accepts your dick readily and licks it clean for you, not caring that it was in her ass a second ago."),
                    "ass-to-mouth neg_reaction" : __("She retches as you push your dick into her mouth, complaining that it is dirty and disgusting."),

                    "kissing description" : __("kissing."),
                    "kissing action" : __("Kiss her"),
                    "kissing intro" : __("You start kissing %s."),
                    "kissing pos_reaction" : __("She responds enthusiastically to your kiss, mingling her tongue with yours. She doesn't let go until the very end."),
                    "kissing neg_reaction" : __("She tries to avoid you and doesn't seem to enjoy kissing at all. She is relieved when you stop."),

                    "spanking description" : __("spanking."),
                    "spanking action" : __("Spank her"),
                    "spanking intro" : __("You tell %s that she's been a bad girl, and that she is going to get spanked hard."),
                    "spanking pos_reaction" : __("She screams with pain and pleasure, crying tears of happiness as you give her a thorough spanking while fucking her."),
                    "spanking neg_reaction" : __("You spank her and fuck her at the same time. She wriggles and tries to escape you, moaning in pain. She doesn't like it."),

                    "rimming description" : __("rimming."),
                    "rimming action" : __("Rimming"),
                    "rimming intro" : __("You tell %s to lick your asshole thoroughly."),
                    "rimming pos_reaction" : __("She is very serious about licking you clean, pushing her tongue into your ass as she gives you a frantic handjob."),
                    "rimming neg_reaction" : __("She is disgusted by the act and only timidly licks around your asshole. It tickles, but doesn't feel good in any way."),

                    "fondling her boobs description" : __("being fondled."),
                    "fondling her boobs action" : __("Fondle her boobs"),
                    "fondling her boobs intro" : __("You fondle her tits and play with her nipples as %s performs for you."),
                    "fondling her boobs pos_reaction" : __("She loves it when you squeeze her tits and moans sexily as you rub her erect nipples."),
                    "fondling her boobs neg_reaction" : __("She doesn't like to be touched there and tenses up, making the training less enjoyable."),

                    "groping her ass description" : __("being groped."),
                    "groping her ass action" : __("Grope her ass"),
                    "groping her ass intro" : __("You grope her ass and start fingering her asshole as %s performs for you."),
                    "groping her ass pos_reaction" : __("She loves to be touched and groped and moans hornily as you shove two fingers up her butthole."),
                    "groping her ass neg_reaction" : __("She doesn't like to be touched there and tenses up, making the training less enjoyable."),

                    "lactation description" : __("lactation."),
                    "lactation action" : __("Milk her"),
                    "lactation intro" : __("Groping %s's boobs, you take out a syringe filled with a strange liquid and plunge it into her nipple."),
                    "lactation pos_reaction" : __("She gasps with astonishment as her tits grow larger in size. Soon, she begins to lactate uncontrollably, moaning as you milk her large breasts for all they're worth."),
                    "lactation neg_reaction" : __("She yells and cries with pain as her boobs grow heavier and larger. The experience is too traumatic, however, and she fails to give you any milk."),

                    "doggy style description" : __("doggy style."),
                    "doggy style action" : __("Doggy style"),
                    "doggy style intro" : __("Pushing her on all fours, you start fucking %s from behind."),
                    "doggy style pos_reaction" : __("She moans with pleasure as the length of your shaft runs along her most sensitive parts. She cannot get enough of it."),
                    "doggy style neg_reaction" : __("She grinds her teeth as she waits for you to be finished. She doesn't enjoy that position at all."),

                    "cowgirl description" : __("cowgirl style."),
                    "cowgirl action" : __("Cowgirl style"),
                    "cowgirl intro" : __("You make %s ride your dick."),
                    "cowgirl pos_reaction" : __("She likes to be on top and lovingly bounces on your dick until you both get close to your limit."),
                    "cowgirl neg_reaction" : __("She doesn't like to be on top and stays passive as you fuck her from below."),

                    "piledriver description" : __("piledriver."),
                    "piledriver action" : __("Piledriver"),
                    "piledriver intro" : __("Pushing %s on her back and lifting her legs in the air, you plunge your hard dick inside her."),
                    "piledriver pos_reaction" : __("She is overwhelmed with lust and pleasure as the blood flows to her head while you pound her mercilessly."),
                    "piledriver neg_reaction" : __("She is confused and bothered by this new position, telling you she doesn't like it at all."),

                    "spooning description" : __("spooning."),
                    "spooning action" : __("Spooning"),
                    "spooning intro" : __("Hugging %s from behind, you slowly slide into her while caressing her body."),
                    "spooning pos_reaction" : __("She loves being cradled and fucked at the same time. She relaxes completely, moaning softly, soon ready to reach orgasm."),
                    "spooning neg_reaction" : __("She stays passive as you fuck her from behind, looking bored."),

                    "bukkake description" : __("bukkake."),
                    "bukkake action" : __("Bukkake"),
                    "bukkake intro" : __("Calling a group of your security guards, you let them watch as you and Sill fuck %s. They start jerking off while watching her. As you reach your limit, you pull out and cum all over her face, quickly followed by the other men."),
                    "bukkake pos_reaction" : __("She shakes with a massive orgasm as she experiences a shower of cum on her face, hair and body. She gorges up on leftover cum from everyone's dick."),
                    "bukkake neg_reaction" : __("She tries to get away and whines as everyone cums on her face and hair. She bitterly complains about the smell and taste."),

                    "cum in mouth description" : __("cum in her mouth."),
                    "cum in mouth action" : __("Cum in her mouth"),
                    "cum in mouth intro" : __("You decide to use %s's mouth for a big finish."),
                    "cum in mouth pos_reaction" : __("She looks entranced as you unload a wad of semen into her ready mouth. She plays with it on her tongue, enjoying the taste and texture."),
                    "cum in mouth neg_reaction" : __("You cum a lot in her mouth, sending her into a fit of coughing. She spits it all out, complaining."),

                    "cum on face description" : __("cumshots."),
                    "cum on face action" : __("Cum on her face"),
                    "cum on face intro" : __("Popping your dick out, you shoot a load of semen all over %s's face."),
                    "cum on face pos_reaction" : __("She sighs happily as she receives load after load of your cum. She uses her hands to spread the cum all over her face, then licks her fingers."),
                    "cum on face neg_reaction" : __("She recoils with disgust as you shoot your load. She rushes to get a wet cloth and clean it up."),

                    "cum in hair description" : __("cum in her hair."),
                    "cum in hair action" : __("Cum in her hair"),
                    "cum in hair intro" : __("Popping your dick out, you decide to cum all over %s's soft, silky hair."),
                    "cum in hair pos_reaction" : __("She moans as you wrap her hair around your dick and squeeze every last drop on her scalp. She enjoys being treated like a dirty cum dump."),
                    "cum in hair neg_reaction" : __("She yells awfully as you shoot a load of semen on her hair, whining that it's gonna take ages to get it off."),

                    "cum on body description" : __("cum on her body."),
                    "cum on body action" : __("Cum on her body"),
                    "cum on body intro" : __("You decide to cum all over %s's body."),
                    "cum on body pos_reaction" : __("She reaches her climax as you take out your dick and spill a load of white cum all over her soft skin."),
                    "cum on body neg_reaction" : __("She squirms as you shoot cum all over her body, complaining that it is sticky and smelly."),

                    "cum shower description" : __("getting showered with cum."),
                    "cum shower action" : __("Shower her with cum"),
                    "cum shower intro" : __("Popping a special pill from the spice market, your dick starts bulging, ready to burst with huge amounts of cum. You tell %s to lay down and get ready to receive your seed."),
                    "cum shower pos_reaction" : __("You cum and cum buckets, until she is covered with white, sticky semen. She is enthralled by the sensation."),
                    "cum shower neg_reaction" : __("She squeals and cowers in fear as you cum buckets all over her body, disgusted by the smell and feel."),

                    "swallowing description" : __("swallowing cum."),
                    "swallowing action" : __("Make her swallow"),
                    "swallowing intro" : __("Shoving your dick deep into %s's mouth for the big finish, you shoot loads of cum deep down her throat."),
                    "swallowing pos_reaction" : __("She gulps it all down with gusto, squeezing every last drop of cum out of your throbbing dick. She licks her lips sexily when you are finished."),
                    "swallowing neg_reaction" : __("She gets tearful and gags, trying to spit it all out as you shoot load after load. She only partly succeeds, and looks unhappy at having to drink cum."),

                    "creampie description" : __("receiving a creampie."),
                    "creampie action" : __("Creampie"),
                    "creampie intro" : __("Taking your dick slowly out of %s, you shoot a thick load of white cum all over her ass and pussy."),
                    "creampie pos_reaction" : __("She shakes with a massive orgasm as you spurt cum all over her holes. She seems to love it."),
                    "creampie neg_reaction" : __("She covers her face and begs you to stop, saying that it's creepy and disgusting."),

                    "cum inside description" : __("cum inside her."),
                    "cum inside action" : __("Cum inside"),
                    "cum inside intro" : __("Not caring about the consequences, you decide to cum deep inside %s."),
                    "cum inside pos_reaction" : __("She reaches a blinding orgasm, moaning wildly as you unload a wad of cum deep inside her."),
                    "cum inside neg_reaction" : __("She screams for you to get out, but you ignore her, smearing her insides with thick, sticky cum. She cries with shame and disgust."),

                    "multiple orgasms description" : __("having multiple orgasms."),
                    "multiple orgasms action" : __("Give her multiple orgasms"),
                    "multiple orgasms intro" : __("Rubbing her clit with one hand, you keep the pace up until %s cannot but shake with a shattering orgasm. Giving her no moment to rest, you increase the build-up until she comes another time, and another time."),
                    "multiple orgasms pos_reaction" : __("She loves it and loses her mind completely over the sensations washing over her, looking nothing but an obedient, adoring slave by the time you are finished."),
                    "multiple orgasms neg_reaction" : __("She feels overtly sensitive and begs you to stop, almost in pain from excessive climaxing. She doesn't like it."),

                    "denied orgasm description" : __("being denied orgasm."),
                    "denied orgasm action" : __("Deny her orgasm"),
                    "denied orgasm intro" : __("You decide to tease %s to the limit, not letting her reach climax."),
                    "denied orgasm pos_reaction" : __("She seems to love being teased and indefinitely denied orgasm, becoming incredibly horny and sensitive over time."),
                    "denied orgasm neg_reaction" : __("She screams with frustration and begs you to let her climax. She is upset that you won't let her."),

                    "squirting description" : __("squirting."),
                    "squirting action" : __("Make her squirt"),
                    "squirting intro" : __("Pushing your hand inside %s's pussy, you start rubbing the walls of her pussy, looking for her sensitive G-spot. She looks overwhelmed by the sensation."),
                    "squirting pos_reaction" : __("She squirts hard, showering the room with her juice. She climaxes so hard that she can't even move afterwards."),
                    "squirting neg_reaction" : __("She feels weird and gross, and begs you to take your hand out. She isn't into it at all."),

                    "stripping description" : __("stripping."),
                    "stripping action" : __("Make her strip"),
                    "stripping intro" : __("Telling %s to remove her clothes slowly and sexily, you look on as she does what she's told."),
                    "stripping pos_reaction" : __("She moans as she feels the caress of her clothing rubbing against her soft skin. Looking straight into your eyes, she slowly removes her underwear last, inch by inch, making sure to give you a good show."),
                    "stripping neg_reaction" : __("Whining and bitching, she reluctantly takes off her clothes, hiding her private parts in embarrassment. She looks angry and shameful."),

                    }

    fix_dict = {
                "stripping" : Fixation("stripping", acts=("naked", "sex", "bisexual"), step=1, attribute="modest", tag_list=(["strip"], ["naked", "dancer"])),
                "public acts" : Fixation("public acts", acts=("naked", "service", "sex", "group"), step=1, attribute="extravert", tag_list=(["public"]), not_list=["rest"]), # Location tags are allowed but display special flavor text
                "cosplay" : Fixation("cosplay", acts=("naked", "fetish", "bisexual"), step=1, attribute="extravert", tag_list=(["cosplay"], ["maid", "kimono"], ["swim", "waitress", "dancer"]), not_list=["naked"], cannot_have_neg=["roleplay"]),
                "dildos" : Fixation("dildos", acts=("sex", "anal", "bisexual"), step=1, attribute="introvert", tag_list=(["dildo"], ["toy"],)),
                "vibrators" : Fixation("vibrators", acts=("naked", "fetish", "bisexual"), step=1, attribute="introvert", tag_list=(["vibrator"], ["toy"],)),
                "dirty sex" : Fixation("dirty sex", acts=("sex", "fetish", "group"), step=1, attribute="sub", tag_list=(["dirty"],)),
                "penis worship" : Fixation("penis worship", acts=("service", "group"), step=1, attribute="sub", tag_list=(["handjob", "big"], ["service", "big"], ["handjob"],), cannot_have_neg=["handjob"]),
                "bondage" : Fixation("bondage", acts=("fetish", "naked"), step=1, attribute="sub", tag_list=(["bondage"],)),
                "oil" : Fixation("oil", acts=("group", "anal"), step=1, attribute="extravert", tag_list=(["wet"],)),
                "wet" : Fixation("wet", acts=("naked", "sex", "bisexual"), step=1, attribute="extravert", tag_list=(["wet"],)),
                "submission" : Fixation("submission", acts=("service", "fetish", "bisexual"), step=1, attribute="sub", tag_list=(["sub"],)),
                "femdom" : Fixation("femdom", acts=("bisexual", "sex", "service"), step=1, attribute="dom", tag_list=(["dom"],)),
                "gags" : Fixation("gags", acts=("fetish", "naked"), step=1, attribute="introvert", tag_list=(["gag"], ["bondage"],)),
                "strap-ons" : Fixation("strap-ons", acts=("bisexual", "group"), step=1, attribute="dom", tag_list=(["strap-on"], ["lesbian"], ["toy"],)),
                "roleplay" : Fixation("roleplay", acts=("naked", "sex", "fetish"), step=1, attribute="extravert", tag_list=(["cosplay"], ["maid", "kimono"], ["swim", "waitress", "dancer"]), cannot_have_neg=["cosplay"]),
                "plugs" : Fixation("plugs", acts=("naked", "anal"), step=1, attribute="modest", tag_list=(["plug"], ["toy"],)),
                "enemas" : Fixation("enemas", acts=("group", "anal"), step=1, attribute="materialist", tag_list=(["enema"], ["toy"],)),
                "beads" : Fixation("beads", acts=("anal"), step=1, attribute="introvert", tag_list=(["beads"], ["toy"],)),

                "masturbation" : Fixation("masturbation", acts=("service", "naked", "sex"), step=2, attribute="extravert", tag_list=(["mast"], ["naked"],)),
                "fingering" : Fixation("fingering", acts=("naked", "fetish", "bisexual", "group"), step=2, attribute="lewd", tag_list=(["finger"],)),
                "handjobs" : Fixation("handjobs", acts=("service", "group"), step=2, attribute="modest", tag_list=(["handjob"],)),
                "cunnilingus" : Fixation("cunnilingus", acts=("service", "bisexual"), step=2, attribute="introvert", tag_list=(["cunnilingus"],["finger"])),
                "oral" : Fixation("oral", acts=("service", "bisexual", "group"), step=2, tag_list=(["oral"],)),
                "irrumatio" : Fixation("irrumatio", acts=("fetish"), step=2, attribute="sub", tag_list=(["deep"], ["oral"],)),
                "deep throat" : Fixation("deep throat", acts=("service", "group"), step=2, attribute="sub", tag_list=(["deep"], ["oral"],), cannot_have_neg=["oral"]),
                "titjobs" : Fixation("titjobs", acts=("service", "group"), step=2, attribute="extravert", tag_list=(["titjob"],)),
                "footjobs" : Fixation("footjobs", acts=("service", "fetish"), step=2, attribute="dom", tag_list=(["footjob"],)),
                "double penetration" : Fixation("double penetration", acts=("group"), step=2, attribute="lewd", tag_list=(["double"],)),
                "fisting" : Fixation("fisting", acts=("fetish", "bisexual", "anal"), step=2, attribute="lewd", tag_list=(["fist"], ["finger"])),
                "insults" : Fixation("insults", acts=("fetish", "naked"), step=2, attribute="sub", tag_list=(["sub"],)),
                "69" : Fixation("69", acts=("service", "bisexual"), step=2, attribute="dom", tag_list=(["69"], ["oral"],), cannot_have_neg=["oral"]),
                "watersports" : Fixation("watersports", acts=("fetish", "sex"), step=2, attribute="sub", tag_list=(["watersports"], ["squirt"],)),
                "ass-to-mouth" : Fixation("ass-to-mouth", acts=("anal", "group"), step=2, attribute="sub", tag_list=(["cim"], ["oral"],), cannot_have_neg=["oral"]),
                "kissing" : Fixation("kissing", acts=("naked", "sex", "bisexual"), step=2, attribute="idealist", tag_list=(["kiss"],)),
                "spanking" : Fixation("spanking", acts=("fetish", "anal"), step=2, attribute="sub", tag_list=(["spank"], ["sub"],)),
                "rimming" : Fixation("rimming", acts=("service", "fetish"), step=2, attribute="sub", tag_list=(["rim"],)),
                "fondling her boobs" : Fixation("fondling her boobs", short_name = "fondling", acts=("naked", "sex", "bisexual", "group"), step=2, tag_list=(["fondle"],)),
                "groping her ass" : Fixation("groping her ass", short_name = "groping", acts=("naked", "anal", "bisexual", "group"), step=2, tag_list=(["grope"],)),
                "lactation" : Fixation("lactation", acts=("naked", "fetish"), step=2, attribute="extravert", tag_list=(["lactation"], ["titjob"],)),
                "doggy style" : Fixation("doggy style", acts=("sex", "anal"), step=2, attribute="lewd", tag_list=(["doggy"],)),
                "cowgirl" : Fixation("cowgirl", acts=("sex", "anal"), step=2, attribute="dom", tag_list=(["cowgirl"],)),
                "piledriver" : Fixation("piledriver", acts=("sex", "anal"), step=2, attribute="materialist", tag_list=(["piledriver"],)),
                "spooning" : Fixation("spooning", acts=("sex", "anal"), step=2, attribute="idealist", tag_list=(["spoon"],)),

                "bukkake" : Fixation("bukkake", acts=("bisexual", "group"), step=3, attribute="lewd", tag_list=(["buk"], ["cof"], ["cumshot"],), cannot_have_neg=["cum shower"]),
                "cum in mouth" : Fixation("cum in mouth", acts=("service", "anal", "bisexual"), step=3, attribute="lewd", tag_list=(["cim"], ["oral"],), cannot_have_neg=["oral"]),
                "cum on face" : Fixation("cum on face", acts=("service", "sex", "fetish"), step=3, attribute="sub", tag_list=(["cof"], ["buk"], ["cumshot"],)),
                "cum in hair" : Fixation("cum in hair", acts=("service", "fetish"), step=3, attribute="sub", tag_list=(["cih", "coh"], ["cof", "buk"], ["cumshot"],)),
                "cum on body" : Fixation("cum on body", acts=("sex", "anal", "service"), step=3, attribute="dom", tag_list=(["cob"], ["cumshot"],)),
                "cum shower" : Fixation("cum shower", acts=("bisexual", "group"), step=3, attribute="sub", tag_list=(["cum shower"], ["cob", "cih"], ["cumshot"],), cannot_have_neg=["bukkake"]),
                "swallowing" : Fixation("swallowing", acts=("service", "fetish"), step=3, attribute="materialist", tag_list=(["cim"], ["deep"], ["oral"],), cannot_have_neg=["oral", "cum in mouth"]),
                "creampie" : Fixation("creampie", acts=("sex", "anal", "group"), step=3, attribute="extravert", tag_list=(["creampie"], ["cin"],)),
                "cum inside" : Fixation("cum inside", acts=("sex", "anal"), step=3, attribute="introvert", tag_list=(["cin"], ["creampie"],)),
                "multiple orgasms" : Fixation("multiple orgasms", acts=("group", "bisexual"), step=3, attribute="lewd", tag_list=(["orgasm"],)),
                "denied orgasm" : Fixation("denied orgasm", acts=("anal", "fetish", "bisexual"), step=3, attribute="sub", tag_list=(["denied"],)),
                "squirting" : Fixation("squirting", acts=("service", "sex", "bisexual"), step=3, attribute="extravert", tag_list=(["squirt"], ["watersport", "orgasm"],)),
                }


    ## PERKS AND ARCHETYPES ##
init -4 python:
    # EN: Load archetype data from JSON (BK Evolution).
    # ZH: 从 JSON 加载天赋原型数据（BK Evolution）。
    _arch_json = DataLoader.load_archetype_data()
    if _arch_json:
        archetype_list = _arch_json.get("archetype_list", [])
        archetype_description = {k: __(v) for k, v in _arch_json.get("archetype_description", {}).items()}
    else:
        archetype_list = []
        archetype_description = {}

    ## GIRL BACKGROUND ##

    # EN: Load random pools for girl background generation from JSON (BK Evolution).
    # ZH: 从 JSON 加载女孩背景生成随机池（BK Evolution）。
    _bgp_json = DataLoader.load_girl_background_pools()
    if _bgp_json:
        slave_stories = _bgp_json.get("slave_stories", [])
        homes = _bgp_json.get("homes", [])
        guardians = _bgp_json.get("guardians", [])
        hobbies = _bgp_json.get("hobbies", [])
        colors = _bgp_json.get("colors", [])
        food = _bgp_json.get("food", [])
        drinks = _bgp_json.get("drinks", [])
    else:
        slave_stories = []
        homes = []
        guardians = []
        hobbies = []
        colors = []
        food = []
        drinks = []

    origins = ["Zan", "the border with the Holy Lands", "the Blood Islands", "Karkyr", "Westmarch", "the desert of Hokoma", "Borgo, the port city", "the Goliath desolations", "the Arik mountains"]

#     origin_description = {
#                           "Zan" : __("I know the old streets of Zan like the back of my hand... I used to walk to the market with my %s, wondering what the strange houses with the red lanterns were... Now I know... *blush*"),
#                           "the border with the Holy Lands" : __("The Holy Lands are a place of war and suffering, always have been. Still, I remember a few peaceful moments. Walking with my %s across old battlefields, covered with red blooming flowers, watching nature reclaim its rights..."),
#                           "the Blood Islands" : __("The Blood Islands are a cruel place... I remember going to the arena with my %s and me, watching slaves being shredded to pieces by monsters... It was bloody and exciting. The arena here is very tame in comparison."),
#                           "Karkyr" : __("Karkyr is a beautiful and fascinating city, ruled by the Archmage Council. Everything is magical, even the wells and the furniture can speak. It used to freak my %s out! There were also some spectacular incidents, of course, but that was part of the fun."),
#                           "Westmarch" : __("The Westmarch Principalities, where I grew up, is a very unpredictable place. One day a city is flourishing, the next it descends into anarchy, and raiders loot and rape the town. I used to think danger was exciting, but my %s didn't like it one bit."),
#                           "the desert of Hokoma" : __("The desert people are a quiet and wise sort. My %s know many secrets, and knew how to keep them. I miss the peace and quiet of nights in the desert."),
#                           "Borgo, the port city" : __("There's no describing how busy and crowded Borgo is on most days, with sailors from all over the world selling everything you can imagine, and many other things, too. I loved to sit by the pier with my %s in the early hours, listenning to the waves."),
#                           "the Goliath desolations" : __("The desolations are a cold, horrible place. Whether you are rich or poor, you have to work hard every day, just to barely survive. If I didn't have my %s to rely on, I don't know what I would have done."),
#                           "the Arik mountains" : __("They say the Arik mountains are the highest in the world. The air is pure there, not full of filth and magic like here... My %s taught me how to love and respect the mountains."),
#                           }

    ## MC interact counters ##


    ## MC interact counters ##

#    MC_interact_counters = {
#                            "chat" : 0, "gossip" : 0, "life" : 0, "love" : 0,
#                            "origins" : 0, "hobbies" : 0, "likes" : 0, "dislikes" : 0,
#                            "harmless" : 0, "adult" : 0, "dark" : 0, "mean" : 0,
#                            "present" : 0, "money" : 0,
#                            "beauty" : 0, "body" : 0, "mind" : 0, "spirit" : 0,
#                            "hand" : 0, "kiss" : 0, "ass" : 0, "breasts" : 0, "pussy" : 0,
#                            "service" : 0, "sex" : 0, "anal" : 0, "fetish" : 0,
#                            "offer" : 0,
#                            "well_being" : 0, "happiness" : 0, "job" : 0,
#                            "scold" : 0, "threaten" : 0, "beat" : 0, "torture" : 0,
#                            "charm_obedience" : 0, "charm_sensitivity" : 0, "charm_libido" : 0, "charm_love" : 0, "charm_fear" : 0
#                            }

    result_colors = {"very bad" : c_red, "bad" : c_lightred, "average" : c_white, "good" : c_lightgreen, "very good" : c_green, "perfect" : c_orange}
    result_star_dict = {"very bad" : "{image=img_empty_star}"*5, "bad" : "{image=img_star}"+"{image=img_empty_star}"*4, "average" : "{image=img_star}"*2+"{image=img_empty_star}"*3, "good" : "{image=img_star}"*3+"{image=img_empty_star}"*2, "very good" : "{image=img_star}"*4+"{image=img_empty_star}", "perfect" : "{image=img_star}"*5}

#    result_names = {v: k for k, v in result_value.items()}
#    roll_names = {v: k for k, v in roll_value.items()}

    # <MIGRATED: see data/jobs.rpy>

    stat_increase_dict = {
                        "level" : __("\n{color=[c_lightgreen]}LEVEL UP{/color}"),
                        "stat" : __("\n%s {color=[c_green]}+%s{/color}"),
                        "stat_neg" : __("\n%s {color=[c_red]}%s{/color}"),
                        "xp" : __("\nXP {color=[c_lightgreen]}+%s{/color}"),
                        "xp_dark" : __("\nXP {color=[c_darkgreen]}+%s{/color}"),
                        "jp" : __("\nJP {color=[c_orange]}+%s{/color}"),
                        "gold+" : __("\nGold {color=[c_darkgold]}+%s{/color}"),
                        "gold-" : __("\nGold {color=[c_darkgold]}%s{/color}"),
                        "rep" : __("\nRep. {color=[c_softpurple]}+%s{/color}"),
                        "rep_neg" : __("\nRep. {color=[c_red]}%s{/color}"),
                        "job_up" : __("\n{color=[c_orange]}JOB SKILL UP{/color}"),
                        "rank" : __("\n{color=[c_softpurple]}NEW RANK AVAILABLE{/color}")
                    }

    # makes text bold
    btext = "{b}%s{/b}"

    # Contrast colors are for lighter backgrounds
    event_color = {None : __("%s")}

    for k in color_dict.keys():
        event_color[k] = "{color=" + color_dict[k] + "}%s{/color}"

    #### ITEMS ####

    #### QUESTS & CLASSES ####

    ## PRICES ##
    # Loaded from JSON (BK Evolution)

    _qp_json = DataLoader.load_quest_prices()
    if _qp_json:
        if "quest_base_gold" in _qp_json:
            quest_base_gold = _qp_json["quest_base_gold"]
        if "class_prices" in _qp_json:
            class_prices = {int(k): v for k, v in _qp_json["class_prices"].items()}
    else:
        quest_base_gold = {}
        class_prices = {}

    ## CLASS PREFIXES ##

    #### MODIFIERS ####

    ## PRICE MODIFIERS ##

    # EN: Load economy modifiers from JSON (BK Evolution).
    # ZH: 从 JSON 加载经济修正参数（BK Evolution）。
    _econ_json = DataLoader.load_economy_modifiers()
    if _econ_json:
        price_modifiers = _econ_json.get("price_modifiers", {})
        stat_bonus = {k: tuple(v) for k, v in _econ_json.get("stat_bonus", {}).items()}
        roll_modifier = _econ_json.get("roll_modifier", {})
        helper_cost = {int(k): v for k, v in _econ_json.get("helper_cost", {}).items()}
    else:
        price_modifiers = {}
        stat_bonus = {}
        roll_modifier = {}
        helper_cost = {}

    # max_upkeep = {
    #             1 : 75,
    #             2 : 250,
    #             3 : 500,
    #             4 : 1000,
    #             5 : 2000
    #             }



## XP and RANK ##


    ## LEVEL UP / RANKS / JOB POINTS
    # EN: Loaded from JSON (BK Evolution).
    # ZH: 从 JSON 加载等级、晋升与职业点参数（BK Evolution）。
    _xp_json = DataLoader.load_xp_rank_params()
    if _xp_json:
        xp_to_levelup = {int(k): v for k, v in _xp_json.get("xp_to_levelup", {}).items()}
        MC_xp_to_levelup = {int(k): v for k, v in _xp_json.get("MC_xp_to_levelup", {}).items()}
        rank_cost = {int(k): v for k, v in _xp_json.get("rank_cost", {}).items()}
        rank_stat_step = {int(k): tuple(v) for k, v in _xp_json.get("rank_stat_step", {}).items()}
        jp_result_modifier = _xp_json.get("jp_result_modifier", {})
        jp_customer_rank_modifier = {int(k): v for k, v in _xp_json.get("jp_customer_rank_modifier", {}).items()}
        jp_job_level_modifier = {int(k): v for k, v in _xp_json.get("jp_job_level_modifier", {}).items()}
    else:
        xp_to_levelup = {}
        MC_xp_to_levelup = {}
        rank_cost = {}
        rank_stat_step = {}
        jp_result_modifier = {}
        jp_customer_rank_modifier = {}
        jp_job_level_modifier = {}

    ## RANKS / JOB POINTS — JSON-driven (BK Evolution) ##
    _ranks_path = _os.path.join(renpy.config.gamedir, "core", "data", "ranks", "ranks.json")
    _ranks_data = {}
    if _os.path.exists(_ranks_path):
        with open(_ranks_path, 'r', encoding='utf-8') as _f:
            _ranks_data = _json.load(_f)
        del _f

    _rn = _ranks_data.get("rank_names", {})
    rank_name = {int(k) if str(k).lstrip('-').isdigit() else k: __(v) for k, v in _rn.items()}

    _jtl = _ranks_data.get("jp_to_level", {})
    jp_to_level = {int(k): v for k, v in _jtl.items()}

    _jud = _ranks_data.get("job_up_dict", {})
    job_up_dict = {k: tuple(v) for k, v in _jud.items()}

    _juc = _ranks_data.get("job_up_change", {})
    job_up_change = {int(k): tuple(v) for k, v in _juc.items()}

    _rtr = _ranks_data.get("rep_to_rank", {})
    rep_to_rank = {int(k): v for k, v in _rtr.items()}

    _rgd = _ranks_data.get("rep_gains_dict", {})
    rep_gains_dict = {int(k): {sk: __(sv) for sk, sv in svdict.items()} for k, svdict in _rgd.items()}

    _rld = _ranks_data.get("rep_loss_dict", {})
    rep_loss_dict = {int(k): {sk: __(sv) for sk, sv in svdict.items()} for k, svdict in _rld.items()}

#     rep_gains_dict = {
#                      1 : 6, # average score or better raises reputation
#                      2 : 6, # average score or better raises reputation
#                      3 : 9, # good score or better raises reputation
#                      4 : 9, # good score or better raises reputation
#                      5 : 12 # very good or better score raises reputation
#                      6 : 15 # perfect score raises reputation
#                      }

#     rep_loss_dict = {
#                      1 : -1, # very bad score damages reputation
#                      2 : -1, # very bad score damages reputation
#                      3 : 5, # bad score or lower damages reputation
#                      4 : 5, # bad score or lower damages reputation
#                      5 : 8 # average score or lower damages reputation
#                      }

    # (rank_cost, rank_stat_step, jp_* loaded from JSON above)



#### TRANSFORMS/EFFECTS ####

init:

    transform blink(_duration=0.5, _pause=2.0):
        on start:
            alpha 1.0
            linear _duration alpha 0.0
            linear _duration alpha 1.0
            pause _pause
            repeat

    transform myalpha(a):
            alpha a

    transform totheleft:
        xalign 0.2
        yalign 1.0

    transform totheright:
        xalign 0.8
        yalign 1.0

    transform centertextbox:
        xalign 0.5
        yanchor 1.0
        ypos 0.8

    transform centerleft:
        xalign 0.0
        yalign 0.5

    transform centerright:
        xalign 1.0
        yalign 0.5

    transform move_to(start_pos=(0,0), new_pos=(0,0), duration=0.6, fades=0.0): # Default: fades after moving

        pos start_pos xanchor 0.5 yanchor 1.0

        ease duration pos new_pos xanchor 0.5

        linear .5 alpha fades

    transform ninja_move:

        xanchor 0.0 yanchor 0.5

        xalign 0.75 yalign 0.4

        choice:
            ease 0.33 xalign 0.8 yalign 0.45

        choice:
            ease 0.33 xalign 0.7 yalign 0.45

        choice:
            ease 0.33 xalign 0.8 yalign 0.35

        choice:
            ease 0.33 xalign 0.7 yalign 0.35

        ease 0.33 xalign 0.75 yalign 0.4

        repeat

    transform fly_off(x=0.5, y=1.0):
        xalign x
        yalign y
        matrixtransform RotateMatrix(0.0, 0.0, 0.0)
        easein 2.0 xalign x+1.0 ypos y-1.0 matrixtransform RotateMatrix(0.0, 0.0, 1440.0) zoom 0.25


    transform rotate_y: # 3D y axis rotation
        matrixtransform RotateMatrix(0.0, 0.0, 0.0)
        ease 3.0 matrixtransform RotateMatrix(0.0, 360.0, 0.0)
        repeat

    transform disappear_in(s):
        pause s
        alpha 0

    transform flip_to_back:
        perspective True
        subpixel True
        matrixtransform RotateMatrix(0, 0, 0)
        linear 0.8 matrixtransform RotateMatrix(0, -180, 0)

    transform reverse_horizontal:
        subpixel True
        zpos 1
        matrixtransform RotateMatrix(0, 180, 0)

    transform jitter(start_pos=(0.5, 0.5), adj=0.005, t=0.4):
        ease t zoom 1.0 # align start_pos  matrixtransform RotateMatrix(0.0, 0.0, 0.0)
        ease t zoom 0.92 # align randomize_align(adj) matrixtransform RotateMatrix(*randomize_matrix())
        repeat

    transform bounce(start_pos=(0.5, 0.5), adj=0.005, t=0.4):
        zoom 1.0
        ease t zoom 1.25 # align randomize_align(adj) matrixtransform RotateMatrix(*randomize_matrix())
        ease t zoom 0.92 # align start_pos  matrixtransform RotateMatrix(0.0, 0.0, 0.0)

    transform repeat_bounce():
        zoom 1.0
        linear 1.0 zoom 0.8
        linear 0.5 zoom 1.0
        repeat

    transform shake(t=0.4, degrees=15):
        rotate 0
        ease t rotate degrees
        ease t rotate -degrees
        ease t rotate 0
        repeat

    transform flip:
        xzoom -1.0

    $ quake = Move((0, 20), (20, -15), 0.05+renpy.random.random()*.15, bounce=True, repeat=True, delay=1.0)

    $ define.move_transitions("smove", 2.0)

    transform jumping:
        linear 0.1 yoffset -50
        linear 0.1 yoffset 0

    transform fadeinout(y_offset=0):
        xanchor 0.0
        yanchor 0.0
        xpos 1.0
        ypos 0 + y_offset
        alpha 0.0
        ease 2.5 xalign 1.0 alpha 1.0
        pause 2.0
        ease 2.5 xalign 1.5 alpha 0.0

    transform fademove(from_tup, to_tup): # Moves from coordinates from_tup to to_tup while fading

        on show:
            xanchor 0.5
            yanchor 0.5
            xalign from_tup[0]
            yalign from_tup[1]

            pause 1.0

            ease 1.5  xalign to_tup[0] yalign to_tup[1] alpha 0.0

    transform burn_card(xs, ys):

        pause 0.3

        AlphaMask(Frame("resources/transitions/flames.webp", xsize=xs, ysize=ys), Frame("resources/ui/powers/cards/front_Bronze.webp", xsize=xs, ysize=ys))
        alpha 0.0
        linear 0.8 alpha 1.0


    # Speed
    image speed_effect:
        im.Scale("resources/transitions/speed.webp", config.screen_width, config.screen_height)
        xpan 180
        xalign 0
        yalign 0
        linear 0.5 xpan -180
        xalign 0
        yalign 0
        repeat

    # Rain
    # image rev_lightning = im.Flip("resources/minigame/rain/lightning.webp", horizontal=True)
    image rev_lightning = Transform("resources/minigame/rain/lightning.webp", xzoom = -1.0) # updated transform (Dexell)

    image rain:
        zoom 2.0

        "resources/minigame/rain/heavyrain1.webp"
        0.1
        "resources/minigame/rain/rain1.webp"
        0.1
        "resources/minigame/rain/heavyrain2.webp"
        0.1
        "resources/minigame/rain/rain3.webp"
        0.1
        "resources/minigame/rain/rain2.webp"
        0.1
        "resources/minigame/rain/heavyrain3.webp"
        0.1
        repeat

    image lightning:
        zoom 3.0
        yalign 0.0

        choice:   #weight of choice is 0.1
            "resources/minigame/rain/lightning.webp" with vpunch
            xalign 0.0
            alpha  0.0
            linear 0.6 alpha  1.0
            linear 0.6 alpha  0.0

        choice:
            "rev_lightning" with vpunch
            xalign 1.0
            alpha  0.0
            linear 0.6 alpha  1.0
            linear 0.6 alpha  0.0

        repeat

    image static:
        "noise1" with Dissolve(0.3, alpha=True)
        0.3
        "noise2" with Dissolve(0.2, alpha=True)
        0.2
        "noise3" with Dissolve(0.4, alpha=True)
        0.4
        "noise4" with Dissolve(0.1, alpha=True)
        0.1
        "noise1" with Dissolve(0.2, alpha=True)
        0.2
        "noise2" with Dissolve(0.1, alpha=True)
        0.1
        "noise3" with Dissolve(0.3, alpha=True)
        0.3
        "noise4" with Dissolve(0.4, alpha=True)
        0.4
        repeat

    image supercharge_card:
        subpixel True
        "resources/ui/powers/supercharge/card_supercharge/sc_1.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_2.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_3.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_4.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_5.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_6.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_7.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_8.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_9.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_10.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_11.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_12.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_13.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_14.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_15.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_16.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_17.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_18.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_19.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_20.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_21.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_22.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_23.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_24.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_25.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_26.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_27.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_28.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_29.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_30.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_31.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_32.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_33.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_34.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_35.webp"
        pause 0.06
        "resources/ui/powers/supercharge/card_supercharge/sc_36.webp"
        pause 0.06
        repeat

    image supercharge:
        subpixel True
        pause 0.1
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-1.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-2.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-3.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-4.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-5.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-6.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-7.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-8.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-9.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-10.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-11.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-12.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-13.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-14.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-15.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-16.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-17.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-18.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-19.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-20.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-21.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-22.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-23.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-24.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-25.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-26.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-27.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-28.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-29.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-30.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-31.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-32.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-33.webp"
        pause 0.02
        "resources/ui/powers/supercharge/screen_supercharge/supercharge-placeholder.webp"

    # Mojos
    image mojo_green:
        "resources/ui/Powers/orb_green.webp"
        size res_tb(25)
    image mojo_blue:
        "resources/ui/Powers/orb_blue.webp"
        size res_tb(25)
    image mojo_red:
        "resources/ui/Powers/orb_red.webp"
        size res_tb(25)
    image mojo_yellow:
        "resources/ui/Powers/orb_yellow.webp"
        size res_tb(25)
    image mojo_purple:
        "resources/ui/Powers/orb_purple.webp"
        size res_tb(25)

    # Evil spell splash screen
    image evil_spell:
        "resources/ui/Powers/Evil spell.webp"
        zoom 0.4

    image princess fucked: ## There really must be a shorter way to do this, but I've had no luck so far

        "resources/characters/npc/Misc/princess/princess fucked1.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked2.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked3.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked4.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked5.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked6.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked7.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked8.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked9.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked10.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked11.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked12.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked13.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked14.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked15.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked16.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked17.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked18.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked19.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked20.gif"
        pause 0.03
        "resources/characters/npc/Misc/princess/princess fucked21.gif"
        pause 0.03
        repeat



#### COLORS #### Shortcuts for color codes used in the game

init -5 python:

    c_default = "#D96B00" #"#D67229"

    c_white = "#FFFFFF"

    c_black = "#000000"

    c_grey = "#ADB9CC"

    c_lightgrey = "#D3D3D3"

    c_steel = "#4682B4"

    c_main = "#00BFFF"

    c_darkred = "#8B0000"

    c_darkblue = "#00008b"

    c_grey_blue = "#5d5ea0"

    c_darkgrey = "#1A2B47"

    c_hotpink = "#FF69B4"

    c_pink = "#FFC0CB"

    c_orange_pink = "#FF6666"

    c_gold = "#FFD700"

    c_darkgold = "#B8860B"

    c_blue = "#0000FF"

    c_lavender = "#E6E6FA"

    c_lightblue = "#6699ff" #"#00BFFF"

    c_copper = "#CC3300"

    c_red = "#FF0000"

    c_lightred = "#F78181"

    c_redpink = "#cc0052"

    c_yellow = "#FFFF33"

    c_blonde = "#FCF3CF"

    c_cream = "#FDF1B8"

    c_brown = "#502F13"

    c_lightbrown = "#D2B48C"

    c_darkbrown = "#502F13"

    c_lightprune = "#F1D4F1"

    c_prune = "#811453"

    c_darkprune = "#32274d"

    c_magenta = "#A41CC6"

    c_lightmagenta = "#FF33FF" # pink

    c_purple = "#9933FF"

    c_softpurple = "#9683EC"

    c_darkpurple = "#3D007A"

    c_orange = "#FF9900" # #FD9B1C

    c_lightorange = "#FFCC66"

    c_darkorange = "#D67229"

    c_emerald = "#009874"

    c_lightgreen = "#66FF99"

    c_darkgreen = "#003333"

    c_green = "#00B050"

    c_turquoise = "#30DADD"

    c_sapphire = "#0F52BA"

    c_azure = "#B7DBFF"

    c_crimson = "#DC143C"

    c_firered = "#B22222"

    c_violet = "#C71585"

    c_ui_unlocked = c_orange

    c_ui_sensitive = c_white

    c_ui_insensitive = c_lightgrey

    c_ui_dark = "#00000066" # "#000000CC" "#22222288"

    c_ui_darker = "#000000CC"

    c_ui_darkblue = "#000022AA"

    c_ui_darkpink = "#af3683aa"

    c_ui_brown = "#D2B48CCC"

    c_ui_light = "#FFECBFDD"

    c_ui_blue = "#69b0e2"

    c_ui_lightblue = "#69b0e277"

    c_ui_light_solid = "#FFECBF"

    all_colors = [c for c in dir(renpy.store) if c.startswith("c_")]

## COLOR DICTIONARY

    color_dict = { # Event colors
        "special": c_orange,
        "good": c_green,
        "a little good": c_lightgreen,
        "average": c_yellow,
        "average contrast": c_darkorange,
        "a little bad": c_lightred,
        "a little bad contrast": c_redpink,
        "bad": c_red,
        "very bad": c_crimson,
        "fear": c_purple,
        "gold": c_gold,
        "xp" : c_lightgreen,
        "jp" : c_orange,
        "rep": c_softpurple,
        "normal": c_white,
        "normal contrast": c_black,

        "+++" : c_emerald,
        "++" : c_green,
        "+" : c_lightgreen,

        "=" : c_white,

        "---" : c_crimson,
        "--" : c_red,
        "-" : c_lightred,

        "love +++" : c_hotpink,
        "love ++" : c_hotpink,
        "love +" : c_hotpink,
        "love -" : c_red,

        "fear +++" : c_softpurple,
        "fear ++" : c_softpurple,
        "fear +" : c_softpurple,
        "fear -" : __("#A6DEEE"),

        "special" : c_orange,
        "special contrast" : c_softpurple,
        "average" : c_yellow,
        "leveling" : c_steel,
        "normal" : c_white,
    }

    ## EN: Load event colors from JSON (BK Evolution).
    ## ZH: 从 JSON 加载事件颜色映射（BK Evolution）。
    _ec_json = DataLoader.load_event_colors()
    if _ec_json and "color_dict" in _ec_json:
        color_dict = _ec_json["color_dict"]



## MODS ##

    detected_mods = {}

    if persistent.mods is None:
        persistent.mods = {}

    mod_traceback = ""
    updated_games = defaultdict(bool)


init -2 python:
    # EN: Load contract parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载契约参数（BK Evolution）。
    _contract_json = DataLoader.load_contract_params()
    if _contract_json:
        contract_level = {int(k): v for k, v in _contract_json.get("contract_level", {}).items()}
        contract_value = {int(k): v for k, v in _contract_json.get("contract_value", {}).items()}
        contract_skill_limit = {int(k): v for k, v in _contract_json.get("contract_skill_limit", {}).items()}
        contract_sex_limit = {int(k): v for k, v in _contract_json.get("contract_sex_limit", {}).items()}
    else:
        contract_level = {}
        contract_value = {}
        contract_skill_limit = {}
        contract_sex_limit = {}


init python:

    # EN: Load contract parameters from JSON (BK Evolution) — continued.
    # ZH: 从 JSON 加载契约参数（BK Evolution）— 续。
    if _contract_json:
        contract_specials = [tuple(x) for x in _contract_json.get("contract_specials", [])]
        contract_stage_modifier = {int(k): v for k, v in _contract_json.get("contract_stage_modifier", {}).items()}
    else:
        contract_specials = []
        contract_stage_modifier = {}


    ### Brothel Rankings ###

# init -1 python:
#     init_galleries()


### MOD DEFAULT SETTINGS ### For hard-coded mod hooks. Override this after init in your mod.

## Jman - Headhunter

init -10 python:
    HH_market_jump_label = "headhunter_main"
    HH_market_caption = "{u}H{/u}eadhunter" #
    HH_market_text = "Order slaves with specific characteristics for increased cost."
    HH_main_jump_label = "headhunter_delivers"
    HH_back_caption = "Headhunter"
    HH_back_text = "The headhunter is back with your prize!"
    HH_wait_caption = "Headhunter: [game.headhunter_time] days"
    HH_wait_text = "The headhunter will be back in [game.headhunter_time] days."
    HH_button_align = {"main x" : 0.7, "main y" : 0.0825, "market x" : 0.5, "market y" : 0.99}
    HH_button_text_size = 36
    HH_button_text_font = "CHOWFUN_0.TTF"

## End of Jman Headhunter ##

### End of Mod defaut settings ###

## END OF BK INIT VARIABLES FILE ##


init 1 python:

    # EN: Load minion definitions from JSON (BK Evolution).
    # ZH: 从 JSON 加载仆从定义（BK Evolution）。
    _minions_json = DataLoader.load_minions()
    if _minions_json:
        if "all_minion_types" in _minions_json:
            all_minion_types = _minions_json["all_minion_types"]
        if "minion_descriptions" in _minions_json:
            minion_description = {k: __(v) for k, v in _minions_json["minion_descriptions"].items()}
        if "minion_xp_to_level" in _minions_json:
            minion_xp_to_level = _minions_json["minion_xp_to_level"]
        if "minion_price" in _minions_json:
            minion_price = _minions_json["minion_price"]
        if "farm_pics" in _minions_json:
            farm_pics = _minions_json["farm_pics"]

    # EN: Load farm installation parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载农场安装参数（BK Evolution）。
    _installations_json = DataLoader.load_installations()
    if _installations_json:
        if "installation_price" in _installations_json:
            installation_price = _installations_json["installation_price"]
        if "farm_type_list" in _installations_json:
            farm_type_list = _installations_json["farm_type_list"]
        if "farm_inst_list" in _installations_json:
            farm_inst_list = _installations_json["farm_inst_list"]
        if "farm_installations_dict" in _installations_json:
            farm_installations_dict = _installations_json["farm_installations_dict"]

    # EN: Load farm performance text dictionary from JSON (BK Evolution).
    # ZH: 从 JSON 加载农场表演文本字典（BK Evolution）。
    _farm_json = DataLoader.load_farm_perform_dict()
    if _farm_json:
        def _to_tuples(lst):
            return tuple(tuple(x) for x in lst)

        def _tr_dict(dct):
            return {k: __(v) for k, v in dct.items()}

        farm_perform_dict = {
            "pref_bonus": _farm_json["pref_bonus"],
            "naked_stats": _to_tuples(_farm_json["naked_stats"]),
            "service_stats": _to_tuples(_farm_json["service_stats"]),
            "sex_stats": _to_tuples(_farm_json["sex_stats"]),
            "anal_stats": _to_tuples(_farm_json["anal_stats"]),
            "fetish_stats": _to_tuples(_farm_json["fetish_stats"]),
            "bisexual_stats": _to_tuples(_farm_json["bisexual_stats"]),
            "group_stats": _to_tuples(_farm_json["group_stats"]),
            "location": [__(s) for s in _farm_json["location_i18n"]],
            "intro minion": _tr_dict(_farm_json["intro_minion_i18n"]),
            "intro perfect": _tr_dict(_farm_json["intro_perfect_i18n"]),
            "intro good": _tr_dict(_farm_json["intro_good_i18n"]),
            "intro average+": _tr_dict(_farm_json["intro_average_plus_i18n"]),
            "intro average-": _tr_dict(_farm_json["intro_average_minus_i18n"]),
            "intro bad": _tr_dict(_farm_json["intro_bad_i18n"]),
            "intro very bad": _tr_dict(_farm_json["intro_very_bad_i18n"]),
        }

        for _act in ("naked", "service", "sex", "anal", "fetish", "bisexual", "group"):
            for _mtype in ("stallion", "beast", "monster", "machine"):
                _key = _act + " story " + _mtype
                _json_key = _act + "_story_" + _mtype + "_i18n"
                farm_perform_dict[_key] = _tr_dict(_farm_json[_json_key])

        farm_perform_dict["perf good"] = _tr_dict(_farm_json["perf_good_i18n"])
        farm_perform_dict["perf bad"] = _tr_dict(_farm_json["perf_bad_i18n"])

        for _act in ("service", "sex", "anal", "fetish", "bisexual", "group"):
            for _qual in ("perfect", "good", "average", "bad", "very bad"):
                _key = _act + " " + _qual
                _json_key = _act + "_" + _qual.replace(" ", "_") + "_i18n"
                farm_perform_dict[_key] = __(_farm_json[_json_key])

        for _mtype in ("stallion", "beast", "monster", "machine"):
            farm_perform_dict[_mtype + " cum"] = __(_farm_json[_mtype + "_cum_i18n"])
            farm_perform_dict[_mtype + " cum group"] = __(_farm_json[_mtype + "_cum_group_i18n"])
        farm_perform_dict["various cum group"] = __(_farm_json["various_cum_group_i18n"])

    # EN: Load gossip text from JSON (BK Evolution).
    # ZH: 从 JSON 加载流言文本（BK Evolution）。
    _gossip_json = DataLoader.load_gossip()
    if _gossip_json:
        generic_gossip = [__(s) for s in _gossip_json.get("generic_gossip_i18n", [])]
        chapter_gossip = {k: [__(s) for s in v] for k, v in _gossip_json.get("chapter_gossip_i18n", {}).items()}
        district_gossip = {k: [__(s) for s in v] for k, v in _gossip_json.get("district_gossip_i18n", {}).items()}
    else:
        generic_gossip = []
        chapter_gossip = {}
        district_gossip = {}

    # EN: Load stat increase text from JSON (BK Evolution).
    # ZH: 从 JSON 加载属性增长文本（BK Evolution）。
    _stat_json = DataLoader.load_stat_increase_dict()
    if _stat_json and "stat_increase_dict_i18n" in _stat_json:
        stat_increase_dict = {k: __(v) for k, v in _stat_json["stat_increase_dict_i18n"].items()}

    # EN: Load maintenance description text from JSON (BK Evolution).
    # ZH: 从 JSON 加载维护描述文本（BK Evolution）。
    _maint_json = DataLoader.load_maintenance_desc()
    if _maint_json and "maintenance_desc_i18n" in _maint_json:
        maintenance_desc = {}
        _maint_colors = _maint_json.get("maintenance_desc_colors", {})
        for k, parts in _maint_json["maintenance_desc_i18n"].items():
            prefix, body, suffix = parts
            color_key = _maint_colors.get(k, "normal")
            maintenance_desc[k] = __(prefix) + event_color[color_key] % __(body) + __(suffix)

    # EN: Load jokes and compliments from JSON (BK Evolution).
    # ZH: 从 JSON 加载笑话和赞美语文本（BK Evolution）。
    _dialogue_json = DataLoader.load_dialogue_texts()
    if _dialogue_json:
        def _expand_inline_i18n(text):
            import re
            def _repl(m):
                return __(m.group(1))
            return re.sub(r"__\('([^']+?)'\)", _repl, text)

        if "jokes_i18n" in _dialogue_json:
            jokes = {k: tuple(_expand_inline_i18n(__(s)) for s in v) for k, v in _dialogue_json["jokes_i18n"].items()}
        else:
            jokes = {}
        if "compliments_i18n" in _dialogue_json:
            compliments = {k: tuple(_expand_inline_i18n(__(s)) for s in v) for k, v in _dialogue_json["compliments_i18n"].items()}
        else:
            compliments = {}

    # EN: Load recent event templates from JSON (BK Evolution).
    # ZH: 从 JSON 加载近期事件模板（BK Evolution）。
    _recent_json = DataLoader.load_recent_events()
    if _recent_json and "recent_event_templates_i18n" in _recent_json:
        recent_event_templates = {}
        for key, evt in _recent_json["recent_event_templates_i18n"].items():
            kwargs = {"type": evt["type"]}
            if "action_i18n" in evt:
                kwargs["action"] = __(evt["action_i18n"])
            if "base_description_i18n" in evt:
                kwargs["base_description"] = __(evt["base_description_i18n"])
            if "encourage" in evt:
                kwargs["encourage"] = evt["encourage"]
            if "discipline" in evt:
                kwargs["discipline"] = evt["discipline"]
            recent_event_templates[key] = GirlRecentEvent(**kwargs)
    else:
        recent_event_templates = {}

    # EN: Load log events and attraction descriptions from JSON (BK Evolution).
    # ZH: 从 JSON 加载日志事件和吸引力描述文本（BK Evolution）。
    _event_texts_json = DataLoader.load_event_texts()
    if _event_texts_json:
        if "log_event_dict_i18n" in _event_texts_json:
            log_event_dict = {}
            for k, v in _event_texts_json["log_event_dict_i18n"].items():
                color = color_dict.get(v["color_key"], c_white)
                log_event_dict[k] = "{color=" + color + "}" + __(v["template_i18n"]) + "{/color}"
        if "attraction_dict_i18n" in _event_texts_json:
            attraction_dict = {k: __(v) for k, v in _event_texts_json["attraction_dict_i18n"].items()}
    else:
        log_event_dict = {}
        attraction_dict = {}

    # EN: Load roll and result dictionaries from JSON (BK Evolution).
    # ZH: 从 JSON 加载掷骰和结果字典（BK Evolution）。
    _roll_json = DataLoader.load_roll_results()
    if _roll_json:
        if "roll_dict" in _roll_json:
            roll_dict = {int(k): v for k, v in _roll_json["roll_dict"].items()}
        if "result_dict" in _roll_json:
            result_dict = {int(k): v for k, v in _roll_json["result_dict"].items()}
            reversed_result_dict = {v: k for k, v in result_dict.items()}
        if "result_reference_templates_i18n" in _roll_json and "result_reference_labels_i18n" in _roll_json:
            _ref_tmpl = _roll_json["result_reference_templates_i18n"]
            _ref_lbl = _roll_json["result_reference_labels_i18n"]
            result_reference = (
                _ref_tmpl["very_bad"] % (reversed_result_dict["bad"]-1, result_colors["very bad"], __(_ref_lbl["very_bad"]))
                + _ref_tmpl["bad"] % (reversed_result_dict["bad"], reversed_result_dict["average"]-1, result_colors["bad"], __(_ref_lbl["bad"]))
                + _ref_tmpl["average"] % (reversed_result_dict["average"], reversed_result_dict["good"]-1, result_colors["average"], __(_ref_lbl["average"]))
                + _ref_tmpl["good"] % (reversed_result_dict["good"], reversed_result_dict["very good"]-1, result_colors["good"], __(_ref_lbl["good"]))
                + _ref_tmpl["very_good"] % (reversed_result_dict["very good"], reversed_result_dict["perfect"]-1, result_colors["very good"], __(_ref_lbl["very_good"]))
                + _ref_tmpl["perfect"] % (reversed_result_dict["perfect"], result_colors["perfect"], __(_ref_lbl["perfect"]))
            )
    else:
        roll_dict = {}
        result_dict = {}
        reversed_result_dict = {}
        result_reference = ""

    # EN: Load quality prefix and modifier tables from JSON (BK Evolution).
    # ZH: 从 JSON 加载品质前缀和修正值表（BK Evolution）。
    _quality_json = DataLoader.load_quality()
    if _quality_json:
        if "quality_prefix" in _quality_json:
            quality_prefix = _quality_json["quality_prefix"]
        if "quality_modifier" in _quality_json:
            quality_modifier = {int(k): v for k, v in _quality_json["quality_modifier"].items()}
    else:
        quality_prefix = {}
        quality_modifier = {}

    # EN: Load mood/love/fear description dictionaries from JSON (BK Evolution).
    # ZH: 从 JSON 加载心情/爱意/恐惧描述字典（BK Evolution）。
    _desc_json = DataLoader.load_girl_descriptions()
    if _desc_json:
        if "mood_description_i18n" in _desc_json:
            mood_description = {k: __(v) for k, v in _desc_json["mood_description_i18n"].items()}
        if "love_description_i18n" in _desc_json:
            love_description = {k: __(v) for k, v in _desc_json["love_description_i18n"].items()}
        if "fear_description_i18n" in _desc_json:
            fear_description = {k: __(v) for k, v in _desc_json["fear_description_i18n"].items()}
    else:
        mood_description = {}
        love_description = {}
        fear_description = {}

    # EN: Load merchant dialogue and title data from JSON (BK Evolution).
    # ZH: 从 JSON 加载商人对话和头衔数据（BK Evolution）。
    _merchant_json = DataLoader.load_merchants()
    if _merchant_json:
        if "merchant_dict" in _merchant_json:
            merchant_dict = _merchant_json["merchant_dict"]
        if "merchant_title_i18n" in _merchant_json:
            merchant_title = {k: __(v) for k, v in _merchant_json["merchant_title_i18n"].items()}
        if "merchant_greetings_i18n" in _merchant_json:
            merchant_greetings = {k: __(v) for k, v in _merchant_json["merchant_greetings_i18n"].items()}
    else:
        merchant_dict = {}
        merchant_title = {}
        merchant_greetings = {}

    # EN: Load brothel ranking reputation titles from JSON (BK Evolution).
    # ZH: 从 JSON 加载青楼声望等级头衔（BK Evolution）。
    _rankings_json = DataLoader.load_rankings()
    if _rankings_json and "brothel_ranking_reputations_i18n" in _rankings_json:
        brothel_ranking_reputations = {int(k): __(v) for k, v in _rankings_json["brothel_ranking_reputations_i18n"].items()}
    else:
        brothel_ranking_reputations = {}

    # EN: Load event sounds and gold threat parameters from JSON (BK Evolution).
    # ZH: 从 JSON 加载事件音效和金币威胁参数（BK Evolution）。
    _threat_json = DataLoader.load_threat_params()
    if _threat_json:
        if "event_sounds" in _threat_json:
            event_sounds = {}
            for k, v in _threat_json["event_sounds"].items():
                event_sounds[k] = getattr(store, v, None)
        if "gold_threat_amount" in _threat_json:
            gold_threat_amount = {int(k): v for k, v in _threat_json["gold_threat_amount"].items()}
        if "gold_threat_max" in _threat_json:
            gold_threat_max = {int(k): v for k, v in _threat_json["gold_threat_max"].items()}
    else:
        event_sounds = {}
        gold_threat_amount = {}
        gold_threat_max = {}

    # EN: Load preference responses and act descriptions from JSON (BK Evolution).
    # ZH: 从 JSON 加载偏好反应和性行为描述文本（BK Evolution）。
    _sex_desc_json = DataLoader.load_sex_descriptions()
    if _sex_desc_json:
        if "pref_response_i18n" in _sex_desc_json:
            pref_response = {k: __(v) for k, v in _sex_desc_json["pref_response_i18n"].items()}
        if "long_act_description_i18n" in _sex_desc_json:
            long_act_description = {k: __(v) for k, v in _sex_desc_json["long_act_description_i18n"].items()}
        if "experienced_description_i18n" in _sex_desc_json:
            experienced_description = {k: __(v) for k, v in _sex_desc_json["experienced_description_i18n"].items()}
    else:
        pref_response = {}
        long_act_description = {}
        experienced_description = {}

    # EN: Load miscellaneous UI texts from JSON (BK Evolution).
    # ZH: 从 JSON 加载杂项 UI 文本（BK Evolution）。
    _misc_json = DataLoader.load_misc_texts()
    if _misc_json:
        if "shopgirl_comment_i18n" in _misc_json:
            shopgirl_comment = {k: __(v) for k, v in _misc_json["shopgirl_comment_i18n"].items()}
        if "gift_description_i18n" in _misc_json:
            gift_description = {k: __(v) for k, v in _misc_json["gift_description_i18n"].items()}
        if "class_prefixes_i18n" in _misc_json:
            class_prefixes = {int(k): __(v) for k, v in _misc_json["class_prefixes_i18n"].items()}
    else:
        shopgirl_comment = {}
        gift_description = {}
        class_prefixes = {}

    # EN: Load small UI text dictionaries from JSON (BK Evolution).
    # ZH: 从 JSON 加载小型 UI 文本字典（BK Evolution）。
    _small_json = DataLoader.load_small_texts()
    if _small_json:
        if "attract_pop_dict_i18n" in _small_json:
            attract_pop_dict = {int(k): __(v) for k, v in _small_json["attract_pop_dict_i18n"].items()}
        if "workshift_dict_i18n" in _small_json:
            workshift_dict = {int(k): __(v) for k, v in _small_json["workshift_dict_i18n"].items()}
        if "special_quest_description_i18n" in _small_json:
            special_quest_description = {k: __(v) for k, v in _small_json["special_quest_description_i18n"].items()}
    else:
        attract_pop_dict = {}
        workshift_dict = {}
        special_quest_description = {}

    # EN: Load contract task definitions from JSON (BK Evolution).
    # ZH: 从 JSON 加载契约任务定义（BK Evolution）。
    _contracts_json = DataLoader.load_contract_tasks()
    if _contracts_json:
        if "contract_description_i18n" in _contracts_json:
            contract_description = {k: __(v) for k, v in _contracts_json["contract_description_i18n"].items()}
        if "contract_task_types_order" in _contracts_json:
            contract_task_types_order = _contracts_json["contract_task_types_order"]
        if "contract_task_types_description_i18n" in _contracts_json:
            contract_task_types_description = {k: __(v) for k, v in _contracts_json["contract_task_types_description_i18n"].items()}
        if "contract_tasks" in _contracts_json:
            contract_tasks = []
            for t in _contracts_json["contract_tasks"]:
                kwargs = {
                    "name": __(t.get("name_i18n", t.get("name", ""))),
                    "type": t["type"],
                    "requirements": t["requirements"],
                    "tags": tuple(tuple(x) if isinstance(x, list) else x for x in t["tags"]),
                }
                if "and_tags" in t and t["and_tags"]:
                    kwargs["and_tags"] = t["and_tags"]
                if "and_tags2" in t and t["and_tags2"]:
                    kwargs["and_tags2"] = t["and_tags2"]
                if "soft" in t:
                    kwargs["soft"] = t["soft"]
                contract_tasks.append(ContractTask(**kwargs))
    else:
        contract_description = {}
        contract_task_types_order = {}
        contract_task_types_description = {}
        contract_tasks = []

    # EN: Load MC class/stat/god/alignment descriptions from JSON (BK Evolution).
    # ZH: 从 JSON 加载主角职业/属性/神祇/阵营描述（BK Evolution）。
    _mc_json = DataLoader.load_mc_descriptions()
    if _mc_json:
        if "MC_playerclass_description_i18n" in _mc_json:
            MC_playerclass_description = {k: __(v) for k, v in _mc_json["MC_playerclass_description_i18n"].items()}
        if "MC_stat_description_i18n" in _mc_json:
            MC_stat_description = {k: __(v) for k, v in _mc_json["MC_stat_description_i18n"].items()}
        if "god_description_i18n" in _mc_json:
            god_description = {(None if k == "null" else k): __(v) for k, v in _mc_json["god_description_i18n"].items()}
        if "alignment_description_i18n" in _mc_json:
            alignment_description = {k: __(v) for k, v in _mc_json["alignment_description_i18n"].items()}
    else:
        MC_playerclass_description = {}
        MC_stat_description = {}
        god_description = {}
        alignment_description = {}

    # NOTE: TagRegistry tag_dict is loaded from JSON in settings.rpy (init -10)
    # and registered at init -4, before tag_list_dict is built at init -3.