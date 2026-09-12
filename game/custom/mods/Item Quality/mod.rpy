################################################################################
##  Item Quality Mod — BK Evolution
##  EN: Standalone mod housing the default 0-6 item quality tier data
##      (ex game/core/data/settings/quality.json): name prefixes per adjective
##      category, price multipliers, rarity bump and effect scaling applied to
##      generated template items.
##  ZH: 物品品质独立 Mod（原 game/core/data/settings/quality.json）：各形容词
##      类别的名称前缀、价格乘数、稀有度提升与效果缩放，作用于模板物品生成的
##      各档变体。
##
##  EN: The core framework (QualityTier + QualityRegistry) stays in
##      game/core/systems/registry/quality_registry.rpy, with a hardcoded
##      fallback copy of these exact 7 tiers in game/core/data/quality.rpy.
##      With this mod absent OR disabled, item generation falls back to those
##      tiers — identical data, so players see no difference.
##  ZH: 核心框架（QualityTier + QualityRegistry）保留在
##      game/core/systems/registry/quality_registry.rpy，同样的 7 档硬编码回退
##      副本在 game/core/data/quality.rpy。本 Mod 缺席或被禁用时，物品生成
##      回退到那套档位——数据完全相同，玩家无感。
##
##  EN: Registered through Mod API v2 with "always_on": False — it can be
##      toggled off in the main-menu Mod Manager screen
##      (persistent._bk_v2_mod_states). Uninstall = remove this folder.
##      Other mods can retune or extend the tiers by calling
##      api.register_quality(QualityTier(...)) from a later init block, or
##      declare "dependencies": ["item_quality"] to build on this data.
##  ZH: 通过 Mod API v2 注册，"always_on": False——可在主菜单 Mod 管理界面禁用
##      （persistent._bk_v2_mod_states）。卸载 = 删除本目录。
##      其他 Mod 可在更晚的 init 块中调用 api.register_quality(QualityTier(...))
##      调整或扩展档位，也可声明 "dependencies": ["item_quality"] 前置依赖本 Mod。
################################################################################

init -1 python:

    services.mod_api_v2.register_mod("item_quality", {
        "name": __("Item Quality"),
        "version": "1.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("Registers the default 0-6 item quality tiers: name prefixes per adjective category, price multipliers, rarity bump and effect scaling for generated template items. Disabling this mod reverts to the core hardcoded fallback tiers (identical data)."),
        "requires": ["items"],
        "hooks": {},
        "dependencies": [],
        ## EN: Explicitly declared: this mod CAN be disabled by the player.
        ## ZH: 显式声明：本 Mod 可被玩家禁用。
        "always_on": False,
    })

    ## EN: Register the tiers into the core QualityRegistry — only while this
    ##     mod is active. When the mod is disabled in the Mod Manager,
    ##     register_mod leaves it inactive (persistent._bk_v2_mod_states), so
    ##     the registry keeps the core fallback tiers registered at init -4.
    ## ZH: 将档位注册进核心 QualityRegistry——仅在本 Mod 激活时进行。
    ##     Mod 管理界面禁用本 Mod 后，register_mod 不会激活它
    ##     （persistent._bk_v2_mod_states），注册表保留 init -4 注册的核心回退档位。
    if services.mod_api_v2.is_mod_active("item_quality"):
        load_quality_tiers()
