#### GirlEconomy — Economic calculations | 经济计算组件 ####
# Phase 2.1: Prices, upkeep, tips, customer capacity, performance estimation.
# 价格、维护费、小费、客户容量、表现评估
# ★ get_price/get_xp/get_jp/get_rep/estimate_performance — 已从 girlclass.rpy 移入
# Methods: get_tip, change_rep, get_max_cust_served, adjust_upkeep, etc.
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

        # ── Performance & capacity (implementations moved from girlclass.rpy) ──

        def get_max_cust_served(self, job="current"):
            return self.girl._get_max_cust_served_impl(job)

        def get_max_interactions(self):
            return self.girl._get_max_interactions_impl()

        def get_interaction_modifier(self):
            return self.girl._get_interaction_modifier_impl()

        def reset_interactions(self):
            return self.girl._reset_interactions_impl()

        def estimate_performance(self, sex_act):
            g = self.girl
            if g.will_do_sex_act(sex_act):
                stats = perform_job_dict[sex_act + "_stats"]
                score = 0
                totalw = 0
                for tup in stats:
                    stat, weight = tup
                    score += g.get_stat(stat) * weight
                    totalw += weight
                score /= float(totalw)
                return score
            return -1

        # ── Rewards (implementations moved from girlclass.rpy) ──

        def get_xp(self, act, result, customers):
            g = self.girl
            cust_diff = round_int(sum(c.diff for c in customers))
            if act in all_jobs:
                xp = xp_bonus_dict[result] * cust_diff ** 1.1 / 2
            elif act in all_sex_acts:
                xp = (xp_bonus_dict[result] * cust_diff) ** 1.1 / len(customers)

            xp_ttip = _("Base XP vs Difficulty: %s") % event_color["xp"] % (str_int(xp) + " XP")
            boost = g.get_effect("boost", result + " result xp")
            if boost != 1.0:
                xp = xp * boost
                xp_ttip += _("\nPerks & special effects: x%s") % percent_text(boost, False)

            if game.has_active_mod("chrisjobmod") and act in all_jobs:
                xp /= act_max_customers_modifier[g.job]
                xp_ttip += _("\nJob Mod modifier: x%s") % percent_text(1.0 / act_max_customers_modifier[g.job], False)

            xp = max(xp * cheat_modifier["xp"] * game.get_diff_setting("xp"), 1)
            xp_ttip += _("\n\nDifficulty modifier: x%s") % percent_text(cheat_modifier["xp"] * game.get_diff_setting("xp"), False)
            return xp, xp_ttip

        def get_jp(self, act, result, customers, silent=False):
            g = self.girl
            cust_rank = round_int(sum(c.rank for c in customers) / len(customers))
            if act in all_jobs:
                jp = dice(3, len(customers))
            else:
                jp = dice(3, 1 + len(customers))

            jp_ttip = _("Base JP vs customers: %s") % event_color["jp"] % (str_int(jp) + " JP")
            jp += jp_job_level_modifier[g.job_level[act]] + jp_customer_rank_modifier[cust_rank] + jp_result_modifier[result]
            jp_ttip += _("\nGirl rank vs Customer rank: %s\n") % plus_text(jp_job_level_modifier[g.job_level[act]] + jp_customer_rank_modifier[cust_rank], color_scheme="jp")
            jp_ttip += result.capitalize() + _(" result: %s") % plus_text(jp_result_modifier[result], color_scheme="jp")

            boost = g.get_effect("boost", result + " result jp")
            if boost != 1.0:
                jp = jp * boost
                jp_ttip += _("\nPerks & special effects: x%s") % percent_text(boost, False)

            if game.has_active_mod("chrisjobmod") and act in all_jobs:
                jp /= act_max_customers_modifier[g.job]
                jp_ttip += _("\nJob Mod modifier: x%s") % percent_text(1.0 / act_max_customers_modifier[g.job], False)

            jp_ttip += _("\n\nDifficulty modifier: x%s") % percent_text(cheat_modifier["jp"] * game.get_diff_setting("jp"), False)
            jp *= cheat_modifier["jp"] * game.get_diff_setting("jp")
            return jp, jp_ttip

        def get_rep(self, score, customers, first_customer=False):
            g = self.girl
            cust_rank = round_int(sum(c.rank for c in customers) / float(len(customers)))

            if cust_rank + 1 < g.rank:
                rep_ttip = _("No reputation change: customer rank too low.")
                return 0, rep_ttip
            elif cust_rank < g.rank:
                relative_rank = "lower"; pos_rep = 0.25; neg_rep = -0.75
            elif cust_rank == g.rank:
                relative_rank = "same"; pos_rep = 1; neg_rep = -0.5
            elif cust_rank > g.rank:
                relative_rank = "higher"; pos_rep = 1; neg_rep = -0.25

            if score >= (reversed_result_dict[rep_gains_dict[g.rank][relative_rank]] + g.get_effect("special", "score_to_rep")):
                pos_rep *= dice(len(customers))
                rep_ttip = _("Reputation increase vs Customers: +%s") % str_dec(pos_rep, 1)
                if first_customer:
                    first_rep_boost = g.get_effect("boost", "first customer rep")
                    if first_rep_boost != 1.0:
                        pos_rep *= first_rep_boost
                        rep_ttip += _("\nFirst customer bonus: x%s") % percent_text(first_rep_boost, False)
                return pos_rep, rep_ttip
            else:
                return neg_rep, ""

        def get_tip(self, act, result, customers, final_tip_change=0, first_customer=False, specials=[]):
            '''计算女孩小费收入 | Calculate girl's tip income'''
            g = self.girl
            cust_rank = ((sum(c.diff for c in customers) / float(len(customers))) / 10.0) ** 0.5
            tip = tip_base * cust_rank * g.rank
            tip += sum(cust.diff for cust in customers)
            tip = max(10, tip)

            if "lost virginity" in specials:
                tip += 100
                gold_ttip = _("Base tip: {image=img_gold}%i(Lost virginity: {image=img_gold}+100)\n") % tip
            else:
                gold_ttip = _("Base tip: {image=img_gold}%i\n") % tip

            tip_multiplier = 1.0
            if g.naked and act in all_jobs:
                tip_multiplier *= tip_act_modifier["naked bonus"] * g.get_effect("boost", "naked bonus")
                gold_ttip += _("\nNaked bonus: x%s") % percent_text(tip_act_modifier["naked bonus"] * g.get_effect("boost", "naked bonus"), False)
            if "bisexual" in specials:
                tip_multiplier *= tip_act_modifier["bisexual bonus"]
                gold_ttip += _("\nBisexual bonus: %s") % tip_act_modifier["bisexual bonus"]
            if act in all_sex_acts and len(customers) > 1:
                tip_multiplier *= tip_act_modifier["group bonus"] * len(customers)
                gold_ttip += _("\nGroup bonus: x%s") % percent_text(tip_act_modifier["group bonus"] * len(customers), False)
            if act in all_jobs:
                tip_multiplier *= tip_result_modifier["job " + result] * g.get_effect("boost", result + " result tip")
                gold_ttip += _("\nResult bonus: x%s") % percent_text(tip_result_modifier["job " + result] * g.get_effect("boost", result + " result tip"), False)
            else:
                tip_multiplier *= tip_result_modifier["whore " + result] * g.get_effect("boost", result + " result tip")
                gold_ttip += _("\nResult bonus: x%s") % percent_text(tip_result_modifier["whore " + result] * g.get_effect("boost", result + " result tip"), False)

            perk_tip_multiplier = g.get_effect("boost", "tip")
            if "focus" in specials: perk_tip_multiplier += 0.25
            if "virgin tip" in specials: perk_tip_multiplier += g.get_effect("boost", "virgin tip") - 1
            if first_customer: perk_tip_multiplier += (g.get_effect("boost", "first customer tip") - 1) / len(customers)
            if act in all_jobs: perk_tip_multiplier += g.get_effect("boost", "total tip", custom_scale=("job cust nb", len(customers))) - 1
            elif act in all_sex_acts: perk_tip_multiplier += g.get_effect("boost", "total tip", custom_scale=("whore cust nb", g.get_log("whore_cust", "today"))) - 1
            if perk_tip_multiplier != 1.0: gold_ttip += _("\nPerks and special effects: x%s") % percent_text(perk_tip_multiplier, False)
            tip_multiplier *= perk_tip_multiplier

            # BK Evolution: customer mood tip modifiers
            if customers:
                _mood_mult_sum = _mood_chance_sum = 0.0
                _mood_count = 0
                for cust in customers:
                    if hasattr(cust, 'affixes') and cust.affixes and cust.affixes.mood:
                        _mood_mult_sum += cust.affixes.mood.tip_multiplier
                        _mood_chance_sum += cust.affixes.mood.tip_chance
                        _mood_count += 1
                if _mood_count:
                    _avg_mult = _mood_mult_sum / _mood_count
                    _avg_chance = _mood_chance_sum / _mood_count
                    if _avg_mult != 1.0:
                        tip_multiplier *= _avg_mult
                        gold_ttip += _("\nCustomer mood avg: x%s") % percent_text(_avg_mult, False)
                    if _avg_chance > 0:
                        _tc_bonus = 1.0 + _avg_chance
                        tip_multiplier *= _tc_bonus
                        gold_ttip += _("\nCustomer mood tip chance avg: x%s") % percent_text(_tc_bonus, False)

            if tip_multiplier > maximum_tip_modifier:
                gold_ttip += _("\n{i}Total modifier cannot exceed x%s{/i}") % str(maximum_tip_modifier)
            tip_multiplier = min(maximum_tip_modifier, max(0.1, tip_multiplier))
            tip *= tip_multiplier

            act_modif = tip_act_modifier[act]
            if act_modif != 1.0:
                tip *= act_modif
                gold_ttip += _("\nAct modifier: x%i") % (act_modif * 100) + "%"
                if not game.has_active_mod("chrisjobmod") or cap_positive_tip_act_modifier:
                    if act_modif > 1.0: tip_multiplier = min(maximum_tip_modifier, max(0.1, tip_multiplier))

            if game.has_active_mod("chrisjobmod") and act in all_jobs:
                tip /= act_max_customers_modifier[g.job]
                gold_ttip += _("\nJob Mod modifier: x%s") % percent_text(1.0 / act_max_customers_modifier[g.job], False)

            extra = g.get_effect("change", "tip") + final_tip_change
            tip += extra
            if extra:
                gold_ttip += _("\n\nExtra tip: {image=img_gold}%s") % plus_text(extra)
                if final_tip_change: gold_ttip += _(" (Five stars perk: {image=img_gold}%s") % plus_text(final_tip_change)

            tip *= cheat_modifier["gold"] * game.get_diff_setting("gold")
            gold_ttip += _("\n\nDifficulty modifier: x%s") % percent_text(cheat_modifier["gold"] * game.get_diff_setting("gold"), False)
            tip = max(10, round_int(tip))
            gold_ttip += _("\n\n= {image=img_gold}%i") % tip
            return tip, gold_ttip

        def get_street_tip(self):
            return self.girl._get_street_tip_impl()

        def whore_on_street(self):
            return self.girl._whore_on_street_impl()

        def change_rep(self, chg, silent=False):
            return self.girl._change_rep_impl(chg, silent)

        def customer_populations_safety_check(self, current_pop):
            return self.girl._customer_populations_safety_check_impl(current_pop)
