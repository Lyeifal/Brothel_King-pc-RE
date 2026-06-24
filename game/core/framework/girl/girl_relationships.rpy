#### GirlRelationships — Love, fear, obedience, social component ####
# Phase 2.1: Love/fear, obedience checks, MC relationship, friendships/rivals.
# Methods to migrate: get_MC_relation, change_relationship, get_compatibility,
# update_relationships, get_friendship, get_love, get_fear, change_love,
# change_fear, meet_MC, spoil, terrify, refresh_spoil_terrify_points.

init -2 python:

    class GirlRelationships(object):
        """Relationship management for a Girl. Delegates to _impl methods."""

        def __init__(self, girl):
            self.girl = girl

        def get_MC_relation(self):
            return self.girl._get_MC_relation_impl()
        def change_relationship(self, other_girl, chg):
            return self.girl._change_relationship_impl(other_girl, chg)
        def get_compatibility(self, other_girl):
            return self.girl._get_compatibility_impl(other_girl)
        def update_relationships(self):
            return self.girl._update_relationships_impl()
        def get_friendship(self, other_girl):
            return self.girl._get_friendship_impl(other_girl)
        def get_love(self):
            return self.girl._get_love_impl()
        def get_fear(self):
            return self.girl._get_fear_impl()
        def change_love(self, amount, min_cap=None, max_cap=None, silent=False):
            return self.girl._change_love_impl(amount, min_cap, max_cap, silent)
        def change_fear(self, amount, min_cap=None, max_cap=None, mojo_color="purple", silent=False):
            return self.girl._change_fear_impl(amount, min_cap, max_cap, mojo_color, silent)
        def meet_MC(self):
            return self.girl._meet_MC_impl()
        def spoil(self, nb):
            return self.girl._spoil_impl(nb)
        def terrify(self, nb):
            return self.girl._terrify_impl(nb)
        def refresh_spoil_terrify_points(self):
            return self.girl._refresh_spoil_terrify_points_impl()
