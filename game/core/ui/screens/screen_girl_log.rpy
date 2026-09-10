#### Screen Girl Log — Girl logs and night reports | 女孩日志界面 ####
# Phase 2: 女孩日志/昨夜回顾
# Contains: screen girl_log, screen previous_night_log
# Extracted from ui/screens.rpy on 2026-09-10

screen girl_log(): # Reminder: selected_girl is a Global variable that holds the currently selected girl

    modal True

    key "mouseup_3" action Return()

    use dark_filter(can_click=False)

#     $ girl = selected_girl
    $ log_dict = compile_girl_log(selected_girl) # Hands the screen a dictionary holding all calculations (to avoid refreshing calc with every frame)

    default days = 1

    $ biggest = res_font(24)

    $ big = res_font(18)

    $ average = res_font(14)

    $ small = res_font(12)

    frame:
        background None
        yalign 0.5
        ypadding 0
        ymargin 20

        has vbox

        frame:
            xmargin 40
            ymargin 0
            xpadding 40
            ypadding 20
            xalign 0.5
            yalign 0.5

            yfill False
            xfill True

            has vbox

            use close(Return())
            use girl_select(MC.girls, orange = True)

            text "" size average
            text "" size average

            hbox:

                xfill True
                yfill False

                textbutton _("Yesterday") action SetScreenVariable("days", 1) xsize xres(200) background c_brown + "AA" text_color c_white selected_idle_background c_orange + "AA" selected_hover_background c_orange + "AA" hover_background c_orange + "55"

                textbutton _("Last 7 days") action SetScreenVariable("days", 7) xsize xres(200) background c_brown + "AA" text_color c_white selected_idle_background c_orange + "AA" selected_hover_background c_orange + "AA" hover_background c_orange + "55"

                textbutton _("Last 28 days") action SetScreenVariable("days", 28) xsize xres(200) background c_brown + "AA" text_color c_white selected_idle_background c_orange + "AA" selected_hover_background c_orange + "AA" hover_background c_orange + "55"

                textbutton _("All time") action SetScreenVariable("days", 0) xsize xres(200) background c_brown + "AA" text_color c_white selected_idle_background c_orange + "AA" selected_hover_background c_orange + "AA" hover_background c_orange + "55"


        frame:
            xmargin 40
            ymargin 0
            xpadding 40
            ypadding 20

            xalign 0.5
            yalign 0.5
            xfill False
            yfill False

            has vbox

            xfill True
            yfill False
            xalign 0.5

            hbox:
                vbox:
                    hbox:
                        spacing 150

                        vbox:
                            text _("General") size average color c_prune

                            text "" size average

                            grid 5 2:

                                transpose True
                                spacing 3

                                text _("{b}Days{/b}") color c_darkgrey size small xalign 0.5

                                if days == 0:
                                    text str(log_dict["age"]) size average color c_prune xalign 0.5

                                elif days > log_dict["age"]:
                                    text str(log_dict["age"]) size average color c_prune xalign 0.5

                                else:
                                    text str(days) size average color c_prune xalign 0.5

                                text _("{b}Gold{/b}") color c_darkgold size small xalign 0.5

                                $ j_gold = log_dict["total_gold"][days]
                                $ q_gold = log_dict["quest_gold"][days]
                                $ upk = log_dict["upkeep"][days]
                                $ net = j_gold + q_gold - upk

                                if round_int(net) < 0:
                                    $ col1 = c_red
                                elif round_int(net) > 0:
                                    $ col1 = c_green
                                else:
                                    $ col1 = c_white

                                $ ttip = __("{b}Profit: {color=[c_white]}%s{/color}{/b}") % str_int(net)
                                $ ttip += __("\nJobs: {color=[c_green]}%s{/color}") % str_int(j_gold)
                                $ ttip += __("     Quests: {color=[c_green]}%s{/color}") % str_int(q_gold)
                                $ ttip += __("\nUpkeep: {color=[c_red]}-%s{/color}") % str_int(upk)

                                textbutton str_int(j_gold + q_gold) background None xpadding 0 ypadding 0 xmargin 0 ymargin 0 text_size average text_color c_prune xalign 0.5 action NullAction() tooltip ttip

                                text _("{b}XP{/b}") color c_emerald size small xalign 0.5

                                text str_int(log_dict["total_xp"][days]) size average color c_prune xalign 0.5

                                text _("{b}JP{/b}") color c_orange size small xalign 0.5

                                text str_int(log_dict["total_jp"][days]) size average color c_prune xalign 0.5

                                text _("{b}Reputation{/b}") color c_purple size small xalign 0.5

                                text str_int(log_dict["total_rep"][days]) size average color c_prune xalign 0.5

                        vbox:
                            text _("Activity") size average color c_prune

                            hbox:

                                spacing 20

                                grid 2 4:

                                    spacing 3

                                    text "" size small

                                    text _("{b}Days{/b}") color c_darkgrey size small xalign 0.5

                                    text _("{b}Worked{/b}") color c_orange size small xalign 0.5

                                    $ ttip = __("Waitress: %s              Dancer: %s\nMasseuse: %s            Geisha: %s\nWhore: %s                 Work/whore : %s") % (str_int(log_dict["waitress_days"][days]), str_int(log_dict["waitress_days"][days]), str_int(log_dict["masseuse_days"][days]), str_int(log_dict["geisha_days"][days]), str_int(log_dict["whore_days"][days]), str_int(log_dict["work_whore_days"][days]))

                                    textbutton str_int(log_dict["work_days"][days]) background None xpadding 0 ypadding 0 xmargin 0 ymargin 0 text_size average text_color c_brown xalign 0.5 action NullAction() hovered tt.Action(ttip)

                                    text _("{b}Rested{/b}") color c_green size small xalign 0.5

                                    text str_int(log_dict["rest_days"][days]) size average color c_brown xalign 0.5

                                    text _("{b}Away{/b}") color c_blue size small xalign 0.5

                                    text str_int(log_dict["away_days"][days] + log_dict["farm_days"][days]) size average color c_brown xalign 0.5

                                grid 2 3:

                                    spacing 3

                                    text "" size small

                                    text _("{b}Days{/b}") color c_darkgrey size small xalign 0.5

                                    text _("{b}On strike{/b}") color c_red size small xalign 0.5

                                    text str_int(log_dict["strike_days"][days]) size average color c_brown xalign 0.5

                                    text _("{b}Hurt/Sick{/b}") color c_red size small xalign 0.5

                                    text str_int(log_dict["hurt_days"][days] + log_dict["sick_days"][days]) size average color c_brown xalign 0.5

#                                    text "{b}Sick{/b}" color c_red size small xalign 0.5

#                                    text str_int(log_dict["sick_days"][days]) size average color c_brown xalign 0.5

                    text "" size average

    #            vbox:

                    text _("Jobs") size average color c_prune

#                    text "" size average

                    grid 7 6:

                        spacing 1

                        text "" size small

                        text _("{b}Customers{/b}") color c_darkgrey size small xalign 0.5

                        text _("{b}Gold{/b}") color c_darkgold size small xalign 0.5

                        text _("{b}XP{/b}") color c_emerald size small xalign 0.5

                        text _("{b}JP{/b}") color c_orange size small xalign 0.5

                        text _("{b}Reputation{/b}") color c_purple size small xalign 0.5

                        text "{b}Av. score{/b}" color c_crimson size small xalign 0.5

                        for job in all_jobs:

                            text __("{b}%s{/b}") % job.capitalize() color c_firered size small xalign 0.5

                            text str_int(log_dict[job + "_cust"][days]) size average color c_brown xalign 0.5

                            text str_int(log_dict[job + "_gold"][days]) size average color c_brown xalign 0.5

                            text str_int(log_dict[job + "_xp"][days]) size average color c_brown xalign 0.5

                            text str_int(log_dict[job + "_jp"][days]) size average color c_brown xalign 0.5

                            text str_int(log_dict[job + "_rep"][days]) size average color c_brown xalign 0.5

                            $ perf, ttip = log_dict[job + "_perf"][days]

                            if perf != "-":
                                if perf <= 2:
                                    $ col1 = c_red
                                elif perf <= 5:
                                    $ col1 = c_lightred
                                elif perf <= 8:
                                    $ col1 = c_brown
                                elif perf <= 11:
                                    $ col1 = c_lightgreen
                                elif perf <= 14:
                                    $ col1 = c_green
                                else:
                                    $ col1 = c_orange

                            textbutton str(perf) background None xpadding 0 ypadding 0 xmargin 0 ymargin 0 text_size average text_color col1 xalign 0.5 action NullAction() hovered tt.Action(ttip)


                        text _("{b}Whore{/b}") color c_firered size small xalign 0.5

                        text str(round_int(log_dict["whore_cust"][days])) size average color c_brown xalign 0.5

                        text str_int(log_dict["whore_gold"][days]) size average color c_brown xalign 0.5

                        text str_int(log_dict["whore_xp"][days]) size average color c_brown xalign 0.5

                        text str_int(log_dict["whore_jp"][days]) size average color c_brown xalign 0.5

                        text str_int(log_dict["whore_rep"][days]) size average color c_brown xalign 0.5

                        $ perf, ttip = log_dict["whore_perf"][days]

                        if perf != "-":
                            if perf <= 2:
                                    $ col1 = c_red
                            elif perf <= 5:
                                $ col1 = c_lightred
                            elif perf <= 8:
                                $ col1 = c_prune
                            elif perf <= 11:
                                $ col1 = c_lightgreen
                            elif perf <= 14:
                                $ col1 = c_green
                            else:
                                $ col1 = c_orange

                        textbutton str(perf) background None xpadding 0 ypadding 0 xmargin 0 ymargin 0 text_size average text_color col1 xalign 0.5 action NullAction() hovered tt.Action(ttip)


                    text "" size average

                    text _("Sex Acts") size average color c_prune

#                    text "" size average

                    grid 7 5:

                        spacing 1

                        text "" size small

                        text _("{b}Customers{/b}") color c_darkgrey size small xalign 0.5

                        text _("{b}Gold{/b}") color c_darkgold size small xalign 0.5

                        text _("{b}Xp{/b}") color c_emerald size small xalign 0.5

                        text _("{b}JP{/b}") color c_orange size small xalign 0.5

                        text _("{b}Reputation{/b}") color c_purple size small xalign 0.5

                        text "{b}Av. score{/b}" color c_crimson size small xalign 0.5

                        for act in all_sex_acts:

                            text __("{b}%s{/b}") % act.capitalize() color c_firered size small xalign 0.5

                            text str_int(log_dict[act + "_cust"][days]) size average color c_brown xalign 0.5

                            text str_int(log_dict[act + "_gold"][days]) size average color c_brown xalign 0.5

                            text str_int(log_dict[act + "_xp"][days]) size average color c_brown xalign 0.5

                            text str_int(log_dict[act + "_jp"][days]) size average color c_brown xalign 0.5

                            text str_int(log_dict[act + "_rep"][days]) size average color c_brown xalign 0.5

                            $ perf, ttip = log_dict[act + "_perf"][days]

                            textbutton str(perf) background None xpadding 0 ypadding 0 xmargin 0 ymargin 0 text_size average text_color c_prune xalign 0.5 action NullAction() hovered tt.Action(ttip)


screen previous_night_log(log):
    modal True

    key "mouseup_3" action (Hide("previous_night_log"))

    use dark_filter

    frame ypos 0.1 xpadding 12 ypadding 12:
        use night_log(log, use_filter=True)

    use close(Hide("previous_night_log"))
