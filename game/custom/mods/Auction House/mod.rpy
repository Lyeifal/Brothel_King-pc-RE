################################################################################
##  Auction House — Mod 入口 | Mod entry
##  EN: Mod declaration and home right-menu button for the auction house.
##  ZH: 拍卖行 Mod 声明与主页右侧菜单按钮。
##
##  EN: This mod was extracted from game/core/systems/auction/ (BK Evolution).
##      The v1 Mod() mechanism is used because Mod API v2 hook points are not
##      wired into game flow yet; migrate to register_mod() once they are.
##  ZH: 本 Mod 提取自 game/core/systems/auction/（BK Evolution）。
##      因 Mod API v2 钩子点尚未接入游戏流程，此处使用可用的 v1 Mod() 机制；
##      待钩子接线后可迁移至 register_mod()。
################################################################################

init -1 python:

    auction_house_mod = Mod(
        ## EN: Basic mod information. ZH: Mod 基本信息。
        name = __("Auction House"),
        folder = "Auction House",
        creator = "BK Evolution",
        version = 1.0,
        description = __("The auction house lets you buy and sell girls through bidding. Access it from the right menu (Mods) on the home screen."),

        ## EN: Button shown in the home right menu under "Mods" (screen name).
        ## ZH: 主页右侧菜单 "Mods" 下显示的按钮（屏幕名）。
        home_rightmenu_add_buttons = ["right_menu_auction"],
    )


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
