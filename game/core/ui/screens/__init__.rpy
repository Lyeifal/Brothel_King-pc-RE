#### UI Screens Package — Phase 3.1 / Phase 2 ####
# The monolithic ui/screens.rpy (~460KB) has been split into focused screen
# files. Each file contains related screens, keeping each under ~1,500 lines.
#
# Files:
#   screen_common.rpy       — Shared components: tool, overlay, quick_start, popups, shortcuts
#   screen_girl_list.rpy    — Girl list (pre-existing)
#   screen_girl_profile.rpy — Girl profile (Phase 3.1)
#   screen_brothel.rpy      — Brothel management (Phase 3.1)
#   screen_girl_stats.rpy   — Stat bars, girl stats, trait/perk details
#   screen_girl_log.rpy     — Girl log, previous night log
#   screen_progress.rpy     — Level, perks, autorest
#   screen_farm.rpy         — Farm menus, minions, shows
#   screen_districts.rpy    — Districts, locations, matchmaking
#   screen_schedule.rpy     — Schedule, save/load schedule
#   screen_home.rpy         — Home screen, brothel report
#   screen_misc.rpy         — Top overlay, girl list widgets
#   screen_misc2.rpy        — Main character, hints, girl detail panels
#   screen_quest.rpy        — Postings, spellbook, challenges, interactions, mods
#   screen_powers.rpy       — Evil powers, cards, brothel ranking
#   screen_resources.rpy    — Resources, achievements, contracts
#
# ui/screens.rpy now only holds image/style declarations, section headers
# and EXTRACTED placeholder comments; all screen definitions live here.
