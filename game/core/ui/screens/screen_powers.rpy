#### Screen Powers — Evil powers, cards and ranking | 邪恶力量/卡牌/排名界面 ####
# Phase 2: 邪恶力量/卡牌/排名
# Contains: screen mojo_bar, screen power_detail, screen power_draw, screen power_hand, screen power_card, screen power_card_content, screen power_target, screen girl_vp_selector, screen mojo_payment, screen mojo_trade, screen micro_transac, screen brothel_ranking, screen scroll_list, screen brothel_ranking_button, screen harem_button
# Extracted from ui/screens.rpy on 2026-09-10

screen mojo_bar():

    zorder 10

    use adv_tooltip()


    hbox xalign 0.5 spacing xres(30) ypos 0.02:
        for mcolor, mpoints in MC.mojo.items():
            hbox spacing xres(6):
                imagebutton:
                    idle "mojo_" + mcolor
                    action NullAction()
                    tooltip persistent.help_dict[mcolor + " mojo"]
                text (_("%i") % int(mpoints)) bold True size res_font(16) yalign 0.5


## Cards

# Card detail (right side of screen)

screen power_detail(pow):

    frame xalign 1.0 xsize 0.2 ypos 0.1 xmargin xres(6) top_padding yres(6) bottom_padding yres(12) background c_ui_dark:
        vbox spacing yres(3):

            add pow.pic.get() xalign 0.5

            text pow.name + {True : " (S)", False : ""}[pow.super] size res_font(24) bold True
            text pow.description size res_font(14)

            text _("Mojo cost:") size res_font(18) bold True
            hbox spacing xres(6):
                if conduit:
                    $ mod = conduit.get_effect("change", "mojo cost")
                else:
                    $ mod = 0
                for mcolor, mcost in pow.get_mojo_cost():
                    if mcost != 0:
                        fixed fit_first True:
                            add "resources/ui/Powers/orb_[mcolor].webp" size (40, 40)
                            text (_("%i") % (mcost + mod)) bold True size res_font(20) outlines [(1, "#000", 0, 0)] at truecenter:
                                if mod:
                                    color c_green

            text _("Sanity cost:") size res_font(18) bold True
            hbox spacing xres(3):
                add "resources/ui/Powers/sanity_cost_[pow.sanity_lvl].webp" zoom 1.2
                text _("[pow.sanity_lvl]") size res_font(14) yalign 0.4

            text _("Target:") size res_font(18) bold True
            $ target = pow.target.capitalize()
            text target.capitalize() size res_font(14)

            if pow.duration:
                text _("Duration:") size res_font(18) bold True
                text _("[pow.duration] days") size res_font(14)


# Card deck

screen power_draw(x=0.505, y=0.425): # Check if deck can be drawn must happen before the screen is shown

    key "mouseup_3" action Return("back")
    use close(Return("back"))

    button style "inv_no_padding" xsize yres(200) ysize yres(200) align (x, y):
        action (Return("draw"), Hide())

        text _("Draw a card") color c_white drop_shadow (2, 2) align (0.5, 0.5) at blink(_duration=0.5, _pause=0.5)

# Card hand

screen power_hand(hand, context="idle", start_at = 0, x=0.5, y=0.75):

    use shortcuts()

    default selected_card = None
    default _super = False
    default _super_on = [SelectedIf(True), ToggleScreenVariable("_super")]
    default _super_off = [SelectedIf(False), ToggleScreenVariable("_super"), Return("supercharge")]

    if _super:
        key "keydown_K_LSHIFT" action _super_on
        key "keydown_K_RSHIFT" action _super_on
        key "keyup_K_LSHIFT" action _super_off
        key "keyup_K_RSHIFT" action _super_off
    else:
        key "keydown_K_LSHIFT" action _super_off
        key "keydown_K_RSHIFT" action _super_off
        key "keyup_K_LSHIFT" action _super_on
        key "keyup_K_RSHIFT" action _super_on

    key "mouseup_3" action Return("back")
    use close(Return("back"))

    $ card_space = (evil_card_size*1.15)/config.screen_width

    if not hand:
        text _("You have used all of your powers this week.") xalign 0.5 yalign 0.45 drop_shadow (1, 1) at blink

    for i in range(len(hand)):
        $ xc = x + (card_space * i) - card_space * len(hand)/2 + card_space/2
        $ pow = hand[i].get(_super)

        # Using conditions instead of a transform to avoid blur when zooming
        if pow == selected_card:
            $ size_boost = 1.15
        else:
            $ size_boost = 1.0

        if i >= start_at: # Only newly drawn cards will be flipped
            use power_card(pow, context, xc, y, size_boost)
        else:
            use power_card(pow, context, xc, y, size_boost, existing=True)

    if hand and context == "idle":
        button pos (0.675, 0.4) xsize yres(45) ysize yres(45) style "push_button":
            if _super:
                # at jitter
                action _super_on
                tooltip _("Click or hold shift to deactivate supercharge (boost powers for more mojo and sanity)")
                add "supercharge_card" xsize yres(40) ysize yres(40) xalign 0.5 yalign 0.5
            else:
                action _super_off
                tooltip _("Click or hold shift to activate supercharge (boost powers for more mojo and sanity)")
            text _("S") size res_font(28) bold True xalign 0.5 yalign 0.5:
                if not _super:
                    color c_brown

    # Card detail (right side of screen)
    if selected_card:
        use power_detail(selected_card.get(_super))

screen power_card(pow, context = "idle", x = 0, y = 0, size_boost=1.0, existing=False):

    sensitive False

    $ xs = int(evil_card_size * size_boost)
    $ ys = int(xs * 1.6)

    if context == "move":
        frame style "inv_no_padding" xanchor 0.5 yanchor 1.0 at move_to(start_pos = (0.5, 0.45), new_pos = (x, y), fades=1.0):
            if existing: # Previously drawn cards show face up
                use power_card_content
            else:
                add "resources/ui/Powers/cards/back.webp" size (xs, ys) perspective True

    elif context == "flip" and not existing: # Only newly drawn cards will be flipped
        frame style "inv_no_padding" xanchor 0.5 yanchor 1.0 xpos x ypos y:
            fixed fit_first True at flip_to_back:
                # Front face
                fixed fit_first True at reverse_horizontal:
                    use power_card_content
                # Back face
                fixed fit_first True at disappear_in(0.4):
                    add "resources/ui/Powers/cards/back.webp" size (xs, ys) perspective True

    elif context == "burn":
        frame style "inv_no_padding" xanchor 0.5 yanchor 1.0 xpos x ypos y:
            fixed xsize xs ysize ys:
                fixed at disappear_in(0.8):
                    use power_card_content
                add burn_card(xs, ys)

    else:
        button style "inv_no_padding":
            xanchor 0.5 yanchor 1.0 xpos x ypos y
            hovered SetScreenVariable("selected_card", pow)
            unhovered SetScreenVariable("selected_card", None)
            action (SetScreenVariable("selected_card", pow), Return(pow), Hide())
            use power_card_content

screen power_card_content:

    zorder 0

    if pow.type == "Platinum":
        $ col = evpower_color["platinum"][pow.super]
    else:
        $ col = evpower_color["regular"][pow.super]

    fixed fit_first True xysize (xs, ys):
        if pow.super:
            add "resources/ui/Powers/cards/front_[pow.type]_super.webp" perspective False fit "contain"
        else:
            add "resources/ui/Powers/cards/front_[pow.type].webp" perspective False fit "contain"

        vbox xsize 0.98 xalign 0.5 spacing 0:

            # Display card art
            add pow.pic.get() fit "contain" #xoffset 1 yoffset 6

            # Display sanity cost (per level basis)
            add "resources/ui/Powers/sanity_cost_[pow.sanity_lvl].webp" zoom size_boost - 0.15 xalign 0.5 yoffset -yres(16)

        if pow.super:
            add "supercharge_card" size (xs, ys) perspective False alpha 0.65

        frame xfill True xpadding int(xs/25) ypadding int(ys/25) ysize 0.33 xalign 0.5 yalign 1.0 background None:
            has vbox spacing yres(2) xfill True yfill True
            # Display name and short description
            text pow.name bold True color col xalign 0.5 yalign 0.0 size res_font(1+int(9 * size_boost)) text_align 0.5
            text pow.short_description color col xalign 0.5 yalign 0.0 size res_font(1+int(7 * size_boost)) text_align 0.5

        vbox align (0.05, 0.05) spacing yres(3):
            for mcolor, mcost in pow.get_mojo_cost():
                if mcost > 0:
                    fixed fit_first True:
                        add "mojo_[mcolor]" size res_tb(20)
                        text _("[mcost]") size res_font(12) outlines [(1, "#000", 0, 0)] at truecenter

        if pow.duration:
            hbox align (0.95, 0.05):
                add "resources/ui/Powers/timer_duration.webp" size res_tb(20)
                text str(pow.duration) size res_font(12) xalign 0.5 yalign 0.75 outlines [(1, "#000", 0, 0)]


# conduit and target selection

screen power_target(pow):

    modal True
    zorder 0

    key "mouseup_3" action [Return("back"), Hide()]

    default selected_conduit = None
    default selected_target = None
    default _selected = None
    default blocked = []
    default block_dict = {}

    if pow.target == "city girl" and _selected in game.free_girls:
        use girl_stats(_selected, context="free")
    else:
        use girl_stats(_selected, context="powers")
    use power_detail(pow)

    if selected_target and (selected_target == selected_conduit): # Cannot select the same target as conduit
        $ selected_target = None

    frame background c_ui_dark xpadding yres(25) ypadding yres(25) xmaximum 0.45 ysize 0.8 xalign 0.6 ypos 0.1:

        use close([Return("back"), Hide("power_target")])

        hbox spacing xres(25) xfill True:

            for girl in farm.girls:
                if not debug_mode:
                    if girl.last_power == calendar.time:
                        $ blocked.append(girl)
                        $ block_dict[girl] = "This girl already conducted a power today."
                    elif girl.broken:
                        $ blocked.append(girl)
                        $ block_dict[girl] = "This girl's sanity is broken."

            vbox xsize xres(200) ysize 0.9:
                hbox:
                    text _("Conduit: ") bold True
                    if isinstance(selected_conduit, Girl):
                        text selected_conduit.fullname bold True color c_yellow
                text ""
                use girl_vp_selector([("farm", farm.girls)], _selected, "selected_conduit", blocked=blocked, block_dict=block_dict)

            vbox xfill True ysize 0.9:
                hbox:
                    text _("Target: ") bold True
                    if isinstance(selected_target, Girl):
                        text selected_target.fullname bold True color c_yellow

                    elif pow.target == "conduit":
                        text _("Herself") bold True color c_pink
                    elif pow.target == "MC":
                        text MC.name bold True color c_main
                    else:
                        text pow.target.capitalize() bold True color c_yellow

                text ""

                if pow.target == "other girl":
                    if selected_conduit:
                        $ blocked.append(selected_conduit)
                        $ block_dict[selected_conduit] = "You cannot choose the conduit as the target."
                    if pow.power.startswith("leech"):
                        if selected_conduit:
                            $ glist1 = [g for g in MC.girls if g.rank <= selected_conduit.rank]
                            $ glist2 = [g for g in farm.girls if g.rank <= selected_conduit.rank]
                        else:
                            $ glist1 = glist2 = None
                    else:
                        $ glist1 = MC.girls
                        $ glist2 = farm.girls
                    use girl_vp_selector([("brothel", glist1), ("farm", glist2)], _selected, "selected_target", blocked=blocked, block_dict=block_dict)
                elif pow.target == "city girl":
                    use girl_vp_selector([("city", game.free_girls)], _selected, "selected_target", blocked=blocked, block_dict=block_dict)

        textbutton _("Commit") xalign 0.95 yalign 1.0 text_size res_font(24) text_bold True:
            if pow.target in ("other girl", "city girl") and selected_conduit and selected_target:
                action (Return((selected_conduit, selected_target)), Hide())
            elif pow.target not  in ("other girl", "city girl") and selected_conduit:
                action (Return(selected_conduit), Hide())
            elif not selected_conduit:
                text_color c_lightgrey
                action NullAction() tooltip _("Choose a conduit for your power first.")
            else:
                text_color c_lightgrey
                action NullAction() tooltip _("Choose a target for your power first.")

screen girl_vp_selector(girl_lists, _selected = None, return_value = "selected_target", blocked=None, block_dict=None): # girl_lists must be a list of tuples (title, glist)

    # Parent screen can pass a list of blocked girls. It should include a block_dict variable storing tooltips explaining why a girl is blocked.

    if blocked and _selected in blocked:
        $ _selected = None

    viewport xfill True:
        mousewheel True
        arrowkeys True
        pagekeys True
        scrollbars "vertical"
        xalign 0.0

        has vbox spacing yres(6)

        for title, glist in girl_lists:
            textbutton title.capitalize() style "inv_no_padding" text_bold True
            if glist:
                for girl in glist:
                    if title == "city":
                        use girl_button(girl, bsize="x12", context="free", custom_action=[SetScreenVariable("_selected", girl), SetScreenVariable(return_value, girl)], hovered_action=[SetScreenVariable("_selected", girl)], unhovered_action=[SetScreenVariable("_selected", None)], custom_ttip=None)
                    elif blocked and girl in blocked:
                        use girl_button(girl, bsize="x12", context="powers", custom_action=NullAction(), hovered_action=[SetScreenVariable("_selected", girl)], unhovered_action=[SetScreenVariable("_selected", None)], custom_ttip=block_dict[girl])
                    else:
                        use girl_button(girl, bsize="x12", context="powers", custom_action=[SetScreenVariable("_selected", girl), SetScreenVariable(return_value, girl)], hovered_action=[SetScreenVariable("_selected", girl)], unhovered_action=[SetScreenVariable("_selected", None)], custom_ttip=None)

            else:
                textbutton _("No girls are available.") style "inv_no_padding" text_size res_font(16) text_italic True xsize xres(300)
            null



# Final screens

screen mojo_payment(pow, conduit, other_girl = None):
    modal True

    key "mouseup_3" action [Return(False), Hide()]

    use power_detail(pow)

    # add "#0005"

    frame:
        align (0.5, 0.2)
        xsize 0.3
        xpadding xres(25)
        top_padding xres(15)
        bottom_padding xres(25)
        background c_ui_dark

        vbox xfill True:
            spacing yres(12)
            use close([Return(False), Hide("mojo_payment")])

            # Confirmation info
            text pow.name bold True xalign 0.5
            null
            hbox xalign 0.5:
                vbox xalign 0.0 spacing yres(12):
                    text _("Supercharge: ") size res_font(14)
                    text _("Conduit: ") size res_font(14)
                    text _("Target: ") size res_font(14)

                    # Reminder: The main loop checks that MC has enough to pay before this screen is shown
                    text _("Payment: ") size res_font(14)

                vbox xalign 0.0 spacing yres(12):
                    text {True : "ON", False : "OFF"}[pow.super] size res_font(14) bold True
                    text conduit.fullname size res_font(14) bold True

                    if pow.target == "conduit":
                        text _("Herself") size res_font(14) bold True
                    elif pow.target == "MC":
                        text MC.name size res_font(14) bold True
                    elif pow.target in ("other girl", "city girl"):
                        text other_girl.fullname size res_font(14) bold True
                    else:
                        text pow.target.capitalize() size res_font(14) bold True

                    hbox xalign 0.5:
                        spacing xres(20)
                        $ mod = conduit.get_effect("change", "mojo cost")
                        $ purple_cost = MC.get_missing_mojo(pow.get_mojo_cost(conduit))

                        for mcolor, mpoints in (pow.get_mojo_cost() + [("purple", purple_cost)]):
                            if mpoints + mod > MC.mojo[mcolor]:
                                $ val = MC.mojo[mcolor]
                            else:
                                $ val = mpoints + mod

                            if mpoints > 0:
                                fixed fit_first True:
                                    add "mojo_[mcolor]" size res_tb(25) # Color
                                    text (_("%i") % val) bold True size res_font(16) outlines [(1, "#000", 0, 0)] at truecenter: # Amount
                                        if mod:
                                            color c_green

            textbutton _("Cast"):
                text_bold True
                text_size res_font(18)
                xalign 0.5
                action (Return(True), Hide())

screen mojo_trade(sell_rate=2, buy_rate=1): # Returns a dict with changes to commit

    modal True

    default change_dict = {"purple" : 0, "green" : 0, "blue" : 0, "red" : 0, "yellow" : 0}

    key "mouseup_3" action [Return("back"), Hide()]

    frame background c_ui_darker:
        xpadding yres(30)
        ypadding yres(30)
        xalign 0.5
        yalign 0.5

        has vbox
        spacing yres(12)

        use close([Return("back"), Hide("mojo_trade")])

        text _("Current rate:\n{b}%i {image=mojo purple} for %i {image=mojo green}{image=mojo blue}{image=mojo red}{image=mojo yellow}{/b}") % (buy_rate, sell_rate) size res_font(16) xalign 0.5

        hbox:
            spacing xres(12)

            fixed fit_first True:
                align (0.5, 0.5)
                $ mpoints = MC.mojo["purple"]
                add "resources/ui/Powers/orb_purple.webp" size res_tb(25)
                text "{b}%i{/b}" % (int(mpoints) + change_dict["purple"]) size res_font(16) outlines [(1, "#000", 0, 0)] at truecenter:
                    if change_dict["purple"]:
                        color c_green

            text "|" size res_font(20) yalign 0.5 color c_white + "AA"

            grid 2 2:
                spacing yres(20)
                for mcolor, mpoints in MC.mojo.items():
                    if mcolor != "purple":
                        hbox:
                            spacing xres(3)

                            if mpoints + change_dict[mcolor] >= sell_rate:
                                textbutton "+" xysize res_tb(20):
                                    action (SetDict(change_dict, mcolor, change_dict[mcolor]-sell_rate), SetDict(change_dict, "purple", change_dict["purple"]+buy_rate))
                                    yalign 0.5
                            else:
                                null width yres(20)

                            fixed fit_first True:
                                add "resources/ui/Powers/orb_[mcolor].webp" size res_tb(30)
                                text "{b}%i{/b}" % (int(mpoints) + change_dict[mcolor]) size res_font(18) outlines [(1, "#000", 0, 0)] at truecenter:
                                    if change_dict[mcolor]:
                                        color c_red

                            if change_dict[mcolor]:
                                textbutton "-" xysize res_tb(20):
                                    action (SetDict(change_dict, mcolor, change_dict[mcolor]+sell_rate), SetDict(change_dict, "purple", change_dict["purple"]-buy_rate))
                                    yalign 0.5
                            else:
                                null width yres(20)

        hbox:
            xalign 0.5
            textbutton _("{b}Clear{/b}") text_size res_font(16) action SetLocalVariable("change_dict", {"purple" : 0, "green" : 0, "blue" : 0, "red" : 0, "yellow" : 0})
            textbutton _("{b}Commit{/b}") text_size res_font(16) action (Return(change_dict), Hide())

screen micro_transac():

    default x = ui.adjustment(100)

    add "micro_transac_rain"

    frame background c_ui_darkblue:
        xysize (0.66, 0.66)
        align (0.5, 0.5)


        vbox xfill True:
            viewport:
                xadjustment x
                draggable True
                ysize 0.1
                frame background c_ui_dark:
                    text _("                                                                                                  Buy Sill's 'Slutty Schoolgirl' outfit for only $29.99...                                                   Get the ultimate 'Hung like a horse' armor for just $149.99 (2 minutes remaining)...                                                 *SEXY* Recruit the exciting new character 'Lara Crotch' for only $49.99...                                                 *SPECIAL SALE* Don't miss out on our latest season pass 'Summer of a cocksucker' for only $69.99 (valid for 7 days)...                                                                                                                                                                                    ") layout "nobreak"

            hbox spacing xres(20) xalign 0.5:
                button xsize xres(200) yfill True action NullAction():
                    vbox xfill True yfill True:
                        vbox yalign 0.5 xfill True:
                            fixed align 0.5, 0.5 ysize 0.45:
                                add "misc" xalign 0.5
                                text _("Losers'\nchoice!") align 0.5, 0.5 outlines [(1, "#000", 0, 0)] size res_font(24) at blink(0.5, 0.5)
                            null height yres(10)
                            text _("x100 P2W Crystals") xalign 0.5 yalign 0.5 bold True font "resources/fonts/DejaVuSans.ttf"
                        frame xfill True yalign 0.9 ysize yres(60) background Frame("orange_button", borders=gui.button_borders):
                            text "$14.99" font "resources/fonts/DejaVuSans.ttf" align 0.5, 0.5 size res_font(32) bold True at repeat_bounce

                button xsize xres(200) yfill True action NullAction():
                    vbox xfill True yfill True:
                        vbox yalign 0.5 xfill True:
                            fixed align 0.5, 0.5 ysize 0.45:
                                add "misc" xalign 0.25
                                add "misc" xalign 0.75 ypos 0.1
                                text _("Popular\nchoice!!") align 0.5, 0.5 outlines [(1, "#000", 0, 0)] size res_font(24) at shake
                            null height yres(10)
                            text _("x1,000 P2W Crystals") xalign 0.5 yalign 0.5 bold True font "resources/fonts/DejaVuSans.ttf"
                        frame xfill True yalign 0.9 ysize yres(60) background Frame("orange_button", borders=gui.button_borders):
                            text "$59.99" font "resources/fonts/DejaVuSans.ttf" align 0.5, 0.5 size res_font(32) bold True at repeat_bounce

                button xsize xres(200) yfill True action NullAction():
                    vbox xfill True yfill True:
                        vbox yalign 0.5 xfill True:
                            fixed align 0.5, 0.5 ysize 0.45:
                                add "misc" xalign 0.15
                                add "misc" xalign 0.5 ypos 0.1
                                add "misc" xalign 0.85 ypos 0.2
                                text _("Best\nvalue!!!") align 0.5, 0.5 outlines [(1, "#000", 0, 0)] size res_font(24) at jitter
                            null height yres(10)
                            text _("x5,000 P2W Crystals") xalign 0.5 yalign 0.5 bold True font "resources/fonts/DejaVuSans.ttf"
                        frame xfill True yalign 0.9 ysize yres(60) background Frame("orange_button", borders=gui.button_borders):
                            text "$149.99" font "resources/fonts/DejaVuSans.ttf" align 0.5, 0.5 size res_font(32) bold True at repeat_bounce


    timer 0.001 repeat True:
        if x.value >= x.range:
            action Function(x.change, 0)
        else:
            action Function(x.change, x.value+3)

screen brothel_ranking(old, new):

    default yadj = ui.adjustment()
    default but_size = int(0.075 * config.screen_height)
    default max_adj = int(but_size * 42 - config.screen_height*0.85)
    default old_adj = min(but_size * old.index(brothel) - config.screen_height*0.85//2, max_adj)
    default new_adj = min(int(0.075 * config.screen_height) * new.index(brothel) - config.screen_height*0.85//2, max_adj)
    default t = 0
    
    if t == 0:
        timer 0.01 action (Function(yadj.change, old_adj))

    key "mouseup_3" action Return() capture True

    frame background c_ui_darkblue ysize 1.0:
        has vbox box_wrap True spacing yres(10)

        text _("Top Brothels In The City") font "resources/fonts/MATURASC.ttf" color c_orange xalign 0.5

        $ pace = int((new_adj - yadj.value) * min(1, max(0, (t-0.25)/6)))

        viewport ysize 0.85 yadjustment yadj:
            use scroll_list(old_brothel_ranking, current_brothel_ranking, but_size)

        textbutton _("OK") xsize 0.15 xalign 0.5 action Return()
    
        timer 0.05 repeat True action (SetScreenVariable("t", t + 0.05), Function(yadj.change, max(0, yadj.value + pace))) # Scrolls up after 0.25 seconds

    button xmaximum 0.25 ymaximum 0.5 xanchor 1.0 xpos 0.325 yalign 0.5 background Frame("darkorange_button") ypadding yres(20):
        vbox:
            add AlphaMask(MC.current_pic.get(), Frame("GUI/edge_mask.png")) fit "contain" xalign 0.5 ysize 0.85

            text "{b}%s{/b}" % MC.name xalign 0.5
            text _("Known as: {b}%s{/b}") % brothel_ranking_reputations[new.index(brothel)+1].capitalize() xalign 0.5 size res_font(16)
    
    # text str(old_adj) + ": " + str(new_adj) + ": " + str(max_adj) + "\n" + str(yadj.value)

screen scroll_list(old, new, but_size):

    fixed align (0.5, 0.5) ysize but_size * 40 + yres(10):

        for i in old:
            use brothel_ranking_button(i, old.index(i), new.index(i), but_size)

screen brothel_ranking_button(bro, old_rank, new_rank, but_size):
    default y = but_size
    default move_time = 2.0

    button selected_background Frame ("lightblue_button", borders=gui.button_borders) hover_background Frame("darkorange_button", borders=gui.button_borders) action SelectedIf(bro == brothel) ysize y xsize 0.33:
        xpadding yres(18) # Using yres to maintain aspect in wide screen
        ypadding yres(6)
        
        if old_rank != new_rank:
                at transform:
                    xalign 0.5
                    ypos y * old_rank
                    ease move_time ypos y * new_rank
        else:
            at transform:
                xalign 0.5
                ypos y * new_rank
                alpha 0.0
                ease 1.0 alpha 1.0

        if bro == brothel:
            at transform:
                ease 1.0 alpha 0.2
                ease 1.0 alpha 1.0
                repeat 4

        has hbox spacing xres(10) xfill True yalign 0.5

        add bro.get_pic() xsize 0.15 ysize 1.0 align 0.0, 0.5

        if len(bro.name) > 20:
            $ _font = 16
        else:
            $ _font = 18

        text str(new_rank+1) + " - " + bro.name align 0.5, 0.5 xmaximum 0.6:
            size res_font(_font)
            if bro == brothel:
                bold True
        
        hbox align 1.0, 0.5 spacing xres(5):
            add "img_gold" yalign 0.5
            text gold_text(bro.get_income()) size res_font(18):
                if bro == brothel:
                    bold True

#### Pic testing ####

# Calling pic_test and farm_pic_test will display all relevant pictures for the given tags and kwargs for all brothel, farm and slavemarket girls. 
# It's a quick way to check nothing strange is going on with some girl packs.
# Kwargs (reminder): tags, alt_tags1 = None, alt_tags2 = None, alt_tags3 = None, and_tags = None, not_tags = None, strict = False, and_priority=True, naked_filter=False, attempts=0, soft=False, hide_farm=False, pref_filter=False, allow_lesbian=False, always_stock=False, horizontal=False, vertical=False

screen harem_button():
    textbutton _("Chat") xsize xres(75) xalign 0.09 yalign 0.25 action Jump("harem_" + MC.current_trainer.name.lower()) hovered tt.Action("Talk to " + MC.current_trainer.name + ".")

#### END OF BK SCREENS FILE ####
