## BK Phase 6 — Mod API
## Safe, high-level API for Mod authors.  Wraps Registry and HookManager calls.

init -3 python:

    class ModAPI(object):
        """
        Public API surface for Mods.
        All methods are safe to call from Mod init blocks (init -2 ~ init 1).
        """

        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(ModAPI, cls).__new__(cls)
            return cls._instance

        @classmethod
        def instance(cls):
            return cls.__new__(cls)

        # --- Registry Wrappers ---

        def register_trait(self, trait, category=None):
            """Register a custom Trait."""
            return trait_registry.register_trait(trait, category=category)

        def register_perk(self, perk, category=None):
            """Register a custom Perk."""
            return perk_registry.register_perk(perk, category=category)

        def register_tag(self, filename_substring, game_tags):
            """Register a custom picture tag mapping."""
            return tag_registry.register_tag(filename_substring, game_tags)

        def register_dialogue(self, topic, key, dialogue, merge=True):
            """Register custom dialogue lines."""
            return dialogue_registry.register_dialogue(topic, key, dialogue, merge=merge)

        def register_event(self, event_id, event, category=None):
            """Register a custom StoryEvent."""
            return event_registry.register_event(event_id, event, category=category)

        def register_ngp_setting(self, setting_id, ngp_setting, category="misc"):
            """Register a custom New Game+ setting."""
            return ngp_registry.register_ngp(setting_id, ngp_setting, category=category)

        def register_game_mode(self, mode):
            """EN: Register a custom game mode.
               ZH: 注册一个自定义游戏模式。"""
            return gamemode_registry.register(mode)

        def register_quality(self, tier):
            """EN: Register a custom item quality tier (QualityTier), keyed by
                   its rank. Overwrites any tier of the same rank, so a Mod can
                   retune or extend the default 0-6 range.
               ZH: 注册一个自定义物品品质档位（QualityTier），按其 rank 键控。
                   同 rank 覆盖，因此 Mod 可调整或扩展默认的 0-6 档范围。"""
            return quality_registry.register_quality(tier)

        # --- Hook Wrappers ---

        def hook(self, hook_name, callback, mod=None):
            """Register a hook callback."""
            return hook_manager.register(hook_name, callback, mod=mod)

        def unhook(self, hook_name, callback):
            """Unregister a hook callback."""
            return hook_manager.unregister(hook_name, callback)

        # --- Utility ---

        def get_mod_path(self, mod_name):
            """Return the folder path for a registered Mod."""
            mod = detected_mods.get(mod_name)
            return mod.path if mod else None

        def is_mod_active(self, mod_name):
            """Check if a Mod is currently active."""
            mod = detected_mods.get(mod_name)
            return mod.active if mod else False

        def get_active_mods(self):
            """Return list of currently active Mod names."""
            return [m.name for m in detected_mods.values() if m.active]

    # Global API handle (use this in Mods: mod_api.register_trait(...))
    mod_api = ModAPI.instance()
