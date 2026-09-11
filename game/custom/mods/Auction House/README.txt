拍卖行 Mod — 说明 | Auction House Mod — README
=====================================================

本 Mod 通过 Mod API v2 注册，mod_id 为 "auction_house"。安装即常驻激活；
卸载 = 删除本目录。

 v2.1 场景化改造 | Scenario-driven overhaul (v2.1)
-----------------------------------------------------

日程 | Schedule
--------------
- 拍卖行每周举行一次。游戏日历每月 28 天，可举行的日子为
  第 1 / 8 / 15 / 22 天（即 (calendar.day - 1) % 7 == 0）。
- 每月"第一次举行"的拍卖会是大拍卖会（Grand Auction）：
  拍品更多（3 女孩 + 3 道具），且道具拍品仅限稀有货
  （数值稀有度 >= 3 或特殊稀有度 S/U/M）。NPC 竞买人的预算 ×1.3、
  热切值 +10。
- 主页右侧菜单的 Auction 按钮仅在可举行日可点击（sensitive），
  悬浮提示显示"下次拍卖：第 X 天（大拍卖）"。
- 举行一次后 next_auction_day = 当天 + 7，并记录
  last_auction_month。注意 22 + 7 = 29 越过 28 天的月末，
  代码中将 next_auction_day > 28 视为"周期已到期"，
  下一个拍卖日（次月第 1 天）即可举行。

拍品 | Lots
------------
- 拍品分两类：kind = "girl"（女孩）/ "item"（道具）。
- NPC 拍品：女孩由 get_girls() 生成；道具从全局 item_dict
  道具池随机抽取（防御式读取——读取失败时自动跳过道具拍品，
  兼容正在进行中的道具系统重构）。
- 玩家拍品：在拍卖现场通过"提交拍品"面板上架女孩或道具。
  选中即收取挂牌手续费，商品进入托管（女孩离开 MC.girls，
  道具离开背包），直至结拍：
  - 售出 → 女孩按 relinquish_girl 清理、道具由买家所得；
  - 流拍或玩家自己拍下 → 退回青楼 / 背包。

手续费公式 | Fee formula
--------------------------
本体难度为字符串（very easy / easy / normal / hard / insane），
代码按下标 +1 映射为数值 1-5（未知值回退 3）：

    fee_rate = min(0.30, 0.08 + 0.015 × difficulty)

对应费率：非常简单 9.5% / 简单 11% / 普通 12.5% / 困难 14% / 疯狂 15.5%。

- 挂牌手续费（提交时收取）= int(估值 × fee_rate)，至少 1 金币。
- 自购佣金（玩家拍下自己的商品）= int(落锤价 × fee_rate)。
  自买自卖不获得销售款，但佣金照付（用户明确要求）。

骰子抬价 | Dice counter-bidding
---------------------------------
- 每个拍品开拍时生成 3-5 名虚拟竞买人（复用现有角色名）：
  budget = 拍品买价 × (0.8~1.6 随机)；
  agitation = (d60 + 10) ~ d100 随机，即
  renpy.random.randint(dice(60) + 10, 100)。
- 玩家出价后，每名竞买人掷 d100：点数 ≤ agitation 且
  预算足够时反价（当前价 + 最小加价，不超过预算）。
  过程逐条叙述（含骰点 flavor，如
  "Merchant Velira 掷出 43，决定加价到 320 金币！"）。
- 无人反价 → 立即落锤，拍品归玩家；被反价 → 玩家可加价或放弃
  （放弃则按当前最高结拍，可能是 NPC 购得玩家商品）。

场景 | Scene
------------
- 入口：右侧菜单按钮 action = Call("auction_scene")（label 驱动）。
- 背景用游戏现有素材：bg slave market；拍卖师为 Gio
  （show gio at right，slave market intro 同款角色）。
- auction_house 屏幕为透明背景 + modal True，场景从面板边缘透出；
  按钮一律 Return(("action", ...))，由 label 统一处理状态变更，
  不使用 Function() action（避免主循环 teleport 崩溃，见 v2.0 修复）。
- 提前离场：剩余拍品由 NPC 骰子自动结拍，玩家商品流拍自动退还。

存档兼容 | Save compatibility
--------------------------------
- AuctionHouse / AuctionSession / AuctionLot 新增字段均通过
  类级 FIELD_DEFAULTS + __getattr__ 兜底：Ren'Py 恢复旧存档实例时
  不运行 __init__，缺失属性按默认值返回（kind="girl"、
  last_auction_month=None 等）。
- frequency 字段已弃用（v1 为 30 天/次），仅作兼容保留。

文件 | Files
------------
- auction.rpy         核心类与调度、费率、托管、骰子竞买人
- auction_scene.rpy   label auction_scene：场景 + 竞拍主循环
- auction_screens.rpy auction_house / auction_submit 屏幕
- mod.rpy             Mod API v2 注册 + 右侧菜单按钮
- tl/                 中文翻译（strings 由翻译工具链维护）
