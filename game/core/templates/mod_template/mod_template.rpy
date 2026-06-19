## BK Phase 6 — Mod Template
## This is a starter template for creating Brothel King mods.
## Place this file in game/custom/mods/<YourModName>/

init 1 python:

    # 1. DECLARE THE MOD
    my_mod = Mod(
        name="My Awesome Mod",
        folder="mod_template",  # Must match the folder name
        creator="Your Name",
        version=1.0,
        description=__("This is a sample mod demonstrating the Phase 6 API."),
        help_prompts=[
            ("About this mod", "bk_template_mod_about"),
        ],
        init_label="bk_template_mod_init",
        night_label="bk_template_mod_night",
        early_label="",
        update_label="",
        load_label="",
        remove_label="bk_template_mod_remove",
    )

    # 2. REGISTER HOOKS (Phase 6)
    # Hooks let your mod intercept core game events safely.
    def on_girl_generated(girl):
        # Example: give every generated girl a small bonus
        pass

    def on_day_ended():
        # Example: log something at end of day
        pass

    my_mod.hooks = {
        "on_girl_generate": on_girl_generated,
        "on_day_end": on_day_ended,
    }

    # 3. REGISTER CUSTOM CONTENT VIA API (Phase 6)
    # Traits, perks, tags, dialogue, events, and NG+ settings can all be registered.

    # mod_api.register_trait(
    #     Trait("Lucky", verb="be", effects=[Effect("special", "lucky")])
    # )

    # mod_api.register_tag("custom_tag", ("custom",))

    # mod_api.register_dialogue(
    #     topic="free_greetings_polite",
    #     key="generic",
    #     dialogue=Dialogue("Hello from my mod!"),
    #     merge=True,
    # )

    # mod_api.register_event(
    #     "my_mod_event",
    #     StoryEvent("my_mod_event_label", type="city", location="market", chance=0.5),
    # )

    # 4. REGISTER CUSTOM NG+ SETTING (Phase 6)
    # mod_api.register_ngp_setting(
    #     "my_mod_bonus",
    #     NGPSetting("mod bonus gold", "gold", label="Mod Bonus", values=[100, 500], cost=[1, 2]),
    #     category="resources",
    # )


# --- LABELS ---

label bk_template_mod_init:
    # Runs when the mod is activated (after district/brothel setup)
    "System" "My Awesome Mod has been activated!"
    return

label bk_template_mod_night:
    # Runs every night (added to daily_events automatically if night_label is set)
    return

label bk_template_mod_about:
    # Called from the Mod help menu
    "System" "This is a sample mod for Brothel King Phase 6."
    return

label bk_template_mod_remove:
    # Runs when the mod is deactivated
    "System" "My Awesome Mod has been removed."
    return

# Example custom event label (if you register an event pointing here)
label bk_template_mod_event_label:
    "System" "You encountered a custom event from My Awesome Mod!"
    return
