#### GirlTraining — Farm training, obedience, resistance | 农场训练与服从 ####
# Phase 2.1: 农场行为、服从检查、逃跑、反抗
# Farm acts, obedience checks, run away, resistance
# ★ will_do_farm_act / will_rebel_in_farm / farm_beg_test — 已迁入
# ★ will_rebel_in_farm/farm_beg_test 以 girlclass 版覆盖组件旧手写版 (Phase 7 批次9)
# ★ get_obedience_check_target/get_working_chance/get_training_chance/build_up/get_build_up/reset_build_up — 已从 girlclass.rpy 移入 (Phase 7 批次9)

init -2 python:

    class GirlTraining(object):
        '''农场训练与服从管理 | Farm training and obedience management'''

        def __init__(self, girl):
            self.girl = girl

        # ── 农场行为 | Farm acts ──

        def will_do_farm_act(self, act, mode=None):
            '''判断女孩是否接受农场训练 | Determine if girl accepts farm training'''
            g = self.girl
            # 指定模式直接返回 | Direct return when mode is specified
            if mode:
                if mode == "gentle": return "accepted"
                elif mode == "tough":
                    if g.obedience_check(act): return "accepted"
                    elif g.run_away_check(): return "refused"
                    else: return "resisted"
                elif mode == "hardcore": return g.obedience_check(act)
                else: return False
            # 根据偏好和服从判断 | Based on preference and obedience
            if not g.will_do_sex_act(act): return "refused"
            elif g.get_preference(act) > dice(100): return "accepted"
            else:
                if g.obedience_check(act): return "accepted"
                elif g.run_away_check(): return "refused"
                else: return "resisted"

        def will_rebel_in_farm(self, train_mode, reaction):
            '''判断女孩是否会反抗训练 | Determine if girl rebels against training'''
            g = self.girl
            if train_mode == "gentle":
                return False

            if g.is_("very dom"):
                diff = 200
            elif g.is_("dom"):
                diff = 100
            elif g.is_("very sub"):
                diff = 0
            elif g.is_("sub"):
                diff = 50

            if train_mode == "tough":
                diff -= 25
            elif train_mode == "hardcore":
                diff += 25

            if reaction == "accepted":
                diff -= 25
            elif reaction == "refused":
                diff += 25

            if dice(100) < (diff - g.get_love()//2 - g.get_fear() - g.get_stat("obedience")): # Fear impacts rebel chances more than love
                return True
            return False

        def farm_beg_test(self): # Determines if the girl will beg not to go to the farm
            '''测试女孩是否求饶 | Test if girl begs not to go to farm'''
            g = self.girl
            r = dice(10)

            r -= g.get_stat("obedience") // 50

            if g.is_("very sub"):
                r += 2
            elif g.is_("sub"):
                r += 1
            elif g.is_("very dom"):
                r -= 1

            if g.is_("very modest"):
                r += 2
            elif g.is_("modest"):
                r += 1
            elif g.is_("very lewd"):
                r -= 1

            if farm.knows["weakness"][g]:
                r += 1

            if r >= 10:
                return True
            else:
                return False

        # ── 服从与逃跑 | Obedience & run away ──

        def get_obedience_check_target(self, act=None, train=False): # This is the target (in %) UNDER which a girl must roll to obey.
            '''获取服从检查的目标值 | Get target for obedience check'''
            g = self.girl
            if g.job == "whore" or act == "whore":
                coeff = 70
                if g.has_activated_sex_acts():
                    # Only the average modifier is kept
                    coeff += sum(preference_modifier[g.get_preference(act)] for act in g.does if (g.does[act] and act in all_sex_acts)) / sum(1 for act in g.does if (g.does[act] and act in all_sex_acts))

                    # Cannot completely offset mod (mood, obedience...)
                    if coeff < 30:
                        coeff = 30
                else: # Can no longer work as a whore
                    if g.job == "whore":
                        g.job = None
                        notify(_("%s cannot work as a whore anymore.") % g.fullname, pic=g.portrait)

                    # raise AssertionError("No sex act activated")

            elif act and act != "whore":
                coeff = 70

                # Checks modifier according to girl's preference/reluctance
                coeff += preference_modifier[g.get_preference(act)]

            else: # Regular job
                coeff = 35

            coeff += g.get_effect("change", "obedience target")

            if train:
                if g.get_love() > g.get_fear(): # Dominant emotion is used if training.
                    mod = g.get_stat("obedience") + g.get_love() + g.mood//4
                else:
                    mod = g.get_stat("obedience") + g.get_fear() + g.mood//4
            else:
                mod = g.get_stat("obedience") + g.mood//4 - (g.get_stat_minmax("energy")[1] - g.energy)//10

                if g.get_fear() > 0:
                    mod += g.get_fear()
                elif g.get_fear() < 0: # lower impact of trust on disobedience to compensate the rank penalty
                    mod += g.get_fear()//2

            # New: Target is affected by rank and total girl number in the Brothel, giving more importance to Obedience in late-game
            coeff += (len(MC.girls)-1 + len(g.rivals) - len(g.friends))*15 # Friends do not count towards the overcrowding penalty, rivals count double
            mod -= (g.rank-1) * 20

            target = (0.96 ** mod) * coeff # Make 0.96 higher to increase difficulty

            if train:
                target += g.get_effect("change", "train obedience target")
            elif g.job == "whore" or act == "whore":
                target += g.get_effect("change", "whore obedience target")
            else:
                target += g.get_effect("change", "job obedience target")

            ## Obedience link effect ##

            if g.get_effect("special", "link obedience", raw=True):
                girl2, is_super = g.get_effect("special", "link obedience", raw=True)

                if is_super:
                    target = min(target, girl2.get_obedience_check_target(act=act, train=train))
                else:
                    target = min(target, (target + girl2.get_obedience_check_target(act=act, train=train))/2)

            return target


        def obedience_check(self, act=None):
            '''执行服从检查 | Perform an obedience check (will she accept to work tonight)'''
            g = self.girl
            # 服从检查目标值 | Obedience check target value
            target = g.get_obedience_check_target(act, train=False)

            result = renpy.random.randrange(100) * g.get_effect("boost", "obedience tests")

            # 奖惩记忆修正（Dom 女孩不喜欢惩罚）| Reward/punishment memory boost (Dom girls dislike punishment)

            if g.remembers("punish", "disobey"):
                if g.is_("very dom"):
                    result -= 5
                elif g.is_("dom"):
                    result += 0
                elif g.is_("very sub"):
                    result += 6 * g.remembers("punish", "disobey")
                elif g.is_("sub"):
                    result += 3 * g.remembers("punish", "disobey")

            g.last_obedience_check = str(result) + "/" + str(round_int(target))

            if result > target:
                return True

            else:
                return False

        def training_check(self, act):
            '''执行训练检查 | Perform a training check'''
            g = self.girl

            target = g.get_obedience_check_target(act, train=True)
            result = renpy.random.randrange(100) * g.get_effect("boost", "obedience tests")

            # 奖励记忆修正 | Reward memory boost

            if g.remembers("reward", act):
                if g.is_("very materialist"):
                    result += 9 * g.remembers("reward", "act")
                elif g.is_("materialist"):
                    result += 6 * g.remembers("reward", "act")
                elif g.is_("very idealist"):
                    result += 0
                elif g.is_("idealist"):
                    result += 6 * g.remembers("reward", "act")

            if g.remembers("punish", act):
                if g.is_("very dom"):
                    result -= 5
                elif g.is_("dom"):
                    result += 0
                elif g.is_("very sub"):
                    result += 6 * g.remembers("punish", "act")
                elif g.is_("sub"):
                    result += 3 * g.remembers("punish", "act")

            if result > target:
                return "accepted"

            elif result > (target - 25):
                return "resisted"

            else:
                return "refused"

        def run_away_check(self):
            '''检查女孩是否尝试逃跑 | Check if girl attempts to run away in the morning'''
            g = self.girl
            result = False

            # 上次逃跑失败需满5个工作日才会再次尝试 | Girls only retry 5 working days after last failed attempt
            if g.mood < mood_runaway_limit and g.ran_away_counter >= 5 and not (g.away or g.farm):

                if g.remembers("punish", "ran away"):
                    if g.is_("very dom"):
                        mod = 5
                    elif g.is_("dom"):
                        mod = 0
                    elif g.is_("very sub"):
                        mod = -6 * g.remembers("punish", "ran away")
                    elif g.is_("sub"):
                        mod = -3 * g.remembers("punish", "ran away")
                else:
                    mod = 0

                if dice(100) > 100 - (mood_runaway_limit - g.mood):
                    if dice(25*g.rank) + mod*g.rank >= (g.get_stat("obedience") + g.get_fear() + brothel.get_security()):
                        result = "runaway"

                if not result:
                    if 25*g.rank + mod*g.rank >= (g.get_stat("obedience") + g.get_fear() + brothel.get_security()):
                        result = "warning"

            return result

        def get_working_chance(self, act):
            '''获取工作成功率 | Get working success chance'''
            g = self.girl
            chance = 100 - g.get_obedience_check_target(act)

            return get_change_min_max(0, chance, 0, 100)


        def get_training_chance(self, act): # Chance to accept training
            '''获取训练接受率 | Get training acceptance chance'''
            g = self.girl
            chance = 100 - g.get_obedience_check_target(act, train=True)

            return get_change_min_max(0, chance, 0, 100)

        # ── Farm build-up ──

        def build_up(self, v): # FARM EVENTS - Builds-up her farm show jauge
            g = self.girl
            try:
                g.buildup += v
            except:
                g.buildup = v

            g.buildup = clamp(g.buildup, 0, 200)

            if g.buildup >= 100:
                if not story_flags["farm shows"]:
                    calendar.set_alarm(calendar.time+1, StoryEvent("farm_shows_intro", arg=g, type = "morning"))
                    g.flags["buildup warning 100"] = True
                elif not g.flags["buildup warning 100"]:
                    notify(__("%s is now ready to attend a farm show (100%).") % g.fullname)
                    g.flags["buildup warning 100"] = True
                elif g.buildup >= 150 and not g.flags["buildup warning 150"]:
                    notify(__("%s is now ready to attend a farm show (150%).") % g.fullname)
                    g.flags["buildup warning 150"] = True
                elif g.buildup >= 200 and not g.flags["buildup warning 200"]:
                    notify(__("%s is now ready to attend a farm show (200%).") % g.fullname)
                    g.flags["buildup warning 200"] = True

        def get_build_up(self): # FARM EVENTS - Recovers her farm show jauge
            g = self.girl
            try:
                return g.buildup
            except:
                g.buildup = 0
                return g.buildup

        def reset_build_up(self):
            g = self.girl
            g.buildup = 0
            g.flags["buildup warning 100"] = False
            g.flags["buildup warning 150"] = False
            g.flags["buildup warning 200"] = False
