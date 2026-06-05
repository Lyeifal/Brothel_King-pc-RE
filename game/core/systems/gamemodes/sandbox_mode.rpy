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
                     icon_tag="origin_default", talents=None, starting_bonus=None):
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


## EN: Built-in default origins. Deferred to init -1 so Effect class is available.
## ZH: 内置默认出身。延迟到 init -1 以确保 Effect 类已加载。
init -1 python:

    origin_registry.register(PlayerOrigin(
        origin_id="fallen_noble",
        name_i18n_key="落魄贵族",
        description_i18n_key="曾经受人尊敬的贵族，如今落魄失势。起始声望高但资金有限。",
        icon_tag="origin_noble",
        talents=[
            OriginTalent(
                talent_id="noble_bearing",
                name_i18n_key="贵族气质",
                description_i18n_key="声望获取增加50%%。",
                effects=[Effect("boost", "reputation", 0.5)]
            ),
        ],
        starting_bonus={"reputation": 30}
    ))

    origin_registry.register(PlayerOrigin(
        origin_id="street_thug",
        name_i18n_key="街头混混",
        description_i18n_key="在贫民窟长大。 ruthless 且足智多谋。掳走更容易，但人们不太信任你。",
        icon_tag="origin_thug",
        talents=[
            OriginTalent(
                talent_id="underworld_connections",
                name_i18n_key="地下关系",
                description_i18n_key="掳走成功率+20%%。起始邪恶声望+10。",
                effects=[Effect("boost", "kidnap success", 0.2)]
            ),
        ],
        starting_bonus={"evil": 10}
    ))

    origin_registry.register(PlayerOrigin(
        origin_id="merchant_family",
        name_i18n_key="商人世家",
        description_i18n_key="出身贸易世家。你懂得讨价还价和发现好买卖。",
        icon_tag="origin_merchant",
        talents=[
            OriginTalent(
                talent_id="sharp_deal",
                name_i18n_key="精明交易",
                description_i18n_key="商店价格降低15%%。",
                effects=[Effect("boost", "shop prices", -0.15)]
            ),
        ],
        starting_bonus={"gold": 500}
    ))

    origin_registry.register(PlayerOrigin(
        origin_id="wandering_mage",
        name_i18n_key="流浪法师",
        description_i18n_key="一个自学成才的施法者，寻求财富。女孩们被你神秘的气质所吸引。",
        icon_tag="origin_mage",
        talents=[
            OriginTalent(
                talent_id="arcane_charm",
                name_i18n_key="神秘魅力",
                description_i18n_key="法术学习速度+30%%。起始额外获得一个女孩。",
                effects=[Effect("boost", "spell learning", 0.3)]
            ),
        ],
        starting_bonus={}
    ))

    origin_registry.register(PlayerOrigin(
        origin_id="pirate_captain",
        name_i18n_key="海盗船长",
        description_i18n_key="私掠船的前船长。异域女孩觉得你很有魅力，但安保成本更高。",
        icon_tag="origin_pirate",
        talents=[
            OriginTalent(
                talent_id="exotic_allure",
                name_i18n_key="异域诱惑",
                description_i18n_key="特殊女孩遭遇率+10%%。",
                effects=[Effect("boost", "special girl chance", 0.1)]
            ),
            OriginTalent(
                talent_id="loose_crew",
                name_i18n_key="散漫船员",
                description_i18n_key="安保维护费用增加20%%。",
                effects=[Effect("boost", "security upkeep", 0.2)]
            ),
        ],
        starting_bonus={}
    ))
