####            NEW SCREENS                 ####
##  Those are the screens specific to BKING   ##
##                                            ##
####                                        ####

## This script is long, redundant, and an utter mess. This is related to my severe lack of understanding of screen language in general, and especially styles. Sorry.


#### DECLARATIONS ####

image img_AP = ProportionalScale("resources/ui/power.webp", *res_tb(16))
image img_AP_small = ProportionalScale("resources/ui/power.webp", *res_tb(12))
image img_MP = ProportionalScale("resources/ui/mana.webp", *res_tb(16))
image img_gold = ProportionalScale("resources/ui/coin.webp", *res_tb(16))
image img_gold_18 = ProportionalScale("resources/ui/coin.webp", *res_tb(18))
image img_gold_20 = ProportionalScale("resources/ui/coin.webp", *res_tb(20))
image img_gold_24 = ProportionalScale("resources/ui/coin.webp", *res_tb(24))
image img_star = ProportionalScale("resources/ui/star.webp", *res_tb(16))
image img_empty_star = ProportionalScale("resources/ui/star_empty.webp", *res_tb(16))
image img_lock = ProportionalScale("resources/ui/lock.webp", *res_tb(80))
image img_cust = ProportionalScale("resources/ui/customer.webp", *res_tb(22))
# image img_girl = ProportionalScale(im.Crop("resources/ui/girl_shadow.webp", (0, 0, 380, 350)), *res_tb(24))
image img_girl = ProportionalScale(Transform("resources/ui/girl_shadow.webp", crop = (0, 0, 380, 350)), *res_tb(24)) # updated transform (Dexell)
image lines = ProportionalScale("resources/perks/lines.webp", xres(800), yres(640))
image filter_all = ProportionalScale("resources/ui/filters/all.webp", *res_tb(30))
image filter_weapon = ProportionalScale("resources/ui/filters/weapon.webp", *res_tb(30))
image filter_clothing = ProportionalScale("resources/ui/filters/clothing.webp", *res_tb(30))
image filter_trinket = ProportionalScale("resources/ui/filters/trinket.webp", *res_tb(30))
image filter_consumable = ProportionalScale("resources/ui/filters/consumable.webp", *res_tb(30))
image filter_misc = ProportionalScale("resources/ui/filters/misc.webp", *res_tb(30))
image filter_all_unselect = ProportionalScale("resources/ui/filters/all.webp", *res_tb(30), matrixcolor=SaturationMatrix(0))
image filter_weapon_unselect = ProportionalScale("resources/ui/filters/weapon.webp", *res_tb(30), matrixcolor=SaturationMatrix(0))
image filter_clothing_unselect = ProportionalScale("resources/ui/filters/clothing.webp", *res_tb(30), matrixcolor=SaturationMatrix(0))
image filter_trinket_unselect = ProportionalScale("resources/ui/filters/trinket.webp", *res_tb(30), matrixcolor=SaturationMatrix(0))
image filter_consumable_unselect = ProportionalScale("resources/ui/filters/consumable.webp", *res_tb(30), matrixcolor=SaturationMatrix(0))
image filter_misc_unselect = ProportionalScale("resources/ui/filters/misc.webp", *res_tb(30), matrixcolor=SaturationMatrix(0))

# image filter_weapon_unselect = im.MatrixColor(ProportionalScale("resources/ui/filters/weapon.webp", *res_tb(30)), im.matrix.desaturate())
# image filter_clothing_unselect = im.MatrixColor(ProportionalScale("resources/ui/filters/clothing.webp", *res_tb(30)), im.matrix.desaturate())
# image filter_trinket_unselect = im.MatrixColor(ProportionalScale("resources/ui/filters/trinket.webp", *res_tb(30)), im.matrix.desaturate())
# image filter_consumable_unselect = im.MatrixColor(ProportionalScale("resources/ui/filters/consumable.webp", *res_tb(30)), im.matrix.desaturate())
# image filter_misc_unselect = im.MatrixColor(ProportionalScale("resources/ui/filters/misc.webp", *res_tb(30)), im.matrix.desaturate())

image tb goal = ProportionalScale("resources/ui/goal.webp", *res_tb(50))
image tb advance = ProportionalScale("resources/characters/npc/Sill/portrait.webp", *res_tb(30))
image tb story = ProportionalScale("resources/characters/npc/Kurohime/portrait.webp", *res_tb(30))
image tb other = ProportionalScale("resources/characters/npc/Gio/portrait.webp", *res_tb(30))
image tb papa = ProportionalScale("resources/characters/npc/Misc/freak portrait.webp", *res_tb(20))
image tb contract = ProportionalScale("resources/characters/npc/Jobgirl/portrait.webp", *res_tb(30), xzoom = -1.0)

image tb rest = ProportionalScale("resources/backgrounds/rest.webp", xres(100), yres(60))
image tb waitress = ProportionalScale("resources/backgrounds/waitress.webp", xres(100), yres(60))
image tb dancer = ProportionalScale("resources/backgrounds/stripper.webp", xres(100), yres(60))
image tb masseuse = ProportionalScale("resources/backgrounds/masseuse.webp", xres(100), yres(60))
image tb geisha = ProportionalScale("resources/backgrounds/geisha.webp", xres(100), yres(60))
image tb whore = ProportionalScale("resources/backgrounds/whore.webp", xres(100), yres(60))
image tb farm = ProportionalScale("resources/brothels/farm/farm.webp", xres(100), yres(60))

# image success = ProportionalScale("resources/ui/challenges/success.webp", config.screen_width, config.screen_height)
# image failure = ProportionalScale("resources/ui/challenges/failure.webp", config.screen_width, config.screen_height)


image girl_shadow = ProportionalScale("resources/ui/girl_shadow.webp", *res_tb(75))

image tb wood = ProportionalScale("resources/ui/fast buttons/wood.webp", *res_tb(40))
image tb wood grey = ProportionalScale("resources/ui/fast buttons/wood.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))
image tb leather = ProportionalScale("resources/ui/fast buttons/leather.webp", *res_tb(40))
image tb leather grey = ProportionalScale("resources/ui/fast buttons/leather.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))
image tb dye = ProportionalScale("resources/ui/fast buttons/dye.webp", *res_tb(40))
image tb dye grey = ProportionalScale("resources/ui/fast buttons/dye.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))
image tb silk = ProportionalScale("resources/ui/fast buttons/silk.webp", *res_tb(40))
image tb silk grey = ProportionalScale("resources/ui/fast buttons/silk.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))
image tb marble = ProportionalScale("resources/ui/fast buttons/marble.webp", *res_tb(40))
image tb marble grey = ProportionalScale("resources/ui/fast buttons/marble.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))
image tb ore = ProportionalScale("resources/ui/fast buttons/ore.webp", *res_tb(40))
image tb ore grey = ProportionalScale("resources/ui/fast buttons/ore.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))
image tb diamond = ProportionalScale("resources/ui/fast buttons/diamond.webp", *res_tb(40))
image tb diamond grey = ProportionalScale("resources/ui/fast buttons/diamond.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))

image tb renza = ProportionalScale("resources/ui/fast buttons/renza.webp", *res_tb(40))
image tb renza grey = ProportionalScale("resources/ui/fast buttons/renza.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))
image tb captain = ProportionalScale("resources/ui/fast buttons/captain.webp", *res_tb(40))
image tb captain grey = ProportionalScale("resources/ui/fast buttons/captain.webp", *res_tb(40), matrixcolor=SaturationMatrix(0))

image tb banker = ProportionalScale("resources/ui/fast buttons/banker.webp", *res_tb(40))
image tb bast = ProportionalScale("resources/ui/fast buttons/bast.webp", *res_tb(40))
image tb giftgirl = ProportionalScale("resources/ui/fast buttons/giftgirl.webp", *res_tb(40))
image tb gina = ProportionalScale("resources/ui/fast buttons/gina.webp", *res_tb(40))
image tb goldie = ProportionalScale("resources/ui/fast buttons/goldie.webp", *res_tb(40))
image tb gurigura = ProportionalScale("resources/ui/fast buttons/gurigura.webp", *res_tb(40))
image tb katryn = ProportionalScale("resources/ui/fast buttons/katryn.webp", *res_tb(40))
image tb papa = ProportionalScale("resources/characters/npc/misc/freak portrait.webp", *res_tb(40))
image tb ramias = ProportionalScale("resources/ui/fast buttons/ramias.webp", *res_tb(40))
image tb riche = ProportionalScale("resources/ui/fast buttons/riche.webp", *res_tb(40))
image tb stella = ProportionalScale("resources/ui/fast buttons/stella.webp", *res_tb(40))
image tb twins = ProportionalScale("resources/ui/fast buttons/twins.webp", *res_tb(40))
image tb willow = ProportionalScale("resources/ui/fast buttons/willow.webp", *res_tb(40))

image tb empty = ProportionalScale("resources/ui/tb empty.webp", *res_tb(30))
image tb advertising = ProportionalScale("resources/ui/tb advertising.webp", *res_tb(30))
image tb security = ProportionalScale("resources/ui/tb security.webp", *res_tb(30))
image tb maintenance = ProportionalScale("resources/ui/tb maintenance.webp", *res_tb(30))

image penta = ProportionalScale("resources/ui/powers/pentagram.webp", *res_tb(100))
image magic fire = SnowBlossom("resources/ui/powers/magic fire.webp", 100, xspeed=(-200, 200), yspeed=(-500, -1000), start=0)
image penta_fire = Crop((0, 0, yres(120), yres(120)), "magic fire")
image evil_deck_fire = Crop((0, 0, yres(160), yres(160)), "magic fire")
image evil_deck = ProportionalScale("resources/ui/powers/evil deck.webp", *res_tb(150))
image mojo purple = ProportionalScale("resources/ui/powers/orb_purple.webp", *res_tb(16))
image mojo green = ProportionalScale("resources/ui/powers/orb_green.webp", *res_tb(16))
image mojo blue = ProportionalScale("resources/ui/powers/orb_blue.webp", *res_tb(16))
image mojo red = ProportionalScale("resources/ui/powers/orb_red.webp", *res_tb(16))
image mojo yellow = ProportionalScale("resources/ui/powers/orb_yellow.webp", *res_tb(16))
image img_fear = ProportionalScale("resources/ui/skull.webp", *res_tb(20))
image img_fear_x2 = ProportionalScale("resources/ui/skull x2.webp", *res_tb(20))
image img_fear_x3 = ProportionalScale("resources/ui/skull x3.webp", *res_tb(20))
image card_back = ProportionalScale("resources/ui/powers/back.webp", xres(80), yres(120))
image card_front = ProportionalScale("resources/ui/powers/front.webp", xres(80), yres(120))

image tb crystal = ProportionalScale("resources/items/misc/misc.webp", *res_tb(18))
image misc = "resources/items/misc/misc.webp"

image mike = Transform("resources/characters/npc/Misc/Pets/pet1.webp", zoom=2.0)
image tanuki = "resources/ui/tanuki.webp"

image img_tavern = ProportionalScale("resources/brothels/rooms/tavern.webp", xres(192), yres(108))
image img_strip club = ProportionalScale("resources/brothels/rooms/strip club.webp", xres(120), yres(108))
image img_onsen = ProportionalScale("resources/brothels/rooms/onsen.webp", xres(192), yres(108))
image img_okiya = ProportionalScale("resources/brothels/rooms/okiya.webp", xres(192), yres(108))

## CUSTOM STYLES

init:
    # girl buttons ysize (hard-coded)
    $ girl_but_ysize = {"x4" : yres(125), "x12" : yres(100), "x24" : yres(80), "x40" : yres(60)}

    style hyperlink_text:
        hover_color c_orange
        idle_color c_pink
        hover_underline True

    style inv_no_padding: # For invisible buttons and frames
        background None
        xpadding 0
        ypadding 0
        xmargin 0
        ymargin 0

    style button:
        xpadding xres(6)
        ypadding yres(6)
        ymargin yres(2)
        idle_background Frame("darkorange_button", borders=gui.button_borders)
        selected_background Frame("orange_button", borders=gui.button_borders)
        hover_background Frame("lightblue_button", borders=gui.button_borders)
        selected_hover_background Frame("lightblue_button", borders=gui.button_borders)
        insensitive_background Frame("lightgrey_button", borders=gui.button_borders)
        activate_sound "resources/sounds/click.ogg"

    style button_text is gui_text:
        properties gui.text_properties("button")
        # padding (xres(6), yres(3), xres(6), yres(3))
        yalign 0.5

    style contrast_button is button:
        selected_background Frame("lightblue_button", borders=gui.button_borders)

    # style contrast_button_text:
    #     idle_color c_brown

    style small_button is button:
        xpadding xres(3)
        ypadding yres(3)
        xmargin 0
        ymargin 0

    style small_button_text:
        size res_font(14)

# Updated the following transforms (suggested by Dexell)
    style insensitive_button:
        background Frame (
                # im.MatrixColor(
                #     "resources/ui/cry_box.webp",
                #     im.matrix.colorize(c_lightgrey, "#000")), left=10, right=10)
                Transform(
                    "resources/ui/cry_box.webp",
                    matrixcolor = ColorizeMatrix(c_lightgrey, "#000")), left=10, right=10)

    style insensitive_button_text:
        color c_white

    style girlbutton:
        idle_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_darkorange + "CC", "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_darkorange + "CC", "#000")), left=10, right=10)
        selected_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize("#298ed6CC", "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix("#298ed6CC", "#000")), left=10, right=10)
        hover_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize("#69b0e2", "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix("#69b0e2", "#000")), left=10, right=10)

    style girlbutton_blue:
        idle_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_darkorange + "CC", "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_darkorange + "CC", "#000")), left=10, right=10)
        selected_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize("#298ed6CC", "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix("#298ed6CC", "#000")), left=10, right=10)
        hover_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_ui_lightblue, "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_ui_lightblue, "#000")), left=10, right=10)

    style girlbutton_light:
        idle_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_ui_light, "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_ui_light, "#000")), left=10, right=10)
        selected_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_orange, "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_orange, "#000")), left=10, right=10)
        hover_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_lightorange, "#000")), left=10, right=10)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_lightorange, "#000")), left=10, right=10)

    style posting_button is button:
        selected_background Frame ("lightblue_button")

    style push_button:
        idle_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_lightgrey, "#000")))
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_lightgrey, "#000")))
        selected_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_darkpurple, "#000")))
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_darkpurple, "#000")))
        hover_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_softpurple, "#000")))
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_softpurple, "#000")))

    style push_button_text:
        selected_color c_white
        hover_color c_white
        idle_color c_brown

    style farm_button:
        xpadding yres(18) # Using yres to maintain aspect in wide screen
        ypadding yres(9)
        idle_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_lightprune + "CC", "#000")), left=12, right=12)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_lightprune + "CC", "#000")), left=12, right=12)
        selected_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_prune, "#000")), left=12, right=12)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_prune, "#000")), left=12, right=12)
        hover_background Frame (
            # im.MatrixColor(
            #     "resources/ui/cry_box.webp",
            #     im.matrix.colorize(c_prune + "CC", "#000")), left=12, right=12)
            Transform(
                "resources/ui/cry_box.webp",
                matrixcolor = ColorizeMatrix(c_prune + "CC", "#000")), left=12, right=12)

    style farm_button_text:
        selected_color c_white
        hover_color c_white
        idle_color c_darkprune

## TOP OVERLAY (displays time, money, help button...)

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


# screen tool + overlay → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy

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



# screen girl_profile → EXTRACTED to ui/screens/screen_girl_profile.rpy (Phase 3.1)


# screen stat_bar + custom_bar + girl_stats + assign_job + girl_stats_light → EXTRACTED to ui/screens/screen_girl_stats.rpy (Phase 2)
# 女孩属性/属性条/特性详情 已提取到 screen_girl_stats.rpy



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


## SCHEDULE SCREEN

screen schedule(glist):

    modal True

    key "mouseup_3" action (Return())
    key "noshift_K_d" action Return()

    use dark_filter(False)

    frame:
        ypos 0.08
        xmargin 20
#        ymargin 20
        xpadding 20
        ypadding 20

        has vbox

        spacing 3

        hbox:
            spacing 6
            xfill True
            ysize yres(22)
            xalign 1.0
            hbox:
                xsize xres(150)
                xfill True
                xalign 0.0
                yalign 1.0
                text _("Girl Schedule") color c_darkorange xsize xres(95) xalign 0.5 yalign 0.0 text_align 1.0 size res_font(20)

            for day in weekdays:

                frame xsize xres(88) ysize yres(20)  yalign 1.0 background None:
                    text day size res_font(14) xalign 0.5 color c_brown xsize xres(90):
                        if day == calendar.get_weekday():
                            bold True

            null width xres(20)

            if brothel.get_effect("special", "autorest") or debug_mode:
                frame xsize xres(88) ysize yres(20)  yalign 1.0 background None:
                    text _("Autorest") color c_emerald size res_font(14) xalign 0.5

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            ymaximum 0.8
            yfill False
            yadjustment sched_adj

            has vbox
            spacing 6

            for girl in glist:
                hbox:
                    spacing 6
                    xfill True
                    xalign 1.0

                    hbox:
                        xsize xres(150)
                        xfill True
                        xalign 1.0
                        yalign 0.5

                        button xsize xres(95) ysize yres(53) style "girlbutton" xpadding xres(6) ypadding yres(3) action (SetVariable("selected_girl", girl), Return()) tooltip __("Click here to check %s's profile.") % girl.fullname:
                            has vbox

                            xalign 1.0
                            yalign 0.5

                            text girl.name size res_font(14) text_align 1.0 color c_brown xalign 1.0:

                                if selected_girl == girl:
                                    bold True
                                    color c_white

                            if girl.job:
                                $ text1 = __(girl.job.capitalize())
                                $ col = job_color[girl.job]
                            else:
                                $ text1 = __("No job")
                                $ col = c_white

                            text text1 size res_font(12) text_align 1.0 color col xalign 1.0

                            if girl.exhausted:
                                $ text1 = event_color["a little bad"] % "Exhausted"
                            elif girl.hurt:
                                $ text1 = event_color["bad"] % ("Hurt (" + str(round_int(girl.hurt)) + " days)")
                            else:
                                $ en_max = girl.get_stat_minmax("energy")[1]

                                if girl.energy < en_max / 5:
                                    $ text1 = "{color=[c_red]}" + str(round_int(girl.energy)) + "{/color}/" + str(round_int(en_max))
                                else:
                                    $ text1 = str(round_int(girl.energy)) + "/" + str(round_int(en_max))

                            text text1 size res_font(12) text_align 1.0 color c_brown xalign 1.0

                        hbox:
                            xmaximum xres(50)
                            xfill True
                            xalign 1.0
                            yalign 0.5
                            spacing 20

                            fixed fit_first True xalign 0.5 yalign 0.5:
                                add girl.portrait.get(*res_tb(40)) xalign 0.5 yalign 0.5

                                $ badge = girl.get_badge()
                                if badge:
                                    add ProportionalScale(badge, *res_tb(20)) xalign 0.9 yalign 0.1

                    for day in weekdays:

                        if girl.workdays[day] == 100:
                            $ ttip = "She will work to the maximum of her abilities."

                        elif girl.workdays[day] == 50:
                            $ ttip = "She will receive half the usual number of clients, saving some energy."

                        elif girl.workdays[day] == 0:
                            $ ttip = "She will rest and recover some energy."

                        $ ttip += "\n{i}Right-click to reverse cycle order.{/i}"

                        textbutton workshift_dict[girl.workdays[day]] text_size res_font(14) xsize xres(90) ysize yres(40) yalign 0.5 tooltip ttip idle_background workshift_color[girl.workdays[day]] hover_background c_darkbrown + "CC":
                            if girl.block_schedule != day:
                                action Function(girl.cycle_workday, day) # renpy.curried_invoke_in_new_context(girl.cycle_workday, day)
                                alternate Function(girl.cycle_workday, day, True)
                            else:
                                action Function(notify, "You cannot change her schedule as you gave her a day off.")
                                alternate Function(notify, "You cannot change her schedule as you gave her a day off.")


                    hbox yalign 0.5:
                        textbutton _("S") text_size res_font(14) action ShowTransient("save_schedule", girl=girl, transition=Dissolve(0.15)) tooltip "Click here to save %s's schedule." % girl.fullname
                        textbutton _("L") text_size res_font(14) action ShowTransient("load_schedule", girl=girl, transition=Dissolve(0.15)) tooltip "Click here to load a schedule for %s." % girl.fullname
                    
                    if brothel.get_effect("special", "autorest")  or debug_mode:
                        if autorest_limit[girl] > 0:
                            $ text1 = "at %i en." % autorest_limit[girl]
                        else:
                            $ text1 = "No"

                        textbutton text1 text_size res_font(14) action Show("autorest", girl=girl) tooltip "Set up %s's autorest options." % girl.fullname yalign 0.5 xsize xres(70)

        text ""

        hbox spacing 10 xalign 1.0:
            if brothel.get_effect("special", "autorest") or debug_mode:
                textbutton _("Autorest options") xalign 1.0 action Show("autorest") tooltip _("Adjust default autorest options")
            textbutton _("Ok") action (Return())

screen save_schedule(girl):

    modal True

    key "mouseup_3" action Hide("save_schedule", transition=Dissolve(0.15))

    frame background c_ui_darkblue align(0.5, 0.5) xpadding xres(20) ypadding yres(20):

        vbox:
            text (_("Save %s's schedule") % (event_color["special"] % girl.fullname)) bold True color c_white size res_font(18) xalign 0.5
            null height yres(20)
            for i in range(10):
                button action (Function(game.save_schedule, girl, i), Hide("save_schedule", transition=Dissolve(0.15))) xsize xres(220) ysize yres(28):
                    hbox spacing xres(20) yalign 0.5:
                        textbutton str(i+1) xsize xres(20) xalign 0.5 background None
                        if game.saved_schedules[i]:
                            hbox align(0.5, 0.5):
                                for j in range(7):
                                    textbutton weekdays[j][0] xalign 0.5 background workshift_color[game.saved_schedules[i][j]]
                        else:
                            text _("Empty") italic True size res_font(18)

            null height yres(10)
            textbutton _("Cancel") action Hide("save_schedule", transition=Dissolve(0.15)) xalign 1.0

screen load_schedule(girl):

    modal True

    key "mouseup_3" action Hide("load_schedule", transition=Dissolve(0.15))

    frame background c_ui_darkblue align(0.5, 0.5) xpadding xres(20) ypadding yres(20):

        vbox:
            text (_("Load a schedule for %s") % (event_color["special"] % girl.fullname)) bold True color c_white size res_font(18) xalign 0.5
            null height yres(20)
            for i in range(10):
                button xsize xres(220) ysize yres(28):
                    if game.saved_schedules[i]:
                        action (Function(girl.load_schedule, game.saved_schedules[i]), Hide("load_schedule", transition=Dissolve(0.15)))
                    hbox spacing xres(20) yalign 0.5:
                        textbutton str(i+1) xsize xres(20) xalign 0.5 background None
                        if game.saved_schedules[i]:
                            hbox align(0.5, 0.5):
                                for j in range(7):
                                    textbutton weekdays[j][0] xalign 0.5 background workshift_color[game.saved_schedules[i][j]]
                        else:
                            text _("Empty") italic True size res_font(18)

            null height yres(10)
            textbutton _("Cancel") action Hide("load_schedule", transition=Dissolve(0.15)) xalign 1.0


# screen autorest + level + perks → EXTRACTED to ui/screens/screen_progress.rpy (Phase 2)
# 升级/加点/作息 已提取到 screen_progress.rpy

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

screen home():

    tag menu
    use overlay("main")
    use right_menu
    use shortcuts()


############ Jman - Headhunter Mod ############
    if game.has_active_mod("Headhunter Mod"):
        if game.headhunter_girl:
            $ game.headhunter_button_enabled = 0
            if game.headhunter_time <= 0:
                if not game.interacting_with_headhunter:
                    textbutton HH_back_caption:
                        xalign HH_button_align["main x"]
                        yalign HH_button_align["main y"]
                        text_size HH_button_text_size
                        text_font HH_button_text_font
                        action Jump(HH_main_jump_label)
                        hovered tt.Action(HH_back_text)

            else:
                textbutton HH_wait_caption:
                    xalign HH_button_align["main x"]
                    yalign HH_button_align["main y"]
                    text_size HH_button_text_size
                    text_font HH_button_text_font
                    hovered tt.Action(HH_wait_text)
        else:
            $ game.headhunter_button_enabled = 1
############ Jman - Headhunter Mod End ########

    if always_show_brothel_report:
        use brothel_report

    button background None action (Hide("brothel_report"), ToggleVariable("always_show_brothel_report"), SelectedIf(always_show_brothel_report)) xalign 0.5 xmargin 25 ypos 0.1 :
        if not always_show_brothel_report:
            tooltip _("Click to keep the brothel report showing at all times.")
            hovered (Show("brothel_report"))
            unhovered Hide("brothel_report")
        else:
            tooltip _("Click to hide the brothel report.")

        hbox xalign 0.0 spacing 10:
            frame xalign 0.0 xsize xres(25) ysize yres(25):
                style "contrast_button"
                hover_background Frame("orange_button")
                selected_background Frame("darkorange_button")

                if always_show_brothel_report:
                    text "✓" font "resources/fonts/DejaVuSans.ttf" size res_font(14) xalign 0.5 yalign 0.5
                else:
                    text " " size res_font(14) xalign 0.5
            text _("Show brothel report") size res_font(14) xalign 0.0 yalign 0.5 drop_shadow (2, 2)


screen brothel_report():

    tag brothel_report

    if brothel.get_cleanliness() in ("disgusting", "fire"):
        default side_pic = "side sill sad"
        default shown_tip = __("Master!!! %s is very dirty... Please do something!") % brothel.name
    elif calendar.time == 1:
        default side_pic = "side sill happy"
        default shown_tip = __("Welcome to your new brothel, Master! I'm sure you will be a great manager!")
    elif logs[calendar.time-1] and logs[calendar.time-1].net < 0:
        default side_pic = "side sill sad"
        default shown_tip = __("Master!!! %s is losing money... What's going on?") % brothel.name
    else:
        default side_pic = "side sill happy"
        default shown_tip = __("{color=[c_lightblue]}Did you know? {/color}%s") % daily_tip

    frame:
        xanchor 1.0
        if screen_is_wide:
            xalign 0.85
            xsize 0.7
        else:
            xalign 0.775
            xsize 0.75
        ypos 0.15
        ysize 0.8
        xpadding xres(10)
        ypadding yres(10)

        has vbox spacing yres(10) xfill True

        hbox spacing xres(10):
            add side_pic zoom 0.5 xalign 0.0 
            textbutton _("Next\ntip") text_size 18 xalign 0.0 yalign 0.5:
                if always_show_brothel_report:
                    action SetLocalVariable("shown_tip", __("{color=[c_lightblue]}Did you know? {/color}%s") % rand_choice(random_tips))
            text shown_tip xalign 0.0 yalign 0.5 size res_font(18) justify True italic True xsize 0.8 color c_brown
            #? Why does the textbutton 'dance' around when changing tips? Investigate

        hbox spacing xres(20) xfill True yfill False:

            vbox:
                xsize 0.4
                xfill True
                yfill False

                text _("Yesterday") color c_prune

                text "" size res_font(14)

                if calendar.time > 1 and logs[calendar.time-1]:
                    text logs[calendar.time-1].get_day_report() size res_font(14) color c_brown

                    textbutton _("Show last night's log") xsize xres(250) ypadding 5 text_size res_font(14) xalign 0.5:
                        if always_show_brothel_report:
                            action (Show("previous_night_log", log=logs[calendar.time-1]))
                    textbutton _("Show satisfaction report") xsize xres(250) ypadding 5 text_size res_font(14) xalign 0.5:
                        if always_show_brothel_report:
                            action Call("latest_customer_satisfaction")

                else:
                    text _("Nothing to report") size res_font(14) italic True color c_brown

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                xfill True
                yfill False

                has vbox
                xfill True
                yfill False

                text _("Today") color c_prune

                text "" size res_font(14)

                text get_next_day_report() size res_font(14) color c_brown

                text "" size res_font(14)

                text brothel.get_ASM_report() size res_font(14) color c_brown

                text "" size res_font(14)

                text get_warnings() size res_font(14) color c_brown

# screen previous_night_log → EXTRACTED to ui/screens/screen_girl_log.rpy (Phase 2)
# 女孩日志/昨夜回顾 已提取到 screen_girl_log.rpy


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



## GIRL BROWSER

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


## START SCREEN

# screen quick_start → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy

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

screen active_spells():

    hbox box_wrap True:
        text _("Active:") size res_font(14) color c_brown yalign 0.5
        for spell in MC.active_spells:
            button xpadding 0 ypadding 0 xsize xres(40) ysize yres(40) action NullAction() tooltip "{b}" + spell.name + "{/b}: " + spell.description: # get_description("", spell.effects):
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
                                    $ extra = "(Auto-cast: " + s.auto.capitalize() + ")\n(Active)"

                                elif s.auto:
                                    $ col = c_firered
                                    $ extra = "(Auto-cast: " + s.auto.capitalize() + ")"

                                elif s in MC.active_spells:
                                    $ col = c_main
                                    $ extra = "(Active)"

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
            textbutton "{i}You do not know any spells yet. You must increase your level.{/i}" xalign 0.5 yalign 0.5 xsize xres(250) text_size res_font(18)

    if MC.active_spells:
        frame xalign 0.5 yalign 0.95 xmaximum 0.85 xpadding 20:
            use active_spells()




## CLASSES AND QUESTS POSTINGS

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
                            textbutton _("{image=img_star} %s {image=img_star}") % selected_quest.special xalign 0.0 yalign 0.5 ypadding 0 text_color c_orange background None action NullAction() hovered tt.Action(special_quest_description[selected_quest.special])

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
                                        text str(int(selected_quest.get_gold())) + " gold" size res_font(14) color c_brown
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
                                textbutton selected_quest.jp_target.capitalize() text_size res_font(14) text_color c_brown xalign 0.0 yalign 0.5 xpadding 0 ypadding 0 background None:
                                    action NullAction()
                                    tooltip "This class will give a small boost to %s Job Points (JP)." % selected_quest.jp_target


                            elif selected_quest.type == "quest":

                                text _("Reward") size res_font(18) color c_prune

                                text str(selected_quest.get_gold()) + " gold" size res_font(14) color c_brown

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
                            use girl_select(available_girls, action_button = ("Commit", (SetScreenVariable("clicked_quest", None), Return("commit")), ttip))
                        else:
                            use girl_select(available_girls, action_button = ("Commit", NullAction(), ttip))


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
                                    $ ttip += str(len(quest.enrolled)) + "/" + str(quest.capacity) + " are enrolled in this class"
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
                                                text str(int(quest.get_gold())) + " gold" size res_font(13)
                                            else:
                                                text _("FREE") size res_font(13)

                if calendar.active_contract:
                    text ""
                    text ""
                    button xfill True xpadding 6 ypadding 6 action Return("active_contract"): # hovered Show("contract_tab", contract=calendar.active_contract, x=450, active=True, transition=Dissolve(0.15)) unhovered Hide("contract_tab", transition=Dissolve(0.15)) tooltip (_("Show active contract (%s day%s left).") % (28-calendar.day, plural(28-calendar.day))):
                        vbox xfill True:
                            text _("Active contract") size res_font(14) color c_darkbrown xalign 0.5
                            add ProportionalScale("resources/ui/" + license_dict[1][1], *res_tb(50)) xalign 0.5





# screen dark_filter → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy


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



## FARM SCREENS ##

# screen farm_menu + farm_tab + minion_button + fshow_init → EXTRACTED to ui/screens/screen_farm.rpy (Phase 2)
# 农场/小黄人/展示 已提取到 screen_farm.rpy

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

# Generic event screen

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

# Profile details

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


## CHALLENGE SCREENS ##

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
                $ ttip = __("{b}%s challenge{/b}: This challenges your {b}%s{/b} (%s). Estimated difficulty: {b}%s{/b}.") % (__(chal.name_i18n), chal.stat.capitalize(), str_int(MC.get_stat(chal.stat)), chal.estimate_diff(diff=diff))

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
                                text chal.estimate_diff(diff=diff) size res_font(12)
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
                    textbutton __("Player %s: %s") % (chal.stat.capitalize(), str_int(MC.get_stat(chal.stat, raw=True))) text_size res_font(18) style "inv_no_padding"
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
                    text __("Opponent %s: %s") % (chal.stat.capitalize(), str_int(diff + opponent_bonus)) size res_font(18)
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

#### LETTER SCREEN ####

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


#### RESOURCES ####

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
        text "+" + str(round_int(number)) + " " + resource size res_font(28) yalign 0.5


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
                        button background None action NullAction() tooltip __("There is a shortage of %s this week. Value is going up.") % r.capitalize():
                            has hbox spacing 3
                            add resource.pic.get(*res_tb(20)) yalign 0.5
                            text "▲" size res_font(16) color c_emerald yalign 0.5 font "DejaVuSans.TTF"

                for r in calendar.discounted:
                    $ resource = resource_dict[r]
                    if resource.rank <= story_flags["builder license"]:
                        button background None action NullAction() tooltip __("%s is plentiful this week. Value is going down.") % r.capitalize():
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

                    button xfill True ysize yres(60) action (SetScreenVariable("source", resource), SetScreenVariable("source_name", resource.name), SetScreenVariable("source_nb", 0), SelectedIf(source==resource)) tooltip ("Trade your " + r + " for other resources"):
                        selected_background c_emerald
                        has hbox xfill True yfill True spacing 10
                        add resource.pic.get(*res_tb(40)) yalign 0.5
                        vbox xfill True spacing 6 yalign 0.5:
                            hbox spacing 3:
                                text resource.name.capitalize() size res_font(18)
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
                        tooltip "Sell your " + source_name + " for gold"
                        selected_background c_emerald

                    hbox xfill True yfill True spacing 10:
                        add ProportionalScale("resources/ui/coin.webp", *res_tb(40)) yalign 0.5
                        vbox xfill True spacing 6 yalign 0.5:
                            text _("Gold") size res_font(18)
                            if "gold" != source:
                                hbox spacing 6:
                                    $ rate = get_exchange_rate(source, "gold")
                                    if rate < 1:
                                        $ text2 = "Get 1 for " + str_dec(1/rate, 1)
                                    else:
                                        $ text2 = "Get " + str_dec(rate, 1) + " for 1"

                                    text text2 size res_font(14)
                                    add source.pic.get(*res_tb(16))

                for r in build_resources:
                    $ resource = resource_dict[r]

                    if resource.rank <= story_flags["builder license"]:

                        button xfill True ysize yres(60):
                            if resource != source:
                                action (SetScreenVariable("target", resource), SetScreenVariable("target_name", resource.name), SetScreenVariable("target_nb", 0), SelectedIf(resource==target))
                                tooltip "Trade " + r +" in exchange for your " + source_name
                                selected_background c_emerald
                            hbox xfill True yfill True spacing 10:
                                add resource.pic.get(*res_tb(40)) yalign 0.5
                                vbox xfill True spacing 6 yalign 0.5:
                                    hbox spacing 3:
                                        text resource.name.capitalize() size res_font(18)
                                        if r in calendar.discounted:
                                            text "▼" size res_font(14) yalign 0.5 font "DejaVuSans.TTF"
                                        elif r in calendar.scarce:
                                            text "▲" size res_font(14) yalign 0.5 font "DejaVuSans.TTF"
                                    if resource != source:
                                        hbox spacing 6:
                                            $ rate = get_exchange_rate(source, resource)
                                            if rate < 1:
                                                $ text2 = "Get 1 for " + str(round_up(1/rate))
                                            else:
                                                $ text2 = "Get " + str(round_up(rate)) + " for 1"

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
                    $ text1 = "Buy"
                else:
                    $ text1 = "Trade"

                textbutton text1 xalign 0.5 xsize 0.8 ysize yres(65):
                    if source == "gold" and MC.gold >= source_nb:
                        action Return(("gold", target_name, source_nb, target_nb))
                        tooltip "Buy " + str(target_nb) + " " + target_name + " for " + str(source_nb) + " " + target_name
                    elif MC.resources[source_name] >= source_nb:
                        action Return((source_name, target_name, source_nb, target_nb))
                        tooltip "Trade " + str(source_nb) + " " + source_name + " for " + str(target_nb) + " " + target_name

                textbutton "+" xsize xres(65) ysize yres(65) text_size res_font(32) xalign 1.0:
                    if rate < 1:
                        action (SetScreenVariable("target_nb", target_nb+1), SetScreenVariable("source_nb", round_up((target_nb+1)/rate)))
                    elif rate >= 1:
                        action (SetScreenVariable("source_nb", source_nb+1), SetScreenVariable("target_nb", round_up((source_nb+1)*rate)))



## MODAL INVISIBLE SCREEN ##

screen modal():

    modal True

screen invisible_button():

    zorder 20

    key "K_UP" action Function(renpy.notify, "Your precious keyboard can't save you now!")
    key "K_DOWN" action Function(renpy.notify, "Your precious keyboard can't save you now!")

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






## MOD SCREENS ##


screen mods():

    tag menu

    $ mod_list = list(detected_mods) # Creates a list of keys from the dictionary
    $ mod_list.sort() # Sorts mods by name

    use game_menu(_("Mods")):

        if mod_list:
            default selected_mod = detected_mods[mod_list[0]]
        else:
            default selected_mod = None

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
                            button xsize xres(140) action SelectedIf(selected_mod == mod) hovered SetScreenVariable("selected_mod", mod), SetField(mod, "seen", True):
                                if not mod.seen:
                                    at blink

                                text mod.name size res_font(18):
                                    if mod.active:
                                        bold True

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
                                $ text1 = ": %s" % girl.magic_training.capitalize()
                            elif topic.label == "slave_hypnotize_driver":
                                if MC.hypnotize_driver == "gold":
                                    $ text1 = " %s {image=img_gold}" % MC.hypnotize_driver
                                elif MC.hypnotize_driver == "mana":
                                    $ text1 = " %s {image=img_MP}" % MC.hypnotize_driver
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
                    textbutton k.capitalize() text_size res_font(18) action SetScreenVariable("pic", girl.get_pic(farm_holding_tags[k], soft=True))

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

                        textbutton fix.name.capitalize() + " " + act.capitalize() text_size res_font(14) action SetScreenVariable("pic", girl.get_fix_pic(act, fix, not_tags=not_tags))


#### GIRL MIXES ####

label girlpack_menu:
    menu:
        "Girl pack mix":

            menu:
                "Would you like to see girl ratings (this may take some time if you have many girl packs)?"

                "Yes":
                    call screen girl_mix(True) nopredict
                "No":
                    call screen girl_mix(False)

        "Update packstates":
            call packstates_menu from _call_packstates_menu

        "Cancel":
            pass

    return

label girlpack_menu_restart:
    hide screen main_menu

    call girlpack_menu() from _call_girlpack_menu

    $ renpy.full_restart()

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
                    textbutton mix_name.capitalize()[:25] action (SetField(persistent, "active_mix", mix_name), SelectedIf(persistent.active_mix==mix_name)) text_size res_font(18) text_selected_bold True tooltip "Click here to see the %s girl mix." % mix_name.capitalize()
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
                    $ ttip = "{b}%s{/b} {i}by %s{/i}\n%s\n\nVersion: %s\n\nDescription: %s\n\n" % (pack_name, gpinfo_dict[gp]["creator"], {True: event_color["good"] % "Unique girl", False: "Generic girl"}[gpinfo_dict[gp]["unique"]], gpinfo_dict[gp]["version"], gpinfo_dict[gp]["description"])

                    if filter.lower() in pack_name.lower():
                        if show_rating:
                            $ rating, rtg_text = get_girlpack_rating(path=gp)

                        hbox spacing 12:

                            button xfill True ysize yres(82) ymargin 0 ypadding 0:
                                if gp in persistent.girl_mix[persistent.active_mix]:
                                    action RemoveFromSet(persistent.girl_mix[persistent.active_mix], gp)
                                    tooltip ttip + "{i}Click to remove this girl pack from the mix.{/i}"
                                else:
                                    idle_background None
                                    action AddToSet(persistent.girl_mix[persistent.active_mix], gp)
                                    tooltip ttip + "{i}Click to add this girl pack to the mix.{/i}"

                                hbox spacing 12 yalign 0.5:
                                    frame xalign 0.0 yalign 0.5 xsize xres(80) background None:
                                        add fast_portrait(gp, *res_tb(70)) xalign 0.5 yalign 0.5

                                    vbox xsize xres(360) yalign 0.5:
                                        text pack_name + {True: event_color["good"] % " (unique)", False: ""}[gpinfo_dict[gp]["unique"]] drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" size res_font(18)
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

## ACHIEVEMENT SCREENS ##

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



## CONTRACT SCREENS ##

init:
    transform contract_result_transform:
        alpha 0.0
        linear 0.25 alpha 1.0

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
                text (_("The %s") % contract.location.name) drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" color c_brown
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
            text (_("The %s") % contract.location.name) drop_shadow (1, 1) font "resources/fonts/MATURASC.ttf" color c_brown
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
                            text str_int(tsk.value) + " gold" color c_darkgold yalign 0.5 size res_font(13) at contract_result_transform
                        else:
                            text _("{color=[c_red]}{i}Failed{/i}{/color}") yalign 0.5 size res_font(13) at contract_result_transform

        hbox:
            vbox xsize xres(320) spacing 3:
                text _("Bonus requirement") size res_font(16) bold True color c_prune
                text contract.get_special_description() size res_font(13) color c_brown
            if t >= len(contract.tasks) + 1:
                if contract.special_bonus != 1.0:
                    text str(contract.get_special_value()) + " gold" color c_darkgold yalign 0.5 size res_font(13) at contract_result_transform
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

screen increment_counter(startv = 0, stopv = 1000, duration = 3.0, _caption = "%s gold", _background = None, _size = 16, _color = c_white, _sound=s_gold): # Displays an incremental counter counting from startv to stopv

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

screen increment_display(title="", _caption="%s gold", pic=None, side_pic=None, startv = 0, stopv = 1000, duration=3.0, _size = 16, _color = c_white, _sound=s_gold):

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


## EVIL POWERS SCREENS ## Thanks to who designed these screens

## Overlay

# MC mojo points (topscreen)
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

label pic_test(tags, _size=220, **kwargs):

    python:
        pics=[]
        for girl in (MC.girls + farm.girls + slavemarket.girls):
            pics.append(girl.get_pic(tags, **kwargs))

    call screen pic_tester(pics, _size)

    return

label farm_pic_test(act, min_type, _size=220):

    python:
        pics=[]
        for girl in (MC.girls + farm.girls + slavemarket.girls):
            pics.append(farm.get_girl_pic(girl, act, min_type))

    call screen pic_tester(pics, _size)

    return

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


#### Mod specific ####

#<Chris12 PackState>
label packstates_menu :
    hide screen main_menu

    menu:
        "Welcome to the packstate feature (courtesy of {color=[c_magenta]}{b}Chris12{/b}{/color})"
        "Introduction to Packstates" :
            $ packdir = GirlFilesDict.get_packstate_directory()
            "Oftentimes, a Girlpack creator may wish to change some of the picture names to better fit Brothel King's tagging system. The packstate feature helps updating girlpacks without having to download hundreds of pictures all over again."
            "" "{b}Packstates{/b} contain all the necessary information to keep the tags of a Girlpack up to date. These files need to be put into the {color=[c_magenta]}/game/[packdir]{/color} directory and named exactly like the girlpack they are for."
            "" "During the renaming process, a {b}log file{/b} is created in the BrothelKing main directory\n({color=[c_magenta]}packstate_log.txt{/color}), showing in detail everything that was changed."
            "" "You can also do a {b}simulation{/b}. This creates the same log file, but without actually renaming any files. This lets you check which changes would be made, without any risk."
            "" "No files are actually deleted. Instead, unwanted files are tagged as {b}_TRASH{/b}. These files will not get used by BrothelKing, so you can safely just leave them there, or delete them for real. You may notice the duplicate tag on some _TRASH files - these are duplicates of existing images."
            "" "If you have added your own images, they will get tagged as {b}_UNRECOGNIZED{/b} by default. They will still get used by BrothelKing."
            "Please note that {b}duplicates{/b} only get detected for recognized images. You can change this behavior in the {b}packstates menu{/b} (Ignore will not even rename them, Hide will prevent them from showing in the game)."
            "" "That's all! Why not try a {b}simulation{/b} and see if the {color=[c_magenta]}/packstate_log.txt{/color} shows any useful changes?"
            jump packstates_menu

        "Unrecognized Images: [preferences.packstate_unrecognized]":
            menu:
                "Hide: Rename and don't show unrecognized images.\nRename: Rename unrecognized images, but show them.\nIgnore: Don't rename unrecognized images. Will also show them.\n   Removes any _UNRECOGNIZED tags again.\n(Renaming means adding _UNRECOGNIZED as tag to the filename)"
                "Hide":
                    $ preferences.packstate_unrecognized = "Hide"
                    jump packstates_menu
                "Rename":
                    $ preferences.packstate_unrecognized = "Rename"
                    jump packstates_menu
                "Ignore":
                    $ preferences.packstate_unrecognized = "Ignore"
                    jump packstates_menu
                "Back (don't change setting)":
                    jump packstates_menu

        "Simulation" :
            python:
                GirlFilesDict.import_packstates(simulate = True)
                # renpy.full_restart()

        "Apply packstate" :
            menu:
                "It is recommended that you backup your girls folder and run a simulation beforehand. There is no Undo operation!{fast}{nw}"
                "Continue" :
                    python:
                        GirlFilesDict.import_packstates(simulate = False) # if files get renamed, this will call renpy.utter_restart() on its own
                        # renpy.full_restart() # only gets called if no files are renamed
                "Back" :
                    jump packstates_menu
        "Back" :
            pass
    return
#</Chris12 PackState>


# This screen has been added for the specific needs of the Harem mod by maxxronoa

# This adds a 'Chat' button to certain trainers in the brothel screen when harem mode is activated

screen harem_button():
    textbutton _("Chat") xsize xres(75) xalign 0.09 yalign 0.25 action Jump("harem_" + MC.current_trainer.name.lower()) hovered tt.Action("Talk to " + MC.current_trainer.name + ".")

#### END OF BK SCREENS FILE ####
