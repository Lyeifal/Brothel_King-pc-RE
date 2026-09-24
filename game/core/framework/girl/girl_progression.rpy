#### GirlProgression — Level, rank, XP/JP/rep, Perks | 进阶组件 ####
# Phase 2.1: 等级、排名、职业等级、经验/职业经验/声望、Perk、属性升级
# Level, rank, job levels, XP/JP/REP, perks, stat upgrades
# ★ level_up/rank_up/job_up/adjust_level/auto_level_up/debug_auto_level/ready_to_* — 已从 girlclass.rpy 移入 (Phase 7 批次6)
# ★ change_xp/change_jp/change_rep/get_xp_cap/get_jp_cap/get_rep_cap (Phase 7 批次6)
# ★ can_acquire_perk/acquire_perk/refund_perks/check_combo_perks/has_prerequisites/get_perk/get_perk_level/update_can_perk/unlock_archetype (Phase 7 批次6)
# ★ upgrade_stat/can_upgrade_stat/get_max_stat_upgrade_points (Phase 7 批次6)

init -2 python:

    class GirlProgression(object):
        '''进阶管理 | Progression for a Girl: level/rank/job-ups, XP/JP/rep, perks, stat upgrades'''

        def __init__(self, girl):
            # 持有 Girl 实例引用 | Hold reference to the Girl instance
            self.girl = girl

        def level_up(self, forced = False, silent=False):
            g = self.girl
            if g.ready_to_level() or forced:

                if forced:
                    g.xp = g.get_xp_cap()

                if g.level < 25: # Hard-coded level cap
                    g.level += 1

                    g.upgrade_points += 5 + 5 * g.rank

                    if g.level == 25:
                        g.perk_points += 3
                        notify(__("Maximum level reached! +1 Perk Point"), pic=g.portrait, col=c_lightgreen)
                    elif g.level%5 == 0:
                        g.perk_points += 2
                    else:
                        g.perk_points += 1

                    g.update_can_perk() # This is not checked dynamically for performance
                    # MC earns prestige when a girl levels up
                    MC.prestige += g.rank

                    if not silent:
                        g.track_event("level up", arg=g.level)

                    return True

            return False

        def rank_up(self, forced = False, silent=False):
            g = self.girl
            if g.ready_to_rank() or forced:
                if forced:
                    g.rep = rep_to_rank[g.rank]

                if g.rank < 5:
                    g.rank += 1
                    g.rank_up_sanity()

                if g.auto_upkeep:
                    g.adjust_upkeep()

                g.update_can_perk() # This is not checked dynamically for performance

                if not silent:
                    g.track_event("rank up", arg=rank_name[g.rank])

                #ADD rank up animation

        def job_up(self, job, forced = False, announcement_delay=0):
            g = self.girl
            if g.ready_to_job_up(job) or forced:

                if g.job_level[job] < 5:
                    g.job_level[job] += 1

                    primary, secondary, add1, add2 = job_up_dict[job]

                    g.change_stat(primary, job_up_change[g.job_level[job]][0], apply_boost = False)
                    g.change_stat(secondary, job_up_change[g.job_level[job]][1], apply_boost = False)
                    g.change_stat(add1, job_up_change[g.job_level[job]][2], apply_boost = False)
                    g.change_stat(add2, job_up_change[g.job_level[job]][2], apply_boost = False)

                    g.track_event("job up", arg=job)

                    calendar.set_alarm(calendar.time + announcement_delay, Event(label = "job_up", object = (g, job, g.job_level[job])))

        def adjust_level(self, level):
            g = self.girl
            g.level = level

            # Adjust rank
            while g.rank * 5 < g.level:
                g.rank += 1

            # Adjust XP and REP

            g.xp = xp_to_levelup[g.level-1]
            g.rep += rep_to_rank[g.rank-1]

            # Get perk points

            g.perk_points += (g.level-1) + g.level // 5

            if g.level == 25:
                g.perk_points += 1

            #! No skill points are distributed for now, see if it works

        def auto_level_up(self, forced = False, silent = False):
            g = self.girl
            if g.level_up(forced, silent):
                for stat in g.stats:
                    g.upgrade_stat(stat.name, g.upgrade_points/8.0)

        def debug_auto_level(self, chapter):
            g = self.girl
            if chapter > 6:
                ranks = 3
                levels = 20
            elif chapter > 4:
                ranks = 2
                levels = 15
            elif chapter > 2:
                ranks = 1
                levels = 10
            elif chapter > 1:
                ranks = 0
                levels = 5
            else:
                ranks = 0
                levels = 0

            ranks = ranks - g.rank
            levels = levels - g.level

            if levels > 0:
                for i in range(levels):
                    # Simulates gained skills
                    g.upgrade_points += 10*g.rank

                    # Auto level and rank up
                    g.auto_level_up(forced=True, silent=True)
                    if g.level % 5 == 0 and ranks > 0:
                        g.rank_up(forced=True, silent=True)
                        ranks -= 1

        def ready_to_level(self):
            g = self.girl
            if g.level < g.rank * 5:

                if g.xp >= g.get_xp_cap():

                    return True

            return False

        def ready_to_rank(self):
            g = self.girl
            if g.rank < district.rank:

                if g.rep >= rep_to_rank[g.rank] * g.get_effect("boost", "new rank reputation requirement") and g.level >= g.rank * 5:

                    return True

            return False

        def ready_to_job_up(self, job):
            g = self.girl
            if job in (all_jobs + all_sex_acts):

                mylevel = g.job_level[job]

                if mylevel == 5:

                    return False

                elif g.jp[job] >= jp_to_level[mylevel] and mylevel < g.rank:

                    return True

            return False

        def can_spend_upgrade_points(self):
            g = self.girl
            if g.upgrade_points >= 1:
                for stat in g.stats:
                    if g.can_upgrade_stat(stat):
                        return True
            return False

        def change_xp(self, value, apply_boost = True, spillover=True, silent=False):
            g = self.girl
            # XP spillover (Bride perk: confession) - Boosts don't apply
            if spillover:
                g.stat_spillover("xp", value)

            _min, _max = g.get_stat_minmax("xp")

            if apply_boost:

                boost = g.get_effect("boost", "xp gains")

                boost += 0.05 * g.remembers("reward", "level up") # Boosts XP is she was rewarded before

                boost = reverse_if(boost, value) ## Reverses boost if decreasing stat

            else:
                boost = 1.0

            change = value * boost

            if _min > g.xp + change:

                change = _min - g.xp
                g.xp = _min

            elif _max < g.xp + change:

                change = _max - g.xp
                g.xp = _max

            else:
                g.xp += change

            if change and not silent: notify(_("XP: %s") % plus_text(change, color_scheme="xp"), pic=g.portrait) # Experimental

            return change

        def change_jp(self, value, job, apply_boost = True, spillover=True, announcement_delay=1, silent=False):
            g = self.girl
            # JP spillover (Bride perk: confession) - Boosts don't apply
            if spillover:
                g.stat_spillover("jp", value, job=job)

            _min, _max = g.get_stat_minmax("jp")

            if apply_boost:

                boost = g.get_effect("boost", "all jp gains") * g.get_effect("boost", job + " jp gains")

                boost += 0.05 * g.remembers("reward", "job up") # Boosts JP is she was rewarded before

                boost = reverse_if(boost, value)

            else:

                boost = 1.0

            change = value * boost

            if _min > g.jp[job] + change:

                change = _min - g.jp[job]
                g.jp[job] = _min

            elif _max < g.jp[job] + change:

                change = _max - g.jp[job]
                g.jp[job] = _max

            else:
                g.jp[job] += change

            while g.ready_to_job_up(job):
                g.job_up(job, announcement_delay=announcement_delay)

            if change and not silent: notify(_("%s JP: %s") % (__(job.capitalize()), plus_text(change, color_scheme="jp")), pic=g.portrait) # Experimental

            return change

        def change_rep(self, chg, silent=False):
            g = self.girl
            _min, _max = g.get_stat_minmax("rep")

            boost = g.get_effect("boost", "reputation gains") * game.get_diff_setting("rep")

            boost += 0.05 * g.remembers("reward", "rank up") # Boosts REP is she was rewarded before

            boost = reverse_if(boost, chg)

            chg = get_change_min_max(g.rep, chg*boost, _min, _max)
#            renpy.say("", "Changing rep by " + str(chg))

            g.rep += chg

            if not silent: notify(_("Reputation: %s") % plus_text(int(chg)), col="rep", pic=g.portrait)

            return chg

        def get_xp_cap(self):
            g = self.girl
            if g.level < g.rank * 5:
                cap = xp_to_levelup[g.level]
            else:
                cap = xp_to_levelup[g.rank * 5 - 1]

            return cap

        def get_jp_cap(self, job = "all"):
            g = self.girl
            if job == "all":

                cap = jp_to_level[g.rank - 1]

            elif g.job_level[job] < g.rank:

                cap = jp_to_level[g.job_level[job]]

            else:

                cap = jp_to_level[g.rank - 1]

            return cap

        def get_rep_cap(self): # Adds 0.99 to avoid strange back and forth effects where girls can rank up briefly then are pulled back by rep decay
            g = self.girl
            if g.rank < district.rank:
                cap = rep_to_rank[g.rank] + 0.99

            else:
                cap = rep_to_rank[district.rank] + 0.99
            return cap

        def can_acquire_perk(self, perk, context=None): # Where perk is an object
            g = self.girl
            if g.has_perk(perk.name):
                return False, __("She already has that perk.")

            if context == "perk_screen":
                points = perk_points
                perks = g.perks + new_perks
            else:
                points = g.perk_points
                perks = g.perks

            val = sum(1 for p in perks if p.archetype == perk.archetype)

            message = ""

            if not g.archetypes[perk.archetype].unlocked:
                message += perk.archetype + " is locked for now.\n"
            elif val < perk.value:
                message += str(perk.value) + " more perk" + plural(perk.value) + " must be unlocked first.\n"
            elif g.rank < perk.min_rank:
                message += g.name + " must be rank " + rank_name[perk.min_rank] + " before she can acquire this perk.\n"
            elif points < 1:
                message = g.name + " does not have enough points."
            else:
                return True, ""

            return False, message

        def acquire_perk(self, perk, forced=False): ## Where perk is an object
            g = self.girl
            if perk not in g.perks:
                if not forced:
                    if g.can_acquire_perk(perk)[0]:
                        g.perk_points -= 1
                    else:
                        return g.can_acquire_perk(perk, g.perk_points)

                g.perks.append(perk)
                g.add_effects(perk.effects)
                g.reset_sex_acts(first=False)

                if perk.level == 3:
                    unlock_achievement(perk.archetype)

                g.update_can_perk()

            return True, ""

        def refund_perks(self, min_level=0): # all perks above or equal to min_level will be refunded. Use min_level=0 to refund archetypes
            g = self.girl
            perk_points = 0

            for perk in list(g.perks):
                if perk.level >= min_level:
                    g.perks.remove(perk)
                    g.remove_effects(perk.effects)
                    g.reset_sex_acts(first=False)

                    perk_points += 1

            if min_level <= 0:
                for arch in archetype_dict.keys():
                    if g.archetypes[arch].unlocked:
                        g.archetypes[arch].unlocked = False
                        perk_points += 2

            g.perk_points += perk_points

            g.update_can_perk()

            return perk_points

        def check_combo_perks(self):
            g = self.girl
            for p in combo_perks:
                if not g.has_perk(p.name) and g.has_prerequisites(p):
                    g.perks.append(p)
                    g.add_effects(p.effects)

                    renpy.call_screen("OK_screen", title = p.name, message = g.name + __(" has learnt a new combo! ") + p.description)

        def has_prerequisites(self, perk):
            g = self.girl
            if perk.prerequisite != None:

                for pre in perk.prerequisite:
                    if not g.has_perk(pre):
                        return False

            return True

        def get_perk(self, perk): ## Where perk is an object (important)
            g = self.girl
            for p in g.perks:
                if p.name == perk.name:
                    return p
            else:
                return False

        def get_perk_level(self, perk): ## Where perk is an object (important)
            g = self.girl
            p = g.get_perk(perk)

            if p:
                return p.level

            else:
                return 0

        def update_can_perk(self): # 'can_perk' is used to trigger UI alerts
            g = self.girl
            g.can_perk = False

            # Can unlock perk tree
            if g.perk_points >= 2 and [a for a in g.archetypes.values() if not a.unlocked]:
                g.can_perk = True

            # Can unlock perk
            for perk in perk_dict.values():
                if g.can_acquire_perk(perk)[0]:
                    g.can_perk = True

        def unlock_archetype(self, archetype_name):
            g = self.girl
            if not g.archetypes[archetype_name].unlocked:
                g.archetypes[archetype_name].unlocked = True
                g.update_can_perk() # This is not checked dynamically for performance
                return True
            else:
                return False

        def upgrade_stat(self, stat, chg, silent=True):
            g = self.girl
            r = g.change_stat(stat, chg, apply_boost = False, silent=silent)

            g.upgrade_points -= r

            if r < chg:
                return False
            else:
                return True

        def can_upgrade_stat(self, stat): # Where stat is an object
            g = self.girl
            _min, _max = g.get_stat_minmax(stat.name, raw = True)

            if stat.value >= _max:
                return False
            return True

        def get_max_stat_upgrade_points(self, stat):
            g = self.girl
            result = g.get_stat_minmax(stat, raw = True)[1] - g.get_stat(stat, raw = True)
            if result > 0:
                if result > g.upgrade_points:
                    result = g.upgrade_points
                return round_int(result)
            else:
                return 0
