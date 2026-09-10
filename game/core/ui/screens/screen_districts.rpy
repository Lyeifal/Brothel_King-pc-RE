#### Screen Districts — Districts, locations and matchmaking | 城区/地点/配对界面 ####
# Phase 2: 城区/地点/配对/顾客满意度
# Contains: screen districts, screen district_button, screen visit_district, screen visit_location, screen matchmaking, screen customer_satisfaction
# Extracted from ui/screens.rpy on 2026-09-10

screen districts(context = "visit"): # returns a chosen district. Context can be "first visit", "visit" or "relocate"

    zorder 0

    if context == "visit":
        key "mouseup_3" action ((Hide("districts"), Hide("tool"), Jump("main")))
        use shortcuts()

    $ i = 1
    for dis in all_districts:
        if dis.chapter <= game.chapter:
            key str(i) action Return(dis)
            $ i += 1

    # BK Evolution: Build column groups from ui_layout
    python:
        _ui = active_world_map.ui_layout if active_world_map else {}
        _col_map = {}
        for _did, _dinfo in _ui.items():
            _c = _dinfo.get("column", 0)
            if _c not in _col_map:
                _col_map[_c] = []
            _col_map[_c].append((_dinfo.get("row", 0), _did))
        _max_col = max(_col_map.keys()) if _col_map else 3
        _col_count = _max_col + 1
        # Sort each column by row
        for _c in _col_map:
            _col_map[_c].sort(key=lambda x: x[0])

    frame:
        background "bg zan"
        xysize (config.screen_width, int(config.screen_height*0.8))
        xfill True
        yfill True

        has hbox

        xalign 0.5
        yalign 0.5

        # Column 0: special handling for The Hunt / No license required
        vbox:
            xsize int(config.screen_width * 0.25)
            yalign 0.5
            ysize yres(400)
            yfill True

            if suzume_hints_active and context == "visit":
                frame background c_ui_dark xpadding 6 ypadding 6 xalign 0.35:
                    vbox:
                        text _("The Hunt") size res_font(14) xalign 0.5 yalign 0.5
                        button xsize yres(120) ysize yres(120) xpadding 6 ypadding 6:
                            if MC.interactions >= 1:
                                action Call("c3_interrogate_contacts")
                            tooltip "Talk to Suzume to {b}talk to your contacts{/b} and discover {b}hints{/b} about the Kunoichi you are hunting."
                            has vbox
                            xalign 0.5
                            # text "Inquire" size res_font(14) xalign 0.5 yalign 0.5
                            add "side suzume" xalign 0.5 yalign 0.5 fit "contain"

            else:
                text _("No license\nrequired") xalign 0.5 yalign 0.0 size res_font(14) text_align 0.5 color c_darkgrey

            if 0 in _col_map:
                for _row, _did in _col_map[0]:
                    if _did in district_dict:
                        use district_button(district_dict[_did], context)

        # Dynamic columns 1..N
        for _c in range(1, _col_count):
            vbox:
                yalign 0.5
                spacing 60
                xsize int(config.screen_width * 0.25)
                ysize yres(400)
                yfill True

                # License header: computed from max chapter in this column
                $ _col_districts = [district_dict[_did] for _row, _did in _col_map.get(_c, []) if _did in district_dict]
                $ _max_ch = max([d.chapter for d in _col_districts] + [1])
                $ _lic_idx = min(_max_ch // 2, 3)

                hbox:
                    xalign 0.5
                    spacing 10

                    if game.chapter >= _max_ch:
                        add ProportionalScale("resources/ui/" + license_dict[_lic_idx][1], *res_tb(50)) xalign 0.5
                    else:
                        add ProportionalScale("resources/ui/" + license_dict[0][1], *res_tb(50)) xalign 0.5

                    if _lic_idx > 0:
                        text __("%s\nrequired") % license_dict[_lic_idx][0] xalign 0.5 yalign 0.0 size res_font(14) text_align 0.5 color c_darkgrey
                    else:
                        text _("No license\nrequired") xalign 0.5 yalign 0.0 size res_font(14) text_align 0.5 color c_darkgrey

                if _c in _col_map:
                    for _row, _did in _col_map[_c]:
                        if _did in district_dict:
                            use district_button(district_dict[_did], context)

    if context != "first visit":
        use overlay("districts")

    if context == "visit":
        use close((Hide("districts"), Hide("tool"), Jump("main")))

screen district_button(dis, context):

    button:
        xalign 0.5
        ycenter 0.5
        xpadding xres(9)
        ypadding yres(9)
        at alpha_transform

        if game.chapter >= dis.chapter:
            if context != "relocate":
                action Return(dis)
                tooltip (_("Visit %s (press %s to visit this district).") % (__(dis.name), str(all_districts.index(dis) + 1)))
            elif dis not in game.blocked_districts and district != dis:
                action Return(dis)
                tooltip (_("Choose %s to relocate your brothel.") % __(dis.name))
        vbox:

            spacing 10

            text __(dis.name) size res_font(14) xalign 0.5 yalign 0.5

            fixed:
                fit_first True

                add dis.get_pic(xres(150), yres(100)) # alpha 0.66 insensitive_alpha 0.33 hover_alpha 1.0

                $ max_love = 0

                for loc in location_dict[dis.name]:
                    for girl in loc.girls:
                        if girl.love > max_love:
                            $ max_love = girl.love

                if max_love > 0:

                    $ h = 1 + max_love // 2

                    add ProportionalScale("resources/ui/heart.webp", h, 50) xalign 0.5 yalign 0.4 # idle_alpha 0.66 hover_alpha 0.8

                text str(all_districts.index(dis) + 1) size res_font(14) xalign 0.05 yalign 0.95

                if district == dis:
                    button xsize yres(45) ysize yres(45) xalign 0.95 yalign 0.05:
                        action NullAction()
                        tooltip("This is where {b}%s{/b} is currently located." % brothel.name)
                        idle_background Frame("resources/ui/brothelnavbutton_idle.webp")
                        insensitive_background Frame("resources/ui/brothelnavbutton_idle.webp")
                        hover_background Frame("resources/ui/brothelnavbutton_hover.webp")

screen visit_district():

    zorder 0

    key "mouseup_3" action (SetVariable("selected_destination", "districts"), Jump("teleport"))
    use close((SetVariable("selected_destination", "districts"), Jump("teleport")))
    use shortcuts()

    $ available_districts = [d for d in all_districts if d.chapter <= game.chapter]

    key "K_LEFT" action (SetVariable('selected_district', get_previous(available_districts, selected_district, loop=True)), Jump("visit_district"))
    key "K_RIGHT" action (SetVariable('selected_district', get_next(available_districts, selected_district, loop=True)), Jump("visit_district"))

    if len(available_districts) > 1:
        textbutton "<" xalign 0.05 ysize yres(120) yalign 0.4 action (SetVariable('selected_district', get_previous(available_districts, selected_district, loop=True)), Jump("visit_district")) tooltip _("Visit the previous district (you can use arrow keys).")

        textbutton ">" xalign 0.95 ysize yres(120) yalign 0.4 action (SetVariable('selected_district', get_next(available_districts, selected_district, loop=True)), Jump("visit_district")) tooltip _("Visit the next district (you can use arrow keys).")

    $ i = 1
    for loc in location_dict[selected_district.name]:
        key str(i) action Return([loc, "go"])

        # Shortcut added by Lokplart
        if loc.can_do_action():
            key "alt_K_" + str(i) action Return([loc, "special"])

        $ i += 1

    fixed:
        xysize (config.screen_width, int(config.screen_height*0.8))
        xfill True
        yfill True

        vbox focus None:

            xalign 0.5
            yalign 0.5

            text __(selected_district.name) xalign 0.5

            text ""
            text ""

            grid 3 2:

                spacing 50

                for location in location_dict[selected_district.name]:

                    button focus None:
                        xalign 0.5
                        yalign 0.33
                        xpadding xres(9)
                        ypadding yres(9)
                        at alpha_transform

                        action Return([location, "go"])

                        if location.secret:
                            tooltip _("You have not discovered this location yet.")
                        else:
                            tooltip __("{b}%s{/b}. Press %s to visit this location.") % (location.name, str(location_dict[selected_district.name].index(location) + 1))

                        vbox:

                            spacing 10

                            if location.secret:

                                text "???" size res_font(14) xalign 0.5

                                add im.Scale("resources/districts/locations/secret.webp", xres(150), yres(100)) # insensitive_alpha 0.33 idle_alpha 0.66 hover_alpha 1.0

                            else:
                                text location.name size res_font(14) xalign 0.5

                                fixed:
                                    fit_first True
                                    add location.get_pic(xres(150), yres(100)) # insensitive_alpha 0.33 alpha 0.66 hover_alpha 1.0

                                    $ max_love = 0

                                    for girl in location.girls:
                                        if girl.love > max_love:
                                            $ max_love = girl.love

                                    if max_love > 0:

                                        $ h = 1 + max_love // 2

                                        add ProportionalScale("resources/ui/heart.webp", h, 50) xalign 0.5 yalign 0.4 # insensitive_alpha 0.33 idle_alpha 0.66 hover_alpha 0.8

                                    if location.action:
                                        button xsize xres(60) ysize yres(60) xpos xres(105) ypos yres(45) background None xmargin yres(5) ymargin yres(5) xpadding yres(5) ypadding yres(5) focus None:
                                            at alpha_transform
                                            if location.can_do_action() and location.menu[1] in location_tb.keys():
                                                add location_tb[location.menu[1]] fit "contain" # insensitive_alpha 0.33 alpha 0.66 hover_alpha 1.0
                                            elif location.menu[1] in location_tb.keys():
                                                add location_tb[location.menu[1]] + " grey" fit "contain" # insensitive_alpha 0.33 alpha 0.66 hover_alpha 1.0

                                            if location.menu_costs_AP and MC.interactions < 1:
                                                action NullAction()
                                                tooltip __("%s. You cannot collect as you are out of AP.") % location.menu[0]
                                            else:
                                                action Return([location, "special"])
                                                if location.menu_costs_AP:
                                                    tooltip __("%s. Costs 1 {image=img_AP}.") % location.menu[0]
                                                else:
                                                    tooltip __(location.menu[0]) + "."

                                    text str(location_dict[selected_district.name].index(location) + 1) size res_font(14)  xalign 0.05 yalign 0.95

    use overlay("visit_district")
    use close((Hide("visit_district"), Jump("districts")))

screen visit_location():

    zorder 0

    key "mouseup_3" action (SetVariable("selected_destination", "visit_district"), Jump("teleport"))
    use close((SetVariable("selected_destination", "visit_district"), Jump("teleport")))
    use shortcuts()

    # Note: won't work if two locations are secret next to each other (shouldn't happen)

    $ _previous = get_previous(location_dict[selected_district.name], selected_location, loop=True)
    if _previous.secret:
        $ _previous = get_previous(location_dict[selected_district.name], _previous, loop=True)
    $ _next = get_next(location_dict[selected_district.name], selected_location, loop=True)
    if _next.secret:
        $ _next = get_next(location_dict[selected_district.name], _next, loop=True)

    key "K_LEFT" action (SetVariable('selected_location', _previous), Jump("visit_location"))
    key "K_RIGHT" action (SetVariable('selected_location', _next), Jump("visit_location"))

    textbutton "<" xalign 0.05 ysize yres(120) yalign 0.4 action (SetVariable('selected_location', _previous), Jump("visit_location")) tooltip _("Visit the previous location in this district (you can use arrow keys).")

    textbutton ">" xalign 0.95 ysize yres(120) yalign 0.4 action (SetVariable('selected_location', _next), Jump("visit_location")) tooltip _("Visit the next location in this district (you can use arrow keys).")

    frame:
        background None # loc.get_pic(config.screen_width, int(config.screen_height*0.8))
        xysize (config.screen_width, int(config.screen_height*0.8))
        xfill True
        yfill True

        has vbox
        xalign 0.5
        yalign 0.7
#        yfill True

        text selected_location.name xalign 0.5

        text ""
        text ""

        hbox xalign 0.5 ysize yres(280):

            spacing xres(30)

            for girl in selected_location.girls:

                button:
                    xalign 0.5
                    yalign 0.33
                    xpadding xres(18)
                    ypadding yres(18)
                    action Return(girl)
                    at alpha_transform

                    if girl.MC_interact:
                        tooltip __("Talk to %s.") % girl.fullname
                    else:
                        tooltip _("Talk to this unknown girl. Costs 1 {image=img_AP}.")

                    vbox:

                        spacing yres(3)

                        if girl.MC_interact:
                            text girl.fullname size res_font(14) align 0.5, 0.5:
                                if girl.original:
                                    color c_yellow
                        else:
                            text "?" size res_font(14) align 0.5, 0.5

                        fixed:
                            fit_first True
                            xmaximum xres(240)
                            ymaximum yres(240)
                            xfill False
                            yfill False

                            add AlphaMask(girl.profile.get(*res_tb(240)), Frame("GUI/edge_mask.png")) xalign 0.5 # insensitive_alpha 0.33 idle_alpha 0.8 hover_alpha 1.0
                            # add girl.profile.get(*res_tb(240)) xalign 0.5 insensitive_alpha 0.33 idle_alpha 0.8 hover_alpha 1.0

                            if girl.love >= 5:

                                $ h = 5 + girl.love // 2

                                add ProportionalScale("resources/ui/heart.webp", *res_tb(h)) xalign 0.97 yalign 0.03 # idle_alpha 0.66 hover_alpha 0.8

                            if persistent.show_girlpack_rating in ("In market and city", "Everywhere"):

                                $ rating, ttip = get_girlpack_rating(girl)

                                textbutton _("Girl rating (%s): %s") % (capitalize(girl.path.split("/")[-1]), rating) background c_ui_darkblue text_size res_font(18) yalign 1.0 xmargin 10 ymargin 10 action NullAction() tooltip ttip

        text ""
        text ""

        hbox:
            spacing 25
            xalign 0.5

            button:
                xsize xres(240)
                ysize yres(50)

                if MC.interactions > 0:
                    action Return("visit")
                    tooltip _("Explore this location. Costs 1 {image=img_AP}.")

                hbox xalign 0.5 yalign 0.5:
                    text _("Take a look around (1 ") size res_font(18)
                    text "{image=img_AP}" xalign 0.0 yalign 0.5
                    text ")" xalign 0.0 yalign 1.0 size res_font(18)

            if selected_location.action:
                button xsize xres(240) ysize yres(50) xpadding xres(18):
                    at alpha_transform
                    if selected_location.can_do_action():
                        action Return("special")
                        if selected_location.menu_costs_AP:
                            tooltip __("%s. Costs 1 {image=img_AP}.") % selected_location.menu[0]
                        else:
                            tooltip __("%s (free).") % selected_location.menu[0]
                    hbox yalign 0.5 xfill True:
                        if selected_location.can_do_action() and selected_location.menu[1] in location_tb.keys():
                            add location_tb[selected_location.menu[1]] fit "contain" # insensitive_alpha 0.33 idle_alpha 0.66 hover_alpha 1.0
                        elif selected_location.menu[1] in location_tb.keys():
                            add location_tb[selected_location.menu[1]] + " grey" fit "contain" # insensitive_alpha 0.33 idle_alpha 0.66 hover_alpha 1.0

                        hbox spacing xres(10) xalign 0.0 yalign 0.5 box_wrap True:
                            text selected_location.menu[0] size res_font(18)
                            if selected_location.menu_costs_AP:
                                text _("(1 {image=img_AP})") yalign 1.0 size res_font(16)

            if story_flags["ninja hunt"] and not story_flags["ninja hunt locked %s" % selected_district.name] and story_flags["ninja hunt"] != calendar.time and not story_flags["ninja hunt hide " + selected_location.name] and selected_district.rank <= 2:
                textbutton _("Hunt ninjas") text_size res_font(18) xsize xres(240) ysize yres(50):

                    if MC.interactions > 0:
                        action Return("hunt")
                    tooltip _("Hunt for ninjas dwelling in this location.")

    use overlay("visit_location")
    use close((Hide("visit_location"), Jump("visit_district")))



## BROTHEL SCREEN ##

# screen brothel + furniture + brothel_options → EXTRACTED to ui/screens/screen_brothel.rpy (Phase 3.1)
# 青楼/家具/选项界面已提取到 screen_brothel.rpy

screen matchmaking(girls, customers, match_list, context="job"): # Where match list is a list of tuples (girl, customer)

    tag show_screen

    key "mouseup_1" action Return()
    key "mouseup_3" action Return()
    if persistent.can_skip_reports:
        key ['K_LCTRL', 'K_RCTRL', 'repeat_K_LCTRL', 'repeat_K_RCTRL'] action Return()
    use close(Return(), "next")

    default t = 0
    default n = 0
    default idle_customers = sorted(customers, key=lambda x: x.rank)
    default girl_customers = defaultdict(list)
    default job_customers = defaultdict(int)
    default cust_act = defaultdict(str)
    default load_txt = " (matching...)"

    if match_list:
        $ tick = min(1.5 / len(match_list), 0.2) # Takes maximum 1.5 seconds to display all customer matches

    frame background c_ui_dark:
        xalign 0.0
        yalign 0.05
        xsize int(0.95*config.screen_width)
        ysize yres(615)
        left_margin 6
        ymargin 2
        xfill True
        yfill True

        has vbox spacing 10

        if context == "job":
            $ text1 = "Entertainment Phase"
        else:
            $ text1 = "Whoring Phase"

        text "[text1!t]" + load_txt xalign 0.0 bold True drop_shadow (2, 2) #color c_prune

        frame xfill True ymaximum yres(160) right_margin 10:
            has hbox spacing 20
            add brothel.get_pic(*res_tb(100))

            vbox spacing 6:
                text __("Waiting customers ({image=img_cust} %i)/%i") % (len(idle_customers), len(customers)) size res_font(18) color c_brown

                if customers:
                    vpgrid rows 4 spacing 3 ymaximum yres(160):
                        mousewheel True
                        draggable True
                        scrollbars "horizontal"
                        allow_underfull True

                        if not idle_customers:
                            text _("All customers have been assigned.") size res_font(12) italic True yalign 0.5 color c_brown
                        else:
                            for cust in idle_customers:
                                button yalign 0.5 xmargin 0 xpadding 0 ymargin 0 ypadding 0 background None action NullAction() tooltip cust.get_description("idle " + context):
                                    if cust.crazy:
                                        add cust.get_pic(*res_tb(25)) at red_saturate
                                        at blink
                                    else:
                                        add cust.get_pic(*res_tb(25))

                else:
                    text _("No customers.") size res_font(12) italic True yalign 0.5 color c_brown



        viewport:
            mousewheel True # "change"
            draggable False
            scrollbars "vertical"
            yfill True

            if context == "job":

                vbox spacing 10:
                    for job in all_jobs:
                        $ room = brothel.rooms[job_room_dict[job]]

                        if room.level > 0:
                            frame xfill True yfill False:
    #                             has vbox spacing 3

                                hbox spacing 20:
                                    add room.get_pic(*res_tb(100))

                                    vbox spacing 6:
                                        text __("%s ({image=img_cust} %i/%i)") % (room.name.capitalize(), job_customers[job], room.cust_limit) size res_font(18) color c_brown

                                        vbox spacing 3:
                                            for girl in [g for g in girls if g.job == job]:
                                                hbox ysize yres(25) yalign 0.5:
                                                    button xmargin 0 xpadding 0 ymargin 0 ypadding 0 xsize xres(45) yalign 0.5 background None action NullAction() tooltip  __("{b}%s: %s (capacity: %s/%s).{/b}") % (girl.fullname, __(girl.job.capitalize()), len(girl_customers[girl]), girl.get_max_cust_served()):
                                                        add girl.portrait.get(*res_tb(25)) xalign 0.5 yalign 0.5

                                                    frame ysize yres(25) ymargin 0 ypadding 1 background c_ui_brown xfill True:
                                                        has hbox spacing 3 yalign 0.5
                                                        for cust in girl_customers[girl]:
                                                            button xmargin 0 xpadding 0 ymargin 0 ypadding 0 background None action NullAction() tooltip cust.get_description(job): #  xalign 0.0 yalign 0.5 yanchor 0.5
                                                                if cust.crazy:
                                                                    add cust.get_pic(*res_tb(22)) at red_saturate
                                                                    at blink
                                                                else:
                                                                    add cust.get_pic(*res_tb(22))
                                                        if not girl_customers[girl]:
                                                            text _("No customers.") size res_font(12) italic True yalign 0.5

            elif context == "whore":
                frame xfill True yfill False:
                    has vbox spacing 3
                    $ room = brothel.bedroom_type

                    text __("Bedrooms ({image=img_cust} %i)") % job_customers["whore"] size res_font(18) color c_brown
                    hbox spacing 20:
                        add room.get_pic(*res_tb(100))

                        vbox spacing 3 box_wrap True:
                            for girl in girls:
                                hbox ysize yres(25) yalign 0.5:
                                    button xmargin 0 xpadding 0 ymargin 0 ypadding 0 xsize xres(45) yalign 0.5 background None action NullAction() tooltip __("{b}%s: %s (interactions: %s/%s).{/b}") % (girl.fullname, __(girl.job.capitalize()), girl.get_max_interactions()-girl.interactions, girl.get_max_interactions()):
                                        add girl.portrait.get(*res_tb(25)) yalign 0.5

                                    frame ysize yres(25) ymargin 0 ypadding 1 background c_ui_brown xfill True xmaximum xres(220):
                                        has hbox spacing 3 yalign 0.5
                                        for cust in girl_customers[girl]:
                                            button xmargin 0 xpadding 0 ymargin 0 ypadding 0 background None action NullAction() tooltip cust.get_description(cust.got_sex_act): #  xalign 0.0 yalign 0.5 yanchor 0.5
                                                if cust.crazy:
                                                    add cust.get_pic(*res_tb(22)) at red_saturate
                                                    at blink
                                                else:
                                                    add cust.get_pic(*res_tb(22))
                                        if not girl_customers[girl]:
                                            text _("No customers.") size res_font(12) italic True yalign 0.5

    if match_list and len(match_list) > n:
        timer 0.05 repeat True action SetScreenVariable("t", t + 0.05)

        if t >= 0.3 + (tick * n):
            $ girl, cust, act = match_list[n]
            if cust in idle_customers:
                $ idle_customers.remove(cust)
            $ girl_customers[girl].append(cust)
            if act in all_sex_acts:
                $ job_customers["whore"] += 1
            else:
                $ job_customers[girl.job] += 1
            $ cust_act[cust] = act
            $ n += 1

            $ renpy.play(s_click, "sound")
    else:
        $ load_txt = __(" (done)")

screen customer_satisfaction(customers, old_rep, rep_chg):

    tag show_screen

    zorder 5

    default t = 0
    default displayed_rep = round_int(old_rep)
    default total_change = 0
    default displayed_customers = []

    key "mouseup_1" action Return()
    key "mouseup_3" action Return()
    if persistent.can_skip_reports:
        key ['K_LCTRL', 'K_RCTRL', 'repeat_K_LCTRL', 'repeat_K_RCTRL'] action Return()
    use close(Return(), "next")

    if persistent.dark_night_UI:
        $ tcolor = c_white
    else:
        $ tcolor = c_brown

    frame:
        xalign 0.0
        yalign 0.0
        xsize int(0.95*config.screen_width)
        ysize yres(615)
        left_margin 6
        ymargin 2
        if persistent.dark_night_UI:
            background c_ui_darker

        has vbox spacing 10

        $ text1 = __("Brothel reputation: %s") % displayed_rep

        if len(displayed_customers) == len(customers):
            $ text1 += " (%s)" % plus_text(total_change)
        else:
            timer 0.05 repeat True action SetScreenVariable("t", t + 0.05)

        # text text1 xalign 1.0 bold True color c_prune

        text "[text1!t]" xalign 0.0 bold True drop_shadow (2, 2)

        hbox spacing 10:
            textbutton __("Customer") style "inv_no_padding" xsize xres(80) text_bold True text_color tcolor text_size res_font(14)
            textbutton __("Satisfaction") style "inv_no_padding" xsize xres(100) text_bold True text_color tcolor text_size res_font(14)
            textbutton __("Rep.") style "inv_no_padding" xsize xres(100) text_bold True text_color tcolor text_size res_font(14)
            textbutton __("Comment") style "inv_no_padding" xsize xres(100) text_bold True text_color tcolor text_size res_font(14)

        viewport:
            mousewheel "change"
            draggable True
            scrollbars True
            xfill True
            yfill True

            vbox spacing 3:

                for cust in displayed_customers:
                    hbox spacing 10:
                        button xsize xres(80) xalign 0.5 xmargin 0 xpadding 0 ymargin 0 ypadding 0 background None action NullAction() tooltip cust.get_description("end"): #  xalign 0.0 yalign 0.5 yanchor 0.5
                            add cust.get_pic(*res_tb(25)) xalign 0.5

                        $ chg = cust.reputation_change

                        if chg > 0:
                            $ col = c_emerald
                        elif chg < 0:
                            $ col = c_crimson
                        else:
                            $ col = None

                        fixed fit_first True ypos -0.2 xsize xres(100):
                            bar xsize xres(100) value cust.base_rating range 8 thumb None ypos 0.4: # AnimatedValue(value=cust.base_rating, range=8, delay=1.0) Animated value doesn't work :/
                                if col: # Updated method as suggested by Dexell
                                    # left_bar Frame(im.Twocolor("resources/ui/cryslider_full.webp", col, col), 12, 0)
                                    # right_bar Frame(im.Twocolor("resources/ui/cryslider_empty.webp", col, col), 12, 0)
                                    left_bar Frame(Transform("resources/ui/cryslider_full.webp", matrixcolor = ColorizeMatrix(col, col)), 12, 0)
                                    right_bar Frame(Transform("resources/ui/cryslider_empty.webp", matrixcolor = ColorizeMatrix(col, col)), 12, 0)

                            text _("I") color c_brown size res_font(20) xpos xres(3) + (cust.rank-1)*xres(95/8) ypos 0.5

                        textbutton plus_text(chg) xsize xres(80) xalign 0.5 yalign 0.65 text_size res_font(14) text_color c_brown text_bold True

                        frame ysize yres(20) yalign 0.5 ymargin 0 ypadding 1 xsize xres(600):
                            if persistent.dark_night_UI:
                                background None
                            else:
                                background c_ui_brown
                            text _("[cust.reputation_comment!t]") size res_font(14):
                                if persistent.dark_night_UI:
                                    color c_softpurple
                                else:
                                    color c_brown

    if t > 0.3 and len(displayed_customers) < len(customers):
        $ idx = min(int(len(customers) * (t - 0.3)), len(customers)) # Takes 1 second to display all customers
        if idx > 0:
            $ displayed_customers = customers[:idx]
            $ total_change = round_int(sum(c.reputation_change for c in displayed_customers))
            $ displayed_rep = min(max(round_int(old_rep + total_change), 0), brothel.max_rep)


## RIGHT MENU : this is the main menu on the main screen (not named main menu to avoid confusion with the standard Renpy screen)
