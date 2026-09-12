#### ITEM QUALITY TIERS (FALLBACK) ####
## EN: Hardcoded fallback copy of the default 0-6 item quality tiers.
##     The authoritative data now lives in the "Item Quality" mod
##     (game/custom/mods/Item Quality/quality.json), which registers over this
##     fallback at init -1. Do NOT delete: per the DATA_MIGRATION policy the
##     game must stay bootable when JSON / mod content is missing.
##     Values are verbatim from the former core/data/settings/quality.json
##     (including the trailing spaces of the "Cheap " / "Worn " prefixes, which
##     are deliberate — they replace the "{0} {1}" separator).
## ZH: 默认 0-6 物品品质档位的硬编码回退副本。权威数据已迁至 "Item Quality" Mod
##     （game/custom/mods/Item Quality/quality.json），该 Mod 在 init -1 覆盖本
##     回退。勿删：按 DATA_MIGRATION 政策，JSON / Mod 内容缺失时游戏仍须可启动。
##     数值逐字来自原 core/data/settings/quality.json（含 "Cheap " / "Worn " 等
##     前缀的尾随空格——那是有意为之，用于替换 "{0} {1}" 的分隔空格）。
init -4 python:

    _fallback_quality_tiers = [

        #  rank  price_modifier  prefixes (adjective category -> English prefix)
        QualityTier(0, 0.25, {"dress": "Ragged", "necklace": "Rusty", "ring": "Rusty", "food": "Rotten", "scroll": "Tattered", "misc": "Worthless"}),
        QualityTier(1, 1.0,  {"dress": "Worn", "necklace": "Broken", "ring": "Fake", "gift": "Cheap ", "food": "Bland", "accessory": "Worn ", "scroll": "Minor", "misc": "Cheap"}),
        QualityTier(2, 2.5,  {"dress": "Simple", "necklace": "Small", "ring": "Small", "gift": "Common ", "food": "Tasty", "accessory": "Simple ", "scroll": "Lesser", "misc": "Common"}),
        QualityTier(3, 5.0,  {"dress": "Fine", "necklace": "Medium", "ring": "Medium", "gift": "Fine ", "food": "Juicy", "accessory": "Fine ", "scroll": "Medium", "misc": "Fine"}),
        QualityTier(4, 12.5, {"dress": "Fancy", "necklace": "Heavy", "ring": "Large", "gift": "Rare ", "food": "Organic", "accessory": "Fancy ", "scroll": "Greater", "misc": "Rare"}),
        QualityTier(5, 25.0, {"dress": "Enchanted", "necklace": "Magical", "ring": "Magical", "food": "Enchanted", "accessory": "Enchanted ", "scroll": "Ultimate", "misc": "Magical"}),
        QualityTier(6, 50.0, {"dress": "Legendary", "necklace": "Legendary", "ring": "Legendary", "food": "Legendary", "misc": "Legendary"}),
    ]

    for _tier in _fallback_quality_tiers:
        quality_registry.register_quality(_tier)


#### END OF ITEM QUALITY TIERS (FALLBACK) ####
