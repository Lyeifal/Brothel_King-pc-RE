#### GirlBase — Core identity component ####
# Phase 2.1: Identity, name handling, level, serialization.
# Methods to migrate: __init__, randomize, is_unique, set_name, set_fullname,
# random_rename, get_name, get_badge, adjust_level, load_ini, read_ini.

init -2 python:

    class GirlBase(object):
        """Core identity and lifecycle for a Girl. Delegates to _impl methods."""

        def __init__(self, girl):
            self.girl = girl

        def set_name(self):
            return self.girl._set_name_impl()
        def set_fullname(self):
            return self.girl._set_fullname_impl()
        def random_rename(self):
            return self.girl._random_rename_impl()
        def get_name(self):
            return self.girl._get_name_impl()
        def get_badge(self):
            return self.girl._get_badge_impl()
        def is_unique(self):
            return self.girl._is_unique_impl()
        def load_ini(self, search_for=None, skip_checks=False):
            return self.girl._load_ini_impl(search_for, skip_checks)
        def read_ini(self, section=None, key=None):
            return self.girl._read_ini_impl(section, key)
        def adjust_level(self, level):
            return self.girl._adjust_level_impl(level)
        def randomize(self, free=False, p_traits=None, n_trait=None, perks=None, force_original=False, level=1, personality=None, temp_list=None):
            return self.girl._randomize_impl(free, p_traits, n_trait, perks, force_original, level, personality, temp_list)
