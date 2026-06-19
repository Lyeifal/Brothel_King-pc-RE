################################################################################
##  DataExporter — BK Evolution
##  EN: Exports hardcoded game data (traits, perks, events) to JSON files.
##      Run this by calling label export_all_data from a debug menu or console.
##  ZH: 将硬编码的游戏数据（特质、天赋、事件）导出为 JSON 文件。
##      通过调试菜单或控制台调用 label export_all_data 来运行。
################################################################################

init -1 python:
    import json

    class DataExporter(object):
        """
        EN: Exports in-memory game objects to JSON files in game/core/data/.
        ZH: 将内存中的游戏对象导出到 game/core/data/ 的 JSON 文件。
        """

        DATA_DIR = "core/data"

        @classmethod
        def export_all(cls):
            cls.export_traits()
            cls.export_perks()
            cls.export_story_events()
            cls.export_achievements()
            cls.export_difficulty()
            cls.export_ngp_settings()
            cls.export_meta_progression()

        @classmethod
        def export_traits(cls):
            """EN: Export all registered traits to JSON.
               ZH: 导出所有已注册特质到 JSON。"""
            data = []
            for trait in trait_dict.values():
                try:
                    data.append(trait.to_dict())
                except Exception as e:
                    renpy.notify(__("Export trait error: %s - %s") % (trait.name, str(e)))
            path = cls.DATA_DIR + "/traits/traits.json"
            cls._write_json(path, data)
            renpy.notify(__("Exported %s traits to %s") % (len(data), path))

        @classmethod
        def export_perks(cls):
            """EN: Export all registered perks to JSON.
               ZH: 导出所有已注册天赋到 JSON。"""
            data = []
            # EN: perk_registry stores perks in category dicts.
            # ZH: perk_registry 按类别字典存储天赋。
            for cat, perks in perk_registry._registry.items():
                for perk in perks:
                    try:
                        data.append(perk.to_dict())
                    except Exception as e:
                        renpy.notify(__("Export perk error: %s - %s") % (perk.name, str(e)))
            path = cls.DATA_DIR + "/perks/perks.json"
            cls._write_json(path, data)
            renpy.notify(__("Exported %s perks to %s") % (len(data), path))

        @classmethod
        def export_story_events(cls):
            """EN: Export all registered story events to JSON.
               ZH: 导出所有已注册剧情事件到 JSON。"""
            data = []
            for label, ev in event_dict.items():
                try:
                    item = {
                        "label": ev.label,
                        "chapter": ev.chapter,
                        "rank": ev.rank,
                        "date": ev.date,
                        "year": ev.year,
                        "month": ev.month,
                        "day": ev.day,
                        "weekday": ev.weekday,
                        "chance": ev.chance,
                        "type": ev.type,
                        "location": ev.location,
                        "locations": ev.locations,
                        "seasons": ev.seasons,
                        "min_gold": ev.min_gold,
                        "condition": ev.condition,
                        "not_condition": ev.not_condition,
                        "once": ev.once,
                        "AP_cost": ev.AP_cost,
                        "order": ev.order,
                        "call_args": ev.call_args,
                        "modes": getattr(ev, "modes", ["story"]),
                    }
                    data.append(item)
                except Exception as e:
                    renpy.notify(__("Export event error: %s - %s") % (label, str(e)))
            path = cls.DATA_DIR + "/stories/story_events.json"
            cls._write_json(path, data)
            renpy.notify(__("Exported %s events to %s") % (len(data), path))

        @classmethod
        def export_achievements(cls):
            """EN: Export current achievement_list to JSON keyed by target.
               ZH: 将当前成就列表按 target 导出为 JSON。"""
            data = {}
            for ach in achievement_list:
                try:
                    data[ach.target] = ach.to_dict()
                except Exception as e:
                    renpy.notify(__("Export achievement error: %s - %s") % (ach.target, str(e)))
            path = cls.DATA_DIR + "/achievements/achievements.json"
            cls._write_json(path, data)
            renpy.notify(__("Exported %s achievements to %s") % (len(data), path))

        @classmethod
        def export_difficulty(cls):
            """EN: Export current difficulty tables to JSON.
               ZH: 导出当前难度表为 JSON。"""
            data = {
                "diff_list": diff_list,
                "diff_settings_range": diff_settings_range,
                "diff_dict": diff_dict,
            }
            path = cls.DATA_DIR + "/difficulty/difficulty.json"
            cls._write_json(path, data)
            renpy.notify(__("Exported difficulty tables to %s") % path)

        @classmethod
        def export_ngp_settings(cls):
            """EN: Export current NG+ settings to JSON.
               ZH: 导出当前 NG+ 设置为 JSON。"""
            data = []
            for setting in NGP_settings:
                try:
                    data.append(setting.to_dict())
                except Exception as e:
                    renpy.notify(__("Export NGP error: %s - %s") % (setting.name, str(e)))
            path = cls.DATA_DIR + "/ngp/ngp_settings.json"
            cls._write_json(path, data)
            renpy.notify(__("Exported %s NG+ settings to %s") % (len(data), path))

        @classmethod
        def export_meta_progression(cls):
            """EN: Export current meta upgrades to JSON.
               ZH: 导出当前局外养成升级为 JSON。"""
            data = {"meta_upgrades": []}
            for upgrade in meta_registry.values():
                try:
                    data["meta_upgrades"].append(upgrade.to_dict())
                except Exception as e:
                    renpy.notify(__("Export meta error: %s - %s") % (upgrade.upgrade_id, str(e)))
            path = cls.DATA_DIR + "/meta/meta_progression.json"
            cls._write_json(path, data)
            renpy.notify(__("Exported %s meta upgrades to %s") % (len(data["meta_upgrades"]), path))

        @classmethod
        def _write_json(cls, rel_path, data):
            """EN: Write JSON data to a file in the game directory.
               ZH: 将 JSON 数据写入游戏目录中的文件。"""
            full_path = renpy.config.gamedir + "/" + rel_path
            import os
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")


label export_all_data:
    """
    EN: Export all hardcoded game data to JSON.
        Call this from the console or a debug menu.
    ZH: 将所有硬编码游戏数据导出为 JSON。
        从控制台或调试菜单调用此标签。
    """
    python:
        DataExporter.export_all()
    return
