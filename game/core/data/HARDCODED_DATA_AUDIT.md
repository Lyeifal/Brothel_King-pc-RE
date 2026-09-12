# BK Evolution — 硬编码数据迁移审计表

> 生成时间: 2026-06-08
> 范围: `game/core/` 及子目录下的 `.rpy` 文件

---

## 图例

| 状态 | 含义 |
|------|------|
| ✅ JSON 已迁移 | JSON 文件 + DataLoader 方法已存在，`.rpy` 中保留 fallback |
| 🚧 部分迁移 | 同类数据部分在 JSON，部分仍硬编码 |
| ❌ 纯硬编码 | 无任何 JSON 对应，完全内联在 `.rpy` 中 |
| ⚠️ 不建议迁移 | 运行时对象实例、UI 布局常量等，不适合 JSON 化 |

---

## 一、已完全 JSON 化（代码仅存 fallback）

| # | 变量名 | 文件 | JSON 文件 | 说明 |
|---|--------|------|-----------|------|
| 1 | `diff_dict` / `diff_settings_range` / `diff_list` | `init/variables.rpy` | `data/difficulty/difficulty.json` | 5 档难度预设 + 自定义滑块范围 |
| 2 | `preference_modifier` / `base_reluctance` / `preference_limit` / `experienced_modifiers` / `experienced_color` / `sexual_training_value` | `init/variables.rpy` | `data/settings/sex_training_params.json` | 性行为训练参数全家桶 |
| 3 | `all_jobs` / `all_sex_acts` / `extended_sex_acts` / `farm_hardcore_acts` / `opposite_sex_acts` / `normal_tags` / `all_farm_tags` / `job_color` | `init/variables.rpy` | `data/settings/job_params.json` | 工作/性行为标签定义 |
| 4 | `brothel_pics` / `bro_cost` / `bro_capacity` / `bro_helpers` / `bro_reputation_cap` | `init/settings.rpy` | `data/economy/brothel_params.json` | 青楼参数 |
| 5 | `farm_pics` / `all_minion_types` / `minion_description` / `minion_xp_to_level` / `minion_price` | `init/variables.rpy` | `data/farm/minions.json` | 农场仆从参数 |
| 6 | `farm_perform_dict` (pref_bonus, naked_stats, service_stats 等) | `init/variables.rpy` | `data/farm/farm_perform_dict.json` | 农场表演文本字典 |
| 7 | `advertising_pics` / `pony_pics` / `security_pics` / `arson_pics` / `violent_pics` / `treasure_pics` / `no_girls_pics` | `init/settings.rpy` | `data/settings/picture_mappings.json` | 事件/UI 图片映射 |
| 8 | `stat_increase_dict` | `init/variables.rpy` | `data/settings/stat_increase_dict.json` | 属性增长提示文本 |
| 9 | `ev_gallery_list` | (原 BKsettings.rpy) | `data/settings/ev_gallery_list.json` | 画廊事件列表 |
| 10 | `UI_elements_colors` | (原 BKsettings.rpy) | `data/settings/ui_element_colors.json` | UI 元素颜色 |
| 11 | `loandict` | (原 BKsettings.rpy) | `data/settings/loans.json` | 贷款参数 |
| 12 | `s_des` | `framework/economy.rpy` | `data/settings/sex_act_descriptions.json` | 性行为描述短语 |
| 13 | `rank_lookup_dict` | `framework/economy.rpy` | `data/settings/rank_lookup.json` | 等级查询 |
| 14 | `god_dict` / `name_map` / `all_qualities` | (原 BKsettings.rpy) | `data/settings/entity_lookups.json` | 神祇/名字/品质查询 |
| 15 | 妓院名池 (first/second/third/fourth/names) | (原 BKsettings.rpy) | `data/settings/brothel_name_pools.json` | ~160 词 |
| 16 | `opposed_chance_table` | `framework/economy.rpy` | `data/settings/opposed_chance_table.json` | MC 对抗挑战概率 |
| 17 | `quest_templates` / `class_templates` | `systems/postings.rpy` | `data/settings/quest_templates.json` | 26 条任务/课程模板 |
| 18 | `item_type_by_name` / `all_equipement_types` / `furniture_types` | `framework/economy.rpy` | `data/settings/item_type_params.json` | 物品类型映射 |
| 19 | `_wd_dict` / `base_value` / `step` | `framework/girlclass.rpy` | `data/settings/girl_upkeep_params.json` | 女孩维护阈值/工作日映射 |
| 20 | `CUSTOMER_COLOR_TIERS` | `framework/customer.rpy` | `data/settings/customer_affixes.json` | 顾客颜色等级 |
| 21 | `upgrade_cost` (庭院) | `systems/courtyard/courtyard.rpy` | `data/settings/courtyard_upgrade_costs.json` | 3 设施升级费用 |
| 22 | `limit` (自由女孩) | `content/interactions_free.rpy` | `data/settings/free_girl_limits.json` | 6 档关系等级好感上限 |
| 23 | `diff` (性行为训练基准) | `content/interactions.rpy` | `data/settings/training_difficulty.json` | 7 性行为基准难度 |
| 24 | cumshot 标签排除 | `content/interactions.rpy` | `data/settings/training_tag_exclusions.json` | 训练步骤标签排除规则 |
| 25 | `house_templates` | `systems/minigame.rpy` | `data/settings/minigame_templates.json` | 忍者追捕小游戏 8 房屋模板 |
| 26 | traits | `init/variables.rpy` | `data/traits/traits.json` | 130+ 特质定义 |
| 27 | perks | `init/variables.rpy` | `data/perks/perks.json` | 50+ 天赋定义 |
| 28 | origins (PlayerOrigin) | `init/variables.rpy` | `data/sandbox/origins.json` | 玩家出身 |
| 29 | story events | `init/variables.rpy` | `data/story_events/story_events.json` | 剧情事件 |
| 30 | achievements | `init/variables.rpy` | `data/achievements/achievements.json` | 成就 |
| 31 | challenges | `init/variables.rpy` | `data/challenges/challenges.json` | MC 挑战 |
| 32 | resources | `init/start.rpy` | `data/resources/resources.json` | 资源定义 |
| 33 | contracts | `init/start.rpy` | `data/contracts/contracts.json` | 契约模板 |
| 34 | cleanliness_penalties | `init/variables.rpy` | `data/settings/cleanliness_penalties.json` | 清洁惩罚 |
| 35 | treasure_thresholds | `init/variables.rpy` | `data/settings/treasure_thresholds.json` | 宝藏阈值 |
| 36 | chapter_goals | `init/variables.rpy` | `data/chapter_goals.json` | 章节目标 |
| 37 | MC descriptions | `init/variables.rpy` | `data/settings/mc_descriptions.json` | MC 描述文本 |
| 38 | girl descriptions | `init/variables.rpy` | `data/settings/girl_descriptions.json` | 女孩描述文本 |
| 39 | dialogue texts | `init/variables.rpy` | `data/settings/dialogue_texts.json` | 对话文本 |
| 40 | event texts | `init/variables.rpy` | `data/settings/event_texts.json` | 事件文本 |
| 41 | help texts | `init/variables.rpy` | `data/settings/help_texts.json` | 帮助文本 |
| 42 | gossip | `init/variables.rpy` | `data/settings/gossip.json` | 八卦文本 |
| 43 | small texts | `init/variables.rpy` | `data/settings/small_texts.json` | 小文本 |
| 44 | power_ui | `init/variables.rpy` | `data/settings/power_ui.json` | 权力 UI 文本 |
| 45 | unlock params | `init/variables.rpy` | `data/settings/unlock_params.json` | 解锁参数 |
| 46 | recent events | `init/variables.rpy` | `data/settings/recent_events.json` | 近期事件文本 |
| 47 | inventory sorters | `init/variables.rpy` | `data/settings/inventory_sorters.json` | 库存排序器 |
| 48 | rankings | `init/variables.rpy` | `data/settings/rankings.json` | 排名文本 |
| 49 | xp rank params | `init/variables.rpy` | `data/settings/xp_rank_params.json` | XP 等级参数 |
| 50 | security events | `init/variables.rpy` | `data/settings/security_events.json` | 安全事件 |
| 51 | security scaling | `init/variables.rpy` | `data/settings/security_scaling.json` | 安全缩放 |
| 52 | threat params | `init/variables.rpy` | `data/settings/threat_params.json` | 威胁参数 |
| 53 | quality | `init/variables.rpy` | ~~`data/settings/quality.json`~~ → **Mod 化** | 品质定义。2026-09-13：JSON 已删除，数据迁出 core 至 `custom/mods/Item Quality/quality.json`；core 保留 `data/quality.rpy` 硬编码 fallback（**勿删**）+ `systems/registry/quality_registry.rpy` 框架 |
| 54 | girl background pools | `init/variables.rpy` | `data/settings/girl_background_pools.json` | 女孩背景池 |
| 55 | sex descriptions | `init/variables.rpy` | `data/settings/sex_descriptions.json` | 性行为描述 |
| 56 | sex training params | `init/variables.rpy` | `data/settings/sex_training_params.json` | 性训练参数 |
| 57 | training tests | `init/variables.rpy` | `data/settings/training_tests.json` | 训练测试 |
| 58 | contract params | `init/variables.rpy` | `data/settings/contract_params.json` | 契约参数 |
| 59 | customer params | `init/variables.rpy` | `data/settings/customer_params.json` | 顾客参数 |
| 60 | economy modifiers | `init/variables.rpy` | `data/settings/economy_modifiers.json` | 经济修改器 |
| 61 | game constants | `init/variables.rpy` | `data/settings/game_constants.json` | 游戏常量 |
| 62 | archetype data | `init/variables.rpy` | `data/settings/archetype_data.json` | 原型数据 |
| 63 | audio registry | `init/variables.rpy` | `data/settings/audio_registry.json` | 音频注册 |
| 64 | merchants | `init/variables.rpy` | `data/settings/merchants.json` | 商人配置 |
| 65 | tags | `init/variables.rpy` | `data/settings/tags.json` | 标签定义 |
| 66 | location tooltips | `init/variables.rpy` | `data/settings/location_tooltips.json` | 地点工具提示 |
| 67 | personality gift params | `init/variables.rpy` | `data/settings/personality_gift_params.json` | 个性礼物参数 |
| 68 | quest prices | `init/variables.rpy` | `data/settings/quest_prices.json` | 任务价格 |
| 69 | roll results | `init/variables.rpy` | `data/settings/roll_results.json` | 掷骰结果 |
| 70 | tracked achievements | `init/variables.rpy` | `data/settings/tracked_achievements.json` | 追踪成就 |

**已迁移总计: 70 项**

---

## 二、尚未迁移（纯硬编码）

### 2.1 农场系统

| # | 变量名 | 文件 | 行号 | 条目数 | 说明 | 迁移优先级 |
|---|--------|------|------|--------|------|-----------|
| 1 | `farm_description` | `init/variables.rpy` | 628 | 51 | 农场事件文本大字典（intro/good/average/bad/pen/holding 等） | ✅ **已完成** — `data/farm/farm_descriptions.json` |
| 2 | `farm_holding_dict` | `init/variables.rpy` | 609 | 5 | 农场持有类型 → 显示名称 | ✅ **已完成** — `data/settings/farm_holding_params.json` |
| 3 | `farm_ttip` | `init/variables.rpy` | 617 | 9 | 农场模式工具提示 | ✅ **已完成** — `data/settings/farm_holding_params.json` |
| 4 | `farm_holding_stats` | `init/variables.rpy` | 706 | 4 | 持有属性 → (主行为, 次行为) | ✅ **已完成** — `data/settings/farm_holding_params.json` |
| 5 | `farm_holding_tags` | `init/variables.rpy` | 708 | 4 | 持有属性 → 图片标签 | ✅ **已完成** — `data/settings/farm_holding_params.json` |
| 6 | `minion_adjectives` | `init/variables.rpy` | 710 | ~32 | 仆从类型 → 形容词列表 | ✅ **已完成** — `data/settings/minion_params.json` |
| 7 | `minion_name_dict` | `init/variables.rpy` | 717 | ~20 | 仆从/怪物名字生成音节池 | ✅ **已完成** — `data/settings/minion_params.json` |
| 8 | `farm_installations` | `init/start.rpy` | 545 | 4 | `Installation` 对象实例（stables/pig stall/monster den/workshop） | 🟢 低（含对象实例，JSON 化需反序列化） |

### 2.2 商店系统

| # | 变量名 | 文件 | 行号 | 条目数 | 说明 | 迁移优先级 |
|---|--------|------|------|--------|------|-----------|
| 9 | `shop_item_number` | `init/settings.rpy` | 251 | ~8 | 商店物品生成骰子公式 | ✅ **已完成** — `data/settings/shop_params.json` |
| 10 | `shop_chapter_modifiers` | `init/settings.rpy` | 259 | 42 | 章节 → 物品类型库存修正 | ✅ **已完成** — `data/settings/shop_params.json` |
| 11 | `shop_restock_cost` | `init/settings.rpy` | 270 | 18 | 商店类型×章节 → 重进货金币成本 | ✅ **已完成** — `data/settings/shop_params.json` |
| 12 | `shop_upgrades` | `init/settings.rpy` | 277 | 10 | 升级序号 → [章节, 资源成本, 额外库存] | ✅ **已完成** — `data/settings/shop_params.json` |
| 13 | `shop_chapter_price_multiplier` | `init/settings.rpy` | 297 | 7 | 章节 → 价格倍数 | ✅ **已完成** — `data/settings/shop_params.json` |
| 14 | `shop_chapter_stock_bonus` | `init/settings.rpy` | 298 | 7 | 章节 → 库存加成 | ✅ **已完成** — `data/settings/shop_params.json` |
| 15 | `shop_time_pressure_settings` | `init/settings.rpy` | 299 | 4 | 时间压力参数（价格增长/库存衰减） | ✅ **已完成** — `data/settings/shop_params.json` |

### 2.3 名字/文本生成

| # | 变量名 | 文件 | 行号 | 条目数 | 说明 | 迁移优先级 |
|---|--------|------|------|--------|------|-----------|
| 16 | `girl_name_dict` | `init/variables.rpy` | 724 | ~100+ | 随机女孩名字音节/填充/结尾池 | ✅ **已完成** — `data/settings/girl_name_pools.json` |
| 17 | `origins` (女孩出生地) | `init/variables.rpy` | 1530 | 9 | 女孩出生地地名列表 | 🟢 低（简短列表） |
| 18 | `random_tips` | `init/variables.rpy` | 284 | 99 | 加载画面提示文本 | ✅ **已完成** — `data/settings/loading_tips.json` |

### 2.4 颜色/UI 映射

| # | 变量名 | 文件 | 行号 | 条目数 | 说明 | 迁移优先级 |
|---|--------|------|------|--------|------|-----------|
| 19 | `color_dict` | `init/variables.rpy` | 2294 | 35 | 事件颜色键 → 颜色常量映射 | ✅ **已完成** — `data/settings/event_colors.json` |
| 20 | `result_colors` | `init/variables.rpy` | 1563 | 6 | 掷骰结果 → 颜色常量 | 🟢 低 |
| 21 | `result_star_dict` | `init/variables.rpy` | 1564 | 6 | 掷骰结果 → 星级图片字符串 | 🟢 低 |
| 22 | `mojo_act_dict` | `init/variables.rpy` | 736 | 10 | 行为 → mojo 颜色元组 | 🟢 低 |
| 23 | `stat_name_dict` | `data/settings.rpy` | 47 | 13 | 属性名 → 翻译显示名 | 🟢 低 |
| 24 | `brothel_images` | `init/variables.rpy` | 446 | 7 | 章节 → `renpy.image()` 调用 | ⚠️ 不建议（含运行时 API 调用） |
| 25 | `but_sizes` | `content/declarations.rpy` | 1738 | 6 | 画廊按钮数量 → (宽, 高) | 🟢 低 |
| 26 | `room_pics` | `init/settings.rpy` | 315 | ~22 | 房间类型 → 图片文件名 | 🟢 低 |

### 2.5 对象/杂项

| # | 变量名 | 文件 | 行号 | 条目数 | 说明 | 迁移优先级 |
|---|--------|------|------|--------|------|-----------|
| 27 | `extractor_items` | `systems/items.rpy` | 400 | 2 | `Item` 对象实例（Extractor Mk I/II） | ⚠️ 不建议（含对象实例） |
| 28 | `npc_names` | `custom/mods/Auction House/auction.rpy` | 179 | 6 | 拍卖 NPC 名字列表（拍卖系统已提取为 Mod） | 🟢 低 |
| 29 | `_sound_map` | `systems/postings.rpy` | 9 | 5 | 声音名 → 声音变量映射 | 🟢 低 |

### 2.6 训练系统（diff 扩展）

| # | 变量名 | 文件 | 行号 | 条目数 | 说明 | 迁移优先级 |
|---|--------|------|------|--------|------|-----------|
| 30 | obedience diff | `content/interactions.rpy` | 1581 | 4 | very dom=7, dom=6, very sub=4, sub=5 | ✅ **已完成** — 并入 `data/settings/training_difficulty.json` |
| 31 | constitution diff | `content/interactions.rpy` | 1647 | 4 | very introvert=7, introvert=6, very extravert=4, extravert=5 | ✅ **已完成** — 并入 `data/settings/training_difficulty.json` |
| 32 | hypnosis diff | `content/interactions.rpy` | 2364 | 11 | obedience/libido/sensitivity=2, naked=4, service=5, sex=6, anal=7, fetish=8, bisexual=9, group=10 | ✅ **已完成** — 并入 `data/settings/training_difficulty.json` |

---

## 三、统计

| 类别 | 数量 |
|------|------|
| 已完全 JSON 化 | 90 项 |
| 尚未迁移 | 9 项（低优先级） |
| 不建议迁移 | 2 项 (`brothel_images`, `extractor_items`) |

**实际剩余可迁移: 9 项（均为低优先级小数据集）**

---

## 四、推荐下一批次（按优先级排序）

### 🔴 高优先级（文本量大，改动机高）
1. ~~`farm_description` — ✅ 已完成~~

### 🟡 中优先级（配置/平衡数据，可并包）
2. ~~商店全家桶 — ✅ 已完成~~
3. ~~仆从生成参数 — ✅ 已完成~~
4. ~~`girl_name_dict` — ✅ 已完成~~
5. ~~农场持有参数 — ✅ 已完成~~
6. ~~`color_dict` — ✅ 已完成~~
7. ~~`random_tips` — ✅ 已完成~~
8. ~~训练难度扩展 — ✅ 已完成~~

### 🟢 低优先级（条目少或改动频率低）
9. `stat_name_dict` — 属性名称映射（13 条）
10. `result_colors` + `result_star_dict` — 掷骰结果 UI（12 条）
11. `mojo_act_dict` — mojo 颜色映射（10 条）
12. `room_pics` — 房间图片映射（22 条）
13. `origins` — 女孩出生地（9 条）
14. `npc_names` — 拍卖 NPC 名字（6 条）
15. `_sound_map` — 声音映射（5 条）
16. `but_sizes` — 画廊按钮尺寸（6 条）
17. `farm_installations` — 农场设施对象（4 条，含对象实例）
