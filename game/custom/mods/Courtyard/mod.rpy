################################################################################
##  Courtyard Mod — BK Evolution
##  EN: Standalone mod housing the former core courtyard system
##      (ex game/core/systems/courtyard/): a villa for excess girls.
##  ZH: 庭院系统独立 Mod（原 game/core/systems/courtyard/）：
##      用于安置超编女孩的别院。
##  EN: Install = always active (Mod API v2). Uninstall = remove this folder.
##  ZH: 安装即常驻激活（Mod API v2）。卸载 = 删除本目录。
################################################################################

init -1 python:

    services.mod_api_v2.register_mod("courtyard", {
        "name": __("Courtyard"),
        "version": "1.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("House excess girls in a villa outside the brothel. Girls recover mood and energy slowly, and can train at reduced efficiency."),
        "requires": [],
        "hooks": {},
        "dependencies": [],
        "home_rightmenu_add_buttons": ["right_menu_courtyard"],
    })

    ## EN: Register "courtyard" as a destination when acquiring a girl while the
    ##     brothel is at the 24-girl working cap.
    ## ZH: 当青楼达到 24 人工作上限收购女孩时，将"别院"注册为安置目的地。
    def _courtyard_destination_list(context):
        if not context.get("at_working_cap"):
            return []
        if not courtyard.can_add_girl():
            return []
        return [{"id": "courtyard", "text": __("Send her to the Courtyard"), "available": True}]

    def _courtyard_destination_accept(context):
        girl = context.get("girl")
        if girl is None:
            return
        if courtyard.add_girl(girl):
            notify_list.append((girl.name + __(" has been moved to the Courtyard.")), col="green")

    ## EN: Daily recovery for courtyard girls. Wired via the day_ending hook —
    ##     this activates the process_day() logic that existed in the core system.
    ## ZH: 别院女孩的每日恢复。通过 day_ending 钩子接线——
    ##     这激活了原核心系统中已存在但从未被调用的 process_day() 逻辑。
    def _courtyard_day_ending(context):
        try:
            courtyard.process_day()
        except Exception as e:
            renpy.notify("Courtyard mod: %s" % e)

    mod_api_v2.register_hook(mod_api_v2.HOOK_GIRL_DESTINATION_LIST, _courtyard_destination_list, priority=0)
    mod_api_v2.register_hook(mod_api_v2.HOOK_GIRL_DESTINATION_ACCEPT, _courtyard_destination_accept, priority=0)
    mod_api_v2.register_hook(mod_api_v2.HOOK_DAY_ENDING, _courtyard_day_ending, priority=0)

screen right_menu_courtyard():

    hbox xalign 1.0 spacing 20:
        text ""

        textbutton _("Courtyard") style_group "rm":
            action Show("courtyard")
            tooltip __("管理安置在别院的女孩。")
