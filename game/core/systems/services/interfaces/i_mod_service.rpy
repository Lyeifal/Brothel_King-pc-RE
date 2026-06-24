#### IModService — Mod lifecycle and hook management interface ####
# Phase 1.2: Defines the contract for mod registration, activation,
# and hook execution.

init -12 python:

    class IModService(object):
        """Interface for mod management.

        Concrete implementations: ModAPI (v1/v2), HookManager.
        """

        def register_mod(self, mod_def):
            """Register a new mod definition."""
            raise NotImplementedError

        def activate_mod(self, mod_id):
            """Enable a mod for the current game session."""
            raise NotImplementedError

        def deactivate_mod(self, mod_id):
            """Disable a mod, cleaning up its hooks and state."""
            raise NotImplementedError

        def get_active_mods(self):
            """Return dict of currently active mods."""
            raise NotImplementedError

        def register_hook(self, hook_name, callback, priority=0):
            """Register a callback for a named hook point."""
            raise NotImplementedError

        def execute_hook(self, hook_name, **context):
            """Execute all registered callbacks for a hook point."""
            raise NotImplementedError
