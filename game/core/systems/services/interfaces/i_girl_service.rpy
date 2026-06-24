#### IGirlService — Girl lifecycle management interface ####
# Phase 1.2: Defines the contract for girl creation, serialization,
# and collection management.

init -12 python:

    class IGirlService(object):
        """Interface for girl lifecycle management."""

        def generate_girl(self, pack_name=None, template=None, **kwargs):
            """Create and randomize a new girl from a pack or template."""
            raise NotImplementedError

        def get_girl_packs(self):
            """Return list of all available girl pack names."""
            raise NotImplementedError

        def get_active_girls(self):
            """Return all girls currently in the game (brothel, market, free, farm)."""
            raise NotImplementedError

        def save_girl_state(self, girl):
            """Serialize a girl to a dict for save/load."""
            raise NotImplementedError

        def restore_girl_state(self, data):
            """Restore a girl from serialized state."""
            raise NotImplementedError
