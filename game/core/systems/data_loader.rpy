################################################################################
##  DataLoader — BK Evolution
##  EN: Loads JSON data files from game/custom/data/ into game registries.
##  ZH: 从 game/custom/data/ 加载 JSON 数据文件到游戏注册表。
################################################################################

init -1 python:

    import json

    class DataLoader(object):
        """
        EN: Unified loader for all JSON-driven content.
            Loads traits, perks, origins, story events, and scenarios
            from game/custom/data/ into their respective registries.
        ZH: 所有 JSON 驱动内容的统一加载器。
            从 game/custom/data/ 加载特质、天赋、出身、剧情事件和剧本
            到各自的注册表中。
        """

        DATA_DIR = "custom/data"

        @classmethod
        def load_all(cls):
            """EN: Load all JSON data categories.
               ZH: 加载所有 JSON 数据类别。"""
            cls.load_traits()
            cls.load_perks()
            cls.load_origins()
            cls.load_story_events()
            cls.load_sandbox_events()
            cls.load_scenarios()

        @classmethod
        def _load_json_file(cls, rel_path):
            """
            EN: Safely load a JSON file from DATA_DIR.
                Returns None if file doesn't exist or is invalid.
            ZH: 安全地从 DATA_DIR 加载 JSON 文件。
                若文件不存在或无效则返回 None。
            """
            full_path = cls.DATA_DIR + "/" + rel_path
            if not renpy.loadable(full_path):
                return None
            try:
                data = renpy.open_file(full_path).read()
                return json.loads(data)
            except Exception as e:
                renpy.notify("DataLoader error loading %s: %s" % (rel_path, str(e)))
                return None

        @classmethod
        def load_traits(cls):
            """EN: Load traits from JSON and register them.
               ZH: 从 JSON 加载特质并注册。"""
            data = cls._load_json_file("traits/traits.json")
            if not data:
                return
            for item in data:
                try:
                    trait = Trait.from_dict(item)
                    trait_registry.register(trait)
                except Exception as e:
                    renpy.notify("Trait load error: %s" % str(e))

        @classmethod
        def load_perks(cls):
            """EN: Load perks from JSON and register them.
               ZH: 从 JSON 加载天赋并注册。"""
            data = cls._load_json_file("perks/perks.json")
            if not data:
                return
            for item in data:
                try:
                    perk = Perk.from_dict(item)
                    perk_registry.register(perk)
                except Exception as e:
                    renpy.notify("Perk load error: %s" % str(e))

        @classmethod
        def load_origins(cls):
            """EN: Load player origins from JSON and register them.
               ZH: 从 JSON 加载玩家出身并注册。"""
            data = cls._load_json_file("sandbox/origins.json")
            if not data:
                return
            for item in data:
                try:
                    origin = PlayerOrigin(
                        origin_id=item["origin_id"],
                        name_i18n_key=item.get("name", item["origin_id"]),
                        description_i18n_key=item.get("description", ""),
                        icon_tag=item.get("icon_tag", "origin_default"),
                        talents=cls._parse_talents(item.get("talents", [])),
                        starting_bonus=item.get("starting_bonus", {}),
                    )
                    origin_registry.register(origin)
                except Exception as e:
                    renpy.notify("Origin load error: %s" % str(e))

        @classmethod
        def _parse_talents(cls, talent_list):
            """EN: Parse a list of talent dicts into OriginTalent objects.
               ZH: 将天赋字典列表解析为 OriginTalent 对象。"""
            talents = []
            for t in talent_list:
                effects = []
                for eff in t.get("effects", []):
                    effects.append(Effect(
                        type=eff.get("type", "boost"),
                        target=eff.get("target"),
                        value=eff.get("value", 0),
                        scope=eff.get("scope"),
                    ))
                talents.append(OriginTalent(
                    talent_id=t["talent_id"],
                    name_i18n_key=t.get("name", t["talent_id"]),
                    description_i18n_key=t.get("description", ""),
                    effects=effects,
                ))
            return talents

        @classmethod
        def load_story_events(cls):
            """EN: Load story-mode events from JSON into event_dict.
               ZH: 从 JSON 加载剧情模式事件到 event_dict。"""
            data = cls._load_json_file("stories/story_events.json")
            if not data:
                return
            for item in data:
                try:
                    ev = StoryEvent(
                        label=item["label"],
                        chapter=item.get("chapter", 0),
                        rank=item.get("rank", 0),
                        date=item.get("date", 0),
                        year=item.get("year", 0),
                        month=item.get("month", 0),
                        day=item.get("day", 0),
                        weekday=item.get("weekday", ""),
                        chance=item.get("chance", 1.0),
                        type=item.get("type", "any"),
                        location=item.get("location"),
                        locations=item.get("locations"),
                        seasons=item.get("seasons"),
                        min_gold=item.get("min_gold", -999999999),
                        condition=item.get("condition"),
                        not_condition=item.get("not_condition"),
                        once=item.get("once", True),
                        AP_cost=item.get("AP_cost", 1),
                        order=item.get("order", 0),
                        call_args=item.get("call_args", []),
                    )
                    ## EN: Store modes as custom attribute for filtering.
                    ## ZH: 将模式存储为自定义属性用于筛选。
                    ev.modes = item.get("modes", ["story"])
                    event_dict[item["label"]] = ev
                except Exception as e:
                    renpy.notify("StoryEvent load error: %s" % str(e))

        @classmethod
        def load_sandbox_events(cls):
            """EN: Load sandbox-mode exclusive events from JSON.
               ZH: 从 JSON 加载沙盒模式专属事件。"""
            data = cls._load_json_file("sandbox/events.json")
            if not data:
                return
            for item in data:
                try:
                    ev = StoryEvent(
                        label=item["label"],
                        chapter=item.get("chapter", 0),
                        rank=item.get("rank", 0),
                        date=item.get("date", 0),
                        chance=item.get("chance", 1.0),
                        type=item.get("type", "any"),
                        location=item.get("location"),
                        condition=item.get("condition"),
                        not_condition=item.get("not_condition"),
                        once=item.get("once", True),
                        AP_cost=item.get("AP_cost", 1),
                        order=item.get("order", 0),
                        call_args=item.get("call_args", []),
                    )
                    ev.modes = item.get("modes", ["sandbox"])
                    event_dict[item["label"]] = ev
                except Exception as e:
                    renpy.notify("SandboxEvent load error: %s" % str(e))

        @classmethod
        def load_scenarios(cls):
            """EN: Load community scenarios from JSON and register them.
               ZH: 从 JSON 加载社区剧本并注册。"""
            data = cls._load_json_file("scenarios/scenarios.json")
            if not data:
                return
            for item in data:
                try:
                    sc = Scenario(
                        scenario_id=item["scenario_id"],
                        name_i18n_key=item.get("name", item["scenario_id"]),
                        description_i18n_key=item.get("description", ""),
                        author=item.get("author", ""),
                        version=item.get("version", "1.0"),
                        rules=item.get("rules", {}),
                        events_script=item.get("events_script", "scenario_default"),
                        starting_conditions=item.get("starting_conditions", {}),
                        victory_conditions=item.get("victory_conditions", []),
                    )
                    scenario_registry.register(sc)
                except Exception as e:
                    renpy.notify("Scenario load error: %s" % str(e))
