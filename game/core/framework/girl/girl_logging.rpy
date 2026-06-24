#### GirlLogging — Event logging and tracking | 日志与追踪组件 ####
# Phase 2.1: Logging, stats tracking, memory, event history.
# 日志、属性追踪、记忆、事件历史
# Methods to migrate: commit, return_from, add_log, get_log, get_average_performance,
# track_event, get_recent_events, get_recent_events_description, count_occurences.

init -2 python:

    class GirlLogging(object):
        """Event logging and tracking for a Girl. Delegates to _impl methods."""

        def __init__(self, girl):
            self.girl = girl

        def commit(self, quest):
            return self.girl._commit_impl(quest)
        def return_from(self, quest):
            return self.girl._return_from_impl(quest)
        def add_log(self, root, v=1, _delay=0):
            return self.girl._add_log_impl(root, v, _delay)
        def get_log(self, root, days=0):
            return self.girl._get_log_impl(root, days)
        def get_average_performance(self, root, days):
            return self.girl._get_average_performance_impl(root, days)
        def track_event(self, type, arg=None, silent=False):
            return self.girl._track_event_impl(type, arg, silent)
        def get_recent_events(self, day_number=7, filter=None):
            return self.girl._get_recent_events_impl(day_number, filter)
        def get_recent_events_description(self, day_number=7):
            return self.girl._get_recent_events_description_impl(day_number)
        def count_occurences(self, context="all", original=False, add_list=None):
            return self.girl._count_occurences_impl(context, original, add_list)
