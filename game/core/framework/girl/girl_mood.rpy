#### GirlMood — Mood, sanity, energy, health | 情绪、理智、体力、健康 ####
# Phase 2.1: Mood, sanity, energy, health, exhaustion, hurt.
# 情绪、理智、体力、健康、疲惫、伤害
# ★ change_energy/heal/full_rest/rest — 已从 girlclass.rpy 移入
# Methods: init_sanity, get_sanity, update_mood, change_mood,
#          get_mood_modifier, get_mood_description, build_up, etc.

init -2 python:

    class GirlMood(object):
        """Mood, sanity, and energy management for a Girl.

        Each method delegates to the Girl's _impl alias, which points to
        the original implementation in girlclass.rpy.
        """

        def __init__(self, girl):
            self.girl = girl

        # ── Sanity ──
        # ── 理智值管理 | Sanity management ──

        def init_sanity(self):
            '''初始化理智值 | Initialize girl's sanity based on rank and dominance'''
            g = self.girl
            if g.is_("very dom"): mod = 7
            elif g.is_("dom"): mod = 5
            else: mod = 4
            g.sanity = dice(11, g.rank) + mod * g.rank

        def rank_up_sanity(self):
            '''升级时增加理智值 | Increase sanity on rank up'''
            g = self.girl
            if g.is_("very dom"): mod = 7
            elif g.is_("dom"): mod = 5
            else: mod = 4
            g.sanity += dice(11) + mod

        def lose_sanity(self, cost):
            '''减少理智值（含效果修正）| Decrease sanity with effect modifiers'''
            g = self.girl
            g.sanity -= cost * g.get_effect("boost", "sanity loss") - g.get_effect("change", "sanity loss")
            if g.sanity <= 0:
                g.broken = True
            return g.sanity_warning()

        def get_sanity(self):
            '''获取理智值文本描述 | Get sanity status as localized text'''
            g = self.girl
            if g.broken: san = event_color["very bad"] % __("Broken")
            elif g.sanity < 5: san = event_color["very bad"] % __("Nearly broken")
            elif g.sanity < 10: san = event_color["bad"] % __("Very frail")
            elif g.sanity < 20: san = event_color["a little bad"] % __("Frail")
            elif g.sanity < 50: san = event_color["a little bad"] % __("Shaken")
            else: san = event_color["a little bad"] % __("Normal")
            if debug_mode: san += " (%i)" % g.sanity
            return san

        def sanity_warning(self):
            '''理智值过低时返回警告文本 | Warning text when sanity is very low'''
            g = self.girl
            if g.broken:
                calendar.set_alarm(calendar.time + 1, StoryEvent("is_broken", arg=g, type="morning"))
                renpy.play(s_scream_loud, "sound")
                return event_color["fear"] % (__("A long, inhumane shriek sends shivers down your spine. It came from %s, who is white with terror and on the verge of collapsing. This can't be good...") % g.name)
            elif g.sanity < 5:
                return event_color["very bad"] % (__("%s has a look of sheer terror in her eyes, and she shakes uncontrollably. She moans like a wounded animal if you move even slightly towards her. You can tell that a slight push would be all it takes to send her mind over the edge now.") % g.name)
            elif g.sanity < 10:
                return event_color["bad"] % (__("%s curls and looks around herself in complete panic, her eyes wild with fear. If you insist on using your powers on her, her mind will end up breaking.") % g.name)

        # ── Energy & health (implementations moved from girlclass.rpy) ──
        def change_energy(self, x):
            g = self.girl
            _min, _max = g.get_stat_minmax("energy")
            boost = reverse_if(g.get_effect("boost", "energy"), x)
            r = get_change_min_max(g.energy, x * boost + g.get_effect("change", "energy"), _min, _max)

            if g in farm.girls:
                if farm.exhaust_girl(g, energy=g.energy + r):
                    notify(__("%s was so tired that she fell sick for %i day%s") % (g.fullname, g.hurt, plural(g.hurt)), pic=g.portrait, col="bad")

            g.energy += r

            if g.energy <= 0:
                if not g.exhausted:
                    g.exhausted = True
                    g.resting = True
                    update_effects()
                return r, "exhausted"
            elif g.energy >= _max:
                if g.exhausted:
                    g.exhausted = False
                    g.resting = False
                    update_effects()
                    return r, "recovered"
            return r, ""

        def tire(self, x):
            return self.girl._tire_impl(x)
        def get_hurt(self, x):
            return self.girl._get_hurt_impl(x)
        def health_check(self):
            return self.girl._health_check_impl()

        def heal(self, chg=1, from_item=False):
            g = self.girl
            chg = chg * g.get_effect("boost", "heal") + g.get_effect("change", "heal")
            g.hurt = max(g.hurt - chg, 0)
            if from_item:
                g.last_healing_item = calendar.time
            if g.hurt > 0:
                return chg, "sick"
            else:
                update_effects()
                notify(__("%s is fully healed.") % g.fullname, pic=g.portrait)
                return chg, "healthy"

        def full_rest(self):
            g = self.girl
            g.hurt = 0
            g.energy = g.get_stat_minmax("energy")[1]

        def rest(self, context=None, mod=1):
            g = self.girl
            if context == "farm":
                resting_changes = NightChangeLog(title=__("Holding"))
                resting_text = __("%s rested in her pen today.") % g.fullname
            else:
                resting_changes = NightChangeLog(title=__("Resting"))
                resting_text = __("%s rested in her room today.") % g.fullname

            if g.hurt > 0:
                r, case = g.heal(1)
                resting_changes.add("\n{color=[c_green]}Health{/color}: %s" % plus_text(r, color_scheme="standard"))
                if case == "healthy":
                    resting_changes.add("(full recovery)", "header", col="good", separator="\n")
                    if context == "farm":
                        resting_text += __("\n{color=[c_emerald]}She is now fully recovered and can go back to work or training.{/color}")
                    elif g.job:
                        resting_text += __("\n{color=[c_emerald]}She is now fully recovered and can go back to work as a %s.{/color}") % __(g.job.capitalize())
                    else:
                        resting_text += __("\n{color=[c_emerald]}She is now fully recovered and went back to resting.{/color}")

            x = (25 + g.get_stat("constitution")/4) * g.get_effect("boost", "energy when resting") + g.get_effect("change", "energy when resting")
            if g.hurt > 0:
                x = x // 2
            x *= mod

            r, case = g.change_energy(x)
            max_en = g.get_stat_max("energy")

            if g.energy >= 0.8 * max_en:   col = c_green
            elif g.energy >= 0.6 * max_en: col = c_lightgreen
            elif g.energy >= 0.4 * max_en: col = c_yellow
            elif g.energy >= 0.2 * max_en: col = c_lightred
            else:                          col = c_red

            resting_changes.add("Energy: %s/%i (%s)" % ("{color=%s}%i{/color}" % (col, g.energy), max_en, plus_text(r)), "header")

            if case == "recovered":
                resting_changes.add("(fully rested)", "header", col="good", separator="\n")
                if context == "farm":
                    resting_text += __("\n{color=[c_emerald]}She is now fully rested and can go back to her training.{/color}")
                elif g.job:
                    resting_text += __("\n{color=[c_emerald]}She is now fully rested and can go back to work as a %s.{/color}") % __(g.job.capitalize())
                else:
                    resting_text += __("\n{color=[c_emerald]}She is now fully rested and is waiting for a job assignment.{/color}")

            return resting_text, resting_changes

        def can_heal_from_item(self):
            return self.girl._can_heal_from_item_impl()
        def get_energy_color(self):
            return self.girl._get_energy_color_impl()
        def get_energy_ttip(self):
            return self.girl._get_energy_ttip_impl()

        # ── Mood ──
        def update_mood(self, resting=False):
            return self.girl._update_mood_impl(resting)
        def change_mood(self, chg):
            return self.girl._change_mood_impl(chg)
        def get_mood_modifier(self, love_text="", fear_text="", description=False, resting=False):
            return self.girl._get_mood_modifier_impl(love_text, fear_text, description, resting)
        def get_mood_description(self, filter=None):
            return self.girl._get_mood_description_impl(filter)
        def get_mood_picture(self):
            return self.girl._get_mood_picture_impl()

        # ── Farm build-up ──
        def build_up(self, v):
            return self.girl._build_up_impl(v)
        def get_build_up(self):
            return self.girl._get_build_up_impl()
        def reset_build_up(self):
            return self.girl._reset_build_up_impl()
