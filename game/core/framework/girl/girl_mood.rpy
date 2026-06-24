#### GirlMood — Mood, sanity, energy, health component ####
# Phase 2.1: Mood, sanity, energy, health, exhaustion, hurt.
# Methods to migrate: init_sanity, rank_up_sanity, lose_sanity, get_sanity,
# sanity_warning, change_energy, tire, get_hurt, health_check, heal, full_rest,
# rest, get_energy_color, get_energy_ttip, update_mood, change_mood,
# get_mood_modifier, get_mood_description, get_mood_picture,
# build_up, get_build_up, reset_build_up.

init -2 python:

    class GirlMood(object):
        """Mood, sanity, and energy management for a Girl."""

        def __init__(self, girl):
            self.girl = girl
