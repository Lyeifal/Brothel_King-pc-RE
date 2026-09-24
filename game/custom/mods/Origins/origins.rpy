################################################################################
##  Origins Mod — 出身系统（独立 Mod）
##  EN: Player origins as a standalone mod (moved out of the Game Modes mod).
##      At game start the player picks a background; each origin grants a
##      UNIQUE player class with its own spell tree (the class spellbook,
##      auto-learned as the MC levels — see Main.update_spells), plus origin
##      talents and starting bonuses. Religion (god choice) is untouched.
##  ZH: 玩家出身独立 Mod（自 Game Modes Mod 迁出）。开局选择出身后，
##      主角获得该出身的独特职业与专属技能树（职业法术书，随 MC 升级
##      自动领悟——见 Main.update_spells），以及出身天赋与起始奖励。
##      信仰（神灵选择）沿用本体机制，不做改动。
##
##  EN: Class injection: the core rebuilds all_player_classes/spellbook at
##      every init_game (label init_spells), so this mod re-injects its
##      classes lazily by wrapping Main.update_spells (idempotent).
##  ZH: 职业注入：核心在每次 init_game 时重建 all_player_classes/
##      spellbook（label init_spells），因此本 Mod 通过包装
##      Main.update_spells 懒注入职业（幂等）。
################################################################################

init -2 python:

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
            ## ZH: 描述翻译键。
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
            EN: Apply all effects to the target (usually MC).
            ZH: 将所有效果应用到目标上（通常是 MC）。
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
        EN: Player background/origin. Selecting one at game start locks the
            MC to a unique class (self.class_id) with its own spell tree
            (self.class_def["spellbook"]), and grants talents + a starting
            bonus. The god (religion) choice stays with the base game.
        ZH: 玩家出身背景。开局选择后，主角锁定为该出身的独特职业
            （self.class_id），附带专属技能树
            （self.class_def["spellbook"]），并获得天赋与起始奖励。
            信仰（神灵）选择沿用本体机制。
        """

        def __init__(self, origin_id, name_i18n_key, description_i18n_key,
                     icon_tag="origin_default", class_id=None, talents=None,
                     starting_bonus=None, class_def=None):
            ## EN: Unique identifier.
            ## ZH: 唯一标识符。
            self.origin_id = origin_id

            ## EN: Display name translation key.
            ## ZH: 显示名称翻译键。
            self.name_i18n_key = name_i18n_key

            ## EN: Description translation key.
            ## ZH: 描述翻译键。
            self.description_i18n_key = description_i18n_key

            ## EN: Image tag for origin icon (looked up in UI).
            ## ZH: 出身图标的图片标签（UI 中查找）。
            self.icon_tag = icon_tag

            ## EN: Unique player class id granted by this origin.
            ## ZH: 此出身授予的独特主角职业 ID。
            self.class_id = class_id

            ## EN: List of OriginTalent objects.
            ## ZH: OriginTalent 对象列表。
            self.talents = talents or []

            ## EN: Dict of starting bonuses
            ##     (gold / reputation / good / neutral / evil).
            ## ZH: 起始奖励字典（金币 / 声望 / 善良 / 中立 / 邪恶）。
            self.starting_bonus = starting_bonus or {}

            ## EN: Raw class definition dict from JSON (name/description/
            ##     stats/spellbook). Consumed by origins_ensure_classes().
            ## ZH: 来自 JSON 的原始职业定义（名称/描述/属性/法术书）。
            ##     由 origins_ensure_classes() 消费。
            self.class_def = class_def or {}

        def get_name(self):
            return __(self.name_i18n_key)

        def get_description(self):
            return __(self.description_i18n_key)

        def get_class_name(self):
            """EN: Translated unique class name (falls back to the id).
                   ZH: 翻译后的独特职业名（无则回退 ID）。"""
            return __(self.class_def.get("name_i18n", self.class_id or __("Wanderer")))

        def apply_to_mc(self, mc):
            """
            EN: Apply all origin talents and starting bonuses to the MC.
                The unique class itself is set via MC.set_playerclass().
            ZH: 将所有出身天赋与起始奖励应用到 MC。
                独特职业本身通过 MC.set_playerclass() 设置。
            """
            for talent in self.talents:
                talent.apply(mc)

            ## EN: Starting bonuses (accumulate onto the MC fields).
            ## ZH: 起始奖励（累加到 MC 对应字段）。
            for key in ("gold", "reputation", "good", "neutral", "evil"):
                if key in self.starting_bonus:
                    setattr(mc, key, getattr(mc, key) + self.starting_bonus[key])

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


    ## EN: Global origin registry (consumed by core start.rpy via store).
    ## ZH: 全局出身注册表（由核心 start.rpy 经 store 消费）。
    origin_registry = OriginRegistry()

    ## EN: Load-once flag for the mod's own origins.json.
    ## ZH: Mod 自身 origins.json 的加载标记。
    origins_data_loaded = False


    def origins_load_data():
        """
        EN: Load origins (with their unique class definitions and spell
            trees) from the mod's own data/origins.json.
        ZH: 从 Mod 自带的 data/origins.json 加载出身（含独特职业定义
            与技能树）。
        """
        global origins_data_loaded
        if origins_data_loaded:
            return
        origins_data_loaded = True

        _data = None
        try:
            import json as _ojson
            with renpy.loader.load("custom/mods/Origins/data/origins.json") as _ofile:
                _data = _ojson.load(_ofile)
        except Exception as e:
            renpy.notify(__("Origins mod: data load failed (%s)") % e)
            return

        for item in (_data or []):
            try:
                _talents = []
                for t in item.get("talents", []):
                    _effects = [Effect(
                        type=eff.get("type", "boost"),
                        target=eff.get("target"),
                        value=eff.get("value", 0),
                        scope=eff.get("scope"),
                        dice=eff.get("dice", False),
                        scales_with=eff.get("scales_with"),
                    ) for eff in t.get("effects", [])]
                    _talents.append(OriginTalent(
                        talent_id=t["talent_id"],
                        name_i18n_key=t.get("name_i18n", t["talent_id"]),
                        description_i18n_key=t.get("description_i18n", ""),
                        effects=_effects,
                    ))

                origin = PlayerOrigin(
                    origin_id=item["origin_id"],
                    name_i18n_key=item.get("name_i18n", item["origin_id"]),
                    description_i18n_key=item.get("description_i18n", ""),
                    icon_tag=item.get("icon_tag", "origin_default"),
                    class_id=item.get("class_id"),
                    talents=_talents,
                    starting_bonus=item.get("starting_bonus", {}),
                    class_def=item.get("class_def", {}),
                )
                origin_registry.register(origin)

                ## EN: Register every translatable string with the
                ##     translation generator (same trick as the core JSON
                ##     scanner — without this, translate --empty cannot
                ##     see mod-JSON strings and they stay English).
                ## ZH: 将所有可翻译字符串注册给翻译生成器（与核心
                ##     JSON 扫描器同一手法——缺少这一步，
                ##     translate --empty 看不到 Mod JSON 字符串，
                ##     运行时只能显示英文）。
                _strings = [origin.name_i18n_key, origin.description_i18n_key]
                _cd = origin.class_def
                if _cd:
                    _strings.append(_cd.get("name_i18n", ""))
                    _strings.append(_cd.get("description_i18n", ""))
                    for _s in _cd.get("spellbook", []):
                        _strings.append(_s.get("name_i18n", ""))
                        _strings.append(_s.get("description_i18n", ""))
                for _t in _talents:
                    _strings.append(_t.name_i18n_key)
                    _strings.append(_t.description_i18n_key)
                for _s in _strings:
                    if _s:
                        try:
                            __(_s)
                        except Exception:
                            pass
            except Exception as e:
                renpy.notify(__("Origin load error: %s") % str(e))


    def origins_ensure_classes():
        """
        EN: Idempotently register the origins' unique classes into the core
            store registries (all_player_classes, spellbook, MC_CLASS_STAT_DEFS).
            Must run AFTER label init_spells (which rebuilds the dicts), so it
            is called from the wrapped Main.update_spells and on game load.
        ZH: 幂等地将出身独特职业注册进核心 store 注册表
            （all_player_classes、spellbook、MC_CLASS_STAT_DEFS）。
            必须在 label init_spells（会重建这些字典）之后运行，
            因此由包装后的 Main.update_spells 与读档钩子调用。
        """
        try:
            _apc = all_player_classes
            _spellbook = spellbook
            _stat_defs = MC_CLASS_STAT_DEFS
        except NameError:
            return

        for origin in origin_registry.list_origins():
            cid = origin.class_id
            if not cid or cid in _apc:
                continue
            cd = origin.class_def

            _apc[cid] = {
                "name": __(cd.get("name_i18n", cid)),
                "description": __(cd.get("description_i18n", "")),
                "icon": cd.get("icon", ""),
                "modes": ["story", "sandbox"],
            }

            _spells = []
            for s in cd.get("spellbook", []):
                _effects = [Effect.from_dict(e) for e in s.get("effects", [])] if s.get("effects") else None
                _spells.append(Spell(
                    name=__(s.get("name_i18n", "")),
                    pic=s.get("pic", "aura1.webp"),
                    type=s.get("type", "passive"),
                    level=s.get("level", 2),
                    cost=s.get("cost", 0),
                    effects=_effects,
                    duration=s.get("duration"),
                    sound=s.get("sound"),
                    description=__(s.get("description_i18n", "")),
                ))
            _spellbook[cid] = _spells

            _stats = cd.get("stats")
            if _stats:
                _stat_defs[cid] = {
                    "strength": _stats.get("strength", 1),
                    "spirit": _stats.get("spirit", 1),
                    "charisma": _stats.get("charisma", 1),
                    "speed": _stats.get("speed", 2),
                }


    def origins_patch_update_spells():
        """
        EN: Wrap Main.update_spells so the origins' classes are (re)injected
            right before the core iterates the spellbook. Idempotent; safe
            to call again after a reload.
        ZH: 包装 Main.update_spells，使出身职业在核心遍历法术书之前
            （重新）注入。幂等；重载后再次调用也安全。
        """
        if getattr(Main, "_origins_patched", False):
            return

        _origins_base_update_spells = Main.update_spells

        def _origins_update_spells(self):
            origins_ensure_classes()
            return _origins_base_update_spells(self)

        Main.update_spells = _origins_update_spells
        Main._origins_patched = True


    def _origins_on_game_loaded(context):
        """EN: Re-inject classes after a save is loaded.
               ZH: 读档后重新注入职业。"""
        origins_ensure_classes()
