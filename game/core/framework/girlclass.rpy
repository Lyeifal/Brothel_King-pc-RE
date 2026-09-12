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
            self._progression = GirlProgression(self)

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

## Phase 2.1: Delegated to GirlSchedule component ##
        def set_workdays(self): #Value is a percentage (0% = resting, 50% = working at half capacity, 100% = full capacity)
            return self._schedule.set_workdays()

## Phase 2.1: Delegated to GirlSchedule component ##
        def cycle_workday(self, day, reverse = False):
            return self._schedule.cycle_workday(day, reverse)


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

## Phase 2.1: Delegated to GirlStats component ##
        def generate_stats(self, sex=False): # regular stats are generated first, sx stats are generated after fixations
            return self._stats.generate_stats(sex)

## Phase 2.1: Delegated to GirlProgression component ##
        def adjust_level(self, level):
            return self._progression.adjust_level(level)

        def will_do_farm_act(self, act, mode=None):
            return self._training.will_do_farm_act(act, mode)


## Phase 2.1: Delegated to GirlTraining component ##
        def will_rebel_in_farm(self, train_mode, reaction):
            return self._training.will_rebel_in_farm(train_mode, reaction)

## Phase 2.1: Delegated to GirlTraining component ##
        def farm_beg_test(self): # Determines if the girl will beg not to go to the farm
            return self._training.farm_beg_test()


        # Phase 2.1: Delegated to GirlSex component
        def will_do_sex_act(self, sex_act, use_desc=False):
            return self._sex.will_do_sex_act(sex_act, use_desc)

        def toggle_sex_act(self, sex_act):
            return self._sex.toggle_sex_act(sex_act)


## Phase 2.1: Delegated to GirlSex component ##
        def does_anything(self): ## Tests if the girl has any activated sex act. She will be excluded from whoring if she isn't.
            return self._sex.does_anything()

## Phase 2.1: Delegated to GirlSex component ##
        def will_do_anything(self): ## Tests if the girl is open to a sex act. She will be excluded from the whore job if she isn't.
            return self._sex.will_do_anything()

## Phase 2.1: Delegated to GirlSex component ##
        def count_available_sex_acts(self, discovered=True, extended=True): # unused
            return self._sex.count_available_sex_acts(discovered, extended)

## Phase 2.1: Delegated to GirlSex component ##
        def get_trainable_sex_acts(self):
            return self._sex.get_trainable_sex_acts()

        def count_activated_sex_acts(self):
            return sum(1 for act in all_sex_acts if self.does[act])

## Phase 2.1: Delegated to GirlSex component ##
        def has_activated_sex_acts(self): # Checks if the girl has any sex acts activated
            return self._sex.has_activated_sex_acts()

        # Phase 2.1: Delegated to GirlSex component
        def refresh_sex_acts(self):
            return self._sex.refresh_sex_acts()

        def activate_sex_act(self, sex_act):
            return self._sex.activate_sex_act(sex_act)

        def deactivate_sex_act(self, sex_act):
            return self._sex.deactivate_sex_act(sex_act)


## Phase 2.1: Delegated to GirlSex component ##
        def get_sex_act_modifier(self, sex_act = "all"):
            return self._sex.get_sex_act_modifier(sex_act)


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


## Phase 2.1: Delegated to GirlEconomy component ##
        def get_med_upkeep(self):
            return self._economy.get_med_upkeep()


## Phase 2.1: Delegated to GirlEconomy component ##
        def adjust_upkeep(self):
            return self._economy.adjust_upkeep()

## Phase 2.1: Delegated to GirlEconomy component ##
        def update_upkeep_ratio(self):
            return self._economy.update_upkeep_ratio()

## Phase 2.1: Delegated to GirlEconomy component ##
        def get_upkeep_threshold(self, step): # Only use integers from +5 to -5 as step values, or "min".
            return self._economy.get_upkeep_threshold(step)

## Phase 2.1: Delegated to GirlEconomy component ##
        def get_upkeep_modifier(self):
            return self._economy.get_upkeep_modifier()

## Phase 2.1: Delegated to GirlEconomy component ##
        def get_next_upkeep_step(self):
            return self._economy.get_next_upkeep_step()

## Phase 2.1: Delegated to GirlEconomy component ##
        def get_previous_upkeep_step(self):
            return self._economy.get_previous_upkeep_step()






## Items

        # Phase 2.1: Delegated to GirlItems component
        def equip(self, item):
            return self._items.equip(item)

        # Phase 2.1: Delegated to GirlItems component
## Phase 2.1: Delegated to GirlItems component ##
        def unequip(self, item):
            return self._items.unequip(item)

## Phase 2.1: Delegated to GirlItems component ##
        def get_equipped(self, slot):
            return self._items.get_equipped(slot)

## Phase 2.1: Delegated to GirlItems component ##
        def use_item(self, item, night=False):
            return self._items.use_item(item, night)

## Phase 2.1: Delegated to GirlItems component ##
        def take(self, giver, obj):
            return self._items.take(giver, obj)

## Phase 2.1: Delegated to GirlRelationships component ##
        def get_MC_relation(self):
            return self._relationships.get_MC_relation()

## Phase 2.1: Delegated to GirlRelationships component ##
        def receive_gift(self, item):
            return self._relationships.receive_gift(item)


## Phase 2.1: Delegated to GirlDialogue component ##
        def test_say(self):
            return self._dialogue.test_say()


## Jobs

## Phase 2.1: Delegated to GirlSchedule component ##
        def will_do(self, job, silent=False):
            return self._schedule.will_do(job, silent)

## Phase 2.1: Delegated to GirlSchedule component ##
        def set_job(self, job, forced=False):
            return self._schedule.set_job(job, forced)

## Phase 2.1: Delegated to GirlSchedule component ##
        def set_rest(self):
            return self._schedule.set_rest()


## Phase 2.1: Delegated to GirlSchedule component ##
        def works_today(self, check_autorest=False):
            return self._schedule.works_today(check_autorest)

        def get_schedule(self): # Returns a list of values for the seven days of the week
            return [self.workdays[d] for d in weekdays]

## Phase 2.1: Delegated to GirlSchedule component ##
        def load_schedule(self, schedule):
            return self._schedule.load_schedule(schedule)

        # Phase 2.1: Delegated to GirlSchedule component (implementations moved)
        def get_status(self):
            return self._schedule.get_status()

        def get_status_summary(self):
            return self._schedule.get_status_summary()


## Phase 2.1: Delegated to GirlEconomy component ##
        def get_max_cust_served(self, job="current"):
            return self._economy.get_max_cust_served(job)

## Phase 2.1: Delegated to GirlEconomy component ##
        def get_max_interactions(self):
            return self._economy.get_max_interactions()

## Phase 2.1: Delegated to GirlEconomy component ##
        def get_interaction_modifer(self): # Spent interactions are multiplied by this number (higher modifier=less interactions)
            return self._economy.get_interaction_modifier()

## Phase 2.1: Delegated to GirlEconomy component ##
        def reset_interactions(self):
            return self._economy.reset_interactions()


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

## Phase 2.1: Delegated to GirlEconomy component ##
        def get_street_tip(self): # Returns average tip value for street whores
            return self._economy.get_street_tip()

## Phase 2.1: Delegated to GirlEconomy component ##
        def whore_on_street(self): # Runs every night a broken girl is on the street. Returns tip value.
            return self._economy.whore_on_street()


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


## Phase 2.1: Delegated to GirlProgression component ##
        def get_xp_cap(self):
            return self._progression.get_xp_cap()


## Phase 2.1: Delegated to GirlProgression component ##
        def get_jp_cap(self, job = "all"):
            return self._progression.get_jp_cap(job)


## Phase 2.1: Delegated to GirlProgression component ##
        def get_rep_cap(self): # Adds 0.99 to avoid strange back and forth effects where girls can rank up briefly then are pulled back by rep decay
            return self._progression.get_rep_cap()


## Phase 2.1: Delegated to GirlTraits component ##
        def has_trait(self, name):
            return self._traits.has_trait(name)


        def has_perk(self, name): # Where name is a string, not the perk object

            if name == None:
                return True

            for p in self.perks:

                if p.name.lower() == name.lower():
                    return True

            else:
                return False


## Phase 2.1: Delegated to GirlTraits component ##
        def add_trait(self, trait, _pos=None, forced=False, no_perks=False): # Where 'trait' is an object (important)
            return self._traits.add_trait(trait, _pos, forced, no_perks)


## Phase 2.1: Delegated to GirlTraits component ##
        def remove_trait(self, trait): # Where trait is a Trait object
            return self._traits.remove_trait(trait)


        def list_effects(self):
            return self._effects.list_effects()

        def get_effect(self, type, target, raw=False, custom_scale=("factor", 0), change_cap=False):
            # raw=True means no additional brothel or world effects will be included. MUST if you expect to get a string value
            return self._effects.get_effect(type, target, raw, custom_scale, change_cap)

        def remove_effects(self, effects):
            return self._effects.remove_effects(effects)


## Phase 2.1: Delegated to GirlTraits component ##
        def get_defense(self, fight = False, raw=False):
            return self._traits.get_defense(fight, raw)

## Phase 2.1: Delegated to GirlTraits component ##
        def add_shield(self):
            return self._traits.add_shield()

## Phase 2.1: Delegated to GirlTraits component ##
        def test_shield(self):
            return self._traits.test_shield()



## Phase 2.1: Delegated to GirlStats component ##
        def average_stats(self, stats): #Unused with the new system
            return self._stats.average_stats(stats)


## Phase 2.1: Delegated to GirlStats component ##
        def test_stats(self, stats=None, diff=0, advanced_stats=None): # Result will range from total of positive max modifiers in stat_bonus (+9) to negative max modifiers for primary and secondary (-6). Advanced stats will feed a stat_list directly with more flexibility.
            return self._stats.test_stats(stats, diff, advanced_stats)


## Phase 2.1: Delegated to GirlStats component ##
        def raise_stats(self, stats, silent=False):
            return self._stats.raise_stats(stats, silent)

## Phase 2.1: Delegated to GirlProgression component ##
        def can_upgrade_stat(self, stat): # Where stat is an object
            return self._progression.can_upgrade_stat(stat)

## Phase 2.1: Delegated to GirlProgression component ##
        def upgrade_stat(self, stat, chg, silent=True):
            return self._progression.upgrade_stat(stat, chg, silent)

## Phase 2.1: Delegated to GirlProgression component ##
        def get_max_stat_upgrade_points(self, stat):
            return self._progression.get_max_stat_upgrade_points(stat)

        def get_stat_max(self, stat_name, raw = False, custom_cap=None):
            return self.get_stat_minmax(stat_name, raw, custom_cap)[1]

## Phase 2.1: Delegated to GirlStats component ##
        def get_stat_minmax(self, stat_name, raw = False, custom_cap=None):
            return self._stats.get_stat_minmax(stat_name, raw, custom_cap)

## Phase 2.1: Delegated to GirlStats component ##
        def stat_spillover(self, stat, chg, job=None): # Job must be specified for JP
            return self._stats.stat_spillover(stat, chg, job)


        def change_stat(self, stat, chg, apply_boost=True, spillover=True, custom_cap=None, silent=False, notify_prefix="", notify_suffix=""):
            return self._stats.change_stat(stat, chg, apply_boost, spillover, custom_cap, silent, notify_prefix, notify_suffix)

        def set_stat(self, stat, val):
            return self._stats.set_stat(stat, val)

        def average_skills(self, sk_list, mod=1.0):
            change_dict = self._stats.average_skills(sk_list, mod)

            for sk in sk_list:
                self.set_stat(sk, change_dict[sk])

## Phase 2.1: Delegated to GirlStats component ##
        def shuffle_skills(self, sk_list, mod=1.0):
            return self._stats.shuffle_skills(sk_list, mod)

## XP, rank and Level up

## Phase 2.1: Delegated to GirlProgression component ##
        def change_xp(self, value, apply_boost = True, spillover=True, silent=False):
            return self._progression.change_xp(value, apply_boost, spillover, silent)


## Phase 2.1: Delegated to GirlProgression component ##
        def change_jp(self, value, job, apply_boost = True, spillover=True, announcement_delay=1, silent=False):
            return self._progression.change_jp(value, job, apply_boost, spillover, announcement_delay, silent)


## Phase 2.1: Delegated to GirlProgression component ##
        def level_up(self, forced = False, silent=False):
            return self._progression.level_up(forced, silent)

## Phase 2.1: Delegated to GirlProgression component ##
        def debug_auto_level(self, chapter):
            return self._progression.debug_auto_level(chapter)


## Phase 2.1: Delegated to GirlProgression component ##
        def auto_level_up(self, forced = False, silent = False):
            return self._progression.auto_level_up(forced, silent)

## Phase 2.1: Delegated to GirlProgression component ##
        def rank_up(self, forced = False, silent=False):
            return self._progression.rank_up(forced, silent)


## Phase 2.1: Delegated to GirlProgression component ##
        def job_up(self, job, forced = False, announcement_delay=0):
            return self._progression.job_up(job, forced, announcement_delay)


## Phase 2.1: Delegated to GirlProgression component ##
        def ready_to_level(self):
            return self._progression.ready_to_level()

## Phase 2.1: Delegated to GirlProgression component ##
        def can_spend_upgrade_points(self):
            return self._progression.can_spend_upgrade_points()


## Phase 2.1: Delegated to GirlProgression component ##
        def ready_to_rank(self):
            return self._progression.ready_to_rank()


## Phase 2.1: Delegated to GirlProgression component ##
        def ready_to_job_up(self, job):
            return self._progression.ready_to_job_up(job)


## Phase 2.1: Delegated to GirlProgression component ##
        def unlock_archetype(self, archetype_name):
            return self._progression.unlock_archetype(archetype_name)

## Phase 2.1: Delegated to GirlProgression component ##
        def can_acquire_perk(self, perk, context=None): # Where perk is an object
            return self._progression.can_acquire_perk(perk, context)

## Phase 2.1: Delegated to GirlProgression component ##
        def update_can_perk(self): # 'can_perk' is used to trigger UI alerts
            return self._progression.update_can_perk()

## Phase 2.1: Delegated to GirlProgression component ##
        def acquire_perk(self, perk, forced=False): ## Where perk is an object
            return self._progression.acquire_perk(perk, forced)

## Phase 2.1: Delegated to GirlProgression component ##
        def refund_perks(self, min_level=0): # all perks above or equal to min_level will be refunded. Use min_level=0 to refund archetypes
            return self._progression.refund_perks(min_level)



## Phase 2.1: Delegated to GirlProgression component ##
        def check_combo_perks(self):
            return self._progression.check_combo_perks()



## Phase 2.1: Delegated to GirlProgression component ##
        def has_prerequisites(self, perk):
            return self._progression.has_prerequisites(perk)


## Phase 2.1: Delegated to GirlProgression component ##
        def get_perk(self, perk): ## Where perk is an object (important)
            return self._progression.get_perk(perk)


## Phase 2.1: Delegated to GirlProgression component ##
        def get_perk_level(self, perk): ## Where perk is an object (important)
            return self._progression.get_perk_level(perk)

## Phase 2.1: Delegated to GirlProgression component ##
        def change_rep(self, chg, silent=False):
            return self._progression.change_rep(chg, silent)




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

## Phase 2.1: Delegated to GirlRelationships component ##
        def change_relationship(self, other_girl, chg):
            return self._relationships.change_relationship(other_girl, chg)

## Phase 2.1: Delegated to GirlRelationships component ##
        def get_compatibility(self, other_girl): # Calculates a score to see if the girl is an ally or a rival. Relationship scores are stored in a dictionary for faster processing
            return self._relationships.get_compatibility(other_girl)

## Phase 2.1: Delegated to GirlRelationships component ##
        def update_relationships(self): # Returns a list of all changed relationships
            return self._relationships.update_relationships()


## Phase 2.1: Delegated to GirlRelationships component ##
        def get_friendship(self, other_girl):
            return self._relationships.get_friendship(other_girl)

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


## Phase 2.1: Delegated to GirlSex component ##
        def add_random_fixation(self, act=None, fixation=None, type="pos", nb=1): # When provided, fixation is the name (string), not the object
            return self._sex.add_random_fixation(act, fixation, type, nb)

## Phase 2.1: Delegated to GirlSex component ##
        def reset_sex_acts(self, first=True):
            return self._sex.reset_sex_acts(first)

        def raise_preference(self, act, type = None, bonus = 1, status_change=False, silent=False, use_effects=True, context="MC"): # Type is fear, love, or None. Bonus depends on the training act (MC, farm or normal play)
            return self._sex.raise_preference(act, type, bonus, status_change, silent, use_effects, context)

        def change_preference(self, act, nb, fast=False, silent=False): # Fast disables some checks for performance
            return self._sex.change_preference(act, nb, fast, silent)


## Phase 2.1: Delegated to GirlSex component ##
        def get_preference(self, act, bonus=0):
            return self._sex.get_preference(act, bonus)

        def compare_preference(self, sex_act, min_pref): # Returns True if a girl's preference is better or equal to min_pref (e.g. 'indifferent')
            return compare_preference(self, sex_act, min_pref)

## Phase 2.1: Delegated to GirlSex component ##
        def get_preference_bonus(self, act, minion_type=None): # Used for farm shows. Returns a modifier between 35% and 185%, and a list of applied effects
            return self._sex.get_preference_bonus(act, minion_type)



## Girl moods

## Phase 2.1: Delegated to GirlRelationships component ##
        def get_love(self):
            return self._relationships.get_love()

## Phase 2.1: Delegated to GirlRelationships component ##
        def get_fear(self):
            return self._relationships.get_fear()


        # Phase 2.1: Delegated to GirlRelationships component
        def change_love(self, amount, min_cap=None, max_cap=None, silent=False):
            return self._relationships.change_love(amount, min_cap, max_cap, silent)

        def change_fear(self, amount, min_cap=None, max_cap=None, mojo_color="purple", silent=False):
            return self._relationships.change_fear(amount, min_cap, max_cap, mojo_color, silent)


## Phase 2.1: Delegated to GirlTraining component ##
        def get_obedience_check_target(self, act=None, train=False): # This is the target (in %) UNDER which a girl must roll to obey.
            return self._training.get_obedience_check_target(act, train)


        def obedience_check(self, act=None): # Will check if the girl will accept to work tonight
            return self._training.obedience_check(act)

        def training_check(self, act):
            return self._training.training_check(act)

        def run_away_check(self): # Will check if the girl attempts to run away in the morning
            return self._training.run_away_check()


## Phase 2.1: Delegated to GirlTraining component ##
        def get_working_chance(self, act):
            return self._training.get_working_chance(act)

## Phase 2.1: Delegated to GirlTraining component ##
        def get_training_chance(self, act): # Chance to accept training
            return self._training.get_training_chance(act)

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

## Phase 2.1: Delegated to GirlSex component ##
        def test_weakness(self, act, unlock=False, feedback=False):
            return self._sex.test_weakness(act, unlock, feedback)

## Phase 2.1: Delegated to GirlSex component ##
        def get_reaction_to_act(self, act):
            return self._sex.get_reaction_to_act(act)

## Phase 2.1: Delegated to GirlSchedule component ##
        def get_day_off(self, day_nb):
            return self._schedule.get_day_off(day_nb)

## Phase 2.1: Delegated to GirlMood component ##
        def tired_check(self):
            return self._mood.tired_check()

## Phase 2.1: Delegated to GirlEconomy component ##
        def cut_upkeep(self, day_nb):
            return self._economy.cut_upkeep(day_nb)

## Phase 2.1: Delegated to GirlEconomy component ##
        def restore_upkeep(self):
            return self._economy.restore_upkeep()

## Phase 2.1: Delegated to GirlRelationships component ##
        def refresh_spoil_terrify_points(self):
            return self._relationships.refresh_spoil_terrify_points()

## Phase 2.1: Delegated to GirlRelationships component ##
        def spoil(self, nb):
            return self._relationships.spoil(nb)

## Phase 2.1: Delegated to GirlRelationships component ##
        def terrify(self, nb):
            return self._relationships.terrify(nb)

## Phase 2.1: Delegated to GirlSex component ##
        def pop_virginity(self, origin="brothel"):
            return self._sex.pop_virginity(origin)

## Phase 2.1: Delegated to GirlSex component ##
        def restore_virginity(self):
            return self._sex.restore_virginity()

## Phase 2.1: Delegated to GirlLogging component ##
        def count_occurences(self, context="all", original=False, add_list=None):
            return self._logging.count_occurences(context, original, add_list)

## Phase 2.1: Delegated to GirlSex component ##
        def talk_tastes(self, type):
            return self._sex.talk_tastes(type)


## Phase 2.1: Delegated to GirlSex component ##
        def try_to_remove_fix(self, fix_name, type=None):
            return self._sex.try_to_remove_fix(fix_name, type)

## Phase 2.1: Delegated to GirlSex component ##
        def remove_fixation(self, fix_name):
            return self._sex.remove_fixation(fix_name)

## Phase 2.1: Delegated to GirlSex component ##
        def has_fixation(self, type="pos", fix_name=None):
            return self._sex.has_fixation(type, fix_name)

## Phase 2.1: Delegated to GirlRelationships component ##
        def meet_MC(self):
            return self._relationships.meet_MC()


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

## Phase 2.1: Delegated to GirlTraining component ##
        def build_up(self, v): # FARM EVENTS - Builds-up her farm show jauge
            return self._training.build_up(v)

## Phase 2.1: Delegated to GirlTraining component ##
        def get_build_up(self): # FARM EVENTS - Recovers her farm show jauge
            return self._training.get_build_up()

## Phase 2.1: Delegated to GirlTraining component ##
        def reset_build_up(self):
            return self._training.reset_build_up()

        # ── Phase 2.1: Economy delegation aliases ──
        _customer_populations_safety_check_impl = customer_populations_safety_check

        # ── Phase 2.1: Mood delegation aliases ──
        # (Sanity methods now delegate directly to GirlMood — aliases removed)
        _change_energy_impl = change_energy
        _heal_impl = heal
        _full_rest_impl = full_rest
        _rest_impl = rest
        _can_heal_from_item_impl = can_heal_from_item

        # ── Phase 2.1: Schedule delegation aliases ──
        _get_schedule_impl = get_schedule
        _get_status_impl = get_status
        _get_status_summary_impl = get_status_summary

        # ── Phase 2.1: Stats delegation aliases ──
        _find_stat_impl = find_stat
        _get_stat_max_impl = get_stat_max
        _average_skills_impl = average_skills

        # ── Phase 2.1: Relationships delegation aliases ──

        # ── Phase 2.1: Dialogue delegation aliases ──
        _generate_personality_impl = generate_personality
        _adjust_personality_impl = adjust_personality
        _generate_background_impl = generate_background
        _pick_dialogue_impl = pick_dialogue
        _say_impl = say
        _rand_say_impl = rand_say

        # ── Phase 2.1: Traits delegation aliases ──
        _generate_traits_impl = generate_traits
        _has_perk_impl = has_perk

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

        # ── Phase 2.1: Sex delegation aliases ──
        _will_do_sex_act_impl = will_do_sex_act
        _toggle_sex_act_impl = toggle_sex_act
        _count_activated_sex_acts_impl = count_activated_sex_acts
        _refresh_sex_acts_impl = refresh_sex_acts
        _activate_sex_act_impl = activate_sex_act
        _deactivate_sex_act_impl = deactivate_sex_act
        _compare_preference_impl = compare_preference

        # ── Phase 2.1: Items delegation aliases | 物品方法别名 ──

        # -- Phase 2.1: Training delegation aliases | 训练方法别名 --
        _will_do_farm_act_impl = will_do_farm_act



#<Chris12 PackState>

####          FILES DICTIONARY FOR B KING                  ####################################################
##   Helper class for girl files and pictures.             ##################################################
##   Saves them in a global variable so that they          ##################################################
##     are only read once without getting saved by Renpy.  ##################################################
##   Also handles packstates.                              ##################################################
##                                                         ##################################################


#### END OF BK GIRLCLASS FILE ####
