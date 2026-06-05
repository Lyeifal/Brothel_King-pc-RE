## BK Phase 6 — Perk Registry
## Replaces the hard-coded perk_dict from data/perks.rpy
## Supports runtime perk registration for Mods.

init -5 python:

    class PerkRegistry(Registry):
        """Registry for all Perk definitions."""

        def __init__(self):
            super(PerkRegistry, self).__init__(name="PerkRegistry")

        def register_perk(self, perk, category=None):
            """
            Register a Perk instance.
            :param perk: Perk object
            :param category: optional category (e.g., archetype name)
            """
            self.register(perk.name, perk, category=category)
            return perk

        def get_perk(self, name):
            return self.get(name)

        def get_perks_by_archetype(self, archetype):
            return list(self.get_by_category(archetype).values())

        def get_all_perks(self):
            return list(self.values())

    _perk_registry = PerkRegistry()
    perk_registry = _perk_registry
    perk_dict = _RegistryProxy(_perk_registry)
