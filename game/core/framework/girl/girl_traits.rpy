#### GirlTraits — Trait and perk management component ####
# Phase 2.1: Traits, perks, archetypes, combo checks.
# Methods to migrate: generate_traits, has_trait, has_perk, add_trait,
# remove_trait, can_acquire_perk, update_can_perk, acquire_perk,
# refund_perks, check_combo_perks, has_prerequisites, get_perk, get_perk_level.

init -2 python:

    class GirlTraits(object):
        """Trait and perk management for a Girl."""

        def __init__(self, girl):
            self.girl = girl
