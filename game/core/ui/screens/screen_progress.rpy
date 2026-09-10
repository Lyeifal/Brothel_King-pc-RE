#### Screen Progress — Level, perks and autorest | 升级/加点/作息界面 ####
# Phase 2: 升级/加点/作息
# Contains: screen autorest, screen level, screen perks
# Extracted from ui/screens.rpy on 2026-09-10

screen autorest(girl="default"):
    modal True

    key "mouseup_3" action Hide("autorest")

    if girl == "default":
        $ girl_name = "Default"
    elif isinstance(girl, Girl):
        $ girl_name = girl.name

    frame background c_ui_darkblue xalign 0.5 yalign 0.5 xpadding 10 ypadding 10:
        has vbox spacing 6

        hbox xalign 0.5 spacing xres(12):
            if isinstance(girl, Girl):
                add girl.portrait.get(*res_tb(80)) yalign 0.5
            text girl_name color c_white bold True yalign 0.5
            text _("- Autorest options") color c_white bold True yalign 0.5

        text ""
        add "resources/items/furniture/scanner.webp" xalign 0.5
        text ""
        if girl == "default":
            text "This makes your girls rest automatically if their energy falls too low.\nLeft-click to increase threshold / Right-click to lower it.\nThis will only apply to new girls unless you click 'Apply to all'" italic True size res_font(14) color c_white xsize xres(360)
        else:
            text "This makes your girl rest automatically if her energy falls too low.\nLeft-click to increase threshold / Right-click to lower it." italic True size res_font(14) color c_white xsize xres(360)
            
        text "" size res_font(18)
        if autorest_limit[girl] == 0:
            $ text1 = "%s - Autorest OFF"
        else:
            $ text1 = "%s - Autorest at <=" + str(autorest_limit[girl]) + " energy"

        textbutton text1 % girl_name action Function(change_autorest, girl, "+") alternate Function(change_autorest, girl, "-") xalign 0.5 xsize xres(360) ysize yres(40) text_size res_font(18)
        text "" size res_font(18)

        if girl == "default":
            hbox xalign 1.0:
                textbutton _("Apply all") action (Function(reset_autorest), Hide("autorest")) tooltip _("Apply to all girls, ignoring their current setting.")
                textbutton _("Apply") action Hide("autorest") tooltip _("Apply for new girls only, leaving current girls' settings unchanged.")
        else:
            textbutton _("Ok") action Hide("autorest") xalign 1.0

## LEVEL & PERKS SCREEN

screen level(girl):

    modal True

    key "mouseup_3" action Hide("level")

    frame:

        background c_ui_light_solid

        xmargin 20
        ymargin 20
        xpadding 80
        ypadding 40
        xalign 0.5
        yalign 0.5
        xsize int(0.5*config.screen_width)
        xfill True

        has vbox

        spacing 3
        xalign 0.5

        $ text1 = __("%s is ready to level up.") % girl.name

        text text1 color c_emerald xalign 0.5

        hbox:
            spacing 6
            xalign 0.5
            text _("Available points:") size res_font(14) color c_brown
            text str(round_int(girl.upgrade_points)) size res_font(14) color c_emerald

        text ""

        vbox:

            for stat in gstats_main:

                hbox spacing 3:

                    frame background None xsize xres(180):
                        hbox:
                            text __("{b}%s{/b}: ") % stat_name_dict[stat] size res_font(14) color c_brown
                            text str(girl.get_stat(stat)) + " / " + str(girl.get_stat_minmax(stat)[1]) size res_font(14) color c_green

                    grid 4 1:
                        if girl.get_max_stat_upgrade_points(stat) >= 1:
                            textbutton "+1" xsize xres(50) ysize yres(25) text_size res_font(14) action (SetVariable("selected_girl", girl), SetVariable("selected_stat", stat), Return("up_stat"), Play("sound", s_click))
                        else:
                            null
                        if girl.get_max_stat_upgrade_points(stat) >= 5:
                            textbutton "+5" xsize xres(50) ysize yres(25) text_size res_font(14) action (SetVariable("selected_girl", girl), SetVariable("selected_stat", stat), Return("up_stat5"), Play("sound", s_click))
                        elif 5 > girl.get_max_stat_upgrade_points(stat) > 1 and girl.get_max_stat_upgrade_points(stat) not in (5, 10, 20):
                            textbutton "+" + str(int(girl.get_max_stat_upgrade_points(stat))) xsize xres(50) ysize yres(25) text_size res_font(14) action (SetVariable("selected_girl", girl), SetVariable("selected_stat", stat), Return("up_stat_all"), Play("sound", s_click))
                        else:
                            null
                        if girl.get_max_stat_upgrade_points(stat) >= 10:
                            textbutton "+10" xsize xres(50) ysize yres(25) text_size res_font(14) action (SetVariable("selected_girl", girl), SetVariable("selected_stat", stat), Return("up_stat10"), Play("sound", s_click))
                        elif 10 > girl.get_max_stat_upgrade_points(stat) > 5 and girl.get_max_stat_upgrade_points(stat) not in (5, 10, 20):
                            textbutton "+" + str(int(girl.get_max_stat_upgrade_points(stat))) xsize xres(50) ysize yres(25) text_size res_font(14) action (SetVariable("selected_girl", girl), SetVariable("selected_stat", stat), Return("up_stat_all"), Play("sound", s_click))
                        else:
                            null
                        if girl.get_max_stat_upgrade_points(stat) >= 20:
                            textbutton "+20" xsize xres(50) ysize yres(25) text_size res_font(14) action (SetVariable("selected_girl", girl), SetVariable("selected_stat", stat), Return("up_stat20"), Play("sound", s_click))
                        elif 20 > girl.get_max_stat_upgrade_points(stat) > 10 and girl.get_max_stat_upgrade_points(stat) not in (5, 10, 20):
                            textbutton "+" + str(int(girl.get_max_stat_upgrade_points(stat))) xsize xres(50) ysize yres(25) text_size res_font(14) action (SetVariable("selected_girl", girl), SetVariable("selected_stat", stat), Return("up_stat_all"), Play("sound", s_click))
                        else:
                            null

        text ""

        if girl.perk_points > 0:
            $ _next = "perks"
        else:
            $ _next = ""

        textbutton _("Ok") xalign 1.0 action (Hide("level"), Return(_next))

screen perks(girl):

    modal True

    default selected_archetype = "The Maid"
    default selected_perk = None

    default alpha_unhover = 0.6
    default alpha_hover = 1.0
    default alpha_dict = {k: 0.6 for k in archetype_list}

    key "mouseup_3" action Return(("commit", ""))

    use dark_filter(False)

    frame ypos 0.1 xalign 0.5 xpadding xres(20) ypadding yres(20):
        background c_ui_light_solid

        has vbox spacing 10 xalign 0.5

        text __("%s's perks") % girl.fullname color c_darkorange xalign 0.5

        hbox:
            for archetype in archetype_list:
                button xsize xres(100) xfill True background None action (SetScreenVariable("selected_archetype", archetype), SelectedIf(selected_archetype==archetype)):
                    hovered SetDict(alpha_dict, archetype, alpha_hover)
                    unhovered SetDict(alpha_dict, archetype, alpha_unhover)
                    vbox:
                        fixed:
                            fit_first True
                            if girl.archetypes[archetype].unlocked:
                                add girl.archetypes[archetype].get_pic(portrait=True).get(*res_tb(75)) alpha alpha_dict[archetype]
                            else:
                                add girl.archetypes[archetype].get_pic(portrait=True).get(*res_tb(75)) alpha alpha_dict[archetype] at desaturate
                                add "img_lock"  zoom 0.7 xalign 0.5 yalign 0.5 alpha alpha_dict[archetype]

                        text archetype size res_font(12) selected_bold True color c_darkgrey selected_color c_black

        frame background c_ui_dark xalign 0.5 yalign 0.5 ypadding 0 xpadding 0 xmargin 0:
            fixed fit_first True:
                add archetype_dict[selected_archetype].get_pic().get(yres(800), yres(640)) alpha 0.6

                if not girl.archetypes[selected_archetype].unlocked:
                    add "img_lock" xpos 0 ypos 0.03

                hbox xalign 1.0 xfill True yfill True:
                    fixed xalign 0.3 ypos 0.05 xsize yres(400) ysize yres(620) xfill True yfill True:
                        fit_first True

                        $ perks = archetype_dict[selected_archetype].get_perks()
                        $ pos_dict = {0: (yres(150), 0), 1: (0, yres(100)), 2: (yres(300), yres(100)), 3: (0, yres(250)), 4: (yres(300), yres(250)), 5: (yres(150), yres(350))}

                        add "lines" xalign 0.5 ypos 0.05 alpha 0.7 fit "contain"

                        for perk in perks:
                            $ perk_index = perks.index(perk)

                            button xpos pos_dict[perk_index][0] ypos pos_dict[perk_index][1] xsize yres(110) ysize yres(110) xfill True yfill True:

                                if girl.has_perk(perk.name) or perk in new_perks:
                                    background c_ui_unlocked
                                    add perk.get_pic().get(*res_tb(100)) xalign 0.5 yalign 0.5
                                    action NullAction()
                                    hovered (tt.Action(_("This perk has already been unlocked.")), SetScreenVariable("selected_perk", perk))
                                    unhovered SetScreenVariable("selected_perk", None)

                                elif girl.can_acquire_perk(perk, context="perk_screen")[0]:
                                    at alpha_transform
                                    background c_ui_sensitive + "DD"
                                    hover_background c_ui_sensitive
                                    add perk.get_pic().get(*res_tb(100)) xalign 0.5 yalign 0.5 # alpha 0.6 hover_alpha 1.0
                                    action Return(("add", perk))
                                    hovered (tt.Action("Acquire " + perk.name + " for 1 perk point."), SetScreenVariable("selected_perk", perk))
                                    unhovered SetScreenVariable("selected_perk", None)
                                else:
                                    background c_ui_insensitive + "AA"
                                    # button background None xsize xres(110) ysize yres(110) xfill True yfill True:
                                    add perk.get_pic().get(*res_tb(100)) xalign 0.5 yalign 0.5 at desaturate
                                    action NullAction()
                                    hovered (tt.Action(event_color["a little bad"] % girl.can_acquire_perk(perk, context="perk_screen")[1]), SetScreenVariable("selected_perk", perk))
                                    unhovered SetScreenVariable("selected_perk", None)

                    frame background c_ui_dark xsize xres(260) xalign 1.0 xfill True yfill True:
                        # vbox spacing yres(10) xfill True yfill True:

                            vbox xfill True spacing yres(10):

                                if selected_perk:
                                    $ title = selected_perk.name
                                    $ pic = selected_perk.get_pic()
                                    if selected_perk.min_rank:
                                        $ text1 = "Rank " + rank_name[selected_perk.min_rank] + " perk"
                                    else:
                                        $ text1 = "Rank C perk"
                                    $ text2 = selected_perk.get_description()

                                else:
                                    $ title = selected_archetype
                                    $ pic = archetype_dict[selected_archetype].get_pic()
                                    $ text1 = ""
                                    $ text2 = archetype_description[selected_archetype]

                                text __(title) size res_font(18) bold True yalign 0.0 xalign 0.5 drop_shadow 2,2

                                add pic.get(*res_tb(220)) xalign 0.5

                                if not selected_perk and not girl.archetypes[selected_archetype].unlocked:
                                    textbutton _("Unlock\n{size=-6}(costs 2 perk points){/size}") xalign 0.5 xpadding 6 ypadding 6:
                                        if perk_points >= 2:
                                            action Return(("unlock", selected_archetype))

                                text __(text1) size res_font(14) bold True yalign 0.0
                                text __(text2) size res_font(14) yalign 0.0

                            vbox yalign 1.0 xfill True:
                                text __("Perk points: %s") % str_int(perk_points) color c_orange size res_font(20) xalign 0.5 drop_shadow 2,2
                                hbox xalign 0.5:
                                    textbutton _("Cancel") action Return(("cancel", ""))
                                    textbutton _("Confirm"):
                                        if new_perks:
                                            action Return(("commit", ""))


# screen trait_details + perk_details → EXTRACTED to ui/screens/screen_girl_stats.rpy (Phase 2)
# 女孩属性/属性条/特性详情 已提取到 screen_girl_stats.rpy

# screen girl_log → EXTRACTED to ui/screens/screen_girl_log.rpy (Phase 2)
# 女孩日志/昨夜回顾 已提取到 screen_girl_log.rpy
