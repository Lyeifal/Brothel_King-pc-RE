# Translation of game/custom/mods/Item Quality/quality.rpy
# Maintained for the mod's own tl/chinese_simplified/ (mod self-managed).
# EN: The quality prefixes are DATA (quality.json), translated at generation
#     time by Item.generate_new_item via __(prefix). `old` texts must stay
#     byte-identical to the prefix strings in quality.json / data/quality.rpy
#     — trailing spaces included (they replace the "{0} {1}" separator).
# ZH: 品质前缀是数据（quality.json），生成时由 Item.generate_new_item 通过
#     __(prefix) 翻译。`old` 必须与 quality.json / data/quality.rpy 中的前缀串
#     逐字节一致——包括尾随空格（用于替换 "{0} {1}" 的分隔空格）。
#     "Cheap"/"Common"/"Fine"/"Rare"/"Broken"/"Medium" 等词在核心正文中另有
#     用途，其核心翻译仍保留在 game/tl/chinese_simplified/strings.rpy。
#
# EN: DO NOT repeat an `old` string that already exists in another tl file of
#     the same language: Ren'Py raises at init
#     ("A translation for X already exists at ...") and the game will not start.
#     The words also used by core text (Fine / Fine / Broken / Medium / Cheap /
#     "Cheap ") therefore stay ONLY in game/tl/chinese_simplified/strings.rpy —
#     string translations are global, so item generation still picks them up.
# ZH: 不要重复定义同语言其他 tl 文件里已有的 `old`：Ren'Py 会在 init 期抛异常
#     （"A translation for X already exists at ..."），游戏无法启动。
#     因此核心正文也在用的词（Fine / Fine / Broken / Medium / Cheap / "Cheap "）
#     只保留在 game/tl/chinese_simplified/strings.rpy——字符串翻译是全局的，
#     物品生成时照样能取到中文。

translate chinese_simplified strings:

    old "Ragged"
    new "破烂"

    old "Worn"
    new "磨损"

    old "Worn "
    new "磨损"

    old "Simple"
    new "简单"

    old "Simple "
    new "简单"

    old "Fancy"
    new "花式"

    old "Fancy "
    new "花式"

    old "Enchanted"
    new "魔法"

    old "Enchanted "
    new "魔法"

    old "Legendary"
    new "传奇"

    old "Rusty"
    new "拉斯蒂"

    old "Small"
    new "小"

    old "Heavy"
    new "重"

    old "Magical"
    new "魔法"

    old "Fake"
    new "假货"

    old "Large"
    new "大型"

    old "Common"
    new "普通"

    old "Common "
    new "普通"

    old "Rare"
    new "罕见"

    old "Rare "
    new "罕见"

    old "Rotten"
    new "腐烂"

    old "Bland"
    new "布兰德"

    old "Tasty"
    new "美味"

    old "Juicy"
    new "多汁"

    old "Organic"
    new "有机物"

    old "Tattered"
    new "破烂不堪"

    old "Minor"
    new "小"

    old "Lesser"
    new "小"

    old "Greater"
    new "更大的"

    old "Ultimate"
    new "终极"

    old "Worthless"
    new "无价值"

    ## NOTE: strings defined directly in quality.rpy (load-failure notifications)

    old "Item Quality mod: could not load quality.json (%s)"
    new "物品品质 Mod：无法加载 quality.json（%s）"

    old "Item Quality mod: quality.json contains no tiers."
    new "物品品质 Mod：quality.json 中没有档位数据。"

