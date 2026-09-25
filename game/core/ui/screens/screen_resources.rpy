#### Screen Resources — Resources, achievements and contracts | 资源/成就/契约界面 ####
# Phase 2: 资源/成就/契约
# Contains: screen resource_tab, screen resource_gain, screen resource_exchange, screen achievement_notification, screen crystal_display, screen achievements, screen contracts, screen contract_tab, screen pick_girl, screen contract_result, screen increment_counter, screen increment_display, screen auction_brothel, screen goal_ttip
# Extracted from ui/screens.rpy on 2026-09-10

screen resource_tab(rlist="MC", sz = yres(15), sp = 3, x=0.0, y=0.0, bg=None, font_sz=res_font(12)): # If provided, rlist must be a list of tuples (resource_name, number)

    if rlist == "MC":
        frame background bg xpadding sp ypadding sp xpos x ypos y xanchor 0.5 yanchor 0.5:
            has hbox spacing sp//2 xalign 0 box_wrap True

            for resource in [resource_dict[r] for r in build_resources]:

                if MC.resources[resource.name]>0:
                    button background None action NullAction() tooltip __("%s You have %s %s in store.") % (resource.description, str(MC.resources[resource.name]), resource.name) xpadding sp ypadding sp:
                        has hbox spacing sp*2 yalign 0.5
                        add resource.pic.get(sz, sz) yalign 0.5
                        if MC.resources[resource.name] < 100:
                            text str(MC.resources[resource.name]) size font_sz yalign 0.5
                        else:
                            text "99+" size font_sz - res_font(2) yalign 0.5
    else:
        frame background bg xpadding sp ypadding sp xalign x yalign y:
            has hbox xalign 0 box_wrap True

            for resource, nb in rlist:
                button background None action NullAction() xpadding sp*2 ypadding sp*2:
                    has hbox box_wrap True spacing sp*2
                    add resource_dict[resource].pic.get(sz, sz) yalign 0.5
                    text str(nb) size res_font(14) yalign 0.5:
                        if MC.has_resource(resource, nb):
                            color c_emerald
                        else:
                            color c_red

screen resource_gain(resource, number): # Where resource is a string

    tag resource_gain

    zorder 10

    button style "girlbutton_blue":
        xalign 0.5
        yalign 0.5
        xsize 0.6
        ysize 0.5
        xpadding 50

        has hbox
        xalign 0.5
        yalign 0.5
        spacing 25

        add resource_dict[resource].get_pic(*res_tb(100))
        text "+" + str(round_int(number)) + " " + __(resource) size res_font(28) yalign 0.5

screen resource_exchange():

    tag exchange

    default source = None
    default target = None
    default source_name = None
    default target_name = None
    default source_nb = 0
    default target_nb = 0
    default t = 0

    use shortcuts()
    use overlay()
    use close(Return("quit"))

    key "mouseup_3" action Return("quit")

#    timer 0.5 repeat True action SetScreenVariable("t", int(100*renpy.random.random())/10.0)

    fixed ypos 0.1 xfill True yfill True:

    # Weekly deals

        frame xsize xres(250) yanchor 1.0 ypos 0.2:
            has vbox
            text _("Weekly trade information") size res_font(14) italic True color c_brown
            hbox spacing 3 box_wrap True:
                for r in calendar.scarce:
                    $ resource = resource_dict[r]
                    if resource.rank <= story_flags["builder license"]:
                        button background None action NullAction() tooltip __("There is a shortage of %s this week. Value is going up.") % __(r.capitalize()):
                            has hbox spacing 3
                            add resource.pic.get(*res_tb(20)) yalign 0.5
                            text "▲" size res_font(16) color c_emerald yalign 0.5 font "DejaVuSans.TTF"

                for r in calendar.discounted:
                    $ resource = resource_dict[r]
                    if resource.rank <= story_flags["builder license"]:
                        button background None action NullAction() tooltip __("%s is plentiful this week. Value is going down.") % __(r.capitalize()):
                            has hbox spacing 3
                            add resource.pic.get(*res_tb(20)) yalign 0.5
                            text "▼" size res_font(16) color c_red yalign 0.5 font "DejaVuSans.TTF"


    # Left frame

        frame xsize xres(250) ypos 0.2:
            has vbox

#            text(str(t))

            text _("Your resources") size res_font(14) italic True color c_brown

            button xfill True ysize yres(60) action (SetScreenVariable("source", "gold"), SetScreenVariable("source_name", "gold"), SetScreenVariable("source_nb", 0), SelectedIf(source=="gold")) tooltip _("Use your gold to buy resources"):
                selected_background c_emerald
                has hbox xfill True yfill True spacing 10
                add ProportionalScale("resources/ui/coin.webp", *res_tb(40)) yalign 0.5
                hbox spacing 6 xfill True yalign 0.5:
                    text _("Gold") size res_font(18)
                    text '{:,}'.format(round_int(MC.gold)) xalign 1.0 size res_font(16)


            for r in build_resources:
                $ resource = resource_dict[r]

                if resource.rank <= story_flags["builder license"]:

                    button xfill True ysize yres(60) action (SetScreenVariable("source", resource), SetScreenVariable("source_name", resource.name), SetScreenVariable("source_nb", 0), SelectedIf(source==resource)) tooltip __("Trade your %s for other resources") % r:
                        selected_background c_emerald
                        has hbox xfill True yfill True spacing 10
                        add resource.pic.get(*res_tb(40)) yalign 0.5
                        vbox xfill True spacing 6 yalign 0.5:
                            hbox spacing 3:
                                text __(resource.name.capitalize()) size res_font(18)
                                if r in calendar.discounted:
                                    text "▼" size res_font(14) yalign 0.5 font "DejaVuSans.TTF"
                                elif r in calendar.scarce:
                                    text "▲" size res_font(14) yalign 0.5 font "DejaVuSans.TTF"
                            hbox spacing 6 xfill True:
                                text _("In storage: ") size res_font(14) yalign 1.0
                                text str(MC.resources[resource.name]) xalign 1.0 size res_font(16)

        # Right frame

        if source:

            frame xsize xres(250) xalign 1.0 ypos 0.2:
                has vbox

                text _("Market resources") size res_font(14) italic True color c_brown

                button xfill True ysize yres(60):
                    if "gold" != source:
                        action (SetScreenVariable("target", "gold"), SetScreenVariable("target_name", "gold"), SetScreenVariable("target_nb", 0), SelectedIf("gold"==target))
                        tooltip __("Sell your %s for gold") % source_name
                        selected_background c_emerald

                    hbox xfill True yfill True spacing 10:
                        add ProportionalScale("resources/ui/coin.webp", *res_tb(40)) yalign 0.5
                        vbox xfill True spacing 6 yalign 0.5:
                            text _("Gold") size res_font(18)
                            if "gold" != source:
                                hbox spacing 6:
                                    $ rate = get_exchange_rate(source, "gold")
                                    if rate < 1:
                                        $ text2 = __("Get 1 for %s") % str_dec(1/rate, 1)
                                    else:
                                        $ text2 = __("Get %s for 1") % str_dec(rate, 1)

                                    text text2 size res_font(14)
                                    add source.pic.get(*res_tb(16))

                for r in build_resources:
                    $ resource = resource_dict[r]

                    if resource.rank <= story_flags["builder license"]:

                        button xfill True ysize yres(60):
                            if resource != source:
                                action (SetScreenVariable("target", resource), SetScreenVariable("target_name", resource.name), SetScreenVariable("target_nb", 0), SelectedIf(resource==target))
                                tooltip __("Trade %s in exchange for your %s") % (r, source_name)
                                selected_background c_emerald
                            hbox xfill True yfill True spacing 10:
                                add resource.pic.get(*res_tb(40)) yalign 0.5
                                vbox xfill True spacing 6 yalign 0.5:
                                    hbox spacing 3:
                                        text __(resource.name.capitalize()) size res_font(18)
                                        if r in calendar.discounted:
                                            text "▼" size res_font(14) yalign 0.5 font "DejaVuSans.TTF"
                                        elif r in calendar.scarce:
                                            text "▲" size res_font(14) yalign 0.5 font "DejaVuSans.TTF"
                                    if resource != source:
                                        hbox spacing 6:
                                            $ rate = get_exchange_rate(source, resource)
                                            if rate < 1:
                                                $ text2 = __("Get 1 for %s") % str(round_up(1/rate))
                                            else:
                                                $ text2 = __("Get %s for 1") % str(round_up(rate))

                                            text text2 size res_font(14)
                                            if source == "gold":
                                                add ProportionalScale("resources/ui/coin.webp", *res_tb(16))
                                            else:
                                                add source.pic.get(*res_tb(16))

    # Middle window

    if source and target and (source != target):

        $ rate = get_exchange_rate(source, target)

        if source_nb == 0 or target_nb == 0:
            if rate < 1:
                $ source_nb = round_up(1/rate)
                $ target_nb = 1

            elif rate >= 1:
                $ source_nb = 1
                $ target_nb = round_up(rate)

        frame xalign 0.5 yalign 0.6 xsize xres(400) xpadding 20 ypadding 20 background c_ui_dark:

            has vbox xfill True

            hbox xfill True spacing 6 ysize yres(70):
                if source != "gold":
                    add source.pic.get(*res_tb(60))
                else:
                    add ProportionalScale("resources/ui/coin.webp", *res_tb(65))

                text _("[source_nb]") size res_font(32) xalign 0.0 yalign 0.5:
                    if source == "gold":
                        if MC.gold >= source_nb:
                            color c_white
                        else:
                            color c_red
                    elif MC.resources[source_name] >= source_nb:
                        color c_white
                    else:
                        color c_red


                text "➜" size 54 xalign 0.5 yalign 0.5 font "DejaVuSans.TTF"

                text _("[target_nb]") size res_font(32) color c_white xalign 1.0 yalign 0.5

                if target != "gold":
                    add target.pic.get(*res_tb(60)) xalign 1.0
                else:
                    add ProportionalScale("resources/ui/coin.webp", *res_tb(65)) xalign 1.0


            hbox xfill True:
                textbutton "-" xsize xres(65) ysize yres(65) text_size res_font(32):
                    if rate < 1 and target_nb > 1:
                        action (SetScreenVariable("target_nb", target_nb-1), SetScreenVariable("source_nb", round_up((target_nb-1)/rate)))
                    elif rate >= 1 and source_nb > 1:
                        action (SetScreenVariable("source_nb", source_nb-1), SetScreenVariable("target_nb", round_up((source_nb-1)*rate)))

                if source == "gold":
                    $ text1 = __("Buy")
                else:
                    $ text1 = __("Trade")

                textbutton text1 xalign 0.5 xsize 0.8 ysize yres(65):
                    if source == "gold" and MC.gold >= source_nb:
                        action Return(("gold", target_name, source_nb, target_nb))
                        tooltip __("Buy %s %s for %s %s") % (str(target_nb), target_name, str(source_nb), target_name)
                    elif MC.resources[source_name] >= source_nb:
                        action Return((source_name, target_name, source_nb, target_nb))
                        tooltip __("Trade %s %s for %s %s") % (str(source_nb), source_name, str(target_nb), target_name)

                textbutton "+" xsize xres(65) ysize yres(65) text_size res_font(32) xalign 1.0:
                    if rate < 1:
                        action (SetScreenVariable("target_nb", target_nb+1), SetScreenVariable("source_nb", round_up((target_nb+1)/rate)))
                    elif rate >= 1:
                        action (SetScreenVariable("source_nb", source_nb+1), SetScreenVariable("target_nb", round_up((source_nb+1)*rate)))


screen achievement_notification(achievement_list, replay=False):

    zorder 20

    vbox xalign 0.5 yalign 0.5 spacing 10:
        at fadeinout
        for achievement in achievement_list:
            if replay:
                $ achv, level = achievement # Unpacking tuple
            else:
                $ achv, level = (achievement, None)

            frame xsize xres(320) ysize yres(150) xpadding 10 ypadding 10 background c_lightorange:

                has hbox yfill True spacing 12
                frame xalign 0.5 yalign 0.5:
                    if achv.pic:
                        add achv.pic.get(*res_tb(100))
                    else:
                        text _("Not found") italic True color c_red

                vbox yalign 0.5:
                    hbox spacing xres(6) ysize yres(24):
                        text achv.get_title(force_level=level) xalign 0.0 size res_font(20) bold True color c_prune # font "resources/fonts/VIVALDII.TTF"
                        null width xres(10)
                        if persistent.new_game_plus:
                            use crystal_display(achv.multi, sz = 18)
                    text achv.get_description(force_level=level) xalign 0.0 size res_font(20) font "resources/fonts/VIVALDII.TTF" color c_brown
    timer 6.5 action Hide("achievement_notification")

screen crystal_display(v, sz=24, prefix=" x "):

    hbox yalign 0.5 ysize yres(sz):
        add "misc" fit "contain" yalign 0.0
        text "{color=#fff}%s{/color}%s" % (prefix, str(v)) size res_font(sz) color c_purple yalign 1.0 bold True font "resources/fonts/DejaVuSans.ttf"

screen achievements(main=False):

    tag menu

    default confirm_reset = False
    default total_crystals = count_achievements()

    key "mouseup_3":
        if main:
            action ShowMenu("galleries")
        else:
            action Return()

    vbox:
        fixed ysize yres(160):
            frame xfill True xpadding xres(10) ypadding xres(10) background c_lightorange:
                if selected_achievement:
                    hbox yfill True spacing 12:
                        frame xalign 0.5 yalign 0.5:
                            add selected_achievement.pic.get(*res_tb(125))

                        vbox xsize xres(500) yalign 0.5:
                            if persistent.new_game_plus:
                                use crystal_display(selected_achievement.multi)
                            text selected_achievement.get_title() xalign 0.0 size res_font(20) bold True color c_prune
                            text selected_achievement.get_description() xalign 0.0 size res_font(20) font "resources/fonts/VIVALDII.TTF" color c_brown

                        if selected_achievement.level < selected_achievement.level_nb:
                            vbox yalign 0.5:
                                text _("Next unlock:") italic True size res_font(20)
                                text selected_achievement.get_description(_next=True) xalign 0.0 size res_font(20) font "resources/fonts/VIVALDII.TTF" color c_brown

            vbox xalign 1.0 yalign 0.0:
                hbox:
                    if persistent.new_game_plus:
                        use crystal_display(total_crystals)
                        null width xres(10)
                    if not confirm_reset:
                        textbutton _("Reset achievements") text_size res_font(14) ysize yres(36) xalign 0.2 yalign 1.0:
                            action SetScreenVariable("confirm_reset", True)
                    else:
                        textbutton (_("Reset achievements (%s)") % (event_color["bad"] % _("CONFIRM"))) text_size res_font(14) ysize yres(36) xalign 0.0 yalign 0.0:
                            action (Function(reset_achievements), SetScreenVariable("confirm_reset", False))

                    textbutton _("Back")  ysize yres(36):
                        if main:
                            action ShowMenu("galleries")
                        else:
                            action Return()

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            xfill True

            frame xfill True background c_ui_darkblue:
                hbox:
                    xalign 0.5
                    spacing xres(6)
                    box_wrap True

                    for achv in achievement_list:
                        if achv.level > 0:
                            textbutton achv.get_title(_button=True) xsize xres(150) ysize yres(50) text_size res_font(12) action NullAction() hovered [SetVariable("selected_achievement", achv), SelectedIf(selected_achievement==achv)]
                        else:
                            textbutton "???" xsize xres(150) ysize yres(50)

                # if len(achievement_list) % 6 > 0:
                #     for _ in range(6 - len(achievement_list) % 6):
                #         null


screen contracts(contracts, free=False):

    modal True

    frame xalign 0.5 yalign 0.5 xpadding(xres(20)):
        has vbox

        text _("Choose a contract") xalign 0.5 yalign 0.5 color c_brown

        text "" size res_font(14)

        hbox:
            for con in contracts:
                vbox:
                    # if not free:
                    hbox xalign 0.5 spacing xres(20):
                        frame background Frame("darkorange_button") xfill False yfill False xpadding xres(12):
                            text (_("Fee: %s gold.") % str(con.base_value)) size res_font(14) color c_white bold True
                        if MC.gold < con.base_value:
                            text _(" Not enough gold.") color c_red italic True size res_font(14) yalign 0.5
                    button idle_background Frame("lightgrey_button") hover_background Frame("lightorange_button") xpadding 6 ypadding 6:
                        if MC.gold >= con.base_value:
                            action Return(con)
                        use contract_tab(con)

        text "" size res_font(14)

        textbutton _("Skip") action Return("back") xalign 0.5 yalign 0.5

screen contract_tab(contract, x=320, active=False):

    modal True
    if active:
        use dark_filter()
        key "mouseup_3" action Return()
        use close(Return(), "back")

    frame xalign 0.5 yalign 0.5 xsize xres(x) ysize yres(600) xpadding 10 ypadding 10:
        if not active:
            background None
        viewport:
            mousewheel True
            draggable False
            scrollbars "vertical"

            has vbox spacing 12

            vbox spacing 3:
                text (_("The %s") % __(contract.location.name)) drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" color c_brown
                text contract.title drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" color c_prune

            vbox spacing 3:
                add contract.location.get_pic(xres(200), yres(140)) insensitive_alpha 0.33 idle_alpha 0.66 hover_alpha 1.0

                text contract.description size res_font(12) color c_brown

            # text "" size res_font(14)

            vbox spacing 6:
                text _("Tasks") size res_font(16) bold True color c_prune

                for tsk in contract.tasks:
                    vbox spacing 3 xpos 0.02:
                        text tsk.title size res_font(13) bold True color c_prune
                        for req in tsk.get_requirements():
                            text req size res_font(13) color c_brown

            vbox spacing 3:
                text _("Bonus requirement") size res_font(16) bold True color c_prune
                text contract.get_special_description() size res_font(13) color c_brown

            hbox:
                text _("Reward: ") size res_font(16) bold True color c_prune
                text (_("%s gold") % str(contract.get_value())) size res_font(16) bold True color c_darkgold

screen pick_girl(girls, nb, contract=None):
    hbox spacing 20:
        use girl_stats(selected_girl, "postings")

        vbox:
            if contract:
                use contract_tab(contract, x=400)
            use girl_select(girls, True)
            textbutton _("Send") action Return(selected_girl) xalign 0.85 ypos -0.25

screen contract_result(contract, x=450):

    default t = 0
    default earned_gold = contract.get_value()
    default displayed_gold = 0

    frame xalign 0.5 yalign 0.5 xsize xres(x) xpadding 10 ypadding 10:
        has vbox spacing 12

        vbox spacing 3:
            text (_("The %s") % __(contract.location.name)) drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" color c_brown
            text contract.title drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" color c_prune

        vbox spacing 3:
            add contract.location.get_pic(xres(200), yres(140)) insensitive_alpha 0.33 idle_alpha 0.66 hover_alpha 1.0

            text contract.description size res_font(12) color c_brown

        # text "" size res_font(14)

        vbox spacing 9:
            text _("Tasks") size res_font(16) bold True color c_prune

            for tsk in contract.tasks:
                hbox:
                    vbox xsize xres(320) spacing 3:
                        text tsk.title size res_font(13) bold True color c_prune
                        for req in tsk.get_requirements():
                            text req size res_font(13) color c_brown xpos 0.02
                    if t >= contract.tasks.index(tsk) + 1:
                        if tsk.result:
                            text __("%s gold") % str_int(tsk.value) color c_darkgold yalign 0.5 size res_font(13) at contract_result_transform
                        else:
                            text _("{color=[c_red]}{i}Failed{/i}{/color}") yalign 0.5 size res_font(13) at contract_result_transform

        hbox:
            vbox xsize xres(320) spacing 3:
                text _("Bonus requirement") size res_font(16) bold True color c_prune
                text contract.get_special_description() size res_font(13) color c_brown
            if t >= len(contract.tasks) + 1:
                if contract.special_bonus != 1.0:
                    text __("%s gold") % str(contract.get_special_value()) color c_darkgold yalign 0.5 size res_font(13) at contract_result_transform
                else:
                    text _("{i}Missing{/i}") color c_lightred yalign 0.5 size res_font(13) at contract_result_transform

        vbox spacing 6:
            text _("Score") size res_font(16) bold True color c_prune
            hbox:
                text ""
                for i in [tsk for tsk in contract.tasks if tsk.result]:
                    if t >= contract.tasks.index(i) + 1:
                        text "{image=img_star}" at contract_result_transform
                if t >= len(contract.tasks) + 1 and contract.special_bonus > 1.0:
                    text "{image=img_star}" at contract_result_transform

        hbox:
            text _("Reward: ") size res_font(16) bold True color c_prune

            text (_("%s gold") % min(displayed_gold, earned_gold)) size res_font(16) bold True:
                if earned_gold > 0:
                    color c_darkgold
                else:
                    color c_red

        textbutton _("OK") action Return() xalign 0.5

    if t < len(contract.tasks) + 1:
        timer 0.8 action [SetScreenVariable("t", t + 1), Play("sound",s_spell)] repeat True

    if displayed_gold < earned_gold:
        timer 0.1 action [SetScreenVariable("displayed_gold", round_up((1 - 0.15) * displayed_gold + 0.15 * earned_gold)), Play("sound2",s_gold)] repeat True

screen increment_counter(startv = 0, stopv = 1000, duration = 3.0, _caption = __("%s gold"), _background = None, _size = 16, _color = c_white, _sound=s_gold): # Displays an incremental counter counting from startv to stopv

    default displayv = startv

    frame align (0.5, 0.5) background _background:
        has vbox
        text _caption % '{:,}'.format(displayv) color _color size res_font(_size) bold True

    if stopv > startv and displayv < stopv:
        timer 0.01 action [SetLocalVariable("displayv", displayv + round_up(max(1, min(displayv, stopv-displayv))/duration/10)), Play("sound2", _sound)] repeat True
    else:
        null # Needed to avoid graphical glitch

    if stopv < startv and displayv > stopv:
        timer 0.01 action [SetLocalVariable("displayv", displayv - round_up(max(1, min(displayv, startv-displayv))/duration/10)), Play("sound2", _sound)] repeat True
    else:
        null

screen increment_display(title="", _caption=__("%s gold"), pic=None, side_pic=None, startv = 0, stopv = 1000, duration=3.0, _size = 16, _color = c_white, _sound=s_gold):

    modal True

    key "mouseup_3" action (Hide(), Return())

    frame xsize 0.33 align (0.5, 0.5) background c_ui_darkblue:
        has vbox spacing yres(10)

        text title xalign 0.5

        if pic:
            fixed xalign 0.5 xfill True fit_first True:
                add pic yalign 0.5 fit "contain"

        if side_pic:
            hbox:
                fixed xsize yres(120) ysize yres(120):
                    add side_pic yalign 0.5 fit "contain"
                use increment_counter(startv = startv, stopv = stopv, duration = duration, _caption = _caption, _size = _size, _color = _color, _sound=_sound) #? Incomplete

        textbutton _("OK") xalign 0.5 action (Hide(), Return())

screen auction_brothel(name, pic, price):

    # modal True

    tag brothel_auction

    zorder 10

    button:
        xalign 0.5
        yalign 0.5
        xpadding 20
        ypadding 20
        xsize 0.3
        ysize 0.4

        has vbox
        xalign 0.5
        yalign 0.5
        spacing 20

        add pic xalign 0.0 fit "contain"
        use increment_counter(0, price, _caption = __("Sold %s for {b}%s{/b} {image=img_gold}") % (name, '{:,}'.format(price)), _color = c_emerald)
        # text __("Sold %s for {b}%s{/b} {image=img_gold}") % (name, '{:,}'.format(price)) color c_emerald size res_font(16) xalign 0.5 yalign 0.5

screen goal_ttip():

    frame xalign 0.5 yalign 0.5 xsize 0.5 xpadding xres(20) ypadding yres(20) background c_ui_darkblue:
        has vbox spacing yres(10) xfill True
        text (_("{image=tb goal} Chapter %i - Your Goals") % game.chapter) size res_font(28) color c_white bold True xalign 0.5
        text "" size res_font(14)

        for channel in game.get_goal_channels():
            vbox:
                hbox spacing xres(10):
                    add goal_tb[channel]
                    text goal_categories[channel] size res_font(18) bold True color goal_colors[goal_categories[channel]] yalign 0.5
                    if game.get_blocking_goals(channel):
                        add "img_lock" xsize xres(20) ysize yres(30) yalign 0.5
                text game.get_goal_description(channel) size res_font(18) color c_white

        hbox xalign 0.5 spacing xres(10):
            add "img_lock" xsize xres(14) ysize yres(21) yalign 0.5
            text _("You must complete this to advance to the next chapter.") yalign 0.5 size res_font(14)
