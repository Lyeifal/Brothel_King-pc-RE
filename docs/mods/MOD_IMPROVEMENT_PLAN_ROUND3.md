# 第三轮完善方案：拍卖行可读性、Mod 管理页、移除剧本模式、出身独立 Mod

## R1. 拍卖行黄色背景（auction_screens.rpy）

- 三个面板 frame 背景 `c_ui_dark` → `c_ui_light`（#FFECBF 浅黄，游戏任务/日结界面同款）
- 同步反转文字颜色（浅底深字）：
  - `#FFFFFF` → `#3B2F20`，`#FFD700` → `#9A6A00`，`#BBBBBB` → `#6B5B45`，
    `#888888` → `#7A6A52`，`#AAAAAA` → `#8A7A62`，`#4ECDC4` → `#1F7A72`，
    `#E74C3C` → `#B03A2E`，`#2ECC71` → `#1E8449`，`#FFAAAA` → `#B03A2E`
- 拍卖提交屏（auction_submit）按钮保持深底白字不动；女孩悬浮提示保持深底不动

## R2+R3. Mod 管理页：黑背景修复 + 黄色底 + 绿色对勾（screen_mod_manager.rpy）

- 黑背景根因：全屏 `Solid(#000000B3)` 压暗层叠在暗色主题图上≈纯黑
- 改为：屏内直接 `add gui.main_menu_background` + 轻度压暗 `#00000040`，
  不依赖主菜单屏幕是否在场
- 外框与每行 frame 背景 → `c_ui_light` 黄底，文字转深色（同 R1 色板）
- 已启用 Mod 名字后追加绿色 "✓"（#1E8449）；常驻 Mod 也打勾

## R4. Mod 管理页：确定/返回，确定才生效

- 屏内 `default pending = {}`：切换只改 pending 并打"有未应用更改"标记
- 底部「确定」：批量 `set_mod_enabled` + `save_persistent`，显示重启提示
- 底部「返回」/右键：丢弃 pending 直接 Return()
- 依赖连锁：禁用一个 Mod 时其依赖者也在 pending 里联动禁用（提示缺前置）

## R5. 移除开局剧本模式

- Game Modes mod：注销 ScenarioMode 注册；删除 scenario_mode.rpy 及 tl
- 删除 screen_gamemode.rpy 的 scenario_select 屏幕与 start.rpy 的
  select_scenario label 及调用分支
- data_loader：移除 load_scenarios（含 core 数据文件如存在）
- 更新 Game Modes README 与 manifest（description/requires）

## R6. 出身独立 Mod：独特职业 + 技能树（新 Origins mod）

结构：`game/custom/mods/Origins/`
- `mod.rpy`：注册 origins（Mod API v2，可被禁用）
- `origins.rpy`：OriginTalent/PlayerOrigin/OriginRegistry（自 Game Modes 迁入），
  PlayerOrigin 新增 class_id；懒注入 `origins_ensure_classes()` 把出身职业
  注册进 store.all_player_classes / store.spellbook（Hook：猴子补丁
  Main.update_spells，幂等，init_spells 之后生效）
- `screen_origin.rpy`：origin_select 屏幕（自 Game Modes 迁入，详情区加
  职业名与技能数量预览）
- `data/origins.json`：5 出身，各含 class_id、天赋、起始奖励、法术书（技能树）

核心配套改动：
- core_entities.reset_stats：改用 `MC_CLASS_STAT_DEFS` 注册表（核心三职业
  为默认值，Mod 可追加），未知职业回退 (1,1,1,2)
- spells.rpy get_available_player_classes：选了出身 → 只返回该出身的职业
- start.rpy：select_origin 对剧情/沙盒两种模式都调用（origins mod 在场时），
  选中出身存入 store._selected_origin；移除 SandboxMode.set_origin 耦合
- intro.rpy：有出身时跳过职业三选一菜单，直接 set_playerclass(出身职业) +
  一句通用叙述；信仰菜单原样保留；随后 apply_to_mc（天赋+奖励）
- start_no_intro 路径：同样套用出身（class + apply_to_mc，一次性标记防重）
- data_loader：移除 load_origins；core 的 data/sandbox/origins.json 迁入 Mod
- Game Modes mod：SandboxMode 移除出身字段与 on_game_start 应用逻辑

五个出身 → 五个独特职业（技能树 = 各职业专属法术书，随 MC 等级自动领悟，
法术书界面 K 键查看，无需新 UI）：
| 出身 | 职业 | 定位 |
|---|---|---|
| 落魄贵族 | Aristocrat 贵族 | 魅力/声望 |
| 街头混混 | Enforcer 打手 | 力量/治安 |
| 商人世家 | Magnate 豪商 | 交易/金钱 |
| 流浪法师 | Sorcerer 咒术师 | 精神/光环 |
| 海盗船长 | Reaver 掠夺者 | 掳人/混合 |

法术效果全部复用现有 Effect 目标（gain strength/spirit/charisma、boost
buy/sell、brothel scope 的 change/boost、special defender 等），法术图标
复用现有资源。

## 收尾

- T1 translate --empty 解析验证
- T2 新串模型直译导入 + count/placeholders/lint/json 审计
- T3 分 commit：拍卖行背景 / mod 管理页 / 移除剧本 / 出身 mod + 核心配套

## 完成记录（2026-09-25）

- [x] R1 拍卖行主屏面板换浅黄背景（auction_house 屏内 c_ui_dark→c_ui_light +
      深色系颜色映射；提交/女孩提示浮层保持深底）
- [x] R2 mod 管理页修复黑背景：屏内直接 add gui.main_menu_background +
      40% 黑色轻压暗（原 70% 重压暗叠暗色主题图≈纯黑）
- [x] R3 已启用 Mod 名字后显示绿色「✓」
- [x] R4 「确定 / 返回」机制：切换只写 pending 并标注「(未应用)」，
      点确定才调用 apply_pending_changes 批量生效并保存 persistent；
      mod_api_v2 新增 apply_pending_changes()
- [x] R5 移除开局剧本模式：Game Modes 注销 ScenarioMode、删除
      scenario_mode.rpy / scenarios.json / scenario.schema.json /
      scenario_template.rpy 及对应 tl；start.rpy 删 select_scenario 分支；
      data_loader 删 load_scenarios；mod_api 删 register_scenario
- [x] R6 出身独立成 Origins Mod：5 出身 → 5 独特职业（Aristocrat / Enforcer /
      Magnate / Sorcerer / Reaver），各带专属法术书；核心配套：
      MC_CLASS_STAT_DEFS 注册表、reset_stats 查表、出身选择对
      剧情/沙盒双模式生效、信仰系统沿用原菜单不动

收尾：

- [x] T1 translate --empty 解析验证通过（EXIT=0）
- [x] T2 新增串模型直译导入：applied 78 条；--count 0 missing；
      placeholders 审计仅历史 contexttext 1 条；json 审计 3511/3511
- [x] T3 分 commit 提交（见 git log）
