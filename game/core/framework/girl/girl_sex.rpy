#### GirlSex — Sex acts, fixations, preferences component ####
# Phase 2.1: 性行为、固恋、偏好管理 | Sex act, fixation, and preference management
# ★ does_anything/will_do_anything/count_available_sex_acts/get_trainable_sex_acts/has_activated_sex_acts — 已从 girlclass.rpy 移入 (Phase 7 批次8)
# ★ generate_preferences（合并 girlclass 外层校验）/add_random_fixation/reset_sex_acts — 已从 girlclass.rpy 移入 (Phase 7 批次8)
# ★ get_preference/get_preference_bonus/get_sex_act_modifier/test_weakness/get_reaction_to_act/pop_virginity/restore_virginity (Phase 7 批次8)
# ★ talk_tastes/has_fixation/remove_fixation/try_to_remove_fix (Phase 7 批次8)
# 待迁移: count_activated_sex_acts, compare_preference

init -2 python:

    class GirlSex(object):
        '''性行为相关管理 | Sex act management for a Girl.'''

        def __init__(self, girl):
            # 持有 Girl 实例引用 | Hold reference to the Girl instance
            self.girl = girl

        # ── 性行为检查 | Sex act checks ──

        def will_do_sex_act(self, sex_act, use_desc=False):
            '''检查女孩是否愿意进行某性行为 | Check if a girl will perform a sex act'''
            g = self.girl
            sex_act = sex_act.lower()

            if sex_act in all_sex_acts:
                tests = sex_act_test[sex_act]
                modifier = g.get_sex_act_modifier(sex_act)
                for stat, target in tests:
                    target += modifier
                    if g.get_stat(stat) < target:
                        if use_desc:
                            return False, sex_act.capitalize() + __(" cannot be activated.\n") + event_color["a little bad"] % (__("Her {b}%s{/b} is too low (min: %s).") % (stat.lower(), str(target)))
                        return False

            min_pref = g.get_effect("special", "minimum preference", raw=True) or "reluctant"
            if not compare_preference(g, sex_act, min_pref):
                if use_desc:
                    return False, sex_act.capitalize() + __(" cannot be activated.\n") + event_color["a little bad"] % (__("Her preference for {b}%s{/b} acts is too low. She requires more training.") % sex_act.lower())
                return False

            if use_desc:
                return True, ""
            return True

        def toggle_sex_act(self, sex_act):
            '''切换性行为开关 | Toggle sex act on/off'''
            g = self.girl
            sex_act = sex_act.lower()
            if g.does[sex_act]:
                g.does[sex_act] = False
                if not g.has_activated_sex_acts() and g.job == "whore":
                    g.set_job(None)
                    renpy.say("", __("%s cannot remain a whore if you deactivate all sex acts. She has been set to rest.") % g.fullname)
            else:
                result = g.will_do_sex_act(sex_act, use_desc=True)
                if result[0]:
                    g.does[sex_act] = True
                    if use_desc:
                        return result[1]
                elif use_desc:
                    return result[1]

        def does_anything(self): ## Tests if the girl has any activated sex act. She will be excluded from whoring if she isn't.
            '''检查是否有任何已激活的性行为 | Check if any sex act is activated'''
            g = self.girl
            for act in all_sex_acts:
                if g.does[act]:
                    return True

            return False


        def will_do_anything(self): ## Tests if the girl is open to a sex act. She will be excluded from the whore job if she isn't.
            # 检查是否对任何性行为开放 | Check if open to any sex act
            g = self.girl
            for act in all_sex_acts:
                if g.will_do_sex_act(act):
                    return True

            return False


        def count_available_sex_acts(self, discovered=True, extended=True): # unused
            # 统计可用的性行为数量 | Count available sex acts
            g = self.girl
            if extended:
                acts = extended_sex_acts
            else:
                acts = all_sex_acts

            if discovered:
                return sum(1 for act in acts if (g.will_do_sex_act(act) and g.personality_unlock[act]))
            return sum(1 for act in acts if g.will_do_sex_act(act))


        def get_trainable_sex_acts(self):
            # 获取可训练的性行为列表 | Get trainable sex acts
            g = self.girl
            available_acts = []
            _debug = ""

            for act in extended_sex_acts:
                if training_test_dict[act]:
                    for cond, pref in training_test_dict[act]:
                        if compare_preference(g, cond, pref) and g.personality_unlock[act] != 0:
                            _debug += act + ": No cond "
                            available_acts.append(act)
                            break
                        elif not compare_preference(g, cond, pref):
                            _debug += act + ": %s is not %s " % (cond, pref)
                        elif not g.personality_unlock[act]:
                            _debug += act + ": No unlock "
                        else:
                            _debug += act + ": ???"
                else:
                    _debug += act + ": No cond "
                    available_acts.append(act)

            return available_acts


        def count_activated_sex_acts(self):
            # 统计已激活的性行为数 | Count activated sex acts
            return self.girl._count_activated_sex_acts_impl()

        def has_activated_sex_acts(self): # Checks if the girl has any sex acts activated
            # 是否有已激活的性行为 | Whether any sex acts are activated
            g = self.girl
            for act in all_sex_acts:
                if g.does[act]:
                    return True

            return False


        # ── 性行为激活/停用 | Sex act activation/deactivation ──

        def refresh_sex_acts(self):
            '''刷新性行为列表 | Ensure disabled sex acts stay unchecked, notify on changes'''
            g = self.girl
            for sex_act in all_sex_acts:
                if g.does[sex_act] and not g.will_do_sex_act(sex_act):
                    g.does[sex_act] = False
                    notify(__("%s can no longer do %s.") % (g.fullname, sex_act), pic=g.portrait)

        def activate_sex_act(self, sex_act):
            '''激活性行为 | Activate a sex act'''
            g = self.girl
            sex_act = sex_act.lower()
            if g.will_do_sex_act(sex_act):
                g.does[sex_act] = True
                return True
            return False

        def deactivate_sex_act(self, sex_act):
            '''停用性行为 | Deactivate a sex act'''
            g = self.girl
            sex_act = sex_act.lower()
            g.does[sex_act] = False
            if not g.has_activated_sex_acts() and g.job == "whore":
                renpy.say("", __("%s cannot remain a whore if you deactivate all sex acts. She has been set to rest.") % g.fullname)

        def get_sex_act_modifier(self, sex_act = "all"):
            # 获取性行为修正系数 | Get sex act modifier
            g = self.girl
            modifier = g.get_effect("change", "all sex acts requirements")

            if sex_act in extended_sex_acts:
                modifier += g.get_effect("change", sex_act + " requirements") # Unused for now

            return modifier


        # ── 固恋管理 | Fixation management ──

        def test_fix(self, name, unlock=False, feedback=False):
            '''测试固恋 | Test a fixation (optionally unlock it with feedback)'''
            g = self.girl
            r = g.check_fix(name)

            if r == "pos":
                if unlock:
                    if not g.personality_unlock[name]:
                        g.personality_unlock[name] = True
                        if feedback:
                            renpy.play(s_aaah, "sound")
                            renpy.say("", __("You have discovered %s's fixation with %s.") % (g.name, name))
                return "pos"
            elif r == "neg":
                if unlock:
                    if not g.personality_unlock[name]:
                        g.personality_unlock[name] = True
                        if feedback:
                            renpy.play(s_surprise, "sound")
                            renpy.say("", __("You have discovered %s's disgust for %s.") % (g.name, name))
                return "neg"
            else:
                return False

        def check_fix(self, fix_name):
            '''检查固恋状态 | Check fixation status (pos/neg/False)'''
            g = self.girl
            if fix_name in [fix.name for fix in g.pos_fixations]:
                return "pos"
            elif fix_name in [fix.name for fix in g.neg_fixations]:
                return "neg"
            else:
                return False

        def get_sex_attitude(self, act=None, fix=None):
            '''获取女孩对性行为或固恋的态度 | Get girl's attitude toward an act or fixation (fix is a String, not an Object)'''
            g = self.girl

            score = g.get_stat("libido")

            if act:
                score += g.preferences[act]
                if act in all_sex_acts:
                    score += g.get_stat(act)

            else: # 无性行为时（如亲吻、抚摸）| When there's no sex act, such as kissing or groping
                score += g.get_stat("obedience") - 75

            if fix:

                fix = make_list(fix)

                for fix_name in fix:
                    if fix_name in [fix.name for fix in g.pos_fixations]:
                        score += g.get_stat("sensitivity") // 2
                    elif fix_name in [fix.name for fix in g.neg_fixations]:
                        if g.is_("dom"):
                            score -= g.get_stat("sensitivity")
                        elif g.is_("very sub"):
                            score += g.get_stat("sensitivity") // 2
                        elif g.is_("sub"):
                            score += g.get_stat("sensitivity") // 4
            return score

        def get_preference_bonus(self, act, minion_type=None): # Used for farm shows. Returns a modifier between 35% and 185%, and a list of applied effects
            # 获取偏好加成（农场用）| Get preference bonus (for farm use)
            g = self.girl
            pref = g.get_preference(act)
            pref_effects = [pref]

            pref_bonus = 1.0 + farm_perform_dict["pref_bonus"][pref]

            if act in g.pos_acts:
                pref_bonus += farm_perform_dict["pref_bonus"]["positive act"]
                pref_effects.append("pos_act")
            if act in g.neg_acts:
                pref_bonus += farm_perform_dict["pref_bonus"]["negative act"]
                pref_effects.append("neg_act")

            if minion_type and minion_type == g.weakness:
                pref_bonus += farm_perform_dict["pref_bonus"]["farm weakness"]
                pref_effects.append("weakness")

            return pref_bonus, pref_effects


        def add_random_fixation(self, act=None, fixation=None, type="pos", nb=1): # When provided, fixation is the name (string), not the object
            # 添加随机固恋 | Add a random fixation
            g = self.girl
            # Returns False or a list of fixation names (may be only one)

            fixations = []

            if fixation:
                if fix_dict[fixation].available(g):
                    fixations.append(fixation)
                else:
                    return False
            
            else:
                if act:
                    available_fix = [(fix.name, fix.get_weight(g, type)) for fix in fix_dict.values() if fix.available(g, act, type)]
                else:
                    available_fix = [(fix.name, fix.get_weight(g, type)) for fix in fix_dict.values() if fix.available(g, type=type)]

                if available_fix:
                    fixations = weighted_choice(available_fix, nb) # always returns a list
                else:
                    debug_notify("No " + type + " fixations found for " + g.fullname)
                    return False

                if not fixations and debug_mode:
                    raise AssertionError("Couldn't find %s %s fixations among available list: %s" % (nb, type, available_fix))

                if len(fixations) < nb and debug_mode:
                    raise AssertionError("Couldn't find %s %s fixations among available list: %s" % (nb, type, available_fix))

            if type == "pos":
                g.pos_fixations += [fix_dict[f] for f in fixations]
            elif type == "neg":
                g.neg_fixations += [fix_dict[f] for f in fixations]

            return fixations # Returns a list of fixation names


        def reset_sex_acts(self, first=True):
            # 重置所有性行为 | Reset all sex acts
            g = self.girl
            g.pos_acts = []
            g.neg_acts = []

            for fix in g.pos_fixations:
                g.pos_acts += [a for a in fix.acts if a not in g.pos_acts]

            for fix in g.neg_fixations:
                g.neg_acts += [a for a in fix.acts if a not in g.neg_acts]

            if first:
                for act in g.pos_acts:
                    eff = Effect("change", act + " preferences changes", 25)
                    g.effects.append(eff) # Removed add_effects to improve performance
                    g.effect_dict[(eff.type, eff.target)].append(eff)

                for act in g.neg_acts:
                    eff = Effect("change", act + " preferences changes", -50)
                    g.effects.append(eff) # Removed add_effects to improve performance
                    g.effect_dict[(eff.type, eff.target)].append(eff)


        # ── 偏好管理 | Preference management ──

        def raise_preference(self, act, type=None, bonus=1, status_change=False, silent=False, use_effects=True, context="MC"):
            '''提升偏好 | Raise preference for an act (may go down with fixation modifiers; use_effects=False enforces positive)'''
            g = self.girl

            # 检查当前偏好 | Checks current preference

            _old = g.get_preference(act)

            # 测试：加入欲望加成 | Test: adding libido to the result

            change = g.get_stat("obedience")//2 + g.get_stat("libido")

            if use_effects:
                change += g.get_effect("change", act + " preferences changes") + g.get_effect("change", "all preferences changes") # preferences changes effects can be negative

                if context == "MC":
                    change *= MC.get_effect("boost", "MC training")

                elif context == "farm":
                    change *= MC.get_effect("boost", "farm training")

            if type == "love":
                change += g.get_love()
            elif type == "fear":
                change += g.get_fear()

            change *= bonus

            if change != 0:
                if change > 0 or use_effects:
                    change = g.change_preference(act, change, silent=silent)

            if change > 0 and use_effects: # Only happens if use_effects is on (normal case)
                if act not in ("naked", "service"): # All sex acts other than service influence naked preference a little
                    change2 = g.change_preference("naked", 0.25*change, silent=silent)

            _new = g.get_preference(act)

            # 状态变化时返回新偏好 | Returns new preference if there was a change in status

            if status_change:
                if _old != _new:
                    return change, _new
                else:
                    return change, False
            else:
                return change

        def change_preference(self, act, nb, fast=False, silent=False):
            '''改变偏好值 | Change preference value (fast disables some checks for performance)'''
            g = self.girl

            if fast:
                boost = 1.0
            else:
                boost = g.get_effect("boost", act + " preference increase") * g.get_effect("boost", "all sex acts preference increase") * game.get_diff_setting("pref")

                if g in farm.girls:
                    boost *= g.get_effect("boost", "farm preference increase") # To be replaced with "boost", "farm training" effect?

                boost = reverse_if(boost, nb)

            nb = get_change_min_max(g.preferences[act], nb*boost, -1000, 1000)

            g.preferences[act] += nb

            if not fast:
                if act == "bisexual" and compare_preference(g, "bisexual", "a little interested"):
                    story_flags["has_bis"] = True
                    if not bis_perk in g.perks:
                        g.acquire_perk(bis_perk, forced=True)
                        test_achievement("bisexual")

                if act == "group" and compare_preference(g, "group", "a little interested"):
                    story_flags["has_group"] = True
                    if not group_perk in g.perks:
                        g.acquire_perk(group_perk, forced=True)
                        test_achievement("group")
                    if compare_preference(g, "group", "very interested"):
                        if not orgy_perk in g.perks:
                            g.acquire_perk(orgy_perk, forced=True)

            if not silent:
                debug_notify("Changing " + act + " preference (%s), value: %i" % (g.fullname, nb), pic=g.portrait)

            return nb

        def get_preference(self, act, bonus=0):
            # 获取偏好值 | Get preference value for an act
            g = self.girl
            act = act.lower()
            pref = g.preferences[act] + bonus

            # Reminder: Base reluctance is negative

            for res in ("fascinated", "very interested", "interested", "a little interested", "indifferent", "a little reluctant", "reluctant", "very reluctant", "refuses"):
                if g.preferences[act] + bonus > get_preference_limit(act, res):
                    return res


        def compare_preference(self, sex_act, min_pref):
            # 比较偏好与最低要求 | Compare preference against a minimum threshold
            return self.girl._compare_preference_impl(sex_act, min_pref)

        # ── 处女膜管理 | Virginity management ──

        def pop_virginity(self, origin="brothel"):
            # 破处 | Pop virginity
            g = self.girl
            for trait in g.traits: # Update trait list in restore_virginity if adding new special traits
                if trait.name == "Virgin":
                    g.remove_trait(trait)

                    if origin == "brothel":
                        g.add_trait(housebroken_trait, _pos=1, no_perks=True)
                    elif origin == "farm":
                        g.add_trait(farmgirl_trait, _pos=1, no_perks=True)
                    elif origin == "MC" and g.get_love() > g.get_fear():
                        g.add_trait(t_pet_trait, _pos=1, no_perks=True)
                    elif origin == "MC" and g.get_love() <= g.get_fear():
                        g.add_trait(trauma_trait, _pos=1, no_perks=True)
                    elif origin == "rape":
                        g.add_trait(trauma_trait, _pos=1, no_perks=True)
                    elif origin == "chaos":
                        g.add_trait(chaos_trait, _pos=1)
                    else: # Catch all for other origins
                        g.add_trait(trait_dict["Kinky"], _pos=1)

                    return True

            else:
                return False


        def restore_virginity(self):
            # 恢复处女 | Restore virginity
            g = self.girl
            for t in (housebroken_trait, farmgirl_trait, trauma_trait, chaos_trait):
                if t in g.traits:
                    g.remove_trait(t)

            g.add_trait(virgin_trait, _pos=1)


        # ── 弱点测试 | Weakness testing ──

        def test_weakness(self, act, unlock=False, feedback=False):
            # 测试弱点 | Test a weakness
            g = self.girl
            _pos = False
            _neg = False

            if act in g.pos_acts:
                _pos=True

            if act in g.neg_acts:
                _neg=True

            if unlock:
                if not g.personality_unlock[act]:
                    g.personality_unlock[act] = True # Testing weakness unlocks the act for the personality screen

                    if feedback:
                        if _pos and _neg:
                            renpy.play(s_ahaa, "sound")
                            renpy.say("", __("You notice that %s is feeling a mix of pleasure and discomfort during %s. It seems she has ambivalent feelings about it.") % (g.name, __(long_act_description[act])))
                        elif _pos:
                            renpy.play(s_mmh, "sound")
                            renpy.say("", __("You notice that %s seems to enjoy %s.") % (g.name, __(long_act_description[act])))
                        elif _neg:
                            renpy.play(s_scream, "sound")
                            renpy.say("", __("You notice that %s seems disgusted by %s.") % (g.name, __(long_act_description[act])))

            return _pos, _neg


        # ── 偏好生成 | Preference generation ──

        def generate_preferences(self):
            '''生成女孩性偏好 (偏好值 + 固恋 + 性经历) | Generate sexual preferences'''
            g = self.girl
            g.preferences = copy.copy(base_reluctance)
            g.fix_level = defaultdict(int)
            g.locked_fix = []

            pos_fix_nb = 2
            neg_fix_nb = 1

            if g.is_("very modest"): neg_fix_nb += 2
            elif g.is_("modest"): neg_fix_nb += 1
            elif g.is_("very lewd"): pos_fix_nb += 2
            elif g.is_("lewd"): pos_fix_nb += 1

            if use_ini_sex and g.init_dict["sexual preferences/always_fixations"]:
                if len(g.init_dict["sexual preferences/always_fixations"]) <= pos_fix_nb:
                    g.pos_fixations = [fix_dict[fix] for fix in g.init_dict["sexual preferences/always_fixations"]]
                else:
                    g.pos_fixations = [fix_dict[fix] for fix in rand_choice(g.init_dict["sexual preferences/always_fixations"], nb=pos_fix_nb)]
                pos_fix_nb -= len(g.pos_fixations)

            if pos_fix_nb >= 1:
                g.add_random_fixation(type="pos", nb=pos_fix_nb)
            if g.personality.name == "masochist":
                g.add_random_fixation(act="fetish")

            if use_ini_sex and g.init_dict["sexual preferences/always_negative_fixations"]:
                if len(g.init_dict["sexual preferences/always_negative_fixations"]) <= neg_fix_nb:
                    g.neg_fixations = [fix_dict[fix] for fix in g.init_dict["sexual preferences/always_negative_fixations"]]
                else:
                    g.neg_fixations = [fix_dict[fix] for fix in rand_choice(g.init_dict["sexual preferences/always_negative_fixations"], nb=neg_fix_nb)]
                neg_fix_nb -= len(g.neg_fixations)

            if neg_fix_nb >= 1:
                g.add_random_fixation(type="neg", nb=neg_fix_nb)

            g.reset_sex_acts()

            if use_ini_sex and g.init_dict["sexual preferences/farm_weakness"] in farm_type_list:
                g.weakness = g.init_dict["sexual preferences/farm_weakness"]
            else:
                g.weakness = rand_choice(farm_type_list)

            if use_ini_sex and g.init_dict["sexual preferences/sexual_experience"] in ["very experienced", "experienced", "average", "inexperienced", "very inexperienced"]:
                g.sexual_experience = g.init_dict["sexual preferences/sexual_experience"]
                g.training_value = sexual_training_value[g.sexual_experience]
            else:
                d = dice(6, 2)
                if g.free:
                    if g.is_("very lewd"): d += 2
                    elif g.is_("lewd"): d += 1
                    elif g.is_("very modest"): d -= 2
                    elif g.is_("modest"): d -= 1
                else:
                    if g.is_("very sub"): d += dice(3) - 1
                    elif g.is_("sub"): d += dice(2) - 1
                    elif g.is_("very dom"): d -= -1 * dice(3) + 1
                    elif g.is_("dom"): d -= -1 * dice(2) + 1

                if d >= 12: g.sexual_experience = "very experienced"
                elif d >= 10: g.sexual_experience = "experienced"
                elif d >= 5: g.sexual_experience = "average"
                elif d >= 3: g.sexual_experience = "inexperienced"
                else: g.sexual_experience = "very inexperienced"
                g.training_value = sexual_training_value[g.sexual_experience]

            pos_bonus, av_bonus, neg_bonus = experienced_modifiers[g.sexual_experience]

            for act in g.preferences.keys():
                if g.free:
                    if act in g.pos_acts and not act in g.neg_acts:
                        if pos_bonus: g.change_preference(act, pos_bonus * district.rank + dice(pos_bonus, district.rank), fast=True, silent=True)
                    elif act in g.neg_acts and not act in g.pos_acts:
                        if neg_bonus > 0: g.change_preference(act, neg_bonus * district.rank + dice(neg_bonus, district.rank), fast=True, silent=True)
                        elif neg_bonus < 0: g.change_preference(act, neg_bonus * district.rank - dice(-1 * neg_bonus, district.rank), fast=True, silent=True)
                    else:
                        if av_bonus: g.change_preference(act, av_bonus * district.rank + dice(av_bonus, district.rank), fast=True, silent=True)
                else:
                    d = dice(6)
                    if d >= 5:
                        if pos_bonus: g.change_preference(act, pos_bonus * district.rank + dice(pos_bonus, district.rank), fast=True, silent=True)
                    elif d < 2:
                        if neg_bonus > 0: g.change_preference(act, neg_bonus * district.rank + dice(neg_bonus, district.rank), fast=True, silent=True)
                        elif neg_bonus < 0: g.change_preference(act, neg_bonus * district.rank - dice(-1 * neg_bonus, district.rank), fast=True, silent=True)
                    else:
                        if av_bonus: g.change_preference(act, av_bonus * district.rank + dice(av_bonus, district.rank), fast=True, silent=True)


            # Generate x skills according to preferences

            g.generate_stats(sex=True)

            ## Regulations (sanity check)

            # Naturist girls are at least comfortable about being naked
            if g.get_effect("special", "naked"):
                if g.preferences["naked"] < 0:
                    g.preferences["naked"] = 0

            # Virgin girls cannot be experienced with sx or group
            if g.has_trait("Virgin"):
                g.preferences["sex"]=base_reluctance["sex"]
                g.preferences["group"]=base_reluctance["group"]
                g.change_stat("sex", -250, silent=True)

            # Add limits to group and boosts to nkd?

            # NewGame+ settings

            if NGP_settings_dict["preferences1"].get():
                for act in ("naked", "service"):
                    g.change_preference(act, NGP_settings_dict["preferences1"].get(), fast=True, silent=True)

            if NGP_settings_dict["preferences2"].get():
                for act in ("sex", "anal"):
                    g.change_preference(act, NGP_settings_dict["preferences2"].get(), fast=True, silent=True)

            if NGP_settings_dict["preferences3"].get():
                for act in ("fetish", "bisexual", "group"):
                    g.change_preference(act, NGP_settings_dict["preferences3"].get(), fast=True, silent=True)

            # /NewGame+ settings

            return

        # ── 固恋移除 | Fixation removal ──

        def has_fixation(self, type="pos", fix_name=None):
            # 检查是否有特定固恋 | Check if has a specific fixation
            g = self.girl
            if type == "pos":
                for fix in g.pos_fixations:
                    if fix.name == fix_name:
                        return True

            if type == "neg":
                for fix in g.neg_fixations:
                    if fix.name == fix_name:
                        return True


        def remove_fixation(self, fix_name):
            # 移除固恋 | Remove a fixation
            g = self.girl
            for fix in g.pos_fixations:
                _type = "pos"
                if fix.name == fix_name:
                    g.pos_fixations.remove(fix)
                    # Resets farm
                    if fix in farm.knows["pos_fix"][g]:
                        farm.knows["pos_fix"][g].remove(fix)

            for fix in g.neg_fixations:
                _type = "neg"
                if fix.name == fix_name:
                    g.neg_fixations.remove(fix)
                    # Tracks removed fixations for the 'Phobia' achievement
                    try:
                        g.flags["removed neg fixations"] += 1
                    except:
                        g.flags["removed neg fixations"] = 1
                    # Resets farm
                    if fix in farm.knows["neg_fix"][g]:
                        farm.knows["neg_fix"][g].remove(fix)

            g.reset_sex_acts(first=False)

            # Removes fixation preference bonuses/penalties
            for act in fix.acts:
                if type == "pos" and act not in g.pos_acts:
                    g.remove_effects([Effect("change", act + " preferences changes", 25)])
                if type == "neg" and act not in g.neg_acts:
                    g.remove_effects([Effect("change", act + " preferences changes", -50)])


        def try_to_remove_fix(self, fix_name, type=None):
            # 尝试移除固恋 | Try to remove a fixation
            g = self.girl
            if type == "love":
                chance = 40 + (g.mood + g.get_love() - g.get_fear()) // 3
                lock_chance = 0
            elif type == "neutral":
                chance = 40
                lock_chance = 0
            elif type == "fear": # Fear gives a higher bonus and ignores mood but may lock a girl's negative fixation
                chance = 50 + g.get_fear()
                lock_chance = 3

            if dice(100) < lock_chance:
                g.locked_fix.append(fix_name)
                return "locked"

            elif dice(100) < chance:
                g.fix_level[fix_name] += 1

                if g.fix_level[fix_name] < 4:
                    return g.fix_level[fix_name]

                else:
                    g.remove_fixation(fix_name)
                    return "success"

            else:
                return "fail"


        def get_reaction_to_act(self, act):
            g = self.girl
            pos_reaction, neg_reaction = g.test_weakness(act)

            if pos_reaction and neg_reaction:
                return "ambivalent feelings"
            elif pos_reaction:
                return "a weakness"
            elif neg_reaction:
                return "a disgust"
            else:
                return "no particular reaction"

        def talk_tastes(self, type):
            g = self.girl
            if type == "likes":
                mylist = ["color", "food", "drink"]
                renpy.random.shuffle(mylist)

                for thing in mylist:
                    if not g.personality_unlock["fav_" + thing]:
                        break
                else:
                    thing = rand_choice(mylist)
                return thing, g.likes[thing]

            elif type == "dislikes":
                mylist = ["color", "food", "drink"]
                renpy.random.shuffle(mylist)

                for thing in mylist:
                    if not g.personality_unlock["dis_" + thing]:
                        break
                else:
                    thing = rand_choice(mylist)
                return thing, g.dislikes[thing]

            elif type == "loves":
                best_replies = []
                all_replies = []

                for k in [k for k, v in g.personality.gift_likes.items() if v >= 3]:
                    if not k in g.personality_unlock["loves"]:
                        best_replies.append(("loves", k))
                    all_replies.append(("loves", k))

                for k in [k for k, v in g.personality.gift_likes.items() if 3 > v >= 0]:
                    if not k in g.personality_unlock["likes"]:
                        best_replies.append(("likes", k))
                    all_replies.append(("likes", k))

                if best_replies:
                    return rand_choice(best_replies)
                elif all_replies:
                    return rand_choice(all_replies)
                else:
                    return "indifferent", False

            elif type == "hates":
                best_replies = []
                all_replies = []

                for k in [k for k, v in g.personality.gift_likes.items() if v <= -2]:
                    if not k in g.personality_unlock["hates"]:
                        best_replies.append(("hates", k))
                    all_replies.append(("hates", k))

                if best_replies:
                    return rand_choice(best_replies)
                elif all_replies:
                    return rand_choice(all_replies)
                else:
                    return "indifferent", False
