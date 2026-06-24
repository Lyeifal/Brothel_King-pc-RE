#### GirlRelationships — Love, fear, obedience, social component ####
# Phase 2.1: Love/fear, obedience checks, MC relationship, friendships/rivals.
# Methods to migrate: get_MC_relation, change_relationship, get_compatibility,
# update_relationships, get_friendship, get_love, get_fear, change_love,
# change_fear, meet_MC, spoil, terrify, refresh_spoil_terrify_points.

init -2 python:

    class GirlRelationships(object):
        """Relationship management for a Girl."""

        def __init__(self, girl):
            self.girl = girl
