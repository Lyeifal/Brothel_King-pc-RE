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
##      absent, the core start flow falls back to plain story mode (no
##      selection screen).
##  ZH: 核心框架（GameMode 基类 + GameModeRegistry 单例）保留在
##      game/core/systems/gamemodes/gamemode.rpy。本 Mod 缺席时，本体
##      开局流程回退为纯剧情模式（无选择界面）。
##
##  EN: Install = always active (Mod API v2). Uninstall = remove this folder.
##  ZH: 安装即常驻激活（Mod API v2）。卸载 = 删除本目录。
################################################################################

init -1 python:

    services.mod_api_v2.register_mod("game_modes", {
        "name": __("Game Modes"),
        "version": "1.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("Adds the story, sandbox and scenario game modes, including the start-of-game selection screens and the player origin / community scenario systems."),
        "requires": ["game_modes", "origin", "scenario"],
        "hooks": {},
        "dependencies": [],
    })

    ## EN: Register the three game modes into the core registry.
    ##     The classes are defined at init -9 in this mod's mode files,
    ##     the registry singleton itself lives in the core (init -10).
    ## ZH: 将三种游戏模式注册进核心注册表。
    ##     类定义在本 Mod 的模式文件中（init -9），
    ##     注册表单例位于本体（init -10）。
    gamemode_registry.register(StoryMode())
    gamemode_registry.register(SandboxMode())
    gamemode_registry.register(ScenarioMode())
