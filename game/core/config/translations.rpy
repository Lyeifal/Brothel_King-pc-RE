#### TRANSLATION FRAMEWORK #############################################
##  i18n initialization and language switching for Brothel King      ##
########################################################################

init -10 python:

    # Phase 4.6: Language map with JSON override support.
    # Adding a new language requires:
    #   1. Create game/tl/<lang_code>/ directory with translation files
    #   2. Add entry to custom/config/languages.json (optional)
    #   3. Or: add entry to the hardcoded fallback below
    _fallback_languages = {
        None:       "English",
        "chinese_simplified": "简体中文",
    }

    # Try loading language list from JSON (mod/community extensible)
    _loaded_languages = {}
    try:
        import json, os
        _lang_config = os.path.join(renpy.config.gamedir, "custom", "config", "languages.json")
        if os.path.exists(_lang_config):
            with open(_lang_config, "r", encoding="utf-8") as f:
                _json_langs = json.load(f)
                # JSON keys are strings; None is represented as "null" → convert back
                for k, v in _json_langs.items():
                    key = None if k == "null" or k is None else k
                    _loaded_languages[key] = v
    except Exception:
        pass

    # Merge: JSON overrides take precedence, fallback fills gaps
    bk_language_map = {}
    bk_language_map.update(_fallback_languages)
    bk_language_map.update(_loaded_languages)

    bk_language_list = list(bk_language_map.items())

    if persistent._bk_language is None:
        persistent._bk_language = None

    def bk_update_font_replacement():
        """Replace decorative Western fonts with CJK font when playing in Chinese to avoid tofu/boxes."""
        cjk_font = "resources/fonts/NotoSansCJKsc-Regular.otf"
        western_fonts = [
            "resources/fonts/MATURASC.ttf",
            "resources/fonts/VIVALDII.TTF",
            "resources/fonts/SFBurlingtonScript.ttf",
        ]
        if persistent._bk_language == "chinese_simplified":
            for wf in western_fonts:
                config.font_replacement_map[(wf, False, False)] = (cjk_font, False, False)
        else:
            for wf in western_fonts:
                config.font_replacement_map.pop((wf, False, False), None)

    def bk_set_language(lang):
        persistent._bk_language = lang
        bk_update_font_replacement()
        renpy.change_language(lang)
        renpy.restart_interaction()

    def bk_apply_language():
        if persistent._bk_language is not None:
            try:
                bk_update_font_replacement()
                renpy.change_language(persistent._bk_language)
            except Exception as e:
                persistent._bk_language = None
                renpy.change_language(None)

# Language is applied in BKevents.rpy::before_main_menu to avoid duplicate label

    # Apply font replacement immediately in case the game was started with a non-default language
    bk_update_font_replacement()
