#### GirlItems — Equipment, items, inventory | 物品与装备组件 ####
# Phase 2.1: Manage girl items, equipment, inventory.
# 管理女孩物品、装备、背包
# Methods: equip, unequip, get_equipped, use_item, take, receive_gift
# ★ unequip（合并 girlclass 外层 boost 还原）/get_equipped（None→False）/take/use_item — 以 girlclass 版覆盖组件旧手写版 (Phase 7 批次12)

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

            # Restores item effects if girl had boost item type effects
            boost = g.get_effect("boost", item.type.name.lower())

            if boost != 1.0: # Reminder: effects have been previously deep copied on equip
                for eff in item.effects:
                    eff.value /= boost

            g.refresh_sex_acts() # Checks if sex_acts can still be done

        def get_equipped(self, slot):
            '''按槽位获取已装备物品 | Get equipped item by slot name'''
            g = self.girl
            for it in g.equipped:
                if it.slot == slot:
                    return it
            return False

        def use_item(self, item, night=False):
            g = self.girl
            if not isinstance(item, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % item.name)

            changes = NightChangeLog(title=item.name)

            debug_notify("Using " + item.name + " on " + g.fullname, pic=g.portrait)

            used = False
            r = ""

            for e in item.effects:
                if e.type == "gain":
                    c = g.add_effects(e)
                    if c:
                        changes.add(e.target.capitalize() + _(" : %s") % plus_text(c))
                    used = True

                elif e.type == "change": # In case of direct usage, the change will last only for one turn or the item duration
                    if item.type.name == "Food": # Prevents stacking food effects for the same stat
                        if g.current_food_effect[e.target]:
                            changes.add(_("%s: %s (expired)") % (g.current_food_effect[e.target].target.capitalize(), plus_text(-g.current_food_effect[e.target].value)))
                            g.remove_effects(g.current_food_effect[e.target])

                        g.current_food_effect[e.target] = e # Stores the object used to remove the effect in case another food is absorbed

                    if e.duration > 0:
                        c = g.add_effects(e, expires = calendar.time + e.duration)
                        if c:
                            changes.add(_("%s: %s (duration: %s days)") % (e.target.capitalize(), plus_text(c), e.duration))
                    else:
                        c = g.add_effects(e, expires = calendar.time + 1)
                        if c:
                            changes.add(_("%s: %s") % (e.target.capitalize(), plus_text(c)))

                    used = True

                elif e.type in ("special", "instant"):
                    if e.target == "level":
                        if g.level < e.value:
                            g.xp = g.get_xp_cap()
                            g.level_up()
                            changes.add(_("Level: +1"), col=c_orange)
                            used = True
                        else:
                            notify(__("This item can only be used up to level %s") % e.value, pic=g.portrait)

                    elif e.target == "heal":
                        if not g.can_heal_from_item() and not night:
                            renpy.say("", __("Only one healing item can be used per day."))

                        elif g.hurt > 0:
                            c, _ = g.heal(e.value, from_item=True)
                            if c:
                                changes.add(__("Healing"), "header")
                                changes.add(__("Healed: %s") % plus_text(c))
                                if g.hurt <= 0:
                                    changes.add(__("(fully healed)"), col="good")
                                    if not night:
                                        renpy.say("", __("%s has been healed completely.") % g.name)
                                elif not night:
                                    renpy.say("", __("%s has been healed but still need some time to rest.") % g.name)
                                used = True
                        else:
                            notify(__("%s is in good health.") % g.name, pic=g.portrait)

                    # Virginity restoration
                    elif e.target == "virginity":
                        if not g.has_trait("Virgin"):
                            g.restore_virginity()
                            used = True

                    # Sanity restoration
                    elif e.target == "sanity":
                        g.init_sanity()
                        used = True

            if used:
                r = item.use_me()

                if r == "used_up" and item in g.items:
                    g.items.remove(item)
                    changes.add(__("(used up)"), col="bad")

                norollback()

            if night:
                return r, changes
            return r

        def take(self, giver, obj):
            '''从给予者处获取物品 | Take an item from a giver'''
            g = self.girl
            if not isinstance(obj, ItemInstance):
                renpy.say(bk_error, __("Warning: This item is not instantiated (%s).") % obj.name)

            g.items.append(obj)
            if obj.equipped:
                giver.unequip(obj)
            try:
                giver.items.remove(obj)
            except:
                pass

        def receive_gift(self, item):
            '''收到礼物（含偏好/性格处理）| Receive a gift with personality handling'''
            return self.girl.receive_gift(item)
