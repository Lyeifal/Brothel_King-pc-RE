#### GirlTraining — Farm training, obedience, resistance | 农场训练与服从 ####
# Phase 2.1: 农场行为、服从检查、逃跑、反抗
# Farm acts, obedience checks, run away, resistance
# ★ will_do_farm_act / will_rebel_in_farm / farm_beg_test — 已迁入

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
            if train_mode == "gentle": return False

            if g.is_("very dom"): diff = 200
            elif g.is_("dom"): diff = 100
            elif g.is_("very sub"): diff = 0
            elif g.is_("sub"): diff = 50

            if train_mode == "tough": diff -= 25
            elif train_mode == "hardcore": diff += 25
            if reaction == "accepted": diff -= 25
            elif reaction == "refused": diff += 25

            # 恐惧比爱更影响反抗 | Fear impacts rebel chances more than love
            return dice(100) < (diff - g.get_love() // 2 - g.get_fear() - g.get_stat("obedience"))

        def farm_beg_test(self):
            '''测试女孩是否求饶 | Test if girl begs not to go to farm'''
            g = self.girl
            r = dice(10) - g.get_stat("obedience") // 50
            if g.is_("very sub"): r += 2
            elif g.is_("sub"): r += 1
            elif g.is_("very dom"): r -= 1
            if g.is_("very modest"): r += 2
            elif g.is_("modest"): r += 1
            elif g.is_("very lewd"): r -= 2
            elif g.is_("lewd"): r -= 1
            if g.get_love() > 5: r -= 1
            elif g.get_love() < -5: r += 1
            return r <= 0

        # ── 服从与逃跑 | Obedience & run away ──

        def get_obedience_check_target(self, act=None, train=False):
            '''获取服从检查的目标值 | Get target for obedience check'''
            return self.girl._get_obedience_check_target_impl(act, train)

        def obedience_check(self, act=None):
            '''执行服从检查 | Perform an obedience check'''
            return self.girl._obedience_check_impl(act)

        def training_check(self, act):
            '''执行训练检查 | Perform a training check'''
            return self.girl._training_check_impl(act)

        def run_away_check(self):
            '''检查女孩是否尝试逃跑 | Check if girl runs away'''
            return self.girl._run_away_check_impl()

        def get_working_chance(self, act):
            '''获取工作成功率 | Get working success chance'''
            return self.girl._get_working_chance_impl(act)

        def get_training_chance(self, act):
            '''获取训练接受率 | Get training acceptance chance'''
            return self.girl._get_training_chance_impl(act)
