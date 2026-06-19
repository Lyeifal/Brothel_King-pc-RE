## BK Phase 6 — Meta Progression Registry
## Replaces scattered persistent-only meta progression with a queryable registry.
## Supports runtime meta upgrade registration for Mods.

init -5 python:

    class MetaRegistry(Registry):
        """Registry for all permanent cross-run meta upgrades."""

        def __init__(self):
            super(MetaRegistry, self).__init__(name="MetaRegistry")

        def register_meta(self, upgrade_id, meta_upgrade, category="general"):
            """
            Register a MetaUpgrade.
            :param upgrade_id: string identifier
            :param meta_upgrade: MetaUpgrade instance
            :param category: optional UI grouping
            """
            self.register(upgrade_id, meta_upgrade, category=category)
            return meta_upgrade

        def get_meta(self, upgrade_id):
            return self.get(upgrade_id)

        def get_meta_list(self):
            """Return list of all MetaUpgrade objects."""
            return list(self.values())

        def get_meta_dict(self):
            """Return {id: MetaUpgrade} dict."""
            return self.get_all()

        def get_unlocked(self):
            """Return upgrades whose unlock_condition is satisfied."""
            return [m for m in self.values() if m.rank > 0]

    _meta_registry = MetaRegistry()
    meta_registry = _meta_registry
    meta_dict = _RegistryProxy(_meta_registry)
