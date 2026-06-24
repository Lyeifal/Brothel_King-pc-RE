#### ViewModel Package — Phase 3.2 ####
# ViewModels decouple UI rendering from game state.
# Screens read from ViewModels rather than directly touching game objects.
#
# Planned:
#   girl_view_model.rpy     — Girl data formatted for UI display
#   brothel_view_model.rpy  — Brothel state formatted for UI
#   economy_view_model.rpy  — Economy data formatted for UI
#
# Benefits:
#   - I18N formatting happens in ViewModels (not in screens)
#   - Screens become pure presentation (easier to split and test)
#   - Game state changes don't break UI if ViewModel API is stable
