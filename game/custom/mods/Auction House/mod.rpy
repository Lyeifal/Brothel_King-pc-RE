################################################################################
##  Auction House — Mod 入口 | Mod entry (Mod API v2)
##  EN: Registers the auction house through Mod API v2 and provides the home
##      right-menu button. Core logic lives in auction.rpy, UI in
##      auction_screens.rpy.
##  ZH: 通过 Mod API v2 注册拍卖行并提供主页右侧菜单按钮。
##      核心逻辑在 auction.rpy，UI 在 auction_screens.rpy。
##
##  EN: v2 mods are always active once installed (no per-save toggle); remove
##      this folder from game/custom/mods/ to disable.
##  ZH: v2 Mod 安装后即常驻激活（无逐存档开关）；停用请删除
##      game/custom/mods/ 下的本文件夹。
################################################################################

init -1 python:

    services.mod_api_v2.register_mod("auction_house", {
        "name": __("Auction House"),
        "version": "2.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("The auction house lets you buy and sell girls through bidding. Access it from the right menu (Mods) on the home screen."),
        "requires": [],
        "hooks": {},
        "dependencies": [],
        "home_rightmenu_add_buttons": ["right_menu_auction"],
    })


################
## Home - Right menu - Auction House button (moved from screen_home.rpy)
## EN: Kept the same screen name so existing behavior is unchanged.
## ZH: 保持原屏幕名，行为不变。
################

screen right_menu_auction():

    hbox xalign 1.0 spacing 20:
        text ""

        textbutton _("Auction") style_group "rm":
            action Show("auction_house")
            tooltip __("访问拍卖行买卖女孩。")
