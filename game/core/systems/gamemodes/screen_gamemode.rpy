################################################################################
##  Game Mode & Origin Selection Screens — BK Evolution
##  EN: Visual screens for choosing game mode and player origin.
##  ZH: 选择游戏模式和玩家出身的视觉界面。
################################################################################

## EN: Mode selection screen — card-based layout.
## ZH: 模式选择屏幕 — 卡片式布局。
screen game_mode_select():

    tag menu
    modal True

    frame:
        xfill True
        yfill True
        background "bg black"

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

        ## EN: Mode cards in a horizontal row.
        ## ZH: 模式卡片横向排列。
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 30

            use mode_card(
                mode_id=GameMode.MODE_STORY,
                title=__("剧情模式"),
                desc=__("跟随史诗般的主线剧情，包含章节推进、叙事目标和戏剧性事件。推荐给首次游玩的玩家。"),
                color="#FF6B6B",
                icon="mode_story"
            )

            use mode_card(
                mode_id=GameMode.MODE_SANDBOX,
                title=__("沙盒模式"),
                desc=__("在没有剧情锁定的情况下打造你自己的道路。选择你的出身和独特天赋。适合想要自由的资深玩家。"),
                color="#4ECDC4",
                icon="mode_sandbox"
            )

            use mode_card(
                mode_id=GameMode.MODE_SCENARIO,
                title=__("剧本模式"),
                desc=__("游玩社区创作的剧本，包含自定义规则和胜利条件。新剧本可通过 Mod 添加。"),
                color="#9B59B6",
                icon="mode_scenario"
            )


## EN: Individual mode card.
## ZH: 单个模式卡片。
screen mode_card(mode_id, title, desc, color, icon):

    button:
        xsize 320
        ysize 400
        background Frame("gui/frame.png", 10, 10)
        hover_background Frame("gui/frame_hover.png", 10, 10)

        action [SetVariable("game_mode", mode_id), Return()]

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 15
            xfill True

            ## EN: Color strip at top.
            ## ZH: 顶部彩色条。
            frame:
                xsize 280
                ysize 6
                background color
                xalign 0.5

            text title:
                size 28
                xalign 0.5
                color color
                bold True
                text_align 0.5

            text desc:
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
        background "bg black"

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
                background Frame("gui/frame.png", 10, 10)

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
                background Frame("gui/frame.png", 10, 10)

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
        background "bg black"

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
                    background Frame("gui/frame.png", 10, 10)

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

                                        text "v[sc.version] by [sc.author]":
                                            size 14
                                            color "#888888"
                                            xalign 0.5

                frame:
                    xsize 450
                    ysize 500
                    background Frame("gui/frame.png", 10, 10)

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
                                text "[key]: [val]":
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
