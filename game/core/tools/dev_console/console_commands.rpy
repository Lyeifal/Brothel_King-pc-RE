#### Dev Console — Debugging commands ####
# Phase 6.3: In-game Python REPL with predefined commands for
# inspecting game state, triggering events, and profiling.
#
# Toggle: backtick/tilde key (only in developer mode)

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

    # ── Singleton ──
    dev_console = DevConsole()
    services.register("dev_console", dev_console)
