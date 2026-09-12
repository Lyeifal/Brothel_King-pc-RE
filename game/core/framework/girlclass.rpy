####            GIRL CLASS FOR B KING             ####################################################
##        This is the girl class.                   ##################################################
##         Others classes and functions are         ##################################################
##             in separate files.                   ##################################################


init -2 python:

    ## EN: Load girl upkeep/workday mapping parameters from JSON (BK Evolution), fallback to hardcoded.
    ## ZH: 从 JSON 加载女孩维护/工作日映射参数（BK Evolution），否则使用硬编码。
    _gup_json = DataLoader.load_girl_upkeep_params()
    if _gup_json:
        workday_map_reverse = {int(k): v for k, v in _gup_json["workday_map_reverse"].items()}
        workday_map_normal = {int(k): v for k, v in _gup_json["workday_map_normal"].items()}
        upkeep_base_value = {int(k): v for k, v in _gup_json["upkeep_base_value"].items()}
        upkeep_modifier_step = {int(k): v for k, v in _gup_json["upkeep_modifier_step"].items()}
    else:
        workday_map_reverse = {100 : 50, 50 : 0, 0 : 100}
        workday_map_normal = {100 : 0, 50 : 100, 0 : 50}
        upkeep_base_value = {5 : 10, 4 : 8, 3 : 6, 2 : 4, 1 : 2, 0 : -2, -1 : -4, -2 : -6, -3 : -8, -4 : -10, -5 : -15}
        upkeep_modifier_step = {-20 : -6, -12 : -5, -8 : -4, -4 : -3, -2 : -2, -1 : -1, 0 : 0, 1 : 1, 2 : 2, 3 : 3, 4 : 4, 5 : 5}

## GIRLS GIRLS GIRLS! ##


    class Girl(EffectBearer): #Attributes: name, lastname, age, description, pictures, stats, status, inventory, character

        """This class is for free and working girls in the game. This should probably inherit from the NPC
        class, but I'm not using inheritance."""


## CONSTRUCTOR METHODS

        def __init__(self): # Note: Init is not finalised until the randomize method is called

            self.type = "girl"

            # Placeholder information (changed after girl creation)
            self.id = 0 # Changed externally when creating the girl (create_girl() / get_girls() functions)
            self.pack_name = ""
            self.path = ""
            self.ini = None
            self.portrait = None
            # self.files = [] # <Chris12 PackState - moved to GirlFilesDict />
            # self.pics = [] # <Chris12 PackState - moved to GirlFilesDict />

            # Experience and rep
            self.rank = 1
            self.level = 1
            self.xp = 0
            self.rep = 0
            self.defense = 0
            self.upgrade_points = 0
            self.perk_points = 4
            self.original_price = 0
            self.jp = {
                        "waitress" : 0,
                        "dancer" : 0,
                        "masseuse" : 0,
                        "geisha" : 0,
                        "service" : 0,
                        "sex" : 0,
                        "anal" : 0,
                        "fetish" : 0
                        }
            self.job_level = {
                        "waitress" : 0,
                        "dancer" : 0,
                        "masseuse" : 0,
                        "geisha" : 0,
                        "service" : 0,
                        "sex" : 0,
                        "anal" : 0,
                        "fetish" : 0
                        }
            self.log = {} # Dictionary including all girl logged stats

            # Traits, Perks, Items and effects
            self.traits = []
            self.perks = []
            self.archetypes = copy.copy(archetype_dict) # Perk archetypes (as defined in BKperks.rpy)

            self.items = []
            self.equipped = []
            self.slots = girl_inventory_slots

            self.effects = []
            self.effect_dict = defaultdict(list)
            self.current_food_effect = defaultdict(bool)

            # Job and statuses
            self.resting = False # Forces a resting status on the girl regardless of schedule
            self.job = None # Girl's assigned job. She will still rest or quest according to her schedule
            self.old_job = None # To be phased out, kept here for possible backwards compatibility

            self.has_worked = False
            self.farm = False # Farm girls should be in 'farm.girls'. This shouldn't be needed: to be deleted if useless
            self.away = False # Indicates that the girl is away from the Brothel and unaffected by any brothel event or effect
            self.assignment = None
            self.street_days = 0

            self.exhausted = False # Indicates the girl is exhausted and cannot return to work until her energy is fully recovered
            self.hurt = 0 # If > 0, indicates the number of days the girl will stay incapacitated (before effects are applied)
            self.ran_away_counter = 0

            self.work_whore = False
            self.block_schedule = False
            self.farm_lock = False
            self.job_sort_value = 100
            self.workdays = {"Monday" : 100, "Tuesday" : 100, "Wednesday" : 100, "Thursday" : 100, "Friday" : 100, "Saturday" : 100, "Sunday" : 100} # Changed upon randomization

            self.badge = ""
            self.refused_populations = defaultdict(bool)

            # Interactions
            self.love = 0
            self.fear = 10 # Girls fear you at the beginning
            self.mood = 0

            self.MC_interact = False
            self.MC_interact_counters = defaultdict(int)
            self.MC_relationship_level = 0 # 0: stranger, 1: friend, 2: love interest, 3: girlfriend, 4: lover, 5: job offer
            self.MC_lied = None
            self.promised = False

            self.has_trained = []
            self.training_days = defaultdict(bool)
            self.magic_training = "balanced"

            self.spoiled = False
            self.spoil_points = 0
            self.terrified = False
            self.terrify_points = 0

            self.friends = []
            self.rivals = []
            self.g_compatibility = defaultdict(bool)

            self.custom_dialogue_label = None
            self.custom_tags = {}
            self.custom_dialogue = {}

            # Sexuality
            self.naked = False
            self.pos_fixations = []
            self.neg_fixations = []

            # Background
            self.location = ""
            self.origin = None
            self.hobbies = []
            self.likes = {"color" : None, "food" : None, "drink" : None}
            self.dislikes = {"color" : None, "food" : None, "drink" : None}
            self.notebook_unlocks = [] # stores status of notebook display for better performance

            self.flags = defaultdict(bool)

            # Phase 2.1: Component delegation (see game/core/framework/girl/)
            self._base = GirlBase(self)
            self._stats = GirlStats(self)
            self._traits = GirlTraits(self)
            self._pictures = GirlPictures(self)
            self._economy = GirlEconomy(self)
            self._mood = GirlMood(self)
            self._schedule = GirlSchedule(self)
            self._relationships = GirlRelationships(self)
            self._dialogue = GirlDialogue(self)
            self._logging = GirlLogging(self)
            self._sex = GirlSex(self)
            self._items = GirlItems(self)
            self._training = GirlTraining(self)
            self._effects = GirlEffects(self)
            self._generation = GirlGeneration(self)

        def randomize(self, free=False, p_traits=None, n_trait=None, perks=None, force_original=False, level=1, personality=None, temp_list=None):
            return self._generation.randomize(free, p_traits, n_trait, perks, force_original, level, personality, temp_list)

        def is_unique(self): # Unique girls may only generate if none other already exists
            if self.init_dict["identity/unique"] or self.init_dict["cloning options/unique"]:
                return True
            return False

        ## Phase 2.1: Delegated to GirlMood component ##
        def init_sanity(self):
            return self._mood.init_sanity()

        def rank_up_sanity(self):
            return self._mood.rank_up_sanity()

        def lose_sanity(self, cost):
            return self._mood.lose_sanity(cost)

        def get_sanity(self):
            return self._mood.get_sanity()

## Phase 2.1: Delegated to GirlMood component ##
        def sanity_warning(self): # Returns a message to display as narrator dialogue
            return self._mood.sanity_warning()


        def set_name(self): ## This creates the full name with or without lastname

            first, last = get_name(self.path)

            if self.original:
                if self.ini:
                    self.name = self.init_dict["identity/first_name"]
                    self.lastname = self.init_dict["identity/last_name"]
                    if not self.name and not self.lastname:
                        self.name, self.lastname = first, last
                else:
                    self.name, self.lastname = first, last

            else: # Clones will either receive _BK.ini settings as priority or option settings depending on option choice
                new_name = generate_name("girl")

                if not persistent.gp_name_customization and self.init_dict["identity/first_name"] != "?rand" and self.init_dict["identity/first_name"]: # If _BK.ini has priority
                    self.name = self.init_dict["identity/first_name"] # Automatically set to "?rand" if unspecified in _BK.ini
                elif persistent.keep_firstname:
                    self.name = first
                elif self.init_dict["identity/first_name"] != "?rand" and self.init_dict["identity/first_name"]:
                    self.name = self.init_dict["identity/first_name"] # Automatically set to "?rand" if unspecified in _BK.ini
                else:
                    self.name = new_name[0]

                if not persistent.gp_name_customization and self.init_dict["identity/last_name"] != "?rand": # If _BK.ini has priority
                    self.lastname = self.init_dict["identity/last_name"] # Automatically set to "?rand" if unspecified in _BK.ini
                elif persistent.keep_lastname:
                    self.lastname = last
                elif self.init_dict["identity/last_name"] != "?rand":
                    self.lastname = self.init_dict["identity/last_name"] # Automatically set to "?rand" if unspecified in _BK.ini
                else:
                    self.lastname = new_name[1]

            if self.name == "?rand" or not self.name:
                self.name = generate_name("girl")[0]

            if self.lastname == "?rand":
                self.lastname = generate_name("girl")[1]

            elif not self.lastname:
                self.lastname = ""

            self.set_fullname()

        def set_fullname(self):

            if self.init_dict["identity/inverted_name"]:
                self.fullname = self.lastname
                if self.name:
                    if self.fullname:
                        self.fullname += " "
                    self.fullname += self.name
            else:
                self.fullname = self.name
                if self.lastname:
                    if self.fullname:
                        self.fullname += " "
                    self.fullname += self.lastname

        def random_rename(self):
            self.name, self.lastname = generate_name("girl")
            self.set_fullname()

#             if self.lastname != "":
#                 self.fullname += " " + self.lastname

        def get_badge(self): # Returns the picture file name or None
            if not hasattr(self, 'badge') or self.badge not in badge_pics: # Sanity check
                self.badge = ""

            return self.badge

        def set_workdays(self): #Value is a percentage (0% = resting, 50% = working at half capacity, 100% = full capacity)

            i = calendar.day % 7

            self.workdays[weekdays[i-2]] = 0
            self.workdays[weekdays[i-3]] = 0

        def cycle_workday(self, day, reverse = False):

            if reverse:
                _wd = workday_map_reverse
            else:
                _wd = workday_map_normal

            self.workdays[day] = _wd[self.workdays[day]]

            renpy.restart_interaction()


        def update_files(self):
            #<Chris12 PackState>
            #Moved to GirlFilesDict - Should no longer be necessary
            return len(GirlFilesDict.get_pics(self.path)) > 0
            #</Chris12 PackState>


        def load_ini(self, search_for=None, skip_checks=False):

            self.init_dict = defaultdict(list)

            self.ini = GirlFilesDict.get_ini(self.path)

            if self.ini is not None:
                self.init_dict = read_init_file(self.ini, search_for=search_for, skip_checks=skip_checks)

                # Extract custom tags from init_dict
                self.custom_tags = {}
                for key, value in self.init_dict.items():
                    if key.startswith("custom tags/"):
                        tag_name = key[len("custom tags/"):]
                        if value:
                            self.custom_tags[tag_name] = make_list(value)

                # Apply custom tags to the global tag system and re-tag pictures
                if self.custom_tags:
                    register_custom_tags_for_pack(self.path, self.custom_tags)

                # Extract custom dialogue from init_dict
                self.custom_dialogue = {}
                for key, value in self.init_dict.items():
                    if key.startswith("custom dialogue/"):
                        topic = key[len("custom dialogue/"):]
                        if value:
                            self.custom_dialogue[topic] = make_list(value)

                # Register custom dialogue lines globally
                if self.custom_dialogue:
                    register_custom_dialogue_for_pack(self.path, self.custom_dialogue)

        def read_ini(self, section=None, key=None): # Debug function

            if section and key:
                return self.init_dict[section + "/" + key]
            elif section:
                return [[k, v] for k, v in self.init_dict.items() if k.startswith(section)]
            elif key:
                return [[k, v] for k, v in self.init_dict.items() if k.endswith(key)]
            elif self.ini:
                return self.init_dict
            else:
                return "No init file"

        def load_pics(self):
            #<Chris12 PackState>Moved to GirlFilesDict</Chris12 PackState>
            pass

        # Phase 2.1: Delegated to GirlPictures component
        def evaluate_girlpack(self):
            return self._pictures.evaluate_girlpack()

        def refresh_pictures(self, force_default=False, silent=False):
            self._pictures.refresh_pictures(force_default, silent)

        def create_char(self):
            self._pictures.create_char()

        def check_pictures(self):
            self._pictures.check_pictures()

        def generate_stats(self, sex=False): # regular stats are generated first, sx stats are generated after fixations

            if not sex:
                self.stats = []

                for stat in gstats_main:
                    if use_ini_skills:
                        self.stats.append(Stat(stat, "main", self, weight=self.init_dict["base skills/" + stat]))
                    else:
                        self.stats.append(Stat(stat, "main", self))
            else:
                self.sex_stats = []
                self.does = defaultdict(bool)

                for stat in gstats_sex:
                    self.sex_stats.append(Stat(stat, "sex", self))

        def adjust_level(self, level):
            self.level = level

            # Adjust rank
            while self.rank * 5 < self.level:
                self.rank += 1

            # Adjust XP and REP

            self.xp = xp_to_levelup[self.level-1]
            self.rep += rep_to_rank[self.rank-1]

            # Get perk points

            self.perk_points += (self.level-1) + self.level // 5

            if self.level == 25:
                self.perk_points += 1

            #! No skill points are distributed for now, see if it works

        def will_do_farm_act(self, act, mode=None):
            return self._training.will_do_farm_act(act, mode)

        def will_rebel_in_farm(self, train_mode, reaction):
            return self._training.will_rebel_in_farm(train_mode, reaction)

        def farm_beg_test(self):
            return self._training.farm_beg_test()


        def will_rebel_in_farm(self, train_mode, reaction):

            if train_mode == "gentle":
                return False

            if self.is_("very dom"):
                diff = 200
            elif self.is_("dom"):
                diff = 100
            elif self.is_("very sub"):
                diff = 0
            elif self.is_("sub"):
                diff = 50

            if train_mode == "tough":
                diff -= 25
            elif train_mode == "hardcore":
                diff += 25

            if reaction == "accepted":
                diff -= 25
            elif reaction == "refused":
                diff += 25

            if dice(100) < (diff - self.get_love()//2 - self.get_fear() - self.get_stat("obedience")): # Fear impacts rebel chances more than love
                return True
            return False

        def farm_beg_test(self): # Determines if the girl will beg not to go to the farm
            r = dice(10)

            r -= self.get_stat("obedience") // 50

            if self.is_("very sub"):
                r += 2
            elif self.is_("sub"):
                r += 1
            elif self.is_("very dom"):
                r -= 1

            if self.is_("very modest"):
                r += 2
            elif self.is_("modest"):
                r += 1
            elif self.is_("very lewd"):
                r -= 1

            if farm.knows["weakness"][self]:
                r += 1

            if r >= 10:
                return True
            else:
                return False


        # Phase 2.1: Delegated to GirlSex component
        def will_do_sex_act(self, sex_act, use_desc=False):
            return self._sex.will_do_sex_act(sex_act, use_desc)

        def toggle_sex_act(self, sex_act):
            return self._sex.toggle_sex_act(sex_act)


        def does_anything(self): ## Tests if the girl has any activated sex act. She will be excluded from whoring if she isn't.

            for act in all_sex_acts:
                if self.does[act]:
                    return True

            return False

        def will_do_anything(self): ## Tests if the girl is open to a sex act. She will be excluded from the whore job if she isn't.

            for act in all_sex_acts:
                if self.will_do_sex_act(act):
                    return True

            return False

        def count_available_sex_acts(self, discovered=True, extended=True): # unused
            if extended:
                acts = extended_sex_acts
            else:
                acts = all_sex_acts

            if discovered:
                return sum(1 for act in acts if (self.will_do_sex_act(act) and self.personality_unlock[act]))
            return sum(1 for act in acts if self.will_do_sex_act(act))

        def get_trainable_sex_acts(self):
            available_acts = []
            _debug = ""

            for act in extended_sex_acts:
                if training_test_dict[act]:
                    for cond, pref in training_test_dict[act]:
                        if compare_preference(self, cond, pref) and self.personality_unlock[act] != 0:
                            _debug += act + ": No cond "
                            available_acts.append(act)
                            break
                        elif not compare_preference(self, cond, pref):
                            _debug += act + ": %s is not %s " % (cond, pref)
                        elif not self.personality_unlock[act]:
                            _debug += act + ": No unlock "
                        else:
                            _debug += act + ": ???"
                else:
                    _debug += act + ": No cond "
                    available_acts.append(act)

            return available_acts

        def count_activated_sex_acts(self):
            return sum(1 for act in all_sex_acts if self.does[act])

        def has_activated_sex_acts(self): # Checks if the girl has any sex acts activated
            for act in all_sex_acts:
                if self.does[act]:
                    return True

            return False

        # Phase 2.1: Delegated to GirlSex component
        def refresh_sex_acts(self):
            return self._sex.refresh_sex_acts()

        def activate_sex_act(self, sex_act):
            return self._sex.activate_sex_act(sex_act)

        def deactivate_sex_act(self, sex_act):
            return self._sex.deactivate_sex_act(sex_act)


        def get_sex_act_modifier(self, sex_act = "all"):

            modifier = self.get_effect("change", "all sex acts requirements")

            if sex_act in extended_sex_acts:
                modifier += self.get_effect("change", sex_act + " requirements") # Unused for now

            return modifier


        # Phase 2.1: Delegated to GirlTraits component
        def generate_traits(self, p_traits=None, n_trait=None):
            return self._traits.generate_traits(p_traits, n_trait)



## Get methods

        def get_name(self):
            return self.fullname

        def get_pic(self, tags, alt_tags1 = None, alt_tags2 = None, alt_tags3 = None, and_tags = None, not_tags = None, strict = False, and_priority=True, naked_filter=False, attempts=0, soft=False, hide_farm=False, pref_filter=False, allow_lesbian=False, always_stock=False, horizontal=False, vertical=False):
            return self._pictures.get_pic(tags, alt_tags1, alt_tags2, alt_tags3, and_tags, not_tags, strict, and_priority, naked_filter, attempts, soft, hide_farm, pref_filter, allow_lesbian, always_stock, horizontal, vertical)

        def get_pic_not_tags(self, tags, alt_tags1 = None, alt_tags2 = None, alt_tags3 = None, and_tags = None, not_tags = None, strict = False, and_priority=True, naked_filter=False, attempts=0, soft=False, hide_farm=False, pref_filter=False, allow_lesbian=False, always_stock=False):
            return self._pictures.get_pic_not_tags(tags, alt_tags1, alt_tags2, alt_tags3, and_tags, not_tags, strict, and_priority, naked_filter, attempts, soft, hide_farm, pref_filter, allow_lesbian, always_stock)

        # Phase 2.1: Delegated to GirlPictures component
        def get_pic_by_name(self, filename):
            return self._pictures.get_pic_by_name(filename)

        def get_fix_pic(self, act=None, fix=None, and_tags=None, not_tags=None, hide_farm=True, naked_filter=False, pref_filter=True, attempts=0, allow_lesbian=False, always_stock=False, strict=False):
            return self._pictures.get_fix_pic(act, fix, and_tags, not_tags, hide_farm, naked_filter, pref_filter, attempts, allow_lesbian, always_stock, strict)


        def test_fix(self, name, unlock=False, feedback=False):
            return self._sex.test_fix(name, unlock, feedback)

        def check_fix(self, fix_name):
            return self._sex.check_fix(fix_name)

        def get_sex_attitude(self, act=None, fix=None): # Measures how much a girl enjoys a particular sex act or fixation
            return self._sex.get_sex_attitude(act, fix)


        # Phase 2.1: Delegated to GirlEconomy component
        def get_price(self, operation, raw=False):
            return self._economy.get_price(operation, raw)


        def get_med_upkeep(self):

            eff = self.get_effect("boost", "upkeep")

            av_stat = (sum(s.value for s in self.stats) + sum(s.value for s in self.sex_stats)) // (len(self.stats) + len(self.sex_stats))

            return round_int(av_stat * eff * (2 ** (self.rank-1))) # Testing upkeep formula suggested by Chris12 (exponential upkeep growth) #! Change from 1.5 to 2


        def adjust_upkeep(self):

            if self.upkeep > 0: # 0 upkeep happens when she is punished.
                self.upkeep = round_int(self.get_med_upkeep() + self.upkeep_ratio*self.rank)

            return

        def update_upkeep_ratio(self):
            self.upkeep_ratio = (self.upkeep - self.get_med_upkeep())/float(self.rank)

        def get_upkeep_threshold(self, step): # Only use integers from +5 to -5 as step values, or "min".
            if step == "min" or step == -6:
                return self.get_med_upkeep() // 4

            _bv = upkeep_base_value[step]

            r = self.get_med_upkeep() + (_bv * self.rank * 2 ** self.rank)

            if step <= 0: # To emulate the legacy switch from >= to >
                r += 1
            
            return r

        def get_upkeep_modifier(self):

            m = self.get_med_upkeep()

            if self.upkeep >= self.get_upkeep_threshold(5):
                modifier = +5

            elif self.upkeep >= self.get_upkeep_threshold(4):
                modifier = +4

            elif self.upkeep >= self.get_upkeep_threshold(3):
                modifier = +3

            elif self.upkeep >= self.get_upkeep_threshold(2):
                modifier = +2

            elif self.upkeep >= self.get_upkeep_threshold(1):
                modifier = +1

            elif self.upkeep >= self.get_upkeep_threshold(0):
                modifier = 0

            elif self.upkeep >= self.get_upkeep_threshold(-1):
                modifier = -1

            elif self.upkeep >= self.get_upkeep_threshold(-2):
                modifier = -2

            # Higher mood penalties incurred for very negative upkeep

            elif self.upkeep >= self.get_upkeep_threshold(-3):
                modifier = -4

            elif self.upkeep >= self.get_upkeep_threshold(-4):
                modifier = -8

            elif self.upkeep >= self.get_upkeep_threshold(-5):
                modifier = -12

            else:
                modifier = -20


            if modifier > 0:
                modifier += self.get_effect("change", "positive upkeep mood modifier")
            elif modifier < 0:
                modifier += self.get_effect("change", "negative upkeep mood modifier")

            return modifier

        def get_next_upkeep_step(self):
            m = self.get_upkeep_modifier()
            _st = upkeep_modifier_step[m]
            
            if _st < 5:
                return self.get_upkeep_threshold(_st + 1)
            else:
                return get_upkeep_threshold(5)

        def get_previous_upkeep_step(self):
            m = self.get_upkeep_modifier()
            _st = upkeep_modifier_step[m]
            
            if _st > -6:
                return max(self.get_upkeep_threshold(_st - 1), self.get_upkeep_threshold("min"))
            else:
                return self.get_upkeep_threshold("min")






## Items

        # Phase 2.1: Delegated to GirlItems component
        def equip(self, item):
            return self._items.equip(item)

        # Phase 2.1: Delegated to GirlItems component
        def unequip(self, item):
            self._items.unequip(item)

            # Restores item effects if girl had boost item type effects
            boost = self.get_effect("boost", item.type.name.lower())

            if boost != 1.0: # Reminder: effects have been previously deep copied on equip
                for eff in item.effects:
                    eff.value /= boost

            self.refresh_sex_acts() # Checks if sex_acts can still be done

        def get_equipped(self, slot):

            for it in self.equipped:
                if it.slot == slot:
                    return it
            return False

        def use_item(self, item, night=False):
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)

            changes = NightChangeLog(title=item.name)

            debug_notify("Using " + item.name + " on " + self.fullname, pic=self.portrait)

            used = False
            r = ""

            for e in item.effects:
                if e.type == "gain":
                    c = self.add_effects(e)
                    if c:
                        changes.add(e.target.capitalize() + _(" : %s") % plus_text(c))
                    used = True

                elif e.type == "change": # In case of direct usage, the change will last only for one turn or the item duration
                    if item.type.name == "Food": # Prevents stacking food effects for the same stat
                        if self.current_food_effect[e.target]:
                            changes.add(_("%s: %s (expired)") % (self.current_food_effect[e.target].target.capitalize(), plus_text(-self.current_food_effect[e.target].value)))
                            self.remove_effects(self.current_food_effect[e.target])

                        self.current_food_effect[e.target] = e # Stores the object used to remove the effect in case another food is absorbed

                    if e.duration > 0:
                        c = self.add_effects(e, expires = calendar.time + e.duration)
                        if c:
                            changes.add(_("%s: %s (duration: %s days)") % (e.target.capitalize(), plus_text(c), e.duration))
                    else:
                        c = self.add_effects(e, expires = calendar.time + 1)
                        if c:
                            changes.add(_("%s: %s") % (e.target.capitalize(), plus_text(c)))

                    used = True

                elif e.type in ("special", "instant"):
                    if e.target == "level":
                        if self.level < e.value:
                            self.xp = self.get_xp_cap()
                            self.level_up()
                            changes.add(_("Level: +1"), col=c_orange)
                            used = True
                        else:
                            notify(__("This item can only be used up to level %s") % e.value, pic=self.portrait)

                    elif e.target == "heal":
                        if not self.can_heal_from_item() and not night:
                            renpy.say("", __("Only one healing item can be used per day."))

                        elif self.hurt > 0:
                            c, _ = self.heal(e.value, from_item=True)
                            if c:
                                changes.add(__("Healing"), "header")
                                changes.add(__("Healed: %s") % plus_text(c))
                                if self.hurt <= 0:
                                    changes.add(__("(fully healed)"), col="good")
                                    if not night:
                                        renpy.say("", __("%s has been healed completely.") % self.name)
                                elif not night:
                                    renpy.say("", __("%s has been healed but still need some time to rest.") % self.name)
                                used = True
                        else:
                            notify(__("%s is in good health.") % self.name, pic=self.portrait)

                    # Virginity restoration
                    elif e.target == "virginity":
                        if not self.has_trait("Virgin"):
                            self.restore_virginity()
                            used = True

                    # Sanity restoration
                    elif e.target == "sanity":
                        self.init_sanity()
                        used = True

            if used:
                r = item.use_me()

                if r == "used_up" and item in self.items:
                    self.items.remove(item)
                    changes.add("(used up)", col="bad")

                norollback()

            if night:
                return r, changes
            return r

        def take(self, giver, obj):
            if not isinstance(obj, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % obj.name)

            self.items.append(obj)
            if obj.equipped:
                giver.unequip(obj)
            try:
                giver.items.remove(obj)
            except:
                pass

        def get_MC_relation(self):
            if self in MC.girls + farm.girls:
                return "slave"

            elif girl in game.free_girls:
                if self.MC_relationship_level == 0:
                        return "stranger"

                elif self.MC_relationship_level == 1:
                        return "friend"

                elif self.MC_relationship_level == 2:
                        return "love interest"

                elif self.MC_relationship_level == 3:
                        return "girlfriend"

                elif self.MC_relationship_level == 4:
                        return "lover"

                elif self.MC_relationship_level == 5:
                        return "lover"

            return "unknown"

        def receive_gift(self, item):
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)

            flower = False
            potion = False

            score = 1
            mod = 1.0

            for e in item.effects:
                if e.type == "gift":
                    score += self.personality.gift_likes[e.target]
                    mod = e.value

                elif e.type == "flower":
                    flower = True
                    break

                elif e.type == "potion":
                    potion = e.target
                    break


            if flower:
                if e.target == self.likes["color"]:
                    score += 4
                    self.personality_unlock["fav_color"] = True
                    renpy.say(self.char, __("Oh, you remembered my favorite color! You're so considerate..."))

                elif e.target == self.dislikes["color"]:
                    score += 0
                    self.personality_unlock["dis_color"] = True
                    renpy.say(self.char, __("Ah, em, thanks. You know, I don't like this color, but I appreciate the gesture."))

                else:
                    score += 2
                    renpy.say(self.char, __("Flowers! For me! Thank you..."))

                if self.MC_relationship_level == 2:
                    renpy.say(self.char, __("This is very romantic... Was there something you wanted from me?"))

                    r = menu(items = (("Actually...", None), ("Ask her out", True), ("Never mind", False)))

                    if r:
                        norollback()
                        self.MC_relationship_level = 3
                        self.track_event("MC girlfriend", arg=self.name)
                        test_achievement("girlfriends")
                        self.say("free_ask_out")

                    else:
                        norollback()
                        renpy.say(you, __("Hmm, no, not really."))
                        renpy.say(self.char, __("Oh... I see."))

            elif potion:
                if potion == "seduction":
                    if self not in game.free_girls:
                        return False

                    # NG+ - Potion of seduction
                    if self.MC_relationship_level < 1:
                        renpy.call("free_girl_friend", self)
                    elif self.MC_relationship_level < 2:
                        renpy.call("free_girl_love_interest", self)
                    elif self.MC_relationship_level < 3:
                        norollback()
                        self.MC_relationship_level = 3
                        self.track_event("MC girlfriend", arg=self.name)
                        test_achievement("girlfriends")
                        self.say("free_ask_out")
                    elif self.MC_relationship_level < 4:
                        renpy.call("free_girl_girlfriend", self)
                    elif self.MC_relationship_level < 5:
                        renpy.call("free_girl_job_request", self)
                    else:
                        renpy.say(narrator, __("Already at the maximum relationship level. This potion had no effect."))
                    # /NG+

            else:
                if score >= 4:
                    renpy.say(self.char, __("Oh, I love it so much!!! Thank you, thank you!"))

                elif score >= 2:
                    renpy.say(self.char, __("It's nice! Thanks for thinking about me."))

                elif score >= 0:
                    renpy.say(self.char, __("Ah, em, thanks. It's an interesting... whatever it is, I guess."))

                else:
                    renpy.say(self.char, __("What the? Ew, take this away from me!"))

            if score >= 0:
                score *= mod

            self.change_love(score)
            self.change_mood(score)

            return score


## Phase 2.1: Delegated to GirlDialogue component ##
        def test_say(self):
            return self._dialogue.test_say()


## Jobs

        def will_do(self, job, silent=False):

            if job == "whore":

                modifier = self.get_sex_act_modifier()

                if self.get_stat("obedience") + self.get_stat("libido") >= (whore_test / cheat_modifier["stats"]) + modifier:
                    if self.will_do_anything():
                        return True
                    elif not silent:
                        notify("No sex acts available for whoring", pic=self.portrait)
                elif not silent:
                    notify("Libido/Obedience too low", pic=self.portrait)
                return False

            else:
                return True

        def set_job(self, job, forced=False):

            if self.will_do(job):

                self.old_job = self.job # Obsolete

                self.job = job

                if job == "whore" or (job in all_jobs and self.work_whore):
                    if not self.has_activated_sex_acts():
                        for stat in gstats_sex:
                            self.activate_sex_act(stat)

                self.job_sort_value = job_sort_value[job]

                if not job or job == "rest":
                    self.resting = True
                    self.work_whore = False
                    if forced:
                        self.away = False # For the 'force rest' cheat
                else:
                    self.resting = False

                return True

            else:
                return False

        def set_rest(self):

            if self.resting:
                return False

            self.resting = True

            self.job_sort_value = job_sort_value[job]

            return True


        def works_today(self, check_autorest=False):

            day = calendar.get_weekday()

            if self.job and not (self.resting or self.away or self.farm or self.exhausted or self.hurt > 0):
                if self.workdays[day] > 0:
                    if not check_autorest or self.energy > autorest_limit[self] or self.energy >= self.get_stat_max("energy"):
                        return self.workdays[day]

            return False

        def get_schedule(self): # Returns a list of values for the seven days of the week
            return [self.workdays[d] for d in weekdays]

        def load_schedule(self, schedule):
            i = 0
            for day in weekdays:
                self.workdays[day] = schedule[i]
                i += 1

        # Phase 2.1: Delegated to GirlSchedule component (implementations moved)
        def get_status(self):
            return self._schedule.get_status()

        def get_status_summary(self):
            return self._schedule.get_status_summary()


        def get_max_cust_served(self, job="current"):

            if job == "current":
                job = self.job

            # Unavailable (returns 0 if she can't have any more interactions)
            if not job or job == "rest" or self.away or self.hurt > 0:
#                renpy.say(self.char, "My capacity is zero (" + self.fullname + ")")
                return 0

            if job == "whore":
                cust_cap = self.get_max_interactions()

            else:
                stats = perform_job_dict[job + "_stats"]

                main_stat, weight = stats[0]

                cust_cap = job_base_customer + ((self.get_stat(main_stat) + self.get_stat("constitution")) / float(job_customer_points)) + self.get_effect("change", "job customer capacity")

                #<Chris Job Mod: >
                if game.has_active_mod("chrisjobmod") and job in all_jobs:
                    cust_cap *= act_max_customers_modifier[job]
                    if cust_cap < job_base_customer:
                        cust_cap = job_base_customer
                #</Chris Job Mod>

            # Reduce capacity if the girl is working half shift

            cust_cap = round_int(cust_cap * self.workdays[calendar.get_weekday()] / 100.0)

            # Halves capacity if girl is working and whoring

            if self.work_whore:
                cust_cap = round_int(cust_cap / 2)

            if cust_cap < 1:
                cust_cap = 1

#            renpy.say(self.char, "My capacity is " + str(cust_cap) + " for " + job + " (" + self.fullname + "")

            return cust_cap

        def get_max_interactions(self):
            inter = whore_base_customer + round_int((self.get_stat("libido") + self.get_stat("constitution")) / float(whore_customer_points) + self.get_effect("change", "whore customer capacity"))

            # At least 1 interaction is guaranteed
            return max(inter, 1)

        def get_interaction_modifer(self): # Spent interactions are multiplied by this number (higher modifier=less interactions)

            mod = 100 // self.workdays[calendar.get_weekday()]

            if self.work_whore and self.job in all_jobs:
                mod = mod * 2

            return mod

        def reset_interactions(self):

            self.old_interactions = self.interactions # Used for triggering the libido event

            self.interactions = self.get_max_interactions()

            self.MC_interact_counters = defaultdict(int)

            # Updates memories of rewards and punishments

            self.forgets()

            # Resets naked status to False, except if girl has the naturist perk

            if not self.get_effect("special", "naked"):
                self.naked = False

            # Resets farm promise

            self.farm_lock = False


        # Phase 2.1: Delegated to GirlEconomy component
        def estimate_performance(self, sex_act):
            return self._economy.estimate_performance(sex_act)


        def get_xp(self, act, result, customers):
            return self._economy.get_xp(act, result, customers)

        def get_jp(self, act, result, customers, silent=False):
            return self._economy.get_jp(act, result, customers, silent)

        def get_rep(self, score, customers, first_customer=False):
            return self._economy.get_rep(score, customers, first_customer)

        # Phase 2.1: Delegated to GirlEconomy component
        def get_tip(self, act, result, customers, final_tip_change=0, first_customer=False, specials=[]):
            return self._economy.get_tip(act, result, customers, final_tip_change, first_customer, specials)

        def get_street_tip(self): # Returns average tip value for street whores
            return max(self.get_price("sell") // 100, tip_base) * cheat_modifier["gold"] * game.get_diff_setting("gold")

        def whore_on_street(self): # Runs every night a broken girl is on the street. Returns tip value.

            # 1. Get tip
            min_tip = self.get_street_tip() // 2

            tip = renpy.random.randrange(min_tip, min_tip*3) * self.get_effect("boost", "street whore tip")

            # 2. Degrade stats (Street whores erode their stats over time)
            for s in self.stats + self.sex_stats:

                eff = self.get_effect("change", "street whore skill erosion") # May be -1 or -2

                if self.get_stat(s.name) > 150:
                    chg = 1-dice(6+eff) # 0 to -5
                elif self.get_stat(s.name) > 75:
                    chg = 1-dice(5+eff) # 0 to -4
                elif self.get_stat(s.name) > 25:
                    chg = 1-dice(4+eff) # 0 to -3
                else:
                    chg = 1-dice(3+eff) # 0 to -2

                if chg:
                    self.change_stat(s.name, chg, silent=True)

            # 3. Chance of disappearance

            grace_period = 14 # Girls will not disappear during the grace period

            if self.streetdays < grace_period:
                pass
            elif self.street_roll <= 1 + (self.streetdays - grace_period)/10: # After the grace period, increasing chance of disappearance
                calendar.set_alarm(calendar.time + 1, StoryEvent("girl_disappeared", arg=self, type = "morning"))

            # Roll is generated the day prior to discourage save scumming. Boost values can be 3.0, 9.0, 27.0
            self.street_roll = dice(100 * self.get_effect("boost", "street whore security"))

            # 4. Counter and log
            self.street_days += 1
            self.today_street_tip = tip

            return tip


## Phase 2.1: Delegated to GirlMood component ##
        def get_energy_color(self):
            return self._mood.get_energy_color()

        def get_energy_ttip(self):
            return self._mood.get_energy_ttip()

        def tire(self, x): # Where x is a positive number (important)
            return self._mood.tire(x)


## Phase 2.1: Delegated to GirlMood component ##
        def get_hurt(self, x):
            return self._mood.get_hurt(x)

        def health_check(self):
            return self._mood.health_check()


        # Phase 2.1: Delegated to GirlMood component
        def change_energy(self, x):
            return self._mood.change_energy(x)

        def can_heal_from_item(self):
            return self._mood.can_heal_from_item()

        def heal(self, chg=1, from_item=False):
            return self._mood.heal(chg, from_item)

        def full_rest(self):
            self._mood.full_rest()

        def rest(self, context=None, mod=1):
            return self._mood.rest(context, mod)


## Stats, Traits, Perks

        def find_stat(self, stat_name): # Returns the Stat object for a given stat name
            for s in (self.stats+self.sex_stats):
                if s.name.lower() == stat_name.lower():
                    return s
            return False

        def get_stat(self, stat_name, raw=False):
            return self._stats.get_stat(stat_name, raw)


        def get_xp_cap(self):

            if self.level < self.rank * 5:
                cap = xp_to_levelup[self.level]
            else:
                cap = xp_to_levelup[self.rank * 5 - 1]

            return cap


        def get_jp_cap(self, job = "all"):

            if job == "all":

                cap = jp_to_level[self.rank - 1]

            elif self.job_level[job] < self.rank:

                cap = jp_to_level[self.job_level[job]]

            else:

                cap = jp_to_level[self.rank - 1]

            return cap


        def get_rep_cap(self): # Adds 0.99 to avoid strange back and forth effects where girls can rank up briefly then are pulled back by rep decay

            if self.rank < district.rank:
                cap = rep_to_rank[self.rank] + 0.99

            else:
                cap = rep_to_rank[district.rank] + 0.99
            return cap


        def has_trait(self, name):

            for t in self.traits:
                if t.name.lower() == name.lower():
                    return True

            else:
                return False


        def has_perk(self, name): # Where name is a string, not the perk object

            if name == None:
                return True

            for p in self.perks:

                if p.name.lower() == name.lower():
                    return True

            else:
                return False


        def add_trait(self, trait, _pos=None, forced=False, no_perks=False): # Where 'trait' is an object (important)

#            renpy.say("", "Adding " + trait.name)

            if not forced:
                for t in self.traits:
                    if t.name in trait.opposite or t.name == trait.name:
                        return False

            if _pos != None:
                self.traits.insert(_pos, trait)
            else:
                self.traits.append(trait)

            self.add_effects(trait.effects)

            if trait.archetype and self.perk_points > 0 and not no_perks:
                if self.archetypes[trait.archetype].unlocked:
                    self.perk_points -= 1
                    self.acquire_perk(self.archetypes[trait.archetype].get_perks(0)[0], forced=True)
                else:
                    self.perk_points -= 2
                    self.unlock_archetype(trait.archetype)

                # Sanity check: Perk points cannot go lower than 0 (for mods that add more Traits)
                self.perk_points = max(0, self.perk_points)

            return True


        def remove_trait(self, trait): # Where trait is a Trait object

            if trait in self.traits:
                self.traits.remove(trait)
                self.remove_effects(trait.effects)


        def list_effects(self):
            return self._effects.list_effects()

        def get_effect(self, type, target, raw=False, custom_scale=("factor", 0), change_cap=False):
            # raw=True means no additional brothel or world effects will be included. MUST if you expect to get a string value
            return self._effects.get_effect(type, target, raw, custom_scale, change_cap)

        def remove_effects(self, effects):
            return self._effects.remove_effects(effects)


        def get_defense(self, fight = False, raw=False):

            defense = self.get_effect("change", "defense", raw=raw) * self.get_effect("boost", "defense", raw=raw)

            return defense

        def add_shield(self):
            self.add_effects(shield_effect)

        def test_shield(self):

            # Shield code to be fixed later

            if self.get_effect("special", "shield", raw=True):

                self.remove_effects(shield_effect)
                notify(self.name + " was protected by a magic shield", pic=self.portrait)
                renpy.pause(0.5)

                return True

            elif brothel.get_effect("special", "shield"):

                spl = MC.has_spell(bshield_spell)

                notify(self.name + " was protected by a magic shield", pic=self.portrait)
                renpy.pause(0.5)

                if spl:
                    MC.deactivate_spell(spl)

                return True

            return False



        def average_stats(self, stats): #Unused with the new system

            ## Tests the weighted average of all stats

            score = 0
            totalw = 0

            for tup in stats:

                stat, weight = tup

                score += self.get_stat(stat) * weight
                totalw += weight

            score /= float(totalw)

            return score


        def test_stats(self, stats=None, diff=0, advanced_stats=None): # Result will range from total of positive max modifiers in stat_bonus (+9) to negative max modifiers for primary and secondary (-6). Advanced stats will feed a stat_list directly with more flexibility.

            if advanced_stats:
                stat_list = advanced_stats
            else:
                stat_list = [(stats[0][0], "primary"), (stats[1][0], "secondary"), (stats[2][0], "booster"), (stats[3][0], "booster")]

            score = 0

            for stat, _type in stat_list:

                if self.get_stat(stat) - diff >= 40: # Reduced the pos threshold for stats for now
                    score += stat_bonus[_type][0]

                elif self.get_stat(stat) - diff >= 20: # Reduced the pos threshold for stats for now
                    score += stat_bonus[_type][1]

                elif self.get_stat(stat) - diff >= 10:
                    score += stat_bonus[_type][2]

                elif self.get_stat(stat) - diff >= 0:
                    score += stat_bonus[_type][3]

                elif _type != "booster":
                    if self.get_stat(stat) - diff <= -40: # Reduced the neg threshold for stats for now
                        score -= stat_bonus[_type][0]

                    elif self.get_stat(stat) - diff <= -20: # Reduced the neg threshold for stats for now
                        score -= stat_bonus[_type][1]

                    elif self.get_stat(stat) - diff <= -10:
                        score -= stat_bonus[_type][2]

                    else:
                        score -= stat_bonus[_type][3]

            return round_int(score)


        def raise_stats(self, stats, silent=False):

            changes = []

            # Stat increases are stored as tuples (stat_name, %chance, max increase/decrease)

            for s, chance, value in stats:

                if dice(100) <= chance:

                    stat = rand_choice(s)

                    if value > 0: # A dice is rolled from 1 to value
                        if dice(250) > self.get_stat(stat, raw=True): # A skill check makes it harder to raise a stat the higher it gets
                            r = self.change_stat(stat, dice(value) * cheat_modifier["stats"] * game.get_diff_setting("stats"), silent=silent)
                            changes.append((stat, r))

                    elif value < 0:
                        if dice(250) < self.get_stat(stat, raw=True): # A skill check makes it harder to lower a stat the lower it gets
                            r = self.change_stat(stat, value / cheat_modifier["stats"], silent=silent) # Diff setting modifier only applies to stat gains
                            changes.append((stat, r))

            return changes

        def can_upgrade_stat(self, stat): # Where stat is an object

            _min, _max = self.get_stat_minmax(stat.name, raw = True)

            if stat.value >= _max:
                return False
            return True

        def upgrade_stat(self, stat, chg, silent=True):
            r = self.change_stat(stat, chg, apply_boost = False, silent=silent)

            self.upgrade_points -= r

            if r < chg:
                return False
            else:
                return True

        def get_max_stat_upgrade_points(self, stat):
            result = self.get_stat_minmax(stat, raw = True)[1] - self.get_stat(stat, raw = True)
            if result > 0:
                if result > self.upgrade_points:
                    result = self.upgrade_points
                return round_int(result)
            else:
                return 0

        def get_stat_max(self, stat_name, raw = False, custom_cap=None):
            return self.get_stat_minmax(stat_name, raw, custom_cap)[1]

        def get_stat_minmax(self, stat_name, raw = False, custom_cap=None):

            if stat_name in ("love", "fear"):
                _min = -125
                _max = 125

            elif stat_name == "mood":

                _min = -125
                _max = 125

            elif stat_name in ("rep", "rep_neg", "reputation"):

                _min = rep_to_rank[self.rank-1]
                _max = self.get_rep_cap()

            elif stat_name == "energy":

                _min = 0

                eff = self.get_effect("boost", "max energy")

                base = self.get_stat("constitution")+50

                _max = round(base * eff)

            elif stat_name == "xp":

                _min = 0
                _max = xp_to_levelup[self.rank * 5 - 1]

            elif stat_name == "jp":

                _min = 0
                _max = self.get_jp_cap()

            elif stat_name.capitalize() in gstats_main + gstats_sex:

                _min = 0

                max_eff = self.get_effect("change", stat_name.lower() + " max") + self.get_effect("change", "all skill max")

                if custom_cap: # Can set cap to a different value (for classes)
                    _max = custom_cap
                else: # Max cannot be be lower than current stat value
                    _max = max(self.rank * 50 + max_eff, self.get_effect("set", "all skill max"), self.get_stat(stat_name, raw=True))

                    if not raw:
                        eff = self.get_effect("change", stat_name.lower(), change_cap=True) + self.get_effect("change", "all skills", change_cap=True)

                        if stat_name.capitalize() in gstats_main:
                            eff += self.get_effect("change", "all main skills")
                        elif stat_name.capitalize() in gstats_sex:
                            eff += self.get_effect("change", "all sex skills")

                        _max += eff


            else:
                raise AssertionError(stat_name + " min/max not found.")

            return _min, round_int(_max)

        def stat_spillover(self, stat, chg, job=None): # Job must be specified for JP
            eff = self.get_effect("spillover", stat)

            if eff:
                # Targetting girls

                target_list = []

                if self in MC.girls:
                    if stat == "jp":
                        target_list = [g for g in MC.girls if g.job == job]
                    else:
                        target_list = MC.girls

                elif self in farm.girls:
                    target_list = farm.girls

                # Applying spillover effect

                if len(target_list) > 1:
                    chg = chg / (len(target_list) - 1)

                    for g in target_list:
                        if g != self:
                            if stat == "jp":
                                g.change_jp(chg*eff, job, apply_boost=False, spillover=False, silent=True) # spillover=False is needed to avoid an infinite feedback loop
                            else:
                                g.change_stat(stat, chg*eff, apply_boost=False, spillover=False, silent=True) # spillover=False is needed to avoid an infinite feedback loop


        def change_stat(self, stat, chg, apply_boost=True, spillover=True, custom_cap=None, silent=False, notify_prefix="", notify_suffix=""):
            return self._stats.change_stat(stat, chg, apply_boost, spillover, custom_cap, silent, notify_prefix, notify_suffix)

        def set_stat(self, stat, val):
            return self._stats.set_stat(stat, val)

        def average_skills(self, sk_list, mod=1.0):
            change_dict = self._stats.average_skills(sk_list, mod)

            for sk in sk_list:
                self.set_stat(sk, change_dict[sk])

        def shuffle_skills(self, sk_list, mod=1.0):

            t = 0

            for sk in sk_list:
                t += self.get_stat(sk, raw=True)

            # The points are spread out randomly in rounds (producing more pronounced variation)
            change_dict = {sk: 0 for sk in sk_list}

            while t > len(sk_list)*10:
                change_dict[rand_choice(sk_list)] += 10
                t -= 10

            while t > len(sk_list)*5:
                change_dict[rand_choice(sk_list)] += 5
                t -= 5

            while t > 0:
                change_dict[rand_choice(sk_list)] += 1
                t -= 1

            for sk in sk_list:
                self.set_stat(sk, change_dict[sk])

## XP, rank and Level up

        def change_xp(self, value, apply_boost = True, spillover=True, silent=False):

            # XP spillover (Bride perk: confession) - Boosts don't apply
            if spillover:
                self.stat_spillover("xp", value)

            _min, _max = self.get_stat_minmax("xp")

            if apply_boost:

                boost = self.get_effect("boost", "xp gains")

                boost += 0.05 * self.remembers("reward", "level up") # Boosts XP is she was rewarded before

                boost = reverse_if(boost, value) ## Reverses boost if decreasing stat

            else:
                boost = 1.0

            change = value * boost

            if _min > self.xp + change:

                change = _min - self.xp
                self.xp = _min

            elif _max < self.xp + change:

                change = _max - self.xp
                self.xp = _max

            else:
                self.xp += change

            if change and not silent: notify(_("XP: %s") % plus_text(change, color_scheme="xp"), pic=self.portrait) # Experimental

            return change


        def change_jp(self, value, job, apply_boost = True, spillover=True, announcement_delay=1, silent=False):

            # JP spillover (Bride perk: confession) - Boosts don't apply
            if spillover:
                self.stat_spillover("jp", value, job=job)

            _min, _max = self.get_stat_minmax("jp")

            if apply_boost:

                boost = self.get_effect("boost", "all jp gains") * self.get_effect("boost", job + " jp gains")

                boost += 0.05 * self.remembers("reward", "job up") # Boosts JP is she was rewarded before

                boost = reverse_if(boost, value)

            else:

                boost = 1.0

            change = value * boost

            if _min > self.jp[job] + change:

                change = _min - self.jp[job]
                self.jp[job] = _min

            elif _max < self.jp[job] + change:

                change = _max - self.jp[job]
                self.jp[job] = _max

            else:
                self.jp[job] += change

            while self.ready_to_job_up(job):
                self.job_up(job, announcement_delay=announcement_delay)

            if change and not silent: notify(_("%s JP: %s") % (__(job.capitalize()), plus_text(change, color_scheme="jp")), pic=self.portrait) # Experimental

            return change


        def level_up(self, forced = False, silent=False):

            if self.ready_to_level() or forced:

                if forced:
                    self.xp = self.get_xp_cap()

                if self.level < 25: # Hard-coded level cap
                    self.level += 1

                    self.upgrade_points += 5 + 5 * self.rank

                    if self.level == 25:
                        self.perk_points += 3
                        notify("Maximum level reached! +1 Perk Point", pic=self.portrait, col=c_lightgreen)
                    elif self.level%5 == 0:
                        self.perk_points += 2
                    else:
                        self.perk_points += 1

                    self.update_can_perk() # This is not checked dynamically for performance
                    # MC earns prestige when a girl levels up
                    MC.prestige += self.rank

                    if not silent:
                        self.track_event("level up", arg=self.level)

                    return True

            return False

        def debug_auto_level(self, chapter):
            if chapter > 6:
                ranks = 3
                levels = 20
            elif chapter > 4:
                ranks = 2
                levels = 15
            elif chapter > 2:
                ranks = 1
                levels = 10
            elif chapter > 1:
                ranks = 0
                levels = 5
            else:
                ranks = 0
                levels = 0

            ranks = ranks - self.rank
            levels = levels - self.level

            if levels > 0:
                for i in range(levels):
                    # Simulates gained skills
                    self.upgrade_points += 10*self.rank

                    # Auto level and rank up
                    self.auto_level_up(forced=True, silent=True)
                    if self.level % 5 == 0 and ranks > 0:
                        self.rank_up(forced=True, silent=True)
                        ranks -= 1


        def auto_level_up(self, forced = False, silent = False):

            if self.level_up(forced, silent):
                for stat in self.stats:
                    self.upgrade_stat(stat.name, self.upgrade_points/8.0)

        def rank_up(self, forced = False, silent=False):

            if self.ready_to_rank() or forced:
                if forced:
                    self.rep = rep_to_rank[self.rank]

                if self.rank < 5:
                    self.rank += 1
                    self.rank_up_sanity()

                if self.auto_upkeep:
                    self.adjust_upkeep()

                self.update_can_perk() # This is not checked dynamically for performance

                if not silent:
                    self.track_event("rank up", arg=rank_name[self.rank])

                #ADD rank up animation


        def job_up(self, job, forced = False, announcement_delay=0):

            if self.ready_to_job_up(job) or forced:

                if self.job_level[job] < 5:
                    self.job_level[job] += 1

                    primary, secondary, add1, add2 = job_up_dict[job]

                    self.change_stat(primary, job_up_change[self.job_level[job]][0], apply_boost = False)
                    self.change_stat(secondary, job_up_change[self.job_level[job]][1], apply_boost = False)
                    self.change_stat(add1, job_up_change[self.job_level[job]][2], apply_boost = False)
                    self.change_stat(add2, job_up_change[self.job_level[job]][2], apply_boost = False)

                    self.track_event("job up", arg=job)

                    calendar.set_alarm(calendar.time + announcement_delay, Event(label = "job_up", object = (self, job, self.job_level[job])))


        def ready_to_level(self):

            if self.level < self.rank * 5:

                if self.xp >= self.get_xp_cap():

                    return True

            return False

        def can_spend_upgrade_points(self):
            if self.upgrade_points >= 1:
                for stat in self.stats:
                    if self.can_upgrade_stat(stat):
                        return True
            return False


        def ready_to_rank(self):

            if self.rank < district.rank:

                if self.rep >= rep_to_rank[self.rank] * self.get_effect("boost", "new rank reputation requirement") and self.level >= self.rank * 5:

                    return True

            return False


        def ready_to_job_up(self, job):

            if job in (all_jobs + all_sex_acts):

                mylevel = self.job_level[job]

                if mylevel == 5:

                    return False

                elif self.jp[job] >= jp_to_level[mylevel] and mylevel < self.rank:

                    return True

            return False


        def unlock_archetype(self, archetype_name):
            if not self.archetypes[archetype_name].unlocked:
                self.archetypes[archetype_name].unlocked = True
                self.update_can_perk() # This is not checked dynamically for performance
                return True
            else:
                return False

        def can_acquire_perk(self, perk, context=None): # Where perk is an object
            if self.has_perk(perk.name):
                return False, "She already has that perk."

            if context == "perk_screen":
                points = perk_points
                perks = self.perks + new_perks
            else:
                points = self.perk_points
                perks = self.perks

            val = sum(1 for p in perks if p.archetype == perk.archetype)

            message = ""

            if not self.archetypes[perk.archetype].unlocked:
                message += perk.archetype + " is locked for now.\n"
            elif val < perk.value:
                message += str(perk.value) + " more perk" + plural(perk.value) + " must be unlocked first.\n"
            elif self.rank < perk.min_rank:
                message += self.name + " must be rank " + rank_name[perk.min_rank] + " before she can acquire this perk.\n"
            elif points < 1:
                message = self.name + " does not have enough points."
            else:
                return True, ""

            return False, message

        def update_can_perk(self): # 'can_perk' is used to trigger UI alerts

            self.can_perk = False

            # Can unlock perk tree
            if self.perk_points >= 2 and [a for a in self.archetypes.values() if not a.unlocked]:
                self.can_perk = True

            # Can unlock perk
            for perk in perk_dict.values():
                if self.can_acquire_perk(perk)[0]:
                    self.can_perk = True

        def acquire_perk(self, perk, forced=False): ## Where perk is an object
            if perk not in self.perks:
                if not forced:
                    if self.can_acquire_perk(perk)[0]:
                        self.perk_points -= 1
                    else:
                        return self.can_acquire_perk(perk, self.perk_points)

                self.perks.append(perk)
                self.add_effects(perk.effects)
                self.reset_sex_acts(first=False)

                if perk.level == 3:
                    unlock_achievement(perk.archetype)

                self.update_can_perk()

            return True, ""

        def refund_perks(self, min_level=0): # all perks above or equal to min_level will be refunded. Use min_level=0 to refund archetypes
            perk_points = 0

            for perk in list(self.perks):
                if perk.level >= min_level:
                    self.perks.remove(perk)
                    self.remove_effects(perk.effects)
                    self.reset_sex_acts(first=False)

                    perk_points += 1

            if min_level <= 0:
                for arch in archetype_dict.keys():
                    if self.archetypes[arch].unlocked:
                        self.archetypes[arch].unlocked = False
                        perk_points += 2

            self.perk_points += perk_points

            self.update_can_perk()

            return perk_points



        def check_combo_perks(self):

            for p in combo_perks:
                if not self.has_perk(p.name) and self.has_prerequisites(p):
                    self.perks.append(p)
                    self.add_effects(p.effects)

                    renpy.call_screen("OK_screen", title = p.name, message = self.name + " has learnt a new combo! " + p.description)



        def has_prerequisites(self, perk):

            if perk.prerequisite != None:

                for pre in perk.prerequisite:
                    if not self.has_perk(pre):
                        return False

            return True


        def get_perk(self, perk): ## Where perk is an object (important)

            for p in self.perks:
                if p.name == perk.name:
                    return p
            else:
                return False


        def get_perk_level(self, perk): ## Where perk is an object (important)

            p = self.get_perk(perk)

            if p:
                return p.level

            else:
                return 0

        def change_rep(self, chg, silent=False):

            _min, _max = self.get_stat_minmax("rep")

            boost = self.get_effect("boost", "reputation gains") * game.get_diff_setting("rep")

            boost += 0.05 * self.remembers("reward", "rank up") # Boosts REP is she was rewarded before

            boost = reverse_if(boost, chg)

            chg = get_change_min_max(self.rep, chg*boost, _min, _max)
#            renpy.say("", "Changing rep by " + str(chg))

            self.rep += chg

            if not silent: notify(_("Reputation: %s") % plus_text(int(chg)), col="rep", pic=self.portrait)

            return chg




## For MC / Girl interactions

        # Phase 2.1: Delegated to GirlDialogue component
        def generate_personality(self, personality=None, change=False):
            return self._dialogue.generate_personality(personality, change)

        def adjust_personality(self):
            return self._dialogue.adjust_personality()

        # Phase 2.1: Delegated to GirlDialogue component
        def generate_background(self, t2=0):
            return self._dialogue.generate_background(t2)
## Phase 2.1: Delegated to GirlDialogue component ##
        def unlock_NGP_personality_settings(self):
            return self._dialogue.unlock_NGP_personality_settings()

        def change_relationship(self, other_girl, chg):

            self.relations[other_girl] += chg

            if self.relations[other_girl] > 3 and other_girl not in self.friends:
                self.friends.append(other_girl)
                if other_girl in self.rivals:
                    self.rivals.remove(other_girl)

            elif self.relations[other_girl] <= 3 and other_girl in self.friends:
                self.friends.remove(other_girl)

            elif self.relations[other_girl] >= -3 and other_girl in self.rivals:
                self.rivals.remove(other_girl)

            elif self.relations[other_girl] < -3 and other_girl not in self.rivals:
                self.rivals.append(other_girl)
                if other_girl in self.friends:
                    self.friends.remove(other_girl)

            return self.get_friendship(other_girl)

        def get_compatibility(self, other_girl): # Calculates a score to see if the girl is an ally or a rival. Relationship scores are stored in a dictionary for faster processing
            if self.g_compatibility[other_girl] is False:
                # Calculates a score if none exists for this pairing
                self.g_compatibility[other_girl] = 0

                for attr in self.attributes:
                    for k, v in attribute_score_dict[attr].items():
                        if other_girl.is_(k):
                            self.g_compatibility[other_girl] += v

            if self.g_compatibility[other_girl] >= 4:
                return "good"
            elif self.g_compatibility[other_girl] <= -4:
                return "bad"
            else:
                return None

        def update_relationships(self): # Returns a list of all changed relationships

            # Clears previous relationships if a girl has left
            for g in self.friends:
                if g not in MC.girls + farm.girls:
                    self.friends.remove(g)
            for g in self.rivals:
                if g not in MC.girls + farm.girls:
                    self.rivals.remove(g)

            _girls = [g for g in MC.girls if not (g.away or g == self)]

            if len(_girls) < 1:
                return None

            other_girl = rand_choice(_girls)

            # while other_girl == self:
            #     other_girl = rand_choice(_girls)

            old_status = self.get_friendship(other_girl)

            if self.get_compatibility(other_girl) == "good":
                mod = 1
            elif self.get_compatibility(other_girl) == "bad":
                mod = -1
            else:
                mod = 0

            if self.get_effect("change", "making friends"):
                mod += self.get_effect("change", "making friends")
            if other_girl.get_effect("change", "making friends"):
                mod += other_girl.get_effect("change", "making friends")

            r = dice(6, 2) + mod

            if r >= 11:
                new_status = self.change_relationship(other_girl, 1)
                other_girl.change_relationship(self, 1)

            elif r <= 3:
                new_status = self.change_relationship(other_girl, -1)
                other_girl.change_relationship(self, -1)

            else:
                new_status = old_status

            if new_status != old_status:
                change = [self, other_girl, old_status, new_status]
            else:
                change = None

            return change


        def get_friendship(self, other_girl):

            if other_girl == self:
                return "self"
            elif self.relations[other_girl] > 3:
                return "friend"
            elif self.relations[other_girl] < -3:
                return "rival"
            else:
                return "normal"

        def init_after_acquire(self, refresh_pics=True):

            self.location = None
            self.set_job(None)
            self.set_workdays()

            if refresh_pics:
                self.refresh_pictures()

            self.log["acquired"] = calendar.time
            self.track_event("acquired", arg=self.name, silent=True)
            girl_status_dict = load_girl_status(MC.girls + farm.girls)

            autorest_limit[self] = autorest_limit["default"]

            # Restores relationships if there were any
            for other_girl in MC.girls + farm.girls:
                self.change_relationship(other_girl, 0)


        # Phase 2.1: Delegated to GirlSex component
        def generate_preferences(self):
            self._sex.generate_preferences()

            # Generate x skills according to preferences

            self.generate_stats(sex=True)

            ## Regulations (sanity check)

            # Naturist girls are at least comfortable about being naked
            if self.get_effect("special", "naked"):
                if self.preferences["naked"] < 0:
                    self.preferences["naked"] = 0

            # Virgin girls cannot be experienced with sx or group
            if self.has_trait("Virgin"):
                self.preferences["sex"]=base_reluctance["sex"]
                self.preferences["group"]=base_reluctance["group"]
                self.change_stat("sex", -250, silent=True)

            # Add limits to group and boosts to nkd?

            # NewGame+ settings

            if NGP_settings_dict["preferences1"].get():
                for act in ("naked", "service"):
                    self.change_preference(act, NGP_settings_dict["preferences1"].get(), fast=True, silent=True)

            if NGP_settings_dict["preferences2"].get():
                for act in ("sex", "anal"):
                    self.change_preference(act, NGP_settings_dict["preferences2"].get(), fast=True, silent=True)

            if NGP_settings_dict["preferences3"].get():
                for act in ("fetish", "bisexual", "group"):
                    self.change_preference(act, NGP_settings_dict["preferences3"].get(), fast=True, silent=True)

            # /NewGame+ settings

            return


        def add_random_fixation(self, act=None, fixation=None, type="pos", nb=1): # When provided, fixation is the name (string), not the object

            # Returns False or a list of fixation names (may be only one)

            fixations = []

            if fixation:
                if fix_dict[fixation].available(self):
                    fixations.append(fixation)
                else:
                    return False
            
            else:
                if act:
                    available_fix = [(fix.name, fix.get_weight(self, type)) for fix in fix_dict.values() if fix.available(self, act, type)]
                else:
                    available_fix = [(fix.name, fix.get_weight(self, type)) for fix in fix_dict.values() if fix.available(self, type=type)]

                if available_fix:
                    fixations = weighted_choice(available_fix, nb) # always returns a list
                else:
                    debug_notify("No " + type + " fixations found for " + self.fullname)
                    return False

                if not fixations and debug_mode:
                    raise AssertionError("Couldn't find %s %s fixations among available list: %s" % (nb, type, available_fix))

                if len(fixations) < nb and debug_mode:
                    raise AssertionError("Couldn't find %s %s fixations among available list: %s" % (nb, type, available_fix))

            if type == "pos":
                self.pos_fixations += [fix_dict[f] for f in fixations]
            elif type == "neg":
                self.neg_fixations += [fix_dict[f] for f in fixations]

            return fixations # Returns a list of fixation names

        def reset_sex_acts(self, first=True):
            self.pos_acts = []
            self.neg_acts = []

            for fix in self.pos_fixations:
                self.pos_acts += [a for a in fix.acts if a not in self.pos_acts]

            for fix in self.neg_fixations:
                self.neg_acts += [a for a in fix.acts if a not in self.neg_acts]

            if first:
                for act in self.pos_acts:
                    eff = Effect("change", act + " preferences changes", 25)
                    self.effects.append(eff) # Removed add_effects to improve performance
                    self.effect_dict[(eff.type, eff.target)].append(eff)

                for act in self.neg_acts:
                    eff = Effect("change", act + " preferences changes", -50)
                    self.effects.append(eff) # Removed add_effects to improve performance
                    self.effect_dict[(eff.type, eff.target)].append(eff)

        def raise_preference(self, act, type = None, bonus = 1, status_change=False, silent=False, use_effects=True, context="MC"): # Type is fear, love, or None. Bonus depends on the training act (MC, farm or normal play)
            return self._sex.raise_preference(act, type, bonus, status_change, silent, use_effects, context)

        def change_preference(self, act, nb, fast=False, silent=False): # Fast disables some checks for performance
            return self._sex.change_preference(act, nb, fast, silent)


        def get_preference(self, act, bonus=0):

            act = act.lower()
            pref = self.preferences[act] + bonus

            # Reminder: Base reluctance is negative

            for res in ("fascinated", "very interested", "interested", "a little interested", "indifferent", "a little reluctant", "reluctant", "very reluctant", "refuses"):
                if self.preferences[act] + bonus > get_preference_limit(act, res):
                    return res

        def compare_preference(self, sex_act, min_pref): # Returns True if a girl's preference is better or equal to min_pref (e.g. 'indifferent')
            return compare_preference(self, sex_act, min_pref)

        def get_preference_bonus(self, act, minion_type=None): # Used for farm shows. Returns a modifier between 35% and 185%, and a list of applied effects
            
            pref = self.get_preference(act)
            pref_effects = [pref]

            pref_bonus = 1.0 + farm_perform_dict["pref_bonus"][pref]

            if act in self.pos_acts:
                pref_bonus += farm_perform_dict["pref_bonus"]["positive act"]
                pref_effects.append("pos_act")
            if act in self.neg_acts:
                pref_bonus += farm_perform_dict["pref_bonus"]["negative act"]
                pref_effects.append("neg_act")

            if minion_type and minion_type == self.weakness:
                pref_bonus += farm_perform_dict["pref_bonus"]["farm weakness"]
                pref_effects.append("weakness")

            return pref_bonus, pref_effects



## Girl moods

        def get_love(self):

            love = self.love

            love += self.get_effect("change", "love")
            if love > 0:
                love *= self.get_effect("boost", "love")
            elif love < 0:
                love *= self.get_effect("boost", "hate")

            return love

        def get_fear(self):

            fear = self.fear

            fear += self.get_effect("change", "fear")
            if fear > 0:
                fear *= self.get_effect("boost", "fear")
            elif fear < 0:
                fear *= self.get_effect("boost", "trust")

            return fear


        # Phase 2.1: Delegated to GirlRelationships component
        def change_love(self, amount, min_cap=None, max_cap=None, silent=False):
            return self._relationships.change_love(amount, min_cap, max_cap, silent)

        def change_fear(self, amount, min_cap=None, max_cap=None, mojo_color="purple", silent=False):
            return self._relationships.change_fear(amount, min_cap, max_cap, mojo_color, silent)


        def get_obedience_check_target(self, act=None, train=False): # This is the target (in %) UNDER which a girl must roll to obey.

            if self.job == "whore" or act == "whore":
                coeff = 70
                if self.has_activated_sex_acts():
                    # Only the average modifier is kept
                    coeff += sum(preference_modifier[self.get_preference(act)] for act in self.does if (self.does[act] and act in all_sex_acts)) / sum(1 for act in self.does if (self.does[act] and act in all_sex_acts))

                    # Cannot completely offset mod (mood, obedience...)
                    if coeff < 30:
                        coeff = 30
                else: # Can no longer work as a whore
                    if self.job == "whore":
                        self.job = None
                        notify(_("%s cannot work as a whore anymore.") % self.fullname, pic=self.portrait)

                    # raise AssertionError("No sex act activated")

            elif act and act != "whore":
                coeff = 70

                # Checks modifier according to girl's preference/reluctance
                coeff += preference_modifier[self.get_preference(act)]

            else: # Regular job
                coeff = 35

            coeff += self.get_effect("change", "obedience target")

            if train:
                if self.get_love() > self.get_fear(): # Dominant emotion is used if training.
                    mod = self.get_stat("obedience") + self.get_love() + self.mood//4
                else:
                    mod = self.get_stat("obedience") + self.get_fear() + self.mood//4
            else:
                mod = self.get_stat("obedience") + self.mood//4 - (self.get_stat_minmax("energy")[1] - self.energy)//10

                if self.get_fear() > 0:
                    mod += self.get_fear()
                elif self.get_fear() < 0: # lower impact of trust on disobedience to compensate the rank penalty
                    mod += self.get_fear()//2

            # New: Target is affected by rank and total girl number in the Brothel, giving more importance to Obedience in late-game
            coeff += (len(MC.girls)-1 + len(self.rivals) - len(self.friends))*15 # Friends do not count towards the overcrowding penalty, rivals count double
            mod -= (self.rank-1) * 20

            target = (0.96 ** mod) * coeff # Make 0.96 higher to increase difficulty

            if train:
                target += self.get_effect("change", "train obedience target")
            elif self.job == "whore" or act == "whore":
                target += self.get_effect("change", "whore obedience target")
            else:
                target += self.get_effect("change", "job obedience target")

            ## Obedience link effect ##

            if self.get_effect("special", "link obedience", raw=True):
                girl2, is_super = self.get_effect("special", "link obedience", raw=True)

                if is_super:
                    target = min(target, girl2.get_obedience_check_target(act=act, train=train))
                else:
                    target = min(target, (target + girl2.get_obedience_check_target(act=act, train=train))/2)

            return target


        def obedience_check(self, act=None): # Will check if the girl will accept to work tonight
            return self._training.obedience_check(act)

        def training_check(self, act):
            return self._training.training_check(act)

        def run_away_check(self): # Will check if the girl attempts to run away in the morning
            return self._training.run_away_check()


        def get_working_chance(self, act):

            chance = 100 - self.get_obedience_check_target(act)

            return get_change_min_max(0, chance, 0, 100)

        def get_training_chance(self, act): # Chance to accept training
            chance = 100 - self.get_obedience_check_target(act, train=True)

            return get_change_min_max(0, chance, 0, 100)

## Phase 2.1: Delegated to GirlMood component ##
        def update_mood(self, resting=False):
            return self._mood.update_mood(resting)

        def change_mood(self, chg):
            return self._mood.change_mood(chg)

## Phase 2.1: Delegated to GirlMood component ##
        def get_mood_modifier(self, love_text="", fear_text="", description=False, resting=False):
            return self._mood.get_mood_modifier(love_text, fear_text, description, resting)

        def get_mood_description(self, filter=None): # This returns text for the mood help screen

            l = self.get_love()

            if l > 90:
                love_text = "{color=" + color_dict["love +++"] + "}" + love_description["++++++"] + "{/color}"
            elif l > 70:
                love_text = "{color=" + color_dict["love +++"] + "}" + love_description["+++++"] + "{/color}"
            elif l > 50:
                love_text = "{color=" + color_dict["love ++"] + "}" + love_description["++++"] + "{/color}"
            elif l > 30:
                love_text = "{color=" + color_dict["love ++"] + "}" + love_description["+++"] + "{/color}"
            elif l > 15:
                love_text = "{color=" + color_dict["love +"] + "}" + love_description["++"] + "{/color}"
            elif l >= 5:
                love_text = "{color=" + color_dict["love +"] + "}" + love_description["+"] + "{/color}"
            elif l > -5:
                love_text = "{color=" + color_dict["normal"] + "}" + love_description["0"] + "{/color}"
            elif l >= -15:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["-"] + "{/color}"
            elif l >= -30:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["--"] + "{/color}"
            elif l >= -50:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["---"] + "{/color}"
            elif l >= -70:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["----"] + "{/color}"
            elif l >= -90:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["-----"] + "{/color}"
            else:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["------"] + "{/color}"

            f = self.get_fear()

            if self.personality.name != "masochist":
                if f > 90:
                    fear_text = "{color=" + color_dict["fear +++"] + "}" + fear_description["++++++"] + "{/color}"
                elif f > 70:
                    fear_text = "{color=" + color_dict["fear +++"] + "}" + fear_description["+++++"] + "{/color}"
                elif f > 50:
                    fear_text = "{color=" + color_dict["fear ++"] + "}" + fear_description["++++"] + "{/color}"
                elif f > 30:
                    fear_text = "{color=" + color_dict["fear ++"] + "}" + fear_description["+++"] + "{/color}"
                elif f > 15:
                    fear_text = "{color=" + color_dict["fear +"] + "}" + fear_description["++"] + "{/color}"
                elif f > 5:
                    fear_text = "{color=" + color_dict["fear +"] + "}" + fear_description["+"] + "{/color}"
                elif f >= -5:
                    fear_text = "{color=" + color_dict["normal"] + "}" + fear_description["0"] + "{/color}"
                elif f >= -15:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["-"] + "{/color}"
                elif f >= -30:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["--"] + "{/color}"
                elif f >= -50:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["---"] + "{/color}"
                elif f >= -70:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["----"] + "{/color}"
                elif f >= -90:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["-----"] + "{/color}"
                else:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["------"] + "{/color}"

            else:
                if f > 90:
                    fear_text = "{color=" + color_dict["fear +++"] + "}" + fear_description["M++++++"] + "{/color}"
                elif f > 70:
                    fear_text = "{color=" + color_dict["fear +++"] + "}" + fear_description["M+++++"] + "{/color}"
                elif f > 50:
                    fear_text = "{color=" + color_dict["fear ++"] + "}" + fear_description["M++++"] + "{/color}"
                elif f > 30:
                    fear_text = "{color=" + color_dict["fear ++"] + "}" + fear_description["M+++"] + "{/color}"
                elif f > 15:
                    fear_text = "{color=" + color_dict["fear +"] + "}" + fear_description["++"] + "{/color}"
                elif f > 5:
                    fear_text = "{color=" + color_dict["fear +"] + "}" + fear_description["+"] + "{/color}"
                elif f >= -5:
                    fear_text = "{color=" + color_dict["normal"] + "}" + fear_description["0"] + "{/color}"
                elif f >= -15:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["-"] + "{/color}"
                elif f >= -30:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["--"] + "{/color}"
                elif f >= -50:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["M---"] + "{/color}"
                elif f >= -70:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["M----"] + "{/color}"
                elif f >= -90:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["M-----"] + "{/color}"
                else:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["M------"] + "{/color}"

            m = self.mood

            if m > 90:
                mood_text = "{color=" + color_dict["+++"] + "}" + mood_description["++++++"] + "{/color}"
            elif m > 70:
                mood_text = "{color=" + color_dict["+++"] + "}" + mood_description["+++++"] + "{/color}"
            elif m > 50:
                mood_text = "{color=" + color_dict["++"] + "}" + mood_description["++++"] + "{/color}"
            elif m > 30:
                mood_text = "{color=" + color_dict["++"] + "}" + mood_description["+++"] + "{/color}"
            elif m > 15:
                mood_text = "{color=" + color_dict["+"] + "}" + mood_description["++"] + "{/color}"
            elif m >= 5:
                mood_text = "{color=" + color_dict["+"] + "}" + mood_description["+"] + "{/color}"
            elif m >= -5:
                mood_text = "{color=" + color_dict["normal"] + "}" + mood_description["0"] + "{/color}"
            elif m >= -15:
                mood_text = "{color=" + color_dict["-"] + "}" + mood_description["-"] + "{/color}"
            elif m >= -30:
                mood_text = "{color=" + color_dict["-"] + "}" + mood_description["--"] + "{/color}"
            elif m >= -50:
                mood_text = "{color=" + color_dict["--"] + "}" + mood_description["---"] + "{/color}"
            elif m >= -70:
                mood_text = "{color=" + color_dict["--"] + "}" + mood_description["----"] + "{/color}"
            elif m >= -90:
                mood_text = "{color=" + color_dict["---"] + "}" + mood_description["-----"] + "{/color}"
            else:
                mood_text = "{color=" + color_dict["---"] + "}" + mood_description["------"] + "{/color}"

            chg, mood_factors = self.get_mood_modifier(love_text, fear_text, description=True)

            if chg > 3:
                mood_change_text = mood_description["change +++"] + " {color=" + color_dict["+++"] + "}(+"
            elif chg > 1:
                mood_change_text = mood_description["change ++"] + " {color=" + color_dict["++"] + "}(+"
            elif chg > 0:
                mood_change_text = mood_description["change +"] + " {color=" + color_dict["+"] + "}(+"
            elif chg == 0:
                mood_change_text = mood_description["no change"] + " {color=" + color_dict["normal"] + "}("
            elif chg >= -1:
                mood_change_text = mood_description["change -"] + " {color=" + color_dict["-"] + "}("
            elif chg >= -3:
                mood_change_text = mood_description["change --"] + " {color=" + color_dict["--"] + "}("
            else:
                mood_change_text =  mood_description["change ---"] + " {color=" + color_dict["---"] + "}("

            mood_change_text += str(round_best(chg)) + "){/color}."

## Phase 2.1: Delegated to GirlMood component ##
            return self._mood.get_mood_description(filter)



        def get_mood_picture(self): # returns picture path
            return self._mood.get_mood_picture()



## Commit girl to external job or class

## Phase 2.1: Delegated to GirlLogging component ##
        def commit(self, quest):
            return self._logging.commit(quest)

## Phase 2.1: Delegated to GirlLogging component ##
        def return_from(self, quest):
            return self._logging.return_from(quest)


## LOG ACTIONS - Note: The various logs and stats are really messy and should be reworked from the grounds up

## Phase 2.1: Delegated to GirlLogging component ##
        def add_log(self, root, v = 1, _delay = 0):
            return self._logging.add_log(root, v, _delay)


## Phase 2.1: Delegated to GirlLogging component ##
        def get_log(self, root, days = 0): # If days = 0, get all time stats
            return self._logging.get_log(root, days)


## Phase 2.1: Delegated to GirlLogging component ##
        def get_average_performance(self, root, days):
            return self._logging.get_average_performance(root, days)

        # Personality traits

        # def is_old(self, attr): # Attr can be a string or a tuple. If several attributes are requested, an 'and' clause is used
        #
        #     return self.has_attributes(attr)

## Phase 2.1: Delegated to GirlDialogue component ##
        def is_(self, attributes, type="and"): # Checks if the girl has one or several attributes. Note: A girl with 'very X' will also be 'X'.
            return self._dialogue.is_(attributes, type)

## Phase 2.1: Delegated to GirlDialogue component ##
        def unlock_info(self, topic):
            return self._dialogue.unlock_info(topic)

## Phase 2.1: Delegated to GirlDialogue component ##
        def get_personality_description(self, show="personality"):
            return self._dialogue.get_personality_description(show)



## Phase 2.1: Delegated to GirlLogging component ##
        def track_event(self, type, arg=None, silent=False):
            return self._logging.track_event(type, arg, silent)


## Phase 2.1: Delegated to GirlLogging component ##
        def get_recent_events(self, day_number = 7, filter = None): # Events are returned with a tuple: Type, description, date
            return self._logging.get_recent_events(day_number, filter)


## Phase 2.1: Delegated to GirlLogging component ##
        def get_recent_events_description(self, day_number = 7):
            return self._logging.get_recent_events_description(day_number)

## Phase 2.1: Delegated to GirlLogging component ##
        def will_remember(self, context, type, score):
            return self._logging.will_remember(context, type, score)

## Phase 2.1: Delegated to GirlLogging component ##
        def remembers(self, context, type): # Remembering is more effective when the memory is fresh
            return self._logging.remembers(context, type)

## Phase 2.1: Delegated to GirlLogging component ##
        def forgets(self):
            return self._logging.forgets()

        def test_weakness(self, act, unlock=False, feedback=False):

            _pos = False
            _neg = False

            if act in self.pos_acts:
                _pos=True

            if act in self.neg_acts:
                _neg=True

            if unlock:
                if not self.personality_unlock[act]:
                    self.personality_unlock[act] = True # Testing weakness unlocks the act for the personality screen

                    if feedback:
                        if _pos and _neg:
                            renpy.play(s_ahaa, "sound")
                            renpy.say("", __("You notice that %s is feeling a mix of pleasure and discomfort during %s. It seems she has ambivalent feelings about it.") % (self.name, __(long_act_description[act])))
                        elif _pos:
                            renpy.play(s_mmh, "sound")
                            renpy.say("", __("You notice that %s seems to enjoy %s.") % (self.name, __(long_act_description[act])))
                        elif _neg:
                            renpy.play(s_scream, "sound")
                            renpy.say("", __("You notice that %s seems disgusted by %s.") % (self.name, __(long_act_description[act])))

            return _pos, _neg

        def get_reaction_to_act(self, act):

            pos_reaction, neg_reaction = self.test_weakness(act)

            if pos_reaction and neg_reaction:
                return "ambivalent feelings"
            elif pos_reaction:
                return "a weakness"
            elif neg_reaction:
                return "a disgust"
            else:
                return "no particular reaction"

        def get_day_off(self, day_nb):

            if self.works_today():

                day = calendar.get_weekday()
                charge = self.workdays[day]
                self.workdays[day] = 0
                self.block_schedule = day
                calendar.set_alarm(calendar.time + day_nb, Event(label =  "reset_workday", object = (self, day, charge)))

                return True

            else:
                return False

## Phase 2.1: Delegated to GirlMood component ##
        def tired_check(self):
            return self._mood.tired_check()

        def cut_upkeep(self, day_nb):

            self.locked_upkeep = self.upkeep
            self.upkeep = 0
            calendar.set_alarm(calendar.time + 1, Event(label = "restore_upkeep", object = self))

        def restore_upkeep(self):
            if self.locked_upkeep:
                self.upkeep = self.locked_upkeep
                self.locked_upkeep = None

        def refresh_spoil_terrify_points(self):

            self.spoil_points = max(self.spoil_points-1, 0)

            if self.spoil_points == 0:
                self.spoiled = False

            self.terrify_points = max(self.terrify_points-1, 0)

            if self.terrify_points == 0:
                self.terrified = False

            return

        def spoil(self, nb):

            self.spoil_points += nb

            if dice(6) + 2 < self.spoil_points:
                self.spoiled = True

            return

        def terrify(self, nb):

            self.terrify_points += nb

            if dice(6) + 2 < self.terrify_points:
                self.terrified = True

            return

        def pop_virginity(self, origin="brothel"):

            for trait in self.traits: # Update trait list in restore_virginity if adding new special traits
                if trait.name == "Virgin":
                    self.remove_trait(trait)

                    if origin == "brothel":
                        self.add_trait(housebroken_trait, _pos=1, no_perks=True)
                    elif origin == "farm":
                        self.add_trait(farmgirl_trait, _pos=1, no_perks=True)
                    elif origin == "MC" and self.get_love() > self.get_fear():
                        self.add_trait(t_pet_trait, _pos=1, no_perks=True)
                    elif origin == "MC" and self.get_love() <= self.get_fear():
                        self.add_trait(trauma_trait, _pos=1, no_perks=True)
                    elif origin == "rape":
                        self.add_trait(trauma_trait, _pos=1, no_perks=True)
                    elif origin == "chaos":
                        self.add_trait(chaos_trait, _pos=1)
                    else: # Catch all for other origins
                        self.add_trait(trait_dict["Kinky"], _pos=1)

                    return True

            else:
                return False

        def restore_virginity(self):

            for t in (housebroken_trait, farmgirl_trait, trauma_trait, chaos_trait):
                if t in self.traits:
                    self.remove_trait(t)

            self.add_trait(virgin_trait, _pos=1)

## Phase 2.1: Delegated to GirlLogging component ##
        def count_occurences(self, context="all", original=False, add_list=None):
            return self._logging.count_occurences(context, original, add_list)

        def talk_tastes(self, type):

            if type == "likes":
                mylist = ["color", "food", "drink"]
                renpy.random.shuffle(mylist)

                for thing in mylist:
                    if not self.personality_unlock["fav_" + thing]:
                        break
                else:
                    thing = rand_choice(mylist)
                return thing, self.likes[thing]

            elif type == "dislikes":
                mylist = ["color", "food", "drink"]
                renpy.random.shuffle(mylist)

                for thing in mylist:
                    if not self.personality_unlock["dis_" + thing]:
                        break
                else:
                    thing = rand_choice(mylist)
                return thing, self.dislikes[thing]

            elif type == "loves":
                best_replies = []
                all_replies = []

                for k in [k for k, v in self.personality.gift_likes.items() if v >= 3]:
                    if not k in self.personality_unlock["loves"]:
                        best_replies.append(("loves", k))
                    all_replies.append(("loves", k))

                for k in [k for k, v in self.personality.gift_likes.items() if 3 > v >= 0]:
                    if not k in self.personality_unlock["likes"]:
                        best_replies.append(("likes", k))
                    all_replies.append(("likes", k))

                if best_replies:
                    return rand_choice(best_replies)
                elif all_replies:
                    return rand_choice(all_replies)
                else:
                    return "indifferent", False

            elif type == "hates":
                best_replies = []
                all_replies = []

                for k in [k for k, v in self.personality.gift_likes.items() if v <= -2]:
                    if not k in self.personality_unlock["hates"]:
                        best_replies.append(("hates", k))
                    all_replies.append(("hates", k))

                if best_replies:
                    return rand_choice(best_replies)
                elif all_replies:
                    return rand_choice(all_replies)
                else:
                    return "indifferent", False


        def try_to_remove_fix(self, fix_name, type=None):

            if type == "love":
                chance = 40 + (self.mood + self.get_love() - self.get_fear()) // 3
                lock_chance = 0
            elif type == "neutral":
                chance = 40
                lock_chance = 0
            elif type == "fear": # Fear gives a higher bonus and ignores mood but may lock a girl's negative fixation
                chance = 50 + self.get_fear()
                lock_chance = 3

            if dice(100) < lock_chance:
                self.locked_fix.append(fix_name)
                return "locked"

            elif dice(100) < chance:
                self.fix_level[fix_name] += 1

                if self.fix_level[fix_name] < 4:
                    return self.fix_level[fix_name]

                else:
                    self.remove_fixation(fix_name)
                    return "success"

            else:
                return "fail"

        def remove_fixation(self, fix_name):

            for fix in self.pos_fixations:
                _type = "pos"
                if fix.name == fix_name:
                    self.pos_fixations.remove(fix)
                    # Resets farm
                    if fix in farm.knows["pos_fix"][self]:
                        farm.knows["pos_fix"][self].remove(fix)

            for fix in self.neg_fixations:
                _type = "neg"
                if fix.name == fix_name:
                    self.neg_fixations.remove(fix)
                    # Tracks removed fixations for the 'Phobia' achievement
                    try:
                        self.flags["removed neg fixations"] += 1
                    except:
                        self.flags["removed neg fixations"] = 1
                    # Resets farm
                    if fix in farm.knows["neg_fix"][self]:
                        farm.knows["neg_fix"][self].remove(fix)

            self.reset_sex_acts(first=False)

            # Removes fixation preference bonuses/penalties
            for act in fix.acts:
                if type == "pos" and act not in self.pos_acts:
                    self.remove_effects([Effect("change", act + " preferences changes", 25)])
                if type == "neg" and act not in self.neg_acts:
                    self.remove_effects([Effect("change", act + " preferences changes", -50)])

        def has_fixation(self, type="pos", fix_name=None):
            if type == "pos":
                for fix in self.pos_fixations:
                    if fix.name == fix_name:
                        return True

            if type == "neg":
                for fix in self.neg_fixations:
                    if fix.name == fix_name:
                        return True

        def meet_MC(self):
            self.MC_interact = True
            self.track_event("MC met", arg=self.name)
            self.activation_date = calendar.time
            self.talked_to_date = calendar.time


        # Phase 2.1: Delegated to GirlDialogue component
        def pick_dialogue(self, topic):
            return self._dialogue.pick_dialogue(topic)

        def say(self, topic, custom_label=True, custom_arg=False, nw=False, narrator_mode=False):
            return self._dialogue.say(topic, custom_label, custom_arg, nw, narrator_mode)

        def rand_say(self, *dialogue_options):
            return self._dialogue.rand_say(*dialogue_options)


        def customer_populations_safety_check(self, current_pop): # Where current_pop is a population name
            for pop, refused in self.refused_populations.items():
                if brothel.get_effect("allow", pop) and not refused:
                    break
            else:
                self.refused_populations[current_pop] = False
                notify("You must activate at least one customer population for this girl.", pic=self.portrait)

            return

        def build_up(self, v): # FARM EVENTS - Builds-up her farm show jauge

            try:
                self.buildup += v
            except:
                self.buildup = v

            self.buildup = clamp(self.buildup, 0, 200)

            if self.buildup >= 100:
                if not story_flags["farm shows"]:
                    calendar.set_alarm(calendar.time+1, StoryEvent("farm_shows_intro", arg=self, type = "morning"))
                    self.flags["buildup warning 100"] = True
                elif not self.flags["buildup warning 100"]:
                    notify(__("%s is now ready to attend a farm show (100%).") % self.fullname)
                    self.flags["buildup warning 100"] = True
                elif self.buildup >= 150 and not self.flags["buildup warning 150"]:
                    notify(__("%s is now ready to attend a farm show (150%).") % self.fullname)
                    self.flags["buildup warning 150"] = True
                elif self.buildup >= 200 and not self.flags["buildup warning 200"]:
                    notify(__("%s is now ready to attend a farm show (200%).") % self.fullname)
                    self.flags["buildup warning 200"] = True

        def get_build_up(self): # FARM EVENTS - Recovers her farm show jauge

            try:
                return self.buildup
            except:
                self.buildup = 0
                return self.buildup

        def reset_build_up(self):
            self.buildup = 0
            self.flags["buildup warning 100"] = False
            self.flags["buildup warning 150"] = False
            self.flags["buildup warning 200"] = False

        # ── Phase 2.1: Economy delegation aliases ──
        _get_price_impl = get_price
        _get_med_upkeep_impl = get_med_upkeep
        _adjust_upkeep_impl = adjust_upkeep
        _update_upkeep_ratio_impl = update_upkeep_ratio
        _get_upkeep_threshold_impl = get_upkeep_threshold
        _get_upkeep_modifier_impl = get_upkeep_modifier
        _get_next_upkeep_step_impl = get_next_upkeep_step
        _get_previous_upkeep_step_impl = get_previous_upkeep_step
        _cut_upkeep_impl = cut_upkeep
        _restore_upkeep_impl = restore_upkeep
        _get_max_cust_served_impl = get_max_cust_served
        _get_max_interactions_impl = get_max_interactions
        _get_interaction_modifier_impl = get_interaction_modifer
        _reset_interactions_impl = reset_interactions
        _estimate_performance_impl = estimate_performance
        _get_xp_impl = get_xp
        _get_jp_impl = get_jp
        _get_rep_impl = get_rep
        _get_tip_impl = get_tip
        _get_street_tip_impl = get_street_tip
        _whore_on_street_impl = whore_on_street
        _change_rep_impl = change_rep
        _customer_populations_safety_check_impl = customer_populations_safety_check

        # ── Phase 2.1: Mood delegation aliases ──
        # (Sanity methods now delegate directly to GirlMood — aliases removed)
        _change_energy_impl = change_energy
        _heal_impl = heal
        _full_rest_impl = full_rest
        _rest_impl = rest
        _can_heal_from_item_impl = can_heal_from_item
        _build_up_impl = build_up
        _get_build_up_impl = get_build_up
        _reset_build_up_impl = reset_build_up

        # ── Phase 2.1: Schedule delegation aliases ──
        _set_workdays_impl = set_workdays
        _cycle_workday_impl = cycle_workday
        _set_job_impl = set_job
        _set_rest_impl = set_rest
        _works_today_impl = works_today
        _will_do_impl = will_do
        _get_schedule_impl = get_schedule
        _load_schedule_impl = load_schedule
        _get_status_impl = get_status
        _get_status_summary_impl = get_status_summary
        _get_day_off_impl = get_day_off

        # ── Phase 2.1: Stats delegation aliases ──
        _generate_stats_impl = generate_stats
        _find_stat_impl = find_stat
        _get_stat_impl = get_stat
        _average_stats_impl = average_stats
        _test_stats_impl = test_stats
        _raise_stats_impl = raise_stats
        _can_upgrade_stat_impl = can_upgrade_stat
        _upgrade_stat_impl = upgrade_stat
        _get_stat_max_impl = get_stat_max
        _get_stat_minmax_impl = get_stat_minmax
        _stat_spillover_impl = stat_spillover
        _change_stat_impl = change_stat
        _set_stat_impl = set_stat
        _average_skills_impl = average_skills
        _get_xp_cap_impl = get_xp_cap
        _get_jp_cap_impl = get_jp_cap
        _get_rep_cap_impl = get_rep_cap
        _adjust_level_impl = adjust_level

        # ── Phase 2.1: Relationships delegation aliases ──
        _get_MC_relation_impl = get_MC_relation
        _change_relationship_impl = change_relationship
        _get_compatibility_impl = get_compatibility
        _update_relationships_impl = update_relationships
        _get_friendship_impl = get_friendship
        _get_love_impl = get_love
        _get_fear_impl = get_fear
        _change_love_impl = change_love
        _change_fear_impl = change_fear
        _meet_MC_impl = meet_MC
        _spoil_impl = spoil
        _terrify_impl = terrify
        _refresh_spoil_terrify_points_impl = refresh_spoil_terrify_points

        # ── Phase 2.1: Dialogue delegation aliases ──
        _generate_personality_impl = generate_personality
        _adjust_personality_impl = adjust_personality
        _generate_background_impl = generate_background
        _talk_tastes_impl = talk_tastes
        _pick_dialogue_impl = pick_dialogue
        _say_impl = say
        _rand_say_impl = rand_say

        # ── Phase 2.1: Traits delegation aliases ──
        _generate_traits_impl = generate_traits
        _has_trait_impl = has_trait
        _has_perk_impl = has_perk
        _add_trait_impl = add_trait
        _remove_trait_impl = remove_trait
        _can_acquire_perk_impl = can_acquire_perk
        _update_can_perk_impl = update_can_perk
        _acquire_perk_impl = acquire_perk
        _refund_perks_impl = refund_perks
        _check_combo_perks_impl = check_combo_perks
        _has_prerequisites_impl = has_prerequisites
        _get_perk_impl = get_perk
        _get_perk_level_impl = get_perk_level

        # ── Phase 2.1: Logging delegation aliases ──

        # ── Phase 2.1: Base/Identity delegation aliases (10/10 complete) ──
        _set_name_impl = set_name
        _set_fullname_impl = set_fullname
        _random_rename_impl = random_rename
        _get_name_impl = get_name
        _get_badge_impl = get_badge
        _is_unique_impl = is_unique
        _load_ini_impl = load_ini
        _read_ini_impl = read_ini
        # _adjust_level_impl already defined in Stats section above

        # ── Phase 2.1: Sex delegation aliases ──
        _will_do_sex_act_impl = will_do_sex_act
        _toggle_sex_act_impl = toggle_sex_act
        _does_anything_impl = does_anything
        _will_do_anything_impl = will_do_anything
        _count_available_sex_acts_impl = count_available_sex_acts
        _get_trainable_sex_acts_impl = get_trainable_sex_acts
        _count_activated_sex_acts_impl = count_activated_sex_acts
        _has_activated_sex_acts_impl = has_activated_sex_acts
        _refresh_sex_acts_impl = refresh_sex_acts
        _activate_sex_act_impl = activate_sex_act
        _deactivate_sex_act_impl = deactivate_sex_act
        _get_sex_act_modifier_impl = get_sex_act_modifier
        _get_preference_bonus_impl = get_preference_bonus
        _add_random_fixation_impl = add_random_fixation
        _reset_sex_acts_impl = reset_sex_acts
        _get_preference_impl = get_preference
        _compare_preference_impl = compare_preference
        _pop_virginity_impl = pop_virginity
        _restore_virginity_impl = restore_virginity
        _test_weakness_impl = test_weakness
        _has_fixation_impl = has_fixation
        _remove_fixation_impl = remove_fixation
        _try_to_remove_fix_impl = try_to_remove_fix

        # ── Phase 2.1: Items delegation aliases | 物品方法别名 ──
        _get_equipped_impl = get_equipped
        _receive_gift_impl = receive_gift

        # -- Phase 2.1: Training delegation aliases | 训练方法别名 --
        _will_do_farm_act_impl = will_do_farm_act
        _will_rebel_in_farm_impl = will_rebel_in_farm
        _farm_beg_test_impl = farm_beg_test
        _get_obedience_check_target_impl = get_obedience_check_target
        _get_working_chance_impl = get_working_chance
        _get_training_chance_impl = get_training_chance



#<Chris12 PackState>

####          FILES DICTIONARY FOR B KING                  ####################################################
##   Helper class for girl files and pictures.             ##################################################
##   Saves them in a global variable so that they          ##################################################
##     are only read once without getting saved by Renpy.  ##################################################
##   Also handles packstates.                              ##################################################
##                                                         ##################################################


#### END OF BK GIRLCLASS FILE ####
