################################################################################
##  Sandbox Mode — BK Evolution (Game Modes Mod)
##  EN: Free-form gameplay without forced story progression.
##      Moved from game/core/systems/gamemodes/sandbox_mode.rpy — the GameMode
##      base class and gamemode_registry stay in the core.
##      The player origin system lives in its own "Origins" mod now
##      (game/custom/mods/Origins/).
##  ZH: 无强制剧情推进的自由玩法。
##      原位于 game/core/systems/gamemodes/sandbox_mode.rpy —— GameMode 基类
##      与 gamemode_registry 注册表保留在本体。
##      玩家出身系统已独立为 "Origins" Mod
##      （game/custom/mods/Origins/）。
################################################################################

init -9 python:

    class SandboxMode(GameMode):
        """
        EN: Sandbox mode — free-form gameplay without forced story progression.
        ZH: 沙盒模式 — 无强制剧情推进的自由玩法。
        """

        def __init__(self):
            super(SandboxMode, self).__init__(
                mode_id=GameMode.MODE_SANDBOX,
                name_i18n_key="沙盒模式",
                description_i18n_key="自由玩法。在没有剧情锁定的情况下打造自己的道路。"
            )

            ## EN: UI card metadata for the mode selection screen.
            ## ZH: 模式选择界面的卡片元数据。
            self.ui_color = "#4ECDC4"
            self.ui_icon = "mode_sandbox"

        def on_game_start(self, game):
            """
            EN: Set up sandbox goal channels (fewer story gates).
            ZH: 设置沙盒目标频道（更少的剧情锁定）。
            """
            game.goal_channels = ("advance", "advance2", "contract", "other")

        def can_advance_chapter(self, game):
            """
            EN: Sandbox allows free chapter advancement (or locks to a chosen chapter).
            ZH: 沙盒允许自由章节推进（或锁定到选定章节）。
            """
            return True

        def get_goal_channels(self):
            return ("advance", "advance2", "contract", "other")

        def is_story_locked(self):
            return False
