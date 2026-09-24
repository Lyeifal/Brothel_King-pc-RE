################################################################################
##  Auction Screens — BK Evolution ("Auction House" mod v2.1)
##  EN: UI for the scenario-driven auction. The main screen is transparent
##      (no fullscreen black frame) and modal: the slave-market scene with the
##      auctioneer shows through. Buttons return ("action", ...) tuples to the
##      auction_scene label, which owns all game-state changes — no Function()
##      actions are used here, so the main interaction loop is never involved.
##  ZH: 场景化拍卖会的 UI。主屏幕为透明背景（无全屏黑框）且 modal：
##      奴隶市场场景与拍卖师从背景透出。按钮向 auction_scene label 返回
##      ("action", ...) 元组，所有状态变更由 label 处理——此处不使用
##      Function() action，主交互循环完全不介入。
################################################################################


## EN: Main auction screen — current lot, bidding paddle, lot overview.
##     Shown with `call screen` from label auction_scene.
## ZH: 拍卖主屏幕——当前拍品、出价牌、拍品总览。
##     由 auction_scene label 以 `call screen` 方式显示。
screen auction_house(session):

    modal True

    key "mouseup_3" action Return(("leave",))

    ## EN: The python block re-runs on every screen refresh, so the working
    ##     bid lives in a screen variable (default) and the displayed amount
    ##     is derived as max(bid_amount, minimum bid).
    ## ZH: python 块在每次屏幕刷新时都会重跑，因此工作出价值存放于屏幕
    ##     变量（default），显示值取 max(出价值, 最低出价)。
    default bid_amount = 0

    python:
        auction_lot = session.current_lot
        auction_min_bid = 0
        auction_display_bid = 0
        if auction_lot is not None:
            auction_min_bid = auction_lot.current_bid + auction_lot.min_increment
            auction_display_bid = max(bid_amount, auction_min_bid)
        auction_player = auction_player_name()
        auction_committed = getattr(session, "player_committed", 0)
        ## EN: Bidder roster (persists for the whole session) + insight flag.
        ## ZH: 竞买人名单（整场有效）+ 洞察解锁标记。
        if auction_lot is not None and auction_lot.status == AuctionLot.STATUS_ACTIVE:
            session.ensure_bidders(auction_lot)
        auction_bidders = list(getattr(session, "bidders", None) or [])
        auction_insight = False
        try:
            auction_insight = auction_house.has_insight()
        except Exception:
            auction_insight = False
        ## EN: Avatar palette (by roster index). ZH: 头像配色（按名单序号取色）。
        auction_palette = ("#8E44AD", "#2E86C1", "#138D75", "#B9770E", "#A93226")
        ## EN: Girl portrait for the current lot (None if unavailable).
        ## ZH: 当前拍品女孩的立绘（不可用时为 None）。
        auction_girl_pic = None
        if auction_lot is not None and auction_lot.kind == "girl" and auction_lot.girl is not None:
            try:
                auction_girl_pic = auction_lot.girl.get_pic(200, 280)
            except Exception:
                auction_girl_pic = None

    ## EN: Title panel — transparent margins let the scene show around it.
    ## ZH: 标题面板——边缘透明，透出场景。
    frame:
        xalign 0.5
        yalign 0.02
        xpadding 24
        ypadding 8
        background c_ui_light

        hbox:
            spacing 25
            yalign 0.5

            text __("[session.session_name] — Day [session.date]"):
                size 22
                color "#9A6A00"
                bold True
                yalign 0.5

            if session.grand:
                text __("GRAND AUCTION"):
                    size 18
                    color "#FF6B6B"
                    bold True
                    yalign 0.5

            text __("Your gold: [MC.gold]"):
                size 18
                color "#9A6A00"
                yalign 0.5

            text __("Committed: [auction_committed]"):
                size 18
                color "#B03A2E"
                yalign 0.5

    hbox:
        xalign 0.5
        yalign 0.45
        spacing 15

        ## EN: Left panel — today's lots overview.
        ## ZH: 左侧面板——今日拍品总览。
        frame:
            xsize 260
            ysize 430
            background c_ui_light

            vbox:
                spacing 6
                xfill True

                text __("Today's lots"):
                    size 18
                    color "#3B2F20"
                    bold True
                    xalign 0.5

                text __("Lot %d/%d") % (min(session.current_lot_index + 1, len(session.lots)), len(session.lots)):
                    size 13
                    color "#7A6A52"
                    xalign 0.5

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    xfill True
                    ysize 360

                    vbox:
                        spacing 5
                        xfill True

                        for i, lot in enumerate(session.lots):
                            hbox:
                                spacing 6
                                xfill True

                                text str(i + 1):
                                    size 14
                                    color "#7A6A52"

                                vbox:
                                    xsize 130
                                    spacing 2
                                    text lot.get_display_name():
                                        size 14
                                        color ({AuctionLot.STATUS_SOLD: "#1E8449",
                                                AuctionLot.STATUS_UNSOLD: "#B03A2E",
                                                AuctionLot.STATUS_CANCELLED: "#7A6A52"}.get(lot.status, "#3B2F20"))
                                        bold (i == session.current_lot_index)

                                vbox:
                                    xalign 1.0
                                    spacing 2
                                    text str(lot.current_bid):
                                        size 13
                                        color "#9A6A00"
                                        xalign 1.0
                                    text lot.get_status_text():
                                        size 11
                                        xalign 1.0
                                        color ({AuctionLot.STATUS_ACTIVE: "#1F7A72",
                                                AuctionLot.STATUS_SOLD: "#1E8449",
                                                AuctionLot.STATUS_UNSOLD: "#B03A2E",
                                                AuctionLot.STATUS_PENDING: "#8A7A62"}.get(lot.status, "#8A7A62"))

        ## EN: Center panel — the bidders: avatars, standing bids, gold spent,
        ##     lots won, and (with the Insider's Ledger) their hidden limits.
        ## ZH: 中间面板——竞买人：头像、在场出价、已消耗金币、
        ##     已获得拍品，以及（持有《内行账本》时）隐藏阈值。
        frame:
            xsize 400
            ysize 430
            background c_ui_light

            vbox:
                spacing 6
                xfill True

                text __("Bidders"):
                    size 18
                    color "#3B2F20"
                    bold True
                    xalign 0.5

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    xfill True
                    ysize 300

                    vbox:
                        spacing 8
                        xfill True

                        if not auction_bidders:
                            text __("No bidders have taken a seat yet."):
                                size 14
                                color "#7A6A52"
                                xalign 0.5

                        for i, bidder in enumerate(auction_bidders):
                            hbox:
                                spacing 8
                                xfill True

                                ## EN: Avatar — a solid tile with the initial.
                                ## ZH: 头像——纯色块 + 首字母。
                                frame:
                                    xysize (36, 36)
                                    background auction_palette[i % len(auction_palette)]

                                    text bidder.name[:1]:
                                        size 20
                                        color "#3B2F20"
                                        bold True
                                        xalign 0.5
                                        yalign 0.5

                                vbox:
                                    spacing 1
                                    xfill True

                                    hbox:
                                        spacing 8
                                        xfill True

                                        text bidder.name:
                                            size 14
                                            color "#3B2F20"
                                            bold True

                                        if auction_lot is not None and auction_lot.current_bidder == bidder.name:
                                            text __("%d gold") % auction_lot.current_bid:
                                                size 13
                                                color "#1F7A72"
                                                xalign 1.0

                                    hbox:
                                        spacing 10
                                        xfill True

                                        text __("Spent: %d") % bidder.spent:
                                            size 12
                                            color "#9A6A00"

                                        text __("Holding: %d") % bidder.committed:
                                            size 12
                                            color "#B03A2E"

                                    if bidder.won:
                                        text __("Won: %s") % ", ".join(bidder.won):
                                            size 12
                                            color "#1E8449"

                                    ## EN: Hidden thresholds — only with the Ledger.
                                    ## ZH: 隐藏阈值——仅持有《内行账本》时可见。
                                    if auction_insight:
                                        text __("Budget: %d — Max premium: x%.2f — Base chance: %d%%") % (int(bidder.budget_total), bidder.premium_max, int(bidder.base_chance * 100)):
                                            size 12
                                            color "#1F7A72"

                                        text bidder.strategy_name():
                                            size 11
                                            color "#7A6A52"

                null height 4

                textbutton __("Wait for other bids"):
                    xfill True
                    sensitive (auction_lot is not None and auction_lot.status == AuctionLot.STATUS_ACTIVE)
                    action Return(("wait",))

                if not auction_insight:
                    textbutton __("Buy Insider's Ledger (%d gold)") % auction_house.INSIGHT_PRICE:
                        xfill True
                        sensitive (MC.gold >= auction_house.INSIGHT_PRICE)
                        action Return(("buy_insight",))

        ## EN: Right panel — current lot card and bidding paddle.
        ## ZH: 右侧面板——当前拍品卡与出价牌。
        frame:
            xsize 520
            ysize 430
            background c_ui_light

            if auction_lot is not None:

                vbox:
                    spacing 10
                    xfill True
                    xalign 0.5

                    text auction_lot.get_display_name():
                        size 28
                        color "#3B2F20"
                        bold True
                        xalign 0.5

                    hbox:
                        xalign 0.5
                        spacing 15

                        if auction_lot.kind == "item" and auction_lot.item is not None:
                            add auction_lot.item.get_pic(72, 72)

                        vbox:
                            spacing 4
                            yalign 0.5

                            if auction_lot.get_subtitle():
                                text auction_lot.get_subtitle():
                                    size 15
                                    color "#6B5B45"

                            text __("Seller: [auction_lot.seller]"):
                                size 14
                                color "#7A6A52"

                    null height 5

                    ## EN: Girl portrait — hover to peek at her stats.
                    ## ZH: 女孩立绘——鼠标悬浮查看属性。
                    if auction_girl_pic is not None:
                        button:
                            xalign 0.5
                            ysize 280
                            background None
                            padding (0, 0)
                            add auction_girl_pic
                            hovered Show("auction_girl_tip", girl=auction_lot.girl)
                            unhovered Hide("auction_girl_tip")

                    null height 5

                    text __("Current bid: {b}[auction_lot.current_bid]{/b} gold"):
                        size 24
                        xalign 0.5
                        color "#9A6A00"

                    if auction_lot.current_bidder:
                        text __("Highest bidder: [auction_lot.current_bidder]"):
                            size 16
                            xalign 0.5
                            color ({True: "#1F7A72", False: "#B03A2E"}.get(auction_lot.current_bidder == auction_player, "#8A7A62"))

                    hbox:
                        xalign 0.5
                        spacing 20

                        text __("Reserve: [auction_lot.reserve_price]"):
                            size 13
                            color "#7A6A52"

                        text __("Increment: [auction_lot.min_increment]"):
                            size 13
                            color "#7A6A52"

                    null height 10

                    if auction_lot.seller == "player":
                        text __("This is your own lot — you cannot bid on it. If it sells, the proceeds are yours; if not, it comes back to you."):
                            size 13
                            color "#B03A2E"
                            xalign 0.5
                            text_align 0.5

                    if auction_lot.status == AuctionLot.STATUS_ACTIVE and auction_lot.seller != "player":

                        hbox:
                            xalign 0.5
                            spacing 10

                            textbutton __("-"):
                                action SetScreenVariable("bid_amount", max(0, auction_display_bid - auction_lot.min_increment))

                            text __("[auction_display_bid] gold"):
                                size 22
                                yalign 0.5
                                color "#3B2F20"

                            textbutton __("+"):
                                action SetScreenVariable("bid_amount", auction_display_bid + auction_lot.min_increment)

                            textbutton __("+10"):
                                action SetScreenVariable("bid_amount", auction_display_bid + 10 * auction_lot.min_increment)

                            textbutton __("+50"):
                                action SetScreenVariable("bid_amount", auction_display_bid + 50 * auction_lot.min_increment)

                        textbutton __("Bid"):
                            xalign 0.5
                            sensitive (auction_display_bid >= auction_min_bid and (auction_display_bid - auction_lot.player_bid) + auction_committed <= MC.gold)
                            action Return(("bid", auction_display_bid))

                        if (auction_display_bid - auction_lot.player_bid) + auction_committed > MC.gold:
                            text __("Not enough gold — you have [auction_committed] gold committed on other lots."):
                                size 13
                                xalign 0.5
                                color "#B03A2E"

                    else:
                        text auction_lot.get_status_text():
                            size 20
                            xalign 0.5
                            color "#7A6A52"

            else:
                text __("The auction is over."):
                    size 22
                    xalign 0.5
                    yalign 0.5
                    color "#7A6A52"

    ## EN: Bottom action bar.
    ## ZH: 底部操作栏。
    hbox:
        xalign 0.5
        yalign 0.93
        spacing 20

        textbutton (_("Gavel (finalize)") if (auction_lot is not None and auction_lot.warned) else _("Pass (going once)")):
            sensitive (auction_lot is not None and auction_lot.status == AuctionLot.STATUS_ACTIVE)
            action Return(("next",))

        textbutton __("List my own goods"):
            action Return(("submit",))

        textbutton __("Leave the auction"):
            action Return(("leave",))


## EN: Submission screen — list a girl or an item from MC's roster/inventory.
##     A listing fee (int(value x fee_rate)) is charged on selection; goods
##     are held in escrow until the lot settles (sold / returned).
## ZH: 提交拍品屏幕——从 MC 的女孩/背包中选择一件上拍。
##     选中时收取挂牌手续费（int(估值 × 费率)）；商品托管至结拍
##     （售出/退还）。
screen auction_submit(session):

    modal True

    key "mouseup_3" action Return(("cancel",))

    default tab = "girls"

    ## EN: Precompute (goods, value, fee) entries — properties like
    ##     `sensitive` may not follow a python block inside a button.
    ## ZH: 预计算 (商品, 估值, 手续费) 列表——按钮内属性不允许跟在
    ##     python 块之后。
    python:
        auction_girl_entries = []
        for _auction_g in MC.girls:
            try:
                _auction_val = _auction_g.get_price("sell", raw=True) if hasattr(_auction_g, "get_price") else 100
            except Exception:
                _auction_val = 100
            auction_girl_entries.append((_auction_g, int(_auction_val), auction_listing_fee(_auction_val)))

        auction_item_entries = []
        for _auction_it in MC.items:
            if getattr(_auction_it, "equipped", False) or not getattr(_auction_it, "sellable", True):
                continue
            try:
                _auction_gp = getattr(_auction_it, "get_price", None)
                _auction_val = _auction_gp("sell") if callable(_auction_gp) else getattr(_auction_it, "price", 100)
            except Exception:
                _auction_val = 100
            auction_item_entries.append((_auction_it, int(_auction_val), auction_listing_fee(_auction_val)))

    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        ysize 520
        background c_ui_dark

        vbox:
            spacing 10
            xfill True

            text __("List your own goods"):
                size 26
                xalign 0.5
                color "#FFD700"
                bold True

            text __("A listing fee is charged up front and scales with game difficulty. If the lot sells, the proceeds are yours; if not, the goods come back to you."):
                size 13
                color "#AAAAAA"
                xalign 0.5
                text_align 0.5

            hbox:
                xalign 0.5
                spacing 15

                textbutton __("Girls"):
                    action SetScreenVariable("tab", "girls")
                    selected (tab == "girls")

                textbutton __("Items"):
                    action SetScreenVariable("tab", "items")
                    selected (tab == "items")

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xsize 700
                ysize 320

                vbox:
                    spacing 8
                    xfill True

                    if tab == "girls":

                        if not MC.girls:
                            text __("You have no girls to list."):
                                size 16
                                color "#888888"
                                xalign 0.5

                        for girl, auction_val, auction_fee_amt in auction_girl_entries:
                            button:
                                xfill True
                                ysize 56
                                background "#333333"
                                hover_background "#555555"

                                sensitive (MC.gold >= auction_fee_amt)
                                action Return(("girl", girl))

                                hbox:
                                    spacing 15
                                    xfill True
                                    yalign 0.5

                                    text girl.name:
                                        size 18
                                        color "#FFFFFF"
                                        xsize 300
                                        yalign 0.5

                                    text __("Value: %d — Fee: %d") % (auction_val, auction_fee_amt):
                                        size 15
                                        color "#FFD700"
                                        xalign 1.0
                                        yalign 0.5

                    else:

                        if not auction_item_entries:
                            text __("Nothing in your inventory can be listed."):
                                size 16
                                color "#888888"
                                xalign 0.5

                        for item, auction_val, auction_fee_amt in auction_item_entries:
                            button:
                                xfill True
                                ysize 56
                                background "#333333"
                                hover_background "#555555"

                                sensitive (MC.gold >= auction_fee_amt)
                                action Return(("item", item))

                                hbox:
                                    spacing 15
                                    xfill True
                                    yalign 0.5

                                    text item.name:
                                        size 18
                                        color "#FFFFFF"
                                        xsize 300
                                        yalign 0.5

                                    text __("Value: %d — Fee: %d") % (auction_val, auction_fee_amt):
                                        size 15
                                        color "#FFD700"
                                        xalign 1.0
                                        yalign 0.5

            textbutton __("Cancel"):
                xalign 0.5
                action Return(("cancel",))


## EN: Hover tooltip for a lot girl's portrait in the auction screen —
##     name, rank and key stats. Shown/hidden by the portrait button.
## ZH: 拍卖屏拍品女孩立绘的悬浮提示——名字、阶级与关键属性。
##     由立绘按钮的 hovered/unhovered 控制显示。
screen auction_girl_tip(girl):

    zorder 20

    frame:
        pos (920, 120)
        xpadding 14
        ypadding 10
        background "#000000CC"

        vbox:
            spacing 3

            text "[girl.name]":
                size 18
                color "#FFD700"
                bold True

            text __("Rank [girl.rank] — Level [girl.level]"):
                size 14
                color "#FFFFFF"

            null height 4

            text __("Charm: [girl.char]"):
                size 13
                color "#BBBBBB"

            text __("Beauty: [girl.beauty]"):
                size 13
                color "#BBBBBB"

            text __("Body: [girl.body]"):
                size 13
                color "#BBBBBB"

            text __("Refinement: [girl.refinement]"):
                size 13
                color "#BBBBBB"

            text __("Sensitivity: [girl.sensitivity]"):
                size 13
                color "#BBBBBB"

            text __("Libido: [girl.libido]"):
                size 13
                color "#BBBBBB"

            text __("Constitution: [girl.constitution]"):
                size 13
                color "#BBBBBB"

            text __("Obedience: [girl.obedience]"):
                size 13
                color "#BBBBBB"
