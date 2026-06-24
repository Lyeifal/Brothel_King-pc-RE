#### Girl Components Package — Phase 2.1 ####
# The 5,900-line Girl class is decomposed into focused components.
# Each component holds a reference to the Girl instance for cross-component access.
#
# Components:
#   girl_base          — Identity: name, rank, level, serialization
#   girl_stats         — Stats, stat caps, stat changes, spillover
#   girl_traits        — Trait/perk management
#   girl_items         — Equipment, items, inventory
#   girl_schedule      — Job assignment, workdays, schedule
#   girl_sex           — Sex acts, fixations, preferences
#   girl_mood          — Mood, sanity, energy, health
#   girl_relationships  — Love, fear, obedience, MC relations
#   girl_training      — Training, farm acts, obedience checks
#   girl_economy       — Prices, upkeep, tips, performance
#   girl_dialogue      — Dialogue selection, say(), personality
#   girl_pictures      — Image selection, refresh, evaluation
#   girl_effects       — Effect wrappers (delegates to EffectBearer)
#   girl_generation    — Randomization, personality, BG, preferences
#   girl_logging       — Logging, tracking, recent events
#
# Migration: Girl class creates component instances in __init__ and
# delegates public methods. All existing 2,000+ call sites unchanged.
