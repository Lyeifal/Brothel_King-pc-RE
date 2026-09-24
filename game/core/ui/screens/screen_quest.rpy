#### Screen Quest — Postings, challenges and interactions | 任务/挑战/互动界面 ####
# Phase 2: 任务/挑战/互动/mod
# Contains: screen active_spells, screen spellbook, screen postings, screen challenge_menu, screen challenge, screen letter, screen modal, screen invisible_button, screen mods, screen free_girl_interact, screen girl_interact, screen free_girl_stats, screen debug_pics, screen girl_mix, screen pic_tester
# Extracted from ui/screens.rpy on 2026-09-10

screen active_spells():

    hbox box_wrap True:
        text _("Active:") size res_font(14) color c_brown yalign 0.5
        for spell in MC.active_spells:
            button xpadding 0 ypadding 0 xsize xres(40) ysize yres(40) action NullAction() tooltip __("{b}%s{/b}: %s") % (spell.name, spell.description): # get_description("", spell.effects):
                add spell.pic.get(*res_tb(30)) xalign 0.5 yalign 0.5

screen spellbook():

    modal True
    zorder 5

    key "mouseup_3" action (Hide("spellbook"), SetVariable("show_spellbook", False)) capture True

#    use dark_filter

    textbutton _("%s's Spellbook") % MC.name yalign 0.1 xalign 0.5

    fixed xalign 0.5 yalign 0.5:
        fit_first True

        add "resources/ui/spellbook.webp" fit "contain"

        frame xalign 0.95 yalign 0.05:
            use close((Hide("spellbook"), SetVariable("show_spellbook", False)))

        if MC.known_spells:
            frame xalign 0.5 yalign 0.05:
                text _("Right-click on a spell to set-up auto-cast") size res_font(14) color c_brown

            frame ypadding yres(66) xfill True yfill True background None:
                viewport:
                    xalign 0.5
                    yalign 0.0
                    xsize 0.95
                    ysize 0.95
                    mousewheel True
                    draggable True
                    scrollbars "vertical"

                    fixed xalign 1.0 ysize yres(80) * round_up(len(MC.known_spells)/2.0):

                        $ x = 0
                        $ y = 0
                        $ i = 0

                        for s in MC.known_spells:
                            if s.type != "passive":

                                if s in MC.active_spells and s.auto:
                                    $ col = c_darkpurple
                                    $ extra = __("(Auto-cast: %s)\n(Active)") % __(s.auto.capitalize())

                                elif s.auto:
                                    $ col = c_firered
                                    $ extra = __("(Auto-cast: %s)") % __(s.auto.capitalize())

                                elif s in MC.active_spells:
                                    $ col = c_main
                                    $ extra = __("(Active)")

                                else:
                                    $ col = False
                                    $ extra = ""

                                button:
                                    xpos x + xres(80)
                                    ypos y
                                    xsize xres(220)
                                    ysize yres(80)
                                    xfill True
                                    xanchor 0.0
                                    xpadding 3
                                    xmargin 0

                                    if col:
                                        background col

                                    action Return((s, "cast"))

                                    alternate Function(MC.toggle_auto_spell, s) #ToggleField(s, "auto")

                                    tooltip s.description

                                    hbox spacing 3 xalign 0.0 yfill True:

                                        frame background None xsize xres(60) yfill True xmargin 6:
                                            add s.pic.get(*res_tb(50)) xalign 0.5 yalign 0.5


                                        vbox yalign 0.5:

                                            text s.name size res_font(14) bold True

                                            hbox:
                                                text str(s.get_cost()) size res_font(14)

                                                add ProportionalScale("resources/ui/mana.webp", *res_tb(15))

                                                if s.duration == "turn":

                                                    text _("/night") size res_font(14)

                                            if extra:
                                                text extra size res_font(14)

                                if i%2:
                                    $ x = 0
                                    $ y += yres(80)
                                else:
                                    $ x = yres(500)

                                $ i += 1

        else:
            textbutton __("{i}You do not know any spells yet. You must increase your level.{/i}") xalign 0.5 yalign 0.5 xsize xres(250) text_size res_font(18)

    if MC.active_spells:
        frame xalign 0.5 yalign 0.95 xmaximum 0.85 xpadding 20:
            use active_spells()


screen postings(qlist):

    key "mouseup_3" action ((SetVariable("selected_destination", "main"), Jump("teleport")))
    use shortcuts()
    use close((SetVariable("selected_destination", "main"), Jump("teleport")))
    use overlay("postings")

    if qlist:
        key "K_UP" action SetVariable("selected_quest", get_previous(qlist, selected_quest))
        key "K_DOWN" action SetVariable("selected_quest", get_next(qlist, selected_quest))

    if not selected_quest and qlist:
        $ selected_quest = qlist[0]
    elif not qlist:
        $ selected_quest = None

    default clicked_quest = selected_quest

    hbox:

        ypos 0.1
        yfill False

        if selected_girl:
            use girl_stats(selected_girl, context = "postings")

        vbox:
            xsize 0.5


            frame:
                xsize int(0.5*config.screen_width)
                ysize 0.7

                xpadding 10

                has vbox

                spacing 3

                if selected_quest:

                    hbox:
                        spacing 0
                        xalign 0.0

                        if selected_quest.special:
                            textbutton _("{image=img_star} %s {image=img_star}") % __(selected_quest.special) xalign 0.0 yalign 0.5 ypadding 0 text_color c_orange background None action NullAction() hovered tt.Action(special_quest_description[selected_quest.special])

                        text selected_quest.name xalign 0.0 yalign 0.5 color c_prune

                    hbox:
                        spacing 10

                        frame:
                            xmaximum xres(360)
                            ysize yres(480)
                            background None

                            if selected_quest.pic:
                                add selected_quest.pic.get(xres(350), yres(480)) xalign 0.0 yalign 0.0

                        vbox xfill True:

                            text selected_quest.description size res_font(14) color c_brown

                            text "" size res_font(18)

                            text _("Duration") size res_font(18) color c_prune

                            text __("%s days") % str(selected_quest.duration) size res_font(14) color c_brown

                            text "" size res_font(18)

                            if selected_quest.type == "class":
                                button style "inv_no_padding" action NullAction() tooltip (_("Current discount: %i%%") % (len(selected_quest.enrolled)*-100*class_discount)):
                                    has vbox
                                    text _("Cost") size res_font(18) color c_prune

                                    if not story_flags["postings free class"]:
                                        text __("%s gold") % str(int(selected_quest.get_gold())) size res_font(14) color c_brown
                                    else:
                                        text _("FREE") size res_font(14) color c_orange

                                text "" size res_font(18)

                                button style "inv_no_padding" action NullAction() tooltip (_("Price drops by %i%% for each girl enrolling after the first") % (100*class_discount)):
                                    has vbox
                                    text _("Enrolled") size res_font(18) color c_prune

                                    text __("%s/%s girls") % (str(len(selected_quest.enrolled)), str(selected_quest.capacity)) size res_font(14) color c_brown

                                text "" size res_font(18)

                                text _("Skill gains") size res_font(18) color c_prune

                                for stat, _min, _max in selected_quest.bonuses:

                                    if _max >= 12:
                                        $ t = "+++"

                                    elif _max >= 6:
                                        $ t = "++"

                                    else:
                                        $ t = "+"

                                    text "[stat!t]" + " " + t size res_font(14) color c_brown

                                textbutton _("\nMax skill: %s") % selected_quest.stat_cap text_size res_font(14) text_color c_brown xalign 0.0 yalign 0.5 xpadding 0 ypadding 0 background None:
                                    action NullAction()
                                    tooltip _("Classes may cause a girl's skills to exceed their level cap.")

                                text "" size res_font(18)
                                text _("JP bonus") size res_font(18) color c_prune
                                textbutton __(selected_quest.jp_target.capitalize()) text_size res_font(14) text_color c_brown xalign 0.0 yalign 0.5 xpadding 0 ypadding 0 background None:
                                    action NullAction()
                                    tooltip __("This class will give a small boost to %s Job Points (JP).") % selected_quest.jp_target


                            elif selected_quest.type == "quest":

                                text _("Reward") size res_font(18) color c_prune

                                text __("%s gold") % str(selected_quest.get_gold()) size res_font(14) color c_brown

                                text "" size res_font(18)

                                text _("Requirements") size res_font(18) color c_prune

                                for stat, val in selected_quest.requirements:

                                    text "[stat!t]" + " " + str(val) size res_font(14) color c_brown

                                text "" size res_font(18)

                                if selected_quest.pos_traits:

                                    text _("Desirable") size res_font(18) color c_prune

                                    text selected_quest.pos_traits[0].display_name + ", " + selected_quest.pos_traits[1].display_name size res_font(14) color c_emerald

                                    text "" size res_font(18)

                                if selected_quest.neg_trait:

                                    text _("Undesirable") size res_font(18) color c_prune

                                    text selected_quest.neg_trait.display_name size res_font(14) color c_crimson

                else:
                    text _("No task is currently available.") italic True color c_brown size res_font(18)

            fixed xalign 0.5:
                fit_first True

                if selected_quest:

                    $ available_girls = [g for g in MC.girls if selected_quest.test_eligibility(g)[0]]

                    if selected_girl:
                        $ r, ttip = selected_quest.test_eligibility(selected_girl)

                        if r: # or debug_mode:
                            use girl_select(available_girls, action_button = (__("Commit"), (SetScreenVariable("clicked_quest", None), Return("commit")), ttip))
                        else:
                            use girl_select(available_girls, action_button = (__("Commit"), NullAction(), ttip))


        vbox:
            yalign 0.0
            xfill False
            yfill False


            frame:

                xalign 0.0
                yalign 0.0
                xmargin 3
                xpadding 6
                xfill False
                yfill False
                ysize int(0.7*config.screen_height)

                has vbox

                hbox:

                    textbutton _("Quests") text_size res_font(14) xsize xres(80) xfill True style "posting_button" action (Return("quests"), SelectedIf(qlist == quest_board.quests))
                    textbutton _("Classes") text_size res_font(14) xsize xres(80) xfill True style "posting_button" action (Return("classes"), SelectedIf(qlist == quest_board.classes))


                if qlist:
                    viewport:
                        xalign 0.0
                        yalign 0.0
                        xfill False
                        mousewheel True
                        draggable True
                        scrollbars "vertical"

                        vbox xfill False:
                            spacing 1

                            for quest in qlist:

                                $ ttip = ""

                                if quest.type == "quest":

                                    $ ttip = __("This task requires %s.\n") % and_text([stat for stat, v in quest.requirements])
                                    $ ttip += __("%s girls can complete this task.") % str(quest.count_eligible_girls())

                                elif quest.type == "class":

                                    $ ttip = __("This class may improve {b}%s{/b}.\n") % and_text([stat for stat, _min, _max in quest.bonuses])
                                    $ ttip += __("%s/%s are enrolled in this class") % (str(len(quest.enrolled)), str(quest.capacity))
                                    if quest.enrolled:
                                        $ ttip += __(" (%i%% discount).") % (len(quest.enrolled)*-100*class_discount)
                                    else:
                                        $ ttip += "."

                                button:
                                    xsize xres(160)
                                    ysize yres(60)
                                    xmargin 0
                                    xpadding 0
                                    ypadding 0
                                    action (SetVariable("selected_quest", quest), SetScreenVariable("clicked_quest", quest), Return("change"), SelectedIf(clicked_quest == quest))

                                    if persistent.hover_for_preview_postings:
                                        hovered (SetVariable("selected_quest", quest), Return("change"))
                                        unhovered (SetVariable("selected_quest", clicked_quest), Return("change"))

                                    tooltip ttip

                                    hbox spacing xres(5) xalign 0.0 yalign 0.5:

                                        fixed xsize xres(50) ysize yres(50) yalign 0.5:
                                            if quest.pic:
                                                add quest.pic.get(*res_tb(45)) xalign 0.5 yalign 0.5

                                        vbox xalign 0.0 yalign 0.5:
                                            if quest.special:
                                                $ text1 = "{image=img_star}"
                                            else:
                                                $ text1 = ""
                                            text text1 + "[quest.name!t]"  size res_font(13)
                                            if quest.type != "class" or not story_flags["postings free class"]:
                                                text __("%s gold") % str(int(quest.get_gold())) size res_font(13)
                                            else:
                                                text _("FREE") size res_font(13)

                if calendar.active_contract:
                    text ""
                    text ""
                    button xfill True xpadding 6 ypadding 6 action Return("active_contract"): # hovered Show("contract_tab", contract=calendar.active_contract, x=450, active=True, transition=Dissolve(0.15)) unhovered Hide("contract_tab", transition=Dissolve(0.15)) tooltip (_("Show active contract (%s day%s left).") % (28-calendar.day, plural(28-calendar.day))):
                        vbox xfill True:
                            text _("Active contract") size res_font(14) color c_darkbrown xalign 0.5
                            add ProportionalScale("resources/ui/" + license_dict[1][1], *res_tb(50)) xalign 0.5


screen challenge_menu(header=_("What do you do?"), challenges=[], cancel=False):
    # challenges is a list of arrays (caption, challenge_type, base_diff) where caption is the text displayed on the button.
    # challenge_type must be an existing type in MC.challenges. base_diff is the lowest possible difficulty to achieve success.
    # cancel must be an array (caption, return_value) if the challenge can be avoided.

    tag challenge_menu

    modal True
    zorder 5

    use overlay()

    frame xalign 0.5 yalign 0.5:

        has vbox spacing 10

        text header xalign 0.5 color c_brown

        hbox:

            for title, challenge_type, diff in challenges:
                $ chal = MC.challenges[challenge_type]
                $ diff = chal.adjust_diff(diff)
                $ ttip = __("{b}%s challenge{/b}: This challenges your {b}%s{/b} (%s). Estimated difficulty: {b}%s{/b}.") % (__(chal.name_i18n), __(chal.stat.capitalize()), str_int(MC.get_stat(chal.stat)), __(chal.estimate_diff(diff=diff)))
                $ diff_label = __(chal.estimate_diff(diff=diff))

                button background None action(Return(challenge_type)):
                    vbox:
                        button:
                            ysize yres(132)
                            yfill True
                            xpadding 6
                            ypadding 6
                            insensitive_background "#1A2B47E5"
                            at alpha_transform
                            action(Return(challenge_type))
                            tooltip ttip

                            fixed yalign 0.5:
                                fit_first True
                                add chal.get_pic(xres(200), yres(120)) # idle_alpha 0.66 hover_alpha 1.0
                                text diff_label size res_font(12)
                                frame background None xpadding 10 xalign 0.5 yalign 0.5:
                                    text title size res_font(18) bold True

        if cancel:
            textbutton cancel[0] action Return(cancel[1]) xalign 0.5

screen challenge(name, diff, raw=False, bonus=0, opponent_bonus=0, bonus_text="", opponent_bonus_text=""): #! Opponent bonus text not done

    tag challenge

    modal True
    zorder 5

    $ chal = MC.challenges[name]

    default phase = 0
    frame background Frame(chal.pic.get(int(0.5*config.screen_width), int(0.5*config.screen_height))) xalign 0.5 yalign 0.5 xsize int(0.5*config.screen_width) ysize int(0.4*config.screen_height) xfill True yfill True:

        has vbox

        frame xalign 0.5 xfill True background "#22222288":
            text __("Player challenge: %s") % __(chal.name_i18n) xalign 0.5

        text ""

        hbox xfill True spacing 10:

            frame background "#22222288" xfill True xsize xres(250) ysize yres(160) xpadding 10 ypadding 10:

                vbox:
                    textbutton __("Player %s: %s") % (__(chal.stat.capitalize()), str_int(MC.get_stat(chal.stat, raw=True))) text_size res_font(18) style "inv_no_padding"
                    textbutton __("Active bonus: ") + str_int(bonus + MC.get_stat(chal.stat, raw) - MC.get_stat(chal.stat, raw=True) + MC.get_effect("change", chal.name + " challenges")) text_size int(config.screen_height*0.0222) style "inv_no_padding" action NullAction() tooltip bonus_text
                    text ""

                    if phase >= 1:
                        text __("Roll: {image=img_dice%s}") % str(chal.d) size res_font(18)
                        text ""

                        if phase >= 2:
                            text __("Final Result: %s") % str(round_int(chal.score)) size res_font(18)

                    elif chal.opposed:
                        textbutton _("Roll") action (SetScreenVariable("phase", 1), Play("sound", s_dice)) tooltip _("Roll the dice")
                    else:
                        textbutton _("Roll") action (SetScreenVariable("phase", 2), Play("sound", s_dice)) tooltip _("Roll the dice")



            frame background "#22222288" xsize xres(250) xfill True ysize yres(160) xalign 1.0 xpadding 6 ypadding 6:
                has vbox

                if chal.opposed:
                    text __("Opponent %s: %s") % (__(chal.stat.capitalize()), str_int(diff + opponent_bonus)) size res_font(18)
                    text "" size res_font(18)
                    text ""

                    if phase >= 2:
                        text __("Roll: {image=img_dice%s}") % str_int(chal.d_op) size res_font(18)
                        text ""
                        text __("Final Result: %s") % str_int(chal.score_op) size res_font(18)
                    elif phase == 1:
                        textbutton __("Roll") action (SetScreenVariable("phase", 2), Play("sound", s_dice)) tooltip _("Roll the opponent's dice")
                else:
                    text __("Difficulty: %s") % str_int(diff) size res_font(18)

        if phase >= 2:
            text ""
            textbutton _("OK") xalign 0.5 action Return()

    use adv_tooltip()

screen letter(header="", message="", signature = ""): # Returns True upon closing

    tag letter

    modal True
    zorder 5

    key "mouseup_3" action (Return(True))

    frame xalign 0.5 ypos 0.1 xsize 0.8 ysize 0.9 xfill True yfill True xpadding 50 ypadding 25 background Frame("resources/ui/paper.webp"):

        has vbox
        xsize 0.75
        xalign 0.5
        ysize 0.9

        hbox xfill True yalign 0.1:
            text header xalign 0.0 size res_font(32) font "resources/fonts/MATURASC.ttf" color c_black
            fixed fit_first True xalign 1.0 yalign 0.5:
                use close(act=Return(True), name = "close")

        text ""
        text ""

        text message size res_font(48) font "SFBurlingtonScript.TTF" color c_black yalign 0.5

        text ""
        text ""

        text signature size res_font(52) font "SFBurlingtonScript.TTF" xalign 1.0 color c_black yalign 0.9


screen modal():

    modal True

screen invisible_button():

    zorder 20

    key "K_UP" action Function(renpy.notify, __("Your precious keyboard can't save you now!"))
    key "K_DOWN" action Function(renpy.notify, __("Your precious keyboard can't save you now!"))

    vbox:
        style "menu"
        xalign 0.5
        xfill True
        yalign 0.5
        yfill True

        textbutton "" xalign 0.5 background None:
            style "menu_choice_button"
        textbutton "" xalign 0.5 background None action NullAction() hovered Function(this_is_a_hentai_game_so_why_are_you_trying_to_act_classy_all_of_a_sudden):
            style "menu_choice_button"


screen mods():

    tag menu

    $ mod_list = list(detected_mods) # Creates a list of keys from the dictionary
    $ mod_list.sort() # Sorts mods by name

    # EN: Mod API v2 mods (always active once installed).
    # ZH: Mod API v2 Mod（安装后常驻激活）。
    $ v2_mod_list = []
    python:
        try:
            v2_mod_list = sorted(services.mod_api_v2.list_active_mods())
        except Exception:
            v2_mod_list = []

    use game_menu(_("Mods")):

        default selected_mod = None
        default selected_v2 = None

        if selected_mod is None and selected_v2 is None:
            if mod_list:
                $ selected_mod = detected_mods[mod_list[0]]
            elif v2_mod_list:
                $ selected_v2 = v2_mod_list[0]

        frame xsize 0.82 xpadding xres(20) ypadding yres(20):

            hbox xfill True spacing xres(6):
                viewport xsize xres(155):
                    mousewheel True
                    scrollbars "vertical"

                    has vbox xfill False

                    text _("Mod List") color c_brown

                    # style_group "pref"

                    for mod_name in mod_list:
                        $ mod = detected_mods[mod_name]
                        if mod:
                            button xsize xres(140) action [SelectedIf(selected_mod == mod), SetScreenVariable("selected_mod", mod), SetScreenVariable("selected_v2", None)] hovered SetField(mod, "seen", True):
                                if not mod.seen:
                                    at blink

                                text mod.name size res_font(18):
                                    if mod.active:
                                        bold True

                    if v2_mod_list:
                        null height yres(12)
                        text _("API v2 Mods") color c_brown size res_font(14)

                        for mod_id in v2_mod_list:
                            button xsize xres(140) action [SetScreenVariable("selected_v2", mod_id), SetScreenVariable("selected_mod", None)]:
                                text mod_id size res_font(16)

                if selected_mod:
                    $ selected_mod.seen = True

                    hbox xfill True spacing xres(6):
                        frame xpadding xres(10) ypadding yres(10):
                            has vbox
                            text selected_mod.full_name size res_font(24) bold True color c_darkorange
                            if selected_mod.active:
                                text _("(Active)") color c_emerald
                            else:
                                text _("(Inactive)") color c_grey

                            null height yres(16)

                            viewport xsize xres(480):
                                mousewheel True
                                draggable True
                                scrollbars "vertical"

                                vbox xfill True:
                                    if selected_mod.pic:
                                        frame xsize xres(250) background None:
                                            add selected_mod.pic.get() fit "contain"

                                    null height yres(16)

                                    text selected_mod.description size res_font(14) color c_brown

                        if selected_mod.active:
                            textbutton _("Deactivate Mod") action renpy.curried_invoke_in_new_context(selected_mod.deactivate) xalign 1.0 xsize xres(100) text_size res_font(24)
                        else:
                            textbutton _("Activate Mod") action renpy.curried_invoke_in_new_context(selected_mod.activate) xalign 1.0 xsize xres(100) text_size res_font(24)

                            # textbutton "Reset Mod" action renpy.curried_invoke_in_new_context(reset_mod, selected_mod)

                elif selected_v2:
                    # EN: Mod API v2 mod details (read-only: always active).
                    # ZH: Mod API v2 Mod 详情（只读：常驻激活）。
                    $ v2_info = services.mod_api_v2.get_mod_info(selected_v2)

                    if v2_info:
                        hbox xfill True spacing xres(6):
                            frame xpadding xres(10) ypadding yres(10):
                                has vbox
                                text v2_info.get("name", selected_v2) size res_font(24) bold True color c_darkorange
                                text _("(Always Active — API v2)") color c_emerald
                                text __("v%s, by %s") % (v2_info.get("version", "?"), v2_info.get("author", __("Unknown"))) size res_font(16) color c_grey

                                null height yres(16)

                                viewport xsize xres(480):
                                    mousewheel True
                                    draggable True
                                    scrollbars "vertical"

                                    vbox xfill True:
                                        text v2_info.get("description", "") size res_font(14) color c_brown


### GIRL INTERACT SCREEN

screen free_girl_interact(girl):

    tag girl_interact

    use dark_filter()
    use overlay(current_screen = "location")
    use shortcuts()
    use girl_stats(girl, "free")
    use girl_profile(girl, "free")

    key "mouseup_3" action (Return("back"))
    use close(Return("back"))

    default menu_choice = last_free_interact_menu

    frame:
        background c_ui_darkblue
        xsize xres(325)
        ysize int(0.7*config.screen_height)
        xmargin 3
        xalign 1.0
        ypos 0.1

        has vbox spacing 3

        text _("City girl interactions") size res_font(18) bold True

        text "" size res_font(14)

        hbox box_wrap True:
            $ choices = ["chat", "give", "flirt", "fun"]

            for cap in choices:
                textbutton __(cap.capitalize()) action SelectedIf(menu_choice == cap) hovered SetScreenVariable("menu_choice", cap) text_size res_font(14) xpadding 6 ypadding 6 text_selected_bold True xsize xres(60)

        for cat in free_interact_dict[menu_choice]:

            if [top for top in free_interact_dict[cat] if top.is_shown(girl)]:

                text "" size res_font(18)
                text __(cat) size res_font(14)

            for topic in free_interact_dict[cat]:
                if topic.is_shown(girl):
                    $ text1 = " ([topic.AP_cost]{image=img_AP})"

                    textbutton __("%s%s") % (topic.caption, text1) background None ypadding yres(0) text_size res_font(16):
                        if topic.is_available(girl)[0]:
                            action Return(topic)
                            text_hover_underline True
                        else:
                            text_color c_grey
                            action NullAction()
                        if topic.is_available(girl)[1]:
                            tooltip topic.is_available(girl)[1]

# This code could be used for future custom city dialogue in _BK.ini

#        if menu_choice == "misc" and girl.init_dict["background story/free_interact_prompt"]:
#            text ""
#            text "OTHER" size res_font(14)

#            python:
#                try:
#                    custom_caption, custom_option_label, custom_cost = girl.init_dict["background story/free_interact_prompt"]
#                except:
#                    custom_caption, custom_option_label = girl.init_dict["background story/free_interact_prompt"] # For backwards compatibility with older _BK.ini
#                    custom_cost = 0
#                topic = GirlInteractionTopic("misc", None, custom_caption, "slave_custom_option", AP_cost=custom_cost)

#            textbutton topic.caption + " ([topic.AP_cost]{image=img_AP})" background None text_size res_font(14):
#                if topic.is_available(girl)[0]:
#                    action Return(topic)
#                    text_hover_underline True
#                else:
#                    text_color c_grey
#                    action NullAction()
#                    tooltip topic.is_available(girl)[1]

screen girl_interact(girl, free=False):

    tag girl_interact

    use overlay(current_screen = "girls")
    use girl_stats(girl, "girls")
    use girl_profile(girl, "girls")

    if not free:
        use shortcuts()

    key "mouseup_3" action (Return("back"))
    use close(Return("back"))

    key "K_LEFT" action Return("previous")
    key "K_RIGHT" action Return("next")

    default menu_choice = last_interact_menu

    if free:
        $ normal_cost = 0
        $ adv_cost = 0
    else:
        $ normal_cost = 1
        $ adv_cost = 2

    frame:
        background c_ui_darkblue
        xsize xres(325)
        ysize int(0.7*config.screen_height)
        xmargin 0
        xalign 1.0
        ypos 0.1

        has vbox spacing 3

        text _("Girl interactions") size res_font(18) bold True
#        text "Every interaction costs 1 AP" size res_font(14) italic True
        text "" size res_font(14)

        hbox box_wrap True:
            if free:
                $ choices = ["train", "magic"]
                if menu_choice not in choices:
                    $ menu_choice = "train"
            else:
                $ choices = ["chat", "train", "magic", "react", "misc"]

            for cap in choices:
                textbutton __(cap.capitalize()) action SelectedIf(menu_choice == cap) hovered SetScreenVariable("menu_choice", cap) text_size res_font(14) xpadding 6 ypadding 6 text_selected_bold True xsize xres(60)

        vbox xpos xres(12):
            for cat in interact_dict[menu_choice]:

                if [top for top in interact_dict[cat] if top.is_shown(girl)]:

                    null height yres(16)
                    text __(cat) size res_font(14) bold True

                for topic in interact_dict[cat]:
                    if topic.is_shown(girl):

                        if topic.advanced:
                            hbox spacing 0:

                                textbutton __("%s%s") % (topic.caption, get_act_weakness_symbol(girl, topic.act)) background None text_layout "nobreak" text_size res_font(13) text_color c_white xsize xres(100) text_xalign 0.0 action NullAction():
                                    if girl.personality_unlock[topic.act]:
                                        tooltip __("You know that [girl.name] has %s for %s acts.") % (girl.get_reaction_to_act(topic.act), topic.act)
                                    else:
                                        tooltip __("You do not know [girl.name]'s reaction to %s acts.") % topic.act
                                    hovered Show("sex_details", girl=girl)
                                    unhovered Hide("sex_details")

                                if topic.type == "train":
                                    textbutton _("Talk") background None text_size res_font(13):
                                        if topic.is_available(girl, "lecture", free)[0]:
                                            text_hover_underline True
                                            action Return([topic, "lecture"])
                                            tooltip __("Lecture [girl.name] about the virtues of %s acts (soft).\nCosts {image=img_AP} %i.") % (topic.act, normal_cost)
                                        else:
                                            text_color c_grey
                                            action NullAction()
                                            tooltip topic.is_available(girl, "lecture", free)[1]

                                textbutton _("Train") background None text_size res_font(13):
                                    if topic.is_available(girl, "train", free)[0]:
                                        text_hover_underline True
                                        action Return([topic, "train"])
                                        if topic.gold_cost:
                                            tooltip __("Train [girl.name] for %s acts.\nCosts {image=img_AP} %i and {image=img_gold} %i.") % (topic.act, normal_cost, topic.get_gold_cost())
                                        elif topic.base_MP_cost:
                                            tooltip __("Train [girl.name] for %s acts.\nCosts {image=img_AP} %i and {image=img_MP} %i.") % (__(topic.act), normal_cost, topic.get_MP_cost(girl))
                                        else:
                                            tooltip __("Train [girl.name] for %s acts.\nCosts {image=img_AP} %i.") % (__(topic.act), normal_cost)
                                    else:
                                        text_color c_grey
                                        action NullAction()
                                        tooltip topic.is_available(girl, "train", free)[1]

                                $ pos_reaction, neg_reaction = girl.test_weakness(topic.act)

                                if not (pos_reaction or neg_reaction):
                                    $ ttip = event_color["a little bad"] % __("Advanced training is available, but she isn't particularly sensitive to this sex act.")
                                else:
                                    $ ttip = __("You can use advanced training to find out more about her fixations and use them for faster training.")

                                textbutton _("Advanced") background None text_size res_font(13):
                                    if topic.is_available(girl, "advanced", free)[0]:
                                        text_hover_underline True
                                        action Return([topic, "advanced"])
                                        if topic.gold_cost:
                                            tooltip (ttip + _("\nCosts {image=img_AP} %i and {image=img_gold} %i.") % (adv_cost, topic.get_gold_cost()))
                                        elif topic.base_MP_cost:
                                            tooltip (ttip + _("\nCosts {image=img_AP} %i and {image=img_MP} %i.") % (adv_cost, topic.get_MP_cost(girl)))
                                        else:
                                            tooltip (ttip + _("\nCosts {image=img_AP} %i.") % adv_cost)
                                    else:
                                        text_color c_grey
                                        action NullAction()
                                        tooltip topic.is_available(girl, "advanced", free)[1]
                        else:
                            if topic.label == "slave_hypnotize_method":
                                $ text1 = __(": %s") % __(girl.magic_training.capitalize())
                            elif topic.label == "slave_hypnotize_driver":
                                if MC.hypnotize_driver == "gold":
                                    $ text1 = __(" %s {image=img_gold}") % __(MC.hypnotize_driver)
                                elif MC.hypnotize_driver == "mana":
                                    $ text1 = __(" %s {image=img_MP}") % __(MC.hypnotize_driver)
                            else:
                                $ text1 = ""

                            if free or topic.AP_cost == 0:
                                # $ text1 += " ({image=img_AP} 0"
                                $ text1 += ""
                            else:
                                $ text1 += " ({image=img_AP} [topic.AP_cost]"
                            if topic.gold_cost:
                                $ text1 += ", {image=img_gold} %i" % topic.get_gold_cost()
                            if topic.base_MP_cost:
                                $ text1 += ", {image=img_MP} %i" % topic.get_MP_cost(girl)
                            
                            if free or topic.AP_cost or topic.gold_cost or topic.base_MP_cost:
                                $ text1 += ")"

                            textbutton __("%s%s") % (topic.caption, text1) background None ypadding yres(3) text_size res_font(16):
                                if topic.is_available(girl, free=free)[0]:
                                    action Return(topic)
                                    text_hover_underline True
                                else:
                                    text_color c_grey
                                    action NullAction()
                                tooltip topic.is_available(girl, free=free)[1]

            if menu_choice == "misc" and girl.init_dict["background story/interact_prompt"]:
                text ""
                text _("OTHER") size res_font(14)

                python:
                    custom_caption = girl.init_dict["background story/interact_prompt"][0]
                    try:
                        custom_cost = girl.init_dict["background story/interact_prompt"][2]
                    except:
                        custom_cost = 0 # For backwards compatibility with older _BK.ini

                    topic = GirlInteractionTopic("misc", None, custom_caption, "slave_custom_option", AP_cost=custom_cost)

                textbutton __("%s ([topic.AP_cost]{image=img_AP})") % topic.caption background None text_size res_font(16):
                    if topic.is_available(girl)[0]:
                        action Return(topic)
                        text_hover_underline True
                    else:
                        text_color c_grey
                        action NullAction()
                        tooltip topic.is_available(girl)[1]

screen free_girl_stats(girl):

    modal True

    use girl_stats(girl, context="free")
    use button_overlay(girl, context="free")
    use close(Return())
    key "mouseup_3" action (Return())

screen debug_pics(girl):

    modal True

    default mode = "soft"
    default pic = girl.profile

    key "mouseup_3" action Return()

    use dark_filter
    use show_sex_event(pic)

    vbox xalign 1.0 xfill False:

        hbox:
            textbutton _("SOFT") text_size res_font(18) action SetScreenVariable("mode", "soft")
            textbutton _("HARD") text_size res_font(18) action SetScreenVariable("mode", "hard")
            textbutton _("FARM") text_size res_font(18) action SetScreenVariable("mode", "farm")
            textbutton _("FIX") text_size res_font(18) action SetScreenVariable("mode", "fix")

        viewport xalign 1.0 xsize xres(250):
            mousewheel True
            draggable True
            scrollbars "vertical"

            has vbox xalign 1.0 xfill False

            if mode == "soft":

                textbutton _("Portrait") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("portrait", "profile", not_tags=["naked"]))
                textbutton _("Portrait Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("portrait", "profile", and_tags=["naked"]))
                textbutton _("Profile") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("profile", "portrait", not_tags=["naked"]))
                textbutton _("Profile Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("profile", "portrait", and_tags=["naked"]))

                textbutton _("Rest") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("rest", "profile", not_tags=["naked"], soft=True))
                textbutton _("Rest Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("rest", "profile", and_tags=["naked"], soft=True))
                textbutton _("Waitress") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["waitress_tags"], perform_job_dict["waitress_tags2"], not_tags=["naked", "monster", "beast"], soft=True))
                textbutton _("Waitress Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["waitress_tags"], perform_job_dict["waitress_tags2"], and_tags=["naked"], not_tags=["monster", "beast"], soft=True))
                textbutton _("Dancer") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["dancer_tags"], perform_job_dict["dancer_tags2"], not_tags=["naked", "monster", "beast"], soft=True))
                textbutton _("Dancer Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["dancer_tags"], perform_job_dict["dancer_tags2"], and_tags=["naked"], not_tags=["monster", "beast"], soft=True))
                textbutton _("Masseuse") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["masseuse_tags"], perform_job_dict["masseuse_tags2"], not_tags=["naked", "monster", "beast"], soft=True))
                textbutton _("Masseuse Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["masseuse_tags"], perform_job_dict["masseuse_tags2"], and_tags=["naked"], not_tags=["monster", "beast"], soft=True))
                textbutton _("Geisha") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["geisha_tags"], perform_job_dict["geisha_tags2"], not_tags=["naked", "monster", "beast"], soft=True))
                textbutton _("Geisha Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["geisha_tags"], perform_job_dict["geisha_tags2"], and_tags=["naked"], not_tags=["monster", "beast"], soft=True))

                for k, tags in farm_holding_tags.items():
                    textbutton __(k.capitalize()) text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(farm_holding_tags[k], soft=True))

            elif mode == "hard":

                textbutton _("Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("naked", "rest", "profile", not_tags=["monster", "beast", "machine", "group", "bisexual"]))
                textbutton _("Service") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["service_tags"], "naked", "rest", "profile", not_tags=["monster", "beast", "machine", "group", "bisexual"]))
                textbutton _("Sex") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["sex_tags"], not_tags=["monster", "beast", "machine", "group", "bisexual"]))
                textbutton _("Anal") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["anal_tags"], not_tags=["monster", "beast", "machine", "group", "bisexual"]))
                textbutton _("Fetish") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["fetish_tags"], not_tags=["monster", "beast", "group", "bisexual"]))
                textbutton _("Bisexual Service") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["bisexual_tags"], perform_job_dict["service_tags"], and_tags= ["service"], not_tags=["monster", "beast", "machine", "group"], and_priority=False))
                textbutton _("Bisexual Sex") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["bisexual_tags"], perform_job_dict["sex_tags"], and_tags= ["sex"], not_tags=["monster", "beast", "machine", "group"], and_priority=False))
                textbutton _("Bisexual Anal") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["bisexual_tags"], perform_job_dict["anal_tags"], and_tags= ["anal"], not_tags=["monster", "beast", "machine", "group"], and_priority=False))
                textbutton _("Bisexual Fetish") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["bisexual_tags"], perform_job_dict["fetish_tags"], and_tags= ["fetish"], not_tags=["monster", "beast", "group"], and_priority=False))
                textbutton _("Group Service") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["group_tags"], perform_job_dict["service_tags"], and_tags= ["service"], not_tags=["monster", "beast", "machine"], and_priority=False))
                textbutton _("Group Sex") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["group_tags"], perform_job_dict["sex_tags"], and_tags= ["sex"], not_tags=["monster", "beast", "machine"], and_priority=False))
                textbutton _("Group Anal") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["group_tags"], perform_job_dict["anal_tags"], and_tags= ["anal"], not_tags=["monster", "beast", "machine"], and_priority=False))
                textbutton _("Group Fetish") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(perform_job_dict["group_tags"], perform_job_dict["fetish_tags"], and_tags= ["fetish"], not_tags=["monster", "beast"], and_priority=False))

            elif mode == "farm":

                textbutton _("Stallion Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("naked", and_tags = ["big"], not_tags=["monster", "beast", "machine"]))
                textbutton _("Stallion Service") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("service", and_tags = ["big"], not_tags=["monster", "beast", "machine"]))
                textbutton _("Stallion Sex") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("sex", and_tags = ["big"], not_tags=["monster", "beast", "machine"]))
                textbutton _("Stallion Anal") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("anal", and_tags = ["big"], not_tags=["monster", "beast", "machine"]))
                textbutton _("Stallion Fetish") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("fetish", and_tags = ["big"], not_tags=["monster", "beast"]))
                textbutton _("Stallion Bisexual") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("bisexual", and_tags = ["big"], not_tags=["monster", "beast", "machine"]))
                textbutton _("Stallion Group") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("group", and_tags = ["big"], not_tags=["monster", "beast", "machine"]))

                textbutton _("Beast Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("beast", and_tags = ["naked"]))
                textbutton _("Beast Service") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("beast", and_tags = ["service"]))
                textbutton _("Beast Sex") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("beast", and_tags = ["sex"]))
                textbutton _("Beast Anal") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("beast", and_tags = ["anal"]))
                textbutton _("Beast Fetish") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("beast", and_tags = ["fetish"]))
                textbutton _("Beast Bisexual") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("beast", and_tags = ["bisexual"]))
                textbutton _("Beast Group") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("beast", and_tags = ["group"]))

                textbutton _("Monster Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("monster", and_tags = ["naked"]))
                textbutton _("Monster Service") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("monster", and_tags = ["service"]))
                textbutton _("Monster Sex") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("monster", and_tags = ["sex"]))
                textbutton _("Monster Anal") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("monster", and_tags = ["anal"]))
                textbutton _("Monster Fetish") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("monster", and_tags = ["fetish"]))
                textbutton _("Monster Bisexual") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("monster", and_tags = ["bisexual"]))
                textbutton _("Monster Group") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic("monster", and_tags = ["group"]))

                textbutton _("Machine Naked") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(["machine", "toy"], and_tags = ["naked"]))
                textbutton _("Machine Service") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(["machine", "toy"], and_tags = ["service"]))
                textbutton _("Machine Sex") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(["machine", "toy"], and_tags = ["sex"]))
                textbutton _("Machine Anal") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(["machine", "toy"], and_tags = ["anal"]))
                textbutton _("Machine Fetish") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(["machine", "toy"], and_tags = ["fetish"]))
                textbutton _("Machine Bisexual") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(["machine", "toy"], and_tags = ["bisexual"]))
                textbutton _("Machine Group") text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(["machine", "toy"], and_tags = ["group"]))

            elif mode == "fix":
                for fix in fix_dict.values():

                    for act in fix.acts:
                        if act != "group":
                            $ not_tags.append("group")
                        if act != "bisexual":
                            $ not_tags.append("bisexual")

                        textbutton __(fix.name.capitalize()) + " " + __(act.capitalize()) text_size res_font(14) action SetScreenVariable("pic", girl.get_fix_pic(act, fix, not_tags=not_tags))


screen girl_mix(show_rating=False):

    modal True

    default filter = ""
    default ttip = ""

    key "mouseup_3" action Return()

    $ shown_gp = sorted(persistent.girl_packs, key=lambda x: (-(x in persistent.girl_mix[persistent.active_mix]), x))

    hbox:
        frame xsize 0.7 yfill True:
            has vbox

            text _("Girl Mix") bold True drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" xpos xres(6)

            hbox box_wrap True:
                for mix_name in sorted(persistent.girl_mix):
                    textbutton __(mix_name.capitalize())[:25] action (SetField(persistent, "active_mix", mix_name), SelectedIf(persistent.active_mix==mix_name)) text_size res_font(18) text_selected_bold True tooltip __("Click here to see the %s girl mix.") % mix_name.capitalize()
                textbutton "+" action renpy.curried_invoke_in_new_context(add_mix) text_size res_font(18) tooltip _("Click here to create a new girl mix.")

            text "" size res_font(12)
            text _("Click on a girl's profile to add or remove this girl from the mix.\nYou can create a new mix by clicking '+'") size res_font(14) color c_brown xpos xres(6)

            text "" size res_font(12)

            frame background c_ui_light xfill True:
                has hbox
                text _("Filter: ") size res_font(18) color c_brown
                input value ScreenVariableInputValue("filter", returnable=False) size res_font(18) color c_darkorange

            text "" size res_font(12)

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                ymaximum 0.77
                yfill False

                has vbox spacing 0

                for gp in shown_gp:
                    $ pack_name = get_name(gp, full=True)
                    $ ttip = __("{b}%s{/b} {i}by %s{/i}\n%s\n\nVersion: %s\n\nDescription: %s\n\n") % (pack_name, gpinfo_dict[gp]["creator"], {True: event_color["good"] % __("Unique girl"), False: __("Generic girl")}[gpinfo_dict[gp]["unique"]], gpinfo_dict[gp]["version"], gpinfo_dict[gp]["description"])

                    if filter.lower() in pack_name.lower():
                        if show_rating:
                            $ rating, rtg_text = get_girlpack_rating(path=gp)

                        hbox spacing 12:

                            button xfill True ysize yres(82) ymargin 0 ypadding 0:
                                if gp in persistent.girl_mix[persistent.active_mix]:
                                    action RemoveFromSet(persistent.girl_mix[persistent.active_mix], gp)
                                    tooltip ttip + __("{i}Click to remove this girl pack from the mix.{/i}")
                                else:
                                    idle_background None
                                    action AddToSet(persistent.girl_mix[persistent.active_mix], gp)
                                    tooltip ttip + __("{i}Click to add this girl pack to the mix.{/i}")

                                hbox spacing 12 yalign 0.5:
                                    frame xalign 0.0 yalign 0.5 xsize xres(80) background None:
                                        add fast_portrait(gp, *res_tb(70)) xalign 0.5 yalign 0.5

                                    vbox xsize xres(360) yalign 0.5:
                                        text pack_name + {True: event_color["good"] % __(" (unique)"), False: ""}[gpinfo_dict[gp]["unique"]] drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" size res_font(18)
                                        text _("by %s") % gpinfo_dict[gp]["creator"] drop_shadow (1, 1) size res_font(14) italic True
                                        if show_rating:
                                            text _("{size=14}Rating: {/size}%s") % rating size res_font(18) drop_shadow (1, 1) # drop_shadow_color c_white
                                    if show_rating:
                                        text rtg_text size res_font(14) yalign 0.5 color c_darkbrown
            text "" size res_font(14)

            hbox:
                textbutton _("Delete mix") text_size res_font(18):
                    if persistent.active_mix != "default":
                        action renpy.curried_invoke_in_new_context(delete_mix, persistent.active_mix)
                textbutton _("Add all") action Function(add_all_to_mix, persistent.active_mix) text_size res_font(18)
                textbutton _("Remove all") action Function(remove_all_from_mix, persistent.active_mix) text_size res_font(18)
                textbutton _("Back") action Return() text_size res_font(18)

        frame background c_darkorange xfill True yfill True:
            if GetTooltip():
                text GetTooltip() color c_white


screen pic_tester(pics, _size): # Checks example pictures for one get_pic prompt

    modal True
    key "mouseup_3" action Return()

    frame xfill True:
        viewport xsize 0.9:
            mousewheel True
            scrollbars "horizontal"

            vbox box_wrap True xsize _size:

                for p in pics:
                    if p:
                        button style "inv_no_padding" action NullAction() tooltip p.path:
                            add p.get(x=_size, y=_size)


#<Chris12 PackState>
