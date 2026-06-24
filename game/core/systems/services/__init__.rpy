#### Services Package — Centralized dependency management ####
# Phase 1: GameServices container replaces global singleton proliferation.
#
# Import order within this package:
#   1. service_container.rpy  — GameServices class + singleton
#   2. interfaces/             — Abstract service interfaces (Phase 1.2)
#
# External modules import `services` directly from the container.
# The singleton is created at init -12 (before all other game code).
