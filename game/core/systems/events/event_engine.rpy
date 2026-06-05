## BK Phase 6 — Event Engine
## High-level event management system.
## Provides declarative event registration, custom event scanning,
## and runtime queue management. Integrates with EventRegistry,
## StoryEvent, and HookManager.

init -4 python:

    import os

    class EventEngine(object):
        """
        Central engine for registering, queueing, and managing StoryEvents.
        Backward compatible with event_dict, story_add_event(), and add_event().
        """

        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(EventEngine, cls).__new__(cls)
                cls._instance._scanned_files = []
                cls._instance._loaded_packs = []
            return cls._instance

        @classmethod
        def instance(cls):
            return cls.__new__(cls)

        # --- Registration ---

        def register_story_event(self, event_id, story_event, auto_add=False):
            """
            Register a StoryEvent to the EventRegistry.
            :param event_id: string identifier
            :param story_event: StoryEvent instance
            :param auto_add: if True, also add to the appropriate runtime queue
            :returns: the registered StoryEvent
            """
            event_registry.register_event(event_id, story_event)
            if auto_add:
                ev_type = story_event.type if story_event.type != "any" else "city"
                self.add_event_to_queue(event_id, event_type=ev_type)
            return story_event

        def register_event_from_dict(self, event_id, data_dict):
            """
            Create a StoryEvent from a dictionary and register it.
            :param event_id: string identifier
            :param data_dict: dict of StoryEvent constructor kwargs
            :returns: the registered StoryEvent
            """
            kwargs = dict(data_dict)
            if "label" not in kwargs:
                kwargs["label"] = event_id
            story_event = StoryEvent(**kwargs)
            return self.register_story_event(event_id, story_event)

        # --- Runtime Queue Management ---

        def add_event_to_queue(self, event_id, event_type="city"):
            """
            Add a registered event to the runtime queue.
            Matches legacy story_add_event() semantics: events with a location
            are forced into the city queue regardless of event_type.
            :param event_id: string identifier
            :param event_type: "city" or "daily"
            :returns: True if added (or already present), False if event unknown
            """
            event = event_registry.get_event(event_id)
            if event is None:
                if config.developer:
                    renpy.log("EventEngine: Cannot add unknown event '%s' to queue" % event_id)
                return False

            # Location forces city queue, matching story_add_event() logic
            if event_type == "city" or event.location:
                if event not in city_events:
                    city_events.append(event)
                    city_events.sort(key=lambda x: x.order)
                    # Keep registry queues in sync for forward compatibility
                    event_registry.add_to_city_events(event)
            else:
                if event not in daily_events:
                    daily_events.append(event)
                    daily_events.sort(key=lambda x: x.order)
                    # Keep registry queues in sync for forward compatibility
                    event_registry.add_to_daily_events(event)

            return True

        def remove_event_from_queue(self, event_id, event_type="city"):
            """
            Remove a registered event from the runtime queue.
            :param event_id: string identifier
            :param event_type: "city" or "daily"
            :returns: True if removed, False if not found or unknown
            """
            event = event_registry.get_event(event_id)
            if event is None:
                if config.developer:
                    renpy.log("EventEngine: Cannot remove unknown event '%s' from queue" % event_id)
                return False

            if event_type == "city":
                try:
                    city_events.remove(event)
                    return True
                except ValueError:
                    return False
            else:
                try:
                    daily_events.remove(event)
                    return True
                except ValueError:
                    return False

        # --- Custom Event Scanning ---

        def scan_custom_events(self):
            """
            Scan game/custom/events/ for .rpy files.
            :returns: list of absolute file paths
            """
            events_dir = os.path.join(config.gamedir, "custom", "events")
            if not os.path.isdir(events_dir):
                return []

            files = []
            for filename in sorted(os.listdir(events_dir)):
                if filename.endswith(".rpy"):
                    filepath = os.path.join(events_dir, filename)
                    files.append(filepath)
                    if filepath not in self._scanned_files:
                        self._scanned_files.append(filepath)

            return files

        def load_event_pack(self, filepath):
            """
            Dynamically load a custom event pack (.rpy file) at runtime.
            Uses renpy.load_string() for runtime script loading.
            :param filepath: absolute path to the .rpy file
            :returns: True on success, False on failure
            """
            if not os.path.isfile(filepath):
                if config.developer:
                    renpy.log("EventEngine: Event pack not found: %s" % filepath)
                return False

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                renpy.load_string(content, filename=filepath)
                if filepath not in self._loaded_packs:
                    self._loaded_packs.append(filepath)
                return True
            except Exception as e:
                if config.developer:
                    renpy.log("EventEngine: Failed to load event pack '%s': %s" % (filepath, str(e)))
                return False

        # --- Hook Integration ---

        def on_event_trigger(self, event_id, context=None):
            """
            Invoke hooks when an event is triggered.
            :param event_id: string identifier of the triggered event
            :param context: optional dict with trigger context
            :returns: list of hook callback return values
            """
            if context is None:
                context = {}
            return hook_manager.invoke("on_event_trigger", event_id, context)

        # --- Utility ---

        def get_loaded_packs(self):
            """Return list of file paths that have been loaded via load_event_pack()."""
            return list(self._loaded_packs)

        def get_scanned_files(self):
            """Return list of file paths that have been discovered via scan_custom_events()."""
            return list(self._scanned_files)

        def reset(self):
            """Clear internal tracking lists (does NOT affect queues or registry)."""
            self._scanned_files = []
            self._loaded_packs = []

    # Global handle
    event_engine = EventEngine.instance()
