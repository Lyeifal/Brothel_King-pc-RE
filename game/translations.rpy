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

    def bk_set_language(lang):
        persistent._bk_language = lang
        renpy.change_language(lang)
        renpy.restart_interaction()

    def bk_apply_language():
        if persistent._bk_language is not None:
            try:
                renpy.change_language(persistent._bk_language)
            except Exception as e:
                persistent._bk_language = None
                renpy.change_language(None)

# Language is applied in BKevents.rpy::before_main_menu to avoid duplicate label
