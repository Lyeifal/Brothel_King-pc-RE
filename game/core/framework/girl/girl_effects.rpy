#### GirlEffects — Effect query & management component | 效果查询与管理组件 ####
# Phase 2.1: 效果列表、效果获取、效果移除 | Effect listing, retrieval, removal
# Methods: list_effects, get_effect, remove_effects

init -2 python:

    class GirlEffects(object):
        '''效果查询与管理 | Effect query and management for a Girl'''

        def __init__(self, girl):
            # 持有 Girl 实例引用 | Hold reference to the Girl instance
            self.girl = girl

        def list_effects(self):
            '''列出所有效果 | List all active effects as a text summary'''
            g = self.girl
            msg = ""
            for eff in g.effects:
                msg += eff.type + " " + eff.target + ", "

            return msg

        def get_effect(self, type, target, raw=False, custom_scale=("factor", 0), change_cap=False):
            '''获取效果值 | Get effect value for a type/target pair

            raw=True 时不叠加青楼/世界效果（获取字符串值时必须）| raw=True excludes brothel/world effects (MUST for string values)
            custom_scale 是用于部分特权的元组 ('factor name', 'value') | custom_scale is a tuple used for some perks
            change_cap=True 只返回影响属性上下限的效果 | change_cap=True only returns effects affecting stat min/max
            '''
            g = self.girl

            # 目前仅青楼效果生效 | Only brothel effects are currently in use

            r = get_effect(thing=g, type=type, target=target, custom_scale=custom_scale, change_cap=change_cap)

            if not raw:
                if type == "boost":
                    if g in MC.girls:
                        r *= get_effect(brothel, type, target, change_cap=change_cap)
                    elif g in farm.girls:
                        r *= get_effect(farm, type, target, change_cap=change_cap)
                    elif g in game.free_girls:
                        r *= get_effect(game, type, target, change_cap=change_cap)

                else:
                    if g in MC.girls:
                        r += get_effect(brothel, type, target, change_cap=change_cap)
                    elif g in farm.girls:
                        r += get_effect(farm, type, target, change_cap=change_cap)
                    elif g in game.free_girls:
                        r += get_effect(game, type, target, change_cap=change_cap)

            return r

        def remove_effects(self, effects):
            '''移除效果并刷新性行为 | Remove effects and refresh available sex acts'''
            g = self.girl
            remove_effects(g, effects)
            g.refresh_sex_acts() # Checks if sex_acts can still be done
