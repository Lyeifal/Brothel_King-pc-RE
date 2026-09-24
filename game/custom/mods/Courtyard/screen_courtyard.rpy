################################################################################
##  Courtyard Screens — BK Evolution ("Courtyard" mod v2.0)
##  EN: UI for the scenario-driven courtyard visit. The screen is transparent
##      (no fullscreen black frame) and modal: the villa scene with Sill shows
##      through around the panels. It is called with `call screen` from label
##      courtyard_scene; every button returns an ("action", ...) tuple that the
##      label handles — no Function() actions are used here, so the main
##      interaction loop is never involved.
##  ZH: 场景化别院的 UI。屏幕为透明背景（无全屏黑框）且 modal：
##      别院场景与 Sill 从面板边缘透出。由 courtyard_scene label 以
##      `call screen` 方式调用；所有按钮一律返回 ("action", ...) 元组由
##      label 统一处理——此处不使用 Function() action，
##      主交互循环完全不介入。
################################################################################


## EN: Main courtyard management screen.
##     Shown with `call screen` from label courtyard_scene (v2.0).
## ZH: 别院管理主屏幕。由 courtyard_scene label 以 `call screen` 方式显示（v2.0）。
screen courtyard():

    modal True

    ## EN: Right-click leaves the villa (handled by the label, like every
    ##     other action).
    ## ZH: 右键离开别院（与其他操作一样由 label 处理）。
    key "mouseup_3" action Return(("close",))

    default selected_girl = None

    ## EN: Precompute values for text interpolation (function calls are not allowed inside [ ]).
    ## ZH: 预先计算文本插值用的值（[ ] 内不允许函数调用）。
    python:
        _courtyard_girl_count = len(courtyard_villa.girls)
        _courtyard_room_limit = courtyard_villa.room_limit()
        _courtyard_rent = courtyard_villa.get_daily_rent()
        _courtyard_upkeep = courtyard_villa.get_daily_upkeep()
        _courtyard_brothel_full = (len(MC.girls) >= 24)
        _courtyard_expansion_offer = courtyard_villa.can_buy_expansion()

    ## EN: Title/status panel — transparent margins let the villa show around it.
    ## ZH: 标题/状态面板——边缘透明，透出别院场景。
    frame:
        xalign 0.5
        yalign 0.02
        xpadding 24
        ypadding 8
        background c_ui_dark

        hbox:
            spacing 25
            yalign 0.5

            text __("Courtyard"):
                size 24
                color "#4ECDC4"
                bold True
                yalign 0.5

            text __("Girls: [_courtyard_girl_count] / [_courtyard_room_limit]"):
                size 18
                color "#FFFFFF"
                yalign 0.5

            text __("Rent today: [_courtyard_rent] gold"):
                size 18
                color "#FFD700"
                yalign 0.5

            text __("Upkeep: [_courtyard_upkeep] gold"):
                size 18
                color "#BBBBBB"
                yalign 0.5

    hbox:
        xalign 0.5
        yalign 0.52
        spacing 20

        ## EN: Left panel — girl list.
        ## ZH: 左侧面板 — 女孩列表。
        frame:
            xsize 360
            ysize 480
            background c_ui_dark

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 6
                    xfill True

                    for girl in courtyard_villa.girls:
                        button:
                            xfill True
                            ysize 60
                            background "#333333"
                            hover_background "#555555"
                            selected_background "#444466"
                            selected (selected_girl == girl)

                            action SetScreenVariable("selected_girl", girl)

                            hbox:
                                spacing 10
                                xfill True
                                yalign 0.5

                                text girl.name:
                                    size 18
                                    color "#FFFFFF"
                                    yalign 0.5

                                vbox:
                                    xalign 1.0
                                    yalign 0.5
                                    spacing 2

                                    if hasattr(girl, "mood"):
                                        text _("M: [girl.mood]"):
                                            size 13
                                            color "#FF69B4"
                                            xalign 1.0

                                    if hasattr(girl, "energy"):
                                        text _("E: [girl.energy]"):
                                            size 13
                                            color "#4ECDC4"
                                            xalign 1.0

        ## EN: Middle panel — selected girl details & actions.
        ## ZH: 中间面板 — 选中女孩详情与操作。
        frame:
            xsize 340
            ysize 480
            background c_ui_dark

            if selected_girl:
                vbox:
                    spacing 12
                    xfill True
                    xalign 0.5
                    yalign 0.1

                    text selected_girl.name:
                        size 26
                        xalign 0.5
                        color "#FFFFFF"
                        bold True

                    if getattr(selected_girl, "job", None):
                        text selected_girl.job.capitalize():
                            size 16
                            xalign 0.5
                            color "#BBBBBB"

                    null height 10

                    hbox:
                        xalign 0.5
                        spacing 15

                        if hasattr(selected_girl, "mood"):
                            text _("Mood: [selected_girl.mood]"):
                                size 16
                                color "#FF69B4"

                        if hasattr(selected_girl, "energy"):
                            text _("Energy: [selected_girl.energy]"):
                                size 16
                                color "#4ECDC4"

                    null height 20

                    textbutton __("Return to Brothel"):
                        xalign 0.5
                        sensitive (not _courtyard_brothel_full)
                        action Return(("move_brothel", selected_girl))

                    if _courtyard_brothel_full:
                        text __("The brothel is at maximum working capacity (24)."):
                            size 14
                            xalign 0.5
                            color "#E74C3C"
                            italic True

                    textbutton __("Train (slow)"):
                        xalign 0.5
                        sensitive (selected_girl not in courtyard_villa.trained_today)
                        action Return(("train", selected_girl))

                    if selected_girl in courtyard_villa.trained_today:
                        text __("Already trained today."):
                            size 13
                            xalign 0.5
                            color "#888888"
                            italic True

                    textbutton __("Release"):
                        xalign 0.5
                        action Return(("release", selected_girl))

            else:
                text __("Select a girl to manage."):
                    size 18
                    xalign 0.5
                    yalign 0.5
                    color "#888888"
                    text_align 0.5

        ## EN: Right panel — facilities, rent reminder and expansion deed.
        ## ZH: 右侧面板 — 设施、租金提示与扩建地契。
        frame:
            xsize 300
            ysize 480
            background c_ui_dark

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 10
                    xfill True
                    xalign 0.5
                    yalign 0.1

                    text __("Facilities"):
                        size 24
                        xalign 0.5
                        color "#FFD700"
                        underline True

                    for fid, facility in courtyard_villa.facilities.items():
                        vbox:
                            spacing 4
                            xfill True

                            hbox:
                                xfill True

                                text facility.get_name():
                                    size 18
                                    color "#FFFFFF"
                                    bold True

                                text __("Lv. [facility.upgrade_level]/[facility.max_level]"):
                                    size 14
                                    color "#AAAAAA"
                                    xalign 1.0

                            text facility.get_description():
                                size 14
                                color "#BBBBBB"
                                text_align 0.5

                            if facility.upgrade_level < facility.max_level:
                                $ next_cost = facility.upgrade_cost.get(facility.upgrade_level + 1, 0)
                                textbutton __("Upgrade ([next_cost] gold)"):
                                    xalign 0.5
                                    sensitive (MC.gold >= next_cost)
                                    action Return(("upgrade", fid))
                            else:
                                text __("Max level"):
                                    size 13
                                    xalign 0.5
                                    color "#2ECC71"
                                    italic True

                    null height 10

                    ## EN: Rent reminder — same formula as process_day().
                    ## ZH: 租金提示——与 process_day() 同一公式。
                    text __("Rent scales with district rank, difficulty and the number of housed girls; idle girls' skills decay over time."):
                        size 13
                        xalign 0.5
                        color "#888888"
                        text_align 0.5

                    ## EN: Villa expansion deed (final district, not bought yet).
                    ## ZH: 别院扩建地契（最终区域、尚未购买时显示）。
                    if _courtyard_expansion_offer:
                        null height 6

                        textbutton __("Buy Courtyard Expansion Deed ([courtyard_villa.EXPANSION_PRICE] gold)"):
                            xalign 0.5
                            sensitive (MC.gold >= courtyard_villa.EXPANSION_PRICE)
                            action Return(("buy_expansion",))

                            text_size 14

                    elif courtyard_villa.expansion_unlocked:
                        text __("Expansion complete — capacity [courtyard_villa.MAX_CAPACITY]"):
                            size 13
                            xalign 0.5
                            color "#2ECC71"
                            text_align 0.5

    ## EN: Bottom close button.
    ## ZH: 底部关闭按钮。
    textbutton __("Close"):
        xalign 0.5
        yalign 0.97
        action Return(("close",))
