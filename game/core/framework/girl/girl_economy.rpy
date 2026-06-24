#### GirlEconomy — Economic calculations component ####
# Phase 2.1: Prices, upkeep, tips, customer capacity, performance estimation.
# Methods to migrate: get_price, get_med_upkeep, adjust_upkeep, update_upkeep_ratio,
# get_upkeep_threshold, get_upkeep_modifier, get_next_upkeep_step, get_previous_upkeep_step,
# get_max_cust_served, get_max_interactions, get_interaction_modifer, reset_interactions,
# estimate_performance, get_xp, get_jp, get_rep, get_tip, get_street_tip, whore_on_street,
# cut_upkeep, restore_upkeep, customer_populations_safety_check, change_rep.

init -2 python:

    class GirlEconomy(object):
        """Economic calculations for a Girl."""

        def __init__(self, girl):
            self.girl = girl
