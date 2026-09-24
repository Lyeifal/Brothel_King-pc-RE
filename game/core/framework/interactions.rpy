#### Interactions classes ####

init -2 python:
    class Event(object):

        """This class covers 2 kinds of events: Night events (run during working hours) and Day events (run when returning to the main screen). Day events should be phased out and replaced by Story Events"""

        def __init__(self, pic = None, background = None, char = None, text = "", changes = "", sound = None, with_st = None, type="Normal", label = None, object = None, order = 0, weight = 1, debug_id=0):

            self.pic = pic
            self.background = background
            self.char = char
            self.text = text
            self.sound = sound
            self.with_st = with_st
            self.type = type
            self.changes = changes
            self.label = label
            self.object = object
            self.order = order # Lower order = go first
            self.debug_id = debug_id

        def show_night(self):

#            renpy.show_screen("night", self.pic)

            log.changes = self.changes

            if self.sound:
                renpy.play(self.sound, "sound")

            renpy.say(self.char, self.text)

        def happens(self):
            return True

        def play(self):

            if self.label:

                if self.object:
                    renpy.call(self.label, self.object)

                else:
                    renpy.call(self.label)

            else:

                if self.sound:
                    renpy.play(self.sound, "sound")

                renpy.say(self.char, self.text)


    class StoryEvent():

        def __init__(self, label, chapter=0, rank=0, date=0, year=0, month=0, day=0, weekday="", chance = 1.0, type="any", location = None, locations = None, seasons = None, min_gold = -999999999, condition = None, not_condition = None, condition_func=None, call_args=None, arg=None, once = True, AP_cost = 1, order = 0, weight = 1, room = None, modes=None):
            # Use arg to transmit a single argument, call_args for several arguments ordered in a list. Don't use both.

            self.label = label
            self.chapter = chapter
            self.rank = rank
            self.date = date
            self.year = year
            self.month = month
            self.day = day
            self.weekday = weekday
            self.chance = chance
            self.type = type # Type can be: "any" (plays anytime), "city", "day" (plays on main screen), "night" (plays upon ending day), "morning" (plays after night events)
            self.location = location # location must be the location's name
            self.locations = locations # A list of location names
            self.seasons = seasons # A list of seasons
            self.min_gold = min_gold
            self.condition = condition
            self.not_condition = not_condition
            self.condition_func = condition_func # For complex conditions, this function is called with no arguments and must return a bool
            self.room = room
            if arg:
                call_args = [arg]
            elif call_args == None:
                call_args = []
            self.call_args = call_args # call_args must be a list
            self.once = once
            self.AP_cost = AP_cost
            self.order = order # Base order is 0. Lower values will fire first.

            ## EN: BK Evolution — Game mode filter for this event.
            ## ZH: BK Evolution — 此事件适用的游戏模式过滤器。
            ## modes can be None (all modes), a string (single mode), or a tuple/list of strings.
            self.modes = modes

            self.happened = False
            self.mod = None

        @classmethod
        def from_dict(cls, data):
            """EN: Create a StoryEvent from a JSON-compatible dict.
               ZH: 从 JSON 兼容的字典创建 StoryEvent 对象。"""
            kwargs = dict(data)
            # EN: Resolve function name strings to actual callables for condition_func.
            # ZH: 将 condition_func 的函数字符串解析为实际可调用对象。
            if isinstance(kwargs.get("condition_func"), str):
                func_name = kwargs.pop("condition_func")
                kwargs["condition_func"] = globals().get(func_name)
            return cls(**kwargs)

        def happens(self, type="any"): # Tests if happened, current chapter, chance of happening, location and custom story flags (optional)

            if type != "any" and self.type not in ("any", type):
                return False

            if self.happened and self.once:
                return False

            if game.chapter < self.chapter:
                return False

            if district.rank < self.rank:
                return False

            if calendar.time < self.date:
                return False

            if self.year and calendar.year != self.year:
                return False

            if self.month and calendar.month != self.month:
                return False

            if self.day and calendar.day != self.day:
                return False

            try:
                if self.weekday and calendar.get_weekday() != self.weekday:
                    return False
            except:
                self.weekday = None

            if self.min_gold > MC.gold:
                return False

            if renpy.random.random() > self.chance:
                return False

            if self.location:
                if self.location.lower() != selected_location.name.lower():
                    return False

            if self.locations:
                for loc in self.locations:
                    if loc.lower() == selected_location.name.lower():
                        break
                else:
                    return False

            if self.seasons:
                if calendar.get_season() not in self.seasons:
                    return False

            if self.condition:
                if self.mod:
                    if not self.mod.flags[self.condition]:
                        return False

                elif not story_flags[self.condition]:
                    return False

            if self.not_condition:
                if self.mod:
                    if self.mod.flags[self.not_condition]:
                        return False
                elif story_flags[self.not_condition]:
                    return False

            if self.room: # room must be spelled in lower case
                if not brothel.has_room(self.room):
                    return False

            if self.condition_func: # A custom function that must return 'True' or 'False'
                if not self.condition_func():
                    return False

            if self.mod:
                if self.mod not in game.active_mods.values():
                    return False

#            renpy.say("", self.label + "HAPPENS")

            return True

        def play(self):

            if self.once:
                r = story_remove_event(self.label)

                if not r:
                    if self.type == "city" and self in city_events:
                        city_events.remove(self)
                    elif self.type != "city" and self in daily_events:
                        daily_events.remove(self)

            renpy.call(self.label, *self.call_args)

            # Renpy probably doesn't reach those two command lines, so I have included them within the display_events label instead
            self.happened = True

            story_flags[self.label] = True

            return


    class Quest(object):

        """This class is a template for quests and classes"""

        def __init__(self, type, name, main_stat, second_stat, other_stats, tags, description, sound = s_sigh, special_event = (None, 1.0), commit_label=None, return_label=None, jp_type = None):

            self.type = type # "class" or "quest"
            self.name = name
            self.description = description
            self.tags = make_list(tags)
            self.sound = sound

            self.main_stat = main_stat
            self.secondary_stat = second_stat
            self.other_stats = other_stats
            self.xp = 0
            self.jp = 0
            self.jp_type = jp_type # a list of possible JP types

            self.enrolled = []
            self.special = None
            self.special_event = special_event[0] # To be implemented later
            self.special_event_chance = special_event[1] # To be implemented later
            self.commit_label = commit_label
            self.return_label = return_label

        @classmethod
        def from_dict(cls, d, sound_resolver=None, jp_type_resolver=None):
            """EN: Build a Quest from a JSON dict.
               ZH: 从 JSON 字典构建任务/课程模板。"""
            _sound = d.get("sound", "sigh")
            sound = s_sigh
            if sound_resolver:
                sound = sound_resolver(_sound)

            _jp = d.get("jp_type")
            jp_type = None
            if _jp:
                if isinstance(_jp, list):
                    jp_type = list(_jp)
                elif jp_type_resolver:
                    jp_type = jp_type_resolver(_jp)

            return cls(
                type=d.get("type", "quest"),
                name=__(d.get("name_i18n", d.get("name", ""))),
                main_stat=d.get("main_stat", ""),
                second_stat=d.get("second_stat", ""),
                other_stats=tuple(d.get("other_stats", [])),
                tags=d.get("tags", ""),
                description=__(d.get("description_i18n", d.get("description", ""))),
                sound=sound,
                special_event=tuple(d.get("special_event", [None, 1.0])) if d.get("special_event") else (None, 1.0),
                commit_label=d.get("commit_label"),
                return_label=d.get("return_label"),
                jp_type=jp_type,
            )

        def set_to(self, rank, pic, duration, special, requirements, pos_traits=None, neg_trait=None, gold=0, xp=0, rep=0): # For story events
            self.rank = round_int(rank)
            self.pic = pic
            self.duration = duration
            self.special = special
            self.requirements = requirements
            self.pos_traits = pos_traits or []
            self.neg_trait = None
            self.gold = gold
            self.xp = xp
            self.rep = rep
            self.energy = -5 * rank * self.duration

        def randomize(self, rank):

            self.enrolled = []
            self.rank = round_int(rank)

            ## Randomize picture

            self.pic = get_pic(quest_board, self.tags)


            ## Set duration

            self.duration = max(dice(2 + rank//2), rank//2) # Rank 1: 1-2d Rank 2: 1-3d Rank 3: 2-3d Rank 4: 2-4d Rank 5: 2-4d


            ## Test special status

            if dice(6) == 6:
                if self.type == "class":
                    self.special = rand_choice(("Cheap", "Masterclass"))
                elif self.type == "quest":
                    self.special = rand_choice(("High reward", "Notorious"))
            else:
                self.special = None

            ## Set bonus and stat cap for classes

            if self.type == "class":

                self.bonuses = []

                #? Improved bonuses with rank
                self.bonuses.append([self.main_stat, self.duration*2 + rank, self.duration*4 + rank]) # Stores min/max bonuses to stat per day

                if rank > 1 and dice(100) < (rank-1) * 25: # Chance of adding second bonus at higher ranks
                    self.bonuses.append([self.secondary_stat, self.duration + rank//1.5, self.duration*3 + rank//1.5]) # Stores min/max bonuses to stat per day
                if rank > 3 and dice(100) < (rank-3) * 25: # Chance of adding third bonus at higher ranks
                    self.bonuses.append([rand_choice(self.other_stats), self.duration-1 + rank//2, self.duration*2 + rank//2]) # Stores min/max bonuses to stat per day

                self.stat_cap = 55 * rank #? Experimental

                self.capacity = 1 + dice(rank+1)


            ## Randomize stat requirements for quests

            if self.type == "quest":

                self.requirements = []

                # Normal stats have higher requirements than sx stats at earlier ranks then converge at rank 5
                if self.main_stat.capitalize() in gstats_main:
                    self.requirements.append([self.main_stat, 20 * rank + dice(40, rank)])

                else:
                    self.requirements.append([self.main_stat, 4 * rank**2 + dice(40, rank)])

                if dice(100) < (rank - 1) * 25: # Chance of adding second requirement at higher ranks

                    if self.main_stat.capitalize() in gstats_main:
                        self.requirements.append([self.secondary_stat, 20 * (rank-1) + dice(40, rank-1)])

                    else:
                        self.requirements.append([self.secondary_stat, 4 * (rank-1)**2 + dice(40, rank-1)])

                if dice(100) < (rank - 2) * 25: # Chance of adding third requirement at higher ranks

                    if self.main_stat.capitalize() in gstats_main:
                        self.requirements.append([rand_choice(self.other_stats), 20 * (rank-1) + dice(40, rank-1)])

                    else:
                        self.requirements.append([rand_choice(self.other_stats), 4 * (rank-1)**2 + dice(40, rank-1)])


            ## Add 2 positive + 1 negative traits

            self.pos_traits = rand_choice(gold_traits + pos_traits, 2)

            self.neg_trait = rand_choice(neg_traits)


            ## Calculate rewards and costs

            if self.type == "quest":

                self.gold = 25*rank**2
                self.xp = 0
                self.rep = 0

                # Values have yet to be play-tested to make sure nothing is broken

                for stat, value in self.requirements:

                    if stat in gstats_main:
                        self.gold += value * quest_base_gold["normal"]
                        self.rep += 2 ** (rank-1)

                    else:
                        self.gold += value * quest_base_gold["sex"]
                        self.rep += 2 * (2 ** (rank-1))

                    self.xp += value * rank

                # Apply duration bonus (long quests bring more cash, short quests are good for rep)

                self.gold *= self.duration + 0.05*(self.duration-1)
                self.rep *= 1 + 0.05*(self.duration-1)
                self.xp *= self.duration

                if self.special == "High reward":
                    self.gold *= 1.5

                self.gold = round_int(self.gold * brothel.get_effect("boost", "quest rewards") * game.get_diff_setting("rewards"))
                self.rep = round_int(self.rep * brothel.get_effect("boost", "quest rewards") * game.get_diff_setting("rewards"))
                self.xp = round_int(self.xp * brothel.get_effect("boost", "quest rewards") * game.get_diff_setting("rewards"))

            elif self.type == "class":

                self.gold = 25*rank**2

                for stat, _min, _max in self.bonuses:
                    if stat in gstats_main:
                        self.gold += (_min+_max)/2 * 5
                    else:
                        self.gold += (_min+_max)/2 * 10

                # Classes now affect JP
                self.jp = (2 * rank**2) * self.duration * game.get_diff_setting("rewards") #? Experimental
                self.jp_target = rand_choice(self.jp_type)

                self.rep = (1 + 0.05*(self.duration-1)) * 2**(rank-1) * game.get_diff_setting("rewards")

                if self.special == "Cheap":
                    self.gold = round_int(0.75*self.gold)

            self.energy = -5 * rank * self.duration


        def test_eligibility(self, girl, ignore_status = False): # Returns a tuple: bool + ttip

            if not ignore_status:
                if girl.hurt > 0 or girl.away or girl.exhausted:
                    return (False, _("Your girl is unable to work or study at the moment."))

            if self.type == "class":

                if self.capacity <= len(self.enrolled):
                    return (False, "This class is full.")

                elif MC.gold >= self.gold:

                    for stat, _min, _max in self.bonuses:
                        if girl.get_stat(stat, raw=True) < self.stat_cap:
                            return (True, _("Register %s for the selected class.") % girl.fullname)

                    return (False, _("Your girl's skills are too high to learn anything from this class."))

                else:
                    return (False, _("You do not have enough money to register a girl for this class."))


            elif self.type == "quest":

                for stat, value in self.requirements:
                    if girl.get_stat(stat) < value:
                        return (False, _("Your girl doesn't meet the requirements for this assignment."))
                return (True, __("Send %s on this assignment.") % girl.fullname)

            raise AssertionError("Something is weird with " + self.type)

        def count_eligible_girls(self):

            eligible = sum(1 for girl in MC.girls if self.test_eligibility(girl, ignore_status=True)[0])

            return eligible

        def get_gold(self):
            if self.type == "class":
                return max(0, int(self.gold * (1.0 - class_discount*len(self.enrolled))))
            return self.gold

        def get_results(self, girl):

            title = __("%s completed") % self.type.capitalize()
            description = __("%s has returned from her %s. ") % (girl.fullname, self.type)

            if self.type == "class":

                # Only mood affects learning for now (from +5 to -5)
                perf = dice(6, 2) + girl.mood // 20

                # Having friends in the class improves learning (checked twice: on enrollment and when results are delivered)

                for g in girl.friends:
                    if g in self.enrolled:
                        girl.class_friend_bonus = 2
                        break
                for g in girl.rivals:
                    if g in self.enrolled:
                        girl.class_friend_bonus = -1
                        break

                perf += girl.class_friend_bonus

                # Memories of rewards and punishment

                perf += girl.remembers("reward", "class good result")
                perf += girl.remembers("punish", "class bad result")

                if perf >= 12:
                    description += __("She studied very hard and made exceptional progress.")
                    boost = 2.0

                    girl.track_event("class good result", arg=__("She studied really hard for her %s class.") % self.name)

                elif perf >= 9:
                    description += __("She listened carefully to her teacher and made good progress.")
                    boost = 1.5

                    girl.track_event("class good result", arg=__("She made good progress during her %s class.") % self.name)

                elif perf <= 2:
                    description += __("She was distracted and didn't pay much attention to her teacher, hindering her progress.")
                    boost = 0.75

                    girl.track_event("class bad result", arg=__("She didn't study hard during her %s class.") % self.name)

                elif perf <= 5:
                    description += __("She didn't care about the lessons at all, making almost no progress.")
                    boost = 0.5

                    girl.track_event("class bad result", arg=__("She didn't study at all for her %s class.") % self.name)

                else:
                    description += __("She made some progress with the help of her teacher.")
                    boost = 1.0

                if girl.class_friend_bonus > 0:
                    description += __(" She was happy to study alongside friends.")
                    girl.change_mood(10)
                elif girl.class_friend_bonus < -1:
                    description += __(" She didn't like that she was in the same class as her rival.")
                    girl.change_mood(-5)

                if self.special == "Masterclass":
                    boost *= 1.5

                boost *= girl.get_effect("boost", "class results") * game.get_diff_setting("rewards")

                changes = [(stat, round_int(girl.change_stat(stat, renpy.random.randint(_min, _max)*boost, custom_cap = self.stat_cap))) for stat, _min, _max in self.bonuses]

            elif self.type == "quest":

                # Only main stat affects result. Random variation from +6 to -6 times rank
                perf = girl.get_stat(self.main_stat) + girl.mood // 5 + dice(13, self.rank) - 7*self.rank - self.requirements[0][1]

                # Memories of rewards and punishment

                perf += girl.remembers("reward", "quest good result")
                perf += girl.remembers("punish", "quest bad result")

                # Story override #
                if "Story" in self.tags:
                    perf = 0
                    boost = 1.0

                elif perf >= 20 * self.rank:
                    description += __("{color=[c_orange]}Her performance was amazing. The customer was ecstatic!{/color}")
                    boost = 1.5

                    girl.track_event("quest good result", arg=__("She performed {color=[c_emerald]}amazingly well{/color} on a quest"))

                elif perf >= 10 * self.rank:
                    description += __("{color=[c_emerald]}She performed well. The customer was happy.{/color}")
                    boost = 1.25

                    girl.track_event("quest good result", arg=__("She performed {color=[c_emerald]}well{/color} on a quest"))

                elif perf < 0:
                    description += __("{color=[c_red]}She performed poorly. The customer was disappointed and refused to pay in full.{/color}")
                    boost = 0.75
                    girl.track_event("quest bad result", arg=__("She performed {color=[c_crimson]}badly{/color} while on a quest"))

                else:
                    description += __("She completed the assignment without incident.")
                    boost = 1.0

                had = []

                for trait in self.pos_traits:
                    if girl.has_trait(trait.name):
                        had.append(trait.get_past_tense())
                        boost *= 1.5

                if had:
                    description += __(" The customer was excited that she %s.") % and_text(had)

                if self.neg_trait:
                    if girl.has_trait(self.neg_trait.name):
                        description += __(" The customer was upset that she %s.") % self.neg_trait.get_past_tense()
                        boost /= 2.0

                boost *= girl.get_effect("boost", "quest results") # Note quest results boost is different from quest reward boost

                reward = round_int(self.gold*boost)
                self.rep = round_int(self.rep*boost)

                if self.special == "Notorious":
                    self.rep *= 2.0

                MC.gold += reward
                girl.add_log("quest_gold", reward, -1)

            if self.xp:
                xp = round_int(girl.change_xp(self.xp))
                girl.add_log("total_xp", xp, -1)

            if self.jp:
                jp = round_int(girl.change_jp(self.jp, self.jp_target))
                girl.add_log("total_jp", jp, -1)
                girl.add_log(self.jp_target + "_jp", jp, -1)

            rep = round_int(girl.change_rep(self.rep))
            energy, status = girl.change_energy(self.energy)

            if status == "exhausted":
                " She is {color=[c_red]}exhausted{/color} and will need to rest until she recovers."

            description += "\n"

            if self.jp and self.type == "class":
                girl.add_log("class_jp", jp, -1)

                for stat, value in changes:
                    description += stat_increase_dict["stat"] % (__(stat.capitalize()), value)

            elif self.xp and self.type == "quest":
                girl.add_log("quest_xp", xp, -1)

                description += stat_increase_dict["gold+"] % reward

            if self.xp:
                description += stat_increase_dict["xp_dark"] % xp
            if self.jp:
                description += stat_increase_dict["jp"] % jp + "(%s)" % self.jp_target
            description += stat_increase_dict["rep"] % rep
            description += stat_increase_dict["stat_neg"] % (__("Energy"), round_int(energy))

            if girl.ready_to_level():
                girl.level_up()
                description += stat_increase_dict["level"]

            if girl.ready_to_rank():
                description += stat_increase_dict["rank"]

            return title, description


init -10 python:

    class GirlInteractionTopic(object):

        def __init__(self, type, group, caption, label, AP_cost=1, MP_cost=0, gold_cost=0, act=None, condition=None, advanced=False, love_test=None, relationship_level=0):

            self.type = type # Determines which tab the option belongs to in the interaction menu
            self.group = group # Determines which group the interaction is counted a part of (e.g. all training shares the 'train' group)
            self.caption = caption
            self.label = label
            self.AP_cost = AP_cost
            self.base_MP_cost = MP_cost
            self.gold_cost = gold_cost
            self.act = act # For training and magic training
            self.advanced = advanced # Determines if advanced options are available
            self.condition = condition
            self.love_test = love_test
            self.relationship_level = relationship_level

        @classmethod
        def from_dict(cls, data):
            """EN: Create a GirlInteractionTopic from a JSON dict.
               ZH: 从 JSON 字典创建 GirlInteractionTopic 对象。"""
            return cls(
                type=data.get("type"),
                group=data.get("group"),
                caption=__(data.get("caption_i18n", "")),
                label=data.get("label", ""),
                AP_cost=data.get("AP_cost", 1),
                MP_cost=data.get("MP_cost", 0),
                gold_cost=data.get("gold_cost", 0),
                act=data.get("act"),
                condition=data.get("condition"),
                advanced=data.get("advanced", False),
                love_test=data.get("love_test"),
                relationship_level=data.get("relationship_level", 0)
            )

        def get_gold_cost(self):
            return self.gold_cost*(district.rank ** 2)

        def get_MP_cost(self, girl):
            if self.base_MP_cost:
                return max(1, self.base_MP_cost + girl.rank - 2)
            return 0

        def is_shown(self, girl): # The option won't display unless the condition is True
            if self.love_test != None:
                if girl.get_love() + MC.get_charisma() >= self.love_test: # a value of 0 for love_test will be used in the test. Give love_test a 'None' value to ignore the test.
                    return True
                else:
                    return False

            if self.relationship_level:
                if girl.MC_relationship_level >= self.relationship_level:
                    return True
                else:
                    return False

            if not self.condition:
                return True
            elif self.condition == "has_worked":
                if girl.has_worked:
                    return True
            elif self.condition == "other_girls":
                if len(MC.girls) >= 2:
                    return True
            elif self.condition == "story":
                if girl.flags["story"] == 50: #! To do: Make it so that she can repeat earlier parts of the story
                    return True
            elif self.condition == "neg_fix":
                neg_fix = [fix.name for fix in girl.neg_fixations if girl.personality_unlock[fix.name]]
                if neg_fix:
                    return True
            elif self.condition == "free-form":
                if girl.will_do_sex_act("naked") and len(girl.get_trainable_sex_acts()) >= 3:
                    return True
            elif self.condition == "master_bedroom_add":
                if brothel.master_bedroom.level >= 1 and girl not in brothel.master_bedroom.girls:
                    return True
            elif self.condition == "master_bedroom_remove":
                if girl in brothel.master_bedroom.girls:
                    return True
            elif self.condition == "can_undress":
                if girl.get_effect("special", "naked") and not girl.naked:
                    return True
            elif self.condition == "dressed":
                if not girl.naked:
                    return True
            elif self.condition == "naked":
                if girl.naked:
                    return True
            elif self.condition == "farm":
                if farm.active:
                    return True
            elif self.condition == "debug_mode":
                if debug_mode:
                    return True
            elif self.condition == "gold_driver":
                if MC.hypnotize_driver == "gold":
                    return True
            elif self.condition == "mana_driver":
                if MC.hypnotize_driver == "mana":
                    return True

            else: # Other conditions should be strings that will be tested as a boolean flag (start flag name with ! to test for False)
                if self.condition.startswith("!") and not girl.flags[self.condition[1:]]:
                    return True
                elif girl.flags[self.condition]:
                    return True

            return False

        def is_available(self, girl, mode=None, free=False): # The option will display inactive if False. Returns a tuple with bool and a tooltip description.

            if girl.away:
                return False, _("%s is away. You cannot interact with her.") % girl.fullname

            if self.group == "train":
                if girl.exhausted:
                    return False, _("You cannot train %s, because she is exhausted.") % girl.fullname

                elif girl.hurt > 0:
                    return False, _("You cannot train %s, because she is hurt.") % girl.fullname

                elif not MC.training:
                    return False, _("Training is disabled due to NewGame+ challenge")

            if mode: # 'mode' is either 'lecture' (Talk), 'train' or advanced.
                if mode == "lecture":
                    pass
                elif mode in ("train", "advanced"):

                    text1 = ""

                    if self.type == "train":
                        if training_test_dict[self.act]:
                            for cond, pref in training_test_dict[self.act]:
                                if compare_preference(girl, cond, pref):
                                    break
                                if text1:
                                    text1 += __(" or ")
                                text1 += __("%s (%s)") % (cond, pref)
                            else:
                                return False, __("You cannot train %s yet. Requirements: %s") % (self.act, text1)

                    elif self.type == "magic":
                        if magic_training_test_dict[self.act]:
                            for cond, pref in magic_training_test_dict[self.act]:
                                if compare_preference(girl, cond, pref):
                                    break
                                if text1:
                                    text1 += __(" or ")
                                text1 += __("%s (%s)") % (cond, pref)
                            else:
                                return False, __("You cannot train %s yet. Requirements: %s") % (self.act, text1)

                    if mode == "advanced":
                        if MC.interactions < 2 and not free:
                            return False, __("You do not have enough interactions left for advanced training.")

                        if not girl.personality_unlock[self.act]:
                            return False, __("You need to train a girl at least once before you can access advanced training.")

                elif mode == "master_bedroom_add":
                    if not brothel.master_bedroom.can_have_girl():
                        return False, __("The master bedroom is already full.")

            if MC.interactions < 1 and self.AP_cost > 0 and not free:
                return False, __("You have no interactions left for today.")
            elif MC.interactions < self.AP_cost and not free:
                return False, __("You do not have enough interactions left for this.")
            elif self.get_MP_cost(girl) and MC.mana < self.get_MP_cost(girl):
                return False, __("You do not have enough mana for this training (%i{image=img_MP}).") % self.get_MP_cost(girl)
            elif self.get_gold_cost() and MC.gold < self.get_gold_cost():
                return False, __("You do not have enough money to pay for this training (%i{image=img_gold}).") % self.get_gold_cost()
            elif self.group == "train" and girl.MC_interact_counters[self.group] >= 1:
                return False, __("You cannot train a girl more than once per day.")
            elif self.group in ("reward", "discipline") and girl.MC_interact_counters[self.group] >= 1:
                return False, __("You cannot reward or discipline a girl more than once per day.")
            elif self.group in ("gold", "gift", "sex_reward", "rape", "offer") and girl.MC_interact_counters[self.group] >= 1:
                return False, __("You cannot do that more than once per day.")
            elif self.group == "offer" and len(MC.girls) >= brothel.bedrooms:
                return False, __("You don't have room in your brothel for another girl.")
            elif self.group and girl.MC_interact_counters[self.group] >= 3:
                return False, __("You cannot %s more than 3 times a day with a girl.") % self.group
            elif self.label == "slave_master_bedroom_add" and not brothel.master_bedroom.can_have_girl():
                return False, __("The master bedroom is already full.")

            if self.condition == "free-form":
                return True, __("In free-form training, you will be able to switch between different sex acts she is comfortable with. Only the {b}last chosen sex act{/b} will actually be trained.")

            return True, ""



    class GirlInteraction(object):

        def __init__(self, girl, topic, mode=None, free=False):

            self.girl = girl
            self.topic = topic
            self.mode = mode
            self.free = free

            if self.free or topic.AP_cost == 0:
                self.cost = 0
            elif self.mode == "advanced":
                self.cost = 2
            else:
                self.cost = 1

            self.type = topic.type # This gets replaced by chat or react type in the course of the interaction (not stricly necessary, but easier to manipulate)
            self.act = topic.act # Can be any of the extended sex acts

            self.response = None # The girl's response. Can be: 'afraid' (failed fear test and too afraid to talk), 'begged', 'accepted' (obeyed request), 'resisted' (shows reluctance), 'refused' (flat-out rejection)
            self.MC_reaction = None # MC's reaction to the girl. Can be: 'love', 'neutral', 'fear' (when removing fixations), 'proceed', 'force', 'warning', 'give up' (if begged, refused or rejected), 'encourage' (chatting), 'discipline' (scold or punish her), 'praise friend', 'demean rival', 'break friendship', 'make peace'
            self.reason = None # Reason for Reward/Punishment. Can be: '', back', or any positive, neutral or negative reason from recent_event_templates
            self.pic = None
            self.score = 0
            self.result = None
            self.other_girl = None
            self.canceled = False

        def resolve(self):

#            renpy.say("", "RESOLVING")

            if self.canceled:
                return

            girl = self.girl

            if debug_mode:
                renpy.call_screen("OK_screen", girl.fullname + "-Interaction resolving", "Group: [inter.topic.group]\nType: [inter.type]\nAction: [inter.topic.caption]\nReason: [inter.reason]\nResponse: [inter.response]\nAct: [inter.act]\nResult: [inter.result]\nMC Reaction: [inter.MC_reaction]")
            else:
                norollback()


            # Charging interactions

            if self.result in ("moderate", "fail") or self.MC_reaction == "give up": # Failed advanced training attempts only cost 1 AP
                MC.interactions -= 1
            else:
                MC.interactions -= self.cost

            # Tracking interaction count
            girl.MC_interact_counters[self.topic.group] += 1

            if topic.type == "react":
                girl.MC_interact_counters["react"] += 1

            # Creating local variables for the stat changes
            m = 0 # mood
            l = 0 # love
            f = 0 # fear
            p = 0 # prestige
            bea = 0 # beauty
            bod = 0 # body
            cha = 0 # charm
            ref = 0 # refinement
            ob = 0 # obedience
            lib = 0 # libido
            sen = 0 # sensitivity
            con = 0 # constitution
            sv = 0 # service
            sx = 0 # sex
            an = 0 # anal
            fe = 0 # fetish
            gd = 0 # good
            ev = 0 # evil
            ne = 0 # neutral
            brk = defaultdict(int) # preferences
            inter = 0 # interactions
            en = 0 # energy
            virgin = False
            spillover = {}

            if girl.get_effect("special", "fear interactions"): # Evil power effect
                f += 1

            if self.topic.type == "chat":

                # In case she is too afraid to talk

                if self.response == "afraid":
                    ## Personality unlocking
                    # girl.personality_unlock["DM"] += dice(6) + MC.get_charisma() # Temp, see how it behaves
                    pass

                else:

                    ## 1. Personality unlocking
                    # if self.response in ("accepted", "resisted"):
                    #     if self.type == "slave_life":
                    #         unlock = "DS"
                    #         dice_nb = 1
                    #     elif self.type == "brothel":
                    #         unlock = "LM"
                    #         dice_nb = 1
                    #     elif self.type == "customers":
                    #         unlock = "MI"
                    #         dice_nb = 1
                    #     elif self.type == "other_girls":
                    #         unlock = "EI"
                    #         dice_nb = 1
                    #     elif self.type == "well_being":
                    #         unlock = "DS"
                    #         dice_nb = 2
                    #     elif self.type == "feelings":
                    #         unlock = "LM"
                    #         dice_nb = 2
                    #     elif self.type == "tastes":
                    #         unlock = "MI"
                    #         dice_nb = 2
                    #     elif self.type == "origins":
                    #         unlock = "EI"
                    #         dice_nb = 2
                    #     else:
                    #         raise AssertionError, "Type not found. Type is " + str(self.type)

                    #     girl.personality_unlock[unlock] += dice(6, dice_nb) + MC.get_charisma() # Temp, see how it behaves

                    ## 2. Mood change

                    if self.MC_reaction != "discipline":

                        # Extravert people like chatting

                        if girl.is_("very extravert"):
                            m += 2
                        elif girl.is_("extravert"):
                            m += 1
                        elif girl.is_("very introvert"):
                            m -= 1

                        # Mood improves when chatting (except if punished)

                        m += 1

                    else: # Discipline

                        # Negative impact is stronger on dom girls

                        if girl.is_("very dom"):
                            m -= 2
                        elif girl.is_("dom"):
                            m -= 1
                        elif girl.is_("very sub"):
                            m += 1

                    ## 3. Personality unlocking

                    # Story unlocking, faster if chatting about personal stuff: First step unlocks at 4, then 10, then 20

                    if self.type in ("well_being", "feelings", "tastes", "origins"):
                        girl.personality_unlock["story"] += 1 + 0.1 * MC.get_charisma()
                    else:
                        girl.personality_unlock["story"] += 0.5 + 0.05 * MC.get_charisma()


                    ## 4. Love and fear

                    r = dice(6) + MC.get_charisma()

                    if self.MC_reaction == "encourage": # Idealist girls like to be encouraged

                        m += dice(3)

                        if r >= 6:
                            f -= 1

                        if r >= 9:
                            l += 1

                        if girl.is_("very idealist"):
                            l += 0.5
                            f -= 1
                        elif girl.is_("idealist"):
                            l += 0.25
                            f -= 0.5
                        elif girl.is_("materialist"):
                            f -= 0.25

                    elif self.MC_reaction == "discipline": # Dom girls dislike being disciplined

                        m -= dice(3)

                        if r < 6:
                            l -= 1

                        if r >= 9:
                            f += 1

                        if girl.is_("very sub"):
                            l += 0.5
                            f += 1
                        elif girl.is_("sub"):
                            l += 0.25
                            f += 0.5
                        elif girl.is_("very dom"):
                            l -= 0.5
                        elif girl.is_("dom"):
                            l -= 0.25


                    ## 5. Random skill increases

                    r = dice(6) + MC.get_charisma()

                    if self.type == "slave_life":
                        if r >= 9:
                            ob += 1

                    elif self.type == "brothel":
                        if r >= 9:
                            lib += 1

                    elif self.type == "customers":
                        if r >= 9:
                            sen += 1

                    elif self.type == "other_girls":
                        if r >= 9:
                            cha += 1

                    ## Impact other girls (if necessary)

                    if self.other_girl:

                        r = dice(6) + MC.get_charisma()

                        if self.MC_reaction == "praise friend": # Extraverts and idealists like to be encouraged in their relationships
                            m += dice(3)

                            if r >= 6:
                                f -= 1

                            if r >= 9:
                                l += 1

                            if girl.is_("very extravert"):
                                l += 0.5
                                f -= 1
                            elif girl.is_("extravert"):
                                l += 0.25
                                f -= 0.5
                            elif girl.is_("introvert"):
                                f += 0.5

                            if girl.is_("very idealist"):
                                l += 0.5
                            elif girl.is_("idealist"):
                                l += 0.25
                            elif girl.is_("materialist"):
                                l -= 0.5

                            self.other_girl.change_love(1 * (1+MC.get_charisma()/10))

                        elif self.MC_reaction == "demean rival": # Extraverts and materialists like to be encouraged in their feuds

                            m += dice(3)

                            if r >= 6:
                                f -= 1

                            if r >= 9:
                                l += 1

                            if girl.is_("very extravert"):
                                l += 0.5
                            elif girl.is_("extravert"):
                                l += 0.25
                            elif girl.is_("introvert"):
                                f += 0.5

                            if girl.is_("very materialist"):
                                l += 0.5
                            elif girl.is_("materialist"):
                                l += 0.25
                            elif girl.is_("idealist"):
                                l -= 0.5

                            self.other_girl.change_love(-1 * (1+MC.get_charisma()/10))

                        elif self.MC_reaction == "break friendship": # Extraverts and idealists hate to be discouraged in their relationships

                            m -= dice(6)

                            if r >= 6:
                                l -= 1

                            if r >= 9:
                                f += 1

                            if girl.is_("very extravert"):
                                l -= 2
                                f += 1
                            elif girl.is_("extravert"):
                                l -= 1
                                f += 0.5
                            elif girl.is_("introvert"):
                                l -= 0.5

                            if girl.is_("very idealist"):
                                l -= 2
                                f += 1
                            elif girl.is_("idealist"):
                                l -= 1
                                f += 0.5
                            elif girl.is_("materialist"):
                                f += 0.5

                            girl.change_relationship(self.other_girl, -1 * MC.get_charisma()/3)

                            self.other_girl.change_love(-1)

                        elif self.MC_reaction == "make peace": # Extraverts and materialists don't like to be discouraged in their feuds

                            m -= dice(3)

                            if r >= 6:
                                l -= 1

                            if r >= 9:
                                f += 1

                            if girl.is_("very extravert"):
                                l -= 1
                                f += 0.5
                            elif girl.is_("extravert"):
                                l -= 0.5
                            elif girl.is_("introvert"):
                                f -= 0.5

                            if girl.is_("very materialist"):
                                l -= 1
                                f += 0.5
                            elif girl.is_("materialist"):
                                l -= 0.5
                            elif girl.is_("idealist"):
                                l += 0.5

                            girl.change_relationship(self.other_girl, MC.get_charisma()/3)

                            self.other_girl.change_love(1)


            elif self.topic.type == "train" and self.mode != "lecture": # Non-magical training, excluding lectures

                ## In case she refused training

                r = dice(6) + MC.get_charisma()

                # MC gave up

                if self.MC_reaction == "give up":
                    f -= 1

                    if self.response == "begged":
                        gd += 1

                    elif self.response == "resisted":
                        ev -= 1 # MC gets less evil when not forcing

                        if r <= 6: # Girls may respect the player less
                            ob -= dice(3)

                    if self.response != "refused": # Repressed girls are more relieved when MC gives up
                        if girl.is_("very modest"):
                            l += 1
                            f -= 1
                        elif girl.is_("modest"):
                            l += 0.5
                            f += 0.5
                        else:
                            ob -= 1

                elif self.MC_reaction == "warning": # Warnings work better on sub girls
                    ev -= 1

                    if self.response == "begged":
                        ev -= 1

                    if girl.is_("very sub"):
                        f += 1
                        ob += 2
                    elif girl.is_("sub"):
                        f += 0.5
                        ob += 1
                    elif girl.is_("very dom"):
                        f -= 1
                        ob -= 2
                    elif girl.is_("dom"):
                        f -= 0.5
                        ob -= 1


                # MC got into a fight and lost

                elif self.response == "refused" and self.result == "fail":
                    ev += 1
                    l -= 5
                    f -= 5

                ## If she went on with the training

                else:
                    ## 1. Mood change

                    m -= 1

                    if girl.fear >= girl.love + 10: # She doesn't like interacting with MC
                        m -= 1
                    elif girl.love >= girl.fear + 10: # She likes the MC
                        m += 1

                    if self.MC_reaction == "encourage":
                        m += 1
                    elif self.MC_reaction == "discipline":
                        m -= 1

                    ## 2. Stat changes (normal training)

                    if self.act in ("obedience", "constitution", "lecture"):

                        r = dice(6) + MC.get_charisma()

                        if self.act == "obedience":
                            if self.result == "good":
                                ob += dice(6)
                            elif self.MC_reaction == "discipline": # Scolding her might have a good effect
                                if r >= 9:
                                    ob += dice(3)

                        elif self.act == "constitution":
                            if self.result == "good":
                                con += dice(6)
                            elif self.MC_reaction == "discipline": # Scolding her might have a good effect
                                if r >= 9:
                                    con += dice(3)

                    # 3. Love and fear (sexual training)

                    else:

                        r = dice(6) + MC.get_charisma()

                        if self.response == "accepted": # Lewd girls like consensual sex, repressed girls are reassured

                            f -= 0.5

                            if girl.is_("very lewd"):
                                l += 1
                            elif girl.is_("lewd"):
                                l += 0.5
                            elif girl.is_("very modest"):
                                f -= 1
                            elif girl.is_("modest"):
                                f -= 0.5

                        elif self.response == "resisted": # Dom and repressed girls hate being forced, sub and lewd girls don't mind too much
                            ne += 1

                            f += 1

                            if girl.is_("very dom"):
                                l -= 1
                            elif girl.is_("dom"):
                                l -= 0.5
                            elif girl.is_("very sub"):
                                l += 1
                            elif girl.is_("sub"):
                                l += 0.5

                            if girl.is_("very modest"):
                                f += 1
                            elif girl.is_("modest"):
                                f += 0.5
                            elif girl.is_("very lewd"):
                                f -= 1
                            elif girl.is_("lewd"):
                                f -= 0.5

                        elif self.response == "begged": # If MC ignored her begging
                            gd -= 1

                            if girl.is_("very sub"): # Reminder: Only sub girls may beg
                                l += 1.5
                                f += 1
                            elif girl.is_("sub"):
                                l += 0.5
                                f += 0.5

                            if girl.is_("very modest"):
                                f += 1
                            elif girl.is_("modest"):
                                f += 0.5
                            elif girl.is_("very lewd"):
                                f -= 1
                            elif girl.is_("lewd"):
                                f -= 0.5

                        elif self.response == "refused": # Dom and repressed girls hate being forced. Very sub and very lewd girls kind of like it
                            ev += 1

                            f += 3

                            if girl.is_("very dom"):
                                l -= 2
                            elif girl.is_("dom"):
                                l -= 1
                            elif girl.is_("very sub"):
                                l += 0.5

                            if girl.is_("very modest"):
                                f += 2
                            elif girl.is_("modest"):
                                f += 1
                            elif girl.is_("very lewd"):
                                f -= 1

                        # Obedience may increase during s. training

                        if r >= 9:
                            ob += dice(3)
                        elif r >= 6:
                            ob += 1

            elif self.topic.type == "magic": # Magical training

                if self.result == "success": # Note: stat changes and breaking handled with sex act results below
                    if girl.magic_training == "positive":
                        l += 1
                    elif girl.magic_training == "negative":
                        f += 1

                    if self.act == "obedience":
                        ob += dice(6)
                        if MC.get_effect("special", "hypnosis spillover"):
                            spillover["obedience"] = ob//2
                    elif self.act == "libido":
                        lib += dice(6)
                        if MC.get_effect("special", "hypnosis spillover"):
                            spillover["libido"] = lib//2
                    elif self.act == "sensitivity":
                        sen += dice(6)
                        if MC.get_effect("special", "hypnosis spillover"):
                            spillover["sensitivity"] = sen//2

                elif self.result == "moderate": # Breaking handled here (no sex happens)

                    if girl.magic_training == "positive":
                        l += 0.5
                    elif girl.magic_training == "negative":
                        f += 0.5

                    if self.act == "obedience":
                        ob += dice(3)
                    elif self.act == "libido":
                        lib += dice(3)
                    elif self.act == "sensitivity":
                        sen += dice(3)
                    else:
                        if girl.magic_training == "positive":
                            brk[self.act] += girl.raise_preference(self.act, "love", 0.75)
                        elif girl.magic_training == "negative":
                            brk[self.act] += girl.raise_preference(self.act, "fear", 0.75)
                        else:
                            brk[self.act] += girl.raise_preference(self.act, None, 0.75)

                # Magic failure

                else:
                    if girl.is_("very dom"):
                        l -= 1
                    elif girl.is_("dom"):
                        l -= 0.5
                    elif girl.is_("very sub"):
                        f += 1
                    elif girl.is_("sub"):
                        f += 0.5

            elif self.topic.type == "react" and self.type in ("praise", "gold", "gift", "pet", "day off", "sex"):

                ## 1. Personality unlocking

                # if self.type == "pet" or self.type == "day off":
                #     unlock = "DS"
                # elif self.type == "sex":
                #     unlock = "LM"
                # elif self.type == "praise" or self.type == "gold" or self.type == "gift":
                #     unlock = "MI"
                # else:
                #     raise AssertionError, "Type not found. Type is " + str(self.type)

                # girl.personality_unlock[unlock] += 15 + MC.get_charisma() + dice(10) # Temp, see how it behaves


                ## 2. Mood, love and fear changes: A score is calculated according to the impact and result of the interaction

                m += self.score
                l += self.score
                f -= self.score

                if self.score >= 1: # Fear diminishes faster for dom girls
                    if girl.is_("very dom"):
                        f -= 1
                    elif girl.is_("dom"):
                        f -= 0.5
                    elif girl.is_("very sub"):
                        f += 1
                    elif girl.is_("sub"):
                        f += 1

#                 if self.type == "praise": # More efficient for idealist girls
#                     if girl.is_("very idealist"):
#                         l += 1
#                     elif girl.is_("idealist"):
#                         l += 0.5
#                     elif girl.is_("very materialist"):
#                         l -= 1
#                     elif girl.is_("materialist"):
#                         l -= 0.5

#                 elif self.type == "gold": # More efficient for materialist girls
#                     if girl.is_("very materialist"):
#                         l += 1
#                     elif girl.is_("materialist"):
#                         l += 0.5
#                     elif girl.is_("very idealist"):
#                         l -= 1
#                     elif girl.is_("idealist"):
#                         l -= 0.5

                if self.type == "gift": # Good for all girls
                        l += 1

#                 elif self.type == "pet": # More efficient for sub girls
#                     if girl.is_("very sub"):
#                         l += 1
#                     elif girl.is_("sub"):
#                         l += 0.5
#                     elif girl.is_("very dom"):
#                         l -= 1
#                     elif girl.is_("dom"):
#                         l -= 0.5

#                 elif self.type == "day off": # More efficient for dom girls
#                     if girl.is_("very dom"):
#                         l += 1
#                     elif girl.is_("dom"):
#                         l += 0.5
#                     elif girl.is_("very sub"):
#                         l -= 1
#                     elif girl.is_("sub"):
#                         l -= 0.5

                else: # Sexual reward
#                     if self.response == "accepted":
#                         if girl.is_("very lewd"):
#                             l += 2
#                         elif girl.is_("lewd"):
#                             l += 1
#                         elif girl.is_("modest"):
#                             f -= 1

                    if self.response == "resisted":
                        ne += 1

#                         if girl.is_("very dom"):
#                             l -= 2
#                         elif girl.is_("dom"):
#                             l -= 1
#                         elif girl.is_("very sub"):
#                             l += 1
#                         elif girl.is_("sub"):
#                             l += 0.5

                        if girl.is_("very modest"):
                            l -= 1
                            f += 1
                        elif girl.is_("modest"):
                            l -= 0.5
                            f += 0.5

                    elif self.response == "refused": # (forced) --> Score is then set to zero
                        ev += 1

                        if girl.is_("very dom"):
                            l -= 2
                        elif girl.is_("dom"):
                            l -= 1
                        elif girl.is_("very sub"):
                            l += 0.5

                        if girl.is_("very modest"):
                            f += 3
                        elif girl.is_("modest"):
                            f += 2
                        else:
                            f += 1

                # Justify effect

                if self.reason: # Idealist girls like fairness
                    if girl.is_("very idealist"):
                        l += 1
                    elif girl.is_("idealist"):
                        l += 0.5
                    elif girl.is_("very materialist"):
                        l -= 0.5

                    ob += self.score

                else: # Materialist girls like to be rewarded for no reason
                    if girl.is_("very materialist"):
                        l += 1
                    elif girl.is_("materialist"):
                        l += 0.5
                    elif girl.is_("very idealist"):
                        l -= 0.5

                ## 3. Remember this

                girl.will_remember("reward", self.reason, self.score)

                ## 4. Spoil her

                if self.reason:
                    girl.spoil(self.score)
                else:
                    girl.spoil(3*self.score)


            elif self.topic.type == "react" and self.type in ("scold", "upkeep", "naked", "beat", "rape", "farm"):

                # This happens if a sub girl begs for mercy and MC complies
                if self.MC_reaction == "give up":
                    ev -= 1
                    f -= 1
                    ob -= dice(6)
                elif self.MC_reaction == "warning":
                    ne += 1
                    ob -= dice(3)
                else:
                    ## 1. Personality unlocking

                    if self.MC_reaction == "proceed": # Punishment is especially efficient is girl begged and was denied
                        self.score *= 1.5
                        ev += 1

                    # if self.type == "beat" or self.type == "farm":
                    #     unlock = "DS"
                    # elif self.type == "naked" or self.type == "rape":
                    #     unlock = "LM"
                    # elif self.type == "scold" or self.type == "upkeep":
                    #     unlock = "MI"
                    # else:
                    #     raise AssertionError, "Type not found. Type is " + str(self.type)

                    # girl.personality_unlock[unlock] += 15 + MC.get_charisma() + dice(10) # Temp, see how it behaves

                    ## 2. Mood, love and fear changes

                    m -= self.score
                    l -= self.score
                    f += self.score
                    ob += self.score

                    if self.score > 0: # Fear increases faster for sub girls
                        if girl.is_("very dom"):
                            f -= 1
                        elif girl.is_("dom"):
                            f -= 0.5
                        elif girl.is_("very sub"):
                            f += 1
                        elif girl.is_("sub"):
                            f += 1

#                     if self.type == "scold": # Idealist girls care more about it
#                         if girl.is_("very idealist"):
#                             f += 1
#                         elif girl.is_("idealist"):
#                             f += 0.5
#                         elif girl.is_("very materialist"):
#                             f -= 1
#                         elif girl.is_("materialist"):
#                             f -= 0.5

#                     elif self.type == "upkeep": # Hurts materialist girls more
#                         if girl.is_("very materialist"):
#                             f += 1
#                         elif girl.is_("materialist"):
#                             f += 0.5
#                         elif girl.is_("very idealist"):
#                             f -= 1
#                         elif girl.is_("idealist"):
#                             f -= 0.5

                    if self.type == "beat": # Scares sub girls more
                        gd -= 1

#                         if girl.is_("very sub"):
#                             f += 1
#                         elif girl.is_("sub"):
#                             f += 0.5
#                         elif girl.is_("very dom"):
#                             f -= 1
#                         elif girl.is_("dom"):
#                             f -= 0.5

#                     elif self.type == "naked": # Repressed girls care more
#                         if girl.is_("very modest"):
#                             f += 1
#                         elif girl.is_("modest"):
#                             f += 0.5
#                         elif girl.is_("very lewd"):
#                             f -= 1
#                         elif girl.is_("lewd"):
#                             f -= 0.5

                    elif self.type == "rape": # Sexual punishment (forced)

                        ev += 1

                        if girl.is_("very dom"):
                            l -= 2
                        elif girl.is_("dom"):
                            l -= 1
                        elif girl.is_("very sub"):
                            l += 0.5

#                         if girl.is_("very modest"):
#                             f += 3
#                         elif girl.is_("modest"):
#                             f += 2
#                         else:
#                             f += 1

#                         if self.result == "neg_fix":
#                             l -= 2
#                             f += 3
#                         elif self.result == "pos_fix":
#                             l += 1
#                             f -= 1

                    elif self.type == "farm": # More effective on dom girls, sub girls are somewhat less affected
                        gd -= 1

#                         if girl.is_("very dom"):
#                             f += 1
#                         elif girl.is_("dom"):
#                             f += 0.5
#                         elif girl.is_("very sub"):
#                             f -= 1
#                         elif girl.is_("sub"):
#                             f -= 0.5


                    ## 3. Justify effect

#                     if self.reason: # Idealist girls like fairness
#                         if girl.is_("very idealist"):
#                             f -= 1
#                             ob += 1
#                         elif girl.is_("idealist"):
#                             f -= 0.5
#                             ob += 0.5
#                         elif girl.is_("very materialist"):
#                             f += 0.5
#                             ob -= 0.5

#                     else: # Idealist girls hate to be punished for no reason
#                         if girl.is_("very idealist"):
#                             l -= 1
#                             ob -= 1
#                         elif girl.is_("idealist"):
#                             l -= 0.5
#                             ob -= 0.5
#                         elif girl.is_("very materialist"):
#                             l += 0.5
#                             ob += 0.5


                ## 4. Remembering and terrify effect (applies regardless of whether the punishment was given or not)

                # Remember this

                girl.will_remember("punish", self.reason, self.score)

                # Terrify her

                if self.reason:
                    girl.terrify(self.score)
                else:
                    girl.terrify(3*self.score)


            ## SEX STAT CHANGES

            # Random skill increases

            if self.act in extended_sex_acts:

                if self.mode == "lecture": # Results of lectures are handled here (not in sexual training)

                    # Mood and love change
                    if (girl.is_("very lewd") and compare_preference(girl, self.act, "a little reluctant")) or (girl.is_("lewd") and compare_preference(girl, self.act, "a little interested")):
                        l += 2
                        m += 2
                    elif (girl.is_("very lewd") and compare_preference(girl, self.act, "very reluctant")) or (girl.is_("lewd") and compare_preference(girl, self.act, "reluctant")):
                        m += 1
                    elif (girl.is_("very modest") and compare_preference(girl, self.act, "a little interested")) or (girl.is_("modest") and compare_preference(girl, self.act, "a little reluctant")):
                        m -= 1
                    elif (girl.is_("very modest") and compare_preference(girl, self.act, "reluctant")) or (girl.is_("modest") and compare_preference(girl, self.act, "very reluctant")):
                        l -= 2
                        m -= 2

                    if (girl.get_love() - girl.get_fear()) // 10 >= 0:
                        mod = "love"
                    else:
                        mod = "fear"

                    if self.score > 0:
                        brk[self.act] += girl.raise_preference(self.act, mod, 1.25)

                    elif self.score == 0:
                        brk[self.act] += girl.raise_preference(self.act, mod, 0.75)

                    else:
                        brk[self.act] += girl.raise_preference(self.act, mod, 0.25)

                elif self.topic.label == "slave_remove_fixation":
                    if not self.MC_reaction == "give up":
                        if self.result != "locked": # Modest break even if training fails
                            brk[self.act] + girl.raise_preference(self.act, self.MC_reaction, 0.5)
                        else: # Negative break if fix is locked
                            brk[self.act] + girl.raise_preference(self.act, self.MC_reaction, -1)

                        # Prestige

                        if self.act == "naked":
                            p += girl.rank / 2
                        else:
                            p += girl.rank


                else:

                    if not (self.MC_reaction in ("give up", "warning") or self.result in ("fail", "fled", "moderate")):
                        # All sex training costs energy

                        if self.act == "naked":
                            en = -5

                            lib += dice(5)

                            d = dice(6)

                            if d >= 6:
                                ob += dice(3)
                            elif d >= 5:
                                bea += dice(3)
                            elif d >= 4:
                                bod += dice(3)

                        elif self.act == "service":
                            en = -7

                            sv += dice(3)

                            d = dice(6)

                            if d >= 5:
                                sen += dice(3)
                            elif d >= 4:
                                cha += dice(3)

                        elif self.act == "sex":
                            en = -9

                            sx += dice(3)

                            d = dice(6)

                            if d >= 5:
                                lib += dice(3)
                            elif d >= 4:
                                bea += dice(3)

                        elif self.act == "anal":
                            en = -11

                            an += dice(3)

                            d = dice(6)

                            if d >= 5:
                                con += dice(3)
                            elif d >= 4:
                                bod += dice(3)

                        elif self.act == "fetish":
                            en = -13

                            fe += dice(3)

                            d = dice(6)

                            if d >= 5:
                                ob += dice(3)
                            elif d >= 4:
                                ref += dice(3)

                        elif self.act == "bisexual":
                            en = -9

                            if dice(6) >= 4:
                                sx += dice(3)
                            else:
                                sv += dice(3)

                            d = dice(6)

                            if d >= 5:
                                sen += dice(3)
                            elif d >= 4:
                                lib += dice(3)

                        elif self.act == "group":
                            en = -15

                            d = dice(6)

                            if d >= 5:
                                sv += dice(3)
                            elif d >= 3:
                                sx += dice(3)
                            else:
                                an += dice(3)

                            d = dice(6)

                            if d >= 5:
                                con += dice(3)
                            elif d >= 4:
                                ob += dice(3)

                        # Breaking (Warning: lecture breaking is handled above)

                        if self.topic.type == "magic": # Moderate magic results are handled above
                            if girl.magic_training == "positive":
                                brk[self.act] += girl.raise_preference(self.act, "love", 2)
                                if MC.get_effect("special", "hypnosis spillover"):
                                    spillover[self.act] = "love"
                            elif girl.magic_training == "negative":
                                brk[self.act] += girl.raise_preference(self.act, "fear", 2)
                                if MC.get_effect("special", "hypnosis spillover"):
                                    spillover[self.act] = "fear"
                            else:
                                brk[self.act] += girl.raise_preference(self.act, None, 2)
                                if MC.get_effect("special", "hypnosis spillover"):
                                    spillover[self.act] = None

                        elif self.response == "accepted":
                            brk[self.act] += girl.raise_preference(self.act, "love", 2)

                        elif self.response == "resisted":
                            if girl.is_("very sub"):
                                brk[self.act] += girl.raise_preference(self.act, "fear", 1.5)
                            elif girl.is_("sub"):
                                brk[self.act] += girl.raise_preference(self.act, "fear", 1)
                            elif girl.is_("very dom"):
                                brk[self.act] += girl.raise_preference(self.act, "fear", 0)
                            elif girl.is_("dom"):
                                brk[self.act] += girl.raise_preference(self.act, "fear", 0.5)

                        elif self.response == "refused":
                            if girl.is_("very sub"):
                                brk[self.act] += girl.raise_preference(self.act, "fear", 2.5)
                            elif girl.is_("sub"):
                                brk[self.act] += girl.raise_preference(self.act, "fear", 2)
                            elif girl.is_("very dom"):
                                brk[self.act] += girl.raise_preference(self.act, "fear", -2)
                            elif girl.is_("dom"):
                                brk[self.act] += girl.raise_preference(self.act, "fear", -1)

                        else:
                            brk[self.act] += girl.raise_preference(self.act, None, 2)

                        # Prestige

                        if self.act != "naked":
                            brk["naked"] += girl.raise_preference("naked", None, 1) # Naked acts rise with other sex acts
                            p += girl.rank
                            girl.add_log("perform " + self.act)

                        if self.act in ("sex", "group"):
                            if girl.pop_virginity(origin="MC"):
                                virgin = True
                                p += 3 * girl.rank


            ## Apply changes

            changes = [("mood", m), ("love", l), ("fear", f), ("beauty", bea), ("body", bod), ("charm", cha), ("refinement", ref), ("obedience", ob), ("sensitivity", sen), ("constitution", con), ("libido", lib), ("service", sv), ("sex", sx), ("anal", an), ("fetish", fe), ("energy", en)]

#            renpy.say("", "love value:" + str(l))

            text1 = "{size=-2}"

            for s, v in changes: # Charisma impacts all changes

                if s == "energy":
                    c = girl.change_stat(s, v)
                    shown = str(round_int(c))
                else:
                    c = girl.change_stat(s, v * (1 + (MC.get_charisma()/10)))
                    shown = get_plus_rating(c)

                if debug_mode: # Always show precise numbers in debug mode
                    shown = str(round_int(c))

                if v != 0 and c != 0:
                    text1 += __("\n%s: %s") % (__(s.capitalize()), shown)

            text1 += "\n"

            for a in brk.keys():
                if brk[a] != None:
                    if debug_mode:
                        shown = str(round_int(brk[a]))
                    else:
                        shown = get_plus_rating(brk[a], "pref")

                    text1 += __("\n%s preference: %s") % (__(a.capitalize()), shown)
                else:
                    raise AssertionError("Unexpected breaking value for " + a + ". Please report this bug.")

            if inter:
                text1 += __("\nGirl interactions: %s") % str(inter)
                girl.interactions += inter

            if virgin:
                text1 += __("\n%s has lost her virginity with you.") % girl.fullname

            text1 += "\n"

            if gd:
                MC.good += gd
            if ne:
                MC.neutral += ne
            if ev:
                MC.evil += ev

            if debug_mode:
                if gd:
                    text1 += __("\nGood: %s") % str(gd)
                if ne:
                    text1 += __("\nNeutral: %s") % str(ne)
                if ev:
                    text1 += __("\nEvil: %s") % str(ev)
            if p:
                MC.change_prestige(p)
                text1 += __("\nPrestige: %s") % str(p)

            if not text2:
                text1 = __("No changes")

            if spillover: # Mass Hysteria spell
                for k in spillover.keys():
                    if k in ("obedience", "libido", "sensitivity"):
                        for g in MC.girls:
                            if g != girl and dice(6) >= 6:
                                g.change_stat(k, spillover[k], spillover=False, notify_suffix=__(" (Mass hysteria)"))
                    
                    elif k in extended_sex_acts:
                        for g in MC.girls:
                            if g != girl and dice(6) >= 6:
                                _, r = g.raise_preference(k, spillover[k], 1, use_effects=False, status_change=True)
                                notify(__(act.capitalize()) + __(" preference + (Mass hysteria)"), pic=g.portrait)

            norollback()

            renpy.call_screen("OK_screen", __("[girl.fullname] - Interaction results"), text1, dark=True, pic=girl.portrait, always_scrollbar=True)

            return



    class GirlRecentEvent(object):

        def __init__(self, type, action=None, base_description="", encourage=True, discipline=True):

            self.type = type
            self.action = action
            self.base_description = base_description
            self.description = ""
            self.encourage = encourage
            self.discipline = discipline

            self.time = 0
            self.rewarded = 0
            self.punished = 0

        def reward(self, score):

            self.rewarded += score

            if self.rewarded > 10:
                self.rewarded = 10

        def punish(self, score):

            self.punished += score

            if self.punished > 10:
                self.punished = 10

        def refresh(self):
            if self.rewarded > 0:
                self.rewarded -= 1
            if self.punished > 0:
                self.punished -= 1


