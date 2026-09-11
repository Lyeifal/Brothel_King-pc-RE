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


## EN: Origin selection screen — vertical list with details.
## ZH: 出身选择屏幕 — 带详情的纵向列表。
screen origin_select():

    tag menu
    modal True

    default selected_origin = None

    frame:
        xfill True
        yfill True
        background c_black

        vbox:
            xalign 0.5
            yalign 0.05
            spacing 15

            text __("选择你的出身"):
                size 44
                xalign 0.5
                color "#FFD700"
                outlines [(2, "#000", 0, 0)]

            text __("你的背景决定了你的起始天赋和加成。"):
                size 20
                xalign 0.5
                color "#AAAAAA"

        ## EN: Left panel — origin list. Right panel — details.
        ## ZH: 左侧面板 — 出身列表。右侧面板 — 详情。
        hbox:
            xalign 0.5
            yalign 0.55
            spacing 30

            ## EN: Origin list.
            ## ZH: 出身列表。
            frame:
                xsize 350
                ysize 500
                background c_ui_dark

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 8
                        xfill True

                        for origin in origin_registry.list_origins():
                            button:
                                xfill True
                                ysize 60
                                background "#333333"
                                hover_background "#555555"
                                selected_background "#444466"
                                selected (selected_origin == origin)

                                action SetScreenVariable("selected_origin", origin)

                                hbox:
                                    spacing 10
                                    xalign 0.5
                                    yalign 0.5

                                    text origin.get_name():
                                        size 22
                                        color "#FFFFFF"
                                        yalign 0.5

            ## EN: Detail panel.
            ## ZH: 详情面板。
            frame:
                xsize 450
                ysize 500
                background c_ui_dark

                vbox:
                    spacing 15
                    xfill True
                    xalign 0.5
                    yalign 0.1

                    if selected_origin:
                        text selected_origin.get_name():
                            size 32
                            xalign 0.5
                            color "#4ECDC4"
                            bold True

                        text selected_origin.get_description():
                            size 18
                            xalign 0.5
                            xsize 400
                            color "#DDDDDD"
                            text_align 0.5

                        null height 15

                        text __("天赋"):
                            size 22
                            xalign 0.5
                            color "#FFD700"
                            underline True

                        for talent in selected_origin.talents:
                            vbox:
                                xalign 0.5
                                spacing 4

                                text talent.get_name():
                                    size 18
                                    xalign 0.5
                                    color "#FFFFFF"
                                    bold True

                                text talent.get_description():
                                    size 16
                                    xalign 0.5
                                    xsize 380
                                    color "#BBBBBB"
                                    text_align 0.5

                        if selected_origin.starting_bonus:
                            null height 15
                            text __("起始奖励"):
                                size 22
                                xalign 0.5
                                color "#FFD700"
                                underline True

                            for key, val in selected_origin.starting_bonus.items():
                                text __("{b}[key]{/b}: +[val]"):
                                    size 16
                                    xalign 0.5
                                    color "#AAAAAA"

                        null height 30

                        textbutton __("确认选择"):
                            xalign 0.5
                            action [SetVariable("_selected_origin_id", selected_origin.origin_id), Return()]

                    else:
                        text __("从列表中选择一个出身以查看详情。"):
                            size 20
                            xalign 0.5
                            yalign 0.5
                            color "#888888"
                            text_align 0.5


## EN: Scenario selection screen.
## ZH: 剧本选择屏幕。
screen scenario_select():

    tag menu
    modal True

    default selected_scenario = None

    frame:
        xfill True
        yfill True
        background c_black

        vbox:
            xalign 0.5
            yalign 0.05
            spacing 15

            text __("选择剧本"):
                size 44
                xalign 0.5
                color "#FFD700"
                outlines [(2, "#000", 0, 0)]

        python:
            _scenarios = scenario_registry.list_scenarios()

        if not _scenarios:
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 20

                text __("当前没有安装任何剧本。"):
                    size 28
                    xalign 0.5
                    color "#FF6B6B"

                text __("剧本可以通过 Mod 添加。将回退到沙盒模式。"):
                    size 20
                    xalign 0.5
                    color "#AAAAAA"

                textbutton __("继续"):
                    xalign 0.5
                    action [SetVariable("game_mode", GameMode.MODE_SANDBOX), Return()]
        else:
            hbox:
                xalign 0.5
                yalign 0.55
                spacing 30

                frame:
                    xsize 350
                    ysize 500
                    background c_ui_dark

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            spacing 8
                            xfill True

                            for sc in _scenarios:
                                button:
                                    xfill True
                                    ysize 70
                                    background "#333333"
                                    hover_background "#555555"
                                    selected_background "#444466"
                                    selected (selected_scenario == sc)

                                    action SetScreenVariable("selected_scenario", sc)

                                    vbox:
                                        xalign 0.5
                                        yalign 0.5
                                        spacing 2

                                        text sc.get_name():
                                            size 20
                                            color "#FFFFFF"
                                            xalign 0.5

                                        text _("v[sc.version] by [sc.author]"):
                                            size 14
                                            color "#888888"
                                            xalign 0.5

                frame:
                    xsize 450
                    ysize 500
                    background c_ui_dark

                    vbox:
                        spacing 15
                        xfill True
                        xalign 0.5
                        yalign 0.1

                        if selected_scenario:
                            text selected_scenario.get_name():
                                size 32
                                xalign 0.5
                                color "#9B59B6"
                                bold True

                            text selected_scenario.get_description():
                                size 18
                                xalign 0.5
                                xsize 400
                                color "#DDDDDD"
                                text_align 0.5

                            null height 15

                            text __("规则"):
                                size 22
                                xalign 0.5
                                color "#FFD700"
                                underline True

                            for key, val in selected_scenario.rules.items():
                                text _("[key]: [val]"):
                                    size 16
                                    xalign 0.5
                                    color "#BBBBBB"

                            null height 30

                            textbutton __("开始剧本"):
                                xalign 0.5
                                action [SetVariable("_selected_scenario_id", selected_scenario.scenario_id), Return()]
                        else:
                            text __("选择一个剧本以查看详情。"):
                                size 20
                                xalign 0.5
                                yalign 0.5
                                color "#888888"
                                text_align 0.5
