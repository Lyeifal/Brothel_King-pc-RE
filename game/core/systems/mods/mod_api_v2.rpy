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
# v2 mods declare: api_version, min_game_version, requires, hooks,
#                  dependencies, always_on
#
# EN: Persistent enable/disable (BK Evolution): v2 mods can be toggled from
#     the main-menu Mod Manager screen (screen mod_manager). The flag lives
#     in persistent._bk_v2_mod_states (mod_id -> bool; unrecorded ids default
#     to enabled). A mod is active iff it is registered AND (always_on OR
#     persistently enabled) AND every mod_id in its manifest "dependencies"
#     is active as well (uninstalled deps count as missing). Ren'Py binds
#     `persistent` before init code runs, so register_mod already activates
#     only enabled mods at init time; apply_startup_states() re-syncs
#     idempotently from label before_main_menu as a safety net.
# ZH: 持久化启用/禁用（BK Evolution）：v2 Mod 可在主菜单 Mod 管理界面
#     （screen mod_manager）切换。开关存于 persistent._bk_v2_mod_states
#     （mod_id -> bool；未记录的 id 默认启用）。Mod 激活当且仅当：已注册 ∧
#     （always_on ∨ 持久化启用）∧ manifest "dependencies" 全部激活
#     （依赖未安装视为缺失）。Ren'Py 在 init 代码运行前已绑定 persistent，
#     故 register_mod 在 init 期即只激活已启用的 Mod；
#     apply_startup_states() 在 before_main_menu 幂等重建兜底。

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

        # EN: persistent field holding per-mod enable flags (mod_id -> bool)
        # ZH: 存放各 Mod 启用开关的 persistent 字段（mod_id -> bool）
        PERSISTENT_STATES_ATTR = "_bk_v2_mod_states"

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
            # EN: ALL registered mods (mod_id -> manifest), including inactive
            #     ones. Registration happens at init -1 of every boot.
            # ZH: 全部已注册 Mod（含未激活），每次启动 init -1 时登记。
            self._registered_mods = {}
            # EN: Active subset, rebuilt by _rebuild_active_mods() from
            #     persistent enable flags + always_on + dependencies.
            # ZH: 激活子集，由 _rebuild_active_mods() 按持久化开关、
            #     always_on 与依赖关系重建。
            self._active_mods = {}
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
                "dependencies": [str],    # Other mod IDs that must be active
                                          # for this mod to activate
                "always_on": bool,        # True = cannot be disabled
                                          # (default False)
                "home_rightmenu_add_buttons": [str],  # Screen names shown in the
                                        # home right menu under "Mods" (no-arg screens)
            }

            EN: Registration is per-boot (init) and pure in-memory; the enable
                flag itself is persisted in persistent._bk_v2_mod_states and
                consulted right away (Ren'Py binds `persistent` before init
                code runs). The mod activates iff it is enabled (or always_on)
                AND all of its dependencies activate. To disable a v2 mod from
                the player's perspective, toggle it off in the main-menu Mod
                Manager screen instead of removing its files.
            ZH: 注册为每次启动的内存行为；启用开关存于
                persistent._bk_v2_mod_states 并立即读取（Ren'Py 在 init 代码
                运行前已绑定 persistent）。Mod 在已启用（或 always_on）且其
                全部 dependencies 激活时才激活。玩家侧禁用 v2 Mod 请在
                主菜单 Mod 管理界面切换，无需删除文件。
            """
            # Validate
            if manifest.get("api_version") != self.API_VERSION:
                raise ValueError("Mod '%s' requires API v%s, but v%d is current" % (
                    mod_id, manifest.get("api_version"), self.API_VERSION))

            for cap in manifest.get("requires", []):
                if cap not in self.CAPABILITIES:
                    raise ValueError("Mod '%s' requires unknown capability: %s" % (mod_id, cap))

            if mod_id in self._registered_mods:
                raise ValueError("Mod '%s' is already registered" % mod_id)

            self._registered_mods[mod_id] = manifest

            # Register hooks (they stay registered while the mod is disabled,
            # but execute_hook/cancel_hook skip callbacks of inactive mods).
            # 注册钩子（Mod 被禁用时钩子仍保留，但 execute_hook/cancel_hook
            # 会跳过未激活 Mod 的回调）。
            for hook_name, callback in manifest.get("hooks", {}).items():
                self._mod_hooks[hook_name].append((mod_id, callback, 0))

            # EN: Activation is recomputed globally so dependency order among
            #     mods registered at different init priorities does not matter.
            # ZH: 全局重算激活状态，不同 init 优先级注册的 Mod 之间
            #     无需关心依赖顺序。
            self._rebuild_active_mods()

            if renpy.config.developer:
                ## EN: Dev-only log — intentionally NOT translated: translation stubs
                ##     (new "") would break the %-formatting below.
                ## ZH: 仅开发者日志——有意不翻译：翻译空槽（new ""）会让下面的 % 格式化崩溃。
                renpy.log("[ModAPI v2] Registered mod '%s' (%s)" % (
                    mod_id, manifest.get("name", mod_id)))

        def unregister_mod(self, mod_id):
            """Remove a mod and clean up its hooks."""
            self._registered_mods.pop(mod_id, None)
            self._active_mods.pop(mod_id, None)
            for hook_list in self._mod_hooks.values():
                hook_list[:] = [(mid, cb, pri) for mid, cb, pri in hook_list if mid != mod_id]

        # ── Persistent enable/disable (main-menu Mod Manager) ──

        def _get_persistent_states(self, create=False):
            """Return the persistent enable-flag dict, or None when persistent
            is unavailable (e.g. stubbed test environments).

            EN: Never raises: any persistent access problem falls back to None,
                which callers treat as "no records" (everything defaults to
                enabled).
            ZH: 永不抛异常：任何 persistent 访问问题都回退为 None，
                调用方按"无记录"处理（全部默认启用）。
            """
            try:
                states = getattr(persistent, self.PERSISTENT_STATES_ATTR, None)
            except Exception:
                return None
            if states is None and create:
                states = {}
                try:
                    setattr(persistent, self.PERSISTENT_STATES_ATTR, states)
                except Exception:
                    return None
            return states

        def is_mod_enabled(self, mod_id):
            """Read the persistent enable flag; unrecorded ids default to True.

            EN: Used by the Mod Manager screen; does not require the mod to be
                active (it can be enabled but kept inactive by a dependency).
            ZH: 供 Mod 管理界面读取；不要求 Mod 处于激活状态
                （可能因缺前置而处于"已启用但未激活"）。"""
            states = self._get_persistent_states()
            if states is None:
                return True
            return bool(states.get(mod_id, True))

        def set_mod_enabled(self, mod_id, enabled):
            """Write the persistent enable flag and re-sync the in-memory
            active set (no hot reload — full effect after restart).

            ZH: 写入持久化启用开关并同步内存中的激活状态
                （不做热重载，重启后完全生效）。"""
            if mod_id not in self._registered_mods:
                raise ValueError("Mod '%s' is not registered" % mod_id)
            states = self._get_persistent_states(create=True)
            if states is not None:
                states[mod_id] = bool(enabled)
            self._rebuild_active_mods()

        def apply_startup_states(self):
            """Idempotent rebuild of _active_mods from persistent + deps.

            EN: Called from label before_main_menu (events_dispatcher.rpy) as a
                safety net after all init-time registrations; safe to call
                again at any time.
            ZH: 由 before_main_menu label（events_dispatcher.rpy）在所有
                init 注册完成后兜底调用；可随时重复调用。
            """
            self._rebuild_active_mods()
            if renpy.config.developer:
                _inactive = sorted(set(self._registered_mods) - set(self._active_mods))
                if _inactive:
                    renpy.log("[ModAPI v2] Inactive mods (disabled or missing "
                              "dependencies): %s" % ", ".join(_inactive))

        def _rebuild_active_mods(self):
            """Recompute _active_mods: registered AND (always_on OR persistently
            enabled) AND all manifest dependencies active.

            EN: Dependencies are resolved before their dependents (topological
                pass); mods left unresolved — missing/uninstalled deps or
                dependency cycles — stay inactive.
            ZH: 被依赖者优先解析（拓扑遍历）；无法解析的 Mod——
                依赖缺失/未安装或存在依赖环——保持未激活。
            """
            _active = {}
            _remaining = dict(self._registered_mods)
            while _remaining:
                _progressed = False
                for _mod_id, _manifest in list(_remaining.items()):
                    _deps = _manifest.get("dependencies") or []
                    if all(_dep in _active for _dep in _deps):
                        if _manifest.get("always_on") or self.is_mod_enabled(_mod_id):
                            _active[_mod_id] = _manifest
                        del _remaining[_mod_id]
                        _progressed = True
                if not _progressed:
                    break
            self._active_mods = _active

        def list_registered_mods(self):
            """EN: Return ALL registered mod ids (active or not) — the
                     main-menu Mod Manager lists these.
               ZH: 返回全部已注册 mod_id（含未激活）——主菜单
                     Mod 管理界面据此列表。"""
            return list(self._registered_mods.keys())

        def missing_dependencies(self, mod_id):
            """EN: Dependency ids of mod_id that are NOT currently active
                     (uninstalled or disabled) — shown as 缺少前置 in the
                     Mod Manager. Empty list for unknown mods.
               ZH: mod_id 的依赖中当前未激活的 id（未安装或被禁用）——
                     Mod 管理界面据此显示"缺少前置"。未知 mod 返回空列表。"""
            _manifest = self._registered_mods.get(mod_id)
            if not _manifest:
                return []
            return [_dep for _dep in (_manifest.get("dependencies") or [])
                    if _dep not in self._active_mods]

        def is_mod_active(self, mod_id):
            return mod_id in self._active_mods

        def list_active_mods(self):
            return list(self._active_mods.keys())

        # ── UI integration (home right menu, mods screen) ──

        def get_menu_buttons(self):
            """EN: Return [(mod_id, display_name, [button_screen_names])] for all
                     active mods that declared home right-menu buttons.
               ZH: 返回所有声明了主页右侧菜单按钮的激活 Mod 的
                     [(mod_id, 显示名, [按钮屏幕名])] 列表。"""
            result = []
            for mod_id, manifest in self._active_mods.items():
                buttons = manifest.get("home_rightmenu_add_buttons") or []
                if buttons:
                    result.append((mod_id, manifest.get("name", mod_id), list(buttons)))
            return result

        def get_mod_info(self, mod_id):
            """EN: Return a copy of the manifest for a REGISTERED mod (active
                     or not; the Mod Manager needs details of disabled mods).
                     None for unknown ids.
               ZH: 返回已注册 Mod（含未激活；Mod 管理界面需要展示被禁用
                     Mod 的详情）的 manifest 副本；未知 id 返回 None。"""
            manifest = self._registered_mods.get(mod_id)
            return dict(manifest) if manifest else None

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
                # EN: Skip callbacks belonging to inactive mods (disabled or
                #     missing dependencies); "_direct" hooks (registered via
                #     register_hook) are not attributable and always run.
                # ZH: 跳过属于未激活 Mod（被禁用/缺前置）的回调；
                #     "_direct" 钩子（register_hook 直注册）无法归属，始终执行。
                if mod_id != "_direct" and mod_id not in self._active_mods:
                    continue
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
                # EN: Same skip rule as execute_hook: inactive mods are
                #     filtered out by attribution.
                # ZH: 与 execute_hook 相同的过滤规则：
                #     按归属跳过未激活 Mod 的回调。
                if mod_id != "_direct" and mod_id not in self._active_mods:
                    continue
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
        HOOK_GIRL_DESTINATION_LIST = "girl_destination_list"
        HOOK_GIRL_DESTINATION_ACCEPT = "girl_destination_accept"

    # ── Singleton ──
    mod_api_v2 = ModAPIV2()
    services.register("mod_api_v2", mod_api_v2)


init -2 python:

    # ── game_saved hook via Ren'Py save callbacks ──
    # 通知 Mod: 游戏已保存 | Notify mods: game saved

    def _mod_api_v2_on_save(_save_data):
        mod_api_v2.execute_hook(mod_api_v2.HOOK_GAME_SAVED)

    # 防重复注册（init 重跑时避免多次 append） | Guard against duplicate registration
    if _mod_api_v2_on_save not in renpy.config.save_json_callbacks:
        renpy.config.save_json_callbacks.append(_mod_api_v2_on_save)
