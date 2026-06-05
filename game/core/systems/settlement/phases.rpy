## BK Phase 6 — Settlement Phase Handlers
## Modular settlement phases extracted from endday.rpy.
## Each handler operates on a SettlementContext and can be intercepted by Mods.

init -2 python:

    # ───────────────────────────────────────────────
    # Phase 1: Girl categorization
    # ───────────────────────────────────────────────
    def phase_categorize_girls(context):
        """
        Categorize all girls into working/striking/resting/sick/away/job/whore.
        Populates the corresponding lists in SettlementContext.
        """
        context.working_girls = []
        context.striking_girls = []
        context.resting_girls = []
        context.away_girls = []
        context.sick_girls = []
        context.job_girls = []
        context.whores = []

        for girl in MC.girls:
            if girl.works_today():
                # Autorest check
                if girl.energy <= autorest_limit[girl] and girl.energy < girl.get_stat_max("energy"):
                    if context.log:
                        context.log.add_report("{color=[c_red]}" + girl.fullname + " was under the energy threshold and was set to rest automatically.{/color}")
                    context.resting_girls.append(girl)
                    girl.add_log("rest_days")

                # Health check
                elif girl.health_check() == "sick":
                    context.sick_girls.append(girl)
                    girl.add_log("sick_days")

                else:
                    # Sanity check: whore must do something
                    if girl.job == "whore" and not girl.does_anything():
                        renpy.say("", "[girl.fullname] cannot work as a whore as she refuses to do any sex act.")
                        context.striking_girls.append(girl)
                        girl.add_log("work_days", -1)
                        girl.add_log("rest_days")

                    elif girl.obedience_check():
                        girl.add_log("work_days")
                        context.working_girls.append(girl)

                        if girl.job == "whore":
                            context.whores.append(girl)
                            girl.add_log("whore_days")
                        elif girl.work_whore and girl.does_anything():
                            context.job_girls.append(girl)
                            context.whores.append(girl)
                            girl.add_log("work_whore_days")
                        else:
                            context.job_girls.append(girl)
                            girl.add_log(girl.job + "_days")
                    else:
                        context.striking_girls.append(girl)
                        girl.track_event("disobey", arg=girl.job)
                        girl.add_log("strike_days")

            elif girl.away:
                context.away_girls.append(girl)
                girl.add_log("away_days")

            else:
                if girl.farm or girl.job == "farm":
                    girl.set_job(None)
                context.resting_girls.append(girl)
                girl.add_log("rest_days")

        renpy.random.shuffle(context.job_girls)
        renpy.random.shuffle(context.whores)

        # Sync back to context lists expected by legacy code
        context.working_girls = context.job_girls + context.whores
        # Remove duplicates while preserving order
        seen = set()
        uniq = []
        for g in context.working_girls:
            if g not in seen:
                seen.add(g)
                uniq.append(g)
        context.working_girls = uniq

    # ───────────────────────────────────────────────
    # Phase 2: Customer generation
    # ───────────────────────────────────────────────
    def phase_generate_customers(context):
        """Generate customers and apply brothel cleanliness penalties."""
        context.customers, context.cust_text, context.cust_nb_dict = generate_customers(brothel.rep, use_adv=len(context.working_girls))

        # Cleanliness check
        context.turned_away = 0
        context.maint_text = ""

        if context.working_girls:
            cleanliness = brothel.get_cleanliness()

            if cleanliness == "dusty":
                context.turned_away = (dice(2, district.rank) - 1)
                context.maint_text = "\nYour brothel is getting dusty. There are cobwebs in the rooms."
            elif cleanliness == "dirty":
                context.turned_away = dice(3, district.rank)
                context.maint_text = "\nYour brothel is getting dirty. Sill thinks she saw a rat."
            elif cleanliness == "disgusting":
                context.turned_away = dice(6, district.rank)
                context.maint_text = "\nThis place is a disgusting mess. Customers are turning away and girls are getting sick!"

            if context.turned_away > 0:
                if context.turned_away < len(context.customers):
                    lost = context.customers[:context.turned_away]
                    context.customers = context.customers[context.turned_away:]
                else:
                    lost = list(context.customers)
                    context.customers = []

                rep_loss = -sum(c.rank for c in lost)
                rep_loss = brothel.change_rep(rep_loss)
                if not context.customers:
                    text1 = "Your brothel was so dirty that all %s customers ran away (%s reputation)" % (str(len(lost)), str_int(rep_loss))
                else:
                    text1 = "%s customers turned away because the brothel looked filthy (%s reputation)" % (str(len(lost)), str_int(rep_loss))
                context.maint_text += "\n" + text1
                if context.log:
                    context.log.add_report(event_color["bad"] % text1)
                context.lost_customers = lost
                context.rep_loss = rep_loss
            else:
                context.lost_customers = []
                context.rep_loss = 0

    # ───────────────────────────────────────────────
    # Phase 3: Income calculation
    # ───────────────────────────────────────────────
    def phase_calculate_income(context):
        """Calculate nightly income, costs, and net profit."""
        if not context.log:
            return

        log = context.log

        # Upkeep
        log.upkeep = 0
        free_girl = None
        if MC.get_effect("special", "free upkeep"):
            free_girl = rand_choice(MC.girls)

        for girl in MC.girls:
            if girl != free_girl:
                log.upkeep += girl.upkeep * girl.get_effect("boost", "total upkeep")
                girl.add_log("upkeep", girl.upkeep * girl.get_effect("boost", "total upkeep"))

        for girl in farm.girls:
            log.upkeep += girl.get_med_upkeep() * girl.get_effect("boost", "total upkeep") // 4
            girl.add_log("upkeep", girl.get_med_upkeep() * girl.get_effect("boost", "total upkeep") // 4)

        # Brothel costs
        if context.working_girls:
            log.costs = brothel.get_adv_cost() + brothel.get_sec_cost() + brothel.get_maintenance_cost()
        else:
            log.costs = brothel.get_maintenance_cost()

        # Loan payment
        loan_payment = MC.repay_loan()
        if loan_payment:
            log.costs += loan_payment

        # Income bonus/penalty
        bonus = log.gold_made * min((brothel.get_effect("boost", "income") - 1, 2.0))
        log.gold_made += bonus

        # Street whores
        street_gold = sum(g.whore_on_street() for g in MC.street_girls)
        log.gold_made += street_gold

        log.net = round_int(log.gold_made - log.upkeep - log.costs)
        MC.gold += log.net
        NPC_taxgirl.MC_income += (log.net * brothel.get_effect("boost", "taxable net income"))

        context.income = log.gold_made
        context.upkeep = log.upkeep
        context.costs = log.costs
        context.net = log.net
        context.bonus = bonus
        context.street_gold = street_gold
        context.loan_payment = loan_payment

    # ───────────────────────────────────────────────
    # Phase 4: Level up and skill catch-up
    # ───────────────────────────────────────────────
    def phase_levelup(context):
        """Process girl level-ups, job-ups, and skill catch-up."""
        context.leveled = []
        context.jobbed = []
        context.catch_up_changes = []

        for girl in MC.girls:
            if not girl.away or girl.hurt or girl.exhausted:
                if girl.get_effect("special", "skill catch up") and len(MC.girls) > 1:
                    target_girls = rand_choice([g for g in MC.girls if g != girl], girl.rank)
                    girl_changes = []
                    for girl2 in target_girls:
                        girl2_changes = []
                        for stat in gstats_main + gstats_sex:
                            if girl.get_stat(stat, raw=True) >= girl2.get_stat(stat, raw=True) + 1:
                                if dice(250) > girl2.get_stat(stat, raw=True):
                                    girl2.change_stat(stat, 1, silent=True)
                                    girl2_changes.append(stat)
                        if girl2_changes:
                            girl_changes.append([girl2, girl2_changes])
                    if girl_changes:
                        context.catch_up_changes.append([girl, girl_changes])

            if girl.ready_to_level():
                girl.level_up()
                context.leveled.append(girl)

            for act in [girl.job] + all_sex_acts:
                if girl.ready_to_job_up(act):
                    girl.job_up(act)
                    context.jobbed.append(girl)

    # ───────────────────────────────────────────────
    # Phase 5: Morning preparation
    # ───────────────────────────────────────────────
    def phase_morning_prep(context):
        """Run morning checks: runaway, tired, farm exit, portrait refresh."""
        context.exit_girls = []

        # Runaway checks
        for girl in MC.girls:
            check = girl.run_away_check()
            girl.ran_away_counter += 1
            if check == "runaway" and girl not in context.away_girls:
                girl.ran_away_counter = 0
                renpy.call("run_away", girl)
                girl.add_log("run_away", delay=-1)
            elif check == "warning":
                renpy.say(sill, "Warning! [girl.fullname] is unhappy and grumbling about running away...")

        # Tired checks
        for girl in MC.girls:
            if girl.tired_check():
                renpy.say(sill, "Warning! [girl.fullname] is getting tired...")
                if dice(6) >= 6:
                    calendar.set_alarm(calendar.time, Event(label="too_tired", object=girl))

        # Farm exit
        if farm.active:
            for girl in farm.girls:
                if farm.test_exit_conditions(girl):
                    context.exit_girls.append(girl)

        # Portrait refresh
        for girl in MC.girls:
            girl.refresh_pictures(silent=True)

    # ───────────────────────────────────────────────
    # Phase 6: Mood and interaction reset
    # ───────────────────────────────────────────────
    def phase_end_night(context):
        """Reset interactions, update mood, love/fear decay."""
        MC.reset_interactions()

        all_girls = MC.girls + game.free_girls + farm.girls + MC.escaped_girls
        for girl in all_girls:
            girl.reset_interactions()
            girl.refresh_spoil_terrify_points()

        for girl in MC.girls + farm.girls:
            if girl not in context.away_girls:
                girl.update_mood(resting=girl in (context.striking_girls + context.resting_girls))

                # Love/fear revert to mean
                if girl.get_love() > 0:
                    girl.change_love(-0.2)
                else:
                    girl.change_love(0.2)

                if girl.get_fear() > 0:
                    girl.change_fear(-0.2)
                else:
                    girl.change_fear(0.2)

                # Daily love/fear effects
                girl.change_love(girl.get_effect("change", "love per day"))
                girl.change_fear(girl.get_effect("change", "fear per day"))

    # ───────────────────────────────────────────────
    # Registration
    # ───────────────────────────────────────────────
    def _register_default_settlement_phases():
        settlement_pipeline.register_phase("categorize_girls", phase_categorize_girls, order=10)
        settlement_pipeline.register_phase("generate_customers", phase_generate_customers, order=20)
        settlement_pipeline.register_phase("calculate_income", phase_calculate_income, order=80)
        settlement_pipeline.register_phase("levelup", phase_levelup, order=90)
        settlement_pipeline.register_phase("end_night", phase_end_night, order=100)
        settlement_pipeline.register_phase("morning_prep", phase_morning_prep, order=110)

    _register_default_settlement_phases()
