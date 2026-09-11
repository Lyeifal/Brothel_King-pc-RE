################################################################################
##  Courtyard Scene — BK Evolution ("Courtyard" mod v2.0)
##  EN: Scenario-driven courtyard visit: the villa backdrop (mansion interior,
##      an existing game background) with Sill as the caretaker. Opening
##      flavor dialogue reports the current rent and room status; when the
##      brothel has reached the final district and the expansion has not been
##      bought yet, Sill pitches the villa expansion deed (10,000,000 gold).
##      The label then calls the transparent courtyard screen and handles the
##      ("action", ...) tuples it returns — no Function() actions are used
##      here, so the main interaction loop is never involved. At the end the
##      label discards the Call() return point (same trick as teleport) and
##      jumps back to main.
##  ZH: 场景化别院：背景用游戏现有素材（宅邸内景），管家为 Sill。
##      开场 flavor 对话汇报当前租金与房间状况；若青楼已抵达最终区域
##      且尚未购买扩建，Sill 会推销别院扩建地契（10,000,000 金币）。
##      随后 label call 透明版 courtyard 屏幕并处理其返回的
##      ("action", ...) 元组——此处不使用 Function() action，
##      主交互循环完全不介入。结束时丢弃 Call() 返回点（与 teleport
##      同理）并 jump main 回主页。
################################################################################


label courtyard_scene():

    $ norollback()

    hide screen home
    hide screen tool

    play sound s_chimes

    scene black
    show bg mansion inside at top
    with Fade(0.15, 0.3, 0.15)

    show sill happy at right with dissolve

    ## EN: Precompute the status narration (no function calls inside [ ]).
    ## ZH: 预先计算状态叙述文本（[ ] 内不允许函数调用）。
    python:
        _cy_count = len(courtyard_villa.girls)
        _cy_limit = courtyard_villa.room_limit()
        _cy_rent = courtyard_villa.get_daily_rent()
        _cy_diff_name = game.diff.capitalize() if getattr(game, "diff", None) else "?"
        _cy_district_name = getattr(courtyard_current_district(), "name", None) or __("the city")

    sill "Welcome to the villa, Master. We are keeping [_cy_count] of your girls here in [_cy_district_name] — the rooms can house up to [_cy_limit] of them."

    if _cy_count > 0:
        sill "The rent comes to [_cy_rent] gold tonight, on top of their upkeep. [_cy_diff_name] times, Master — every district charges more for its rooms, and the landlord raises his rates as your household grows."
        sill "And do visit them once in a while. Idling day after day dulls a girl's skills, especially in... challenging times."
    else:
        sill "The villa is empty right now, so there is no rent to pay. Should you ever need the extra rooms, you know where to find us."

    ## EN: Final district: pitch the villa expansion deed once per visit until
    ##     it is bought.
    ## ZH: 最终区域：每次来访推销一次扩建地契，直至购得。
    if courtyard_villa.can_buy_expansion():

        sill "Ah — before I forget. Word is the crown is selling land grants here in the King's Hold. With one of these deeds, the villa could be expanded into a proper estate."

        sill "The asking price is a kingly sum — [courtyard_villa.EXPANSION_PRICE] gold, to be precise. I know, I know... but it would lift the room cap entirely. You can review the offer from the facilities panel."

        you "Ten million gold for a bigger courtyard. Sill, remind me to fire whoever came up with that idea."

        sill happy "Noted, Master. Shall I tell them before or after they take your money?"


label courtyard_loop:

    call screen courtyard
    $ _cy_action = _return

    if not _cy_action:
        $ _cy_action = ("close",)

    ## ────────────────────────────────────────────────────────────
    ##  Move the selected girl back to the brothel
    ## ────────────────────────────────────────────────────────────
    if _cy_action[0] == "move_brothel":

        python:
            _cy_ok, _cy_msg = courtyard_villa.move_to_brothel(_cy_action[1])

        $ renpy.say("", _cy_msg)

    ## ────────────────────────────────────────────────────────────
    ##  Train the selected girl (reduced efficiency)
    ## ────────────────────────────────────────────────────────────
    elif _cy_action[0] == "train":

        python:
            _cy_girl = _cy_action[1]
            _cy_name = getattr(_cy_girl, "name", __("the girl"))
            _cy_ok = courtyard_villa.train_girl(_cy_girl, "obedience", 1)

        if _cy_ok:
            sill "[_cy_name] put in a quiet hour of practice at the training ground. Slow and steady, Master."
        else:
            sill "I'm afraid [_cy_name] is in no state to train right now."

    ## ────────────────────────────────────────────────────────────
    ##  Release the selected girl (frees her from your service)
    ## ────────────────────────────────────────────────────────────
    elif _cy_action[0] == "release":

        python:
            _cy_girl = _cy_action[1]
            _cy_name = getattr(_cy_girl, "name", __("the girl"))
            courtyard_villa.remove_girl(_cy_girl)
            _cy_released = True
            try:
                relinquish_girl(_cy_girl)  ## EN: Unequip items & clear roster refs, same cleanup as a sale. ZH: 卸下道具并清理名册引用，与出售时相同。
            except Exception:
                _cy_released = False

        if _cy_released:
            sill "[_cy_name] has been released from your service, Master. She seemed... relieved."
        else:
            sill "[_cy_name] has left the villa, Master."

    ## ────────────────────────────────────────────────────────────
    ##  Upgrade a facility
    ## ────────────────────────────────────────────────────────────
    elif _cy_action[0] == "upgrade":

        python:
            _cy_facility = courtyard_villa.facilities.get(_cy_action[1])
            _cy_ok, _cy_msg = _cy_facility.upgrade(MC) if _cy_facility else (False, __("Unknown facility."))

        if _cy_ok:
            sill "[_cy_msg] The workmen will have it ready by tonight."
        else:
            sill "[_cy_msg]"

    ## ────────────────────────────────────────────────────────────
    ##  Buy the villa expansion deed (final district only)
    ## ────────────────────────────────────────────────────────────
    elif _cy_action[0] == "buy_expansion":

        python:
            _cy_ok, _cy_msg = courtyard_villa.buy_expansion()

        if _cy_ok:
            sill happy "[_cy_msg]"
            you "Ten million gold... I hope the girls appreciate the new wing."
        else:
            sill "[_cy_msg]"

    ## ────────────────────────────────────────────────────────────
    ##  Leave the villa
    ## ────────────────────────────────────────────────────────────
    elif _cy_action[0] == "close":

        jump courtyard_scene_end

    jump courtyard_loop


label courtyard_scene_end:

    if len(courtyard_villa.girls) > 0:
        sill "Have a good evening, Master. The girls will be waiting for your next visit."
    else:
        sill "Goodbye, Master."

    hide sill with dissolve

    scene black with fade

    ## EN: Discard the Call() return point (the same trick label teleport
    ##     uses) so the home loop re-enters cleanly, then jump main.
    ## ZH: 丢弃 Call() 产生的返回点（与 label teleport 相同的手法），
    ##     随后 jump 回主页。
    python:
        for _cy_i in range(renpy.call_stack_depth()):
            renpy.pop_call()

    jump main
