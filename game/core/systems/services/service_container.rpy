#### GameServices — Centralized service locator for Brothel King ####
# Phase 1.1: Replaces scattered global singletons with a single service
# container. Services are registered at their respective init levels and
# accessed through `services.game`, `services.mc`, etc.
#
# Migration strategy:
#   1. Create container early (init -12)
#   2. Register services as they are created at their init levels
#   3. Keep old module-level globals as aliases (backward compat)
#   4. Gradually migrate all references to services.xxx
#
# All existing code continues to work — global aliases are set up
# after each service registration.

init -12 python:

    class GameServices(object):
        """Central service locator for all game singletons.

        Usage:
            services = GameServices.instance()
            services.register("game", game_obj)
            game = services.game    # typed property access
            game = services.get("game")  # key-based access
        """

        _instance = None
        _services = {}

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(GameServices, cls).__new__(cls)
            return cls._instance

        @classmethod
        def instance(cls):
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

        def register(self, key, service):
            """Register a service. Overwrites if already registered (for reload scenarios)."""
            self._services[key] = service

        def unregister(self, key):
            """Remove a service (e.g. on game reset)."""
            self._services.pop(key, None)

        def get(self, key, default=None):
            """Get a service by key. Returns default if not found."""
            return self._services.get(key, default)

        def has(self, key):
            """Check if a service is registered."""
            return key in self._services

        def require(self, key):
            """Get a service, raising an error if not registered."""
            if key not in self._services:
                raise RuntimeError(
                    "Required service '%s' is not registered. "
                    "Check init priority ordering." % key
                )
            return self._services[key]

        def list_services(self):
            """Return all registered service keys (for debugging)."""
            return sorted(self._services.keys())

        # ── Typed property accessors for common services ──
        # These provide IDE-friendly access: services.game, services.mc, etc.

        @property
        def game(self):
            return self.get("game")

        @property
        def mc(self):
            return self.get("mc")

        @property
        def brothel(self):
            return self.get("brothel")

        @property
        def farm(self):
            return self.get("farm")

        @property
        def calendar(self):
            return self.get("calendar")

        @property
        def event_engine(self):
            return self.get("event_engine")

        @property
        def girl_files_dict(self):
            return self.get("girl_files_dict")

        @property
        def i18n(self):
            return self.get("i18n")

        @property
        def mod_api(self):
            return self.get("mod_api")

        @property
        def config(self):
            return self.get("config")

        @property
        def data_loader(self):
            return self.get("data_loader")


    # ── Singleton instance ──
    services = GameServices()

    # ── Convenience: register utility globals early ──
    # Many modules at init -10 through init -2 declare globals that other
    # modules depend on. We register them in __init__.rpy and the respective
    # module files once they exist.


# ── Dependency assertion helper ──
# Use in init blocks to verify that required services exist before
# running code that depends on them.

init -11 python:

    def require_service(key, message=None):
        """Assert that a service is registered. Use at the start of init blocks.

        Example:
            init -2 python:
                require_service("tag_dict")
        """
        if not services.has(key):
            msg = message or (
                "Service '%s' is required but not yet registered. "
                "Check that it is registered at an earlier init priority." % key
            )
            raise RuntimeError(msg)


# ── Phase 1.4: Init priority documentation ──
# Services are registered at these init levels:
#
#   init -10:  bk_language_map, persistent defaults, config.image_cache_size
#   init -4:   tag_dict (loaded from JSON), tag_list_dict
#   init -3:   globalFilesDict (GirlFilesDict), utility globals
#   init -2:   Class definitions only (no instances)
#   init:      game, MC, brothel, farm, calendar (start.rpy label)
