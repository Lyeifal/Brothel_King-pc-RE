# 第二轮 Mod 完善方案：模组管理页、庭院交互、拍卖行 NPC 策略与场景重排

> 状态：实施中。日期：2026-09-25（第二轮）
> 依赖：第一轮方案 `MOD_IMPROVEMENT_PLAN.md`（已完成）

## M1. 模组管理页（screen mod_manager）

**问题**：页面 `tag menu` 替换了主菜单屏幕，而主菜单背景图是主菜单屏幕自己画的
（`add gui.main_menu_background`），被替换后只剩 `Solid("#000000B3")` → 全黑。
启用状态虽有文字但辨识度差。

**修法**：
- 去掉 `tag menu`，改为 `zorder 10` 浮层：主菜单背景保留、压暗显示
- 状态改为高对比徽章：绿色底"已启用" / 红色底"已禁用" / 橙色"常驻"，
  按钮文字与状态同步切换；切换后立即刷新（现有 SetScreenVariable 已保证）

## M2. 女孩移入庭院交互

**问题**：现有入口仅在"收购女孩且青楼满员"时触发（HOOK_GIRL_DESTINATION_LIST），
日常无法把已有女孩送进庭院。

**修法**（沿用农场模式，核心代码走 Mod 钩子，不写死 courtyard）：
- `mod_api_v2` 新增两个钩子常量：
  - `HOOK_GIRL_ASSIGN_LIST`：Mod 返回 `[{id, text, tooltip, available}]`
  - `HOOK_GIRL_ASSIGN_ACCEPT`：Mod 执行实际移送（context 含 girl、dest_id）
- 核心 `assign_job` 屏幕（screen_girl_stats.rpy）：
  - `grid 4 2` → `grid 4 3`，新增"庭院"格（无图素材，文字钮 + 序号 9），
    仅在钩子返回 available 时渲染，否则补 null
  - 返回 `("mod_dest", dest_id)`；核心 main.rpy 循环新分支调 ACCEPT 钩子
- 庭院 mod 注册两钩子：`can_add_girl()` 判定可用性，accept 时
  `courtyard_villa.add_girl(girl)`（已有方法，内部从 MC.girls 移除）

## M3. 庭院温泉改为受伤恢复概率

**问题**：温泉当前加能量恢复速度；用户要求改为"概率加速受伤恢复"。

**修法**：
- 移除温泉的 energy recovery 效果；新效果：每日每名别院女孩
  `chance = min(10%, 2% + 1% × 温泉等级)` 使 `girl.hurt` 额外 -1
  （1 级 3%、每级 +1%、上限 10%）
- 为让上限可达：温泉 `max_level` 3 → 8，`courtyard_upgrade_costs.json`
  补 4-8 级费用（800/2000/3200/4600/6200/8000/10000 顺延）
- 设施效果说明文案同步改；process_day 中在恢复后、衰减前执行
- 花园（心情恢复）不动

## A1. NPC 策略引擎（auction.rpy 大改）

**NPC 属性扩展**（AuctionBidder 重构）：
- `budget_total`：本场拍卖总花费阈值（全场所有出价之和的上限）
- `premium_max`：单件溢价阈值（愿出到的最高价 = 原价 × premium_max，1.2~2.0 随机）
- `base_chance`：参与喊价/抬价的基础概率（20%~70% 随机）
- `decay_per_step`：每超过原价 5%，意愿降低值（3~10 个百分点，各 NPC 不同）
- `strategy`：性格策略，随机分配：
  - `persistent` 稳健派——每个拍品固定抬一次价（必触发一次）
  - `finale` 压轴派——只参与最后 2 个拍品
  - `collector` 收藏派——全场最多拍下 2 件，达到后不再出价
  - `stubborn` 执拗派——一旦对某件出过价，此后无视溢价阈值（受其总预算约束）
- `spent`：本场已花费；`won`：已拍得件数

**出价判定**（每次 NPC 行动）：
1. 策略门槛（persistent/finale/collector/stubborn 各自规则）
2. `spent + 本次出价 ≤ budget_total`
3. 当前价 ≤ 原价 × premium_max（stubborn 激活后跳过）
4. 概率判定：`p = base_chance - decay_per_step × floor((当前价-原价)/原价/5%)`，
   另：本轮中若出现"高于最低加价 3% 原价"的抬价，全场 NPC 意愿额外 -10%
   （一次性事件惩罚，记 session 级标记）

**价格规则**：
- 起拍价 = 商店价 × 90%（`starting_price = int(value*0.9)`，下限 1）
- 最低加价 = 原价 × 5% 向上取整（`min_increment = ceil(value*0.05)`，下限 1）

**阈值可见性**：
- 新增 `auction_house.insight_unlocked`（持久化字段，FIELD_DEFAULTS 兜底 False）
- 解锁途径二选一即生效：MC 持有名称含 "insider"/"ledger"/"洞察"/"手册" 的道具，
  或向 Gio 一次性购买"内行手册"（场景内购买按钮，价格 2500，买后常显阈值）
- 未解锁时 NPC 面板只显示名字/当前出价/花费/收获；解锁后追加
  总预算/溢价阈值/基础概率

## A2. 拍卖流程：等待按钮、流拍提醒、离场静默

- **等待按钮** "Wait"：玩家不出价，直接进行一轮 NPC 竞价（复用
  `_npc_counter_round`），返回事件照常播报；全场冷场时可用来钓鱼
- **流拍提醒**：落锤拆成两步——第一次点"Pass / gavel"只喊"第一次
  （Going once...）"并在拍品上标记 `warned=True`；第二次点才正式落锤。
  当前价未达保留价（将流拍）时同样走两次确认，给玩家留下介入机会
- **离场静默**：`wrap_up` 增加 narrate 开关；离场时静默结算，只播报一行
  汇总（"本场剩余 N 件成交，你收入/支出 M 金币"），不再逐条展示 NPC 骰子过程
- 拍卖过长问题由等待按钮+两步落锤共同缓解（玩家可主动推进节奏）

## A3. 拍卖场景 UI 重排（auction_screens.rpy 重写主屏）

三栏布局（屏幕 1280 宽容器）：
- **左栏（260px）**：本场拍品列表（已有，微调：显示起拍价与状态）
- **中栏（400px）**：参与 NPC 面板——彩色圆形首字母头像 + 名字 + 当前出价 +
  已花费 + 已获拍品；解锁洞察后追加阈值行；下方放"Wait"按钮与事件滚动条
- **右栏（520px）**：当前拍品详情——
  - 道具：图标 + 名称 + 类型/稀有度/充能 + 原价/起拍价/当前价/保留价
  - 女孩：`girl.get_pic()` 立绘；**鼠标悬浮立绘显示属性浮层**
    （独立 tooltip 屏幕，hovered Show/unhovered Hide）
  - 出价区在价格下方：`-`/`+`/`+10`/`+50` + 出价金额 + Bid 按钮
    （沿用第一轮的承诺金币校验）
- 底栏：Pass/Gavel（两步提示）/ List goods / Leave

## 收尾

- T1. `translate --empty` 解析验证
- T2. 新增字符串模型直译导入，三项校验（count/placeholders/lint）
- T3. 分模块提交：核心（mod_manager + assign_job 钩子）、庭院（温泉）、
  拍卖行（引擎+流程+UI）三个 commit

## 不做 / 默认决定

- 不引入新图片素材：NPC "头像"用彩色首字母圆盘，女孩立绘用游戏自带 `get_pic()`
- 不改动农场训练与庭院衰减（用户已确认保留）
- 玩家自售拍品的起拍规则沿用原估值逻辑（新价格规则只作用于 NPC 上架商品）

## 完成记录（2026-09-25）

- [x] M1 模组管理页：`tag menu` → `zorder 10` 浮层（修黑背景），状态徽章改纯色底
- [x] M2 女孩移入庭院：`HOOK_GIRL_ASSIGN_LIST/ACCEPT` 钩子 + assign_job 网格 4x3 + 快捷键 K_9 + main.rpy 分发；庭院注册钩子
- [x] M3 温泉改受伤恢复：效果接线 `injury recovery`，1 级 3%/日、每级 +1%、上限 10%，仅庭院女孩生效，扩建至 8 级
- [x] A1 NPC 策略引擎：四策略（稳健/压轴/收藏/执拗）、双阈值（全场总预算 + 单件溢价）、概率随超原价 5% 衰减、最低加价 = 原价 5% 向上取整、起拍价 = 商店价 90%、跳价降温（玩家与 NPC 双向）、竞买人整场有效
- [x] A2 拍卖流程：Wait 按钮、两步落锤（第一次提醒/第二次结拍）、离场静默结算（只报金币差额）、冷场单行播报
- [x] A3 UI 重排：左拍品列表 / 中 NPC 面板（头像、出价、已消耗、已获得、账本阈值）/ 右详情 + 女孩立绘悬浮属性；洞察 = Gio 处 2500 金购《内行账本》
- [x] T1-T3 解析验证、34 条新串模型直译、三项校验通过、分 3 个 commit
- 修复过程中的额外发现：`_apply_npc_raise` 旧出价释放计算恒为 0 的 bug（已修）
