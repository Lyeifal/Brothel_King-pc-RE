#### Screen Girl Profile — Girl display and interactions ####
# Phase 3.1: Extracted from ui/screens.rpy (line 1411-1556).
# Shows profile picture, farm training status, and action buttons.

screen girl_profile(girl, context = None): # context can be girls, slavemarket, farm, free

    tag girl_profile
    zorder 0

    if girl.profile != None:
        key ['K_DELETE'] action Function(toggle_ignore_pic, girl.profile)

    fixed:
        fit_first True
        xalign 0.5
        ypos 0.1
        xfill True
        yfill False

        if girl.profile != None:

            frame xpadding 6 ypadding 6 xalign 0.5 yfill False:
                add girl.profile.get(config.screen_width//2.8, config.screen_height*2//3) xalign 0.5

            if context == "farm":
                frame background c_ui_dark:
                    xmaximum int(12 + config.screen_width // 2.8)
                    yminimum int(0.3*config.screen_height)
                    ymaximum config.screen_height*2//3.5
                    yalign 1.0

                    has vbox
                    spacing 12
                    xfill True
                    yalign 1.0

                    text farm.programs[girl].name bold True size res_font(18) xalign 0.5 yalign 0.5 drop_shadow(1, 1)

                    if farm.programs[girl].target != "no training":

                        if farm.programs[girl].target in farm.knows["reaction"][girl] and farm.programs[girl].target != "auto":

                            $ reaction = girl.will_do_farm_act(farm.programs[girl].target)

                            if reaction == "accepted":
                                $ text1 = event_color["good"] % __("Gizel thinks she will accept this training without causing trouble.")
                            elif reaction == "resisted":
                                $ text1 = event_color["a little bad"] % __("Gizel thinks she will be reluctant to train this act and will take a little convincing (tough mode needed).")
                            elif reaction == "refused":
                                $ text1 = event_color["a little bad"] % __("Gizel thinks she will refuse this act unless she is beaten into submission (hardcore mode needed).")

                        else:
                            $ text1 = __("Gizel isn't sure how %s will react to this training.") % girl.name

                    else:
                        $ text1 = __("%s will never resist this.") % girl.name

                    text text1 size res_font(14) italic True xalign 0.08 drop_shadow(1, 1) xsize 0.85

                    text "" size res_font(18)

                    if farm.programs[girl].target != "no training" or farm.programs[girl].holding != "rest":
                        hbox xalign 0.5 spacing xres(10):
                            textbutton _("Training mode:") xsize xres(100) yalign 0.5 text_xalign 0.0 text_size res_font(14) background None text_color c_white action NullAction() tooltip _("Decide if Gizel will force girls to train against their will.")
                            textbutton __(farm.programs[girl].mode.capitalize()) style "inv_no_padding" text_size res_font(14) yalign 0.5 text_bold True action NullAction() tooltip farm_ttip[farm.programs[girl].mode]

                            if farm.programs[girl].mode == "tough":
                                text _("{image=img_fear}")
                            elif farm.programs[girl].mode == "hardcore":
                                text _("{image=img_fear}{image=img_fear}")

                    if farm.programs[girl].target != "no training":
                        hbox xalign 0.5 spacing xres(10):
                            textbutton _("Training facility:") style "inv_no_padding" xsize xres(100) yalign 0.0 text_xalign 0.0 text_size res_font(14) text_color c_white action NullAction() tooltip _("Define which facility to use for her training (if any).")
                            textbutton __(farm.programs[girl].installation_name.capitalize()) style "inv_no_padding" yalign 0.0 text_size res_font(14) text_bold True action NullAction():
                                if farm.programs[girl].installation:
                                    tooltip farm.programs[girl].installation.get_tooltip()
                                else:
                                    tooltip _("Gizel will choose an available facility automatically for her training.")

                            if farm.programs[girl].installation:
                                vbox:
                                    for mn in farm.get_minions(farm.programs[girl].installation.minion_type):
                                        button background None xalign 0.5 xpadding 0 xmargin 0 ypadding 0 ymargin 0 action NullAction() tooltip mn.get_tooltip() hovered tt.Action(mn.description):
                                            has hbox
                                            add mn.get_pic(*res_tb(20))

                                            vbox:
                                                text __(" %s, Lv. %s") % (mn.name, str(mn.level)) size res_font(14):
                                                    if mn.hurt:
                                                        color c_red

                        if farm.knows["weakness"][girl]:
                            hbox xalign 0.5 spacing xres(10):
                                textbutton _("Use Weakness:") xsize xres(100) text_xalign 0.0 text_size res_font(14) background None text_color c_white action NullAction() tooltip _("Determines if Gizel will use her known weakness against her.")
                                text {True: __("No"), False: __("Yes")}[farm.programs[girl].avoid_weakness] size res_font(14) bold True

                    else:
                        hbox xalign 0.5 spacing 10:
                            textbutton _("Holding mode:") xsize 0.5 xfill True text_xalign 0 text_size res_font(14) background None text_color c_white xpadding 0 xmargin 0.05 ypadding 0 ymargin 0 action NullAction() hovered tt.Action(_("Decide what the girl will do when not in training (work or rest)."))
                            text __(farm.programs[girl].holding.capitalize()) size res_font(14) bold True

                    textbutton _("Change program") text_size res_font(16) xalign 0.5 action Return(("change program", girl)) tooltip __("Change %s's current training program.") % girl.name

                    text "" size res_font(18)

            if (context == "girls" and not girls_firstvisit) or context == "free" or context == "farm":

                vbox xalign 0.0 yalign 0.0 spacing 6:

                    if MC.get_effect("special", "notebook"):
                        key "noshift_K_n" action Show("notebook")
                        button background None xsize xres(80) ysize yres(80) xmargin 10 xpadding 0 action Show("notebook") tooltip __("Open %s's entry in your magical notebook (shortcut: {u}n{/u})") % girl.fullname:
                            at alpha_transform
                            add "resources/items/misc/magic notebook.webp" fit "contain"

                vbox xalign 1.0:
                    frame xmargin 10 ymargin 10:
                        has hbox spacing 6
                        use love_button(girl)
                        use fear_button(girl)

                    frame xalign 0.5 xmargin 10 ymargin 10 background None:
                        use badge_button(girl, 48, 40)

                if context == "girls" and district.rank > 1:
                    use girl_fast_actions(girl, notebook=False, love_fear=False, schedule=False, customers=True)

            if persistent.show_girlpack_rating:
                if context == "slavemarket" or persistent.show_girlpack_rating=="Everywhere":
                    $ rating, ttip = get_girlpack_rating(girl)

                    textbutton _("Girl rating (%s): %s") % (capitalize(girl.path.split("/")[-1]), rating) background c_ui_darkblue text_size res_font(18) yalign 1.0 xmargin 10 ymargin 10 action NullAction() tooltip ttip
