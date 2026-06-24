#### GirlSchedule — Job and workday management component ####
# Phase 2.1: Schedule, job assignment, workdays, status display.
# Methods to migrate: set_workdays, cycle_workday, set_job, set_rest,
# works_today, will_do, get_schedule, load_schedule, get_status,
# get_status_summary, get_day_off, tired_check.

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

        def get_status(self):
            return self.girl._get_status_impl()

        def get_status_summary(self):
            return self.girl._get_status_summary_impl()

        def get_day_off(self, day_nb):
            return self.girl._get_day_off_impl(day_nb)

        def tired_check(self):
            return self.girl._tired_check_impl()
