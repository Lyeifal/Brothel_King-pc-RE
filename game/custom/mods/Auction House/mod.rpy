################################################################################
##  Auction House — Mod 入口 | Mod entry (Mod API v2)
##  EN: Registers the auction house through Mod API v2 and provides the home
##      right-menu button. Core logic lives in auction.rpy, UI in
##      auction_screens.rpy, and the scenario-driven session in
##      auction_scene.rpy.
##  ZH: 通过 Mod API v2 注册拍卖行并提供主页右侧菜单按钮。
##      核心逻辑在 auction.rpy，UI 在 auction_screens.rpy，
##      场景化拍卖流程在 auction_scene.rpy。
##
##  EN: v2 mods are always active once installed (no per-save toggle); remove
##      this folder from game/custom/mods/ to disable.
##  ZH: v2 Mod 安装后即常驻激活（无逐存档开关）；停用请删除
##      game/custom/mods/ 下的本文件夹。
################################################################################

init -1 python:

    services.mod_api_v2.register_mod("auction_house", {
        "name": __("Auction House"),
        "version": "2.1",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("The auction house holds sales every 7 days (days 1/8/15/22 of each month); the first sale each month is a grand auction with rare items. Bid on girls and items, or list your own goods for a fee. Access it from the right menu on the home screen on auction days."),
        "requires": [],
        "hooks": {},
        "dependencies": [],
        "home_rightmenu_add_buttons": ["right_menu_auction"],
        "home_rightmenu_anchor": "before_shop",
    })


################
## Home - Right menu - Auction House button
## EN: Entry point into the scenario-driven label. The button is only
##     sensitive on auction days; the tooltip shows the next auction day
##     and whether it will be a grand auction.
## ZH: 场景化 label 的入口。按钮仅在拍卖日可点击；
##     悬浮提示显示下次拍卖日期及是否为大拍卖。
################

screen right_menu_auction():

    hbox xalign 1.0 spacing 20:
        text ""

        textbutton _("Auction") style_group "rm":
            action Call("auction_scene")
            sensitive (auction_house.can_hold_auction())
            tooltip auction_house.get_menu_tooltip()
