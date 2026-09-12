## BK Phase 6 — Mod Template (v2 API)
## This is a starter template for creating Brothel King mods.
## Place this file in game/custom/mods/<YourModName>/

init 1 python:

    # ── 1. DECLARE THE MOD (v2 API with capability flags) ──
    api = ModAPIV2.instance()

    my_mod_manifest = {
        "name": "My Awesome Mod",
        "version": "1.0.0",
        "api_version": 2,
        "min_game_version": "0.3.0",
        "author": "Your Name",
        "description": __("This is a sample mod demonstrating the v2 API."),
        "requires": ["girl_traits", "events"],  # Capability flags
        "dependencies": [],                      # Other mod IDs this depends on
        "hooks": {},                              # {hook_name: callback} dict
        # EN: No-arg screens shown in the home right menu under "Mods".
        # ZH: 显示在主页右侧菜单 "Mods" 下的无参屏幕列表。
        "home_rightmenu_add_buttons": [],
    }

    api.register_mod("my_awesome_mod", my_mod_manifest)

    # ── 2. REGISTER CUSTOM CONTENT ──

    # Register a custom trait
    # custom_trait = Trait(name="Custom", verb="customizes", effects=[...])
    # api.register_trait(custom_trait, category="community")

    # Register a custom event
    # custom_event = StoryEvent(label="my_custom_event", type="city", chance=0.3)
    # api.register_event("my_custom_event", custom_event, category="community")

    # ── 3. REGISTER HOOKS (v2 standardized naming) ──
    # Hook naming: <domain>_<action>_<tense>
    # Available hooks: see ModAPIV2.HOOK_* constants

    def on_girl_generated(context):
        # context = {"girl": Girl instance, "pack_name": str}
        girl = context.get("girl")
        # Custom logic here
        pass

    api.register_hook(api.HOOK_GIRL_GENERATED, on_girl_generated, priority=0)

    def on_night_finished(context):
        # context = {"log": NightLog instance, "net_gold": int}
        pass

    api.register_hook(api.HOOK_NIGHT_FINISHED, on_night_finished)

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

    # 5. REGISTER CUSTOM ITEM QUALITY TIERS (requires: ["items"])
    # EN: Same rank overwrites (last registration wins), so a mod can retune the
    #     default 0-6 tiers or extend beyond 7. Data-driven reference: the
    #     "Item Quality" mod (custom/mods/Item Quality/), which also shows how to
    #     gate registration behind is_mod_active() and ship its own tl/ strings.
    # ZH: 同 rank 覆盖（后注册者胜），可调整默认 0-6 档或扩展更多档位。
    #     数据型范例见 custom/mods/Item Quality/（含 is_mod_active 门控与自带 tl/ 翻译）。
    # mod_api.register_quality(QualityTier(
    #     rank=3, price_modifier=12.0,
    #     prefixes={"dress": "Gilded", "misc": "Gilded"},
    # ))

    # The item_generated hook fires for every item cooked from a template
    # (context: item / template / tier) — see api.HOOK_ITEM_GENERATED.
    def on_item_generated(context):
        # context = {"item": new Item, "template": template Item, "tier": QualityTier}
        pass

    api.register_hook(api.HOOK_ITEM_GENERATED, on_item_generated)


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
