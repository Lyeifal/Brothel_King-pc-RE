#### GirlStats — Stat management | 属性管理组件 ####
# Phase 2.1: 属性、上限、变更、溢出、经验/职业经验/声望上限
# Stats, caps, changes, spillover, XP/JP/REP caps
# ★ get_stat / change_stat / set_stat / average_skills — 已迁入

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

        def get_stat_minmax(self, stat_name, raw=False, custom_cap=None):
            '''获取属性最小/最大值 | Get min/max values for a stat'''
            _min = 0
            _max = self.get_stat_max(stat_name, raw, custom_cap)
            return _min, _max

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

        def stat_spillover(self, stat, chg, job=None):
            '''属性溢出处理 | Handle stat spillover between main and sex stats'''
            return self.girl._stat_spillover_impl(stat, chg, job)

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

        def generate_stats(self, sex=False):
            '''生成属性 | Generate base or sex stats'''
            return self.girl._generate_stats_impl(sex)

        def test_stats(self, stats=None, diff=0, advanced_stats=None):
            '''测试属性（用于挑战）| Test stats for challenges'''
            return self.girl._test_stats_impl(stats, diff, advanced_stats)

        def raise_stats(self, stats, silent=False):
            '''提升属性 | Raise stats'''
            return self.girl._raise_stats_impl(stats, silent)

        def can_upgrade_stat(self, stat):
            '''检查属性是否可以升级 | Check if stat can be upgraded'''
            return self.girl._can_upgrade_stat_impl(stat)

        def upgrade_stat(self, stat, chg, silent=True):
            '''升级属性 | Upgrade a stat'''
            return self.girl._upgrade_stat_impl(stat, chg, silent)

        # ── 经验/职业经验/声望上限 | XP/JP/REP caps ──

        def get_xp_cap(self):
            '''获取经验上限 | Get XP cap for current level'''
            return self.girl._get_xp_cap_impl()

        def get_jp_cap(self, job="all"):
            '''获取职业经验上限 | Get JP cap for current level/job'''
            return self.girl._get_jp_cap_impl(job)

        def get_rep_cap(self):
            '''获取声望上限 | Get reputation cap'''
            return self.girl._get_rep_cap_impl()

        def adjust_level(self, level):
            '''调整等级 | Adjust girl level and related values'''
            return self.girl._adjust_level_impl(level)

        def average_stats(self, stats):
            '''已被新系统取代 | Deprecated with new system'''
            return self.girl._average_stats_impl(stats)
