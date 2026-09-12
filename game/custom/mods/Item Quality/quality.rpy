################################################################################
##  Item Quality Mod — tier loading
##  EN: Loads the mod's own quality.json and registers the tiers into the core
##      QualityRegistry. Definition block is init -9 so that mod.rpy's
##      init -1 registration can call it (same convention as Game Modes).
##  ZH: 加载本 Mod 自带的 quality.json 并把档位注册进核心 QualityRegistry。
##      定义块放在 init -9，以便 mod.rpy 的 init -1 注册流程调用
##      （与 Game Modes 同一约定）。
################################################################################

init -9 python:

    import json

    ## EN: Mod-local data file, loaded the same way as Courtyard's JSON.
    ## ZH: Mod 自带数据文件，加载方式同 Courtyard。
    QUALITY_JSON_PATH = "custom/mods/Item Quality/quality.json"

    def load_quality_tiers():
        """
        EN: Read quality.json and register every tier over the core fallback.
            On failure the core fallback tiers stay in place and the game
            keeps running (a notification is shown to the player).
        ZH: 读取 quality.json 并把每个档位覆盖注册到核心回退之上。
            失败时核心回退档位保持有效，游戏继续运行（向玩家显示提示）。
        """
        try:
            with renpy.loader.load(QUALITY_JSON_PATH) as _f:
                _data = json.load(_f)
        except Exception as _e:
            renpy.notify(__("Item Quality mod: could not load quality.json (%s)") % _e)
            return

        _tiers = _data.get("tiers", [])
        if not _tiers:
            renpy.notify(__("Item Quality mod: quality.json contains no tiers."))
            return

        for _tier_data in _tiers:
            quality_registry.register_quality(QualityTier.from_dict(_tier_data))
