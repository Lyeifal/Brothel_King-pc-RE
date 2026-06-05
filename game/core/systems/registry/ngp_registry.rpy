## BK Phase 6 — New Game+ Registry
## Replaces the hard-coded NGP_settings / NGP_settings_dict from gameplay/start.rpy
## Supports runtime NG+ setting registration for Mods.

init -5 python:

    class NGPRegistry(Registry):
        """Registry for all New Game+ settings."""

        def __init__(self):
            super(NGPRegistry, self).__init__(name="NGPRegistry")

        def register_ngp(self, setting_id, ngp_setting, category="misc"):
            """
            Register an NGPSetting.
            :param setting_id: string identifier (same as setting.name)
            :param ngp_setting: NGPSetting instance
            :param category: UI grouping ("resources", "girls", "MC", "misc")
            """
            self.register(setting_id, ngp_setting, category=category)
            return ngp_setting

        def get_ngp(self, setting_id):
            return self.get(setting_id)

        def get_ngp_settings_list(self):
            """Return list of all NGPSetting objects (for backward compat)."""
            return list(self.values())

        def get_ngp_settings_dict(self):
            """Return {name: NGPSetting} dict (for backward compat)."""
            return self.get_all()

        def get_by_category(self, category):
            """Return all settings in a UI category."""
            return super(NGPRegistry, self).get_by_category(category)

    _ngp_registry = NGPRegistry()
    ngp_registry = _ngp_registry
    NGP_settings_dict = _RegistryProxy(_ngp_registry)
