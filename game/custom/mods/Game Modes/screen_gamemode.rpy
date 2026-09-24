################################################################################
##  Game Mode & Origin Selection Screens — BK Evolution (Game Modes Mod)
##  EN: Visual screens for choosing game mode and player origin.
##      Moved from game/core/systems/gamemodes/screen_gamemode.rpy.
##      The mode cards are generated from gamemode_registry (registry-driven):
##      each GameMode instance supplies its display name, description and
##      optional ui_color / ui_icon metadata.
##  ZH: 选择游戏模式和玩家出身的视觉界面。
##      原位于 game/core/systems/gamemodes/screen_gamemode.rpy。
##      模式卡片由 gamemode_registry 驱动生成：每个 GameMode 实例提供
##      显示名称、描述以及可选的 ui_color / ui_icon 元数据。
################################################################################

## EN: Mode selection screen — card-based layout, registry-driven.
## ZH: 模式选择屏幕 — 卡片式布局，由注册表驱动。
screen game_mode_select():

    tag menu
    modal True

    ## EN: All registered modes (story/sandbox/scenario live in this mod,
    ##     other mods may add their own GameMode subclasses).
    ## ZH: 所有已注册模式（story/sandbox/scenario 在本 Mod 中，
    ##     其他 Mod 也可以注册自己的 GameMode 子类）。
    python:
        _modes = gamemode_registry.list_mode_instances()

    frame:
        xfill True
        yfill True
        background c_black

        vbox:
            xalign 0.5
            yalign 0.1
            spacing 20

            text __("选择你的道路"):
                size 48
                xalign 0.5
                color "#FFD700"
                outlines [(2, "#000", 0, 0)]

            text __("选择一种游戏模式开始你的旅程。"):
                size 24
                xalign 0.5
                color "#CCCCCC"

        if not _modes:

            ## EN: Defensive fallback — normally unreachable while this mod
            ##     is installed, since the three modes are registered at init.
            ## ZH: 防御性回退 —— 只要本 Mod 已安装就不会走到这里，
            ##     因为三个模式在初始化时已注册。
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 20

                text __("当前没有安装任何游戏模式。"):
                    size 28
                    xalign 0.5
                    color "#FF6B6B"

                textbutton __("以剧情模式继续"):
                    xalign 0.5
                    action [SetVariable("game_mode", GameMode.MODE_STORY), Return()]

        else:

            ## EN: Mode cards in a horizontal row, one per registered mode.
            ## ZH: 模式卡片横向排列，每个已注册模式一张。
            hbox:
                xalign 0.5
                yalign 0.5
                spacing 30

                for _mode in _modes:
                    use mode_card(mode=_mode)


## EN: Individual mode card — populated from the GameMode instance.
## ZH: 单个模式卡片 —— 内容由 GameMode 实例提供。
screen mode_card(mode):

    button:
        xsize 320
        ysize 400
        background c_ui_dark
        hover_background c_ui_darker

        action [SetVariable("game_mode", mode.mode_id), Return()]

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 15
            xfill True

            ## EN: Color strip at top (mod-provided, defaults to grey).
            ## ZH: 顶部彩色条（由 Mod 提供，默认为灰色）。
            frame:
                xsize 280
                ysize 6
                background (mode.ui_color or "#888888")
                xalign 0.5

            text mode.get_name():
                size 28
                xalign 0.5
                color (mode.ui_color or "#FFFFFF")
                bold True
                text_align 0.5

            text mode.get_description():
                size 18
                xalign 0.5
                xsize 280
                color "#DDDDDD"
                text_align 0.5

            null height 20

            text __("点击选择"):
                size 16
                xalign 0.5
                color "#888888"
                italic True
