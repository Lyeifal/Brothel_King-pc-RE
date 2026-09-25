## BK Evolution — Unlock Registry
##
## EN: Centralized unlock state management. Decouples "what is unlocked"
##     from "who uses it" (Location, Farm, NPC shops, etc.).
##     Unlock states are persistent (saved to Ren'Py save files).
##
## ZH: 集中式解锁状态管理。将"什么已解锁"与"谁在使用它"
##     （Location、Farm、NPC 商店等）解耦。
##     解锁状态是持久化的（保存到 Ren'Py 存档中）。

init -9 python:

    class UnlockRegistry(Registry):
        """
        EN: Tracks which locations, systems, NPCs, or features are unlocked.
            Uses a plain set for state (pickle-friendly, Ren'Py save compatible).
            All systems query this registry instead of checking .action / .active
            on scattered global objects.

           ZH: 追踪哪些地点、系统、NPC 或功能已解锁。
            使用普通 set 存储状态（pickle 友好，兼容 Ren'Py 存档）。
            所有系统通过此注册表查询，而非在零散的全局对象上检查 .action / .active。
        """

        def __init__(self):
            super(UnlockRegistry, self).__init__(name="UnlockRegistry")
            self._unlocked = set()  # EN: Set of unlocked ids. ZH: 已解锁 id 集合。

        # --- State API ---

        def unlock(self, unlock_id):
            """EN: Mark an id as unlocked. ZH: 将指定 id 标记为已解锁。"""
            self._unlocked.add(unlock_id)
            ## EN: If the id matches a city location (exposed as a store
            ##     global by the world loader), also enable its action
            ##     button and un-hide it. The registry→Location reverse
            ##     sync was missing, leaving e.g. Goldie's ranch button
            ##     permanently disabled after unlock("farmland").
            ## ZH: 若 id 对应城市地点（world loader 已按 id 暴露为 store
            ##     全局变量），同时启用其操作按钮并取消隐藏。此前缺少
            ##     注册表→Location 的反向同步，导致 unlock("farmland")
            ##     后 Goldie 牧场按钮仍永久禁用。
            try:
                _loc = getattr(store, unlock_id, None)
                if _loc is not None and hasattr(_loc, "action"):
                    _loc.action = True
                    _loc.secret = False
            except Exception:
                pass

        def lock(self, unlock_id):
            """EN: Mark an id as locked (re-lock). ZH: 将指定 id 标记为锁定（重新锁定）。"""
            self._unlocked.discard(unlock_id)

        def is_unlocked(self, unlock_id):
            """EN: Check if an id is unlocked. ZH: 检查指定 id 是否已解锁。"""
            return unlock_id in self._unlocked

        def toggle(self, unlock_id):
            """EN: Toggle unlock state. ZH: 切换解锁状态。"""
            if unlock_id in self._unlocked:
                self._unlocked.discard(unlock_id)
            else:
                self._unlocked.add(unlock_id)

        def get_all_unlocked(self):
            """EN: Return a copy of all unlocked ids. ZH: 返回所有已解锁 id 的副本。"""
            return self._unlocked.copy()

        def load_defaults(self, default_ids):
            """
            EN: Unlock a list of ids (used at init time for default unlocks).
               Does not re-lock already-unlocked ids.
            ZH: 解锁一组 id（在 init 阶段用于默认解锁）。
               不会重新锁定已解锁的 id。
            """
            for uid in default_ids:
                self._unlocked.add(uid)

        def reset(self):
            """EN: Clear all unlocks. Use with caution. ZH: 清除所有解锁状态。慎用。"""
            self._unlocked.clear()

        # --- Serialization helpers (for Ren'Py save compatibility) ---

        def __getstate__(self):
            return {"_unlocked": list(self._unlocked)}

        def __setstate__(self, state):
            self.__init__()
            self._unlocked = set(state.get("_unlocked", []))

    # Create singleton instance
    unlock_registry = UnlockRegistry()

    # EN: Convenience functions for use in Ren'Py script (e.g. $ unlock("farm"))
    # ZH: 便利函数，供 Ren'Py 脚本使用（如 $ unlock("farm")）
    def unlock(unlock_id):
        unlock_registry.unlock(unlock_id)

    def is_unlocked(unlock_id):
        return unlock_registry.is_unlocked(unlock_id)

    def lock(unlock_id):
        unlock_registry.lock(unlock_id)
