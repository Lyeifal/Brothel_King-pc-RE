# BK Evolution — i18n Best Practices

> Last updated: 2026-09-11 (verified against code)
>
> This document defines the internationalization (i18n) conventions for the BK Evolution project, ensuring all player-visible text is correctly collected by the Ren'Py translation system.
>
> Scope: all `.rpy` scripts under `game/core/` and all JSON data files under `game/core/data/`.

---

## Core principles

1. **All player-visible strings must be explicitly marked as translatable**
2. **Do not concatenate player-visible sentences with Python `+`**
3. **Data-driven text must live in JSON, using the `_i18n` suffix**
4. **Translation files are distributed following the source file directory structure, per the Ren'Py standard**

---

## 1. Ren'Py script layer conventions

### 1.1 String wrapping

All strings shown to players must use `__()` (use `_()` in Screen Language):

```renpy
# ✅ Correct
renpy.call_screen("yes_no", __("Do you really want to buy this item?"))
renpy.say(npc, __("Hello, Master!"))
renpy.notify(__("Saved successfully."))

# ❌ Wrong
renpy.call_screen("yes_no", "Do you really want to buy this item?")
renpy.say(npc, "Hello, Master!")
renpy.notify("Saved successfully.")
```

### 1.2 Screen Language

`text`, `button`, `label`, etc. in screens must be wrapped with `_()`:

```renpy
# ✅ Correct
text _("Choose an option")
button _("Cancel") action Return()
label _("Settings") style "preferences_label"

# ❌ Wrong
text "Choose an option"
button "Cancel" action Return()
label "Settings" style "preferences_label"
```

Exceptions (no translation needed):
- Pure icon/image tags: `{image=...}`
- Single-character symbols: `"-"`, `"+"`, `">"`
- Pure numbers or the formatting placeholders themselves

### 1.3 menu: options

Literal options in Ren'Py's native `menu:` are extracted automatically. If an option comes from a variable, it needs `__()` wrapping:

```renpy
# ✅ Correct: literals are extracted automatically
menu:
    "Train her gently":
        ...
    "Punish her":
        ...

# ✅ Correct: variable wrapped
$ caption = __("Train her gently")
menu:
    "[caption]":
        ...

# ❌ Wrong: variable not wrapped
$ caption = "Train her gently"
menu:
    "[caption]":
        ...
```

### 1.4 String concatenation is forbidden

Concatenating player-visible text with `+` is forbidden. Use a complete template + placeholders instead:

```renpy
# ❌ Wrong
"Are you sure you want to take a loan for " + str(r.amount) + " gold?"

# ✅ Correct: % placeholders
__("Are you sure you want to take a loan for %s gold?") % r.amount

# ✅ Correct: format placeholders
__("Are you sure you want to take a loan for {amount} gold?").format(amount=r.amount)

# ✅ Correct: Ren'Py interpolation (recommended when the variable is available in Ren'Py context)
__("Are you sure you want to take a loan for [r.amount] gold?")
```

### 1.5 Wrapping formatted strings

All player-visible `%` formatted strings must be wrapped with `__()`:

```renpy
# ❌ Wrong
"You gained %s gold." % amount

# ✅ Correct
__("You gained %s gold.") % amount
```

### 1.6 Dynamic text interpolation

Prefer Ren'Py's built-in `[variable]` interpolation:

```renpy
# ✅ Recommended
__("Hello, [girl.name]!")

# ✅ Also fine
__("Hello, %s!") % girl.name
```

---

## 2. JSON data layer conventions

### 2.1 The `_i18n` suffix convention

All translatable text fields must end with `_i18n`:

```json
{
  "id": "pirate_captain",
  "name_i18n": "Pirate Captain",
  "description_i18n": "A feared captain of the high seas.",
  "icon_tag": "origin_pirate",
  "price": 100
}
```

| Field type | Example | Needs `_i18n`? |
|----------|------|------------------|
| Display name | `name_i18n` | ✅ Yes |
| Description | `description_i18n` | ✅ Yes |
| Internal ID/code key | `id`, `key`, `tag` | ❌ No |
| Picture/audio path | `pic`, `icon`, `sound` | ❌ No |
| Numeric | `price`, `rank`, `cost` | ❌ No |
| Effect/condition expression | `effects`, `requirements` | ❌ No |

### 2.2 Dictionary value collections

If a parent field itself ends with `_i18n`, its dictionary values are also treated as translatable:

```json
{
  "help_dict_i18n": {
    "intro": "Welcome to the help system.",
    "combat": "Combat is turn-based."
  }
}
```

`json_i18n.rpy` automatically collects all string values under `help_dict_i18n`.

### 2.3 Usage in code

Use `get_i18n()` or `I18nMixin` to read and translate from JSON:

```renpy
init python:
    # Method A: get_i18n()
    name = get_i18n(item, "name")
    description = get_i18n(item, "description")

    # Method B: I18nMixin
    class MyEntity(I18nMixin):
        @classmethod
        def from_dict(cls, data):
            d = cls._resolve_i18n(data)
            return cls(name=d["name"], description=d.get("description"))
```

---

## 3. Randomly generated text conventions

### 3.1 Template pools in JSON

Random girl dialogue, gossip, background generation pools, etc. should be placed in JSON files under `game/core/data/settings/` (loaded by the corresponding `DataLoader` `load_*()` methods):

```json
{
  "greeting_i18n": {
    "friendly": [
      "Good morning, Master!",
      "I hope you're having a good day."
    ],
    "shy": [
      "H-hello...",
      "Um, good morning..."
    ]
  }
}
```

Existing instances (verified against code on 2026-09-11):

| JSON file | Loading method (`game/core/systems/data_loader.rpy`) | Content |
|-----------|------------------------------------------|------|
| `settings/gossip.json` | `load_gossip()` | City gossip text library |
| `settings/dialogue_texts.json` | `load_dialogue_texts()` | Jokes/compliments and other social dialogue text |
| `settings/girl_background_pools.json` | `load_girl_background_pools()` | Girl background generation random pools (stories/family/guardian/hobbies, etc.) |
| `settings/farm/…` (`farm/farm_perform_dict.json`) | `load_farm_perform_dict()` | Farm performance text |

### 3.2 Runtime population

Code randomly selects from the template pool and populates placeholders at runtime:

```renpy
init python:
    def get_girl_line(pool_name, personality, **kwargs):
        templates = girl_background_pools.get(pool_name, {}).get(personality, [])
        if templates:
            tmpl = random.choice(templates)
            return __(tmpl) % kwargs
        return ""
```

Do not assemble random descriptions word-by-word in code.

---

## 4. Translation file directory structure

Ren'Py `translate --empty` generates `translate chinese_simplified strings:` blocks based on the source file locations. Keep this distribution:

```
game/tl/chinese_simplified/
├── core/content/         # Story, event, and interaction translations
│   ├── main_story/
│   ├── city_events/
│   ├── day_events/
│   └── interactions.rpy
├── core/ui/              # UI translations
│   ├── screens.rpy
│   └── main.rpy
├── core/systems/         # System message translations
│   └── help.rpy
└── strings.rpy           # Generic string translations
```

Do not force all strings back into `strings.rpy`.

---

## 5. Verification workflow

The following must be run before every commit:

```powershell
# 1. i18n audit
python tools/i18n_lint.py

# 2. Regression test
python tools/verify_i18n.py

# 3. Ren'Py lint
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint
```

All checks must pass.

---

## 6. Common anti-patterns and fixes

| Anti-pattern | Problem | Fix |
|--------|------|------|
| `call_screen("yes_no", "...")` | Confirmation dialog in English | `call_screen("yes_no", __("..."))` |
| `"Hello " + name` | Grammar untranslatable | `__("Hello %s") % name` |
| `"%s gold" % amount` | Template not entering the translation system | `__("%s gold") % amount` |
| `text "Settings"` | UI in English | `text _("Settings")` |
| Hardcoded girl descriptions | Can't be translated as data | Migrate to JSON template pools under `data/settings/` (see §3.1) |
| JSON field `name` used as both display and key | Persistence/lookup breaks after switching language | Use `id` as the key and `name_i18n` for display |

---

## 7. Exceptions

The following may stay in English / untranslated:

1. **Debug information**: only shown in developer mode
2. **Picture/audio paths**: e.g. `resources/pics/foo.webp`
3. **Code keys/identifiers**: e.g. `trait_id`, `effect_name`
4. **Ren'Py internal tags**: e.g. `{image=...}`, `{color=...}`
5. **Pure numbers, single-character symbols**

---

## Related files

- [`game/core/i18n/json_i18n.rpy`](../../game/core/i18n/json_i18n.rpy) — JSON i18n registration
- [`game/core/systems/data_loader.rpy`](../../game/core/systems/data_loader.rpy) — JSON data loading
- [`tools/i18n_lint.py`](../../tools/i18n_lint.py) — i18n audit
- [`tools/verify_i18n.py`](../../tools/verify_i18n.py) — i18n regression test
- [`tools/audit_placeholders.py`](../../tools/audit_placeholders.py) — placeholder consistency audit
- [`I18N_ROADMAP.md`](I18N_ROADMAP.md) — current i18n status and roadmap
- [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md) — Chinese translation completion log (history + current baseline)
