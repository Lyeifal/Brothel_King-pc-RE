#### GirlDialogue — Dialogue, personality, background | 对话、个性、背景 ####
# Phase 2.1: Dialogue selection, say(), personality generation, background.
# 对话选择、说话、个性生成、背景故事
# ★ pick_dialogue / say / rand_say — 已从 girlclass.rpy 移入
# Methods: generate_personality, generate_background, unlock_info,
#          talk_tastes, will_remember, remembers, forgets, test_say.

init -2 python:

    class GirlDialogue(object):
        """Dialogue and personality for a Girl. Delegates to _impl methods."""

        def __init__(self, girl):
            self.girl = girl

        def generate_personality(self, personality=None, change=False):
            return self.girl._generate_personality_impl(personality, change)
        def adjust_personality(self):
            return self.girl._adjust_personality_impl()
        def generate_background(self, t2=0):
            return self.girl._generate_background_impl(t2)
        def unlock_NGP_personality_settings(self):
            return self.girl._unlock_NGP_personality_settings_impl()
        def get_personality_description(self, show="personality"):
            return self.girl._get_personality_description_impl(show)
        def talk_tastes(self, type):
            return self.girl._talk_tastes_impl(type)
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
            return self.girl._test_say_impl()
        def will_remember(self, context, type, score):
            return self.girl._will_remember_impl(context, type, score)
        def remembers(self, context, type):
            return self.girl._remembers_impl(context, type)
        def forgets(self):
            return self.girl._forgets_impl()
        def unlock_info(self, topic):
            return self.girl._unlock_info_impl(topic)
