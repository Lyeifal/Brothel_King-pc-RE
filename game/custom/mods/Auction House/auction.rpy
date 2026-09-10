################################################################################
##  Auction System — BK Evolution (now part of the "Auction House" mod)
##  EN: Core classes for the auction house (buying/selling girls via bidding).
##      Moved from game/core/systems/auction/auction.rpy into this mod.
##  ZH: 拍卖行核心类（通过竞拍买卖女孩）。
##      从 game/core/systems/auction/auction.rpy 移至本 Mod。
################################################################################

init -1 python:

    class AuctionBid(object):
        """
        EN: A single bid placed on an auction lot.
        ZH: 对拍卖品出的单次出价。
        """

        def __init__(self, bidder_name, amount, is_player=False):
            self.bidder_name = bidder_name  ## EN: Display name of bidder. ZH: 出价者显示名。
            self.amount = amount            ## EN: Bid amount in gold. ZH: 出价金额（金币）。
            self.is_player = is_player      ## EN: True if bid by MC. ZH: 若为 MC 出价则为 True。
            self.timestamp = calendar.day if calendar else 0  ## EN: Day of bid. ZH: 出价日期。

        def __repr__(self):
            return __("<AuctionBid %s: %s gold>") % (self.bidder_name, self.amount)


    class AuctionLot(object):
        """
        EN: A single lot (girl) up for auction.
        ZH: 拍卖会上的一件拍品（女孩）。
        """

        STATUS_PENDING = "pending"      ## EN: Not yet auctioned. ZH: 尚未拍卖。
        STATUS_ACTIVE = "active"        ## EN: Currently being bid on. ZH: 正在竞拍。
        STATUS_SOLD = "sold"            ## EN: Sold to highest bidder. ZH: 已售出给最高出价者。
        STATUS_UNSOLD = "unsold"        ## EN: No bids met reserve. ZH: 未达保留价，流拍。
        STATUS_CANCELLED = "cancelled"  ## EN: Removed from auction. ZH: 已撤拍。

        def __init__(self, girl, seller="player", starting_price=None,
                     reserve_price=None, min_increment=10):
            self.girl = girl
            self.seller = seller            ## EN: 'player' or NPC name. ZH: 'player' 或 NPC 名字。
            self.status = self.STATUS_PENDING

            ## EN: Compute starting price from girl value if not provided.
            ## ZH: 若未提供，根据女孩价值计算起拍价。
            if starting_price is None:
                base = girl.get_price("sell", raw=True) if hasattr(girl, "get_price") else 100
                self.starting_price = max(int(base * 0.8), 50)
            else:
                self.starting_price = starting_price

            self.reserve_price = reserve_price or self.starting_price
            self.min_increment = min_increment  ## EN: Minimum bid increment. ZH: 最小加价幅度。

            self.current_bid = self.starting_price
            self.current_bidder = None      ## EN: Name of highest bidder. ZH: 最高出价者名字。
            self.bids = []                  ## EN: List of AuctionBid. ZH: AuctionBid 列表。
            self.player_bid = 0             ## EN: Highest player bid on this lot. ZH: 玩家对此拍品的最高出价。

        def place_bid(self, bidder_name, amount, is_player=False):
            """
            EN: Place a bid on this lot. Returns True if bid is accepted.
            ZH: 对此拍品出价。若出价被接受则返回 True。
            """
            if self.status != self.STATUS_ACTIVE:
                return False

            if amount < self.current_bid + self.min_increment:
                return False

            bid = AuctionBid(bidder_name, amount, is_player)
            self.bids.append(bid)
            self.current_bid = amount
            self.current_bidder = bidder_name

            if is_player:
                self.player_bid = amount

            return True

        def npc_bid(self, npc_name, enthusiasm=1.0):
            """
            EN: Have an NPC place a bid based on enthusiasm (0.5=low, 2.0=high).
            ZH: 让 NPC 根据热情度出价（0.5=低，2.0=高）。
            """
            if self.status != self.STATUS_ACTIVE:
                return False

            ## EN: NPCs bid up to 1.5x the girl's buy price based on enthusiasm.
            ## ZH: NPC 最高出到女孩买价的 1.5 倍，根据热情度调整。
            max_val = self.girl.get_price("buy", raw=True) * (0.8 + enthusiasm * 0.7)
            max_val = int(max_val)

            if max_val <= self.current_bid + self.min_increment:
                return False

            ## EN: NPC bids between current+increment and their max.
            ## ZH: NPC 在当前价+加价幅度到其最高出价之间随机出价。
            import random
            bid_amount = random.randint(self.current_bid + self.min_increment, max_val)
            return self.place_bid(npc_name, bid_amount, is_player=False)

        def finalize(self):
            """
            EN: Close bidding and determine result.
                Returns (status, winner_name, final_price).
            ZH: 结束竞拍并确定结果。
                返回 (状态, 赢家名字, 最终价格)。
            """
            if self.status != self.STATUS_ACTIVE:
                return self.status, self.current_bidder, self.current_bid

            if self.current_bid >= self.reserve_price and self.current_bidder:
                self.status = self.STATUS_SOLD
            else:
                self.status = self.STATUS_UNSOLD

            return self.status, self.current_bidder, self.current_bid

        def get_status_text(self):
            """EN: Return translated status text.
               ZH: 返回翻译后的状态文字。"""
            return __(self.status.capitalize())


    class AuctionSession(object):
        """
        EN: Manages a single auction event with multiple lots.
        ZH: 管理一场包含多个拍品的拍卖活动。
        """

        PHASE_SETUP = "setup"
        PHASE_BIDDING = "bidding"
        PHASE_RESOLVED = "resolved"

        def __init__(self, lots, session_name="Monthly Auction"):
            self.lots = lots
            self.session_name = session_name
            self.phase = self.PHASE_SETUP
            self.current_lot_index = 0
            self.results = []           ## EN: List of finalized lot results. ZH: 已结拍拍品结果列表。
            self.date = calendar.day if calendar else 0

        @property
        def current_lot(self):
            """EN: Get the lot currently being bid on.
               ZH: 获取当前正在竞拍的拍品。"""
            if 0 <= self.current_lot_index < len(self.lots):
                return self.lots[self.current_lot_index]
            return None

        def start_bidding(self):
            """EN: Open bidding on all lots.
               ZH: 开启所有拍品的竞拍。"""
            self.phase = self.PHASE_BIDDING
            for lot in self.lots:
                lot.status = AuctionLot.STATUS_ACTIVE

        def advance_lot(self):
            """
            EN: Finalize current lot and move to next. Returns next lot or None.
            ZH: 结拍当前拍品并移至下一个。返回下一个拍品或 None。
            """
            if self.current_lot:
                result = self.current_lot.finalize()
                self.results.append(result)
                self.current_lot_index += 1
            return self.current_lot

        def auto_resolve(self):
            """
            EN: Simulate NPC bidding on all lots and finalize everything.
                Used when player skips or for background auction resolution.
            ZH: 模拟所有拍品的 NPC 出价并全部结拍。
                用于玩家跳过或后台拍卖结算。
            """
            import random
            npc_names = [__("Lord Blackwood"), __("Merchant Velira"), __("Countess Sable"),
                         __("The Iron Duke"), __("Madame Zara"), __("Guildmaster Orin")]

            for lot in self.lots:
                lot.status = AuctionLot.STATUS_ACTIVE
                ## EN: 1-3 NPCs bid on each lot with varying enthusiasm.
                ## ZH: 每个拍品有 1-3 个 NPC 出价，热情度各异。
                for _ in range(random.randint(1, 3)):
                    npc = random.choice(npc_names)
                    enthusiasm = random.uniform(0.5, 1.8)
                    lot.npc_bid(npc, enthusiasm)
                result = lot.finalize()
                self.results.append(result)

            self.phase = self.PHASE_RESOLVED

        def player_buy_lot(self, lot_index):
            """
            EN: Player buys a lot instantly at reserve price (no bidding).
                Used for direct purchase of NPC-listed girls.
            ZH: 玩家以保留价直接购买拍品（无需竞拍）。
                用于直接购买 NPC 挂出的女孩。
            """
            if lot_index < 0 or lot_index >= len(self.lots):
                return False
            lot = self.lots[lot_index]
            if lot.status != AuctionLot.STATUS_ACTIVE:
                return False
            if MC.gold < lot.reserve_price:
                return False

            lot.place_bid(__("You"), lot.reserve_price, is_player=True)
            lot.finalize()
            return True

        def player_sell_girl(self, girl, starting_price=None, reserve_price=None):
            """
            EN: Add a girl from MC's roster to the auction session.
            ZH: 将 MC 队伍中的一个女孩加入拍卖会话。
            """
            if girl not in MC.girls:
                return None

            lot = AuctionLot(girl, seller="player", starting_price=starting_price,
                            reserve_price=reserve_price)
            self.lots.append(lot)
            return lot


    class AuctionHouse(object):
        """
        EN: Persistent auction house that tracks history and schedules sessions.
        ZH: 持久化的拍卖行，追踪历史记录并安排拍卖会话。
        """

        def __init__(self):
            self.history = []           ## EN: Past auction results. ZH: 过去的拍卖结果。
            self.next_auction_day = 0   ## EN: Day of next scheduled auction. ZH: 下次预定拍卖日。
            self.frequency = 30         ## EN: Days between auctions. ZH: 拍卖间隔天数。

        def schedule_next(self, from_day=None):
            """EN: Schedule the next auction day.
               ZH: 安排下次拍卖日。"""
            base = from_day if from_day is not None else (calendar.day if calendar else 0)
            self.next_auction_day = base + self.frequency

        def is_due(self):
            """EN: Return True if an auction should happen today.
               ZH: 返回今天是否应举行拍卖。"""
            return calendar and calendar.day >= self.next_auction_day

        def generate_npc_lots(self, count=3):
            """
            EN: Generate random girls from the city as auction lots.
            ZH: 从城中生成随机女孩作为拍卖拍品。
            """
            lots = []
            girls = get_girls(count)
            for g in girls:
                price = g.get_price("buy", raw=True) if hasattr(g, "get_price") else 200
                lot = AuctionLot(g, seller=__("Anonymous Seller"),
                                starting_price=max(int(price * 0.5), 50),
                                reserve_price=int(price * 0.9))
                lots.append(lot)
            return lots

        def record_session(self, session):
            """EN: Store a completed session in history.
               ZH: 将完成的会话存入历史记录。"""
            self.history.append({
                "date": session.date,
                "name": session.session_name,
                "results": session.results,
            })


    ## EN: Global auction house instance.
    ## ZH: 全局拍卖行实例。
    auction_house = AuctionHouse()
