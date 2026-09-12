#### GirlRelationships — Love, fear, obedience, social | 关系组件 ####
# Phase 2.1: Love/fear, obedience checks, MC relationship, friendships/rivals.
# 爱情、恐惧、服从、MC 关系、友谊、敌对
# ★ change_love / change_fear — 已从 girlclass.rpy 移入
# ★ get_MC_relation/receive_gift/change_relationship/get_compatibility/update_relationships/get_friendship — 已从 girlclass.rpy 移入 (Phase 7 批次5)
# ★ get_love/get_fear/spoil/terrify/refresh_spoil_terrify_points/meet_MC (Phase 7 批次5)

init -2 python:

    class GirlRelationships(object):
        """Relationship management for a Girl."""

        def __init__(self, girl):
            self.girl = girl

        def get_MC_relation(self):
            g = self.girl
            if g in MC.girls + farm.girls:
                return "slave"

            elif girl in game.free_girls:
                if g.MC_relationship_level == 0:
                        return "stranger"

                elif g.MC_relationship_level == 1:
                        return "friend"

                elif g.MC_relationship_level == 2:
                        return "love interest"

                elif g.MC_relationship_level == 3:
                        return "girlfriend"

                elif g.MC_relationship_level == 4:
                        return "lover"

                elif g.MC_relationship_level == 5:
                        return "lover"

            return "unknown"

        def change_relationship(self, other_girl, chg):
            g = self.girl
            g.relations[other_girl] += chg

            if g.relations[other_girl] > 3 and other_girl not in g.friends:
                g.friends.append(other_girl)
                if other_girl in g.rivals:
                    g.rivals.remove(other_girl)

            elif g.relations[other_girl] <= 3 and other_girl in g.friends:
                g.friends.remove(other_girl)

            elif g.relations[other_girl] >= -3 and other_girl in g.rivals:
                g.rivals.remove(other_girl)

            elif g.relations[other_girl] < -3 and other_girl not in g.rivals:
                g.rivals.append(other_girl)
                if other_girl in g.friends:
                    g.friends.remove(other_girl)

            return g.get_friendship(other_girl)

        def get_compatibility(self, other_girl): # Calculates a score to see if the girl is an ally or a rival. Relationship scores are stored in a dictionary for faster processing
            g = self.girl
            if g.g_compatibility[other_girl] is False:
                # Calculates a score if none exists for this pairing
                g.g_compatibility[other_girl] = 0

                for attr in g.attributes:
                    for k, v in attribute_score_dict[attr].items():
                        if other_girl.is_(k):
                            g.g_compatibility[other_girl] += v

            if g.g_compatibility[other_girl] >= 4:
                return "good"
            elif g.g_compatibility[other_girl] <= -4:
                return "bad"
            else:
                return None

        def update_relationships(self): # Returns a list of all changed relationships
            g = self.girl
            # Clears previous relationships if a girl has left
            for gf in g.friends:
                if gf not in MC.girls + farm.girls:
                    g.friends.remove(gf)
            for gf in g.rivals:
                if gf not in MC.girls + farm.girls:
                    g.rivals.remove(gf)

            _girls = [gf for gf in MC.girls if not (gf.away or gf == g)]

            if len(_girls) < 1:
                return None

            other_girl = rand_choice(_girls)

            # while other_girl == g:
            #     other_girl = rand_choice(_girls)

            old_status = g.get_friendship(other_girl)

            if g.get_compatibility(other_girl) == "good":
                mod = 1
            elif g.get_compatibility(other_girl) == "bad":
                mod = -1
            else:
                mod = 0

            if g.get_effect("change", "making friends"):
                mod += g.get_effect("change", "making friends")
            if other_girl.get_effect("change", "making friends"):
                mod += other_girl.get_effect("change", "making friends")

            r = dice(6, 2) + mod

            if r >= 11:
                new_status = g.change_relationship(other_girl, 1)
                other_girl.change_relationship(g, 1)

            elif r <= 3:
                new_status = g.change_relationship(other_girl, -1)
                other_girl.change_relationship(g, -1)

            else:
                new_status = old_status

            if new_status != old_status:
                change = [g, other_girl, old_status, new_status]
            else:
                change = None

            return change

        def get_friendship(self, other_girl):
            g = self.girl
            if other_girl == g:
                return "g"
            elif g.relations[other_girl] > 3:
                return "friend"
            elif g.relations[other_girl] < -3:
                return "rival"
            else:
                return "normal"

        def get_love(self):
            g = self.girl
            love = g.love

            love += g.get_effect("change", "love")
            if love > 0:
                love *= g.get_effect("boost", "love")
            elif love < 0:
                love *= g.get_effect("boost", "hate")

            return love

        def get_fear(self):
            g = self.girl
            fear = g.fear

            fear += g.get_effect("change", "fear")
            if fear > 0:
                fear *= g.get_effect("boost", "fear")
            elif fear < 0:
                fear *= g.get_effect("boost", "trust")

            return fear

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
            g = self.girl
            g.MC_interact = True
            g.track_event("MC met", arg=g.name)
            g.activation_date = calendar.time
            g.talked_to_date = calendar.time

        def spoil(self, nb):
            g = self.girl
            g.spoil_points += nb

            if dice(6) + 2 < g.spoil_points:
                g.spoiled = True

            return

        def terrify(self, nb):
            g = self.girl
            g.terrify_points += nb

            if dice(6) + 2 < g.terrify_points:
                g.terrified = True

            return

        def refresh_spoil_terrify_points(self):
            g = self.girl
            g.spoil_points = max(g.spoil_points-1, 0)

            if g.spoil_points == 0:
                g.spoiled = False

            g.terrify_points = max(g.terrify_points-1, 0)

            if g.terrify_points == 0:
                g.terrified = False

            return

        def receive_gift(self, item):
            g = self.girl
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)

            flower = False
            potion = False

            score = 1
            mod = 1.0

            for e in item.effects:
                if e.type == "gift":
                    score += g.personality.gift_likes[e.target]
                    mod = e.value

                elif e.type == "flower":
                    flower = True
                    break

                elif e.type == "potion":
                    potion = e.target
                    break


            if flower:
                if e.target == g.likes["color"]:
                    score += 4
                    g.personality_unlock["fav_color"] = True
                    renpy.say(g.char, __("Oh, you remembered my favorite color! You're so considerate..."))

                elif e.target == g.dislikes["color"]:
                    score += 0
                    g.personality_unlock["dis_color"] = True
                    renpy.say(g.char, __("Ah, em, thanks. You know, I don't like this color, but I appreciate the gesture."))

                else:
                    score += 2
                    renpy.say(g.char, __("Flowers! For me! Thank you..."))

                if g.MC_relationship_level == 2:
                    renpy.say(g.char, __("This is very romantic... Was there something you wanted from me?"))

                    r = menu(items = (("Actually...", None), ("Ask her out", True), ("Never mind", False)))

                    if r:
                        norollback()
                        g.MC_relationship_level = 3
                        g.track_event("MC girlfriend", arg=g.name)
                        test_achievement("girlfriends")
                        g.say("free_ask_out")

                    else:
                        norollback()
                        renpy.say(you, __("Hmm, no, not really."))
                        renpy.say(g.char, __("Oh... I see."))

            elif potion:
                if potion == "seduction":
                    if g not in game.free_girls:
                        return False

                    # NG+ - Potion of seduction
                    if g.MC_relationship_level < 1:
                        renpy.call("free_girl_friend", g)
                    elif g.MC_relationship_level < 2:
                        renpy.call("free_girl_love_interest", g)
                    elif g.MC_relationship_level < 3:
                        norollback()
                        g.MC_relationship_level = 3
                        g.track_event("MC girlfriend", arg=g.name)
                        test_achievement("girlfriends")
                        g.say("free_ask_out")
                    elif g.MC_relationship_level < 4:
                        renpy.call("free_girl_girlfriend", g)
                    elif g.MC_relationship_level < 5:
                        renpy.call("free_girl_job_request", g)
                    else:
                        renpy.say(narrator, __("Already at the maximum relationship level. This potion had no effect."))
                    # /NG+

            else:
                if score >= 4:
                    renpy.say(g.char, __("Oh, I love it so much!!! Thank you, thank you!"))

                elif score >= 2:
                    renpy.say(g.char, __("It's nice! Thanks for thinking about me."))

                elif score >= 0:
                    renpy.say(g.char, __("Ah, em, thanks. It's an interesting... whatever it is, I guess."))

                else:
                    renpy.say(g.char, __("What the? Ew, take this away from me!"))

            if score >= 0:
                score *= mod

            g.change_love(score)
            g.change_mood(score)

            return score
