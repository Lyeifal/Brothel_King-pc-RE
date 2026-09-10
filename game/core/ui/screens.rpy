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

# screen tax_tooltip + tax_tab + adv_tooltip + girls + girl_tab + girl_pick_badge + badge_button + girl_button + girl_fast_actions → EXTRACTED to ui/screens/screen_misc.rpy (Phase 2)
# 悬浮层/女孩列表控件 已提取到 screen_misc.rpy

# screen girl_profile → EXTRACTED to ui/screens/screen_girl_profile.rpy (Phase 3.1)

# screen stat_bar + custom_bar + girl_stats + assign_job + girl_stats_light → EXTRACTED to ui/screens/screen_girl_stats.rpy (Phase 2)
# 女孩属性/属性条/特性详情 已提取到 screen_girl_stats.rpy

# screen button_overlay + rank_level_details → EXTRACTED to ui/screens/screen_misc.rpy (Phase 2)
# 悬浮层/女孩列表控件 已提取到 screen_misc.rpy

## GIRL TAB

# screen schedule + save_schedule + load_schedule → EXTRACTED to ui/screens/screen_schedule.rpy (Phase 2)
# 日程安排/保存/读取 已提取到 screen_schedule.rpy

## SCHEDULE SCREEN

# screen autorest + level + perks → EXTRACTED to ui/screens/screen_progress.rpy (Phase 2)
# 升级/加点/作息 已提取到 screen_progress.rpy

## LEVEL & PERKS SCREEN

# screen trait_details + perk_details → EXTRACTED to ui/screens/screen_girl_stats.rpy (Phase 2)
# 女孩属性/属性条/特性详情 已提取到 screen_girl_stats.rpy

## GIRL LOG SCREEN ## Displays statistics about each girl

# screen girl_log → EXTRACTED to ui/screens/screen_girl_log.rpy (Phase 2)
# 女孩日志/昨夜回顾 已提取到 screen_girl_log.rpy

## DISTRICT SCREEN ##

# screen suzume_hints → EXTRACTED to ui/screens/screen_misc2.rpy (Phase 2)
# 主角面板/提示/详情面板 已提取到 screen_misc2.rpy

# screen districts + district_button + visit_district + visit_location + matchmaking + customer_satisfaction → EXTRACTED to ui/screens/screen_districts.rpy (Phase 2)
# 城区/地点/配对/顾客满意度 已提取到 screen_districts.rpy

## BROTHEL SCREEN ##

# screen brothel + furniture + brothel_options → EXTRACTED to ui/screens/screen_brothel.rpy (Phase 3.1)
# 青楼/家具/选项界面已提取到 screen_brothel.rpy

## RIGHT MENU : this is the main menu on the main screen (not named main menu to avoid confusion with the standard Renpy screen)

# screen home + brothel_report → EXTRACTED to ui/screens/screen_home.rpy (Phase 2)
# 主页/青楼报告 已提取到 screen_home.rpy

# screen previous_night_log → EXTRACTED to ui/screens/screen_girl_log.rpy (Phase 2)
# 女孩日志/昨夜回顾 已提取到 screen_girl_log.rpy

## Yes / No Confirmation (used for buying, selling...)

# screen yes_no + OK_screen + show_img + show_event + show_sex_event → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy

# show_img, show_event and show_sex_event do basically the same thing and have finally been merged into show_event. Hurray!

## Ok message (used for giving information...)

# screen shortcuts → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy

## Shortcuts

# screen close → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy

## Close button

# screen receive_item → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy

## ITEMS

# Inventory screens are located in BKitems.rpy

# screen restock_button + inventory_filter → EXTRACTED to ui/screens/screen_misc2.rpy (Phase 2)
# 主角面板/提示/详情面板 已提取到 screen_misc2.rpy

## GIRL BROWSER

# screen girl_select → EXTRACTED to ui/screens/screen_misc2.rpy (Phase 2)
# 主角面板/提示/详情面板 已提取到 screen_misc2.rpy

## START SCREEN

# screen quick_start → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy

## MAIN CHARACTER SCREEN

# screen main_character → EXTRACTED to ui/screens/screen_misc2.rpy (Phase 2)
# 主角面板/提示/详情面板 已提取到 screen_misc2.rpy

# screen active_spells + spellbook → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

## CLASSES AND QUESTS POSTINGS

# screen postings → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

# screen dark_filter → EXTRACTED to ui/screens/screen_common.rpy (Phase 2)
# 通用组件 已提取到 screen_common.rpy

# screen personality_screen + notebook → EXTRACTED to ui/screens/screen_misc2.rpy (Phase 2)
# 主角面板/提示/详情面板 已提取到 screen_misc2.rpy

## FARM SCREENS ##

# screen farm_menu + farm_tab + minion_button + fshow_init → EXTRACTED to ui/screens/screen_farm.rpy (Phase 2)
# 农场/小黄人/展示 已提取到 screen_farm.rpy

# Generic event screen

# Profile details

# screen fshow_screen + farm_show_gold + generic_event_screen + mood_details + love_button + fear_button + sex_details → EXTRACTED to ui/screens/screen_misc2.rpy (Phase 2)
# 主角面板/提示/详情面板 已提取到 screen_misc2.rpy

## CHALLENGE SCREENS ##

# screen challenge_menu + challenge → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

#### LETTER SCREEN ####

# screen letter → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

#### RESOURCES ####

# screen resource_tab + resource_gain + resource_exchange → EXTRACTED to ui/screens/screen_resources.rpy (Phase 2)
# 资源/成就/契约 已提取到 screen_resources.rpy

## MODAL INVISIBLE SCREEN ##

# screen modal + invisible_button → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

## MOD SCREENS ##

# screen mods + free_girl_interact + girl_interact + free_girl_stats + debug_pics → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

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

# screen girl_mix → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

label girlpack_menu_restart:
    hide screen main_menu

    call girlpack_menu() from _call_girlpack_menu

    $ renpy.full_restart()

## ACHIEVEMENT SCREENS ##

# screen achievement_notification + crystal_display + achievements → EXTRACTED to ui/screens/screen_resources.rpy (Phase 2)
# 资源/成就/契约 已提取到 screen_resources.rpy

## CONTRACT SCREENS ##

init:
    transform contract_result_transform:
        alpha 0.0
        linear 0.25 alpha 1.0

# screen contracts + contract_tab + pick_girl + contract_result + increment_counter + increment_display + auction_brothel + goal_ttip → EXTRACTED to ui/screens/screen_resources.rpy (Phase 2)
# 资源/成就/契约 已提取到 screen_resources.rpy

## EVIL POWERS SCREENS ## Thanks to who designed these screens

## Overlay

# MC mojo points (topscreen)

# screen mojo_bar + power_detail + power_draw + power_hand + power_card + power_card_content + power_target + girl_vp_selector + mojo_payment + mojo_trade + micro_transac + brothel_ranking + scroll_list + brothel_ranking_button → EXTRACTED to ui/screens/screen_powers.rpy (Phase 2)
# 邪恶力量/卡牌/排名 已提取到 screen_powers.rpy

## Cards

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

# screen pic_tester → EXTRACTED to ui/screens/screen_quest.rpy (Phase 2)
# 任务/挑战/互动/mod 已提取到 screen_quest.rpy

#### Mod specific ####

# This screen has been added for the specific needs of the Harem mod by maxxronoa
# This adds a 'Chat' button to certain trainers in the brothel screen when harem mode is activated

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

# screen harem_button → EXTRACTED to ui/screens/screen_powers.rpy (Phase 2)
# 邪恶力量/卡牌/排名 已提取到 screen_powers.rpy

#### END OF BK SCREENS FILE ####
