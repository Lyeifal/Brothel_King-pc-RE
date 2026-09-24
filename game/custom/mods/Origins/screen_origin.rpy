################################################################################
##  Origin Selection Screen — Origins Mod
##  EN: Moved from the Game Modes mod (screen_gamemode.rpy), extended with the
##      origin's unique class name and spell-tree size. Sets the store global
##      _selected_origin_id on confirm; core start.rpy resolves it into
##      _selected_origin.
##  ZH: 自 Game Modes Mod 迁入（screen_gamemode.rpy），扩展显示出身的
##      独特职业名与技能树规模。确认时设置 store 全局
##      _selected_origin_id；核心 start.rpy 将其解析为 _selected_origin。
################################################################################

## EN: Origin selection screen — vertical list with details.
## ZH: 出身选择屏幕 — 带详情的纵向列表。
screen origin_select():

    tag menu
    modal True

    default selected_origin = None

    python:
        ## EN: Make sure the origins' classes are registered so the preview
        ##     can count the spell tree (covers screens shown before the
        ##     first MC.update_spells call).
        ## ZH: 确保出身职业已注册，预览可以统计技能树规模
        ##     （覆盖在首次 MC.update_spells 之前打开屏幕的情况）。
        try:
            origins_ensure_classes()
        except Exception:
            pass

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

            text __("你的出身决定你的独特职业、技能树与起始天赋。"):
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

                        ## EN: Unique class + spell tree preview.
                        ## ZH: 独特职业 + 技能树预览。
                        if selected_origin.class_id:
                            null height 5

                            text __("独特职业: [selected_origin.get_class_name()]"):
                                size 20
                                xalign 0.5
                                color "#FFD700"
                                bold True

                            text __("%d 个职业技能，随主角等级自动领悟（法术书界面查看）") % len(selected_origin.class_def.get("spellbook", [])):
                                size 15
                                xalign 0.5
                                xsize 400
                                color "#AAAAAA"
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
