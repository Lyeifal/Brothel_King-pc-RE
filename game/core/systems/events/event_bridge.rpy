#### Event Bridge — Compatibility shim for old/new event systems ####
# Phase 1.3: Ensures that code using the old event system
# (city_events, daily_events globals) and the new system
# (EventEngine + EventRegistry) see the same events.
#
# When both systems are active, this bridge syncs changes:
#   - Old → New: add_event() / story_add_event() also register with EventEngine
#   - New → Old: EventEngine registrations are visible via event_dict proxy
#
# The event_dict proxy (event_registry.rpy line 65) already handles
# the New → Old direction. This module adds Old → New sync.
#
# Migration path:
#   Phase 1.3: Bridge active (both systems coexist)
#   Phase 5:   Old system deprecated, new callers use EventEngine directly
#   Phase 6:   Old globals removed

init -11 python:

    class EventBridge(object):
        """Syncs old global event lists with the new EventEngine.

        Singleton. Created early so both old and new code can use it.
        """

        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(EventBridge, cls).__new__(cls)
            return cls._instance

        @classmethod
        def instance(cls):
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

        @staticmethod
        def sync_to_engine(event, event_type):
            """Sync an event added via the old API to the EventEngine.

            Called by add_event() after it appends to city_events/daily_events.

            Args:
                event: StoryEvent instance
                event_type: "city" or "day" (old API type)
            """
            try:
                engine = services.get("event_engine")
                if engine is not None:
                    engine.register_runtime_event(event, event_type)
            except Exception:
                pass  # Bridge failure should never crash the game

        @staticmethod
        def sync_remove_to_engine(event_label, event_type):
            """Sync an event removal via the old API to the EventEngine."""
            try:
                engine = services.get("event_engine")
                if engine is not None:
                    engine.unregister_runtime_event(event_label, event_type)
            except Exception:
                pass


    # Singleton
    event_bridge = EventBridge()
