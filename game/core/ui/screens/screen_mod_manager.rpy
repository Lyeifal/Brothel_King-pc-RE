################################################################################
##  Mod Manager — 主菜单 v2 Mod 管理界面
##  EN: Main-menu screen listing every registered v2 mod (Mod API v2) with its
##      name, version, author and enable state. Toggles only edit a pending
##      dict; nothing is written until the player clicks OK, which applies all
##      pending changes via ModAPIV2.apply_pending_changes() and saves
##      persistent._bk_v2_mod_states. Back / right-click discards pending.
##      Changes take full effect after a restart (no hot reload). Opened from
##      the main-menu "Mods" button via Show("mod_manager").
##  ZH: 主菜单界面，列出全部已注册 v2 Mod（Mod API v2）的名称、版本、
##      作者与启用状态。切换只写入待应用字典；玩家点击「确定」才通过
##      ModAPIV2.apply_pending_changes() 批量生效并保存
##      persistent._bk_v2_mod_states；「返回」/右键丢弃待应用更改。
##      不做热重载，重启游戏后完全生效。由主菜单 "Mods" 按钮
##      （Show("mod_manager")）打开。
################################################################################

screen mod_manager():

    modal True

    ## EN: zorder overlay on top of the main menu.
    ## ZH: 浮层叠在主菜单之上。
    zorder 10

    ## EN: Backdrop — draw the main menu art inside this screen (do not rely
    ##     on screen main_menu still being composited under us) with a light
    ##     dim. A heavy black dim over the dark theme art looked pitch black.
    ## ZH: 背景——在本屏幕内直接绘制主菜单图（不依赖 screen main_menu
    ##     仍在下方合成），加轻度压暗。此前重度黑色压暗叠在暗色
    ##     主题图上看起来一片漆黑。
    add gui.main_menu_background
    add Solid("#00000040")

    ## EN: Pending toggle states {mod_id: bool}; empty = nothing to apply.
    ## ZH: 待应用的开关状态 {mod_id: 布尔}；为空表示没有待应用更改。
    default pending = {}

    ## EN: This screen is opened from the main menu via Show("mod_manager"),
    ##     so it must be closed with Hide (Return would end the main menu's
    ##     interaction without removing this overlay). OK applies the pending
    ##     changes, closes the screen and surfaces a transient restart notice.
    ## ZH: 本屏幕由主菜单 Show("mod_manager") 打开，因此必须用 Hide
    ##     关闭（Return 会结束主菜单的交互但不移除此浮层）。「确定」应用
    ##     待更改、关闭界面，并以临时通知提示重启后完全生效。

    python:
        _mod_rows = []
        for _mid in mod_api_v2.list_registered_mods():
            _info = mod_api_v2.get_mod_info(_mid) or {}
            _always_on = bool(_info.get("always_on"))
            _enabled = mod_api_v2.is_mod_enabled(_mid)
            ## EN: Displayed state = pending override or persisted state.
            ## ZH: 显示状态 = 待应用覆盖值或持久化值。
            _disp = pending.get(_mid, _enabled)
            _mod_rows.append((
                _mid,
                _info,
                _always_on,
                _enabled,
                _disp,
                mod_api_v2.missing_dependencies(_mid),
            ))
        ## EN: True when any pending value differs from the persisted one.
        ## ZH: 任一待应用值与持久化值不同即为真。
        _dirty = any(_disp != _enabled for _mid, _info, _always_on, _enabled, _disp, _missing in _mod_rows)

    ## EN: Toggle actions build the next pending dict inline with
    ##     dict(list(...) + [(k, v)]) — a nested def inside a screen python
    ##     block cannot see screen variables (NameError), and ** unpacking
    ##     in screen actions is best avoided.
    ## ZH: 切换动作用 dict(list(...) + [(k, v)]) 内联构造新待应用字典——
    ##     屏幕 python 块内嵌的 def 读不到屏幕变量（NameError），
    ##     屏幕动作里也最好避免 ** 解包。

    key "mouseup_3" action Hide("mod_manager")

    frame:
        xalign 0.5
        yalign 0.5
        xsize xres(900)
        ysize yres(640)
        background c_ui_light
        xpadding xres(24)
        ypadding yres(20)

        vbox:
            xfill True
            yfill True
            spacing yres(12)

            text _("Mod 管理") size res_font(30) bold True color "#9A6A00" xalign 0.5

            if not _mod_rows:

                text _("没有安装任何 v2 Mod。") size res_font(18) color "#7A6A52" xalign 0.5 yalign 0.5

            else:

                viewport:
                    yfill True
                    mousewheel True
                    draggable True
                    scrollbars "vertical"

                    vbox:
                        xfill True
                        spacing yres(8)

                        for _mid, _info, _always_on, _enabled, _disp, _missing in _mod_rows:

                            frame:
                                xfill True
                                background c_ui_light
                                xpadding xres(12)
                                ypadding yres(8)

                                hbox:
                                    xfill True
                                    spacing xres(10)

                                    vbox:
                                        xfill True
                                        spacing yres(2)

                                        ## EN: The whole name row is the toggle —
                                        ##     clicking the mod name (or the green
                                        ##     check) flips its pending state.
                                        ##     always_on mods render as plain text.
                                        ## ZH: 整行名字都是开关——点击 Mod 名
                                        ##     （或绿色对勾）即切换待应用状态。
                                        ##     常驻 Mod 显示为纯文本。
                                        if _always_on:
                                            hbox:
                                                spacing xres(6)
                                                text (_info.get("name") or _mid) size res_font(20) bold True color "#3B2F20" yalign 0.5
                                                text "✓" size res_font(20) bold True color "#1E8449" yalign 0.5
                                        else:
                                            button:
                                                xalign 0.0
                                                background None
                                                action SetScreenVariable("pending", dict(list(pending.items()) + [(_mid, (not _disp))]))

                                                hbox:
                                                    spacing xres(6)

                                                    text ((_info.get("name") or _mid) + (" ✓" if _disp else "")) size res_font(20) bold True color "#3B2F20" yalign 0.5

                                                    ## EN: Pending marker — toggled but
                                                    ##     not yet applied.
                                                    ## ZH: 待应用标记——已切换但尚未生效。
                                                    if _disp != _enabled:
                                                        text _("(未应用)") size res_font(13) color "#B03A2E" yalign 0.5

                                        text __("v%s · %s") % (_info.get("version") or "?", _info.get("author") or __("未知")) size res_font(14) color "#7A6A52"

                                        if _missing:
                                            text __("缺少前置: %s") % ", ".join(_missing) size res_font(14) color "#B03A2E"

                                    vbox:
                                        yalign 0.5
                                        spacing yres(4)
                                        xsize xres(150)

                                        ## EN: High-contrast status badge — solid
                                        ##     background, state visible at a glance.
                                        ## ZH: 高对比状态徽章——纯色底色，一眼可辨。
                                        frame:
                                            xalign 1.0
                                            xpadding xres(10)
                                            ypadding yres(3)
                                            if _always_on:
                                                background Solid("#B9770E")
                                            elif _missing:
                                                background Solid("#7B241C")
                                            elif _disp:
                                                background Solid("#1E8449")
                                            else:
                                                background Solid("#5D6D7E")

                                            if _always_on:
                                                text _("常驻") size res_font(15) bold True color "#FFFFFF"
                                            elif _missing:
                                                text _("未激活") size res_font(15) bold True color "#FFFFFF"
                                            elif _disp:
                                                text _("已启用") size res_font(15) bold True color "#FFFFFF"
                                            else:
                                                text _("已禁用") size res_font(15) bold True color "#FFFFFF"

                                        ## EN: always_on mods cannot be toggled.
                                        ## ZH: always_on 的 Mod 不可切换。
                                        if not _always_on:
                                            textbutton (_("禁用") if _disp else _("启用")):
                                                xalign 1.0
                                                text_size res_font(16)
                                                action SetScreenVariable("pending", dict(list(pending.items()) + [(_mid, (not _disp))]))

            if _dirty:
                text _("有未应用的更改——点击「确定」生效，「返回」放弃。") size res_font(15) color "#B03A2E" xalign 0.5

            ## EN: Bottom bar — OK applies all pending changes and closes the
            ##     screen with a transient restart notice; Back discards.
            ## ZH: 底部栏——「确定」应用全部待更改、以临时通知提示重启后
            ##     生效并关闭界面；「返回」丢弃。
            hbox:
                xalign 0.5
                spacing xres(30)

                textbutton _("确定"):
                    sensitive _dirty
                    text_size res_font(18)
                    action [Function(mod_api_v2.apply_pending_changes, pending), Function(renpy.save_persistent), Function(notify, __("更改将在重启游戏后完全生效。"), col=c_gold), Hide("mod_manager")]

                textbutton _("返回"):
                    text_size res_font(18)
                    action Hide("mod_manager")
