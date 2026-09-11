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
        "version": "2.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("House excess girls in a villa outside the brothel. Housing costs daily rent that scales with district rank, difficulty and headcount; idle girls slowly lose skills; each district offers a limited number of rooms, and a very expensive deed bought in the final district lifts the cap. Girls recover mood and energy slowly, and can train at reduced efficiency."),
        "requires": [],
        "hooks": {},
        "dependencies": [],
        "home_rightmenu_add_buttons": ["right_menu_courtyard"],
        "home_rightmenu_anchor": "after_farm",
    })

    ## EN: Register "courtyard" as a destination when acquiring a girl while the
    ##     brothel is at the 24-girl working cap. Capacity now follows
    ##     room_limit() (district rank based, 99 once expanded).
    ## ZH: 当青楼达到 24 人工作上限收购女孩时，将"别院"注册为安置目的地。
    ##     容量判定现走 room_limit()（按地区等级，扩建后为 99）。
    def _courtyard_destination_list(context):
        if not context.get("at_working_cap"):
            return []
        if not courtyard_villa.can_add_girl():
            return []
        return [{"id": "courtyard", "text": __("Send her to the Courtyard"), "available": True}]

    def _courtyard_destination_accept(context):
        girl = context.get("girl")
        if girl is None:
            return
        if courtyard_villa.add_girl(girl):
            notify(girl.name + __(" has been moved to the Courtyard."), col="green")

    ## EN: Daily processing for courtyard girls. Wired via the day_ending hook:
    ##     mood/energy recovery -> stat decay -> rent collection.
    ## ZH: 别院女孩的每日处理。通过 day_ending 钩子接线：
    ##     心情/能量恢复 → 属性衰减 → 收租。
    def _courtyard_day_ending(context):
        try:
            courtyard_villa.process_day()
        except Exception as e:
            renpy.notify("Courtyard mod: %s" % e)

    ## EN: Right-menu tooltip: room usage, tonight's rent and expansion status.
    ##     Uses % formatting — the returned string is displayed outside this
    ##     scope, so [ ] interpolation would not see these locals.
    ## ZH: 右侧菜单悬浮提示：房间使用、今晚租金与扩建状态。
    ##     用 % 格式化——返回串在函数作用域外显示，[ ] 插值读不到这些局部变量。
    def _courtyard_menu_tooltip():
        try:
            _count = len(courtyard_villa.girls)
            _limit = courtyard_villa.room_limit()
            _rent = courtyard_villa.get_daily_rent()
            if courtyard_villa.expansion_unlocked:
                return __("Courtyard: %d/%d girls. Rent tonight: %d gold. The villa expansion is complete.") % (_count, _limit, _rent)
            elif courtyard_villa.can_buy_expansion():
                return __("Courtyard: %d/%d girls. Rent tonight: %d gold. The villa expansion deed is on sale here (10,000,000 gold)!") % (_count, _limit, _rent)
            return __("Courtyard: %d/%d girls. Rent tonight: %d gold.") % (_count, _limit, _rent)
        except Exception:
            return __("Manage the girls housed in your villa.")

    mod_api_v2.register_hook(mod_api_v2.HOOK_GIRL_DESTINATION_LIST, _courtyard_destination_list, priority=0)
    mod_api_v2.register_hook(mod_api_v2.HOOK_GIRL_DESTINATION_ACCEPT, _courtyard_destination_accept, priority=0)
    mod_api_v2.register_hook(mod_api_v2.HOOK_DAY_ENDING, _courtyard_day_ending, priority=0)

################
## Home - Right menu - Courtyard button
## EN: Entry point into the scenario-driven label. The button is always
##     available; the tooltip shows room usage, tonight's rent and whether
##     the expansion deed is on sale.
## ZH: 场景化 label 的入口。按钮始终可点击；悬浮提示显示房间使用、
##     今晚租金及是否有扩建地契出售。
################

screen right_menu_courtyard():

    hbox xalign 1.0 spacing 20:
        text ""

        textbutton _("Courtyard") style_group "rm":
            action Call("courtyard_scene")
            tooltip _courtyard_menu_tooltip()
