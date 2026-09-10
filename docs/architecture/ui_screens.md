# UI 屏幕架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/ui/screens.rpy`（620 行，原 8,886 行）、`game/core/ui/screens/`（16 个文件，共 9,240 行）
> **Phase**: Phase 2/3（屏幕按域提取）

---

## 1. 系统职责

BK 的所有游戏内屏幕（screen）按业务域从单体 `screens.rpy` 提取到 `ui/screens/` 下的独立文件。提取后：

- `screens.rpy` 只保留**图片声明**（`image` 语句，约 11 行起）、**自定义样式**（`init:` 块内的 style，约 133 行起）、**transform**（约 180 行起）和 **5 个 label**；**不含任何 screen**（`^screen ` 计数为 0）。
- `ui/screens/` 承载全部约 90+ 个 screen 定义，按域拆为 15 个 `screen_*.rpy` + 1 个 `__init__.rpy`。
- 原文件中每个提取区块留有迁移注释（如 screens.rpy:325-343），标注去向文件与 Phase，可作索引使用。

## 2. screens.rpy 剩余内容（620 行）

| 类别 | 位置 | 内容 |
|------|------|------|
| 图片声明 | 11-63 行附近 | UI 图标（`img_AP`、`img_gold`、`filter_*` 等）、缩略图按钮（`tb_*`）、背景图 |
| 自定义样式 | 133 行 `init:` 块 | 提取后保留的全局 style 定义 |
| Transforms | 180 行起 | 通用 transform（含 Dexell 更新版） |
| Labels | 474 / 497 / 536 / 547 / 566 行 | `girlpack_menu`、`girlpack_menu_restart`、`pic_test`、`farm_pic_test`、`packstates_menu` —— 女孩包管理与图片测试流程入口 |

## 3. `ui/screens/` 文件清单（16 个文件）

每个文件的 screen 列表经逐文件 grep 核实：

| 文件 | 行数 | Screen 列表 |
|------|-----:|------------|
| `__init__.rpy` | — | 包说明注释 |
| `screen_common.rpy` | — | 见第 4 节（共享屏幕） |
| `screen_brothel.rpy` | — | `brothel`、`furniture` |
| `screen_districts.rpy` | — | `districts`、`district_button`、`visit_district`、`visit_location`、`matchmaking`、`customer_satisfaction` |
| `screen_farm.rpy` | — | `farm_menu`、`farm_tab`、`minion_button`、`fshow_init` |
| `screen_girl_list.rpy` | — | `girls` |
| `screen_girl_log.rpy` | — | `girl_log`、`previous_night_log` |
| `screen_girl_profile.rpy` | — | `girl_profile` |
| `screen_girl_stats.rpy` | — | `stat_bar`、`custom_bar`、`girl_stats`、`assign_job`、`girl_stats_light`、`trait_details`、`perk_details` |
| `screen_home.rpy` | — | `home`、`brothel_report` |
| `screen_misc.rpy` | — | `tax_tooltip`、`tax_tab`、`adv_tooltip`、`girls`、`girl_tab`、`girl_pick_badge`、`badge_button`、`girl_button`、`girl_fast_actions`、`button_overlay`、`rank_level_details` |
| `screen_misc2.rpy` | — | `suzume_hints`、`restock_button`、`inventory_filter`、`girl_select`、`main_character`、`personality_screen`、`notebook`、`fshow_screen`、`farm_show_gold`、`generic_event_screen`、`mood_details`、`love_button`、`fear_button`、`sex_details` |
| `screen_powers.rpy` | — | `mojo_bar`、`power_detail`、`power_draw`、`power_hand`、`power_card`、`power_card_content`、`power_target`、`girl_vp_selector`、`mojo_payment`、`mojo_trade`、`micro_transac`、`brothel_ranking`、`scroll_list`、`brothel_ranking_button`、`harem_button` |
| `screen_progress.rpy` | — | `autorest`、`level`、`perks` |
| `screen_quest.rpy` | — | `active_spells`、`spellbook`、`postings`、`challenge_menu`、`challenge`、`letter`、`modal`、`invisible_button`、`mods`、`free_girl_interact`、`girl_interact`、`free_girl_stats`、`debug_pics`、`girl_mix`、`pic_tester` |
| `screen_resources.rpy` | — | `resource_tab`、`resource_gain`、`resource_exchange`、`achievement_notification`、`crystal_display`、`achievements`、`contracts`、`contract_tab`、`pick_girl`、`contract_result`、`increment_counter`、`increment_display`、`auction_brothel`、`goal_ttip` |
| `screen_schedule.rpy` | — | `schedule`、`save_schedule`、`load_schedule` |

注：上表只列 `screen` 语句；各文件还含配套 python 工具函数与样式。

## 4. 共享屏幕：screen_common.rpy

跨域复用的基础屏幕，其他 screen 文件直接 `use` 或 `call screen` 引用：

`tool`、`overlay`、`quick_start`、`dark_filter`、`yes_no`、`OK_screen`、`show_img`、`show_event`、`show_sex_event`、`shortcuts`、`close`、`receive_item`

提取规则之一即"被 3 个以上域引用的通用控件进 `screen_common.rpy`"。

## 5. 提取规则

1. **按业务域聚类**：同一功能域的 screen 及其私有 python 工具函数整体搬迁，保持文件内聚（如 schedule 三件套、powers 十五件套）。
2. **共享下沉**：跨域控件进 `screen_common.rpy`；全局样式/图片/transform 留在 `screens.rpy`。
3. **留注释索引**：原位置插入 `## EXTRACTED to ui/screens/xxx.rpy (Phase N)##` 注释，便于追溯。
4. **不改调用点**：Ren'Py screen 按名字解析，`call screen xxx` / `use xxx` 无需因文件搬迁而修改。
5. **与组件化协同**：`girl_profile`（Phase 3.1）等屏幕提取与 Girl 组件化同一批工程推进。

## 6. UI 层其他文件（边界说明）

- `game/core/ui/main.rpy` — 主交互循环（含 girl_sold 钩子等调用点）。
- `game/core/ui/notify.rpy`、`content_menu.rpy`、`screen_home.rpy`（ui/ 根下另有一份）— 通知与内容菜单。
- `game/core/config/screens.rpy` — Ren'Py 引擎级屏幕（say/choice/nvl/file 等），与游戏屏幕分层，未参与本次提取。

---

## 相关文档

- [girl_components.md](girl_components.md) — Girl 组件化（同期工程）
- [mod_system.md](mod_system.md) — v2 Mod 的 `home_rightmenu_add_buttons` 指向本层 screen
- [editor_suite.md](editor_suite.md) — 屏幕相关的女孩包/剧本编辑器
