#### GirlDialogue — Dialogue, personality, background | 对话、个性、背景 ####
# Phase 2.1: Dialogue selection, say(), personality generation, background.
# 对话选择、说话、个性生成、背景故事
# ★ pick_dialogue / say / rand_say — 已从 girlclass.rpy 移入
# ★ get_personality_description / unlock_NGP_personality_settings / test_say / unlock_info / is_ — 已从 girlclass.rpy 移入 (Phase 7 批次3)
# 注: will_remember/remembers/forgets 已改属 GirlLogging (Phase 7 批次2)
# Methods: generate_personality, adjust_personality, generate_background,
#          unlock_NGP_personality_settings, get_personality_description, is_,
#          talk_tastes, test_say, unlock_info.

init -2 python:

    class GirlDialogue(object):
        """Dialogue, personality and background for a Girl."""

        def __init__(self, girl):
            self.girl = girl

        def generate_personality(self, personality=None, change=False):
            return self.girl._generate_personality_impl(personality, change)
        def adjust_personality(self):
            return self.girl._adjust_personality_impl()
        def generate_background(self, t2=0):
            return self.girl._generate_background_impl(t2)
        def unlock_NGP_personality_settings(self):
            g = self.girl
            # NewGame+ additional info

            if NGP_settings_dict["personality"].get() == 2:
                g.notebook_unlocks += ["EI", "MI", "LM", "DS"]

            elif NGP_settings_dict["personality"].get() == 1:
                g.notebook_unlocks += rand_choice(["EI", "MI", "LM", "DS"], 2)

            if NGP_settings_dict["taste"].get() == 2:
                g.notebook_unlocks += ["fav_color", "fav_food", "fav_drink", "dis_color", "dis_food", "dis_drink", "loves", "likes", "hates"]
                g.personality_unlock["loves"] = [k for k, v in g.personality.gift_likes.items() if v >= 3]
                g.personality_unlock["likes"] = [k for k, v in g.personality.gift_likes.items() if 3 > v >= 0]
                g.personality_unlock["hates"] = [k for k, v in g.personality.gift_likes.items() if v <= -2]

            elif NGP_settings_dict["taste"].get() == 1:
                g.notebook_unlocks += ["fav_color", "fav_food", "fav_drink", "dis_color", "dis_food", "dis_drink"]
            # /NewGame+

        def get_personality_description(self, show="personality"):
            g = self.girl
            des = "{b}" + g.fullname + "'s "

            if show == "personality":
                des += "personality{/b}{size=-1}\n\n"

                # Update notebook

                for att in [a for a in ("EI", "MI", "LM", "DS") if a not in g.notebook_unlocks]:
                    if g.personality_unlock[att] >= 100 or always_show_personality[g]:
                        g.unlock_info(att)

                for info in [i for i in ("origin", "fav_color", "fav_food", "fav_drink", "hobby_" + g.hobbies[0], "hobby_" + g.hobbies[1], "dis_color", "dis_food", "dis_drink", "loves", "likes", "hates") if i not in g.notebook_unlocks]:
                    if g.personality_unlock[info] or always_show_personality[g]:
                        g.unlock_info(info)

                for act in [a for a in extended_sex_acts if a not in g.notebook_unlocks]:
                    if g.personality_unlock[act] or always_show_personality[g] or NGP_settings_dict["fixation"].get():
                        g.unlock_info(act)

                for fix in [f for f in (g.pos_fixations + g.neg_fixations) if f not in g.notebook_unlocks]:
                    if g.personality_unlock[fix.name] or always_show_personality[g] or NGP_settings_dict["fixation"].get() == 2:
                        g.unlock_info(fix.name)


                # Background

                background_des = g.name + __(" is a ")

                if g.free and g in MC.girls + farm.girls:
                    background_des += __("former free girl")
                elif g.free:
                    background_des += __("free girl")
                else:
                    background_des += __("slave")

                if "origin" in g.notebook_unlocks:
                    background_des += __(" from ") + g.origin

                background_des += ". "

                if g.flags["story"] < 10:
                    background_des += __("You do not know her story.")
                elif g.flags["story"] < 20:
                    background_des += __("You know a few things about her story.")
                elif g.flags["story"] < 50:
                    background_des += __("You know some things about her story.")
                elif g.flags["story"] < 100:
                    background_des += __("She has told you her story, but you haven't done anything about it yet.")
                elif g.flags["MC refused story"]:
                    background_des += __("You know about her story.")
                else:
                    background_des += __("You know about her story, and did something about it.")

                background_des += "\n\n"

                des += background_des

                # Personality

                pers_des = ""

                if "EI" in g.notebook_unlocks and "MI" in g.notebook_unlocks and "DS" in g.notebook_unlocks and "LM" in g.notebook_unlocks:
                    pers_des += g.personality.description + "\n\n"

                if "EI" in g.notebook_unlocks:
                    if g.is_("very extravert"):
                        pers_des += "She is very {b}lively and outgoing{/b}.\n"
                    elif g.is_("extravert"):
                        pers_des += "She is quite {b}sociable{/b}.\n"
                    elif g.is_("very introvert"):
                        pers_des += "She is {b}quiet and very shy{/b}.\n"
                    elif g.is_("introvert"):
                        pers_des += "She is {b}a little shy{/b}.\n"

                if "MI" in g.notebook_unlocks:
                    if g.is_("very materialist"):
                        pers_des += "She is very {b}selfish and greedy{/b}, ready to crush people if they get in her way.\n"
                    elif g.is_("materialist"):
                        pers_des += "She is quite {b}shallow and materialistic{/b}.\n"
                    elif g.is_("very idealist"):
                        pers_des += "She is a {b}dreamer{/b}, wanting to make the world a better place.\n"
                    elif g.is_("idealist"):
                        pers_des += "She {b}cares about others{/b}.\n"

                if "DS" in g.notebook_unlocks:
                    if g.is_("very dom"):
                        pers_des += "She is {b}aggressive, strong-headed{/b} and wants others to see things her way.\n"
                    elif g.is_("dom"):
                        pers_des += "She knows what she wants, and she likes to be {b}independent{/b}.\n"
                    elif g.is_("very sub"):
                        pers_des += "She is {b}very submissive{/b} and always puts herself last.\n"
                    elif g.is_("sub"):
                        pers_des += "She is {b}rather submissive{/b}, avoiding conflict whenever possible.\n"

                if "LM" in g.notebook_unlocks:
                    if g.is_("very modest"):
                        pers_des += "She has strong moral views and is {b}repressed{/b} about sex.\n"
                    elif g.is_("modest"):
                        pers_des += "She follows her own {b}code of ethics{/b}, frowning upon lewd behavior.\n"
                    elif g.is_("very lewd"):
                        pers_des += "She only cares about {b}her own pleasure{/b}, not giving a damn about morality.\n"
                    elif g.is_("lewd"):
                        pers_des += "She's {b}open-minded and relaxed{/b} about morals.\n"

                if not pers_des:
                    pers_des += "You don't know her personality very well."

                des += pers_des

            # Tastes

            elif show == "tastes":

                des += "tastes{/b}{size=-1}\n\n"

                taste_text = ""

                if "fav_color" in g.notebook_unlocks:
                    taste_text += "Her favourite color is {b}" + g.likes["color"] + "{/b}. "

                if "fav_food" in g.notebook_unlocks:
                    taste_text += "Her favourite food is {b}" + g.likes["food"] + "{/b}. "

                if "fav_drink" in g.notebook_unlocks:
                    taste_text += "Her favourite drink is {b}" + g.likes["drink"] + "{/b}. "

                if ("hobby_" + g.hobbies[0]) in g.notebook_unlocks and ("hobby_" + g.hobbies[1]) in g.notebook_unlocks:
                    taste_text += "She likes {b}" + g.hobbies[0] + " and " + g.hobbies[1] + "{/b}. "

                elif ("hobby_" + g.hobbies[0]) in g.notebook_unlocks:
                    taste_text += "She likes {b}" + g.hobbies[0] + "{/b}. "

                elif ("hobby_" + g.hobbies[1]) in g.notebook_unlocks:
                    taste_text += "She likes {b}" + g.hobbies[1] + "{/b}. "

                if taste_text:
                    taste_text += "\n\n"

                if "dis_color" in g.notebook_unlocks:
                    taste_text += "Her least favourite color is {b}" + g.dislikes["color"] + "{/b}. "

                if "dis_food" in g.notebook_unlocks:
                    taste_text += "Her least favourite food is {b}" + g.dislikes["food"] + "{/b}. "

                if "dis_drink" in g.notebook_unlocks:
                    taste_text += "Her least favourite drink is {b}" + g.dislikes["drink"] + "{/b}. "


                if taste_text:
                    taste_text += "\n\n"

                if "loves" in g.notebook_unlocks and g.personality_unlock["loves"]:
                    taste_text += "She loves {color=[c_emerald]}" + and_text([gift_description[luv] for luv in g.personality_unlock["loves"]]) + "{/color}. "
                    prior = "also "
                    prior2 = "However, she "

                else:
                    prior = ""
                    prior2 = "She "

                if "likes" in g.notebook_unlocks and g.personality_unlock["likes"]:
                    taste_text += "She " + prior + "likes {color=[c_orange]}" + and_text([gift_description[lik] for lik in g.personality_unlock["likes"]]) + "{/color}. "
                    prior2 = "However, she "

                if "hates" in g.notebook_unlocks and g.personality_unlock["hates"]:
                    taste_text += prior2 + "hates {color=[c_crimson]}" + and_text([gift_description[hat] for hat in g.personality_unlock["hates"]]) + "{/color}. "

                if taste_text:
                    des += taste_text
                else:
                    des += __("You don't know anything about her tastes.")

            elif show == "sexual":

                des += "sexuality{/b}\n\n"

                sex_text = ""

                pos_unlocked = []
                amb_unlocked = []
                neg_unlocked = []

                for act in g.pos_acts:
                    if act in g.notebook_unlocks:
                        if act in g.neg_acts: # Ambivalent acts
                            amb_unlocked.append(act)
                        else:
                            pos_unlocked.append(act)

                for act in g.neg_acts:
                    if act in g.notebook_unlocks and act not in g.pos_acts:
                        neg_unlocked.append(act)

                if pos_unlocked:
                    sex_text += "She has a weakness for {color=[c_emerald]}" + and_text(pos_unlocked) + "{/color} acts"

                    if neg_unlocked:
                        sex_text += ", but she "
                    else:
                        sex_text += ". "

                if neg_unlocked:
                    if not sex_text:
                        sex_text += "She "
                    sex_text += "dislikes {color=[c_crimson]}" + and_text(neg_unlocked) + "{/color} acts. "

                if amb_unlocked:
                    sex_text += "She is ambivalent towards {color=[c_yellow]}" + and_text(amb_unlocked) + "{/color} acts. "

                if sex_text:
                    sex_text += "\n\n"

                pos_fix = [fix.name for fix in g.pos_fixations if fix.name in g.notebook_unlocks]
                neg_fix = [fix.name for fix in g.neg_fixations if fix.name in g.notebook_unlocks]

                if pos_fix:
                    sex_text += "She is especially fascinated by {color=[c_emerald]}" + and_text(pos_fix) + "{/color}. "
                if neg_fix:
                    sex_text += "She is disgusted by {color=[c_crimson]}" + and_text(neg_fix) + "{/color}. "

                if sex_text:
                    des += sex_text
                else:
                    des += "You do not know her sexual tastes very well."

                if farm.knows["weakness"][g]:
                    des+= _("\nShe is vulnerable to farm %ss.") % g.weakness

            elif show == "recent":

                if g.free:
                    day_number = 84
                else:
                    day_number = 7

                des += "recent events{/b}\n\n" + g.get_recent_events_description(day_number) + ""

            return des

        def is_(self, attributes, type="and"): # Checks if the girl has one or several attributes. Note: A girl with 'very X' will also be 'X'.
            g = self.girl
            attributes = make_list(attributes)

            if type == "and":
                for a in attributes:
                    if not a in g.attributes: # or "very " + a in g.attributes):
                        return False
                return True

            elif type == "or":
                for a in attributes:
                    if a in g.attributes: # or "very " + a in g.attributes:
                        return True
                return False

        def talk_tastes(self, type):
            return self.girl.talk_tastes(type)
        # ── 个性生成 | Personality generation ──

        def generate_personality(self, personality=None, change=False):
            '''生成女孩个性 | Generate girl's personality'''
            g = self.girl
            if use_ini_personality and g.init_dict["custom personality/custom_personality"] and not change:
                g.personality = Personality(
                    name=g.init_dict["custom personality/personality_name"],
                    attributes=g.init_dict["custom personality/attributes"],
                    personality_dialogue_only=g.init_dict["custom personality/personality_dialogue_only"],
                    dialogue_personality_weight=g.init_dict["custom personality/dialogue_personality_weight"],
                    dialogue_attribute_weight=g.init_dict["custom personality/dialogue_attribute_weight"],
                    description=g.init_dict["custom personality/description"],
                )
            elif use_ini_personality and g.init_dict["base personality/always"] and not change:
                g.personality = gpersonalities[rand_choice(g.init_dict["base personality/always"])]
            elif personality and (personality not in g.init_dict["base personality/never"] or not use_ini_personality):
                g.personality = gpersonalities[personality]
            else:
                personalities = []
                for pers in gpersonalities.values():
                    if pers in g.init_dict["base personality/never"] or (change and g.personality == pers):
                        pass
                    elif pers in g.init_dict["base personality/often"]:
                        personalities.append((pers, 4))
                    elif pers in g.init_dict["base personality/rarely"]:
                        personalities.append((pers, 1))
                    else:
                        personalities.append((pers, 2))
                g.personality = weighted_choice(personalities)

            if use_ini_personality and g.init_dict["custom personality/custom_dialogue_label"]:
                g.custom_dialogue_label = g.init_dict["custom personality/custom_dialogue_label"]
            g.attributes = g.personality.generate_attributes(g)
            g.gift_likes = g.personality.gift_likes

        def adjust_personality(self):
            '''检查并调整个性 | Check and adjust personality if attributes changed'''
            g = self.girl
            adjust = False
            for attr in g.personality.attributes:
                if attr.startswith("very"):
                    if not g.is_(attr[5:]): adjust = True; break
                elif not g.is_(attr): adjust = True; break
            if adjust:
                new_pers = None
                best_score = 0
                for pers in random.sample(gpersonalities, len(gpersonalities)):
                    score = sum(3 if g.is_(attr) else 1 if g.is_(attr[5:]) else 0 for attr in pers.attributes)
                    if score > best_score:
                        new_pers = pers; best_score = score
                g.personality = new_pers
                g.gift_likes = g.personality.gift_likes

        def generate_background(self, t2=0):
            '''生成女孩背景故事 | Generate girl's background story'''
            g = self.girl
            if g.init_dict["tastes/hobbies"]:
                g.hobbies = g.init_dict["tastes/hobbies"]
            else:
                g.hobbies = rand_choice(hobbies, 2)

            if g.init_dict["background story/origin"] and g.init_dict["background story/origin"] != "random":
                g.origin = g.init_dict["background story/origin"]
            else:
                g.origin = rand_choice(origins)

            if g.init_dict["background story/story_label"]:
                g.story = g.init_dict["background story/story_label"]
            else:
                if g.init_dict["background story/always_slave_story"]:
                    g.story = rand_choice(g.init_dict["background story/always_slave_story"])
                else:
                    available_stories = []
                    for story in slave_stories:
                        if story not in (g.init_dict["background story/never_slave_story"] + g.personality.story_dict["never"]):
                            if story in g.init_dict["background story/often_slave_story"]: w = 4
                            elif story in g.init_dict["background story/rarely_slave_story"]: w = 1
                            elif story in g.personality.story_dict["often"]: w = 4
                            elif story in g.personality.story_dict["rarely"]: w = 1
                            else: w = 2
                            available_stories.append((story, w))
                    g.story = weighted_choice(available_stories)

            g.story_profession = rand_choice([pop for pop in all_populations if pop.name != "royals"]).get_rand_name("M")
            g.story_profession_article = article(g.story_profession)
            g.story_home = rand_choice(homes)
            g.story_home_article = article(g.story_home)
            g.story_guardian = rand_choice(guardians)
            g.flags["story"] = 4
            g.personality_unlock = defaultdict(int)
            g.personality_unlock["likes"] = []
            g.personality_unlock["loves"] = []
            g.personality_unlock["hates"] = []

            if g.init_dict["tastes/favorite_color"]: g.likes["color"] = g.init_dict["tastes/favorite_color"]
            else: g.likes["color"] = rand_choice(colors)
            if g.init_dict["tastes/favorite_food"]: g.likes["food"] = g.init_dict["tastes/favorite_food"]
            else: g.likes["food"] = rand_choice(food)
            if g.init_dict["tastes/favorite_drink"]: g.likes["drink"] = g.init_dict["tastes/favorite_drink"]
            else: g.likes["drink"] = rand_choice(drinks)
            if g.init_dict["tastes/disliked_color"]: g.dislikes["color"] = g.init_dict["tastes/disliked_color"]
            else: g.dislikes["color"] = rand_choice(colors)
            if g.init_dict["tastes/disliked_food"]: g.dislikes["food"] = g.init_dict["tastes/disliked_food"]
            else: g.dislikes["food"] = rand_choice(food)
            if g.init_dict["tastes/disliked_drink"]: g.dislikes["drink"] = g.init_dict["tastes/disliked_drink"]
            else: g.dislikes["drink"] = rand_choice(drinks)

            return time.perf_counter()

        # ── 对话方法（已迁移）| Dialogue methods (moved) ──
        def pick_dialogue(self, topic):
            g = self.girl
            if topic in g.personality.personality_dialogue_only:
                if dialogue_dict[topic][g.personality.name]:
                    return get_dialogue(topic, g.personality.name)
                else:
                    return Dialogue(event_color["bad"] % topic + " <PERSONALITY DIALOGUE NOT FOUND: " + g.personality.name + ">")

            available_dialogue = []
            if dialogue_dict[topic][g.personality.name]:
                available_dialogue += [(d, g.personality.dialogue_personality_weight) for d in get_dialogue(topic, g.personality.name)]
            for attr in g.attributes:
                if dialogue_dict[topic][attr]:
                    available_dialogue += [(d, g.personality.dialogue_attribute_weight) for d in get_dialogue(topic, attr)]
            for stat in g.stats + g.sex_stats:
                if dialogue_dict[topic][stat] and g.get_stat(stat) >= 40 * g.rank:
                    available_dialogue += [(d, 1) for d in get_dialogue(topic, stat)]

            if not available_dialogue and dialogue_dict[topic]["generic"]:
                available_dialogue += [(d, 1) for d in get_dialogue(topic, "generic")]

            available_dialogue = [d for d in available_dialogue if d]
            if not available_dialogue:
                return Dialogue(event_color["bad"] % topic + " <DIALOGUE NOT FOUND>")
            return weighted_choice(available_dialogue)

        def say(self, topic, custom_label=True, custom_arg=False, nw=False, narrator_mode=False):
            g = self.girl
            if not hasattr(g, "custom_dialogue_label"):
                g.custom_dialogue_label = None
            if custom_label and g.custom_dialogue_label:
                if renpy.has_label(g.custom_dialogue_label):
                    renpy.call(g.custom_dialogue_label, girl=g, topic=topic)
                    return
                else:
                    renpy.say(__("System"), __("Label: {color=[c_red]}%s{/color} doesn't exist (Custom girl: {color=[c_red]}%s/_BK.ini{/color}).") % (g.custom_dialogue_label, g.path))

            dial = g.pick_dialogue(topic)
            dial.apply_changes(g)
            if narrator_mode:
                dial.say(narrator, custom_arg, nw)
            else:
                dial.say(g.char, custom_arg, nw)

        def rand_say(self, *dialogue_options):
            g = self.girl
            if len(dialogue_options) == 1 and not is_string(dialogue_options):
                sentences = dialogue_options[0]
            dialogue_options = make_list(dialogue_options)
            sentences = []
            for sentence in dialogue_options:
                if sentence.startswith("ex: ") and g.is_("extravert"): sentences.append(sentence[4:])
                elif sentence.startswith("in: ") and g.is_("introvert"): sentences.append(sentence[4:])
                elif sentence.startswith("id: ") and g.is_("idealist"): sentences.append(sentence[4:])
                elif sentence.startswith("ma: ") and g.is_("materialist"): sentences.append(sentence[4:])
                elif sentence.startswith("mo: ") and g.is_("modest"): sentences.append(sentence[4:])
                elif (sentence.startswith("le: ") or sentence.startswith("lw: ")) and g.is_("lewd"): sentences.append(sentence[4:])
                elif sentence.startswith("su: ") and g.is_("sub"): sentences.append(sentence[4:])
                elif sentence.startswith("do: ") and g.is_("dom"): sentences.append(sentence[4:])
                elif sentence.startswith("di: ") and g.is_("diligent"): sentences.append(sentence[4:])
                elif sentence.startswith("la: ") and g.is_("lazy"): sentences.append(sentence[4:])
                elif sentence.startswith("ki: ") and g.is_("kind"): sentences.append(sentence[4:])
                elif sentence.startswith("cr: ") and g.is_("cruel"): sentences.append(sentence[4:])
                elif sentence.startswith("ag: ") and g.is_("aggressive"): sentences.append(sentence[4:])
                elif sentence.startswith("ca: ") and g.is_("calm"): sentences.append(sentence[4:] + ".")
                elif sentence.startswith("st: "): sentences.append(sentence[4:])
            if not sentences:
                sentences = [s for s in dialogue_options if not s.startswith(("ex: ", "in: ", "id: ", "ma: ", "mo: ", "le: ", "lw: ", "su: ", "do: ", "di: ", "la: ", "ki: ", "cr: ", "ag: ", "ca: ", "st: "))]
            return rand_choice(sentences) if sentences else ""
        def test_say(self):
            g = self.girl
            renpy.say(g.char, __("Let's test if say methods break the flow."))
            g.change_love(200)
            renpy.say(g.char, __("Did my love go up? Now it's %s") % g.love)
            g.say("free_ask_out")
            g.change_love(-200)
            renpy.say(g.char, __("Did my love go down now? It's %s") % g.love)
            return

        def unlock_info(self, topic):
            g = self.girl
            if topic not in g.notebook_unlocks:
                g.notebook_unlocks.append(topic)
