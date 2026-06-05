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

            text __("Choose Your Path"):
                size 48
                xalign 0.5
                color "#FFD700"
                outlines [(2, "#000", 0, 0)]

            text __("Select a game mode to begin your journey."):
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
                title=__("Story Mode"),
                desc=__("Follow the epic main storyline with chapter-based progression, narrative goals, and dramatic events. Recommended for first-time players."),
                color="#FF6B6B",
                icon="mode_story"
            )

            use mode_card(
                mode_id=GameMode.MODE_SANDBOX,
                title=__("Sandbox Mode"),
                desc=__("Forge your own path without story locks. Choose your origin and unique talents. Perfect for experienced players who want freedom."),
                color="#4ECDC4",
                icon="mode_sandbox"
            )

            use mode_card(
                mode_id=GameMode.MODE_SCENARIO,
                title=__("Scenario Mode"),
                desc=__("Play a community-created scenario with custom rules and victory conditions. New scenarios can be added via Mods."),
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

            text __("Click to select"):
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

            text __("Choose Your Origin"):
                size 44
                xalign 0.5
                color "#FFD700"
                outlines [(2, "#000", 0, 0)]

            text __("Your background determines your starting talents and bonuses."):
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

                        text __("Talents"):
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
                            text __("Starting Bonus"):
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

                        textbutton __("Confirm Selection"):
                            xalign 0.5
                            action [SetVariable("_selected_origin_id", selected_origin.origin_id), Return()]

                    else:
                        text __("Select an origin from the list to see details."):
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

            text __("Select a Scenario"):
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

                text __("No scenarios are currently installed."):
                    size 28
                    xalign 0.5
                    color "#FF6B6B"

                text __("Scenarios can be added via Mods. Falling back to Sandbox mode."):
                    size 20
                    xalign 0.5
                    color "#AAAAAA"

                textbutton __("Continue"):
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

                            text __("Rules"):
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

                            textbutton __("Play Scenario"):
                                xalign 0.5
                                action [SetVariable("_selected_scenario_id", selected_scenario.scenario_id), Return()]
                        else:
                            text __("Select a scenario to see details."):
                                size 20
                                xalign 0.5
                                yalign 0.5
                                color "#888888"
                                text_align 0.5
