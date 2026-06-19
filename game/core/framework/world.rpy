#### World classes ####

init -2 python:
    class District(): # Attributes: name, populations, brothels, competitors, vice, tooltip

        """This class covers the districts of the city, where each chapter of the game is played."""

        def __init__(self, name, chapter, rank, diff, pop, room = None, pic = None, locations = None, description = ""):

            self.name = name
            self.chapter = chapter
            self.rank = rank
            self.diff = diff
            self.pic = pic
            self.description = description
            self.quests_updated = -99
            if room:
                self.room = room
            else:
                self.room = []
            if locations is not None:
                self.locations = locations
            elif self.name in location_dict:
                self.locations = location_dict[self.name]
            else:
                self.locations = []

            self.items = defaultdict(list)

            self.no_reminder = -1 # storing the latest skipped day for the 'relocate/visit city' reminder

        def get_rand_pop(self):
            return weighted_choice([(p, p.weight) for p in all_populations])

        def get_pic(self, x, y):
            return im.Scale(self.pic, x, y)

        ## BK Evolution: Data serialization
        @classmethod
        def from_dict(cls, d, world_map=None):
            """EN: Deserialize District from dict. world_map is used to resolve population/location references.
               ZH: 从字典反序列化 District，world_map 用于解析人口/地点引用。"""
            # Resolve location references
            _loc_ids = d.get("location_ids", [])
            if world_map and _loc_ids:
                _locations = [world_map.locations[lid] for lid in _loc_ids if lid in world_map.locations]
            else:
                _locations = None

            # Resolve population references
            _pop_refs = d.get("pop", [])
            _pop = []
            for pref in _pop_refs:
                if isinstance(pref, (list, tuple)) and len(pref) == 2:
                    _pop.append(tuple(pref))
                elif isinstance(pref, dict):
                    _pid = pref.get("population_id")
                    _w = pref.get("weight", 0)
                    if world_map and _pid in world_map.populations:
                        _pop.append((world_map.populations[_pid], _w))
                    else:
                        _pop.append((_pid, _w))  # Delayed resolution fallback
                else:
                    _pop.append(pref)

            _room = d.get("room")
            if _room == "free":
                _room = "free"
            elif isinstance(_room, list):
                _room = list(_room)
            else:
                _room = None

            return cls(
                name=d.get("name", ""),
                chapter=d.get("chapter", 1),
                rank=d.get("rank", 1),
                diff=d.get("diff", 0),
                pop=_pop,
                room=_room,
                pic=d.get("pic"),
                locations=_locations,
                description=__(d.get("description_i18n", "")) if d.get("description_i18n") else "",
            )

        def to_dict(self):
            """EN: Serialize District to dict (for editor/scenario export).
               ZH: 将 District 序列化为字典（供编辑器/剧本导出）。"""
            return {
                "name": self.name,
                "chapter": self.chapter,
                "rank": self.rank,
                "diff": self.diff,
                "pop": [(pop.name if hasattr(pop, "name") else pop[0], pop[1] if hasattr(pop, "__getitem__") else pop.weight) for pop in self.pop],
                "room": self.room,
                "pic": self.pic,
                "description_i18n": self.description,
            }


    class Population(PicHolder):

        def __init__(self, name, pic, diff, range, rank=1, effects=None, weight=0, base_description = ""):

            self.name = name
            self.pic = Picture(pic, "resources/ui/customers/" + pic)
            self.diff = diff
            self.range = range
            self.rank = rank
            if effects == None: effects = []
            self.effects = effects
            self.effect_dict = defaultdict(list)
            for effect in self.effects:
                self.effect_dict[effect.type, effect.target].append(effect)
            self.weight = weight
            self.description = __("{b}%s{/b} (difficulty: %s): %s") % (self.name.capitalize(), self.get_difficulty(), get_description(base_description, effects))

        def is_allowed(self):
            return brothel.get_effect("allow", self.name) and self.weight > 0

        def get_rand_name(self, gender="M"):
            return rand_choice(pop_name_dict[gender + " " + self.name])

        def get_average_budgets(self, description=False):
            base = (self.diff + self.range//2) * game.get_diff_setting("budget")
            ent_budget = int(base * self.get_effect("boost", "job customer budget") + self.get_effect("change", "job customer budget"))
            wh_budget = int(base * 3 * self.get_effect("boost", "whore customer budget") + self.get_effect("change", "whore customer budget"))
            total_budget = ent_budget + wh_budget

            if description:
                if ent_budget != base:
                    ent_budget = event_color["good"] % str(ent_budget)

                if wh_budget != base*3:
                    wh_budget = event_color["good"] % str(wh_budget)

            return total_budget, ent_budget, wh_budget

        def get_effect(self, type, target, randomize=False): # Turn randomize off for UI display

#             if type == "boost":
#                 r = 1 * brothel.get_effect(type, target)
#             else:
#                 r = 0 + brothel.get_effect(type, target)

#             for eff in self.effects:
#                 if eff.target.lower() == target.lower():
#                     if renpy.random.random() <= eff.chance:
#                         r += eff.value
            if type == "boost":
                return get_effect(self, type, target, randomize=randomize) * brothel.get_effect(type, target, randomize=randomize)
            else:
                return get_effect(self, type, target, randomize=randomize) + brothel.get_effect(type, target, randomize=randomize)

        def get_difficulty(self):

            if self.diff <= 25:
                return event_color["good"] % str(self.diff)
            elif self.diff <= 50:
                return event_color["a little good"] % str(self.diff)
            elif self.diff <= 90:
                return event_color["average"] % str(self.diff)
            elif self.diff <= 120:
                return event_color["a little bad"] % str(self.diff)
            elif self.diff <= 170:
                return event_color["bad"] % str(self.diff)
            else:
                return event_color["fear"] % str(self.diff)

        ## BK Evolution: Data serialization
        @classmethod
        def from_dict(cls, d):
            """EN: Deserialize Population from dict.
               ZH: 从字典反序列化 Population。"""
            _effects = d.get("effects", [])
            _effect_objs = [Effect.from_dict(e) for e in _effects] if _effects else []
            _base_desc = d.get("base_description_i18n", "")
            if _base_desc:
                _base_desc = __(_base_desc)
            return cls(
                name=d.get("name", ""),
                pic=d.get("pic", ""),
                diff=d.get("diff", 0),
                range=d.get("range", 0),
                rank=d.get("rank", 1),
                effects=_effect_objs,
                weight=d.get("weight", 0),
                base_description=_base_desc,
            )

        def to_dict(self):
            """EN: Serialize Population to dict.
               ZH: 将 Population 序列化为字典。"""
            return {
                "name": self.name,
                "pic": self.pic.filename if hasattr(self.pic, "filename") else "",
                "diff": self.diff,
                "range": self.range,
                "rank": self.rank,
                "effects": [e.to_dict() for e in self.effects],
                "weight": self.weight,
                "description": self.description,
            }


    class Customer():

        """This class is for individual customers interacting with the girls."""

        def __init__(self, pop):

            if pop:
                self.pop = pop
            else:
                self.pop = beggar

            self.rank = self.pop.rank

            self.adjective = ""

            self.randomize()

            self.name = article(__("%s%s") % (self.adjective, self.pop.get_rand_name())).capitalize()

            self.reason = ""
            self.satisfaction = self.get_effect("change", "overall customer satisfaction")

            ## EN: BK Evolution — customer affix system (personality + wealth tier + mood).
            ## ZH: BK Evolution — 顾客词缀系统（性格+财富等级+心情）。
            self.affixes = None
            self.service_dict = {"entertained" : 0, "laid" : 0, "both" : 0, "favorite entertainment" : 0, "favorite sex act" : 0, "extra" : 0} # Extra is earned with the right trait or bis/group sex
            self.got_entertainment = None
            self.got_sex_act = None
            self.group = False

            self.gender = "M"

            self.reputation_change = 0

#             self.got_service = False
#             self.entertained = False
#             self.got_laid = False
#             self.satisfied = False

            #<Chris Job Mod>
            if game.has_active_mod("chrisjobmod"):
                self.entertainment_score = unentertained_customer_score
            #</Chris Job Mod>

        def set_gender(self, gender):
            self.gender = gender
            self.name = article(__("%s%s") % (self.adjective, self.pop.get_rand_name(self.gender))).capitalize()

        def get_pic(self, x, y):
            return self.pop.get_pic(x, y)

        def receive_entertainment(self, entertainment):

            self.got_entertainment = entertainment
            self.service_dict["entertained"] = 1

            if entertainment == self.wants_entertainment:
                self.service_dict["favorite entertainment"] = 1

        def receive_sex_act(self, act):

            self.got_sex_act = act
            self.service_dict["laid"] = 1

            if act == self.wants_sex_act:
                self.service_dict["favorite sex act"] = 1

            if self.service_dict["entertained"] > 0:
                self.service_dict["both"] = 1

        def get_entertainment_bonus(self):
            r = self.get_effect("change", "job satisfaction") + self.get_effect("change", "satisfaction")

            ## EN: BK Evolution — apply preference matrix modifier for the received entertainment act.
            ## ZH: BK Evolution — 应用偏好矩阵修正到收到的娱乐行为。
            if self.affixes and self.got_entertainment:
                r += self.affixes.preferences.get_score_modifier(self.got_entertainment)

            if self.wants_entertainment != self.got_entertainment:
                return r - self.rank, False # Didn't get the entertainment they wanted
            else:
                return r, True # Got the entertainment they wanted

        def get_sex_act_bonus(self, bis=False, group=False):
            r = self.get_effect("change", "whore satisfaction") + self.get_effect("change", "satisfaction")

            # Customers that haven't been entertained first get an additional penalty
            if not self.got_entertainment:
                r -= self.rank - 1

            ## EN: BK Evolution — apply preference matrix modifier for the received sex act.
            ## ZH: BK Evolution — 应用偏好矩阵修正到收到的性行为。
            if self.affixes and self.got_sex_act:
                r += self.affixes.preferences.get_score_modifier(self.got_sex_act)

            # Customers will not complain about the sex act during group or bisexual
            if bis or group:
                self.service_dict["extra"] = 1
            elif self.wants_sex_act != self.got_sex_act:
                r -= self.rank - 1

            # JMan's suggestion to make Group a lower class thing

            ################ NEW CODE #########################################################
            if group and game.has_active_mod("chrisjobmod"):
                if group_rank_penalty_applies:
                    r -= self.rank//2 + 1
            ################ END OF NEW CODE ##################################################

            return r

        def get_reputation_change(self): # Returns change to brothel reputation at the end of the day

            # Rating will bring a positive change to rep if >= rank, will bring negative change if < rank-1
            self.base_rating = sum(v for v in self.service_dict.values())

            ## EN: BK Evolution — apply preference matrix and mood modifiers to reputation rating.
            ## ZH: BK Evolution — 应用偏好矩阵和心情修正到声望评分。
            if self.affixes:
                if self.got_entertainment:
                    self.base_rating += self.affixes.preferences.get_score_modifier(self.got_entertainment)
                if self.got_sex_act:
                    self.base_rating += self.affixes.preferences.get_score_modifier(self.got_sex_act)
                if self.affixes.mood:
                    self.base_rating += self.affixes.mood.satisfaction_mod
                if self.affixes.personality:
                    self.base_rating += self.affixes.personality.satisfaction_mod

            rating = self.base_rating + 1 - self.rank

            chg = min(2 ** self.rank, 2 ** rating - 1)

            if chg < 0:
                chg = 1 - 2 ** (-rating)

            self.reputation_change = chg
            self.reputation_comment = self.get_reputation_comment(chg)

            return chg

        def get_reputation_comment(self, chg):

            # Get random comment

            if self.base_rating == 0:
                comment = rand_choice([__("I came here for nothing."), __("I didn't get attended at all."), __("What a disgrace. I wasted my time here."), __("No one attended me. Such a waste of time...")])

                if chg < 0:
                    comment = event_color["bad"] % comment

            elif self.base_rating == 8:
                comment = event_color["special contrast"] % rand_choice([__("I had the time of my life."), __("Everything was perfect."), __("Best night ever! I'm spent."), __("This place is amazing. Five stars!")])

            else:
                pos_comments = []
                neg_comments = []

                if self.service_dict["entertained"] >= 2:
                    pos_comments.append(__("I saw a really great performance."))
                elif self.service_dict["entertained"] == 1:
                    pos_comments += [__("I got some entertainment."), __("I was entertained while waiting."), __("A girl performed for me.")]
                    neg_comments.append(__("The entertainer could have been better."))
                else:
                    neg_comments += [__("There was no entertainment."), __("I was bored while waiting."), __("No entertainment. Boooring...")]

                if self.service_dict["laid"] >= 2:
                    pos_comments.append(__("The sex was really awesome."))
                elif self.service_dict["laid"] == 1:
                    pos_comments += [__("I got laid."), __("A whore took care of me."), __("I had %s.") % __(self.got_sex_act)]
                    neg_comments.append(__("The sex could have been better."))
                else:
                    neg_comments += [__("No whores! What kind of brothel is this?"), __("I couldn't find a whore. So frustrating."), __("Couldn't get laid, damn it!"), __("Where are the whores? Hello?")]

                if self.service_dict["both"] > 1:
                    pos_comments.append(__("I got both sex and entertainment."))

                if self.service_dict["favorite entertainment"] >= 1:
                    pos_comments.append(__("I got my favorite entertainment while waiting."))
                else:
                    neg_comments.append(__("My favorite entertainment was unavailable."))

                if self.service_dict["favorite sex act"] > 1:
                    pos_comments.append(__("I got my favorite sex act."))
                else:
                    neg_comments.append(__("My favorite sex act was unavailable."))

                if self.service_dict["extra"] > 1:
                    pos_comments.append(__("Sex is better with more people!"))

                if chg > 0:
                    comment = event_color["good"] % __(rand_choice(pos_comments))
                elif chg < 0:
                    comment = event_color["bad"] % __(rand_choice(neg_comments))
                else:
                    comment = rand_choice(pos_comments+neg_comments)

            return comment


        def randomize(self):

            self.preference = weighted_choice([("beauty", 25 + self.get_effect("change", "beauty preference")), ("body", 25 + self.get_effect("change", "body preference")), ("charm", 25 + self.get_effect("change", "charm preference")), ("refinement", 25 + self.get_effect("change", "refinement preference"))])
            self.wants_entertainment = weighted_choice([(j, customer_base_preference[j]*(1 + 0.5*game.customer_preference_weight[j]) + self.get_effect("change", j + " preference")) for j in all_jobs])
            self.wants_sex_act = weighted_choice([(a, customer_base_preference[a]*(1 + 0.5*game.customer_preference_weight[a]) + self.get_effect("change", a + " preference")) for a in all_sex_acts])
            self.fetish = rand_choice(trait_dict)

            self.diff = self.pop.diff + dice(self.pop.range + 1) - 1 ## Varies up to +10 to +40 (maximum rank)
            self.defense = 2 * (self.rank-2) + dice(self.rank+2) # from -1 to 13 defense depending on rank

            ## EN: Generate BK Evolution affixes and apply modifiers.
            ## ZH: 生成 BK Evolution 词缀并应用修正。
            try:
                self.affixes = generate_customer_affixes(pop_rank=self.pop.rank)
                self.affixes.apply_to_customer(self)
            except:
                self.affixes = None

            self.set_budgets()

            if dice(100) <= 2 * self.get_effect("boost", "crazy") + self.get_effect("change", "crazy"):
                self.crazy = rand_choice(["arsonist", "rapist", "violent"])
            else:
                self.crazy = False

        def get_defense(self, fight = False):
            return self.defense * self.get_effect("boost", "customer defense") + self.get_effect("change", "customer defense")

        def get_effect(self, type, target, randomize=True): # Keep randomize True so that random customer effects will proc
            return self.pop.get_effect(type, target, randomize)

        def get_description(self, act="idle"):

            pronoun = {"M": "He", "F": "She"}[self.gender]

            desc = ""

            if self.crazy:
                crz_text = __(" {color=%s}%s is crazy!{/color}") % (c_red, pronoun)
            else:
                crz_text = ""

            if act == "idle job" or act in all_jobs:
                return __("%s came in.%s %s wanted to be entertained by a {b}%s{/b}. %s prefers %s girls.") % (self.name, crz_text, pronoun, self.wants_entertainment, pronoun, self.fetish.lower())

            elif act == "idle whore":
                return __("%s %s likes {b}%s{/b}. %s prefers %s girls.") % (self.name, crz_text, pronoun, self.wants_sex_act, pronoun, self.fetish.lower())

            # elif act in all_jobs:
            #     desc += self.name + __(" came in.%s\n%s wanted to be entertained by a {b}%s{/b}") % (crz_text, __(pronoun), __(self.wants_entertainment))
            #     if self.wants_entertainment != act:
            #         desc += __(", but settled for a {b}%s{/b}") % __(act)
            #     return desc

            elif act in all_sex_acts:
                desc += __("%s %s likes {b}%s{/b}. %s prefers %s girls.") % (self.name, crz_text, pronoun, self.wants_sex_act, pronoun, self.fetish.lower())
                if self.wants_sex_act != act:
                    desc += __(", but settled for {b}%s{/b}") % __(act)
                if self.group:
                    desc += __(". %s joined a {color=#9933FF}{b}group of %s{/b}{/color}") % (pronoun, self.group)
                return desc + "." + crz_text

            elif act == "end":
                desc += self.name + " wanted to be entertained by a {b}%s{/b}, " % self.wants_entertainment
                if self.got_entertainment:
                    desc += "and got {b}%s{/b}. " % self.got_entertainment
                else:
                    desc += "but was left unattended. "

                desc += "%s wanted {b}%s{/b}, " % (pronoun, self.wants_sex_act)
                if self.got_sex_act:
                    desc += "and got {b}%s{/b}. " % self.got_sex_act
                else:
                    desc += "but no whore was available. "

                return desc

        def set_budgets(self):
            d = dice(12)
            mod = 1.0

            if d == 12:
                self.adjective = __("rich ")
                mod = 2.0
            elif d == 1:
                self.adjective = __("poor ")
                mod = 0.5

            ## EN: Apply BK Evolution affix budget multiplier if available.
            ## ZH: 如可用，应用 BK Evolution 词缀预算倍率。
            if self.affixes:
                mod *= self.affixes.get_budget_multiplier()

            self.ent_budget = int((self.diff * mod  + self.get_effect("change", "job customer budget")) * self.get_effect("boost", "job customer budget") * brothel.get_adv_budget())
            self.wh_budget = int((self.diff * 3 * mod + self.get_effect("change", "whore customer budget")) * self.get_effect("boost", "whore customer budget") * brothel.get_adv_budget())

        def choose_girl(self, girls): # For xxx interactions: returns a girl and a reason for choosing her.

            chosen = None
            best_score = 0
            sex_act = self.wants_sex_act

            # Sanity check

            if not girls:
                raise AssertionError("Customer could not find girls to choose from. (%s)" % and_text([g.name for g in girls]))

#             girls = [g for g in girls if g.does_anything()]

#             if not girls:
#                 raise AssertionError, "Customer could not find girls with an active sex act to choose from. (%s)" % and_text([g.name for g in girls])

            # Looks for the best girl

            for girl in girls:

                girl_score = 0
                reason = ""

                # 1. The customer looks for a particular trait (his fetish)

                if girl.has_trait(self.fetish):
                    girl_score += 250

                    if trait_dict[self.fetish].verb == "be":
                        reason = __(":cust: came looking for a %s girl. :Pron: :verb: elated to meet :girl:.") % self.fetish
                    elif trait_dict[self.fetish].verb == "be a":
                        reason = __(":cust: came looking for a %s. :Pron: :verb: elated to meet :girl:.") % self.fetish
                    elif trait_dict[self.fetish].verb == "have":
                        reason = __(":cust: came looking for a girl with %s. :Pron: :verb: elated to meet :girl:.") % self.fetish
                    elif trait_dict[self.fetish].verb == "have a":
                        reason = __(":cust: came looking for a girl with a %s. :Pron: :verb: elated to meet :girl:.") % self.fetish

                # 2. The customer looks for a particular stat

                girl_score += girl.get_stat(self.preference) # Customers are looking for one stat in particular

                if not reason:
                    reason = __(":cust: wanted to meet %s. ") % gstats_descript[self.preference]

                    if girl_score >= 50*self.rank:
                        reason += __(":Pron: :verb: elated to meet :girl:.")
                    elif girl_score >= 35*self.rank:
                        reason += __(":Pron: :verb: pleased to meet :girl:.")
                    elif girl_score >= 20*self.rank:
                        reason += __(":Pron: settled for :girl:.") # Special case handled with a try / except clause within the perform method
                    else:
                        reason += __(":Pron: :verb: disappointed to meet :girl:.")

                # 3. The customer looks for the best performer

                if girl.does[self.wants_sex_act]:
                    girl_score += girl.get_stat(self.wants_sex_act)

                if girl.rank < self.rank: # Customers will favor girls with their rank or higher
                    girl_score -= 100 * (self.rank - girl.rank)
                elif self.rank < girl.rank:
                    girl_score -= 50 * (girl.rank - self.rank)

                # 4. Check score

                if girl_score > best_score:
                    chosen = girl
                    best_score = girl_score
                    self.reason = reason

                    if girl.does[self.wants_sex_act]:
                        sex_act = self.wants_sex_act
                    else:
                        sex_act = rand_choice([act for act in all_sex_acts if girl.does[act] == True])

            # Choose a random girl if no-one matches their tastes

            if not chosen:
                chosen = rand_choice(girls)
                if chosen.does[self.wants_sex_act]:
                    sex_act = self.wants_sex_act
                else:
                    sex_act = rand_choice([act for act in all_sex_acts if chosen.does[act] == True])
            if not self.reason:
                self.reason = __(":cust: wanted to meet %s. :pron: couldn't find a suitable girl.") % gstats_descript[self.preference]

            return chosen, sex_act






    ## The code for brothels and room is messy / redundant and should be cleaned up some time

    class Brothel(EffectBearer): #Attributes: name, rooms, reputation, advertisement, tooltip

        """This class is for available brothels that you can operate."""

        def __init__(self, rank, level, upgrades, max_rep):

            self.name = __("The Rose Garden")
            self.rank = rank
            self.level = level
            self.cost = bro_cost[self.level]
            self.total_value = self.cost
            self.bedroom_type = room_dict[upgrades[0]]
            self.maxupgrade = upgrades[1]
            self.max_rep = max_rep
            self.furniture = []
            self.rooms = {k: copy.copy(v) for k, v in common_room_dict.items()}
            self.effect_dict = defaultdict(list)
            self.reset_threat()

        # Set up Brothel

        def get_pic(self, x=0, y=0):
            return ProportionalScale("resources/brothels/" + brothel_pics[self.pic_index], x, y)

        def get_bg(self):
            return "bg brothel%s" % self.pic_index

        ## BK Evolution: Data serialization
        @classmethod
        def from_dict(cls, d):
            """EN: Deserialize Brothel from dict. Note: setup() must be called separately after deserialization.
               ZH: 从字典反序列化 Brothel。注意：setup() 需在反序列化后单独调用。"""
            return cls(
                rank=d.get("rank", 1),
                level=d.get("level", 1),
                upgrades=list(d.get("upgrades", [1, 1])),
                max_rep=d.get("max_rep", 100),
            )

        def to_dict(self):
            """EN: Serialize Brothel to dict (minimal - does not include runtime state).
               ZH: 将 Brothel 序列化为字典（最小化，不包含运行时状态）。"""
            return {
                "rank": self.rank,
                "level": self.level,
                "upgrades": [self.bedroom_type.name if hasattr(self.bedroom_type, "name") else self.bedroom_type, self.maxupgrade],
                "max_rep": self.max_rep,
            }

        def setup(self, name, furniture=None, current_building=None, started_building=0, master_bedroom_girls=None, free_room=None):

            self.pic_index = self.level
            self.pic = self.get_pic(config.screen_width, int(config.screen_height*0.8))
            # Unlocks pics for gallery
            unlock_pic("resources/brothels/" + brothel_pics[self.pic_index])
            unlock_pic(self.bedroom_type.pic_path)

            self.rep = 0
            self.advertising = 0
            self.advertising_setting = 0 # advertising_setting is a value from -2 to +2. -2 is max customer attraction, 0 is balanced, +2 is max customer budget

            self.maintenance = 0
#             self.maint_value = 1 # maint_value is antiquated
            self.dirt = 0

            self.security = 0
            self.threat = 0 # Threat builds up over time and causes security events to proc
            self.alert_level = 1 # Alert level determines the type of security events that can proc

            self.free_room = False
            if free_room:
                if free_room == "free":
                    self.free_room = True
                else:
                    for room in free_room:
                        self.rooms[room].buy(forced=True)

            self.bedrooms = bro_capacity[self.level][0]
            self.max_help = bro_helpers[self.level]

            self.magic_shield = False

            self.name = name
            if furniture == None: furniture = []
            self.furniture = furniture
            self.current_building = current_building
            self.started_building = started_building

            self.master_bedroom = master_bedrooms[self.rank-1]
            if master_bedroom_girls == None:
                master_bedroom_girls = []
            elif len(master_bedroom_girls) > self.master_bedroom.level:
                master_bedroom_girls = master_bedroom_girls[:self.master_bedroom.level]
            self.master_bedroom.girls = master_bedroom_girls

            self.contract_modifier = -20

            self.customer_count = 0


        def get_maxbedrooms(self): # Replaces the old 'maxbedrooms' property
            return bro_capacity[game.chapter][1]

        def can_upgrade(self):
            if brothel.bedrooms < brothel.get_maxbedrooms():
                return True
            if self.bedroom_type.level < self.maxupgrade:
                return True
            if self.master_bedroom.level < self.rank:
                return True
            for room in self.rooms.values():
                if room.level < district.rank:
                    return True
            return False


        # Master bedroom

        def upgrade_master_bedroom(self, target_level="auto"):
            if target_level == "auto":
                target_level = self.master_bedroom.level + 1

            if MC.has_gold(master_bedrooms[target_level].cost):
                if renpy.call_screen("yes_no", __("Are you sure you want to upgrade your room for ") + str(master_bedrooms[target_level].cost) + " gold?"):
                    renpy.play(s_gold, "sound")
                    MC.gold -= master_bedrooms[target_level].cost
                    self.total_value += master_bedrooms[target_level].cost
                    temp_girls = self.master_bedroom.girls
                    self.master_bedroom.girls = []

                    self.master_bedroom = master_bedrooms[target_level]

                    self.master_bedroom.girls = temp_girls

#                     test_achievement("upgrades")

            else:
                renpy.say(sill, __("Sorry Master, you do not have enough money."))


        def can_have(self, job):
            if job == "farm":
                return False
            elif job not in all_jobs:
                return True
            elif self.rooms[job_room_dict[job.lower()]].level > 0:
                return True
            else:
                return False

        # Furniture

        def can_build_anything(self, max_chapter=MAX_CHAPTER):
            if [f for f in all_furniture if f.can_build() and f.chapter <= max_chapter]:
                return True
            return False

        def buy_furniture(self, furn):

            if self.current_building:
                renpy.say(carpenter, __("Sorry boss, I still have work to do on that %s you ordered.") % self.current_building.name)
                return False

            elif not furn.can_build():
                if furn.built:
                    renpy.say(carpenter, __("You've got it already. I don't think you need a second one."))
                renpy.say(carpenter, __("Cannot build that for now, I'm 'fraid. You'd need a larger place."))
                return False

            for resource, amount in furn.cost:
                if not MC.has_resource(resource, amount):
                    renpy.say(carpenter, __("Look, boss, you gotta have the right amount of resources before I can start the job."))
                    break
            else:
                renpy.say(carpenter, __("A'right, looks like you've got the goods. Hand them over, and I'll get started on that %s right away.") % furn.name)
                if renpy.call_screen("yes_no", __("Are you sure you want to build a %s for %s?") % (furn.name, furn.describe_cost())):
                    MC.spend_resources(furn.cost)
                    norollback()
                    furn.start_building()
                    return True
            return False

        def activate_furniture(self, furn):
            return furn.activate()

        def deactivate_furniture(self, furn):
            return furn.deactivate()

        def toggle_furniture(self, furn):
            return furn.toggle()

        def destroy_furniture(self, furn):
            furn.destroy()

        def force_build(self, furn_name):
            furn = [f for f in all_furniture if f.name.lower().startswith(furn_name.lower())][0]
            if furn:
                furn.build()
                return True
            return False


        # Effects

        # def update_effects(self):
        #
        #     update_effects()


        ## Important: Security, advertising and maintenance change effects are applied BEFORE boost effects

        def get_security(self):

            return ((self.security + self.get_effect("change", "security")) * self.get_effect("boost", "security"))


        # Advertising

        def update_customer_count(self): # customer count is not refreshed constantly to avoid UI lag
            self.avoid_no_population()
            self.customer_count, self.customer_count_dict = count_customers(self.rep, randomize=False)
            self.calculate_average_customer_budget()

        def avoid_no_population(self): # sanity check
            for pop in all_populations:
                if pop.weight > 0:
                    return
            all_populations[0].weight = 1

        def calculate_average_customer_budget(self):

            # Calculate average budget for active populations

            self.customer_budget_dict = defaultdict(int)
            total_ent = 0
            total_wh = 0
            weight = 0

            for pop in all_populations:
                total_budget, ent_budget, wh_budget = pop.get_average_budgets()
                total_ent += self.customer_count_dict[pop.name] * ent_budget
                total_wh += self.customer_count_dict[pop.name] * wh_budget
                weight += self.customer_count_dict[pop.name]

            if weight > 0:
                self.customer_budget_dict["ent budget"] = round_int(total_ent / weight)
                self.customer_budget_dict["wh budget"] = round_int(total_wh / weight)

            # Calculates advertising bonus

            self.customer_budget_dict["ent advertising"] = self.customer_budget_dict["ent budget"] * (brothel.get_adv_budget() - 1)
            self.customer_budget_dict["wh advertising"] = self.customer_budget_dict["wh budget"] * (brothel.get_adv_budget() - 1)

            self.customer_budget_dict["ent budget"] += self.customer_budget_dict["ent advertising"]
            self.customer_budget_dict["wh budget"] += self.customer_budget_dict["wh advertising"]

            # Calculates act bonus (for whoring-only unless BKsettings.rpy has been edited)

            act_boost = 0
            weight = 0

            for job in all_jobs:
                act_boost += tip_advertising_modifier[job] * (1 + 0.5*game.customer_preference_weight[job])
                weight += 1 + 0.5*game.customer_preference_weight[job]

            if weight > 0:
                self.customer_budget_dict["ent acts"] = round_int(self.customer_budget_dict["ent budget"] * (act_boost/weight - 1))

            act_boost = 0
            weight = 0

            for act in all_sex_acts:
                act_boost += tip_advertising_modifier[act] * (1 + 0.5*game.customer_preference_weight[act])
                weight += 1 + 0.5*game.customer_preference_weight[act]

            if weight > 0:
                self.customer_budget_dict["wh acts"] = round_int(self.customer_budget_dict["wh budget"] * (act_boost/weight - 1))

            self.customer_budget_dict["ent budget"] += self.customer_budget_dict["ent acts"]
            self.customer_budget_dict["wh budget"] += self.customer_budget_dict["wh acts"]


        def count_budget_description(self):
            try:
                base_ent_budget = self.customer_budget_dict["ent budget"] - self.customer_budget_dict["ent advertising"] - self.customer_budget_dict["ent acts"]
                base_wh_budget = self.customer_budget_dict["wh budget"] - self.customer_budget_dict["wh advertising"] - self.customer_budget_dict["wh acts"]
            except:
                self.calculate_average_customer_budget()
                base_ent_budget = self.customer_budget_dict["ent budget"] - self.customer_budget_dict["ent advertising"] - self.customer_budget_dict["ent acts"]
                base_wh_budget = self.customer_budget_dict["wh budget"] - self.customer_budget_dict["wh advertising"] - self.customer_budget_dict["wh acts"]

            # Entertainment budget description

            des = __("Your customers' average {b}entertainment budget{/b} is estimated to be around {b}%s gold{/b}") % int(self.customer_budget_dict["ent budget"])

            if self.customer_budget_dict["ent budget"] != base_ent_budget:
                des += " ("
                if self.customer_budget_dict["ent advertising"]:
                    des += event_color["good"] % ("+%s from advertising" % int(self.customer_budget_dict["ent advertising"]))
                    if self.customer_budget_dict["ent acts"]:
                        des += ", "
                if self.customer_budget_dict["ent acts"] > 0:
                    des += event_color["good"] % ("+%s from job bonuses" % int(self.customer_budget_dict["ent acts"]))
                elif self.customer_budget_dict["ent acts"] < 0:
                    des += event_color["bad"] % ("%s from job bonuses" % int(self.customer_budget_dict["ent acts"]))
                des += ")"

            des += ".\n"

            # Whoring budget description

            des += __("\nYour customers' average {b}whoring budget{/b} is estimated to be around {b}%s gold{/b}") % int(self.customer_budget_dict["wh budget"])

            if self.customer_budget_dict["wh budget"] != base_wh_budget:
                des += " ("
                if self.customer_budget_dict["wh advertising"]:
                    des += event_color["good"] % ("+%s from advertising" % int(self.customer_budget_dict["wh advertising"]))
                    if self.customer_budget_dict["wh acts"]:
                        des += ", "
                if self.customer_budget_dict["wh acts"] > 0:
                    des += event_color["good"] % (__("+%s from sex acts") % int(self.customer_budget_dict["wh acts"]))
                elif self.customer_budget_dict["wh acts"] < 0:
                    des += event_color["bad"] % (__("%s from sex acts") % int(self.customer_budget_dict["wh acts"]))
                des += ")"

            des += "."

            return des

        def count_customers_description(self, short=False, col=c_lightblue):


            try:
                base_cust_nb = self.customer_count - self.customer_count_dict["advertising"] - self.customer_count_dict["special"]
            except:
                self.update_customer_count()
                base_cust_nb = self.customer_count - self.customer_count_dict["advertising"] - self.customer_count_dict["special"]

            if short:
                des = __("{color=%s}{b}%i customer%s{/b}{/color} expected") % (col, self.customer_count, plural(self.customer_count))
            else:
                des = __("{b}%i customer%s{/b} are expected to come to the brothel tonight") % (self.customer_count, plural(self.customer_count))

            if self.customer_count != base_cust_nb:
                des += " ("

                if self.customer_count_dict["advertising"]:
                    if short:
                        des += event_color["good"] % ("Ads: +%s" % str_int(self.customer_count_dict["advertising"]))
                    else:
                        des += event_color["good"] % ("+" + str_int(self.customer_count_dict["advertising"]) + " from advertising")
                    if self.customer_count_dict["special"]:
                        des += ", "
                if self.customer_count_dict["special"]:
                    if short:
                        des += event_color["good"] % ("Other: +%s" % str_int(self.customer_count_dict["special"]))
                    else:
                        des += event_color["good"] % ("+" + str_int(self.customer_count_dict["special"]) + " from girls and brothel effects")

                des += ")"

            return des + "."

        def get_advertising(self, boost=True):

            r = self.advertising + self.get_effect("change", "advertising")

            if boost:
                return r * self.get_effect("boost", "advertising")
            else:
                return r

        def get_adv_reputation(self):
            raw_adv = self.advertising
            bonus_adv = self.get_advertising() - raw_adv

            raw_adv *= advertising_settings[self.get_effect("special", "advertising power")]["reputation"]
            bonus_adv *= advertising_settings[self.get_effect("special", "advertising power")]["reputation"]
            decay = (raw_adv + bonus_adv) * reputation_decay[game.chapter]

            return raw_adv, bonus_adv, decay

        def get_adv_setting(self, target):
            adv_lvl = self.get_effect("special", "advertising power")

            if target == "attraction":

                # Neutral advertising setting
                if self.advertising_setting == 0:
                    r = advertising_settings[adv_lvl]["customer attraction"]

                # Custom advertising setting
                elif self.advertising_setting == 2: # 2 is the min setting
                    r = advertising_settings[adv_lvl]["min customer attraction"]
                elif self.advertising_setting == 1: # 1 is the low setting
                    r = (advertising_settings[adv_lvl]["customer attraction"] + advertising_settings[adv_lvl]["min customer attraction"]) / 2
                elif self.advertising_setting == -1: # -1 is the high setting
                    r = (advertising_settings[adv_lvl]["customer attraction"] + advertising_settings[adv_lvl]["max customer attraction"]) / 2
                elif self.advertising_setting == -2: # -2 is the max setting
                    r = advertising_settings[adv_lvl]["max customer attraction"]

            elif target == "budget":
                r = 1.0

                # Neutral advertising setting
                if self.advertising_setting == 0: # 0 is the neutral setting
                    r += advertising_settings[adv_lvl]["customer budget"]

                # Custom advertising setting

                elif self.advertising_setting == -2: # -2 is the min setting
                    r += advertising_settings[adv_lvl]["min customer budget"]
                elif self.advertising_setting == -1: # -1 is the low setting
                    r += (advertising_settings[adv_lvl]["customer budget"] + advertising_settings[adv_lvl]["min customer budget"]) / 2
                elif self.advertising_setting == 1: # 1 is the high setting
                    r += (advertising_settings[adv_lvl]["customer budget"] + advertising_settings[adv_lvl]["max customer budget"]) / 2
                elif self.advertising_setting == 2: # 2 is the max setting
                    r += advertising_settings[adv_lvl]["max customer budget"]

            return r

        def get_adv_attraction(self):

            # Customer attraction boost is proportional to advertising
            return self.get_adv_setting("attraction") * self.get_advertising()

        def get_adv_budget(self):

            # Customer budget boost is proportional to advertising/max_advertising ratio
            # Budget setting is expressed as a percentage increase to base budget, so we add 100% (same as 'boost' effects)
            return 1.0 + (self.get_adv_setting("budget") * self.get_advertising() / self.max_help)


        # Maintenance

        def get_maintenance(self):
            return (self.maintenance + self.get_effect("change", "maintenance")) * self.get_effect("boost", "maintenance")


        ## Brothel Threat

        def get_gold_threat(self):

            gt = (MC.gold - self.get_effect("special", "safe")) / gold_threat_amount[district.rank]

            if gt > gold_threat_max[game.chapter]:
                return gold_threat_max[game.chapter]
            else:
                return gt

        def get_threat(self): # Threat is influenced by district rank, gold (up to a maximum) and the number of working girls

            threat = district.rank + self.get_gold_threat() + sum(girl.rank/2.0 for girl in MC.girls if girl.works_today())

            return threat * self.get_effect("boost", "threat") + self.get_effect("change", "threat")

        def get_risk(self):

            return self.get_threat() - self.get_security()

        def estimate_threat_level(self, contrast=False, caps=False):

            risk = self.get_risk()

            if risk >= 10:
                level =  "very high"
                col = "bad"

            elif risk >= 5:
                level =  "high"
                if contrast:
                    col = "a little bad contrast"
                else:
                    col = "a little bad"

            elif risk <= -10:
                level =  "very low"
                col = "good"

            elif risk <= -5:
                level = "low"
                col = "a little good"

            else:
                level = "normal"
                if contrast:
                    col = "normal contrast"
                else:
                    col = "normal"

            if caps:
                level = capitalize(level)

            return "{b}%s{/b}" % event_color[col] % level

        def threat_build_up(self): # Builds up threat every turn depending on active security, with a minimum of 1. Returns True if security event can proc.

            if self.security_grace_period > 0: # Goes down one tick every day if the grace period is active. The grace period restarts after a security event happens.
                self.security_grace_period -= 1
                return False

            if self.get_risk() < 1:
                self.threat += 1 * self.get_effect("boost", "threat build up")
            else:
                self.threat += self.get_risk() * self.get_effect("boost", "threat build up")

            if self.threat >= 50 and self.alert_level == 3:
                return True
            elif self.threat >= 25 and self.alert_level == 2:
                return True
            elif self.threat >= 10 and self.alert_level == 1:
                return True

            return False

        def reset_threat(self):
            self.alert_level = 1
            self.threat = 0
            self.security_grace_period = game.get_diff_setting("security")

        def get_ASM_report(self, short=False):

            cust, extra = self.customer_count, self.customer_count_dict["special"]
            msg = ""

            if short:
                msg += __("Advertising: %s") % brothel.count_customers_description(short=True)

                msg += __("\nSecurity: The threat level is %s.") % self.estimate_threat_level(contrast=False)

                msg += __("\nMaintenance: %s") % maintenance_desc[self.get_cleanliness()]

            else:
                msg += __("Advertising report: %s") % brothel.count_customers_description()

                msg += __(".\n\nSecurity report: The threat to your brothel is %s.") % self.estimate_threat_level(contrast=True)

                msg += __("\n\nMaintenance report: %s") % maintenance_desc[self.get_cleanliness()]

            return msg


        def change_rep_nightly(self, chg):
            return self.change_rep(chg, raw=False, silent=True)

        def change_rep(self, chg, raw=True, silent=False): # Boost and change effects are only applied once nightly

            if not raw:
                chg = chg * reverse_if(self.get_effect("boost", "brothel reputation"), chg) + self.get_effect("change", "brothel reputation")

            chg = get_change_min_max(self.rep, chg, 0, self.max_rep)
            self.rep += chg

            notify(__("%s: reputation: %s") % (brothel.name, plus_text(chg, color_scheme="rep")))

            return chg


        # ROOMS

        def upgrade_bedrooms(self):

            price = self.get_room_upgrade_price(self.bedrooms)

            text1 = "Do you really want to upgrade the bedrooms for " + str(price) + " gold?"

            if self.bedroom_type.level < self.maxupgrade:

                if renpy.call_screen("yes_no", text1):

                    if MC.has_gold(price):

                        MC.gold -= price
                        self.total_value += price

                        self.bedroom_type = room_dict[self.bedroom_type.level+1]
                        unlock_pic(self.bedroom_type.pic_path)


                        norollback()

                        renpy.restart_interaction()

                    else:
                        renpy.say(narrator, __("You don't have enough money."))

            else:
                renpy.say(sill, __("You cannot upgrade this brothel's rooms further."))

        def get_mood_modifier(self, rank): #Increases with bedroom type: Girls score higher with customers and their mood improves

            mood_modifier = self.bedroom_type.level + self.get_effect("change", "mood modifier") - (rank * 2)

            return mood_modifier


        def get_room_price(self, room = "bedroom"):

            if room == "bedroom":
                price = (100 * self.bedrooms)

                for lvl in range(self.bedroom_type.level):

                    price += 50 * lvl

                price *= district.rank #? Increased bedroom price

            else:
                if brothel_firstvisit or self.free_room:
                    price = 0
                else:
                    price = sum(room.level for room in self.rooms.values()) * (50 + 150*1.5**(game.chapter-1)) # (sum(room.level for room in self.rooms.values()) - 1) * (50 + 150*1.5**(game.chapter-1))

            return round_int(price)

        def get_room_upgrade_price(self, nb = 1):
            # This is the cost per bedroom
            price = 50 * self.bedroom_type.level * district.rank #? Increased room upgrade price
            return price * nb

        def add_room(self, room = "bedroom", forced=False):

            if room == "bedroom":

                price = self.get_room_price()

                text1 = __("Do you want to buy a new bedroom for %s gold?") % str(price)

                if self.bedrooms < self.get_maxbedrooms():

                    if forced or renpy.call_screen("yes_no", text1):

                        if forced or MC.has_gold(price):

                            MC.change_gold(-price)
                            self.total_value += price

                            self.bedrooms += 1

                            test_achievement("upgrades")

                            norollback()

                            renpy.restart_interaction()

                            return True

                        else:
                            renpy.say(narrator, __("You don't have enough money."))
                            return False
                else:
                    renpy.say(sill, __("You already have the maximum number of bedrooms for this brothel."))
                    return False

            else:
                self.rooms[room].buy(forced)
#                 test_achievement("upgrades")

        def upgrade_room(self, room):
            self.rooms[room].upgrade()
#             test_achievement("upgrades")

        def has_room(self, room = "any"):

            if room == "bedroom":
                return True

            elif room != "any":

                if self.rooms[room.lower()].level > 0:
                    return True

                else:
                    return False

            else:
                if self.get_common_rooms():
                    return True
                return False

        def get_common_rooms(self):
            return [room for room in self.rooms.values() if room.level > 0]

        def get_bedroom_pic(self, x=None, y=None):
            return self.bedroom_type.get_pic(x, y)

        def get_room_pic(self, type, x, y):
            if type == "bedroom":
                return self.get_bedroom_pic(x, y)
            elif type.lower() == "tavern":
                return tavern.get_pic(x, y)
            elif type.lower() == "strip club":
                return club.get_pic(x, y)
            elif type.lower() == "onsen":
                return onsen.get_pic(x, y)
            elif type.lower() == "okiya":
                return okiya.get_pic(x, y)

        def get_random_room_pic_path(self, show_dirt=True):
            if show_dirt:
                return rand_choice(self.get_common_rooms()).get_bg(self.get_cleanliness())

            return rand_choice(self.get_common_rooms()).get_bg()

        def get_random_room_pic(self, show_dirt=True):
            if show_dirt:
                return rand_choice(self.get_common_rooms()).get_bg(self.get_cleanliness())

            return rand_choice(self.get_common_rooms()).get_bg()

        def get_adv_cost(self):

            return self.advertising * helper_cost[district.rank]

        def get_sec_cost(self):

            return self.security * helper_cost[district.rank]

        def get_maintenance_cost(self):

            return self.maintenance * helper_cost[district.rank]

        def change_dirt(self, nb):

            boost = self.get_effect("boost", "dirt")

            boost = reverse_if(boost, nb)

            nb *= boost

            if self.dirt + nb < 0:
                nb = -self.dirt
                self.dirt = 0
            elif self.dirt + nb > 1000:
                nb = 1000 - self.dirt
                self.dirt = 1000
            else:
                self.dirt += nb

            return nb

        def get_cleanliness(self):

            if self.dirt < 10:
                return "clean"
            elif self.dirt < 25*district.rank:
                return "clean enough"
            elif self.dirt < 50*district.rank:
                return "dusty"
            elif self.dirt < 75*district.rank:
                return "dirty"
            elif self.dirt < 100*district.rank:
                return "disgusting"
            else:
                return "fire"

        def clean_up(self, factor = 1.0):

            price = round_int(self.get_clean_up_cost() * factor)

            if MC.has_gold(price):

                MC.gold -= price
                self.dirt = self.dirt - self.dirt * factor
                game.track("gold clean", price)
                norollback()

                return True

            else:
                renpy.say(narrator, __("You don't have enough money."))

                return False

        def get_clean_up_cost(self):
            rank_factor = {1: 0.05, 2: 0.1, 3: 0.2, 4: 0.3, 5: 0.4}

            return round_int((1.0 + rank_factor[district.rank]) * (helper_cost[district.rank]*self.dirt))

        def get_auction_value(self):
            v = max(self.total_value - self.get_clean_up_cost(), 0)

            mod = (dice(7-district.rank) - 1) * 0.025 + (6-district.rank) * 0.05

            return round_int(v * mod * game.get_diff_setting("gold"))

        def cycle_pic(self, reverse = False):

            if not reverse:
                self.pic_index += 1
                if self.pic_index > 7:
                    self.pic_index = 1
            else:
                self.pic_index -= 1
                if self.pic_index < 1:
                    self.pic_index = 7

            debug_notify("Cycling..." + str(self.pic_index))

            self.pic = self.get_pic(config.screen_width, int(config.screen_height*0.8))

            renpy.jump("brothel")

        def get_income(self, old=False): # Income is stored in the NPC_taxgirl object to avoid reset when switching brothels
            if old:
                return NPC_taxgirl.old_MC_income
            return int(NPC_taxgirl.MC_income / self.get_effect("boost", "taxable net income")) # Calculates full income






    class Location(object):

        """This class is used for locations you can visit in the various city districts"""

        def __init__(self, name, pic, has_girls = True, secret = False, action = False, menu = None, menu_costs_AP = True):

            self.name = name
            self.pic = "resources/districts/locations/" + pic
            self.has_girls = has_girls
            self.secret = secret
            self.action = action
            self.menu = menu # Menu is a tuple: first is the button caption, second is the target label
            self.menu_costs_AP = menu_costs_AP
            self.girls = []
            self.runaways = []

        def get_district(self): # Returns the location's parent district
            for d in district_dict.values():
                if self in d.locations:
                    return d
            return None

        def get_pic(self, x=None, y=None, wide=False):
            if not x:
                x = config.screen_width
            if not y:
                y = config.screen_height
                if wide:
                    y = int(y*0.8)

            return im.Scale(self.pic, x, y)

        def list_girls(self):

            l = []

            for g in self.girls:

                l.append(g.name)

            return "This location has girls: " + and_text(l)

        def clear_girls(self):

            del self.girls[:]

            return

        def can_do_action(self):
            if not self.action:
                return False
            if self.menu_costs_AP and MC.interactions < 1:
                return False
            if self.menu[1].startswith("collect_"):
                if MC.last_collected[self.menu[1][8:]] == calendar.time:
                    return False
            elif self.menu[1] == "visit_thieves_guild":
                if not NPC_renza.items:
                    return False
            elif self.menu[1] == "visit_watchtower":
                if not NPC_captain.items:
                    return False
            return True

        ## BK Evolution: Data serialization
        @classmethod
        def from_dict(cls, d):
            """EN: Deserialize Location from dict.
               ZH: 从字典反序列化 Location。"""
            _menu = None
            _mcap = d.get("menu_caption_i18n")
            _mlbl = d.get("menu_label")
            if _mcap and _mlbl:
                _menu = (__(_mcap), _mlbl)
            elif _mlbl:
                _menu = (None, _mlbl)
            return cls(
                name=d.get("name", ""),
                pic=d.get("pic", ""),
                has_girls=d.get("has_girls", True),
                secret=d.get("secret", False),
                action=d.get("action", False),
                menu=_menu,
                menu_costs_AP=d.get("menu_costs_AP", True),
            )

        def to_dict(self):
            """EN: Serialize Location to dict.
               ZH: 将 Location 序列化为字典。"""
            d = {
                "name": self.name,
                "pic": self.pic.replace("resources/districts/locations/", "") if self.pic else "",
                "has_girls": self.has_girls,
                "secret": self.secret,
                "action": self.action,
                "menu_costs_AP": self.menu_costs_AP,
            }
            if self.menu:
                d["menu_caption_i18n"] = self.menu[0] if self.menu[0] else None
                d["menu_label"] = self.menu[1]
            return d


    class Room(object):

        """This class is for rooms in a brothel, normal (bedrooms) and special (commons)"""

        def __init__(self, name, level = 0, type = "bedroom", job = None, cost=0): # Level is used for price of special rooms

            self.name = name
            self.level = level # Should be replaced with rank
            self.type = type # bedroom or special
            self.cust_limit = 0
            self.job = job
            self.cost = cost
            self.girls = [] # Used for the master bedroom
            self.build_pics()

        def build_pics(self):
            self.pic_path = "resources/brothels/rooms/" + room_pics[self.name]
            self.pic = Picture(path=self.pic_path)
            self.bg = {}
            self.bg["clean"] = "bg " + self.name

            if self.type == "special":
                self.bg["clean"] = "bg " + self.name
                root = "bg " + self.name

                for dirt_state in ("clean enough", "dusty", "dirty", "disgusting", "fire"):
                    name = root + {"clean enough" : "", "dusty" : " dusty", "dirty" : " dirty", "disgusting" : " verydirty", "fire" : " verydirty"}[dirt_state]
                    #renpy.image(self.name + " " + dirt_state, ProportionalScale(path, config.screen_width, config.screen_height))
                    self.bg[dirt_state] = name
            else:
                renpy.image("bg " + self.name, ProportionalScale(self.pic_path))

        def add_girl(self, girl): # Used for the master bedroom
            if len(self.girls) < self.level:
                self.girls.append(girl)
                return True
            else:
                return False

        def remove_girl(self, girl): # Used for the master bedroom
            if girl in self.girls:
                self.girls.remove(girl)
                return True
            return False

        def can_have_girl(self, number=1):
            if len(self.girls) + number <= self.level:
                return True
            return False

        def buy(self, forced=False):
            if forced:
                self.level = 1
                self.update_cust_limit(True)

            elif brothel.free_room:
                if renpy.call_screen("yes_no", __("Do you really want to choose the %s as your free room?") % self.name):
                    renpy.play(s_spell, "sound")
                    self.level = 1
                    self.update_cust_limit()
                    brothel.free_room = False

            elif self.get_price() >= MC.gold:
                renpy.say(sill, __("Sorry Master, you do not have enough gold to build this room."))


            elif renpy.call_screen("yes_no", __("Are you sure you want to build the %s for %s gold?") % (self.name, str(self.get_price()))):
                MC.gold -= self.get_price()
                brothel.total_value += self.get_price()
                renpy.play(s_gold, "sound")
                self.level = 1
                self.update_cust_limit()

            unlock_pic(self.pic_path)

        def upgrade(self, forced = False):
            if forced:
                self.level += 1
                self.update_cust_limit(True)
            elif self.get_price() >= MC.gold:
                renpy.say(sill, __("Sorry Master, you do not have enough gold to upgrade this room."))
            elif renpy.call_screen("yes_no", __("Are you sure you want to upgrade the %s for %s gold?") % (self.name, str(self.get_price()))):
                MC.gold -= self.get_price()
                brothel.total_value += self.get_price()
                renpy.play(s_gold, "sound")
                self.level += 1
                self.update_cust_limit()

        def get_pic(self, x=None, y=None, proportional=True):
            if not x:
                x = config.screen_width
            if not y:
                y = config.screen_height
            return self.pic.get(x, y, proportional)

        def get_bg(self, dirt_state="clean"):
            if self.type == "special":
                return self.bg[dirt_state]
            else:
                return self.bg["clean"]

        def get_price(self):
            if self.cost:
                return self.cost
            else:
                return brothel.get_room_price(self.type)

        def get_description(self):
            if self.type == "master":
                if self.level > 1:
                    desc = __("Can host up to {b}%s girls{/b} for training. Girls in the master bedroom receive {b}free training{/b} every night.") % self.level
                elif self.level == 1:
                    desc = __("Can host up to {b}1 girl{/b} for training. Girls in the master bedroom receive {b}free training{/b} every night.")
                else:
                    desc = __("Your bachelor pad. No room for a bachelorette yet.")

                if self.level < brothel.rank:
                    desc += __(" Improve this room for {b}%s gold{/b}.") % master_bedrooms[self.level+1].cost
                elif self.level == 5:
                    desc += __(" {i}You cannot improve the master bedroom further.{/i}")

                return desc

            if brothel_firstvisit:
                return __("Build the {b}%s{/b} to train a {b}%s{/b}.") % (__(self.name), __(self.job.capitalize()))
            elif self.level == 0:
                return __("Build the {b}%s{/b} for {b}%s gold{/b}.") % (__(self.name), self.get_price())
            elif self.level < district.rank:
                return __("The {b}%s{/b} can host %s customers every night. Upgrade the %s for {b}%s gold{/b} to accommodate more customers.") % (__(self.name), self.cust_limit, __(self.name), self.get_price())
            else:
                return __("The {b}%s{/b} can host %s customers every night.") % (__(self.name), self.cust_limit)

        def update_cust_limit(self, silent=False): # Returns value if changed
            _old = self.cust_limit
            self.cust_limit = room_capacity_dict[game.chapter] * self.level + brothel.get_effect("change", "room capacity") + brothel.get_effect("change", self.name + " room capacity")
            self.cust_limit = round_int(self.cust_limit * brothel.get_effect("boost", "room capacity") * brothel.get_effect("boost", self.name + " room capacity"))

            #<Chris Job Mod>
            if game.has_active_mod("chrisjobmod"):
                self.cust_limit = round_int(self.cust_limit * act_max_customers_modifier[self.job])
            #</Chris Job Mod>

            if self.cust_limit != _old:
                if not silent:
                    renpy.say(sill, __("You may now entertain %s customers in the %s. {w=1.0}{nw}") % (self.cust_limit, self.name))

            return self.cust_limit - _old

    class Moon(object):

        """A new Moon appears every month. They have an effect on gameplay."""

        def __init__(self, name, display_name=None, effects=None, description="", sound=None):
            self.name = (display_name or name.capitalize()) + " " + __("Moon")
            self.pic = Picture(name + ".webp", "resources/backgrounds/moons/" + name + ".webp")
            self.tb = ProportionalScale("resources/backgrounds/moons/%s tb.webp" % name, *res_tb(25))
            if effects == None: effects = []
            self.effects = effects
            self.short_description = get_description("%s" % self.name, self.effects, separator=": ")
            self.description = get_description(description, self.effects)
            self.sound = sound

        def get_effect(self, type, target): # Returns only the effect related to this object
            if type == "special":
                result = 0

            elif type in ("boost"):
                # result is a % expressed as a float. 1.0 (100%) means no positive or negative effect occur.
                result = 1.0
            else:
                # result is a number expressed as int or float. 0 means no positive or negative effect occur.
                result = 0

            for eff in self.effects:
                if eff.type == type and eff.target == target:
                    result += eff.value

            return result


    class WorldMap(object):
        """EN: Container for all world map data (districts, locations, populations, brothels).
           Supports multiple world templates for different scenarios.
           ZH: 世界地图数据容器（区域、地点、人口、青楼）。支持不同剧本的多世界模板。"""

        def __init__(self):
            self.world_id = ""
            self.world_name = ""
            self.populations = {}       # id → Population
            self.locations = {}         # id → Location
            self.districts = {}         # id → District
            self.district_order = []    # Ordered list of district ids
            self.brothels = {}          # chapter → Brothel
            self.location_groups = {}   # district_id → [location_id, ...]
            self.classifications = {    # location name lists by category
                "town": [],
                "beach": [],
                "nature": [],
                "court": [],
            }
            self.endless_district = None
            self.ui_layout = {}         # district_id → {"column": int, "row": int, "column_span": int}

        @classmethod
        def from_dict(cls, data):
            """EN: Build a WorldMap from a JSON dict.
               ZH: 从 JSON 字典构建 WorldMap。"""
            wm = cls()
            wm.world_id = data.get("world_id", "")
            wm.world_name = data.get("world_name_i18n", "")

            # 1. Load populations
            for pop_data in data.get("populations", []):
                _pid = pop_data.get("id")
                if _pid:
                    wm.populations[_pid] = Population.from_dict(pop_data)

            # 2. Load locations
            for loc_data in data.get("locations", []):
                _lid = loc_data.get("id")
                if _lid:
                    wm.locations[_lid] = Location.from_dict(loc_data)

            # 3. Load districts (needs populations + locations resolved)
            for dis_data in data.get("districts", []):
                _did = dis_data.get("id")
                if _did:
                    wm.districts[_did] = District.from_dict(dis_data, world_map=wm)

            wm.district_order = data.get("district_order", list(wm.districts.keys()))

            # 4. Load brothels
            for bro_data in data.get("brothels", []):
                _bid = bro_data.get("id")
                if _bid is not None:
                    wm.brothels[_bid] = Brothel.from_dict(bro_data)

            # 5. Load classifications
            _cls = data.get("classifications", {})
            wm.classifications["town"] = _cls.get("town_locations", [])
            wm.classifications["beach"] = _cls.get("beach_locations", [])
            wm.classifications["nature"] = _cls.get("nature_locations", [])
            wm.classifications["court"] = _cls.get("court_locations", [])

            # 6. Endless district (separate definition, not part of district_dict)
            _ed_data = data.get("endless_district")
            if _ed_data:
                wm.endless_district = District.from_dict(_ed_data, world_map=wm)

            # 7. UI layout hints
            wm.ui_layout = data.get("ui_layout", {})

            return wm


    def activate_world_map(world_map):
        """EN: Bind a WorldMap instance to the legacy global variables.
           This ensures backward compatibility with all existing code.
           ZH: 将 WorldMap 实例绑定到遗留全局变量，保证现有代码兼容。"""
        global location_dict, district_dict, all_districts, all_populations
        global all_locations, blist, town_locations, beach_locations
        global nature_locations, court_locations, endless_district, active_world_map
        active_world_map = world_map

        # District proxies
        district_dict = {k: v for k, v in world_map.districts.items()}
        all_districts = [world_map.districts[did] for did in world_map.district_order if did in world_map.districts]

        # Location proxies
        location_dict = {}
        for did, dis in world_map.districts.items():
            location_dict[dis.name] = dis.locations
            # Also index by location name for direct lookup
            for loc in dis.locations:
                location_dict[loc.name] = loc
        all_locations = []
        for dis in all_districts:
            all_locations.extend(dis.locations)

        # Population proxies
        all_populations = list(world_map.populations.values())

        # Brothel proxies
        blist = {k: v for k, v in world_map.brothels.items()}

        # Classification proxies
        town_locations = list(world_map.classifications.get("town", []))
        beach_locations = list(world_map.classifications.get("beach", []))
        nature_locations = list(world_map.classifications.get("nature", []))
        court_locations = list(world_map.classifications.get("court", []))

        # Endless district proxy
        endless_district = world_map.endless_district

        # Expose each location as a global variable for backward compatibility (e.g. shipyard, beach)
        # EN: Also sync location unlock state to UnlockRegistry.
        # ZH: 同时将位置解锁状态同步到 UnlockRegistry。
        for loc_id, loc in world_map.locations.items():
            safe_name = loc.name.lower().replace(" ", "_")
            try:
                setattr(store, safe_name, loc)
            except:
                pass

            # EN: Also expose by location id for cases where id != name (e.g. farmland).
            # ZH: 当 id 与 name 不同时，也按 location id 暴露（如 farmland）。
            safe_id = loc_id.lower().replace(" ", "_")
            if safe_id != safe_name:
                try:
                    setattr(store, safe_id, loc)
                except:
                    pass

            if getattr(loc, 'action', False):
                unlock_registry.unlock(loc_id)

        return world_map


