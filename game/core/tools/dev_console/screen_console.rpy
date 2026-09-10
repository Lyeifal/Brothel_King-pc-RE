#### Dev Console — Ren'Py screen UI ####
# Phase 6.3: Interactive developer console for debugging and inspection.
# Toggle: Shift+O (letter O) — only when config.developer is True.
#
# Commands: help, girls, gold, stats, event, heal, repair, services, profile
# Python expressions are evaluated directly.

# ── Console state (global list for output) ──
default console_output_lines = [
    "{color=[c_emerald]}{b}Dev Console{/b}{/color} — Type 'help' for commands."
]

screen dev_console():
    modal True
    zorder 100

    default console_input = ""

    key "K_ESCAPE" action Hide("dev_console")

    # EN: Shift+O must also be bound INSIDE the screen: the screen is modal,
    #     and modal screens block all events from reaching displayables below
    #     (including the global underlay Keymap), so the underlay binding can
    #     open the console but can never close it.
    # ZH: Shift+O 也必须在屏幕内部绑定：本屏幕是 modal，modal 屏幕会阻断
    #     事件传向下层（包括全局 underlay Keymap），因此 underlay 绑定只能
    #     打开控制台，无法在控制台显示期间将其关闭。
    key "shift_K_o" action Function(_console_toggle)

    frame:
        xalign 0.5
        yalign 0.0
        xsize 950
        ysize 520
        background Solid("#0a0a0aEE")

        vbox:
            spacing 8
            xfill True
            yfill True

            # ── Title bar ──
            hbox:
                text "{b}Dev Console{/b}" size 16 color c_emerald
                null width 20
                text "(Shift+O or Esc to close)" size 12 color "#888888" yalign 0.5
                null width 20
                textbutton "Clear" text_size 12 action Function(console_clear) xalign 1.0

            # ── Output area ──
            viewport:
                ysize 400
                yinitial 1.0
                scrollbars "vertical"
                mousewheel True
                xfill True
                vbox:
                    for line in console_output_lines:
                        text line size 13 color "#CCCCCC"

            # ── Input area ──
            # EN: Use a button with default=True to capture Enter key.
            # ZH: 使用 default=True 的按钮来捕获回车键。
            hbox:
                spacing 5
                text ">>>" size 15 color c_emerald yalign 0.5
                input:
                    id "console_input"
                    value ScreenVariableInputValue("console_input")
                    size 15
                    color "#FFFFFF"
                    xsize 800
                    copypaste True
                textbutton "Run" text_size 13:
                    action [
                        Function(console_execute, console_input),
                        SetScreenVariable("console_input", ""),
                    ]
                    yalign 0.5
                    xpadding 10


init -1 python:

    def console_execute(text):
        """Execute a console command and append result to output."""
        text = text.strip()
        if not text:
            return

        console = services.get("dev_console")
        if console is None:
            console_output_lines.append("{color=[c_red]}Console not available.{/color}")
            return

        result = console.execute(text)

        # Add input + result to output
        console_output_lines.append(">>> {color=[c_emerald]}%s{/color}" % text)
        for line in result.split("\n"):
            console_output_lines.append("    " + line)

        # Trim history
        while len(console_output_lines) > 300:
            console_output_lines.pop(0)

    def console_clear():
        """Clear console output."""
        global console_output_lines
        console_output_lines = [
            "{color=[c_emerald]}{b}Dev Console{/b}{/color} — Type 'help' for commands."
        ]


# ── Key binding: Shift+O to toggle (when developer mode) ──
# EN: Binding mechanism, in two parts:
#     1. config.keymap["console_toggle"] + a renpy.Keymap appended to
#        config.underlay opens the console globally (underlay displayables
#        receive key events whenever no modal screen is on top).
#     2. The dev_console screen itself is modal, so while it is shown the
#        underlay never sees keys. The screen's own `key "shift_K_o"`
#        statement (above) handles closing. Both paths call _console_toggle.
#     The keysym "shift_K_o" means Shift held + letter O.
# ZH: 绑定机制分两部分：
#     1. config.keymap["console_toggle"] + 追加到 config.underlay 的
#        renpy.Keymap 负责全局打开（无 modal 屏幕遮挡时 underlay 能收到按键）。
#     2. dev_console 屏幕本身是 modal，显示期间 underlay 收不到按键，
#        由屏幕内的 `key "shift_K_o"` 语句负责关闭。两条路径都调用
#        _console_toggle。keysym "shift_K_o" 表示按住 Shift + 字母 O。

init -1 python:

    def _console_toggle():
        # EN: Toggle the dev console (developer mode only). While the console
        #     input widget holds keyboard focus, Shift+O is ignored so that
        #     typing a capital "O" does not close the console.
        # ZH: 开关控制台（仅开发者模式）。输入框持有键盘焦点时不切换，
        #     避免输入大写字母 O 时误关控制台。
        if not config.developer:
            return
        try:
            if renpy.display.focus.get_focused() is renpy.get_widget("dev_console", "console_input"):
                return
        except Exception:
            pass  # EN: Screen not shown or widget lookup failed | ZH: 屏幕未显示或控件查找失败
        if renpy.get_screen("dev_console"):
            renpy.hide_screen("dev_console")
        else:
            renpy.show_screen("dev_console")

    # EN: See the comment block above for why this is "shift_K_o" and why the
    #     screen also binds the same key. Direct assignment (not setdefault)
    #     so a stale/wrong value can never survive a restart.
    # ZH: 为何用 "shift_K_o"、为何屏幕内也绑定同一按键，见上方注释块。
    #     用直接赋值而非 setdefault，保证错误的旧值不会在重启后残留。
    config.keymap["console_toggle"] = ["shift_K_o"]
    config.underlay.append(
        renpy.Keymap(console_toggle=_console_toggle)
    )
