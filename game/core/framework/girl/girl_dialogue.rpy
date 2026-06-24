#### GirlDialogue — Dialogue, personality, background component ####
# Phase 2.1: Dialogue selection, say(), personality generation, background.
# Methods to migrate: generate_personality, adjust_personality, generate_background,
# unlock_NGP_personality_settings, get_personality_description, talk_tastes,
# pick_dialogue, say, rand_say, test_say, will_remember, remembers, forgets.

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
        # ── Dialogue methods (implementations moved from girlclass.rpy) ──
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
