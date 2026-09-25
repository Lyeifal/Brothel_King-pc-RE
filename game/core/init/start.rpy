######         BRO KING          ######

## The game starts here. ##

# Order of operations:
# 1. start
# 2. intro (optional)
# 3. init_game
# 4. choose_difficulty
# 5. Advance to chapter

label start:

    stop music fadeout 3.0

    $ gp_gallery = {} # Empties gallery to save on memory in-game

    $ debug_mode = False
    $ story_mode = True
    $ game_mode = None  ## EN: No start-of-game mode selection — always story (Game Modes mod select screen removed). ZH: 开局不再有模式选择——始终剧情模式（Game Modes 选择界面已移除）。
    $ starting_chapter = 1
    $ enemy_general = None
    $ unlocked_shops = []
    $ extras_dict = {"farm" : False, "carpenter" : False, "locations" : False, "shops" : False, "trainers" : False, "resources" : False}
    $ c1_path = "good" # Only used for custom starts
    $ notify_list = []
    $ notify_history = [] # Needed to avoid certain formating problems

    scene black with fade

    ## EN: No game mode selection — new games always play the intro story
    ##     (the seen_intro shortcut silently dropped the opening on repeat
    ##     runs, which read as "the story is gone"). Developers keep the
    ##     debug menu for quick starts.
    ## ZH: 不再选择游戏模式——新开局始终播放开场剧情（此前按
    ##     seen_intro 跳过的逻辑让重复开局看不到开场，像是"剧情没了"）。
    ##     开发者保留调试菜单便于快速开局。

    if debug:
        menu:
            "Choose a starting mode"

            "Normal mode - See intro":
                jump intro

            "Normal mode - No intro":
                pass

            "No story mode (Test)":
                $ story_mode = False

            "Debug mode - Fast":
                $ persistent.active_mix = "default"
                $ debug_mode = "quick"

            "Debug mode - Custom":
                $ debug_mode = "custom"

            "Export hardcoded data to JSON (Evolution)":
                call export_all_data
                $ renpy.notify(__("Data export completed. Restart game to see changes."))
                $ renpy.pause(1.0)

    else:
        jump intro

    jump start_no_intro


label start_no_intro:

    call init_game(quick=True) from _call_init_game

    if debug_mode != "quick":
        call choose_difficulty() from _call_choose_difficulty

    ## EN: Origins mod — the class is chosen on the quick_start page; if the
    ##     final class belongs to an origin, apply its talents and starting
    ##     bonus once. The registry lives in the mod, so look it up
    ##     defensively. MC is created by init_game above.
    ## ZH: Origins Mod——职业在 quick_start 页选择；若最终职业属于某个
    ##     出身，则套用其天赋与起始奖励（仅一次）。注册表位于 Mod 内，
    ##     做防御式查找。MC 由上方 init_game 创建。
    python:
        _oreg = globals().get("origin_registry")
        if _oreg is not None and MC:
            _orig = next((o for o in _oreg.list_origins() if o.class_id == MC.playerclass), None)
            if _orig is not None and getattr(MC, "_origin_applied", None) != _orig.origin_id:
                _orig.apply_to_mc(MC)
                MC._origin_applied = _orig.origin_id

    call advance_to_chapter(starting_chapter, start=True) from _call_advance_to_chapter_3

    if debug_mode == "quick": # Base values for debugging
        $ MC.set_playerclass("Wizard")
        $ MC.girls = get_girls(24)
        $ MC.gold = 100000
        $ MC.speed = 30
        $ MC.reset_interactions()

        python:
            for g in MC.girls:
                g.init_after_acquire(refresh_pics=False)
            for room in brothel.rooms.values():
                room.buy(forced=True)

    # # SET UP CALENDAR
    # $ calendar.updates()

    jump main

## DIFFICULTY

label choose_difficulty():
    scene black with fade
    play music m_suspense fadein 3.0

    $ def_panel = "MC"

    # Recall previous NG+ settings

    python:
        for s in NGP_settings:
            s.recall()

    # Sanity check - Remove unavailable girl mixes

    while True:
        show screen quick_start(def_panel)
        $ r = ui.interact()

        if r:
            hide screen quick_start
            if r == "edit mix":
                call girlpack_menu() from _call_girlpack_menu_1
                $ def_panel = "mix"

            elif r == "reset NGP":
                python:
                    for s in NGP_settings:
                        s.reset()
                $ def_panel = "extras"

            else: # CONFIRM
                $ starting_chapter = NGP_settings_dict["starting chapter"].get()

                if starting_chapter > 1 and (NGP_settings_dict["free girl challenge"].get() or NGP_settings_dict["training challenge"].get()) and not debug_mode:
                    menu:
                        "You have activated a challenge. You cannot start at a later chapter if you want to complete the challenge."
                        "Do the challenge and start at chapter 1":
                            $ starting_chapter = 1

                        "Cancel the challenge":
                            $ NGP_settings_dict["free girl challenge"].reset()
                            $ NGP_settings_dict["training challenge"].reset()

                        "Change settings":
                            jump choose_difficulty

                stop music fadeout 3.0
                return

label init_game(quick=False):

    scene black
    centered "Loading...{nw}"

    python:

    #### GAME ####

        game = Game()
        calendar = Calendar()

        # Phase 1.1: Register core services
        services.register("game", game)
        services.register("calendar", calendar)

        ## EN: Bind the selected game mode to the Game instance.
        ## ZH: 将选中的游戏模式绑定到 Game 实例。
        if game_mode:
            _mode_obj = gamemode_registry.get(game_mode)
            if _mode_obj:
                game.game_mode = _mode_obj
                _mode_obj.on_game_start(game)

        ## EN: Load JSON-driven content (traits, perks, origins, events, scenarios).
        ## ZH: 加载 JSON 驱动的内容（特质、天赋、出身、事件、剧本）。
        DataLoader.load_all()

        ## EN: Load runtime settings from JSON (BK Evolution), fallback to hardcoded dicts.
        ## ZH: 从 JSON 加载运行时设置（BK Evolution），否则使用硬编码字典。
        _fallback_cleanliness_penalties = {
            "dusty": {"dice_count": 2, "dice_bonus": -1, "text_i18n": "\nYour brothel is getting dusty. There are cobwebs in the rooms."},
            "dirty": {"dice_count": 3, "dice_bonus": 0, "text_i18n": "\nYour brothel is getting dirty. Sill thinks she saw a rat."},
            "disgusting": {"dice_count": 6, "dice_bonus": 0, "text_i18n": "\nThis place is a disgusting mess. Customers are turning away and girls are getting sick!"},
        }
        cleanliness_penalties = DataLoader.load_cleanliness_penalties() or _fallback_cleanliness_penalties

        _fallback_treasure_thresholds = [
            {"min": 2501, "category": "+++"},
            {"min": 501, "category": "++"},
            {"min": 1, "category": "+"},
            {"min": None, "category": "-"},
        ]
        treasure_thresholds = DataLoader.load_treasure_thresholds() or _fallback_treasure_thresholds

        # CHEATS #

        if persistent.cheats:
            game.activate_cheats()

        # STORY #

        logs = defaultdict(bool)
        story_flags = defaultdict(bool)
        city_events = []
        daily_events = [StoryEvent("random_night_events", type="night", chance=0.1, once=False, date=6),
                        StoryEvent("random_morning_events", type="morning", chance=0.2, once=False, date=6),
                        ] # Contains conditional night or morning events (not alarms)
        night_checks = [] # Used for custom lists [girl, label] that will be checked every night (currently only girls with a customized _BK.ini file)
        story_gossip = [] # Stores story-specific and custom gossip (permanent)
        temp_gossip = [] # Stores story-specific and custom gossip (cleared at the end of each chapter)

        # HELP FLAGS #

        help_tips = defaultdict(bool)
        help_tips["whore"] = True

        # FIRST TIME FLAGS #

        if quick:
            main_firstvisit = False
            district_firstvisit = False
            brothel_firstvisit = False
            shop_firstvisit = False
            slavemarket_firstvisit = False
            girls_firstvisit = False
            postings_firstvisit = False

        else:
            main_firstvisit = True
            district_firstvisit = True
            brothel_firstvisit = True
            shop_firstvisit = True
            slavemarket_firstvisit = True
            girls_firstvisit = True
            postings_firstvisit = True

        farm_firstvisit = True
        brothel_secondvisit = True

        # UNIQUE IDS #

        girl_id_generated = 0
        minion_id_generated = defaultdict(int)

        # CUSTOM VARIABLE #

        last_set_duration = 3 # Used for the farm
        autorest_limit = {"default" : 0}

    #### MAIN CHARACTER ####

        # CREATE MC #

        MC_name = "Nero"
        MC = Main()
        MC.char = you
        services.register("mc", MC)  # Phase 1.1

        ## EN: Load MC challenges from JSON (BK Evolution), fallback to hardcoded dict.
        ## ZH: 从 JSON 加载 MC 挑战（BK Evolution），否则使用硬编码字典。
        _fallback_challenges = {
                        "fight" : MC_challenge("Fight", stat="strength", opposed=True),
                        "force" : MC_challenge("Force", stat="strength", opposed=False),
                        "stamina" : MC_challenge("Stamina", stat="strength", opposed=False),

                        "cast" : MC_challenge("Cast Spell", stat="spirit", opposed=False),
                        "control" : MC_challenge("Control", stat="spirit", opposed=True),
                        "detect" : MC_challenge("Detect Magic", stat="spirit", opposed=False),

                        "rally" : MC_challenge("Rally", stat="charisma", opposed=False),
                        "charm" : MC_challenge("Charm", stat="charisma", opposed=False),
                        "bluff" : MC_challenge("Bluff", stat="charisma", opposed=True),

                        "speed" : MC_challenge("Speed", stat="speed", opposed=False),
                        }

        MC.challenges = DataLoader.load_challenges() or _fallback_challenges


    #### NPCs #### Declare unique NPCs


        # DEFAULT NAMES #

        sill_name = __("Sill")
        kuro_name = __("Princess")
        maid_name = __("Minako")
        gio_fucked_sill = ""
        kosmo_name = __("Strange man")
        sergeant_name = __("Woman")
        captain_name = __("Captain Farah")
        lieutenant_name = __("Lieutenant")
        maya_name = __("Woman")
        maya_love = 0
        renza_name = __("Woman")
        satella_name = __("Girl")
        shalia_name = __("Voice")
        mask_name = __("Shadow")
        gizel_name = __("Elf girl")
        stella_name = __("Woman slaver")
        goldie_name = __("Woman")
        willow_name = __("Strange girl")
        gina_name = __("Girl")
        carpenter_name = __("Woman")
        bast_name = __("Market girl")
        banker_name = __("Mysterious woman")
        riche_name = __("Sweet girl")
        ramias_name = __("Tough girl")
        gurigura_name = __("Wild girl")
        katryn_name = __("Nerdy girl")
        today_name = __("Happy tailor")
        yesterday_name = __("Quiet tailor")
        jobgirl_name = __("Freelancer")
        kenshin_name = __("Female knight")
        homura_name = __("Noble lady")
        suzume_name = __("Blue-haired girl")
        taxgirl_name = __("Elegant woman")
        narika_name = __("Petite Kunoichi")
        mizuki_name = __("Elegant Kunoichi")
        haruka_name = __("Athletic Kunoichi")
        chaos_name = __("Talking sword")
        shizuka_name = __("Mage Girl")

        # NPC OBJECTS / TRAINERS #

        NPC_sill = NPC(name = __("Sill"), portrait = "side sill happy", trainer_description = "'{i}Another cum stain? *sigh* Give me that.{/i}'\n\n{b}The Caretaker{/b}\nGrants free upkeep to a random girl every night.", effects = Effect("special", "free upkeep", 1, scope = "brothel"))
        NPC_sad_sill = NPC(name = __("Sad Sill"), portrait = "side sill sad") #, trainer_description = "bla", effects = Effect("change", "charm", 40, scope = "brothel"))
        NPC_gio = NPC()
        NPC_kosmo = NPC()
        NPC_sergeant = NPC(name = __("Kashiv"), char = sergeant)
        NPC_roz = NPC(name = __("Roz"), char = roz)
        NPC_maya = NPC(name = __("Maya"), portrait = "side maya", trainer_description = "'{i}I'd better check the perimeter. Again.{/i}'\n\n{b}Ever vigilant{/b}\nBrothel threat builds up 33 per cent slower.", effects = Effect("boost", "threat build up", -0.33, scope = "brothel"))
        NPC_renza = NPC(name = __("Renza"), portrait = "side renza", bg = 'bg thieves_guild room', trainer_description = "'{i}This purse seems heavy. Let me relieve you...{/i}'\n\n{b}Sleight of hand{/b}\nAll girls can pick pockets. Girls with the {i}Thief{/i} trait never get caught.", effects = Effect("special", "pickpocket", 1, scope = "brothel"))
        NPC_satella = NPC(name = __("Satella"), portrait = "side satella", bg = "bg shalia_temple", trainer_description = "'{i}Isn't it fun to play in the shadows? Fufufu...{/i}'\n\n{b}Dark priestess{/b}\nFear increases faster.", effects = Effect("boost", "fear gains", 1, scope = "world"))
        NPC_captain = NPC(name = __("Farah"), char=captain, portrait = "side captain", bg = 'bg vault', trainer_description = "'{i}If you wanna get on top, you must be ready to do anything. ANYTHING!{/i}'\n\n{b}Immoral{/b}\nGirls will grow used to anal and fetish acts faster.", effects = (Effect("change", "anal preferences changes", 25, scope = "brothel"), Effect("change", "fetish preferences changes", 25, scope = "brothel")))
        NPC_lieutenant = NPC(name = __("Lydie"), char = lieutenant, bg = "bg guard_office", portrait = "side lieutenant", trainer_description = "'{i}Do you want me to make an example of you? I didn't think so.{/i}'\n\n{b}Harsh discipline{/b}\nGirls are less likely to refuse to work.", effects = Effect("boost", "obedience tests", 0.1, scope = "brothel"))
        NPC_gizel = NPC(name = __("Gizel"), defense = 3, portrait = "side gizel smirk", bg = 'bg farm', trainer_description = "'{i}I love the smell of despair in the morning.{/i}'\n\n{b}Bad mojo{/b}\nEarn more mojo from fear interactions in and out of the farm.", effects = Effect("boost", "all mojo gains", 0.5))
        NPC_banker = NPC(name = __("Banker"), portrait = "side banker", bg = 'bg banking_quarter')
        NPC_riche = NPC(name = __("Riche"), id="Riche", char=riche, portrait = "side riche", bg = 'bg botanical_garden', item_types=["Flower"])
        NPC_ramias = NPC(name = __("Ramias"), id="Ramias", char=ramias, portrait = "side ramias", bg = 'bg arena_front', item_types=["Weapon"], trainer_description = "'{i}Stick 'em with the pointy end!{/i}'\n\n{b}Martial training{/b}\nAll girls receive +2 to their personal defense.", effects = Effect("change", "defense", 2, scope = "brothel"))
        NPC_gurigura = NPC(name = __("Gurigura"), id="Gurigura", char=gurigura, portrait = "side gurigura", bg = 'bg prison', item_types=["Toy", "Food", "Supplies"])
        NPC_katryn = NPC(name = __("Katryn"), id="Katryn", char=katryn, portrait = "side katryn", bg = 'bg magic_university', item_types=["Ring", "Necklace"])
        NPC_giftgirl = NPC(name = __("Gift Shop Girl"), id="Gift Shop Girl", char=giftgirl, portrait = "side giftgirl", bg = 'bg exotic_emporium', item_types=["Gift", "Misc"])
        NPC_twins = NPC(name = __("Today"), id="Today", char=today, portrait = "side today", bg = 'bg pilgrim_road', item_types=["Dress", "Accessory"])
        NPC_stella = NPC(name=__("Stella"), id="Stella", char=stella, portrait = "side stella", bg = 'bg harbor', minion_type="stallion", trainer_description = "'{i}Your weak training techniques are no match for the Blood Islands.{/i}'\n\n{b}Intensive Farming{/b}\nIncreases the efficiency of all Farm sexual training.", effects = Effect("boost", "farm preference increase", 0.5, scope = "farm"))
        NPC_goldie = NPC(name=__("Goldie"), id="Goldie", char=goldie, portrait = "side goldie", bg = 'bg farmland', minion_type="beast", trainer_description = "'{i}I read it in a book... *blush*{/i}'\n\n{b}Technique{/b}\nGirls will grow used to service and sex acts faster.", effects = (Effect("change", "service preferences changes", 25, scope = "brothel"), Effect("change", "sex preferences changes", 25, scope = "brothel")))
        NPC_willow = NPC(name=__("Willow"), id="Willow", char=willow, portrait = "side willow", bg = 'bg sewers', minion_type="monster")
        NPC_gina = NPC(name=__("Gina"), id="Gina", char=gina, portrait = "side gina", bg = 'bg junkyard', minion_type="machine")
        NPC_bast = NPC(name=__("Bast"), char=bast, portrait = "side bast", bg = 'bg market', trainer_description = "'{i}Gold is only one of the many resources that can be traded in Zan.{/i}'\n\n{b}Resourceful{/b}\nPart of your brothel's income is converted to random resources.", effects = [Effect("special", "resources as income", 1.0, scope = "brothel"), Effect("boost", "income", -0.2, scope = "brothel")])
        NPC_jobgirl = NPC(name=__("Scarlet"), char=jobgirl, bg = "bg town")
        NPC_kuro = NPC(name=__("Kurohime"), char=kuro)
        NPC_homura = NPC(name=__("Homura"), char=homura)
        NPC_mask = NPC(name=__("Shirohito"), char=mask)
        NPC_taxgirl = NPC(name=__("Taxgirl"), char=taxgirl, portrait = "side taxgirl", trainer_description = "'{i}Just expense the lobster and champagne... And give me some more.{/i}'\n\n{b}Tax Deductible{/b}\nShields part of your income against taxes every night.", effects = [Effect("boost", "taxable net income", -0.05, scope = "brothel")])

        # Chapter 2 Kunoichi
        NPC_suzume = NPC(name=__("Suzume"), char=suzume, portrait = "side suzume", trainer_description = "'{i}Found another spy yesterday... He tried to stab me, it was hilarious! Kukukuku...{/i}'\n\n{b}Night Patrol{/b}\n33%% chance of twarting security events (does not reset threat level).", effects = [Effect("special", "security block", 1.0, 0.33, scope = "brothel")])
        NPC_narika = NPC(name=__("Narika"), char=narika)
        NPC_mizuki = NPC(name=__("Mizuki"), char=mizuki)
        NPC_haruka = NPC(name=__("Haruka"), char=haruka)

        NPC_carpenter = NPC(name=__("Iulia"), char=carpenter)
        NPC_freak = NPC(name=__("Papa Freak"), char=papa)
        NPC_kenshin = NPC(name=__("Lady Kenshin"), char=kenshin, portrait = "side kenshin", bg = "bg palace")
        NPC_knight = NPC(name=__("Knight"), char = knight, bg = "bg palace")


    #### WORLD MAP (BK Evolution) ####
    python:
        ## EN: Load world map from JSON. Falls back to hardcoded initialization if JSON is missing.
        ## ZH: 从 JSON 加载世界地图。若 JSON 缺失则回退到硬编码初始化。
        _world_data = DataLoader.load_world_map("default")
        if _world_data:
            world_map = WorldMap.from_dict(_world_data)
            activate_world_map(world_map)
        else:
            # Fallback: hardcoded world map (original behavior)
            blist = {
                    1 : Brothel(1, 1, upgrades = [1, 3], max_rep = 120),
                    2 : Brothel(2, 2, [2, 5], max_rep = 1150),
                    3 : Brothel(2, 3, [3, 6], max_rep = 1800),
                    4 : Brothel(3, 4, [3, 8], max_rep = 5800),
                    5 : Brothel(3, 5, [4, 9], max_rep = 8000),
                    6 : Brothel(4, 6, [5, 11], max_rep = 18500),
                    7 : Brothel(5, 7, [6, 12], max_rep = 33750),
                    }

            beggar = Population("beggars", "beggar.webp", diff = 15, range = 10, rank=1, weight=5, base_description="An extremely unrefined and undemanding class of customers. After all, beggars can't be choosers.")
            thug = Population("thugs", "thug.webp", diff = 20, range = 10, rank=1, weight=3, effects=[Effect("boost", "crazy", 1)], base_description="Thug life comes with its share of bros and hoes. You're the bro that gets the hoes.")
            laborer = Population("laborers", "laborer.webp", 30, range = 20, rank=1, weight=2, base_description="Workers of the world, unite! Or, you know, get a girl for the night.")
            sailor = Population("sailors", "sailor.webp", 40, range = 20, rank=2, effects=[Effect("change", "waitress preference", 15), Effect("change", "anal preference", 15)], base_description="Sailors are famously randy when they come ashore. After a long voyage, seamen need some release.")
            commoner = Population("commoners", "commoner.webp", 50, range = 20, rank=2, effects=[Effect("change", "dancer preference", 15), Effect("change", "service preference", 15)], base_description="Common lives, common jobs, common wives... Seeing a commoner trying to escape all of this in a brothel is... common.")
            craftsman = Population("craftsmen", "craftsman.webp", 70, range = 30, rank=2, effects=[Effect("special", "horny", 1)], base_description="Craftsmen work with their hands, and when their hands get restless, they like to lay them on a pretty girl. Craftsmen are crafty.")
            bourgeois = Population("bourgeois", "bourgeois.webp", 90, range = 30, rank=3, effects=[Effect("change", "geisha preference", 15), Effect("change", "sex preference", 15)], base_description="When did 'down with the bourgeoisie' become 'get down with the bourgeoisie'? You sold out, man.")
            guildmember = Population("guild members", "guild member.webp", 110, range = 30, rank=3, effects=[Effect("change", "masseuse preference", 15), Effect("change", "fetish preference", 15)], base_description="Guild members are like craftsmen, but craftier.")
            patrician = Population("patricians", "patrician.webp", 110, range = 40, rank=3, effects=[Effect("special", "horny", 1), Effect("change", "satisfaction", -1)], base_description="Father figures to the community, ready to meet young girls with daddy issues.")
            aristocrat = Population("aristocrats", "aristocrat.webp", 135, range = 40, rank=4, effects=[Effect("boost", "crazy", 1.5), Effect("change", "satisfaction", -1)], base_description="Above the law. Entitled AF. Filthy rich. What's not to like?")
            noble = Population("nobles", "noble.webp", 160, range = 40, rank=4, effects=[Effect("change", "satisfaction", -2)], base_description="Nobles are easily bored. Living a life of privilege isn't all fun and games, it's also yawns.")
            royal = Population("royals", "royal.webp", 200, range = 50, rank=5, effects=[Effect("change", "satisfaction", -3)], base_description="People say royals are jaded, undeserving narcissistic parasites. No one gives them credit for how generous they are with their subjects' money. Sad.")
            all_populations = [beggar, thug, laborer, sailor, commoner, craftsman, bourgeois, guildmember, patrician, aristocrat, noble, royal]

            # Locations (simplified fallback)
            _loc_data = [
                ("Spice market", "Spice market.webp"), ("Sewers", "Sewers.webp"), ("Farm", "farmland.webp"),
                ("Watchtower", "Watchtower.webp"), ("Junkyard", "Junkyard.webp"), ("Thieves guild", "Thieves guild.webp"),
                ("Harbor", "Harbor.webp"), ("Shipyard", "Shipyard.webp"), ("Taverns", "Taverns.webp"),
                ("Seafront", "Seafront.webp"), ("Beach", "Beach.webp"), ("Exotic emporium", "Exotic emporium.webp"),
                ("Stables", "Stables.webp"), ("Plaza", "Plaza.webp"), ("Market", "Market.webp"),
                ("Gallows", "Gallows.webp"), ("Prison", "Prison.webp"), ("Arena", "Arena.webp"),
                ("Botanical garden", "Botanical garden.webp"), ("Magic university", "magic_university.webp"),
                ("Magic forest", "Magic forest.webp"), ("Hanging gardens", "Hanging gardens.webp"),
                ("Guild quarter", "Guild quarter.webp"), ("Magic guild", "Magic guild.webp"),
                ("Pilgrim road", "Pilgrim road.webp"), ("Banking quarter", "Banking quarter.webp"),
                ("Old ruins", "Ruins.webp"), ("Lakefront", "Lake.webp"), ("Training ground", "Training ground.webp"),
                ("Cathedra", "Cathedra.webp"), ("Battlements", "Battlements.webp"), ("Keep", "Keep.webp"),
                ("Hall", "Hall.webp"), ("Courtyard", "Courtyard.webp"), ("Temple", "Temple.webp"),
                ("Waterfalls", "Falls.webp"),
            ]
            _loc_objs = {name: Location(name, pic=pic) for name, pic in _loc_data}
            location_dict = {
                "The Slums": [_loc_objs["Spice market"], _loc_objs["Sewers"], _loc_objs["Farm"], _loc_objs["Watchtower"], _loc_objs["Junkyard"], _loc_objs["Thieves guild"]],
                "The Docks": [_loc_objs["Harbor"], _loc_objs["Shipyard"], _loc_objs["Seafront"], _loc_objs["Beach"], _loc_objs["Taverns"], _loc_objs["Exotic emporium"]],
                "The Warehouse": [_loc_objs["Market"], _loc_objs["Stables"], _loc_objs["Plaza"], _loc_objs["Gallows"], _loc_objs["Prison"], _loc_objs["Arena"]],
                "The Magic Gardens": [_loc_objs["Botanical garden"], _loc_objs["Magic university"], _loc_objs["Magic forest"], _loc_objs["Hanging gardens"], _loc_objs["Guild quarter"], _loc_objs["Magic guild"]],
                "The Cathedra": [_loc_objs["Pilgrim road"], _loc_objs["Banking quarter"], _loc_objs["Old ruins"], _loc_objs["Lakefront"], _loc_objs["Training ground"], _loc_objs["Cathedra"]],
                "The King's Hold": [_loc_objs["Battlements"], _loc_objs["Keep"], _loc_objs["Hall"], _loc_objs["Courtyard"], _loc_objs["Temple"], _loc_objs["Waterfalls"]],
            }
            location_dict.update(_loc_objs)
            all_locations = sum((location_dict[d] for d in ["The Slums", "The Docks", "The Warehouse", "The Magic Gardens", "The Cathedra", "The King's Hold"]), [])

            # Expose individual locations as globals for backward compatibility (Resource location=shipyard etc.)
            for _loc_name, _loc_obj in _loc_objs.items():
                _safe = _loc_name.lower().replace(" ", "_")
                globals()[_safe] = _loc_obj

            town_locations = ["spice market", "taverns", "market", "plaza", "guild quarter", "pilgrim road", "banking quarter"]
            beach_locations = ["beach", "seafront", "lakefront", "waterfalls"]
            nature_locations = ["farm", "botanical garden", "magic forest", "hanging gardens", "old ruins", "courtyard"]
            court_locations = ["magic university", "magic guild", "cathedra", "keep", "hall", "temple"]

            district_dict = {
                "slum": District("The Slums", 1, 1, 15, ((beggar, 80), (thug, 20)), pic="resources/districts/slums.webp", description=__("The Slums are located on the outskirts of Zan...")),
                "docks": District("The Docks", 2, 2, 40, ((thug, 10), (laborer, 10), (sailor, 40), (commoner, 25), (craftsman, 15)), room=["tavern"], pic="resources/districts/docks.webp", description=__("The docks are home to rowdy sailors...")),
                "warehouse": District("The Warehouse", 2, 2, 40, ((thug, 10), (laborer, 20), (sailor, 20), (commoner, 30), (craftsman, 20)), ["strip club"], pic="resources/districts/warehouse.webp", description=__("The warehouse is the industrial part of Zan...")),
                "gardens": District("The Magic Gardens", 4, 3, 100, ((commoner, 5), (craftsman, 15), (bourgeois, 30), (guildmember, 30), (patrician, 20)), ["onsen"], pic="resources/districts/gardens.webp", description=__("The gardens are where the magic-wielding locals...")),
                "cathedra": District("The Cathedra", 4, 3, 100, ((commoner, 5), (craftsman, 10), (bourgeois, 20), (guildmember, 35), (patrician, 30)), ["okiya"], pic="resources/districts/cathedra.webp", description=__("The Cathedra is the holy center...")),
                "hold": District("The King's Hold", 6, 4, 150, ((patrician, 20), (aristocrat, 50), (noble, 30)), "free", pic="resources/districts/final castle night.webp", description=__("This is the center of power in Zan...")),
            }
            endless_district = District("The King's Hold", chapter=7, rank=5, diff=200, pop=((royal, 100),), room=["tavern", "strip club", "onsen", "okiya"], pic="resources/districts/final castle.webp", description=__("This is the center of power in Zan..."))
            all_districts = [district_dict[d] for d in ["slum", "warehouse", "docks", "gardens", "cathedra", "hold"]]

            # Build minimal active_world_map for UI compatibility
            _fallback_wm = WorldMap()
            _fallback_wm.districts = district_dict
            _fallback_wm.district_order = ["slum", "warehouse", "docks", "gardens", "cathedra", "hold"]
            _fallback_wm.ui_layout = {
                "slum": {"column": 0, "row": 0, "column_span": 1},
                "warehouse": {"column": 1, "row": 0, "column_span": 1},
                "docks": {"column": 1, "row": 1, "column_span": 1},
                "gardens": {"column": 2, "row": 0, "column_span": 1},
                "cathedra": {"column": 2, "row": 1, "column_span": 1},
                "hold": {"column": 3, "row": 0, "column_span": 1},
            }
            active_world_map = _fallback_wm

    #### FARM ####

        farm_installations = {
                            "stables" : Installation(name = __("stables"), pic = "stables.webp", tags = ["big"], minions = [Minion("stallion", name=__("Bob"), start=True)], minion_type = "stallion", skill = "libido", rank = 1),
                            "pig stall" : Installation(name = __("pig stall"), pic = "pig stall.webp", tags = ["beast"], minion_type = "beast", skill = "obedience"),
                            "monster den" : Installation(name = __("monster den"), pic = "monster den.webp", tags = ["monster"], minion_type = "monster", skill = "constitution"),
                            "workshop" : Installation(name = __("workshop"), pic = "workshop.webp", tags = ["machine", "toy"], minion_type = "machine", skill = "sensitivity"),
                            }
        farm = Farm()
        services.register("farm", farm)  # Phase 1.1
        init_powers()

    #### SPELLS ####

    call init_spells() from _call_init_spells

    #### GIRLS ####

    # # TRAITS & PERKS # Moved to before_main_menu
    #
    # call init_traits() from _call_init_traits
    # call init_perks() from _call_init_perks


    # SEX ACTS #
    python:
        anal = Sexact(0.2, 1.25)
        sex = Sexact(0.5, 1.0)
        service = Sexact(0.4, 1.0)
        fetish = Sexact(0.1, 1.5)


    # CREATE SLAVEMARKET #
        slavemarket = NPC()
        slavemarket.active = True


    #### ITEMS ####

    call init_items() from _call_init_items

    # FURNITURE

    call init_furniture() from _call_init_furniture

    #### RESOURCES ####

    python:
        ## EN: Load resources from JSON (BK Evolution), fallback to hardcoded dict.
        ## ZH: 从 JSON 加载资源（BK Evolution），否则使用硬编码字典。
        ## NOTE: Ensure location variables are available (JSON or fallback may set them at different times)
        shipyard = globals().get("shipyard") or location_dict.get("Shipyard")
        beach = globals().get("beach") or location_dict.get("Beach")
        stables = globals().get("stables") or location_dict.get("Stables")
        old_ruins = globals().get("old_ruins") or location_dict.get("Old ruins")
        hanging_gardens = globals().get("hanging_gardens") or location_dict.get("Hanging gardens")
        guild_quarter = globals().get("guild_quarter") or location_dict.get("Guild quarter")

        _fallback_resource_dict = {
                        "gold" : Resource("gold", rank=0, sound=s_gold),
                        "prestige" : Resource("prestige", rank=0, sound=s_chimes),
                        "action" : Resource("action", rank=0, sound=s_success),
                        "mana" : Resource("mana", rank=0, sound=s_spell),
                        "wood" : Resource("wood", rank=2, stat="strength", sound=s_saw, location=shipyard),
                        "dye" : Resource("dye", rank=2, stat="spirit", sound=s_bubbling, location=beach),
                        "leather" : Resource("leather", stat="charisma", rank=2, sound=s_equip_item, location=stables),
                        "marble" : Resource("marble", rank=3, stat="strength", sound=s_stone, location=old_ruins),
                        "silk" : Resource("silk", rank=3, stat="spirit", sound=s_dress, location=hanging_gardens),
                        "ore" : Resource("ore", rank=3, stat="charisma", sound=s_clash, location=guild_quarter),
                        "diamond" : Resource("diamond", rank=4, sound=s_success),
                        }

        resource_dict = DataLoader.load_resources(location_resolver=lambda name: globals().get(name) or location_dict.get(name.replace("_", " ").title())) or _fallback_resource_dict

        auto_extractors = defaultdict(bool)

        # CREATE SHOPS #
        # BK Evolution: Load shop definitions from JSON and bind attributes to NPCs.

        shop = NPC("shop", id="shop", char=shopgirl, portrait = "side shopgirl", bg = "bg shop")
        unlocked_shops += [shop]
        init_items()

        _json_shops = DataLoader.load_shops()
        if _json_shops:
            _shop_upgrades_json = _json_shops.get("upgrades")
            if _shop_upgrades_json:
                shop_upgrades = _shop_upgrades_json
            for _shop_def in _json_shops.get("shops", []):
                _shop_id = _shop_def.get("id")
                _shop_var = globals().get(_shop_id if _shop_id == "shop" else "NPC_" + _shop_id)
                if _shop_var:
                    _shop_var.shop_type = _shop_def.get("shop_type")
                    _shop_var.restock_formula = _shop_def.get("restock_formula")
                    _shop_var.restock_cost = _shop_def.get("restock_cost")
                    _shop_var.special_items = _shop_def.get("special_items", [])
                    _shop_var.item_type_weights = _shop_def.get("item_type_weights")
                    if _shop_def.get("district"):
                        _shop_var.district = _shop_def.get("district")
                    if _shop_def.get("unlock_batch"):
                        _shop_var.unlock_batch = _shop_def.get("unlock_batch")
            all_shops = [shop] + [globals().get("NPC_" + s["id"]) for s in _json_shops.get("shops", []) if s["id"] != "shop" and globals().get("NPC_" + s["id"])]
            city_merchants = [s for s in all_shops if getattr(s, 'shop_type', None) == "specialist"]
            minion_merchants = [s for s in all_shops if getattr(s, 'shop_type', None) == "minion"]
        else:
            # Legacy fallback
            city_merchants = [NPC_riche, NPC_ramias, NPC_gurigura, NPC_katryn, NPC_giftgirl, NPC_twins]
            minion_merchants = [NPC_goldie, NPC_willow, NPC_gina, NPC_stella]
            all_shops = [shop] + city_merchants + minion_merchants

        # Equip magic notebook (temp)
        MC.items.append(magic_notebook)
        MC.equip(magic_notebook)


        # INIT TAXES

        init_tax()

        # #### NO STORY ####

        # if debug_mode or not story_mode:
        #     farm.activate()
        #     farm_firstvisit = False
        #     gizel_name = "Gizel"

        #     harbor.action = True
        #     stella_name = "Stella"
        #     farmland.action = True
        #     goldie_name = "Goldie"
        #     sewers.action = True
        #     willow_name = "Willow"
        #     junkyard.action = True
        #     gina_name = "Gina"

        #     unlocked_shops += [NPC_goldie, NPC_willow, NPC_gina]

        #     thieves_guild.secret = False
        #     if c1_path == "good":
        #         thieves_guild.action = False
        #     elif c1_path == "neutral":
        #         thieves_guild.action = True
        #     elif c1_path == "evil":
        #         thieves_guild.action = False
        #         watchtower.action = True

        #     renza_name = "Renza"
        #     captain_name = "Farah"

        #     story_flags["found wagon"] = True
        #     story_flags["met carpenter"] = True
        #     carpenter_name = "Iulia"

        #     shipyard.action = True # Wood
        #     stables.action = True # Leather
        #     beach.action = True # Dye
        #     old_ruins.action = True # Stone
        #     hanging_gardens.action = True # Silk
        #     guild_quarter.action = True # Ore
        #     falls.action = True # Diamond


    #### QUESTS AND CLASSES ####

    call init_postings() from _call_init_postings

    # CREATE POSTING BOARD #
    python:
        quest_board = NPC()
        load_quest_pics()

    # CREATE CONTRACT TEMPLATES

        ## EN: Load contract templates from JSON (BK Evolution), fallback to hardcoded list.
        ## ZH: 从 JSON 加载契约模板（BK Evolution），否则使用硬编码列表。
        _fallback_contract_templates = [
                    Contract(type="cruise", district="The Docks", archetypes = ["The Player", "The Fox"],
                            names=["A Night At Sea", "Touring Zan's Bay", "The Retired Sailor", "A Fancy Cruise"],
                            organizers=["the rowdy sailor fraternity", "Zan's navy", "the flibusteer social club", "the Northern merchant navy"],
                            venues=["refitted galleon", "private junk", "princely yacht", "fleet of small fishing boats", "large tour boat"],
                            character=young_sailor,
                            MC_event_pic="resources/events/brawl3.webp",
                            ),
                    Contract(type="party", district="The Cathedra", archetypes = ["The Maid", "The Slut"],
                            names=["Party Hard", "All-Nighter by The Cathedra", "Shameless Party", "From Dusk Till Dawn", "Blackjack Tables, and Hookers", "Dude, Where's My Cart?"],
                            organizers=["a foreign dignitary", "a wealthy patrician family", "an interguild association", "a visiting High Mage of Karkyr", "a close advisor of the king", "a wealthy brothel master", "the House of Lannister"],
                            venues=["abandoned church", "famous okiya", "fancy palace", "seedy tavern", "underground casino"],
                            character=party_girl,
                            MC_event_pic="resources/events/violent2.webp",
                            ),
                    Contract(type="ceremony", district="The Cathedra", archetypes = ["The Model", "The Bride"],
                            names=["A Holy Affair", "A Religious Festival", "The Saintly Ceremony", "A Most Holy Gathering", "After The Prayer"],
                            organizers=["The Holy Church of Arios", "The Nuns of Saint Dil d'Oh", "The Enlightened Brothers", "The Pious Fraternity", "The Friends of Shalia", "The Ol' Gods Alliance", "The Worshippers of the Unspeakable Yog'Gluglu", "The Priestesses of Arios"],
                            venues=["large convent", "venerable cathedral", "isolated monastery", "quiet retreat", "forgotten temple", "glorious church", "destitute orphanage"],
                            character=nun,
                            MC_event_pic="resources/events/monster assault.webp",
                            ),
                    Contract(type="festival", district="The Slums", archetypes = ["The Player", "The Fox"],
                            names=["The Moonlight Festival", "A Country Festival", "Season's Greetings", "The Countryside Fair", "The Farmers Market", "A Prized Tradition"],
                            organizers=["The Bumpkin Pumpkins", "The Farmers Guild", "Zan's Country Club", "The Gardening Brotherhood", "The Landlords Cooperative", "Dirty hippies from the Valley", "The Union of Goat-Herders"],
                            venues=["former junkyard", "large plaza", "market square", "city gate", "main roadside"],
                            character=kimono_lady,
                            MC_event_pic="resources/characters/default/farm/sex beast (7).webp",
                            ),
                    Contract(type="date", district="The Magic Gardens", archetypes = ["The Bride", "The Model"],
                            names=["A Romantic Date", "The Lonely Gentleman", "The Lord's Penthouse", "Pretty Woman"],
                            organizers=["Calif Bretznah", "High Priest Ronan", "Lord Nabukov", "Master Rhi-Seung", "Count Dicku", "The Pink Baron", "Duke Nukem", "Guild Master Felix"],
                            character=young_maid,
                            venues=["luxurious penthouse", "big country house", "old mansion", "family palace", "private temple", "popular resort"],
                            MC_event_pic="resources/characters/npc/encounters/thief4.webp",
                            ),
                    Contract(type="meeting", district="The Warehouse", archetypes = ["The Courtesan", "The Maid"],
                            names=["A Strategic Meeting", "A Show of Power", "A Political Reunion", "A Momentous Occasion", "A Pompous Conference"],
                            organizers=["The Zanic City Council", "The Rebel Alliance", "The government of His Majesty's King Pharo the 1st", "The Knights of the Oddly-Shaped Table", "The Blood-Island Coalition"],
                            venues=["progress in the Holy War", "military cooperation", "freer sex slave trading", "new fishery regulations", "limits on magic weapon stockpiles", "lowering taxes for the noble-born", "raising taxes on the poor and destitute"], # Different use for venue for this particular contract
                            character=diplomat,
                            MC_event_pic="resources/characters/npc/encounters/thief2.webp", #impress1_5.webp / quests/sex9.webp
                            ),
                    Contract(type="magic", district="The Magic Gardens", archetypes = ["The Escort", "The Courtesan"],
                            names=["Magic: The Gathering", "The Wizard Annual Convention", "The Magical Science Fair", "Fun at the Magic Guild", "Magic Schools Face-Off", "Witch Please"],
                            organizers=["High Mage Windzoss", "The Union of Concerned Sorceresses", "The Necromancer Social Club", "The Elders of Karkyr", "The Friendly Neighborhood Dark Cultists"],
                            venues=["haunted manor", "creepy old house", "high tower", "underground lair", "recently-opened demonic plane", "dusty library"],
                            character=sorceress,
                            MC_event_pic="resources/characters/npc/encounters/witches (1).webp",
                            ),
                    Contract(type="orgy", district="The King's Hold", archetypes = ["The Slut", "The Escort"],
                            names=["Orgy Night", "Sleazy Party", "Ready To Mingle", "Bachelors Day Out", "A Night Of Dirty Fun"],
                            organizers=["Mistress Smutty Kitty", "Brothel Master Quinn", "High Priest Ronan", "The Arios Nun Choir", "The Gimp", "The Hooker Trade Union", "An anonymous member of the royal family", "A rich businessman", "A noble lady"],
                            venues=["mysterious forest clearing", "gipsy camp", "dark dungeon", "decadent palace", "smutty tavern", "hidden basement", "forgotten temple"],
                            character=naked_lady,
                            MC_event_pic="resources/characters/npc/encounters/ev_onsens2.webp",
                            ),
                            ]

        contract_templates = DataLoader.load_contracts(character_resolver=lambda name: globals().get(name)) or _fallback_contract_templates

    # CREATE MOONS
    call init_moons() from _call_init_moons

    # CREATE RIVAL BROTHELS
    python:
        game.en_brothels = create_enemy_brothels()


    # SELECT GOAL CHANNELS
    ## EN: Use the new GameMode system if available, fall back to story_mode flag.
    ## ZH: 优先使用新的 GameMode 系统，回退到 story_mode 标志。

    python:
        _mode = None
        if game_mode:
            _mode = gamemode_registry.get(game_mode)
        if _mode:
            game.game_mode = _mode
            game.goal_channels = _mode.get_goal_channels()
        elif story_mode:
            ## EN: Fallback for old saves / pre-GameMode initialization.
            ## ZH: 旧存档 / GameMode 初始化前的回退。
            _fallback_story = gamemode_registry.get(GameMode.MODE_STORY)
            if _fallback_story:
                game.game_mode = _fallback_story
            game.goal_channels = goal_channels
        else:
            game.goal_channels = goal_channels_no_story


    # EVENT DICTIONARY (Events need to be added to the game with 'story_add_event' in order to proc)

    ## EN: Fallback hardcoded event dict (used if JSON is missing or invalid).
    ## ZH: 硬编码回退事件字典（JSON 缺失或无效时使用）。
    $_event_dict_fallback = {
                "zodiac_intro" : StoryEvent("zodiac_intro", type="day", once=False),
                "new_contract" : StoryEvent("new_contract", rank=2, day=1, once=False, type="morning"),
                "run_contract" : StoryEvent("run_contract", rank=2, day=28, once=False, type="night"),
                "tax_check" : StoryEvent("tax_check", rank=2, day=15, once=False, type="morning"),
                "tax_payment" : StoryEvent("tax_payment", rank=2, day=1, once=False, type="night"),
                "advertising_intro" : StoryEvent("advertising_intro", once=False, type="morning"),
                "bis_introduction" : StoryEvent("bis_introduction", condition="has_bis"),
                "group_introduction" : StoryEvent("group_introduction", condition="has_group"),

                "farm_meet_gizel" : StoryEvent(label = "farm_meet_gizel", chapter = 1, chance = 0.5, location = "spice market", condition = None, not_condition = None, once = True),
                "farm_meet_gizel2" : StoryEvent(label = "farm_meet_gizel2", chapter = 1, chance = 1.0, location = "junkyard", condition = None, not_condition = None, once = True),
                "farm_go_with_gizel" : StoryEvent(label = "farm_go_with_gizel", chapter = 1, chance = 1.0, location = "farm", condition = None, not_condition = None, once = True),
                "farm_found_a_place" : StoryEvent(label = "farm_found_a_place", chapter = 1, chance = 1.0, location = "junkyard", condition = None, not_condition = None, once = True),
                "farm_gizel_introduction" : StoryEvent(label = "farm_gizel_introduction", chapter = 1, chance = 1.0, location = "farm", condition = None, not_condition = None, once = True),
                "farm_meet_goldie" : StoryEvent(label = "farm_meet_goldie", chapter = 1, chance = 0.5, location = "farm", condition = None, not_condition = None, once = True, order=1),
                "farm_meet_stella" : StoryEvent(label = "farm_meet_stella", chapter = 2, chance = 1.0, location = "harbor", condition = None, not_condition = None, once = True, order=1),
                "farm_meet_willow" : StoryEvent(label = "farm_meet_willow", chapter = 1, chance = 1.0, location = "sewers", condition = None, not_condition = None, once = True, order=1),
                "farm_meet_gina" : StoryEvent(label = "farm_meet_gina", chapter = 1, chance = 1.0, location = "junkyard", condition = None, not_condition = None, once = True, order=1),
                "farm_activate_goldie" : StoryEvent(label = "farm_activate_goldie", chapter = 1, chance = 1.0, location = "farm", condition = None, not_condition = None, once = True),
                "farm_second_monster" : StoryEvent(label = "farm_second_monster", chapter = 1, chance = 1.0, location = "farm", condition = None, not_condition = None, once = True),

                "c1_visit_watchtower" : StoryEvent(label = "c1_visit_watchtower", chapter = 1, chance = 1.0, location = "watchtower", condition = "c1_goal_reached", min_gold=1000, not_condition = None, once = True, modes="story"),
                "c1_thieves_guild_tip" : StoryEvent(label = "c1_thieves_guild_tip", chapter = 1, type="city", chance = 0.25, not_condition = "c1_spice_market", modes="story"),
                "c1_spice_market_25" : StoryEvent(label = "c1_spice_market", chapter = 1, chance = 0.25, location = "spice market", condition = "c1_thieves_guild_tip", modes="story"),
                "c1_spice_market" : StoryEvent(label = "c1_spice_market", chapter = 1, chance = 1.0, location = "spice market", condition = "c1_thieves_guild_tip", modes="story"),
                "c1_sewers" : StoryEvent(label = "c1_sewers", chapter = 1, location = "sewers", condition = "c1_spice_market", modes="story"),
                "c1_sewers_return" : StoryEvent(label = "c1_sewers_return", chapter = 1, location = "sewers", modes="story"),
                "c1_thieves_guild_found" : StoryEvent(label = "c1_thieves_guild_found", chapter = 1, location = "thieves guild", not_condition = "c1_goal_reached", modes="story"),
                "c1_ask_guild_for_help" : StoryEvent(label = "c1_ask_guild_for_help", chapter = 1, location = "thieves guild", condition = "c1_robbed", modes="story"),
                "c1_satella_intro" : StoryEvent(label = "c1_satella_intro", chapter = 1, location = "thieves guild", condition = "c1_ask_guild_for_help", modes="story"),
                "c1_captain_meeting" : StoryEvent(label = "c1_captain_meeting", chapter = 1, location = "watchtower", condition = "c1_satella_intro", modes="story"),

                "c2_sewer_girl_returns" : StoryEvent(label = "c2_sewer_girl_returns", chapter = 2, modes="story"),
                "c2_meet_carpenter" : StoryEvent(label = "meet_carpenter", location = "gallows", modes="story"),
                # "c2_intro" : StoryEvent(label = "c2_intro", chapter=2, modes="story"),
                "c2_princess_visit1" : StoryEvent(label = "c2_princess_visit1", chapter=2, location = "stables", weekday="Saturday", modes="story"),
                "c2_princess_visit2" : StoryEvent(label = "c2_princess_visit2", chapter=2, weekday="Monday", modes="story"),
                "c2_gio_meeting" : StoryEvent(label = "c2_gio_meeting", chapter=2, location = "plaza", modes="story"),
                "c2_suzume_forest1" : StoryEvent(label = "c2_suzume_forest1", chapter=2, location = "farm", modes="story"),
                "c2_suzume_arena" : StoryEvent(label = "c2_suzume_arena", chapter=2, location = "arena", modes="story"),
                "c2_suzume_forest2" : StoryEvent(label = "c2_suzume_forest2", chapter=2, location = "farm", modes="story"),
                "c2_suzume_brothel" : StoryEvent(label = "c2_suzume_brothel", chapter=2, location = "seafront", modes="story"),
                "c2_homura_okiya1" : StoryEvent(label = "c2_homura_okiya1", type="night", chapter=2, room="okiya", chance=0.3, modes="story"),
                "c2_narika_H1" : StoryEvent(label = "c2_narika_H1", type="night", modes="story"),

                "c3_suzume_hint" : StoryEvent(label = "c3_suzume_hint", type="morning", chapter=3, condition="homura summoned", modes="story"),
                "c3_narika_MU_class" : StoryEvent(label = "c3_narika_MU_class", type = "morning", once=False, modes="story"),
                "narika_break_test" : StoryEvent(label = "narika_break_test", type="night", once=False),
                "haruka_break_test" : StoryEvent(label = "haruka_break_test", type="morning", once=False),
                "homura_farm" : StoryEvent(label = "homura_farm", type="morning", once=False),

                "meet_gurigura" : StoryEvent(label = "meet_gurigura", location = "prison", order=1),
                "meet_ramias" : StoryEvent(label = "meet_ramias", location = "arena", order=1),
                "meet_katryn" : StoryEvent(label = "meet_katryn", location = "magic university", order=1),
                "meet_riche" : StoryEvent(label = "meet_riche", location = "botanical garden", order=1),
                "meet_giftgirl" : StoryEvent(label = "meet_giftgirl", location = "exotic emporium", order=1),
                "meet_twins" : StoryEvent(label = "meet_twins", location = "pilgrim road", order=1),

                "satella_first_visit" : StoryEvent(label = "satella_first_visit", location = "thieves guild", chapter = 2),
                "satella_visit" : StoryEvent(label = "satella_visit", location = "thieves guild", chapter = 2, once = False),

                "wood_intro" : StoryEvent(label = "wood_intro", location = "shipyard", order=1),
                "dye_intro" : StoryEvent(label = "dye_intro", location = "beach", order=1),
                "leather_intro" : StoryEvent(label = "leather_intro", location = "stables", order=1),
                "marble_intro" : StoryEvent(label = "marble_intro", location = "old ruins", order=1),
                "silk_intro" : StoryEvent(label = "silk_intro", location = "hanging gardens", order=1),
                "ore_intro" : StoryEvent(label = "ore_intro", location = "guild quarter", order=1),
                "diamond_intro" : StoryEvent(label = "diamond_intro", location = "waterfalls", order=1),

                "willow fight" : StoryEvent(label = "willow_fight", chance = 0.04, once = False, room="onsen"),
                "willow relative" : StoryEvent(label = "willow_relative", room="onsen"),
                "gina research" : StoryEvent(label = "gina_research", location="prison"),
                "jobgirl_beach" : StoryEvent(label = "jobgirl_beach", location="beach", once=False),
                "MU_jobgirl" : StoryEvent(label = "MU_jobgirl", location="Magic guild", once=False),

                "stella_invitation" : StoryEvent(label = "stella_invitation", chance = 0.05, chapter=4),
                "stella_secret1" : StoryEvent(label = "stella_secret1", location="guild quarter", condition_func=is_first_tuesday),
                "stella_secret2" : StoryEvent(label = "stella_secret2", location="guild quarter", condition_func=is_first_tuesday, once=False),

                "slave_beach_event" : StoryEvent(label = "slave_beach_event", locations=beach_locations, seasons=["spring", "summer"], condition_func=slave_beach_event_happens, once=False),

                }

    ## EN: Try loading event_dict from JSON (BK Evolution data-driven events).
    ## ZH: 尝试从 JSON 加载 event_dict（BK Evolution 数据驱动事件）。
    python:
        event_dict = _event_dict_fallback
        try:
            import json, os
            _events_json_path = os.path.join(config.gamedir, "core", "data", "events", "event_dict.json")
            if os.path.exists(_events_json_path):
                with open(_events_json_path, "r", encoding="utf-8") as _f:
                    _events_data = json.load(_f)
                del _f
                event_dict = {}
                for _ev_id, _ev_data in _events_data.items():
                    event_dict[_ev_id] = StoryEvent.from_dict(_ev_data)
        except Exception:
            pass

    # Phase 6: Register events to EventRegistry
    python:
        for _ev_id, _ev_obj in event_dict.items():
            event_registry.register_event(_ev_id, _ev_obj)
        del _ev_id, _ev_obj

    # # REGISTER EVENTS

    # call init_events() from _call_init_events_1


    # NG+ Settings init

    ## EN: Fallback NG+ settings (used only if JSON is missing).
    ## ZH: NG+ 设置 fallback 数据（仅在 JSON 缺失时使用）。
    $ _fallback_NGP_settings = [ # Types: gold, resources, int, bool, plus, boost, dispenser, item, pref, girl
        NGPSetting("starting chapter", "int", label="Headstart", values = range(1, 8), cost=[10*i for i in range(2, 8)], ttip="The chapter you will start the game at. Not compatible with challenges such as the free girl challenge."),

        NGPSetting("starting gold", "gold", label="Savings", values = [5, 15, 100, 999], cost = [2, 3, 4, 5], ttip="The amount of money you will start the game with (default: {image=img_gold} [starting_gold])."),
        NGPSetting("starting resources", "resources", label="Resourceful", values= [20, 10, 5], cost = [15, 20, 25], ttip="Start the game with extra resources."),
        NGPSetting("extractors Mk I", "int", label="Capitalist I", values= range(1, 4), cost = [25, 50, 75], ttip="Start the game with resource extractors Mk I."),
        NGPSetting("extractors Mk II", "int", label="Capitalist II", values= range(1, 4), cost = [35, 70, 105], ttip="Start the game with resource extractors Mk II."),

        NGPSetting("farm", "bool", label="Farm key", cost = 10, ttip="Unlock Gizel and the Farm from the beginning of the game."),
        NGPSetting("carpenter", "bool", label="Carpenter wagon", cost = 10, ttip="Unlock Iulia the Carpenter from the beginning of the game."),
        NGPSetting("minion merchants", "bool", label="Merchant connections (minions)", cost = 25, ttip="Unlock Stella, Goldie, Willow and Gina from the beginning of the game."),
        NGPSetting("item merchants", "bool", label="Merchant connections (items)", cost = 100, ttip="Unlock Riche, Ramias, Gurigura, Katryn, the twins and the Giftshop girl from the beginning of the game."),
        NGPSetting("all trainers", "bool", label="All trainers", cost = 100, ttip="Unlock all trainers from the beginning of the game."),

        NGPSetting("strength", "plus", label="Strong", values= [1, 2, 3], cost = [15, 30, 45], ttip="Increase your character's Strength and Strength maximum beyond its base value (up to +3)."),
        NGPSetting("spirit", "plus", label="Wise", values= [1, 2, 3], cost = [15, 30, 45], ttip="Increase your character's Spirit and Spirit maximum beyond its base value (up to +3)."),
        NGPSetting("charisma", "plus", label="Funny", values= [1, 2, 3], cost = [15, 30, 45], ttip="Increase your character's Charisma and Charisma maximum beyond its base value (up to +3)."),
        NGPSetting("speed", "plus", label="Quick", values= [1, 2, 3], cost = [30, 60, 90], ttip="Increase your character's Speed and Speed maximum beyond its base value (up to +3)."),

        NGPSetting("good alignment", "bool", label="Nice guy", cost = 5, ttip="Start the game as a good person."),
        NGPSetting("evil alignment", "bool", label="Bad boy", cost = 5, ttip="Start the game as an evil person."),
        # NGPSetting("polytheist", "bool", label="Polytheist", cost = 15, ttip="Unlock all deities and atheist story lines."),
        # NGPSetting("multiclass")
        # NGPSetting("new events")

        NGPSetting("love generation", "boost", label="Gangster of love", values= [0.25, 0.5, 1.0], cost = [10, 25, 50], ttip="Gain love faster with slaves and free girls. Some people call you 'Maurice'."),
        NGPSetting("fear generation", "boost", label="Actual gangster", values= [0.25, 0.5, 1.0], cost = [5, 15, 30], ttip="Gain fear faster with slaves."),
        NGPSetting("xp generation", "boost", label="XP trainer", values= [0.25, 0.5, 1.0], cost = [5, 15, 45], ttip="Girls will gain XP faster."),
        NGPSetting("jp generation", "boost", label="JP trainer", values= [0.25, 0.5, 1.0], cost = [5, 10, 30], ttip="Girls will gain JP faster."),
        NGPSetting("prestige generation", "boost", label="Prestigious", values= [0.25, 0.5, 1.0], cost = [5, 15, 45], ttip="MC will earn Prestige faster."),
        NGPSetting("training efficiency", "boost", label="Experienced", values= [0.5, 1.0, 2.0], cost = [15, 30, 60], ttip="Train your girls significantly faster."),

        NGPSetting("tax reduction", "boost", label="Tax evasion", values= [0.15, 0.3, 0.5], cost = [50, 100, 150], ttip="Reduce your taxes thanks to the judicious application of offshore finance, political donations and elaborate voodoo curses."),

        NGPSetting("free girl", "dispenser", label="Young chemist", cost = [5, 20, 40], ttip="Produce Potions of Seduction (raises the relationship level with any free girl by one step)."),
        NGPSetting("virginity", "dispenser", label="Young surgeon", cost = [10, 50, 100], ttip="Produce Balms of Restoration (restores a girl's virginity)."),
        NGPSetting("sanity", "dispenser", label="Young therapist", cost = [10, 50, 100], ttip="Produce Incense of Bliss (restores some of a girl's sanity)."),
        NGPSetting("interactions", "dispenser", label="Young drug lord", cost = [5, 20, 40], ttip="Produce Magic Powder (regain all AP)."),
        NGPSetting("perks", "dispenser", label="Wyvern nest", cost = [25, 100, 250], ttip="Produce Wyvern eggs (+1 Perk points)."),

        NGPSetting("autorest", "bool", label="Autorest", cost = 10, ttip="Receive a Vitals Scanner from the beginning of the game, allowing you to use autorest."),
        NGPSetting("personality", "item", label="Personality reader", cost = [10, 20], ttip="Receive additional information on a girl's personality in your journal."),
        NGPSetting("taste", "item", label="Taste reader", cost = [5, 15], ttip="Receive additional information on a girl's tastes in your journal."),
        NGPSetting("fixation", "item", label="Fixation reader", cost = [5, 25], ttip="Receive additional information on a girl's sexual preferences in your journal."),

        NGPSetting("naturist frequency", "boost", label="Hippie", values= [8, 16, 32], cost = [5, 10, 20], ttip="Increase the frequency of the 'Naturist' trait for all girls."),
        # NGPSetting("portal", "special", label="Portal", cost = 0, ttip="Unlock the girl portal early."),
        NGPSetting("preferences1", "pref", label="Naked/Service preferences", values= [125, 250, 500], cost = [5, 15, 30], ttip="Increase base sexual preferences for Naked and Service for all girls."),
        NGPSetting("preferences2", "pref", label="Sex/Anal preferences", values= [125, 250, 500], cost = [10, 25, 50], ttip="Increase base sexual preferences for Sex and Anal for all girls."),
        NGPSetting("preferences3", "pref", label="Fetish/Bisexual/Group preferences", values= [125, 250, 500], cost = [15, 35, 70], ttip="Increase base sexual preferences for Fetish, Bisexual and Group for all girls."),

        NGPSetting("girl", "girl rank", label="Starting girl", values= [2, 3, 4], cost = [50, 100, 200], ttip="Receive a free girl at the start with random stats."),

        NGPSetting("free girl challenge", "bool", label="Free girl challenge", cost = 50, ttip="Receive a new girl at the start of each month. The slavemarket will become inaccessible. Worth 100 crystals if you complete the game."),
        NGPSetting("training challenge", "bool", label="No training challenge", cost = 50, ttip="The Farm becomes much more efficient, but you can no longer personally train your girls. Worth 200 crystals if you complete the game."),
        ]

    ## EN: Load NG+ settings from JSON (BK Evolution), fallback to hardcoded list.
    ## ZH: 从 JSON 加载 NG+ 设置（BK Evolution），否则使用硬编码列表。
    $ NGP_settings = DataLoader.load_ngp_settings() or _fallback_NGP_settings

    $ NGP_settings_dict = {v.name : v for v in NGP_settings}

    # Phase 6: Register NG+ settings to NGPRegistry
    python:
        for _ngp in NGP_settings:
            _cat = "misc"
            if _ngp.name in ("starting chapter", "starting gold", "starting resources", "extractors Mk I", "extractors Mk II"):
                _cat = "resources"
            elif _ngp.name in ("farm", "carpenter", "minion merchants", "item merchants", "all trainers", "girl"):
                _cat = "girls"
            elif _ngp.name in ("strength", "spirit", "charisma", "speed", "good alignment", "evil alignment"):
                _cat = "MC"
            ngp_registry.register_ngp(_ngp.name, _ngp, category=_cat)
        del _ngp, _cat

    return


label init_events(chapter=1):

    # Reminder: story_add_event type can be either 'city' (default) or 'daily'

    python:
        print("Initiating events for chapter %i" % chapter)
        ## 1. GENERIC EVENTS ##

        # CONTRACTS #
        story_add_event("new_contract", "daily")
        story_add_event("run_contract", "daily")
        story_add_event("bis_introduction", "daily")
        story_add_event("group_introduction", "daily")
        story_add_event("advertising_intro", "daily")

        # TAXES #
        story_add_event("tax_check", "daily")
        story_add_event("tax_payment", "daily")

        # RESOURCES #
        for res in build_resources:
            story_add_event(res + "_intro")

        # MISC #
        calendar.set_alarm(333, Event(label = "hmas"))
        story_add_event("slave_beach_event", "city")

        ## 2. CHAPTER EVENTS ##

        # Set-up story-quests for Mizuki
        mizuki_questK = Quest("quest", name = __('Investigate Mizuki: Karkyr'), main_stat = 'Obedience', second_stat = 'Refinement', other_stats = None, tags = 'Story', description = __("Explore Karkyr to discover the story of Mizuki"), sound = s_mystery, commit_label = "mizuki_k_go", return_label = "mizuki_k_back")
        mizuki_questK.set_to(2, Picture(path="resources/characters/npc/Kunoichi/Mizuki/react.webp"), duration = 7, special = "Story", requirements = [("Obedience", 75)], pos_traits=None, neg_trait=None, gold=0, xp=750, rep=10)
        mizuki_questW = Quest("quest", name = __('Investigate Mizuki: Westmarch'), main_stat = 'Obedience', second_stat = 'Charm', other_stats = None, tags = 'Story', description = __("Explore Westmarch to discover the story of Mizuki"), sound = s_mystery, commit_label = "mizuki_w_go", return_label = "mizuki_w_back")
        mizuki_questW.set_to(2, Picture(path="resources/characters/npc/Kunoichi/Mizuki/intro.webp"), duration = 14, special = "Story", requirements = [("Obedience", 75)], pos_traits=None, neg_trait=None, gold=0, xp=1250, rep=15)
        
        ## EN: Use GameMode's story lock check if available.
        ## ZH: 优先使用 GameMode 的剧情锁定检查。
        _use_story_mode = game.is_story_mode()
        if game.game_mode:
            _use_story_mode = game.game_mode.is_story_locked()

        if _use_story_mode and not debug_mode:
            # TUTORIAL #
            daily_events.append(event_dict["zodiac_intro"])
            
            if chapter <= 1:
                # STORY #
                calendar.set_alarm(3, Event(label = "c1_gio_is_back"))
                calendar.set_alarm(5, Event(label = "c1_meet_kosmo"))
                calendar.set_alarm(8, Event(label = "c1_ambush"))
                story_add_event("c1_thieves_guild_tip", "city")
                story_add_event("farm_meet_gizel")
                story_add_event("farm_meet_goldie")

            if chapter <= 2:
                story_add_event("c2_meet_carpenter")

            if chapter > 2:
                # MERCHANT INITIALIZATION #
                story_add_event("meet_giftgirl", duplicates=False)
                story_add_event("meet_twins", duplicates=False)
                story_add_event("meet_gurigura", duplicates=False)
                story_add_event("meet_ramias", duplicates=False)
                story_add_event("meet_katryn", duplicates=False)
                story_add_event("meet_riche", duplicates=False)

    return

#### END OF BK START FILE ####
