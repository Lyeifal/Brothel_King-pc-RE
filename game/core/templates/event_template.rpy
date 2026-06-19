## ============================================================================
## BK Custom Event Pack Template
## ============================================================================
## Copy this file to game/core/content/events/ and rename it to your_mod_events.rpy
## Then fill in your custom events below.
##
## Recommended init level for custom events: init 1 (after all core systems).
## ============================================================================

init 1 python:

    # -------------------------------------------------------------------------
    # EXAMPLE 1: Register a simple city event using mod_api
    # -------------------------------------------------------------------------
    # my_city_event = StoryEvent(
    #     label="my_custom_city_event",
    #     chapter=1,
    #     type="city",
    #     location="docks",
    #     chance=0.5,
    #     once=True,
    #     order=10
    # )
    # mod_api.register_event("my_city_event_id", my_city_event)
    # event_engine.add_event_to_queue("my_city_event_id", event_type="city")

    # -------------------------------------------------------------------------
    # EXAMPLE 2: Register a daily event from a dictionary
    # -------------------------------------------------------------------------
    # event_engine.register_event_from_dict("my_daily_event_id", {
    #     "label": "my_custom_daily_event",
    #     "chapter": 2,
    #     "type": "day",
    #     "chance": 1.0,
    #     "once": False,
    #     "order": 5,
    #     "min_gold": 100
    # })
    # event_engine.add_event_to_queue("my_daily_event_id", event_type="daily")

    # -------------------------------------------------------------------------
    # EXAMPLE 3: Register and auto-add in one call
    # -------------------------------------------------------------------------
    # my_auto_event = StoryEvent(
    #     label="my_auto_event",
    #     chapter=1,
    #     type="night",
    #     chance=0.25,
    #     once=False
    # )
    # event_engine.register_story_event("my_auto_event_id", my_auto_event, auto_add=True)

    # -------------------------------------------------------------------------
    # EXAMPLE 4: Hook into event triggers
    # -------------------------------------------------------------------------
    # def my_event_trigger_hook(event_id, context):
    #     if event_id == "my_city_event_id":
    #         # React to the event being triggered (e.g. log analytics)
    #         pass
    #
    # mod_api.hook("on_event_trigger", my_event_trigger_hook)

    pass


## ============================================================================
## Ren'Py labels for your custom events go below this line.
## ============================================================================

# label my_custom_city_event:
#     "This is my custom city event!"
#     return
#
# label my_custom_daily_event:
#     "This is my custom daily event!"
#     return
