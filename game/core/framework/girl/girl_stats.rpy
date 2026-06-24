#### GirlStats — Stat management component ####
# Phase 2.1: Stats, stat caps, stat changes, spillover, JP/XP/REP management.
# Methods to migrate: generate_stats, find_stat, get_stat, average_stats,
# test_stats, raise_stats, can_upgrade_stat, upgrade_stat, get_stat_max,
# get_stat_minmax, stat_spillover, change_stat, set_stat, average_skills,
# get_xp_cap, get_jp_cap, get_rep_cap.

init -2 python:

    class GirlStats(object):
        """Stat management for a Girl. Delegates to _impl methods on Girl."""

        def __init__(self, girl):
            self.girl = girl

        def generate_stats(self, sex=False):
            return self.girl._generate_stats_impl(sex)
        def find_stat(self, stat_name):
            return self.girl._find_stat_impl(stat_name)
        def get_stat(self, stat_name, raw=False):
            return self.girl._get_stat_impl(stat_name, raw)
        def average_stats(self, stats):
            return self.girl._average_stats_impl(stats)
        def test_stats(self, stats=None, diff=0, advanced_stats=None):
            return self.girl._test_stats_impl(stats, diff, advanced_stats)
        def raise_stats(self, stats, silent=False):
            return self.girl._raise_stats_impl(stats, silent)
        def can_upgrade_stat(self, stat):
            return self.girl._can_upgrade_stat_impl(stat)
        def upgrade_stat(self, stat, chg, silent=True):
            return self.girl._upgrade_stat_impl(stat, chg, silent)
        def get_stat_max(self, stat_name, raw=False, custom_cap=None):
            return self.girl._get_stat_max_impl(stat_name, raw, custom_cap)
        def get_stat_minmax(self, stat_name, raw=False, custom_cap=None):
            return self.girl._get_stat_minmax_impl(stat_name, raw, custom_cap)
        def stat_spillover(self, stat, chg, job=None):
            return self.girl._stat_spillover_impl(stat, chg, job)
        def change_stat(self, stat, chg, apply_boost=True, spillover=True, custom_cap=None, silent=False, notify_prefix="", notify_suffix=""):
            return self.girl._change_stat_impl(stat, chg, apply_boost, spillover, custom_cap, silent, notify_prefix, notify_suffix)
        def set_stat(self, stat, val):
            return self.girl._set_stat_impl(stat, val)
        def average_skills(self, sk_list, mod=1.0):
            return self.girl._average_skills_impl(sk_list, mod)
        def get_xp_cap(self):
            return self.girl._get_xp_cap_impl()
        def get_jp_cap(self, job="all"):
            return self.girl._get_jp_cap_impl(job)
        def get_rep_cap(self):
            return self.girl._get_rep_cap_impl()
        def adjust_level(self, level):
            return self.girl._adjust_level_impl(level)
