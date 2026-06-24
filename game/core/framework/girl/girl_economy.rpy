#### GirlEconomy — Economic calculations component ####
# Phase 2.1: Prices, upkeep, tips, customer capacity, performance estimation.
# Methods to migrate: get_price, get_med_upkeep, adjust_upkeep, update_upkeep_ratio,
# get_upkeep_threshold, get_upkeep_modifier, get_next_upkeep_step, get_previous_upkeep_step,
# get_max_cust_served, get_max_interactions, get_interaction_modifer, reset_interactions,
# estimate_performance, get_xp, get_jp, get_rep, get_tip, get_street_tip, whore_on_street,
# cut_upkeep, restore_upkeep, customer_populations_safety_check, change_rep.
#
# Migration: Delegation wrappers added. Implementation bodies remain in girlclass.rpy
# and will be moved incrementally.

init -2 python:

    class GirlEconomy(object):
        """Economic calculations for a Girl.

        Each method delegates to girlclass.rpy implementation via self.girl.
        """

        def __init__(self, girl):
            self.girl = girl

        # ── Price (implementations moved from girlclass.rpy) ──

        def get_price(self, operation, raw=False):
            g = self.girl
            modifier = MC.get_modifier(operation, raw)

            if game.has_active_mod("traitking"):
                traitking_modifier = 1.0
                if not hasattr(g, 'valuation'):
                    g.valuation = 100
                traitking_valuation = g.valuation + g.get_effect("change", "valuation")
                traitking_modifier *= max(10, traitking_valuation) / 100.0
                modifier *= traitking_modifier

            if g.original:
                modifier *= 1.15

            stat_average = sum(s.value for s in g.stats + g.sex_stats) / 12
            baseprice = rank_cost[g.rank] + stat_average * (rank_stat_step[g.rank][0] + rank_stat_step[g.rank][1] * (g.level - (g.rank - 1) * 5))
            pref_boost = 1 + sum((sell_girl_preference_boost * (g.preferences[act] - base_reluctance[act])) for act in g.preferences.keys())
            finalprice = round_int(baseprice * pref_boost * modifier)

            return finalprice

        def get_med_upkeep(self):
            return self.girl._get_med_upkeep_impl()

        def adjust_upkeep(self):
            return self.girl._adjust_upkeep_impl()

        def update_upkeep_ratio(self):
            return self.girl._update_upkeep_ratio_impl()

        def get_upkeep_threshold(self, step):
            return self.girl._get_upkeep_threshold_impl(step)

        def get_upkeep_modifier(self):
            return self.girl._get_upkeep_modifier_impl()

        def get_next_upkeep_step(self):
            return self.girl._get_next_upkeep_step_impl()

        def get_previous_upkeep_step(self):
            return self.girl._get_previous_upkeep_step_impl()

        def cut_upkeep(self, day_nb):
            return self.girl._cut_upkeep_impl(day_nb)

        def restore_upkeep(self):
            return self.girl._restore_upkeep_impl()

        # ── Performance & capacity ──

        def get_max_cust_served(self, job="current"):
            return self.girl._get_max_cust_served_impl(job)

        def get_max_interactions(self):
            return self.girl._get_max_interactions_impl()

        def get_interaction_modifier(self):
            return self.girl._get_interaction_modifier_impl()

        def reset_interactions(self):
            return self.girl._reset_interactions_impl()

        def estimate_performance(self, sex_act):
            return self.girl._estimate_performance_impl(sex_act)

        # ── Rewards ──

        def get_xp(self, act, result, customers):
            return self.girl._get_xp_impl(act, result, customers)

        def get_jp(self, act, result, customers, silent=False):
            return self.girl._get_jp_impl(act, result, customers, silent)

        def get_rep(self, score, customers, first_customer=False):
            return self.girl._get_rep_impl(score, customers, first_customer)

        def get_tip(self, act, result, customers, final_tip_change=0, first_customer=False, specials=[]):
            return self.girl._get_tip_impl(act, result, customers, final_tip_change, first_customer, specials)

        def get_street_tip(self):
            return self.girl._get_street_tip_impl()

        def whore_on_street(self):
            return self.girl._whore_on_street_impl()

        def change_rep(self, chg, silent=False):
            return self.girl._change_rep_impl(chg, silent)

        def customer_populations_safety_check(self, current_pop):
            return self.girl._customer_populations_safety_check_impl(current_pop)
