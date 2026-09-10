#### Screen Misc — Top overlay and girl list widgets | 悬浮层与女孩列表控件 ####
# Phase 2: 悬浮层/女孩列表控件
# Contains: screen tax_tooltip, screen tax_tab, screen adv_tooltip, screen girls, screen girl_tab, screen girl_pick_badge, screen badge_button, screen girl_button, screen girl_fast_actions, screen button_overlay, screen rank_level_details
# Extracted from ui/screens.rpy on 2026-09-10

screen tax_tooltip():
    zorder 10
    tag tax_tooltip

    if NPC_taxgirl.current_tax:
        use tax_tab()

    elif NPC_taxgirl.active:
        frame background c_ui_dark:
            xalign 0.5
            yalign 0.1

            hbox:
                spacing 10

                add ProportionalScale("resources/characters/npc/taxgirl/portrait.webp", *res_tb(35)) yalign 0.5

                text _("No guild fee is due.") xalign 0.0 yalign 0.5 size res_font(14) color c_emerald

screen tax_tab(fade=False):
    zorder 10
    frame background c_ui_dark:

        if fade:
            at fademove([0.5, 0.5], [0.5, 0.0])
        else:
            xalign 0.65
            yalign 0.05

        hbox:

            spacing 10

            add ProportionalScale("resources/characters/npc/taxgirl/portrait.webp", *res_tb(35)) yalign 0.5

            if calendar.day in (28, 7):
                $ due_date = "tomorrow"
            elif calendar.day in (1, 8):
                $ due_date = "tonight"
            elif calendar.day >= 15:
                $ due_date = _("in %s days") % (29-calendar.day)
            else: # Tax due date has been extended by a week
                $ due_date = _("in %s days") % (8-calendar.day)

            vbox:
                text _("Guild Fee") bold True size res_font(14)
                text (_("{image=img_gold} %s due %s.") % ('{:,}'.format(round_int(NPC_taxgirl.current_tax)).replace(',', ' '), due_date)) xalign 0.0 yalign 0.5 size res_font(14) color c_red

screen adv_tooltip():

    zorder 100

    $ ttip = GetTooltip()
    if ttip:
        nearrect:
            focus "tooltip"

            prefer_top False

            frame:
                if renpy.get_screen("home") and GetFocusRect("tooltip") and GetFocusRect("tooltip")[0] > config.screen_width - xres(150):
                    xoffset xres(-150)
                    yoffset yres(-30)
                else:
                    xoffset xres(10)
                    yoffset yres(2)
                xminimum xres(0)
                xmaximum xres(320)
                xpadding xres(10)
                ypadding yres(4)
                background c_ui_darker
                text ttip size res_font(15)


screen girls(girls, context = "girls"): # context can be girls, slavemarket, farm

    tag girls

    default hovered_girl = selected_girl

    # $ renpy.maximum_framerate(86400) #! Uncomment for stable FPS measurements

    if not girls_firstvisit:
        key "mouseup_3" action (SetVariable("choice_menu_girl_interact", False), SetVariable("selected_destination", "main"), Jump("teleport"))
        use close((SetVariable("choice_menu_girl_interact", False), SetVariable("selected_destination", "main"), Jump("teleport")))
        use shortcuts()

#    if selected_girl:
#        text selected_girl.name color c_red

    use girl_tab(girls, context=context)

    if persistent.hover_for_preview_girls and hovered_girl and hovered_girl in girls:
        use girl_stats(hovered_girl, context=context)

        use button_overlay(hovered_girl, context=context)

        use girl_profile(hovered_girl, context=context)

    elif selected_girl and selected_girl in girls:
        use girl_stats(selected_girl, context=context)

        use button_overlay(selected_girl, context=context)

        use girl_profile(selected_girl, context=context)

screen girl_tab(girls, context="girls"):

    zorder 0

    tag girl_tab

    default sort_view = "normal"

    if context == "slavemarket":

############ Jman - Headhunter Mod ############
        if game.has_active_mod("Headhunter Mod"):
            if game.headhunter_button_enabled:
                key "shift_K_h" action Jump(HH_market_jump_label)

            if game.headhunter_button_enabled:
                textbutton HH_market_caption:
                    xalign HH_button_align["market x"]
                    yalign HH_button_align["market y"]
                    text_size HH_button_text_size
                    text_font HH_button_text_font
                    action Jump(HH_market_jump_label)
                    hovered tt.Action(HH_market_text)

            else:
                textbutton HH_market_caption:
                    xalign HH_button_align["market x"]
                    yalign HH_button_align["market y"]
                    text_size HH_button_text_size
                    text_font HH_button_text_font
                    hovered tt.Action(HH_market_text)

############ Jman - Headhunter Mod End ########

        use overlay("slavemarket")
        $ sorters = ["rank", "experience", "alpha"]

    elif context == "girls":
        use overlay("girls")
        $ sorters = ["rank", "level", "job", "energy", "alpha", "badge"]

        if selected_girl:
            key "alt_K_UP" action [Function(move_up_list, girls, selected_girl)]
            key "alt_K_DOWN" action [Function(move_down_list, girls, selected_girl)]

    elif context == "farm":
        $ sorters = ["rank", "level", "alpha", "badge"]

    if selected_view_mode == "x40" or (selected_view_mode == "Auto" and len(girls) > 24):
        $ bsize = "x40"
        $ c = 4
        $ l = 10

    elif selected_view_mode == "x24" or (selected_view_mode == "Auto" and len(girls) > 12):
        $ bsize = "x24"
        $ c = 3
        $ l = 8

    elif selected_view_mode == "x12" or (selected_view_mode == "Auto" and len(girls) > 4):
        $ bsize = "x12"
        $ c = 2
        $ l = 6

    else:
        $ bsize = "x4"
        $ c = 1
        $ l = 4

    if len(girls) > 24:
        $ view_modes = ["x4", "x12", "x24", "x40", "Auto"]

    elif len(girls) > 12:
        $ view_modes = ["x4", "x12", "x24", "Auto"]

    elif len(girls) > 4:
        $ view_modes = ["x4", "x12", "Auto"]

    else:
        $ view_modes = ["x4", "Auto"]

    $ vp_adj.step = girl_but_ysize[bsize]
    $ y = int((girl_but_ysize[bsize]) * l)

    default lup_filter = False

    vbox:
        xalign 1.0
        ypos 0.075
        xsize xres(325)

        hbox xalign 0.1:
            if sort_view == "normal":
                use sorting_tab(context, girls, sorters)

                frame xsize yres(38) ysize yres(20) xpadding 0 ypadding 0 xmargin 0 ymargin 0:
                    textbutton _("Sk.") text_italic True text_color c_darkbrown text_selected_color c_emerald text_size res_font(14) xpadding 0 ypadding 0 xalign 0.5 yalign 0.6 xsize yres(38) ysize yres(20) idle_background None action SetLocalVariable("sort_view", "advanced") tooltip _("Sort girls by specific skills.")

                if view_modes:
                    $ _next = get_next(view_modes, selected_view_mode, True)

                    frame xsize yres(38) ysize yres(20) xpadding 0 ypadding 0 xmargin 0 ymargin 0:
                        textbutton selected_view_mode text_italic True text_color c_darkbrown text_size res_font(14) xpadding 0 ypadding 0 xalign 0.5 yalign 0.6 xsize yres(38) ysize yres(20) idle_background None:
                            action SetVariable("selected_view_mode", _next)
                            tooltip _("Click to change view mode")
                
                frame xsize yres(38) ysize yres(20) xpadding 0 ypadding 0 xmargin 0 ymargin 0:
                    textbutton _("L.Up") text_italic True text_color c_darkbrown text_selected_color c_emerald text_size res_font(14) xpadding 0 ypadding 0 xalign 0.5 yalign 0.6 xsize yres(38) ysize yres(20) idle_background None action ToggleLocalVariable("lup_filter"):
                        if lup_filter:
                            tooltip _("Filter girls that are ready to level up (filter ON)")
                        else:
                            tooltip _("Filter girls that are ready to level up (filter OFF)")

            
            elif sort_view == "advanced":
                use sorting_tab(context, girls, sorters = all_skills, use_stats=True, small=True)

                frame xsize yres(30) ysize yres(20) xpadding 0 ypadding 0 xmargin 0 ymargin 0:
                    textbutton "↑" text_font "DejaVuSans.TTF" text_italic True text_color c_darkbrown text_selected_color c_emerald text_size res_font(12) xpadding 0 ypadding 0 xalign 0.5 yalign 0.6 xsize yres(30) ysize yres(20) idle_background None action SetLocalVariable("sort_view", "normal") tooltip _("Go back to other filters.")


        frame:

            id "girl_tab"

            xmargin 3
            xpadding xres(3)
            ypadding 0
            if persistent.girls_display_mode == "pages":
                ysize y + yres(30)
            else:
                ysize y

            xfill True
            yfill True

            if girls:
                if girls and not girls_firstvisit:
                    key "K_UP" action [Function(select_previous_girl, girls, False, pace=c), Hide("rank_level_details"), Hide("mood_details"), Hide("sex_details"), Hide("trait_details"), Hide("perk_details")]

                    key "K_DOWN" action [Function(select_next_girl, girls, False, pace=c), Hide("rank_level_details"), Hide("mood_details"), Hide("sex_details"), Hide("trait_details"), Hide("perk_details")]

                    key "repeat_K_UP" action [Function(select_previous_girl, girls, False, pace=c), Hide("rank_level_details"), Hide("mood_details"), Hide("sex_details"), Hide("trait_details"), Hide("perk_details")]

                    key "repeat_K_DOWN" action [Function(select_next_girl, girls, False, pace=c), Hide("rank_level_details"), Hide("mood_details"), Hide("sex_details"), Hide("trait_details"), Hide("perk_details")]

                    if c > 1:

                        key "K_LEFT" action [Function(select_previous_girl, girls, False), Hide("rank_level_details"), Hide("mood_details"), Hide("sex_details"), Hide("trait_details"), Hide("perk_details")]

                        key "K_RIGHT" action [Function(select_next_girl, girls, False), Hide("rank_level_details"), Hide("mood_details"), Hide("sex_details"), Hide("trait_details"), Hide("perk_details")]

                        key "repeat_K_LEFT" action [Function(select_previous_girl, girls, False), Hide("rank_level_details"), Hide("mood_details"), Hide("sex_details"), Hide("trait_details"), Hide("perk_details")]

                        key "repeat_K_RIGHT" action [Function(select_next_girl, girls, False), Hide("rank_level_details"), Hide("mood_details"), Hide("sex_details"), Hide("trait_details"), Hide("perk_details")]

                if persistent.girls_display_mode == "vp":

                    vpgrid:
                        cols c
                        allow_underfull True # necessary to avoid VPgrid crash when modifying children
                        draggable True
                        mousewheel True

                        scrollbars "vertical"

                        side_xalign 0.0
                        side_yalign 0.0
                        vscrollbar_ysize 0.98
                        vscrollbar_yalign 0.5
                        vscrollbar_xpos 1.0
                        vscrollbar_xanchor 1.0

                        xalign 1.0
                        xfill True
                        yfill True

                        spacing 0
                        yadjustment vp_adj

                        for girl in girls:
                            if not lup_filter or girl.upgrade_points >= 1 or girl.can_perk:
                                use girl_button(girl, bsize, status_list=girl_status_dict[girl], context=context, hovered_action=SetScreenVariable("hovered_girl", girl), unhovered_action=SetScreenVariable("hovered_girl", None)) id girl.fullname + str(girl.id)

                elif persistent.girls_display_mode == "pages":

                    default current_page = 1
                    default page_offset = 0 # Adds this to page numbers when there are more than 6
                    default page_button_nb = 14 # Number of tabs
                    $ nb = c*l
                    $ page_nb = round_up(len(girls) / nb)
                    $ first_girl_index = (current_page-1)*nb
                    $ last_girl_index = min((current_page)*nb, len(girls))

                    if lup_filter:
                        $ shown_girls = [g for g in girls if g.upgrade_points >= 1 or g.can_perk]
                    else:
                        $ shown_girls = girls

                    vbox:
                        fixed ysize y:
                            hbox box_wrap True spacing 0:
                                for girl in shown_girls[first_girl_index:last_girl_index]:
                                    if not lup_filter or girl.upgrade_points >= 1 or girl.can_perk:
                                        use girl_button(girl, bsize, status_list=girl_status_dict[girl], context=context, hovered_action=SetScreenVariable("hovered_girl", girl), unhovered_action=SetScreenVariable("hovered_girl", None)) id girl.fullname + str(girl.id)

                        $ start = page_offset

                        # No arrows required
                        if page_nb <= page_button_nb:
                            $ previous = None
                            $ next = None
                            $ finish = page_nb
                        # More than one set of page numbers is needed
                        else:
                            if page_offset:
                                $ previous = page_button_nb-2
                            else:
                                $ previous = None

                            if page_nb-page_offset >= page_button_nb-1:
                                $ next = page_button_nb-2
                            else:
                                $ next = None

                            if next:
                                $ finish = start + next
                            else:
                                $ finish = page_nb

                        if page_nb > 1:
                            if current_page > 1:
                                key "mousedown_4" capture True:
                                    if current_page-1 <= start and previous:
                                        action (SetLocalVariable("current_page", current_page-1), SetLocalVariable("page_offset", page_offset-previous))
                                    else:
                                        action SetLocalVariable("current_page", current_page-1)
                            if current_page < page_nb:
                                key "mousedown_5" capture True:
                                    if current_page+1 > finish and next:
                                        action (SetLocalVariable("current_page", current_page+1), SetLocalVariable("page_offset", page_offset+next))
                                    else:
                                        action SetLocalVariable("current_page", current_page+1)

                        hbox:

                            if previous:
                                textbutton "↑" style "UI_button":
                                    xalign 0.0
                                    xsize xres(22)
                                    ysize yres(22)
                                    action (SetLocalVariable("page_offset", page_offset-previous), SetLocalVariable("current_page", page_offset))
                                    text_size res_font(14)
                                    text_font "DejaVuSans.TTF"

                            for p in range(start, finish):
                                textbutton str(p+1) style "UI_button":
                                    xalign 0.0
                                    xsize xres(22)
                                    ysize yres(22)
                                    action SetLocalVariable("current_page", p+1)
                                    text_size res_font(14)
                                    text_selected_bold True

                                    tooltip _("Use mousewheel to cycle girls' pages.")

                            if next:
                                textbutton "↓" style "UI_button":
                                    xalign 0.0
                                    xsize xres(22)
                                    ysize yres(22)
                                    action (SetLocalVariable("page_offset", page_offset+next), SetLocalVariable("current_page", page_offset+next+1))
                                    text_size res_font(14)
                                    text_font "DejaVuSans.TTF"

            else:
                text _("{i}  No girl available  {/i}") size res_font(18) color c_brown

screen girl_pick_badge(girl):

    modal True
    key "mouseup_3" action Return()

    use dark_filter()

    frame xalign 0.5 yalign 0.5 xpadding 20 ypadding 20:
        has vbox

        text _("Choose a badge for [girl.fullname]") color c_darkorange

        text ""

        vpgrid xalign 0.5:
            cols 3
            spacing 5
            draggable True
            mousewheel True
            allow_underfull True

            for i in range(len(badge_pics)):
                button xsize yres(80) ysize yres(80):
                    if i == 0:
                        action (SetField(girl, "badge", ""), Return())
                        tooltip _("No badge")
                    else:
                        action (SetField(girl, "badge", badge_pics[i]), Return())
                        tooltip _("Pick this badge")
                    add ProportionalScale(badge_pics[i], *res_tb(60)) xalign 0.5 yalign 0.5

        text _("\nYou can add your own badges in the UI/Badges folder (restart required).") italic True size res_font(12) xalign 0.5 color c_darkorange

screen badge_button(girl, _size, t_size=20, active=True): # Where badge is a file name or ""
    $ badge = girl.get_badge()

    if not badge:
        if active:
            textbutton "+" xmargin 0 ymargin 0 xpadding 0 ypadding 0 background None xalign 0.9 yalign 0.1 text_size res_font(t_size) tooltip _("Add a custom badge to this girl. Custom badges do not do anything, they are for your own convenience."):
                action Return(("badge", girl))
                text_color c_white
                text_drop_shadow (1, 1)

    else:
        $ badge_name = badge.rsplit(".", 1)[0]
        button xmargin 0 ymargin 0 xpadding 0 ypadding 0 background None xalign 0.9 yalign 0.1 tooltip "Current badge: {b}%s{/b}.\nClick to change the custom badge for this girl." % badge_name:
            if active:
                action Return(("badge", girl))
            add ProportionalScale(badge, *res_tb(_size))

screen girl_button(girl, bsize="x4", status_list=[], context="girls", extra_action=None, custom_action=None, hovered_action=None, unhovered_action=None, custom_ttip=None):

    $ sel_col = c_emerald + "CC"
    $ use_badge = False

    # Deactivate hovering if the option is disabled
    if not persistent.hover_for_preview_girls:
        $ hovered_action = NullAction()
        $ unhovered_action = NullAction()

    if context == "girls" or context == "powers":
        if girl.job:
            $ text1 = __(girl.job.capitalize()) # text1 is displayed on the button next to girl name and portrait
            $ but_ttip = __("{b}%s{/b} is a level %s %s.") % (girl.fullname, girl.level, __(girl.job.capitalize()))
        else:
            $ text1 = __("No job")
            $ but_ttip = __("{b}%s{/b} has no job.") % girl.fullname
        $ text_col = job_color[girl.job]
        $ use_badge = True

    elif context == "free":
        $ text1 = __(girl.get_MC_relation()).capitalize()
        if girl.MC_interact:
            $ but_ttip = __("%s is currently at the %s.") % (girl.fullname, girl.location)
        else:
            $ but_ttip = __("You haven't met this girl before.")
        $ text_col = c_white

    elif context == "farm":
        if farm.programs[girl].target != "no training":
            $ text1 = farm.programs[girl].target.capitalize()
            $ but_ttip = __("{b}%s{/b} is training (%s).") % (girl.fullname, text1)
            $ text_col = c_orange
        else:
            $ text1 = farm.programs[girl].holding.capitalize()
            $ but_ttip = __("{b}%s{/b} is being held (%s).") % (girl.fullname, text1)
            $ text_col = c_white
        $ use_badge = True

    elif context == "slavemarket":
        $ text1 = experienced_description[girl.sexual_experience]
        $ text2 = "{image=img_gold}%s" % '{:,}'.format(girl.get_price("buy"))
        $ but_ttip = __("{b}%s{/b}, %s. Click for details.") % (girl.fullname, text2)
        $ text_col = experienced_color[girl.sexual_experience]

    if context == "powers":
        $ text1 += "\n" + girl.get_sanity()

    if custom_ttip:
        $ but_ttip = custom_ttip

    if context not in ("free", "slavemarket"):
        $ but_ttip += __("\nEnergy: %s/%s") % (str_int(girl.energy), str(int(girl.get_stat_minmax("energy")[1])))
        $ but_ttip += girl_status_dict[girl, "summary"]

    if custom_action:
        $ but_action = custom_action
    else:
        $ but_action = [SetVariable("selected_girl", girl), SelectedIf(selected_girl==girl)]

    if extra_action: # extra_action must be a list
        $ but_action += extra_action

    if bsize == "x40":
        button:
            xsize xres(75)
            ysize girl_but_ysize[bsize]
            xalign 0.5
            yalign 0.5
            xpadding xres(3)
            ypadding yres(3)
            xmargin 0
            ymargin yres(3)
            style "girlbutton"
            action but_action
            tooltip but_ttip

            frame background None xsize yres(45) ysize yres(45) xmargin 0 ymargin 0 xpadding 2 yalign 1.0:

                has hbox yalign 0.5 xfill True yfill True

                fixed xalign 0.5 yalign 0.5:
                    add AlphaMask(girl.portrait.get(*res_tb(35)), Frame("GUI/edge_mask.png")) xalign 0.5 yalign 0.5

                    if use_badge:
                        use badge_button(girl, 20, 18, active=persistent.badges_on_portraits)

                # button style "inv_no_padding" action but_action xalign 1.0 yalign 1.0:
                #     if hovered_action:
                #         hovered hovered_action

                #     tooltip __("She has ") + str_int(girl.energy) + __(" energy left out of ") + str(int(girl.get_stat_minmax("energy")[1])) + "."

                vbar value girl.energy range girl.get_stat_minmax("energy")[1] xalign 1.0 yalign 1.0:
                    thumb None
                    thumb_offset 0
                    top_gutter 0
                    left_bar Frame ("resources/ui/cryvslider_empty.webp", 10, 0)
                    right_bar Frame ("resources/ui/cryvslider_scale.webp", 10, 0)
                    xsize xres(6)
                    ysize yres(36)

            text text1[:3] bold True size res_font(11) color text_col drop_shadow (1, 1):
                xalign 0.05
                yalign 0.95

            hbox:
                spacing 3
                xalign 0.05

                hbox spacing 3 xalign 1.0:
                    text _("Rk") size res_font(11)  drop_shadow (1, 1)
                    text rank_name[girl.rank] size res_font(14) bold True drop_shadow (1, 1)
                hbox spacing 3 xalign 1.0:
                    text _("Lv") size res_font(11)  drop_shadow (1, 1)
                    text str(girl.level) size res_font(14) bold True drop_shadow (1, 1)

            frame:
                background None
                xpos xres(70)
                xanchor 1.0
                yalign 1.0
                xmargin 1
                ymargin 2
                ypadding 0

                has vbox spacing 0 ymaximum 50 box_wrap True

                if context == "slavemarket":
                    text text2 size res_font(11) bold True textalign 1.0 xalign 1.0

                else:
                    if len(status_list) > 3:
                        $ i = 2
                    else:
                        $ i = 3

                    for pic, ttip in status_list[:i]:
                        # button style "inv_no_padding":
                        #     # if hovered_action:
                        #     #     hovered hovered_action
                        #     # action but_action
                        #     # tooltip ttip
                        add ProportionalScale("resources/ui/status/" + pic, *res_tb(16))

                    if i == 2:
                        text "..." size res_font(10) bold True xalign 0.5 yoffset -4 # tooltip girl_status_dict[girl, "summary"]

    elif bsize == "x24":
        button:
            xsize xres(100)
            ysize girl_but_ysize[bsize]
            xalign 0.5
            yalign 0.5
            xpadding xres(3)
            ypadding yres(3)
            xmargin 0
            ymargin yres(3)
            style "girlbutton"
            action but_action
            tooltip but_ttip

            if hovered_action:
                hovered hovered_action
            if unhovered_action:
                unhovered unhovered_action

            frame background None xsize yres(70) ysize yres(70) xmargin 0 ymargin 0 xpadding 2 yalign 1.0:
                has hbox yalign 0.5 xfill True yfill True

                fixed xalign 0.5 yalign 0.5 fit_first True:
                    add AlphaMask(girl.portrait.get(*res_tb(55)), Frame("GUI/edge_mask.png")) xalign 0.5 yalign 0.5

                    if use_badge:
                        use badge_button(girl, 25, 20, active=persistent.badges_on_portraits)

                # button style "inv_no_padding" action but_action xalign 1.0 yalign 0.5:
                #     if hovered_action:
                #         hovered hovered_action #! Does not work for girls that have the same exact name. Investigate.
                #     # if unhovered_action:
                #     #     unhovered unhovered_action
                #     tooltip __("She has ") + str_int(girl.energy) + __(" energy left out of ") + str(int(girl.get_stat_minmax("energy")[1])) + "."
                vbar value girl.energy+1 range girl.get_stat_minmax("energy")[1] xalign 1.0 yalign 0.5:
                    thumb None
                    thumb_offset 0
                    top_gutter 0
                    left_bar Frame ("resources/ui/cryvslider_empty.webp", 10, 0)
                    right_bar Frame ("resources/ui/cryvslider_scale.webp", 10, 0)
                    xsize xres(8)
                    ysize yres(42)

            text text1 bold True size res_font(12) color text_col drop_shadow (1, 1):
                xalign 0.05
                yalign 0.95

            hbox:
                spacing 3
                xalign 0.05

                hbox spacing 3 xalign 1.0:
                    text _("Rk") size res_font(12)  drop_shadow (1, 1)
                    text rank_name[girl.rank] size res_font(16) bold True  drop_shadow (1, 1)
                hbox spacing 3 xalign 1.0:
                    text _("Lv") size res_font(12)  drop_shadow (1, 1)
                    text str(girl.level) size res_font(16) bold True  drop_shadow (1, 1)

            frame:
                background None
                xpos xres(90)
                xanchor 1.0
                yalign 1.0
                xmargin 1
                ymargin 2
                ypadding 0

                has vbox spacing 0 ymaximum yres(70) box_wrap True

                if context == "slavemarket":
                    text text2 size res_font(13) bold True textalign 1.0 xalign 1.0

                else:
                    if len(status_list) > 3:
                        $ i = 2
                    else:
                        $ i = 3
                    for pic, ttip in status_list[:i]:
                        # button style "inv_no_padding":
                        #     action but_action
                            # if hovered_action:
                            #     hovered hovered_action
                            # tooltip ttip
                        add ProportionalScale("resources/ui/status/" + pic, *res_tb(20))

                    if i == 2:
                        text "..." size res_font(10) bold True xalign 0.5 yoffset -4 # tooltip girl_status_dict[girl, "summary"]


    elif bsize == "x12":
        button:
            xsize xres(150)
            ysize girl_but_ysize[bsize]
            xalign 0.5
            yalign 0.5
            xpadding xres(6)
            ypadding yres(3)
            xmargin 0
            ymargin yres(3)
            style "girlbutton"
            action but_action
            tooltip but_ttip

            if hovered_action:
                hovered hovered_action
            if unhovered_action:
                unhovered unhovered_action

            frame background None xsize yres(90) ysize yres(90) xmargin 0 ymargin 0 yalign 1.0:
                has hbox spacing 0 yalign 0.5 xfill True yfill True

                fixed xalign 0.5 yalign 0.5 xysize res_tb(75):
                    add AlphaMask(girl.portrait.get(*res_tb(75)), Frame("GUI/edge_mask.png")) xalign 0.5 yalign 0.6

                    if use_badge:
                        use badge_button(girl, 30, 24, active=persistent.badges_on_portraits)

                # button style "inv_no_padding" action but_action yalign 1.0:
                #     if hovered_action:
                #         hovered hovered_action
                #     tooltip __("She has ") + str_int(girl.energy) + __(" energy left out of ") + str(int(girl.get_stat_minmax("energy")[1])) + "."
                vbar value girl.energy range girl.get_stat_minmax("energy")[1] xalign 1.0 yalign 1.0:
                    thumb None
                    thumb_offset 0
                    top_gutter 0
                    left_bar Frame ("resources/ui/cryvslider_empty.webp", 10, 0)
                    right_bar Frame ("resources/ui/cryvslider_scale.webp", 10, 0)
                    xsize xres(10)
                    ysize yres(75)

            if context != "free" or girl.MC_interact:
                if len(girl.fullname) <= 10:
                    $ text3 = girl.fullname
                else:
                    $ text3 = girl.name[0] + ". " + girl.lastname
            else:
                $ text3 = "?"


            text text3 size res_font(16) drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" xalign 0.05:
                if girl.original:
                    color c_yellow

            text text1 bold True size res_font(14) color text_col drop_shadow (1, 1):
                xalign 0.05
                yalign 0.95


            vbox:
                spacing 0
                xalign 0.95
                yalign 0.25

                hbox spacing 3 xalign 1.0:
                    text _("Rk") size res_font(11)
                    text rank_name[girl.rank] size res_font(14) bold True drop_shadow (1, 1)
                hbox spacing 3 xalign 1.0:
                    text _("Lv") size res_font(11)
                    text str(girl.level) size res_font(14) bold True drop_shadow (1, 1)

            frame:
                background None
                xpos xres(140)
                xanchor 1.0
                yalign 1.0
                # xmargin xres(2)
                # ymargin yres(3)
                # xpadding 0
                # ypadding 0

                if context == "slavemarket":
                    text text2 size res_font(14) bold True textalign 1.0 xalign 1.0

                else:
                    hbox spacing 1 box_wrap True xsize xres(50):

                        if len(status_list) > 4:
                            $ i = 3
                        else:
                            $ i = 4

                        for pic, ttip in status_list[:i]:
                            # button style "inv_no_padding":
                            #     action but_action
                                # if hovered_action:
                                #     hovered hovered_action
                                # tooltip ttip
                            add ProportionalScale("resources/ui/status/" + pic, *res_tb(22))

                        if i == 3:
                            text "..." size res_font(11) bold True xalign 0.5 yoffset -4 # tooltip girl_status_dict[girl, "summary"]


    elif bsize == "x4":
        button:
            xsize xres(300)
            ysize girl_but_ysize[bsize]
            xalign 0.5
            yalign 0.5
            xpadding xres(12)
            ypadding yres(12)
            xmargin xres(3)
            ymargin yres(3)
            style "girlbutton"
            action but_action
            tooltip but_ttip

            if hovered_action:
                hovered hovered_action
            if unhovered_action:
                unhovered unhovered_action

            fixed fit_first True:
                hbox xfill True spacing xres(12):
                    frame xsize yres(100) ysize yres(100) ymargin 3 yalign 1.0:
                        fixed fit_first True:
                            add AlphaMask(girl.portrait.get(), Frame("GUI/edge_mask.png")) yalign 0.5 fit "contain"

                        if use_badge:
                            use badge_button(girl, 40, 32, active=persistent.badges_on_portraits)

                        # button style "inv_no_padding" action but_action xalign 1.0 yalign 1.0:
                        #     if hovered_action:
                        #         hovered hovered_action
                        #     tooltip __("She has ") + str_int(girl.energy) + __(" energy left out of ") + str(int(girl.get_stat_minmax("energy")[1])) + "."
                        vbar value girl.energy range girl.get_stat_minmax("energy")[1] xalign 1.0 yalign 1.0:
                            thumb None
                            thumb_offset 0
                            top_gutter 0
                            left_bar Frame ("resources/ui/cryvslider_empty.webp", 10, 0)
                            right_bar Frame ("resources/ui/cryvslider_scale.webp", 10, 0)
                            xsize xres(12)
                            ysize yres(85)

                    vbox xalign 0.0 ypos 0.2 xfill True xsize 0.5:
                        text text1 bold True size res_font(15) color text_col drop_shadow (1, 1) xalign 0.0

                        frame:
                            background None
                            xpadding 0
                            xalign 0.0
                            yalign 1.0
                            ymargin 3

                            has hbox

                            if context == "slavemarket":
                                text text2 size res_font(18) bold True

                            else:
                                if len(status_list) > 5:
                                    $ i = 4
                                else:
                                    $ i = 5

                                for pic, ttip in status_list[:i]:
                                    # button style "inv_no_padding":
                                    #     action but_action
                                        # if hovered_action:
                                        #     hovered hovered_action
                                        # tooltip ttip
                                    add ProportionalScale("resources/ui/status/" + pic, *res_tb(35))

                                if i == 4:
                                    text "..." size res_font(12) bold True xalign 0.5 yoffset -4 # tooltip girl_status_dict[girl, "summary"]

                    vbox:
                        spacing 6
                        xalign 1.0
                        yalign 0.6

                        hbox spacing 6:
                            text _("Rank") size res_font(14)
                            text rank_name[girl.rank] bold True drop_shadow (1, 1)
                        hbox spacing 6:
                            text _("Level") size res_font(14)
                            text str(girl.level) bold True drop_shadow (1, 1)

                if context != "free" or girl.MC_interact:
                    $ text3 = girl.fullname
                else:
                    $ text3 = "?"

                text text3 drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf":
                    if girl.original:
                        color c_yellow

screen girl_fast_actions(girl, notebook=True, love_fear=True, schedule=True, customers=True, bg=None):

    frame:
        xalign 0.5
        ypos 1.0
        yanchor 0.0
        xminimum xres(180)
        xmaximum int(12 + config.screen_width // 2.8) # Makes it the same size as the girl profile pic
        ysize int(config.screen_height*0.0814)
        xmargin 0
        xpadding 6
        ymargin 0
        ypadding 0

        if bg:
            background bg

        has hbox spacing 5 xfill True yfill True

        if schedule:
            button yalign 0.5 xmargin 0 xpadding 3 ymargin 0 ypadding 3 action Return("sched") tooltip __("Open%s's schedule") % girl.fullname:
                at alpha_transform
                add "resources/ui/calendar.webp" zoom 0.4 #idle_alpha 0.66 hover_alpha 1.0
        else:
            null

        if notebook:
            if MC.get_effect("special", "notebook"):
                button action Show("notebook") xmargin 0 xpadding 3 ymargin 0 ypadding 3 yalign 0.5 tooltip __("Open %s's entry in your magical notebook") % girl.fullname:
                    at alpha_transform
                    add "resources/items/misc/magic notebook.webp" zoom 0.4 #idle_alpha 0.5 hover_alpha 1.0
        else:
            null

        if love_fear:
            hbox spacing 3 xsize xres(70) yalign 0.5: # 73
                use love_button(girl)
                use fear_button(girl)
        else:
            null
            null

        if customers and district.rank > 1:
            frame background c_ui_dark xmargin 0 xpadding 0 ymargin 0 ypadding 0 xfill False xalign 1.0 yalign 0.5:
                has hbox spacing 1 box_wrap True xmaximum xres(180) # previously 156
                for pop in all_populations:
                    if brothel.get_effect("allow", pop.name):
                        if girl.refused_populations[pop.name]:
                            $ X_text = "{b}X{/b}"
                            $ ttip = __("Click to allow %s") % pop.description
                        else:
                            $ X_text = ""
                            $ ttip = __("Click to block %s") % pop.description
                        button xsize xres(25) ysize yres(25) xmargin 0 xpadding 0 ymargin 0 ypadding 0 background None yalign 0.5:
                            at alpha_transform
                            action (ToggleDict(girl.refused_populations, pop.name), girl.customer_populations_safety_check(pop.name))
                            tooltip ttip
                            add pop.get_pic(*res_tb(25)) xalign 0.5 yalign 0.5
                            text X_text color c_crimson size res_font(24) xalign 0.5 yalign 0.5


screen button_overlay(girl, context="girls"):

    zorder 5

    if context == "slavemarket":

        frame:

            xalign 0.0
            xmargin 0.1
            xsize 0.3
            xfill True
            ypos 0.14
            background None

            has hbox

            xfill True

            $ text1 = str(girl.get_price('buy')) + " gold"

            text text1 xalign 0.0

            key "noshift_K_y" action Return(girl)

            textbutton _("Bu{u}y{/u}") xsize xres(60) text_size res_font(22) xalign 1.0 action Return(girl) tooltip __("Click to buy %s for %s") % (girl.fullname, text1)

    elif context == "girls":

        key "noshift_K_j" action (SetVariable("selected_girl", girl), Return("assign"))


        if not (girls_firstvisit or girl.away): # Interaction menu can still be accessed when MC interactions=0 (to listen to her story again, for instance)
            key "noshift_K_i" action (SetVariable("selected_girl", girl), Return("interact"))
            key "noshift_K_t" action (SetVariable("selected_girl", girl), Return("equip"))
            if girl.free:
                key "K_BACKSPACE" action (SetVariable("selected_girl", girl), Return("dismiss"))
            else:
                key "K_BACKSPACE" action (SetVariable("selected_girl", girl), Return("sell"))

        frame:

            background None

            xalign 0.0
            yalign 0.2
            xmargin 6
            xpadding 3
            ypadding 6
            xsize xres(320)
            yfill False

            has hbox

            spacing 1
            box_wrap True


            if girl.away:
                $ text1 = "Away"
                $ ttip = __("She is away on a class or assignment for %s more day%s.") % (girl.return_date - calendar.time, plural(girl.return_date - calendar.time))

            elif girl.hurt > 0:
                $ text1 = "Hurt"
                if girl.hurt <= 1:
                    $ ttip = __("This girl is hurt and will need to rest for 1 more day until she is ready to do anything.")
                else:
                    $ ttip = __("This girl is hurt and will need to rest for %s more days until she is ready to do anything.") % str(round_int(girl.hurt))

            elif girl.exhausted:
                $ text1 = "Tired"
                $ ttip = __("This girl needs to be fully rested until she can work again.")

            elif girl.resting and girl.job:
                $ text1 = "Resting"
                $ ttip = __("This girl has been set to rest today according with her schedule.")

            elif not girl.job:
                $ text1 = "No {u}j{/u}ob"
                $ ttip = __("No job assigned. This girl has been set to rest until further instructions.")

            elif girl.work_whore:
                $ text1 = __(girl.job.capitalize())[:4] + "./Wh."
                $ ttip = __("Working and whoring. Change this girl's job or let her rest.")

            else:
                $ text1 = __(girl.job.capitalize())
                $ ttip = __("Change this girl's job or let her rest.")

            textbutton text1 style "small_button" action (SetVariable("selected_girl", girl), Return("assign")) tooltip __("%s ({i}shortcut: {u}j{/u}{/i})") % ttip selected False

            $ sched = girl.workdays[calendar.get_weekday()]

            if sched == 0:
                $ text1 = "Resting"
            elif sched == 50:
                $ text1 = "Half-Shift"
            elif sched == 100:
                $ text1 = "Full shift"

            if not girls_firstvisit:
                key "noshift_K_d" action Return("sched")

            textbutton _("Sche{u}d{/u}ule") style "small_button":
                tooltip "{i}Current schedule: %s{/i}.\nClick to open %s's schedule." % (text1, girl.fullname)
                if not girls_firstvisit:
                    action Return("sched") selected False

            button:
                style "inv_no_padding"

                textbutton _("{u}I{/u}nteract"):
                    selected False
                    style "small_button"
                    hovered tt.Action(_("Interact with your girl. Costs actions."))

                    if MC.interactions > 0 and not (girls_firstvisit or girl.away):
                        action (SetVariable("selected_girl", girl), Return("interact"))

                if not (girls_firstvisit or girl.away):
                    action (SetVariable("selected_girl", girl), Return("interact"))
                else:
                    action NullAction()

                if MC.interactions <= 0:
                    tooltip _("You cannot take any more actions today.")

                elif girl.away:
                    tooltip "You cannot interact with %s as she is away." % girl.name

            textbutton _("I{u}t{/u}ems"):
                selected False
                style "small_button"

                if not girls_firstvisit: # Available for away girls to avoid complications in the Equipment screen

                    action (SetVariable("selected_girl", girl), Return("equip"))

                    tooltip __("Change this girl's equipment.")

                # else:
                #     tooltip "[girl.fullname] is away on a class or assignment."

            if girl.free:
                textbutton _("Dismiss"):
                    selected False
                    style "small_button"
                    if not (girls_firstvisit or girl.away):
                        action (SetVariable("selected_girl", girl), Return("dismiss"))
                    tooltip "Release this free girl from your custody. ({i}shortcut: {u}Backspace{/u}{/i})"

            else:
                textbutton _("Sell"):
                    selected False
                    style "small_button"
                    if not (girls_firstvisit or girl.away):
                        action (SetVariable("selected_girl", girl), Return("sell"))
                    tooltip __("Sell this slave girl for %s gold (original cost: %s gold). ({i}shortcut: {u}Backspace{/u}{/i})") % (str(girl.get_price("sell")), girl.original_price)


            if girl.upgrade_points >= 1 or girl.can_perk:
                key "noshift_K_u" action (SetVariable("selected_girl", girl), Return("level_or_perks"))
                key "noshift_K_k" action (SetVariable("selected_girl", girl), Return("perks"))
                textbutton _("Level {u}u{/u}p") style "small_button":
                    action (SetVariable("selected_girl", girl), Return("level_or_perks"))
                    alternate (SetVariable("selected_girl", girl), Return("perks"))
                    tooltip (__("You have %s perk points to spend.\nRight-click to access perks.") % str_int(girl.perk_points))
                    hovered Show("perk_details", girl=girl)
                    unhovered Hide("perk_details")

            else:
                if not girls_firstvisit:
                    key "noshift_K_k" action (SetVariable("selected_girl", girl), Return("perks"))

                textbutton _("Per{u}k{/u}s"):
                    selected False
                    style "small_button"
                    if not girls_firstvisit:
                        action (SetVariable("selected_girl", girl), Return("perks"))
                    tooltip _("Check her current perks")
                    hovered Show("perk_details", girl=girl)
                    unhovered Hide("perk_details")



            if girl.ready_to_rank():
                key "noshift_K_r" action (SetVariable("selected_girl", girl), Return("rank"))
                textbutton _("{u}R{/u}ank up") style "small_button" action (SetVariable("selected_girl", girl), Return("rank"))

            if not girls_firstvisit:
                key "noshift_K_a" action (SetVariable("selected_girl", girl), Return("stats"))

                textbutton _("St{u}a{/u}ts"):
                    style "small_button"
                    selected False
                    action (SetVariable("selected_girl", girl), Return("stats"))
                    tooltip _("Click here for useful stats about your girl.")

            if debug_mode:
                textbutton _("Pics") style "small_button" action (SetVariable("selected_girl", girl), Return("debug_pics")) text_size res_font(14) tooltip _("Test girl pack with the game's picture generation.") selected False

    elif context == "free":

        frame:

            xalign 0.0
            xmargin 0.1
            xsize 0.3
            xfill True
            ypos 0.15
            background None

            has hbox

            xfill True

            if girl.MC_relationship_level <= 1:
                $ text1 = event_color["a little bad"] % "Acquaintance"
            elif girl.MC_relationship_level == 1:
                $ text1 = event_color["average"] % "Friend"
            elif girl.MC_relationship_level == 2:
                $ text1 = event_color["a little good"] % "Love interest"
            elif girl.MC_relationship_level == 3:
                $ text1 = event_color["good"] % "Girlfriend"
            elif girl.MC_relationship_level >= 4:
                $ text1 = event_color["special"] % "Lover"

            text (_("Current relationship: %s") % text1)

    elif context == "farm":

        frame:

            background None

            xalign 0.0
            yalign 0.19
            xmargin 6
            xpadding 3
            ypadding 6
            xsize xres(320)
            yfill False

            has hbox

            spacing 1
            box_wrap True

#            textbutton "Change program" text_size res_font(14) action Return(("change program", girl)) hovered tt.Action("Change " + girl.name + "'s current training program.")

            key "noshift_K_t" action Return(("equip", girl))
            key "noshift_K_a" action Return(("take out", girl))
            if girl.free:
                key "K_BACKSPACE" action Return(("dismiss", girl))
            else:
                key "K_BACKSPACE" action Return(("sell", girl))

            if story_flags["farm shows"] == True:
                textbutton _("{u}F{/u}arm show (%i%%)") % girl.get_build_up() text_size res_font(14):
                    if girl.get_build_up() >= 100:
                        action Return(("show", girl))
                    else:
                        action NullAction()
                        style "insensitive_button"
                        xpadding xres(12)
                    tooltip _("Builds-up as she trains on the farm. After reaching 100%, you can organize a farm show with this girl. You may raise this up to 200% to get additional bonuses.")

            textbutton _("I{u}t{/u}ems"):
                text_size res_font(14)
                if not girls_firstvisit:
                    action Return(("equip", girl))

                tooltip _("Change this girl's equipment.")

            textbutton _("Le{u}a{/u}ve farm") text_size res_font(14) action Return(("take out", girl)) tooltip __("Send %s back to the brothel.") % girl.name

            if girl.free:
                textbutton _("Dismiss"):
                    text_size res_font(14)
                    action Return(("dismiss", girl))
                    tooltip "Release this girl from your custody. ({i}shortcut: {u}Backspace{/u}{/i})"
            else:
                textbutton _("Sell"):
                    text_size res_font(14)
                    if not girls_firstvisit and not girl.broken:
                        action Return(("sell", girl))
                    tooltip __("Sell this girl for %s gold (original cost: %s gold). ({i}shortcut: {u}Backspace{/u}{/i})") % (str(girl.get_price("sell")), girl.original_price)

screen rank_level_details(girl):

    modal False

    frame:

        xpadding 10

        xfill False

        xalign 0.5
        yalign 0.5
        ypadding 25
        ymargin 10
        background c_ui_darkblue

        has vbox
        xalign .5
        yalign .5
        spacing 25

        text girl.fullname:
            xalign 0.5
            color c_orange

        grid 2 2:

            spacing 10

            vbox:
                text __("RANK") size res_font(12)

                $ text1 = rank_name[girl.rank]

                if girl.rank == district.rank:
                    $ text1 += " {size=12} (max){/size}"

                text text1 color c_softpurple

            vbox:
                text __("LEVEL") size res_font(12)
                text str(girl.level) + " {size=12} / " + str(girl.rank * 5) + "{/size}" color c_lightgreen

            vbox:
                text __("REPUTATION") size res_font(12)
                text str(int(girl.rep)) + " {size=12}/ " + str(int(girl.get_rep_cap())) + "{/size}" color c_softpurple

            vbox:
                text __("EXPERIENCE") size res_font(12)
                text str(int(girl.xp)) + " {size=12}/ " + str(girl.get_xp_cap()) + "{/size}" color c_lightgreen



        grid 3 10:

            text __("SKILLS") size res_font(12)

            text "" size res_font(12)

            text _("JP") size res_font(12)

            for job in all_jobs:

                text __(job.capitalize()) yalign 0.5
                $ star_text = ""
                for i in range(girl.job_level[job]):
                    $ star_text += "{image=img_star}"

                text star_text yalign 0.5

                text str(int(girl.jp[job])) + " {size=12}/ " + str(girl.get_jp_cap(job)) + "{/size}" yalign 0.5 color c_orange

            null height yres(3)
            null height yres(3)
            null height yres(3)

            for job in ("service", "sex", "anal", "fetish"):

                text __(job.capitalize()) yalign 0.5
                $ star_text = ""
                for i in range(girl.job_level[job]):
                    $ star_text += "{image=img_star}"

                text star_text yalign 0.5

                text str(round_int(girl.jp[job])) + " {size=12}/ " + str(girl.get_jp_cap(job)) + "{/size}" yalign 0.5 color c_orange


