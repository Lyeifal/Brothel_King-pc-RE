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

# screen suzume_hints + restock_button + inventory_filter + girl_select + main_character → EXTRACTED to ui/screens/screen_misc2.rpy (Phase 2)
# 主角面板/提示/详情面板 已提取到 screen_misc2.rpy

# screen active_spells + spellbook + postings + challenge_menu + challenge + letter → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

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

# screen modal + invisible_button + mods + free_girl_interact + girl_interact + free_girl_stats + debug_pics → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

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

# screen girl_mix → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

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
# screen mojo_bar + power_detail + power_draw + power_hand + power_card + power_card_content + power_target + girl_vp_selector + mojo_payment + mojo_trade + micro_transac + brothel_ranking + scroll_list + brothel_ranking_button → EXTRACTED to ui/screens/screen_powers.rpy (Phase 2)
# 邪恶力量/卡牌/排名 已提取到 screen_powers.rpy

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

# screen pic_tester → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy
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

# screen harem_button → EXTRACTED to ui/screens/screen_powers.rpy (Phase 2)
# 邪恶力量/卡牌/排名 已提取到 screen_powers.rpy
