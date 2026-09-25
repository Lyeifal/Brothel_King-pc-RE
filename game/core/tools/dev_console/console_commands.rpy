#### Dev Console — Debugging commands ####
# Phase 6.3: In-game Python REPL with predefined commands for
# inspecting game state, triggering events, and profiling.
#
# Toggle: Shift+O (only in developer mode)

init -1 python:

    class DevConsole(object):
        """In-game developer console for debugging and inspection."""

        def __init__(self):
            self.history = []
            self._commands = {}
            self._register_defaults()

        def _register_defaults(self):
            """Register built-in debug commands."""
            self.register("help", self.cmd_help, "Show available commands")
            self.register("girls", self.cmd_girls, "List all girls: girls [brothel|market|free|farm]")
            self.register("gold", self.cmd_gold, "Add gold: gold <amount>")
            self.register("stats", self.cmd_stats, "Show MC stats")
            self.register("event", self.cmd_event, "Trigger event: event <label>")
            self.register("heal", self.cmd_heal, "Heal all girls")
            self.register("repair", self.cmd_repair, "Run AutoRepair now")
            self.register("services", self.cmd_services, "List registered services")
            self.register("profile", self.cmd_profile, "Profile last operation timing")
            self.register("farmdiag", self.cmd_farmdiag, "Diagnose farm/ranch shop/thieves guild unlock state")

        def register(self, name, callback, description=""):
            self._commands[name] = (callback, description)

        def execute(self, cmd_string):
            """Parse and execute a command string."""
            self.history.append(cmd_string)
            parts = cmd_string.strip().split()
            if not parts:
                return ""

            cmd_name = parts[0].lower()
            args = parts[1:]

            if cmd_name in self._commands:
                try:
                    return self._commands[cmd_name][0](args)
                except Exception as e:
                    return "Error: %s" % str(e)
            else:
                # Try as Python expression
                try:
                    result = eval(cmd_string)
                    return repr(result)
                except Exception as e:
                    return "Unknown command: %s (type 'help' for list)" % cmd_name

        # ── Built-in commands ──

        def cmd_help(self, args):
            lines = ["{b}Dev Console Commands:{/b}"]
            for name, (cb, desc) in sorted(self._commands.items()):
                lines.append("  {color=[c_emerald]}%s{/color} — %s" % (name, desc))
            lines.append("  Any Python expression is also evaluated directly.")
            return "\n".join(lines)

        def cmd_girls(self, args):
            collection = args[0] if args else "brothel"
            mapping = {
                "brothel": MC.girls, "market": slavemarket.girls,
                "free": game.free_girls, "farm": farm.girls,
                "all": MC.girls + slavemarket.girls + game.free_girls + farm.girls,
            }
            girls = mapping.get(collection, MC.girls)
            lines = ["%i girl(s) in %s:" % (len(girls), collection)]
            for g in girls[:20]:
                lines.append("  %s (Lv.%s %s) — %s" % (g.fullname, g.level, g.job or "no job", g.path))
            return "\n".join(lines)

        def cmd_gold(self, args):
            amount = int(args[0]) if args else 1000
            MC.gold += amount
            return "Added %s gold. Current: %s" % (amount, MC.gold)

        def cmd_stats(self, args):
            lines = [
                "MC: %s, Level %s, Gold: %s" % (MC.name, MC.level, MC.gold),
                "Brothel: %s, Rep: %s, Chapter: %s" % (brothel.name if services.has("brothel") else "N/A", brothel.rep if services.has("brothel") else "N/A", game.chapter),
                "Girls: %s, Free: %s, Farm: %s" % (len(MC.girls), len(game.free_girls), len(farm.girls)),
                "Calendar: Day %s, Week %s" % (calendar.day, (calendar.time - 1) // 7 + 1),
            ]
            return "\n".join(lines)

        def cmd_event(self, args):
            if not args:
                return "Usage: event <label>"
            label = args[0]
            story_add_event(label)
            return "Event '%s' added to queue." % label

        def cmd_heal(self, args):
            for g in MC.girls + farm.girls:
                g.heal(99)
                g.change_energy(999)
                g.hurt = 0
            return "All girls fully healed and energized."

        def cmd_repair(self, args):
            game.update_files_timestamp()
            return "AutoRepair triggered."

        def cmd_services(self, args):
            return "Registered services: %s" % ", ".join(services.list_services())

        def cmd_profile(self, args):
            try:
                return game.func_time_log2 or "No profile data available."
            except:
                return "Profiling not available."

        def cmd_farmdiag(self, args):
            """EN: Detailed farm/ranch-shop/thieves-guild unlock diagnostics.
               ZH: 农场/牧场商店/盗贼公会解锁状态详细诊断。"""
            return farm_diag_text()

    def farm_diag_text():
        """EN: Build the farm/ranch-shop/thieves-guild diagnostic report.
           ZH: 生成农场/牧场商店/盗贼公会解锁诊断报告（控制台与读档自诊断共用）。"""
        if globals().get("farm") is None:
            return "farm unavailable (before init_game or not in this save)."
        L = []
        A = L.append

        A("{b}== 基本状态 =={/b}")
        A("farm.active（家园农场）: %s" % getattr(farm, "active", "?"))
        A("chapter: %s | story_mode: %s | debug_mode: %r" % (game.chapter, game.is_story_mode(), debug_mode))
        A("NGP 农场钥匙: %s" % NGP_settings_dict["farm"].get())
        try:
            _reg = globals().get("unlock_registry")
            if _reg is not None:
                A("解锁注册表: %s" % sorted(_reg.get_all_unlocked()))
            else:
                A("解锁注册表: {color=[c_red]}store 中找不到 unlock_registry!{/color}")
        except Exception as _e:
            A("解锁注册表: 读取失败 %r" % _e)
        try:
            _fl = globals().get("farmland")
            A("store.farmland 对象: %s (action=%s)" % ("存在" if _fl is not None else "缺失", getattr(_fl, "action", "?")))
        except Exception as _e:
            A("store.farmland 对象: 读取失败 %r" % _e)

        def _find_loc(name):
            for d in district_dict.values():
                for loc in d.locations:
                    if loc.name.lower() == name:
                        return loc
            return None

        A("")
        A("{b}== 城市地点 =={/b}")
        for loc_name, desc in (("farm", "牧场(商店农场)"), ("thieves guild", "盗贼公会"), ("spice market", "香料市场"), ("junkyard", "垃圾场"), ("sewers", "下水道")):
            loc = _find_loc(loc_name)
            if loc:
                A("%s [%s]: secret=%s action=%s menu=%s" % (desc, loc.name, loc.secret, loc.action, loc.menu))
            else:
                A("%s: {color=[c_red]}未找到地点对象!{/color}" % desc)

        A("")
        A("{b}== 已解锁商店 =={/b}")
        A(", ".join(_s.name for _s in unlocked_shops) if unlocked_shops else "（无）")

        chains = (
            ("农场链", ("farm_meet_gizel", "farm_meet_gizel2", "farm_go_with_gizel", "farm_found_a_place", "farm_gizel_introduction", "farm_meet_goldie", "farm_activate_goldie", "farm_meet_willow", "farm_meet_gina", "farm_meet_stella", "farm_second_monster")),
            ("盗贼链", ("c1_thieves_guild_tip", "c1_spice_market", "c1_sewers", "c1_thieves_guild_found")),
        )
        for title, labels in chains:
            A("")
            A("{b}== %s事件 =={/b}" % title)
            for lbl in labels:
                ev = event_dict.get(lbl)
                if ev is None:
                    A("%s: {color=[c_red]}event_dict 无此事件!{/color}" % lbl)
                    continue
                in_list = ev in city_events
                flag = story_flags.get(lbl)
                if in_list:
                    status = "{color=[c_emerald]}在事件池中{/color}"
                elif ev.happened or flag:
                    status = "{color=[c_darkgray]}已触发过{/color}"
                else:
                    status = "{color=[c_red]}缺失(永不触发!){/color}"
                A("%s: %s | chance=%s loc=%s happened=%s flag=%s" % (lbl, status, ev.chance, ev.location, ev.happened, bool(flag)))

        # 在牧场地点实测 happens（换入换出 selected_location，不改动其他状态）
        A("")
        A("{b}== 牧场地点实测（happens 100 次抽样）{/b}")
        A("(已触发过的一次性事件显示 0% 属正常)")
        farm_loc = _find_loc("farm")
        if farm_loc is not None:
            # EN: use store.selected_location explicitly — any bare assignment
            #     would make the name function-local and break the read above.
            # ZH: 必须用 store.selected_location 显式访问——函数内一旦出现
            #     裸赋值，该名字在整个函数内都会被视为局部变量。
            old_sel = store.selected_location
            try:
                store.selected_location = farm_loc
                for lbl in ("farm_meet_goldie", "farm_activate_goldie", "farm_meet_stella"):
                    ev = event_dict.get(lbl)
                    if ev is None:
                        continue
                    n = sum(1 for _ in range(100) if ev.happens())
                    A("%s @牧场: %s%%" % (lbl, n))
            finally:
                store.selected_location = old_sel

        A("")
        A("{b}== 结论 =={/b}")
        ev = event_dict.get("farm_activate_goldie")
        # EN: compare against the NPC object, not a hardcoded English name —
        #     NPC names are i18n'd (Goldie vs 戈尔迪).
        # ZH: 与 NPC 对象比对而非硬编码英文名——NPC 名字已 i18n 化
        #     （Goldie / 戈尔迪）。
        _goldie_obj = globals().get("NPC_goldie")
        _goldie_unlocked = _goldie_obj is not None and _goldie_obj in unlocked_shops
        if not getattr(farm, "active", False):
            A("家园农场未激活 → 需先走 Gizel 链（香料市场→垃圾场）或 NG+ 农场钥匙")
        elif _goldie_unlocked and farm_loc is not None and farm_loc.action:
            A("牧场商店已解锁 ✓ 地点按钮已启用 ✓")
        elif _goldie_unlocked:
            A("商店已解锁但牧场地点按钮未启用 → {color=[c_red]}读档修复钩子未生效，请把本文件内容发给我{/color}")
        elif ev is not None and (ev.happened or story_flags.get("farm_activate_goldie")):
            A("商店事件已触发但未进 unlocked_shops → 异常，请报告")
        elif ev is not None and ev in city_events:
            A("商店解锁事件已在池中 → {color=[c_emerald]}去牧场地点访问即可 100%% 触发{/color}")
        else:
            A("{color=[c_red]}商店解锁事件缺失 → 读档修复钩子未覆盖，请报告{/color}")
        return "\n".join(L)

    def _write_farm_diag():
        """EN: Write the farm diagnostic report to farm_diag.txt.
           Defined at init level so no store variables leak (an `import os`
           inside an after_load python block would poison the save pickle).
           Errors are written into the file itself so they are visible.
           ZH: 把农场诊断报告写入 farm_diag.txt。定义在 init 层，
           避免污染 store（在 after_load 的 python 块里 import os
           会让 store 混入模块对象，导致存档无法序列化）。
           错误也写入文件本身，便于排查。"""
        _path = config.gamedir + "/farm_diag.txt"
        try:
            _text = renpy.filter_text_tags(farm_diag_text(), allow=[])
        except Exception:
            import traceback
            _text = "DIAG ERROR:\n" + traceback.format_exc()
        try:
            with open(_path, "w", encoding="utf-8") as _f:
                _f.write(_text)
        except Exception:
            pass

    # ── Singleton ──
    dev_console = DevConsole()
    services.register("dev_console", dev_console)
