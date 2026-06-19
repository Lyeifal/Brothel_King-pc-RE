#### TRANSLATION FRAMEWORK #############################################
##  i18n initialization and language switching for Brothel King      ##
########################################################################

init -10 python:

    bk_language_map = {
        None:       "English",
        "chinese":  "中文",
        "chinese_simplified": "简体中文",
    }

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
        if persistent._bk_language in ("chinese", "chinese_simplified"):
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
