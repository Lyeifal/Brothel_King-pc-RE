#### GirlStats — Stat management component ####
# Phase 2.1: Stats, stat caps, stat changes, spillover, JP/XP/REP management.
# Methods to migrate: generate_stats, find_stat, get_stat, average_stats,
# test_stats, raise_stats, can_upgrade_stat, upgrade_stat, get_stat_max,
# get_stat_minmax, stat_spillover, change_stat, set_stat, average_skills,
# get_xp_cap, get_jp_cap, get_rep_cap.

init -2 python:

    class GirlStats(object):
        """Stat management for a Girl."""

        def __init__(self, girl):
            self.girl = girl
