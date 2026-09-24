#### Screen Girl Stats — Stat bars and girl statistics | 女孩属性界面 ####
# Phase 2: 女孩属性/属性条/特性详情
# Contains: screen stat_bar, screen custom_bar, screen girl_stats, screen assign_job, screen girl_stats_light, screen trait_details, screen perk_details
# Extracted from ui/screens.rpy on 2026-09-10

screen stat_bar(base_value, bonus, max_skill=100, max_cap=None, separator=50, bar_color=c_darkorange, pos_color=c_emerald, neg_color=c_crimson, color_scale=False): # All purpose stat bar, can be recolored

    # For now, proportionality using float is broken. So we use hardcoded values instead.
    default bar_xsize = xres(160)
    $ max_bar = max_skill

    if bonus > 0:
        $ bonus_offset = -xres(2) # int(max(xres(-6), xres(-base_value*50//max_skill))) # empirical
        $ max_bar = max_skill
    elif bonus < 0:
        $ bonus_offset = -xres(2) # int(max(xres(-6), xres(-(base_value+bonus)*50//max_skill))) # empirical
        $ max_bar = max_skill

    fixed fit_first True:
        fixed fit_first True xalign 1.0 xsize bar_xsize + xres(6) ypos -0.33:
            add AlphaMask(Solid(bar_color), Frame("GUI/bar/cryslider_empty.webp", left=xres(3), right=xres(3), top=0, bottom=0)) ysize yres(24)
            if color_scale: # Does not work with bonus/malus colors
                bar value base_value+bonus range max_cap thumb None left_bar Frame("GUI/bar/cryslider_scale.webp", left=xres(3), right=xres(3), top=3, bottom=3) xsize int(bar_xsize * max_cap/max_bar) + xres(4) ysize yres(24) right_bar None
            elif bonus > 0:
                add AlphaMask(Solid(bar_color), Frame("GUI/bar/cryslider_full.webp", left=xres(3), top=3, bottom=3)) xsize xres(160*base_value/max_bar + 6) ysize yres(24)

                fixed fit_first True xanchor 0.0 xoffset bonus_offset: # Don't ask me why, it works
                    xpos int(bar_xsize * base_value/max_bar)
                    xsize int(bar_xsize * bonus/max_bar) - bonus_offset
                    add AlphaMask(Solid(pos_color), Frame("GUI/bar/cryslider_full.webp", left=xres(3), right=xres(3), top=3, bottom=3)) xalign 0.0 xsize 1.0 ysize yres(24) # hover_alpha 1.0 idle_alpha 0.7
                    if base_value+bonus <= 0.8*max_bar: # Avoids visual glitch when stat is close to max
                        $ text1 = "+%i" % bonus
                    else:
                        $ text1 = "+%i\n" % bonus
                    text text1 xalign 0.5 yalign 1.0 hover_color c_white idle_color c_white + "00" size res_font(12)
            elif bonus < 0:
                add AlphaMask(Solid(bar_color), Frame("GUI/bar/cryslider_full.webp", left=xres(3), top=3, bottom=3)) xsize max(xres(160*(base_value+bonus)/max_bar + 6), 0) ysize yres(24)

                fixed fit_first True xanchor 0.0 xoffset bonus_offset: # Don't ask me why, it works
                    xpos max(int(bar_xsize * (base_value+bonus)/max_bar), 0)
                    xsize int(bar_xsize * -bonus/max_bar) - bonus_offset*3
                    add AlphaMask(Solid(neg_color), Frame("GUI/bar/cryslider_full.webp", left=xres(3), right=xres(3), top=3, bottom=3)) xalign 0.0 xsize 1.0 ysize yres(24) # idle_alpha 0.5 hover_alpha 1.0
                    if base_value <= 0.8*max_bar: # Avoids visual glitch when stat is close to max
                        text _("%i") % bonus xalign 0.5 yalign 1.0 hover_color c_white idle_color c_white + "00" size res_font(12)
                    else:
                        text _("%i\n") % bonus xalign 0.5 yalign 1.0 hover_color c_white idle_color c_white + "00" size res_font(12)
            else:
                add AlphaMask(Solid(bar_color), Frame("GUI/bar/cryslider_full.webp", left=xres(3), right=xres(3), top=3, bottom=3)) xsize xres(160*base_value/max_bar + 4) ysize yres(24)

        if separator:
            for x in range(max_bar//separator):
                if (x+1)*separator != max_bar:
                    text "{color=[c_brown]}I{/color}" xpos int(bar_xsize * ((x+1)*separator / max_bar)) xanchor 0.0 ypos -0.4 size res_font(10) bold True # xalign (x+1)*separator/max_skill

        if max_cap: # Adds a red bar to mark the artificial cap
            text "{color=[c_red]}I{/color}" xpos int(xres(6) + bar_xsize * max_cap/max_bar) xanchor xres(6) ypos -0.4 size res_font(24)

# screen stat_bar(base_value, bonus, max_skill=100, max_cap=None, separator=50, bar_color=c_darkorange, pos_color=c_emerald, neg_color=c_crimson, color_scale=False): # All purpose stat bar, can be recolored
#     # For now, proportionality using float is broken. So we use hardcoded values instead.
#     $ bar_xsize = xres(160)
#
#     if bonus > 0:
#         $ bonus_offset = int(max(xres(-7), xres(-base_value*50//max_skill))) # empirical
#     elif bonus < 0:
#         $ bonus_offset = int(max(xres(-7), xres(-(base_value+bonus)*50//max_skill))) # empirical
#
#     fixed fit_first True:
#         fixed fit_first True xalign 1.0 xsize bar_xsize + xres(6) ypos -0.33:
#             add AlphaMask(Solid(bar_color), Frame("GUI/bar/cryslider_empty.webp", left=6, right=6, top=3, bottom=3)) yoffset 0
#             if color_scale: # Does not work with bonus/malus colors
#                 bar value base_value+bonus range max_cap thumb None left_bar Frame("resources/ui/cryslider_scale.webp", left=6, right=6, top=3, bottom=3) xpos xres(6) xsize int(bar_xsize * max_cap/max_skill) ysize yres(24) right_bar None
#             elif bonus > 0:
#                 add AlphaMask(Solid(bar_color), Frame("GUI/bar/cryslider_full.webp", left=xres(3), top=3, bottom=3)) xpos xres(6) xsize int(bar_xsize * base_value/max_skill) ysize yres(24)
#
#                 fixed fit_first True xanchor 0.0 xoffset bonus_offset: # Don't ask me why, it works
#                     xpos xres(6) + int(bar_xsize * base_value/max_skill)
#                     xsize int(bar_xsize * bonus/max_skill) - bonus_offset
#                     add AlphaMask(Solid(pos_color), Frame("GUI/bar/cryslider_full.webp", right=xres(3), top=3, bottom=3)) xalign 0.0 xsize 1.0 ysize yres(24) hover_alpha 1.0 idle_alpha 0.5
#                     if base_value+bonus <= 0.8*max_skill: # Avoids visual glitch when stat is close to max
#                         $ text1 = "+%i" % bonus
#                     else:
#                         $ text1 = "+%i\n" % bonus
#                     text text1 xalign 0.5 yalign 1.0 hover_color c_white idle_color c_white + "00" size res_font(12)
#             elif bonus < 0:
#                 add AlphaMask(Solid(bar_color), Frame("GUI/bar/cryslider_full.webp", left=xres(3), top=3, bottom=3)) xpos xres(6) xsize max(int(bar_xsize * (base_value+bonus)/max_skill), 0) ysize yres(24)
#
#                 fixed fit_first True xanchor 0.0 xoffset bonus_offset: # Don't ask me why, it works
#                     xpos xres(6) + max(int(bar_xsize * (base_value+bonus)/max_skill), 0)
#                     xsize int(bar_xsize * -bonus/max_skill) - bonus_offset
#                     add AlphaMask(Solid(neg_color), Frame("GUI/bar/cryslider_full.webp", right=xres(3), top=3, bottom=3)) xalign 0.0 xsize 1.0 ysize yres(24) idle_alpha 0.5 hover_alpha 1.0
#                     if base_value <= 0.8*max_skill: # Avoids visual glitch when stat is close to max
#                         text "%i" % bonus xalign 0.5 yalign 1.0 hover_color c_white idle_color c_white + "00" size res_font(12)
#                     else:
#                         text "%i\n" % bonus xalign 0.5 yalign 1.0 hover_color c_white idle_color c_white + "00" size res_font(12)
#             else:
#                 add AlphaMask(Solid(bar_color), Frame("GUI/bar/cryslider_full.webp", left=xres(3), right=xres(3), top=3, bottom=3)) xpos xres(6) xsize base_value/max_skill ysize yres(24)
#
#         if separator:
#             for x in range(max_skill//separator):
#                 if (x+1)*separator != max_skill:
#                     text "{color=[c_brown]}I{/color}" xpos xres(6) + int(bar_xsize * ((x+1)*separator / max_skill)) xanchor xres(6) ypos -0.4 size res_font(10) bold True # xalign (x+1)*separator/max_skill
#
#         if max_cap: # Adds a red bar to mark the artificial cap
#             text "{color=[c_red]}I{/color}" xpos int(xres(6) + bar_xsize * max_cap/max_skill) xanchor xres(6) ypos -0.33 size res_font(24)


# screen stat_bar(base_value, bonus, max_skill=100, max_cap=None, separator=50, bar_color=c_darkorange, pos_color=c_emerald, neg_color=c_crimson, color_scale=False): # All purpose stat bar, can be recolored
#
#     fixed fit_first True:
#         frame xalign 1.0 xsize 0.6 ypos -0.37 xpadding 0 ypadding 0:
#             background AlphaMask(Solid(bar_color), Frame("resources/ui/cryslider_empty.webp", left=12, right=12, top=3, bottom=3))
#             hbox spacing max(xres(-7), xres(-base_value)): # Necessary to avoid glitch
#                 if color_scale: # Does not work with bonus/malus colors
#                     bar value base_value+bonus range max_cap thumb None left_bar Frame("resources/ui/cryslider_scale.webp", left=6, right=6, top=6, bottom=6) xsize (base_value+bonus)/max_skill ysize yres(24) right_bar None
#                 elif bonus > 0:
#                     add AlphaMask(Solid(bar_color), Frame("resources/ui/cryslider_full.webp", left=12, top=6, bottom=6)) xsize base_value/max_skill ysize yres(24)
#                     fixed fit_first True:
#                         add AlphaMask(Solid(pos_color), Frame("resources/ui/cryslider_full.webp", right=12, top=6, bottom=6)) xsize bonus/(max_skill-base_value) ysize yres(24) idle_alpha 0.5 hover_alpha 1.0
#                         text "+%i" % bonus xalign 0.5 yalign 1.0 hover_color c_white idle_color c_white + "00" size res_font(12)
#                 elif bonus < 0:
#                     add AlphaMask(Solid(bar_color), Frame("resources/ui/cryslider_full.webp", left=12, top=6, bottom=6)) xsize (base_value+bonus)/max_skill ysize yres(24)
#                     fixed fit_first True:
#                         add AlphaMask(Solid(neg_color), Frame("resources/ui/cryslider_full.webp", right=12, top=6, bottom=6)) xsize -bonus/max_skill ysize yres(24) idle_alpha 0.5 hover_alpha 1.0
#                         text "%i" % bonus xalign 0.5 yalign 1.0 hover_color c_white idle_color c_white + "00" size res_font(12)
#                 else:
#                     add AlphaMask(Solid(bar_color), Frame("resources/ui/cryslider_full.webp", left=12, right=12, top=3, bottom=3)) xsize base_value/max_skill ysize yres(24)
#
#         if separator:
#             for x in range(max_skill//separator):
#                 if (x+1)*separator != max_skill:
#                     text "{color=[c_brown]}I{/color}" xalign (x+1)*separator/max_skill xanchor 6 ypos -0.4 size res_font(10) bold True
#
#         if max_cap: # Adds a red bar to mark the artificial cap
#             text "{color=[c_red]}I{/color}" xalign max_cap/max_skill xanchor 6 ypos -0.375 size res_font(24)

screen custom_bar(labl = "Level 25", hov = None, unhov = None, val = 0, _max = 100, col = c_green, col2 = c_ui_light, x = xres(100), y = yres(6), txt_size = res_font(14)):
    frame:
        xmaximum x
        xfill True
#        ysize y
        xmargin 0
        ymargin 0
        xpadding 0
        ypadding 0
        background None

        has vbox
        spacing 1

        text labl size txt_size xalign 0.0 yalign 0.0
        if col:
            bar value val range _max thumb None thumb_offset 0 xfill True ysize y yalign 0.0 left_gutter 0 right_gutter 0: #top_gutter 1 bottom_gutter 0:
                # left_bar col right_bar col2
                left_bar AlphaMask(Solid(col), Frame("resources/ui/cryslider_full.webp", left=12, right=12, bottom=0))
                right_bar AlphaMask(Solid(col2), Frame("resources/ui/cryslider_empty.webp", left=12, right=12, bottom=0))

screen girl_stats(girl, context = "girls"): # context can be girls, slavemarket, farm, free, postings, contracts, capture, powers

    tag gst

    zorder 0

    if girl:
        frame:
            xalign 0.0

            if context not in ("postings"):
                ypos 0.1

            xmargin xres(6)
            xpadding xres(6)
            xfill True
            xsize xres(320)

            if context in ("farm", "powers"):
                background c_ui_dark
            else:
                background c_ui_darkblue

            vbox:

                spacing yres(3)

                hbox:

                    xfill True

                    if len(girl.fullname) > 23:
                        $ text1 = girl.fullname[:20] + "..."
                    else:
                        $ text1 = girl.fullname

                    textbutton text1:
                        xalign 0.0
                        background None
                        text_color c_white
                        text_size res_font(20)
                        text_font "resources/fonts/MATURASC.ttf"

                        if context == "girls":
                            action (SetVariable("selected_girl", girl), Return("change_name"))
                            tooltip __("Click to change her name")

                        elif context == "farm":
                            action Return(("change_name", girl))
                            tooltip __("Click to change her name")

                        xmargin 0
                        ymargin 0
                        xpadding xres(3)
                        ypadding 0


                    if context in ("girls", "farm"):

                        frame:

                            background None
                            xmargin 0
                            ymargin 0
                            xpadding 0
                            ypadding 0
                            xalign 1.0
                            yalign 1.0
                            xfill False

                            has hbox

                            spacing xres(6)
                            xfill False

                            # Add defense meter

                            $ defense = girl.get_defense()

                            if defense <= 0:
                                    $ ttip = __("{b}Helpless")
                            elif defense <= 3:
                                $ ttip = __("{b}Mostly harmless")
                            elif defense <= 6:
                                $ ttip = __("{b}Competent")
                            elif defense <= 9:
                                $ ttip = __("{b}Dangerous")
                            else:
                                $ ttip = __("{b}Deadly")

                            $ ttip += __("{/b}\nHow well she can defend herself. Raise this by giving her a weapon.")

                            button:

                                xmargin 0
                                ymargin 0
                                xpadding 0
                                ypadding 0
                                xsize yres(20)
                                ysize yres(20)
                                xalign 0.0
                                yalign 1.0
                                background None

                                action NullAction()
                                tooltip ttip

                                add ProportionalScale("resources/ui/defense.webp", *res_tb(20)) xalign 0.5 yalign 0.5

                                text str(round_int(defense)) size res_font(12) xalign 0.5 yalign 0.5 color c_white


                            button background None action NullAction() hovered (Show("mood_details", girl=girl, transition=Dissolve(0.15)), tt.Action(girl.get_mood_description("mood"))) unhovered Hide("mood_details", transition=Dissolve(0.15)):

                                xalign 0.0
                                yalign 0.7
                                xmargin 0
                                ymargin 0
                                xpadding 0
                                ypadding 0

                                add ProportionalScale(girl.get_mood_picture(), *res_tb(16))

                    elif context == "powers":
                        text _("Sanity: %s") % girl.get_sanity() size res_font(16)


                if context in ["girls", "farm", "contract", "postings", "powers"]:

                    ## Levels and rank info

                    button style "inv_no_padding":

                        xalign 0.0

                        if debug_mode:
                            action Function(girl.rank_up, forced = True)
                        else:
                            action NullAction()
                        hovered Show("rank_level_details", girl = girl, transition=Dissolve(0.15))
                        unhovered Hide("rank_level_details", transition=Dissolve(0.15))

                        has hbox
                        xfill True
                        spacing xres(6)

                        #Rank

                        $ rank_text = __("Rank %s") % rank_name[girl.rank]

        #                $ rank_ttip = "Reputation: " + str(round_int(girl.rep)) + "/" + str(girl.get_rep_cap())

        #                if girl.rank >= str(district.rank):

        #                    $ rank_ttip += "{b}Max rank reached.{/b}\n"

        #                $ rank_ttip += "\nRank affects many aspects of the game, including maximum level and skill values."

                        use custom_bar(labl = rank_text, val = (girl.rep - rep_to_rank[girl.rank - 1]), _max = (girl.get_rep_cap() - rep_to_rank[girl.rank - 1]), col = c_softpurple, x = xres(70), y=yres(10))


                        #Level

                        $ level_text = __("Level %s") % girl.level

                        use custom_bar(labl = level_text, val = (girl.xp - xp_to_levelup[girl.level - 1]), _max = (girl.get_xp_cap() - xp_to_levelup[girl.level - 1]), col = c_lightgreen, x = xres(70), y=yres(10))


                        #JP

                        $ jp_show = False

                        if girl.away:
                            if girl.job in all_jobs:
                                $ job = girl.job
                                $ jp_show = True
                            $ jp_text = __("Away")

                        elif girl.hurt > 0:
                            if girl.job in all_jobs:
                                $ job = girl.job
                                $ jp_show = True
                            $ jp_text = __("Hurt (%id)") % int(girl.hurt)

                        elif girl.workdays[calendar.get_weekday()] == 0:
                            if girl.job in all_jobs:
                                $ job = girl.job
                                $ jp_show = True
                            $ jp_text = __("Resting")

                        elif girl.resting or not girl.job:
                            $ jp_text = __("Resting")

                        elif girl.job in all_jobs:
                            $ job = girl.job
                            $ jp_show = True

                        elif girl in farm.girls:
                            if farm.programs[girl].target == "no training":
                                if farm.programs[girl].holding == "rest":
                                    $ jp_text = __("Resting")
                                else:
                                    $ jp_text = __("Holding")
                            else:
                                $ jp_text = __("Training")

                        else: # Whore
                            $ job = None

                            $ best = -1
                            for act in all_sex_acts:
                                if girl.jp[act] > best and girl.does[act]:
                                    $ best = girl.jp[act]
                                    $ job = act
                                    $ jp_show = True

                        if jp_show:
                            $ jp_text = __(job.capitalize()) + " " + str(girl.job_level[job]) + " {image=img_star}"

                            $ jp_val = girl.jp[job]
                            $ jp_max = girl.get_jp_cap(job)
                            $ jp_col = c_orange

                            use custom_bar(labl = jp_text, val = (jp_val - jp_to_level[girl.job_level[job] - 1]), _max = (jp_max - jp_to_level[girl.job_level[job] - 1]), col = jp_col, x=xres(70), y=yres(10))

                        else:
                            use custom_bar(labl = jp_text, val = 0, _max = 0, col = None, col2 = None)


                if context != "capture":
                    null height yres(30)


                ## SKILLS LISTING

                text _("Main skills") size res_font(18)

                vbox:
                    spacing 0

                    if context != "free" or girl.MC_relationship_level >= 1:

                        for stat in girl.stats:

                            $ total_value = girl.get_stat(stat.name)
                            $ maxrange = max(girl.get_stat_minmax(stat.name)[1], girl.rank*50)

                            if total_value > round_int(stat.value):
                                $ col = "good"
                            elif total_value < round_int(stat.value):
                                $ col = "bad"
                            else:
                                $ col = "normal"

                            button focus stat.name:
                                background None
                                if debug_mode:
                                    action Return(("debug change stat", stat))
                                else:
                                    action NullAction()
                                tooltip stat.get_description(total_value, girl.get_stat_minmax(stat.name)[1])
                                keyboard_focus False
                                yfill False
                                ysize yres(30)

                                if debug_mode:
                                    hovered tt.Action(_("value: %i, total_value: %i, bonus: %i, maxrange: %i") % (stat.value, total_value, total_value-round_int(stat.value), maxrange))

                                hbox:
                                    spacing 6
                                    use stat_bar(stat.value, total_value-round_int(stat.value), maxrange) id "bar_" + stat.name
                                    text stat_name_dict[stat.name] bold True layout "nobreak" size res_font(14) xpos 0.0 ypos -0.05 idle_color c_white + "CC"
                                text event_color[col] % ("%s/%s" % (str_int(total_value), girl.get_stat_minmax(stat.name)[1])) size res_font(12) yalign 0.1 xanchor 1.0 idle_color c_white + "CC" drop_shadow (1, 1):
                                    xpos 0.525

                        # Energy bar

                        $ girl_max = girl.get_stat_minmax("energy")[1]
                        $ rank_max = 50+50*girl.rank

                        if girl_max > rank_max:
                            $ rank_max = girl_max

                        button:
                            background None
                            if debug_mode:
                                action Return(("debug change all stats", 0))
                            else:
                                action NullAction()
                            tooltip __("She has {b}%s{/b} energy remaining. Her maximum energy is {b}%s{/b} (increase constitution for higher energy).") % (str_int(girl.energy), str_int(girl_max))
                            keyboard_focus False
                            yfill False
                            ysize yres(30)

                            hbox:
                                spacing 6
                                use stat_bar(girl.energy, bonus=0, max_skill=rank_max, max_cap=girl_max, color_scale=True, separator=False)  id "bar_energy"
                                text stat_name_dict["Energy"] bold True size res_font(14) xpos 0.0 ypos -0.05 idle_color c_white + "CC"

                            text "%s/%s" % (int(girl.energy), int(girl_max)) size res_font(12) yalign 0.1 xanchor 1.0 idle_color c_white + "CC":
                                xpos 0.525

                    else:
                        for stat in girl.stats[:4]:

                            $ total_value = girl.get_stat(stat.name)
                            $ maxrange = max(girl.get_stat_minmax(stat.name)[1], girl.rank*50)

                            if total_value > stat.value:
                                $ col = "good"
                            elif total_value < stat.value:
                                $ col = "bad"
                            else:
                                $ col = "normal"

                            button:
                                background None
                                action NullAction()
                                tooltip stat.get_description(total_value, girl.get_stat_minmax(stat.name)[1])
                                keyboard_focus False
                                ysize yres(30)

                                hbox:
                                    spacing 6

                                    use stat_bar(total_value, 0, maxrange) id "bar_" + stat.name
                                    text stat_name_dict[stat.name] bold True layout "nobreak" size res_font(14) xpos 0.0 ypos -0.05 idle_color c_white + "CC"
                                text event_color[col] % ("%s/%s" % (str_int(total_value), girl.get_stat_minmax(stat.name)[1])) size res_font(12) yalign 0.1 xanchor 1.0 idle_color c_white + "CC" drop_shadow (1, 1):
                                    xpos 0.525

                        for stat in girl.stats[4:]:
                            button:
                                background None
                                action NullAction()
                                tooltip _("You need to become her friend to see her level for this skill.")
                                keyboard_focus False
                                ysize yres(30)

                                fixed fit_first True:

                                    hbox:
                                        spacing 6

                                        use stat_bar(0, 0, 50) id "bar_" + stat.name
                                        text stat_name_dict[stat.name] bold True layout "nobreak" size res_font(14) xpos 0.0 ypos -0.05 idle_color c_white + "CC"

                                    text "???" xpos 75 size res_font(14)




                    # text "" size res_font(6)

                hbox spacing 14:
                    textbutton _("Sex skills") style "inv_no_padding" text_size res_font(18) yalign 0.0 action NullAction() hovered Show("sex_details", girl=girl) unhovered Hide("sex_details")

                    for act in ("group", "bisexual"):

                        if girl.does[act]:
                            $ text1 = "{b}✓{/b}"
                        else:
                            $ text1 = ""

                        if girl.has_perk(act.capitalize()):

                            button xpadding 0 ypadding 0 xmargin 0 ymargin 0 yalign 1.0 background None action NullAction() hovered Show("sex_details", girl=girl) unhovered Hide("sex_details"):
                                hbox spacing 5:
                                    textbutton text1:
                                        text_font "resources/fonts/DejaVuSans.ttf"
                                        text_size res_font(12)
                                        xsize yres(35)
                                        ysize yres(20)
                                        ypos -0.1
                                        if not girls_firstvisit:
                                            action (SetVariable("selected_girl", girl), SetVariable("selected_sex_act", act), Return("sex_act"))

                                        hovered (tt.Action(__("This will activate {b}%s acts{/b} for this girl. At least one regular sex act muct be active as well.") % act), Show("sex_details", girl=girl))
                                        unhovered Hide("sex_details")
                                    text __(act.capitalize()) layout "nobreak": #preference_color[pref] % stat.name:
                                        size res_font(12)

                if context == "slavemarket":
                    $ ttip = __("%s Prior training may make a girl more suitable for sex acts.") % experienced_description[girl.sexual_experience + " ttip"]
                    textbutton __("Prior training received:   {color=%s}%s{/color}") % (experienced_color[girl.sexual_experience], experienced_description[girl.sexual_experience]) ymargin yres(3) ypadding 0 text_color c_white text_size res_font(14) background None action NullAction() tooltip ttip


                vbox:
                    spacing 0

                    if context != "free" or girl.MC_relationship_level >= 4:

                        for stat in girl.sex_stats:

                            $ total_value = girl.get_stat(stat.name)
                            $ maxrange = max(girl.get_stat_minmax(stat.name)[1], girl.rank*50)

                            if total_value > round_int(stat.value):
                                $ col = "good"
                            elif total_value < round_int(stat.value):
                                $ col = "bad"
                            else:
                                $ col = "normal"

                            button:
                                background None
                                if debug_mode:
                                    action Return(("debug change stat", stat))
                                else:
                                    action NullAction()
                                hovered Show("sex_details", girl=girl)
                                unhovered Hide("sex_details")
                                tooltip stat.get_description(total_value, girl.get_stat_minmax(stat.name)[1]) # stat.get_description(total_value, maxrange)
                                keyboard_focus False
                                ysize yres(30)

                                hbox:

                                    spacing 6

                                    use stat_bar(stat.value, total_value-round_int(stat.value), maxrange) id "bar_" + stat.name
                                    # use stat_bar(total_value, total_value - stat.value, maxrange)

                                    if context == "girls":

                                        if girl.does[stat.name.lower()]:
                                            $ text1 = "✓"
                                        else:
                                            $ text1 = ""

                                        $ result, reason = girl.will_do_sex_act(stat.name.lower(), True)

                                        if result:
                                            $ ttip = __("This will activate {b}%s{/b} for this girl.") % stat_name_dict[stat.name]
                                        else:
                                            $ ttip = reason

                                        button xpadding 0 ypadding 0 xmargin 0 ymargin 0 background None action NullAction() hovered (Show("sex_details", girl=girl)) unhovered Hide("sex_details"):
                                            tooltip ttip
                                            textbutton text1:
                                                text_font "resources/fonts/DejaVuSans.ttf"
                                                text_size res_font(12)
                                                xsize int(config.screen_height*0.0341)
                                                ysize yres(20)
                                                ypos -0.1
                                                if not girls_firstvisit and result:
                                                    action (SetVariable("selected_girl", girl), SetVariable("selected_sex_act", stat.name), Return("sex_act"))

                                                hovered (Show("sex_details", girl=girl))
                                                unhovered Hide("sex_details")
                                                tooltip ttip

                                    $ pref = girl.get_preference(stat.name)

                                    text stat_name_dict[stat.name] bold True layout "nobreak" size res_font(14) xpos 0.0 ypos -0.05 idle_color c_white + "CC"

                                text event_color[col] % ("%s/%s" % (str_int(total_value), girl.get_stat_minmax(stat.name)[1])) size res_font(12) yalign 0.1 xanchor 1.0 idle_color c_white + "CC" drop_shadow (1, 1):
                                    xpos 0.525

                    else:
                        for stat in girl.sex_stats:
                            button:
                                background None
                                action NullAction()
                                tooltip _("You need to become her lover to see her level for this skill.")
                                keyboard_focus False
                                ysize yres(30)

                                fixed fit_first True:

                                    hbox:
                                        spacing 6

                                        use stat_bar(0, 0, 50) id "bar_" + stat.name
                                        text stat_name_dict[stat.name] bold True size res_font(14) xpos 0.0 ypos -0.05 idle_color c_white + "CC"

                                    text "???" xpos 75 size res_font(14)

                    # text "" size res_font(3)


                ## TRAITS LIST ##
                textbutton _("Traits") text_color c_white text_size res_font(18) background None xpadding 0 ypadding 0 xmargin 0 ymargin 0:
                    action NullAction()
                    if context != "free" or girl.MC_relationship_level >= 3:
                        hovered Show("trait_details", girl=girl)
                        unhovered Hide("trait_details")

                viewport:
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    if len(girl.traits) > 3 or sum(len(t.name) for t in girl.traits) >= 27:
                        ysize yres(36)
                    else:
                        ysize yres(22)

                    if context != "free" or girl.MC_relationship_level >= 3:
                        hbox spacing xres(10) box_wrap True:
                            for trait in girl.traits:

                                $ ttip = trait.get_description(context)

                                textbutton trait.display_name:

                                    style "inv_no_padding"
                                    xalign 0.0
                                    yalign 0.5
                                    text_size res_font(14)
                                    action NullAction()
                                    tooltip ttip
                                    hovered Show("trait_details", girl=girl)
                                    unhovered Hide("trait_details")
                                    keyboard_focus False

                                    if trait in pos_traits:
                                        text_color c_emerald
                                    elif trait in neg_traits:
                                        text_color c_crimson
                                    elif trait in gold_traits:
                                        text_color c_orange
                                    else:
                                        text_color c_softpurple

                    else:
                        textbutton "???":
                            background None
                            xalign 0.0
                            yalign 0.5
                            text_size res_font(14)
                            action NullAction()
                            tooltip _("You need to become her boyfriend to see her traits.")
                            keyboard_focus False

                if context == "girls":
                    text "" size res_font(3)

                    hbox spacing xres(10):
                        text _("Upkeep: ") size res_font(18) yalign 0.5
                        text (_("{image=img_gold_18} %i") % round_int(girl.upkeep)) size res_font(16) yalign 0.5

                        if girl.get_upkeep_modifier() != 0:
                            text (_(" (%s mood)") % plus_text(girl.get_upkeep_modifier())):
                                size res_font(14)
                                yalign 0.5
                                if girl.get_upkeep_modifier() < 0:
                                    color c_red

                                elif girl.get_upkeep_modifier() == 0:
                                    color c_white

                                else:
                                    color c_emerald

                    if girl.locked_upkeep:
                        text _("Her upkeep is currently withdrawn.") size res_font(14) italic True

                    else:
                        key "noshift_K_a" action (ToggleField(girl, "auto_upkeep"), SetField(girl, "upkeep_ratio", (girl.upkeep - girl.get_med_upkeep())/girl.rank), Play("sound", s_click))

                        hbox:
                            spacing xres(2)

                            $ minrange = girl.get_upkeep_threshold("min")
                            $ maxrange = girl.get_upkeep_threshold(5)

                            text "" size res_font(14)

                            bar style "slider" value FieldValue(girl, "upkeep", range=maxrange-minrange, offset=minrange, action=Function(girl.update_upkeep_ratio)):
                                if girl.get_upkeep_modifier() < 0:
                                    left_bar Frame("red_bar_left", gui.bar_borders, tile=gui.bar_tile)

                                elif girl.get_upkeep_modifier() == 0:
                                    left_bar Frame("lightorange_bar_left", gui.bar_borders, tile=gui.bar_tile)

                                else:
                                    left_bar Frame("green_bar_left", gui.bar_borders, tile=gui.bar_tile)

                                xsize 0.45
                                yalign 0.5
                                keyboard_focus False
                                tooltip _("You must pay upkeep every day. Higher-end girls will require higher upkeep. Keep it high to keep your girl happy.")

                            textbutton "-":
                                style "small_button"
                                xsize xres(25)
                                yalign 0.5
                                if girl.upkeep > minrange:
                                    action (SetField(girl, "upkeep", girl.get_previous_upkeep_step()), Function(girl.update_upkeep_ratio), Play("sound", s_click))
                                tooltip __("Decrease her upkeep.")

                            textbutton "+":
                                style "small_button"
                                xsize xres(25)
                                yalign 0.5
                                if girl.upkeep < maxrange:
                                    action (SetField(girl, "upkeep", girl.get_next_upkeep_step()), Function(girl.update_upkeep_ratio), Play("sound", s_click))
                                tooltip __("Increase her upkeep.")

                            if girl.auto_upkeep:
                                $ text1 = __("Auto upkeep setting is {b}{color=[c_green]}on{/color}{/b} {i}(shortcut: {u}Shift+a{/u}){/i}")
                            else:
                                $ text1 = __("Auto upkeep setting is {b}{color=[c_red]}off{/color}{/b} {i}(shortcut: {u}Shift+a{/u}){/i}")

                            textbutton _("A"):
                                if girl.auto_upkeep:
                                    text_bold True
                                    background Frame("lightblue_button", borders=gui.button_borders)

                                style "small_button"
                                xsize xres(25)
                                yalign 0.5
                                action (ToggleField(girl, "auto_upkeep"), SetField(girl, "upkeep_ratio", (girl.upkeep - girl.get_med_upkeep())/girl.rank), Play("sound", s_click))
                                tooltip __("{size=+2}%s\nWhen this is turned on, current upkeep balance will 'lock', and upkeep will rise and fall automatically.{/size=+2}") % text1

                elif context == "farm":
                    text "" size res_font(3)
                    text _("Upkeep") size res_font(18)

                    hbox:
                        spacing 2

                        text "" size res_font(14)

                        text __("%s gold (fixed)") % str(girl.get_med_upkeep() // 4) size res_font(14)


screen assign_job(girl):

    modal True
    tag assign_job

    key "mouseup_3" action (Return("cancel"))

    key "K_1" action (Return("rest"))
    key "K_2" action (Return("waitress"))
    key "K_3" action (Return("dancer"))
    key "K_4" action (Return("masseuse"))
    key "K_5" action (Return("geisha"))
    key "K_6" action (Return("whore"))
    if farm.active:
        key "K_7" action (Return("farm"))
    if brothel.master_bedroom.level >= 1:
        key "K_8" action (Return("master bedroom"))

    ## EN: Query mod-registered extra assign destinations (e.g. the
    ##     "Courtyard" mod). Rendered as extra grid cells below.
    ## ZH: 查询 Mod 注册的额外指派去向（如 "Courtyard" Mod），
    ##     渲染为网格下方的额外格子。
    python:
        _assign_mod_dests = []
        try:
            _assign_results = mod_api_v2.execute_hook(mod_api_v2.HOOK_GIRL_ASSIGN_LIST, girl=girl)
            for _results in _assign_results.values():
                if _results:
                    _assign_mod_dests.extend(_results)
        except Exception:
            _assign_mod_dests = []

    if _assign_mod_dests and _assign_mod_dests[0].get("available"):
        key "K_9" action (Return(("mod_dest", _assign_mod_dests[0]["id"])))

    frame ypos 0.25 xfill False:

        grid 4 3:
            # xsize xres(450)
            xspacing xres(3)
            yspacing yres(3)

            button background None xpadding 2 ypadding 2:
                action Return("rest")
                tooltip __("Tell %s to get some rest.") % girl.fullname
                at alpha_transform
                fixed fit_first True:
                    add "tb rest" xalign 0.5 yalign 0.5 # alpha 0.6 hover_alpha 1.0 selected_hover_alpha 1.0 selected_idle_alpha 1.0
                    text _("Rest") selected_color c_green hover_bold True xalign 0.5 yalign 0.5 drop_shadow (1, 1) size res_font(14)
                    text "1" size res_font(12) xalign 0.05 yalign 0.95 drop_shadow (1, 1)

            for j in all_jobs + ["whore"]:
                button background None xpadding 2 ypadding 2 xalign 0:
                    if brothel.has_room(job_room_dict[j]):
                        action Return(j)
                        tooltip __("Ask %s to work as a %s.") % (girl.fullname, __(j.capitalize()))
                        at alpha_transform
                        fixed fit_first True:
                            add "tb " + j xalign 0.5 yalign 0.5 # idle_alpha 0.66 selected_hover_alpha 1.0 selected_idle_alpha 1.0 hover_alpha 1.0
                            text __(j.capitalize()) selected_color c_yellow hover_bold True xalign 0.5 yalign 0.5 drop_shadow (1, 1) size res_font(14)
                            if j == "whore":
                                $ text1 = "6"
                            else:
                                $ text1 = str(all_jobs.index(j)+2)
                            text text1 size res_font(12) xalign 0.05 yalign 0.95 drop_shadow (1, 1)

                    else:
                        text __("%s\n(unavailable)") % __(j.capitalize()) selected_bold True xalign 0.5 yalign 0.5 drop_shadow (1, 1) size res_font(14)


            if farm.active:
                button background None xpadding 2 ypadding 2 xpos 0:
#                     selected girl.job=="farm" # What was this?
                    action Return("farm")
                    tooltip __("Send %s to the farm.") % girl.fullname
                    at alpha_transform
                    fixed fit_first True:
                        add "tb farm" xalign 0.5 yalign 0.5 # idle_alpha 0.66 selected_hover_alpha 1.0 selected_idle_alpha 1.0 hover_alpha 1.0
                        text _("Farm") selected_color c_green hover_bold True xalign 0.5 yalign 0.5 drop_shadow (1, 1) size res_font(14)
                        text "7" size res_font(12) xalign 0.05 yalign 0.95 drop_shadow (1, 1)
            else:
                null

            if brothel.master_bedroom.level >= 1:
                $ text1 = __("Auto-train ")
                if girl in brothel.master_bedroom.girls:
                    $ ttip = __("Remove %s from your bedroom.") % girl.fullname
                    $ text1 += __("(ON)")
                else:
                    $ ttip = __("Add %s to your bedroom.") % girl.fullname
                    $ text1 += __("(OFF)")

                button background None xpadding 2 ypadding 2 xpos 0:
                    action Return("master bedroom")
                    tooltip ttip
                    at alpha_transform
                    fixed fit_first True:
                        add brothel.master_bedroom.get_pic(xres(100), yres(60)) xalign 0.5 yalign 0.5 # idle_alpha 0.66 selected_hover_alpha 1.0 selected_idle_alpha 1.0 hover_alpha 1.0
                        text text1 selected_color c_green hover_bold True xalign 0.5 yalign 0.5 drop_shadow (1, 1) size res_font(14) text_align 0.5
                        text "8" size res_font(12) xalign 0.05 yalign 0.95 drop_shadow (1, 1)
            else:
                null

            ## EN: Mod-provided destinations (grid cells 9+). Only
            ##     "available" entries are rendered as buttons.
            ## ZH: Mod 提供的去向（第 9 格起）。仅渲染 available 的项。
            for _dest in _assign_mod_dests:
                if _dest.get("available"):
                    button background None xpadding 2 ypadding 2 xpos 0:
                        action Return(("mod_dest", _dest["id"]))
                        tooltip _dest.get("tooltip") or _dest.get("text")
                        at alpha_transform
                        fixed fit_first True:
                            add Solid("#2E4053") xsize xres(100) ysize yres(60) xalign 0.5 yalign 0.5
                            text _dest.get("text") selected_color c_green hover_bold True xalign 0.5 yalign 0.5 drop_shadow (1, 1) size res_font(14) text_align 0.5
                else:
                    null

            ## EN: Fill the 4x3 grid (8 fixed cells + mod cells).
            ## ZH: 补足 4x3 网格（8 个固定格 + Mod 格）。
            python:
                _assign_fill = 12 - 8 - len(_assign_mod_dests)
                if _assign_fill < 0:
                    _assign_fill = 0

            for _i in range(_assign_fill):
                null

screen girl_stats_light(girl, x=0.5, y=0.85, panel="left"): # Used to display a condensed summary of a girl's stat and show the impact of item changes

    zorder 6

    if isinstance(girl, Girl):
        frame xalign x yalign y xsize xres(450) xpadding 10 ypadding 10:
            has vbox xfill True
            hbox spacing xres(48):
                if panel == "left":
                    xalign 0.0
                elif panel == "right":
                    xalign 1.0

                if panel == "left":
                    text "⟸" font "DejaVuSans.TTF" color c_darkorange bold True
                text girl.fullname color c_darkorange bold True
                if panel == "right":
                    text "⟹" font "DejaVuSans.TTF" color c_darkorange

            hbox spacing 10 xalign 0.5:
                grid 3 8:
                    for stat in girl.stats:
                        $ change = 0
                        if selected_item:
                            if selected_item.equipped:
                                $ change = -round_int(girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("change", stat.name) + (1 - selected_item.get_effect("boost", stat.name))*girl.get_stat(stat.name)))
                            else:
                                $ change = round_int(girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("change", stat.name) + (1 - selected_item.get_effect("boost", stat.name))*girl.get_stat(stat.name)))

                                for it in girl.equipped:
                                    if it.slot == selected_item.slot:
                                        $ change -= round_int(girl.get_effect("boost", it.type.name.lower()) * (it.get_effect("change", stat.name) + (1 - it.get_effect("boost", stat.name))*girl.get_stat(stat.name)))

                                # Adjust Food bonuses
                                if selected_item.type.name == "Food":
                                    python:
                                        for eff in selected_item.effects:
                                            if eff.target == stat.name.lower() and girl.current_food_effect[stat.name.lower()]:
                                                change -= girl.current_food_effect[stat.name.lower()].value

                        text stat_name_dict[stat.name] size res_font(13) bold True:
                            if change:
                                color c_darkorange
                            else:
                                color c_brown

                        text str_int(girl.get_stat(stat.name)) size res_font(14) color c_brown xalign 1.0:
                            if change:
                                bold True

                        if change:
                            text "  {font=DejaVuSans.TTF}➔{/font}  " + str_int(girl.get_stat(stat.name) + change) size res_font(14) bold True:
                                if change >= 0:
                                    color c_emerald
                                else:
                                    color c_red
                        else:
                            null

                grid 3 7:
                    for stat in girl.sex_stats:
                        $ change = 0
                        if selected_item:
                            if selected_item.equipped:
                                $ change = -round_int(girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("change", stat.name) + (1 - selected_item.get_effect("boost", stat.name))*girl.get_stat(stat.name)))
                            else:
                                $ change = round_int(girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("change", stat.name) + (1 - selected_item.get_effect("boost", stat.name))*girl.get_stat(stat.name)))

                                for it in girl.equipped:
                                    if it.slot == selected_item.slot:
                                        $ change -= round_int(girl.get_effect("boost", it.type.name.lower()) * (it.get_effect("change", stat.name) + (1 - it.get_effect("boost", stat.name))*girl.get_stat(stat.name)))

                        text stat_name_dict[stat.name] size res_font(13) bold True yalign 0.5:
                            if change:
                                color c_darkorange
                            else:
                                color c_brown
                        text str_int(girl.get_stat(stat.name)) size res_font(14) color c_brown xalign 1.0:
                            if change:
                                bold True

                        if change:
                            text "  {font=DejaVuSans.TTF}➔{/font}  " + str_int(girl.get_stat(stat.name) + change) size res_font(14):
                                if change > 0:
                                    color c_emerald
                                else:
                                    color c_red
                        else:
                            text "" size res_font(14)

                    text "" size res_font(14)
                    text "" size res_font(14)
                    text "" size res_font(14)

                    $ change = 0
                    if selected_item:
                        if selected_item.equipped:
                            $ change = -round_int(girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("change", "defense") + (1 - selected_item.get_effect("boost", "defense"))*girl.get_stat("defense")))
                        else:
                            $ change = round_int(girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("change", "defense") + (1 - selected_item.get_effect("boost", "defense"))*girl.get_stat("defense")))

                            for it in girl.equipped:
                                if it.slot == selected_item.slot:
                                    $ change -= round_int(girl.get_effect("boost", it.type.name.lower()) * (it.get_effect("change", "defense") + (1 - it.get_effect("boost", "defense"))*girl.get_stat("defense")))

                    text __("Defense") size res_font(13) color c_brown:
                        if change:
                            bold True
                    text str_int(girl.get_defense()) size res_font(14) color c_brown xalign 1.0:
                        if change:
                            bold True

                    if change:
                        text " -> " + str_int(girl.get_stat("defense") + change) size res_font(14):
                            if change > 0:
                                color c_emerald
                            else:
                                color c_red

                    else:
                        text "" size res_font(14)

                    $ change = 0
                    if selected_item:
                        $ change = girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("gain", "energy")*girl.get_effect("boost", "energy") + girl.get_effect("change", "energy"))

        #                if selected_item.equipped:
        #                    $ change = -round_int(girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("change", "energy") + (1 - selected_item.get_effect("boost", "energy"))*girl.energy))
        #                else:
        #                    $ change = round_int(girl.get_effect("boost", selected_item.type.name.lower()) * (selected_item.get_effect("change", "energy") + (1 - selected_item.get_effect("boost", "energy"))*girl.energy))

        #                    for it in girl.equipped:
        #                        if it.slot == selected_item.slot:
        #                            $ change -= round_int(girl.get_effect("boost", it.type.name.lower()) * (it.get_effect("change", "energy") + (1 - it.get_effect("boost", "energy"))*girl.energy))
                    text stat_name_dict["Energy"] size res_font(13) color c_brown:
                        if change:
                            bold True
                    text str_int(girl.energy) size res_font(14) color c_brown xalign 1.0:
                        if change:
                            bold True
                    if change:
                        if girl.energy + change > girl.get_stat_minmax("energy")[1]:
                            $ change = girl.get_stat_minmax("energy")[1] - girl.energy
                        text " -> " + str_int(girl.energy + change) size res_font(14):
                            if change > 0:
                                color c_emerald
                            else:
                                color c_red
                    else:
                        text "" size res_font(14)

screen trait_details(girl):

    tag trait_details

    default yadj = ui.adjustment()
    default t = 0

    if len(girl.traits+girl.perks) > 20:
        if yadj.value < len(girl.traits+girl.perks)*25:
            timer 0.1 repeat True action (SetScreenVariable("t", t + 0.1), Function(yadj.change, max(0, 25*(t-0.25)))) # Scrolls down after 0.25 seconds

    frame:
        background c_ui_darker
        xpos 0.31
        xanchor 0.0
        yalign 0.7
        xsize 0.45
        ymaximum 0.85

        viewport:
            yadjustment yadj
            yfill False

            has vbox

            spacing 3

            text __("%s's traits") % (girl.fullname) xalign 0.5 color c_orange

            text "" size res_font(6)

            for trait in girl.traits:
                hbox:
                    frame background None ypadding 0 xsize xres(150) xfill True xalign 0.0 yalign 0.0:
                        text trait.display_name xmaximum xres(150) yalign 0.0 size res_font(14) bold True:
                            if trait in gold_traits:
                                color c_orange
                            elif trait in pos_traits:
                                color c_emerald
                            elif trait in neg_traits:
                                color c_crimson
                    text trait.get_description(short=True) xfill True size res_font(14) xalign 0.0 yalign 0.0

            text "" size res_font(6)

            if girl.perks:

                text __("%s's perks") % girl.name xalign 0.5 color c_orange

                text "" size res_font(6)

                for perk in girl.perks:
                    hbox:
                        frame background None ypadding 0 xsize xres(150) xfill True xalign 0.0 yalign 0.0:
                            text __(perk.name) xmaximum xres(150) yalign 0.0 size res_font(13) bold True
                        text perk.get_description(short=True) xfill True size res_font(13) xalign 0.0 yalign 0.0

screen perk_details(girl):

    tag trait_details

    if girl.perks:
        frame:
            background c_ui_darker
            xalign 0.5
            yalign 0.8
            xsize int(config.screen_width / 2.8)
            ymaximum int(config.screen_height*0.8)

            has vbox spacing 3

            text  __("%s's active perks") % girl.name xalign 0.5 color c_orange

            text "" size res_font(6)

            for perk in girl.perks:
                hbox:
                    frame background None ypadding 0 xsize xres(150) xfill True xalign 0.0 yalign 0.0:
                        text __(perk.name) xmaximum xres(150) yalign 0.0 size res_font(13) bold True
                    text perk.get_description(short=True) xmaximum xres(250) size res_font(13)
