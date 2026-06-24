#### GirlMood — Mood, sanity, energy, health component ####
# Phase 2.1: Mood, sanity, energy, health, exhaustion, hurt.
# Methods to migrate: init_sanity, rank_up_sanity, lose_sanity, get_sanity,
# sanity_warning, change_energy, tire, get_hurt, health_check, heal, full_rest,
# rest, get_energy_color, get_energy_ttip, update_mood, change_mood,
# get_mood_modifier, get_mood_description, get_mood_picture,
# build_up, get_build_up, reset_build_up.

init -2 python:

    class GirlMood(object):
        """Mood, sanity, and energy management for a Girl.

        Each method delegates to the Girl's _impl alias, which points to
        the original implementation in girlclass.rpy.
        """

        def __init__(self, girl):
            self.girl = girl

        # ── Sanity ──
        def init_sanity(self):
            return self.girl._init_sanity_impl()
        def rank_up_sanity(self):
            return self.girl._rank_up_sanity_impl()
        def lose_sanity(self, cost):
            return self.girl._lose_sanity_impl(cost)
        def get_sanity(self):
            return self.girl._get_sanity_impl()
        def sanity_warning(self):
            return self.girl._sanity_warning_impl()

        # ── Energy & health ──
        def change_energy(self, x):
            return self.girl._change_energy_impl(x)
        def tire(self, x):
            return self.girl._tire_impl(x)
        def get_hurt(self, x):
            return self.girl._get_hurt_impl(x)
        def health_check(self):
            return self.girl._health_check_impl()
        def heal(self, chg=1, from_item=False):
            return self.girl._heal_impl(chg, from_item)
        def full_rest(self):
            return self.girl._full_rest_impl()
        def rest(self, context=None, mod=1):
            return self.girl._rest_impl(context, mod)
        def can_heal_from_item(self):
            return self.girl._can_heal_from_item_impl()
        def get_energy_color(self):
            return self.girl._get_energy_color_impl()
        def get_energy_ttip(self):
            return self.girl._get_energy_ttip_impl()

        # ── Mood ──
        def update_mood(self, resting=False):
            return self.girl._update_mood_impl(resting)
        def change_mood(self, chg):
            return self.girl._change_mood_impl(chg)
        def get_mood_modifier(self, love_text="", fear_text="", description=False, resting=False):
            return self.girl._get_mood_modifier_impl(love_text, fear_text, description, resting)
        def get_mood_description(self, filter=None):
            return self.girl._get_mood_description_impl(filter)
        def get_mood_picture(self):
            return self.girl._get_mood_picture_impl()

        # ── Farm build-up ──
        def build_up(self, v):
            return self.girl._build_up_impl(v)
        def get_build_up(self):
            return self.girl._get_build_up_impl()
        def reset_build_up(self):
            return self.girl._reset_build_up_impl()
