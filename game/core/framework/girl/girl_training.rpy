#### GirlTraining — Farm training, obedience, resistance | 农场训练组件 ####
# Phase 2.1: 农场训练、服从检查、逃跑检查
# Farm acts, obedience checks, run away checks, resistance
# Methods: will_do_farm_act, will_rebel_in_farm, farm_beg_test,
#          obedience_check, training_check, run_away_check,
#          get_working_chance, get_training_chance

init -2 python:

    class GirlTraining(object):
        '''农场训练与服从管理 | Farm training and obedience for a Girl'''

        def __init__(self, girl):
            self.girl = girl

        # ── 农场行为 | Farm acts ──

        def will_do_farm_act(self, act, mode=None):
            '''检查女孩是否愿意进行农场训练 | Check if girl will perform a farm act'''
            return self.girl._will_do_farm_act_impl(act, mode)

        def will_rebel_in_farm(self, train_mode, reaction):
            '''判断女孩是否会反抗训练 | Determine if girl rebels against training'''
            return self.girl._will_rebel_in_farm_impl(train_mode, reaction)

        def farm_beg_test(self):
            '''女孩是否求饶 | Determine if girl begs not to go to farm'''
            return self.girl._farm_beg_test_impl()

        # ── 服从检查 | Obedience checks ──

        def get_obedience_check_target(self, act=None, train=False):
            '''获取服从检查目标值 | Get target value for obedience check'''
            return self.girl._get_obedience_check_target_impl(act, train)

        def obedience_check(self, act=None):
            '''执行服从检查 | Perform an obedience check'''
            return self.girl._obedience_check_impl(act)

        def training_check(self, act):
            '''执行训练检查 | Perform a training check'''
            return self.girl._training_check_impl(act)

        def run_away_check(self):
            '''检查女孩是否尝试逃跑 | Check if girl attempts to run away'''
            return self.girl._run_away_check_impl()

        def get_working_chance(self, act):
            '''获取工作成功率 | Get working success chance'''
            return self.girl._get_working_chance_impl(act)

        def get_training_chance(self, act):
            '''获取训练接受率 | Get training acceptance chance'''
            return self.girl._get_training_chance_impl(act)
