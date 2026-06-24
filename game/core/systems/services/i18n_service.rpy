#### I18nService — Centralized internationalization service ####
# Phase 4.1: Wraps Ren'Py's __() with proper plural forms, context-aware
# translation, gender support, and locale-aware formatting.
#
# Registers with GameServices as "i18n".
# Access via: i18n = services.i18n

init -10 python:

    class I18nService(object):
        """Centralized translation and locale service.

        Wraps Ren'Py's built-in __() with additional capabilities:
        - Plural forms (CLDR-compatible)
        - Context-aware translation (pgettext)
        - Gender-aware pronoun resolution
        - Locale-aware possessive and article formatting
        """

        def __init__(self):
            self._pronoun_tables = {
                None: {  # English
                    "M": {"subjective": "he", "objective": "him", "possessive": "his", "possessive_adj": "his", "reflexive": "himself"},
                    "F": {"subjective": "she", "objective": "her", "possessive": "hers", "possessive_adj": "her", "reflexive": "herself"},
                    "N": {"subjective": "they", "objective": "them", "possessive": "theirs", "possessive_adj": "their", "reflexive": "themself"},
                },
                "chinese_simplified": {  # Chinese uses same pronoun for all genders
                    "M": {"subjective": "他", "objective": "他", "possessive": "他的", "possessive_adj": "他的", "reflexive": "他自己"},
                    "F": {"subjective": "她", "objective": "她", "possessive": "她的", "possessive_adj": "她的", "reflexive": "她自己"},
                    "N": {"subjective": "TA", "objective": "TA", "possessive": "TA的", "possessive_adj": "TA的", "reflexive": "TA自己"},
                },
            }

        # ── Core translation ──

        @staticmethod
        def t(text):
            """Translate a string. Thin wrapper around Ren'Py's __()."""
            return __(text)

        @staticmethod
        def tn(n, singular, plural=None):
            """Translate with plural form.

            English: tn(1, "file", "files") → "file", tn(3, "file", "files") → "files"
            Chinese: tn(n, "file", "files") → "file" (always singular)

            Falls back to pluralize() from utils.rpy.
            """
            return pluralize(n, singular, plural)

        @staticmethod
        def tc(text, context):
            """Context-aware translation (pgettext).

            Uses Ren'Py's __("contexttext") syntax.
            The context disambiguates identical source strings.
            """
            return __("%s%s" % (context, text))

        @staticmethod
        def format(template, **kwargs):
            """Translate a template string then format with kwargs.

            Example: i18n.format("Hello {name}", name="World")
            """
            return __(template).format(**kwargs)

        # ── Possessive ──

        @staticmethod
        def possessive(name):
            """Return the possessive form of a name for the current locale.

            English: possessive("Alice") → "Alice's"
            Chinese: possessive("Alice") → "Alice的"
            """
            if not _is_english_locale():
                return name + __("'s")  # CJK: "'s" translates to "的" or similar
            if name.endswith("s"):
                return name + "'"
            return name + "'s"

        # ── Pronoun ──

        def pronoun(self, gender, form="subjective"):
            """Get a locale-aware pronoun.

            Args:
                gender: "M", "F", or "N" (neutral)
                form: "subjective", "objective", "possessive", "possessive_adj", "reflexive"

            Returns the pronoun string for the current language.
            """
            lang = getattr(renpy.game.preferences, 'language', None)
            table = self._pronoun_tables.get(lang, self._pronoun_tables[None])
            gender_table = table.get(gender, table.get("N", {}))
            return gender_table.get(form, gender)

        # ── Locale info ──

        @staticmethod
        def is_english():
            """True when the active locale is English."""
            return _is_english_locale()

        @staticmethod
        def current_language():
            """Return the current language code (None = English)."""
            return getattr(renpy.game.preferences, 'language', None)

        @staticmethod
        def current_language_name():
            """Return the display name of the current language."""
            lang = getattr(renpy.game.preferences, 'language', None)
            return bk_language_map.get(lang, "English")


    # ── Singleton registration ──
    i18n_service = I18nService()
    services.register("i18n", i18n_service)
