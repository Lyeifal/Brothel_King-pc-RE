#### GirlBase — Core identity component ####
# Phase 2.1: Identity, name handling, level, serialization.
# Methods to migrate: __init__, randomize, is_unique, set_name, set_fullname,
# random_rename, get_name, get_badge, adjust_level, load_ini, read_ini.

init -2 python:

    class GirlBase(object):
        """Core identity and lifecycle for a Girl."""

        def __init__(self, girl):
            self.girl = girl
