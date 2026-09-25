################################################################################
##  Origins Mod — 注册（Mod API v2）
##  EN: Standalone player-origin mod. The five origins are offered as the
##      CLASS choice on the quick_start page (character/religion/difficulty),
##      next to the free religion pick — each origin grants a UNIQUE player
##      class with its own spell tree, plus talents and a starting bonus
##      applied once at game start. Religion is untouched (it has its own
##      story content). Disabled => the class choice falls back to the three
##      base classes.
##  ZH: 独立玩家出身 Mod。五个出身作为职业选项出现在 quick_start 页
##      （人物/信仰/难度），与自由选择的信仰并列——每个出身授予独特
##      职业与专属技能树，外加天赋与起始奖励（开局时套用一次）。
##      信仰沿用本体机制（信仰有后续剧情内容），不做改动。禁用本 Mod
##      时，职业选择回退为三个基础职业。
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
        "description": __("Player origins: the five origins are offered as the class choice on the character setup page (next to religion and difficulty). Each origin grants a unique class with its own spell tree, talents and a starting bonus. Religion choice is unchanged."),
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
