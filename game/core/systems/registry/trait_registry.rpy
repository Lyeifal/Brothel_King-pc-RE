## BK Phase 6 — Trait Registry
## Replaces the hard-coded trait_dict from systems/traits.rpy
## Supports runtime trait registration for Mods.

init -5 python:

    class TraitRegistry(Registry):
        """Registry for all Trait definitions."""

        def __init__(self):
            super(TraitRegistry, self).__init__(name="TraitRegistry")

        def register_trait(self, trait, category=None):
            """
            Register a Trait instance.
            :param trait: Trait object
            :param category: optional category ("gold", "positive", "negative", "special")
            """
            self.register(trait.name, trait, category=category)
            return trait

        def get_trait(self, name):
            return self.get(name)

        def get_traits_by_category(self, category):
            return list(self.get_by_category(category).values())

        def get_all_traits(self):
            return list(self.values())

    _trait_registry = TraitRegistry()
    trait_registry = _trait_registry
    trait_dict = _RegistryProxy(_trait_registry)
