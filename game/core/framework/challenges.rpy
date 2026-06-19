#### Challenges classes ####

init -2 python:
    class Spell(PicHolder):

        """ This class covers spells used by the MC """

        def __init__(self, name, pic = "aura1.webp", type = "passive", level = 0, cost = 0, effects = None, duration = None, sound = s_spell, description = __("A basic spell.")):

            self.name = name
            self.pic = Picture(pic, "resources/spells/" + pic)
            self.type = type
            self.level = level
            self.cost = cost # Passive spells have a cost of zero
            if effects:
                self.effects = effects
            else:
                self.effects = []

            self.duration = duration
            self.sound = sound
            self.description = get_description(description, self.effects)

            self.auto = False

        def get_cost(self):
            return self.cost

        def get_cost_description(self):
            if self.duration == "turn":
                return str_int(self.get_cost()) + " mana/turn"

            else:
                return str_int(self.get_cost()) + " mana"

    ## EN: Load opposed challenge chance table from JSON (BK Evolution), fallback to hardcoded.
    ## ZH: 从 JSON 加载对抗挑战概率表（BK Evolution），否则使用硬编码。
    _oct_json = DataLoader.load_opposed_chance_table()
    if _oct_json:
        opposed_chance_table = [tuple(x) for x in _oct_json.get("opposed_chance_table", [])]
    else:
        opposed_chance_table = [(5, 0.0), (4, 0.03), (3, 0.08), (2, 0.17), (1, 0.28), (0, 0.42), (-1, 0.58), (-2, 0.72), (-3, 0.83), (-4, 0.92), (-99, 1.0)]

    class MC_challenge(PicHolder, EffectBearer):
        """This class is used to run Player challenges and return a result."""

        def __init__(self, name, stat, opposed, name_i18n=None):

            self.name = name
            self.name_i18n = name_i18n if name_i18n else name
            self.pic = Picture(name + ".webp", "resources/ui/challenges/" + name + ".webp")
            self.stat = stat
            self.opposed = opposed
            self.d = 0 # stores the latest MC dice roll
            self.d_op = 0 # stores the latest opponent dice roll

            self.score = 0 # stores the latest MC score
            self.score_op = 0 # stores the latest opponent score

            self.result = 0 # stores the result of the latest challenge

        @classmethod
        def from_dict(cls, d):
            """EN: Build an MC_challenge from a JSON dict.
               ZH: 从 JSON 字典构建挑战。"""
            return cls(
                name=d.get("name", ""),
                stat=d.get("stat", ""),
                opposed=d.get("opposed", False),
                name_i18n=d.get("name_i18n", d.get("name", "")),
            )

        def get_score(self, diff, bonus=0, opponent_bonus=0, dice_faces=6, dice_nb = 1, raw=False):

            self.score = MC.get_stat(self.stat, raw=raw) + MC.get_effect("change", self.name + " challenges")

            self.d = dice(dice_faces, dice_nb)
            self.score += self.d + bonus

            if self.opposed:
                self.d_op = dice(dice_faces, dice_nb)
                self.score_op = diff + self.d_op + opponent_bonus

                result = self.score - self.score_op

            else:
                result = self.score - diff

            return result

        def adjust_diff(self, diff): # Adds 3 to difficulty if test is unopposed.
            if not self.opposed:
                return diff + 3
            return diff

        def run(self, diff, score=False, raw=False, bonus=0, opponent_bonus=0, dice_faces=6, dice_nb = 1, strict=False, forced=False): # Forced can be 'True' or an integer

            if forced:
                return forced
            elif not score:
                return self.run_pass(diff, bonus, opponent_bonus, dice_faces, dice_nb, raw, strict)
            else:
                return self.get_score(diff, bonus, opponent_bonus, dice_faces, dice_nb, raw)

        def run_pass(self, diff, bonus=0, opponent_bonus=0, dice_faces=6, dice_nb=1, raw=False, strict=False): # This test returns pass or fail. strict tests require a strictly superior result to succeed.

            self.result = self.get_score(diff, bonus, opponent_bonus, dice_faces, dice_nb, raw)

            if self.result > 0:
                return True
            elif self.result < 0:
                return False
            elif strict:
                return False
            else:
                return True

        def estimate_diff(self, diff, raw=False, score=False, bonus=0, opponent_bonus=0, strict=False, percentage=False, forced=False): # Returns difficulty as a qualifier or percentage

            if forced:
                return "Safe"

            differential = (diff + opponent_bonus) - (MC.get_stat(self.stat, raw) + bonus) + MC.get_effect("change", self.name + " challenges", randomize=False)

            if not strict:
                differential -= 1

            if not self.opposed:
                chance = 1.0 - (differential)/6.0
            else:
                for d, c in opposed_chance_table:
                    if differential >= d:
                        chance = c
                        break
                else:
                    raise AssertionError("Couldn't process differential during MC challenge.")

            if percentage:
                return str(int(chance*100)) + "%"

            else:
                if chance >= 1.0: # and not score:
                    return "Safe"
                elif chance > 0.8:
                    return "Very easy"
                elif chance > 0.6:
                    return "Easy"
                elif chance > 0.4:
                    return "Fair"
                elif chance > 0.2:
                    return "Hard"
                elif chance > 0.0:
                    return "Very hard"
                else:
                    return "Impossible"

    class Resource(object):

        """Resources are sold at the market and extracted in the city. They serve primarily for furniture and city events."""

        def __init__(self, name, rank, stat=None, sound=s_gold, description="", location=None):
            self.name = name
            self.rank = rank
            self.stat = stat
            self.pic = Picture(name + ".webp", "resources/ui/resources/" + name + ".webp")
            self.sound = sound
            self.description = description
            self.location = location
            if self.location:
                self.base_description = self.location.menu[0]

        @classmethod
        def from_dict(cls, d, location_resolver=None):
            """EN: Build a Resource from a JSON dict.
               ZH: 从 JSON 字典构建资源。
               location_resolver: callable that maps location name strings to Location objects."""
            location_name = d.get("location")
            location = None
            if location_name and location_resolver:
                location = location_resolver(location_name)
            return cls(
                name=d.get("name", ""),
                rank=d.get("rank", 0),
                stat=d.get("stat"),
                sound=d.get("sound", "gold.ogg"),
                description=d.get("description", ""),
                location=location,
            )

        def activate_extractor(self, first=True):
            auto_extractors[self.name] = True
            auto_extractors[self.name + " ON"] = True
            if first:
                auto_extractors[self.name + " durability"] = 150
            self.location.menu = (self.base_description + " [[Extractor ON]", self.location.menu[1])

        def deactivate_extractor(self, final=True):
            auto_extractors[self.name + " ON"] = False
            if final:
                auto_extractors[self.name] = False
                self.location.menu = (self.base_description, self.location.menu[1])
            else:
                self.location.menu = (self.base_description + " [[Extractor OFF]", self.location.menu[1])


    class Furniture(PicHolder):

        """Furniture are upgrades for the brothel that provide permanent bonuses."""

        def __init__(self, name, type, pic=None, rank=2, chapter=2, cost=None, duration=0, effects=None, base_description="", upgrade=False, can_deactivate=False, hidden_effect=False):
            self.name = name
            self.type = type
            if pic:
                self.pic = Picture(pic, "resources/items/furniture/" + pic)
            else:
                self.pic = Picture("misc.webp", "resources/items/misc/misc.webp")
            self.rank = rank # This is the rank at which the furniture becomes available
            self.chapter = chapter # This is the chapter at which the furniture becomes available (if not rank)
            if cost == None: cost = []
            self.cost = cost # Cost is a list of tuples (resource=str, amount=int)

            # Sort resources in same order
            self.cost.sort(key = lambda x: build_resources.index(x[0]))

            self.duration = duration
            if effects == None: effects = []
            self.effects = effects
            if hidden_effect:
                self.description = __("{b}%s{/b}: %s") % (self.name, base_description)
            else:
                self.description = __("{b}%s{/b}: %s") % (self.name, get_description(base_description, effects))
            self.upgrade = upgrade
            self.built = False
            self.can_deactivate = can_deactivate
            self.active = False

        def can_build(self):
            if brothel.current_building == self:
                return False
            elif self.built or (self.rank > district.rank) or (self.chapter > game.chapter):
                return False
            elif self.upgrade:
                if not furniture_dict[self.upgrade].built:
                    return False
            return True

        def get_duration(self): # Minimum one day duration outside of initial furniture
            return max(1, self.duration + MC.get_effect("change", "building duration"))

        def start_building(self):
            if self.get_duration():
                # Carpenter events
                if not story_flags["carpenter first build"]:
                    calendar.set_alarm(calendar.time+1, StoryEvent(label="iulia1", type="morning"))
                    story_flags["carpenter first build"] = True

                calendar.set_alarm(calendar.time + self.get_duration(), StoryEvent(label = "furniture_built", call_args=[self]))
                brothel.current_building = self
                brothel.started_building = calendar.time
                renpy.say(carpenter, __("I'll be finished in %s days. I'm sure you'll be happy with the result.") % str(self.get_duration()))
            else:
                self.build()

        def build(self, message=True):
            self.built = True
            if self not in brothel.furniture:
                brothel.furniture.append(self)
            if self.name == "Priestess outfit":
                all_furniture.append(billboard) # Unlock separated from the story event
            if self.upgrade:
                if furniture_dict[self.upgrade] in brothel.furniture:
                    brothel.furniture.remove(furniture_dict[self.upgrade])
                brothel.deactivate_furniture(furniture_dict[self.upgrade])
                if message:
                    renpy.call_screen("OK_screen", title = __("Furniture Upgraded"), message = __("%s has been upgraded to a %s.\n\n%s") % (self.upgrade, self.name, self.description), pic = self.pic, pic_size = "large")
            elif message:
                renpy.call_screen("OK_screen", title = __("Furniture Built"), message = __("A new %s has been built.\n\n%s") % (self.name, self.description), pic = self.pic, pic_size = "large")
            self.activate()

            # Carpenter events
            if not story_flags["iulia2 registered"] and len(brothel.furniture) >= 10:
                add_event("iulia2", chance = 1.0, type="city", location = "gallows", once = True, AP_cost = 1)
                story_flags["iulia2 registered"] = True
            if not story_flags["iulia3"] and story_flags["iulia2"] and len(brothel.furniture) >= 20:
                calendar.set_alarm(calendar.time+2, StoryEvent(label="iulia3", type="day"))
            if not story_flags["iulia4"] and story_flags["iulia3"] and furniture_dict["Good tools"].built:
                calendar.set_alarm(calendar.time+1, StoryEvent(label="iulia4", type="morning"))
            if not story_flags["iulia5"] and story_flags["iulia4"] and len(brothel.furniture) >= 30:
                calendar.set_alarm(calendar.time+2, StoryEvent(label="iulia5", type="day"))
            if not story_flags["iulia6"] and story_flags["iulia5"] and furniture_dict["Great tools"].built and brothel.has_room("tavern"):
                calendar.set_alarm(calendar.time+1, StoryEvent(label="iulia6", type="day"))
            if not story_flags["iulia7"] and story_flags["iulia6"] and furniture_dict["Master tools"].built:
                calendar.set_alarm(calendar.time+1, StoryEvent(label="iulia7", type="morning"))
            if not story_flags["iulia_H"] and story_flags["iulia7"] and len(brothel.furniture) >= 40:
                calendar.set_alarm(calendar.time+2, StoryEvent(label="iulia_H", type="morning"))
                story_flags["iulia_H"] = True
            
            test_achievement("furniture")

        def destroy(self, message=True):
            self.built = False
            if self in brothel.furniture:
                brothel.furniture.remove(self)
            self.deactivate()
            if self.upgrade:
                brothel.furniture.append(furniture_dict[self.upgrade])
                brothel.activate_furniture(furniture_dict[self.upgrade])
                if message:
                    renpy.call_screen("OK_screen", title = __("Furniture destroyed"), message = self.name + " has been destroyed and replaced with " + self.upgrade, pic = self.pic, pic_size = "large")
            elif message:
                renpy.call_screen("OK_screen", title = __("Furniture destroyed"), message = self.name + " has been destroyed.", pic = self.pic, pic_size = "large")
            self.activate()

        def activate(self):
            if not self.active and self.built:
                self.active = True
                update_effects()
                for e in self.effects:
                    if e.type == "event": # For events tied to the furniture
                        calendar.set_alarm(calendar.time, StoryEvent(e.target, arg=e.value))
                return True

            return False

        def deactivate(self):
            if self.active:
                self.active = False
                update_effects()
                return True
            return False

        def toggle(self):
            if self.active:
                self.deactivate()
            else:
                self.activate()

        def describe_cost(self):
            dlist = [__("%s %s") % (str(amount), resource) for resource, amount in self.cost]

            return and_text(dlist)


    class Loan(PicHolder):

        """A loan is a sum that must be paid back to the banker, with or without interest"""

        def __init__(self, amount, interest=0, duration=10): # Where interest is a float (interest_rate)
            self.amount = amount
            self.initial_amount = amount
            self.interest = interest
            self.duration = duration
            self.total_cost = int(amount * (1+interest))
            self.daily_cost = int(self.total_cost / duration)

        def repay(self):
            amount_reimbursed = get_change_min_max(self.amount, -self.initial_amount/self.duration, 0)
            interest_reimbursed = amount_reimbursed * self.interest

            MC.gold += int(amount_reimbursed + interest_reimbursed)
            self.amount += amount_reimbursed

            return -int(amount_reimbursed + interest_reimbursed)


## Achievement and Contract classes


init -2 python:
    class Mod(object):

        """This class is used to track external mods. Mods are declared in their respective rpy files, and automatically added to 'detected_mods' upon creation."""

        def __init__(self, name, folder, creator="Unknown", version= 1.0, pic=None, description=__("This is a mod for Brothel King."), help_prompts=None, init_label="", night_label = "", update_label = "", home_rightmenu_add_buttons=None, events=None, early_label="", load_label="", remove_label=""):

            #### Init variables - All declared variables below must not be changed after init, as they will not save and will be overwritten when the game starts
            super().__setattr__('name', name)
            super().__setattr__('init', True)

            self.path = "mods/" + folder + "/"
            self.creator = creator
            self.version = version
            if pic:
                self.pic = Picture(pic, self.path + pic)
            else:
                self.pic = None
            self.description = description
            self.full_name = name + " v" + str(self.version) + ", from " + creator

            ## help_prompts is a list of tuples (name, label), each representing a menu prompt in the 'help/mod/mod options' menu.
            ## 'name' is the prompt message as it appears on the menu button, and 'label' is the target label it will call (not jump).
            ## Several actions can be added to the list by adding tuples (name, label) to the list, each separated by a comma
            self.help_prompts = []
            ## Adds [mod name] to prompt messages for clarity
            if help_prompts:
                for prompt in help_prompts:
                    self.help_prompts.append(("[[" + self.name + "] " + prompt[0], prompt[1]))

            ## Early init label: This will run after the game is started, before the district and brothel is set-up.
            self.early_label = early_label

            ## Init label: This will run after the game is started, after the district and brothel is set-up.
            self.init_label = init_label
            self.night_label = night_label
            self.update_label = update_label
            self.chapter_labels = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None} # Stores a label to be called for a specific chapter

            ## Load label: This will run if the mod is loaded with a saved game
            self.load_label = load_label
            
            ## Remove label: This will run if the mod is deactivated, to enable some clean-up
            self.remove_label = remove_label

            ## Event dictionary (all mod events must be declared here)
            if events == None: 
                events = {}
            self.events = events

            ## Add home right menu buttons
            if home_rightmenu_add_buttons == None: 
                home_rightmenu_add_buttons = []
            self.home_rightmenu_add_buttons = home_rightmenu_add_buttons

            ## Phase 6: Hook system
            self.hooks = {}  # {hook_name: callback}
            self.api_version = 1

            #### Default variables
            for ev in self.events.values():
                ev.mod = self

            detected_mods[self.name] = self
            self.seen = False
            self.active = False

            # Turns on mod_settings dictionary to save variables after init
            super().__setattr__('init', False)


        ## Overrides regular assignation methods for attributes so that values do not get erased at every init
        def __setattr__(self, a, v):
            global mod_settings
            
            if a in ("name", "init") or super().__getattribute__('init'):
                super().__setattr__(a, v)

            # Sanity check
            if not "mod_settings" in globals().keys(): # mod_settings will be created the first time a custom Mod attribute is stored (outside init). It will be saved with saved games
                mod_settings = defaultdict(dict)

            mod_settings[self.name][a] = v

        def __getattribute__(self, a):
            try:
                init = super().__getattribute__('init')
            except:
                init = False

            if a in ("name", "init") or init:
                return super().__getattribute__(a)
            else:
                try:
                    return mod_settings[self.name][a]
                except:
                    return super().__getattribute__(a)


        def get_check(self): # Returns a list of values used for comparison
            return (self.version, self.path, self.init_label, len(self.events))

        def check_for_updates(self): # Checks a list of values used for comparison with existing mods

            global mod_traceback

            if self.get_check() != persistent.mods[self.name]["check"]:
#                mod_traceback += "Checked " + str(self.get_check()) + " against " + str(persistent.mods[self.name]["check"])
                return True
            return False

        def activate(self):
            self.flags = defaultdict(bool)
            if renpy.call_screen("yes_no", __("Do you want to activate ") + self.full_name + "?"):
                if not self.active or not persistent.mods[self.name]["active"]:
                    self.active = True
                    persistent.mods[self.name]["active"] = True
                    try:
                        game.activate_mod(self)
                    except:
                        pass
                    reset_updated_games()

                else:
                    renpy.notify(self.name + " is already active.")

        def deactivate(self):
            if renpy.call_screen("yes_no", __("Do you really want to deactivate ") + self.full_name + "? This might negatively affect games saved while this mod was on."):
                if self.active or persistent.mods[self.name]["active"]:
                    self.active = False
                    persistent.mods[self.name]["active"] = False
                    try:
                        game.deactivate_mod(self)
                    except:
                        pass
                    reset_updated_games()
                else:
                    renpy.notify(self.name + " couldn't be found among active mods.")

        def add_event(self, event_name, type=None, date=None, delay=1, call_args=None): # event_name is the event label (not object). date is the exact calendar date. If not provided, current time + delay is used instead (D+1 by default).

            if call_args:
                self.events[event_name].call_args = call_args

            if type:
                self.events[event_name].type = type
            else:
                type = self.events[event_name].type

            if type == "alarm":
                if not date:
                    date = calendar.time + delay
                calendar.set_alarm(date, self.events[event_name])

                if date <= calendar.time:
                    renpy.say("System", __("Warning: Event set to a past date. Change the event time or delay."))

            elif type in ("morning", "day", "night"):
                daily_events.append(self.events[event_name])

            elif type == "city":
                city_events.append(self.events[event_name])

        def set_condition(self, condition, value):
            self.flags[condition] = value

