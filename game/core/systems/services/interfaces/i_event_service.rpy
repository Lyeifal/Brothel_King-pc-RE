#### IEventService — Event management interface ####
# Phase 1.2: Defines the contract for event registration, dispatch,
# and condition evaluation. Implemented by EventEngine.

init -12 python:

    class IEventService(object):
        """Interface for event management.

        Concrete implementation: EventEngine in systems/events/event_engine.rpy
        """

        # ── Event registration ──

        def register_event(self, event_id, event_def):
            """Register a StoryEvent definition by id."""
            raise NotImplementedError

        def add_event_to_queue(self, event_id, **kwargs):
            """Add an event to the runtime queue for dispatch."""
            raise NotImplementedError

        def remove_event_from_queue(self, event_id):
            """Remove an event from the runtime queue."""
            raise NotImplementedError

        # ── Event dispatch ──

        def get_events(self, event_type, **conditions):
            """Return events matching type and conditions, sorted by priority."""
            raise NotImplementedError

        def happens(self, event, **context):
            """Evaluate whether an event should trigger given the current context."""
            raise NotImplementedError

        # ── Event lifecycle ──

        def clear_queue(self, event_type=None):
            """Clear the event queue, optionally filtered by type."""
            raise NotImplementedError

        def on_day_start(self):
            """Called at the start of each game day."""
            raise NotImplementedError

        def on_day_end(self):
            """Called at the end of each game day."""
            raise NotImplementedError
