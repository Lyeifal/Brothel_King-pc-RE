################################################################################
##  Game Modes Mod — BK Evolution
##  EN: Standalone mod housing the former core game mode implementations
##      (ex game/core/systems/gamemodes/): story, sandbox and scenario modes,
##      plus the start-of-game mode/origin/scenario selection screens.
##  ZH: 游戏模式独立 Mod（原 game/core/systems/gamemodes/ 下的模式实现）：
##      剧情、沙盒、剧本三种模式及开局模式/出身/剧本选择屏幕。
##
##  EN: The core framework (GameMode base class + GameModeRegistry singleton)
##      stays in game/core/systems/gamemodes/gamemode.rpy. With this mod
##      absent OR disabled, the core start flow falls back to plain story
##      mode (no selection screen).
##  ZH: 核心框架（GameMode 基类 + GameModeRegistry 单例）保留在
##      game/core/systems/gamemodes/gamemode.rpy。本 Mod 缺席或被禁用
##      时，本体开局流程回退为纯剧情模式（无选择界面）。
##
##  EN: Registered through Mod API v2 with "always_on": False — it can be
##      toggled off in the main-menu Mod Manager screen
##      (persistent._bk_v2_mod_states). Uninstall = remove this folder.
##      Other mods can declare "dependencies": ["game_modes"] to build on
##      the mode/origin/scenario registries (see README.txt).
##  ZH: 通过 Mod API v2 注册，"always_on": False——可在主菜单 Mod 管理
##      界面禁用（persistent._bk_v2_mod_states）。卸载 = 删除本目录。
##      其他 Mod 可声明 "dependencies": ["game_modes"] 以前置依赖本 Mod
##      的模式/出身/剧本注册表（见 README.txt）。
################################################################################

init -1 python:

    services.mod_api_v2.register_mod("game_modes", {
        "name": __("Game Modes"),
        "version": "1.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("Adds the story and sandbox game modes, including the start-of-game mode selection screen and the player origin system."),
        "requires": ["game_modes", "origin"],
        "hooks": {},
        "dependencies": [],
        ## EN: Explicitly declared: this mod CAN be disabled by the player.
        ## ZH: 显式声明：本 Mod 可被玩家禁用。
        "always_on": False,
    })

    ## EN: Register the three game modes into the core registry — only while
    ##     this mod is active. When the mod is disabled in the Mod Manager,
    ##     register_mod leaves it inactive (persistent._bk_v2_mod_states), so
    ##     the registry stays empty and the core start flow falls back to
    ##     plain story mode (start.rpy select_game_mode).
    ## ZH: 将三种游戏模式注册进核心注册表——仅在本 Mod 激活时进行。
    ##     Mod 管理界面禁用本 Mod 后，register_mod 不会激活它
    ##     （persistent._bk_v2_mod_states），注册表保持为空，
    ##     本体开局流程回退为纯剧情模式（start.rpy select_game_mode）。
    if services.mod_api_v2.is_mod_active("game_modes"):
        gamemode_registry.register(StoryMode())
        gamemode_registry.register(SandboxMode())
