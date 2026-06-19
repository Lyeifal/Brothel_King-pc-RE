################################################################################
##  Sandbox Mode + Origin System — BK Evolution
##  EN: Free-form gameplay with player origin selection and unique talents.
##  ZH: 自由玩法，支持玩家出身选择和独特天赋。
################################################################################

init -9 python:

    class OriginTalent(object):
        """
        EN: A special talent granted by a player origin.
            Wraps one or more Effect objects for easy application.
        ZH: 出身赋予的特殊天赋。封装一个或多个 Effect 对象以便应用。
        """

        def __init__(self, talent_id, name_i18n_key, description_i18n_key, effects=None):
            ## EN: Unique identifier.
            ## ZH: 唯一标识符。
            self.talent_id = talent_id

            ## EN: Display name translation key.
            ## ZH: 显示名称翻译键。
            self.name_i18n_key = name_i18n_key

            ## EN: Description translation key.
            ## ZH: 描述文字翻译键。
            self.description_i18n_key = description_i18n_key

            ## EN: List of Effect objects applied when this talent is active.
            ## ZH: 此天赋激活时应用的 Effect 对象列表。
            self.effects = effects or []

        def get_name(self):
            return __(self.name_i18n_key)

        def get_description(self):
            return __(self.description_i18n_key)

        def apply(self, target):
            """
            EN: Apply all effects to the target (usually MC or brothel).
            ZH: 将所有效果应用到目标上（通常是 MC 或 brothel）。
            """
            if self.effects:
                add_effects(target, self.effects)

        def remove(self, target):
            """
            EN: Remove all effects from the target.
            ZH: 从目标上移除所有效果。
            """
            if self.effects:
                remove_effects(target, self.effects)


    class PlayerOrigin(object):
        """
        EN: Player background/origin with unique talents.
            Selected at game start in sandbox mode.
        ZH: 玩家出身背景，带有独特天赋。在沙盒模式开始时选择。
        """

        def __init__(self, origin_id, name_i18n_key, description_i18n_key,
                     icon_tag="origin_default", talents=None, starting_bonus=None,
                     available_classes=None):
            ## EN: Unique identifier.
            ## ZH: 唯一标识符。
            self.origin_id = origin_id

            ## EN: Display name translation key.
            ## ZH: 显示名称翻译键。
            self.name_i18n_key = name_i18n_key

            ## EN: Description translation key.
            ## ZH: 描述文字翻译键。
            self.description_i18n_key = description_i18n_key

            ## EN: Image tag for origin icon (looked up in UI).
            ## ZH: 出身图标的图片标签（UI 中查找）。
            self.icon_tag = icon_tag

            ## EN: List of OriginTalent objects.
            ## ZH: OriginTalent 对象列表。
            self.talents = talents or []

            ## EN: Dict of starting bonuses (e.g. {"gold": 500, "reputation": 20}).
            ## ZH: 起始奖励字典（例如 {"gold": 500, "reputation": 20}）。
            self.starting_bonus = starting_bonus or {}

            ## EN: List of available player classes for this origin in sandbox mode.
            ## ZH: 此出身在沙盒模式下可用的主角职业列表。
            self.available_classes = available_classes or []

        def get_name(self):
            return __(self.name_i18n_key)

        def get_description(self):
            return __(self.description_i18n_key)

        def apply_to_mc(self, mc):
            """
            EN: Apply all origin talents to the player character.
            ZH: 将所有出身天赋应用到玩家角色。
            """
            for talent in self.talents:
                talent.apply(mc)

            ## EN: Apply starting bonuses.
            ## ZH: 应用起始奖励。
            if "gold" in self.starting_bonus:
                mc.gold += self.starting_bonus["gold"]
            if "reputation" in self.starting_bonus:
                mc.reputation += self.starting_bonus["reputation"]

        def to_dict(self):
            return {"origin_id": self.origin_id}

        @classmethod
        def from_dict(cls, data):
            origin_id = data.get("origin_id")
            return origin_registry.get(origin_id)


    class OriginRegistry(object):
        """
        EN: Registry for all player origins.
        ZH: 所有玩家出身的注册表。
        """

        def __init__(self):
            self._origins = {}

        def register(self, origin):
            if not isinstance(origin, PlayerOrigin):
                raise TypeError("EN: Expected PlayerOrigin instance. ZH: 需要 PlayerOrigin 实例。")
            self._origins[origin.origin_id] = origin

        def get(self, origin_id):
            return self._origins.get(origin_id)

        def list_origins(self):
            return list(self._origins.values())

        def list_origin_ids(self):
            return list(self._origins.keys())


    ## EN: Global origin registry.
    ## ZH: 全局出身注册表。
    origin_registry = OriginRegistry()


    class SandboxMode(GameMode):
        """
        EN: Sandbox mode — free-form gameplay without forced story progression.
            Features player origin selection and unique talents.
        ZH: 沙盒模式 — 无强制剧情推进的自由玩法。
            支持玩家出身选择和独特天赋。
        """

        def __init__(self):
            super(SandboxMode, self).__init__(
                mode_id=GameMode.MODE_SANDBOX,
                name_i18n_key="沙盒模式",
                description_i18n_key="自由玩法。选择你的出身，在没有剧情锁定的情况下打造自己的道路。"
            )

            ## EN: Currently selected player origin.
            ## ZH: 当前选中的玩家出身。
            self.selected_origin = None

        def on_game_start(self, game):
            """
            EN: Set up sandbox goal channels (fewer story gates).
            ZH: 设置沙盒目标频道（更少的剧情锁定）。
            """
            game.goal_channels = ("advance", "advance2", "contract", "other")

            ## EN: Apply origin talents if an origin was selected.
            ## ZH: 如果选择了出身，应用出身天赋。
            if self.selected_origin and MC:
                self.selected_origin.apply_to_mc(MC)

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

        def set_origin(self, origin):
            """
            EN: Set the player's origin before game start.
            ZH: 在游戏开始前设置玩家出身。
            """
            self.selected_origin = origin

        def get_origin(self):
            """EN: Get the currently selected origin.
               ZH: 获取当前选中的出身。"""
            return self.selected_origin

        def to_dict(self):
            data = super(SandboxMode, self).to_dict()
            if self.selected_origin:
                data["selected_origin"] = self.selected_origin.to_dict()
            return data

        @classmethod
        def from_dict(cls, data):
            mode = SandboxMode()
            mode.settings = data.get("settings", {})
            origin_data = data.get("selected_origin")
            if origin_data:
                mode.selected_origin = PlayerOrigin.from_dict(origin_data)
            return mode


    ## EN: Register sandbox mode in the global registry.
    ## ZH: 在全局注册表中注册沙盒模式。
    gamemode_registry.register(SandboxMode())


## EN: Built-in origins are now loaded from game/core/data/sandbox/origins.json via DataLoader.
## ZH: 内置出身现在通过 DataLoader 从 game/core/data/sandbox/origins.json 加载。
##     See DataLoader.load_origins() in game/core/systems/data_loader.rpy

