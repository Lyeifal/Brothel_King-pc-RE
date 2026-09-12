# BK Evolution — 数据驱动化迁移记录

> 最后更新: 2026-09-11（与代码核对）
>
> **状态：迁移已收官 ✅（原计划核心 12 域及全部追加域均已完成 JSON 化），fallback 保留中。**
> **本文档为历史记录 + 当前数据清单**，不再追踪新任务；剩余清单中未标 ✅ 的条目均为有意保留（运行时动态数据、硬编码 fallback 或低价值内联映射）。
>
> 创建日期：2026-06-08
> 原当前阶段：Phase 7.5（硬编码全面排查）— 已完成
>
> ## 迁移后架构速查（2026-09-11 与代码核对）
>
> | 层 | 位置 | 说明 |
> |----|------|------|
> | 权威数据 | `game/core/data/<域>/*.json` | 共 36 个子目录（含 `_schemas/`），加载点见 `DataLoader`（`game/core/systems/data_loader.rpy`） |
> | Schema 校验 | `game/core/data/_schemas/*.schema.json` | 每域一份 JSON Schema |
> | 加载器 | `game/core/systems/data_loader.rpy` | 全部 `load_*()` 类方法，JSON 优先 |
> | 注册表 | `game/core/systems/registry/` | `registry.rpy` 基类 + trait/perk/tag/dialogue/event/meta/ngp/unlock/quality 十个 Registry |
> | 硬编码 fallback | `game/core/data/*.rpy`（`items.rpy`、`jobs.rpy`、`perks.rpy`、`powers.rpy`、`settings.rpy`、`spells.rpy`、`quality.rpy`）及各 .rpy 内 `_fallback_*` | JSON 缺失时保证游戏可启动；**勿删**。`quality.rpy` 的权威数据已迁出 core，见下方 #12 与附录 |
> | 数据导出 | `game/core/systems/data_exporter.rpy` | 与 DataLoader 对称的 `export_*()` |
> | 可视化编辑 | `tools/bk_editor/` | 编辑器套件，映射见 `tools/bk_editor/README.md` |
>
> ⚠️ 唯一与原计划的偏差：总览表 #14「图片/音频列表」的目标路径 `data/assets/*.json` **未采用**——该内容实际拆入 `settings/audio_registry.json`（音频注册表）与 `settings/picture_mappings.json`（图片映射），`data/assets/` 目录不存在。

---

## 迁移原则

1. **JSON 为主，.rpy fallback** — 新增 JSON 作为首选数据源，保留 `.rpy` 硬编码作为回退
2. **Schema 先行** — 每个 JSON 必须先有 `.schema.json` 定义结构
3. **DataLoader 统一加载** — 所有 JSON 通过 `DataLoader.load_*()` 方法加载
4. **`from_dict()` 反序列化** — 每个类必须有 `from_dict()` 类方法
5. **清除脚本后测试** — 每次迁移后运行 `tools/clean_runtime.ps1` 并实际游玩验证

---

## 总览进度

> i18n 状态：🌐 已完成 | ⏳ 待处理 | ⚠️ 不适用（标识符/图片路径/key）

| 序号 | 领域 | 优先级 | 源文件 | 目标 JSON | 迁移状态 | i18n 状态 | 完成日期 |
|------|------|--------|--------|-----------|----------|-----------|----------|
| 1 | 物品系统 | ⭐⭐⭐ | `data/items.rpy` | `data/items/items.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-10 |
| 2 | 工作/表演 | ⭐⭐⭐ | `data/jobs.rpy` | `data/jobs/perform_job_dict.json` | ✅ 已完成 | ⚠️ 不适用（纯数据结构） | 2026-06-08 |
| 3 | 青楼参数 | ⭐⭐⭐ | `init/settings.rpy` | `data/economy/brothel_params.json` | ✅ 已完成 | ⚠️ 不适用 | 2026-06-08 |
| 4 | 商店系统（阶段1-4） | ⭐⭐⭐ | `init/settings.rpy` + `core_entities.rpy` + `economy.rpy` | `data/shops/*.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| 5 | 税收系统 | ⭐⭐⭐ | `init/settings.rpy` | `data/economy/tax_params.json` | ✅ 已完成 | ⚠️ 不适用 | 2026-06-08 |
| 6 | Minion | ⭐⭐ | `init/variables.rpy` | `data/minions/minions.json` | ✅ 已完成 | 🌐 已完成（值级） | 2026-06-08 |
| 7 | 农场安装 | ⭐⭐ | `init/variables.rpy` | `data/farm/installations.json` | ✅ 已完成 | ⚠️ 不适用 | 2026-06-08 |
| 8 | 房间/建筑 | ⭐⭐ | `init/variables.rpy` | `data/rooms/rooms.json` | ✅ 已完成 | ⚠️ 不适用 | 2026-06-08 |
| 9 | 力量/法术（Powers） | ⭐⭐ | `data/powers.rpy` | `data/powers/powers.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| 10 | 法术/月相（Spells + Moons） | ⭐⭐ | `data/spells.rpy` | `data/spells/spells.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| 11 | 主角职业/法术书（MC Classes） | ⭐⭐ | `data/spells.rpy` | `data/classes/mc_classes.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| 12 | 难度参数 | ⭐⭐ | `init/settings.rpy` | `data/difficulty/difficulty.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| 13 | 目标系统 UI | ⭐ | `init/variables.rpy` | `data/goals/goal_ui.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| 14 | 图片/音频列表 | ⭐ | `init/settings.rpy` | ~~`data/assets/images.json` + `data/assets/audio.json`~~ → 实际拆入 `settings/picture_mappings.json` + `settings/audio_registry.json` | ✅ 已完成（路径有调整，见头部说明） | 🌐/⚠️ 混合 | 2026-06-08 |
| — | Fixations | ⭐⭐ | `init/variables.rpy` | `data/fixations/fixations.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | 交互菜单树 | ⭐⭐ | `init/variables.rpy` | `data/interactions/*.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | Traits | ⭐⭐ | `data/traits.rpy` | `data/traits/traits.json` | ✅ 已完成 | 🌐 已完成（受限） | 2026-06-08 |
| — | Perks | ⭐⭐ | `data/perks.rpy` | `data/perks/perks.json` | ✅ 已完成 | 🌐 已完成（受限） | 2026-06-08 |
| — | Achievements | ⭐ | `systems/achievements.rpy` | `data/achievements/achievements.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | Challenges | ⭐ | `framework/functions.rpy` | `data/challenges/challenges.json` | ✅ 已完成 | ⚠️ 不适用 | 2026-06-08 |
| — | Contracts | ⭐ | `framework/functions.rpy` | `data/contracts/contracts.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | Resources | ⭐ | `framework/functions.rpy` | `data/resources/resources.json` | ✅ 已完成 | ⚠️ 不适用 | 2026-06-08 |
| — | Customers | ⭐ | `systems/customer/` | `data/customers/customer_affixes.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | Cleanliness | ⭐ | `init/start.rpy` | `data/settings/cleanliness_penalties.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | Treasure | ⭐ | `init/start.rpy` | `data/settings/treasure_thresholds.json` | ✅ 已完成 | ⚠️ 不适用 | 2026-06-08 |
| — | Meta Progression | ⭐ | `systems/registry/` | `data/meta/meta_progression.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | NGP Settings | ⭐ | `systems/registry/` | `data/ngp/ngp_settings.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | Stats | ⭐ | `init/variables.rpy` | `data/stats/stats.json` | ✅ 已完成 | 🌐 已完成（值级） | 2026-06-08 |
| — | Ranks | ⭐ | `init/variables.rpy` | `data/ranks/ranks.json` | ✅ 已完成 | 🌐 已完成（值级） | 2026-06-08 |
| — | Personalities | ⭐ | `init/variables.rpy` | `data/personalities/personalities.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | Origins | ⭐ | `systems/gamemodes/` | `data/sandbox/origins.json` | ✅ 已完成 | 🌐 已完成 | 2026-06-08 |
| — | Scenarios | ⭐ | `systems/gamemodes/` | `data/scenarios/scenarios.json` | ✅ 已完成 | ⚠️ 不适用（空） | 2026-06-08 |

---

## 本次会话新增完成（2026-06-08）

| 领域 | 源文件 | 目标 JSON | 完成日期 | 备注 |
|------|--------|-----------|----------|------|
| 物品系统 | `data/items.rpy` | `data/items/items.json` | 2026-06-08 | 90 template + 103 regular items；`Item.from_dict()` / `Item.to_dict()`；Schema 已创建 |
| 工作/表演 | `data/jobs.rpy` | `data/jobs/perform_job_dict.json` | 2026-06-08 | 170 个字典条目；纯字典结构无需 `from_dict()`；`_fallback_perform_job_dict` 回退 |
| 青楼参数 | `init/settings.rpy` | `data/economy/brothel_params.json` | 2026-06-08 | 5 组参数（capacity, helpers, reputation_cap, cost, pics）；字符串键→整数键自动转换 |
| 商店系统（阶段1-4 + A+B） | `init/settings.rpy` + `core_entities.rpy` + `economy.rpy` | `data/shops/*.json` | 2026-06-08 | 11 商店 + 10 升级 + 解锁批次 + 地区绑定 + 章节价格乘数/库存成长/时间压力 + `item_type_weights` 概率权重；`NPC.restock()` 完全数据驱动；`ItemInstance._price_multiplier` |
| 税收系统 | `init/settings.rpy` | `data/economy/tax_params.json` | 2026-06-08 | `tax_brackets` + `tax_chapter_penalty` + `tax_time_pressure_maximum` + `tax_random_range`；字符串键→整数键自动转换 |
| Minion | `init/variables.rpy` | `data/minions/minions.json` | 2026-06-08 | `all_minion_types` + `minion_description` + `minion_xp_to_level` + `minion_price` + `farm_pics`；字符串键→整数键自动转换 |
| 农场安装 | `init/variables.rpy` | `data/farm/installations.json` | 2026-06-08 | `installation_price` + `farm_type_list` + `farm_inst_list` + `farm_installations_dict`；字符串键→整数键自动转换 |
| 房间/建筑 | `init/variables.rpy` | `data/rooms/rooms.json` | 2026-06-08 | `room_pics` + `room_dict` + `common_room_dict` + `master_bedrooms` + `job_room_dict` + `room_capacity`；字符串键→整数键自动转换 |
| 力量/法术 | `data/powers.rpy` | `data/powers/powers.json` | 2026-06-08 | 61 普通 + 61 超级 EvilPower；`EvilPower.from_dict()`；fallback 硬编码保留 |
| 法术/月相 | `data/spells.rpy` | `data/spells/spells.json` | 2026-06-08 | `shield_effect` + `bshield_effect` + `bshield_spell` + `moons`（12 月相）；fallback 保留 |
| 主角职业/法术书 | `data/spells.rpy` | `data/classes/mc_classes.json` | 2026-06-08 | 3 职业（Warrior/Trader/Wizard）+ spellbooks + `modes` + `icon` + `description`；出身 `available_classes` 限制；动态 UI 过滤 |
| 难度参数 | `data/settings.rpy` + `init/settings.rpy` | `data/difficulty/difficulty.json` | 2026-06-08 | 5 难度等级 + 13 设置项的 `name_i18n` / `description_i18n`；`init/settings.rpy` `init 1` 加载覆盖；`data/settings.rpy` 硬编码 fallback 保留 |
| 目标系统 UI | `init/variables.rpy` | `data/goals/goal_ui.json` | 2026-06-08 | 8 通道 + 4 非故事通道 + 8 分类映射 + 8 工具提示按钮 + 4 颜色常量；`init/settings.rpy` `init 1` 加载覆盖；`variables.rpy` 硬编码 fallback 保留 |
| Fixations（癖好/执念） | `init/variables.rpy` | `data/fixations/fixations.json` | 2026-06-08 | 55 个 Fixation 定义 + 275 条 `_i18n` 文本（description/action/intro/pos_reaction/neg_reaction）；`Fixation.from_dict()`；`init/settings.rpy` `init 1` 重建 `fix_dict` + `fix_description`；`variables.rpy` 硬编码 fallback 保留 |
| 交互菜单树 | `init/variables.rpy` | `data/interactions/interact_dict.json` + `free_interact_dict.json` | 2026-06-08 | 22 奴隶菜单（5 子菜单 + 64 topics）+ 14 自由女孩菜单（4 子菜单 + 42 topics）；`GirlInteractionTopic.from_dict()`；`init/settings.rpy` `init 1` 覆盖；`variables.rpy` 硬编码 fallback 保留 |
| 标签词典 | `init/settings.rpy` | `settings/tags.json` | 2026-06-08 | 180 个标签映射；代码标签（非 `_i18n`）；`init -10` 加载；`tag_registry.register_tags_bulk()` |
| 图片映射 | `init/settings.rpy` | `settings/picture_mappings.json` | 2026-06-08 | 7 组图片映射（advertising/pony/security/arson/violent/treasure/no_girls）；`init -10` 加载 |
| 帮助文本 | `systems/help.rpy` | `settings/help_texts.json` | 2026-06-08 | 109 条帮助文本 + 16 图片映射；`_i18n` 文本 + `__()` 后处理；超链接编译逻辑保留 |
| 城市遭遇 | `init/variables.rpy` | `settings/encounters.json` | 2026-06-08 | `pop_name_dict` + `encounters` + `encounter_pics`；元组结构自动还原；`init 1` 加载 |
| 安全参数 | `init/variables.rpy` | `settings/security_params.json` | 2026-06-08 | `security_events` + `alert_limits1` + `alert_limits2`；整数键自动转换；元组自动还原；`init 1` 加载 |
| 训练测试 | `init/variables.rpy` | `settings/training_tests.json` | 2026-06-08 | `training_test_dict` + `magic_training_test_dict`；`init 1` 加载 |
| 任务参数 | `init/variables.rpy` | `settings/quest_params.json` | 2026-06-08 | `quest_base_gold` + `class_prices`；整数键自动转换；`init 1` 加载 |
| 库存排序/筛选 | `init/variables.rpy` | `settings/inventory_sorters.json` | 2026-06-08 | `inventory_filters` + `filter_list` + `sorter_dict`（20 排序器 + 9 过滤器 + 6 筛选列表）；`caption_i18n`/`tooltip_i18n` 可翻译；`init -3` 加载保持屏幕可用性 |
| 性训练参数 | `init/variables.rpy` | `settings/sex_training_params.json` | 2026-06-08 | `base_reluctance` + `preference_modifier` + `preference_limit` + `experienced_modifiers` + `experienced_color` + `sexual_training_value`；颜色使用 hex 值；`init -3` 加载 |
| 女孩背景随机池 | `init/variables.rpy` | `settings/girl_background_pools.json` | 2026-06-08 | `slave_stories` + `homes` + `guardians` + `hobbies` + `colors` + `food` + `drinks`（~69 条）；`init -3` 加载 |
| 音频注册表 | `init/settings.rpy` | `settings/audio_registry.json` | 2026-06-08 | `playlist`（12 首）+ `music_shortcuts`（41 个）+ `sound_shortcuts`（102 个）；`init -10` 加载；`setattr(store, key, value)` 保持变量接口 |
| 契约参数 | `init/variables.rpy` | `settings/contract_params.json` | 2026-06-08 | `contract_level` + `contract_value` + `contract_skill_limit` + `contract_sex_limit` + `contract_stage_modifier` + `contract_specials`；元组自动还原；`init -2`/`init` 加载 |
| 建筑资源 | `init/variables.rpy` | `settings/resource_params.json` | 2026-06-08 | `build_resources` + `resource_gold_value` + `resource_sell_discount` + `resource_base_exchange_rate`；`Fraction` 数组还原；`init -3` 加载 |
| 天赋原型 | `init/variables.rpy` | `settings/archetype_data.json` | 2026-06-08 | `archetype_list` + `archetype_description`；`description_i18n` 可翻译；`init -4` 加载 |
| 游戏常量 | `init/settings.rpy` + `init/variables.rpy` | `settings/game_constants.json` | 2026-06-08 | `weekdays` + `workshift_color` + `MC_class_index` + `roman_numbers` + `playerclass_pics` + `god_pics` + `alignment_pics` + `frequency_tags` + `night_pics` + `fix_pic_balance_*` + `tip_base` + `maximum_tip_modifier` + `starting_gold` + `class_discount` + `nsfw` + `stock_picture_threshold` + `mood_runaway_limit` + `free_girls_per_district`；`init -10`/`init -4` 加载 |
| 工作与性行为参数 | `init/variables.rpy` | `settings/job_params.json` | 2026-06-08 | `all_jobs` + `all_sex_acts` + `extended_sex_acts` + `farm_hardcore_acts` + `opposite_sex_acts` + `job_sort_value` + `job_color` + `normal_tags` + `all_farm_tags`；颜色使用 hex 值；`null` 键映射 `None`；`init -3` 加载 |
| 经验/等级/职业点参数 | `init/variables.rpy` | `settings/xp_rank_params.json` | 2026-06-08 | `xp_to_levelup`（25 级）+ `MC_xp_to_levelup`（26 级）+ `rank_cost` + `rank_stat_step` + `jp_*_modifier`；整数键自动转换；`init python` 加载 |
| 经济修正参数 | `init/variables.rpy` | `settings/economy_modifiers.json` | 2026-06-08 | `price_modifiers` + `stat_bonus` + `roll_modifier` + `helper_cost`；`init -4` 加载 |
| 顾客与广告参数 | `init/settings.rpy` | `settings/customer_params.json` | 2026-06-08 | `customer_base_preference` + `advertising_settings` + `reputation_decay` + `tip_*_modifier` + `xp_bonus_dict`；`init -10` 加载 |
| 解锁/作弊/执照参数 | `init/settings.rpy` + `init/variables.rpy` | `settings/unlock_params.json` | 2026-06-08 | `sex_act_test` + `chapter_district_unlocks` + `cheat_modifier` + `license_dict`；元组自动还原；`license_dict` 的 `name_i18n` 可翻译；`init -10`/`init -3` 加载 |
| 地点工具提示 | `init/variables.rpy` | `settings/location_tooltips.json` | 2026-06-08 | `location_tb` + `papa_location`；`papa_location` 的 `name_i18n` 可翻译；`init -4` 加载 |
| 人格/礼物参数 | `init/variables.rpy` | `settings/personality_gift_params.json` | 2026-06-08 | `alignment_bonus` + `personality_attributes` + `attribute_score_dict` + `gpersonalities_likes` + `gpersonalities_comment`；`comments_i18n` 可翻译；`init -3` 加载 |

## 本轮 i18n 适配新增完成（2026-06-10）

| 领域 | 源文件 | 目标 JSON | 完成日期 | 备注 |
|------|--------|-----------|----------|------|
| 物品 i18n | `core/systems/items.rpy` | `data/items/items.json` | 2026-06-10 | 193 个物品全部添加 `name_i18n` + `description_i18n`；`Item` 类新增 `name_i18n` 属性；`from_dict()` 读取 `name_i18n`；UI 显示改用 `__(it.name_i18n)` |
| 章节标题 i18n | `core/systems/events_dispatcher.rpy` | `data/chapters/chapter_titles.json` | 2026-06-10 | 8 个章节 `title`→`title_i18n`, `subtitle`→`subtitle_i18n`；加载代码使用 `__()` 翻译；fallback 硬编码文本包裹 `__()` |
| 帮助文本运行时翻译 | `core/systems/help.rpy` | `settings/help_texts.json` | 2026-06-10 | `get_help_text()` 所有返回路径包裹 `__()`；帮助文本支持运行时语言切换 |
| i18n 扫描器增强 | `core/i18n/json_i18n.rpy` | — | 2026-06-10 | `_scan_i18n_strings` 支持 `parent_key.endswith("_i18n")` 字典值收集；`help_dict_i18n` 等嵌套字典文本可被 `generate translations` 收集 |

## 已完成迁移（Phase 5-7）

| 领域 | 源文件 | 目标 JSON | 完成日期 | 备注 |
|------|--------|-----------|----------|------|
| Traits | `data/traits.rpy` | `data/traits/traits.json` | Phase 5 | 130+ 定义 |
| Perks | `data/perks.rpy` | `data/perks/perks.json` | Phase 5 | 50+ 定义 + 5 special |
| Achievements | `systems/achievements.rpy` | `data/achievements/achievements.json` | Phase 7 | 231 条成就 |
| Challenges | `framework/functions.rpy` | `data/challenges/challenges.json` | Phase 7 | MC 挑战 |
| Resources | `framework/functions.rpy` | `data/resources/resources.json` | Phase 7 | 建筑资源 |
| Contracts | `framework/functions.rpy` | `data/contracts/contracts.json` | Phase 7 | 8 个契约模板 |
| Goals | `framework/goal.rpy` | `data/goals/chapter_goals.json` | Phase 7 | 章节目标 |
| Chapter Titles | `init/start.rpy` | `data/chapters/chapter_titles.json` | Phase 7 | 章节标题 |
| Stats | `init/variables.rpy` | `data/stats/stats.json` | Phase 7 | 12 个属性定义 |
| Personalities | `init/variables.rpy` | `data/personalities/personalities.json` | Phase 7 | 人格原型 |
| Ranks | `init/variables.rpy` | `data/ranks/ranks.json` | Phase 7 | 等级名称 |
| Scenarios | `systems/gamemodes/` | `data/scenarios/scenarios.json` | Phase 7 | 剧本定义 |
| Origins | `systems/gamemodes/` | `data/sandbox/origins.json` | Phase 7 | 出身定义 |
| Difficulty | `init/settings.rpy` | `data/difficulty/difficulty.json` | Phase 7 | 难度参数 |
| Customer Affixes | `systems/customer/` | `data/customers/customer_affixes.json` | Phase 7 | 顾客词缀 |
| Cleanliness Penalties | `init/start.rpy` | `data/settings/cleanliness_penalties.json` | Phase 7 | 清洁度惩罚 |
| Treasure Thresholds | `init/start.rpy` | `data/settings/treasure_thresholds.json` | Phase 7 | 宝藏阈值 |
| Meta Progression | `systems/registry/` | `data/meta/meta_progression.json` | Phase 7 | Meta 升级 |
| NGP Settings | `systems/registry/` | `data/ngp/ngp_settings.json` | Phase 7 | NG+ 设置 |

---

## 技术债务与已知问题

| 问题 | 影响 | 状态 |
|------|------|------|
| Ren'Py `dict` → `RevertableDict` 替换 | `isinstance(x, dict)` 对 JSON 数据失效 | ✅ 已修复（使用 `__import__('builtins').dict`） |
| `functions.rpy` 拆分遗漏函数 | `generate_name` 等缺失 | ✅ 已修复 |
| `stats.json` 键大小写不匹配 | `gstats_dict` KeyError | ✅ 已修复 |
| `with open` 文件句柄泄漏 | 存档时 pickle 失败 | ✅ 已修复（全部 7 处已加 `del _f`） |
| `settings.rpy` 缩进错误 | 启动报错 | ✅ 已修复 |
| `crazy_customer()` 双重 `%` 格式化 | 运行时 TypeError | ✅ 已修复（移除了多余的 `%`） |
| `unlock_trainer()` 翻译名作为 key | 非英语环境下成就系统崩溃 | ⚠️ 临时修复（从 `portrait` 提取英文名），需系统级 `key`/`id` 属性解耦 |

---

## 迁移检查清单（每个领域通用）

- [ ] 1. 分析源 `.rpy` 中的数据结构
- [ ] 2. 设计 JSON Schema (`data/_schemas/xxx.schema.json`)
- [ ] 3. 编写 `DataLoader.load_xxx()` 方法
- [ ] 4. 实现目标类的 `from_dict()` / `to_dict()`
- [ ] 5. 创建 JSON 数据文件
- [ ] 6. 在 `start.rpy` 中添加 `_fallback_xxx` 回退
- [ ] 7. 修改原 `.rpy` 代码，优先加载 JSON
- [ ] 8. 运行 `tools/clean_runtime.ps1`
- [ ] 9. 运行 `--lint` 验证
- [ ] 10. 实际游玩验证（至少一次完整交互循环）
- [ ] 11. 更新本文档状态

---

## 剩余硬编码数据排查清单（Phase 7.5 全面审计）

> 以下按优先级和影响范围分组，仅列出尚未迁移到 JSON 的硬编码数据结构。
> 已迁移项（items, jobs, brothel_params, shops, tax_params, minions, installations, rooms, powers, spells, mc_classes, traits, perks, achievements, challenges, resources, contracts, goals, chapter_titles, stats, personalities, ranks, scenarios, origins, difficulty, customer_affixes, cleanliness_penalties, treasure_thresholds, meta_progression, ngp_settings）不再重复列出。

### 🔴 高优先级（大型数据集，建议优先迁移）

| # | 文件 | 变量名 | 类型 | 条目数 | 描述 |
|---|------|--------|------|--------|------|
| 1 | `variables.rpy` | `fix_description` + `fix_dict` | dict | ~200 | 全部 Fixation（癖好/执念）定义与描述文本 ✅ 已迁移至 `fixations.json` |
| 2 | `variables.rpy` | `interact_dict` + `free_interact_dict` | dict | ~110 | 奴隶/自由女孩交互菜单树 ✅ 已迁移至 `interactions/*.json` |
| 3 | `variables.rpy` | `farm_perform_dict` | dict | 100+ | 农场表演文本与机制（locations, intros, stories, reactions, cum texts） ✅ 已迁移至 `farm/farm_perform_dict.json` |
| 4 | `variables.rpy` | `generic_gossip` + `chapter_gossip` + `district_gossip` | list/dict | ~150 | 城市流言文本库（通用 + 章节 + 地区） ✅ 已迁移至 `settings/gossip.json` |
| 5 | `variables.rpy` | `recent_event_templates` | dict | 28 | 近期事件模板（28 种事件类型） ✅ 已迁移至 `settings/recent_events.json` |
| 6 | `variables.rpy` | `contract_tasks` + `contract_description` + 相关 | list/dict | ~60 | 契约任务系统（40 个 ContractTask + 描述 + 参数） ✅ 已迁移至 `settings/contracts.json` |
| 7 | `settings.rpy` | `_tag_dict_data` | dict | ~180 | 标签词典：文件名子串 → 游戏内标签映射 ✅ 已迁移至 `settings/tags.json` |
| 8 | `settings.rpy` | `security_pics` + `advertising_pics` + `treasure_pics` + `pony_pics` + `arson_pics` + `violent_pics` + `no_girls_pics` | dict/list | ~50 | 安全/广告/宝藏/ pony/ 纵火/暴力/无女孩图片映射 ✅ 已迁移至 `settings/picture_mappings.json` |
| 9 | `variables.rpy` | `mood_description` + `love_description` + `fear_description` | dict | 54 | 心情/爱意/恐惧等级描述文本 ✅ 已迁移至 `settings/girl_descriptions.json` |
| 10 | `variables.rpy` | `merchant_greetings` + `merchant_title` + `merchant_dict` | dict | 51 | 商人对话数据（问候语 + 头衔 + 类型映射） ✅ 已迁移至 `settings/merchants.json` |

### 🟡 中优先级（中等数据集，独立迁移价值高）

| # | 文件 | 变量名 | 类型 | 条目数 | 描述 |
|---|------|--------|------|--------|------|
| 11 | `variables.rpy` | `brothel_ranking_reputations` | dict | 40 | 青楼声望等级名称（40 个排名头衔） ✅ 已迁移至 `settings/rankings.json` |
| 12 | `variables.rpy` | `quality_prefix` + `quality_modifier` | dict | 57 | 物品品质前缀 + 价格乘数系统 ✅ 已迁移至 `settings/quality.json`，**再于 2026-09-13 从 core 迁出至 `custom/mods/Item Quality/` Mod**（core 只保留 `data/quality.rpy` 硬编码 fallback + `QualityRegistry` 框架） |
| 13 | `variables.rpy` | `encounters` + `encounter_pics` + `pop_name_dict` | tuple/dict | ~60 | 城市遭遇类型 + 图片 + 人口随机名字 ✅ 已迁移至 `settings/encounters.json` |
| 14 | `variables.rpy` | `jokes` + `compliments` | dict | ~20 | 社交交互文本库（笑话 + 赞美） ✅ 已迁移至 `settings/dialogue_texts.json` |
| 15 | `variables.rpy` | `help_dict` + `help_pic_dict` + `help_center_pic_dict` | dict | 120+ | Brokipedia 帮助文本系统（100+ 条目） ✅ 已迁移至 `settings/help_texts.json` |
| 16 | `settings.rpy` | `playlist` + `m_*` 音乐快捷 + `s_*` 音效快捷 | list/string | ~155 | 音频资源注册表（BGM + SFX） ✅ 已迁移至 `settings/audio_registry.json` |
| 17 | `variables.rpy`/`settings.rpy` | `customer_base_preference` + `advertising_settings` + `reputation_decay` + `tip_*_modifier` + `xp_bonus_dict` | dict | ~60 | 顾客偏好/广告/声誉衰减/小费/XB 倍率 ✅ 已迁移至 `settings/customer_params.json` |
| 18 | `variables.rpy` | `security_events` + `alert_limits1` + `alert_limits2` | dict | 17 | 安全事件类型 + 警戒阈值 ✅ 已迁移至 `settings/security_events.json` |
| 19 | `start.rpy` | `blist` + `district_dict` + `location_dict` + 位置实例化 + 人口实例化 | dict/object | ~90 | 世界地图：青楼定义 + 区域 + 地点 + 人口 ✅ 已迁移至 `worlds/default_world.json`（含 UI 布局 + 剧本模式接口） |
| 20 | `variables.rpy` | `xp_to_levelup` + `MC_xp_to_levelup` + `rank_cost` + `rank_stat_step` + `jp_*_modifier` | dict | ~70 | 经验/等级/晋升/职业点系统 ✅ 已迁移至 `settings/xp_rank_params.json` |
| 21 | `variables.rpy` | `base_reluctance` + `preference_modifier` + `preference_limit` + `experienced_*` + `sexual_training_value` | dict | ~40 | 性训练/经验/偏好系统 ✅ 已迁移至 `settings/sex_training_params.json` |
| 22 | `variables.rpy` | `slave_stories` + `homes` + `guardians` + `hobbies` + `colors` + `food` + `drinks` | list | ~63 | 女孩背景生成随机池 ✅ 已迁移至 `settings/girl_background_pools.json` |
| 23 | `variables.rpy` | `training_test_dict` + `magic_training_test_dict` + `long_act_description` | dict | ~28 | 训练前置条件 + 性行为长描述。`long_act_description` + `pref_response` + `experienced_description` ✅ 已迁移至 `settings/sex_descriptions.json` |
| 24 | `variables.rpy` | `sorter_dict` + `inventory_filters` + `filter_list` | dict | ~33 | UI 排序/筛选/库存系统 ✅ 已迁移至 `settings/inventory_sorters.json` |
| 25 | `variables.rpy` | `special_quest_description` + `quest_base_gold` + `class_prices` + `class_prefixes` | dict | ~21 | 任务/课程价格与描述。`class_prefixes` + `special_quest_description` ✅ 已迁移至 `settings/small_texts.json` |
| 26 | `settings.rpy` | `sex_act_test` + `chapter_district_unlocks` + `cheat_modifier` | dict | 13 | 性行为解锁阈值 + 章节区域解锁 + 作弊倍率 ✅ 已迁移至 `settings/unlock_params.json` |
| 27 | `variables.rpy` | `alignment_bonus` + `personality_attributes` + `attribute_score_dict` + `gpersonalities_likes` + `gpersonalities_comment` + `gift_description` | dict/list | ~50 | 人格/属性/礼物系统。`gift_description` ✅ 已迁移至 `settings/misc_texts.json`，其余 ✅ 已迁移至 `settings/personality_gift_params.json` |
| 28 | `variables.rpy` | `event_sounds` + `roll_dict` + `result_dict` + `result_colors` + `result_star_dict` + `result_reference` | dict | ~25 | 结果判定/骰子/音效系统。`roll_dict` + `result_dict` + `result_reference` ✅ 已迁移至 `settings/roll_results.json`，`event_sounds` ✅ 已迁移至 `settings/threat_params.json` |
| 29 | `variables.rpy` | `stat_increase_dict` + `maintenance_desc` + `log_event_dict` + `attraction_dict` + `gold_threat_*` | dict | ~30 | 维护/清洁度/吸引力/威胁系统。`stat_increase_dict` ✅ 已迁移至 `settings/stat_increase_dict.json`，`maintenance_desc` ✅ 已迁移至 `settings/maintenance_desc.json`，`log_event_dict` + `attraction_dict` ✅ 已迁移至 `settings/event_texts.json`，`gold_threat_amount` + `gold_threat_max` ✅ 已迁移至 `settings/threat_params.json` |
| 30 | `variables.rpy` | `price_modifiers` + `stat_bonus` + `roll_modifier` + `helper_cost` | dict | ~16 | 价格/加成/掷骰/助手成本 ✅ 已迁移至 `settings/economy_modifiers.json` |
| 31 | `variables.rpy` | `MC_inventory_slots` + `girl_inventory_slots` + `all_MC_stats` + `MC_stat_description` + `MC_playerclass_description` + `god_description` + `alignment_description` | list/dict | ~20 | MC/女孩库存槽 + 属性/职业/神祇/阵营描述。`MC_stat_description` + `MC_playerclass_description` + `god_description` + `alignment_description` ✅ 已迁移至 `settings/mc_descriptions.json` |
| 32 | `variables.rpy` | `license_dict` + `location_tb` + `papa_location` | dict | ~24 | 执照/地点工具提示/区域别名 ✅ 已迁移至 `settings/unlock_params.json` + `settings/location_tooltips.json` |
| 33 | `variables.rpy` | `archetype_list` + `archetype_description` | list/dict | 16 | 天赋原型名称与描述 ✅ 已迁移至 `settings/archetype_data.json` |
| 34 | `variables.rpy` | `contract_level` + `contract_value` + `contract_skill_limit` + `contract_sex_limit` + `contract_stage_modifier` + `contract_specials` + `contract_task_types_order` + `contract_task_types_description` | dict/list | ~40 | 契约系统参数。`contract_task_types_order` + `contract_task_types_description` ✅ 已随 `contracts.json` 迁移，其余 ✅ 已迁移至 `settings/contract_params.json` |
| 35 | `variables.rpy` | `goal_channels` + `goal_channels_no_story` + `goal_categories` + `goal_tb` + `goal_colors` | tuple/dict | ~32 | 目标系统 UI 常量 ✅ 已迁移至 `goal_ui.json` |
| 36 | `settings.rpy` | `frequency_tags` | dict | 4 | 标签频率权重修正 ✅ 已迁移至 `settings/game_constants.json` |
| 37 | `variables.rpy` | `weekdays` + `workshift_dict` + `workshift_color` + `MC_class_index` + `roman_numbers` | tuple/dict | ~23 | 日历/班次/职业索引/罗马数字。`workshift_dict` ✅ 已迁移至 `settings/small_texts.json`，其余 ✅ 已迁移至 `settings/game_constants.json` |
| 38 | `variables.rpy` | `all_jobs` + `all_sex_acts` + `extended_sex_acts` + `farm_hardcore_acts` + `opposite_sex_acts` + `job_sort_value` + `job_color` | list/dict | ~35 | 职业/性行为 ID 与排序/颜色 ✅ 已迁移至 `settings/job_params.json` |
| 39 | `variables.rpy` | `normal_tags` + `all_farm_tags` | tuple | 12 | 图片标签分类 |
| 40 | `variables.rpy` | `customer_rank_dict` + `attract_pop_dict` | dict | 11 | 顾客等级/人口吸引力。`attract_pop_dict` ✅ 已迁移至 `settings/small_texts.json` |
| 41 | `settings.rpy` | `playerclass_pics` + `god_pics` + `alignment_pics` | dict | 9 | 职业/神祇/阵营图标路径 ✅ 已迁移至 `settings/game_constants.json` |
| 42 | `variables.rpy` | `build_resources` + `resource_gold_value` + `resource_sell_discount` + `resource_base_exchange_rate` | list/dict | ~20 | 建筑资源价格与汇率 ✅ 已迁移至 `settings/resource_params.json` |
| 43 | `settings.rpy` | `night_pics` | list | 1 | 夜晚背景图片 ✅ 已迁移至 `settings/game_constants.json` |
| 44 | `settings.rpy` | `fix_pic_balance_variety` + `fix_pic_balance_accuracy` | dict | 4 | 图片平衡模式权重 ✅ 已迁移至 `settings/game_constants.json` |
| 45 | `settings.rpy` | `tip_base` + `maximum_tip_modifier` + `sell_girl_preference_boost` + `starting_gold` + `class_discount` + `nsfw` + `stock_picture_threshold` + `mood_runaway_limit` + `free_girls_per_district` | constant | ~9 | 独立数值常量（除 `sell_girl_preference_boost` 外）✅ 已迁移至 `settings/game_constants.json` |

### 🟢 低优先级（小型数据集或 inline 映射）

| # | 文件 | 变量名 | 类型 | 条目数 | 描述 |
|---|------|--------|------|--------|------|
| 46 | `framework/economy.rpy` | `s_des` | dict | 5 | 性行为简短描述 ✅ 已迁移至 `settings/sex_act_descriptions.json` |
| 47 | `framework/economy.rpy` | `rank_lookup_dict` + `order` + `check_order` | dict/list | 11 | 顾客匹配优先级 ✅ `rank_lookup_dict` 已迁移至 `settings/rank_lookup.json`（`order`/`check_order` 为动态变量，保留原处） |
| 48 | `framework/world.rpy` | `pronoun` | dict | 2 | 性别代词 ✅ 已迁移至 `settings/pronoun.json` |
| 49 | `framework/world.rpy` | `rank_factor` | dict | 5 | 区域等级→清洁费用系数 ✅ 已迁移至 `settings/rank_factor.json` |
| 50 | `framework/progression.rpy` | `first`/`second`/`third`/`names`/`fourth` | tuple | ~160 | 青楼名称生成词库 ✅ 已迁移至 `settings/brothel_name_pools.json` |
| 51 | `framework/character.rpy` | `weight_dict` + `weight` + `pref_dict` | dict | ~25 | 偏好权重与范围 |
| 52 | `framework/core_entities.rpy` | `god_dict` + `name_map` + `all_qualities` | dict/list | 9 | 神祇/名称映射/品质等级 ✅ 已迁移至 `settings/entity_lookups.json` |
| 53 | `framework/challenges.rpy` | inline opposed-chance table | list | 11 | 对抗骰差值表 ✅ 已迁移至 `settings/opposed_chance_table.json` |
| 54 | `framework/progression.rpy` | `_rank_dict` + `pace` | dict | 12 | 等级→数字映射 + XP 节奏 |
| 55 | `framework/girlclass.rpy` | `_wd_dict` (×2) + `base_value` + `step` (×2) | dict | ~30 | 工作日映射 + 偏好基础值 + 心情步长 |
| 56 | `systems/game_systems.rpy` | inline challenge pics + `_batch` (×4) | dict/list | 10 | 挑战图片 + 解锁批次 NPC 列表 |
| 57 | `systems/customer/customer_affixes.rpy` | `CUSTOMER_COLOR_TIERS` | dict | 8 | 顾客颜色层级（JSON fallback 已存在） |
| 58 | `systems/security.rpy` | `siege_enemy_scaling` | dict | 4 | 围城敌人规模配置 ✅ 已迁移至 `settings/security_scaling.json` |
| 59 | `systems/postings.rpy` | `quest_templates` + `class_templates` | list | 26 | 任务模板 + 课程模板 ✅ 已迁移至 `settings/quest_templates.json` |
| 60 | `systems/items.rpy` | `item_type_by_name` + `all_equipement_types` + `furniture_types` + `extractor_items` + `all_furniture` | dict/list | ~40 | 物品类型映射 + 装备槽 + 家具 |
| 61 | `systems/minigame.rpy` | `house_templates` + inline ninja effects | list/dict | 11 | 忍者小游戏房屋模板 |
| 62 | `systems/endday.rpy` | `latest_ent_match` + `latest_wh_match` | dict | 8 | 娱乐/卖淫匹配结果结构 |
| 63 | `systems/events_dispatcher.rpy` | `_bbcr` + `_neg_stats` + inline prep maps | list/dict | ~10 | 事件分发器内联常量 |
| 64 | `systems/farm.rpy` | `imgfiles` + `available_acts` | list | dynamic | 农场图片扫描 + 可用行为 |
| 65 | `systems/courtyard/courtyard.rpy` | `upgrade_cost` (×3) | dict | 6 | 庭院升级成本 |
| 66 | `systems/powers.rpy` | `evpower_color` + `evil_card_size` | dict/int | 3 | 力量稀有度颜色 + 卡片尺寸 ✅ 已迁移至 `settings/power_ui.json` |
| 67 | `systems/achievements.rpy` | `tracked_achievements` | list | 36 | 追踪中的成就目标 ✅ 已迁移至 `settings/tracked_achievements.json` |
| 68 | `systems/traits.rpy` | `gold_traits` + `pos_traits` + `neg_traits` | list | 127 | 特质硬编码定义（traits.json 已迁移，此为 fallback） |
| 69 | `content/declarations.rpy` | `y_ratio` + `UI_elements_colors` + `ev_gallery_list` | dict/list | 14 | 图片比例 + UI 主题 + 画廊分类 ✅ `UI_elements_colors` + `ev_gallery_list` 已迁移至 `settings/ui_element_colors.json` / `settings/ev_gallery_list.json` |
| 70 | `content/interactions.rpy` | inline cumshot tags + `diff` | dict | ~20 | 性行为 cumshot 标签 + 训练难度 |
| 71 | `content/interactions_free.rpy` | `limit` | dict | 6 | 自由女孩交互次数限制 |
| 72 | `content/story_events/story_events.rpy` | `loandict` + `loans` | dict/list | 14 | 贷款层级与贷款对象 ✅ 已迁移至 `settings/loans.json` |
| 73 | `data/settings.rpy` | `diff_name` + `diff_description` + `diff_settings` + `diff_setting_name` + `diff_setting_description` + `stat_name_dict` | dict/list | ~50 | 难度 UI 文本 + 属性名称（difficulty.json 已迁移，此为 UI 层） |
| 74 | `data/perks.rpy` | `archetype_dict` + `perk_description` + `perk_dict` | dict | 103 | 天赋硬编码（perks.json 已迁移，此为 fallback） |
| 75 | `data/items.rpy` | `_fallback_template_items` + `_fallback_all_items` | list | 131 | 物品硬编码 fallback |
| 76 | `data/jobs.rpy` | `_fallback_perform_job_dict` | dict | ~100 | 工作表演 fallback |
| 77 | `start.rpy` | `extras_dict` | dict | 6 | 解锁额外功能标志 ✅ 已迁移至 `settings/extras_dict.json` |
| 78 | `start.rpy` | `town_locations` + `beach_locations` + `nature_locations` + `court_locations` + `all_locations` | list | ~23 | 地点分类列表 |
| 79 | `start.rpy` | `endless_district` + `all_districts` | object/list | 7 | 无尽模式区域 + 区域列表 |

### 迁移建议路线图

**短期（1-2 个会话）：**
- ✅ Fixation 系统 — 已迁移至 `fixations.json`
- ✅ 交互菜单 — 已迁移至 `interactions/*.json`
- ✅ 农场表演文本 — 已迁移至 `farm/farm_perform_dict.json`
- ✅ 城市流言 — 已迁移至 `settings/gossip.json`
- ✅ 标签词典 — 已迁移至 `settings/tags.json`
- ✅ 图片映射 — 已迁移至 `settings/picture_mappings.json`
- ✅ 帮助系统 — 已迁移至 `settings/help_texts.json`
- ✅ 音频资源注册表 — 已迁移至 `settings/audio_registry.json`
- ✅ 库存排序/筛选 — 已迁移至 `settings/inventory_sorters.json`
- 世界地图（`blist` + `district_dict` + `location_dict` + 实例化）— 90+ 条目，复杂（需 `from_dict()`）

**中期（3-5 个会话）：**
- ✅ 契约任务系统 — 已迁移至 `settings/contracts.json`
- ✅ 经验/等级/晋升系统 — 已迁移至 `settings/xp_rank_params.json`
- ✅ 品质系统 — 已迁移至 `settings/quality.json`，再迁出至 `custom/mods/Item Quality/` Mod（2026-09-13；core 保留 `data/quality.rpy` fallback）
- ✅ 训练/偏好系统 — 已迁移至 `settings/sex_training_params.json`
- ✅ 背景生成随机池 — 已迁移至 `settings/girl_background_pools.json`
- ✅ 结果判定系统 — 已迁移至 `settings/roll_results.json` / `settings/threat_params.json`
- 契约系统参数（`contract_level` + `contract_value` + `contract_specials` 等）
- 建筑资源（`build_resources` + `resource_gold_value` + `resource_base_exchange_rate`）

**长期（可选 / 复杂度较高）：**
- 世界地图完整对象系统（`Population`/`Location`/`District`/`Brothel` `from_dict()`）
- 青楼名称生成词库（`progression.rpy` 词库 ~160 条）
- 物品类型系统（`systems/items.rpy` 映射）
- 成就追踪（`systems/achievements.rpy` `tracked_achievements`）
- 庭院/小游戏内联数据

---

## 附录：已移除的硬编码数据

以下数据已完全从 `.rpy` 中移除（仅 JSON + fallback 保留）：

| 领域 | 原硬编码位置 | 移除方式 |
|------|-------------|----------|
| Items | `data/items.rpy` | 全量移除，仅保留 `_fallback_*` |
| Jobs | `data/jobs.rpy` | 全量移除，仅保留 `_fallback_*` |
| Brothel params | `init/settings.rpy` | 全量移除，仅保留 `_fallback_*` |
| Shops | `init/settings.rpy` + `core_entities.rpy` + `economy.rpy` | 动态加载，无 fallback |
| Tax | `init/settings.rpy` | 全量移除，仅保留 `_fallback_*` |
| Minions | `init/variables.rpy` | 全量移除，仅保留 `_fallback_*` |
| Farm installations | `init/variables.rpy` | 全量移除，仅保留 `_fallback_*` |
| Rooms | `init/variables.rpy` | 全量移除，仅保留 `_fallback_*` |
| Powers | `data/powers.rpy` | 全量移除，仅保留 `_fallback_*` |
| Spells | `data/spells.rpy` | 全量移除，仅保留 `_fallback_*` + `moons` fallback |
| MC Classes | `data/spells.rpy` | `spellbook` 迁移至 `mc_classes.json`，原硬编码改为 fallback |
| Item Quality | `data/settings/quality.json`（原 `init/variables.rpy`） | JSON 已删除；数据迁出 core 至 `custom/mods/Item Quality/quality.json`，core 保留 `data/quality.rpy` 硬编码 fallback（**勿删**）+ `QualityRegistry` 框架 |

---

## 相关文档

- [`../modding/CUSTOM_DIRECTORIES.md`](../modding/CUSTOM_DIRECTORIES.md) — `core/data/` 全量子目录清单与编辑器对应关系
- [`../tools/TOOLS.md`](../tools/TOOLS.md) — 迁移历史脚本（`export_*`、`migrate_variables`、`split_*`）盘点
- [`../i18n/I18N_ROADMAP.md`](../i18n/I18N_ROADMAP.md) — JSON `_i18n` 迁移与翻译状态
- [`../i18n/BEST_PRACTICES.md`](../i18n/BEST_PRACTICES.md) — 新增 JSON 数据的可翻译字段规范
- [`../../game/core/systems/data_loader.rpy`](../../game/core/systems/data_loader.rpy) — DataLoader 加载实现
- [`../../tools/bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md) — 新增 JSON 数据源的操作清单
