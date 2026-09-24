#### Core Entities classes ####

init -2 python:

    import datetime

    ## EN: Load core entity lookup tables from JSON (BK Evolution), fallback to hardcoded.
    ## ZH: 从 JSON 加载核心实体查找表（BK Evolution），否则使用硬编码。
    _elu_json = DataLoader.load_entity_lookups()
    if _elu_json:
        god_dict = {((None if k == "null" else k)): v for k, v in _elu_json["god_dict"].items()}
        name_map = _elu_json["name_map"]
        all_qualities = _elu_json["all_qualities"]
    else:
        god_dict = {"Arios" : "light", "Shalia" : "dark", None : "neutral"}
        name_map = {"captain": "farah", "lieutenant": "lydie"}
        all_qualities = ["junk", "common", "rare", "exceptional"]

    class Game(EffectBearer, Trackable):

        """This class keeps track of various story related variables and methods."""

        def __init__(self):

            self.version = config.version
            self.started = False
            self.chapter = 1
            self.set_max_girl_level()
            self.starting_gold = str(starting_gold) # Must be a string to allow player input
            self.token = 0
            self.girl_id_generated = 0
            self.free_girls = []
            self.kidnapped = []
            self.goals = chapter_goals[1]

            self.seen_goal_message = False
            self.blocked_districts = []
            self.active_mods = {}
            self.track_dict = defaultdict(int)
            self.last_pic = {"tags": [], "and_tags": [], "not_tags": [], "attempts": 0}
            self.load_pics()
            self.effects = []
            self.world_effect_dict = defaultdict(list)
            self.effect_dict = defaultdict(list)
            self.customer_preference_weight = defaultdict(int)
            self.matching_priority = "rank"
#            self.set_difficulty("normal")
            self.__filesdict_timestamp = datetime.datetime.now() #<Chris12 AutoRepair />

            ## EN: Active game mode (story, sandbox, scenario).
            ## ZH: 当前激活的游戏模式（剧情、沙盒、剧本）。
            self.game_mode = None

            self.cheats = False
            self.achievements = True
            self.trainers = []

            self.init_mixes()

            self.set_difficulty(persistent.last_difficulty)

            self.sorting_dict = defaultdict(str) # Stores sorting preferences for girls and items.
            # Keys include 'MC items', 'shop items', 'girls', 'girls items', 'farm', 'farm items', 'slavemarket', 'minion_merchant items', 'city_merchant items'.
            # Values are suffixed with " reverse" if sorting is reversed.

            self.saved_schedules = [None]*10

        def is_story_mode(self):
            """EN: Return True if current game mode is story mode.
               ZH: 返回当前是否为剧情模式。"""
            ## EN: getattr: saves created before game_mode existed lack the
            ##     attribute entirely. None (old saves / mod absent) defaults
            ##     to story mode for backward compatibility.
            ## ZH: getattr：game_mode 字段出现之前的旧存档完全没有该属性。
            ##     None（旧存档 / Mod 缺席）时默认为剧情模式，向后兼容。
            _mode = getattr(self, "game_mode", None)
            if _mode is None:
                return True
            return hasattr(_mode, 'mode_id') and _mode.mode_id == GameMode.MODE_STORY

        def save_schedule(self, girl, slot):
            self.saved_schedules[slot] = girl.get_schedule()

        def get_all_girls(self): # returns a list of all generated girls (for quick fixes and such)
            g_list = MC.girls + farm.girls + game.free_girls + slavemarket.girls + MC.escaped_girls
            if isinstance(enemy_general, Girl):
                g_list += [enemy_general]

            return g_list

        def sort(self, target, context):

            try:
                sorter = self.sorting_dict[context] # Sorter format is [caption, attribute, tooltip, reverse order, use_stats]
            except: # Initializes dict if non-existent to avoid breaking saves
                self.sorting_dict = defaultdict(str)
                return

            if sorter:
                if sorter[4]:
                    target.sort(key=lambda x, s=sorter[1]: x.get_stat(s), reverse=sorter[3])
                else:
                    target.sort(key=lambda x, s=sorter[1]: getattr(x, s), reverse=sorter[3])

        def init_mixes(self):
            self.mixes = list(persistent.game_mixes)

        # Cheats


        def activate_cheats(self):
            if renpy.call_screen("yes_no", __("WARNING. Activating cheats will disable achievements for this game. It will not affect achievements you already have. This decision cannot be reversed.\\n{b}Are you sure you want to activate cheats for this game?{/b}")):
                self.cheats=True
                self.achievements=False
            else:
                persistent.cheats = False

        # Difficulty

        def set_difficulty(self, diff): # Where diff is a string appearing in the 'diff_list' list

            if diff in diff_list:
                self.diff = diff
                self.diff_settings = copy.deepcopy(diff_dict[diff])

                if diff == "very easy" or self.cheats:
                    self.achievements = False
                else:
                    self.achievements = True

            else:
                self.diff = "custom"
                self.diff_settings = copy.deepcopy(diff)

                self.update_achievements()

        def get_diff_setting(self, setting):
            return self.diff_settings[setting]

        def change_diff_setting(self, setting, chg):
            self.diff = "custom"

            _min = diff_settings_range[setting]["min"]
            _max = diff_settings_range[setting]["max"]

            self.diff_settings[setting] += get_change_min_max(self.diff_settings[setting], chg, _min, _max)

            self.update_achievements()

        def update_achievements(self):

            self.achievements = True

            # Disables achievements if difficulty settings are not at least equal to easy mode.
            for k, v in self.diff_settings.items():
                if k == "tax rate":
                    if v <= diff_dict["easy"][k] - 0.05:
                        self.achievements = False
                        break

                elif v > diff_dict["easy"][k]:
                    self.achievements = False
                    break
            else:
                if self.cheats:
                    self.achievements = False
                else:
                    for k, v in cheat_modifier.items():
                        if v > 1.0:
                            self.achievements = False
                            break

        # Logging game stats

        def check(self, k):
            return self.track_dict[k]

        def _on_track(self, k, v):
            if k in tracked_achievements:
                test_achievements(tracked_achievements)

        def load_pics(self): # Those are the default pics for the game

            # Resetting pictures

            self.pics = []

            # Creating pictures

            for file in [f for f in renpy.list_files() if f.startswith("resources/characters/default/") and is_imgfile(f)]:

                file_name = file.split("/")[-1]

                pic = Picture(file_name, file)

                self.pics.append(pic)

                # Tracing untagged pics for debugging

                if pic.tags == []:
                    untagged_pics.append(pic.path)

        def start_mods(self, early=False):
            # Init active mods (mods are stored within the game object, unless they get overwritten after an update)
            for mod in detected_mods.values():
                if mod.active:
                    self.activate_mod(mod, early)

        def update_mods(self): # Fun fact: renpy.call breaks python blocks, but not renpy.call_screen or renpy.say

            # Will return a list of custom calls to be made (if relevant)
            update_list = []

            # Checks if a saved game's mods have been deleted or changed

            for mod in list(self.active_mods.values()):

                if mod.name not in detected_mods.keys():
                    if renpy.call_screen("yes_no", __("%s couldn't be found. Would you like to deactivate this mod for this game (recommended)?") % mod.full_name):
                        self.deactivate_mod(mod)

                elif mod.check_for_updates():
                    renpy.say(__("Mod Update"), __("A different version of mod: %s has been found (%s).") % (mod.name, str(mod.version)))

                    if not hasattr(mod, "update_label"): # Fix for older games
                        mod.update_label = ""

                    if mod.update_label:
                        update_list.append(mod.update_label) # Cannot call directly or would break the python block

                    elif renpy.call_screen("yes_no", __("Would you like to reset this mod for this game (recommended)?")):
                        self.deactivate_mod(mod)
                        self.activate_mod(detected_mods[mod.name])

                elif not persistent.mods[mod.name]["active"]:
                    if renpy.call_screen("yes_no", __("%s has been deactivated. Would you like to deactivate this mod for this game?") % mod.full_name):
                        self.deactivate_mod(mod)

            # Checks if a new mod has been activated

            for name, mod in list(detected_mods.items()):
                if mod.active:
                    if name not in self.active_mods.keys():
                        if renpy.call_screen("yes_no", __("A new mod has been activated: %s. Would you like to activate this mod for this game?") % mod.full_name):
                            self.activate_mod(mod)

            updated_games[self] = True # To do: Check if it works or needs a function

            return update_list

        def activate_mod(self, mod, early=False):

            self.active_mods[mod.name] = mod

            if early:
                if mod.early_label:
                    renpy.call_in_new_context(mod.early_label)
                    debug_notify("\n" + mod.name + ": early activation.")

                return

            # Phase 6: Register mod hooks
            if hasattr(mod, 'hooks') and mod.hooks:
                for hook_name, callback in mod.hooks.items():
                    hook_manager.register(hook_name, callback, mod=mod)

            # Phase 6: Auto-register mod events via EventRegistry
            if hasattr(mod, 'events') and mod.events:
                for ev_id, ev in mod.events.items():
                    event_registry.register_event(ev_id, ev, category="mod")

            if mod.night_label:
                daily_events.append(StoryEvent(label=mod.night_label, type="night", once=False))

            renpy.notify(__("\n%s has been activated.") % mod.name)


            if mod.init_label:
#                try:
                renpy.call_in_new_context(mod.init_label) # Suggested fix by SometimesIsNotEnough
#                except:
#                    renpy.say("System", event_color["bad"] % ("Failure to start " + mod.name) + " (calling " + mod.init_label + " label failed).")


        def deactivate_mod(self, mod):
            try:
                del self.active_mods[mod.name]
            except:
                renpy.say(__("System"), event_color["bad"] % __("Failure to deactivate %s") % mod.name)

            # Phase 6: Unregister mod hooks
            hook_manager.unregister_mod(mod)

            if mod.night_label:
                for ev in daily_events:
                    if ev.name == mod.night_label:
                        daily_events.remove(ev)

            if mod.remove_label:
                renpy.call_in_new_context(mod.remove_label)

            renpy.notify(__("\n%s has been deactivated.") % mod.name)

        def has_active_mod(self, name):
            if name in self.active_mods.keys():
                return True
            return False

        def list_free_girls(self):

            l = []

            for g in self.free_girls:
                l.append(g.name)

            return __("Free girls: ") + and_text(l)

        def get_available_locations(self):
            loc_list = []

            for d in district_dict.values():
                if d.rank <= district.rank:
                    loc_list += location_dict[d.name]

            return loc_list

        def get_goal_description(self, channel="advance"):

            goals = [g.get_description() for g in self.goals if g.channel == channel]

            if goals:
                # if channel == "advance":
                #     return __("{size=-1}To advance to the next chapter, ") + and_text(goals) + ".{/size}"
                # else:
                return "{size=-1}" + and_text(goals) + "{/size}"
            else:
                return ""

        def get_blocking_goals(self, channel="advance"):
            for goal in [g for g in self.goals if g.channel == channel]:
                if not goal.reached():
                    return True
            return False

        def get_goal_channels(self):
            # Creates a list of active channels
            active_channels = []

            for goal in self.goals:
                if goal.channel in self.goal_channels and goal.channel not in active_channels:
                    active_channels.append(goal.channel)

            return active_channels

        def get_goals(self, channel="advance"):

            # if self.chapter == 7:
            #     return [("Endless", "You are now in endless mode, enjoy continuing the game!")]

            goal_list = []

            if channel in self.get_goal_channels():
                for goal in [g for g in self.goals if g.channel == channel]:
                    goal_list.append(goal)

            return goal_list

        def get_first_goal(self):
            return self.get_goal_description(self.get_goal_channels()[0])

        def get_task(self): # Old
            if self.chapter > 2:
                return self.get_goal_description()
            else:
                return self.task

        def set_task(self, val, channel="story", max_chapter=None, blocking=True): # Creates a story goal to match. Overwrites previous story goal on this channel.
            # Clears previous task
            self.goals = [g for g in self.goals if g.channel != channel]

            if val: # Simply clears previous task if None value is provided
                if not max_chapter: max_chapter = self.chapter # Some uncompleted story goals may still allow progress to the next chapter
                self.goals.append(Goal("story", val, channel=channel, max_chapter=max_chapter, blocking=blocking))

        def set_goals(self, goals, channel="advance"): # Adds chapter goals (usually on the advance channel). goals must be a list of Goal objects
            # Clears previous goals
            self.goals = [g for g in self.goals if g.channel != channel]

            if goals:
                self.goals += goals

            if self.chapter < MAX_CHAPTER:
                self.seen_goal_message = False

        def goals_reached(self):
            for goal in self.goals:
                if not goal.reached():
                    return False

            return True

        #<Chris12 AutoRepair>
        # If there could be new images, checks if all girls still have their portraits and profiles.
        # Does not perform any missing_girls business, use the help menu for that
        #
        # Phase 0.5: Now runs at most once per in-game day (was every main-loop
        # iteration, causing unnecessary CPU load with many girl packs).
        def update_files_timestamp(self):
            # Throttle to once per game day
            if hasattr(self, '_last_repair_day') and self._last_repair_day == calendar.day:
                return
            self._last_repair_day = calendar.day

            newFiles = None
            try :
                newFiles = self.__filesdict_timestamp != GirlFilesDict.get_timestamp()
            except :
                newFiles = True # For old savegame compatibility

            if newFiles:
                self.__filesdict_timestamp = GirlFilesDict.get_timestamp()
                for girl in (MC.girls + slavemarket.girls + game.free_girls + MC.escaped_girls + farm.girls):
                    girl.check_pictures()
        #</Chris12 AutoRepair>

        def set_max_girl_level(self): # Random girls will not generate above that level. Increases every week.
            self.max_girl_rank = {0: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5}[self.chapter]
            self.max_girl_level = {0: 1, 1: 1, 2: 4, 3: 6, 4: 9, 5: 12, 6: 16, 7: 20}[self.chapter]

        def update_max_girl_level(self): # Weekly update in random girls max level
            if self.max_girl_level < self.max_girl_rank * 5:
                self.max_girl_level += 0.5 # One level unlocks every two weeks

    class Main(EffectBearer): #Attributes: name, job, god, pictures, decisions, inventory, girl inventory, character

        """This class is for the main character."""

        def __init__(self):

            self.type = "MC"
            self.name = MC_name
            self.level = 1
            self.prestige = 0
            self.gold = 0
            self.loan = None
            self.resources = defaultdict(int)
            self.last_collected = defaultdict(int)
            self.resource_tab_active = False

            self.good = 0
            self.neutral = 0
            self.evil = 0

            self.mojo = {"purple" : 0, "green" : 0, "blue" : 0, "red" : 0, "yellow" : 0}
            self.powers = []
            self.hypnotize_driver = "mana"

            self.playerclass = "Warrior"
            self.god = "Arios"

            self._interactions = self.interactions = 0

            self.reset_stats()
            self.load_pics()

            self.girls = []
            self.escaped_girls = []
            self.street_girls = []
            self.trainers = []
            self.current_trainer = None
            self.items = []
            self.active_inv_filter = []
            self.active_text_filter = ""
            self.effects = []
            self.effect_dict = defaultdict(list)
            self.equipped = []
            self.slots = MC_inventory_slots

            self.noble = False
            self.active_spells = []
            self.known_spells = []
            self.active_powers = []
            self.skill_points = 0
            self.training = True

        # Interactions property
        @property
        def interactions(self):
            return self._interactions

        @interactions.getter
        def interactions(self):
            return self._interactions

        @interactions.setter
        def interactions(self, _value):
            # debug_notify("New value is %s" % _value)
            if self._interactions > _value:
                notify(__("-%s AP") % (self._interactions - _value), pic = "img_AP", col=c_white)

            self._interactions = _value


        ## Fear Points (mojo)

        def refund_mojo(self, cost_list): # Where cost_list is a list of tuples (mojo color, cost)

            for col, nb in cost_list:
                self.mojo[col] += nb

            return True

        def raise_mojo(self, mojo_color, mojo=1, raw=False):
            if mojo <= 0:
                return 0

            if not raw:
                mojo = mojo * self.get_effect("boost", mojo_color + " mojo gains") * self.get_effect("boost", "all mojo gains") + self.get_effect("change", mojo_color + " mojo gains") + self.get_effect("change", "all mojo gains")

            self.mojo[mojo_color] += mojo

            game.track(mojo_color + " mojo", mojo)

            if not story_flags["farm powers initiated"]:
                if farm.active and not farm.powers and self.mojo["purple"] >= 5 and game.chapter >= 3:
                    # 2 days buffer to avoid overlap with chapter change events
                    calendar.set_alarm(calendar.time + 2, StoryEvent(label="farm_powers_init", type="morning"))
                    story_flags["farm powers initiated"] = True

            return mojo

        def spend_mojo(self, cost_list, use_purple=True): # Where cost_list is a list of tuples (mojo color, cost)
            # Returns the list of spent mojo points (for possible refund)

            if not self.has_mojo(cost_list, use_purple=use_purple):
                raise AssertionError("MC mojo is insufficient (%s vs %s)" % (self.mojo, cost_list))
                return False

            spent_list = []
            spent_purple = 0

            for col, nb in cost_list:
                if nb > self.mojo[col]:
                    spent_list.append((col, self.mojo[col]))
                    spent_purple += nb - self.mojo[col]
                    self.mojo[col] = 0
                else:
                    spent_list.append((col, nb))
                    self.mojo[col] -= nb

            if spent_purple:
                spent_list.append(("purple", spent_purple))
                self.mojo["purple"] -= spent_purple

            return spent_list

        def has_mojo(self, cost_list, use_purple=True):
            missing_mojo = self.get_missing_mojo(cost_list)
            if not use_purple or missing_mojo > self.mojo["purple"]:
                return False
            return True

        def get_missing_mojo(self, cost_list):
            missing_mojo = 0
            for col, nb in cost_list:
                if self.mojo[col] < nb:
                    missing_mojo += nb - self.mojo[col]

            return missing_mojo

        ## Playerclass Init ## Everywhere in the code, player class names are written with a capitalized 1st letter.

        def set_playerclass(self, playerclass): # Only call this at the start of a new game: will reset MC stats

            self.playerclass = playerclass

            self.reset_stats()

            self.load_pics()

        def set_god(self, god): # Only call this at the start of a new game: will reset MC stats

            self.god = god

            self.reset_stats()

            self.load_pics()

        def swear(self):
            return rand_choice({"Arios": ["Arios", __("By Arios"), __("By the Lightbringer"), __("By the Lord of Light")], "Shalia": ["Shalia", __("By Shalia"), __("Goddess"), __("By the Night Lady")], None: [__("Demons"), __("Damnation"), __("Priests be damned"), __("By the Seven Hells")]}[self.god])

        def reset_stats(self):
            if self.playerclass == "Warrior":

                self.strength = 2
                self.spirit = 1
                self.charisma = 0
                self.speed = 3

            elif self.playerclass == "Wizard":

                self.strength = 0
                self.spirit = 2
                self.charisma = 1
                self.speed = 3

            elif self.playerclass == "Trader":

                self.strength = 1
                self.spirit = 0
                self.charisma = 2
                self.speed = 3

            if self.god == "Arios":
                self.strength += 1

            elif self.god == "Shalia":
                self.spirit += 1

            else:
                self.charisma += 1

            self.interactions = self.speed
            self.mana = self.spirit
            self.stat_ceil = {s.lower(): 10 for s in all_MC_stats}

        ## Load pics

        def load_pics(self):

            # Loading files

            self.files = []

            for file in renpy.list_files():

                if file.startswith("resources/characters/mc/"):

                    file_parts = file.split("/")
                    file_name = file_parts[-1]

                    self.files.append(file)

            # Identifying image files

            imgfiles = [img for img in self.files if is_imgfile(img)]

            # Resetting pictures

            self.pics = []

            # Creating pictures

            for file in imgfiles:

                file_name = file.split("/")[-1]

                pic = Picture(file_name, file)

                self.pics.append(pic)

            # Choosing the best match

            idx = 0

            for pic in self.pics:
                if self.playerclass.lower() in pic.filename.lower() and god_dict[self.god].lower() in pic.filename.lower():
                    idx = self.pics.index(pic)
                    break
            else:
                for pic in self.pics:
                    if self.playerclass.lower() in pic.filename.lower():
                        idx = self.pics.index(pic)
                        break

            if not self.pics:
                raise AssertionError("No picture found for the Main Character. Check the game/MC folder.")
            else:
                self.current_pic = self.pics[idx]

        # def load_pics_old(self):

        #     # Loading files

        #     self.files = []

        #     for file in renpy.list_files():

        #         if file.startswith("resources/characters/mc/"):

        #             file_parts = file.split("/")
        #             file_name = file_parts[-1]

        #             self.files.append(file)

        #     # Identifying image files

        #     imgfiles = [img for img in self.files if is_imgfile(img)]

        #     # Resetting pictures

        #     self.pics = []

        #     # Creating pictures

        #     for file in imgfiles:

        #         file_name = file.split("/")[-1]

        #         if self.playerclass.lower() in file_name.lower():

        #             pic = Picture(file_name, file)

        #             self.pics.append(pic)

        #     if not self.pics:
        #         raise AssertionError("No picture found for the " + MC.playerclass + " class. Check the game/MC folder.")
        #     else:
        #         self.current_pic = self.pics[0]

        def change_pic(self, direction):
            if direction == "next":
                self.current_pic = get_next(self.pics, self.current_pic, loop=True)
            elif direction == "previous":
                self.current_pic = get_previous(self.pics, self.current_pic, loop=True)

        ## Reset interactions (daily)

        def reset_interactions(self):
            self.interactions = round_int(self.get_speed() * self.get_effect("boost", "AP") + self.get_effect("change", "AP"))
            self.mana = round_int(self.get_spirit() * self.get_effect("boost", "mana") + self.get_effect("change", "mana"))

        ## Banking

        def take_loan(self, loan):
            if not self.loan:
                self.loan = loan
                self.gold += loan.amount
                return True
            return False

        def repay_loan(self):
            if self.loan:
                cost = self.loan.repay()
                if self.loan.amount <= 0: # Loan repaid
                    calendar.set_alarm(calendar.time+1, Event(label = "loan_repaid"))
                return cost
            return False

        def repay_in_full(self):
            if self.loan:
                if self.gold >= self.loan.amount:
                    if renpy.call_screen("yes_no", __("Are you sure you want to repay your loan in full for %s gold?") % self.loan.amount):
                        self.gold -= self.loan.amount
                        self.loan = None
                        return True
            return False


        ## Resources

        def has_gold(self, amount):

            if self.gold >= amount:
                return True

            else:
                return False

        def change_gold(self, amount, silent=False): # should phase out hard-coded gains and losses progressively

            if amount !=0:
                self.gold += amount
                if not silent:
                    renpy.play(s_gold, "sound")
                    notify(__("Gold: ") + plus_text(amount, color_scheme="gold", decimals=0), pic="img_gold_24", col=c_gold)

        def gain_resource(self, resource="", number=1, message=True, _random=False): # Where resource is the resource name

            if _random:
                resource = rand_choice([r for r in build_resources if resource_dict[r].rank <= district.rank])
                if resource == "diamond": # can never get more than 1 diamond from a random city event
                    number=1

            if resource == "prestige":
                self.prestige += number
            elif resource in ("gold", "money", "denar"):
                resource = "gold"
                self.gold += number
            else:
                self.resources[resource] += number
                self.resource_tab_active = True

            if message:
                renpy.call("resource_gained", resource, number)
            else:
                renpy.notify(__("+%s %s") % (number, resource))

        def collect_resource(self, resource): # Where resource is the resource name

#            renpy.say("", "collecting " + str(resource))

            if self.last_collected[resource] == calendar.time:
                return "KO"

            self.last_collected[resource] = calendar.time
            self.interactions -= 1

            res = resource_dict[resource]

            if res.rank == 2:
                nb = dice(3, 1 + int(self.get_stat(res.stat)/2)) # + self.get_effect("change", "basic resource extraction")
            elif res.rank == 3:
                nb = dice(2, 1 + int(self.get_stat(res.stat)/3)) # + self.get_effect("change", "advanced resource extraction")
            elif res.rank == 4:
                if renpy.random.random() <= 0.33: # 33% chance of finding diamond
                    nb = 1 # + self.get_effect("change", "diamond extraction")
                else:
                    renpy.call_screen("OK_screen", message=__("You failed to find anything."))
                    return
            else:
                return

            # The boost is generic (moon effect)
            nb += 1 * self.get_effect("boost", "resource extraction") + self.get_effect("change", resource + " extraction")

            self.gain_resource(resource, number=round_int(nb * game.get_diff_setting("resources")))

            return

        def has_resource(self, resource, amount=1): # Where resource is the resource name or "any"
            if resource == "gold" and self.gold < amount:
                return False
            elif resource != "gold" and self.resources[resource] < amount:
                return False
            return True

        def spend_resource(self, resource, amount):
            self.spend_resources([(resource, amount)])

        def spend_resources(self, resources): # Where resources is a list of (resource, amount) tuples

            sounds = []

            for resource, amount in resources:
                if resource == "gold":
                    sounds.append(s_gold)
                    self.gold -= amount
                else:
                    self.resources[resource] -= amount
                    sounds.append(resource_dict[resource].sound)

            if sounds:
                renpy.play(rand_choice(sounds), "sound")

        def exchange(self, source="gold", target="gold", target_amount=0):

            cost = get_exchange_rate(source, target) * target_amount

            if not self.has_resource(source, cost):
                renpy.say(market_girl, __("I'm sorry, you just don't have enough %s to pay for this.") % source)

            else:
                renpy.play(resource_dict[target].sound, "sound")
                self.resources[source] -= cost
                self.resources[target] += amount


        ## Spells

        def has_spell(self, spl):

            for s in self.known_spells + self.active_spells:

                if s.name == spl.name:

                    return s

            return False

        def has_active_spell(self, spellname = None, spelltype = None):

            if spelltype:
                for s in self.active_spells:
                    if s.type == spelltype:
                        return True

            else:
                for s in self.active_spells:
                    if s.name == spellname:
                        return True

            return False

        def has_auto_spell(self, spelltype):

            for s in self.known_spells:
                if s.auto and s.type == spelltype:
                    return True

            return False


        def update_spells(self):

            for spl in spellbook[self.playerclass]:

                if spl.level <= self.level and not self.has_spell(spl):

                    self.learn(spl)

                # elif spl.level > self.level and self.has_spell(spl): # Shouldn't be needed anymore. #? Check if it solves the 'forgotten spell when levelling' issue

                #     self.unlearn(self.has_spell(spl))
                #     renpy.pause(0.5)

            self.known_spells.sort(key=lambda x: x.get_cost())
#            renpy.say("", "Known spells =" + str(len(self.known_spells)))

        def learn(self, spl):
            if spl.type == "passive":
                self.active_spells.append(spl)
                self.add_effects(spl.effects)

                renpy.call_screen("OK_screen", title = spl.name, message = __("%s has learnt a new talent.\n\n%s") % (self.name, spl.description), pic = spl.pic, pic_size = "small")

            else:
                self.known_spells.append(spl)
                renpy.call_screen("OK_screen", title = spl.name, message = __("%s has learnt a new spell.\n\n%s") % (self.name, spl.description), pic = spl.pic, pic_size = "small")

            spl.auto = False

        def unlearn(self, spl): # Obsolete with 0.14

            if spl in self.active_spells:
                self.deactivate_spell(spl)

            if spl in self.known_spells:
                self.known_spells.remove(spl)
            spl.auto = False

            renpy.notify(__("{color=[c_crimson]}%s has forgotten %s{/color}") % (self.name, spl.name))


        def activate_spell(self, spl):

            if spl in self.active_spells:
                renpy.notify(__("%s: This spell is already active.") % spl.name)
                return False

            elif type != "passive" and self.has_active_spell(spelltype = spl.type):
                renpy.notify(__("Another %s spell is already active.") % spl.type)
                return False

            elif self.mana >= spl.cost:

                self.mana -= spl.cost
                self.active_spells.append(spl)
                self.add_effects(spl.effects)

                renpy.play(spl.sound, channel='sound2')
                renpy.notify(__("%s has been activated.") % spl.name)
                # renpy.pause(0.5)

                return True

            else:

                renpy.notify(__("%s: You do not have enough mana to cast this spell.") % spl.name)

                return False

            return

        def autocast(self, spell, _time):

            msg = ""
            result = False

            if spell.auto == _time and spell not in self.active_spells:
                if self.activate_spell(spell):
                    msg = __("You have cast %s.") % spell.name
                    result = "success"
                    _sound = s_spell
                else:
                    msg = __("You failed to cast %s.") % spell.name
                    result = "fail"
                    _sound = s_fizzle

                renpy.play(_sound, "sound")
                notify(msg)
                # renpy.pause(0.5)

            return result, msg


        def deactivate_spell(self, spl):

            self.active_spells.remove(spl)
            self.remove_effects(spl.effects)

            renpy.notify(__("%s has expired") % spl.name)
            # renpy.pause(0.5)

            return

        def reset_spells(self):
            for spell in [s for s in self.active_spells if s.duration == "turn"]:
                MC.deactivate_spell(spell)

        def toggle_auto_spell(self, spl):

            if spl.auto == "night":
                spl.auto = "morning"

            elif spl.auto == "morning":
                spl.auto = False

            elif self.has_auto_spell(spl.type):
                renpy.notify(__("Only one %s spell can be automated.") % spl.type)

            else:
                spl.auto = "night"


        ## Leveling

        def change_prestige(self, chg, apply_boost=True, silent=False):
            if apply_boost:
                chg = chg * self.get_effect("boost", "prestige") + self.get_effect("change", "prestige")

            chg *= cheat_modifier["prestige"] * game.get_diff_setting("prestige")
            self.prestige += chg

            if MC.ready_to_level():
                MC.level_up()

            game.track("had sex")

            p = round_up(chg/2)

            if not silent:
                notify(__("Prestige ") + "+"*p, pic=self.current_pic, debug_txt="(%s)" % str_int(chg))

            return chg

        def ready_to_level(self):
            if self.level < 25:
                if self.prestige >= MC_xp_to_levelup[self.level]:
                    return True

            return False

        def level_up(self, forced = False):

            if (self.ready_to_level() or forced) and self.level < 25:
                self.level += 1
                self.skill_points += 1
                test_achievements(["Warrior", "Wizard", "Trader"])
                self.update_spells()
                renpy.play(s_spell, "sound")
                return True

            else:
                return False

        def get_stat_cap(self, stat):
            return 10 + self.get_effect("change", stat + " max")

            # try:
            #     return self.stat_ceil[stat]
            # except:
            #     self.stat_ceil = {s.lower(): 10 for s in all_MC_stats}
            #     return 10


        def change_stat(self, stat, nb, apply_boost=True, spillover=False, silent=False):

            stat = stat.lower()

            if stat not in all_MC_stats:
                debug_notify(__("Unknown MC skill: %s") % stat)
                return False

            cap = self.get_stat_cap(stat)

            if apply_boost:
                nb = nb * self.get_effect("boost", stat + " gains") + self.get_effect("change", stat + " gains")

            if stat == "strength":
                nb = min(cap-self.strength, nb)
                self.strength += nb

            elif stat == "spirit":
                nb = min(cap-self.spirit, nb)
                self.spirit += nb

            elif stat == "charisma":
                nb = min(cap-self.charisma, nb)
                self.charisma += nb

            elif stat == "speed":
                nb = min(cap-self.speed, nb)
                self.speed += nb

            if nb > 0:
                if not silent:
                    notify(__("%s's %s: +%i") % (self.name, stat, int(nb)))
                return True

            return False

        def raise_stat(self, stat, nb): # Obsolete: rename to change_stat
            return self.change_stat(stat, nb)


        ## Get methods

        def get_stat(self, statname, raw=False):
            if statname.lower() in ("strength", "defense"):
                r = self.get_defense(raw=raw)

            elif statname.lower() == "spirit":
                r = self.get_spirit(raw=raw)

            elif statname.lower() == "charisma":
                r = self.get_charisma(raw=raw)

            elif statname.lower() == "speed":
                r = self.get_speed(raw=raw)

            return r

        def get_strength(self, fight=False, raw=False):
            return self.get_defense(fight, raw)

        def get_defense(self, fight=False, raw=False): # Raw affects item boosts but not spells

            defense = self.strength

            if not raw:
                defense += self.get_effect("change", "strength") + self.get_effect("change", "defense") - self.get_effect("special", "wound")

                if self.get_effect("special", "dragon form"):
                    defense = self.get_spirit()

            if fight and self.has_active_spell(spellname = "Summon bloodhound"):
                defense += dice(6)

            return max(defense, 0)

        def can_defend(self):
            if self.interactions > 0 or self.get_effect("special", "defender") > 1:
                return True
            return False

        def get_spirit(self, raw=False):

            if raw:
                return self.spirit

            spirit = self.spirit

            if not raw:
                spirit += self.get_effect("change", "spirit") - self.get_effect("special", "wound")

            return max(spirit, 0)


        def get_charisma(self, raw=False):

            char = self.charisma

            if not raw:
                char += self.get_effect("change", "charisma") - self.get_effect("special", "wound")

                if self.get_effect("special", "fairy form"):
                    char = self.get_spirit()

            return max(char, 0)


        def get_speed(self, raw=False):
            if raw:
                return self.speed

            spd = self.speed

            spd += self.get_effect("change", "speed") - self.get_effect("special", "wound")

            return max(spd, 0)

        def get_stat_description(self, stat):
            desc = MC_stat_description[stat]

            if self.get_effect("special", "wound"):
                desc += __("\n{color=[c_red]}You are wounded for %i day%s.{/color}") % ((self.heal_day - calendar.time), plural(self.heal_day - calendar.time))

            return desc


        def has_girlfriend(self):
            if get_known_free_girls(3):
                return True
            return False


        # Old, should be phased out in favor of challenges

        def test_defense(self, diff):

            your_score = self.get_defense(fight = True) + dice(6)
            enemy_score = diff + dice(6)

#            renpy.say("", "Rolled " + str(your_score) + "against " + str(enemy_score))

            if your_score >= enemy_score:
                return True

            else:
                return False

        def test_spirit(self, diff):

            if (self.get_spirit() + dice(6)) >= (diff + dice(6)):
                return True

            else:
                return False

        def test_charisma(self, diff):

            if (self.get_charisma() + dice(6)) >= (diff + dice(6)):
                return True

            else:
                return False

        ## Alignment

        def get_alignment(self):
            if self.good > self.evil + 2 and self.good > self.neutral:
                return "good"
            elif self.evil > self.good + 2 and self.evil > self.neutral:
                return "evil"
            else:
                return "neutral"

        def get_alignment_delta(self, alignment):
            if alignment == "good":
                return min(MC.good - MC.evil, MC.good - MC.neutral)
            elif alignment == "evil":
                return min(MC.evil - MC.good, MC.evil - MC.neutral)
            else:
                return min(MC.neutral - MC.good, MC.neutral - MC.evil)


        def is_good(self):
            return self.get_alignment() == "good"

        def is_neutral(self):
            return self.get_alignment() == "neutral"

        def is_evil(self):
            return self.get_alignment() == "evil"

        ## Playerclass

        def is_warrior(self):
            return self.playerclass == "Warrior"

        def is_wizard(self):
            return self.playerclass == "Wizard"

        def is_trader(self):
            return self.playerclass == "Trader"

        ## Items

        def add_text_filter(self, text_filter):
            self.active_text_filter = text_filter.lower()
            self.active_inv_filter = []
            renpy.restart_interaction()

        def get_modifier(self, operation, raw=False):

            mod = price_modifiers[operation]

            if not raw:
                mod *= self.get_effect("boost", operation)

                # Hard cap on the Haggler talent
                if operation == "buy" and mod < 0.75:
                    mod = 0.75
                elif operation == "sell" and mod > 1.25:
                    mod = 1.25

            return mod

        def buy(self, seller, obj, price, counterpart=None): # For items this is handled by the 'transact' function in most cases

            self.gold -= price

            if counterpart:
                counterpart.take(seller, obj)
            else:
                self.take(seller, obj)

            if obj.type == "girl":
                game.track("gold spent slavemarket", price)
            else:
                game.track("gold spent shops", price)

            norollback()

        def can_sell(self, buyer, obj):
            if not hasattr(self, "sold"):
                self.sold = defaultdict(list)
            elif obj in self.sold[buyer]:
                return False
            return True

        def sell(self, buyer, obj, price = None, owner=None):
            if isinstance(obj, ItemInstance):
                if not obj.sellable:
                    renpy.notify(__("%s: You cannot sell this item.") % obj.name)
                    return False

            self.gold += price

            if owner:
                owner.give(buyer, obj)
            else:
                self.give(buyer, obj)

            self.sold[buyer].append(obj)

            norollback()
            return True


        def take(self, giver, obj): ## I know, girls are not objects...
            if isinstance(obj, Item):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % obj.name)

            if obj.type == "girl":
                try:
                    giver.girls.remove(obj)
                except:
                    pass
                renpy.call("acquire_girl", obj)

            else:
                self.items.append(obj)
                try:
                    giver.items.remove(obj)
                except:
                    pass

            renpy.restart_interaction()


        def give(self, taker, obj):
            if isinstance(obj, Item):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % obj.name)

            if obj.type == "girl":
                if obj in self.girls:
                    self.girls.remove(obj)
                elif obj in farm.girls:
                    farm.girls.remove(obj)
                taker.girls.append(obj)

            elif taker != MC and not obj.giveable:
                renpy.notify(__("%s: You cannot give this item.") % obj.name)
                return False

            elif taker:
                if obj in self.items and obj.equipped:
                    self.unequip(obj)
                renpy.play(obj.sound, "sound")
                self.items.remove(obj)
                taker.items.append(obj)

            # renpy.restart_interaction()
            return True

        def gift(self, taker, item): #? Probably doesn't work #! TEST THIS
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)

            if item.giveable:
                self.items.remove(item)
                renpy.say("", __("You give %s {b}%s{/b}.") % (taker.name, article(item.name)))
                result = taker.receive_gift(item)
                if not result:
                    renpy.notify(__("%s: You cannot give this item to this person.") % item.name)
                    self.items.append(item)
                    return -1
                norollback()

                return result
            else:
                renpy.notify(__("%s: You cannot give this item.") % item.name)
                return -1

        def equip(self, item):
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)

            for i in self.equipped:
                if i.type.slot == item.type.slot:
                    self.unequip(i)

            self.equipped.append(item)
            self.add_effects(item.effects)
            item.equipped = True

            test_achievements(["mc strength", "mc spirit", "mc charisma", "mc speed"])

        def unequip(self, item):
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)

            self.equipped.remove(item)
            self.remove_effects(item.effects)
            item.equipped = False

        def remove_item(self, it, unequip=True, use_sound=True):
            if not isinstance(it, ItemInstance):
                renpy.say(bk_error, __("Warning: This item cannot be removed, it is not instantiated (%s).") % it.name)
            if it in self.items:
                if unequip and it.equipped:
                    self.unequip(it)
                self.items.remove(it)
                if use_sound:
                    renpy.play(it.sound, "sound")

        def add_item(self, it, equip=False, use_sound=True):
            if not isinstance(it, ItemInstance):
                renpy.say(bk_error, __("Warning: This item cannot be added, it is not instantiated (%s).") % it.name)
            self.items.append(it)
            if equip:
                self.equip(it)
            if use_sound:
                renpy.play(it.sound, "sound")

        def use_item(self, item):
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)

            used = True
            #
            # if item.usage == "buff":
            #
            #     self.add_effects(item.effects)
            #
            #     calendar.set_alarm(calendar.time + item.charges, Event(label = "effect_expired", object = (self, item.effects)))
            #
            #     self.items.remove(item)
            #
            #
            # else:

            for e in item.effects:

                if e.type == "gain":

                    if e.target in ("prestige"):
                        e.gain(self)

                        if MC.ready_to_level():
                            MC.level_up()

                    elif e.target in ("skills", "skill points"):
                        self.skill_points += e.value


                elif e.duration > 0:
                    self.add_effects(e, expires=calendar.time + e.duration)
                    used = True

                    # calendar.set_alarm(calendar.time + e.duration, Event(label = "effect_expired", call_args = (self, e)))

                elif e.type == "special":
                    # AP restoration
                    if e.target == "MC interactions":
                        self.reset_interactions()

            if used:

                r = item.use_me()

                if r == "used_up":
                    self.items.remove(item)

                norollback()

            return r

        def has_item(self, it_name):

            for it in self.items:
                if it.name.lower() == it_name.lower():
                    return True

            return False

        def get_items(self, target="any", type="any", name="any", effect_type="any", effect_target="any", strict=False): # Where 'type' is a name, not an object. Use strict to avoid naming errors (such as Extractor MKI being mistaken with MKII)

            items = []

            for it in self.items:
                if not isinstance(it, ItemInstance):
                    renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % it.name)
                if it.target == target or target == "any":
                    if it.type.name == type or type == "any":
                        if name == it.name or (name in it.name and not strict) or name == "any":
                            if effect_type != "any" or effect_target != "any":
                                if it.has_effect(effect_type, effect_target):
                                        items.append(it)
                            else:
                                items.append(it)
            return items

        ## Effects

        def get_effect(self, type, target, randomize=True):
            if type == "boost":
                return get_effect(self, type, target, randomize=randomize) * brothel.get_effect(type, target, randomize=randomize)
            else:
                return get_effect(self, type, target, randomize=randomize) + brothel.get_effect(type, target, randomize=randomize)

        def wound(self, _mod, _duration):
            self.heal_day = calendar.time + _duration # This is needed for the tooltip
            self.add_effect(Effect("special", "wound", _mod, duration=_duration), expires=self.heal_day)
            notify(__("%s is wounded for %i days.") % (MC.name, _duration))


        ## Misc

        def cycle_trainers(self, reverse = False):

            index = self.trainers.index(self.current_trainer)

            if not reverse:
                index += 1
                if index > len(self.trainers)-1:
                    index = 0
            else:
                index -= 1
                if index < 0:
                    index = len(self.trainers)-1

            self.current_trainer = self.trainers[index]

            update_effects()

        def rand_say(self, *sentences): # MC will say a random sentence in the list
            # Can take either a single list of strings, or several strings as arguments.

            if len(sentences) == 1 and not is_string(sentences):
                sentences = sentences[0]
            you(rand_choice(self.filter_say(sentences)))

            return

        def say(self, sentences): # Same as rand_say, just easier to manipulate
            return self.rand_say(sentences)

        def filter_say(self, sentences): # MC may say a random sentence in the list if and only if it checks out with his attributes

            d_list = []

            for it in sentences:

                if it.startswith("wr: ") or it.startswith("wa: "):
                    if self.is_warrior():
                        d_list.append(it[4:])

                elif it.startswith("wz: ") or it.startswith("wi: "):
                    if self.is_wizard():
                        d_list.append(it[4:])

                elif it.startswith("tr: "):
                    if self.is_trader():
                        d_list.append(it[4:])

                elif it.startswith("gd: "):
                    if self.is_good():
                        d_list.append(it[4:])

                elif it.startswith("ne: "):
                    if self.is_neutral():
                        d_list.append(it[4:])

                elif it.startswith("ev: "):
                    if self.is_evil():
                        d_list.append(it[4:])

                elif it.startswith("ar: "):
                    if self.god == "Arios":
                        d_list.append(it[4:])

                elif it.startswith("sh: "):
                    if self.god == "Shalia":
                        d_list.append(it[4:])

                elif it.startswith("ng: "):
                    if self.god == None:
                        d_list.append(it[4:])

                else:
                    d_list.append(it)

            return d_list

    #### End of Main character class ####



    class NPC(): # Attributes: name, pictures, inventory, girl inventory, character

        """This class is for NPCs: story NPCs, shopkeeper and slave master, etc."""

        def __init__(self, name = "", id=None, char=None, defense=0, portrait = None, trainer_description = None, effects = None, item_types = "all", minion_type = None, bg = "bg_bro", shop_type=None, restock_formula=None, restock_cost=None, special_items=None):
            self.type = "NPC"
            self.name = name
            self.id = id or name
            self.girls = []
            self.items = []
            self.love = 0
            self.hate = 0
            self.defense = defense
            self.met = False
            self.banged = False
            self.raped = False
            self.flags = defaultdict(bool)
            self.active = False # Used for carpenter and slavemarket for now
            self.portrait = portrait
            self.bg = bg
            self.location = None

            if effects: # This NPC is also a potential trainer
                self.trainer_description = trainer_description
                self.effects = make_list(effects, Effect)
                game.trainers.append(self) # Updates the list of all available trainers
            self.updated = False
            self.last_restock = 0
            self.item_types = item_types
            self.minion_type = minion_type
            self.upgrade_level = 0
            self.stock_modifiers = {"junk" : 0, "common" : 0, "rare" : 0, "exceptional" : 0, "minion" : 0, "item" : 0}

            # BK Evolution: shop data-driven attributes
            self.shop_type = shop_type
            self.restock_formula = restock_formula
            self.restock_cost = restock_cost
            self.special_items = special_items or []

            if char:
                self.char = char
            else: # imports renpy character if available
                try:
                    self.char = getattr(store, self.name.lower()) #?
                except:
                    self.char = Character(self.name)

        def __getattr__(self, attr):
            if attr == "id":
                return self.name
            raise AttributeError("'NPC' object has no attribute '%s'" % attr)

        def get_bg(self):
            global bg_bro
            if self.bg == "bg_bro":
                return bg_bro
            else:
                return self.bg

        def take(self, giver, obj):
            if isinstance(obj, Item):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % obj.name)

            self.items.append(obj)
            if obj.equipped:
                giver.unequip(obj)
            try:
                giver.items.remove(obj)
            except:
                pass

        def get_defense(self, fight=False):
            return self.defense

        def unlock_trainer(self):
            if self not in MC.trainers:
                MC.trainers.append(self)
                # TODO: SYSTEMIC FIX PENDING (BK Evolution)
                # Problem: self.name is translated via __() but used as an internal key.
                # In non-English locales (e.g. Chinese), self.name becomes "戈尔迪" instead
                # of "goldie", breaking achievement keys and any dict lookups.
                # Temporary workaround: derive English key from portrait field.
                # Proper fix: add a `key` attribute to NPC (and all entity classes) to
                # separate display name (name) from immutable internal identifier (key).
                # See audit report in conversation history for full scope.
                if self.portrait and self.portrait.startswith("side "):
                    base = self.portrait[5:].split()[0]
                else:
                    base = self.name.lower()
                eng_name = name_map.get(base, base)
                unlock_achievement("trainer " + eng_name)

        def can_upgrade(self):
            if self.upgrade_level + 1 in shop_upgrades.keys():
                if shop_upgrades[self.upgrade_level + 1][0] <= game.chapter:
                    return True

            return False

        def upgrade_shop(self, cost, upgrade, forced=False): # Where cost and upgrades are tuples
            if forced or MC.has_resource(*cost):
                if not forced:
                    MC.spend_resource(*cost)
                self.upgrade_level += 1
                self.stock_modifiers[upgrade[0]] += upgrade[1]
            else:
                renpy.call_screen("OK_screen", __("Missing resources"), __("You are missing the resources needed for this upgrade (%s %s).") % (cost[1], cost[0]))
                return False

        def get_restock_cost(self, chapter):
            """EN: Return restock cost for a given chapter. BK Evolution data-driven.
               ZH: 返回给定章节的补货成本。BK Evolution 数据驱动。"""
            restock_cost = getattr(self, 'restock_cost', None)
            if restock_cost:
                return restock_cost.get(chapter)
            # Legacy fallback
            if self == shop:
                return shop_restock_cost["shop"].get(chapter)
            elif hasattr(self, 'minion_type') and self.minion_type:
                return shop_restock_cost["minion_merchant"].get(chapter)
            else:
                return shop_restock_cost["city_merchant"].get(chapter)

        def get_upgrade_info(self):
            """EN: Return upgrade info tuple (chapter, cost, upgrade) if available.
               ZH: 返回升级信息元组 (章节, 成本, 加成)，如果有的话。"""
            if self.upgrade_level + 1 in shop_upgrades:
                return shop_upgrades[self.upgrade_level + 1]
            return None

        def restock(self, once_a_day=True, update_flag = True): # For shop NPCs

            self.items = []
            shop_type = getattr(self, 'shop_type', None)

            # BK Evolution: Shop economy modifiers
            _stock_bonus = shop_chapter_stock_bonus.get(game.chapter, 0)
            _price_multiplier = shop_chapter_price_multiplier.get(game.chapter, 1.0) * (1.0 + shop_time_pressure)

            if shop_type == "minion" or (not shop_type and self in minion_merchants):
                # Minion merchant logic
                restock_formula = getattr(self, 'restock_formula', None)
                if restock_formula:
                    shop_mix = []
                    for typ, formula in restock_formula.items():
                        number = parse_dice_formula(formula) + self.stock_modifiers.get(typ, 0) + shop_chapter_modifiers[game.chapter].get(typ, 0) + _stock_bonus
                        shop_mix.append((typ, number))
                else:
                    shop_mix = [(typ, parse_dice_formula(shop_item_number["minion"][typ]) + self.stock_modifiers[typ] + shop_chapter_modifiers[game.chapter][typ] + _stock_bonus) for typ in ["minion", "item"]]

                for typ, number in shop_mix:
                    if number > 0:
                        if typ == "minion":
                            self.items += get_rand_minion(self.minion_type, nb=number)
                        else:
                            for i in range(number):
                                self.items.append(get_rand_item(rank="M"))

                if self.flags["extractor1 unlock"]:
                    if dice(6) >= 4:
                        self.items.append(extractor_items["extractor1"].get_instance())

                if self.flags["extractor2 unlock"]:
                    if dice(6) >= 5:
                        self.items.append(extractor_items["extractor2"].get_instance())

            elif shop_type in ("general", "specialist") or (not shop_type and (self == shop or self in city_merchants)):
                # Item merchant logic (general + specialist)

                restock_formula = getattr(self, 'restock_formula', None)
                if restock_formula:
                    shop_mix = []
                    for qual, formula in restock_formula.items():
                        number = parse_dice_formula(formula) + self.stock_modifiers.get(qual, 0) + shop_chapter_modifiers[game.chapter].get(qual, 0) + _stock_bonus
                        shop_mix.append((qual, number))
                else:
                    if self == shop:
                        shop_mix = [(qual, parse_dice_formula(shop_item_number["shop"][qual]) + self.stock_modifiers[qual] + shop_chapter_modifiers[game.chapter][qual] + _stock_bonus) for qual in all_qualities]
                    else:
                        shop_mix = [(qual, parse_dice_formula(shop_item_number["city"][qual]) + self.stock_modifiers[qual] + shop_chapter_modifiers[game.chapter][qual] + _stock_bonus) for qual in all_qualities]

                # BK Evolution: item type weights support
                item_type_weights = getattr(self, 'item_type_weights', None)

                def _pick_item(qual):
                    if item_type_weights:
                        candidates = [it for it in district.items[qual] if it.type.name in self.item_types]
                        if candidates:
                            weighted = [(it, item_type_weights.get(it.type.name, 1.0)) for it in candidates]
                            it = weighted_choice(weighted)
                            if it:
                                return it.get_instance()
                        return False
                    else:
                        return get_rand_item(qual, item_types=self.item_types)

                for quality, number in shop_mix:
                    if number > 0:
                        for i in range(number):
                            it = _pick_item(quality)
                            while not (it or quality == "junk"):
                                quality = all_qualities[all_qualities.index(quality)-1]
                                it = _pick_item(quality)
                            if it:
                                self.items.append(it)

                # Data-driven special items (BK Evolution)
                special_items = getattr(self, 'special_items', [])
                for spec in special_items:
                    if spec.get("condition") == "always":
                        count = spec.get("count", 1)
                        for _ in range(count):
                            if spec.get("method") == "rand_item":
                                it = get_rand_item(spec.get("quality"))
                            elif spec.get("method") == "instance":
                                it = globals()[spec.get("item_id")].get_instance()
                            if it:
                                self.items.append(it)
                    elif spec.get("condition") == "story_flag":
                        if story_flags.get(spec.get("flag")):
                            dice_count = parse_dice_formula(spec.get("dice", "1"))
                            for _ in range(dice_count):
                                it = globals()[spec.get("item_id")].get_instance()
                                if it:
                                    self.items.append(it)
                    elif spec.get("condition") == "dice":
                        if dice(100) <= spec.get("chance", 0):
                            it = globals()[spec.get("item_id")].get_instance()
                            if it:
                                self.items.append(it)

                # Legacy fallback special items (for old saves without special_items)
                if not special_items:
                    if self == shop:
                        self.items.append(get_rand_item("F"))
                        if story_flags["ninja hunt"]:
                            for _ in xrange(dice(3)+1):
                                self.items.append(makibishi.get_instance())
                    elif self == NPC_giftgirl and dice(100) <= 10:
                        self.items.append(wyvern_egg.get_instance())

                self.items.sort(key=lambda x: x.price)

            # BK Evolution: Apply price multiplier to all items
            for it in self.items:
                it._price_multiplier = _price_multiplier

            # Track update
            if update_flag:
                self.updated = True

            if once_a_day:
                self.last_restock = calendar.time



#     class City(): # Note: Free girls should be transfered here from the game object

#         """This class is for the main city of Zan."""

#         def __init__():
#             self.effects = []
#             self.effect_dict = defaultdict(list)




    class Calendar(object):

        """This class manages the game calendar, day/night cycle, and updates."""

        def __init__(self):

            self.time = 1
            self.day = 1
            self.month = 1
            self.year = 1
            self.moon = None
            self.alarms = {}
            self.discounted = []
            self.scarce = []
            self.contracts = []
            self.active_contract = None

        def get_today(self, get_year=False):
            return self.get_date(self.time, get_year)

        def get_date(self, _time, get_year=False):

            year = 1 + (_time-1) // (28*12)

            year_time = 1 + (_time-1) % (28*12)

            month = 1 + (year_time-1) // 28

            day = 1 + (year_time-1) % 28

            if get_year:
                return str(year) + "/" + str(month) + "/" + str(day)
            else:
                return str(month) + "/" + str(day)

        def newday(self, number = 1):

            for i in range(number):

                self.time +=1

                if self.day != 28:
                    self.day +=1

                else:
                    self.day = 1

                    if self.month != 12:
                        self.month += 1

                    else:
                        self.month = 1
                        self.year += 1

            if self.time % 7 == 1 :
                # 通知 Mod: 新的一周开始 | Notify mods: week starting
                mod_api_v2.execute_hook(mod_api_v2.HOOK_WEEK_STARTING, week=(self.time - 1) // 7 + 1, time=self.time)
                self.updates()


        def updates(self, change_district=False): #This is the place where weekly updates are handled

            weekly_updates(change_district)

            return


        def get_weekday(self, day=None):

            if not day:
                day = self.day

            wd = day % 7 -1

            return weekdays[wd]


        def find_next(self, weekday, offset=1): # find the next day which will be a specific weekday
            day = self.day + offset

            while not self.get_weekday(day) == weekday:
                day += 1

            return day
            

        def get_discount(self, source, target): # Where source, target are "gold" or a Resource object

            if source == "gold" and target.name in self.discounted:
                return 0.75
            elif source == "gold" and target.name in self.scarce:
                return 1.25
            elif target == "gold" and source.name in self.discounted:
                return 0.75
            elif target == "gold" and source.name in self.scarce:
                return 1.25
            else:
                rate = 1.0

                if source != "gold":
                    if source.name in self.discounted:
    #                    renpy.notify("found " + source + "in discounts 1")
                        rate *= 3/4.0
                    if source.name in self.scarce:
    #                    renpy.notify("found " + source + "in scarce 1")
                        rate *= 3/2.0
                if target != "gold":
                    if target.name in self.discounted:
    #                    renpy.notify("found " + source + "in discounts 2")
                        rate *= 3/2.0
                    if target.name in self.scarce:
    #                    renpy.notify("found " + source + "in scarce 2")
                        rate *= 3/4.0

                return rate

        def set_alarm(self, _time, _event):

            # Story Events

            if is_string(_event): # Creates generic event on the fly if needed. Does not take arguments.
                _event = StoryEvent(label=_event, date=_time)
                daily_events.append(_event)

            elif isinstance(_event, StoryEvent):
                daily_events.append(_event)
                _event.date = _time

            # Old-style Events

            elif _time in self.alarms:
                self.alarms[_time].append(_event)

            else:
                self.alarms[_time] = [_event, ]

            debug_notify(__("Alarm set for %i (%s)") % (_time, _event.label))


        def play_alarms(self, date=None):

            event_list = []

            if not date:
                date = self.time

            # Event objects

            if date in self.alarms:

                event_list = self.alarms[date]

                del self.alarms[date]

            # StoryEvent objects

            for ev in daily_events:
                if ev.happens(type="day"):
                    event_list.append(ev)

            if event_list:
                event_list.sort(key=lambda x: x.order)
                renpy.call("display_events", event_list)

        def get_season(self):

            if self.month <= 3:

                return "winter"

            elif self.month <= 6:

                return "spring"

            elif self.month <= 9:

                return "summer"

            elif self.month <= 12:

                return "fall"

        def generate_contracts(self):
            self.contracts = copy.deepcopy(rand_choice(contract_templates, 3))
            for con in self.contracts:
                con.randomize()





    class Log(object): # One log object is created each day to track various events

        def __init__(self, time):

            self.time = time
            self.cust = 0
            self.cust_served = 0
            self.gold_made = 0
            self.dirt = 0
            self.upkeep = 0
            self.costs = 0
            self.net = 0
            self.date = __(calendar.get_weekday()) + __(", Y%s M%s D%s") % (str(calendar.year), str(calendar.month), str(calendar.day))
            self.report = ""
            self.events = []
            self.changes = ""
            self.track_dict = defaultdict(int)

        def track(self, k, v=1):
            self.track_dict[k] += v

        def filter(self, filter_text):
            if not filter_text:
                self.filtered_report = self.report
            else:
                renpy.notify(_("filtering"))
                report_lines = self.report.splitlines()
                filtered_report_lines = [line for line in report_lines if filter_text.lower() in line.lower()]
                self.filtered_report = "\n".join(filtered_report_lines)

        def get_filtered_report(self):
            try:
                return self.filtered_report
            except:
                return self.report

        def get_day_report(self):
            return get_day_report(self)

        def get_tonight_report(self):
            pass

        def check(self, k):
            return self.track_dict[k]

        def add_report(self, text):

            self.report += "\n" + text

        def add_event(self, event):

            self.events.append(event)

        def show_events(self):

            norollback()

            for event in self.events:

                renpy.checkpoint()

                if event == self.events[-1]:

                    renpy.choice_for_skipping()

                event.show_night()







### SECONDARY CLASSES ##

