################################################################################
##  Scenario Mode — BK Evolution
##  EN: Community-driven scenario framework. Not a built-in play mode,
##      but a platform for Mod authors to create custom campaigns.
##  ZH: 社区驱动的剧本框架。不是内置玩法，而是供 Mod 作者创作
##      自定义战役的平台。
################################################################################

init -9 python:

    class Scenario(object):
        """
        EN: A community-created scenario pack. Mod authors subclass this
            or provide a compatible dict to register_scenario().
        ZH: 社区创作的剧本包。Mod 作者可以继承此类或提供兼容的字典
            给 register_scenario()。
        """

        def __init__(self, scenario_id, name_i18n_key, description_i18n_key,
                     author="", version="1.0",
                     rules=None, events_script="scenario_default",
                     starting_conditions=None, victory_conditions=None):
            ## EN: Unique identifier (namespace prefix recommended: "author.scenario_name").
            ## ZH: 唯一标识符（建议带命名空间前缀："作者.剧本名"）。
            self.scenario_id = scenario_id

            self.name_i18n_key = name_i18n_key
            self.description_i18n_key = description_i18n_key
            self.author = author
            self.version = version

            ## EN: Dict of custom rules overriding default gameplay.
            ## ZH: 覆盖默认玩法的自定义规则字典。
            self.rules = rules or {}

            ## EN: Ren'Py label name for scenario-specific events.
            ## ZH: 剧本专属事件的 Ren'Py 标签名。
            self.events_script = events_script

            ## EN: Dict of starting conditions (gold, girls, chapter, etc.).
            ## ZH: 起始条件字典（金钱、女孩、章节等）。
            self.starting_conditions = starting_conditions or {}

            ## EN: List of victory condition dicts.
            ## ZH: 胜利条件字典列表。
            self.victory_conditions = victory_conditions or []

        def get_name(self):
            return __(self.name_i18n_key)

        def get_description(self):
            return __(self.description_i18n_key)

        def apply_starting_conditions(self, game, mc):
            """
            EN: Override starting values based on scenario rules.
            ZH: 根据剧本规则覆盖起始值。
            """
            cond = self.starting_conditions
            if "gold" in cond:
                mc.gold = cond["gold"]
            if "chapter" in cond:
                game.chapter = cond["chapter"]
            if "girls" in cond:
                for _ in range(cond["girls"]):
                    g = get_rand_girl()
                    if g:
                        mc.girls.append(g)
                        g.init_after_acquire()

        def check_victory(self, game, mc):
            """
            EN: Return True if any victory condition is met.
                Override for custom logic.
            ZH: 如果有任何胜利条件达成则返回 True。子类可覆盖自定义逻辑。
            """
            for vc in self.victory_conditions:
                if self._check_single_condition(vc, game, mc):
                    return True
            return False

        def _check_single_condition(self, condition, game, mc):
            """
            EN: Check a single victory condition dict.
                Supported keys: "gold_min", "reputation_min", "girls_min", "chapter_min", "custom_label"
            ZH: 检查单个胜利条件字典。
                支持的键："gold_min", "reputation_min", "girls_min", "chapter_min", "custom_label"
            """
            if "gold_min" in condition and mc.gold < condition["gold_min"]:
                return False
            if "reputation_min" in condition and getattr(mc, "reputation", 0) < condition["reputation_min"]:
                return False
            if "girls_min" in condition and len(mc.girls) < condition["girls_min"]:
                return False
            if "chapter_min" in condition and game.chapter < condition["chapter_min"]:
                return False
            if "custom_label" in condition:
                return renpy.call_in_new_context(condition["custom_label"])
            return True

        def to_dict(self):
            return {
                "scenario_id": self.scenario_id,
                "name_i18n_key": self.name_i18n_key,
                "description_i18n_key": self.description_i18n_key,
                "author": self.author,
                "version": self.version,
                "rules": self.rules,
                "events_script": self.events_script,
                "starting_conditions": self.starting_conditions,
                "victory_conditions": self.victory_conditions,
            }

        @classmethod
        def from_dict(cls, data):
            return cls(
                scenario_id=data.get("scenario_id", "unknown"),
                name_i18n_key=data.get("name_i18n_key", "未知剧本"),
                description_i18n_key=data.get("description_i18n_key", ""),
                author=data.get("author", ""),
                version=data.get("version", "1.0"),
                rules=data.get("rules", {}),
                events_script=data.get("events_script", "scenario_default"),
                starting_conditions=data.get("starting_conditions", {}),
                victory_conditions=data.get("victory_conditions", []),
            )


    class ScenarioRegistry(object):
        """
        EN: Registry for community scenarios.
        ZH: 社区剧本的注册表。
        """

        def __init__(self):
            self._scenarios = {}

        def register(self, scenario):
            if isinstance(scenario, dict):
                scenario = Scenario.from_dict(scenario)
            if not isinstance(scenario, Scenario):
                raise TypeError("EN: Expected Scenario instance or dict. ZH: 需要 Scenario 实例或字典。")
            self._scenarios[scenario.scenario_id] = scenario

        def get(self, scenario_id):
            return self._scenarios.get(scenario_id)

        def list_scenarios(self):
            return list(self._scenarios.values())

        def list_scenario_ids(self):
            return list(self._scenarios.keys())


    ## EN: Global scenario registry.
    ## ZH: 全局剧本注册表。
    scenario_registry = ScenarioRegistry()


    class ScenarioMode(GameMode):
        """
        EN: Scenario mode — loads a community-created scenario.
            Inherits from sandbox but applies scenario-specific rules.
        ZH: 剧本模式 — 加载社区创作的剧本。
            继承沙盒模式但应用剧本专属规则。
        """

        def __init__(self):
            super(ScenarioMode, self).__init__(
                mode_id=GameMode.MODE_SCENARIO,
                name_i18n_key="剧本模式",
                description_i18n_key="游玩社区创作的剧本，包含自定义规则和胜利条件。"
            )
            self.selected_scenario = None

        def on_game_start(self, game):
            """
            EN: Apply scenario starting conditions and set up goal channels.
            ZH: 应用剧本起始条件并设置目标频道。
            """
            game.goal_channels = ("advance", "advance2", "contract", "other")

            if self.selected_scenario and MC:
                self.selected_scenario.apply_starting_conditions(game, MC)

        def can_advance_chapter(self, game):
            return True

        def get_goal_channels(self):
            return ("advance", "advance2", "contract", "other")

        def is_story_locked(self):
            return False

        def set_scenario(self, scenario):
            """EN: Set the active scenario before game start.
               ZH: 在游戏开始前设置激活的剧本。"""
            self.selected_scenario = scenario

        def get_scenario(self):
            return self.selected_scenario

        def check_victory(self, game, mc):
            """EN: Delegate victory check to the active scenario.
               ZH: 将胜利检查委托给激活的剧本。"""
            if self.selected_scenario:
                return self.selected_scenario.check_victory(game, mc)
            return False

        def to_dict(self):
            data = super(ScenarioMode, self).to_dict()
            if self.selected_scenario:
                data["selected_scenario"] = self.selected_scenario.to_dict()
            return data

        @classmethod
        def from_dict(cls, data):
            mode = ScenarioMode()
            mode.settings = data.get("settings", {})
            sc_data = data.get("selected_scenario")
            if sc_data:
                mode.selected_scenario = Scenario.from_dict(sc_data)
            return mode


    ## EN: Register scenario mode in the global registry.
    ## ZH: 在全局注册表中注册剧本模式。
    gamemode_registry.register(ScenarioMode())
