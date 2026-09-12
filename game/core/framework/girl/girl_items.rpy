#### GirlItems — Equipment, items, inventory | 物品与装备组件 ####
# Phase 2.1: Manage girl items, equipment, inventory.
# 管理女孩物品、装备、背包
# Methods: equip, unequip, get_equipped, use_item, take, receive_gift

init -2 python:

    class GirlItems(object):
        '''物品与装备管理 | Item and equipment management for a Girl'''

        def __init__(self, girl):
            # 持有 Girl 实例引用 | Hold reference to the Girl instance
            self.girl = girl

        # ── 装备管理 | Equipment management ──

        def equip(self, item):
            '''装备物品到女孩 | Equip an item on the girl'''
            g = self.girl
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)
            for it in g.equipped:
                if it.slot == item.slot:
                    g.unequip(it)
            g.equipped.append(item)
            boost = g.get_effect("boost", item.type.name.lower())
            if boost != 1.0:
                item.effects = copy.deepcopy(item.effects)
                for eff in item.effects:
                    eff.value *= boost
            g.add_effects(item.effects)
            item.equipped = True
            g.refresh_sex_acts()
            test_achievements(["hands", "body", "finger", "neck", "accessory"])

        def unequip(self, item):
            '''卸下物品 | Unequip an item from the girl'''
            g = self.girl
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)
            g.equipped.remove(item)
            g.remove_effects(item.effects)
            item.equipped = False

        def get_equipped(self, slot):
            '''按槽位获取已装备物品 | Get equipped item by slot name'''
            g = self.girl
            for it in g.equipped:
                if it.slot == slot:
                    return it
            return None

        def use_item(self, item, night=False):
            '''使用物品（消耗品）| Use a consumable item'''
            g = self.girl
            # EN: Returns the name of the affected stat and the change value.
            # ZH: 返回受影响的属性名和变化值。
            changes = []
            for eff in item.type.effects:
                if eff.type in ("change", "boost"):
                    chg_name = eff.target
                    chg_value = eff.value * item.quality

                    if eff.target in gstats_main + gstats_sex:
                        chg_value, _chg = g.change_stat(eff.target, chg_value, apply_boost=False, spillover=False, silent=True)
                        changes.append((chg_name, chg_value))
                    elif eff.target == "energy":
                        chg, case = g.change_energy(chg_value)
                        changes.append(("energy", chg))
                    elif eff.target == "hurt":
                        g.heal(chg_value, from_item=True)
                        changes.append(("hurt", chg_value))
                    elif eff.target == "love":
                        g.change_love(chg_value, silent=True)
                        changes.append(("love", chg_value))
                    elif eff.target == "fear":
                        g.change_fear(chg_value, silent=True)
                        changes.append(("fear", chg_value))
                    else:
                        g.add_effects(eff)
                        changes.append((chg_name, chg_value))

            if not changes:
                renpy.say("", __("Nothing happened."))

            return changes

        def take(self, giver, obj):
            '''从给予者处获取物品 | Take an item from a giver'''
            g = self.girl
            if not g.equipped:
                giver.give(obj)
                return
            if "ring" in [it.type.name for it in g.equipped]:
                renpy.say("", __("You can't. She's wearing a ring."))
                return
            if g.get_effect("special", "monk"):
                renpy.say("", __("%s has taken a vow of poverty and refuses to have anything to do with material possessions...{w=1} including obscene amounts of currency.") % g.fullname)
                return
            if g.love <= 10:
                renpy.say("", __("%s looks at you suspiciously and refuses the gift.") % g.fullname)
                return
            if obj.value > g.love * 10:
                renpy.say("", __("%s is uncomfortable with such an expensive gift.") % g.fullname)
                return
            giver.give(obj)

        def receive_gift(self, item):
            '''收到礼物（含偏好/性格处理）| Receive a gift with personality handling'''
            return self.girl.receive_gift(item)
