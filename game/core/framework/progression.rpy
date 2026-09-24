#### Progression classes ####

init -2 python:
    class Achievement(PicHolder):

        def __init__(self, title="My cool achievement:\nWell done, bro!", description=__("No description"), pic="misc.webp", pic_path="resources/ui/achievements/", level_nb=1, target="", requirements="default", requirements2=None, custom_titles=None, multi=1): # {1 : C, 2 : B, 3 : A, 4 : S, 5 : X}

            self.title = title
            self.description = description
            if pic_path[-1] != "/": pic_path += "/"
            self.pic = Picture(path = pic_path + pic)
            self.level_nb = level_nb #
            self.target = target
            if requirements == "default": requirements = {1 : 1, 2 : 2, 3 : 3, 4 : 4, 5 : 5}
            self.requirements = requirements
            self.requirements2 = requirements2
            self.custom_titles = custom_titles # custom_titles should be a dictionary {level : custom_title}
            self.multi = multi # Number of crystals unlocked by achievement level

            try: # Value has been stored in persistent
                self.level = persistent.achievements[self.target]
            except: # Value doesn't exist
                self.level = 0
                persistent.achievements[self.target] = 0

        @classmethod
        def from_dict(cls, d):
            """EN: Build an Achievement from a JSON dict.
               ZH: 从 JSON 字典构建成就。"""
            requirements = d.get("requirements", "default")
            # JSON keys are strings; convert integer keys back to int for requirements dicts
            # Note: Ren'Py replaces built-in dict with RevertableDict in init blocks.
            # json.loads() returns standard dict, so we must check against the real dict class.
            _real_dict = __import__('builtins').dict
            if isinstance(requirements, _real_dict):
                requirements = {int(k) if k.isdigit() else k: v for k, v in requirements.items()}
            requirements2 = d.get("requirements2")
            if isinstance(requirements2, _real_dict):
                requirements2 = {int(k) if k.isdigit() else k: v for k, v in requirements2.items()}
            custom_titles = d.get("custom_titles")
            if isinstance(custom_titles, _real_dict):
                custom_titles = {int(k) if k.isdigit() else k: v for k, v in custom_titles.items()}
            return cls(
                title=get_i18n(d, "title", ""),
                description=get_i18n(d, "description", __("No description")),
                pic=d.get("pic", "misc.webp"),
                pic_path=d.get("pic_path", "resources/ui/achievements/"),
                level_nb=d.get("level_nb", 1),
                target=d.get("target", ""),
                requirements=requirements,
                requirements2=requirements2,
                custom_titles=custom_titles,
                multi=d.get("multi", 1),
            )

        def to_dict(self):
            """EN: Serialize this achievement to a JSON-compatible dict.
               ZH: 将此成就序列化为兼容 JSON 的字典。"""
            return {
                "title": self.title,
                "description": self.description,
                "pic": self.pic.filename if self.pic else "misc.webp",
                "pic_path": self.pic.path[:-(len(self.pic.filename))] if self.pic else "resources/ui/achievements/",
                "level_nb": self.level_nb,
                "target": self.target,
                "requirements": self.requirements,
                "requirements2": self.requirements2,
                "custom_titles": self.custom_titles,
                "multi": self.multi,
            }

        def test(self): # Checks if the achievement is unlocked according to its target and requirements

            if not game.achievements:
                return False

            if self.level >= self.level_nb:
                return False

            r = 0

            if self.target == "slaves":
                r = len(MC.girls) + len(farm.girls)

            elif self.target == "gold":
                r = MC.gold

            elif self.target == "rep":
                r = brothel.rep

            elif self.target == "income":
                try:
                    r = logs[calendar.time].net
                except:
                    r = 0

            elif self.target == "losses":
                try:
                    r = -1 * logs[calendar.time].net
                except:
                    r = 0

            elif self.target == "friends":
                r = sum(1 for girl in MC.girls + farm.girls if girl.friends)

            elif self.target == "rivals":
                r = sum(1 for girl in MC.girls + farm.girls if girl.rivals)

            elif self.target == "girlfriends":
                for girl in game.free_girls:
                    if girl.MC_relationship_level >= 3:
                        r += 1

            elif self.target == "originals":
                r = sum(1 for girl in MC.girls if girl.original)

            elif self.target == "furniture": #?
                if not brothel.can_build_anything(max_chapter=self.level+2): # Checks if furniture can be built one chapter at a time (from chapter 2 to chapter 7)
                    return self.unlock(game.chapter-1) # Unlocking capped by chapter (may be unnecessary)

            elif self.target == "upgrades":
                if not brothel.can_upgrade():
                    return self.unlock(game.chapter)

            elif self.target == "months":
                r = calendar.time // 28

            elif self.target in gstats_main + gstats_sex:
                for girl in MC.girls + farm.girls:
                    if girl.get_stat(self.target) >= self.requirements2[self.level+1]:
                        r += 1

            elif self.target == "ultimate":
                for girl in MC.girls + farm.girls:
                    for stat in gstats_main + gstats_sex:
                        if girl.get_stat(stat) < self.requirements2[self.level+1]:
                            break
                    else:
                        r += 1

            elif self.target == "pos fixations":
                for girl in MC.girls + farm.girls:
                    r += sum(1 for fix in girl.pos_fixations if (girl.personality_unlock[fix.name]))

            elif self.target == "neg fixations":
                for girl in MC.girls + farm.girls:
                    r += sum(1 for fix in girl.neg_fixations if (girl.personality_unlock[fix.name]))
                    if girl.flags["removed neg fixations"]:
                        r += girl.flags["removed neg fixations"]

            elif self.target == "minions":
                r = farm.count_minions()

            elif self.target in ("Warrior", "Wizard", "Trader"):
                if MC.playerclass == self.target:
                    r = MC.level

            elif self.target.startswith("mc "):
                if MC.get_stat(self.target[3:], raw=True) >= 10:
                    return self.unlock()

            elif self.target == "good":
                if MC.get_alignment() == self.target:
                    if MC.get_alignment_delta("good") > 50:
                        return self.unlock()

            elif self.target == "neutral":
                if MC.get_alignment() == self.target:
                    if MC.get_alignment_delta("neutral") > 50:
                        return self.unlock()

            elif self.target == "evil":
                if MC.get_alignment() == self.target:
                    r = MC.get_alignment_delta("evil") # Smallest gap between evil and neutral/good points

            elif self.target == "masochist":
                for girl in MC.girls + farm.girls:
                    if girl.personality.name == "masochist" and "DS" in girl.notebook_unlocks:
                        r += 1

            elif self.target == "naked":
                for girl in MC.girls + farm.girls:
                    if girl.naked:
                        r += 1

            elif self.target in ("bisexual", "group"):
                for girl in MC.girls + farm.girls:
                    if girl.will_do_sex_act(self.target):
                        r += 1

            elif self.target in ("hands", "body", "finger", "neck", "accessory"):
                for girl in MC.girls + farm.girls:
                    if girl.get_equipped(self.target):
                        r += 1

            elif self.target.startswith("perform"):
                r = game.check(self.target)

            elif self.target in tracked_achievements:
                r = game.check(self.target)

            elif self.target[:4] == "rank":
                _rank_dict = {"C" : 1, "B" : 2, "A" : 3, "S" : 4, "X" : 5}

                for girl in MC.girls + farm.girls:
                    if girl.rank >= _rank_dict[self.target[5]]:
                        r += 1

            elif self.target == "love":
                for girl in MC.girls + farm.girls:
                    if girl.get_love() >= self.requirements2[self.level+1]:
                        r += 1

            elif self.target == "fear":
                for girl in MC.girls + farm.girls:
                    if girl.get_fear() >= self.requirements2[self.level+1]:
                        r += 1

            elif self.target == "brothel ranking":
                if brothel.my_ranking <= self.requirements[self.level+1]:
                    return self.unlock()

            elif self.target == "debug":
                self.level = 1
                return True

            if r >= self.requirements[self.level+1]:
                return self.unlock()

        def unlock(self, level_cap=99):
            if game.achievements and self.level < min(self.level_nb, level_cap):
                self.level += 1
                persistent.achievements[self.target] = self.level
                return True
            return False

        def get_title(self, _next=False, _button=False, force_level=None):
            if force_level:
                level = force_level
            else:
                level = self.level

            if self.level_nb == 1:
                return __(self.title)
            elif _button:
                return __(self.title) + " " + str(level) + "/" + str(self.level_nb)
            elif _next:
                return __(self.title) + " " + roman_numbers[level+1]
            elif self.custom_titles:
                return __(self.custom_titles[level])
            else:
                return __(self.title) + " " + roman_numbers[level]

        def get_description(self, _next=False, force_level=None):
            if force_level:
                level = force_level
            else:
                level = self.level

            if self.level_nb == 1:
                return __(self.description)

            else:
                if _next:
                    level += 1

                if self.requirements2:
                    return __(self.description) % (str(self.requirements[level]), str(self.requirements2[level]))
                elif self.requirements:
                    if isinstance(self.requirements[level], int):
                        return __(self.description) % '{:,}'.format(self.requirements[level])
                    else:
                        return __(self.description) % str(self.requirements[level])

    class Contract(object):

        # Contracts are a series of tasks (1-4) with a bonus special requirement (a given trait, perk, positive fixation, two girls (not ready), item type with minimum quality)

        def __init__(self, type, district, archetypes=None, names=None, organizers=None, venues=None, character="", MC_event_pic=None):
            self.type = type
            self.district = district
            if archetypes == None: archetypes = []
            self.archetypes = archetypes
            if names == None: names = []
            self.names = names
            if organizers == None: organizers = []
            self.organizers = organizers
            if venues == None: venues = []
            self.venues = venues
            self.character = character
            self.MC_event_pic = Picture(path=MC_event_pic).get(config.screen_width, int(config.screen_height*0.8))

            self.value = 0

        @classmethod
        def from_dict(cls, d, character_resolver=None):
            """EN: Build a Contract from a JSON dict.
               ZH: 从 JSON 字典构建契约。
               character_resolver: callable that maps character name strings to Character objects."""
            character_name = d.get("character")
            character = None
            if character_name and character_resolver:
                character = character_resolver(character_name)
            return cls(
                type=d.get("type", ""),
                district=d.get("district", ""),
                archetypes=d.get("archetypes"),
                names=[__(n) for n in d.get("names_i18n", [])] if d.get("names_i18n") else None,
                organizers=[__(o) for o in d.get("organizers_i18n", [])] if d.get("organizers_i18n") else None,
                venues=[__(v) for v in d.get("venues_i18n", [])] if d.get("venues_i18n") else None,
                character=character,
                MC_event_pic=d.get("MC_event_pic"),
            )


        def randomize(self):

            self.result = False

            # Set level (from 1 to 4)

            self.level = rand_choice(contract_level[game.chapter])
            self.base_value = contract_value[game.chapter]
            self.special_bonus = 1.0
            self.girl_number = 1

            # Set description

            self.organizer = rand_choice(self.organizers)
            self.location = rand_choice(location_dict[self.district])
            self.char = self.character
            self.venue = rand_choice(self.venues)
            self.a_venue = article(self.venue)

            self.title = rand_choice(self.names)
            self.description = self.get_description(contract_description[self.type])
            self.bg = self.location.get_pic(config.screen_width, int(config.screen_height*0.8))

            # Set special requirement (bonus)

            spe = weighted_choice(contract_specials)

            if spe == "trait":
                self.special = (spe, rand_choice([t for t in pos_traits if t.archetype in self.archetypes], 2)) # Chooses two traits to match

            elif spe == "perk":
                self.special = (spe, rand_choice([p for p in perk_dict.values() if p.archetype in self.archetypes and p.level <= district.rank])) # Chooses a perk to match

            elif spe == "fix":
                self.special = (spe, rand_choice(fix_dict.values(), 3)) # Chooses three positive fixations to match

            elif spe == "farm":
                self.special = (spe, rand_choice(farm_type_list)) # Chooses one farm weakness to match (must be known to the player)

            elif spe == "item":
                self.special = (spe, rand_choice([IT_Dress, IT_Ring, IT_Necklace, IT_Accessory]))

            elif spe == "girls":
                self.special = (spe, 2)
                self.girl_number = 2

            # Assign 1 to 4 tasks according to rank

            if self.type == "orgy":
                tasks = rand_choice([tsk for tsk in contract_tasks if tsk.soft != True], self.level)
            else:
                tasks = rand_choice(contract_tasks, self.level)

            self.tasks = make_list(tasks, ContractTask) # No longer necessary with the changes to rand_choice
            self.tasks.sort(key=lambda x: contract_task_types_order[x.type])

            diff = 1
            hard_limit = 5

            for tsk in self.tasks: # Later tasks have more chances to be hard (and are worth more)
                if dice(6) < hard_limit:
                    tsk.randomize(self, "easy")
                else:
                    tsk.randomize(self, "hard")
                hard_limit -= 1

        def get_description(self, base_text): # can be called from outside the Contract object to convert any string (may not be necessary)
            desc = base_text.replace(":ORG:", capitalize(self.organizer))
            desc = desc.replace(":org:", self.organizer)
            desc = desc.replace(":DIS:", capitalize(__(self.district)))
            desc = desc.replace(":dis:", __(self.district).lower())
            desc = desc.replace(":LOC:", self.location.name)
            desc = desc.replace(":loc:", self.location.name.lower())
            desc = desc.replace(":VEN:", capitalize(self.venue))
            desc = desc.replace(":ven:", self.venue.lower())
            desc = desc.replace(":AVEN:", capitalize(self.a_venue))
            desc = desc.replace(":aven:", self.a_venue.lower())
            return desc

        def get_special_description(self):
            spe, target = self.special

            if spe == "trait":
                return __("{b}Traits{/b}: ") + and_text([t.display_name for t in target], __(" or "))

            elif spe == "perk":
                return __("{b}Perks{/b}: ") + target.name

            elif spe == "fix":
                return __("{b}Positive fixations{/b}: ") + and_text([__(f.name.capitalize()) for f in target], __(" or "))

            elif spe == "farm":
                return __("{b}Weakness{/b}: ") + __(target.capitalize())

            elif spe == "item":
                return __("{b}Must wear{/b}: ") + target.name

            elif spe == "girls":
                return __("{b}Send two girls{/b} (extra pay)")

        def get_value(self, raw=False, no_special=False):
            r = self.base_value + sum(tsk.value for tsk in self.tasks)

            if not raw:
                r += brothel.get_effect("change", "contract rewards")
                r *= brothel.get_effect("boost", "contract rewards")

            if not no_special:
                r *= self.special_bonus

            return round_int(r)

        def get_special_value(self):
            if self.special_bonus != 1.0:
                if self.get_value(no_special=True) > 0:
                    return self.get_value() - self.get_value(no_special=True)
                else: # When refunding contract fee
                    return self.base_value
            else:
                return 0

        def enroll(self, free=False):
            calendar.active_contract = self

            task_desc = "{size=-1}"
            for tsk in self.tasks:
                task_desc += "{b}{i}" + tsk.title + "{/i}{/b}\n"
                for req in tsk.get_requirements():
                    task_desc +=  req + "\n"
            game.set_task(task_desc + "{/size}", "contract", 7)

            if not free:
                MC.gold -= self.base_value
                renpy.play(s_gold, "sound")
            return

        def can_contract(self, girl):
            if girl.hurt > 0 or girl.away or girl.exhausted:
                return False
            return True

        def run(self, girls): # Result is True if not all tasks completed, False otherwise

            # Test Special requirement

            spe, target = self.special

            if spe == "girls":
                if len(girls) >= target:
                    self.special_bonus = 1.5

            elif spe == "trait":
                for t in target:
                    if girls[0].has_trait(t.name):
                        self.special_bonus = 1.4
                        break

            elif spe == "perk":
                if girls[0].has_perk(target.name):
                    self.special_bonus = 1.3

            elif spe == "fix":
                for f in target:
                    if girls[0].has_fixation("pos", f.name):
                        self.special_bonus = 1.5
                        break

            elif spe == "farm":
                if girls[0].weakness == target and farm.knows["weakness"][girls[0]]:
                    self.special_bonus = 1.5

            elif spe == "item":
                for it in girls[0].equipped:
                    if it.type.name == target.name:
                        self.special_bonus = 1.2
                        break

            # Test tasks

            self.failed_tasks = 0

            for tsk in self.tasks: # Failed tasks will earn zero and interrupt all remaining tasks
                if not tsk.run(self, girls):
                    self.failed_tasks += 1

            if not self.failed_tasks:
                self.result = "success"
            elif self.failed_tasks < len(self.tasks):
                self.result = "partial"
            else:
                self.result = "failure"

            game.set_task(None, "contract") # Clears contract from goal tooltip

            return


    class ContractTask(object):

        def __init__(self, name, type, requirements, tags, and_tags=None, and_tags2=None, soft=True): # and_tags2 is only used for 'fun' tasks.
            self.name = name # This is the handle used in the contract_task dictionary
            self.type = type # This is the category used to display the task name on the contract description, as well as generating the task intro text
            self.title = contract_task_types_description[self.type]
            self.base_requirements = requirements # List of possible requirements for this task (2 will be selected randomly). May start with 'job ', 'skill ' or 'pref ', followed by the stat name
            self.tags = make_list(tags) # These define the tags used for the task event
            if and_tags == None: and_tags = []
            self.and_tags = make_list(and_tags)
            if and_tags2 == None: and_tags2 = []
            self.and_tags2 = make_list(and_tags2)
            self.soft = soft # This activates/deactivates the soft filter. Special case: use of "naked"

        def get_pic(self, girl, and_tags=None): # and-tags overrides self.and_tags
            if self.soft:
                soft = True
                if self.soft == "naked":
                    naked_filter=False
                else:
                    naked_filter=True
            else:
                soft = False
                naked_filter=False

            if not and_tags:
                and_tags = self.and_tags

            not_tags = []

            for tag_list in self.tags + and_tags:
                if "group" in tag_list:
                    break
            else:
                not_tags.append("group")

            for tag_list in self.tags + and_tags:
                if "bisexual" in tag_list:
                    break
            else:
                not_tags.append("bisexual")

            if len(self.tags) == 4:
                return girl.get_pic(self.tags[0], self.tags[1], self.tags[2], self.tags[3], and_tags=and_tags, not_tags=not_tags, soft=soft, naked_filter=naked_filter, hide_farm=True)
            elif len(self.tags) == 3:
                return girl.get_pic(self.tags[0], self.tags[1], self.tags[2], and_tags=and_tags, not_tags=not_tags, soft=soft, naked_filter=naked_filter, hide_farm=True)
            elif len(self.tags) == 2:
                return girl.get_pic(self.tags[0], self.tags[1], and_tags=and_tags, not_tags=not_tags, soft=soft, naked_filter=naked_filter, hide_farm=True)
            elif len(self.tags) == 1:
                return girl.get_pic(self.tags[0], and_tags=and_tags, not_tags=not_tags, soft=soft, naked_filter=naked_filter, hide_farm=True)

        def randomize(self, contract, diff): # Sets limits and base gold value for the task

            self.value = round_int(contract.base_value * (0.9 + renpy.random.random()*0.2)) # +/-10% price variation
            self.result = False
            self.requirements = rand_choice(self.base_requirements, 2)
            self.limits = {}

            for req in self.requirements:
                if req.startswith("job"): # Easy is one job level under current maximum. Hard is current maximum
#                     name = req[4:]
                    if diff == "easy":
                        self.limits[req] = district.rank -1
                    else:
                        self.limits[req] = district.rank

                    if self.limits[req] <= 0: # Sanity check
                        raise AssertionError("Contract requirement out of bounds: %s (current district: %s)" % (self.limits[req], district.rank))

                elif req.startswith("skill"): # Base skill limit is determined by game chapter and diff, +/- 15, with a -20 modifier then -10 for the first and second contract of each chapter.
                    mod = dice(31)-16
                    self.value += mod * game.chapter + brothel.contract_modifier
                    self.limits[req] = contract_skill_limit[game.chapter][diff] + mod

                elif req.startswith("pref"):
                    self.limits[req] = contract_sex_limit[game.chapter][diff]

            if diff == "easy":
                self.value *= 2 * game.get_diff_setting("rewards")
            elif diff == "hard":
                self.value *= 3 * game.get_diff_setting("rewards")


        def get_requirements(self):

            r = []

            for req in self.requirements:
                if req.startswith("job"):
                    r.append(__("{b}%s{/b} %s or better") % (__(req[4:].capitalize()), "{image=img_star}" * self.limits[req]))
                elif req.startswith("skill"):
                    r.append(__("{b}%s %s{/b} or better") % (stat_name_dict[req[6:].capitalize()], str(self.limits[req])))
                elif req.startswith("pref"):
                    r.append(__("{b}%s preference: %s{/b} or better") % (__(req[5:].capitalize()), __(self.limits[req].capitalize())))

            return r

        def run(self, contract, girls):

            if contract.failed_tasks > 0: # Failed tasks will earn zero
                self.value = 0
                return False

            bonus = 0.0

            for girl in girls:
                for req in self.requirements:
                    target = self.limits[req]

                    if req.startswith("job"):
                        name = req[4:]
                        if girl.job_level[name] < target:
                            self.value = 0
                            return False
                        elif girl.job_level[name] > target: # bonus = 50% if job level above target
                            bonus += 0.5

                    elif req.startswith("skill"):
                        name = req[6:]
                        if girl.get_stat(name) < target:
                            # raise AssertionError, name + " is " + str(girl.get_stat(name)) + "vs target " + str(target)
                            self.value = 0
                            return False
                        else: # Bonus = 1% for each point of difference in stat value
                            bonus += (girl.get_stat(name) - target) / 100.0

                    elif req.startswith("pref"):
                        name = req[5:]
                        if not compare_preference(girl, name, target):
                            self.value = 0
                            return False
                        else: # Bonus = 1% for each point of difference in preference value
                            bonus += (girl.preferences[name] - get_preference_limit(name, target)) / 100.0

            if bonus > 1.0: # Bonus is capped
                bonus = 1.0

            self.result = True
            self.value += contract.base_value * bonus
            if brothel.contract_modifier < 0: # The first and second successful contracts for each chapter are easier for stat requirements, then revert to mean.
                brothel.contract_modifier += 10

            return True


    ### Used for brothel ranking ###
    class EnemyBrothel(object):

        def __init__(self, chapter=1, level=1, special=False):

            self.name = self.generate_name()
            self.pic = self.generate_image()
            self.base_income = self.get_base_income(chapter, level)
            self.randomize_income()

        def randomize_income(self):
            try:
                self.old_income = self.income
                self.income = self.get_rand_income()
            except:
                self.old_income = self.income = self.get_rand_income()
            
            return self.income
        
        def generate_name(self):
            ## EN: Uses global name pools loaded from JSON (BK Evolution).
            ## ZH: 使用从 JSON 加载的全局词库（BK Evolution）。
            d = dice(10)

            if d <=2:
                name = rand_choice(_bn_first) + " " + rand_choice(_bn_second).capitalize() + " " + rand_choice(_bn_third).capitalize()
            elif d <= 3:
                name = rand_choice(_bn_second).capitalize() + " " + rand_choice(_bn_third).capitalize()
            elif d <= 4:
                name = rand_choice(_bn_second).capitalize() + " " + rand_choice(_bn_names).capitalize() + "'s"
            elif d <= 5:
                name = rand_choice(_bn_names).capitalize() + rand_choice(_bn_fourth)
            else:
                name = rand_choice(_bn_second).capitalize() + " " + rand_choice(_bn_third).capitalize() + rand_choice(_bn_fourth)

            return name

        def generate_image(self):
            return rand_choice([img for img in (game_image_dict["Backgrounds"]["inside"] + game_image_dict["Backgrounds"]["outside"]) if img])

        def get_pic(self):
            return self.pic

        def get_base_income(self, chapter, level):
            pace = {1: 25, 2: 50, 3: 100, 4: 200, 5: 325, 6: 500, 7: 1000}
            v = 225
            p = 0

            for i in range(chapter):
                if i+1 == chapter:
                    rng = level
                else:
                    rng = 5

                for _ in range(rng):
                    p += pace[i+1]
                    v += p

            # Make it monthly
            return v*28

        def get_rand_income(self):

            inc = self.base_income

            # Inflates with time pressure modifier
            inc *= (1+NPC_taxgirl.time_pressure_modifier)

            # Takes Moon effects into account
            inc *= moons[calendar.month].get_effect("boost", "income")

            # Randomize by +/- 10%
            inc *= (0.9 + renpy.random.random()*0.2)

            return inc

        def get_income(self, old=False):
            if old:
                return self.old_income
            return self.income


    class NGPSetting(object):

        """A class holding a single NGP setting."""

        def __init__(self, name, type, label=None, values=None, cost=0, ttip=""):
            self.name = name
            self.type = type
            self.label = label or name.capitalize() # The label used in the NG+ menu
            self.costs = make_list(cost)

            # Manual value setting
            if values:
                if type == "gold" or self.name == "starting chapter": # gold option works differently because it is not a finite list
                    self.values = values
                else: # settings with finite lists add 'option 0' at the beginning to represent deactivated status
                    self.values = [0] + values

            # Automatic value setting
            elif self.type == "bool":
                self.values = [0, 1]
            elif self.type == "dispenser":
                self.values = [None, "once", "monthly", "weekly"]
            else: # As many ranks as are provided for the cost
                self.values = range(0, len(self.costs)+1)

            try:
                self.index = persistent.NGPsettings[name]
            except:
                self.index = persistent.NGPsettings[name] = 0

            self.ttip = ttip

        def get(self):
            if self.type == "gold": # gold is a multiple of 100g
                return (self.index*100)

            return self.values[self.index]

        def read(self): # Apply display format to 'get' value. # Types: gold, resources, int, bool, plus, boost, dispenser, item, pref, girl
            if self.type == "gold":
                return '{:,}'.format(starting_gold + self.get())
            elif self.type == "int":
                return '{:,}'.format(self.get())
            elif self.type == "bool":
                return {0: "Off", 1: "On"}[self.index]
            elif self.type in ("item", "resources"):
                return {0: "None", 1: "Basic", 2: "Advanced", 3: "Master"}[self.index]
            elif self.type == "plus":
                return "+%i" % self.get()
            elif self.type in ("boost", "pref"):
                return {0: "None", 1: "Moderate", 2: "Strong", 3: "Strongest"}[self.index]
            elif self.type == "girl rank":
                return {0: "None", 2: "B rank", 3: "A rank", 4: "S rank"}[self.get()]
            return str(self.get()).capitalize()

        def get_used(self):
            if self.type == "gold":
                s = 0
                for i in range(self.index):
                    s+= self.get_cost(-i-1)
                return s
            return sum(self.costs[:self.index])

        def can_raise(self, budget):
            if self.index >= len(self.values)-1 and self.type != "gold":
                return False
            elif debug_mode:
                return True
            elif self.get_cost() > budget:
                return False
            elif self.type == "gold": # No ceiling for gold
                return True
            return True

        def _raise(self):
            if self.index < len(self.values)-1 or self.type == "gold":
                self.index += 1

        def can_lower(self):
            if self.index == 0:
                return False
            return True

        def _lower(self):
            if self.index > 0:
                self.index -= 1

        def reset(self):
            self.index = 0
            self.record()

        def get_cost(self, mod=0): # self.costs[i] is the cost to raise to level i+1
            level = self.index + mod

            if debug_mode:
                return 0
            elif self.type == "gold": # values for gold are tresholds
                for i in range(len(self.values)):
                    if self.index+mod < self.values[i]:
                        return self.costs[i]
            elif self.index+mod < len(self.values)-1:
                return self.costs[self.index+mod]
            return 0

        def get_refund(self):
            if self.index > 0:
                return self.get_cost(-1)
            return 0

        def get_ttip(self, context = "base"): # type can be "base", "plus" or "minus"
            if context == "base":
                if self.type == "resources" and self.index > 0:
                    return self.ttip + " " + __("Will receive %s.") % and_text([__("+%i of each rank %i resource") % (self.values[i+1], i+1) for i in range(self.index)])
                elif context == "girl" and self.index > 0:
                    return self.ttip + " " + __("A Rank %i girl will join your brothel on Day 1.") % self.get()
                return self.ttip

            elif context == "plus":
                if self.type == "bool":
                    return "Activate " + self.name + " for {image=tb crystal} %i."
                elif self.type == "boost":
                    return "Boost " + self.name + " for {image=tb crystal} %i."
                elif self.type == "dispenser":
                    return "Increase rate of production of this item for {image=tb crystal} %i."
                elif self.type == "item":
                    if self.get():
                        return "Increase your magic notebook's capacities for {image=tb crystal} %i (full information)."
                    else:
                        return "Increase your magic notebook's capacities for {image=tb crystal} %i (partial information)."
                elif self.type == "pref":
                    return "Increase base sexual preferences for all girls for {image=tb crystal} %i."
                else:
                    return "Increase " + self.name + " for {image=tb crystal} %i."

            elif context == "minus":
                if self.type == "bool":
                    return "Deactivate " + self.name + " and refund {image=tb crystal} %i."
                elif self.type == "boost":
                    return "Reduce " + self.name + " boost and refund {image=tb crystal} %i."
                elif self.type == "dispenser":
                    return "Decrease rate of production of this item and refund {image=tb crystal} %i."
                elif self.type == "item":
                    if (self.get()-1):
                        return "Decrease your magic notebook's capacities and refund {image=tb crystal} %i (partial information)."
                    else:
                        return "Decrease your magic notebook's capacities and refund {image=tb crystal} %i (no information)."
                elif self.type == "pref":
                    return "Decrease base sexual preferences for all girls and refund {image=tb crystal} %i."
                else:
                    return "Decrease " + self.name + " and refund {image=tb crystal} %i."

        def record(self):
            persistent.NGPsettings[self.name] = self.index

        def recall(self):
            self.index = persistent.NGPsettings[self.name]

        @classmethod
        def from_dict(cls, d):
            """EN: Build an NGPSetting from a JSON dict.
               ZH: 从 JSON 字典构建 NG+ 设置。"""
            return cls(
                name=d.get("name", ""),
                type=d.get("type", "int"),
                label=get_i18n(d, "label"),
                values=d.get("values"),
                cost=d.get("cost", 0),
                ttip=get_i18n(d, "ttip", ""),
            )

        def to_dict(self):
            """EN: Serialize this NG+ setting to a JSON-compatible dict.
               ZH: 将此 NG+ 设置序列化为兼容 JSON 的字典。"""
            return {
                "name": self.name,
                "type": self.type,
                "label_i18n": self.label,
                "values": list(self.values) if hasattr(self.values, "__iter__") and not isinstance(self.values, (str, bytes, dict)) else self.values,
                "cost": list(self.costs) if isinstance(self.costs, (list, tuple)) else self.costs,
                "ttip_i18n": self.ttip,
            }

    class MetaUpgrade(object):
        """
        EN: A permanent cross-run meta-upgrade (e.g. crystal cap, starting bonuses).
        ZH: 跨周目的永久局外养成升级（例如水晶上限、起始加成）。
        """

        def __init__(self, upgrade_id, name_i18n, description_i18n, max_rank=1,
                     cost_per_rank=None, effects=None, unlock_condition="newgame+"):
            self.upgrade_id = upgrade_id
            self.name_i18n = name_i18n
            self.description_i18n = description_i18n
            self.max_rank = max_rank
            self.cost_per_rank = make_list(cost_per_rank) if cost_per_rank else []
            self.effects = make_list(effects, Effect)
            _builtin_dict = __import__('builtins').dict
            self.effects = [Effect.from_dict(e) if isinstance(e, _builtin_dict) else e for e in self.effects]
            self.unlock_condition = unlock_condition

            try:
                self.rank = persistent.meta_upgrades.get(self.upgrade_id, 0)
            except Exception:
                self.rank = 0
                if not persistent.meta_upgrades:
                    persistent.meta_upgrades = {}
                persistent.meta_upgrades[self.upgrade_id] = 0

        def get_name(self):
            return __(self.name_i18n)

        def get_description(self):
            return __(self.description_i18n)

        def get_cost_for_rank(self, rank):
            if 0 <= rank - 1 < len(self.cost_per_rank):
                return self.cost_per_rank[rank - 1]
            return 0

        def can_rank_up(self, budget):
            return self.rank < self.max_rank and budget >= self.get_cost_for_rank(self.rank + 1)

        def rank_up(self):
            if self.rank < self.max_rank:
                self.rank += 1
                persistent.meta_upgrades[self.upgrade_id] = self.rank

        @classmethod
        def from_dict(cls, d):
            effects = d.get("effects", [])
            if effects:
                _builtin_dict = __import__('builtins').dict
                effects = [Effect.from_dict(e) if isinstance(e, _builtin_dict) else e for e in effects]
            _uid = d.get("upgrade_id") or d.get("id")
            return cls(
                upgrade_id=_uid,
                name_i18n=d.get("name_i18n", _uid or ""),
                description_i18n=d.get("description_i18n", ""),
                max_rank=d.get("max_rank", 1),
                cost_per_rank=d.get("cost_per_rank", []),
                effects=effects,
                unlock_condition=d.get("unlock_condition", "newgame+"),
            )

        def to_dict(self):
            """EN: Serialize this meta upgrade to a JSON-compatible dict.
               ZH: 将此局外养成升级序列化为兼容 JSON 的字典。"""
            return {
                "upgrade_id": self.upgrade_id,
                "name_i18n": self.name_i18n,
                "description_i18n": self.description_i18n,
                "max_rank": self.max_rank,
                "cost_per_rank": list(self.cost_per_rank) if isinstance(self.cost_per_rank, (list, tuple)) else self.cost_per_rank,
                "effects": [e.to_dict() for e in self.effects],
                "unlock_condition": self.unlock_condition,
            }

init python:
    ## EN: Load brothel name generation word pools from JSON (BK Evolution), fallback to hardcoded.
    ## ZH: 从 JSON 加载青楼名称生成词库（BK Evolution），否则使用硬编码。
    _bnp_json = DataLoader.load_brothel_name_pools()
    if _bnp_json:
        _bn_first = tuple(_bnp_json.get("first", []))
        _bn_second = tuple([__(w) for w in _bnp_json.get("second_i18n", _bnp_json.get("second", []))])
        _bn_third = tuple([__(w) for w in _bnp_json.get("third_i18n", _bnp_json.get("third", []))])
        _bn_names = tuple([__(w) for w in _bnp_json.get("names_i18n", _bnp_json.get("names", []))])
        _bn_fourth = tuple([__(w) for w in _bnp_json.get("fourth_i18n", _bnp_json.get("fourth", []))])
    else:
        _bn_first = ("The", "House of the", "Den of the", "Garden of the")
        _bn_second = ("beautiful", "sleazy", "naughty", "horny", "hungry", "hasty", "mighty", "sweaty", "rowdy", "bawdy", "screwy", "loony", "bloody", "holy", "spicy", "grim", "old", "ol'", "lame", "hunchback", "blind", "rebel", "mysterious", "secret", "rogue", "lurking", "singing", "dancing", "laughing", "limping", "crying", "golden", "silver", "bronze", "copper", "iron", "stone", "ice", "fire", "velvet", "red", "green", "blue", "yellow", "purple", "violet", "white", "black", "light", "dark", "pink", "hot", "cold", "big", "long", "tiny", "fat", "ruby", "emerald", "opal", "Borgese", "Western", "Eastern", "Northern", "Southern", "Zanic")
        _bn_third = ("dragon", "griffin", "pegasus", "unicorn", "basilisk", "hydra", "hippogriff", "horse", "giant", "goliath", "kraken", "goblin", "orc", "gnoll", "hobgoblin", "troll", "mare", "bear", "boar", "cock", "rabbit", "snake", "serpent", "lizard", "dog", "cat", "swan", "falcon", "owl", "snail", "butterfly", "shark", "dolphin", "whale", "mermaid", "bard", "knight", "prince", "princess", "sailor", "priest", "pirate", "corsair", "gentleman", "man", "lady", "madam", "maiden", "belle", "star", "glove", "hat", "eye", "hand")
        _bn_names = ("Joe", "Mary", "Bill", "Sam", "Wendy", "Zora", "Zelda", "Sara", "Mila", "Estrella", "Lee", "Weng", "Dong", "Fang", "Chan", "Chen", "Mathilda", "Jon", "Dick")
        _bn_fourth = ("'s inn", "'s tavern", "'s club", "'s lair", "'s den", "'s World", "'s parlor", "'s place", "'s emporium", " Villa", " Palazzo", " of Sin", " of Pleasure", " of Redemption", " of Damnation", " of Lust", " of Westmarch", " of Karkyr")

