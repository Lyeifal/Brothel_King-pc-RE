#### GirlLogging — Event logging and tracking component ####
# Phase 2.1: Logging, stats tracking, memory, event history.
# Methods to migrate: commit, return_from, add_log, get_log, get_average_performance,
# track_event, get_recent_events, get_recent_events_description, count_occurences.

init -2 python:

    class GirlLogging(object):
        """Event logging and tracking for a Girl."""

        def __init__(self, girl):
            self.girl = girl
