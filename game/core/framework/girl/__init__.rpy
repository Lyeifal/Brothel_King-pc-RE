#### Girl Components Package — Phase 2.1 ####
# The 5,900-line Girl class is decomposed into focused components.
# Each component holds a reference to the Girl instance for cross-component access.
#
# Components (+ = delegation wrappers implemented, - = stub only):
#   girl_base          — Identity: name, rank, level, serialization
#   girl_stats         — Stats, stat caps, stat changes, spillover
#   girl_traits        — Trait/perk management
#   girl_items         — Equipment, items, inventory
#  +girl_schedule      — Job assignment, workdays, schedule (12 methods)
#   girl_sex           — Sex acts, fixations, preferences
#  +girl_mood          — Mood, sanity, energy, health (25 methods)
#   girl_relationships  — Love, fear, obedience, MC relations
#   girl_training      — Training, farm acts, obedience checks
#  +girl_economy       — Prices, upkeep, tips, performance (22 methods)
#   girl_dialogue      — Dialogue selection, say(), personality
#  +girl_pictures      — Image selection, refresh, evaluation (full impl)
#   girl_effects       — Effect wrappers (delegates to EffectBearer)
#   girl_generation    — Randomization, personality, BG, preferences
#   girl_logging       — Logging, tracking, recent events
#
# Total: 10 components, 4 with full delegation (pictures/economy/mood/schedule)
#        59 _impl aliases in Girl class
#        All existing 2,000+ call sites unchanged.
