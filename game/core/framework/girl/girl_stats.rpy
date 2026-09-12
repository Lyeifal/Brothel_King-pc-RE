#### GirlStats — Stat management | 属性管理组件 ####
# Phase 2.1: 属性、上限、变更、溢出、经验/职业经验/声望上限
# Stats, caps, changes, spillover, XP/JP/REP caps
# ★ get_stat / change_stat / set_stat / average_skills — 已迁入
# ★ generate_stats/test_stats/raise_stats/average_stats/stat_spillover/shuffle_skills — 已从 girlclass.rpy 移入 (Phase 7 批次10)
# ★ get_stat_minmax — 以 girlclass 63 行基线版覆盖组件 5 行简化版 (Phase 7 批次10, 修复 change_stat 技能上限回归)

init -2 python:

    class GirlStats(object):
        '''属性管理 | Stat management for a Girl'''

        def __init__(self, girl):
            # 持有 Girl 实例引用 | Hold reference to the Girl instance
            self.girl = girl

        # ── 核心属性访问 | Core stat access ──

        def find_stat(self, stat_name):
            '''按名称查找 Stat 对象 | Find Stat object by name'''
            g = self.girl
            for s in g.stats + g.sex_stats:
                if s.name.lower() == stat_name.lower():
                    return s
            return False

        def get_stat(self, stat_name, raw=False):
            '''获取属性值（含效果加成）| Get stat value with effect modifiers'''
            g = self.girl
            if stat_name in ("defense", "strength"):
                return g.get_defense()
            elif stat_name == "energy":
                return g.energy

            if raw:
                eff = 0
            else:
                eff = g.get_effect("change", stat_name) + g.get_effect("change", "all skills")
                if stat_name.capitalize() in gstats_main:
                    eff += g.get_effect("change", "all main skills")
                elif stat_name.capitalize() in gstats_sex:
                    eff += g.get_effect("change", "all sex skills")

            stat_obj = g.find_stat(stat_name)
            if not stat_obj: # 属性名错误 | wrong stat name
                raise AssertionError(stat_name + " is not a valid stat/skill name. Accepted: " + and_text(["defense", "strength", "energy"] + [s.name.lower() for s in (g.stats + g.sex_stats)]))

            result = stat_obj.value + eff
            if result > 0:
                return round_int(result)
            else:
                return 0

        def get_stat_max(self, stat_name, raw=False, custom_cap=None):
            '''获取属性最大值 | Get max value for a stat'''
            g = self.girl
            if stat_name in ("defense", "strength"):
                return g.get_defense(raw=True) + 10
            elif stat_name == "energy":
                return g.get_stat("constitution") * 10 + g.get_effect("change", "energy")

            if raw:
                return 100
            cap = custom_cap or 100
            return cap + g.get_effect("change", stat_name) + g.get_effect("change", "all skills")

        def get_stat_minmax(self, stat_name, raw = False, custom_cap=None):
            '''获取属性最小/最大值 | Get min/max values for a stat'''
            g = self.girl
            if stat_name in ("love", "fear"):
                _min = -125
                _max = 125

            elif stat_name == "mood":

                _min = -125
                _max = 125

            elif stat_name in ("rep", "rep_neg", "reputation"):

                _min = rep_to_rank[g.rank-1]
                _max = g.get_rep_cap()

            elif stat_name == "energy":

                _min = 0

                eff = g.get_effect("boost", "max energy")

                base = g.get_stat("constitution")+50

                _max = round(base * eff)

            elif stat_name == "xp":

                _min = 0
                _max = xp_to_levelup[g.rank * 5 - 1]

            elif stat_name == "jp":

                _min = 0
                _max = g.get_jp_cap()

            elif stat_name.capitalize() in gstats_main + gstats_sex:

                _min = 0

                max_eff = g.get_effect("change", stat_name.lower() + " max") + g.get_effect("change", "all skill max")

                if custom_cap: # Can set cap to a different value (for classes)
                    _max = custom_cap
                else: # Max cannot be be lower than current stat value
                    _max = max(g.rank * 50 + max_eff, g.get_effect("set", "all skill max"), g.get_stat(stat_name, raw=True))

                    if not raw:
                        eff = g.get_effect("change", stat_name.lower(), change_cap=True) + g.get_effect("change", "all skills", change_cap=True)

                        if stat_name.capitalize() in gstats_main:
                            eff += g.get_effect("change", "all main skills")
                        elif stat_name.capitalize() in gstats_sex:
                            eff += g.get_effect("change", "all sex skills")

                        _max += eff


            else:
                raise AssertionError(stat_name + " min/max not found.")

            return _min, round_int(_max)

        # ── 属性变更 | Stat changes ──

        def change_stat(self, stat, chg, apply_boost=True, spillover=True, custom_cap=None, silent=False, notify_prefix="", notify_suffix=""):
            '''改变属性值 | Change a stat value'''
            g = self.girl
            # 特殊属性路由 | Route special stats
            if stat == "mood": return g.change_mood(chg)
            elif stat == "love": return g.change_love(chg, silent=silent)
            elif stat == "fear": return g.change_fear(chg, silent=silent)
            elif stat == "energy": return g.change_energy(chg)[0]
            elif stat in ("rep", "reputation"): return g.change_rep(chg, silent=silent)
            elif stat == "xp": return g.change_xp(chg, spillover=spillover, silent=silent)
            elif stat == "jp": return g.change_jp(chg, g.job, spillover=spillover, silent=silent)
            elif stat.endswith(" jp"): return g.change_jp(chg, stat[:-3], spillover=spillover, silent=silent)
            elif stat.endswith(" preference"): return g.change_preference(stat[:-11], chg, silent=silent)

            # 普通属性 | Regular stat
            if spillover:
                self.stat_spillover(stat, chg)
            _min, _max = self.get_stat_minmax(stat, raw=True, custom_cap=custom_cap)
            boost = 1.0
            if apply_boost:
                boost = g.get_effect("boost", stat + " gains") * g.get_effect("boost", "all skill gains")

            for s in g.stats:
                if s.name == stat.capitalize():
                    if apply_boost:
                        boost *= g.get_effect("boost", "all regular skills gains")
                        boost = reverse_if(boost, chg)
                    r = s.change(chg * boost, _max)
                    if g.auto_upkeep: g.adjust_upkeep()
                    if stat in ("obedience", "libido"): g.refresh_sex_acts()
                    if not silent and r:
                        notify(notify_prefix + stat_name_dict[s.name] + __(" : %s") % plus_text(r, color_scheme="stat") + notify_suffix, pic=g.portrait)
                    test_achievements(gstats_main + gstats_sex + ["ultimate"])
                    return r

            for s in g.sex_stats:
                if s.name == stat.capitalize():
                    if apply_boost:
                        boost *= g.get_effect("boost", "all sex skills gains")
                        boost = reverse_if(boost, chg)
                    r = s.change(chg * boost, _max)
                    if g.auto_upkeep: g.adjust_upkeep()
                    test_achievements(gstats_main + gstats_sex + ["ultimate"])
                    if not silent and r:
                        notify(notify_prefix + stat_name_dict[s.name] + __(" : %s") % plus_text(r, color_scheme="stat") + notify_suffix, pic=g.portrait)
                    return r

        def set_stat(self, stat, val):
            '''强制设置属性值 | Force-set a stat value'''
            for s in self.girl.stats + self.girl.sex_stats:
                if s.name == stat.capitalize():
                    s.set(val)
                    return

        def stat_spillover(self, stat, chg, job=None): # Job must be specified for JP
            '''属性溢出处理 | Handle stat spillover between main and sex stats'''
            g = self.girl
            eff = g.get_effect("spillover", stat)

            if eff:
                # Targetting girls

                target_list = []

                if g in MC.girls:
                    if stat == "jp":
                        target_list = [gf for gf in MC.girls if gf.job == job]
                    else:
                        target_list = MC.girls

                elif g in farm.girls:
                    target_list = farm.girls

                # Applying spillover effect

                if len(target_list) > 1:
                    chg = chg / (len(target_list) - 1)

                    for gf in target_list:
                        if gf != g:
                            if stat == "jp":
                                gf.change_jp(chg*eff, job, apply_boost=False, spillover=False, silent=True) # spillover=False is needed to avoid an infinite feedback loop
                            else:
                                gf.change_stat(stat, chg*eff, apply_boost=False, spillover=False, silent=True) # spillover=False is needed to avoid an infinite feedback loop


        # ── 属性操作 | Stat operations ──

        def average_skills(self, sk_list, mod=1.0):
            '''计算平均技能值 | Calculate average of multiple skills'''
            g = self.girl
            t = sum(g.get_stat(sk, raw=True) for sk in sk_list)
            avg = t / len(sk_list) * mod
            change_dict = {sk: 0.8 * avg for sk in sk_list}
            remaining_points = 0.2 * len(sk_list) * avg
            # 随机分配剩余点数 | Spread remaining points randomly
            renpy.random.shuffle(sk_list)
            for sk in sk_list:
                point = min(remaining_points, avg * 0.2)
                change_dict[sk] += point
                remaining_points -= point
            return change_dict

        def generate_stats(self, sex=False): # regular stats are generated first, sx stats are generated after fixations
            '''生成属性 | Generate base or sex stats'''
            g = self.girl
            if not sex:
                g.stats = []

                for stat in gstats_main:
                    if use_ini_skills:
                        g.stats.append(Stat(stat, "main", g, weight=g.init_dict["base skills/" + stat]))
                    else:
                        g.stats.append(Stat(stat, "main", g))
            else:
                g.sex_stats = []
                g.does = defaultdict(bool)

                for stat in gstats_sex:
                    g.sex_stats.append(Stat(stat, "sex", g))


        def test_stats(self, stats=None, diff=0, advanced_stats=None): # Result will range from total of positive max modifiers in stat_bonus (+9) to negative max modifiers for primary and secondary (-6). Advanced stats will feed a stat_list directly with more flexibility.
            '''测试属性（用于挑战）| Test stats for challenges'''
            g = self.girl
            if advanced_stats:
                stat_list = advanced_stats
            else:
                stat_list = [(stats[0][0], "primary"), (stats[1][0], "secondary"), (stats[2][0], "booster"), (stats[3][0], "booster")]

            score = 0

            for stat, _type in stat_list:

                if g.get_stat(stat) - diff >= 40: # Reduced the pos threshold for stats for now
                    score += stat_bonus[_type][0]

                elif g.get_stat(stat) - diff >= 20: # Reduced the pos threshold for stats for now
                    score += stat_bonus[_type][1]

                elif g.get_stat(stat) - diff >= 10:
                    score += stat_bonus[_type][2]

                elif g.get_stat(stat) - diff >= 0:
                    score += stat_bonus[_type][3]

                elif _type != "booster":
                    if g.get_stat(stat) - diff <= -40: # Reduced the neg threshold for stats for now
                        score -= stat_bonus[_type][0]

                    elif g.get_stat(stat) - diff <= -20: # Reduced the neg threshold for stats for now
                        score -= stat_bonus[_type][1]

                    elif g.get_stat(stat) - diff <= -10:
                        score -= stat_bonus[_type][2]

                    else:
                        score -= stat_bonus[_type][3]

            return round_int(score)


        def raise_stats(self, stats, silent=False):
            '''提升属性 | Raise stats'''
            g = self.girl
            changes = []

            # Stat increases are stored as tuples (stat_name, %chance, max increase/decrease)

            for s, chance, value in stats:

                if dice(100) <= chance:

                    stat = rand_choice(s)

                    if value > 0: # A dice is rolled from 1 to value
                        if dice(250) > g.get_stat(stat, raw=True): # A skill check makes it harder to raise a stat the higher it gets
                            r = g.change_stat(stat, dice(value) * cheat_modifier["stats"] * game.get_diff_setting("stats"), silent=silent)
                            changes.append((stat, r))

                    elif value < 0:
                        if dice(250) < g.get_stat(stat, raw=True): # A skill check makes it harder to lower a stat the lower it gets
                            r = g.change_stat(stat, value / cheat_modifier["stats"], silent=silent) # Diff setting modifier only applies to stat gains
                            changes.append((stat, r))

            return changes


        def can_upgrade_stat(self, stat):
            '''检查属性是否可以升级 | Check if stat can be upgraded'''
            return self.girl.can_upgrade_stat(stat)

        def upgrade_stat(self, stat, chg, silent=True):
            '''升级属性 | Upgrade a stat'''
            return self.girl.upgrade_stat(stat, chg, silent)

        # ── 经验/职业经验/声望上限 | XP/JP/REP caps ──

        def get_xp_cap(self):
            '''获取经验上限 | Get XP cap for current level'''
            return self.girl.get_xp_cap()

        def get_jp_cap(self, job="all"):
            '''获取职业经验上限 | Get JP cap for current level/job'''
            return self.girl.get_jp_cap(job)

        def get_rep_cap(self):
            '''获取声望上限 | Get reputation cap'''
            return self.girl.get_rep_cap()

        def adjust_level(self, level):
            '''调整等级 | Adjust girl level and related values'''
            return self.girl.adjust_level(level)

        def average_stats(self, stats): #Unused with the new system
            '''已被新系统取代 | Deprecated with new system'''
            g = self.girl
            ## Tests the weighted average of all stats

            score = 0
            totalw = 0

            for tup in stats:

                stat, weight = tup

                score += g.get_stat(stat) * weight
                totalw += weight

            score /= float(totalw)

            return score

        def shuffle_skills(self, sk_list, mod=1.0):
            g = self.girl
            t = 0

            for sk in sk_list:
                t += g.get_stat(sk, raw=True)

            # The points are spread out randomly in rounds (producing more pronounced variation)
            change_dict = {sk: 0 for sk in sk_list}

            while t > len(sk_list)*10:
                change_dict[rand_choice(sk_list)] += 10
                t -= 10

            while t > len(sk_list)*5:
                change_dict[rand_choice(sk_list)] += 5
                t -= 5

            while t > 0:
                change_dict[rand_choice(sk_list)] += 1
                t -= 1

            for sk in sk_list:
                g.set_stat(sk, change_dict[sk])
