# BK Evolution — JSON i18n 迁移计划 (修订版)

> 本文档追踪将 JSON 数据中的可翻译文本从隐式标记迁移到显式 `_i18n` 后缀约定的进度。
> 最后更新：2026-06-10

---

## 目标

1. **消除猜测**：可翻译字段通过 `_i18n` 后缀显式声明，扫描器不需要白名单/黑名单过滤
2. **代码简化**：`from_dict()` 不需要运行时判断字符串是原文还是图片路径/代码片段
3. **翻译维护**：`generate translations` 运行时自动收集所有 JSON 文本，无需额外脚本

---

## 总览进度

| 阶段 | 状态 | 说明 |
|------|------|------|
| Phase 1（核心 JSON） | ✅ 已完成 | difficulty, origins, shops, powers, spells, personalities, achievements, contracts, customer_affixes, meta, ngp, cleanliness_penalties 等 |
| Phase 2（规模 JSON） | ✅ 已完成 | minions, stats, ranks, archetypes, encounter pops, sex_training_params, job_params, xp_rank_params, economy_modifiers, customer_params, unlock_params, location_tooltips, contract_params, resource_params, security_params, power_ui, game_constants 等 |
| Phase 3（内容密集型） | ✅ 已完成 | items, chapter_titles, fixations, quest_templates, interact_dict, free_interact_dict, farm_perform_dict, help_texts 等 |
| Phase 4（硬编码→JSON） | ✅ 已完成 | 全部硬编码数据已迁移，且直接采用 `_i18n` 后缀 |
| Phase 5（清理收尾） | ⏭️ 待开始 | 移除白名单、generate translations 测试、游戏实测 |

**合计：105 个 JSON 数据文件中，所有含可翻译文本的文件已完成 `_i18n` 适配。**

---

## 已完成的 i18n 适配（按类别汇总）

### 核心系统
- `data/difficulty/difficulty.json` — `name_i18n`, `description_i18n`
- `data/sandbox/origins.json` — `name_i18n`, `description_i18n`
- `data/shops/shops.json` — `name_i18n`
- `data/powers/powers.json` — `name_i18n`, `short_description_i18n`, `description_i18n`
- `data/spells/spells.json` — `name`（代码 key）, `display_name_i18n`, `description_i18n`
- `data/personalities/personalities.json` — `name_i18n`, `description_i18n`
- `data/achievements/achievements.json` — `title_i18n`, `description_i18n`
- `data/meta/meta_progression.json` — `name_i18n`, `description_i18n`
- `data/ngp/ngp_settings.json` — `label_i18n`, `ttip_i18n`
- `data/chapters/chapter_titles.json` — `title_i18n`, `subtitle_i18n`
- `data/classes/mc_classes.json` — `name_i18n`, `description_i18n`

### 内容数据
- `data/traits/traits.json` — `base_description_i18n`（`name`/`verb`/`archetype`/`opposite` 为代码 key，保持原样）
- `data/perks/perks.json` — `base_description_i18n`（`name`/`archetype` 为代码 key，保持原样）
- `data/fixations/fixations.json` — `description_i18n`, `action_i18n`, `intro_i18n`, `pos_reaction_i18n`, `neg_reaction_i18n`
- `data/items/items.json` — `name_i18n`, `description_i18n`（`name` 同时是 `item_dict` 代码 key，保留）
- `data/contracts/contracts.json` — `names_i18n`, `organizers_i18n`, `venues_i18n`
- `data/settings/contracts.json` — `name_i18n`, `contract_description_i18n`, `contract_task_types_description_i18n`
- `data/customers/customer_affixes.json` — `name_i18n`, `description_i18n`
- `data/story_events/story_events.json` — `title_i18n`, `description_i18n`
- `data/rooms/rooms.json` — `job_room_display_name_i18n`

### 交互与事件
- `data/interactions/interact_dict.json` — `caption_i18n`
- `data/interactions/free_interact_dict.json` — `caption_i18n`
- `data/worlds/default_world.json` — `world_name_i18n`, `description_i18n`, `base_description_i18n`, `menu_caption_i18n`

### 农场与表演
- `data/farm/farm_descriptions.json` — `farm_descriptions_i18n`
- `data/farm/farm_perform_dict.json` — 大量表演文本键使用 `_i18n`（如 `intro_good_i18n`, `service_good_i18n`, `sex_story_monster_i18n` 等 77+ 个字段）
- `data/settings/farm_holding_params.json` — `farm_holding_dict_i18n`, `farm_ttip_i18n`

### 文本字典（settings/）
- `settings/cleanliness_penalties.json` — `text_i18n`
- `settings/dialogue_texts.json` — `jokes_i18n`, `compliments_i18n`
- `settings/event_texts.json` — `log_event_dict_i18n`, `attraction_dict_i18n`
- `settings/gossip.json` — `generic_gossip_i18n`, `chapter_gossip_i18n`, `district_gossip_i18n`
- `settings/help_texts.json` — `help_dict_i18n`（109 条帮助文本，扫描器已支持字典值收集）
- `settings/loading_tips.json` — `random_tips_i18n`
- `settings/mc_descriptions.json` — `MC_stat_description_i18n`, `MC_playerclass_description_i18n`, `god_description_i18n`, `alignment_description_i18n`
- `settings/merchants.json` — `merchant_greetings_i18n`, `merchant_title_i18n`
- `settings/recent_events.json` — `recent_event_templates_i18n`
- `settings/sex_act_descriptions.json` — `service_i18n`, `sex_i18n`, `anal_i18n`, `fetish_i18n`, `naked_i18n`
- `settings/sex_descriptions.json` — `long_act_description_i18n`, `experienced_description_i18n`, `pref_response_i18n`
- `settings/small_texts.json` — `attract_pop_dict_i18n`, `workshift_dict_i18n`, `special_quest_description_i18n`
- `settings/stat_increase_dict.json` — `stat_increase_dict_i18n`
- `settings/maintenance_desc.json` — `maintenance_desc_i18n`
- `settings/girl_descriptions.json` — `mood_description_i18n`, `love_description_i18n`, `fear_description_i18n`
- `settings/rankings.json` — `brothel_ranking_reputations_i18n`
- `settings/inventory_sorters.json` — `caption_i18n`, `tooltip_i18n`
- `settings/unlock_params.json` — `name_i18n`
- `settings/location_tooltips.json` — `name_i18n`
- `settings/misc_texts.json` — `class_prefixes_i18n`, `gift_description_i18n`, `shopgirl_comment_i18n`
- `settings/brothel_name_pools.json` — `names_i18n`, `second_i18n`, `third_i18n`, `fourth_i18n`
- `settings/roll_results.json` — `result_reference_labels_i18n`, `result_reference_templates_i18n`

### 商店与参数
- `settings/shop_params.json` — `shop_item_number_i18n`
- `settings/item_type_params.json` — `description_i18n`
- `settings/encounters.json` — `pop_name_dict_i18n`
- `settings/personality_gift_params.json` — `comments_i18n`

### 纯数据（无文本，无需 i18n）
- `settings/event_colors.json` — 纯十六进制值
- `settings/girl_name_pools.json` — 纯数据，无文本
- `settings/minion_params.json` — 纯数据，无文本
- `settings/training_difficulty.json` — 纯数值
- `data/jobs/perform_job_dict.json` — 纯数据结构，无可翻译文本

### 特殊处理（不适用 `_i18n`）
- `data/challenges/challenges.json` — `name` 同时是图片路径 `resources/ui/challenges/{name}.webp`
- `data/resources/resources.json` — `name` 同时是图片路径
- `data/rooms/rooms.json` — `name` 同时是 `room_pics` 字典 key
- `data/traits/traits.json` — `name`/`verb`/`archetype`/`opposite` 为 `trait_dict` 代码 key
- `data/perks/perks.json` — `name`/`archetype` 为 `perk_dict` 代码 key
- `data/items/items.json` — `name` 为 `item_dict` 代码 key（已添加 `name_i18n` 用于显示）
- `data/spells/spells.json` — `name` 为月相代码 key（`display_name_i18n` 用于显示）
- `data/worlds/default_world.json` — `populations[].name` 为顾客群体代码标识符

---

## 本轮（2026-06-10）新增完成

| 文件 | 改动 | 说明 |
|------|------|------|
| `data/items/items.json` | `name_i18n` + `description_i18n` | 193 个物品全部适配；`Item` 类新增 `name_i18n` 属性；UI 显示改用 `__(it.name_i18n)` |
| `data/chapters/chapter_titles.json` | `title_i18n` + `subtitle_i18n` | 8 个章节标题；`events_dispatcher.rpy` 加载时翻译 |
| `core/i18n/json_i18n.rpy` | `_scan_i18n_strings` 增强 | 支持 `parent_key.endswith("_i18n")` 字典值收集（如 `help_dict_i18n`） |
| `core/systems/help.rpy` | `get_help_text()` 翻译 | 所有返回路径包裹 `__()`，帮助文本支持运行时语言切换 |

---

## Phase 5：清理与收尾

- [ ] 移除 `json_i18n.rpy` 中的白名单兼容模式（`_I18N_FIELD_KEYS`）
  - 前提：所有 JSON 已完成 `_i18n` 迁移验证
- [ ] 运行完整 `generate translations` 测试，确认所有字符串被收集
- [ ] 实际游戏测试（切换语言验证显示正确）
- [ ] 更新 `TRANSLATION_GUIDE.md`（如果存在），说明 `_i18n` 约定

---

## 技术约定

### JSON 字段命名

```json
{
  "id": "pirate_captain",
  "name_i18n": "Pirate Captain",
  "description_i18n": "A feared captain of the high seas.",
  "icon_tag": "origin_pirate",
  "talents": ["strength", "constitution"]
}
```

- **可翻译文本**：字段名以 `_i18n` 结尾
- **内部标识符**：使用 `id`、`key`、`tag`、`type` 等不含 `_i18n` 的字段
- **图片/音频路径**：保持原字段名（如 `pic`、`icon`、`sound`），不加 `_i18n`
- **数值/代码**：保持原字段名（如 `price`、`effects`、`rank`），不加 `_i18n`

### 代码中使用

```python
# from_dict 中 —— 使用 get_i18n() 或 I18nMixin
class MyEntity(I18nMixin):
    @classmethod
    def from_dict(cls, data):
        d = cls._resolve_i18n(data)
        return cls(
            id=data["id"],               # 内部标识符，不需要翻译
            name=d["name"],               # 已翻译的显示名称
            description=d.get("description")
        )

# 或手动逐个字段获取
def from_dict(cls, data):
    return cls(
        name=get_i18n(data, "name"),
        description=get_i18n(data, "description"),
        raw_key=get_i18n_raw(data, "name")  # 如果需要原始英文做 key
    )
```

### 白名单兼容模式的生命周期

当前 `json_i18n.rpy` 同时支持两种模式：
1. `_i18n` 后缀（显式，无过滤）
2. 白名单 key（隐式，有过滤逻辑）

当 Phase 5 完成后，可以移除白名单模式，只保留 `_i18n` 后缀识别。届时 `_is_i18n_field()` 的逻辑将简化为：

```python
def _is_i18n_field(key, value):
    return isinstance(value, (str, unicode)) and key.endswith("_i18n")
```

---

## 相关文件

| 文件 | 作用 |
|------|------|
| `game/core/i18n/json_i18n.rpy` | i18n 注册系统 + 辅助函数 + I18nMixin |
| `BK_EVOLUTION_DATA_MIGRATION.md` | 数据迁移总进度 |
| `game/core/systems/data_loader.rpy` | DataLoader，多数 JSON 的加载入口 |
| `game/core/data/HARDCODED_DATA_AUDIT.md` | 硬编码数据迁移审计表 |
