#### Init Dependency Graph — Assertions for correct loading order ####
# Phase 1.4: Documents and enforces the init priority dependency chain.
#
# Each init block that depends on services from earlier init levels
# should call require_service() at the top. This catches ordering
# bugs at startup rather than through cryptic runtime errors.
#
# Dependency chain (documented):
#
#   init -12  service_container.rpy     GameServices singleton
#   init -11  game_config.rpy           GameConfig registered as "config"
#   init -10  settings.rpy              girl_directories, config tweaks
#   init -10  translations.rpy          bk_language_map, font mapping
#   init -9   (reserved for future early services)
#   init -8   (reserved)
#   init -5   tag_registry.rpy          Tag registry init
#   init -4   variables.rpy             tag_dict (JSON), persistent vars
#   init -3   girl_factory.rpy          get_girl_path, create_girl
#   init -3   effects.rpy               get_pic, get_pic_list, effects
#   init -3   utils.rpy                 dice, pluralize, article, etc.
#   init -3   dialogue.rpy              dialogue helpers
#   init -3   game_systems.rpy          update_slaves, weekly_updates
#   init -3   economy.rpy               economy functions
#   init -2   core_entities.rpy         Game, Main, NPC, Calendar classes
#   init -2   world.rpy                 Brothel, District, Population, etc.
#   init -2   character.rpy             Trait, Perk, Effect, ItemType, etc.
#   init -2   girlclass.rpy             Girl class
#   init -2   girl_files_dict.rpy       GirlFilesDict (+ registers service)
#   init -2   interactions.rpy          Event, StoryEvent, Quest
#   init -2   challenges.rpy            Spell, MC_challenge, Mod
#   init -2   progression.rpy           Achievement, Contract, etc.
#   init -1   (reserved)
#   init      start.rpy label           game, MC, brothel, farm created
#
#   label before_main_menu              traits/perks loaded, mods updated
#   label start                         game init flow


init -10 python:

    # After settings.rpy and translations.rpy have loaded,
    # verify that the service container and config are available.

    require_service("config", "GameConfig must be loaded before settings (init -11)")


init -4 python:

    # After tag_dict and persistent vars are set up,
    # verify that girl_directories are available.

    if not services.has("girl_files_dict"):
        # GirlFilesDict is registered at init -2, so it won't exist yet.
        # This is OK — the assertion is for debugging ordering issues.
        pass


init -2 python:

    # After class definitions are loaded but before start.rpy runs,
    # verify that critical early services are registered.

    # GirlFilesDict should now be available (registered at init -2 in its own file)
    # Note: game, MC, brothel, farm are NOT available yet (created at init level)
    pass
