#### Screen Girl List — Girl roster and selection screens ####
# Phase 3.1: Extracted from ui/screens.rpy.
# Contains: screen girls, girl_tab, girl_pick_badge, badge_button,
#           girl_button, girl_fast_actions
#
# These are the most-reused screens in the game — every girl list
# (brothel, slavemarket, farm, free girls) uses them.

screen girls(girls, context = "girls"): # context can be girls, slavemarket, farm

    tag girls

    default hovered_girl = selected_girl

    # $ renpy.maximum_framerate(86400) #! Uncomment for stable FPS measurements

    if not girls_firstvisit:
        key "mouseup_3" action (SetVariable("choice_menu_girl_interact", False), SetVariable("selected_destination", "main"), Jump("teleport"))
        use close((SetVariable("choice_menu_girl_interact", False), SetVariable("selected_destination", "main"), Jump("teleport")))
        use shortcuts()

    use girl_tab(girls, context=context)

    if persistent.hover_for_preview_girls and hovered_girl and hovered_girl in girls:
        use girl_stats(hovered_girl, context=context)
        use button_overlay(hovered_girl, context=context)
        use girl_profile(hovered_girl, context=context)

    elif selected_girl and selected_girl in girls:
        use girl_stats(selected_girl, context=context)
        use button_overlay(selected_girl, context=context)
        use girl_profile(selected_girl, context=context)
