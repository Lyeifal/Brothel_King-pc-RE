#### GirlMood — Mood, sanity, energy, health | 情绪、理智、体力、健康 ####
# Phase 2.1: Mood, sanity, energy, health, exhaustion, hurt.
# 情绪、理智、体力、健康、疲惫、伤害
# ★ change_energy/heal/full_rest/rest/sanity_warning — 已从 girlclass.rpy 移入
# ★ update_mood/change_mood/get_mood_modifier/get_mood_description/get_mood_picture (Phase 7 批次1)
# ★ tire/get_hurt/health_check/get_energy_color/get_energy_ttip/tired_check (Phase 7 批次1)
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
                calendar.set_alarm(calendar.time+1, StoryEvent("is_broken", arg=g, type = "morning"))
                renpy.play(s_scream_loud, "sound")
                return event_color["fear"] % (__("A long, inhumane shriek sends shivers down your spine. It came from %s, who is white with terror and on the verge of collapsing. This can't be good...") % g.name)

            elif g.sanity < 5:
                return event_color["very bad"] % (__("%s has a look of sheer terror in her eyes, and she shakes uncontrollably. She moans like a wounded animal if you move even slightly towards her. You can tell that a slight push would be all it takes to send her mind over the edge now.") % g.name)

            elif g.sanity < 10:
                return event_color["bad"] % (__("%s curls and looks around herself in complete panic, her eyes wild with fear. If you insist on using your powers on her, her mind will end up breaking.") % g.name)

            elif g.sanity < 20:
                return event_color["a little bad"] % (__("%s looks bewildered, not sure what has been happening to her. Little by little her sanity is beginning to slip.") % g.name)

            elif g.sanity < 50:
                if g.is_("dom"):
                    return event_color["a little bad"] % (__("%s seems shaken by what just happened, but puts on a brave face. She looks defiant in spite of what she has been through.") % g.name)
                else:
                    return event_color["a little bad"] % (__("%s seems shaken by what just happened, but she tries to keep it to herself. She looks away from you, trying to suppress a sob.") % g.name)

            else:
                return (__("As %s returns to normal, she barely seems to register what just happened to her, although you know it must have had a subconscious effect.") % g.name)

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

        def tire(self, x): # Where x is a positive number (important)
            g = self.girl

            # Frenzy effect
            if g.get_effect("special", "ignore energy"):
                return "\n{color=[c_purple]}" + g.name + " is working tirelessly.{/color}", 0

            chg = x * g.get_effect("boost", "tiredness") + g.get_effect("change", "tiredness")

            # This is a test: reduce tiredness by 15% per rank

            chg *= g.get_effect("boost", "energy use") # (1 - (g.rank-1)*0.15)

            r, _case = g.change_energy(-chg)

            text1 = ""
            text2 = plus_text(round_int(r), "standard")

            if _case == "exhausted":
                text1 += "\n{color=[c_red]}" + g.name + " is too tired to continue working.{/color}"

                if g.hurt:
                    text1 += "\n{color=[c_red]}" + " She has fallen sick and must rest for " + str(round_int(g.hurt)) + " days.{/color}"

                g.add_log("exhausted")
                g.track_event("exhausted")

            return text1, r

        def get_hurt(self, x):
            g = self.girl

            if g.get_effect("special", "immune"):
                notify(_("%s is immune to getting hurt.") % g.name, pic=g.portrait)
                return 0

            chg = round(x * g.get_effect("boost", "hurt") + g.get_effect("change", "hurt") - g.get_effect("resist", "hurt"))

            g.hurt += chg

            if g.hurt > 0:
                g.interactions = 0
            elif g.hurt < 0:
                g.hurt = 0

            update_effects()

            if chg >= 1:
                notify(_("%s is hurt for %i day%s.") % (g.fullname, chg, plural(chg)), pic=g.portrait)

            return chg

        def health_check(self):
            g = self.girl

            d = dice(100) + g.get_stat("constitution") - brothel.dirt

            if d < -50:
                g.get_hurt(dice(5))
            elif d < -25:
                g.get_hurt(dice(3))
            elif d < -5:
                g.get_hurt(dice(2))

            if d < 0 and g.hurt > 0:
                g.track_event("sick")
                return "sick"

            return "healthy"

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
            return self.girl.can_heal_from_item()

        def get_energy_color(self):
            g = self.girl
            max_en = g.get_stat_max("energy")

            if g.energy >= 0.8 * max_en:
                return c_green
            elif g.energy >= 0.6 * max_en:
                return c_lightgreen
            elif g.energy >= 0.4 * max_en:
                return c_yellow
            elif g.energy >= 0.2 * max_en:
                return c_lightred
            else:
                return c_red

        def get_energy_ttip(self):
            g = self.girl
            max_en = g.get_stat_max("energy")

            if g.energy >= 0.8 * max_en:
                ttip = "She is well-rested."
            elif g.energy >= 0.6 * max_en:
                ttip = "She is rested."
            elif g.energy >= 0.4 * max_en:
                ttip = "She is a little tired."
            elif g.energy >= 0.2 * max_en:
                ttip = "She is quite tired."
            else:
                ttip = event_color["bad"] % "Warning! She is getting very tired."

            return ttip

        # ── Mood ──
        def update_mood(self, resting=False):
            g = self.girl
            g.change_mood(g.get_mood_modifier(resting=resting))

        def change_mood(self, chg):
            g = self.girl

            _min, _max = g.get_stat_minmax("mood")

            chg = get_change_min_max(g.mood, chg, _min, _max)

            g.mood += chg

            return chg

        def get_mood_modifier(self, love_text="", fear_text="", description=False, resting=False):
            g = self.girl

            ## Lists active mood modifiers
            mood_factors = ""

            # Love and Fear
            l = g.get_love()
            f = g.get_fear()

            if g.personality.name != "masochist":
                mood_change = (l - f)/10
                if l >= 1:
                    mood_factors += "+" + str(round_best(l/10)) + ": " + love_text + "\n"
                elif l <= -1:
                    mood_factors += str(round_best(l/10)) + ": " + love_text + "\n"
                if f >= 1:
                    mood_factors += str(round_best(-f/10)) + ": " + fear_text + "\n"
                elif f <= -1:
                    mood_factors += "+" + str(round_best(-f/10)) + ": " + fear_text + "\n"
            else:
                mood_change = (l + f)/20
                if l >= 2:
                    mood_factors += "+" + str(round_best(l/20)) + ": " + love_text + "\n"
                elif l <= -2:
                    mood_factors += str(round_best(l/20)) + ": " + love_text + "\n"
                if f >= 2:
                    mood_factors += "+" + str(round_best(f/20)) + ": " + fear_text + "\n"
                elif f <= -2:
                    mood_factors += str(round_best(f/20)) + ": " + fear_text + "\n"

            # Farm girls

            if g in farm.girls:
                if farm.programs[g].target == "no training" and farm.programs[g].holding == "rest":
                    mood_change += 1
                    mood_factors += "+1: She is resting at the farm.\n"
                else:
                    mood_change -= 1
                    mood_factors += "-1: She is being kept at the farm.\n"

            else: # Working girls
                w = 0
                if g.works_today(check_autorest=True) and not resting:
                    if g.job == "whore" and g.get_effect("special", "whore mood modifier"):
                        w += 1
                        mood_factors += "+1: She works as a whore and she loves it.\n"
                    elif g.workdays[calendar.get_weekday()] == 100:
                        w = -1
                        mood_factors += "-1: She is working today.\n"
                    else: # Half shift
                        w = -0.5
                        mood_factors += "-0.5: She is working a half-shift today.\n"
                elif g.assignment:
                    if g.assignment.type == "quest":
                        w = -1
                        mood_factors += "-1: She is working on a quest today.\n"
                    else: # Classes
                        w = -0.5
                        mood_factors += "-0.5: She is attending a class today.\n"
                else:
                    w = 2
                    mood_factors += "+2: She is resting today.\n"

                up = g.get_upkeep_modifier()
                # fr = (len(g.friends) - len(g.rivals)) * g.get_effect("boost", "mood gains from friendship")
                fr = len(g.friends) * g.get_effect("boost", "mood gains from friendship")
                rv = -len(g.rivals) * g.get_effect("boost", "mood gains from friendship")
                roo = brothel.get_mood_modifier(g.rank) # Uses room type modifier (between -7 and +10)
                bro = g.get_effect("change", "mood gains")

                mood_change += up + roo + bro + w + fr + rv

                if up > 0:
                    mood_factors += "+" + str(up) + ": She feels her allowance is generous.\n"

                elif up < 0:
                    mood_factors += str(up) + ": She isn't happy with her allowance.\n"

                if fr > 0:
                    mood_factors += "+" + str(round_best(fr)) + _(" : She has friends (%s).\n") % and_text([gf.name for gf in g.friends])
                if rv < 0:
                    mood_factors += str(round_best(rv)) + _(" : She has rivals (%s).\n") % and_text([gv.name for gv in g.rivals])

                if roo > 4:
                    mood_factors += "+" + str(round_best(roo)) + ": She loves her accommodations.\n"
                elif roo > 0:
                    mood_factors += "+" + str(round_best(roo)) + ": She likes her accommodations.\n"
                elif roo < -4:
                    mood_factors += str(round_best(roo)) + ": She hates her accommodations.\n"
                elif roo < 0:
                    mood_factors += str(round_best(roo)) + ": She doesn't like her accommodations.\n"

                # Change this later if more mood gain effects are added
                if bro > 1:
                    mood_factors += "+" + str(bro) + ": Other girls helped her relax.\n"
                elif bro > 0:
                    mood_factors += "+" + str(bro) + ": Another girl helped her relax.\n"

            # Life of Luxury perk
            mood_eff = g.get_effect("change", "mood")
            if mood_eff:
                mood_change += mood_eff
                if g.has_perk("Life of Luxury"):
                    mood_factors += plus_minus(mood_eff) + ": She loves her outfit (Life of Luxury).\n"
                else:
                    mood_factors += plus_minus(mood_eff) + ": Other effects.\n"


            if description:
                return mood_change, mood_factors

            else: # The following effects are not described in the mood tooltip

                # Business and Pleasure perk
                mood_change += g.get_effect("change", "mood", custom_scale=("cust nb", g.get_log("total_cust", 1)))

                boost = g.get_effect("boost", "mood gains")
                # reverses boost if negative change
                return mood_change * reverse_if(boost, mood_change)

        def get_mood_description(self, filter=None): # This returns text for the mood help screen
            g = self.girl

            l = g.get_love()

            if l > 90:
                love_text = "{color=" + color_dict["love +++"] + "}" + love_description["++++++"] + "{/color}"
            elif l > 70:
                love_text = "{color=" + color_dict["love +++"] + "}" + love_description["+++++"] + "{/color}"
            elif l > 50:
                love_text = "{color=" + color_dict["love ++"] + "}" + love_description["++++"] + "{/color}"
            elif l > 30:
                love_text = "{color=" + color_dict["love ++"] + "}" + love_description["+++"] + "{/color}"
            elif l > 15:
                love_text = "{color=" + color_dict["love +"] + "}" + love_description["++"] + "{/color}"
            elif l >= 5:
                love_text = "{color=" + color_dict["love +"] + "}" + love_description["+"] + "{/color}"
            elif l > -5:
                love_text = "{color=" + color_dict["normal"] + "}" + love_description["0"] + "{/color}"
            elif l >= -15:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["-"] + "{/color}"
            elif l >= -30:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["--"] + "{/color}"
            elif l >= -50:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["---"] + "{/color}"
            elif l >= -70:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["----"] + "{/color}"
            elif l >= -90:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["-----"] + "{/color}"
            else:
                love_text = "{color=" + color_dict["love -"] + "}" + love_description["------"] + "{/color}"

            f = g.get_fear()

            if g.personality.name != "masochist":
                if f > 90:
                    fear_text = "{color=" + color_dict["fear +++"] + "}" + fear_description["++++++"] + "{/color}"
                elif f > 70:
                    fear_text = "{color=" + color_dict["fear +++"] + "}" + fear_description["+++++"] + "{/color}"
                elif f > 50:
                    fear_text = "{color=" + color_dict["fear ++"] + "}" + fear_description["++++"] + "{/color}"
                elif f > 30:
                    fear_text = "{color=" + color_dict["fear ++"] + "}" + fear_description["+++"] + "{/color}"
                elif f > 15:
                    fear_text = "{color=" + color_dict["fear +"] + "}" + fear_description["++"] + "{/color}"
                elif f > 5:
                    fear_text = "{color=" + color_dict["fear +"] + "}" + fear_description["+"] + "{/color}"
                elif f >= -5:
                    fear_text = "{color=" + color_dict["normal"] + "}" + fear_description["0"] + "{/color}"
                elif f >= -15:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["-"] + "{/color}"
                elif f >= -30:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["--"] + "{/color}"
                elif f >= -50:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["---"] + "{/color}"
                elif f >= -70:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["----"] + "{/color}"
                elif f >= -90:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["-----"] + "{/color}"
                else:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["------"] + "{/color}"

            else:
                if f > 90:
                    fear_text = "{color=" + color_dict["fear +++"] + "}" + fear_description["M++++++"] + "{/color}"
                elif f > 70:
                    fear_text = "{color=" + color_dict["fear +++"] + "}" + fear_description["M+++++"] + "{/color}"
                elif f > 50:
                    fear_text = "{color=" + color_dict["fear ++"] + "}" + fear_description["M++++"] + "{/color}"
                elif f > 30:
                    fear_text = "{color=" + color_dict["fear ++"] + "}" + fear_description["M+++"] + "{/color}"
                elif f > 15:
                    fear_text = "{color=" + color_dict["fear +"] + "}" + fear_description["++"] + "{/color}"
                elif f > 5:
                    fear_text = "{color=" + color_dict["fear +"] + "}" + fear_description["+"] + "{/color}"
                elif f >= -5:
                    fear_text = "{color=" + color_dict["normal"] + "}" + fear_description["0"] + "{/color}"
                elif f >= -15:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["-"] + "{/color}"
                elif f >= -30:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["--"] + "{/color}"
                elif f >= -50:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["M---"] + "{/color}"
                elif f >= -70:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["M----"] + "{/color}"
                elif f >= -90:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["M-----"] + "{/color}"
                else:
                    fear_text = "{color=" + color_dict["fear -"] + "}" + fear_description["M------"] + "{/color}"

            m = g.mood

            if m > 90:
                mood_text = "{color=" + color_dict["+++"] + "}" + mood_description["++++++"] + "{/color}"
            elif m > 70:
                mood_text = "{color=" + color_dict["+++"] + "}" + mood_description["+++++"] + "{/color}"
            elif m > 50:
                mood_text = "{color=" + color_dict["++"] + "}" + mood_description["++++"] + "{/color}"
            elif m > 30:
                mood_text = "{color=" + color_dict["++"] + "}" + mood_description["+++"] + "{/color}"
            elif m > 15:
                mood_text = "{color=" + color_dict["+"] + "}" + mood_description["++"] + "{/color}"
            elif m >= 5:
                mood_text = "{color=" + color_dict["+"] + "}" + mood_description["+"] + "{/color}"
            elif m >= -5:
                mood_text = "{color=" + color_dict["normal"] + "}" + mood_description["0"] + "{/color}"
            elif m >= -15:
                mood_text = "{color=" + color_dict["-"] + "}" + mood_description["-"] + "{/color}"
            elif m >= -30:
                mood_text = "{color=" + color_dict["-"] + "}" + mood_description["--"] + "{/color}"
            elif m >= -50:
                mood_text = "{color=" + color_dict["--"] + "}" + mood_description["---"] + "{/color}"
            elif m >= -70:
                mood_text = "{color=" + color_dict["--"] + "}" + mood_description["----"] + "{/color}"
            elif m >= -90:
                mood_text = "{color=" + color_dict["---"] + "}" + mood_description["-----"] + "{/color}"
            else:
                mood_text = "{color=" + color_dict["---"] + "}" + mood_description["------"] + "{/color}"

            chg, mood_factors = g.get_mood_modifier(love_text, fear_text, description=True)

            if chg > 3:
                mood_change_text = mood_description["change +++"] + " {color=" + color_dict["+++"] + "}(+"
            elif chg > 1:
                mood_change_text = mood_description["change ++"] + " {color=" + color_dict["++"] + "}(+"
            elif chg > 0:
                mood_change_text = mood_description["change +"] + " {color=" + color_dict["+"] + "}(+"
            elif chg == 0:
                mood_change_text = mood_description["no change"] + " {color=" + color_dict["normal"] + "}("
            elif chg >= -1:
                mood_change_text = mood_description["change -"] + " {color=" + color_dict["-"] + "}("
            elif chg >= -3:
                mood_change_text = mood_description["change --"] + " {color=" + color_dict["--"] + "}("
            else:
                mood_change_text =  mood_description["change ---"] + " {color=" + color_dict["---"] + "}("

            mood_change_text += str(round_best(chg)) + "){/color}."

            if filter == "love":
                return love_text
            elif filter == "fear":
                return fear_text
            elif filter == "mood":
                return mood_text + mood_change_text + "\nSanity: " + g.get_sanity()
            else:
                return love_text, fear_text, mood_text, mood_change_text, mood_factors

        def get_mood_picture(self): # returns picture path
            g = self.girl

            if g.mood >= 25:
                pic = "resources/ui/mood good"
            elif g.mood <= -25:
                pic = "resources/ui/mood bad"
            else:
                pic = "resources/ui/mood normal"

            mod = g.get_mood_modifier()

            if mod > 0:
                pic += " up.webp"
            elif mod < 0:
                pic += " down.webp"
            else:
                pic += ".webp"

            return pic

        def tired_check(self):
            g = self.girl
            if g.works_today():
                # Tiredness = 5/customer (regular jobs), 10/interaction (whoring)

                if g.job in all_jobs:
                    if g.get_max_cust_served() * 5 >= g.energy:
                        return True
                else:
                    if 10 * g.interactions >= g.energy:
                        return True

            return False

        # ── Farm build-up ──
        def build_up(self, v):
            return self.girl.build_up(v)
        def get_build_up(self):
            return self.girl.get_build_up()
        def reset_build_up(self):
            return self.girl.reset_build_up()
