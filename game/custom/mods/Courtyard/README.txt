庭院 Mod — 说明 | Courtyard Mod — README
=====================================================

本 Mod 通过 Mod API v2 注册，mod_id 为 "courtyard"。安装即常驻激活；
卸载 = 删除本目录。

 v2.0 场景化改造（租金/衰减/房间上限/终局扩建）| v2.0 overhaul
---------------------------------------------------------------------

场景 | Scene
------------
- 入口：主页右侧菜单 Courtyard 按钮 action = Call("courtyard_scene")
  （label 驱动）。
- 背景用游戏现有素材：bg mansion inside（宅邸内景，declarations.rpy
  已声明）；管家为 Sill（show sill happy at right，游戏自带立绘）。
- 开场 flavor 对话汇报当前女孩数/房间上限/今晚租金；
  抵达最终区域且未扩建时，Sill 会插入扩建地契报价对话。
- courtyard 屏幕为透明背景 + modal True，场景从面板边缘透出；
  按钮一律 Return(("action", ...))，由 courtyard_scene label 统一
  处理状态变更，不使用 Function() action（避免主循环 teleport
  崩溃，与拍卖行 v2.x 同一修复，见 _run 注释）。
- 释放女孩现走 relinquish_girl() 清理（卸下道具、清理名册引用），
  与拍卖售出时相同；此前 remove_girl 会把女孩丢进"三不管"状态。
- 修复顺带发现的旧 bug：_courtyard_destination_accept 里
  notify_list.append(text, col=...) 对纯 list 传两个参数会
  TypeError，已改为 notify(text, col="green")。

租金公式 | Rent formula
------------------------
本体难度为字符串（diff_list），代码按下标 +1 映射为 1-5
（未知值回退 3，与拍卖 Mod 同一做法）：

    人均日租 = 15 × 地区rank × (1 + 0.20 × 难度档)
    总租金   = 人均日租 × 女孩数

- 地区 rank：贫民窟=1，码头/仓库=2，魔法花园/大教堂=3，
  王城=4，无尽模式王城=5（District 定义见 game/core/framework/world.rpy
  与 start.rpy 的 district_dict）。
- 人均日租范围：18（贫民窟·非常简单）~ 150（无尽王城·疯狂）金币。
- 收租顺序（process_day）：心情/能量恢复 → 属性衰减 → 收租。
- 付不起：金币扣到 0 为止；差额部分每个安置女孩额外 -10 心情，
  并 renpy.notify 警告"租金未付清"。
- 维护费（get_daily_upkeep，约为青楼 50%）与租金相互独立，
  两者每日各收一次，屏幕分别显示。

属性衰减 | Stat decay
---------------------
- 每日每个安置女孩：随机 1-2 项技能/属性（主属性 8 项 + 性爱技能
  4 项，见 Courtyard.DECAY_STATS），各失去 ceil(0.5 × 难度档) 点
  （难度 1-5 → 1/1/2/2/3 点）。
- 优先用女孩现有 API change_stat(stat, -amount)（下限 0 由
  Stat.change 内部钳制，不会跌破）；仅有 gain() 时兜底。
- 女孩组件正在并行重构：每个女孩的恢复/衰减/训练均包在
  try/except 中，出错即跳过该女孩，不影响其他人。

房间上限 | Room limit
---------------------
- room_limit()：已购扩建地契 → 99；否则 4 + 地区rank × 2：

    贫民窟 6 | 码头/仓库 8 | 魔法花园/大教堂 10 | 王城 12 | 无尽王城 14

- can_add_girl、屏幕"女孩: n/上限"显示、HOOK_GIRL_DESTINATION_LIST
  注册全部走 room_limit()；地区读取失败回退 rank=1（旧行为 6 间）。
- 旧存档没有 expansion_unlocked 字段 → FIELD_DEFAULTS +
  __getattr__ 兜底为 False（Ren'Py 恢复实例不运行 __init__）。

终局扩建 | Villa expansion deed
---------------------------------
- 判定"最终区域"：当前地区名 = "The King's Hold" 或 rank ≥ 4
  （含无尽模式 rank 5），读取全程防御式。
- 达成且未解锁：场景内 Sill 报价 + 设施面板出现购买按钮，
  价格 10,000,000 金币（Courtyard.EXPANSION_PRICE）。
- 购买 → courtyard_villa.expansion_unlocked = True，
  room_limit() 变为 99。
- "道具"实现说明：游戏物品系统正在并行重构（Item/ItemType/
  item_dict 接口不稳定），为避免深度耦合不做真实背包道具，
  采用"场景购买 + 持久化旗标"；存档经 to_dict/from_dict 与
  FIELD_DEFAULTS 双向兼容。

存档兼容 | Save compatibility
--------------------------------
- 新增字段仅 expansion_unlocked：旧档读缺失 → False；
  新档 to_dict 持久化、from_dict 恢复。
- MAX_CAPACITY 由 50 改为 99（扩建后上限），旧常量语义保留为
  LEGACY_CAPACITY 仅供对照。

文件 | Files
------------
- courtyard.rpy         Courtyard/CourtyardFacility 类：租金、衰减、
                        房间上限、扩建、序列化
- courtyard_scene.rpy   label courtyard_scene：场景 + 动作处理主循环
- screen_courtyard.rpy  透明 courtyard 管理屏幕（call screen 用）
- mod.rpy               Mod API v2 注册 + 右侧菜单按钮 + 日结钩子
- tl/                   中文翻译（strings 由翻译工具链维护；
                        新增示例条目见各文件"TODO: Translation updated"）
