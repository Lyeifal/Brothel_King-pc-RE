#### Screen Misc2 — Main character, hints and girl details | 主角/提示/女孩详情面板 ####
# Phase 2: 主角面板/提示/详情面板
# Contains: screen suzume_hints, screen restock_button, screen inventory_filter, screen girl_select, screen main_character, screen personality_screen, screen notebook, screen fshow_screen, screen farm_show_gold, screen generic_event_screen, screen mood_details, screen love_button, screen fear_button, screen sex_details
# Extracted from ui/screens.rpy on 2026-09-10

screen suzume_hints(contact_list):

    use dark_filter(False, True)

    key "mouseup_3" action (Return(False))

    frame background None xmargin xres(60) top_margin yres(120) bottom_margin(250):
        has vbox
        spacing 20

        hbox:
            box_wrap True

            for contact in contact_list:
                $ img, ttip, npc = contact

                button xsize xres(120) ysize yres(120) xpadding 6 ypadding 6:
                    if MC.interactions >= 1:
                        action Return(npc)
                    add img xalign 0.5 yalign 0.5 fit "contain"
                    if npc == NPC_suzume:
                        tooltip "Talk to {b}Suzume{/b} for general tips, or once you have unlocked all 3 tips for a given Kunoichi."
                    else:
                        tooltip "Ask Suzume to track {b}%s{/b}, for information on the Kunoichi. {b}Costs 1 {/b}{image=img_AP}." % ttip

            textbutton _("Go back") text_bold True xalign 0.5 yalign 0.5 xsize xres(120) ysize yres(120) xpadding 6 ypadding 6 action Return(False) # Note that 'None' is not a valid return value


        hbox spacing 50 xalign 0.5:
            text _("Hints collected:") yalign 0.5 bold True

            for ninja in (NPC_narika, NPC_mizuki, NPC_haruka):
                if ninja.flags["hints"] >=3:
                    $ ttip = "You may now {b}talk to Suzume{/b} to devise a cunning action plan and finally catch her."
                else:
                    $ ttip = "You need to {b}gather 3 hints{/b} before you can attempt to catch her again."

                button background None xsize xres(160) ysize yres(80) xpadding 6 ypadding 6:
                    action NullAction()
                    tooltip "You have received %s tips on {b}%s{/b}. %s" % (str(ninja.flags["hints"]), ninja.name, ttip)
                    has hbox
                    add ninja.name.lower() yalign 0.5 fit "contain"
                    text "%s/3" % str(ninja.flags["hints"]) bold True xalign 0.5 yalign 0.5

        


screen restock_button(merc, upgrade=False):

    hbox spacing 20 xalign 0.5 ypos 0.08 yanchor 0.0:

        $ restock_cost = merc.get_restock_cost(game.chapter)

        textbutton __("Restock inventory") text_size res_font(18) tooltip __("Restock this shop's inventory for %s gold (available once a day).") % restock_cost:
            if merc.last_restock != calendar.time and MC.has_gold(restock_cost):
                action Return((True, "restock"))
            else:
                action Return((False, "restock"))

        if upgrade == True and merc.can_upgrade():
            $ chapter, cost, upgrade = merc.get_upgrade_info()

            $ ttip = __("Upgrade this shop's inventory (+%s %s item%s) for %s %s.") % (str(upgrade[1]), upgrade[0], plural(upgrade[1]), str(cost[1]), cost[0])

            textbutton __("Upgrade shop") text_size res_font(18) tooltip ttip:
                if MC.has_resource(*cost):
                    action Return((True, "upgrade_shop"))
                else:
                    action Return((False, "upgrade_shop"))

screen inventory_filter(filters=inventory_filters["base"]):

    if MC.active_inv_filter not in filters:
        $ active_inv_filter = []

    vbox xfill False yfill False spacing 3:
        for filter in filters:
            frame xsize xres(38) ysize yres(38) xpadding 0 xmargin 0:
                button xalign 0.5 yalign 0.6 ysize yres(30) xpadding 0 xmargin 0 idle_background None:

                    action (SetField(MC, "active_inv_filter", filter), Function(renpy.restart_interaction), SetScreenVariable("left_length", max_item_shown), SetScreenVariable("right_length", max_item_shown))

                    if filter:
                        if filter == MC.active_inv_filter:
                            add "filter_" + filter
                        else:
                            add "filter_" + filter + "_unselect"
                        tooltip __("Show %s items.") % __(filter)
                    else:
                        if filter == MC.active_inv_filter:
                            add "filter_all"
                        else:
                            add "filter_all_unselect"
                        hovered tt.Action(_("Show all items."))


screen girl_select(girl_list, orange = False, no_sched=False, action_button=None):

    frame:

        id "girl_select"

        background None

        xalign 0.5
        yalign 0.1
        xpadding 6
        ypadding 6
        xsize 0.45
        ysize 0.15
        xfill True
        yfill False

        if girl_list:
            key "K_LEFT" action (Function(select_previous_girl, girl_list), Hide("item_profile"))
            key "K_RIGHT" action (Function(select_next_girl, girl_list), Hide("item_profile"))

        hbox spacing 5 xalign 0.5:

            textbutton "<" ysize yres(120) yalign 0.5:
                if girl_list:
                    action (Function(select_previous_girl, girl_list), Hide("item_profile"), SetVariable("selected_item", None))

            frame:
                xsize xres(300)
                ysize yres(120)
                xfill True
                xalign 0.5
                ymargin 3

                if orange:
                    background c_orange + "AA"

                if girl_list and selected_girl:
                    frame background None xsize xres(280) ysize yres(120) xfill True yfill True ypadding 0 ymargin 0:

                        has hbox
                        spacing 6

                        frame style "inv_no_padding" xsize xres(100) ysize yres(100) xfill True yalign 0.5:
                            if selected_girl.portrait != None:
                                fixed fit_first True xalign 0.5 yalign 0.5:
                                    add selected_girl.portrait.get(*res_tb(90)) xalign 0.5 yalign 0.5

                                    $ badge = selected_girl.get_badge()
                                    if badge:
                                        add ProportionalScale(badge, *res_tb(40)) xalign 0.9 yalign 0.1

                        $ text1 = __("%s\nRank %s - Level %s") % (selected_girl.fullname, rank_name[selected_girl.rank], selected_girl.level)

                        if not no_sched:
                            if selected_girl.job:
                                $ text1 += "\n%s" % __(selected_girl.job.capitalize())
                                if selected_girl.job in all_jobs and selected_girl.work_whore:
                                    $ text1 += __("/Whore")
                                $ sched = selected_girl.workdays[calendar.get_weekday()]

                            else:
                                $ text1 += __("\nNo job")
                                $ sched = 0


                            if selected_girl.away:
                                $ text1 += __(" (away)")
                            elif selected_girl.hurt > 0:
                                $ text1 += __(" (hurt)")
                            elif selected_girl.exhausted > 0:
                                $ text1 += __(" (tired)")
                            elif selected_girl.resting or sched == 0:
                                $ text1 += __(" (resting)")
                            elif sched == 50:
                                $ text1 += __(" (half-shift)")

                        text text1 size res_font(14) xalign 0.0 yalign 0.5 color c_brown

                    if action_button:
                        $ _caption, _action, _ttip = action_button
                        textbutton _caption action _action tooltip _ttip xalign 1.0

                elif girl_list:
                    $ selected_girl = girl_list[0]
                    $ renpy.restart_interaction()

                else:
                    text _("{i}No girls are available for this task{/i}") color c_brown size res_font(14) xalign 0.5 yalign 0.5

            textbutton ">" ysize yres(120) yalign 0.5:
                if girl_list:
                    action (Function(select_next_girl, girl_list), Hide("item_profile"), SetVariable("selected_item", None))


screen main_character():

    use shortcuts()
    use overlay("MC")

    frame background None:

        xalign 0.0
        ypos 0.1
        xsize xres(200)
        ysize yres(520)
        xfill True
        yfill True

        has vbox

        spacing 3

        frame xpadding 3 ypadding 10 xfill True:
            has vbox
            textbutton MC.name background None text_color c_main action Return("change_name") hovered tt.Action(_("Click here to change your character's name"))
            textbutton (__("Level %s %s") % (MC.level, MC.playerclass)) background None text_size res_font(18) text_color c_darkgrey action NullAction() tooltip __("You need %s prestige to level up.") % int(MC_xp_to_levelup[MC.level])

        frame xpadding 3 ypadding 10 xfill True:
            has vbox spacing 6

            for stat in all_MC_stats:

                if MC.get_effect("change", stat) < 0 or MC.get_effect("special", "wound"):
                    $ col2 = c_red
                elif MC.get_effect("change", stat) > 0:
                    $ col2 = c_emerald
                else:
                    $ col2 = c_darkgrey

                button:

                    background None
                    xsize xres(180)
                    ysize yres(30)

                    action NullAction()
                    tooltip MC.get_stat_description(stat)

                    text MC_stat_color[stat] % __(stat.capitalize()) size res_font(18)

                    text "{color=[col2]}" + str(int(MC.get_stat(stat))) + "{/color}" size res_font(18) xanchor 1.0 xpos 0.8

                    if MC.skill_points > 0 and MC.get_stat(stat, raw=True) < MC.get_stat_cap(stat):
                        textbutton "+" text_size res_font(14) xpos 0.85 xfill False xpadding xres(4) ypadding yres(2) action Return("raise_" + stat) tooltip "Use a skill point to raise this attribute (max %i)" % MC.get_stat_cap(stat)

            text "" size res_font(8)

            vbox spacing 3:
                $ text1 = __("You earn prestige everytime you or your girls have sex, or when one of your girl earns a new level.")

                if MC.level == 25:
                    $ text1 += __("\nYou have reached the maximum level.")
                else:
                    $ text1 += __("\nYou need %s prestige to level up.") % int(MC_xp_to_levelup[MC.level])

                button:
                    background None
                    action NullAction()
                    tooltip text1

                    text (str(int(MC.prestige)) + " prestige") size res_font(14) color c_brown

                button:
                    background None
                    action NullAction()
                    tooltip _("You get 1 skill point for every new level.")

                    text __("%s skill points") % str(MC.skill_points) size res_font(14) color c_brown

        frame xpadding 3 ypadding 10 xfill True:
            has vbox
            hbox xalign 0.5:

                spacing 16

                button yalign 0.5 xpadding 0 action NullAction() tooltip MC_playerclass_description[MC.playerclass]:
                    add Picture(path=playerclass_pics[MC.playerclass]).get(*res_tb(40)) yalign 0.5

                button yalign 0.5 xpadding 0 action NullAction() tooltip god_description[MC.god]:
                    add Picture(path=god_pics[MC.god]).get(*res_tb(40)) yalign 0.5

                button yalign 0.5 xpadding 0 action NullAction() tooltip (alignment_description[MC.get_alignment()] + "\n" + __("(%s: %s)") % (MC.get_alignment().capitalize(), plus_text(MC.get_alignment_delta(MC.get_alignment())))):
                    add Picture(path=alignment_pics[MC.get_alignment()]).get(*res_tb(40)) yalign 0.5

            text "" size res_font(10)

            textbutton __("{b}Current goal{/b}\n{i}{size=-2}%s") % game.get_first_goal() xalign 0.1 yalign 0.5 xsize xres(180) text_size res_font(14) text_color c_brown background None:
                action NullAction()
                hovered Show("goal_ttip", transition=Dissolve(0.15))
                unhovered Hide("goal_ttip", transition=Dissolve(0.15))

            text "" size res_font(8)

            textbutton __("Spellboo{u}k{/u}") xalign 0.5 action (Show("spellbook"), Function(norollback)) tooltip __("See all available spells and active talents")

    hbox xpos 0.2 ypos 0.8 yanchor 1.0 xsize 0.55 ysize 0.7 xfill True:
        textbutton "<"  ysize yres(120) xalign 0.0 yalign 1.0:

            action Return("previous_pic")
            tooltip _("Change your character's picture.")


        frame background None:
            xalign 0.5
            yalign 1.0
            xmaximum 0.9
            xfill False
            yfill False
            padding (0, 0, 0, 0)
            add AlphaMask(MC.current_pic.get(), Frame("GUI/edge_mask.png")) fit "contain" xalign 0.5

        textbutton ">" xalign 1.0 ysize yres(120) yalign 1.0:

            action Return("next_pic")
            tooltip _("Change your character's picture.")

screen personality_screen():

    tag personality_screen

    frame xalign 0.51 yanchor 0.0 ypos 0.1 ysize yres(320) xfill True xpadding xres(10) ypadding yres(10) xmaximum xres(400) background Frame("resources/ui/paper.webp"): #int(config.screen_width * 0.58):

        has vbox spacing 20

        if selected_girl:

            hbox xalign 0.0:
                textbutton _("Pers. ") xsize xres(85) text_size res_font(18) hovered SetVariable("pers_showing", "personality") action NullAction(), SelectedIf(pers_showing=="personality")
                textbutton _("Tastes") xsize xres(85) text_size res_font(18) hovered SetVariable("pers_showing", "tastes") action NullAction(), SelectedIf(pers_showing=="tastes")
                textbutton _("Sex. ") xsize xres(85) text_size res_font(18) hovered SetVariable("pers_showing", "sexual") action NullAction(), SelectedIf(pers_showing=="sexual")
                textbutton _("Events") xsize xres(85) text_size res_font(18) hovered SetVariable("pers_showing", "recent") action NullAction(), SelectedIf(pers_showing=="recent")

            if debug_mode:
                hbox spacing 20:
                    for att in ["EI", "DS", "MI", "LM"]:
                        text (_("%s discovery: %i") % (att, selected_girl.personality_unlock[att])) size 14


            hbox spacing xres(6) xpos 0.01:

                $ badge = selected_girl.get_badge()
                button xmaximum yres(90) background None action NullAction():
                    if selected_girl in (MC.girls + farm.girls):
                        hovered (Show("mood_details", girl=selected_girl, transition=Dissolve(0.15)), tt.Action(selected_girl.get_mood_description("mood")))
                        unhovered Hide("mood_details", transition=Dissolve(0.15)) xpadding 0 ypadding 0 xmargin 0 ymargin 0 xsize xres(100) ysize yres(100)

                    fixed fit_first True:
                        add selected_girl.portrait.get(*res_tb(90))

                        # Add mood meter
                        if selected_girl in (MC.girls + farm.girls):
                            add ProportionalScale(selected_girl.get_mood_picture(), *res_tb(25)) xalign 0.95 yalign 0.05

                        if badge:
                            add ProportionalScale(badge, *res_tb(25)) xalign 0.95 yalign 0.05

                viewport xmaximum 0.95:
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    ysize yres(220)
                    text selected_girl.get_personality_description(pers_showing) size res_font(14) color c_brown

screen notebook():
    key "mouseup_3" action (Hide("notebook"), Hide("mood_details"))
    key "noshift_K_n" action (Hide("notebook"), Hide("mood_details"))
    use dark_filter()
    use close(Hide("notebook"))
    use personality_screen()


screen fshow_screen(customers, title, pic, desc, but_caption=_("Next")):

    layer "master"

    use generic_event_screen(title, pic, desc, but_caption)

    frame xsize 0.38 pos (0.12, 0.65):
        has hbox box_wrap True spacing xres(5) box_wrap_spacing yres(3)
        for cust in customers:
            button yalign 0.5 xmargin 0 xpadding 0 ymargin 0 ypadding 0 background None action NullAction() tooltip cust.get_description(""):
                if len(customers) <= 80:
                    add cust.get_pic(*res_tb(30))
                else:
                    add cust.get_pic(*res_tb(24))

screen farm_show_gold(girl, total_cust_budget=1000, income=1200, bonus = 1.0):
    modal True

    key "mouseup_1" action (Hide(), Return())
    key "mouseup_3" action (Hide(), Return())

    if total_cust_budget > income:
        default _col = c_lightred
    else:
        default _col = c_lightgreen

    frame align 0.5, 0.5 background c_ui_darkblue left_padding xres(30):
        
        has vbox spacing yres(24) align 0.5, 0.5 xsize 0.3

        text (_("%s's farm show is over") % girl.fullname) bold True size res_font(24) align 0.5, 0.5
        fixed fit_first True xsize 0.7 xalign 0.5:
            add "tanuki" fit "contain"
        hbox spacing xres(24) align 0.5, 0.5:
            text (_("Customer tips (%i%%): ") % (bonus*100)) bold True size res_font(24) align 0.5, 0.5
            use increment_counter(startv = total_cust_budget, stopv = income, duration = 3.0, _caption = "%s gold", _background = None, _size = 24, _color = _col)


screen generic_event_screen(title, pic, desc, but_caption=_("Next")):

    layer "master"

    modal True
    key "mouseup_3" action Return()

    frame xsize 0.8 ysize 0.8 align 0.5, 0.5 background Frame("resources/ui/papersquare.webp", left=12, right=12, top=12, bottom=12) xpadding xres(20) ypadding yres(30):

        has vbox spacing yres(12) xfill True yfill True

        text title color c_white xalign 0.5 font "resources/fonts/MATURASC.ttf" drop_shadow (2, 2) size res_font(32)

        hbox spacing xres(20):
            frame xmaximum 0.5 xpadding xres(3):
                fixed fit_first True:
                    if isinstance(pic, Picture):
                        add pic.get() xalign 0.5 fit "contain"
                    else:
                        add pic xalign 0.5 fit "contain"
                    button xalign 0.0 xmargin xres(2) action NullAction() hovered Show("show_event", event_pic=pic) unhovered Hide("show_event"):
                        add "resources/ui/glass.webp" size res_tb(20)

            vbox xfill True yfill True:
                frame background c_ui_light_solid + "AA" xpadding xres(6) ymargin yres(3) xfill True:
                    text desc color c_brown size res_font(18)

                textbutton but_caption xalign 1.0 yalign 1.0 action Return()


screen mood_details(girl):

    frame:
        background c_ui_darker
        xalign 0.5
        yalign 0.2
        xpadding 0.05
        ypadding 0.05
        xfill True
        xmaximum xres(350)
        ymaximum int(0.5*config.screen_height)

        has vbox

        xfill True

        spacing 6

        text __("%s's mood") % girl.name color c_orange xalign 0.5

        text "" size res_font(6)

        $ love_text, fear_text, mood_text, mood_change_text, mood_factors = girl.get_mood_description()

#        text love_text size res_font(14)

#        text fear_text size res_font(14)

#        text "" size res_font(6)

        text mood_text + mood_change_text size res_font(14)

        # text mood_change_text size res_font(14)

        text "" size res_font(6)

        text mood_factors size res_font(12) color c_white

        if persistent.sanity_display or girl in farm.girls:
            text (_("Current sanity: %s") % girl.get_sanity()) size res_font(14)

screen love_button(girl):

    $ ttip = girl.get_mood_description("love")

    # if debug_mode:
    $ ttip += "\n(" + str(round(girl.get_love(), 1)) + ")"

    button xmargin 0 xpadding 0 xalign 0.5 yalign 0.5:
        background None
        action NullAction()
        tooltip ttip
        at alpha_transform

        $ l = girl.get_love()

        if l >= 5:

            $ h = l // 2.5 + yres(10)

            add ProportionalScale("resources/ui/heart.webp", h, h) xalign 0.5 yalign 0.5 # idle_alpha 0.66 hover_alpha 0.8

        elif l <= -5:
            $ h = l // -2.5 + yres(10)
            add ProportionalScale("resources/ui/broken heart.webp", h, h) xalign 0.5 yalign 0.5 # idle_alpha 0.66 hover_alpha 0.8

        else:
            add ProportionalScale("resources/ui/love question.webp", *res_tb(20)) xalign 0.5 yalign 0.5 # idle_alpha 0.66 hover_alpha 0.8

screen fear_button(girl):

    $ ttip = girl.get_mood_description("fear")

    # if debug_mode:
    $ ttip += "\n(" + str(round(girl.get_fear(), 1)) + ")"

    button xmargin 0 xpadding 0 xalign 0.0 yalign 0.5:
        background None
        action NullAction()
        tooltip ttip
        at alpha_transform

        $ f = girl.get_fear()

        if f >= 5:

            $ h = f // 2.5 + yres(10)

            add ProportionalScale("resources/ui/skull.webp", h, h) xalign 0.5 yalign 0.5 # idle_alpha 0.66 hover_alpha 0.8

        elif f <= -5:
            $ h = f // -2.5 + yres(10)

            add ProportionalScale("resources/ui/droplet.webp", h, h) xalign 0.5 yalign 0.5 # idle_alpha 0.66 hover_alpha 0.8

        else:
            add ProportionalScale("resources/ui/fear question.webp", *res_tb(20)) xalign 0.5 yalign 0.5 # idle_alpha 0.66 hover_alpha 0.8

screen sex_details(girl):

    frame:
        background c_ui_darker
        xalign 0.5
        yalign 0.8

        has vbox

        spacing 6

        text __("%s's sexual preferences") % girl.name xalign 0.5 color c_orange

        text "" size res_font(6)

        grid 4 8 spacing 6:

            text __("Act") size res_font(14) bold True
            text __("Preference") size res_font(14) bold True
            text __("Will train") size res_font(14) bold True xalign 0.5
            text __("Will work") size res_font(14) bold True xalign 0.5

            for act in extended_sex_acts:
                text act.capitalize() size res_font(14) bold True

                if debug_mode:
                    $ text1 = " (" + str(round_int(girl.preferences[act])) + ")"
                else:
                    $ text1 = ""

                if girl.personality_unlock[act]:
                    text (preference_color[girl.get_preference(act)] % girl.get_preference(act).capitalize()) + text1 size res_font(14)
                else:
                    text (_("Unknown") + text1) size res_font(14) italic True

                if girl.personality_unlock[act]:

                    $ tch = girl.get_training_chance(act)

                    text str(round_int(tch)) + "%" size res_font(14) xalign 0.5:
                        if tch > 95:
                            color color_dict["+++"]
                        elif tch > 80:
                            color color_dict["++"]
                        elif tch > 66:
                            color color_dict["+"]
                        elif tch > 50:
                            color color_dict["normal"]
                        elif tch > 33:
                            color color_dict["-"]
                        elif tch > 20:
                            color color_dict["--"]
                        elif tch <= 5:
                            color color_dict["---"]

                else:
                    text "?" size res_font(14) xalign 0.5


                if act == "naked":
                    text "" size res_font(14) xalign 0.5

                elif girl.personality_unlock[act]:

                    if girl.will_do_sex_act(act):

                        $ wch = girl.get_working_chance(act)

                        text str(round_int(wch)) + "%"  size res_font(14) xalign 0.5:
                            if wch > 95:
                                color color_dict["+++"]
                            elif wch > 80:
                                color color_dict["++"]
                            elif wch > 66:
                                color color_dict["+"]
                            elif wch > 50:
                                color color_dict["normal"]
                            elif wch > 33:
                                color color_dict["-"]
                            elif wch > 20:
                                color color_dict["--"]
                            elif wch <= 5:
                                color color_dict["---"]

                    else:
                        text "0%" size res_font(14) xalign 0.5 color color_dict["---"]

                else:
                    text "?" size res_font(14) xalign 0.5
