################################################################################
##  DataLoader — BK Evolution
##  EN: Loads JSON data files from game/core/data/ into game registries.
##  ZH: 从 game/core/data/ 加载 JSON 数据文件到游戏注册表。
################################################################################

init -11 python:

    import json

    class DataLoader(object):
        """
        EN: Unified loader for all JSON-driven content.
            Loads traits, perks, origins, story events, and scenarios
            from game/core/data/ into their respective registries.
            JSON files are parsed only once per session and cached.
        ZH: 所有 JSON 驱动内容的统一加载器。
            从 game/core/data/ 加载特质、天赋、出身、剧情事件和剧本
            到各自的注册表中。
            JSON 文件每个会话只解析一次并缓存。
        """

        DATA_DIR = "core/data"
        _loaded = set()  # EN: Tracks which files have been loaded. ZH: 记录已加载的文件。

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
            cls.load_achievements()
            cls.load_challenges()
            cls.load_difficulty()
            cls.load_ngp_settings()
            cls.load_meta_progression()

        @classmethod
        def reset_cache(cls):
            """EN: Clear load cache. Call this if JSON files changed at runtime.
               ZH: 清除加载缓存。如果 JSON 文件在运行时发生变化则调用此方法。"""
            cls._loaded.clear()

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
                renpy.notify(__("DataLoader error loading %s: %s") % (rel_path, str(e)))
                return None

        @classmethod
        def load_traits(cls):
            """EN: Load traits from JSON and register them.
               ZH: 从 JSON 加载特质并注册。"""
            path = "traits/traits.json"
            if path in cls._loaded:
                return
            data = cls._load_json_file(path)
            if not data:
                return
            cls._loaded.add(path)
            for item in data:
                try:
                    trait = Trait.from_dict(item)
                    trait_registry.register_trait(trait, category=item.get("category"))
                except Exception as e:
                    renpy.notify(__("Trait load error: %s") % str(e))

        @classmethod
        def load_perks(cls):
            """EN: Load perks from JSON and register them.
               ZH: 从 JSON 加载天赋并注册。"""
            path = "perks/perks.json"
            if path in cls._loaded:
                return
            data = cls._load_json_file(path)
            if not data:
                return
            cls._loaded.add(path)
            for item in data:
                try:
                    perk = Perk.from_dict(item)
                    perk_registry.register_perk(perk, category=item.get("archetype"))
                except Exception as e:
                    renpy.notify(__("Perk load error: %s") % str(e))

        @classmethod
        def load_origins(cls):
            """EN: Load player origins from JSON and register them.
               ZH: 从 JSON 加载玩家出身并注册。"""
            path = "sandbox/origins.json"
            if path in cls._loaded:
                return
            data = cls._load_json_file(path)
            if not data:
                return
            cls._loaded.add(path)
            for item in data:
                try:
                    origin = PlayerOrigin(
                        origin_id=item["origin_id"],
                        name_i18n_key=get_i18n_raw(item, "name", item["origin_id"]),
                        description_i18n_key=get_i18n_raw(item, "description", ""),
                        icon_tag=item.get("icon_tag", "origin_default"),
                        talents=cls._parse_talents(item.get("talents", [])),
                        starting_bonus=item.get("starting_bonus", {}),
                        available_classes=item.get("available_classes"),
                    )
                    origin_registry.register(origin)
                except Exception as e:
                    renpy.notify(__("Origin load error: %s") % str(e))

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
                    name_i18n_key=get_i18n_raw(t, "name", t["talent_id"]),
                    description_i18n_key=get_i18n_raw(t, "description", ""),
                    effects=effects,
                ))
            return talents

        @classmethod
        def load_story_events(cls):
            """EN: Load story events from JSON and add them to event_dict.
               ZH: 从 JSON 加载剧情事件并加入 event_dict。"""
            path = "story/events.json"
            if path in cls._loaded:
                return
            data = cls._load_json_file(path)
            if not data:
                return
            cls._loaded.add(path)
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
                        locations=item.get("locations"),
                        seasons=item.get("seasons"),
                        min_gold=item.get("min_gold", 0),
                        condition=item.get("condition"),
                        not_condition=item.get("not_condition"),
                        once=item.get("once", True),
                        AP_cost=item.get("AP_cost", 1),
                        order=item.get("order", 0),
                        call_args=item.get("call_args", []),
                    )
                    ev.modes = item.get("modes", ["story"])
                    event_dict[item["label"]] = ev
                except Exception as e:
                    renpy.notify(__("StoryEvent load error: %s") % str(e))

        @classmethod
        def load_sandbox_events(cls):
            """EN: Load sandbox events from JSON and add them to event_dict.
               ZH: 从 JSON 加载沙盒事件并加入 event_dict。"""
            path = "sandbox/events.json"
            if path in cls._loaded:
                return
            data = cls._load_json_file(path)
            if not data:
                return
            cls._loaded.add(path)
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
                    renpy.notify(__("SandboxEvent load error: %s") % str(e))

        @classmethod
        def load_scenarios(cls):
            """EN: Load community scenarios from JSON and register them.
               ZH: 从 JSON 加载社区剧本并注册。"""
            path = "scenarios/scenarios.json"
            if path in cls._loaded:
                return
            data = cls._load_json_file(path)
            if not data:
                return
            cls._loaded.add(path)
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
                    renpy.notify(__("Scenario load error: %s") % str(e))

        @classmethod
        def load_achievements(cls):
            """EN: Load achievements from JSON into achievement_list/dict.
               ZH: 从 JSON 加载成就到 achievement_list/dict。"""
            path = "achievements/achievements.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            result = []
            for target, item in data.items():
                try:
                    item["target"] = target
                    ach = Achievement.from_dict(item)
                    result.append(ach)
                except Exception as e:
                    renpy.notify(__("Achievement load error: %s") % str(e))
            return result

        @classmethod
        def load_resources(cls, location_resolver=None):
            """EN: Load resources from JSON.
               ZH: 从 JSON 加载资源。
               location_resolver: callable that maps location name strings to Location objects."""
            path = "resources/resources.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            result = {}
            for key, item in data.items():
                try:
                    result[key] = Resource.from_dict(item, location_resolver=location_resolver)
                except Exception as e:
                    renpy.notify(__("Resource load error: %s") % str(e))
            return result

        @classmethod
        def load_contracts(cls, character_resolver=None):
            """EN: Load contract templates from JSON.
               ZH: 从 JSON 加载契约模板。
               character_resolver: callable that maps character name strings to Character objects."""
            path = "contracts/contracts.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            result = []
            for item in data:
                try:
                    result.append(Contract.from_dict(item, character_resolver=character_resolver))
                except Exception as e:
                    renpy.notify(__("Contract load error: %s") % str(e))
            return result

        @classmethod
        def load_challenges(cls):
            """EN: Load MC challenges from JSON.
               ZH: 从 JSON 加载 MC 挑战。"""
            path = "challenges/challenges.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            result = {}
            for key, item in data.items():
                try:
                    result[key] = MC_challenge.from_dict(item)
                except Exception as e:
                    renpy.notify(__("Challenge load error: %s") % str(e))
            return result

        @classmethod
        def load_cleanliness_penalties(cls):
            """EN: Load cleanliness penalty definitions from JSON.
               ZH: 从 JSON 加载清洁度惩罚定义。"""
            path = "settings/cleanliness_penalties.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            return data

        @classmethod
        def load_treasure_thresholds(cls):
            """EN: Load treasure picture thresholds from JSON.
               ZH: 从 JSON 加载宝藏图片阈值。"""
            path = "settings/treasure_thresholds.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            return data.get("thresholds", [])

        @classmethod
        def load_difficulty(cls):
            """EN: Load difficulty tables from JSON.
               ZH: 从 JSON 加载难度表。"""
            path = "difficulty/difficulty.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            return data

        @classmethod
        def load_goal_ui(cls):
            """EN: Load goal UI constants (channels, categories, colors) from JSON.
               ZH: 从 JSON 加载目标 UI 常量（通道、分类、颜色）。"""
            path = "goals/goal_ui.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            return data

        @classmethod
        def load_fixations(cls):
            """EN: Load fixation definitions from JSON.
               ZH: 从 JSON 加载癖好/执念定义。"""
            path = "fixations/fixations.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            result = {}
            for key, fix_data in data.get("fixations", {}).items():
                try:
                    result[key] = Fixation.from_dict(fix_data)
                except Exception as e:
                    if config.developer:
                        print("[Fixation] Load error for '%s': %s" % (key, e))
            return result

        @classmethod
        def _load_interaction_dict(cls, path):
            """EN: Helper to load an interaction menu dict (interact_dict or free_interact_dict) from JSON.
               ZH: 辅助方法：从 JSON 加载交互菜单字典。"""
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            result = {}
            for key, menu_data in data.get("menus", {}).items():
                kind = menu_data.get("kind")
                if kind == "submenu":
                    result[key] = menu_data.get("items", [])
                elif kind == "topics":
                    topics = []
                    for item in menu_data.get("items", []):
                        try:
                            topics.append(GirlInteractionTopic.from_dict(item))
                        except Exception as e:
                            if config.developer:
                                print("[Interaction] Load error for '%s': %s" % (key, e))
                    result[key] = topics
            return result

        @classmethod
        def load_interact_dict(cls):
            """EN: Load slave girl interaction menu from JSON.
               ZH: 从 JSON 加载奴隶女孩交互菜单。"""
            return cls._load_interaction_dict("interactions/interact_dict.json")

        @classmethod
        def load_free_interact_dict(cls):
            """EN: Load free girl interaction menu from JSON.
               ZH: 从 JSON 加载自由女孩交互菜单。"""
            return cls._load_interaction_dict("interactions/free_interact_dict.json")

        @classmethod
        def load_ngp_settings(cls):
            """EN: Load NG+ settings from JSON.
               ZH: 从 JSON 加载 NG+ 设置。"""
            path = "ngp/ngp_settings.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            result = []
            for item in data:
                try:
                    ngp = NGPSetting.from_dict(item)
                    result.append(ngp)
                except Exception as e:
                    renpy.notify(__("NGP load error: %s") % str(e))
            return result

        @classmethod
        def load_meta_progression(cls):
            """EN: Load meta progression upgrades from JSON.
               ZH: 从 JSON 加载局外养成升级。"""
            path = "meta/meta_progression.json"
            if path in cls._loaded:
                return None
            data = cls._load_json_file(path)
            if not data:
                return None
            cls._loaded.add(path)
            result = []
            for item in data.get("meta_upgrades", []):
                try:
                    upgrade = MetaUpgrade.from_dict(item)
                    meta_registry.register_meta(upgrade.upgrade_id, upgrade)
                    result.append(upgrade)
                except Exception as e:
                    renpy.notify(__("Meta progression load error: %s") % str(e))
            return result

        @classmethod
        def load_items(cls, item_type="all"):
            """EN: Load items from JSON.
               ZH: 从 JSON 加载物品。"""
            path = "items/items.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            key = "template_items" if item_type == "template" else "all_items"
            result = []
            for item in data.get(key, []):
                try:
                    result.append(Item.from_dict(item))
                except Exception as e:
                    renpy.notify(__("Item load error: %s") % str(e))
            return result

        @classmethod
        def load_perform_job_dict(cls):
            """EN: Load perform_job_dict from JSON.
               ZH: 从 JSON 加载 perform_job_dict。"""
            path = "jobs/perform_job_dict.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_brothel_params(cls):
            """EN: Load brothel parameters from JSON.
               ZH: 从 JSON 加载青楼参数。"""
            path = "economy/brothel_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            # Convert string keys to int for chapter-based dicts
            int_key_fields = ("bro_capacity", "bro_helpers", "bro_reputation_cap", "bro_cost", "brothel_pics")
            for field in int_key_fields:
                if field in data:
                    data[field] = {int(k): v for k, v in data[field].items()}
            return data

        @classmethod
        def load_rooms(cls):
            """EN: Load room definitions and picture mappings from JSON.
               ZH: 从 JSON 加载房间定义和图片映射。"""
            path = "rooms/rooms.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            # Convert string keys to int where appropriate
            int_key_fields = ("bedrooms", "master_bedrooms", "room_capacity")
            for field in int_key_fields:
                if field in data:
                    data[field] = {int(k): v for k, v in data[field].items()}
            return data

        @classmethod
        def load_powers(cls):
            """EN: Load evil power definitions from JSON.
               ZH: 从 JSON 加载邪恶力量定义。"""
            path = "powers/powers.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_shops(cls):
            """EN: Load shop definitions from JSON.
               ZH: 从 JSON 加载商店定义。"""
            path = "shops/shops.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            # Convert upgrade keys to int
            if "upgrades" in data:
                data["upgrades"] = {int(k): v for k, v in data["upgrades"].items()}
            # Convert restock_cost keys to int for each shop
            for shop in data.get("shops", []):
                if "restock_cost" in shop:
                    shop["restock_cost"] = {int(k): v for k, v in shop["restock_cost"].items()}
            return data

        @classmethod
        def load_mc_classes(cls):
            """EN: Load MC class definitions and spellbooks from JSON.
               ZH: 从 JSON 加载主角职业定义和法术书。"""
            path = "classes/mc_classes.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_spells(cls):
            """EN: Load spellbook, moons, and shield spells from JSON.
               ZH: 从 JSON 加载法术书、月亮和护盾法术。"""
            path = "spells/spells.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            # Convert moon keys to int
            if "moons" in data:
                data["moons"] = {int(k): v for k, v in data["moons"].items()}
            return data

        @classmethod
        def load_shop_economy(cls):
            """EN: Load shop economy parameters from JSON.
               ZH: 从 JSON 加载商店经济参数。"""
            path = "shops/shop_economy.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            # Convert string keys to int
            for field in ("chapter_price_multiplier", "chapter_stock_bonus"):
                if field in data:
                    data[field] = {int(k): v for k, v in data[field].items()}
            return data

        @classmethod
        def load_tax_params(cls):
            """EN: Load tax parameters from JSON.
               ZH: 从 JSON 加载税收参数。"""
            path = "economy/tax_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            # Convert string keys to int for chapter-based dicts
            if "tax_chapter_penalty" in data:
                data["tax_chapter_penalty"] = {int(k): v for k, v in data["tax_chapter_penalty"].items()}
            return data

        @classmethod
        def load_minions(cls):
            """EN: Load minion definitions from JSON.
               ZH: 从 JSON 加载仆从定义。"""
            path = "minions/minions.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            # Convert string keys to int for level-based dicts
            for field in ("minion_xp_to_level", "minion_price"):
                if field in data:
                    data[field] = {int(k): v for k, v in data[field].items()}
            return data

        @classmethod
        def load_installations(cls):
            """EN: Load farm installation parameters from JSON.
               ZH: 从 JSON 加载农场安装参数。"""
            path = "farm/installations.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            # Convert string keys to int for rank-based dicts
            if "installation_price" in data:
                data["installation_price"] = {int(k): v for k, v in data["installation_price"].items()}
            return data

        @classmethod
        def load_farm_perform_dict(cls):
            """EN: Load farm performance text dictionary from JSON.
               ZH: 从 JSON 加载农场表演文本字典。"""
            path = "farm/farm_perform_dict.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_farm_descriptions(cls):
            """EN: Load farm event description texts from JSON.
               ZH: 从 JSON 加载农场事件描述文本。"""
            path = "farm/farm_descriptions.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_stat_increase_dict(cls):
            """EN: Load stat increase text dictionary from JSON.
               ZH: 从 JSON 加载属性增长文本字典。"""
            path = "settings/stat_increase_dict.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_maintenance_desc(cls):
            """EN: Load maintenance description text from JSON.
               ZH: 从 JSON 加载维护描述文本。"""
            path = "settings/maintenance_desc.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_gossip(cls):
            """EN: Load gossip text from JSON.
               ZH: 从 JSON 加载流言文本。"""
            path = "settings/gossip.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_dialogue_texts(cls):
            """EN: Load jokes and compliments from JSON.
               ZH: 从 JSON 加载笑话和赞美语文本。"""
            path = "settings/dialogue_texts.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_recent_events(cls):
            """EN: Load recent event templates from JSON.
               ZH: 从 JSON 加载近期事件模板。"""
            path = "settings/recent_events.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_event_texts(cls):
            """EN: Load log events and attraction descriptions from JSON.
               ZH: 从 JSON 加载日志事件和吸引力描述文本。"""
            path = "settings/event_texts.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_roll_results(cls):
            """EN: Load roll and result dictionaries from JSON.
               ZH: 从 JSON 加载掷骰和结果字典。"""
            path = "settings/roll_results.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_quality(cls):
            """EN: Load quality prefix and modifier tables from JSON.
               ZH: 从 JSON 加载品质前缀和修正值表。"""
            path = "settings/quality.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_girl_descriptions(cls):
            """EN: Load mood/love/fear description dictionaries from JSON.
               ZH: 从 JSON 加载心情/爱意/恐惧描述字典。"""
            path = "settings/girl_descriptions.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_merchants(cls):
            """EN: Load merchant dialogue and title data from JSON.
               ZH: 从 JSON 加载商人对话和头衔数据。"""
            path = "settings/merchants.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_rankings(cls):
            """EN: Load brothel ranking reputation titles from JSON.
               ZH: 从 JSON 加载青楼声望等级头衔。"""
            path = "settings/rankings.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_threat_params(cls):
            """EN: Load event sounds and gold threat parameters from JSON.
               ZH: 从 JSON 加载事件音效和金币威胁参数。"""
            path = "settings/threat_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_sex_descriptions(cls):
            """EN: Load preference responses and act descriptions from JSON.
               ZH: 从 JSON 加载偏好反应和性行为描述文本。"""
            path = "settings/sex_descriptions.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_misc_texts(cls):
            """EN: Load miscellaneous UI texts from JSON.
               ZH: 从 JSON 加载杂项 UI 文本。"""
            path = "settings/misc_texts.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_small_texts(cls):
            """EN: Load small UI text dictionaries from JSON.
               ZH: 从 JSON 加载小型 UI 文本字典。"""
            path = "settings/small_texts.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_contract_tasks(cls):
            """EN: Load contract task definitions from JSON.
               ZH: 从 JSON 加载契约任务定义。"""
            path = "settings/contracts.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_mc_descriptions(cls):
            """EN: Load MC class/stat/god/alignment descriptions from JSON.
               ZH: 从 JSON 加载主角职业/属性/神祇/阵营描述。"""
            path = "settings/mc_descriptions.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_tags(cls):
            """EN: Load TagRegistry tag_dict from JSON.
               ZH: 从 JSON 加载 TagRegistry 标签字典。"""
            path = "settings/tags.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_picture_mappings(cls):
            """EN: Load event/UI picture filename mappings from JSON.
               ZH: 从 JSON 加载事件/UI 图片文件名映射。"""
            path = "settings/picture_mappings.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_help_texts(cls):
            """EN: Load help system texts and picture mappings from JSON.
               ZH: 从 JSON 加载帮助系统文本和图片映射。"""
            path = "settings/help_texts.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_encounters(cls):
            """EN: Load city encounter data from JSON.
               ZH: 从 JSON 加载城市遭遇数据。"""
            path = "settings/encounters.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_security_events(cls):
            """EN: Load security event weights and alert thresholds from JSON.
               ZH: 从 JSON 加载安全事件权重和警戒阈值。"""
            path = "settings/security_events.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_training_tests(cls):
            """EN: Load training prerequisite conditions from JSON.
               ZH: 从 JSON 加载训练前置条件。"""
            path = "settings/training_tests.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_quest_prices(cls):
            """EN: Load quest gold rates and class prices from JSON.
               ZH: 从 JSON 加载任务金币费率和课程价格。"""
            path = "settings/quest_prices.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_inventory_sorters(cls):
            """EN: Load inventory filters, filter lists, and sorters from JSON.
               ZH: 从 JSON 加载库存过滤器、过滤列表和排序器。"""
            path = "settings/inventory_sorters.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_sex_training_params(cls):
            """EN: Load sex training parameters from JSON.
               ZH: 从 JSON 加载性训练参数。"""
            path = "settings/sex_training_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_girl_background_pools(cls):
            """EN: Load random pools for girl background generation from JSON.
               ZH: 从 JSON 加载女孩背景生成随机池。"""
            path = "settings/girl_background_pools.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_audio_registry(cls):
            """EN: Load audio registry (playlist, music shortcuts, sound shortcuts) from JSON.
               ZH: 从 JSON 加载音频注册表（播放列表、音乐快捷、音效快捷）。"""
            path = "settings/audio_registry.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_job_params(cls):
            """EN: Load job and sex act parameters from JSON.
               ZH: 从 JSON 加载工作与性行为参数。"""
            path = "settings/job_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_xp_rank_params(cls):
            """EN: Load XP, rank, and job point parameters from JSON.
               ZH: 从 JSON 加载经验、等级与职业点参数。"""
            path = "settings/xp_rank_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_economy_modifiers(cls):
            """EN: Load economy modifiers from JSON.
               ZH: 从 JSON 加载经济修正参数。"""
            path = "settings/economy_modifiers.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_customer_params(cls):
            """EN: Load customer and advertising parameters from JSON.
               ZH: 从 JSON 加载顾客与广告参数。"""
            path = "settings/customer_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_unlock_params(cls):
            """EN: Load unlock thresholds, cheat modifiers, and license data from JSON.
               ZH: 从 JSON 加载解锁阈值、作弊修正与执照数据。"""
            path = "settings/unlock_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_location_tooltips(cls):
            """EN: Load location tooltip mappings from JSON.
               ZH: 从 JSON 加载地点工具提示映射。"""
            path = "settings/location_tooltips.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_contract_params(cls):
            """EN: Load contract system parameters from JSON.
               ZH: 从 JSON 加载契约系统参数。"""
            path = "settings/contract_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_resource_params(cls):
            """EN: Load building resource parameters from JSON.
               ZH: 从 JSON 加载建筑资源参数。"""
            path = "settings/resource_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_archetype_data(cls):
            """EN: Load archetype names and descriptions from JSON.
               ZH: 从 JSON 加载天赋原型名称与描述。"""
            path = "settings/archetype_data.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_game_constants(cls):
            """EN: Load miscellaneous game constants from JSON.
               ZH: 从 JSON 加载杂项游戏常量。"""
            path = "settings/game_constants.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_personality_gift_params(cls):
            """EN: Load personality alignment, attributes, scores, likes, and comments from JSON.
               ZH: 从 JSON 加载人格对齐、属性、分数、喜好与评论。"""
            path = "settings/personality_gift_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_world_map(cls, world_id="default"):
            """EN: Load a world map definition from JSON.
               ZH: 从 JSON 加载世界地图定义。"""
            path = "worlds/{}_world.json".format(world_id)
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_security_scaling(cls):
            """EN: Load siege enemy scaling config from JSON.
               ZH: 从 JSON 加载围城敌人规模配置。"""
            path = "settings/security_scaling.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_power_ui(cls):
            """EN: Load evil power UI colors and card size from JSON.
               ZH: 从 JSON 加载邪恶力量 UI 颜色与卡片尺寸。"""
            path = "settings/power_ui.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_tracked_achievements(cls):
            """EN: Load achievement tracking targets from JSON.
               ZH: 从 JSON 加载成就追踪目标。"""
            path = "settings/tracked_achievements.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_ev_gallery_list(cls):
            """EN: Load EV gallery tab names from JSON.
               ZH: 从 JSON 加载 EV 画廊标签页名称。"""
            path = "settings/ev_gallery_list.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_ui_element_colors(cls):
            """EN: Load UI element color mappings from JSON.
               ZH: 从 JSON 加载 UI 元素颜色映射。"""
            path = "settings/ui_element_colors.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_loans(cls):
            """EN: Load loan parameters from JSON.
               ZH: 从 JSON 加载贷款参数。"""
            path = "settings/loans.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_sex_act_descriptions(cls):
            """EN: Load sex act short descriptions from JSON.
               ZH: 从 JSON 加载性行为简短描述。"""
            path = "settings/sex_act_descriptions.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_rank_lookup(cls):
            """EN: Load customer rank lookup order from JSON.
               ZH: 从 JSON 加载顾客等级查找优先级。"""
            path = "settings/rank_lookup.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_entity_lookups(cls):
            """EN: Load core entity lookup tables from JSON.
               ZH: 从 JSON 加载核心实体查找表。"""
            path = "settings/entity_lookups.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_brothel_name_pools(cls):
            """EN: Load brothel name generation word pools from JSON.
               ZH: 从 JSON 加载青楼名称生成词库。"""
            path = "settings/brothel_name_pools.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_opposed_chance_table(cls):
            """EN: Load opposed challenge chance table from JSON.
               ZH: 从 JSON 加载对抗挑战概率表。"""
            path = "settings/opposed_chance_table.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_quest_templates(cls):
            """EN: Load quest and class templates from JSON.
               ZH: 从 JSON 加载任务和课程模板。"""
            path = "settings/quest_templates.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_item_type_params(cls):
            """EN: Load equipment types and furniture type descriptions from JSON.
               ZH: 从 JSON 加载装备类型和家具类型描述。"""
            path = "settings/item_type_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_girl_upkeep_params(cls):
            """EN: Load girl upkeep threshold and workday mapping parameters from JSON.
               ZH: 从 JSON 加载女孩维护阈值和工作日映射参数。"""
            path = "settings/girl_upkeep_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_courtyard_upgrade_costs(cls):
            """EN: Load courtyard facility upgrade costs from JSON.
               ZH: 从 JSON 加载庭院设施升级成本。"""
            path = "settings/courtyard_upgrade_costs.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_free_girl_limits(cls):
            """EN: Load free girl interaction love limits from JSON.
               ZH: 从 JSON 加载自由女孩交互爱情上限。"""
            path = "settings/free_girl_limits.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_training_difficulty(cls):
            """EN: Load sex act training difficulty table from JSON.
               ZH: 从 JSON 加载性行为训练难度表。"""
            path = "settings/training_difficulty.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_training_tag_exclusions(cls):
            """EN: Load training step tag exclusions from JSON.
               ZH: 从 JSON 加载训练步骤标签排除规则。"""
            path = "settings/training_tag_exclusions.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_minigame_templates(cls):
            """EN: Load minigame house templates from JSON.
               ZH: 从 JSON 加载小游戏房屋模板。"""
            path = "settings/minigame_templates.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_shop_params(cls):
            """EN: Load shop parameters from JSON.
               ZH: 从 JSON 加载商店参数。"""
            path = "settings/shop_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_minion_params(cls):
            """EN: Load minion generation parameters from JSON.
               ZH: 从 JSON 加载仆从生成参数。"""
            path = "settings/minion_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_farm_holding_params(cls):
            """EN: Load farm holding parameters from JSON.
               ZH: 从 JSON 加载农场持有参数。"""
            path = "settings/farm_holding_params.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_girl_name_pools(cls):
            """EN: Load girl random name generation pools from JSON.
               ZH: 从 JSON 加载女孩随机名字生成池。"""
            path = "settings/girl_name_pools.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_loading_tips(cls):
            """EN: Load loading screen tip texts from JSON.
               ZH: 从 JSON 加载加载画面提示文本。"""
            path = "settings/loading_tips.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

        @classmethod
        def load_event_colors(cls):
            """EN: Load event color mappings from JSON.
               ZH: 从 JSON 加载事件颜色映射。"""
            path = "settings/event_colors.json"
            data = cls._load_json_file(path)
            if not data:
                return None
            return data

init -1 python:
    ## EN: Override difficulty tables with JSON data (BK Evolution).
    ## ZH: 用 JSON 数据覆盖难度表（BK Evolution）。
    _diff_json = DataLoader.load_difficulty()
    if _diff_json:
        if "diff_list" in _diff_json:
            diff_list = _diff_json["diff_list"]
        if "diff_settings_range" in _diff_json:
            diff_settings_range = _diff_json["diff_settings_range"]
        if "diff_dict" in _diff_json:
            diff_dict = _diff_json["diff_dict"]
