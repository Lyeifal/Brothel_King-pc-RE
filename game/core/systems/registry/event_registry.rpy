## BK Phase 6 — Event Registry
## Replaces the hard-coded event_dict from gameplay/start.rpy
## Supports runtime event registration for Mods and custom events.

init -5 python:

    class EventRegistry(Registry):
        """Registry for all StoryEvent definitions."""

        def __init__(self):
            super(EventRegistry, self).__init__(name="EventRegistry")
            # Keep separate lists for runtime event queues (not part of Registry base)
            self._city_events = []
            self._daily_events = []
            self._night_checks = []

        def register_event(self, event_id, event, category=None):
            """
            Register a StoryEvent.
            :param event_id: string identifier
            :param event: StoryEvent instance
            :param category: optional ("chapter1", "farm", "side", etc.)
            """
            self.register(event_id, event, category=category)
            return event

        def get_event(self, event_id):
            return self.get(event_id)

        def add_to_city_events(self, event):
            """Add a StoryEvent to the runtime city event queue."""
            self._city_events.append(event)
            self._city_events.sort(key=lambda ev: ev.order)

        def add_to_daily_events(self, event):
            """Add a StoryEvent to the runtime daily event queue."""
            self._daily_events.append(event)
            self._daily_events.sort(key=lambda ev: ev.order)

        def add_night_check(self, check):
            """Add a night check [girl, label] tuple."""
            self._night_checks.append(check)

        def get_city_events(self):
            return self._city_events

        def get_daily_events(self):
            return self._daily_events

        def get_night_checks(self):
            return self._night_checks

        def clear_runtime_queues(self):
            self._city_events = []
            self._daily_events = []
            self._night_checks = []

        def reset(self):
            """Clear both registry and runtime queues."""
            self.clear()
            self.clear_runtime_queues()

    _event_registry = EventRegistry()
    event_registry = _event_registry
    event_dict = _RegistryProxy(_event_registry)
