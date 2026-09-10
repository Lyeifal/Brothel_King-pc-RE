#### Screen Farm — Farm menus and minions | 农场界面 ####
# Phase 2: 农场/小黄人/展示
# Contains: screen farm_menu, screen farm_tab, screen minion_button, screen fshow_init
# Extracted from ui/screens.rpy on 2026-09-10

screen farm_menu(prog, can_cancel=True):

    modal True
    zorder 5

    default _warning = False
    $ available_installations = [farm.installations[farm_installations_dict[type]] for type in all_minion_types if farm.installations[farm_installations_dict[type]].rank > 0]

    use overlay("farm")
    use dark_filter(False)

    if can_cancel:
        key "mouseup_3" action (Return("back"))

    frame background c_ui_darker xsize yres(800) xalign 0.5 ypos 0.1 xpadding xres(10) ypadding yres(10): # Using yres to maintain proportions in wide screen

        has vbox

        hbox xpos 0.01 xfill True:
            hbox spacing xres(10):
                add girl.portrait.get(xres(40), yres(40))
                text girl.fullname bold True yalign 0.5
            text _("Farm Training Menu") bold True yalign 0.5
            if can_cancel:
                use close(Return("back"))

        text "" size 16

        # Warnings
        $ _warning = False

        if prog.target == "no training" and prog.holding=="rest":
            $ text1 = prog.girl.fullname + " will {b}Rest{/b} in her cell."

        else:
            if prog.target == "no training":
                $ text1 = prog.girl.fullname + " will improve her {b}" + stat_name_dict[prog.holding.capitalize()] + "{/b} from doing chores."
            else:
                if prog.target == "auto":
                    $ text1 = prog.girl.fullname + " will receive {b}automatic training{/b}"
                else:
                    $ text1 = prog.girl.fullname + " will receive {b}" + prog.target.capitalize() + " training{/b}"

                if prog.auto_inst:
                    $ text1 += ".\nI will assign her an {b}automatic facility{/b}, if there is room."

                    $ _warning = "There might not be enough free minions to take care of her in all your facilities." # Reverse logic, because of the lack of for... else loops in screen language

                    for inst in available_installations:
                        # $ other_assigned_girls = [g for g in inst.return_assigned_girls() if g != prog.girl]
                        # $ av_min = len(inst.get_healthy_minions()) - len(other_assigned_girls)
                        if inst.count_busy_minions() <= len(inst.get_healthy_minions()): # (prog.target != "group" and av_min >= 1) or av_min >= 2:
                            $ _warning = False

                elif prog.installation:
                    $ text1 += " at the {b}" + capitalize(prog.installation.name) + "{/b}."

                    # $ other_assigned_girls = [g for g in inst.return_assigned_girls() if g != prog.girl]
                    $ free_m = len(prog.installation.get_healthy_minions()) - prog.installation.count_busy_minions()

                    if free_m < 0:
                        if prog.target == "group":
                            $ _warning = "There may not be enough valid minions for group training. I may assign her to a different facility if other minions are available."
                        else:
                            $ _warning = "There are not enough valid minions in the %s, I may have to rotate this girl in and out of the facility." % prog.installation.name

        if _warning:
            $ pic = "side gizel upset"
            $ text1 += event_color["very bad"] % ("\n{b}Warning{/b}: " + _warning)
        else:
            $ pic = "side gizel"

        hbox spacing xres(20):
            frame background Frame (
                # im.MatrixColor(
                #     "resources/ui/cry_box.webp",
                #     im.matrix.colorize(c_lightprune + "CC", "#000")), left=12, right=12) xfill True:
                Transform(
                    "resources/ui/cry_box.webp",
                    matrixcolor = ColorizeMatrix(c_lightprune + "CC", "#000")), left=12, right=12) xfill True: # Updated transform as suggested by Dexell
                has hbox
                spacing 10
                add pic zoom 0.6 yalign 0.5
                text text1 color c_prune text_align 0.0 xalign 0.0 yalign 0.5 size res_font(16) justify True

        text "" size 16

        textbutton _("Farm activities") style "inv_no_padding" xalign 0.01 text_size res_font(18) text_drop_shadow (2, 2) action NullAction() tooltip _("Work for Gizel on the farm. These activities do no require minions.")

        textbutton _("Rest") style "farm_button" text_size res_font(18) xsize yres(780) action (SetField(prog, "target", "no training"), SetField(prog, "holding", "rest"), SetField(prog, "installation", None), SelectedIf(prog.target == "no training" and prog.holding=="rest")) tooltip _("She will simply rest in her pen.")

        null height yres(9)

        hbox:
            for stat in ("Libido", "Obedience", "Constitution", "Sensitivity"):
                textbutton stat_name_dict[stat] style "farm_button" text_size res_font(18) xsize yres(780//4):
                    if prog.target == "no training" and prog.holding==stat.lower():
                        action (SetField(prog, "target", "no training"), SetField(prog, "holding", "rest"), SetField(prog, "installation", None), SelectedIf(True))
                    else:
                        action (SetField(prog, "target", "no training"), SetField(prog, "holding", stat.lower()), SetField(prog, "installation", None), SelectedIf(False))
                    tooltip farm_ttip[stat.lower()]

        text "" size 16

        textbutton _("Sexual Training") style "inv_no_padding" xalign 0.01 text_size res_font(18) text_drop_shadow (2, 2) action NullAction() tooltip _("Go through Gizel's special training program. Sexual training requires available minions.")

        hbox:
            for act in extended_sex_acts:
                $ ttip = "Gizel will train her in %s acts using minions." % act

                if act == "group":
                    $ ttip += "\nRequires 2 or 3 free minions at the same facility."

                textbutton act.capitalize() style "farm_button" text_size res_font(18) xsize yres(780//7):
                    if prog.target==act:
                        action (SetField(prog, "target", "no training"), SetField(prog, "holding", "rest"), SetField(prog, "installation", None), SelectedIf(True))
                    else:
                        action (SetField(prog, "target", act), SelectedIf(False))

                    tooltip ttip

        null height yres(9)

        hbox:
            for cond in ("indifferent", "interested", "fascinated"):
                textbutton (_("Everything (%s)") % cond.capitalize()) style "farm_button" text_size res_font(14) xsize yres(780//3) ysize yres(28):
                    action (SetField(prog, "target", "auto"), SetField(prog, "condition", cond), SelectedIf(prog.target=="auto" and prog.condition == cond))
                    tooltip (_("She will be assigned sex acts automatically until she is at least %s.") % (preference_color[cond] % cond))

        text "" size 16

        textbutton _("Facility") style "inv_no_padding" xalign 0.01 text_size res_font(18) text_drop_shadow (2, 2) action NullAction() tooltip _("Pick a facility with minions for training (sexual training only).")

        if prog.target == "no training":
            button style "farm_button" action SelectedIf(prog.target=="no training"):

                tooltip _("She will be held in her pen for this activity.")

                vbox:
                    spacing 3
                    fixed xalign 0.5 yalign 0.5:
                        fit_first True
                        add Picture(pic, "resources/brothels/farm/pen.webp").get(yres(120), yres(120))
                    text _("Farm pen") size res_font(16) xcenter 0.5

        else:

            hbox xalign 0.0:
                button style "farm_button" action (SetField(prog, "auto_inst", True), SetField(prog, "installation", None), SelectedIf(prog.installation==None)):
                    at alpha_transform

                    tooltip _("Let Gizel assign a free minion to her automatically.")

                    vbox:
                        spacing 3
                        fixed xalign 0.5 yalign 0.5:
                            fit_first True
                            add Picture(pic, "resources/brothels/farm/auto.webp").get(yres(120), yres(120)) # idle_alpha 0.66 hover_alpha 1.0
                        text _("Auto.") style "farm_button_text" size res_font(16) xcenter 0.5

                for inst in available_installations:
                    # $ other_assigned_girls = [g for g in inst.return_assigned_girls() if g != prog.girl]
                    $ inst_nb = inst.count_busy_minions()
                    $ ttip = _("It has %i healthy minion%s available.") % (len(inst.get_healthy_minions()), plural(len(inst.get_healthy_minions())))
                    # if prog.installation==inst:
                    #     $ inst_nb += 1

                    if farm.knows["weakness"][girl] and girl.weakness == inst.minion_type:
                        $ ttip += _("\nShe is weak to %ss. Training will be more efficient, but doing it against her will will increase fear and decrease mood faster.") % girl.weakness
                    if len(inst.get_healthy_minions()) < 1:
                        $ ttip += event_color["bad"] % "\nThere are no available minions in this facility."

                    button style "farm_button":
                        if len(inst.get_healthy_minions()) >= 1:
                            action (SetField(prog, "auto_inst", False), SetField(prog, "installation", inst), SelectedIf(prog.installation==inst))
                        else:
                            hover_background Frame (
                                # im.MatrixColor(
                                #     "resources/ui/cry_box.webp",
                                #     im.matrix.colorize(c_lightprune + "CC", "#000")), left=12, right=12)
                                Transform(
                                    "resources/ui/cry_box.webp",
                                    matrixcolor = ColorizeMatrix(c_lightprune + "CC", "#000")), left=12, right=12) # Updated transform as suggested by Dexell
                            action NullAction()

                        vbox:
                            spacing 3
                            fixed xalign 0.5 yalign 0.5:
                                fit_first True
                                add inst.get_pic().get(yres(120), yres(120)) idle_alpha 0.66:
                                    if len(inst.get_healthy_minions()) >= 1:
                                        hover_alpha 1.0
                                text str(inst_nb) + "{size=-8}/" + str(len(inst.get_healthy_minions())) xalign 0.9 yalign 0.1

                            hbox xcenter 0.5 spacing xres(9):
                                text inst.name.capitalize() size res_font(16):
                                    if len(inst.get_healthy_minions()) >= 1:
                                        style "farm_button_text"
                                    else:
                                        color c_darkprune
                                if farm.knows["weakness"][girl] and girl.weakness == inst.minion_type:
                                    add "img_fear"

                        if prog.installation==inst:
                            tooltip (_("She will be assigned to this facility. ") + ttip)
                        else:
                            tooltip (_("%s currently assigned to this facility. ") % (and_text([g.fullname for g in inst.return_assigned_girls()], if_none=_("No girls"))) + ttip)

        text ""

        if prog.target == "no training" and prog.holding=="rest":
            textbutton _("Hold her (rest)") ypadding yres(9) text_color c_white text_size res_font(18) xsize yres(780//3) xalign 0.5 action Return("commit") tooltip _("Send her to the farm to rest in a pen.")

        else:
            hbox xalign 0.5:
                for train_mode in ("gentle", "tough", "hardcore"):
                    textbutton _("Train her (%s)") % train_mode ypadding yres(9) text_color c_white text_size res_font(18) xsize yres(780//3) action (SetField(prog, "mode", train_mode), SelectedIf(prog.mode==train_mode), Return("commit")) tooltip farm_ttip[train_mode]

screen farm_tab():

    zorder 0

    use close((SetVariable("selected_destination", "main"), Jump("teleport")))
    use shortcuts()
    use overlay("farm")

    use girl_tab(farm.girls, context="farm")

    if selected_girl and selected_girl in farm.girls:

        key "mouseup_3" action (SetVariable("selected_girl", None))

        use girl_stats(selected_girl, context="farm")

        use button_overlay(selected_girl, context="farm")

        use girl_profile(selected_girl, context="farm")


    else:

        key "mouseup_3" action (SetVariable("selected_destination", "main"), Jump("teleport"))
        key "noshift_K_u" action Return(("items", None))

        frame xsize int(0.625*config.screen_width) ysize yres(520) xfill True yfill True xalign 0.1 ypos 0.1 background None:

            has vbox xalign 0.5

            text _("Gizel's Farm") drop_shadow (2, 2) bold True xalign 0

            if farm.girls:
                $ text1 = "Ah, [MC.name]! Came to check on my pets?"
                $ pic = "side gizel"
            else:
                $ text1 = "My minions are bored... When are you going to send them some new playmates?"
                $ pic = "side gizel upset"

            if MC.street_girls:
                $ text1 += "\n\n%i street whores are currently housed in the barn." % len(MC.street_girls)

            hbox spacing 15:
                if farm.powers:
                    if farm.powers == "intro":
                        $ text1 = "[MC.name], come! There is something you must see."
                    button xmargin 6 ymargin 6 xpadding 6 ypadding 6 xysize res_tb(110):
                        text str_int(MC.mojo["purple"]) size res_font(18) drop_shadow (2, 2) xalign 0.5 yalign 0.0 color c_hotpink
                        text str_int(MC.mojo["green"]) size res_font(18) drop_shadow (2, 2) xalign 0.1 yalign 1.0 color c_lightgreen
                        text str_int(MC.mojo["blue"]) size res_font(18) drop_shadow (2, 2) xalign 0.0 yalign 0.3 color c_lightblue
                        text str_int(MC.mojo["red"]) size res_font(18) drop_shadow (2, 2) xalign 1.0 yalign 0.3 color c_red
                        text str_int(MC.mojo["yellow"]) size res_font(18) drop_shadow (2, 2) xalign 0.9 yalign 1.0 color c_yellow
                        action Return(("powers", None))
                        if farm.powers == "intro":
                            background None
                            tooltip _("Click here to head where Gizel is calling you.")
                        elif evpower_deck.can_draw:
                            background None
                            tooltip "New cards are available! Click here to access the {b}Power Deck{/b}."
                        else:
                            background Frame("resources/ui/powers/pentagram.webp")
                            tooltip "Click here to access the {b}Power Deck{/b}."

                button xfill True xmargin 3 ymargin 3 xpadding 6 ypadding 6 tooltip _("Ask Gizel for help about the farm.") background c_ui_dark:
                    if farm.powers == "intro":
                        action Return(("powers", None))
                        tooltip _("Click here to head where Gizel is calling you.")
                    else:
                        action Return(("help", None))
                        tooltip _("Click here for help on using the farm.")
                    at alpha_transform

                    has hbox spacing 10
                    fixed fit_first True yalign 0.5 xysize res_tb(110):
                        add pic zoom 0.6 # idle_alpha 0.8 hover_alpha 1.0
                        if farm.powers:
                            add AlphaMask("static", pic) zoom 0.6 # idle_alpha 0.8 hover_alpha 1.0
                    text text1 yalign 0.5 size res_font(18) justify True italic True xmaximum 0.8

            hbox spacing 15:

                vbox:

                    text _("{b}Girl pens{/b}") size res_font(18) xalign 0.0 ypos 0.3 drop_shadow (2, 2)

                    text "" size res_font(6)

                    frame background c_ui_dark:

                        has vbox spacing 6

                        $ ttip = "The farm can host one girl per pen."

                        if farm.pens < farm.get_pen_limit():
                            $ ttip += "\nClick here to add a new pen for " + str(farm.get_pen_cost()) + " gold."
                        elif brothel.rank == 5:
                            $ ttip += "You cannot build any more pens."
                        else:
                            $ ttip += "Upgrade your brothel to be able to add more pens."

                        $ ttip += "\n(Currently available pens: " + str(farm.pens - len(farm.girls)) + ")"

                        button:
                            xpadding 6
                            ypadding 6
                            action Return(("pen", None))
                            tooltip ttip
                            at alpha_transform

                            fixed:
                                fit_first True
                                add farm.pen_pic.get(xres(135), yres(135)) # idle_alpha 0.66 hover_alpha 1.0
                                if farm.pens < farm.get_pen_limit():
                                    text "+" xalign 0.5 yalign 0.5 size res_font(36)
                                text str(farm.pens) + "{size=-8}/" + str(farm.get_pen_limit()) xalign 0.9 yalign 0.1

                vbox:
                    text _("{b}Farm status{/b}") size res_font(18) ypos 0.3 drop_shadow (2, 2)
                    text "" size res_font(6)
                    frame background c_ui_dark xfill True:
                        has vbox
                        if farm.get_hurt_minions():
                            text _("Hurt minions: ") size res_font(14)
                            hbox box_wrap True:
                                for mn in farm.get_hurt_minions():
                                    use minion_button(mn)

                        else:
                            text _("Nothing to report.") size res_font(14)

            text ""

            hbox spacing 25:
                text _("{b}Facilities & Minions{/b}") size res_font(18) yalign 0.5 drop_shadow (2, 2)
                textbutton _("{u}U{/u}se item") text_size res_font(18) action Return(("items", None)) tooltip _("Use an item on your minions.") yalign 0.5

            text "" size res_font(6)

            frame:
                background c_ui_dark
                xfill True

                has hbox spacing 25

                for type in all_minion_types:
                    $ inst = farm.installations[farm_installations_dict[type]]

                    vbox xsize xres(130):

                        button:
                            xpadding 6
                            ypadding 6
                            insensitive_background c_darkgrey + "E5"
                            at alpha_transform

                            if inst.can_upgrade():
                                action Return(("upgrade", inst))
                            else:
                                action NullAction()

                            tooltip inst.get_tooltip()

                            vbox:
                                spacing 3
                                fixed:
                                    fit_first True
                                    add inst.get_pic().get(xres(120), yres(120)) # idle_alpha 0.66 hover_alpha 1.0
                                    if inst.can_upgrade():
                                        text "+" xalign 0.5 yalign 0.5 size res_font(36)
                                    text str(inst.rank) + "{size=-8}/" + str(district.rank) xalign 0.9 yalign 0.1

                                if inst.rank > 0:
                                    text inst.name.capitalize() size res_font(14) xcenter 0.5
                                else:
                                    text "???" size res_font(14) xcenter 0.5

#            text "" size res_font(6)
            frame:
                background c_ui_dark
                xsize 0.99
                xfill True
                has hbox spacing 25
                for _type in all_minion_types:

                    vbox xsize xres(130) xfill True:

                        if len(farm.get_minions(_type)) > 0:
                            textbutton str(len(farm.get_minions(_type))) + " " + _type.capitalize() + plural(len(farm.get_minions(_type))) style "inv_no_padding" text_size res_font(14) text_bold True xalign 0.5 action NullAction() tooltip minion_description[_type]

                        text "" size res_font(6)

                        for mn in farm.get_minions(_type):

                            button background None xalign 0.5 xpadding 0 xmargin 0 ypadding 0 ymargin 0 action NullAction() tooltip mn.get_tooltip() hovered tt.Action(mn.description):

                                has hbox spacing xres(3)
                                add mn.get_pic(*res_tb(20))

                                text mn.name + ", Lv. " + str(mn.level) size res_font(14) yalign 0.5:
                                    if mn.hurt:
                                        color c_red
                                if mn.hurt:
                                    text _("{color=[c_red]}✙{/color}") size res_font(14) font "resources/fonts/DejaVuSans.ttf" yalign 0.5

screen minion_button(mn, _action=NullAction(), hurt_action=NullAction(), is_active=True):
    
    button background None xalign 0.5 xpadding 0 xmargin 0 ypadding 0 ymargin 0 tooltip mn.get_tooltip():
        if not is_active:
            at desaturate

        if mn.hurt:
            action hurt_action
        else:
            action _action

        has hbox spacing xres(3)
        add mn.get_pic(*res_tb(20))
        text mn.name + ", Lv. " + str(mn.level) size res_font(14) yalign 0.5:
            if mn.hurt:
                color c_red
            elif not is_active:
                color c_grey
        if mn.hurt:
            text _("{color=[c_red]}✙{/color}") size res_font(14) font "resources/fonts/DejaVuSans.ttf" yalign 0.5

screen fshow_init(girl, initial_act):

    modal True
    zorder 5

    use overlay("farm")
    use dark_filter(False)

    key "mouseup_3" action (Return("cancel"))

    default selected_act = initial_act
    default selected_mn = {mn: False for mn in farm.get_minions()}
    default min_descript = "random minion"

    frame background c_ui_darker xsize yres(800) xalign 0.5 ypos 0.1 xpadding xres(10) ypadding yres(10): # Using yres to maintain proportions in wide screen

        has vbox

        hbox xpos 0.01 xfill True:
            hbox spacing xres(10):
                add girl.portrait.get(xres(40), yres(40))
                text girl.fullname bold True yalign 0.5
            text _("Farm Show Setup") bold True yalign 0.5
            use close(Return("cancel"), name="Cancel")

        text "" size 16

        $ min_type = [mn.type for mn in selected_mn.keys() if selected_mn[mn]]

        if selected_act == "group":
            if 3 >= len(min_type) >= 2:
                # Check if different minion types are mixed
                if are_different(min_type):
                    $ min_descript = "minions"
                else:
                    $ min_descript = min_type[0] + "s"
            else:
                $ min_descript = "random minions"

        elif len(min_type) == 1:
            $ min_descript = min_type[0]

        else:
            $ min_descript = "random minion"

        $ text1 = girl.name + " will %s in front of all customers.\n" % {"naked" : "do a {b}nude show next to a %s{/b}" % min_descript, "service" : "practice her {b}service skills with a %s{/b}" % min_descript, "sex" : "have {b}sex with a %s{/b}" % min_descript, "anal" : "have {b}anal sex with a %s{/b}" % min_descript, "fetish" : "do a {b}fetish show with a %s{/b}" % min_descript, "bisexual" : "fuck {b}another girl with a %s{/b}" % min_descript, "group" : "fuck a {b}group of %s{/b}" % min_descript}[selected_act]

        if girl.will_do_farm_act(selected_act) == "accepted":
            $ pic = "side gizel"
            $ text1 += "\n%s " % girl.name + event_color["good"] % "{b}accepts{/b}" + " this: She won't suffer negative consequences, but won't learn as much from the experience."
        elif girl.will_do_farm_act(selected_act) == "resisted":
            $ pic = "side gizel upset"
            $ text1 += "\n%s " % girl.name + event_color["average"] % "{b}resists{/b}" + " this: She will suffer from fear and mood penalties, but will learn from the experience."
        elif girl.will_do_farm_act(selected_act) == "refused":
            $ pic = "side gizel smirk"
            $ text1 += "\n%s " % girl.name + event_color["bad"] % "{b}refuses{/b}" + " this: She will suffer from large fear and mood penalties, and her sanity may fray.\nIt's a gamble: this may cause a large swing in her preference for this act, good or bad."

        hbox spacing xres(20):
            frame background Frame (
                # im.MatrixColor(
                #     "resources/ui/cry_box.webp",
                #     im.matrix.colorize(c_lightprune + "CC", "#000")), left=12, right=12) xfill True:
                Transform(
                    "resources/ui/cry_box.webp",
                    matrixcolor = ColorizeMatrix(c_lightprune + "CC", "#000")), left=12, right=12) xfill True:
                has hbox
                spacing 10
                add pic zoom 0.6 yalign 0.5
                text text1 color c_prune text_align 0.0 xalign 0.0 yalign 0.5 size res_font(16) justify True

        text "" size 16

        textbutton _("Choose a sex Act") style "inv_no_padding" xalign 0.01 text_size res_font(18) text_drop_shadow (2, 2) action NullAction() tooltip _("Choose which sex act will be featured in the Show.")

        null height yres(9)

        hbox:
            for act in extended_sex_acts:
                $ can_act, why_not = farm_can_perform_act(girl, act)

                if can_act:
                    $ ttip = _("She will perform %s acts during the show") % act

                    if girl.will_do_farm_act(act) == "accepted":
                        $ ttip += __(" (%s).") % (event_color["good"] % __("{b}accepts{/b}"))
                    elif girl.will_do_farm_act(act) == "resisted":
                        $ ttip += __(" (%s).") % (event_color["average"] % __("{b}resists{/b}"))
                    elif girl.will_do_farm_act(act) == "refused":
                        $ ttip += __(" (%s).") % (event_color["bad"] % __("{b}refuses{/b}"))
                else:
                    $ ttip = event_color["bad"] % why_not

                textbutton act.capitalize() style "farm_button" text_size res_font(18) xsize yres(780//7):
                    tooltip ttip

                    if can_act:
                        action SetScreenVariable("selected_act", act)
                    else:
                        action NullAction()
                        style "insensitive_button"
                        xpadding yres(18)
                        ypadding yres(9)

        text "" size 16

        if selected_act == "group":
            $ text2 = "s"
        else:
            $ text2 = ""

        textbutton _("Choose her partner(s)%s") % text2 style "inv_no_padding" xalign 0.01 text_size res_font(18)

        null height yres(9)

        hbox xpos 0.025:
            if not farm.get_healthy_minions():
                text _("No healthy minions are available.") color c_red  size res_font(14)

            else:
                # text "Chosen: " size res_font(16) color c_prune bold True

                $ selected_names = [mn.name for mn in selected_mn.keys() if selected_mn[mn]]

                if selected_names:
                    text and_text(selected_names) size res_font(16) bold True
                    if selected_act == "group":
                        if len(selected_names) > 3:
                            text _(" (3 will be selected at random)") size res_font(16)
                        elif len(selected_names) < 2:
                            text _(" (1 more will be selected at random)") size res_font(16)
                    elif len(selected_names) > 1:
                        text _(" (1 will be selected at random)") size res_font(16)
                else:
                    text _("None") size res_font(16) bold True
                    if selected_act == "group":
                        if farm.count_minions() >= 3:
                            text _(" (3 will be selected at random)") size res_font(16)
                        else:
                            text _(" (2 will be selected at random)") size res_font(16)
                    else:
                        text _(" (1 will be selected at random)") size res_font(16)

        null height yres(9)

        hbox xpos 0.025 spacing xres(10) box_wrap True:
            for mn in farm.get_minions():
                if selected_mn[mn]:
                    use minion_button(mn, _action=ToggleDict(selected_mn, mn), hurt_action=Function(notify, "%s is hurt and cannot participate." % mn.name), is_active=True)
                else:
                    use minion_button(mn, _action=ToggleDict(selected_mn, mn), hurt_action=Function(notify, "%s is hurt and cannot participate." % mn.name), is_active=False)

        text "" size 16

        textbutton _("Commit") xalign 0.5 ypadding yres(9) text_color c_white text_size res_font(18) xsize yres(780//3) tooltip _("Start the show."):
            if farm.get_healthy_minions():
                action (SetVariable("chosen_act", selected_act), SetVariable("chosen_minions", [mn for mn in selected_mn.keys() if selected_mn[mn]]), Return("commit"))
