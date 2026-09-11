################################################################################
##  Mod Manager — 主菜单 v2 Mod 管理界面
##  EN: Main-menu screen listing every registered v2 mod (Mod API v2) with its
##      name, version, author and enable state. Toggling a mod writes
##      persistent._bk_v2_mod_states via ModAPIV2.set_mod_enabled(); the change
##      takes full effect after a restart (no hot reload). Opened from the
##      main-menu "Mods" button via Show("mod_manager").
##  ZH: 主菜单界面，列出全部已注册 v2 Mod（Mod API v2）的名称、版本、
##      作者与启用状态。切换开关经 ModAPIV2.set_mod_enabled() 写入
##      persistent._bk_v2_mod_states，重启游戏后完全生效（不做热重载）。
##      由主菜单 "Mods" 按钮（Show("mod_manager")）打开。
################################################################################

screen mod_manager():

    modal True

    ## EN: tag menu — replaces the main menu screen while shown; Return()
    ##     drops back into the main-menu interaction loop.
    ## ZH: tag menu —— 显示时替换主菜单屏幕；Return() 回到主菜单交互循环。
    tag menu

    ## EN: Dim the main menu behind the popup.
    ## ZH: 压暗弹窗背后的主菜单。
    add Solid("#000000B3")

    ## EN: Set to True after any toggle, to surface the restart notice.
    ## ZH: 任何切换后置真，用于显示重启提示。
    default show_restart_hint = False

    python:
        _mod_rows = []
        for _mid in mod_api_v2.list_registered_mods():
            _info = mod_api_v2.get_mod_info(_mid) or {}
            _mod_rows.append((
                _mid,
                _info,
                bool(_info.get("always_on")),
                mod_api_v2.is_mod_enabled(_mid),
                mod_api_v2.missing_dependencies(_mid),
            ))

    key "mouseup_3" action Return()

    frame:
        xalign 0.5
        yalign 0.5
        xsize xres(900)
        ysize yres(640)
        background c_ui_darker
        xpadding xres(24)
        ypadding yres(20)

        vbox:
            xfill True
            yfill True
            spacing yres(12)

            text _("Mod 管理") size res_font(30) bold True color c_darkorange xalign 0.5

            if not _mod_rows:

                text _("没有安装任何 v2 Mod。") size res_font(18) color c_grey xalign 0.5 yalign 0.5

            else:

                viewport:
                    yfill True
                    mousewheel True
                    draggable True
                    scrollbars "vertical"

                    vbox:
                        xfill True
                        spacing yres(8)

                        for _mid, _info, _always_on, _enabled, _missing in _mod_rows:

                            frame:
                                xfill True
                                background c_ui_dark
                                xpadding xres(12)
                                ypadding yres(8)

                                hbox:
                                    xfill True
                                    spacing xres(10)

                                    vbox:
                                        xfill True
                                        spacing yres(2)

                                        text (_info.get("name") or _mid) size res_font(20) bold True color c_white

                                        text __("v%s · %s") % (_info.get("version") or "?", _info.get("author") or __("未知")) size res_font(14) color c_grey

                                        if _missing:
                                            text __("缺少前置: %s") % ", ".join(_missing) size res_font(14) color c_red

                                    vbox:
                                        yalign 0.5
                                        spacing yres(4)
                                        xsize xres(150)

                                        if _always_on:
                                            text _("常驻") size res_font(16) color c_darkorange xalign 1.0
                                        elif _missing:
                                            text _("未激活") size res_font(16) color c_red xalign 1.0
                                        elif _enabled:
                                            text _("已启用") size res_font(16) color c_emerald xalign 1.0
                                        else:
                                            text _("已禁用") size res_font(16) color c_grey xalign 1.0

                                        ## EN: always_on mods cannot be toggled.
                                        ## ZH: always_on 的 Mod 不可切换。
                                        if not _always_on:
                                            textbutton (_("禁用") if _enabled else _("启用")):
                                                xalign 1.0
                                                text_size res_font(16)
                                                action [Function(mod_api_v2.set_mod_enabled, _mid, not _enabled), Function(renpy.save_persistent), SetScreenVariable("show_restart_hint", True)]

            if show_restart_hint:
                text _("更改将在重启游戏后完全生效。") size res_font(15) color c_darkorange xalign 0.5

            ## EN: Bottom return button (drops back to the main menu).
            ## ZH: 底部返回按钮（回到主菜单）。
            textbutton _("返回") action Return() xalign 0.5
