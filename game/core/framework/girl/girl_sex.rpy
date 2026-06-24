#### GirlSex — Sex acts, fixations, preferences component ####
# Phase 2.1: 性行为、固恋、偏好管理 | Sex act, fixation, and preference management
# Methods to migrate: 需迁移的方法:
# will_do_sex_act, toggle_sex_act, does_anything, will_do_anything,
# count_available_sex_acts, get_trainable_sex_acts, refresh_sex_acts,
# activate_sex_act, deactivate_sex_act, get_sex_act_modifier,
# pop_virginity, restore_virginity, test_fix, check_fix,
# get_sex_attitude, add_random_fixation, reset_sex_acts,
# raise_preference, change_preference, get_preference,
# compare_preference, get_preference_bonus, test_weakness,
# has_fixation, remove_fixation, try_to_remove_fix

init -2 python:

    class GirlSex(object):
        '''性行为相关管理 | Sex act management for a Girl.'''

        def __init__(self, girl):
            # 持有 Girl 实例引用 | Hold reference to the Girl instance
            self.girl = girl

        # ── 性行为检查 | Sex act checks ──

        def will_do_sex_act(self, sex_act):
            # 检查女孩是否愿意进行某性行为 | Check if girl will do a sex act
            g = self.girl
            if sex_act not in g.does:
                return False
            if not g.does[sex_act]:
                return False
            if g.hurt > 0 or g.exhausted:
                return False
            if g.away:
                return False
            if g.farm and sex_act not in farm_hardcore_acts:
                return False
            return True

        def toggle_sex_act(self, sex_act):
            # 切换性行为开关 | Toggle a sex act on/off
            return self.girl._toggle_sex_act_impl(sex_act)

        def does_anything(self):
            # 检查是否有任何已激活的性行为 | Check if any sex act is activated
            return self.girl._does_anything_impl()

        def will_do_anything(self):
            # 检查是否对任何性行为开放 | Check if open to any sex act
            return self.girl._will_do_anything_impl()

        def count_available_sex_acts(self, discovered=True, extended=True):
            # 统计可用的性行为数量 | Count available sex acts
            return self.girl._count_available_sex_acts_impl(discovered, extended)

        def get_trainable_sex_acts(self):
            # 获取可训练的性行为列表 | Get trainable sex acts
            return self.girl._get_trainable_sex_acts_impl()

        def count_activated_sex_acts(self):
            # 统计已激活的性行为数 | Count activated sex acts
            return self.girl._count_activated_sex_acts_impl()

        def has_activated_sex_acts(self):
            # 是否有已激活的性行为 | Whether any sex acts are activated
            return self.girl._has_activated_sex_acts_impl()

        # ── 性行为激活/停用 | Sex act activation/deactivation ──

        def refresh_sex_acts(self):
            # 刷新性行为列表（移除不可用的）| Refresh sex acts, removing unavailable ones
            return self.girl._refresh_sex_acts_impl()

        def activate_sex_act(self, sex_act):
            # 激活性行为 | Activate a sex act
            return self.girl._activate_sex_act_impl(sex_act)

        def deactivate_sex_act(self, sex_act):
            # 停用性行为 | Deactivate a sex act
            return self.girl._deactivate_sex_act_impl(sex_act)

        def get_sex_act_modifier(self, sex_act="all"):
            # 获取性行为修正系数 | Get sex act modifier
            return self.girl._get_sex_act_modifier_impl(sex_act)

        # ── 固恋管理 | Fixation management ──

        def test_fix(self, name, unlock=False, feedback=False):
            # 测试固恋 | Test a fixation
            return self.girl._test_fix_impl(name, unlock, feedback)

        def check_fix(self, fix_name):
            # 检查固恋状态 | Check fixation status
            return self.girl._check_fix_impl(fix_name)

        def get_sex_attitude(self, act=None, fix=None):
            # 获取女孩对性行为或固恋的态度 | Get girl's attitude toward an act or fixation
            return self.girl._get_sex_attitude_impl(act, fix)

        def get_preference_bonus(self, act, minion_type=None):
            # 获取偏好加成（农场用）| Get preference bonus (for farm use)
            return self.girl._get_preference_bonus_impl(act, minion_type)

        def add_random_fixation(self, act=None, fixation=None, type="pos", nb=1):
            # 添加随机固恋 | Add a random fixation
            return self.girl._add_random_fixation_impl(act, fixation, type, nb)

        def reset_sex_acts(self, first=True):
            # 重置所有性行为 | Reset all sex acts
            return self.girl._reset_sex_acts_impl(first)

        # ── 偏好管理 | Preference management ──

        def raise_preference(self, act, type=None, bonus=1, status_change=False, silent=False, use_effects=True, context="MC"):
            # 提升偏好 | Raise preference for an act
            return self.girl._raise_preference_impl(act, type, bonus, status_change, silent, use_effects, context)

        def change_preference(self, act, nb, fast=False, silent=False):
            # 改变偏好值 | Change preference value
            return self.girl._change_preference_impl(act, nb, fast, silent)

        def get_preference(self, act, bonus=0):
            # 获取偏好值 | Get preference value for an act
            return self.girl._get_preference_impl(act, bonus)

        def compare_preference(self, sex_act, min_pref):
            # 比较偏好与最低要求 | Compare preference against a minimum threshold
            return self.girl._compare_preference_impl(sex_act, min_pref)

        # ── 处女膜管理 | Virginity management ──

        def pop_virginity(self, origin="brothel"):
            # 破处 | Pop virginity
            return self.girl._pop_virginity_impl(origin)

        def restore_virginity(self):
            # 恢复处女 | Restore virginity
            return self.girl._restore_virginity_impl()

        # ── 弱点测试 | Weakness testing ──

        def test_weakness(self, act, unlock=False, feedback=False):
            # 测试弱点 | Test a weakness
            return self.girl._test_weakness_impl(act, unlock, feedback)

        # ── 固恋移除 | Fixation removal ──

        def has_fixation(self, type="pos", fix_name=None):
            # 检查是否有特定固恋 | Check if has a specific fixation
            return self.girl._has_fixation_impl(type, fix_name)

        def remove_fixation(self, fix_name):
            # 移除固恋 | Remove a fixation
            return self.girl._remove_fixation_impl(fix_name)

        def try_to_remove_fix(self, fix_name, type=None):
            # 尝试移除固恋 | Try to remove a fixation
            return self.girl._try_to_remove_fix_impl(fix_name, type)
