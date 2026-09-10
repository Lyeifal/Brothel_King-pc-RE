#### Screen Common — Shared UI components | 通用界面组件 ####
# Phase 2: 通用组件
# Contains: screen tool, screen overlay, screen quick_start, screen dark_filter, screen yes_no, screen OK_screen, screen show_img, screen show_event, screen show_sex_event, screen shortcuts, screen close, screen receive_item
# Extracted from ui/screens.rpy on 2026-09-10

screen tool(x, y, w, h, bg = True, use_italic=False, char_limit=70, line_limit=3):

    tag ttip

    zorder 10

    $ text1 = ""

    if GetTooltip():
        use adv_tooltip()

    if tt.value != "":
        $ text1 = tt.value

    if text1:
        frame:

            if bg:
                background c_ui_dark

            else:
                background None

            xalign x
            yalign y

            xmaximum w
            ymaximum h

            xmargin xres(6)
            ymargin yres(3)
            ypadding 0

            xfill True
            yfill True

            if count_lines(text1, char_limit) >= line_limit:
                add Text(text1, size= 14, justify=True, italic=use_italic) fit "contain"
            else:
                text text1 size res_font(14) xsize 1.0 justify True italic use_italic

            # if count_lines(text1, 40) <= 3:
            #     $ s = res_font(13)
            # elif count_lines(text1, 44) <= 3:
            #     $ s = res_font(12)
            # elif count_lines(text1, 50) <= 4:
            #     $ s = res_font(11)
            # elif count_lines(text1, 54) <= 4:
            #     $ s = res_font(10)
            # else:
            #     $ s = res_font(9)
            # text text1 yalign 0.0 size int(s*new_res_ratio) justify True

screen overlay(current_screen = None, kwargs=None, ttip=False):

    zorder 5

    frame:
        id "ol"

        background c_ui_dark
        xsize 1.0
        ysize int(0.075*config.screen_height)
        xpadding xres(12)
        ypadding 0

        has hbox

        xfill True
        yfill True
        yalign 0.5

        button background None xalign 0.0 yalign 0.5 action NullAction():

            tooltip (__("%s\nToday is %s, Y%i M%i D%i." % (moons[calendar.month].short_description, calendar.get_weekday(), calendar.year, calendar.month, calendar.day)))

            hbox:
                spacing xres(8)

                add moons[calendar.month].tb yalign 0.5

                null

                text _("Year: [calendar.year]") size res_font(18) yalign 0.5
                text _("Month: [calendar.month]") size res_font(18) yalign 0.5
                text (__("Day: %s (%s)") % (calendar.day, __(calendar.get_weekday())[:3])) size res_font(18) yalign 0.5

        hbox xalign 1.0 spacing xres(6):
            if MC.resource_tab_active:
                yalign 0.0
            else:
                yalign 0.5

            button background None xalign 0.0 yalign 0.5 action NullAction():
                tooltip _("Your available gold.")
                if game.chapter > 1:
                    hovered (Show("tax_tooltip", transition=Dissolve(0.15)))
                    unhovered (Hide("tax_tooltip", transition=Dissolve(0.15)))

                hbox:
                    spacing xres(6)
                    add ProportionalScale("resources/ui/coin.webp", *res_tb(20)) yalign 0.5
                    text '{:,}'.format(round_int(MC.gold)).replace(',', ' ') xalign 0.0 yalign 0.5 size res_font(18)

            button background None xalign 0.0 yalign 0.5 tooltip __("AP: Your remaining actions for today.") action NullAction():

                has hbox

                spacing xres(3)

                add ProportionalScale("resources/ui/power.webp", *res_tb(20)) yalign 0.5

                text str(round_int(MC.interactions)) xalign 0.0 yalign 0.5 size res_font(18)

            button background None xalign 0.0 yalign 0.5 tooltip __("MP: Your current mana.") action NullAction():

                has hbox

                spacing xres(3)

                add ProportionalScale("resources/ui/mana.webp", *res_tb(20)) yalign 0.5

                text str(round_int(MC.mana)) xalign 0.0 yalign 0.5 size res_font(18)

        null width xres(200)

        textbutton "?" tooltip _("Learn more about the current screen."):

            style "button"
            xalign 1.0
            yalign 0.5
            xysize res_tb(36)

            if current_screen and not slavemarket_firstvisit:
                # action renpy.curried_invoke_in_new_context(help, current_screen)
                action Call("help", scr=current_screen)

    if MC.resource_tab_active:
        use resource_tab(x=0.5, y = 0.055)

    if ttip:
        use tool(x = 0.93, y = 0.0, w = 0.32, h = 0.075, bg = False)


screen quick_start(def_panel = "MC"):

    modal True

    default panel = def_panel
    default ngps = NGP_settings
    default total_crystals = count_achievements()
    $ spent_crystals = sum(s.get_used() for s in ngps)

    vbox xalign 0.5 yalign 0.5 xsize int(0.95*config.screen_width):
        hbox xfill True:
            textbutton _("Character") xsize xres(160) ysize yres(48) text_size res_font(24) text_selected_bold True action SelectedIf(panel == "MC") hovered SetScreenVariable("panel", "MC") tooltip _("Create your Main Character.")

            textbutton _("Difficulty") xsize xres(160) ysize yres(48) text_size res_font(24) text_selected_bold True action SelectedIf(panel == "diff") hovered SetScreenVariable("panel", "diff") tooltip _("Change difficulty settings.")

            textbutton _("Girls") xsize xres(160) ysize yres(48) text_size res_font(24) text_selected_bold True action SelectedIf(panel == "mix") hovered SetScreenVariable("panel", "mix") tooltip _("Choose your girl mixes.")

            if persistent.new_game_plus or debug:
                textbutton _("NewGame+") xsize xres(160) ysize yres(48) text_size res_font(24) text_selected_bold True action SelectedIf(panel == "extras") hovered SetScreenVariable("panel", "extras") tooltip _("Access NewGame+ settings.")

            button background None xsize xres(320) ysize yres(52) xalign 1.0:
                if GetTooltip():
                    $ ttip = GetTooltip()
                else:
                    $ ttip = ""
                text ttip size res_font(13) color c_white justify True

        frame xpadding 20 ypadding 20 xfill True ysize int(0.8*config.screen_height):
            has vbox xfill True spacing 20
            if panel == "MC":

                hbox spacing 30 xalign 0.5:
                    label _("Name: ")
                    input value FieldInputValue(MC, "name") length 20 color c_main bold True
#                     text "Name: " color c_brown yalign 0.5
#                     textbutton "[MC.name]" ysize yres(40) text_color c_white text_bold True action Call("MC_change_name")

                hbox spacing 30 xalign 0.5:
                    frame: # background c_orange:
                        has vbox

                        text _("Class") xalign 0.5 size res_font(18) bold True color c_prune

                        $ _available_classes = get_available_player_classes()
                        hbox spacing 10:
                            for cl in _available_classes:
                                button yalign 0.5 xpadding 0 action Function(MC.set_playerclass, cl) tooltip MC_playerclass_description.get(cl, ""):
                                    if MC.playerclass != cl:
                                        background None

                                    if cl in playerclass_pics and playerclass_pics[cl]:
                                        add Picture(path=playerclass_pics[cl]).get(*res_tb(40)) yalign 0.5:
                                            if MC.playerclass == cl:
                                                alpha 1.0
                                            else:
                                                alpha 0.3
                                    else:
                                        text cl size res_font(14) yalign 0.5

                    frame: # background c_purple:
                        has vbox

                        text _("Religion") xalign 0.5 size res_font(18) bold True color c_emerald

                        hbox spacing 10:
                            for god in ["Arios", "Shalia", None]:
                                button yalign 0.5 xpadding 0 action Function(MC.set_god, god) tooltip god_description[god]:
                                    if MC.god != god:
                                        background None

                                    add Picture(path=god_pics[god]).get(*res_tb(40)) yalign 0.5:
                                        if MC.god == god:
                                            alpha 1.0
                                        else:
                                            alpha 0.3
                                            # hover_alpha 1.0

                    frame xalign 0.5 yalign 0.5 ysize yres(76):
                        grid 4 1 yalign 0.5:
                            for stat in all_MC_stats:
                                button background None action NullAction() tooltip MC_stat_description[stat]:
                                    vbox xsize xres(100):
                                        text MC_stat_color[stat] % __(stat.capitalize()) size res_font(18) xalign 1.0
                                        text MC_stat_color[stat] % int(MC.get_stat(stat, raw=True) + NGP_settings_dict[stat].get()) size res_font(24) xalign 1.0

                # hbox spacing 20 xalign 0.5:


                hbox xalign 0.5 spacing 30:
                    textbutton "<" ysize yres(120) yalign 0.5:

                        action Function(MC.change_pic, "previous")
                        tooltip _("Change your Main Character's picture.")


                    frame:
                        xalign 0.5
                        yalign 0.3
                        xfill False
                        yfill False
                        add MC.current_pic.get(int(config.screen_width*0.5), int(config.screen_height*0.5))

                    textbutton ">" ysize yres(120) yalign 0.5:

                        action Function(MC.change_pic, "next")
                        tooltip _("Change your Main Character's picture.")

            elif panel == "diff":
                hbox spacing 60:
                    frame ysize yres(240):
                        has vbox spacing 10 xalign 0.5 yalign 0.5
                        style_group "diff"
                        for diff in diff_list:
                            textbutton diff_name[diff] xsize xres(220) ysize yres(36) action (Function(game.set_difficulty, diff), SelectedIf(game.diff == diff)) tooltip diff_description[diff] text_selected_bold True

                    vbox spacing 6 box_wrap True:

                        $ y = len(diff_settings)

                        grid 2 y:
                            for ds in diff_settings:
                                if ds == "satisfaction":
                                    textbutton __("%s: %s") % (diff_setting_name[ds], plus_text(game.get_diff_setting(ds))) text_color c_brown background None text_size res_font(18) action NullAction() tooltip diff_setting_description[ds]
                                else: # percentage description
                                    textbutton __("%s: %s") % (diff_setting_name[ds], percent_text(game.get_diff_setting(ds), False)) text_color c_brown background None text_size res_font(18) action NullAction() tooltip diff_setting_description[ds]

                                hbox:
                                    textbutton "-" text_size res_font(18) xsize xres(24) action Function(game.change_diff_setting, ds, -diff_settings_range[ds]["pace"]) # Trying to go around the prediction problem
                                    textbutton "+" text_size res_font(18) xsize xres(24) action Function(game.change_diff_setting, ds, diff_settings_range[ds]["pace"])

            elif panel == "mix":
                $ available_mixes = update_available_mixes()

                vbox spacing 20 xalign 0.05:
                    textbutton __("Active Girl mixes: %s") % and_text(persistent.game_mixes) xpadding 0 xmargin 0 background None text_color c_darkorange action NullAction() tooltip "{b}Warning{/b}: Your choice of active girl mixes cannot be changed after starting a game, although you can still add or remove girl packs from mixes."

                    text _("Click on a girl mix to add or remove it from this game (you must choose at least one).") size res_font(14) italic True color c_brown

                    hbox spacing 30 xfill True xalign 0.05:
                        frame ysize 0.8:
                            has vbox spacing 12 yfill True xalign 0.5
                            vpgrid cols 1 xalign 0.5 draggable True mousewheel True scrollbars "vertical":

                                style_group "mix"

                                for mix in available_mixes:
                                    textbutton mix.capitalize() text_size res_font(18) xsize xres(220) xalign 0.5:
                                        if mix in persistent.game_mixes:
                                            background c_orange
                                            text_color c_white
                                            action RemoveFromSet(persistent.game_mixes, mix)
                                            tooltip __("Click to remove mix: {b}%s{/b} from this game's active mixes.") % mix.capitalize()
                                        else:
                                            background c_ui_insensitive
                                            text_color c_darkgrey
                                            action AddToSet(persistent.game_mixes, mix)
                                            tooltip __("Click to add mix: {b}%s{/b} to this game's active mixes.") % mix.capitalize()

                            textbutton _("Edit girl mixes") xsize xres(220) ysize yres(36) xalign 0.5 yalign 1.0 action Return("edit mix") tooltip _("Click here to edit your girl mixes.")

                        $ selected_girlpacks = get_selected_girlpacks(persistent.game_mixes)

                        vpgrid cols 10 draggable True allow_underfull True mousewheel True scrollbars "vertical" xalign 1.0:
                            for gp in selected_girlpacks:
                                button background None xalign 0.5 yalign 0.5 xmargin 0 ymargin 0 action NullAction() tooltip get_name(gp, full=True) + "{i} by %s{/i} (%s)" % (gpinfo_dict[gp]["creator"], gpinfo_dict[gp]["version"]):
                                    add fast_portrait(gp, *res_tb(30))


            elif panel == "extras":

                vbox xfill True spacing yres(20):
                    hbox xalign 0.05 spacing xres(12):
                        label _("Achievement crystals: ") text_size res_font(24) text_color c_purple yalign 1.0
                        use crystal_display(" %i/%i" % (spent_crystals, total_crystals), sz=24, prefix="")
                        null
                        text _("Use crystals to unlock extra options for the game. You can earn crystals by unlocking achievements.") yalign 1.0 size res_font(14) italic True color c_purple

                    vbox spacing yres(12) box_wrap True xsize 0.7:
                        for s in ngps:
                            $ cost = s.get_cost()
                            $ refund = s.get_refund()

                            hbox spacing xres(10):
                                button xsize xres(160) yalign 0.5 style "inv_no_padding" left_margin xres(20)  action NullAction() tooltip s.ttip:
                                    label s.label text_size res_font(18)

                                button xsize xres(60) yalign 0.5 style "inv_no_padding" action NullAction() tooltip s.get_ttip():
                                    text s.read() size res_font(18):
                                        if s.index == 0:
                                            color c_grey
                                        else:
                                            color c_purple

                                if s.type == "bool":
                                    textbutton {0: "Activate", 1: "Deactivate"}[s.index] xsize xres(48) ysize yres(24) text_size res_font(12):
                                        if s.can_lower():
                                            tooltip s.get_ttip("minus") % refund
                                            action Function(s._lower)
                                        elif s.can_raise(total_crystals-spent_crystals):
                                            tooltip s.get_ttip("plus") % cost
                                            action Function(s._raise)

                                else:
                                    hbox yalign 0.5:
                                        if s.index < len(s.values) or s.type == "gold":
                                            textbutton "+" xsize xres(24) ysize yres(24):
                                                if s.can_raise(total_crystals-spent_crystals):
                                                    tooltip s.get_ttip("plus") % cost
                                                    action Function(s._raise)

                                        if s.can_lower():
                                            textbutton "-" xsize xres(24) ysize yres(24):
                                                tooltip s.get_ttip("minus") % refund
                                                action Function(s._lower)

                        null height yres(10)

                        textbutton _("Reset NG+ settings") text_size res_font(12) xalign 1.0 action Return("reset NGP") tooltip _("Reset all settings to default value")

        frame xfill True xsize int(0.95*config.screen_width) ysize int(0.1*config.screen_height):
            hbox xsize 0.7 xalign 0.95 spacing xres(12):
                add Picture(path=playerclass_pics[MC.playerclass]).get(*res_tb(50)) xalign 0.0 yalign 0.5
                add Picture(path=god_pics[MC.god]).get(*res_tb(50)) xalign 0.0 yalign 0.5

                vbox spacing 10 xalign 0.5 yalign 0.5:
                    text __("{b}%s, %s{/b} ({b}%s{/b}) - {b}%s{/b} difficulty") % (MC.name, __(MC.playerclass), str(MC.god), __(game.diff.capitalize())) color c_prune size res_font(18)
                    if game.achievements:
                        text _("Achievements will be enabled for this game.") italic True color c_emerald size res_font(18)
                    else:
                        text _("Achievements will be disabled for this game.") italic True color c_red size res_font(18)

                textbutton _("CONFIRM") xalign 1.0 yfill True action Return(True) tooltip _("Start a new game with these settings.")


screen dark_filter(can_click=True, covers_dialogue=True):

    tag dark_filter

    modal False

    zorder 0

    if covers_dialogue:
        $ y = int(0.925*config.screen_height)
    else:
        $ y = int(0.925*config.screen_height-res_portrait_size)

    button xfill True yfill True xpadding 0 xmargin 0 ypadding 0 ymargin 0 ypos 0.075 yanchor 0.0 ymaximum y background c_ui_darkblue activate_sound None:
        if can_click:
            action Return()

screen yes_no(message, yes_caption=_("Yes"), no_caption=_("No"), col=c_white, bg=c_ui_darker):

    modal True
    zorder 10

    key "mouseup_3" action (Return(False))

    frame:
        style_group "yesno"

        xfill False
        xmaximum 0.8
        xpadding .05
        xalign 0.5
        yalign 0.5
        ypadding 25
        ymargin 10
        ymaximum 0.85
        background bg

        has vbox:
            xalign .5
            yalign .5
            spacing 25

        viewport:
            id "yesno_message"
            xfill True
            ymaximum 0.6
            mousewheel "change"
            draggable True
            scrollbars "vertical"

            label _(message):
                xalign 0.5
                text_size res_font(18)
                text_color col

        hbox:
            xalign 0.5
            spacing 100

            textbutton _(yes_caption) action Return(True)
            textbutton _(no_caption) action Return(False)


screen OK_screen(title="", message="", pic = None, pic_size = "large", dark=False, x=0.6, y=0.7, always_scrollbar=False):

    modal True

    key "mouseup_3" action (Return(True))

    frame:
        style_group "OK"

        xsize int(x*config.screen_width)
        ymaximum int(y*config.screen_height)

        xalign 0.5
        yalign 0.5
        xpadding 25
        ypadding 25
        ymargin 10
        if not dark:
            background c_ui_light
        else:
            background c_ui_darkblue

        has vbox spacing 25

        vpgrid:
            cols 1
            ymaximum 0.9
            mousewheel "change"
            draggable True
            allow_underfull True
            if len(message) > 1250 or always_scrollbar:
                scrollbars "vertical"

            vbox spacing 25 yalign 0.5 xfill True yfill False:

                label _(title):
                    xalign 0.5
                    if not dark:
                        text_color c_darkred
                    else:
                        text_color c_hotpink
                    text_bold True

                if pic:
                    if pic_size == "large":
                        add pic.get(*res_tb(200)) xalign 0.5

                    elif pic_size == "small":
                        add pic.get(*res_tb(60)) xalign 0.5

                text _(message):
                    xalign 0.5
                    size res_font(18)

                    if not dark:
                        color c_brown
                    else:
                        color c_white

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Ok") action Return(True)


screen show_img(img, bg=None): # Mostly used to show full screen pictures with no background, such as brothel pics

    layer "master" # Shown on master layer (watch out, no interactivity)

    use show_event(img, bg=bg, xs=1.0, ys=1.0, can_ignore=False)

screen show_event(event_pic, x = None, y = None, proportional = True, bg = "black", xs = 1.0, ys = 0.8, xs_bg = None, ys_bg = None, can_ignore=True):

    # event_pic can be a Picture object, a ProportionalScale object, or a string
    # x and y refer to event_pic maximum size in pixels. Use xs and ys to specify a proportional size. x and y override xs and ys.
    # use xs_bg and ys_bg to specify a different size for the BG. By default it is the same as xs and ys

    tag show_screen

    zorder 0

    layer "master" # This excludes this screen from being hidden when middle-click is used

    # Shortcuts and show statements

    if can_ignore:
        key ['K_DELETE'] action Function(toggle_ignore_pic, pic=event_pic)

    on "show" action Function(unlock_pic, pic=event_pic) # This is how the game tracks that this particular picture path has been seen (gallery).

    # size calculations

    if not x:
        $ x = int(config.screen_width*xs)
    if not y:
        $ y = int(config.screen_height*ys)

    if not xs_bg:
        $ xs_bg = x
    if not ys_bg:
        $ ys_bg = y

    frame:
        style "inv_no_padding"
        if bg:
            if isinstance(bg, Picture):
                background bg.get(x=xs_bg, y=ys_bg, proportional=False)
            elif isinstance(bg, ProportionalScale):
                background Frame(bg)
            elif is_string(bg):
                background Frame(bg)
        xalign 0.5
        yalign 0.5
        xfill True
        yfill True
        xsize xs_bg
        ysize ys_bg

        if event_pic:
            fixed xsize x ysize y xalign 0.5 yalign 1.0:
                if isinstance(event_pic, Picture):
                    add event_pic.get() xalign 0.5 yalign 1.0 fit "contain"
                elif isinstance(event_pic, ProportionalScale):
                    add event_pic xalign 0.5 yalign 1.0 fit "contain"
                elif is_string(event_pic):
                    add event_pic xalign 0.5 yalign 1.0 fit "contain"

            if debug_mode:
                frame background c_ui_dark:
                    has vbox
                    text (_("Attempt: %s") % str(game.last_pic["attempts"])) size res_font(14)
                    text (_("Search tags: %s") % and_text(game.last_pic["tags"])) size res_font(14)
                    text (_("AND tags: %s") % and_text(game.last_pic["and_tags"])) size res_font(14)
                    text (_("AND NOT tags: %s") % and_text(game.last_pic["not_tags"])) size res_font(14)
                    # text "y: %i ys: %s ys_bg: %s" % (y, str_dec(ys), str_dec(ys_bg))

screen show_sex_event(event_pic, bg = c_ui_dark): # Mostly used for interactions, wide format.

    use show_event(event_pic, bg=bg, x=res_event_width, y=res_event_height, xs=1.0, ys=0.8)

    # key ['K_DELETE'] action Function(toggle_ignore_pic, event_pic.path)
    #
    # if event_pic:
    #     on "show" action Function(unlock_pic, event_pic.path) # This is how the game tracks that this particular picture has been seen.
    #
    #
    # zorder 0
    #
    # default show_log = False
    #
    #
    # frame:
    #     background bg
    #     xalign 0.0
    #     yalign 0.0
    #     xsize 1.0
    #     ysize 0.8
    #     left_margin 6
    #     ymargin 6
    #     xfill True
    #     yfill True
    #
    #     if event_pic:
    #         add event_pic.get(res_event_width, res_event_height) xalign 0.5
    #
    #         if debug_mode:
    #             frame background c_ui_dark:
    #                 has vbox
    #                 text "Attempt: " + str(game.last_pic["attempts"]) size res_font(14)
    #                 text "Search tags: " + and_text(game.last_pic["tags"]) size res_font(14)
    #                 text "AND tags: " + and_text(game.last_pic["and_tags"]) size res_font(14)
    #                 text "AND NOT tags: " + and_text(game.last_pic["not_tags"]) size res_font(14)


screen shortcuts():

    zorder 100

    # Note: some keys like 'f', 'h', 'm', 's', 'v' are used natively by Ren'py and have been remapped to Shift+* when necessary (see 'BKinit_variables')

    key "noshift_K_h" action (SetVariable("selected_destination", "main"), Jump("teleport"))
    key "noshift_K_c" action (SetVariable("selected_destination", "main_character"), Jump("teleport"))
    key "noshift_K_g" action (SetVariable("selected_destination", "girls"), Jump("teleport"))
    key "noshift_K_b" action (SetVariable("selected_destination", "brothel"), Jump("teleport"))
    key "noshift_K_v" action (SetVariable("selected_destination", "districts"), Jump("teleport"))
    key "noshift_K_s" action (SetVariable("selected_destination", "shop"), Jump("teleport"))
    key "noshift_K_t" action (SetVariable("selected_destination", "postings"), Jump("teleport"))
    key "noshift_K_e" action (SetVariable("selected_destination", "end_day"), Jump("teleport"))
    key "noshift_K_o" action (SetVariable("selected_destination", "customer_options"), Jump("teleport"))
    key "noshift_K_k" action (SetVariable("show_spellbook", True), SetVariable("selected_destination", "main_character"), Jump("teleport"))
    key "K_F5" action QuickSave() #Set the F5 key in your keyboard to Quicksave when pressed
    key "K_F9" action QuickLoad(confirm=False)  #Same for F9 key

    if slavemarket.active:
        key "noshift_K_m" action (SetVariable("selected_destination", "slavemarket"), Jump("teleport"))
    if NPC_carpenter.active:
        key "noshift_K_w" action (SetVariable("selected_destination", "furniture"), Jump("teleport"))
    if farm.active:
        key "noshift_K_f" action (SetVariable("selected_destination", "farm"), Jump("teleport"))
    if selected_location:
        key "noshift_K_l" action (SetVariable("selected_destination", "visit_location"), Jump("teleport"))
    if farm.powers:
        key "noshift_K_p" action (SetVariable("selected_destination", "farm_powers"), Jump("teleport"))


screen close(act, name="back", ttip="Click to go back (or use right-click)."):

    textbutton name:

        background None

        xalign 1.0
        yalign 0.075
        xfill False
        yfill False
        xmargin 3

        text_size res_font(14)
        text_align 1.0
        text_color c_lightred
        text_hover_color c_red
        action act
        tooltip ttip


screen receive_item(it, msg, col=c_emerald):

    tag receive_item

    zorder 10

    button background c_ui_darker:
        xalign 0.5
        yalign 0.5
        xpadding 20
        ypadding 20

        action Return()
        tooltip "{i}" + it.base_description + "{/i}\n\n" + it.description

        has vbox
        xalign 0.5
        yalign 0.5
        spacing 20

        add it.get_pic(*res_tb(100)) xalign 0.5

        text msg color col size res_font(16) xalign 0.5 yalign 0.5
