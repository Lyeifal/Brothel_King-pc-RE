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

# screen tax_tooltip + tax_tab + adv_tooltip + girls + girl_tab + girl_pick_badge + badge_button + girl_button + girl_fast_actions + button_overlay + rank_level_details → EXTRACTED to ui/screens/screen_misc.rpy (Phase 2)
# 悬浮层/女孩列表控件 已提取到 screen_misc.rpy

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

        

# screen districts + district_button + visit_district + visit_location + matchmaking + customer_satisfaction → EXTRACTED to ui/screens/screen_districts.rpy (Phase 2)
# 城区/地点/配对/顾客满意度 已提取到 screen_districts.rpy

# screen home + brothel_report → EXTRACTED to ui/screens/screen_home.rpy (Phase 2)
# 主页/青楼报告 已提取到 screen_home.rpy


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
