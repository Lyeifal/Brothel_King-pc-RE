################################################################################
##  Auction System — BK Evolution (now part of the "Auction House" mod)
##  EN: Core classes for the auction house. v2.1: scenario-driven sessions —
##      weekly schedule with a monthly grand auction, item lots in addition to
##      girls, player submissions with escrow, difficulty-scaled listing fees,
##      and dice-based NPC counter-bidding.
##      Moved from game/core/systems/auction/auction.rpy into this mod.
##  ZH: 拍卖行核心类。v2.1：场景化拍卖会——每周举行、每月首场为大拍卖、
##      拍品除女孩外加入道具、玩家可托管提交商品、手续费随难度缩放、
##      NPC 竞买人使用骰子判定反价。
##      从 game/core/systems/auction/auction.rpy 移至本 Mod。
################################################################################

init -1 python:

    ## ============================================================
    ##  Module helpers
    ## ============================================================

    def auction_bidder_name_pool():
        """EN: Virtual NPC bidders reuse existing character names.
               ZH: 虚拟 NPC 竞买人复用现有角色名。"""
        return [__("Lord Blackwood"), __("Merchant Velira"), __("Countess Sable"),
                __("The Iron Duke"), __("Madame Zara"), __("Guildmaster Orin")]


    ## EN: Numeric mapping of the game's difficulty setting for the fee
    ##     formula. game.diff is one of diff_list ("very easy", "easy",
    ##     "normal", "hard", "insane") — no numeric 1-5 difficulty exists in
    ##     this codebase, so map the string to 1-5 (index + 1). Unknown or
    ##     custom values fall back to 3 (normal).
    ## ZH: 手续费公式所需的游戏难度数值映射。本体难度为字符串
    ##     （diff_list："very easy"/"easy"/"normal"/"hard"/"insane"），
    ##     代码库中没有 1-5 的数值难度，这里按下标 +1 映射为 1-5；
    ##     未知或自定义值回退为 3（normal）。
    auction_difficulty_levels = ("very easy", "easy", "normal", "hard", "insane")

    def auction_difficulty_value():
        try:
            return auction_difficulty_levels.index(game.diff) + 1
        except Exception:
            return 3


    def auction_fee_rate():
        """
        EN: Auction house fee rate (listing fee and self-purchase commission).
            Formula (agreed design, see README.txt):
                fee_rate = min(0.30, 0.08 + 0.015 × difficulty)
            With difficulty mapped to 1-5 this yields:
                very easy 9.5% / easy 11% / normal 12.5% / hard 14% / insane 15.5%.
        ZH: 拍卖行费率（挂牌手续费与自购佣金共用）。
            公式（既定设计，见 README.txt）：
                fee_rate = min(0.30, 0.08 + 0.015 × 难度)
            难度映射为 1-5 后：
                非常简单 9.5% / 简单 11% / 普通 12.5% / 困难 14% / 疯狂 15.5%。
        """
        return min(0.30, 0.08 + 0.015 * auction_difficulty_value())


    def auction_listing_fee(estimated_value):
        """EN: Listing fee charged when goods are submitted.
               ZH: 提交商品时收取的挂牌手续费。"""
        try:
            return max(1, int(estimated_value * auction_fee_rate()))
        except Exception:
            return 1


    ## EN: Player paddle name used in bids (matches existing translations).
    ## ZH: 玩家出价时使用的名牌（与现有翻译一致）。
    def auction_player_name():
        return __("You")


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
        EN: A single lot up for auction — a girl or an item.
        ZH: 拍卖会上的一件拍品——女孩或道具。
        """

        STATUS_PENDING = "pending"      ## EN: Not yet auctioned. ZH: 尚未拍卖。
        STATUS_ACTIVE = "active"        ## EN: Currently being bid on. ZH: 正在竞拍。
        STATUS_SOLD = "sold"            ## EN: Sold to highest bidder. ZH: 已售出给最高出价者。
        STATUS_UNSOLD = "unsold"        ## EN: No bids met reserve. ZH: 未达保留价，流拍。
        STATUS_CANCELLED = "cancelled"  ## EN: Removed from auction. ZH: 已撤拍。

        ## EN: Save-compatibility defaults. Old pickles (Ren'Py restores
        ##     instances without running __init__) lack fields added in v2.1;
        ##     __getattr__ below supplies these values.
        ## ZH: 存档兼容默认值。旧存档实例（Ren'Py 恢复实例时不运行
        ##     __init__）缺少 v2.1 新增字段，由 __getattr__ 兜底。
        FIELD_DEFAULTS = {
            "kind": "girl",             ## EN: "girl" or "item". ZH: "girl" 或 "item"。
            "item": None,               ## EN: ItemInstance for item lots. ZH: 道具拍品的 ItemInstance。
            "estimated_value": None,    ## EN: Appraisal in gold. ZH: 估值（金币）。
            "warned": False,            ## EN: "Going once" has been called. ZH: 已喊过"第一次"。
        }

        def __init__(self, girl=None, seller="player", starting_price=None,
                     reserve_price=None, min_increment=None, kind="girl",
                     item=None, estimated_value=None):
            self.girl = girl
            self.item = item
            self.kind = kind
            self.seller = seller            ## EN: 'player' or NPC name. ZH: 'player' 或 NPC 名字。
            self.status = self.STATUS_PENDING

            ## EN: Appraisal — explicit value, else derived from girl/item.
            ## ZH: 估值——优先显式传入，否则从女孩/道具推导。
            if estimated_value is not None:
                self.estimated_value = int(estimated_value)
            else:
                self.estimated_value = self.get_base_value("sell")

            ## EN: Starting price = 90% of the shop price (design rule).
            ## ZH: 起拍价 = 商店价的 90%（设计规则）。
            if starting_price is None:
                self.starting_price = max(int(self.estimated_value * 0.9), 1)
            else:
                self.starting_price = starting_price

            self.reserve_price = reserve_price or self.starting_price

            ## EN: Minimum increment = 5% of the base value, rounded up
            ##     (design rule; previously a flat 5% with a floor of 10).
            ## ZH: 最低加价 = 原价的 5% 向上取整
            ##     （设计规则；原为固定 5%、下限 10）。
            if min_increment is None:
                import math as _math
                self.min_increment = max(1, int(_math.ceil(self.estimated_value * 0.05)))
            else:
                self.min_increment = min_increment

            self.current_bid = self.starting_price
            self.current_bidder = None      ## EN: Name of highest bidder. ZH: 最高出价者名字。
            self.bids = []                  ## EN: List of AuctionBid. ZH: AuctionBid 列表。
            self.player_bid = 0             ## EN: Highest player bid on this lot. ZH: 玩家对此拍品的最高出价。
            self.warned = False             ## EN: "Going once" called — the next pass gavels. ZH: 已喊"第一次"——再次 pass 即落锤。

        def __getattr__(self, name):
            ## EN: Old-save fallback (see FIELD_DEFAULTS). object.__getattribute__
            ##     avoids any recursion while the class is being restored.
            ## ZH: 旧存档兜底（见 FIELD_DEFAULTS）。恢复期间用
            ##     object.__getattribute__ 避免递归。
            defaults = object.__getattribute__(self, "__class__").FIELD_DEFAULTS
            if name in defaults:
                return defaults[name]
            raise AttributeError(name)

        def get_base_value(self, operation="sell"):
            """
            EN: Appraise the lot in gold. Girls use their price; items use
                get_price()/price. Defensive: the items system is being
                reworked in parallel, so every attribute access is guarded.
            ZH: 对拍品进行金币估值。女孩用身价；道具用 get_price()/price。
                防御式编码：道具系统正在并行改动，所有属性访问均有兜底。
            """
            if self.kind == "girl" and self.girl is not None and hasattr(self.girl, "get_price"):
                try:
                    return int(self.girl.get_price(operation, raw=True))
                except Exception:
                    pass
            if self.item is not None:
                gp = getattr(self.item, "get_price", None)
                if callable(gp):
                    try:
                        return int(gp(operation))
                    except Exception:
                        pass
                try:
                    return int(getattr(self.item, "price", 0))
                except Exception:
                    pass
            if self.estimated_value:
                return int(self.estimated_value)
            return 100

        def get_display_name(self):
            """EN: Lot name for UI and narration.
                   ZH: UI 与叙述用拍品名。"""
            if self.kind == "item" and self.item is not None:
                return getattr(self.item, "name", __("Mysterious item"))
            if self.girl is not None:
                return getattr(self.girl, "name", __("Unknown girl"))
            return __("Mysterious lot")

        def get_subtitle(self):
            """EN: Secondary line for the lot card (rank/job or type/rarity).
                   ZH: 拍品卡第二行（女孩为排名/职业，道具为类型/稀有度）。"""
            if self.kind == "item" and self.item is not None:
                parts = []
                it_type = getattr(self.item, "type", None)
                if it_type is not None and getattr(it_type, "name", None):
                    parts.append(__(it_type.name))
                rarity = getattr(self.item, "rarity", None)
                if rarity is not None:
                    parts.append(__("Rarity: %s") % rarity)
                charges = getattr(self.item, "charges", None)
                if charges:
                    parts.append(__("%d charges") % charges)
                return " — ".join(parts)
            girl = self.girl
            if girl is not None:
                rank = getattr(girl, "rank", "?")
                level = getattr(girl, "level", "?")
                job = getattr(girl, "job", None)
                if job:
                    return __("Rank %s — Level %s — %s") % (rank, level, __(str(job).capitalize()))
                return __("Rank %s — Level %s") % (rank, level)
            return ""

        def is_ownable_by_player(self):
            """EN: False when the player already owns the goods (own lot).
                   ZH: 玩家是否可购得此拍品（自己的拍品为 False）。"""
            return self.seller != "player"

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

            ## EN: NPCs bid up to ~1.5x the appraisal based on enthusiasm.
            ## ZH: NPC 最高出到估值约 1.5 倍，根据热情度调整。
            max_val = self.get_base_value("buy") * (0.8 + enthusiasm * 0.7)
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


    class AuctionBidder(object):
        """
        EN: A virtual NPC bidder with a personality strategy, a total-auction
            spending cap, a per-lot premium threshold, and a participation
            probability that decays as the price climbs above the goods'
            base (shop) value.
        ZH: 虚拟 NPC 竞买人：带有性格策略、全场总花费阈值、单件溢价
            阈值，以及随价格超出原价而衰减的参与概率。
        """

        STRAT_PERSISTENT = "persistent"  ## EN: Raises once on every lot. ZH: 每个拍品固定抬一次价。
        STRAT_FINALE = "finale"          ## EN: Only joins the closing lots. ZH: 只参与压轴拍品。
        STRAT_COLLECTOR = "collector"    ## EN: Buys at most N lots per auction. ZH: 每场最多拍下 N 件。
        STRAT_STUBBORN = "stubborn"      ## EN: Ignores the premium cap once committed to a lot. ZH: 认定某件后无视溢价阈值。

        STRATEGY_NAMES = None  ## EN: Filled below (needs __()). ZH: 在下方填充（需要 __()）。

        def __init__(self, name, budget_total, premium_max, base_chance,
                     decay_per_step, strategy, strategy_param=None):
            self.name = name
            self.budget_total = int(budget_total)       ## EN: Max total gold this auction (both thresholds hidden without the ledger). ZH: 本场总花费阈值（无手册时不可见）。
            self.premium_max = float(premium_max)       ## EN: Max price as a multiple of base value. ZH: 单件溢价阈值（原价倍数）。
            self.base_chance = float(base_chance)       ## EN: Base participation probability (0-1). ZH: 基础参与概率。
            self.decay_per_step = float(decay_per_step) ## EN: Willingness lost per +5% over base value. ZH: 每超原价 5% 降低的意愿。
            self.strategy = strategy
            self.strategy_param = strategy_param        ## EN: e.g. collector's lot cap. ZH: 如收藏派的件数上限。

            self.committed = 0    ## EN: Gold tied in standing top bids. ZH: 在场最高出价占用的金币。
            self.spent = 0        ## EN: Gold actually paid for won lots. ZH: 已实际支付的中拍金额。
            self.won = []         ## EN: Display names of lots won. ZH: 已拍得的拍品名。
            self._bid_lot_ids = []    ## EN: Session lot indexes bid on (stubborn trigger). ZH: 出过价的拍品序号（执拗派触发）。
            self._raised_lot_ids = [] ## EN: Lots already raised once (persistent strategy). ZH: 已抬过价的拍品（稳健派）。

        def strategy_name(self):
            """EN: Translated strategy label for tooltips. ZH: 策略译名（悬浮提示用）。"""
            names = AuctionBidder.STRATEGY_NAMES or {}
            return names.get(self.strategy, __(self.strategy.capitalize()))

        def __repr__(self):
            return __("<AuctionBidder %s: budget %s, premium x%s>") % (self.name, self.budget_total, self.premium_max)

    AuctionBidder.STRATEGY_NAMES = {
        AuctionBidder.STRAT_PERSISTENT: __("Steady hand"),
        AuctionBidder.STRAT_FINALE: __("Latecomer"),
        AuctionBidder.STRAT_COLLECTOR: __("Collector"),
        AuctionBidder.STRAT_STUBBORN: __("Obsessive"),
    }


    class AuctionSession(object):
        """
        EN: Manages a single auction event with multiple lots.
        ZH: 管理一场包含多个拍品的拍卖活动。
        """

        PHASE_SETUP = "setup"
        PHASE_BIDDING = "bidding"
        PHASE_RESOLVED = "resolved"

        ## EN: Save-compatibility defaults (see AuctionLot.FIELD_DEFAULTS).
        ## ZH: 存档兼容默认值（见 AuctionLot.FIELD_DEFAULTS）。
        FIELD_DEFAULTS = {
            "bidders": None,           ## EN: Active AuctionBidder list. ZH: 当前竞买人列表。
            "grand": False,            ## EN: True for a grand auction. ZH: 大拍卖为 True。
            "player_committed": 0,     ## EN: Gold reserved by the player's standing bids across lots. ZH: 玩家所有在场最高出价占用的金币。
        }

        def __init__(self, lots, session_name="Monthly Auction", grand=False):
            self.lots = lots
            self.session_name = session_name
            self.phase = self.PHASE_SETUP
            self.current_lot_index = 0
            self.results = []           ## EN: List of finalized lot results. ZH: 已结拍拍品结果列表。
            self.date = calendar.day if calendar else 0
            self.bidders = None
            self.grand = grand
            self.player_committed = 0   ## EN: Reserved gold so bids on several lots can't overdraw MC. ZH: 预留金币，防止多拍品出价透支。

        def __getattr__(self, name):
            defaults = object.__getattribute__(self, "__class__").FIELD_DEFAULTS
            if name in defaults:
                return defaults[name]
            raise AttributeError(name)

        @property
        def current_lot(self):
            """EN: Get the lot currently being bid on.
               ZH: 获取当前正在竞拍的拍品。"""
            if 0 <= self.current_lot_index < len(self.lots):
                return self.lots[self.current_lot_index]
            return None

        def is_finished(self):
            """EN: True when every lot has been settled.
                   ZH: 所有拍品均已结拍时返回 True。"""
            return self.current_lot is None

        def start_bidding(self):
            """EN: Open bidding on all lots.
               ZH: 开启所有拍品的竞拍。"""
            self.phase = self.PHASE_BIDDING
            for lot in self.lots:
                lot.status = AuctionLot.STATUS_ACTIVE

        ## ============================================================
        ##  NPC bidders (strategy-driven counter-bidding)
        ## ============================================================

        def ensure_bidders(self, lot):
            """
            EN: Roll up 3-5 virtual bidders with distinct personalities.
                Each gets: a total-session budget (2.5-5x the lot's base
                value, +30% at grand auctions), a per-lot premium threshold
                (1.2-2.0x base value), a base participation chance (20-70%),
                a per-step willingness decay (3-10 points per +5% over base),
                and a strategy — the four strategies are dealt round-robin
                so every session shows a mix.
            ZH: 随机生成 3-5 名性格各异的虚拟竞买人。每人获得：
                全场总预算（拍品原价 2.5~5 倍，大拍卖 +30%）、
                单件溢价阈值（原价 1.2~2.0 倍）、基础参与概率（20%~70%）、
                每超原价 5% 的意愿衰减（3~10 个百分点），以及一种策略——
                四种策略轮转发放，保证每场都有搭配。
            """
            if self.bidders:
                return
            value = max(1, lot.get_base_value("buy"))
            names = list(auction_bidder_name_pool())
            renpy.random.shuffle(names)
            count = renpy.random.randint(3, 5)
            grand = bool(self.grand)
            strategies = [AuctionBidder.STRAT_PERSISTENT, AuctionBidder.STRAT_FINALE,
                          AuctionBidder.STRAT_COLLECTOR, AuctionBidder.STRAT_STUBBORN]
            self.bidders = []
            for i, name in enumerate(names[:count]):
                budget_total = value * renpy.random.uniform(2.5, 5.0)
                if grand:
                    budget_total *= 1.3
                strategy = strategies[i % len(strategies)]
                param = 2 if strategy == AuctionBidder.STRAT_COLLECTOR else None
                self.bidders.append(AuctionBidder(
                    name,
                    budget_total=budget_total,
                    premium_max=renpy.random.uniform(1.2, 2.0),
                    base_chance=renpy.random.uniform(0.2, 0.7),
                    decay_per_step=renpy.random.uniform(0.03, 0.10),
                    strategy=strategy,
                    strategy_param=param,
                ))

        def _lot_id(self, lot):
            """EN: Stable per-session index of a lot (bid tracking). ZH: 拍品在本场中的稳定序号（出价记录用）。"""
            try:
                return self.lots.index(lot)
            except ValueError:
                return -1

        def _willingness(self, bidder, lot):
            """
            EN: Participation probability: base_chance minus decay_per_step
                for every +5% of base value the current price exceeds, minus
                a flat 10 points if this round saw a jump raise (more than
                min increment + 3% of base value). Clamped to 0-95%.
            ZH: 参与概率 = 基础概率 - 每超原价 5% 的衰减 -
                （本轮出现跳价时）10 个百分点。钳制在 0~95%。
            """
            base = max(1, lot.get_base_value("buy"))
            over = max(0, lot.current_bid - base)
            steps = int(over / (base * 0.05))
            p = bidder.base_chance - bidder.decay_per_step * steps
            if getattr(self, "_round_big_raise", False):
                p -= 0.10
            return max(0.0, min(0.95, p))

        def _npc_may_bid(self, bidder, lot):
            """
            EN: Hard gates (no probability involved): total budget with the
                standing commitment, premium threshold (ignored by a stubborn
                bidder committed to this lot), strategy-specific rules.
            ZH: 硬性门槛（与概率无关）：含在场占用的总预算、溢价阈值
                （执拗派认定后忽略）、策略特定规则。
            """
            if bidder.committed + lot.current_bid + lot.min_increment > bidder.budget_total:
                return False

            base = max(1, lot.get_base_value("buy"))
            lot_id = self._lot_id(lot)
            stubborn_committed = (bidder.strategy == AuctionBidder.STRAT_STUBBORN
                                  and lot_id in bidder._bid_lot_ids)
            if not stubborn_committed and lot.current_bid + lot.min_increment > base * bidder.premium_max:
                return False

            if bidder.strategy == AuctionBidder.STRAT_FINALE:
                ## EN: Only the last two lots draw their interest.
                ## ZH: 只对最后两件拍品感兴趣。
                if self.current_lot_index < len(self.lots) - 2:
                    return False

            if bidder.strategy == AuctionBidder.STRAT_COLLECTOR:
                max_lots = bidder.strategy_param or 2
                if len(bidder.won) >= max_lots:
                    return False

            return True

        def _apply_npc_raise(self, bidder, lot, events):
            """
            EN: Place one raise for a bidder: usually the minimum increment,
                sometimes a jump raise (min + 3%-9% of base value) that
                cools the whole room. Updates commitments and strategy
                trackers. Returns the raise amount or None.
            ZH: 为一名竞买人执行一次抬价：通常按最低加价，偶尔跳价
                （最低加价 + 原价的 3%~9%）使全场降温。同步更新占用与
                策略记录。返回抬价金额或 None。
            """
            base = max(1, lot.get_base_value("buy"))
            previous_top = lot.current_bidder
            previous_amount = lot.current_bid
            amount = lot.current_bid + lot.min_increment

            ## EN: ~25% of raises are jump bids that chill the room.
            ## ZH: 约 25% 的抬价为跳价，使全场降温。
            if renpy.random.random() < 0.25:
                amount = lot.current_bid + lot.min_increment + int(base * 0.03) * renpy.random.randint(1, 3)
                self._round_big_raise = True

            ## EN: Premium cap (stubborn bidders committed to this lot skip it).
            ## ZH: 溢价阈值（执拗派已认定此拍品则跳过）。
            lot_id = self._lot_id(lot)
            if not (bidder.strategy == AuctionBidder.STRAT_STUBBORN and lot_id in bidder._bid_lot_ids):
                amount = min(amount, int(base * bidder.premium_max))

            ## EN: Hard budget cap on the raise itself.
            ## ZH: 抬价金额本身的预算硬上限。
            amount = min(amount, bidder.budget_total - bidder.committed)
            if amount < lot.current_bid + lot.min_increment:
                return None

            if not lot.place_bid(bidder.name, amount):
                return None

            ## EN: Transfer the standing commitment from the outbid NPC
            ##     (previous_amount = the bid they are being relieved of).
            ## ZH: 将被反价 NPC 的在场占用转移：previous_amount 是其被
            ##     顶掉的旧出价，从占用中扣除。
            if previous_top and previous_top != bidder.name:
                prev = self._bidder_by_name(previous_top)
                if prev is not None:
                    prev.committed = max(0, prev.committed - previous_amount)
            if previous_top == bidder.name:
                bidder.committed += amount - previous_amount  ## EN: raising own bid: only the delta. ZH: 抬自己的价：只计差额。
            else:
                bidder.committed += amount

            bidder._bid_lot_ids.append(lot_id)
            if bidder.strategy == AuctionBidder.STRAT_PERSISTENT and lot_id not in bidder._raised_lot_ids:
                bidder._raised_lot_ids.append(lot_id)

            events.append(__("%s raises to %d gold.") % (bidder.name, amount))
            return amount

        def _bidder_by_name(self, name):
            """EN: Find a live bidder by display name. ZH: 按显示名查找在场竞买人。"""
            if not self.bidders:
                return None
            for b in self.bidders:
                if b.name == name:
                    return b
            return None

        def _npc_counter_round(self, lot, events, big_raise=False):
            """
            EN: One bidding round: each willing bidder rolls against their
                (decaying) participation chance; the "steady hand" strategy
                forces exactly one raise per lot. At most 2 raises per round
                to keep pacing brisk. Quiet rounds say so in one line.
                big_raise=True marks the round as opened by a jump raise
                (player bid well above the minimum), chilling the room.
            ZH: 一轮竞价：每名有意愿的竞买人按（衰减后的）参与概率掷点；
                "稳健派"策略强制每个拍品抬一次价。每轮最多成功抬价 2 次
                以保持节奏。全场冷场时只播报一行。
                big_raise=True 表示本轮由跳价开场（玩家大幅加价），
                全场意愿额外降低。
            """
            self.ensure_bidders(lot)
            bidders = list(self.bidders)
            renpy.random.shuffle(bidders)
            player = auction_player_name()
            lot_id = self._lot_id(lot)
            raises_left = 2  ## EN: Max successful raises per round. ZH: 每轮最多成功抬价次数。
            self._round_big_raise = bool(big_raise)
            any_raise = False

            for bidder in bidders:
                if raises_left <= 0:
                    break
                if not self._npc_may_bid(bidder, lot):
                    continue

                force_raise = (bidder.strategy == AuctionBidder.STRAT_PERSISTENT
                               and lot_id not in bidder._raised_lot_ids)
                if not force_raise and dice(100) > self._willingness(bidder, lot) * 100:
                    continue

                if self._apply_npc_raise(bidder, lot, events) is not None:
                    raises_left -= 1
                    any_raise = True

            if not any_raise:
                events.append(__("The room stays quiet."))
            return lot.current_bidder != player

        def wait_round(self):
            """
            EN: The player waits without bidding — one NPC round plays out.
                Returns the event list (may be a single "room stays quiet").
            ZH: 玩家不出价等待——进行一轮 NPC 竞价。返回事件列表
                （可能只有一行"全场冷场"）。
            """
            events = []
            lot = self.current_lot
            if lot is None or lot.status != AuctionLot.STATUS_ACTIVE:
                return [__("There is no active lot right now.")]
            self._npc_counter_round(lot, events)
            return events

        def _release_player_bid(self, lot):
            """
            EN: Free the gold reserved by the player's standing bid on a lot
                (outbid or settled). Safe to call repeatedly.
            ZH: 释放玩家在此拍品上的在场出价所占用的金币（被反价或已结拍）。
                可重复调用。
            """
            if lot.player_bid:
                self.player_committed = max(0, self.player_committed - lot.player_bid)
                lot.player_bid = 0

        def _cancel_player_bids(self, lot):
            """
            EN: Withdraw every player bid on a lot, restoring the bid history
                to the last NPC bid (or the starting price). Used when the
                player leaves early — the session wraps up without them.
            ZH: 撤回玩家在此拍品上的所有出价，将出价记录恢复到上一个
                NPC 出价（或起拍价）。玩家提前离场时使用——后续结拍与其无关。
            """
            self._release_player_bid(lot)
            lot.bids = [b for b in lot.bids if not b.is_player]
            if lot.bids:
                top = lot.bids[-1]
                lot.current_bid = top.amount
                lot.current_bidder = top.bidder_name
            else:
                lot.current_bid = lot.starting_price
                lot.current_bidder = None

        def player_bid_current(self, amount):
            """
            EN: Place the player's bid on the current lot, then run one NPC
                dice counter-round. The bid reserves gold (player_committed)
                so bidding on several lots cannot overdraw MC. Returns
                (ok, events).
            ZH: 玩家对当前拍品出价，并触发一轮 NPC 骰子反价。出价会占用
                金币（player_committed），防止对多个拍品出价导致 MC 透支。
                返回 (是否接受, 事件文本列表)。
            """
            events = []
            lot = self.current_lot
            if lot is None or lot.status != AuctionLot.STATUS_ACTIVE:
                return False, [__("There is no active lot right now.")]
            previous_bid = lot.player_bid
            previous_top = lot.current_bid
            if not lot.place_bid(auction_player_name(), amount, is_player=True):
                return False, [__("Your bid is too low.")]

            ## EN: Total exposure = commitments on OTHER lots + this lot's new
            ##     bid. player_committed still holds this lot's previous bid,
            ##     so subtract it before adding the new amount back.
            ## ZH: 总占用 = 其他拍品的承诺 + 本拍品新出价。
            ##     player_committed 仍含本拍品旧出价，先减去再加回新出价。
            exposure = (self.player_committed - previous_bid) + lot.player_bid
            if MC.gold < exposure:
                lot.bids.pop()
                lot.current_bid = lot.bids[-1].amount if lot.bids else lot.starting_price
                lot.current_bidder = lot.bids[-1].bidder_name if lot.bids else None
                lot.player_bid = previous_bid
                return False, [__("You don't have enough gold (you have %d gold committed on other lots).") % self.player_committed]

            self.player_committed = exposure
            events.append(__("You raise your paddle: %d gold for %s!") % (amount, lot.get_display_name()))
            ## EN: A raise well above the minimum (more than min + 3% of base
            ##     value) counts as a jump bid and chills this NPC round.
            ## ZH: 明显高于最低加价的出价（超出 最低加价+原价3% 的部分）
            ##     视为跳价，使本轮 NPC 意愿额外降低。
            big_raise = amount > previous_top + lot.min_increment + int(max(1, lot.get_base_value("buy")) * 0.03)
            self._npc_counter_round(lot, events, big_raise=big_raise)
            if lot.current_bidder != auction_player_name():
                self._release_player_bid(lot)
                events.append(__("You have been outbid."))
            return True, events

        ## ============================================================
        ##  Settlement (gavel)
        ## ============================================================

        def settle_lot(self, lot):
            """
            EN: Finalize a lot and move gold/goods. Returns narration events.
                Rules:
                - player buys NPC goods  -> gold leaves, goods delivered;
                - NPC buys player goods  -> gold paid out (listing fee was
                  already charged at submission);
                - player buys own goods  -> NO sale proceeds, and the auction
                  house still charges commission = gavel price x fee_rate;
                - unsold player goods    -> returned from escrow;
                - unsold NPC goods       -> withdrawn.
            ZH: 结拍拍品并转移金币/货物，返回叙述事件。
                规则：
                - 玩家购得 NPC 商品 → 扣款并交割；
                - NPC 购得玩家商品 → 支付货款（挂牌手续费已在提交时收取）；
                - 玩家拍下自己的商品 → 无销售款，拍卖行仍按落锤价 × 费率
                  收取佣金；
                - 玩家商品流拍 → 托管退还；
                - NPC 商品流拍 → 撤回。
            """
            events = []

            ## EN: The lot settles — any reserved player gold is released
            ##     (converted to payment below, or freed when outbid/unsold).
            ## ZH: 拍品结拍——释放玩家在本拍品上预留的金币
            ##     （下方转为货款，或被反价/流拍而释放）。
            self._release_player_bid(lot)

            if lot.status == AuctionLot.STATUS_ACTIVE:
                status, winner, price = lot.finalize()
            else:
                status, winner, price = lot.status, lot.current_bidder, lot.current_bid

            player = auction_player_name()
            winner_is_player = (winner == player)

            if status == AuctionLot.STATUS_SOLD:
                if lot.seller == "player":
                    if winner_is_player:
                        ## EN: Self-purchase: no proceeds, commission still due
                        ##     (capped at what MC can actually pay).
                        ## ZH: 自买自卖：无销售款，仍需支付佣金（以 MC 实际付得起为上限）。
                        fee = min(auction_listing_fee(price), max(0, MC.gold))
                        MC.gold -= fee
                        events.append(__("You wind up buying your own %s for %d gold. The auction house charges its %d gold commission (fee rate %s%%) anyway.") % (lot.get_display_name(), price, fee, "%.1f" % (auction_fee_rate() * 100)))
                        self._return_escrow(lot, events)
                    else:
                        MC.gold += price
                        events.append(__("%s is sold to %s for %d gold!") % (lot.get_display_name(), winner, price))
                        self._release_escrow(lot, events)
                else:
                    if winner_is_player:
                        ## EN: Defensive: with commitment tracking this should
                        ##     never trigger, but never let a gavel drive MC
                        ##     below zero.
                        ## ZH: 防御式：有承诺机制理论上不会触发，但绝不让
                        ##     落锤把 MC 扣成负数。
                        if MC.gold >= price:
                            MC.gold -= price
                            events.append(__("Sold! You win %s for %d gold.") % (lot.get_display_name(), price))
                            self._deliver_to_player(lot, events)
                        else:
                            status = AuctionLot.STATUS_UNSOLD
                            lot.status = AuctionLot.STATUS_UNSOLD
                            events.append(__("You won %s for %d gold but cannot cover it — the lot is passed in.") % (lot.get_display_name(), price))
                    else:
                        bidder = self._bidder_by_name(winner)
                        if bidder is not None:
                            bidder.spent += price
                            bidder.committed = max(0, bidder.committed - price)
                            bidder.won.append(lot.get_display_name())
                        events.append(__("%s buys %s for %d gold.") % (winner, lot.get_display_name(), price))
            else:
                events.append(__("No one meets the reserve. %s is passed in.") % lot.get_display_name())
                if lot.seller == "player":
                    self._return_escrow(lot, events)

            self.results.append((status, winner, price))
            return events

        def _deliver_to_player(self, lot, events):
            """EN: Hand a won NPC lot to MC. ZH: 将购得的 NPC 拍品交给 MC。"""
            try:
                if lot.kind == "item" and lot.item is not None:
                    MC.items.append(lot.item)
                    events.append(__("%s has been added to your inventory.") % lot.get_display_name())
                elif lot.girl is not None:
                    MC.girls.append(lot.girl)
                    if hasattr(lot.girl, "init_after_acquire"):
                        lot.girl.init_after_acquire()
                    events.append(__("%s now belongs to you.") % lot.get_display_name())
            except Exception as e:
                renpy.notify(__("Auction mod: %s") % e)

        def _return_escrow(self, lot, events):
            """EN: Return an unsold/self-bought player lot to MC.
                   ZH: 将流拍/自购的玩家拍品退回托管。"""
            try:
                if lot.kind == "item" and lot.item is not None:
                    if lot.item not in MC.items:
                        MC.items.append(lot.item)
                    events.append(__("%s is returned to your inventory.") % lot.get_display_name())
                elif lot.girl is not None:
                    if lot.girl not in MC.girls:
                        MC.girls.append(lot.girl)
                    events.append(__("%s returns to your brothel.") % lot.get_display_name())
            except Exception as e:
                renpy.notify(__("Auction mod: %s") % e)

        def _release_escrow(self, lot, events):
            """EN: Player goods finally sold to an NPC — clean up like a sale.
                   ZH: 玩家商品最终售予 NPC——按出售清理。"""
            try:
                if lot.kind == "girl" and lot.girl is not None:
                    relinquish_girl(lot.girl)
            except Exception as e:
                renpy.notify(__("Auction mod: %s") % e)

        def settle_current_lot(self):
            """EN: Settle the current lot (gavel) and advance. Returns events.
                   Bidders persist across the whole session (their budgets,
                   strategy memory and win counts are session-scoped).
               ZH: 结拍当前拍品（落锤）并前进，返回事件。
                   竞买人整场有效（预算、策略记忆、拍得计数均为
                   会话级，不随拍品重置）。"""
            events = []
            if self.current_lot:
                events = self.settle_lot(self.current_lot)
                self.current_lot_index += 1
            return events

        def advance_lot(self):
            """
            EN: Two-step gavel. First call warns ("going once...") and gives
                NPCs one final round if the player is not on top — the lot is
                NOT settled yet, so the player gets a last chance to answer.
                Second call finalizes the lot and moves to the next.
                Returns (next_lot, events).
            ZH: 两步落锤。第一次调用只喊"第一次……"并在玩家不是最高价时
                给 NPC 最后一轮出价机会——此时拍品还不结拍，玩家仍可加价
                应答；第二次调用才真正结拍并移至下一件。
                返回 (下一个拍品, 事件)。
            """
            events = []
            lot = self.current_lot
            if lot is not None and lot.status == AuctionLot.STATUS_ACTIVE:
                self.ensure_bidders(lot)
                if not lot.warned:
                    ## EN: First pass — warn only, no gavel yet.
                    ## ZH: 第一次 pass——只喊提醒，不落锤。
                    lot.warned = True
                    if lot.current_bidder != auction_player_name():
                        self._npc_counter_round(lot, events)
                    events.append(__("Going once... %s at %d gold.") % (lot.get_display_name(), lot.current_bid))
                    return self.current_lot, events
                ## EN: Second pass — one last NPC round if the player is not
                ##     on top, then settle.
                ## ZH: 第二次 pass——玩家不是最高价时先给 NPC 最后一轮，
                ##     然后结拍。
                if lot.current_bidder != auction_player_name():
                    self._npc_counter_round(lot, events)
            events = events + self.settle_current_lot()
            return self.current_lot, events

        def wrap_up(self, events):
            """
            EN: Settle all remaining lots without the player (used when the
                player leaves early): one or two NPC dice rounds per lot, then
                the gavel. Player goods that go unsold return from escrow.
            ZH: 不经玩家直接结拍所有剩余拍品（玩家提前离场时使用）：
                每件拍品进行 1-2 轮 NPC 骰子竞价后落锤；
                流拍的玩家商品由托管退还。
            """
            while self.current_lot is not None:
                lot = self.current_lot
                ## EN: The player walked out — withdraw their standing bids
                ##     instead of forcing a purchase they can't attend.
                ## ZH: 玩家已离场——撤回其在场出价，而非强迫成交。
                self._cancel_player_bids(lot)
                self.ensure_bidders(lot)
                for _i in range(renpy.random.randint(1, 2)):
                    self._npc_counter_round(lot, events)
                self.settle_lot(lot)
                self.current_lot_index += 1
            self.bidders = None  ## EN: Session over — release the bidder roster. ZH: 会话结束——释放竞买人名单。
            self.phase = self.PHASE_RESOLVED

        def auto_resolve(self):
            """
            EN: Simulate NPC bidding on all lots and finalize everything.
                Used when player skips or for background auction resolution.
            ZH: 模拟所有拍品的 NPC 出价并全部结拍。
                用于玩家跳过或后台拍卖结算。
            """
            import random
            npc_names = auction_bidder_name_pool()

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
            if MC.gold < lot.reserve_price + self.player_committed:
                return False

            lot.place_bid(auction_player_name(), lot.reserve_price, is_player=True)
            lot.finalize()
            self.player_committed += lot.reserve_price
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
            Schedule: auctions are held every 7 days on days 1/8/15/22 of the
            28-day month ((day - 1) % 7 == 0). The first session held in each
            month is a grand auction. State is kept in this store object, so it
            is saved with the game.
        ZH: 持久化的拍卖行，追踪历史记录并安排拍卖会话。
            日程：每月 28 天中第 1/8/15/22 天（(day - 1) % 7 == 0）每 7 天
            举行一次；每月第一次举行的为大拍卖。状态保存在本 store
            对象中，随存档写入。
        """

        ## EN: Save-compatibility defaults (see AuctionLot.FIELD_DEFAULTS).
        ##     "frequency" is retired: v1 saves carry 30 (monthly); weekly
        ##     scheduling derives from next_auction_day directly.
        ## ZH: 存档兼容默认值（见 AuctionLot.FIELD_DEFAULTS）。
        ##     "frequency" 已弃用：v1 存档带 30（每月一次）；v2.1 每周
        ##     日程直接由 next_auction_day 推导。
        FIELD_DEFAULTS = {
            "history": [],
            "next_auction_day": 1,
            "frequency": 7,
            "last_auction_month": None,
            "insight_unlocked": False,
        }

        ## EN: Price of the Insider's Ledger — the item that reveals bidders'
        ##     hidden thresholds (total budget, premium tolerance, base chance).
        ## ZH: 《内行账本》售价——购买后可见竞买人的隐藏阈值
        ##     （总预算、溢价容忍度、基础概率）。
        INSIGHT_PRICE = 2500

        def __init__(self):
            self.history = []           ## EN: Past auction results. ZH: 过去的拍卖结果。
            self.next_auction_day = 1   ## EN: Next day-of-month an auction may be held. ZH: 下次可举行拍卖的当月日。
            self.frequency = 7          ## EN: Retired (was days between auctions). ZH: 已弃用（原为拍卖间隔天数）。
            self.last_auction_month = None  ## EN: Month of the last held auction. ZH: 上次举行拍卖的月份。
            self.insight_unlocked = False   ## EN: Bidder thresholds revealed. ZH: 已解锁竞买人阈值显示。

        def __getattr__(self, name):
            defaults = object.__getattribute__(self, "__class__").FIELD_DEFAULTS
            if name in defaults:
                return defaults[name]
            raise AttributeError(name)

        ## ============================================================
        ##  Insight (hidden thresholds revealed)
        ## ============================================================

        def has_insight(self):
            """
            EN: True when the player can see bidders' hidden thresholds
                (total budget, premium tolerance, base chance). Unlocked by
                buying the Insider's Ledger from Gio, or by owning any item
                whose name hints at inside information.
            ZH: 玩家是否可见竞买人的隐藏阈值（总预算、溢价容忍度、基础
                概率）。向 Gio 购买《内行账本》后解锁；或持有名称暗示
                内部消息的物品时也视为解锁。
            """
            try:
                if self.insight_unlocked:
                    return True
                for it in getattr(MC, "items", []) or []:
                    name = str(getattr(it, "name", it)).lower()
                    if any(k in name for k in ("insider", "ledger", "spyglass", "洞察", "内行", "账本")):
                        return True
            except Exception:
                pass
            return False

        def buy_insight(self):
            """
            EN: Buy the Insider's Ledger from Gio. Returns True on success.
            ZH: 向 Gio 购买《内行账本》。成功返回 True。
            """
            try:
                if self.insight_unlocked:
                    return True
                if MC.gold < self.INSIGHT_PRICE:
                    return False
                MC.gold -= self.INSIGHT_PRICE
                self.insight_unlocked = True
                return True
            except Exception:
                return False

        ## ============================================================
        ##  Scheduling
        ## ============================================================

        def schedule_next(self, from_day=None):
            """EN: Schedule the next auction day (weekly).
                   ZH: 安排下次拍卖日（每周）。"""
            base = from_day if from_day is not None else (calendar.day if calendar else 0)
            self.next_auction_day = base + 7

        def hold_session(self):
            """EN: Book a session right now: push the schedule a week ahead
                   and stamp the month so the next one is regular.
               ZH: 立即登记一场拍卖会：日程顺延一周，并记录月份，
                   使本月后续场次为普通拍卖。"""
            self.schedule_next()
            if calendar:
                self.last_auction_month = calendar.month

        def is_due(self):
            """EN: Kept for v1 compatibility. Use can_hold_auction().
                   ZH: 为 v1 兼容保留。请使用 can_hold_auction()。"""
            return calendar and calendar.day >= self.next_auction_day

        def can_hold_auction(self):
            """
            EN: True when an auction may be held today: the calendar runs on
                28-day months, so auction days are 1/8/15/22, and the weekly
                appointment must have arrived. next_auction_day may land past
                the month end (22 + 7 = 29) — that simply means "the next
                auction day from now on".
            ZH: 今天是否可举行拍卖：游戏日历每月 28 天，拍卖日为
                第 1/8/15/22 天，且每周的预约必须已到期。
                next_auction_day 可能越过月末（22 + 7 = 29）——
                此时表示"从下一个拍卖日起均可举行"。
            """
            if not calendar:
                return False
            if (calendar.day - 1) % 7 != 0:
                return False
            if self.next_auction_day > 28:
                ## EN: Appointment wrapped past the month end.
                ## ZH: 预约日越过月末，周期已到期。
                return True
            return calendar.day >= self.next_auction_day

        def is_grand_today(self):
            """
            EN: The first session HELD each month is the grand auction.
            ZH: 每月第一次"举行"的拍卖会为大拍卖。
            """
            return bool(calendar) and self.last_auction_month != calendar.month

        def get_next_auction_info(self):
            """
            EN: Tooltip helper. Returns (day_label, is_grand) for the next
                auction day after today.
            ZH: 悬浮提示辅助。返回今天之后下一个拍卖日的 (日标签, 是否大拍卖)。
            """
            if not calendar:
                return (__("No upcoming auction."), False)

            if self.can_hold_auction():
                return (__("Today"), self.is_grand_today())

            ## EN: Next auction day-of-month: 1/8/15/22 cycle.
            ## ZH: 下一拍卖日：1/8/15/22 循环。
            offset = (7 - (calendar.day - 1) % 7) % 7
            if offset == 0:
                offset = 7
            target_day = calendar.day + offset
            if target_day > 28:
                target_day -= 28
                target_month = calendar.month % 12 + 1
            else:
                target_month = calendar.month

            is_grand = (target_month != self.last_auction_month)
            return (__("Day %d") % target_day, is_grand)

        def get_menu_tooltip(self):
            """EN: Right-menu tooltip text. ZH: 右侧菜单悬浮提示文本。"""
            label, grand = self.get_next_auction_info()
            if label == __("Today"):
                if grand:
                    return __("Auction today — grand auction! Bid on girls and rare items, or list your own goods.")
                return __("Auction today! Bid on girls and items, or list your own goods.")
            if grand:
                return __("Next auction: %s (grand auction).") % label
            return __("Next auction: %s.") % label

        ## ============================================================
        ##  Session building
        ## ============================================================

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

        def _npc_item_pool(self, grand=False):
            """
            EN: Candidate items from the game item pool. Defensive: the items
                system is being reworked in parallel — if the pool cannot be
                found or read, item lots are simply skipped. Grand auctions
                only feature rare goods (numeric rarity >= 3 or special
                S/U/M rarities).
            ZH: 从游戏道具池选取候选道具。防御式编码：道具系统正在并行
                改动——若找不到或读取失败，则跳过道具拍品。
                大拍卖仅展示稀有道具（数值稀有度 >= 3 或特殊稀有度 S/U/M）。
            """
            try:
                pool = globals().get("item_dict")
                if not pool:
                    return []
                result = []
                for it in pool.values():
                    try:
                        if not getattr(it, "sellable", False):
                            continue
                        price = getattr(it, "price", 0)
                        if not price or price < 50:
                            continue
                        rarity = getattr(it, "rarity", 1)
                        if isinstance(rarity, str):
                            rarity = 6  ## EN: S/U/M specials count as rare. ZH: S/U/M 特殊稀有度按稀有计。
                        if grand and rarity < 3:
                            continue
                        result.append(it)
                    except Exception:
                        continue
                return result
            except Exception:
                return []

        def build_session(self, grand=False):
            """
            EN: Build a full session for today. Grand auctions offer more lots
                and rare items; regular auctions are smaller. Girls come from
                get_girls(), items from the item pool (skipped defensively).
            ZH: 构建今天的拍卖会话。大拍卖拍品更多且含稀有道具；
                普通拍卖规模较小。女孩来自 get_girls()，
                道具来自道具池（读取失败则跳过）。
            """
            lots = []

            ## EN: NPC girls.
            ## ZH: NPC 女孩拍品。
            try:
                girls = get_girls(3 if grand else 2)
            except Exception:
                girls = []
            for g in girls:
                try:
                    lots.append(AuctionLot(g, seller=__("Anonymous Seller"), kind="girl"))
                except Exception:
                    continue

            ## EN: NPC items (rare-only at grand auctions).
            ## ZH: NPC 道具拍品（大拍卖仅稀有）。
            pool = self._npc_item_pool(grand=grand)
            renpy.random.shuffle(pool)
            for it in pool[: (3 if grand else 2)]:
                try:
                    inst = it.get_instance()
                    value = int(getattr(it, "price", 100))
                    lots.append(AuctionLot(None, seller=__("Anonymous Seller"),
                                           kind="item", item=inst,
                                           estimated_value=value))
                except Exception:
                    continue

            renpy.random.shuffle(lots)

            name = __("Grand Auction") if grand else __("Weekly Auction")
            return AuctionSession(lots, session_name=name, grand=grand)

        ## ============================================================
        ##  Player submissions (escrow + listing fee)
        ## ============================================================

        def submit_girl(self, girl, session):
            """
            EN: Escrow one of MC's girls into the session as a player lot and
                charge the listing fee = int(value x fee_rate). The girl
                leaves MC.girls until the lot settles (sold / returned).
                Returns (lot, fee, error_message_or_None).
            ZH: 将 MC 的一名女孩托管进会话成为玩家拍品，并收取挂牌手续费
                = int(估值 × 费率)。女孩在结拍前离开 MC.girls
                （售出/退还时处理）。返回 (拍品, 手续费, 错误信息或 None)。
            """
            if girl is None or girl not in MC.girls:
                return None, 0, __("She is not in your brothel.")
            try:
                value = girl.get_price("sell", raw=True) if hasattr(girl, "get_price") else 100
                value = int(value)
            except Exception:
                value = 100
            fee = auction_listing_fee(value)
            if MC.gold < fee:
                return None, fee, __("You cannot afford the listing fee (%d gold).") % fee

            MC.gold -= fee
            try:
                if hasattr(girl, "set_job"):
                    girl.set_job(None)
            except Exception:
                pass
            MC.girls.remove(girl)

            lot = AuctionLot(girl, seller="player", kind="girl", estimated_value=value)
            session.lots.append(lot)
            return lot, fee, None

        def submit_item(self, item, session):
            """
            EN: Escrow one of MC's items into the session as a player lot and
                charge the listing fee. Returns (lot, fee, error_message_or_None).
            ZH: 将 MC 的一件道具托管进会话成为玩家拍品并收取手续费。
                返回 (拍品, 手续费, 错误信息或 None)。
            """
            if item is None or item not in MC.items:
                return None, 0, __("This item is not in your inventory.")
            try:
                gp = getattr(item, "get_price", None)
                value = int(gp("sell")) if callable(gp) else int(getattr(item, "price", 100))
            except Exception:
                value = 100
            fee = auction_listing_fee(value)
            if MC.gold < fee:
                return None, fee, __("You cannot afford the listing fee (%d gold).") % fee

            MC.gold -= fee
            MC.items.remove(item)

            lot = AuctionLot(None, seller="player", kind="item", item=item,
                             estimated_value=value)
            session.lots.append(lot)
            return lot, fee, None

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


    ## EN: Wrapper for Function() actions whose target returns a value.
    ##     In Ren'Py 8, a Function action whose callable returns non-None
    ##     ends the current interaction with that value as the result; the
    ##     main loop then treats it as a teleport destination and crashes
    ##     (jump expression <object>). _run discards the return value so the
    ##     interaction keeps running. Example crash: advance_lot() returns
    ##     the next AuctionLot -> "jump teleport" -> ScriptError.
    ## ZH: 用于"被调函数会返回值"的 Function() action 的包装。
    ##     Ren'Py 8 中，Function action 的 callable 返回非 None 时会
    ##     立即结束当前交互并以该值为交互结果；主循环随后把它当作
    ##     teleport 目的地而崩溃（jump expression <对象>）。
    ##     _run 丢弃返回值，使交互继续进行。
    ##     崩溃示例：advance_lot() 返回下一个 AuctionLot →
    ##     "jump teleport" → ScriptError。
    def _run(f, *a, **k):
        f(*a, **k)
