################################################################################
##  Auction Screens — BK Evolution
##  EN: UI for the auction house: lot list, bidding, and results.
##  ZH: 拍卖行 UI：拍品列表、竞拍界面和结果展示。
################################################################################

## EN: Main auction house screen — shows current lots.
## ZH: 拍卖行主屏幕 — 展示当前拍品。
screen auction_house():

    tag menu
    modal True

    default current_session = None
    default selected_lot = None
    default bid_amount = 0

    frame:
        xfill True
        yfill True
        background c_black

        vbox:
            xalign 0.5
            yalign 0.05
            spacing 10

            text __("拍卖行"):
                size 42
                xalign 0.5
                color "#FFD700"
                outlines [(2, "#000", 0, 0)]

            if current_session:
                text "[current_session.session_name] — Day [current_session.date]":
                    size 18
                    xalign 0.5
                    color "#AAAAAA"

        if not current_session:
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 20

                text __("没有活跃的拍卖会话。"):
                    size 24
                    xalign 0.5
                    color "#FF6B6B"

                textbutton __("开始新拍卖"):
                    xalign 0.5
                    action [SetScreenVariable("current_session",
                             AuctionSession(auction_house.generate_npc_lots(4))),
                            SetScreenVariable("selected_lot", None)]

                textbutton __("出售我的一个女孩"):
                    xalign 0.5
                    action Show("auction_sell_girl")
        else:
            hbox:
                xalign 0.5
                yalign 0.55
                spacing 20

                ## EN: Left panel — lot list.
                ## ZH: 左侧面板 — 拍品列表。
                frame:
                    xsize 360
                    ysize 520
                    background c_ui_dark

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            spacing 8
                            xfill True

                            for i, lot in enumerate(current_session.lots):
                                button:
                                    xfill True
                                    ysize 80
                                    background "#333333"
                                    hover_background "#555555"
                                    selected_background "#444466"
                                    selected (selected_lot == lot)

                                    action [SetScreenVariable("selected_lot", lot),
                                            SetScreenVariable("bid_amount", lot.current_bid + lot.min_increment)]

                                    hbox:
                                        spacing 10
                                        xfill True
                                        yalign 0.5

                                        vbox:
                                            spacing 2
                                            xsize 220

                                            text lot.girl.name:
                                                size 18
                                                color "#FFFFFF"
                                                bold True

                                            text "Rank [lot.girl.rank] — [lot.girl.job]":
                                                size 14
                                                color "#BBBBBB"

                                            text "Seller: [lot.seller]":
                                                size 13
                                                color "#888888"

                                        vbox:
                                            xalign 1.0
                                            yalign 0.5
                                            spacing 2

                                            text "[lot.current_bid] gold":
                                                size 16
                                                color "#FFD700"
                                                xalign 1.0

                                            text lot.get_status_text():
                                                size 13
                                                color ({AuctionLot.STATUS_ACTIVE: "#4ECDC4",
                                                        AuctionLot.STATUS_SOLD: "#2ECC71",
                                                        AuctionLot.STATUS_UNSOLD: "#E74C3C",
                                                        AuctionLot.STATUS_PENDING: "#AAAAAA"}.get(lot.status, "#AAAAAA"))
                                                xalign 1.0

                ## EN: Right panel — lot detail & bidding.
                ## ZH: 右侧面板 — 拍品详情与出价。
                frame:
                    xsize 420
                    ysize 520
                    background c_ui_dark

                    if selected_lot:
                        vbox:
                            spacing 12
                            xfill True
                            xalign 0.5
                            yalign 0.1

                            text selected_lot.girl.name:
                                size 28
                                xalign 0.5
                                color "#FFFFFF"
                                bold True

                            hbox:
                                xalign 0.5
                                spacing 15

                                text "Rank [selected_lot.girl.rank]":
                                    size 16
                                    color "#BBBBBB"

                                text "Level [selected_lot.girl.level]":
                                    size 16
                                    color "#BBBBBB"

                            null height 10

                            text __("当前出价: {b}[selected_lot.current_bid]{/b} 金币"):
                                size 20
                                xalign 0.5
                                color "#FFD700"

                            if selected_lot.current_bidder:
                                text __("最高出价者: [selected_lot.current_bidder]"):
                                    size 16
                                    xalign 0.5
                                    color ({True: "#4ECDC4", False: "#E74C3C"}.get(selected_lot.current_bidder == __("你"), "#AAAAAA"))

                            null height 10

                            text __("保留价: [selected_lot.reserve_price] 金币"):
                                size 16
                                xalign 0.5
                                color "#888888"

                            text __("加价幅度: [selected_lot.min_increment] 金币"):
                                size 14
                                xalign 0.5
                                color "#888888"

                            null height 20

                            if selected_lot.status == AuctionLot.STATUS_ACTIVE:
                                hbox:
                                    xalign 0.5
                                    spacing 10

                                    textbutton __("-"):
                                        action SetScreenVariable("bid_amount", max(selected_lot.current_bid + selected_lot.min_increment, bid_amount - selected_lot.min_increment))

                                    text "[bid_amount] gold":
                                        size 20
                                        yalign 0.5
                                        color "#FFFFFF"

                                    textbutton __("+"):
                                        action SetScreenVariable("bid_amount", bid_amount + selected_lot.min_increment)

                                null height 10

                                textbutton __("出价"):
                                    xalign 0.5
                                    sensitive (bid_amount >= selected_lot.current_bid + selected_lot.min_increment and MC.gold >= bid_amount)
                                    action [Function(selected_lot.place_bid, __("You"), bid_amount, True),
                                            SetScreenVariable("bid_amount", bid_amount + selected_lot.min_increment)]

                                if selected_lot.seller != "player":
                                    textbutton __("立即购买 ([selected_lot.reserve_price] 金币)"):
                                        xalign 0.5
                                        sensitive (MC.gold >= selected_lot.reserve_price)
                                        action Function(current_session.player_buy_lot, current_session.lots.index(selected_lot))
                            else:
                                text __("此拍品的竞拍已结束。"):
                                    size 18
                                    xalign 0.5
                                    color "#888888"

                    else:
                        text __("选择一个拍品查看详情并出价。"):
                            size 18
                            xalign 0.5
                            yalign 0.5
                            color "#888888"
                            text_align 0.5

            ## EN: Bottom action bar.
            ## ZH: 底部操作栏。
            hbox:
                xalign 0.5
                yalign 0.95
                spacing 20

                textbutton __("下一个拍品"):
                    sensitive (current_session.current_lot is not None)
                    action Function(current_session.advance_lot)

                textbutton __("自动结拍"):
                    action Function(current_session.auto_resolve)

                textbutton __("关闭"):
                    action [Return(), Hide("auction_house")]


## EN: Screen for selecting a girl from MC's roster to sell.
## ZH: 从 MC 队伍中选择女孩出售的面板。
screen auction_sell_girl():

    modal True

    frame:
        xfill True
        yfill True
        background c_black

        vbox:
            xalign 0.5
            yalign 0.05
            spacing 10

            text __("选择要拍卖的女孩"):
                size 32
                xalign 0.5
                color "#FFD700"

            text __("选择你的一个女孩进行拍卖。"):
                size 16
                xalign 0.5
                color "#AAAAAA"

        frame:
            xalign 0.5
            yalign 0.5
            xsize 700
            ysize 450
            background c_ui_dark

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True

                grid 3 3:
                    spacing 10
                    xalign 0.5
                    yalign 0.5

                    for girl in MC.girls:
                        button:
                            xsize 210
                            ysize 120
                            background "#333333"
                            hover_background "#555555"

                            action [Function(auction_house_session.player_sell_girl, girl),
                                    Hide("auction_sell_girl")]

                            vbox:
                                xalign 0.5
                                yalign 0.5
                                spacing 4

                                text girl.name:
                                    size 18
                                    color "#FFFFFF"
                                    xalign 0.5

                                text "出售价格: [girl.get_price('sell')] 金币":
                                    size 14
                                    color "#FFD700"
                                    xalign 0.5

        textbutton __("取消"):
            xalign 0.5
            yalign 0.95
            action Hide("auction_sell_girl")
