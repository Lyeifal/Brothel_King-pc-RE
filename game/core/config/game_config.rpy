#### GameConfig — Centralized game configuration ####
# Phase 1.5: Single source of truth for all tunable game parameters.
# Replaces scatter-shot constants in settings.rpy, variables.rpy, options.rpy.
#
# Values can be overridden by JSON files in custom/config/ (mod-friendly).
# Fallback chain: JSON override → hardcoded default.

init -11 python:

    class GameConfig(object):
        """Centralized, documented game configuration.

        Access via: config = services.config
        All values have sensible defaults that match legacy behavior.
        """

        def __init__(self):
            self._data = {}
            self._load_defaults()
            self._load_json_overrides()

        def _load_defaults(self):
            """Set default values matching legacy settings.rpy behavior."""
            d = self._data

            # ── Girl pack directories ──
            d["girl_directories"] = ["custom/girls/"]

            # ── Image / memory ──
            d["image_cache_size"] = 144
            d["image_cache_size_mb"] = None  # Alternative: set MB instead of count
            d["refresh_memory_on_home"] = False

            # ── Save / autosave ──
            d["autosave_enabled"] = True
            d["autosave_frequency"] = 200
            d["autosave_slots"] = 12
            d["autosave_on_choice"] = False
            d["autosave_on_quit"] = False
            d["save_every_x_days"] = 2

            # ── Development ──
            d["developer_mode"] = True
            d["debug"] = False

            # ── Display ──
            d["max_item_shown"] = 30
            d["screen_width"] = 1920
            d["screen_height"] = 1080

            # ── Gameplay ──
            d["new_game_plus"] = False
            d["default_difficulty"] = "normal"
            d["cheats_enabled"] = False

            # ── I18N ──
            d["default_language"] = None  # None = English

            # ── Performance ──
            d["stock_picture_threshold"] = 4
            d["fuzzy_tagging_acts"] = True

        def _load_json_overrides(self):
            """Load mod/user overrides from custom/config/ JSON files."""
            try:
                import json, os
                config_dir = os.path.join(renpy.config.gamedir, "custom", "config")
                if os.path.exists(config_dir):
                    for fname in os.listdir(config_dir):
                        if fname.endswith(".json"):
                            with open(os.path.join(config_dir, fname), "r", encoding="utf-8") as f:
                                overrides = json.load(f)
                                self._data.update(overrides)
            except Exception:
                pass  # Overrides are optional

        # ── Accessors ──

        def get(self, key, default=None):
            return self._data.get(key, default)

        def set(self, key, value):
            self._data[key] = value

        def all(self):
            return dict(self._data)

        # ── Convenience properties for commonly accessed settings ──

        @property
        def girl_directories(self):
            return self._data["girl_directories"]

        @property
        def image_cache_size(self):
            return self._data["image_cache_size"]

        @property
        def debug(self):
            return self._data["debug"]

        @property
        def developer_mode(self):
            return self._data["developer_mode"]

        @property
        def default_language(self):
            return self._data["default_language"]

        @property
        def max_item_shown(self):
            return self._data["max_item_shown"]

        @property
        def save_every_x_days(self):
            return self._data["save_every_x_days"]


    # ── Singleton ──
    game_config = GameConfig()
    services.register("config", game_config)
