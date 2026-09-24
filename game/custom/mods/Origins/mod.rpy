################################################################################
##  Origins Mod — 注册（Mod API v2）
##  EN: Standalone player-origin mod. At game start the player picks a
##      background; each origin grants a UNIQUE player class with its own
##      spell tree, plus talents and a starting bonus. Religion is untouched.
##      Disabled => the start flow silently skips origin selection.
##  ZH: 独立玩家出身 Mod。开局选择出身后，主角获得独特职业与专属技能树，
##      外加天赋与起始奖励；信仰沿用本体机制。禁用本 Mod 时，
##      开局流程会静默跳过出身选择。
##
##  EN: Other mods can depend on "origins" to reuse origin_registry /
##      PlayerOrigin. Uninstall = remove this folder.
##  ZH: 其他 Mod 可前置依赖 "origins" 以复用 origin_registry /
##      PlayerOrigin。卸载 = 删除本目录。
################################################################################

init -1 python:

    services.mod_api_v2.register_mod("origins", {
        "name": __("Origins"),
        "version": "1.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("Player origins: pick a background at game start to play a unique class with its own spell tree. Religion choice is unchanged."),
        "requires": [],
        "hooks": {},
        "dependencies": [],
        ## EN: Explicitly declared: this mod CAN be disabled by the player.
        ## ZH: 显式声明：本 Mod 可被玩家禁用。
        "always_on": False,
    })

    ## EN: Only load data / patch the MC while the mod is active.
    ## ZH: 仅在本 Mod 激活时加载数据并包装 MC。
    if services.mod_api_v2.is_mod_active("origins"):
        origins_load_data()
        origins_patch_update_spells()
        services.mod_api_v2.register_hook(services.mod_api_v2.HOOK_GAME_LOADED, _origins_on_game_loaded, priority=0)
