## BK Phase 6 — Mod Hook System
## Provides a centralized hook/callback mechanism for Mods to intercept core game logic.

init -4 python:

    class HookManager(object):
        """
        Central hook dispatcher for the Mod system.
        Mods can register callbacks at named hook points; the game invokes
        them at the appropriate times.
        
        Hooks are stored as a dict: {hook_name: [(callback, mod), ...]}
        Callbacks are invoked in registration order.
        """

        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(HookManager, cls).__new__(cls)
                cls._instance._hooks = {}
                cls._instance._enabled = True
            return cls._instance

        @classmethod
        def instance(cls):
            return cls.__new__(cls)

        def register(self, hook_name, callback, mod=None):
            """
            Register a callback for a hook point.
            :param hook_name: string identifier (e.g. "on_girl_generate")
            :param callback: callable(*args, **kwargs)
            :param mod: optional Mod instance (for debugging / disable)
            """
            if hook_name not in self._hooks:
                self._hooks[hook_name] = []
            self._hooks[hook_name].append((callback, mod))

        def unregister(self, hook_name, callback):
            """Remove a specific callback from a hook."""
            if hook_name in self._hooks:
                self._hooks[hook_name] = [(cb, m) for cb, m in self._hooks[hook_name] if cb is not callback]

        def unregister_mod(self, mod):
            """Remove all callbacks registered by a given Mod."""
            for hook_name in self._hooks:
                self._hooks[hook_name] = [(cb, m) for cb, m in self._hooks[hook_name] if m is not mod]

        def invoke(self, hook_name, *args, **kwargs):
            """
            Invoke all callbacks for a hook point.
            :returns: list of callback return values (None for callbacks that return nothing)
            """
            if not self._enabled:
                return []
            results = []
            for callback, mod in self._hooks.get(hook_name, []):
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    if config.developer:
                        renpy.log(__("Hook error in '%s' (mod: %s): %s") % (hook_name, mod.name if mod else "unknown", str(e)))
            return results

        def invoke_first(self, hook_name, *args, **kwargs):
            """
            Invoke callbacks until one returns a non-None value, then return it.
            Useful for hooks that allow Mods to override default behavior.
            :returns: first non-None result, or None if all returned None
            """
            if not self._enabled:
                return None
            for callback, mod in self._hooks.get(hook_name, []):
                try:
                    result = callback(*args, **kwargs)
                    if result is not None:
                        return result
                except Exception as e:
                    if config.developer:
                        renpy.log(__("Hook error in '%s' (mod: %s): %s") % (hook_name, mod.name if mod else "unknown", str(e)))
            return None

        def has_hooks(self, hook_name):
            return hook_name in self._hooks and len(self._hooks[hook_name]) > 0

        def clear(self):
            self._hooks.clear()

        def enable(self):
            self._enabled = True

        def disable(self):
            self._enabled = False

    # Expose singleton
    hook_manager = HookManager.instance()

    # Convenience function for one-liner hook registration
    def register_hook(hook_name, callback, mod=None):
        hook_manager.register(hook_name, callback, mod=mod)
