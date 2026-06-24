#### GirlRelationships — Love, fear, obedience, social | 关系组件 ####
# Phase 2.1: Love/fear, obedience checks, MC relationship, friendships/rivals.
# 爱情、恐惧、服从、MC 关系、友谊、敌对
# ★ change_love / change_fear — 已从 girlclass.rpy 移入
# Methods: get_MC_relation, get_love, get_fear, spoil, terrify, etc.

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
        # ── Love & fear (implementations moved from girlclass.rpy) ──
        def change_love(self, amount, min_cap=None, max_cap=None, silent=False):
            g = self.girl
            if g in game.free_girls:
                if not min_cap: min_cap = 0
                if not max_cap: max_cap = 100
            else:
                if not min_cap: min_cap = g.rank * -25
                if not max_cap: max_cap = g.rank * 25

            if g in MC.girls or g in game.free_girls:
                if g in MC.girls:
                    boost = g.get_effect("boost", "love gains") * alignment_bonus[MC.get_alignment() + "_love"]
                elif g in game.free_girls:
                    boost = g.get_effect("boost", "love gains") * MC.get_effect("boost", "free girl love gains") * alignment_bonus[MC.get_alignment() + "_love"]
                boost = reverse_if(boost, amount)
                if amount > 0:
                    boost *= (1.0 + MC.get_charisma() * 0.1)
            else:
                boost = 1.0

            change = get_change_min_max(g.love, amount * boost, min_cap, max_cap, enforce_boundaries=False)
            g.love += change

            if not silent:
                if change > 0.5:   notify(__("Love increased"), pic=g.portrait, debug_txt="(%s)" % str(change))
                elif change < -0.5: notify(__("Love decreased"), pic=g.portrait, debug_txt="(%s)" % str(change))

            test_achievement("love")
            return change

        def change_fear(self, amount, min_cap=None, max_cap=None, mojo_color="purple", silent=False):
            g = self.girl
            if not min_cap: min_cap = g.rank * -25
            if not max_cap: max_cap = g.rank * 25

            if g in MC.girls or g in game.free_girls:
                if g in MC.girls:
                    boost = g.get_effect("boost", "fear gains") * alignment_bonus[MC.get_alignment() + "_fear"]
                elif g in game.free_girls:
                    boost = g.get_effect("boost", "fear gains") * MC.get_effect("boost", "free girl fear gains") * alignment_bonus[MC.get_alignment() + "_fear"]
                boost = reverse_if(boost, amount)
                if amount > 0:
                    boost *= (1.0 + MC.get_charisma() * 0.1)
            else:
                boost = 1.0

            change = get_change_min_max(g.fear, amount * boost, min_cap, max_cap, enforce_boundaries=False)
            g.fear += change

            if change > 0:
                if mojo_color == "purple":
                    MC.raise_mojo(mojo_color, mojo=change / NORMAL_MOJO_VALUE)
                else:
                    MC.raise_mojo(mojo_color, mojo=change / FARM_MOJO_VALUE)

            if not silent:
                if change > 0.5:   notify(__("Fear increased"), pic=g.portrait, debug_txt="(%s)" % str(change))
                elif change < -0.5: notify(__("Fear decreased"), pic=g.portrait, debug_txt="(%s)" % str(change))

            test_achievement("fear")
            return change
        def meet_MC(self):
            return self.girl._meet_MC_impl()
        def spoil(self, nb):
            return self.girl._spoil_impl(nb)
        def terrify(self, nb):
            return self.girl._terrify_impl(nb)
        def refresh_spoil_terrify_points(self):
            return self.girl._refresh_spoil_terrify_points_impl()
