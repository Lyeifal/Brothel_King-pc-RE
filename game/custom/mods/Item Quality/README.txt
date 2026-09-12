物品品质 Mod — 说明 | Item Quality Mod — README
=====================================================

本 Mod 通过 Mod API v2 注册，mod_id 为 "item_quality"，能力标志 requires
为 ["items"]。**可被玩家禁用**（"always_on": False）——在主菜单 → Mods
管理界面切换（持久化于 persistent._bk_v2_mod_states）。卸载 = 删除本目录。

作用 | What it does
-----------------
提供模板物品的 0-6 档品质数据：各形容词类别的名称前缀（如 dress_0
"Ragged"）、价格乘数（0.25x ~ 50x）、稀有度提升与效果数值缩放。
数据文件为本目录下的 quality.json，来源为原
`game/core/data/settings/quality.json`（已迁移，逐字一致）。

框架留本体，数据进 Mod（参考 "Game Modes" 剥离先例）
--------------------------------------------------
- 框架：`game/core/systems/registry/quality_registry.rpy`
  （QualityTier 类 + QualityRegistry 注册表，init -5）
- 硬编码兜底：`game/core/data/quality.rpy`（init -4，**勿删**）
  注册与本 Mod 完全相同的 7 档数据，按 DATA_MIGRATION 政策保证
  JSON/Mod 内容缺失时游戏仍可启动。
- 消费点：`game/core/systems/items.rpy`
  `Item.generate_new_item` / `transform_template` / `label init_items`。

禁用或卸载本 Mod 会怎样 | Disabling / uninstalling
---------------------------------------------------
- **禁用**（Mod 管理界面）：init -1 的注册被 is_mod_active 门控跳过，
  注册表保留核心兜底档位。数据完全相同 → 玩家无感。
- **卸载**（删除本目录）：同上回退到核心兜底。副作用仅剩「品质前缀
  的中文翻译不再被加载」——本 Mod 自带 tl/chinese_simplified/，随目录
  一起删除后前缀显示英文原文（核心正文用的几个同名词如
  "Fine"/"Cheap" 仍保留在 game/tl/chinese_simplified/strings.rpy）。
- quality.json 损坏或缺失：加载失败会 renpy.notify 报错并保留核心兜底，
  游戏不会崩溃。

给其他 Mod 作者 | For mod authors
---------------------------------
- 覆盖/调整档位：在任何更晚的 init 块（如 init -1 之后、或自己的 Mod 中，
  注意依赖顺序）调用

      api = services.mod_api_v2
      api.register_quality(QualityTier(7, 100.0, {"dress": "Mythic", "misc": "Mythic"}))

  同 rank 覆盖（后注册胜出）。`QualityTier.rank` 决定它在生成循环中的
  位置；gift/accessory 等稀疏类别可只提供部分 rank 的前缀。
- 新增的 rank 会自动参与 `init_items` 的变体生成，且
  `Item.rank = min(target_rank, quality_registry.get_max_rank())` 会
  跟随最高档位（不再是写死的 6）。
- 前置依赖：在 manifest 里写 `"dependencies": ["item_quality"]` 可确保
  本 Mod 的档位先注册（依赖未激活时你的 Mod 也不会激活）。
- 观察物品生成：注册 v2 钩子 `HOOK_ITEM_GENERATED`（"item_generated"），
  context 为 `{"item": 新物品, "template": 模板物品, "tier": 品质档位}`，
  生成每个品质变体时触发一次（纯通知，无法拦截）。

翻译 | Translations
-------------------
本 Mod 自带翻译，位于 `tl/chinese_simplified/`：
- `quality.rpy` 37 条品质前缀 + 2 条加载失败提示
- `mod.rpy`    Mod 名称与描述

前缀的 `old` 必须与 quality.json 中的英文串逐字节一致（含尾随空格，
如 "Cheap "、"Worn " —— 它们用于替换 "{0} {1}" 的分隔空格）。
注意 "Fine"/"Cheap"/"Common"/"Rare"/"Broken"/"Medium" 在核心正文中
另有用途，其核心翻译仍留在 strings.rpy，改这里的值只影响品质前缀。

文件 | Files
------------
- mod.rpy      Mod API v2 注册 + is_mod_active 门控 + 档位注册调用
- quality.rpy  load_quality_tiers()：读取 quality.json 并注册档位（init -9）
- quality.json 7 档品质数据（原 core/data/settings/quality.json）
- tl/          中文翻译（Mod 自管理）
