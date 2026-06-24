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
        def pick_dialogue(self, topic):
            return self.girl._pick_dialogue_impl(topic)
        def say(self, topic, custom_label=True, custom_arg=False, nw=False, narrator_mode=False):
            return self.girl._say_impl(topic, custom_label, custom_arg, nw, narrator_mode)
        def rand_say(self, *dialogue_options):
            return self.girl._rand_say_impl(*dialogue_options)
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
