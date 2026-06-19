#### Economy functions ####

init -3 python:
    def can_pay(price):

        if MC.gold >= price:
            return True

        else:
            return False


    def transact(obj, seller, buyer, price):
        if isinstance(obj, Item):
            renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % obj.name)
        elif isinstance(obj, ItemInstance) and buyer != MC:
            if not obj.sellable:
                renpy.notify(__("%s: You cannot trade this item.") % obj.name)
                return False
        
        if seller.type in ("MC", "girl"):
            notify(__("You have sold the %s to %s.") % (obj.name, buyer.name))
        # debug_notify(seller.type + " selling to " + buyer.type)

        if buyer.type == "NPC":
            MC.gold += price
        else:
            MC.gold -= price
            game.track("gold spent shops", price)

        if seller.type == "MC":
            MC.sold[buyer].append(obj)

        buyer.take(seller, obj)

        renpy.block_rollback()

        return True

    def get_exchange_rate(source, target): # Where source, target are "gold" or a Resource object

        if source == "gold":
            return 1 * game.get_diff_setting("resources")/(resource_gold_value[target.rank] * calendar.get_discount(source, target))

        elif target == "gold":
            return resource_gold_value[source.rank]*resource_sell_discount * calendar.get_discount(source, target) * game.get_diff_setting("gold")

        else:
            return resource_base_exchange_rate[source.rank][target.rank]  * calendar.get_discount(source, target) * game.get_diff_setting("resources")



#### EFFECT MANAGEMENT ####
## Most skills, items, spells, etc. cause effects. Effects are applied to a target: MC, slaves and girls, the brothel...

    def search_items(_key):

        list = []

        for k, v in item_dict.items():
            if _key in k:
                list.append(v)

        return list


    def cust_diff_description(diff):

        if diff <= 25:
            d = __("Very easy")
            col = "c_green"

        elif diff <= 50:
            d = __("Easy")
            col = "c_lightgreen"

        elif diff <= 100:
            d = __("Medium")
            col = "c_yellow"

        elif diff <= 150:
            d = __("Hard")
            col = "c_lightred"

        else:
            d = __("Very hard")
            col = "c_crimson"

        return "{color=[" + col + "]}" + d + "{/color}"


    def get_entertainment_bonus(customers):
        bonus_list = []
        satisfied = 0
        unsatisfied = 0

        for c in customers:
            val, sat = c.get_entertainment_bonus()
            bonus_list.append(val)
            if sat:
                satisfied += 1
            else:
                unsatisfied += 1

        return mean(bonus_list), satisfied, unsatisfied

## Performing (waitress, masseuse, geisha, dancer, whore)

    def perform(act, girls, customers, customer_reason = "", job_filter=False): # job_filter forces the use of the current job's tag as 'and_tag'

        change_log = NightChangeLog("Results", col=c_lightorange)

        xp_gains = defaultdict(int)
        rep_gains = defaultdict(int)
        jp_gains = defaultdict(int)
        tip_gains = defaultdict(int)

        # As suggested by Jinrey
        tip_multiplier = defaultdict(float) # (multiplicative)
        perk_tip_multiplier = defaultdict(float) # (additive)
        final_tip_change = defaultdict(int) # Applied last

        for girl in girls:
            tip_multiplier[girl] = perk_tip_multiplier[girl] = 1.0
        # End

        stat_gains = defaultdict(list)

        level_up = defaultdict(bool)
        job_up = defaultdict(bool)

        ev_type = "Normal"

        specials = []
        first_customer = defaultdict(bool)
        finish = False
        rape = False
        rand_item = None
        rape_text = ""
        tip_special = ""
        lost_virginity = defaultdict(bool)
        pickpocket_boost = 0
        ignore_budget = sum(g.get_effect("special", "ignore budgets") for g in girls)

        tired_changes = defaultdict(int)
        dirt_change = 0

        ## Update girls and customers flags

        for girl in girls:
            if not girl.has_worked:
                girl.has_worked = defaultdict(bool)

            if not girl.has_worked[calendar.time]:
                girl.has_worked[calendar.time] = True
                first_customer[girl] = True

        if act in all_jobs:
            for cust in customers:
                cust.receive_entertainment(act)
        elif act in all_sex_acts:
            for cust in customers:
                cust.receive_sex_act(act)
        else:
            raise AssertionError(__("%s is not a valid job or sex act for %s.") % (str(act), girls[0].fullname))

        ## STEP 1: Get customers difficulty

        cust_diff = mean_int(c.diff for c in customers) # // len(customers)

        change_log.add(__("Difficulty: %s") % cust_diff_description(cust_diff), "header", ttip = __("Difficulty is related to customer population and averaged among all targeted customers."), ttip_title=__("Difficulty"), separator="\n")


        ## STEP 2: Get customer satisfaction

        entertainment_bonus = 0
        sex_act_bonus = 0
        ttip = ""

        if act in all_jobs:
            # Customers special effects (only one customer result applies: too easy?)
            base_entertainment_bonus, sat, unsat = get_entertainment_bonus(customers) # / len(customers)

            ttip += __("Base modifier: %s") % plus_text(int(base_entertainment_bonus))

            if unsat:
                ttip += __(" (%i wanted to do something else)") % unsat

            # Lowering malus with effects such as the Party Girl perk
            entertainment_bonus = base_entertainment_bonus * girls[0].get_effect("boost", "customer penalties")

            # Up until this point, 'entertainment_bonus' is <= 0
            entertainment_bonus += sum(g.get_effect("increase satisfaction", "all jobs") for g in girls) + sum(g.get_effect("increase satisfaction", act) for g in girls)

            if entertainment_bonus != base_entertainment_bonus:
                ttip += __("\nPerks and special effects: %s") % plus_text(entertainment_bonus - base_entertainment_bonus)

        elif act in all_sex_acts:
            # Customers special effects

            if len(customers) > 1: # Group: Customer satisfaction penalties stack
                base_sex_act_bonus = sum(c.get_sex_act_bonus(group=True) for c in customers)
                ttip = __("Group sex modifier: %s") % plus_text(base_sex_act_bonus)
                sex_act_bonus = base_sex_act_bonus + sum(g.get_effect("increase satisfaction", "group") for g in girls)

            elif len(girls) > 1: # Bisexual: +1 to customer satisfaction
                base_sex_act_bonus = mean(c.get_sex_act_bonus(bis=True) for c in customers) + 1
                ttip = __("Bisexual sex modifier: %s") % plus_text(base_sex_act_bonus, "normal")
                sex_act_bonus = base_sex_act_bonus + sum(g.get_effect("increase satisfaction", "bisexual") for g in girls)

            else: # One on one
                cust = customers[0]

                if cust.wants_sex_act != cust.got_sex_act:
                    for girl in girls:
                        if girl.get_effect("special", "temptress"):
                            cust.wants_sex_act = cust.got_sex_act
                            specials.append(__("temptress"))
                            ttip += " (changed by " + event_color["good"] % "temptress" + ")"
                            break
                    else:
                        # Rape attempts
                        if cust.crazy == "rapist":
                            rape, rape_text = rape_attempt(girl, cust, brothel.get_threat(), change_log)
                            if rape:
                                act = cust.wants_sex_act
                                cust.got_sex_act = act
                                ttip += " (" + event_color["good"] % "raped" + ")"

                sex_act_bonus = base_sex_act_bonus = cust.get_sex_act_bonus()

                ttip = __("Chosen sex act modifier: %s") % plus_text(base_sex_act_bonus) + ttip

            sex_act_bonus += sum(g.get_effect("increase satisfaction", "all sex acts") for g in girls) + sum(g.get_effect("increase satisfaction", act) for g in girls)

            if base_sex_act_bonus != sex_act_bonus:
                ttip += __("\nPerks and special effects: %s") % plus_text(sex_act_bonus - base_sex_act_bonus)

            #<Chris Job Mod: Bonus/Malus from Entertainment Score> # Including edit from JMan
            if game.has_active_mod("chrisjobmod"):
                cust_avg_entertainment_score = round_int((sum((c.entertainment_score) for c in customers )) / (len(customers)*1.0) )
                sex_act_bonus += ((cust_avg_entertainment_score - entertainment_neutral_score) * entertainment_bonus_strength)
                ttip += __("\nJob Mod modifier: %s") % plus_text((cust_avg_entertainment_score - entertainment_neutral_score) * entertainment_bonus_strength)
            #</Chris Job Mod>

        # Improve customer mood if the bedroom type is better (lowers it if it isn't). Lower rank customers will be slightly less picky.

        cust_bonus = round_int(entertainment_bonus + sex_act_bonus + brothel.get_mood_modifier(min(district.rank-1, customers[0].rank)) + game.get_diff_setting("satisfaction"))

        ttip += __("\nRoom modifier: %s") % plus_text(brothel.get_mood_modifier(min(district.rank-1, customers[0].rank)) + game.get_diff_setting("satisfaction"))

        # Special interactions

        for girl in girls:
            if first_customer[girl] and girl.get_effect("change", "first customer satisfaction"):
                cust_bonus += girl.get_effect("change", "first customer satisfaction")
                ttip += __("First customer bonus: %s") % plus_text(girl.get_effect("change", "first customer satisfaction"))


            # BBCR bonus (may boost tip if procs depending on stat) - Unused for now
#             if girl.get_effect("special", "BBCR bonus"):

#                 spe = girl.get_stat(rand_choice(["beauty", "body", "charm", "refinement"])) - diff

#                 if spe > 0:
#                     tip_gains[girl] += spe
#                     specials.append(stat + " bonus")

            # LOCS bonus (may boost tip if procs depending on stat) - Unused for now
#             if girl.get_effect("special", "LOCS bonus"):

#                 spe = girl.get_stat(rand_choice(["libido", "obedience", "constitution", "sensitivity"])) - diff

#                 if spe > 0:
#                     tip_gains[girl] += spe
#                     specials.append(stat + " bonus")

            # Lost and Found perk

            if girl.get_effect("special", "random item"):
                specials.append("random item")
                d = dice(6)
                if d == 6:
                    rand_item = get_rand_item("rare")
                elif d >= 4:
                    rand_item = get_rand_item("common")
                else:
                    rand_item = get_rand_item()

                if rand_item:
                    girl.items.append(rand_item)


#         if act in all_jobs:
#             for girl in girls:

#                 # Flasher - Unused for now
#                 if girl.get_effect("special", "flasher"):
#                     cust_bonus += girl.get_effect("special", "flasher")
#                     rep_gains[girl] += 1
#                     specials.append("flasher")

        if act in all_sex_acts: # Note: some of those effects are antiquated

            if len(customers) > 1:
                suf = "_group"
            else:
                suf = ""

            for girl in girls:

                # Virgin (in use)
                if act == "sex":
                    if girl.pop_virginity():
                        cust_bonus += 3
                        specials.append("virgin" + suf)
                        lost_virginity[girl] = True
                        ttip += event_color["good"] % "Lost virginity: +3"

                # DT (unused)
                spe = girl.get_effect("special", "deep throat")
                if spe and act == "service":
                    cust_bonus += spe
                    specials.append("DT" + suf)
                    ttip += event_color["good"] % __("Deep throat: %s") % plus_text(spe)

                # Irrumatio (unused)
                if girl.get_effect("special", "irrumatio") and act == "service":
                    girl.change_stat("obedience", 1, silent=True)
                    stat_gains[girl].append(("obedience", 1))
                    specials.append("irrumatio")

                # Buk (unused)
                if girl.get_effect("special", "bukkake") and len(customers) > 1  and not finish:
                    cust_bonus += len(customers)
                    finish = True
                    dirt_change += brothel.change_dirt(len(customers))
                    specials.append("bukkake")
                    ttip += event_color["good"] % __("Bukkake: %s") % plus_text(len(customers))

                # Creampie (unused)
                spe = girl.get_effect("special", "creampie")
                if spe and act == "sex" and not finish:
                    cust_bonus += spe
                    specials.append("creampie" + suf)
                    finish = True
                    dirt_change += brothel.change_dirt(1)
                    ttip += event_color["good"] % __("Creampie: %s") % plus_text(spe)

                # A. Creampie (unused)
                spe = girl.get_effect("special", "anal creampie")
                if spe and act == "anal" and not finish:
                    cust_bonus += spe
                    specials.append("anal creampie" + suf)
                    finish = True
                    dirt_change += brothel.change_dirt(1)
                    ttip += event_color["good"] % __("Anal creampie: %s") % plus_text(spe)

                # Cum on face (unused)
                spe = girl.get_effect("special", "cum on face")
                if spe and not finish:
                    cust_bonus += spe
                    specials.append("cum on face" + suf)
                    finish = True
                    dirt_change += brothel.change_dirt(1)
                    ttip += event_color["good"] % __("Cum on face: %s") % plus_text(spe)

                # # Swallow (unused)
                # if girl.get_effect("special", "swallow") and not finish:
                #     final_tip_change[girl] += 25 * customers[0].rank
                #     rep_gains[girl] += 1
                #     finish = True
                #     if girl.get_effect("special", "catgirl"):
                #         specials.append("catgirl")
                #     else:
                #         specials.append("swallow")

                # Heart of gold/Elite pickpocket and Pickpocket perks (including Renza's trainer effect)

                # Pickpocket (Hard-coded)

                caught_chance = 0

                # Converts the pickpocket trait to elite if Renza's effect is on
                if brothel.get_effect("special", "pickpocket") and girl.get_effect("special", "pickpocket", raw=True):
                    if renpy.random.random() <= 0.25:
                        pickpocket_boost = 0.1

                # Regular pickpocket effect
                elif girl.get_effect("special", "pickpocket"):
                    if renpy.random.random() <= 0.25:
                        pickpocket_boost = 0.1
                        caught_chance = 0.15

        change_log.add(__("Customer satisfaction: %s") % plus_text(cust_bonus, "normal"), ttip=ttip, ttip_title=__("Customer satisfaction"))

        ## STEP 3: Calculate stat bonus

        stat_bonus = mean_int(girl.test_stats(perform_job_dict[act + "_stats"], cust_diff) for girl in girls) # // len(girls)
        ttip = __("Skill modifier (%s): %s ({i}%s{/i})") % (act, plus_text(stat_bonus), and_text([s[0] for s in perform_job_dict[act + "_stats"]], ", "))

        sensitivity_bonus = 0
        if act in all_sex_acts:

            # Sensitivity bonus for sex acts

            for girl in girls:
                s = girl.get_stat("sensitivity") - cust_diff

                if s >= 25:
                    sensitivity_bonus += 2
                elif s >= 10:
                    sensitivity_bonus += 1
                elif s <= -25:
                    sensitivity_bonus += -2
                elif s <= -10:
                    sensitivity_bonus += -1
                else:
                    sensitivity_bonus += 0

            sensitivity_bonus = sensitivity_bonus // len(girls)


        if sensitivity_bonus:
            ttip += __("\nSensitivity modifier: %s") % plus_text(sensitivity_bonus)


        ## STEP 4: Get job level bonus

        job_bonus = mean_int(girl.job_level[act] for girl in girls) # // len(girls)
        ttip += __("\nJob level modifier (%s): %s") % (act, plus_text(job_bonus))

        change_log.add(__("Girl skills: %s") % plus_text(stat_bonus + job_bonus, "normal"), ttip = ttip, ttip_title=__("Skill bonuses"))

        ## STEP 5: roll dice

        d = dice(6)
        ttip = __("Represents her performance on a given interaction. She rolled a %i") % d

        # re-rolls (traits/perks)

        if d == 1:
            ttip += " (" + event_color["bad"] % "critical failure" + ")"

            #Reroll chance
            if girls[0].get_effect("reroll", "critical failure") > 0 or (girls[0].get_effect("reroll", "job critical failure") > 0 and act in all_jobs) or (girls[0].get_effect("reroll", "whore critical failure") > 0 and act in all_sex_acts):
                d = dice(6)
                specials.append("reroll")

                ttip += " (" + event_color["bad"] % __("critical failure") + "). " + __("She rerolled a %i") % d

        if d == 2:
            if girls[0].get_effect("special", "unlucky"):
                d = 1
                specials.append("unlucky")

                ttip += ", but it turned to a 1 because she is unlucky (" + event_color["bad"] % __("critical failure") + ")"

        if d == 5:
            if girls[0].get_effect("special", "lucky"):
                d = 6
                specials.append("lucky")

                ttip += ", but it turned to a 6 because she is lucky"

        ttip += "."

        roll = roll_dict[d]

        # A roll of 6 will bypass budget restrictions

        if d == 6:
            ttip += " (" + event_color["good"] % "critical success" + "). She may ignore customer budget limits."
            ignore_budget = 1

        roll_changes = __("Roll: ") + "{image=" + "img_dice" + str(d) + "}"
        if "reroll" in specials:
            roll_changes += __(" (Reroll)")
            ev_sound = s_dice

        change_log.add(roll_changes, "header", ttip = ttip, ttip_title="Dice roll")

        ## STEP 6: Misc. bonuses

        # Activate auto-work items
        item_used = False
        for it in girls[0].items:
            if item_used:
                break
            elif it.usage == "auto_work":
                for e in it.effects:
                    if e.target.startswith(act):
                        text1 = __("Used %s") % (it.name)
                        r = girls[0].use_item(it)
                        if r == "used_up":
                            text1 += event_color["bad"] % " (used up)"
                        item_used = it

                        ttip = ""
                        for e in it.effects:
                            if e.type in ("gain", "changes"):
                                ttip += __("%s: %s\n") % (e.target.capitalize(), plus_text(e.value))

                        change_log.add(text1 + ".", ttip = ttip, ttip_title = it.name)
                        break

        # Apply misc effects
        if act in all_jobs:
            misc_bonus = brothel.get_effect("change", "all jobs") + sum(g.get_effect("change", "all jobs", raw=True) for g in girls)
        elif act in all_sex_acts:
            misc_bonus = brothel.get_effect("change", "all sex acts") + sum(g.get_effect("change", "all sex acts", raw=True) for g in girls)

        misc_bonus += brothel.get_effect("change", act + " results") + sum(girl.get_effect("change", act + " results", raw=True) for girl in girls)

        ttip = __("Perks & special effects: %s") % plus_text(misc_bonus, "normal") + ttip

        #<Chris Job Mod: Apply Difficulty Modifier for Job>
        if game.has_active_mod("chrisjobmod"):
            misc_bonus += act_difficulty_modifier[act]
            ttip += __("\nJob Mod modifier: %s") % plus_text(act_difficulty_modifier[act], "normal")
        #</Chris Job Mod>

        # Memories of rewards and punishment

        for girl in girls:
            if girl.remembers("reward", "good result"):
                misc_bonus += 1
                ttip += "\nRewarded bonus: +1"
            if girl.remembers("punish", "bad result"):
                misc_bonus += 1
                ttip += "\nPunished bonus: +1"

        if misc_bonus:
            change_log.add(__("Misc. effects: %s") % plus_text(misc_bonus, "normal"), ttip = ttip, ttip_title = __("Miscellaneous"))

        ## STEP 7: Get final result

        # Calculate score and get result
        score = d + stat_bonus + cust_bonus + sensitivity_bonus + job_bonus + misc_bonus

        for k in sorted(result_dict): # sorted used on a dictionary returns a list of all keys in ascending order
            if score >= k:
                result = result_dict[k]

        if result in ("very good", "perfect"):
            for cust in customers:
                if act in all_jobs:
                    cust.service_dict["entertained"] += 1
                elif act in all_sex_acts:
                    cust.service_dict["laid"] += 1

                if result == "perfect": unlock_achievement("happy " + cust.pop.name)

        #<Chris Job Mod: Assign the Score to all entertained customers>
        if game.has_active_mod("chrisjobmod"):
            if act in all_jobs:
                for cust in customers:
                    cust.entertainment_score = score
        #</Chris Job Mod>

        change_log.add(__("{b}Final result{/b}: %i\n%s") % (score, result_star_dict[result]), "header", ttip_title="{color=%s}%s result (%i){/color}" % (result_colors[result], result.capitalize(), score), ttip=result_reference)

        if act in all_jobs:
            change_log.add("Customers entertained: %i/%i" % (sum(1 for cust in customers if cust.service_dict["entertained"] > 0), len(customers)))

        elif act in all_sex_acts:
            change_log.add("Customers served: %i/%i" % (sum(1 for cust in customers if cust.service_dict["laid"] > 0), len(customers)))

        # Get tip, xp, jp and rep

        budget_ttip = "Customer budget is the cumulated amount they are willing to spend on this interaction.\n"
        if act in all_jobs:
            total_budget = sum(c.ent_budget for c in customers)
            if not ignore_budget:
                budget_boost = 1.0
                budget_ttip += __("\nCustomer initial budget: %s (%s customers)") % (total_budget, len(customers))
                for girl in girls:
                    budget_boost *= girl.get_effect("boost", "job customer budget")
                if budget_boost != 1.0:
                    budget_ttip += __("\nPerks and special effects: %s") % percent_text(budget_boost - 1.0)

                    total_budget *= budget_boost

        elif act in all_sex_acts:
            total_budget = sum(c.wh_budget for c in customers)
            if not ignore_budget:
                budget_boost = 1.0
                budget_ttip += __("\nCustomer initial budget: %s (%s customers)") % (total_budget, len(customers))
                for girl in girls:
                    budget_boost *= girl.get_effect("boost", "whore customer budget")
                if budget_boost != 1.0:
                    budget_ttip += __("\nPerks and special effects: %s") % percent_text(budget_boost - 1.0)

                    total_budget *= budget_boost

        initial_budget = total_budget # For use in the right-hand screen display

        gold_ttip = {}
        xp_ttip = {}
        jp_ttip = {}
        rep_ttip = {}

        for girl in girls:

            xp_gains[girl], xp_ttip[girl] = girl.get_xp(act, result, customers)
            jp_gains[girl], jp_ttip[girl] = girl.get_jp(act, result, customers)
            rep_gains[girl], rep_ttip[girl] = girl.get_rep(score, customers, first_customer[girl])

            # Calculate performance-related tip modifiers

            if lost_virginity[girl]:
                specials.append("lost virginity")

            # Bisexual modifier
            if len(girls) > 1:
                specials.append("bisexual")

            # Five Stars perk
            if cust_bonus > 0:
                final_tip_change[girl] += girl.get_effect("change", "total tip", custom_scale=("customer satisfaction", cust_bonus))

            # Focus perk
            if girl.get_effect("special", "focus") and act in all_sex_acts:
                if girl.count_activated_sex_acts() == 1:
                    specials.append("focus")
                    # perk_tip_multiplier[girl] += 0.25 # handled in get_tip
                    if rep_gains[girl] > 0:
                        rep_gains[girl] *= 1.25

            # Virgin whore perk
            if girl.has_trait("Virgin"):
                specials.append("virgin tip")
                # perk_tip_multiplier[girl] += girl.get_effect("boost", "virgin tip") - 1 # handled in get_tip
                if rep_gains[girl] > 0:
                    rep_gains[girl] *= girl.get_effect("boost", "virgin rep")

            _gold, gold_ttip[girl] = girl.get_tip(act, result, customers, final_tip_change[girl], first_customer[girl], specials=specials)
            tip_gains[girl] += _gold

            # Apply budget limits

            if not ignore_budget:
                if tip_gains[girl] > total_budget:
                    gold_ttip[girl] += event_color["bad"] % __("\nCustomer budget limit: %s") % (total_budget - tip_gains[girl])
                tip_gains[girl] = min(tip_gains[girl], total_budget)

            total_budget -= tip_gains[girl]

        # Applying pickpocket effect (ignores budgets)

        if pickpocket_boost:
            girl = girls[0]
            gain = round_int(pickpocket_boost * tip_gains[girl])
            tip_gains[girl] += gain
            gold_ttip[girl] += __("\n\nPickpocket: %s (%s)") % (plus_text(gain), girl.name)
            if renpy.random.random() <= caught_chance:
                rep_gains[girl] -= 1
                brothel.change_rep(-1 * customers[0].rank)
                gold_ttip[girl] += event_color["bad"] % "- Rep. lost"


        if len(girls) > 1:
            change_log.add(__("Tip: {image=img_gold_20} %s") % plus_text(sum(tip_gains.values()), "gold"), "header")
            for girl in girls:
                change_log.add(__("%s: {image=img_gold} %s") % (girl.fullname, plus_text(tip_gains[girl], "gold")), ttip=gold_ttip[girl], ttip_title=__("Total tip (%s)") % (girl.fullname))
        else:
            girl = girls[0]
            change_log.add(__("Tip: {image=img_gold_20} %s") % plus_text(tip_gains[girl], "gold"), "header", ttip=gold_ttip[girl], ttip_title=__("Total tip"))

        if ignore_budget:
            change_log.add(__("Customer budget: Unlimited"), ttip=budget_ttip, ttip_title=__("Customer budget"))
        else:
            if sum(tip_gains.values()) >= total_budget:
                budget_ttip += __(" (maxed)")
            change_log.add(__("Customer budget: %i") % int(initial_budget), ttip=budget_ttip, ttip_title=__("Customer budget"))


        ## STEP 8: Apply Changes
        # Receive XP, JP and REP gains

        for girl in girls:
            xp_gains[girl] = girl.change_xp(xp_gains[girl], silent=True)
            jp_gains[girl] = girl.change_jp(jp_gains[girl], act, silent=True)
            rep_gains[girl] = girl.change_rep(rep_gains[girl], silent=True)

            if girl.ready_to_level():
                level_up[girl] = True

            if girl.ready_to_job_up(act):
                job_up[girl] = True

        # Stats changes

        for girl in girls:
            stat_gains[girl] = girl.raise_stats(perform_job_dict[act + "_changes"], silent=True)

        # Prestige and breaking

            if act in all_sex_acts:
                MC.change_prestige(girl.rank*girl.get_effect("boost", "prestige"), silent=True)
                girl.raise_preference(act, bonus = 0.75, context="brothel")
                girl.add_log("perform " + act)

                if len(customers) > 1:
                    girl.raise_preference("group", bonus = 0.75, context="brothel")
                    girl.add_log("perform group")
                if len(girls) > 1:
                    girl.raise_preference("bisexual", bonus = 0.75, context="brothel")
                    girl.add_log("perform bisexual")

            elif act in all_jobs and girl.get_effect("special", "job prestige"):
                MC.change_prestige(girl.rank*girl.get_effect("boost", "prestige"), silent=True)


        ## STEP 9: Maintenance and tiredness

        # Get tired

        if act in all_jobs or len(girls) > 1:
            tiredness = 5 * len(customers)
        else:
            tiredness = 10 * len(customers)

        #<Chris Job Mod>
        if game.has_active_mod("chrisjobmod"):
            tiredness = round_int(tiredness * act_tiredness_per_customer_modifier[act])
        #</Chris Job Mod>

        if "catgirl" in specials:
            tiredness = round_int(tiredness * 0.75) # Ugly, should be changed

        for girl in girls:
            if girl == girls[0]: # Only takes its description from the first girl
                tired_description, tired_changes[girl] = girl.tire(tiredness)
            else:
                tired_changes[girl] = girl.tire(tiredness)[1]

        # Get dirty

        if act in all_jobs:
            dirt_change += brothel.change_dirt(len(customers) / 2)
        elif act in all_sex_acts:
            dirt_change += brothel.change_dirt(len(customers))


        ## STEP 10: Pic, log, descriptions and base event

        # PICTURE - Choose perform picture (New: will now prioritize horizontal pictures for perfect matches)

        and_tags = []
        not_tags = ["monster", "beast"] # Monster and beast pictures are not displayed during normal sex

        girl = girls[0]

        if lost_virginity[girl]:
            and_tags.append("virgin")

        if act in all_sex_acts:
            if not persistent.fuzzy_tagging_acts: # Disables machine and big for all non farm picture search
                not_tags.append("big")
                not_tags.append("machine")
            elif act != "fetish":
                not_tags.append("machine") # Machine pictures are excluded from normal sex (but not toy if fuzzy tagging is on)

            if len(customers) <= 1:
                not_tags.append("group") # Group pictures are excluded when there is only one customer
            if len(girls) <= 1:
                not_tags.append("bisexual") # Bi pictures are excluded when there is only one girl

            if (girl.work_whore or job_filter) and girl.job in all_jobs: # Adds a job tag if the girl is doing work & whore or job_filter is on
                and_tags += perform_job_dict[girl.job + "_tags"]

            # Group/Bisexual pictures can be mixed with regular pictures if the option is active

            if len(customers) > 1 and (not persistent.mix_group_pictures or dice(6) >= 3):
                work_pic = girl.get_pic(perform_job_dict["group_tags"], perform_job_dict[act + "_tags"], and_tags = and_tags + [act], not_tags = not_tags, and_priority=False, allow_lesbian=True, horizontal=True)
            elif len(girls) > 1 and (not persistent.mix_bis_pictures or dice(6) >= 3):
                work_pic = girl.get_pic(perform_job_dict["bisexual_tags"], perform_job_dict[act + "_tags"], and_tags = and_tags + [act], not_tags = not_tags, and_priority=False, allow_lesbian=True, horizontal=True)
            else:
                work_pic = girl.get_pic(perform_job_dict[act + "_tags"], and_tags = and_tags, not_tags = not_tags, allow_lesbian=True, horizontal=True)

#             if not work_pic: # Defaults to sex if a picture hasn't been found
#                 work_pic = girls[0].get_pic("sex")

            if not work_pic: # Defaults to naked if a sex picture hasn't been found
                work_pic = girl.get_pic("naked", allow_lesbian=True, horizontal=True)

        elif act in all_jobs:
            if persistent.fuzzy_tagging_jobs: # Allows secondary tags for jobs
                work_pic = girl.get_pic(perform_job_dict[act + "_tags"], perform_job_dict[act + "_tags2"], and_tags = and_tags, not_tags = not_tags, naked_filter=True, soft=True, horizontal=True)
            else: # Disallows secondary tags
                work_pic = girl.get_pic(perform_job_dict[act + "_tags"], and_tags = and_tags, not_tags = not_tags, naked_filter=True, soft=True, horizontal=True)

        if not work_pic:  # Defaults to profile if no other picture has been found
            work_pic = girl.get_pic("profile", and_tags = and_tags, not_tags = not_tags, naked_filter=True, soft=True, allow_lesbian=True, horizontal=True)

        if not work_pic: # Shouldn't happen unless the pack is Broken
            work_pic = Picture(path="resources/backgrounds/not_found.webp")

        # Determine customer gender

        if work_pic.has_tag("lesbian"):
            customers[0].set_gender("F")

        # Compose description

        cust_names = capitalize(and_text([c.name.lower() for c in customers]))
        girl_names = and_text([g.name for g in girls])

        if len(customers) > 1:
            cust_pronoun = __("they")
            cust_pronoun2 = __("their")
            cust_verb = __("were")
        else:
            if customers[0].gender == "M":
                cust_pronoun = __("he")
                cust_pronoun2 = __("his")
            else:
                cust_pronoun = __("she")
                cust_pronoun2 = __("her")
            cust_verb = __("was")

        if len(girls) > 1:
            girl_pronoun = __("them")
        else:
            girl_pronoun = __("her")

        if act in all_jobs:
            text_descript =  __(perform_job_dict[act + "_init"]) % (girl_names, len(customers))

        elif act in all_sex_acts:
            text_descript = __(customers[0].reason)

        if act in all_sex_acts:
            text_descript += __(perform_job_dict[customers[0].wants_sex_act + "_init"]) % girl_pronoun

            if customers[0].wants_sex_act != customers[0].got_sex_act:
                if len(customers) > 1:
                    text_descript += __(perform_job_dict["group not satisfied"]) % customers[0].got_sex_act

                elif len(girls) > 1:
                    text_descript += __(perform_job_dict["bisexual not satisfied"]) % customers[0].got_sex_act

                else:
                    text_descript += __(perform_job_dict["not satisfied"])

        if entertainment_bonus < 0:
            text_descript += __("\nSome customers would have preferred to do something else.")

        # Replace pronouns
        text_descript = text_descript.replace(":cust:", cust_names)
        text_descript = text_descript.replace(":girl:", girl_names)
        text_descript = text_descript.replace(":pron:", cust_pronoun)
        text_descript = text_descript.replace(":Pron:", cust_pronoun.capitalize())
        text_descript = text_descript.replace(":verb:", cust_verb)
        text_descript = text_descript.replace(":poss:", cust_pronoun2)
        text_descript = text_descript.replace(":Poss:", cust_pronoun2.capitalize())

        log.add_report(text_descript)

        if rape_text:
            text_descript += __(rape_text)
            customers[0].set_gender("M") # Rapists are always males to avoid complications

        if item_used:
            text_descript += "\nShe used " + item_used.name.lower() + " to improve the mood."

        for spe in specials:
            try:
                text_descript += event_color["good"] % __(perform_job_dict[spe]) % plural(len(customers))
            except:
                try:
                    text_descript += event_color["good"] % __(perform_job_dict[spe])
                except:
                    pass

        if act in all_sex_acts:
            if len(customers) > 1:
                text_descript += __(perform_job_dict["roll_" + roll]) % girl_names
                text_descript += __(perform_job_dict["group_" + result]) % girl_names
            elif len(girls) > 1:
                text_descript += __(perform_job_dict["bisexual_roll_" + roll]) % girl_names
                text_descript += __(perform_job_dict[customers[0].gender + " bisexual_" + result]) % girl_names
            else:
                text_descript += __(perform_job_dict["roll_" + roll]) % girl_names
                text_descript += __(perform_job_dict[customers[0].gender + " " + act + "_" + result]) % girl_names
        else:
            text_descript += __(perform_job_dict["roll_" + roll]) % girl_names
            text_descript += __(perform_job_dict[act + "_" + result]) % girl_names

        text_descript += tired_description


        # Budget cap description

        if total_budget == 0:
            text_descript += __(" {color=[c_green]}The customer%s spent all of %s budget on %s.{/color}") % (plural(len(customers)), cust_pronoun2, girl_pronoun)
            for cust in customers:
                unlock_achievement("broke " + cust.pop.name)
        elif total_budget < 0: # with ignore_budget
            text_descript += __(" {color=[c_gold]}The customer%s went over %s budget on %s (+%s gold).{/color}") % (plural(len(customers)), cust_pronoun2, girl_pronoun, str_int(-total_budget))
            for cust in customers:
                unlock_achievement("broke " + cust.pop.name)

        # Compose right menu content (changes) - NEW

        for girl in girls:
            if act in all_jobs:
                job_ttip = list_text([(j.capitalize() + " " + str(girl.job_level[j]) + " {image=img_star}") for j in all_jobs])
            elif act in all_sex_acts:
                job_ttip = list_text([(a.capitalize() + " " + str(girl.job_level[a]) + " {image=img_star}") for a in all_sex_acts])

            change_log.add(__("%s changes") % girl.fullname, "header", ttip_title=girl.fullname, ttip = __("%s is a level %i %s.\n\n%s") % (girl.name, girl.level, girl.job, job_ttip))

            if level_up[girl]:
                ev_type = "Level/Job/Rank up"
                log.add_report(log_event_dict["level"] % girl.fullname)
                # text_changes = __(stat_increase_dict["level"])
                #
                # if len(girls) > 1:
                #     text_changes += " {size=14}(" + girl.name + "){/size}" # Adds girl name for disambiguation if there are several

                change_log.add(__("LEVEL UP"), col="good", ttip = girl.fullname + __(" is ready to level up (%i -> %i)") % (girl.level, girl.level+1))

            change_log.add(__("{color=[c_lightgreen]}XP{/color}: %i/%i (%s)") % (girl.xp, girl.get_xp_cap(), plus_text(int(xp_gains[girl]), color_scheme = "xp")), ttip=xp_ttip[girl], ttip_title = __("Experience"))

            if job_up[girl]:
                ev_type = "Level/Job/Rank up"
                log.add_report(log_event_dict["job_up"] % (girl.fullname, girl.job))
                # text_changes = __(stat_increase_dict["job_up"])
                #
                # if len(girls) > 1:
                #     text_changes += " {size=14}(" + girl.name + "){/size}" # Adds girl name for disambiguation if there are several

                change_log.add("JOB SKILL UP", "header", col=c_orange)

            change_log.add("{color=[c_orange]}JP{/color}: %i/%i (%s)" % (girl.jp[act], girl.get_jp_cap(act), plus_text(int(jp_gains[girl]), color_scheme = "jp")), ttip=jp_ttip[girl], ttip_title = "Job points")

            if girl.ready_to_rank():
                ev_type = "Level/Job/Rank up"
                log.add_report(log_event_dict["rank"] % girl.fullname)
                # text_changes = __(stat_increase_dict["rank"])
                #
                # if len(girls) > 1:
                #     text_changes += " {size=14}(" + girl.name + "){/size}" # Adds girl name for disambiguation if there are several

                change_log.add("RANK UP", "header", col=c_softpurple)

        # text_changes += stat_increase_dict["xp"] % str(round_int(xp_gains[girls[0]]))
        # text_changes += stat_increase_dict["jp"] % str(round_int(jp_gains[girls[0]]))

            if rep_gains[girl] > 0:
                change_log.add("{color=[c_softpurple]}Reputation{/color}: %i/%i (%s)" % (girl.rep, girl.get_rep_cap(), plus_text(rep_gains[girl], color_scheme = "rep", decimals=1)), ttip=rep_ttip[girl], ttip_title = "Girl reputation")

            change_log = get_log_changes(girl, change_log, stat_gains[girl], act)

            change_log.add("Energy: {color=%s}%i{/color}/%i (%s)" % (girl.get_energy_color(), girl.energy, girl.get_stat_max("energy"), event_color["bad"] % str_dec(tired_changes[girl], 1)), ttip=girl.get_energy_ttip(), ttip_title = "Energy", before_separator="\n")

        if dirt_change:
            change_log.add("Dirt: {color=%s}%s{/color}" % (c_lightred, plus_text(dirt_change)), ttip=maintenance_desc[brothel.get_cleanliness()], ttip_title = "Dirt", before_separator="\n")
            log.dirt += dirt_change
            # debug_dirt_log.append([girls, dirt_change])

        # text_changes += "\n" + stat_increase_dict["gold+"] % str(round_int(sum(tip_gains.values()))) + tip_special

        # if total_budget == 0:
        #     text_changes += __("\n(max)")
        # elif total_budget < 0:
        #     text_changes += __("\n(over budget)")



        # Generate event(s)

        events = []

        if rape:
            ev_sound = s_scream_loud
            ev_type = "Health/Security"
        elif rand_item:
            ev_sound = s_spell
        else:
            ev_sound = None

        events.append(Event(pic = work_pic, char = girls[0].char, text = text_descript, changes = change_log, sound = ev_sound, type = ev_type))


        ## STEP 11: Special events

        # Add special breaking events

        if act in all_jobs: # Adds horny customer events during regular jobs

            girl = girls[0] # There is only one girl during jobs anyway
            extra_changes = []
            accepted = False

            chance = 10 * girl.get_effect("boost", "customer events")

            for cust in customers:
                if cust.get_effect("special", "horny"):
                    chance += 10

            if dice(100) <= chance and girl.energy > 0:
                ev_type = "Customer"

                if dice(6) >= 4 or girl.naked:
                    # Jobs are linked to one specific sex act that they have a chance of improving through customer events
                    if act == "waitress":
                        s_act = "service"
                    elif act == "masseuse":
                        s_act = "sex"
                    elif act == "dancer":
                        s_act = "anal"
                    elif act == "geisha":
                        s_act = "fetish"

                    resisted_rule = False

                    # If MC has ruled out sex acts with customers
                    if girl.flags["forbid customer sex"]:
                        ob_target = girl.get_stat("obedience")*2 + girl.mood//5 - girl.get_stat("libido")

                        if girl.is_("very dom"):
                            ob_target -= 50
                        elif girl.is_("dom"):
                            ob_target -= 25
                        elif girl.is_("very sub"):
                            ob_target += 50
                        elif girl.is_("sub"):
                            ob_target += 25

                        ob_target += 15 * girl.remembers("punish", "fooled around")

                        if dice(girl.rank*50) > ob_target:
                            resisted_rule = True

                else:
                    s_act = "naked"

                d = dice(3)

                # Naked event
                if s_act == "naked":

                    if d == 1: # Obedience
                        text1 = __("Customers started clamoring for %s to strip naked. Soon, she found herself surrounded by horny customers trying to rip her clothes off.") % girl.name

                        r = girl.get_stat("obedience") - dice(250)

                        if r > 0:
                            text1 += __("\n{color=[c_green]}Knowing that customers are always right, she let them take her clothes off one by one until she is completely naked.{/color}")
                            extra_changes.append(("obedience", girl.change_stat("obedience", dice(3), silent=True)))
                            extra_changes.append(("reputation", girl.change_stat("reputation", 1, silent=True)))

                            accepted = True

                        elif r > -50:
                            text1 += __("\n{color=[c_yellow]}The customers were really insistant, so she agreed to go topless.{/color}\nThe customers would have wanted more, but were happy to fondle her naked breasts while she worked nonetheless.")
                            extra_changes.append(("obedience", girl.change_stat("obedience", 1, silent=True)))

                            girl.raise_preference(s_act, context="brothel")

                        else:
                            text1 += __("\n{color=[c_red]}She screamed and pushed the customers away, making a fuss.{/color}\nSeveral customers left, muttering that they had seen churches that were wilder than your brothel.")
                            extra_changes.append(("reputation", girl.change_stat("reputation", -1, silent=True)))
                            extra_changes.append(("brothel reputation", brothel.change_rep(-1*customers[0].rank)))


                    elif d == 2: # Libido
                        text1 = __("A horny customer started undressing in the middle of the %s. He dared %s to do the same.") % (job_room_display_name[girl.job], girl.name)

                        r = girl.get_stat("libido") - dice(250)

                        if r > 0:
                            text1 += __("\n{color=[c_green]}She was feeling horny and liked the customer, so she agreed.{/color}")
                            extra_changes.append(("libido", girl.change_stat("libido", dice(3), silent=True)))
                            extra_changes.append(("reputation", girl.change_stat("reputation", 1, silent=True)))

                            accepted = True

                        elif r > -50:
                            text1 += __("\n{color=[c_yellow]}She felt shy and refused, but the customer started grinding against her, lifting her skirt and shirt to give everyone a glimpse at her body.{/color}\nShe felt a little aroused.")
                            extra_changes.append(("libido", girl.change_stat("obedience", 1, silent=True)))

                            girl.raise_preference(s_act, context="brothel")

                        else:
                            text1 += __("\n{color=[c_red]}She told the customer to put his clothes on before she called security.{/color}\nThe customer was upset and left.")
                            extra_changes.append(("reputation", girl.change_stat("reputation", -1, silent=True)))
                            extra_changes.append(("brothel reputation", brothel.change_rep(-1*customers[0].rank)))

                    elif d == 3: # Sensitivity
                        text1 = __("A drunk customer told %s he loved her, and that he would be the happiest man in Zan if she would show him her heavenly body.") % girl.name

                        r = girl.get_stat("sensitivity") - dice(250)

                        if r > 0:
                            text1 += __("\n{color=[c_green]}All the customers then started begging %s to do it, so she felt she couldn't refuse.{/color}") % girl.name
                            extra_changes.append(("sensitivity", girl.change_stat("sensitivity", dice(3), silent=True)))
                            extra_changes.append(("reputation", girl.change_stat("reputation", 1, silent=True)))

                            accepted = True

                        elif r > -50:
                            text1 += __("\n{color=[c_yellow]}She refused, but the man kept pleading her and was soon joined by other customers.{/color}\nEventually, she agreed to flash her boobs to keep the crowd happy. It turned her on a little.")
                            extra_changes.append(("sensitivity", girl.change_stat("sensitivity", 1, silent=True)))

                            girl.raise_preference(s_act, context="brothel")

                        else:
                            text1 += __("\n{color=[c_red]}She snapped and yelled at the customer.{/color}\nHe left unhappy. Other customers overheard and grumbled disapprovingly.")
                            extra_changes.append(("reputation", girl.change_stat("reputation", -1, silent=True)))
                            extra_changes.append(("brothel reputation", brothel.change_rep(-1*customers[0].rank)))

                    if accepted:
                        pic = girl.get_pic(perform_job_dict[act + "_tags"], "naked", and_tags = "naked", not_tags = all_sex_acts + ["group", "bisexual", "beast", "monster"], horizontal=True)
                    else:
                        pic = work_pic

                    events.append(Event(pic, char = girl.char, text = text1, changes = get_change_text(extra_changes), type = ev_type))

                # Sex acts
                else:

                    if d == 1: # Obedience
                        text1 = __("A customer ordered %s to give him extra service. He wanted her to %s.") % (girl.name, s_des[s_act])

                        r =  girl.get_stat("obedience") - dice(100) - preference_modifier[girl.get_preference(s_act)] # Reminder: preference modifier is between 150 (refuses) and -75 (fascinated)

                        if girl.flags["forbid customer sex"] and not resisted_rule:
                            r = min(0, r)

                        if r > 0:
                            if girl.has_trait("Virgin") and s_act == "sex":
                                s_act = weighted_choice([("service", 4), ("anal", 2), ("fetish", 1)])
                                text1 += __("\n{color=[c_green]}As she is a virgin, she gently denied the customer's request and agreed to %s instead.{/color}") % s_des[s_act]
                            else:
                                text1 += __("\n{color=[c_green]}She obediently accepted the customer's request.{/color}")

                            extra_changes.append(("obedience", girl.change_stat("obedience", dice(3), silent=True)))
                            extra_changes.append(("reputation", girl.change_stat("reputation", 1, silent=True)))

                            accepted = True

                        elif r > -50:
                            text1 += __("\n{color=[c_yellow]}She politely declines, saying nothing as the customer whips out his cock and starts masturbating while she works.{/color}\nShe is left confused and a little aroused by the whole experience.")
                            extra_changes.append(("obedience", girl.change_stat("obedience", 1, silent=True)))

                            girl.raise_preference(s_act, context="brothel")

                        else:
                            text1 += __("\n{color=[c_red]}She told the customer to fuck off.{/color}\nHe left upset, complaining about the bad service at your brothel.")
                            extra_changes.append(("reputation", girl.change_stat("reputation", -1, silent=True)))
                            extra_changes.append(("brothel reputation", brothel.change_rep(-1*customers[0].rank)))


                    elif d == 2: # Libido
                        text1 = __("A customer flirted with %s all night. He tried to get her to %s.") % (girl.name, s_des[s_act])

                        r = girl.get_stat("libido") - dice(100) - preference_modifier[girl.get_preference(s_act)] # Reminder: preference modifier is between 150 (refuses) and -75 (fascinated)

                        if r > 0:
                            if girl.has_trait("Virgin") and s_act == "sex":
                                s_act = weighted_choice([("service", 4), ("anal", 2), ("fetish", 1)])
                                text1 += __("\n{color=[c_green]}To protect her virginity, she lustily agreed to %s instead.{/color}") % s_des[s_act]
                            else:
                                text1 += __("\n{color=[c_green]}She was feeling horny and she liked the customer, so she agreed.{/color}")
                            extra_changes.append(("libido", girl.change_stat("libido", dice(3), silent=True)))
                            extra_changes.append(("reputation", girl.change_stat("reputation", 1, silent=True)))

                            accepted = True

                        elif r > -50:
                            text1 += __("\n{color=[c_yellow]}She refused, but the customer was very insistent and she felt a little horny.{/color}\nSo she let him fondle her tits and ass a little.")
                            extra_changes.append(("libido", girl.change_stat("obedience", 1, silent=True)))

                            girl.raise_preference(s_act, context="brothel")

                        else:
                            text1 += __("\n{color=[c_red]}She got upset and left the room.{/color}\nThe customer was grumpy and disappointed.")
                            extra_changes.append(("reputation", girl.change_stat("reputation", -1, silent=True)))
                            extra_changes.append(("brothel reputation", brothel.change_rep(-1*customers[0].rank)))

                    elif d == 3: # Sensitivity
                        text1 = __("A customer told her a very sad and touching story. He asked if she would %s, to help him forget his sorrows.") % s_des[s_act]

                        r = girl.get_stat("sensitivity") - dice(100) - preference_modifier[girl.get_preference(s_act)] # Reminder: preference modifier is between 150 (refuses) and -75 (fascinated)

                        if r > 0:
                            if girl.has_trait("Virgin") and s_act == "sex":
                                s_act = weighted_choice([("service", 4), ("anal", 2), ("fetish", 1)])
                                text1 += __("\n{color=[c_green]}She wanted to help him and offered to %s instead, to retain her virginity.{/color}") % s_des[s_act]
                            else:
                                text1 += __("\n{color=[c_green]}She was touched by his story, and decided she couldn't refuse him.{/color}")
                            extra_changes.append(("sensitivity", girl.change_stat("sensitivity", dice(3), silent=True)))
                            extra_changes.append(("reputation", girl.change_stat("reputation", 1, silent=True)))

                            accepted = True

                        elif r > -50:
                            text1 += __("\n{color=[c_yellow]}She gently refused, instead giving the customer a hug.{/color}\nHe was all too eager to take advantage of it and rub himself against her, but she let it slide.")
                            extra_changes.append(("sensitivity", girl.change_stat("sensitivity", 1, silent=True)))

                            girl.raise_preference(s_act, context="brothel")

                        else:
                            text1 += __("\n{color=[c_red]}She coldly told the customer off, threatening to call security.{/color}\nHe was upset and left grumbling.")
                            extra_changes.append(("reputation", girl.change_stat("reputation", -1, silent=True)))
                            extra_changes.append(("brothel reputation", brothel.change_rep(-1*customers[0].rank)))

                    if accepted and girl.flags["forbid customer sex"]:
                        text1 += event_color["bad"] % __("\nShe ignored your order to stay away from customers.")
                        girl.track_event("fooled around", arg=__(s_des[s_act]))

                    events.append(Event(pic = work_pic, char = girl.char, text = text1, changes = get_change_text(extra_changes), type = ev_type))

                    if accepted:
                        customers[0].wants_sex_act = s_act
                        events += perform(s_act, [girl], [customers[0]], job_filter=True)


        else: # Act weakness discovery during sex acts (actual fixations are only discovered by MC interaction for now)

            for girl in girls:

                if len(customers) > 1:
                    s_act = "group"
                    plur = "s"
                elif len(girls) > 1:
                    s_act = "bisexual"
                    plur = ""
                else:
                    s_act = act
                    plur = ""

                if not girl.personality_unlock[s_act]:

                    ev_type = "Customer"

                    text1 = ""

                    pos_reaction, neg_reaction = girl.test_weakness(s_act, unlock=True)

                    if pos_reaction and neg_reaction:
                        text1 += __("%s blushes bright red and looks very uncomfortable with %s. However, her nipples are erect and she becomes noticeably wet. {color=[c_yellow]}It's like she both loves and hates it.{/color}") % (girl.name, long_act_description[s_act])
                        ev_sound = s_sigh
                        log.add_report(__("%s is {color=[c_darkgold]}ambivalent{/color} about %s.") % (girl.name, long_act_description[s_act]))
                        chg = "{color=%s}Ambivalent act discovered:\n%s{/color}" % (c_yellow, s_act.capitalize())

                    elif pos_reaction:
                        if act == "service":
                            text1 += __("%s is flustered by the sight of the customer's dick while servicing him. She starts masturbating as she plays with the customer%s.") % (girl.name, plur)
                        elif act == "fetish":
                            text1 += __("%s's pleasure centers are overwhelmed by unknown sensations, and she becomes very wet as the customer toys with her.") % girl.name
                        else:
                            text1 += __("%s is very sensitive and she eventully reaches orgasm as she is fucked by the customer%s.") % (girl.name, plur)

                        text1 += __("\n{color=[c_green]}It seems that she loves %s.{/color}") % long_act_description[s_act]
                        ev_sound = s_mmmh
                        log.add_report(__("%s is {color=[c_green]}sensitive{/color} to %s.") % (girl.name, long_act_description[s_act]))
                        chg = "{color=%s}Positive act discovered:\n%s{/color}" % (c_green, s_act.capitalize())

                    elif neg_reaction:
                        text1 += __("%s acts very uncomfortable around the customer%s, something is bothering her. {color=[c_red]}She seems to dislike %s.{/color}") % (girl.name, plur, long_act_description[act])
                        ev_sound = s_surprise
                        log.add_report(__("%s is {color=[c_red]}uncomfortable{/color} with %s.") % (girl.name, long_act_description[s_act]))
                        chg = "{color=%s}Negative act discovered:\n%s{/color}" % (c_red, s_act.capitalize())

                    if pos_reaction or neg_reaction:
                        events.append(Event(pic = work_pic, char = girl.char, text = text1, changes=chg, sound = ev_sound, type = ev_type))


        # Log information for tracking stats

        log.gold_made += sum(tip_gains.values())

        for girl in girls:
            girl.add_log("total_cust", len(customers))
            girl.add_log(act + "_cust", len(customers))
            girl.add_log(act + "_" + result, 1)
            girl.add_log(act + "_score", score)
            girl.add_log(act + "_score_base", 1)

            if act in all_sex_acts:
                girl.add_log("whore_cust", len(customers))
                girl.add_log("whore_" + result, 1)
                girl.add_log("whore_score", score)
                girl.add_log("whore_score_base", 1)

            girl.add_log("total_xp", xp_gains[girl])
            girl.add_log("total_gold", tip_gains[girl])
            girl.add_log("total_jp", jp_gains[girl])
            girl.add_log("total_rep", rep_gains[girl])

            girl.add_log(act + "_xp", xp_gains[girl])
            girl.add_log(act + "_gold", tip_gains[girl])
            girl.add_log(act + "_jp", jp_gains[girl])
            girl.add_log(act + "_rep", rep_gains[girl])

            if result in ("very bad", "bad"):
                girl.track_event("bad result", arg=(__(result), __(act)))

            elif result in ("good", "very good", "perfect"):
                girl.track_event("good result", arg=(__(result), __(act)))


        return events


    def get_customer_population_count(customers):
        pop_count = defaultdict(int)

        for cust in customers:
            pop_count[cust.pop] += 1

        ttip = ""

        for pop in all_populations:
            if pop_count[pop]:
                ttip += __("%s: %i\n") % (pop.name.capitalize(), pop_count[pop])

        return ttip


    def reset_alerts():
        seen_alerts = defaultdict(bool)
        return

    def generate_customers(rep, use_adv=True, use_log=True): # Bring in the customers. use_adv is fed the number of working girls

        customers = []
        cust_nb, cust_nb_dict = count_customers(rep, randomize=True, use_adv=use_adv)

        # Log incoming customers

        cust_text = __("%s customers came to %s.") % (cust_nb, brothel.name)
        if use_log:
            log.add_report(event_color["good"] % cust_text)

        cust_text += __("\nBase customers: %s") % plus_text(cust_nb - cust_nb_dict["advertising"] - cust_nb_dict["special"])


        if cust_nb_dict["advertising"]:
            # cust_text += __(" (including +") + str_int(cust_nb_dict["advertising"]) + __(" from advertising)")
            cust_text += __("\nAdvertising: %s") % (plus_text(cust_nb_dict["advertising"]))
        elif cust_nb_dict["special"]:
            # cust_text += __(" (including +") + str_int(cust_nb_dict["special"]) + __(" from special effects)")
            cust_text += __("\nSpecial effects: %s") % (plus_text(cust_nb_dict["special"]))

        if use_log:
            log.cust = cust_nb

        # Generate customers

        cust_list = []

        for pop in all_populations:
            for i in range(int(cust_nb_dict[pop.name])):
                cust_list.append(Customer(pop))

        renpy.random.shuffle(cust_list)

        if use_log:
            for c in cust_list:
                log.add_report(__("%s came to the brothel. He wants to be attended to by a %s and likes %s.") % (c.name, c.wants_entertainment, c.wants_sex_act))

        return cust_list, cust_text, cust_nb_dict


    def count_customers(rep, randomize=True, use_adv=True): # Turn randomize off for UI display

        cust_nb_dict = defaultdict(int)
        cust_nb = 0

        base_points = rep/10
        adv_points = brothel.get_adv_attraction()
        special_points = brothel.get_effect("change", "customers", randomize=randomize) * district.rank + (brothel.get_effect("boost", "customers") - 1) * (base_points+adv_points)

        if use_adv:
            cust_points = base_points + adv_points + special_points
        else: # Advertising does not apply if the brothel is closed
            cust_points = base_points + special_points

        spent_points = 0

        available_pop = sorted([pop for pop in all_populations if pop.is_allowed()], key = lambda x : x.weight, reverse=True)

        weighted_total = sum((p.weight*p.rank) for p in available_pop)

        # First, creates a balanced mix of customers according to population cost and weight
        for pop in available_pop:
            cust_nb_dict[pop.name] += math.ceil(cust_points * pop.weight / weighted_total)
            spent_points += cust_nb_dict[pop.name] * pop.rank
            if spent_points > cust_points and cust_nb_dict[pop.name] > 0:
                cust_nb_dict[pop.name] -= 1
                spent_points -= pop.rank
            cust_nb += cust_nb_dict[pop.name]

        # Distribute the remaining points to the lowest rank population
        if cust_points > spent_points:
            pop = sorted(available_pop, key = lambda x : x.rank)[0]
            if pop.rank <= cust_points - spent_points:
                cust_nb_dict[pop.name] += (cust_points - spent_points) // pop.rank
                cust_nb += (cust_points - spent_points) // pop.rank

        # Logs advertising and special effect customers (rounded down to avoid potential confusion)

        if cust_points:
            cust_nb_dict["advertising"] = round_int(cust_nb * adv_points // cust_points)
            cust_nb_dict["special"] = round_int(cust_nb * special_points // cust_points)

        # The brothel is guaranteed one free customer no matter what
        cust_nb_dict[available_pop[0].name] += 1
        cust_nb += 1

        return round_int(cust_nb), cust_nb_dict # returns customer total and a dictionary including the number of customers for each type

    def get_available_populations():
        return [pop for pop in all_populations if pop.is_allowed()]

    def job_matchmaking(available_girls, customers, ent_dict=None, job_cap=None, ticket_dict=None):
        game.mm_log = ""

        ### Returns ent_dict as {girl : [affected customers]}, a list of unattended customers, job_cap and ticket_dict

        if not ent_dict:
            ent_dict = defaultdict(list)
        if not ticket_dict:
            ticket_dict = {}

        #### SANITY CHECKS ####

        # Aborpts if no girls or no customers
        if not available_girls or not customers:
            game.mm_log += "\nNo girls or cust left"
            return ent_dict, customers, job_cap, ticket_dict

        # Init job caps (to avoid going over the room limit)
        if not job_cap:
            game.mm_log += "\nInit job cap"
            job_cap = defaultdict(int)
            for job in all_jobs:
                job_cap[job] = min(sum(g.get_max_cust_served() for g in available_girls if g.job == job), brothel.rooms[job_room_dict[job]].cust_limit)

        # Aborpts if no job cap is left
        if sum(job_cap[j] for j in all_jobs) <= 0:
            game.mm_log += "\nNo job cap left"
            return ent_dict, customers, job_cap, ticket_dict

        #### PREPARING ####

        ## Creating a dictionary of girl tickets
        if not ticket_dict:
            game.mm_log += "\nNew ticket dict"
            # ticket_dict = defaultdict(lambda: defaultdict(list)) # nested dictionary - changed because it breaks Renpy saves
            ticket_dict = defaultdict(list)

            # Adding x tickets per girl where x is max_customers_served
            for girl in available_girls:
                ticket_dict[girl.rank, girl.job] += [girl] * girl.get_max_cust_served()

            # Shuffling girl tickets
            for rank in range(1, 6):
                for job in all_jobs:
                    renpy.random.shuffle(ticket_dict[rank, job])

        ## Set up rank lookup order during matchmaking
        # Nearby Ranks are checked first (loaded from JSON in init block)

        ## Preparing customers
        # Higher rank customers are prioritized (not by budget, to provide some variation and keeping rich/broke customers relevant)
        customers.sort(key= lambda x : x.rank, reverse=True)

        # Using a separate list from customers to avoid messing the 'for' loop
        leftover_customers = list(customers)


        #### MATCHMAKING ####

        # If the player is using the 'Prioritize same rank customers' setting
        if game.matching_priority == "rank":
            order = ["wanted same rank", "unwanted same rank", "wanted other rank", "unwanted other rank"]

        # If the player is using the 'Prioritize customer preferences' setting
        elif game.matching_priority == "act":
            order = ["wanted same rank", "wanted other rank", "unwanted same rank", "unwanted other rank"]

        for step in order:
            if step not in ["wanted same rank", "wanted other rank", "unwanted same rank", "unwanted other rank"]:
                raise AssertionError("Step %s is not recognized." % step)

            game.mm_log += __("\nBegin step %s: %s customers") % (step, str(len(customers)))
            for cust in customers:
                if step.endswith("same rank"):
                    rank_list = [cust.rank]
                else:
                    rank_list = rank_lookup_dict[cust.rank]

                if step.startswith("wanted"):
                    job_list = [cust.wants_entertainment]
                else:
                    job_list = list(all_jobs)
                    job_list.remove(cust.wants_entertainment)

                for rank in rank_list:
                    for job in job_list:
                        if job_cap[job] <= 0: # Skip if no room is available
                            game.mm_log += __("\nSkipping %s because it's full") % job
                            continue # Try another job

                        if not ticket_dict[rank, job]: # Skip if no girl ticket is available
                            game.mm_log += __("\nSkipping %s because no tickets left") % job
                            continue # Try another job

                        # Assigns a girl ticket
                        for girl in ticket_dict[rank, job]:
                            # Checks if the girl will accept this customer according to her individual settings
                            if not girl.refused_populations[cust.pop.name]:
                                game.mm_log += __("\nCustomer #%s has been assigned") % customers.index(cust)
                                ent_dict[girl].append(cust)
                                leftover_customers.remove(cust)
                                job_cap[job] -= 1
                                try:
                                    ticket_dict[rank, job].remove(girl) # This breaks the loop, but hopefully no side effects
                                except:
                                    raise AssertionError(ticket_dict[rank, job])
                                break # Exit girl ticket loop
                        else:
                            continue # Try another job
                        break # Exit job loop
                    else:
                        continue # Try another rank
                    break # Exit rank loop

            game.mm_log += __("\nEnd of step %s, %s customers have been assigned.") % (step, str(len(customers)-len(leftover_customers)))
            customers = list(leftover_customers)

        return ent_dict, leftover_customers, job_cap, ticket_dict


    def wh_matchmaking(whores, customers):
        # Returns a list of tuples (girls, customers, sex_act) and a list of unattended customers

        game.mm_log = "" # Leftover from debugging, remove this once the function is stable

        #### SANITY CHECKS ####

        ## Creating local lists to avoid problems
        _whores = list(whores)
        _customers = list(customers)
        _wh_list = []

        # Aborpts if no girls or no customers
        if not _whores or not _customers:
            game.mm_log += "ENDED: No whores or no customers"
            return _wh_list, _customers

        #### PREPARING ####

        ## Preparing customers
        # Higher rank customers are prioritized (not by budget, to provide some variation and keeping rich/broke customers relevant)
        # renpy.random.shuffle(customers)
        # customers.sort(key= lambda x : x.rank, reverse=True)

        ### JMan's code ###
        if not game.has_active_mod("chrisjobmod") or shuffle_whore_customers:
            renpy.random.shuffle(customers)

        customers.sort(key= lambda x : x.rank, reverse=True)

        if game.has_active_mod("chrisjobmod") and shuffle_whore_customers and entertainment_bonus_strength != 0:
            customers.sort(key=lambda x: x.service_dict["entertained"] > 0, reverse=True)
        ### End of JMan's code ###


        # Using a separate list from customers to avoid messing the 'for' loop
        leftover_customers = list(_customers)

        #### MATCHMAKING ####

        # If the player is using the 'Prioritize same rank customers' setting
        if game.matching_priority == "rank":
            order = ["wanted same rank", "unwanted same rank", "wanted other rank", "unwanted other rank"]

        # If the player is using the 'Prioritize customer preferences' setting
        elif game.matching_priority == "act":
            order = ["wanted same rank", "wanted other rank", "unwanted same rank", "unwanted other rank"]

        for step in order:
            game.mm_log += __("\n\nStep: %s (%s whores available)\n") % (step, len(_whores))
            # Customers get their picks in descending order of rank
            for cust in _customers:
                game.mm_log += __("\n%s came ") % cust.name
                # Aborts if no girls are left
                if not _whores:
                    game.mm_log += "but found no whore left."
                    break # Stops matchmaking

                # Ignore grouped customers
                if cust.group:
                    game.mm_log += "and joined a GROUP."
                    leftover_customers.remove(cust)
                    continue # Move on to the next customer

                # Filter available girls
                base_available_girls = [g for g in _whores if g.interactions > 0 and not g.refused_populations[cust.pop.name] and g.does_anything()]

                available_girls = list(base_available_girls) # Keeps track of base_available_girls to increase the bisexual girl pool

                if step.endswith("same rank"):
                    available_girls = [g for g in available_girls if g.rank == cust.rank]

                if step.startswith("wanted"):
                    available_girls = [g for g in available_girls if g.does[cust.wants_sex_act]]

                if not available_girls:
                    game.mm_log += "but no girl was available at this step."
                    continue # Move on to the next customer

                # Choosing the best girl for this customer

                girl, sex_act = cust.choose_girl(available_girls)
                if not girl:
                    raise AssertionError("Error: A customer failed to pick a girl.")

                game.mm_log += __("and chose %s for %s.") % (girl.fullname, sex_act)

                leftover_customers.remove(cust)

                ## Group and bisexual matchmaking

                check_order = ["bisexual", "group"]
                c_list = [cust]
                g_list = [girl]

                if girl.archetypes["The Escort"].unlocked and not girl.archetypes["The Courtesan"].unlocked: # Escort tree favors 'group' acts
                    check_order = ["group", "bisexual"]
                elif girl.archetypes["The Courtesan"].unlocked and not girl.archetypes["The Escort"].unlocked: # Courtesan tree favors 'bisexual' acts
                    pass
                else: # Randomize if both trees are active, or none of them
                    renpy.random.shuffle(check_order)

                for check in check_order:

                    # Group girls may bring in up to 2 more customers
                    if check == "group":

                        if girl.does["group"] and _customers.index(cust) < len(_customers)-1:
                            if girl.get_effect("special", "group"): # Group has a random chance of triggering
                                c_list.append(_customers[_customers.index(cust)+1]) # gets the next customer in the queue

                                if girl.has_perk("Orgy") and _customers.index(cust) < len(_customers)-2:
                                    if girl.get_effect("special", "orgy"): # Orgy has a random chance of triggering
                                        c_list.append(_customers[_customers.index(cust)+2])

                                cust.group = len(c_list)
                                for c in c_list[1:]: # Sharing reason and preference between customers to avoid incoherences
                                    c.group = len(c_list)
                                    c.reason = cust.reason
                                    c.wants_sex_act = cust.wants_sex_act

                                break # This is needed to avoid group and bisexual proccing together (could be something to allow later)

                    # Bisexual girls may bring in a second bisexual girl
                    elif check == "bisexual":
                        if girl.does["bisexual"] and len(c_list) == 1:
                            if girl.get_effect("special", "bisexual"):  # Bis has a random chance of triggering
                                for girl2 in base_available_girls: # The second girl ncan be chosen from the larger pool regardless of rank/act
                                    if girl2 != girl and girl2.does["bisexual"] and girl2.does[sex_act]:
                                        g_list.append(girl2)
                                        game.mm_log += __(" She brought a friend (%s).") % girl2.fullname
                                        break

                                break # This is needed to avoid group and bisexual proccing together

                # Use interactions

                for girl in g_list:
                    spent_interactions = 1

                    # Uses 2 interactions if girl is working half a shift
                    spent_interactions *= (100//girl.workdays[calendar.get_weekday()])

                    # Uses 2 interactions if w&w
                    if girl.work_whore and girl.job in all_jobs:
                        spent_interactions *= 2

                    girl.interactions -= spent_interactions
                    game.mm_log += __(" (%s has spent %s interactions and has %s left)") % (girl.fullname, spent_interactions, girl.interactions)

                    if girl.interactions <= 0:
                        _whores.remove(girl) # Not strictly necessary, but shortens the next loop
                        game.mm_log += __(" (%s has no interactions left and was REMOVED)") % girl.fullname

                # Update _wh_list
                _wh_list.append([g_list, c_list, sex_act])

            # Prepare the next step
            _customers = list(leftover_customers)

        return _wh_list, leftover_customers


## Start settings
    def make_match_list_from_ent_dict(ent_dict, crazy_dict):
        match_list = []

        for girl, customers in ent_dict.items():
            for cust in customers:
                match_list.append((girl, cust, girl.job))

        for girl, customers in crazy_dict.items():
            for cust in customers:
                match_list.append((girl, cust, girl.job))

        return match_list

    def make_match_list_from_wh_list(wh_list, crazy_dict):
        match_list = []

        for girls, customers, act in wh_list:
            for cust in customers:
                match_list.append((girls[0], cust, act))

        for girl, customers in crazy_dict.items():
            for cust in customers:
                match_list.append((girl, cust, cust.wants_sex_act))

        return match_list


    def init_tax(): # Unique variables for the taxgirl NPC
        NPC_taxgirl.MC_income = 0
        NPC_taxgirl.old_MC_income = 0
        NPC_taxgirl.current_tax = 0
        NPC_taxgirl.time_pressure_modifier = 0.0
        NPC_taxgirl.active = False

    def calculate_tax(monthly_income): # Called once a month when announcing next tax

        monthly_income = NPC_taxgirl.MC_income

        # STEP 1: Check tax eligibility

        if monthly_income < tax_brackets[0][0] * 28:
            return 0 # You are too poor to pay taxes. Hurray?

        # STEP 2: Calculate raw tax

        previous_bracket = 0
        total = 0

        for bracket, rate in tax_brackets:
            bracket *= 28
            rate += tax_chapter_penalty[game.chapter] + game.get_diff_setting("tax rate")
            rate *= (1.0 + NPC_taxgirl.time_pressure_modifier) # Time pressure is applied as a multiplier, not an additive modifier

            if rate < 0: # Tax rate cannot be negative
                rate = 0
            if rate > 0.95: # Tax rate cannot exceed 95%
                rate = 0.95

            if monthly_income < bracket:
                total += (monthly_income - previous_bracket) * rate
                break
            else:
                total += (bracket - previous_bracket) * rate
                previous_bracket = bracket

        # STEP 3: Randomize expected sum

        total += total * (renpy.random.random() * 2 * tax_random_range - tax_random_range) # Will return a random float between +tax_random_range and -tax_random_range

        total = min(total, 0.95*monthly_income) # Hard cap on taxes: cannot exceed 95% of the previous income

        # Taxes under 250 gold will be ignored

        if total < 250:
            total = 0

        NPC_taxgirl.current_tax = int(total * MC.get_effect("boost", "taxes"))

        # STEP 4: Update counters and time pressure (once a month)

        if not NPC_taxgirl.flags["last tax"] or NPC_taxgirl.flags["last tax"] <= calendar.time - 28: # Sanity check
            if NPC_taxgirl.active and not NPC_taxgirl.flags["disable time pressure"]:
                if NPC_taxgirl.time_pressure_modifier < tax_time_pressure_maximum:
                    offset = game.get_diff_setting("tax rate") / 10 # Hardcoded for now, will be added to difficulty options eventually

                    NPC_taxgirl.time_pressure_modifier += 0.04 + offset # Increases tax rates by 2% to 6% per month, up to 20% max

                    if NPC_taxgirl.time_pressure_modifier > tax_time_pressure_maximum:
                        NPC_taxgirl.time_pressure_modifier = tax_time_pressure_maximum

            NPC_taxgirl.flags["last tax"] = calendar.time # Sanity check

        # BK Evolution: Update shop time pressure monthly
        global shop_time_pressure
        _max_tp = shop_time_pressure_settings.get("max_price_multiplier", 2.0) - 1.0
        _growth = shop_time_pressure_settings.get("price_growth_per_month", 0.02)
        if shop_time_pressure < _max_tp:
            shop_time_pressure += _growth
            if shop_time_pressure > _max_tp:
                shop_time_pressure = _max_tp

        return NPC_taxgirl.current_tax

    def pay_tax():

        if MC.gold < NPC_taxgirl.current_tax:
            return False
        else:
            MC.gold -= NPC_taxgirl.current_tax
            NPC_taxgirl.current_tax = 0
            NPC_taxgirl.flags["paid tax"] = True
            renpy.play(s_gold, "sound")
            return True


    def init_items():

        # Creates a ranked dictionary for all items

        game.items = defaultdict(list)

        for it in all_items:

            game.items[it.rarity].append(it)

            for dis in list(district_dict.values()) + [endless_district]:
                if it.min_rank <= dis.rank <= it.max_rank:
                    if it.rarity in ("U", "S"):
                        pass
                    elif it.rarity == "M":
                        dis.items["M"].append(it)
                    elif it.rarity == "F":
#                         dis.items["rare"].append(it)
                        dis.items["F"].append(it)
                    elif it.rarity < dis.rank:
                        dis.items["junk"].append(it)
                    elif it.rarity == dis.rank:
                        dis.items["common"].append(it)
                    elif it.rarity == dis.rank + 1:
                        dis.items["rare"].append(it)
                    elif it.rarity == dis.rank + 2:
                        dis.items["exceptional"].append(it)

#        list_district_items()

    def list_district_items():
        tlist = []

        for dis in district_dict.values() + [endless_district]:
            for qual in ("junk", "common", "rare", "exceptional"):
                tlist.append([__(dis.name) + " " + __(qual.capitalize()), and_text([say_name(it) for it in dis.items[qual]])])

        while tlist:
            name, itlist = tlist.pop(0)
            renpy.say(name, itlist)


    def get_rand_item(quality = "junk", rank = None, item_type = None, item_types = None): # Returns an instance of an item

        if rank != None: # Warning: rank can be '0'
            it = rand_choice(game.items[rank])

        elif item_types == ["Flower"]:
            it = rand_choice([it for it in district.items["F"] if it.type.name in item_types])

        elif item_types and item_types != "all":
            it = rand_choice([it for it in district.items[quality] if it.type.name in item_types])

        elif item_type:
            it = rand_choice([it for it in district.items[quality] if it.type.name == item_type.name])

        else:
            it = rand_choice(district.items[quality])

        if it:
            return it.get_instance()
        else:
            return False

    def update_NPC_items(n):

        n.items = []
        it = get_rand_item("rare")
        if it:
            n.items.append(it)

        return

    ## EN: Load customer rank lookup order from JSON (BK Evolution), fallback to hardcoded.
    ## ZH: 从 JSON 加载顾客等级查找优先级（BK Evolution），否则使用硬编码。
    _rl_json = DataLoader.load_rank_lookup()
    if _rl_json:
        rank_lookup_dict = {int(k): v for k, v in _rl_json["rank_lookup_dict"].items()}
    else:
        rank_lookup_dict = {1 : [2, 3, 4, 5], 2 : [3, 1, 4, 5], 3 : [4, 2, 5, 1], 4 : [5, 3, 2, 1], 5 : [4, 3, 2, 1]}

    ## EN: Load sex act short descriptions from JSON (BK Evolution), fallback to hardcoded.
    ## ZH: 从 JSON 加载性行为简短描述（BK Evolution），否则使用硬编码。
    ## NOTE: Must be in init python (not init -3) because get_i18n is defined at init 0.
    pass

init -3 python:

    def crazy_customer(girls, customers):

        crazy_changes = NightChangeLog("Security alert", col=c_lightred)

    ## Tests for violence and arson attempts (returns event if True)

        girl = rand_choice(girls)
        for cust in customers:

            if cust.crazy == "violent":

                notify(_("%s: Assault attempt") % girl.fullname, pic=girl.portrait)
                crazy_changes.add("Assault attempt", "header")

                violent_text = __("%s went berserk and attacked %s all of a sudden!") % (cust.name, girl.name)
                violent_report = __("Security alert! Violent customer.")

                if brothel.get_risk() < 0: # Your guards on duty are ready to help
#                   reward = (cust.diff  + dice(cust.diff)) * district.rank
                    violent_text += __("\n{color=[c_green]}Fortunately, your security is close at hand. They quickly gang up on him and proceed to beat the crap out of his sorry ass.\n{/color}Your girl is safe, and you pocket the content of his wallet: %s gold.") % str(cust.ent_budget)
                    violent_report = __("{color=[c_green]}%s Your guards beat him up (%s gold earned).{/color}") % (violent_report, str(cust.ent_budget))
                    MC.gold += cust.ent_budget
                    girl.change_mood(1)
                    girl.change_fear(-1)

                    pic = Picture(path="resources/events/" + rand_choice(security_pics["girl defense"]))

                    crazy_changes.add(__("Averted by security ({image=img_gold} +%i)") % cust.ent_budget, col="good", ttip = event_color["good"] % __("Mood +, Fear -"))

                elif MC.can_defend() and MC.get_defense() > girl.get_defense(): # Your guards are somewhere else, your girl is helpless, it's your turn to take action!
                    if have_fight(cust, MC) == False:
                        violent_text += __("\n{color=[c_green]}You rush to the scene and break the guy's face before he has any time to act.\n{/color}Your girl is safe, and you pocket the content of his wallet: %s gold.") % str(cust.ent_budget)
                        violent_report = __("{color=[c_green]}%s You beat him up (%s gold earned).{/color}") % (violent_report, str(cust.ent_budget))
                        girl.change_mood(1)
                        girl.change_fear(-2)
                        girl.change_love(1)
                        MC.gold += cust.ent_budget

                        pic = Picture(path="resources/events/" + rand_choice(security_pics["girl defense"]))

                        crazy_changes.add(_("Averted by you ({image=img_gold} +%i)") % cust.ent_budget, col="good", ttip = event_color["good"] % _("Mood +, Love +, Fear --"))

                    elif girl.test_shield():
                        violent_text += __(" She was protected by a magic shield.")
                        girl.change_mood(1)

                        pic = Picture(path="resources/events/" + rand_choice(security_pics["girl shield"]))

                        crazy_changes.add(_("Averted by Magic Shield"), col="good", ttip = event_color["good"] % _("Mood +"))

                    elif girl.get_effect("special", "immune"):
                        violent_text += __(" But she is immune to physical attacks.")
                        girl.change_mood(1)

                        pic = Picture(path="resources/events/" + rand_choice(security_pics["girl shield"]))

                        crazy_changes.add(_("Averted by Immunity"), col="good", ttip = event_color["good"] % _("Mood +"))

                    else:
                        violent_text += __("\n{color=[c_red]}You try to help her but the bastard knocks you to the ground and beats up the both of you.\n{/color}%s is hurt, and you lose some self-respect.") % girl.name
                        wounds = girl.get_hurt(dice(3)+1)

                        girl.track_event("hurt", "a violent customer")

                        violent_report = __("{color=[c_red]}%s He beat you up and %s is hurt.{/color} ") % (violent_report, girl.name)
                        girl.change_mood(-2)
                        girl.change_fear(2)
                        girl.change_love(-1)

                        pic = Picture(path="resources/events/" + rand_choice(violent_pics))

                        crazy_changes.add(_("Security failure"), col="bad", ttip = event_color["bad"] % _("Mood --, Love -, Fear ++"))
                        crazy_changes.add(girl.fullname + __(" hurt for %i day%s") % (wounds, plural(wounds)), col="very bad")

                    MC.interactions -= 1

                else: # Your girl must defend herself!

                    mod = 0

                    if girl.remembers("reward", "defended") or girl.remembers("punish", "hurt"):
                        mod = 1
                    elif girl.remembers("punish", "defended"):
                        mod = -1

                    if girl.get_defense() + mod >= cust.get_defense():
                        defense_action = rand_choice([__("She stabs the poor sod in the guts, stopping him right in his tracks."),
                                        __("She knees the bastard right in the balls and he crumbles on the floor crying."), __("She kicks him right in the face, knocking him out for good.")])
                        violent_text += __("\n{color=[c_green]}Your girl has the means to defend herself, however. %s\n{/color}Your girl is safe, and you pocket the content of his wallet while your henchmen throw the poor sucker out in a dark alley: %s gold.") % (defense_action, str(cust.ent_budget))

                        violent_report = __("{color=[c_green]}%s %s beat him up (%s gold earned).{/color}") % (violent_report, girl.name, str(cust.ent_budget))

                        girl.track_event("defended")

                        girl.change_mood(1)
                        girl.change_fear(-1)
                        MC.gold += cust.ent_budget

                        pic = girl.get_pic("fight", strict=True, naked_filter=True, soft=True)

                        if not pic:
                            pic = girl.get_pic("fight", strict=True)
                            if not pic:
                                pic = Picture(path="resources/events/" + rand_choice(security_pics["default girl fight"]))

                        crazy_changes.add(_("Averted by herself"), col="good", ttip = event_color["good"] % _("Mood +, Fear -"))

                    elif girl.test_shield():
                        violent_text += __(" She was protected by a magic shield.")
                        girl.change_mood(1)

                        pic = Picture(path="resources/events/" + rand_choice(security_pics["girl shield"]))

                        crazy_changes.add(_("Averted by Magic Shield"), col="good", ttip = event_color["good"] % _("Mood +"))

                    elif girl.get_effect("special", "immune"):
                        violent_text += __(" But she is immune to physical attacks.")
                        girl.change_mood(1)

                        pic = Picture(path="resources/events/" + rand_choice(security_pics["girl shield"]))

                        crazy_changes.add(_("Averted by Immunity"), col="good", ttip = event_color["good"] % _("Mood +"))

                    else:
                        violent_text += __("\n{color=[c_red]}Your girl tried to defend herself but he is stronger, kicking her to ground and pummeling her with his fists.\n{/color}You finally throw him out, but %s is hurt.") % girl.name
                        girl.get_hurt(dice(3)+1)
#                         girl.add_log("hurt_days")

                        girl.track_event("hurt", "a violent customer")

                        violent_report = __("{color=[c_red]}%s %s is hurt.{/color}") % (violent_report, girl.name)
                        girl.change_mood(-2)
                        girl.change_fear(2)

                        pic = girl.get_pic("hurt", naked_filter=True, soft=True, strict=True)
                        if not pic:
                            pic = girl.get_pic("hurt", strict=True)
                            if not pic:
                                pic = Picture(path="resources/events/" + rand_choice(violent_pics))

                        crazy_changes.add("Security failure", col="bad", ttip = event_color["bad"] % "Mood --, Fear ++")

                log.add_report(violent_report)

                cust.crazy = "finished" # Prevents craziness from triggering twice

                return Event(pic, text = violent_text, sound = s_punch, with_st = vpunch, changes=crazy_changes), cust

            elif cust.crazy == "arsonist":

                notify(_("%s: Arson attempt") % brothel.name)
                crazy_changes.add("Arson attempt", "header", col="bad")

                arson_text = ""
                arson_report = __("Security alert! Fire started.")
                arson = False

                if brothel.get_risk() < 0: # Your guards on duty are ready to help
                    arson_text += __("%s tried to set fire to your brothel!\n{color=[c_green]}Your guards tackled him and fucked him up before he could light a match.{/color}") % cust.name
                    arson_report = __("{color=[c_green]}%s Your guards stopped it.{/color}") % arson_report

                elif MC.can_defend(): # Your guards are somewhere else, it's your turn to take action!
                    if have_fight(cust, MC) == False:
                        arson_text += __("%s tried to set fire to your brothel!\n{color=[c_green]}You were patrolling as it happened, and knocked the wretch senseless before he could carry out his plan.{/color}") % cust.name
                        arson_report = __("{color=[c_green]}%s You stopped it.{/color}") % arson_report
                    else:
                        arson_text += __("%s tried to set fire to your brothel!\n{color=[c_red]}You tried to stop him but he fought you like a madman, allowing time for the flames to grow high.{/color}") % cust.name
                        arson_report = __("{color=[c_red]}%s You were beaten and the brothel caught fire.{/color}") % arson_report
                        arson = True
                    MC.interactions -= 1

                else: # No one is here to help out
                    arson_text += __("{color=[c_red]}%s has set fire to your brothel!\nYou hear your girls yell, and soon see the smoke rising from your burning estate.{/color}") % cust.name
                    arson_report = __("{color=[c_red]}%s The bro- The bro- The brothel's on fire!{/color}") % arson_report
                    arson = True

                if arson:
                    if MC.playerclass == "Wizard":
                        damage = dice(25) + 25 - 5 * MC.get_spirit()
                        if damage < 0:
                            damage = 0

                        arson_text += __("\nGathering the power of the Storm, you quickly cast a raining spell. In the end, damage is limited. Your brothel condition deteriorates by %s.") % str(damage)
                        brothel.change_dirt(damage)

                    else:
                        damage = dice(25) + 25
                        arson_text += __("\nYou work together with your staff and some helpful customers to extinguish the flames. Alas, the place has been badly damaged. Your brothel condition deteriorates by %s.") % str(damage)
                        brothel.change_dirt(damage)

                pic = rand_choice(arson_pics)

                log.add_report(arson_report)

                cust.crazy = "finished" # Prevents craziness from triggering twice

                return Event(Picture(pic, "resources/events/" + pic), text = arson_text, sound = s_fire, with_st = vpunch, changes=crazy_changes), cust

        return False, False


    def rape_attempt(girl, cust, threat, change_log):

        notify(_("%s: Rape attempt") % girl.fullname, pic=girl.portrait)

        text_descript = _(" Even though she refused, the customer tried to force her to do it. ")
        raped = False

        change_log.add(_("Rape attempt"), "header")

        if brothel.get_security() >= threat: #You have enough guards to look after your girls
            text_descript += girl.name + " {color=[c_green]}called security. He apologized and decided to play nice.{/color}"

            girl.change_mood(1)
            girl.change_fear(-1)

            change_log.add("Averted by security", col="good", ttip = event_color["good"] % "Mood +, Fear -")

        elif MC.can_defend() and MC.get_defense() > girl.get_defense(): #You don't have enough guards but the Player is available and tougher than your girl

            if MC.get_defense() >= cust.get_defense():

                text_descript += "{color=[c_green]}You heard %s crying for help and threatened to throw him out. He decided to play nice.{/color}" % girl.name

                girl.change_mood(1)
                girl.change_love(1)
                girl.change_fear(-2)

                change_log.add("Averted by you", col="good", ttip = event_color["good"] % "Mood +, Love +, Fear -")

            elif girl.test_shield():

                text_descript += "Fortunately, her magic shield protected her. The customer was awed and sheepishly agreed to back off."

                girl.change_mood(1)

                change_log.add("Averted by Magic Shield", col="good", ttip = event_color["good"] % "Mood +")

            else:
                text_descript += "{color=[c_red]}You tried to help, but the customer knocked you out and locked the door shut.{/color}"
                raped = True

                girl.change_mood(-3)
                girl.change_love(-1)
                girl.change_fear(3)

                change_log.add("Security failure", col="very bad", ttip = event_color["bad"] % "Mood --, Love -, Fear ++")

            MC.interactions -= 1

        else: #You don't have enough guards and the Player is not available or weaker than your girl: she's on her own

            # May get a boost of debuff from past interactions with MC

            mod = 0

            if girl.remembers("reward", "defended") or girl.remembers("punish", "hurt"):
                mod = 1
            elif girl.remembers("punish", "defended"):
                mod = -1

            if girl.get_defense() + mod >= cust.get_defense():

                text_descript += "{color=[c_green]}%s told him he could play nice or lose an important body part. He changed his mind.{/color}" % girl.name

                girl.track_event("defended")
                girl.change_mood(1)

                change_log.add("Averted by herself", col="good", ttip = event_color["good"] % "Mood +")

            elif girl.test_shield():

                text_descript += "Fortunately, her magic shield protected her. The customer was awed and sheepishly agreed to back off."
                girl.change_mood(1)

                change_log.add("Averted by Magic Shield", col="good", ttip = event_color["good"] % "Mood +")

            else:

                text_descript += "{color=[c_red]}%s tried to fight him to no avail, and he had his way with her.{/color}" % girl.name
                raped = True

                girl.change_mood(-3)
                girl.change_fear(3)

                change_log.add("Security failure", col="very bad", ttip = event_color["bad"] % "Mood --, Fear ++")

        return raped, text_descript

init -1 python:
    ## EN: Load sex act short descriptions from JSON (BK Evolution), fallback to hardcoded.
    ## ZH: 从 JSON 加载性行为简短描述（BK Evolution），否则使用硬编码。
    ## NOTE: Uses manual _i18n fallback instead of get_i18n() to avoid init-order dependency.
    _sdes_json = DataLoader.load_sex_act_descriptions()
    if _sdes_json:
        _sdes_data = _sdes_json["s_des"]
        s_des = {}
        for _k in ["naked", "service", "sex", "anal", "fetish"]:
            s_des[_k] = _sdes_data.get(_k + "_i18n", _sdes_data.get(_k, _k))
    else:
        s_des = {"naked" : "strip naked for him", "service" : "take care of his cock", "sex" : "have sex with him", "anal" : "let him fuck her ass", "fetish" : "do kinky stuff with him"}

