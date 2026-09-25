################################################################################
##  Game Modes Mod — BK Evolution
##  EN: Standalone mod housing the former core game mode implementations
##      (ex game/core/systems/gamemodes/): story and sandbox modes. The
##      start-of-game mode selection screen has been REMOVED — the start
##      flow always runs in story mode, with no mode/origin selection.
##      (The player origin system lives in the standalone Origins mod and
##      is chosen on the quick_start class page instead.)
##  ZH: 游戏模式独立 Mod（原 game/core/systems/gamemodes/ 下的模式实现）：
##      剧情与沙盒模式。开局模式选择界面已移除——开局流程始终为剧情
##      模式，无模式/出身选择。（出身系统已迁至独立的 Origins Mod，
##      改在 quick_start 职业页选择。）
##
##  EN: The core framework (GameMode base class + GameModeRegistry singleton)
##      stays in game/core/systems/gamemodes/gamemode.rpy. The registered
##      modes are kept only as data/fallback — the story fallback activates
##      when no mode is selected at start.
##  ZH: 核心框架（GameMode 基类 + GameModeRegistry 单例）保留在
##      game/core/systems/gamemodes/gamemode.rpy。注册的模式仅作为数据/
##      兜底保留——开局未选择模式时激活剧情模式兜底。
##
##  EN: Registered through Mod API v2 with "always_on": False — it can be
##      toggled off in the main-menu Mod Manager screen
##      (persistent._bk_v2_mod_states). Uninstall = remove this folder.
##  ZH: 通过 Mod API v2 注册，"always_on": False——可在主菜单 Mod 管理
##      界面禁用（persistent._bk_v2_mod_states）。卸载 = 删除本目录。
################################################################################

init -1 python:

    services.mod_api_v2.register_mod("game_modes", {
        "name": __("Game Modes"),
        "version": "1.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("Houses the story/sandbox game mode classes (kept for fallback and future use). The start-of-game mode selection screen was removed — new games always start in story mode."),
        "requires": ["game_modes", "origin"],
        "hooks": {},
        "dependencies": [],
        ## EN: Explicitly declared: this mod CAN be disabled by the player.
        ## ZH: 显式声明：本 Mod 可被玩家禁用。
        "always_on": False,
    })

    ## EN: Register the game modes into the core registry — only while this
    ##     mod is active. With no start-of-game selection, game_mode stays
    ##     None and init_game falls back to the registered story mode.
    ## ZH: 将游戏模式注册进核心注册表——仅在本 Mod 激活时进行。
    ##     开局不再选择模式，game_mode 保持 None，由 init_game 回退到
    ##     已注册的剧情模式。
    if services.mod_api_v2.is_mod_active("game_modes"):
        gamemode_registry.register(StoryMode())
        gamemode_registry.register(SandboxMode())
