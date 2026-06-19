## BK Phase 6 — Unified Registry System
## Base Registry class and shared utilities
## All registries are rebuilt at init time; nothing is persisted to save files.

init -10 python:

    class Registry(object):
        """
        Base class for all BK registries.
        Provides dict-backed O(1) registration/lookup with overwrite warnings.
        Subclass per domain (Tag, Event, Trait, Perk, Dialogue, NGP).
        """

        _instances = {}

        def __new__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(Registry, cls).__new__(cls)
                cls._instances[cls]._initialized = False
            return cls._instances[cls]

        @classmethod
        def instance(cls):
            return cls.__new__(cls)

        def __init__(self, name="Registry"):
            if self._initialized:
                return
            self._name = name
            self._registry = {}   # id -> obj
            self._categories = {} # id -> category
            self._by_category = {} # category -> {id: obj}
            self._initialized = True

        # --- Core API ---

        def register(self, obj_id, obj, category=None):
            """
            Register an object.  If obj_id already exists, warn and overwrite
            (later registrations take precedence, enabling Mod overrides).
            """
            if obj_id in self._registry:
                if config.developer:
                    renpy.log(__("%s: overwriting '%s' (was %s) with %s") % (self._name, obj_id, self._registry[obj_id], obj))
            self._registry[obj_id] = obj
            self._categories[obj_id] = category
            if category is not None:
                if category not in self._by_category:
                    self._by_category[category] = {}
                self._by_category[category][obj_id] = obj
            return obj

        def unregister(self, obj_id):
            """Remove an object from the registry."""
            if obj_id in self._registry:
                del self._registry[obj_id]
            cat = self._categories.pop(obj_id, None)
            if cat and cat in self._by_category:
                self._by_category[cat].pop(obj_id, None)

        def get(self, obj_id, default=None):
            """Lookup by id."""
            return self._registry.get(obj_id, default)

        def __getitem__(self, obj_id):
            return self._registry[obj_id]

        def __contains__(self, obj_id):
            return obj_id in self._registry

        def get_all(self):
            """Return a dict copy of the full registry."""
            return self._registry.copy()

        def keys(self):
            return self._registry.keys()

        def values(self):
            return self._registry.values()

        def items(self):
            return self._registry.items()

        def get_by_category(self, category):
            """Return all objects in a given category."""
            return self._by_category.get(category, {}).copy()

        def get_categories(self):
            return list(self._by_category.keys())

        def clear(self):
            self._registry.clear()
            self._categories.clear()
            self._by_category.clear()

        def __len__(self):
            return len(self._registry)

        def __repr__(self):
            return __("<%s: %d entries>") % (self._name, len(self._registry))

    # Helper: expose a dict-like view for backward compat
    class _RegistryProxy(object):
        """
        Proxy that makes a Registry instance look like a dict.
        Supports dict[key], dict[key] = value, del dict[key], key in dict,
        dict.get(key), dict.keys(), dict.values(), dict.items().
        Assignments delegate to Registry.register(); deletions to unregister().
        """
        def __init__(self, registry):
            self._registry = registry

        def __getitem__(self, key):
            return self._registry.get(key)

        def __setitem__(self, key, value):
            self._registry.register(key, value)

        def __delitem__(self, key):
            self._registry.unregister(key)

        def __contains__(self, key):
            return key in self._registry

        def get(self, key, default=None):
            return self._registry.get(key, default)

        def keys(self):
            return self._registry.keys()

        def values(self):
            return self._registry.values()

        def items(self):
            return self._registry.items()

        def __len__(self):
            return len(self._registry)

        def __iter__(self):
            return iter(self._registry.keys())

        def __repr__(self):
            return "<RegistryProxy %s>" % repr(self._registry)
