#### Screen Home — Home screen and brothel report | 主页/青楼报告界面 ####
# Phase 2: 主页/青楼报告
# Contains: screen home, screen brothel_report
# Extracted from ui/screens.rpy on 2026-09-10

screen home():

    tag menu
    use overlay("main")
    use right_menu
    use shortcuts()


############ Jman - Headhunter Mod ############
    if game.has_active_mod("Headhunter Mod"):
        if game.headhunter_girl:
            $ game.headhunter_button_enabled = 0
            if game.headhunter_time <= 0:
                if not game.interacting_with_headhunter:
                    textbutton HH_back_caption:
                        xalign HH_button_align["main x"]
                        yalign HH_button_align["main y"]
                        text_size HH_button_text_size
                        text_font HH_button_text_font
                        action Jump(HH_main_jump_label)
                        hovered tt.Action(HH_back_text)

            else:
                textbutton HH_wait_caption:
                    xalign HH_button_align["main x"]
                    yalign HH_button_align["main y"]
                    text_size HH_button_text_size
                    text_font HH_button_text_font
                    hovered tt.Action(HH_wait_text)
        else:
            $ game.headhunter_button_enabled = 1
############ Jman - Headhunter Mod End ########

    if always_show_brothel_report:
        use brothel_report

    button background None action (Hide("brothel_report"), ToggleVariable("always_show_brothel_report"), SelectedIf(always_show_brothel_report)) xalign 0.5 xmargin 25 ypos 0.1 :
        if not always_show_brothel_report:
            tooltip _("Click to keep the brothel report showing at all times.")
            hovered (Show("brothel_report"))
            unhovered Hide("brothel_report")
        else:
            tooltip _("Click to hide the brothel report.")

        hbox xalign 0.0 spacing 10:
            frame xalign 0.0 xsize xres(25) ysize yres(25):
                style "contrast_button"
                hover_background Frame("orange_button")
                selected_background Frame("darkorange_button")

                if always_show_brothel_report:
                    text "✓" font "resources/fonts/DejaVuSans.ttf" size res_font(14) xalign 0.5 yalign 0.5
                else:
                    text " " size res_font(14) xalign 0.5
            text _("Show brothel report") size res_font(14) xalign 0.0 yalign 0.5 drop_shadow (2, 2)

screen brothel_report():

    tag brothel_report

    if brothel.get_cleanliness() in ("disgusting", "fire"):
        default side_pic = "side sill sad"
        default shown_tip = __("Master!!! %s is very dirty... Please do something!") % brothel.name
    elif calendar.time == 1:
        default side_pic = "side sill happy"
        default shown_tip = __("Welcome to your new brothel, Master! I'm sure you will be a great manager!")
    elif logs[calendar.time-1] and logs[calendar.time-1].net < 0:
        default side_pic = "side sill sad"
        default shown_tip = __("Master!!! %s is losing money... What's going on?") % brothel.name
    else:
        default side_pic = "side sill happy"
        default shown_tip = __("{color=[c_lightblue]}Did you know? {/color}%s") % daily_tip

    frame:
        xanchor 1.0
        if screen_is_wide:
            xalign 0.85
            xsize 0.7
        else:
            xalign 0.775
            xsize 0.75
        ypos 0.15
        ysize 0.8
        xpadding xres(10)
        ypadding yres(10)

        has vbox spacing yres(10) xfill True

        hbox spacing xres(10):
            add side_pic zoom 0.5 xalign 0.0 
            textbutton _("Next\ntip") text_size 18 xalign 0.0 yalign 0.5:
                if always_show_brothel_report:
                    action SetLocalVariable("shown_tip", __("{color=[c_lightblue]}Did you know? {/color}%s") % rand_choice(random_tips))
            text shown_tip xalign 0.0 yalign 0.5 size res_font(18) justify True italic True xsize 0.8 color c_brown
            #? Why does the textbutton 'dance' around when changing tips? Investigate

        hbox spacing xres(20) xfill True yfill False:

            vbox:
                xsize 0.4
                xfill True
                yfill False

                text _("Yesterday") color c_prune

                text "" size res_font(14)

                if calendar.time > 1 and logs[calendar.time-1]:
                    text logs[calendar.time-1].get_day_report() size res_font(14) color c_brown

                    textbutton _("Show last night's log") xsize xres(250) ypadding 5 text_size res_font(14) xalign 0.5:
                        if always_show_brothel_report:
                            action (Show("previous_night_log", log=logs[calendar.time-1]))
                    textbutton _("Show satisfaction report") xsize xres(250) ypadding 5 text_size res_font(14) xalign 0.5:
                        if always_show_brothel_report:
                            action Call("latest_customer_satisfaction")

                else:
                    text _("Nothing to report") size res_font(14) italic True color c_brown

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                xfill True
                yfill False

                has vbox
                xfill True
                yfill False

                text _("Today") color c_prune

                text "" size res_font(14)

                text get_next_day_report() size res_font(14) color c_brown

                text "" size res_font(14)

                text brothel.get_ASM_report() size res_font(14) color c_brown

                text "" size res_font(14)

                text get_warnings() size res_font(14) color c_brown

# screen previous_night_log → EXTRACTED to ui/screens/screen_girl_log.rpy (Phase 2)
# 女孩日志/昨夜回顾 已提取到 screen_girl_log.rpy
