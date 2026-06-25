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
                text "(Shift+O to close, Esc to close)" size 12 color "#888888" yalign 0.5
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
                text ">>>" size 15 color c_emerald yalign 0.5 xpadding 5
                input:
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


# ── Key binding: O key to toggle (when developer mode) ──
# Press O to open/close the dev console.

init -1 python:

    def _console_toggle():
        if config.developer:
            if renpy.get_screen("dev_console"):
                renpy.hide_screen("dev_console")
            else:
                renpy.show_screen("dev_console")

    # Register as a keymap entry (works globally in Ren'Py)
    config.keymap.setdefault("console_toggle", ["K_o"])
    config.underlay.append(
        renpy.Keymap(console_toggle=_console_toggle)
    )
