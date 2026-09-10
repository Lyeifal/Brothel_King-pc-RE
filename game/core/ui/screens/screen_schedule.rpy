#### Screen Schedule — Schedule management | 日程安排界面 ####
# Phase 2: 日程安排/保存/读取
# Contains: screen schedule, screen save_schedule, screen load_schedule
# Extracted from ui/screens.rpy on 2026-09-10

screen schedule(glist):

    modal True

    key "mouseup_3" action (Return())
    key "noshift_K_d" action Return()

    use dark_filter(False)

    frame:
        ypos 0.08
        xmargin 20
#        ymargin 20
        xpadding 20
        ypadding 20

        has vbox

        spacing 3

        hbox:
            spacing 6
            xfill True
            ysize yres(22)
            xalign 1.0
            hbox:
                xsize xres(150)
                xfill True
                xalign 0.0
                yalign 1.0
                text _("Girl Schedule") color c_darkorange xsize xres(95) xalign 0.5 yalign 0.0 text_align 1.0 size res_font(20)

            for day in weekdays:

                frame xsize xres(88) ysize yres(20)  yalign 1.0 background None:
                    text day size res_font(14) xalign 0.5 color c_brown xsize xres(90):
                        if day == calendar.get_weekday():
                            bold True

            null width xres(20)

            if brothel.get_effect("special", "autorest") or debug_mode:
                frame xsize xres(88) ysize yres(20)  yalign 1.0 background None:
                    text _("Autorest") color c_emerald size res_font(14) xalign 0.5

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            ymaximum 0.8
            yfill False
            yadjustment sched_adj

            has vbox
            spacing 6

            for girl in glist:
                hbox:
                    spacing 6
                    xfill True
                    xalign 1.0

                    hbox:
                        xsize xres(150)
                        xfill True
                        xalign 1.0
                        yalign 0.5

                        button xsize xres(95) ysize yres(53) style "girlbutton" xpadding xres(6) ypadding yres(3) action (SetVariable("selected_girl", girl), Return()) tooltip __("Click here to check %s's profile.") % girl.fullname:
                            has vbox

                            xalign 1.0
                            yalign 0.5

                            text girl.name size res_font(14) text_align 1.0 color c_brown xalign 1.0:

                                if selected_girl == girl:
                                    bold True
                                    color c_white

                            if girl.job:
                                $ text1 = __(girl.job.capitalize())
                                $ col = job_color[girl.job]
                            else:
                                $ text1 = __("No job")
                                $ col = c_white

                            text text1 size res_font(12) text_align 1.0 color col xalign 1.0

                            if girl.exhausted:
                                $ text1 = event_color["a little bad"] % "Exhausted"
                            elif girl.hurt:
                                $ text1 = event_color["bad"] % ("Hurt (" + str(round_int(girl.hurt)) + " days)")
                            else:
                                $ en_max = girl.get_stat_minmax("energy")[1]

                                if girl.energy < en_max / 5:
                                    $ text1 = "{color=[c_red]}" + str(round_int(girl.energy)) + "{/color}/" + str(round_int(en_max))
                                else:
                                    $ text1 = str(round_int(girl.energy)) + "/" + str(round_int(en_max))

                            text text1 size res_font(12) text_align 1.0 color c_brown xalign 1.0

                        hbox:
                            xmaximum xres(50)
                            xfill True
                            xalign 1.0
                            yalign 0.5
                            spacing 20

                            fixed fit_first True xalign 0.5 yalign 0.5:
                                add girl.portrait.get(*res_tb(40)) xalign 0.5 yalign 0.5

                                $ badge = girl.get_badge()
                                if badge:
                                    add ProportionalScale(badge, *res_tb(20)) xalign 0.9 yalign 0.1

                    for day in weekdays:

                        if girl.workdays[day] == 100:
                            $ ttip = "She will work to the maximum of her abilities."

                        elif girl.workdays[day] == 50:
                            $ ttip = "She will receive half the usual number of clients, saving some energy."

                        elif girl.workdays[day] == 0:
                            $ ttip = "She will rest and recover some energy."

                        $ ttip += "\n{i}Right-click to reverse cycle order.{/i}"

                        textbutton workshift_dict[girl.workdays[day]] text_size res_font(14) xsize xres(90) ysize yres(40) yalign 0.5 tooltip ttip idle_background workshift_color[girl.workdays[day]] hover_background c_darkbrown + "CC":
                            if girl.block_schedule != day:
                                action Function(girl.cycle_workday, day) # renpy.curried_invoke_in_new_context(girl.cycle_workday, day)
                                alternate Function(girl.cycle_workday, day, True)
                            else:
                                action Function(notify, "You cannot change her schedule as you gave her a day off.")
                                alternate Function(notify, "You cannot change her schedule as you gave her a day off.")


                    hbox yalign 0.5:
                        textbutton _("S") text_size res_font(14) action ShowTransient("save_schedule", girl=girl, transition=Dissolve(0.15)) tooltip "Click here to save %s's schedule." % girl.fullname
                        textbutton _("L") text_size res_font(14) action ShowTransient("load_schedule", girl=girl, transition=Dissolve(0.15)) tooltip "Click here to load a schedule for %s." % girl.fullname
                    
                    if brothel.get_effect("special", "autorest")  or debug_mode:
                        if autorest_limit[girl] > 0:
                            $ text1 = "at %i en." % autorest_limit[girl]
                        else:
                            $ text1 = "No"

                        textbutton text1 text_size res_font(14) action Show("autorest", girl=girl) tooltip "Set up %s's autorest options." % girl.fullname yalign 0.5 xsize xres(70)

        text ""

        hbox spacing 10 xalign 1.0:
            if brothel.get_effect("special", "autorest") or debug_mode:
                textbutton _("Autorest options") xalign 1.0 action Show("autorest") tooltip _("Adjust default autorest options")
            textbutton _("Ok") action (Return())

screen save_schedule(girl):

    modal True

    key "mouseup_3" action Hide("save_schedule", transition=Dissolve(0.15))

    frame background c_ui_darkblue align(0.5, 0.5) xpadding xres(20) ypadding yres(20):

        vbox:
            text (_("Save %s's schedule") % (event_color["special"] % girl.fullname)) bold True color c_white size res_font(18) xalign 0.5
            null height yres(20)
            for i in range(10):
                button action (Function(game.save_schedule, girl, i), Hide("save_schedule", transition=Dissolve(0.15))) xsize xres(220) ysize yres(28):
                    hbox spacing xres(20) yalign 0.5:
                        textbutton str(i+1) xsize xres(20) xalign 0.5 background None
                        if game.saved_schedules[i]:
                            hbox align(0.5, 0.5):
                                for j in range(7):
                                    textbutton weekdays[j][0] xalign 0.5 background workshift_color[game.saved_schedules[i][j]]
                        else:
                            text _("Empty") italic True size res_font(18)

            null height yres(10)
            textbutton _("Cancel") action Hide("save_schedule", transition=Dissolve(0.15)) xalign 1.0

screen load_schedule(girl):

    modal True

    key "mouseup_3" action Hide("load_schedule", transition=Dissolve(0.15))

    frame background c_ui_darkblue align(0.5, 0.5) xpadding xres(20) ypadding yres(20):

        vbox:
            text (_("Load a schedule for %s") % (event_color["special"] % girl.fullname)) bold True color c_white size res_font(18) xalign 0.5
            null height yres(20)
            for i in range(10):
                button xsize xres(220) ysize yres(28):
                    if game.saved_schedules[i]:
                        action (Function(girl.load_schedule, game.saved_schedules[i]), Hide("load_schedule", transition=Dissolve(0.15)))
                    hbox spacing xres(20) yalign 0.5:
                        textbutton str(i+1) xsize xres(20) xalign 0.5 background None
                        if game.saved_schedules[i]:
                            hbox align(0.5, 0.5):
                                for j in range(7):
                                    textbutton weekdays[j][0] xalign 0.5 background workshift_color[game.saved_schedules[i][j]]
                        else:
                            text _("Empty") italic True size res_font(18)

            null height yres(10)
            textbutton _("Cancel") action Hide("load_schedule", transition=Dissolve(0.15)) xalign 1.0


# screen autorest + level + perks → EXTRACTED to ui/screens/screen_progress.rpy (Phase 2)
# 升级/加点/作息 已提取到 screen_progress.rpy
