#### Character classes ####

init -2 python:

    # Phase 2.4: Lightweight data validation for from_dict() constructors
    def _require_fields(data, *required, **typed):
        """Validate dict has required keys and optional type-checked keys.

        Raises ValueError with a clear message if validation fails.
        Example: _require_fields(d, "name", "type", effects=list)
        """
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError("Missing required fields: %s" % ", ".join(missing))
        for key, expected_type in typed.items():
            if key in data and not isinstance(data[key], expected_type):
                raise ValueError(
                    "Field '%s' expected %s, got %s" % (key, expected_type.__name__, type(data[key]).__name__)
                )

    class Stat(object):

        """This class is for stats (skills with a value that can be changed)."""

        def __init__(self, name, type, parent, weight=0):

            self.name = name
            self.type = type
            self.parent = parent # For now, parent can be a Girl object only
            self.statmax = self.get_statmax()
            self.init_value(weight)
            self.lastvalue = self.value

        def get_description(self, total_value, maxrange):
            base_value = round_int(self.value)
            bonus = total_value - base_value
            bonus_text = ""
            col = "normal"

            if bonus:
                if bonus > 0:
                    col = "good"
                elif bonus < 0:
                    col = "bad"
                bonus_text = " (%s)" % plus_text(bonus, color_scheme="standard")

            ## EN: gstats_dict is built at init -4, before the string table loads (init 0), so its values are raw English. Translate at this display point instead.
            ## ZH: gstats_dict 构建于 init -4，早于字符串表加载（init 0），值仍为英文原文，故在显示点运行时查表翻译。
            description = __("%s%s. %s") % (event_color[col] % ("{b}%s/%s{/b}" % (int(total_value), maxrange)), bonus_text, __(gstats_dict[self.name]))

            if self.name in gstat_job_skill.keys():
                return description % (self.parent.get_max_cust_served(gstat_job_skill[self.name]), plural(self.parent.get_max_cust_served(gstat_job_skill[self.name])))

            return description

        def get_statmax(self):
            statmax = self.parent.rank * 50
            statmax += self.parent.get_effect("change", self.name.lower(), change_cap=True) + self.parent.get_effect("change", self.name.lower() + " max") + self.parent.get_effect("change", "all skill max")

            return statmax

        def set(self, val): # Forces a stat to raw value val, ignoring random generation and caps
            self.value = val

        def init_value(self, weight): # Where weight is a number from 0 to 5

            if self.type != "sex": # REGULAR SKILLS

                # Skills have 5 levels of base proficiency from 1 (terrible) to 5 (superb)
                # Throws a dice if proficiency (weight) is not specified in init file

                if not weight: # Returns a random weight from 1 to 5
                    weight = weighted_choice([(5, 5), (4, 10), (3, 50), (2, 25), (1, 10)]) # The second number reads as a percentage chance (eg 25 = 25%)

                # This dict lists (a, b) for the skill maximum formula: a + lvl*b
                weight_dict = {5: (33, 7), 4 : (24, 6), 3 : (15, 5), 2 : (6, 4), 1 : (2, 3), 0 : (0, 0)}

                _min = weight_dict[weight-1][0] + self.parent.level * weight_dict[weight-1][1]
                _max = weight_dict[weight][0] + self.parent.level * weight_dict[weight][1]

                _max = min(_max, self.statmax) # Caps maximum according to rank and girl effects
                _min = min(_min, _max) # Minimum cannot exceed maximum

                self.value = renpy.random.randint(_min, _max)

            else: # SEX SKILLS

                # Sex skills are initiated depending on sexual preferences (generated first)
                # Checks preference

                pref = self.parent.get_preference(self.name.lower())

                weight = {"fascinated" : 8, "very interested" : 7, "interested" : 6, "a little interested" : 5, "indifferent" : 4, "a little reluctant" : 3, "reluctant" : 2, "very reluctant" : 1, "refuses" : 0}[pref]

                pref_dict = {8 : (33, 6), 7 : (24, 5), 6 : (20, 4), 5 : (16, 3), 4 : (11, 3), 3 : (7, 2), 2 : (2, 2), 1 : (0, 1), 0 : (0, 0), -1 : (0, 0)}

                _min = pref_dict[weight-1][0] + self.parent.level * pref_dict[weight-1][1]
                _max = pref_dict[weight][0] + self.parent.level * pref_dict[weight][1]

                _max = min(_max, self.statmax) # Caps maximum according to rank and girl effects
                _min = min(_min, _max) # Minimum cannot exceed maximum

                self.value = renpy.random.randint(_min, _max)

        # def init_value_old(self, weight):
        #
        #     if self.type == "sex":
        #         pref = self.parent.get_preference(self.name.lower())
        #
        #         if pref == "refuses":
        #             a = 0
        #             b = -5
        #         elif pref in ("very reluctant", "reluctant"):
        #             a = 1.5
        #             b = 3.5
        #         elif pref in ("a little reluctant", "indifferent"):
        #             a = 5
        #             b = 10
        #         elif pref in ("a little interested", "interested"):
        #             a = 7.5
        #             b = 17.5
        #         elif pref in ("very interested", "fascinated"):
        #             a = 12.5
        #             b = 22.5
        #     else:
        #
        #         # Loads the dice if specified in init file
        #
        #         if weight == 5:
        #             d = 100
        #         elif weight == 4:
        #             d = 90
        #         elif weight == 3:
        #             d = 50
        #         elif weight == 2:
        #             d = 20
        #         elif weight == 1:
        #             d = 0
        #         else:
        #             d = dice(100)
        #
        #         if self.type == "sex":
        #
        #             a = 0
        #             b = -5
        #
        #         elif d > 98: # Superb skill
        #
        #             a = 12.5
        #             b = 22.5
        #
        #         elif d > 85: # High skill
        #
        #             a = 7.5
        #             b = 17.5
        #
        #         elif d > 35: # Average skill
        #
        #             a = 5
        #             b = 10
        #
        #         elif d > 10: # Low skill
        #
        #             a = 1.5
        #             b = 3.5
        #
        #         else: # Terrible skill
        #
        #             a = 0
        #             b = -5
        #
        #     self.value = dice(5 + 5 * game.chapter) + a * game.chapter + b # Changed district.rank to game.chapter to allow for higher stats
        #
        #     if self.value < 0:
        #         self.value = 0
        #
        #     elif self.value > self.statmax:
        #         self.value = self.statmax


        def change(self, chg, _max = 250):

            # Will not revert to cap if value is already higher
            if self.value > _max:
                _max = self.value

            if self.value + chg < 0:

                r = -self.value

                self.value = 0

                return r

            elif self.value + chg > _max:

                r = _max - self.value

                self.value = _max

                return r

            else:
                self.value += chg

                return chg


    class Trait(object):

        """This class is for traits (skills with special effects that are either on or off)."""

        # eff1, eff2, eff3 are kept for backwards compatibility, until I clean up the code

        def __init__(self, name, verb = "be", eff1 = None, eff2 = None, eff3 = None, effects = None, opposite = None, archetype = None, base_description = "", public=True, name_i18n=None):
            # Setting 'public' to True means any girl can generate with this trait. False means it can only be generated through code or _BK.ini

            self.name = name
            self.display_name = __(name_i18n) if name_i18n else __(name)
            self.verb = verb

            self.effects = []

            if effects:
                self.effects = make_list(effects, Effect)
                _builtin_dict = __import__('builtins').dict
                self.effects = [Effect.from_dict(e) if isinstance(e, _builtin_dict) else e for e in self.effects]
            if eff1:
                self.effects.append(eff1)
            if eff2:
                self.effects.append(eff2)
            if eff3:
                self.effects.append(eff3)

            if opposite == None:
                self.opposite = []
            else:
                self.opposite = make_list(opposite)
            self.archetype = archetype

            self.base_description = __(base_description)
            self.public = public

        ## Phase 6: Data serialization
        @classmethod
        def from_dict(cls, d):
            # Phase 2.4: Validate required fields
            _require_fields(d, "name")
            effects = d.get("effects", [])
            if effects:
                _builtin_dict = __import__('builtins').dict
            effects = [Effect.from_dict(e) if isinstance(e, _builtin_dict) else e for e in effects]
            return cls(
                name=d.get("name"),
                verb=d.get("verb", "be"),
                effects=effects,
                opposite=d.get("opposite"),
                archetype=d.get("archetype"),
                base_description=get_i18n(d, "base_description", ""),
                public=d.get("public", True),
                name_i18n=get_i18n(d, "name", None),
            )

        def to_dict(self):
            return {
                "name": self.name,
                "verb": self.verb,
                "effects": [e.to_dict() for e in self.effects],
                "opposite": self.opposite,
                "archetype": self.archetype,
                "base_description_i18n": self.base_description,
                "public": self.public,
            }

        def get_past_tense(self):

            if self.verb.startswith("be"):
                text1 = __("was")
            elif self.verb.startswith("have"):
                text1 = __("had")

            return self.add_article(text1) + " {b}" + self.name.lower() + "{/b}"

        def add_article(self, mytext):
            if self.verb.endswith("a"):
                mytext += " a"
            elif self.verb.endswith("an"):
                mytext += " an"

            return mytext

        def get_description(self, context=None, short=False):

            if short:
                return get_description("", self.effects)
            else:
                des = get_description(self.base_description, self.effects)

                if context in ("slavemarket", "free"):
                    if self.archetype:
                        des += __("\nUnlocks {b}%s{/b} zodiac sign.") % self.archetype

                return des

    class Perk(object):

        """This class is for all kinds of perks (used in the new perk system)"""

        def __init__(self, name, type, effects, archetype=None, pic = None, perk_level=0, min_rank=0, base_description = ""):
            self.name = name
            self.type = type
            self.effects = make_list(effects, Effect)
            _builtin_dict = __import__('builtins').dict
            self.effects = [Effect.from_dict(e) if isinstance(e, _builtin_dict) else e for e in self.effects]
            self.archetype = archetype
            self.level = perk_level
            self.min_rank = perk_level
            self.value = {0: 0, 1: 1, 2: 3, 3: 5}[perk_level]

            self.pic = pic
            if base_description:
                self.base_description = base_description
            else:
                self.base_description = __(perk_description.get(self.name, ""))

        ## Phase 6: Data serialization
        @classmethod
        def from_dict(cls, d):
            # Phase 2.4: Validate required fields
            _require_fields(d, "name", "type")
            effects = d.get("effects", [])
            if effects:
                _builtin_dict = __import__('builtins').dict
            effects = [Effect.from_dict(e) if isinstance(e, _builtin_dict) else e for e in effects]
            return cls(
                name=get_i18n(d, "name"),
                type=d.get("type"),
                effects=effects,
                archetype=d.get("archetype"),
                pic=d.get("pic"),
                perk_level=d.get("perk_level", 0),
                min_rank=d.get("min_rank", 0),
                base_description=get_i18n(d, "base_description", ""),
            )

        def to_dict(self):
            return {
                "name": self.name,
                "type": self.type,
                "effects": [e.to_dict() for e in self.effects],
                "archetype": self.archetype,
                "pic": self.pic,
                "perk_level": self.level,
                "min_rank": self.min_rank,
                "base_description_i18n": self.base_description,
            }

        def get_pic(self):
            if self.pic:
                return Picture(self.pic, "resources/perks/" + self.pic)
            else:
                return None

        def get_effect(self, type, target):
            for e in self.effects:
                if e.type.lower() == type.lower() and e.target.lower() == target.lower():
                    return True
            return False

        def get_description(self, short=False):
            if short:
                return get_description("", self.effects)
            else:
                return get_description("\n{i}" + __(self.base_description) + "\n\n{/i}", self.effects)

    class PerkArchetype(object):

        """This class is for perk archetypes (used in the new perk system)"""

        def __init__(self, name, pic):

            self.name = name
            self.pic = pic
            self.unlocked = False
            self.base_description = archetype_description[self.name]

        def get_pic(self, portrait=False):
            if portrait:
                return Picture(self.pic[:-5] + " portrait" + self.pic[-5:], "resources/perks/" + self.pic[:-5] + " portrait" + self.pic[-5:])
            else:
                return Picture(self.pic, "resources/perks/" + self.pic)

        def get_perks(self, rank=None):
            if rank != None:
                return [perk for perk in perk_dict.values() if (perk.archetype == self.name and perk.level == rank)]
            else:
                mylist = [perk for perk in perk_dict.values() if (perk.archetype == self.name)]
                mylist.sort(key=lambda x: x.level)

                return mylist

        def get_description(self):
            return self.base_description








#            value = 0


#            return value


    class Effect():

        """This class is used for all effects applying to a character"""

        ## Type defines how the effect work

        # Boost applies a % increase (or decrease). Value is a float number
        # Change applies a fixed value change which is not limited by stat max. Change can be reversed. Value is a number.
        # Gain applies a one time permanent gain and is limited by stat max. Gain cannot be reversed. Value is a number.
        # Set replaces a base value with the new value
        # Allow unlocks a brothel option
        # Gift is the property of a gift item. I will have a different effect depending on a girl's tastes. Value is an int representing the gift bonus.
        # Flower is the property of a flower item. Value isn't used.
        # Special is hard-coded

        ## Value depends on the effect type. It is often used for checking the presence of an effect, so set it to 1 unless you need it to work differently

        ## Target defines what the effect affects

        ## Chance is the chance that the effect will happen. A float number.

        ## Scales_with is hard-coded for the moment and only concerns MC stats

        ## Scope is the scope of the effect: individual (None), brothel-wide ("brothel"), farm-wide ("farm"), free-girls ("city"), or "world" ("everywhere")

        def __init__(self, type, target = None, value = 0, chance = 1.0, scales_with = None, scope = None, dice=False, change_cap=True, duration=-1, source=None):
            self.type = type
            self.target = target
            self.value = value
            self.chance = chance
            self.scales_with = scales_with
            self.scope = scope
            self.source = source
            self.dice = dice
            self.change_cap = change_cap
            self.duration = duration # -1 duration = infinite. Duration is only used for buff effects

        ## Phase 6: Data serialization
        @classmethod
        def from_dict(cls, d):
            return cls(
                type=d.get("type"),
                target=d.get("target"),
                value=d.get("value", 0),
                chance=d.get("chance", 1.0),
                scales_with=d.get("scales_with"),
                scope=d.get("scope"),
                dice=d.get("dice", False),
                change_cap=d.get("change_cap", True),
                duration=d.get("duration", -1),
                source=d.get("source"),
            )

        def to_dict(self):
            return {
                "type": self.type,
                "target": self.target,
                "value": self.value,
                "chance": self.chance,
                "scales_with": self.scales_with,
                "scope": self.scope,
                "dice": self.dice,
                "change_cap": self.change_cap,
                "duration": self.duration,
                "source": self.source,
            }

        def gain(self, thing, apply_boost=False, spillover=False):

            c = 0
            result = True

            #### APPLIES SCALING EFFECTS ####

            if self.scales_with:
                factor = get_scale_factor(thing, self.scales_with)
            else:
                factor = 1.0

            if not self.target.endswith(" fixation"):
                v = factor*self.value

            #### APPLIES DICE EFFECT ####

            if self.dice:
                try:
                    v = dice(round_int(v), self.dice) # New: dice property can be an integer
                except:
                    v = dice(round_int(v))

            #### TEST EFFECT PROC CHANCE ####

            # Chance is tested here in case the gain is conditional
            if renpy.random.random() > self.chance:
                result=False

            #### APPLY EFFECT IF SUCCESSFUL ####

            # Instant cleaning (brothel)
            elif self.target == "dirt":
                c = brothel.change_dirt(v)

            elif self.target == "love": # Instant love
                c = thing.change_love(v, silent=True)

            elif self.target == "fear": # Instant fear
                c = thing.change_fear(v, silent=True)

            # Instant healing
            elif self.target == "heal":
                c = thing.heal(v)

            # Instant XP gain
            elif self.target in ("xp", "experience"):
                c = thing.change_xp(v, apply_boost=apply_boost, spillover=spillover, silent=True)

                while thing.ready_to_level():
                    thing.level_up()

            # Instant prestige gain
            elif self.target == "prestige":
                c = thing.change_prestige(v, apply_boost=apply_boost)

                if thing.ready_to_level():
                    thing.level_up()

            # Instant JP gain
            elif self.target[-3:] == " jp":
                c = thing.change_jp(v, self.target[:-3], apply_boost=apply_boost, spillover=spillover, announcement_delay=0, silent=True)

            # Instant REP gain
            elif self.target in ("rep", "reputation"):
                c = thing.change_rep(v, silent=True)

            # Instant perk points gain
            elif self.target in ("perk", "perks"):
                thing.perk_points += v
                thing.update_can_perk()
                c = v

            # Instant skill point gain
            elif self.target in ("skills", "skill points"):
                thing.upgrade_points += v
                c = v

            # Instant positive/negative fixation gain
            elif self.target.endswith(" fixation"):
                if not self.value:
                    raise AssertionError(__("Did not provide value for %s") % self.target)
                if self.value in fix_dict.keys():
                    c = thing.add_random_fixation(fixation=self.value, type=self.target[:3])[0] # because add_random_fixation returns a list
                else:
                    for i in range(self.value):
                        c = thing.add_random_fixation(type=self.target[:3])[0] # because add_random_fixation returns a list

                if c:
                    for fix in c:
                        thing.personality_unlock[c] = False

            # Instant sex preference gain
            elif self.target == "all sexual preferences":
                for act in extended_sex_acts:
                    thing.change_preference(act, v, silent=True)

            elif self.target.endswith(" preference"):
                thing.change_preference(self.target[:-11], v, silent=True)

            # Permanent stat/skill gains
            else:
                # debug_notify(factor*self.value)
                c = thing.change_stat(self.target, v, apply_boost=apply_boost, spillover=spillover, silent=True)

            # Plays a sound when activating gain/instant
            if result:
                renpy.play(s_spell, "sound")
            else:
                renpy.play(s_fizzle, "sound")

            return c

        def get_description(self):

            val = self.value
            target = self.target
            text1 = ""

            if self.type in ("special", "personality"):

                if target == "naked":
                    text1 = __("Accepts nudity")

                elif target == "level":
                    text1 = __("+1 level (max level: %s)") % str(val)

                elif target == "advertising power":
                    text1 = __("Increases the power of your advertising girls (higher bonuses to brothel reputation, customer attraction and customer budget).")

                elif target == "heal minion":
                    text1 = __("Heals a wounded minion.")

                elif target == "workwhore":
                    text1 = __("she may work a half-shift, then whore a half-shift.")

                elif target == "lucky":
                    text1 = __("higher chance of critical success when working or whoring (does not stack)")

                elif target == "unlucky":
                    text1 = __("higher chance of critical failure when working or whoring")

                elif target == "temptress":
                    text1 = __("may talk an unwilling customer into accepting a different sex act")

                elif target == "pickpocket":
                    text1 = __("chance of stealing an extra 10% tip from a customer, lowers reputation if caught")

                elif target == "random item":
                    text1 = __("Customers have a small chance to 'forget' a random item in her care.")

                elif target == "BBCR bonus":
                    text1 = __("may get a customer satisfaction boost if her beauty, body, charm or refinement skill is high enough")

                elif target == "LOCS bonus":
                    text1 = __("may get a customer satisfaction boost if her libido, obedience, constitution or sensitivity skill is high enough")

                elif target == "whore mood modifier":
                    text1 = __("mood increase when whoring")

                elif target == "job prestige":
                    text1 = __("may earn prestige when working")

                elif target == "skill catch up":
                    text1 += __("every night, she will help other girls with lower skills receive a permanent skill increase (one girl per rank)")

                elif target == "effect chance":
                    text1 += __("doubles the base chance of perks activating (up to a maximum of 50%)")

                elif target == "defender":
                    if val == 1:
                        text1 += __("you can defend the brothel once, even when you are out of AP")
                    elif val == 2:
                        text1 += __("you can defend the brothel an unlimited amount of times even when you are out of AP")

                elif target == "snake eyes":
                    text1 += __("hypnosis never fails")

                elif target == "safe":
                    text1 += __("excludes up to %s gold from the brothel threat level") % '{:,}'.format(round_int(val)).replace(',', ' ')

                elif target == "focus":
                    text1 += __("+25% to tip and reputation gains if she has only one activated sex act (not including bisexual and group)")

                elif target == "rest shield":
                    text1 += __("when resting, may cast a magic shield on herself or a friend to protect from attacks")

                elif target == "ignore budgets":
                    text1 += __("ignores customer budget limitations")

                elif target == "ignore energy":
                    text1 += __("Chance of ignoring energy loss during each interaction")

                elif target == "immune":
                    if self.chance < 1:
                        text1 += __("%i%% chance of ignoring hurt damage") % (self.chance*100)
                    else:
                        text1 += __("Cannot be hurt")

                elif target == "hypnosis spillover":
                    text1 += __("Successful hypnosis attempts have a chance to affect more girls in the brothel")

                elif target == "bisexual":
                    text1 += __("She is available for bisexual acts.")

                elif target == "group":
                    text1 += __("She is available for group sex acts.")

                elif target == "orgy":
                    text1 += __("She is available for bisexual group sex acts.")

                elif target == "ponygirl":
                    text1 += __("Adds 2 points of advertising per Rank.")

                return __(text1)

            elif self.type == "instant" and target == "heal":
                return __("accelerates a girl's healing by %s day(s).") % str(val)

            if self.type == "set":
                text1 += __("set %s%s") % (__(target), __(" to %s") % str(val))
                if self.scope:
                    text1 += " (%s)" % __(self.scope)
                return text1

            if self.type == "allow":
                if target.endswith("preference"):
                    text1 += __("Allows you to increase customers' %s by up to +%s%%.") % (__(target), str(50*val))
                else:
                    text1 += __("Allows %s to visit your brothel.") % __(target)

                return text1

            if 0.75 <= self.chance < 1.0:
                text1 += __("high chance of ")

            elif 0.25 < self.chance < 0.75:
                text1 += __("chance of ")
            elif self.chance <= 0.25:
                text1 += __("low chance of ")


            if self.type == "reroll":
                if text1:
                    text1 += __("rerolling ")
                else:
                    text1 += __("reroll")

                if self.target == "job critical failure":
                    text1 += __(" a critical failure when working")

                return text1

            if self.dice:
                text1 += "1-"

            elif is_string(val):
                pass

            elif val > 0:
                text1 += "+"

            if self.type in ("gain", "instant"): # Permanent x gain (xp, reputation...)
                try:
                    text1 += __("%s ") % str(round_int(val))
                except:
                    text1 += __("%s ") % str(val)

                if self.target.endswith("preference") or self.target.endswith("preferences"):
                    text1 += __(" to ")

            elif self.type == "change": # Temporary x effect (can be added or removed)
                text1 += __("%s to ") % str(round_best(val, 2))

            elif self.type == "resist":
                text1 += __("%s negated {#1}") % str(round_int(val))

            elif self.type == "spillover":
                percentage = round_int(val * 100)

                text1 += __("%s%% %s spread out between other girls when earning ") % (str(percentage), __(self.target))

            elif self.type == "boost": # Temporary % effect (can be removed)

                percentage = round_int(val * 100)

                text1 += __("%s%% to ") % str(percentage)

            elif self.type == "gift":
                text1 += str(round_int(val)) + " "

            elif self.type == "increase satisfaction":
                text1 += __("%s to customer satisfaction for ") % str(round_int(val))

            if self.scope and not target.startswith(self.scope): # The second part handles the 'brothel rep' special case, although renaming brothel reputation to something different to avoid confusion with girl reputation would be a good long-term fix
                #text1 += __(self.scope) + " "
                text1 += __("{0} {1}").format(__(self.scope), __(target))
            else:
                text1 += __(target)

            if target == "hurt":
                text1 += __(" damage{#1}")
            elif target in extended_sex_acts:
                text1 += __(" acts{#1}")
            elif target == "random item":
                text1 += __(" when working")

            if self.scales_with:

                if self.scales_with == "equipped":
                    text1 += __(" for each equipped item")

                elif self.scales_with == "cust nb":
                    text1 += __(" for each customer")
                elif self.scales_with == "job cust nb":
                    text1 += __(" for each customer when working")
                elif self.scales_with == "whore cust nb":
                    text1 += __(" for each customer when whoring")

                else:
                    text1 += __(" for each point of %s") % self.scales_with


            if self.duration > 0:
                text1 += __(" (for ")

                if self.duration > 1:
                    text1 += str(self.duration) + __(" turns - does not stack)")

                elif self.duration == 1:
                    text1 += __("1 turn - does not stack)")

            return __(text1)


    class Sexact(): #Attributes: name, description, contributing_stats, variants, results

        """This class is for specifying sex acts and the results they have."""


        def __init__(self, likelihood, bonus):

            self.likelihood = likelihood
            self.bonus = bonus



    class ItemType(object):

        """ This class covers common item types and their base properties """

        def __init__(self, name, usage = "wear", slot = None, filter = "misc", sound = None, adjectives = "misc", stackable = False, dir=None, sellable=True, giveable=True):

            self.name = name
            self.usage = usage
            self.slot = slot
            self.filter = filter
            self.sound = sound
            self.adjectives = adjectives
            if dir:
                self.dir = dir
            else:
                self.dir = self.name
            self.sellable = sellable
            self.giveable = giveable


    class Personality(object): # Personality archetype used to semi-randomize girl personality attributes and specific dialogue

        def __init__(self, name, attributes, personality_dialogue_only=None, dialogue_personality_weight=3, dialogue_attribute_weight=1, custom_dialogue_label=None, description="", often_stories=None, rarely_stories=None, never_stories=None):

            self.name = name
            self.attributes = attributes # 2 very strong attributes by default
#             self.generic_dialogue = generic_dialogue # Disabled. Bool, decides if this personality allows for generic dialogue or not. Custom dialogue should be provided for all relevant situations if set to False.
            if personality_dialogue_only == None: personality_dialogue_only = []
            self.personality_dialogue_only = personality_dialogue_only # A list of topics that will be limited to personality-based dialogue, not generic or attribute-based dialogue.
            self.dialogue_personality_weight = dialogue_personality_weight # Likelihood of using custom personality lines when available
            self.dialogue_attribute_weight = dialogue_attribute_weight # Likelihood of using custom attribute lines when available. Can be set to 0 to avoid all attribute dialogue.
            self.custom_dialogue_label = custom_dialogue_label # For more complex dialogue, a label must be specified. It will receive the 'girl' object and the dialogue 'topic' as arguments.

            if not often_stories: often_stories = []
            if not rarely_stories: rarely_stories = []
            if not never_stories: never_stories = []

            self.story_dict = {"often" : often_stories, "rarely" : rarely_stories, "never" : never_stories}

            self.description = description

            self.generate_gift_likes()

        def generate_gift_likes(self): # Determines gift likes for this personality archetype

            self.gift_likes = {"cute" : 0, "book" : 0, "precious" : 0, "erotica" : -0, "drinks": 0}

            for attr in self.attributes:
                for gift_type, v in gpersonalities_likes[attr].items():
                    self.gift_likes[gift_type] += v

        def generate_attributes(self, girl): # Adds 4 semi-randomized attributes to a girl

            attributes = []

            for attr in self.attributes:
                # Adds mandatory personality attributes
                attributes.append(attr)

                # Important note: for ease of code reasons, both 'very X' and 'X' attributes are added to a girl's attributes.
                if attr.startswith("very "):
                    attributes.append(attr[5:])

                # Checks every pairing and completes the girl's other attributes
                for tup in personality_attributes:
                    if tup[0] in attributes or tup[1] in attributes:
                        pass
                    else:
                        attributes.append(rand_choice(tup))

            return attributes





    class Fixation(object):

        def __init__(self, name, acts, step, frequency = 12.0, tag_list = None, not_list = None, attribute = None, short_name="", cannot_have_neg=None):

            self.name = name
            if short_name:
                self.short_name = short_name
            else:
                self.short_name = self.name
            self.acts = make_list(acts)
            if not cannot_have_neg:
                cannot_have_neg = []
            self.cannot_have_neg = cannot_have_neg
            self.step = step
            self.frequency = frequency
            if not tag_list:
                tag_list = []
            self.tag_list = tag_list
            if not not_list:
                not_list = []
            self.not_list = not_list
            self.attribute = attribute

        @classmethod
        def from_dict(cls, data):
            """EN: Create a Fixation from a JSON dict.
               ZH: 从 JSON 字典创建 Fixation 对象。"""
            return cls(
                name=data["name"],
                acts=data.get("acts", ()),
                step=data.get("step", 1),
                frequency=data.get("frequency", 12.0),
                tag_list=data.get("tag_list"),
                not_list=data.get("not_list"),
                attribute=data.get("attribute"),
                short_name=data.get("short_name", ""),
                cannot_have_neg=data.get("cannot_have_neg")
            )

        def available(self, girl, act=None, type="pos"):

            # Checks if a specific act is covered
            if act and act not in self.acts:
                return False

            # Cannot assign positive fixation which is blocked in _BK.ini
            if use_ini_sex and type == "pos" and self.name in girl.init_dict["sexual preferences/never_fixations"]:
                return False

#             # Cannot assign positive fixation if girl doesn't have the related attribute
#             if type == "pos" and not girl.is_(self.attribute):
#                 return False

#             # Cannot assign negative fixation if girl has the related attribute
#             if type == "neg" and girl.is_(self.attribute):
#                 return False

            # Checks for incompatible positive/negative fixations
            if type == "neg":
                for pos_fix in girl.pos_fixations:
                    if self.name in pos_fix.cannot_have_neg: # cannot_have_neg is a list
                        return False

            # Cannot assign the same fixation twice
            if self.name in [f.name for f in (girl.pos_fixations + girl.neg_fixations)]:
                return False

            return True

        def get_weight(self, girl, type="pos"):

            freq = self.frequency

            if self.attribute:
                if girl.is_(self.attribute):
                    freq *= 3

            if use_ini_sex and self.name in girl.init_dict["sexual preferences/favorite_fixations"]:
                freq *= 3
            elif use_ini_sex and self.name in girl.init_dict["sexual preferences/disliked_fixations"]:
                freq /= 3
            else:
                for act in self.acts:
                    if use_ini_sex and act in girl.init_dict["sexual preferences/favorite_acts"]:
                        freq *= 2
                    elif use_ini_sex and act in girl.init_dict["sexual preferences/disliked_acts"]:
                        freq /= 2

            if type == "neg":
                freq = 144/freq # Probably no longer necessary to ensure weight is an integer with the changes to weighted_choice()

            return int(freq)


