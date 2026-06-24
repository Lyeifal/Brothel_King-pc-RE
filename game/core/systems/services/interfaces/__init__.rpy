#### Service Interfaces Package ####
# Phase 1.2: Abstract contracts for each game domain service.
# These define what each service must provide without dictating
# implementation details.
#
# Currently defined:
#   i_event_service  — Event registration, dispatch, lifecycle
#   i_girl_service   — Girl creation, serialization, collection mgmt
#   i_mod_service    — Mod registration, activation, hooks
#
# Future (Phase 2-5):
#   i_economy_service — Economy calculations, customer matching
#   i_brothel_service — Brothel state, upgrades, rooms
#   i_i18n_service    — Translation, plurals, gender, formatting
