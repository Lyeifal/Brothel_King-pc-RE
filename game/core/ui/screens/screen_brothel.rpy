#### Screen Brothel — Brothel management, furniture, options | 青楼管理界面 ####
# Phase 3.1: 青楼主界面、家具、选项
# Contains: screen brothel, screen furniture, screen brothel_options
# Extracted from ui/screens.rpy (lines 4152-4669)

screen brothel():

    zorder 0
    use overlay("brothel")

    if not brothel_firstvisit:
        key "mouseup_3" action (Hide("brothel"), Jump("main"))
        use close ((Hide("brothel"), Jump("main")))
        use shortcuts()

        if MC.trainers:
            key "K_LEFT" action Function(MC.cycle_trainers, reverse = True)
            key "K_RIGHT" action Function(MC.cycle_trainers)

    if debug_mode: # Checks the UI with a different bg
        key "noshift_K_n" action (Function(brothel.cycle_pic))
        key "shift_K_n" action (Function(brothel.cycle_pic, reverse=True))

    frame background None xalign 0.9 yalign 0.125 ypadding 5 xsize 0.25:
        has vbox
        # if district.rank > 1:
        if not brothel_firstvisit:
            if story_flags["found wagon"]:
                $ text1 = __("Carpenter's {u}W{/u}agon") + "{size=%i}" % -res_font(4)

                if brothel.current_building:
                    if len(brothel.current_building.name) > 15:
                        $ text1 += __("\n(%s. ") % brothel.current_building.name[:15]
                    else:
                        $ text1 += __("\n(%s ") % brothel.current_building.name

                    $ max_dur = float(brothel.current_building.get_duration())
                    $ leftover_dur = round_int(max_dur - (calendar.time - brothel.started_building))

                    if leftover_dur/max_dur <= 0.25:
                        $ text1 += u"\u25d5"
                    elif leftover_dur/max_dur <= 0.5:
                        $ text1 += u"\u25d1"
                    else:
                        $ text1 += u"\u25d4"

                    $ text1 += __("%sd){/size}") % str(leftover_dur)
                
                $ ttip = __("Build furniture to unlock various upgrades for the brothel.")
            else:
                $ text1 = "???"
                $ ttip = "" #!

            if game.chapter >= 2 or NPC_carpenter.active:
                textbutton text1 ysize yres(40) ypadding 5 xfill True action Return("furniture") text_size res_font(18) text_font "DejaVuSans.TTF" tooltip ttip

            if game.chapter >= 2:
                textbutton __("Customer {u}o{/u}ptions") text_size res_font(18) ysize yres(40) xfill True action Return("open options") tooltip __("Fine-tune your brothel for various customer populations and preferences.")

    frame:
        background None
        xpadding xres(25)
        ypadding 0
        ymargin 0
        ypos 0.125
        ysize 0.7
        xfill True
        yfill True

        has vbox
        spacing yres(15)
        yfill True

        if not brothel_firstvisit:
            hbox xfill True xsize 0.66:
                $ bro_costs = round_int(brothel.get_adv_cost() + brothel.get_sec_cost() + brothel.get_maintenance_cost())
                $ bro_upk = round_int(sum(g.upkeep*g.get_effect("boost", "total upkeep") for g in MC.girls))
                $ farm_upk = round_int(sum(g.upkeep*g.get_effect("boost", "total upkeep")//2 for g in farm.girls))

                $ text1 = __("You must pay {b}%s{/b} gold for your brothel services. You must also pay {b}%s{/b} gold for your girls upkeep") % ('{:,}'.format(bro_costs), '{:,}'.format(bro_upk))

                if farm.active and farm.girls:
                    $ text1 += __(" and {b}%s{/b} gold for the girls in the farm") % '{:,}'.format(farm_upk)
                $ text1 += __(" (not accounting for special effects).")

                textbutton __("Daily cost: %s gold") % '{:,}'.format(bro_costs + bro_upk + farm_upk) text_size res_font(18) text_xalign 0.0 xalign 0.0 background c_ui_dark xsize xres(300) ysize yres(36) action NullAction() tooltip text1

                textbutton brothel.name text_size res_font(24) xalign 0.5 ysize yres(40) action Return("change name") tooltip __("Click to change your brothel's name.")

            hbox:
                xalign 0.0
                xfill True

                vbox spacing 10 xalign 0.0:
                    text _("{b}Trainer{/b}") size res_font(18) yalign 0.0 drop_shadow (2, 2)

                    frame:
                        xsize xres(360)
                        ysize yres(220)
                        xalign 0.5
                        xpadding xres(20)
                        background c_ui_dark

                        has vbox yalign 0.5

                        hbox spacing 10 xalign 0.5:
                            if MC.trainers:
                                vbox spacing 0:
                                    button style "inv_no_padding" xsize xres(156) xmargin 0 xpadding 0 action NullAction():
                                        hovered tt.Action(_("Trainers help your girls learn new skills. Discover new trainers by meeting the people of Zan!"))
                                        add MC.current_trainer.portrait zoom 1.0 xalign 0.5 yalign 0.5

                                    if len(MC.trainers) == 1:
                                        $ text1 = __("No other trainer available")
                                    else:
                                        $ text1 = __("Trainers help your girls learning new skills. Discover new trainers by meeting the people of Zan!")

                                    button xmargin 0 xpadding 0 xsize xres(156) background None action NullAction() hovered tt.Action(text1):

                                        has hbox xfill True

                                        textbutton "<" xsize xres(75) xalign 0.0:
                                            if len(MC.trainers) > 1:
                                                action Function(MC.cycle_trainers, reverse = True)
                                                tooltip _("Change trainer.")

                                        textbutton ">" xsize xres(75) xalign 1.0:
                                            if len(MC.trainers) > 1:
                                                action Function(MC.cycle_trainers)
                                                tooltip _("Change trainer.")

                                vbox:
                                    text "{b}" + MC.current_trainer.name + "{/b}" size res_font(18) xalign 0.5
                                    text (_("\n%s") % __(MC.current_trainer.trainer_description)) size res_font(14) justify True

                            else:
                                textbutton "?" xsize xres(100) ysize yres(150)

                                text _("{i}Recruit a trainer to help your girls.{/i}") size res_font(14)

                vbox spacing 10 xalign 1.0:
                    text _("{b}Helpers{/b}") size res_font(18) yalign 0.0 drop_shadow (2, 2)

                    frame:
                        xsize xres(580)
                        ysize yres(220)
                        xalign 1.0
                        background c_ui_dark

                        has vbox spacing 10 xalign 0.0 yalign 0.5

                        fixed yfill False ysize yres(120):

                            $ ttip = __("Your brothel's current reputation is {b}%s{/b}.") % str(brothel.rep)

                            textbutton _("Advertising") ypos 0.1 text_color c_white ypadding 4 text_size res_font(18) background None action NullAction() tooltip ttip text_align 0.0

                            bar:
                                xsize xres(200)
                                xpos 0.25
                                ypos 0.1
                                thumb Frame("tb advertising", xsize=xres(12), ysize=yres(24))
                                thumb_offset xres(3)
                                left_gutter xres(6)
                                right_gutter xres(6)
                                value FieldValue(brothel, "advertising", brothel.max_help, action=Function(brothel.update_customer_count))
                                hovered tt.Action(_("Pay hot chicks with revealing clothing to hang around your brothel, and tell would-be patrons about your establishment."))

                            $ adv_bonus = brothel.get_effect("change", "advertising")
                            if adv_bonus != 0:
                                $ text1 = __(" ({color=[c_green]}+%s{/color} from girls/effects)") % str(adv_bonus)
                            else:
                                $ text1 = ""
                            $ text2 = brothel.get_adv_cost()

                            textbutton __("[brothel.advertising]  babes%s") % text1 background None text_size res_font(14) xpos 0.6 ypos 0.1 ypadding 6

                            $ ttip = __("Your brothel's current threat level is %s.") % brothel.estimate_threat_level()

                            textbutton _("Security") text_color c_white ypos 0.4 ymargin 0 ypadding 4 text_align 0.0  background None text_size res_font(18) action NullAction() tooltip ttip

                            bar:
                                xsize xres(200)
                                xpos 0.25
                                ypos 0.4
                                thumb Frame("tb security", xsize=xres(12), ysize=yres(24))
                                thumb_offset xres(3)
                                left_gutter xres(6)
                                right_gutter xres(6)
                                value FieldValue(brothel, "security", brothel.max_help)
                                hovered tt.Action(_("Pay some sellswords to keep unruly patrons and competitors at bay."))

                            $ sec_bonus = brothel.get_effect("change", "security")
                            if sec_bonus != 0:
                                $ text1 = __(" ({color=[c_green]}+%s{/color} from girls/effects)") % str(sec_bonus)
                            else:
                                $ text1 = ""
                            $ text2 = brothel.get_sec_cost()

                            textbutton __("[brothel.security]  goons%s") % text1 background None text_size res_font(14) xpos 0.6 ypos 0.4 ypadding 6


                            $ ttip = __("Your brothel's current dirt level is {b}%s{/b}.") % str(round_int(brothel.dirt))

                            textbutton _("Maintenance") text_color c_white ypos 0.7 ymargin 0 ypadding 4 text_align 0.0 text_size res_font(18) background None action NullAction() tooltip ttip

                            bar:
                                xsize xres(200)
                                xpos 0.25
                                ypos 0.7
                                thumb Frame("tb maintenance", xsize=xres(12), ysize=yres(24))
                                thumb_offset xres(3)
                                left_gutter xres(6)
                                right_gutter xres(6)
                                value FieldValue(brothel, "maintenance", brothel.max_help)
                                hovered tt.Action(_("Pay a maintenance team to clean up your brothel. And boy, does it get messy in there..."))

                            $ maint_bonus= brothel.get_effect("change", "maintenance")
                            if maint_bonus != 0:
                                $ text1 = __(" ({color=[c_green]}+%s{/color} from girls/effects)") % str(maint_bonus)
                            else:
                                $ text1 = ""
                            $ text2 = brothel.get_maintenance_cost()

                            textbutton __("[brothel.maintenance]  cleaners%s") % text1 background None text_size res_font(14) xpos 0.6 ypos 0.7 ypadding 6

                        hbox xfill True spacing 10:

                            vbox spacing 6 xsize xres(180):
                                text _("Estimated customers") size res_font(14)
                                textbutton _("{image=img_cust} %i") % brothel.customer_count style "inv_no_padding" action NullAction() tooltip brothel.count_customers_description()

                            vbox spacing 6 xsize xres(150):
                                text _("Threat level") size res_font(14)
                                textbutton brothel.estimate_threat_level(caps=True) style "inv_no_padding" action NullAction() tooltip __("Your brothel's current threat level is %s. Brothel threat is affected by brothel security and your Strength skill.") % brothel.estimate_threat_level()

                            vbox spacing 6 xsize xres(200):
                                hbox spacing 10:
                                    text _("Dirt level") size res_font(14)
                                    textbutton _("Clean up") xmargin 10 ymargin 0 ypadding 6 text_size res_font(14):
                                        if brothel.get_clean_up_cost() > 0:
                                            action Return(("clean up", ""))
                                        tooltip __("Buy cleaning material and have Sill and the servants scrub your brothel clean (full clean-up cost: %s gold).") % str(brothel.get_clean_up_cost())
                                textbutton str(round_int(brothel.dirt)) + " {size=-4}(-" + str_int(brothel.get_maintenance()) + ")" style "inv_no_padding" action NullAction() tooltip maintenance_desc[brothel.get_cleanliness()] yoffset -12


        hbox:
            xalign 0.0
            yalign 1.0
            spacing xres(24)
            xfill True
            yfill False

            $ tb_x = 120 # Base thumbnail width for room buttons

            if not brothel_firstvisit:
                frame:
                    background None
                    xpadding 6
                    ypadding 6
                    xalign 0.0
                    yalign 0.0
                    xfill False
                    yfill False

                    has vbox spacing 6

                    hbox spacing xres(6):
                        text _("{b}Bedrooms{/b}") size res_font(18) xalign 0.0 yalign 0.5 drop_shadow (2, 2)

                        $ ttip = __("Upgrade all your bedrooms for %s gold. Upgraded bedrooms are more comfortable for girls and customers alike.") % str(brothel.get_room_upgrade_price(brothel.bedrooms))
                        textbutton _("▲{image=img_gold}") text_font "resources/fonts/DejaVuSans.ttf" ysize yres(24):
                            xalign 0.5
                            yalign 0.5
                            text_size res_font(14)
                            if brothel.bedroom_type.level < brothel.maxupgrade:
                                action renpy.curried_invoke_in_new_context(brothel.upgrade_bedrooms)
                            tooltip ttip

                    frame background c_ui_dark:

                        has vbox spacing 6

                        if brothel.bedrooms < brothel.get_maxbedrooms():
                            $ text1 = __("Add a new bedroom to your brothel for {b}%s gold{/b}. This brothel can only have a maximum of {b}%s bedrooms{/b}.") % (str(brothel.get_room_price()), str(brothel.get_maxbedrooms()))
                        elif district.rank < 5:
                            $ text1 = __("You cannot add any more bedrooms until you move to another brothel.")
                        else:
                            $ text1 = __("You have reached the maximum number of bedrooms.")

                        button style "inv_no_padding" action NullAction():
                            tooltip text1
                            button:
                                insensitive_background c_darkgrey + "E5"
                                at alpha_transform
                                tooltip text1

                                if brothel.bedrooms < brothel.get_maxbedrooms():
                                    action renpy.curried_invoke_in_new_context(brothel.add_room) ## PRAISE BE TO ASCEAI Never would have found this on my own

                                vbox:
                                    spacing 3

                                    fixed:
                                        fit_first True

                                        add brothel.get_bedroom_pic(xres(tb_x), yres(tb_x*3/4)) # idle_alpha 0.66 hover_alpha 1.0
                                        text (_("{image=img_girl}%i") % len(MC.girls)) xalign 0.1 yalign 0.9

                                        if brothel.bedrooms < brothel.get_maxbedrooms():
                                            text "+" xalign 0.5 yalign 0.5 size res_font(36)

                                        text "[brothel.bedrooms]{size=-8}/" + str(brothel.get_maxbedrooms()) xalign 0.9 yalign 0.1

                                    text _("[brothel.bedroom_type.name]") size res_font(14) xcenter 0.5

                frame:
                    background None
                    xalign 0.0
                    yalign 0.0
                    xfill False
                    yfill False

                    has vbox spacing 6

                    text _("{b}Master Bedroom{/b}") size res_font(18) xalign 0.0 drop_shadow (2, 2)

                    frame background c_ui_dark:

                        has vbox spacing 6

                        button style "inv_no_padding" action NullAction():
                            tooltip brothel.master_bedroom.get_description()
                            at alpha_transform
                            button:
                                insensitive_background c_darkgrey + "E5"
                                tooltip brothel.master_bedroom.get_description()

                                if brothel.master_bedroom.level < brothel.rank:
                                    action renpy.curried_invoke_in_new_context(brothel.upgrade_master_bedroom)

                                vbox:
                                    spacing 3

                                    fixed:
                                        fit_first True

                                        add brothel.master_bedroom.get_pic(xres(tb_x), yres(tb_x*3/4), proportional=False) # idle_alpha 0.66 hover_alpha 1.0

                                        if brothel.master_bedroom.level:
                                            text _("Lv. %i{size=-8}/%i") % (brothel.master_bedroom.level , brothel.rank) xalign 0.9 yalign 0.1
                                            hbox xalign 0.1 yalign 0.95:
                                                for girl in brothel.master_bedroom.girls:
                                                    button background c_white yalign 0.5 xmargin 2 ymargin 0 xpadding 1 ypadding 1:
                                                        action NullAction()
                                                        tooltip __("%s is currently assigned to the master bedroom.") % girl.fullname
                                                        add girl.portrait.get(*res_tb(20)) alpha 1.0

                                        if brothel.master_bedroom.level < brothel.rank:
                                            text "+" xalign 0.5 yalign 0.5 size res_font(36)

                                    text brothel.master_bedroom.name size res_font(14) xcenter 0.5


            frame:
                background None
                xpadding 6
                ypadding 6
                xalign 0.5
                yalign 0.0
                xfill False
                yfill False

                has vbox
                spacing 6

                text _("{b}Common Rooms{/b}") size res_font(18) xalign 0.0 drop_shadow (2, 2)

                frame:
                    background c_ui_dark
                    has hbox

                    for room_name in all_common_rooms:

                        $ room = brothel.rooms[room_name]

                        button action NullAction() tooltip room.get_description():
                            background None
                            xpadding 1
                            ypadding 1
                            button:
                                xpadding 6
                                ypadding 6
                                insensitive_background c_darkgrey + "E5"
                                at alpha_transform

                                if room.level < district.rank:
                                    action Return(("add_room", room))
                                    tooltip room.get_description()

                                vbox:
                                    spacing 3

                                    fixed:
                                        fit_first True
                                        add room.pic.get(xres(tb_x), yres(tb_x*3/4)) # idle_alpha 0.66 hover_alpha 1.0
                                        if not brothel_firstvisit:
                                            text _("Lv. %i{size=-8}/%i") % (room.level, district.rank) xalign 1.0
                                        if room.level:
                                            text (_("{image=img_cust} %i") % room.cust_limit) xalign 0.1 yalign 0.9
                                        if room.level < district.rank:
                                            text "+" xalign 0.5 yalign 0.5 size res_font(36)

                                    text __(room.name.capitalize()) size res_font(14) xcenter 0.5


    # Additional button specifically for the harem mod

    if game.has_active_mod("Harem"):
        if MC.current_trainer.name in harem_mod.talkative_NPCs:
            use harem_button()


# BROTHEL SUBSCREENS

screen furniture():

    key "mouseup_3" action (Return("quit"))

    use overlay("wagon")
    use shortcuts()
    use close(Return("quit"))

    frame ypos 0.05 background None xmargin 20 ymargin 20:

        has vbox spacing 10

        text _("Carpenter's Wagon") bold True xalign 0 yalign 0

        hbox spacing 6 xfill True ysize yres(120):
            button style "inv_no_padding":
                if story_flags["carpenter H"]: #! UNUSED
                    action Return("H")
                add "side carpenter" zoom 0.8 yalign 0.5

            if story_flags["carpenter H"]:
                $ text1 = __("Boss, I'm feeling kinda randy today...\nThink we could have a private moment?\n{size=-4}(Click on her portrait)") #! UNUSED
            elif not brothel.current_building:
                $ text1 = __("Oh, hi. Got a new job for me?")
            else:
                $ text1 = __("I'm still working on that %s. You should come back later.") % brothel.current_building.name

            text text1 xsize 0.4 yalign 0.5 size res_font(18) justify True italic True

            vbox xsize 0.4 yfill True xalign 1.0:
                text _("Available resources") drop_shadow (2, 2) size res_font(18)
                frame xfill True yfill True background c_ui_brown xpadding 0 ypadding 0:
                    use resource_tab(x=0.5, y=0.5, sz=yres(24), font_sz=res_font(14))

            vbox xsize 0.6 yfill True xalign 1.0:
                text _("Building Queue") drop_shadow (2, 2) size res_font(18)
                frame xfill True yfill True background c_ui_brown:
                    if brothel.current_building:
                        $ dur = brothel.current_building.get_duration() - (calendar.time - brothel.started_building)
                        button xfill False yfill False xalign 0.5 yalign 0.5 background None:
                            action NullAction()
                            tooltip (brothel.current_building.description + "\n" + __("%s day(s) to complete.") % str(dur))
                            add brothel.current_building.pic.get(*res_tb(50)) xalign 0.5 yalign 0.5
                            text str(dur) + "d" xalign 1.0 yalign 0.0 size res_font(18)
                    else:
                        text _("No building in progress.") italic True size res_font(14)

        text __("%s's Decoration and Furniture") % brothel.name drop_shadow (2, 2) size res_font(18)

        if brothel.furniture:
            frame xfill True background c_ui_brown:
                has hbox spacing 6 box_wrap True
                for furn in brothel.furniture:
                    button background c_ui_brown action NullAction() tooltip furn.description xsize xres(52) ysize yres(44) xpadding 0 ypadding 0:
                        add furn.pic.get(xres(48), yres(40)) xalign 0.5 yalign 0.5

        text _("Build templates") drop_shadow (2, 2) size res_font(18)

        frame background c_ui_dark:
            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                ysize 0.6
                yfill True

                has vbox

                for type, description in furniture_types:
                    $ builds = [f for f in all_furniture if f.type == type and f.can_build()]

                    if builds:
                        text __("{b}%s{/b} - {i}%s") % (type.capitalize(), description) size res_font(14)
                        frame xfill True background c_ui_brown:
                            hbox spacing 6 box_wrap True:
                                for furn in builds:
                                    if furn.get_duration() < 2:
                                        $ text2 = __("%s (%s day to complete).") % (furn.description, str(furn.get_duration()))
                                    else:
                                        $ text2 = __("%s (%s days to complete).") % (furn.description, str(furn.get_duration()))
                                    button xsize xres(110) ysize yres(90) xpadding 2 ypadding 2:
                                        action Return(furn)
                                        tooltip text2
                                        at alpha_transform
                                        add furn.pic.get(xres(90), yres(70)) xalign 0.5 ypos 0.05 # hover_alpha 1.0 idle_alpha 0.8
                                        button xalign 0.5 yalign 1.0 xpadding 0 ypadding 0 background c_ui_brown xfill True:
                                            action Return(furn)
                                            tooltip text2
                                            use resource_tab(furn.cost, sp=1)
                                        text __("%sd") % str(furn.get_duration()) xalign 0.95 yalign 0.05 size res_font(18)
#                        else:
#                            text "You have built every available " + type +"." size res_font(14) italic True
                    text "" size res_font(8)


    zorder 0
    use overlay("customers")

    key "mouseup_3" action (Return("close options"))
    use close(Return("close options"))
    use shortcuts()

    frame:
        background None
        xpadding 25
        ypadding 0
        ypos 0.1
        xfill True
        ysize 0.88

        has hbox spacing 10 yfill True

        if NPC_carpenter.active:
            vbox xsize xres(320):
                text _("{b}Customer populations{/b}") size res_font(18) yalign 0.0 drop_shadow (2, 2)

                frame xpadding xres(10) ypadding yres(10) xfill True yfill True:
                    has vbox
                    text _("Choose customer populations to attract to your brothel (build decoration to attract more)") size res_font(14) italic True color c_brown
                    null height yres(6)
                    vbox spacing yres(6):
                        for pop in all_populations:
                            hbox spacing 6:
                                button style "inv_no_padding" xalign 0.0 yalign 0.5:
                                    action NullAction()
                                    if brothel.get_effect("allow", pop.name):
                                        add pop.get_pic(*res_tb(40))
                                        tooltip pop.description
                                    else:
                                        add pop.get_pic(*res_tb(40)) at desaturate
                                        tooltip _("You must build new decoration at the Carpenter's Wagon to attract this population.")

                                if brothel.get_effect("allow", pop.name):
                                    vbox spacing yres(6):
                                        $ total_budget, ent_budget, wh_budget = pop.get_average_budgets(description=True)
                                        hbox spacing 6 xalign 0.0:
                                            bar thumb Frame("tb empty", xsize=xres(9), ysize=yres(18)) xsize xres(100) ysize yres(18) yalign 0.0 value FieldValue(pop, "weight", 5, action=Function(brothel.update_customer_count))
                                            text attract_pop_dict[pop.weight] color c_brown size res_font(14) yalign 1.0
                                        textbutton _("Average budget: %s gold") % total_budget xalign 0.0 yalign 1.0 xmargin 0 xpadding 0 ymargin 0 ypadding 0 background None text_color c_prune text_size res_font(14) action NullAction() tooltip _("This is the average {b}maximum budget{/b} for %s. (%s for entertainment, %s for whoring)") % (pop.name, ent_budget, wh_budget)
            vbox xsize xres(320):
                text _("{b}Customer preferences{/b}") size res_font(18) yalign 0.0 drop_shadow (2, 2)
                frame xfill True xpadding xres(10) ypadding yres(10):
                    has vbox
                    text _("Influence customer preferences for entertainment and sexual acts (build furnishing to get bigger boosts)") size res_font(14) italic True color c_brown
                    null height yres(6)

                    vbox spacing yres(6):
                        for target in (all_jobs, all_sex_acts):
                            vbox ysize 0.5 spacing 6:
                                for pref in target:
                                    hbox spacing 6:
                                        textbutton __(pref.capitalize()) xsize xres(120) ypadding 5 text_size res_font(18) yalign 0.5:
                                            action NullAction()

                                            if brothel.get_effect("allow", pref + " preference"):
                                                tooltip __("Use this setting to change your customers' preference for ") + __(pref.capitalize()) + __(" up to +") + str(50*brothel.get_effect("allow", pref + " preference")) + __("%") + __(".")
                                            else:
                                                background "#CCB8A0"
                                                text_color c_white
                                                tooltip __("You must build new furnishing at the Carpenter's Wagon to change %s preference.") % __(pref.capitalize())

                                        if brothel.get_effect("allow", pref + " preference"):

                                            bar thumb "tb empty" xsize xres(100) xpos 0 yalign 0.0 value DictValue(game.customer_preference_weight, pref, brothel.get_effect("allow", pref + " preference"), action=Function(brothel.update_customer_count))

                                            if game.customer_preference_weight[pref]:
                                                text percent_text(0.5*game.customer_preference_weight[pref]) color c_brown size res_font(14) yalign 0.5
                                            else:
                                                text "" size res_font(14) yalign 0.5

                text "" size res_font(22)
                text _("{b}Matching preferences{/b}") size res_font(18) yalign 0.0 drop_shadow (2, 2)

                frame ysize yres(150) xpadding xres(10) ypadding yres(10) xfill True:
                    has vbox spacing 6

                    text _("Choose how incoming customers will be matched with your girls.") size res_font(14) italic True color c_brown

                    if game.matching_priority == "rank":
                        $ text1 = __("When possible, customers will be matched with girls of the same rank.")
                    elif game.matching_priority == "act":
                        $ text1 = __("When possible, customers will be matched with girls that allow their preferred job or sex act.")

                    textbutton _("By %s") % game.matching_priority text_size res_font(18) xsize xres(100) action ToggleField(game, "matching_priority", true_value="rank", false_value="act")

                    text text1 size res_font(14) color c_prune


            vbox xsize xres(320):

                if [f for f in brothel.furniture if f.can_deactivate]:
                    text _("{b}Special options{/b}") size res_font(18) yalign 0.0 drop_shadow (2, 2)

                    frame ysize yres(200) xpadding xres(10) ypadding yres(10) xfill True:
                        has vbox
                        text _("Activate or deactivate special brothel furniture.") size res_font(14) italic True color c_brown

                        hbox box_wrap True:
                            for furn in [f for f in brothel.furniture if f.can_deactivate]:

                                button xsize xres(56) ysize yres(56) action Function(furn.toggle) tooltip __("Click here to activate or deactivate %s.\n%s ({b}%s{/b})") % (furn.name, get_description("", furn.effects), {True: __("active"), False: __("inactive")}[furn.active]):

                                    add furn.pic.get(*res_tb(50)) xalign 0.5 yalign 0.5

                                    if not furn.active:
                                        text _("X") color c_crimson size res_font(48) xalign 0.5 yalign 0.5
                    text "" size res_font(22)

                # This will unlock with the 'billboard' upgrade
                if brothel.get_effect("special", "advanced advertising"):
                    text _("{b}Advanced settings{/b}") size res_font(18) yalign 0.0 drop_shadow (2, 2)

                    frame ysize yres(200) xpadding xres(10) ypadding yres(10) xfill True:
                        has vbox

                        text _("In addition to improving your brothel reputation, advertising girls will increase customer attraction and customer budget based on advertising power (create new outfits to increase advertising power).") size res_font(14) italic True color c_brown
                        null height yres(6)
                        hbox spacing xres(3):
                            vbox xsize xres(100):
                                text _("Customers") size res_font(14) bold True color c_brown yalign 1.0
                                text _("%s to customer attraction") % percent_text(brothel.get_adv_setting("attraction")) size res_font(14) color c_brown
                            bar thumb "tb empty" xsize xres(100) xpos 0 yalign 0.0 value FieldValue(brothel, "advertising_setting", range=4, offset=-2, action=Function(brothel.update_customer_count)) tooltip _("Use this setting to adjust the focus between customer attraction (how many customers will come to the brothel) and customer budget (the maximum amount of gold each customer is able to spend).")
                            vbox xsize xres(100):
                                text _("Budget") size res_font(14) bold True color c_brown yalign 1.0
                                #text str(brothel.advertising_setting)
                                text _("%s to customer budget") % percent_text(brothel.get_adv_setting("budget") / brothel.max_help) size res_font(14) color c_brown
                    text "" size res_font(22)

                text _("{b}Forecast{/b}") size res_font(18) yalign 0.0 drop_shadow (2, 2)
                frame xfill True xpadding xres(10) ypadding yres(10):
                    has vbox spacing 12
                    text brothel.count_customers_description() color c_prune size res_font(14)
                    text brothel.count_budget_description() color c_prune size res_font(14)


## MATCHMAKING SCREENS
