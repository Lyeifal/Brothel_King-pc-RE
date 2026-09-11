################################################################################
##  Auction Scene — BK Evolution ("Auction House" mod v2.1)
##  EN: Scenario-driven auction: a proper scene (slave market backdrop + Gio
##      as the auctioneer), label-driven bidding loop that calls the
##      transparent auction_house screen, dice-based NPC counter-bidding with
##      narration, listing fees and escrow for player submissions.
##      The right-menu button calls label auction_scene via Call(); the label
##      discards the Call return point (same trick as teleport) and jumps back
##      to main when done.
##  ZH: 场景化拍卖会：真实场景（奴隶市场背景 + Gio 担任拍卖师）、
##      label 驱动的竞拍主循环 call 透明版 auction_house 屏幕、
##      骰子判定的 NPC 反价并伴随过程叙述、玩家商品托管与手续费。
##      右侧菜单按钮经 Call() 进入 label auction_scene；label 结束前
##      丢弃 Call 返回点（与 teleport 同理）并 jump main 回到主页。
################################################################################


label auction_scene():

    $ norollback()

    ## EN: Fallback guard — the right-menu button is already greyed out on
    ##     non-auction days; this only fires if the label is reached anyway.
    ## ZH: 兜底检查——右侧菜单按钮在非拍卖日已置灰；
    ##     仅当 label 被以其他方式进入时才会走到这里。
    if not auction_house.can_hold_auction():
        "There is no auction today. The auction house holds sales on the 1st, 8th, 15th and 22nd of every month."
        return

    hide screen home
    hide screen tool

    $ auction_grand = auction_house.is_grand_today()
    $ auction_session = auction_house.build_session(grand=auction_grand)

    if not auction_session.lots:
        "The auction house has nothing on the block today. Come back next week."
        return

    play sound s_chimes

    scene black
    show bg slave market at top
    with Fade(0.15, 0.3, 0.15)

    show gio at right with dissolve

    if auction_grand:
        gio "Welcome, welcome! The GRAND auction only happens once a month — finest girls and rarest treasures in all of Zan! Please, take a seat, the bidding is about to start."
    else:
        gio "Ah, my favorite customer! Welcome to the weekly auction — girls, trinkets, everything must go. Bid, or list your own goods for a small fee."

    ## EN: Book the session right away: pushes the schedule a week ahead and
    ##     stamps the month (so the next session this month is a regular one).
    ## ZH: 立即登记本场拍卖会：日程顺延一周并记录月份
    ##     （本月后续场次即为普通拍卖）。
    $ auction_house.hold_session()


label auction_bidding_loop:

    if auction_session.is_finished():
        jump auction_scene_end

    call screen auction_house(auction_session)
    $ auction_action = _return

    if not auction_action:
        $ auction_action = ("leave",)

    ## ────────────────────────────────────────────────────────────
    ##  Player bid on the current lot
    ## ────────────────────────────────────────────────────────────
    if auction_action[0] == "bid":

        python:
            auction_ok, auction_events = auction_session.player_bid_current(auction_action[1])

        python:
            for _auction_ev in auction_events:
                renpy.say("", _auction_ev)

        ## EN: No NPC countered the player's bid — the gavel falls at once.
        ## ZH: 没有 NPC 反价——立即落锤。
        if auction_ok and auction_session.current_lot is not None:
            $ auction_lot = auction_session.current_lot
            if auction_lot.status == AuctionLot.STATUS_ACTIVE and auction_lot.current_bidder == auction_player_name():
                $ auction_tmp_name = auction_lot.get_display_name()
                gio "Going once... going twice... SOLD! [auction_tmp_name] goes to you. Always a pleasure doing business."
                python:
                    auction_events = auction_session.settle_current_lot()
                python:
                    for _auction_ev in auction_events:
                        renpy.say("", _auction_ev)

    ## ────────────────────────────────────────────────────────────
    ##  Pass / gavel the current lot
    ## ────────────────────────────────────────────────────────────
    elif auction_action[0] == "next":

        python:
            auction_next_lot, auction_events = auction_session.advance_lot()
            auction_events = list(auction_events)
            if auction_next_lot is not None:
                auction_events.append(__("Next lot: %s.") % auction_next_lot.get_display_name())

        python:
            for _auction_ev in auction_events:
                renpy.say("", _auction_ev)

    ## ────────────────────────────────────────────────────────────
    ##  Submit own goods (girls / items) with a listing fee
    ## ────────────────────────────────────────────────────────────
    elif auction_action[0] == "submit":

        call screen auction_submit(auction_session)
        $ auction_sub = _return

        if auction_sub:
            if auction_sub[0] == "girl":
                python:
                    auction_lot, auction_fee, auction_err = auction_house.submit_girl(auction_sub[1], auction_session)
            elif auction_sub[0] == "item":
                python:
                    auction_lot, auction_fee, auction_err = auction_house.submit_item(auction_sub[1], auction_session)
            else:
                $ auction_err = None

            if auction_err:
                $ renpy.say("", auction_err)
            else:
                $ auction_tmp_name = auction_lot.get_display_name()
                gio "[auction_tmp_name], listed! The fee's non-refundable, but the proceeds are all yours if it sells."
                $ renpy.say("", __("If the lot goes unsold, your goods come straight back to you."))

    ## ────────────────────────────────────────────────────────────
    ##  Leave early — remaining lots are settled without the player
    ## ────────────────────────────────────────────────────────────
    elif auction_action[0] == "leave":

        $ renpy.say("", __("You slip out before the gavel falls. The remaining lots are settled without you."))

        python:
            auction_events = []
            auction_session.wrap_up(auction_events)
            for _auction_ev in auction_events:
                renpy.say("", _auction_ev)

        jump auction_scene_end

    jump auction_bidding_loop


label auction_scene_end:

    hide gio with dissolve

    python:
        auction_house.record_session(auction_session)

    if auction_grand:
        gio "That's a wrap for the grand auction! Same time next month — bring more gold, heh heh heh."
    else:
        gio "That's all for this week! The next grand auction is on the first sale of the month — don't miss it."

    scene black with fade

    ## EN: Discard the Call() return point (the same trick label teleport
    ##     uses) so the home loop re-enters cleanly, then jump home.
    ## ZH: 丢弃 Call() 产生的返回点（与 label teleport 相同的手法），
    ##     随后 jump 回主页。
    python:
        for _auction_i in range(renpy.call_stack_depth()):
            renpy.pop_call()

    jump main
