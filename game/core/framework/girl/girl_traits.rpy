#### GirlTraits — Trait and perk management component ####
# Phase 2.1: Traits, perks, archetypes, combo checks.
# Methods to migrate: generate_traits, has_trait, has_perk, add_trait,
# remove_trait, can_acquire_perk, update_can_perk, acquire_perk,
# refund_perks, check_combo_perks, has_prerequisites, get_perk, get_perk_level.

init -2 python:

    class GirlTraits(object):
        """Trait and perk management for a Girl. Delegates to _impl methods."""

        def __init__(self, girl):
            self.girl = girl

        def generate_traits(self, p_traits=None, n_trait=None):
            return self.girl._generate_traits_impl(p_traits, n_trait)
        def has_trait(self, name):
            return self.girl._has_trait_impl(name)
        def has_perk(self, name):
            return self.girl._has_perk_impl(name)
        def add_trait(self, trait, _pos=None, forced=False, no_perks=False):
            return self.girl._add_trait_impl(trait, _pos, forced, no_perks)
        def remove_trait(self, trait):
            return self.girl._remove_trait_impl(trait)
        def can_acquire_perk(self, perk, context=None):
            return self.girl._can_acquire_perk_impl(perk, context)
        def update_can_perk(self):
            return self.girl._update_can_perk_impl()
        def acquire_perk(self, perk, forced=False):
            return self.girl._acquire_perk_impl(perk, forced)
        def refund_perks(self, min_level=0):
            return self.girl._refund_perks_impl(min_level)
        def check_combo_perks(self):
            return self.girl._check_combo_perks_impl()
        def has_prerequisites(self, perk):
            return self.girl._has_prerequisites_impl(perk)
        def get_perk(self, perk):
            return self.girl._get_perk_impl(perk)
        def get_perk_level(self, perk):
            return self.girl._get_perk_level_impl(perk)
