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

    ## EN: Title panel — transparent margins let the scene show around it.
    ## ZH: 标题面板——边缘透明，透出场景。
    frame:
        xalign 0.5
        yalign 0.02
        xpadding 24
        ypadding 8
        background c_ui_dark

        hbox:
            spacing 25
            yalign 0.5

            text __("[session.session_name] — Day [session.date]"):
                size 22
                color "#FFD700"
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
                color "#FFD700"
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
            background c_ui_dark

            vbox:
                spacing 6
                xfill True

                text __("Today's lots"):
                    size 18
                    color "#FFFFFF"
                    bold True
                    xalign 0.5

                text __("Lot %d/%d") % (min(session.current_lot_index + 1, len(session.lots)), len(session.lots)):
                    size 13
                    color "#888888"
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
                                    color "#888888"

                                vbox:
                                    xsize 130
                                    spacing 2
                                    text lot.get_display_name():
                                        size 14
                                        color ({AuctionLot.STATUS_SOLD: "#2ECC71",
                                                AuctionLot.STATUS_UNSOLD: "#E74C3C",
                                                AuctionLot.STATUS_CANCELLED: "#888888"}.get(lot.status, "#FFFFFF"))
                                        bold (i == session.current_lot_index)

                                vbox:
                                    xalign 1.0
                                    spacing 2
                                    text str(lot.current_bid):
                                        size 13
                                        color "#FFD700"
                                        xalign 1.0
                                    text lot.get_status_text():
                                        size 11
                                        xalign 1.0
                                        color ({AuctionLot.STATUS_ACTIVE: "#4ECDC4",
                                                AuctionLot.STATUS_SOLD: "#2ECC71",
                                                AuctionLot.STATUS_UNSOLD: "#E74C3C",
                                                AuctionLot.STATUS_PENDING: "#AAAAAA"}.get(lot.status, "#AAAAAA"))

        ## EN: Right panel — current lot card and bidding paddle.
        ## ZH: 右侧面板——当前拍品卡与出价牌。
        frame:
            xsize 520
            ysize 430
            background c_ui_dark

            if auction_lot is not None:

                vbox:
                    spacing 10
                    xfill True
                    xalign 0.5

                    text auction_lot.get_display_name():
                        size 28
                        color "#FFFFFF"
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
                                    color "#BBBBBB"

                            text __("Seller: [auction_lot.seller]"):
                                size 14
                                color "#888888"

                    null height 5

                    text __("Current bid: {b}[auction_lot.current_bid]{/b} gold"):
                        size 24
                        xalign 0.5
                        color "#FFD700"

                    if auction_lot.current_bidder:
                        text __("Highest bidder: [auction_lot.current_bidder]"):
                            size 16
                            xalign 0.5
                            color ({True: "#4ECDC4", False: "#E74C3C"}.get(auction_lot.current_bidder == auction_player, "#AAAAAA"))

                    hbox:
                        xalign 0.5
                        spacing 20

                        text __("Reserve: [auction_lot.reserve_price]"):
                            size 13
                            color "#888888"

                        text __("Increment: [auction_lot.min_increment]"):
                            size 13
                            color "#888888"

                    null height 10

                    if auction_lot.seller == "player":
                        text __("This is your own lot — bid to stir interest, but if you buy it back yourself you still pay the auction house commission."):
                            size 13
                            color "#FFAAAA"
                            xalign 0.5
                            text_align 0.5

                    if auction_lot.status == AuctionLot.STATUS_ACTIVE:

                        hbox:
                            xalign 0.5
                            spacing 10

                            textbutton __("-"):
                                action SetScreenVariable("bid_amount", max(0, auction_display_bid - auction_lot.min_increment))

                            text __("[auction_display_bid] gold"):
                                size 22
                                yalign 0.5
                                color "#FFFFFF"

                            textbutton __("+"):
                                action SetScreenVariable("bid_amount", auction_display_bid + auction_lot.min_increment)

                        textbutton __("Bid"):
                            xalign 0.5
                            sensitive (auction_display_bid >= auction_min_bid and MC.gold >= auction_display_bid)
                            action Return(("bid", auction_display_bid))

                    else:
                        text auction_lot.get_status_text():
                            size 20
                            xalign 0.5
                            color "#888888"

            else:
                text __("The auction is over."):
                    size 22
                    xalign 0.5
                    yalign 0.5
                    color "#888888"

    ## EN: Bottom action bar.
    ## ZH: 底部操作栏。
    hbox:
        xalign 0.5
        yalign 0.93
        spacing 20

        textbutton __("Pass / gavel this lot"):
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
