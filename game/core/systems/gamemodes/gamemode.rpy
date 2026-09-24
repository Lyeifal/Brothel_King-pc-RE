################################################################################
##  GameMode System — BK Evolution
##  EN: Base framework for all game modes (story, sandbox, scenario).
##      This file only holds the framework: the GameMode base class and the
##      gamemode_registry singleton. The built-in mode implementations and
##      the selection screens live in the "Game Modes" mod
##      (game/custom/mods/Game Modes/); without it the start flow falls
##      back to plain story mode.
##  ZH: 所有游戏模式的基础框架（剧情、沙盒、剧本）。
##      本文件只保留框架：GameMode 基类与 gamemode_registry 单例。
##      内置模式实现与选择界面已迁至 "Game Modes" Mod
##      （game/custom/mods/Game Modes/）；无该 Mod 时开局流程
##      回退为纯剧情模式。
################################################################################

init -10 python:

    class GameMode(object):
        """
        EN: Base class for all game modes. Each mode defines its own rules,
            victory conditions, goal channels, and start behavior.
        ZH: 所有游戏模式的基类。每种模式定义自己的规则、胜利条件、
            目标频道和起始行为。
        """

        MODE_STORY   = "story"      # EN: Story mode / ZH: 剧情模式
        MODE_SANDBOX = "sandbox"    # EN: Sandbox mode / ZH: 沙盒模式

        def __init__(self, mode_id, name_i18n_key, description_i18n_key):
            ## EN: Unique identifier for this mode.
            ## ZH: 此模式的唯一标识符。
            self.mode_id = mode_id

            ## EN: Translation key for the mode display name.
            ## ZH: 模式显示名称的翻译键。
            self.name_i18n_key = name_i18n_key

            ## EN: Translation key for the mode description.
            ## ZH: 模式描述文字的翻译键。
            self.description_i18n_key = description_i18n_key

            ## EN: Mode-specific settings dictionary.
            ## ZH: 模式专属设置字典。
            self.settings = {}

            ## EN: Optional UI metadata used by mode-selection cards
            ##     (provided by mods, e.g. the "Game Modes" mod).
            ## ZH: 模式选择卡片使用的可选 UI 元数据（由 Mod 提供，
            ##     例如 "Game Modes" Mod）。
            self.ui_color = None
            self.ui_icon = None

        def get_name(self):
            """EN: Return translated display name.
               ZH: 返回翻译后的显示名称。"""
            return __(self.name_i18n_key)

        def get_description(self):
            """EN: Return translated description.
               ZH: 返回翻译后的描述。"""
            return __(self.description_i18n_key)

        def on_game_start(self, game):
            """
            EN: Initialize mode-specific state after Game object is created.
                Override in subclasses.
            ZH: Game 对象创建后初始化模式专属状态。子类需覆盖。
            """
            pass

        def can_advance_chapter(self, game):
            """
            EN: Return True if chapter advancement is allowed in this mode.
                Story mode uses goal checks; sandbox may allow free advancement.
            ZH: 返回此模式是否允许章节推进。剧情模式使用目标检查；
                沙盒模式可能允许自由推进。
            """
            return True

        def get_goal_channels(self):
            """
            EN: Return tuple of goal channel names active in this mode.
                Override in subclasses.
            ZH: 返回此模式下激活的目标频道名称元组。子类需覆盖。
            """
            return ()

        def get_available_difficulties(self):
            """
            EN: Return list of difficulty IDs available for this mode.
            ZH: 返回此模式可用的难度 ID 列表。
            """
            return ["非常简单", "简单", "普通", "困难", "噩梦", "自定义"]

        def should_show_intro(self):
            """
            EN: Return True if the intro cinematic should play.
            ZH: 返回是否应播放开场动画。
            """
            return True

        def is_story_locked(self):
            """
            EN: Return True if story events should be gated by chapter progress.
                Story mode = True; Sandbox = False.
            ZH: 返回是否应按章节进度锁定剧情事件。剧情模式=True；沙盒=False。
            """
            return True

        def on_chapter_advanced(self, game, new_chapter):
            """
            EN: Called when the player advances to a new chapter.
                Override for mode-specific chapter behavior.
            ZH: 当玩家推进到新章节时调用。子类可覆盖以实现模式专属行为。
            """
            pass

        def to_dict(self):
            """
            EN: Serialize mode state for save files.
            ZH: 序列化模式状态以保存到存档。
            """
            return {
                "mode_id": self.mode_id,
                "settings": self.settings,
            }

        @classmethod
        def from_dict(cls, data):
            """
            EN: Deserialize mode state from save files.
                Returns an instance of the correct subclass.
            ZH: 从存档反序列化模式状态。返回正确子类的实例。
            """
            mode_id = data.get("mode_id", cls.MODE_STORY)
            mode = gamemode_registry.get(mode_id)
            if mode:
                mode.settings = data.get("settings", {})
                return mode
            return None


    class GameModeRegistry(object):
        """
        EN: Registry for all game mode instances.
            Allows looking up modes by ID and listing available modes.
        ZH: 所有游戏模式实例的注册表。
            支持通过 ID 查找模式和列出可用模式。
        """

        def __init__(self):
            self._modes = {}

        def register(self, mode):
            """EN: Register a game mode instance.
               ZH: 注册一个游戏模式实例。"""
            if not isinstance(mode, GameMode):
                raise TypeError("EN: Expected GameMode instance. ZH: 需要 GameMode 实例。")
            self._modes[mode.mode_id] = mode

        def get(self, mode_id):
            """EN: Get a registered mode by ID, or None.
               ZH: 通过 ID 获取已注册的模式，若无则返回 None。"""
            return self._modes.get(mode_id)

        def list_modes(self):
            """EN: Return list of all registered mode IDs.
               ZH: 返回所有已注册模式 ID 的列表。"""
            return list(self._modes.keys())

        def list_mode_instances(self):
            """EN: Return list of all registered mode instances.
               ZH: 返回所有已注册模式实例的列表。"""
            return list(self._modes.values())


    ## EN: Global game mode registry.
    ## ZH: 全局游戏模式注册表。
    gamemode_registry = GameModeRegistry()
