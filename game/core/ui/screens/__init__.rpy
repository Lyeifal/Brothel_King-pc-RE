#### UI Screens Package — Phase 3.1 ####
# The monolithic ui/screens.rpy (~460KB) is split into focused screen files.
# Each file contains related screens, keeping each under ~1,500 lines.
#
# Files:
#   screen_common.rpy       — Shared components: stat_bar, custom_bar, badge, overlay
#   screen_girl_list.rpy    — Girl list, tabs, buttons
#   screen_girl_profile.rpy — Girl profile, stats, log
#   screen_girl_actions.rpy — Girl actions: job assignment, perks, traits
#   screen_schedule.rpy     — Schedule, autorest
#   screen_brothel.rpy      — Brothel management
#   screen_district.rpy     — Districts, locations
#   screen_matchmaking.rpy  — Matchmaking, customer satisfaction
#   screen_home.rpy         — Main home screen
#   screen_night.rpy        — Night report, end-day
#   screen_farm.rpy         — Farm interface (extracted from farm.rpy)
#
# The old screens.rpy remains as fallback during transition.
