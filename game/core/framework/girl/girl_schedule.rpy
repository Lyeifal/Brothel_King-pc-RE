#### GirlSchedule — Job and workday management | 日程与工作管理 ####
# Phase 2.1: Schedule, job assignment, workdays, status display.
# 日程、工作分配、工日、状态显示
# ★ get_status / get_status_summary — 已从 girlclass.rpy 移入
# Methods: set_workdays, set_job, works_today, get_schedule, etc.

init -2 python:

    class GirlSchedule(object):
        """Schedule and job management for a Girl.

        Each method delegates to the Girl's _impl alias, which points to
        the original implementation in girlclass.rpy.
        """

        def __init__(self, girl):
            self.girl = girl

        def set_workdays(self):
            return self.girl._set_workdays_impl()

        def cycle_workday(self, day, reverse=False):
            return self.girl._cycle_workday_impl(day, reverse)

        def set_job(self, job, forced=False):
            return self.girl._set_job_impl(job, forced)

        def set_rest(self):
            return self.girl._set_rest_impl()

        def works_today(self, check_autorest=False):
            return self.girl._works_today_impl(check_autorest)

        def will_do(self, job, silent=False):
            return self.girl._will_do_impl(job, silent)

        def get_schedule(self):
            return self.girl._get_schedule_impl()

        def load_schedule(self, schedule):
            return self.girl._load_schedule_impl(schedule)

        # ── Status display (implementations moved from girlclass.rpy) ──

        def get_status(self):
            """Return a list of (picture_name, tooltip) tuples for UI badges."""
            g = self.girl
            status_list = []

            if g.away and persistent.show_girl_status["away"]:
                status_list.append(["away.webp", __("%s is {b}away{/b} on a class or quest for %s more day%s.") % (g.fullname, str(g.return_date - calendar.time), plural(g.return_date - calendar.time))])

            elif g in farm.girls and persistent.show_girl_status["farm"]:
                try:
                    if farm.programs[g].target == "no training":
                        if farm.programs[g].holding == "rest":
                            status_list.append(["rest.webp", __("%s is {b}resting{/b} in her pen today.") % g.fullname])
                        else:
                            status_list.append(["farm.webp", __("%s is being trained at the {b}farm{/b} (%s training).") % (g.fullname, farm.programs[g].holding)])
                    else:
                        status_list.append(["farm.webp", __("%s is being trained at the {b}farm{/b} (%s training).") % (g.fullname, farm.programs[g].target)])
                except:
                    farm.programs[g] = FarmProgram(g)

            elif (g.resting or not g.job or not g.works_today()) and not g.exhausted:
                if g.workdays[calendar.get_weekday()] > 0 and persistent.show_girl_status["scheduled"]:
                    status_list.append(["scheduled.webp", __("%s is {b}resting{/b} today as scheduled.") % g.fullname])
                elif persistent.show_girl_status["rest"]:
                    status_list.append(["rest.webp", __("%s is {b}resting{/b} today.") % g.fullname])

            elif g.energy <= autorest_limit[g] and g.energy < g.get_stat_max("energy"):
                status_list.append(["autorest.webp", __("%s's energy is low. She will be automatically sent to {b}rest{/b} today.") % g.fullname])

            elif g.works_today() == 50 and persistent.show_girl_status["half-shift"]:
                status_list.append(["half.webp", __("%s is working a {b}half-shift{/b} today.") % g.fullname])

            if g in brothel.master_bedroom.girls and persistent.show_girl_status["master bedroom"]:
                status_list.append(["master.webp", __("%s is set to train in the {b}master bedroom{/b}.") % g.fullname])

            if g.ready_to_rank():
                status_list.append(["rankup.webp", __("%s is ready to {b}rank up{/b}.") % g.fullname])

            if g.can_perk or g.can_spend_upgrade_points():
                status_list.append(["levelup.webp", __("%s is ready to {b}level up{/b}.") % g.fullname])

            if g.hurt > 0:
                if g.hurt <= 1:
                    status_list.append(["hurt.webp", __("%s is {b}hurt or sick{/b} and will need to rest for 1 more day before she can do anything.") % g.fullname])
                else:
                    status_list.append(["hurt.webp", __("%s is {b}hurt or sick{/b} and will need to rest for %s more days until she can do anything.") % (g.fullname, str(round_int(g.hurt)))])

            elif g.exhausted:
                status_list.append(["tired.webp", __("%s is {b}tired{/b} and needs to be fully rested until she can work again.") % g.fullname])

            if persistent.show_girl_status["work&whore"] and g.works_today() and g.work_whore and g in MC.girls:
                status_list.append(["ww.webp", __("%s is {b}working and whoring{/b} today.") % g.fullname])

            if persistent.show_girl_status["not work&whore"] and g.works_today() and not g.work_whore and g in MC.girls:
                status_list.append(["not_ww.webp", __("%s is not {b}working and whoring{/b}.") % g.fullname])

            if g.naked and persistent.show_girl_status["naked"]:
                if g.get_effect("special", "naked"):
                    status_list.append(["naked.webp", __("%s will remain {b}naked{/b} at all times.") % g.fullname])
                else:
                    status_list.append(["naked2.webp", __("%s will remain {b}naked{/b} today.") % g.fullname])

            if not g.naked and persistent.show_girl_status["not naked"]:
                status_list.append(["not_naked.webp", __("%s is not {b}naked{/b} (and that's a problem for you, apparently).") % g.fullname])

            if [fix.name for fix in g.neg_fixations if g.personality_unlock[fix.name]] and persistent.show_girl_status["negative fixation"]:
                status_list.append(["negfix.webp", __("You know that %s has a {b}negative fixation{/b}.") % g.fullname])

            return status_list

        def get_status_summary(self):
            """Return a short text summary of girl status for tooltips."""
            g = self.girl
            r = ""

            if g.ready_to_rank():
                r += "\n" + __("Ready to {b}rank up{/b}")
            if g.can_perk or g.can_spend_upgrade_points():
                r += "\n" + __("Ready to {b}level up{/b}")

            if g.hurt > 0:
                r += "\n" + __("{b}Hurt{/b} for %s day%s") % (round_up(g.hurt), plural(round_up(g.hurt)))

            elif g.exhausted:
                r += "\n" + __("{b}Exhausted{/b}")

            if g.away:
                r += "\n" + __("{b}Away{/b} on a class or quest for %s day%s") % (str(g.return_date - calendar.time), plural(g.return_date - calendar.time))
            elif g in farm.girls:
                r += "\n" + __("Training at the {b}farm{/b}")
            elif g.resting or not g.job or not g.works_today():
                r += "\n" + __("{b}Resting today{/b}")
            elif g.works_today() == 50:
                r += "\n" + __("{b}Half-shift{/b}")

            if g.work_whore:
                r += "\n" + __("{b}Working and whoring{/b}")

            if g.naked:
                r += "\n" + __("{b}Naked{/b}")

            if [fix.name for fix in g.neg_fixations if g.personality_unlock[fix.name]]:
                r += "\n" + __("Has a {b}negative fixation{/b}")

            return r

        def get_day_off(self, day_nb):
            return self.girl._get_day_off_impl(day_nb)

        def tired_check(self):
            return self.girl._tired_check_impl()
