#### TRANSLATION FRAMEWORK #############################################
##  i18n initialization and language switching for Brothel King      ##
##  This file sets up the translation directories and UI controls    ##
########################################################################

init -10 python:

    # List of supported languages with display names
    # Key must match the directory name under game/tl/
    bk_language_map = {
        None:       "English",      # Default (no translation)
        "chinese":  "中文",
        "chinese_simplified": "简体中文",
    }

    # Reverse lookup for preference display
    bk_language_list = list(bk_language_map.items())

    # Persistent language preference (falls back to None = English)
    if persistent._bk_language is None:
        persistent._bk_language = None

    def bk_set_language(lang):
        """
        Switch the game language.
        lang should be a key from bk_language_map (e.g. None, "chinese").
        """
        persistent._bk_language = lang
        renpy.change_language(lang)
        # Force a reload of styles that might depend on language
        renpy.restart_interaction()

    # Apply saved language on startup
    def bk_apply_language():
        if persistent._bk_language is not None:
            try:
                renpy.change_language(persistent._bk_language)
            except Exception as e:
                # If language files are missing, fall back to default
                persistent._bk_language = None
                renpy.change_language(None)

# Apply language when the game starts
label before_main_menu:
    $ bk_apply_language()
    return
