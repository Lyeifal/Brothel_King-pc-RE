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
        
        # Auto-switch fonts for CJK languages if CJK fonts are configured
        if lang in ("chinese", "chinese_simplified"):
            try:
                if hasattr(gui, 'text_font_cjk'):
                    gui.text_font = gui.text_font_cjk
                if hasattr(gui, 'name_text_font_cjk'):
                    gui.name_text_font = gui.name_text_font_cjk
                if hasattr(gui, 'interface_text_font_cjk'):
                    gui.interface_text_font = gui.interface_text_font_cjk
            except:
                pass
        else:
            # Restore default fonts
            gui.text_font = "Lato-Regular.TTF"
            gui.name_text_font = "Lato-Regular.TTF"
            gui.interface_text_font = "Lato-Regular.TTF"
        
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

# Language is applied in BKevents.rpy::before_main_menu to avoid duplicate label
