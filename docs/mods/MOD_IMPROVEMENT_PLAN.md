# Mod 完善方案：庭院（Courtyard）与拍卖行（Auction House）

> 状态：实施中。每个条目完成后在 `[ ]` 中打 `x` 并注明 commit。
> 日期：2026-09-25

## 总体判断

两个 Mod 的底层架构是健康的（Mod API v2 注册、场景化 label + `call screen` + 返回元组、
无 Function() 陷阱、托管/结算闭环完整）。问题集中在四类：

1. **i18n 违规**（庭院屏源语言写成中文，英文玩家会看到中文）
2. **交互逻辑缺陷**（拍卖出价体验、金币可为负、误触无确认）
3. **死代码 / 语义不清**（庭院设施效果未接线、训练把 XP 当属性点）
4. **场景表现单薄**（两个场景只有一张背景 + 一个立绘，无变化）

数值公式（租金、费率、衰减）本次**不改动**，只做体验修正。

---

## 一、庭院（Courtyard）任务清单

### C1. 屏幕硬编码中文改为英文源串 + `__()`

`screen_courtyard.rpy` 中 15 处源串为中文，违反项目 i18n 规范（源串必须英文）：

| 行 | 现源串 | 改为 |
|---|---|---|
| 54 | `别院` | `Courtyard` |
| 60 | `女孩: [n] / [m]` | `Girls: [n] / [m]` |
| 65 | `今日租金: [r] 金币` | `Rent today: [r] gold` |
| 70 | `每日维护: [u] 金币` | `Upkeep: [u] gold` |
| 178 | `返回青楼` | `Return to Brothel` |
| 184 | `青楼已达最大工作容量(24)` | `The brothel is at maximum capacity (24).` |
| 190 | `训练(缓慢)` | `Train (slow)` |
| 194 | `释放` | `Release` |
| 199 | `选择一个女孩进行管理。` | `Select a girl to manage.` |
| 224 | `设施` | `Facilities` |
| 243 | `Lv.[a]/[b]` | `Lv. [a]/[b]` |
| 255 | `升级 ([c] 金币)` | `Upgrade ([c] gold)` |
| 260 | `最高等级` | `Max level` |
| 270 | `房间租金随地区等级…` | `Rent scales with district rank, difficulty and headcount; idle girls' skills decay.` |
| 281 | `购买别院扩建地契 ([p] 金币)` | `Buy Courtyard Expansion Deed ([p] gold)` |
| 289 | `扩建已完成 — 房间上限 [n]` | `Expansion complete — capacity [n]` |
| 297 | `关闭` | `Close` |

另外 `text __(selected_girl.job.capitalize())`（155 行）：对动态值套 `__()` 是**错误用法**
（翻译 key 随运行时值变化，永远命不中）。改为 `text selected_girl.job.capitalize():` 直接显示。

- [x] C1 完成

### C2. 训练语义修正

现状：`train_girl` 只训练 obedience 固定 +1，且 `xp_gain = 10 × duration × efficiency`
被直接当属性增量传给 `change_stat(skill, xp_gain)`——若按字面执行是 +N 属性/天，严重超模；
README 声称"训练效率加成 30%"，与代码 `efficiency = 0.30 + 0.1×lv` 也对不上。

**修法**（保守、不改公式强度）：
1. `change_stat(skill, 1)` 固定 +1 属性（保留"缓慢"定位），`xp_gain` 改为经验：
   调 `girl.xp += xp_gain`（经验不与属性混淆）。
2. 训练按钮 tooltip/提示文案说明效果（+1 指定属性 + 少量经验）。
3. 保持每天限一次（现状已有 day 检查则保留）。

- [x] C2 完成

> **2026-09-25 设计变更（用户裁定）**：庭院的定位是"封存式安置区"——存放超编、
> 不想出售的女孩，本身不带训练属性（训练归农场）。C2 的修正方案随之废止，
> 训练功能**整体移除**：训练按钮、"Already trained today" 提示、`train_girl()`、
> `trained_today` 每日限次机制、training_ground 设施及其升级成本一并删除；
> mod 描述、README 设计定位段落已同步更新。

### C3. 设施效果死代码接线

现状：`facility.get_active_effects()` 生成 Effect 列表，但**全项目无任何调用方**；
恢复/训练加成硬编码在 `_recover_girl` / `train_girl` 里，且与 README 数值不符。

**修法**：在 `_recover_girl` / `train_girl` 中改为读取 `get_active_effects()` 的加成系数，
删除硬编码分支。保持当前实际数值效果不变（等价换算，不增强也不削弱），让 README、
代码、效果三者一致。

- [x] C3 完成

### C4. 场景丰富度（轻量）

现状：庭院场景只有 `bg mansion inside` + Sill 一张立绘。

**修法**：
1. 根据女孩数切换背景（空庭院 / 有女孩在庭院用同背景加环境描述 flavor 轮播文本）。
2. 进场与训练/释放后插入 1-2 条轮播 flavor 文本（已存在 i18n 文案体系则复用）。
3. 不动画效、不引入新素材（无新图片资源）。

- [x] C4 完成

---

## 二、拍卖行（Auction House）任务清单

### A1. 出价交互体验

现状：每次出价后屏幕重建 `bid_amount` 归零；想出高价要连点 `+`；无快捷倍数。

**修法**：
1. 保留 `-` / `+`（步进 min_increment）。
2. 新增 `+×10` / `+×50` 两个按钮（一次加 10/50 个 increment）。
3. `Bid` 按钮旁显示"出价后总计承担"提示文本；玩家当前已承诺金额（对其他 lot 的
   在场最高出价之和）在面板顶部显示。
4. `bid_amount` 不跨 lot 归零问题：改为屏幕 `default` 中 `max(bid_amount, min_bid)`
   显示逻辑保留，但 `+` 按钮基于 `max(bid_amount, current_bid+increment)` 起步即可。

- [x] A1 完成

### A2. 金币可透支（负金币漏洞）

现状：`place_bid` 只检查 `MC.gold >= amount`，**不冻结**。玩家可对多个 lot
分别出价、也可在自购结算时被扣成负数。

**修法**：
1. `AuctionSession` 增加 `player_committed` 属性（玩家所有在场最高出价之和）。
2. `player_bid_current` 校验 `MC.gold >= amount + (committed - 当前 lot 已有玩家出价)`。
3. 玩家被超价 / 落锤时相应增减 `committed`。
4. `settle_lot` 自购分支与 `player_buy_lot` 结算前再次校验
   `MC.gold >= price`，不足则视为 NPC 购得/流拍（防并发负数），扣款用
   `MC.gold = max(0, MC.gold - price)` 兜底。
5. `committed` 加入 session 的 `to_dict/from_dict` 持久化字段（FIELD_DEFAULTS 兼容旧档）。

- [x] A2 完成

### A3. NPC 竞价收敛

现状：`_npc_counter_round` 中每个 NPC 各掷一次，一轮最多抬 3-5 个 increment，
玩家"出价必被连抬"。

**修法**：每次玩家出价后，NPC 反击轮限 **最多 2 次成功抬价**（循环内计数 break），
且单 NPC 每轮最多抬 1 次。预算（`max_bid`）耗尽即不再参与——此逻辑已有，保留。

- [x] A3 完成

### A4. 误触保护

- 右键 `mouseup_3` 直接离场 → 改为 `action Return(("leave",))` 前加确认：
  在 label 层收到 `("leave",)` 时弹 `renpy.display.behavior` 不适用——直接用
  `screen yes_no` 现有模式确认（项目内已有 `call screen confirm` / yesno 工具则复用）。
- 玩家对自己提交上拍的 lot：`Bid` 按钮 `sensitive False` + 提示文本（现状仅提示不禁用）。

- [x] A4 完成

### A5. 场景丰富度（轻量）

现状：拍卖场景 `bg slave market` + Gio，整场无变化。

**修法**：
1. 大拍卖（grand）换用 `bg slave market` 的变体或加聚光效果说明文本；
   若素材库无第二张图，则用 Gio 表情轮换（gio 已有不同表情立绘则换用）。
2. 竞拍白热化（current_bid > reserve×2）时插入拍卖师吆喝 flavor 文本。
3. 不引入新图片资源。

- [x] A5 完成

---

> **2026-09-25 运行时报错修复（用户实测反馈）**：
> - `start_bidding()` 从未被调用 → 拍品永远停在 PENDING，出价牌不出现、落锤灰色。
>   已在构建会话后补调用。
> - 提交商品点 Cancel 返回 `("cancel",)` 落入成功分支 → `auction_lot` 未定义 NameError。
>   已重置 `auction_err/auction_lot` 并仅在成功托管后播报名词。

## 三、收尾（两 Mod 共用）

- [x] T1. 全部改动跑 Ren'Py 解析验证：`translate --empty chinese_simplified` 可执行
- [x] T2. 新增 `__()` 字符串走提取 → 翻译 → 导入流程（renpy-i18n-translate skill，模型翻译）
- [ ] T3. 分 Mod 提交：庭院一个 commit，拍卖行一个 commit（中文提交信息）

## 不做的（本次范围外）

- 不改租金 / 费率 / 衰减等数值公式
- 不重构 Mod 注册与场景化架构（架构本身健康）
- 不引入新的图片/音频素材
- 不兼容旧存档（用户已确认）；但新字段仍走 FIELD_DEFAULTS 兜底，属于顺手健壮性
