#### GirlDialogue — Dialogue, personality, background component ####
# Phase 2.1: Dialogue selection, say(), personality generation, background.
# Methods to migrate: generate_personality, adjust_personality, generate_background,
# unlock_NGP_personality_settings, get_personality_description, talk_tastes,
# pick_dialogue, say, rand_say, test_say, will_remember, remembers, forgets.

init -2 python:

    class GirlDialogue(object):
        """Dialogue and personality for a Girl."""

        def __init__(self, girl):
            self.girl = girl
