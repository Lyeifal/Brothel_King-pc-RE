#### Mod API v2 — Versioned, capability-based modding interface ####
# Phase 5: Clean, documented, type-safe modding API.
#
# Key improvements over v1:
#   - Versioned: mod declares api_version for compatibility checking
#   - Capability flags: mod declares required features
#   - Sandboxed: API exposes only intended surfaces, not internal state
#   - Validated: inputs validated at registration time
#   - Lifecycle: formal install/enable/disable/remove with state cleanup
#   - Standardized hooks: <domain>_<action>_<tense> naming convention
#
# v1 mods continue to work through compatibility layer.
# v2 mods declare: api_version, min_game_version, requires, hooks

init -3 python:

    class ModAPIV2(ModAPI):
        """Version 2 of the Mod API with capability-based access control.

        Usage in a mod:
            api = ModAPIV2.instance()
            api.register_trait(my_trait, category="community")
            api.register_hook("girl_generated", my_callback)
        """

        _instance = None  # EN: Own singleton, separate from ModAPI v1 | 自己的单例，与 v1 分开
        API_VERSION = 2

        # ── Capability flags a mod can require ──
        CAPABILITIES = {
            "girl_stats",       # Access girl stat modification
            "girl_traits",      # Register custom traits/perks
            "economy",          # Modify economy calculations
            "events",           # Register/dispatch events
            "dialogue",         # Custom dialogue lines
            "pictures",         # Custom picture tags
            "game_modes",       # Register custom game modes
            "origin",           # Register player origins
            "scenario",         # Register scenarios
            "ngp_settings",     # New Game+ settings
        }

        def __init__(self):
            super(ModAPIV2, self).__init__()
            self._active_mods = {}       # mod_id -> mod_manifest
            self._mod_hooks = defaultdict(list)  # hook_name -> [(mod_id, callback, priority)]

        # ── Mod lifecycle ──

        def register_mod(self, mod_id, manifest):
            """Register a v2 mod with capability declarations.

            manifest = {
                "name": str,              # Display name
                "version": str,           # Mod version
                "api_version": 2,         # Must be 2
                "min_game_version": str,  # Minimum game version
                "author": str,
                "description": str,
                "requires": [str],        # List of capability flags
                "hooks": {hook_name: callback, ...},
                "dependencies": [str],    # Other mod IDs this depends on
            }
            """
            # Validate
            if manifest.get("api_version") != self.API_VERSION:
                raise ValueError("Mod '%s' requires API v%s, but v%d is current" % (
                    mod_id, manifest.get("api_version"), self.API_VERSION))

            for cap in manifest.get("requires", []):
                if cap not in self.CAPABILITIES:
                    raise ValueError("Mod '%s' requires unknown capability: %s" % (mod_id, cap))

            self._active_mods[mod_id] = manifest

            # Register hooks
            for hook_name, callback in manifest.get("hooks", {}).items():
                self._mod_hooks[hook_name].append((mod_id, callback, 0))

        def unregister_mod(self, mod_id):
            """Remove a mod and clean up its hooks."""
            self._active_mods.pop(mod_id, None)
            for hook_list in self._mod_hooks.values():
                hook_list[:] = [(mid, cb, pri) for mid, cb, pri in hook_list if mid != mod_id]

        def is_mod_active(self, mod_id):
            return mod_id in self._active_mods

        def list_active_mods(self):
            return list(self._active_mods.keys())

        # ── Standardized hook system ──

        # Hook naming convention: <domain>_<action>_<tense>
        # Examples: girl_generated, day_starting, night_finished, event_triggering

        def register_hook(self, hook_name, callback, priority=0):
            """Register a hook callback.

            Args:
                hook_name: Standardized hook name (e.g. 'girl_generated')
                callback: Callable receiving (context: dict)
                priority: Higher = runs earlier (default 0)
            """
            self._mod_hooks[hook_name].append(("_direct", callback, priority))
            self._mod_hooks[hook_name].sort(key=lambda x: -x[2])  # High priority first

        def execute_hook(self, hook_name, **context):
            """Execute all registered callbacks for a hook.

            Returns a dict of {mod_id: result} for hooks that returned values.
            Hooks returning None are filtered out.
            """
            results = {}
            for mod_id, callback, _priority in self._mod_hooks.get(hook_name, []):
                try:
                    result = callback(context)
                    if result is not None:
                        results[mod_id] = result
                except Exception as e:
                    # Hook failure should never crash the game
                    if renpy.config.developer:
                        renpy.notify("Hook '%s' (mod '%s') failed: %s" % (hook_name, mod_id, str(e)))
            return results

        def cancel_hook(self, hook_name):
            """Signal that the default action should be cancelled.

            Returns True if any hook requested cancellation.
            Hooks signal cancellation by setting context["cancel"] = True.
            """
            # EN: Do NOT route this through execute_hook: that method rebuilds
            #     its own context dict from **kwargs, so the dict created here
            #     would never reach the callbacks and cancellation would be
            #     silently lost (cancel_hook always returned False).
            # ZH: 不能经由 execute_hook 中转：该方法会用 **kwargs 重建自己的
            #     context 字典，本方法创建的 dict 到不了回调，取消信号会静默
            #     丢失（cancel_hook 过去永远返回 False）。
            context = {"cancel": False}
            for mod_id, callback, _priority in self._mod_hooks.get(hook_name, []):
                try:
                    callback(context)
                except Exception as e:
                    # EN: Hook failure should never crash the game
                    # ZH: 钩子失败不应导致游戏崩溃
                    if renpy.config.developer:
                        renpy.notify("Hook '%s' (mod '%s') failed: %s" % (hook_name, mod_id, str(e)))
            return context.get("cancel", False)

        # ── Hook point constants (for documentation and auto-complete) ──

        HOOK_GIRL_GENERATED = "girl_generated"
        HOOK_GIRL_ACQUIRED = "girl_acquired"
        HOOK_GIRL_SOLD = "girl_sold"
        HOOK_GIRL_RUNAWAY = "girl_runaway"
        HOOK_DAY_STARTING = "day_starting"
        HOOK_DAY_ENDING = "day_ending"
        HOOK_NIGHT_STARTING = "night_starting"
        HOOK_NIGHT_FINISHED = "night_finished"
        HOOK_WEEK_STARTING = "week_starting"
        HOOK_EVENT_TRIGGERING = "event_triggering"
        HOOK_EVENT_FINISHED = "event_finished"
        HOOK_SECURITY_EVENT = "security_event"
        HOOK_CHAPTER_STARTING = "chapter_starting"
        HOOK_CHAPTER_FINISHED = "chapter_finished"
        HOOK_GAME_SAVED = "game_saved"
        HOOK_GAME_LOADED = "game_loaded"

    # ── Singleton ──
    mod_api_v2 = ModAPIV2()
    services.register("mod_api_v2", mod_api_v2)
