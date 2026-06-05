################################################################################
##  Courtyard Screens — BK Evolution
##  EN: UI for managing the courtyard: viewing housed girls, facilities, training.
##  ZH: 别院管理 UI：查看安置女孩、设施、训练。
################################################################################

## EN: Main courtyard management screen.
## ZH: 别院管理主屏幕。
screen courtyard():

    tag menu
    modal True

    default selected_girl = None
    default selected_facility = None

    frame:
        xfill True
        yfill True
        background "bg black"

        vbox:
            xalign 0.5
            yalign 0.05
            spacing 10

            text __("别院"):
                size 42
                xalign 0.5
                color "#4ECDC4"
                outlines [(2, "#000", 0, 0)]

            hbox:
                xalign 0.5
                spacing 20

                text __("女孩: [len(courtyard.girls)] / [courtyard.MAX_CAPACITY]"):
                    size 18
                    color "#FFFFFF"

                text __("每日维护: [courtyard.get_daily_upkeep()] 金币"):
                    size 18
                    color "#FFD700"

        hbox:
            xalign 0.5
            yalign 0.55
            spacing 20

            ## EN: Left panel — girl list.
            ## ZH: 左侧面板 — 女孩列表。
            frame:
                xsize 360
                ysize 520
                background Frame("gui/frame.png", 10, 10)

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 6
                        xfill True

                        for girl in courtyard.girls:
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
                                            text "M: [girl.mood]":
                                                size 13
                                                color "#FF69B4"
                                                xalign 1.0

                                        if hasattr(girl, "energy"):
                                            text "E: [girl.energy]":
                                                size 13
                                                color "#4ECDC4"
                                                xalign 1.0

            ## EN: Middle panel — selected girl details & actions.
            ## ZH: 中间面板 — 选中女孩详情与操作。
            frame:
                xsize 340
                ysize 520
                background Frame("gui/frame.png", 10, 10)

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

                        if hasattr(selected_girl, "job"):
                            text "[selected_girl.job]":
                                size 16
                                xalign 0.5
                                color "#BBBBBB"

                        null height 10

                        hbox:
                            xalign 0.5
                            spacing 15

                            if hasattr(selected_girl, "mood"):
                                text "Mood: [selected_girl.mood]":
                                    size 16
                                    color "#FF69B4"

                            if hasattr(selected_girl, "energy"):
                                text "Energy: [selected_girl.energy]":
                                    size 16
                                    color "#4ECDC4"

                        null height 20

                        textbutton __("返回青楼"):
                            xalign 0.5
                            sensitive (len(MC.girls) < 24)
                            action [Function(courtyard.move_to_brothel, selected_girl),
                                    SetScreenVariable("selected_girl", None)]

                        if not (len(MC.girls) < 24):
                            text __("青楼已达最大工作容量(24)"):
                                size 14
                                xalign 0.5
                                color "#E74C3C"
                                italic True

                        textbutton __("训练(缓慢)"):
                            xalign 0.5
                            action Function(courtyard.train_girl, selected_girl, "obedience", 1)

                        textbutton __("释放"):
                            xalign 0.5
                            action [Function(courtyard.remove_girl, selected_girl),
                                    SetScreenVariable("selected_girl", None)]

                else:
                    text __("选择一个女孩进行管理。"):
                        size 18
                        xalign 0.5
                        yalign 0.5
                        color "#888888"
                        text_align 0.5

            ## EN: Right panel — facilities.
            ## ZH: 右侧面板 — 设施。
            frame:
                xsize 300
                ysize 520
                background Frame("gui/frame.png", 10, 10)

                vbox:
                    spacing 10
                    xfill True
                    xalign 0.5
                    yalign 0.1

                    text __("设施"):
                        size 24
                        xalign 0.5
                        color "#FFD700"
                        underline True

                    for fid, facility in courtyard.facilities.items():
                        vbox:
                            spacing 4
                            xfill True

                            hbox:
                                xfill True

                                text facility.get_name():
                                    size 18
                                    color "#FFFFFF"
                                    bold True

                                text "Lv.[facility.upgrade_level]/[facility.max_level]":
                                    size 14
                                    color "#AAAAAA"
                                    xalign 1.0

                            text facility.get_description():
                                size 14
                                color "#BBBBBB"
                                text_align 0.5

                            if facility.upgrade_level < facility.max_level:
                                $ next_cost = facility.upgrade_cost.get(facility.upgrade_level + 1, 0)
                                textbutton __("升级 ([next_cost] 金币)"):
                                    xalign 0.5
                                    sensitive (MC.gold >= next_cost)
                                    action Function(facility.upgrade, MC)
                            else:
                                text __("最高等级"):
                                    size 13
                                    xalign 0.5
                                    color "#2ECC71"
                                    italic True

        ## EN: Bottom close button.
        ## ZH: 底部关闭按钮。
        textbutton __("关闭"):
            xalign 0.5
            yalign 0.95
            action [Return(), Hide("courtyard")]
