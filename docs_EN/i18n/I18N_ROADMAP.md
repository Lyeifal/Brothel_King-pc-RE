# BK Evolution — Internationalization (i18n) Roadmap

> Last updated: 2026-09-11 (verified against code)
>
> This document is the **sole active reference** for i18n work. It consolidates the content of the former `I18N_PLAN.md` and `I18N_REFACTOR_PLAN.md`, and reflects the actual current state of the code.
>
> Historical versions: [`../../docs/archive/I18N_PLAN.md`](../../docs/archive/I18N_PLAN.md), [`../../docs/archive/I18N_REFACTOR_PLAN.md`](../../docs/archive/I18N_REFACTOR_PLAN.md)

---

## 1. Current status

| Metric | Status |
|------|------|
| JSON `_i18n` migration | ✅ Fully complete (measured in startup log: 105 JSON files, 1,540 translatable strings registered) |
| `json_i18n.rpy` whitelist mode | ✅ Removed; only `_i18n` suffix recognition remains |
| Wrapping bare strings in code | ✅ Main UI/menus/narration/interaction options wrapped with `__()` / `_()` |
| Chinese translation coverage | ✅ Dialogue and strings/UI near 100%; remaining gaps are content backlog (see below) |
| Current missing baseline (2026-09-11, measured with `translate --count chinese_simplified`) | 📝 1,433 dialogue + 124 string entries missing, all content backlog rather than code defects |
| i18n audit tools | ✅ `tools/i18n_lint.py`, `tools/verify_i18n.py` exist; i18n_lint baseline of 17 false positives on developer-facing text |

---

## 2. Core conventions

### 2.1 JSON fields: `name` vs `name_i18n`

```json
{
  "id": "pirate_captain",
  "name": "pirate_captain",
  "name_i18n": "Pirate Captain",
  "description_i18n": "A feared captain of the high seas."
}
```

- **Code keys**: fields such as `name`, `id`, `type`, `tag` stay in English/identifier form for logic lookups.
- **Translatable text**: field names end with `_i18n` and are automatically registered into the Ren'Py translation system via `game/core/i18n/json_i18n.rpy`.
- **Picture/audio paths**: keep original field names (e.g. `pic`, `sound`); **do not** add `_i18n`.
- **Numeric/boolean/code fields**: keep original field names; do not add `_i18n`.

### 2.2 Using `__()` / `_()` in code

```renpy
# In Python code
text = __("You have %s gold.") % gold

# In Screen Language
text _("Welcome to Brothel King")
```

- Player-visible strings must be wrapped with `__()` (Python) or `_()` (Screen).
- Internal identifiers, debug logs, and file paths must not be wrapped.

### 2.3 Translation at load time

```python
from core.i18n import get_i18n

class MyEntity:
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=get_i18n(data, "name"),        # Prefers name_i18n, falls back to name
            description=get_i18n(data, "description", ""),
        )
```

`get_i18n(data, key)` automatically handles the `key_i18n` → `key` fallback and returns the translation in the current language.

---

## 3. Completed work

### 3.1 JSON `_i18n` migration (Phase 1-4)

All JSON containing translatable text has been adapted to the `_i18n` suffix. Main categories:

- **Core systems**: difficulty, origins, shops, powers, spells, personalities, achievements, contracts, customer_affixes, meta, ngp, chapter_titles, mc_classes
- **Content data**: traits, perks, fixations, items, contracts, rooms, story_events
- **Interactions and events**: interact_dict, free_interact_dict, default_world
- **Farm and performance**: farm_descriptions, farm_perform_dict, farm_holding_params
- **Text dictionaries**: cleanliness_penalties, dialogue_texts, event_texts, gossip, help_texts, loading_tips, mc_descriptions, merchants, recent_events, sex_act_descriptions, sex_descriptions, small_texts, etc.

> The complete file list is in [`../../docs/archive/I18N_PLAN.md`](../../docs/archive/I18N_PLAN.md).

### 3.2 Code wrapping (formerly I18N_REFACTOR_PLAN Phase 1-3)

- Bare strings in `renpy.say` / `renpy.notify` have been wrapped with `__()`.
- Prompts in screen calls such as `call_screen("yes_no", ...)` have been wrapped with `__()`.
- Menu options, category titles, and tab labels in Screen Language have been wrapped with `_()` / `__()`.
- Concatenated strings have been refactored into complete sentences before wrapping with `__()`.

### 3.3 Toolchain (formerly I18N_REFACTOR_PLAN Phase 4-6)

| Tool | Path | Purpose |
|------|------|------|
| `i18n_lint.py` | `tools/i18n_lint.py` | Scans for i18n issues: bare strings, concatenated text, unwrapped formatting, etc. |
| `verify_i18n.py` | `tools/verify_i18n.py` | Runs `translate --count` + `lint` + `i18n_lint.py`, asserting no missing translations (current baseline: 1,433 dialogue + 124 string missing, content backlog rather than code defects) |
| `audit_placeholders.py` | `tools/audit_placeholders.py` | Checks placeholder consistency between Chinese translations and the original text |
| `export_empty_to_xlsx.py` | `tools/export_empty_to_xlsx.py` | Exports empty translations to `temp/translations/to_translate_empty.xlsx` |
| `import_translated_empty.py` | `tools/import_translated_empty.py` | Imports translations back from Excel |

---

## 4. Standard translation workflow

```powershell
# 1. Extract empty translations
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --empty chinese_simplified

# 2. Export to Excel
python tools/export_empty_to_xlsx.py

# 3. Manually/machine-translate temp/translations/to_translate_empty.xlsx

# 4. Import back
python tools/import_translated_empty.py

# 5. Placeholder and tag audit
python tools/audit_placeholders.py

# 6. Run i18n audit and verification
python tools/i18n_lint.py
python tools/verify_i18n.py

# 7. Final lint
game\Brothel_King.py . lint
```

Detailed statistics and history are in [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md).

---

## 5. Coding best practices

See [`BEST_PRACTICES.md`](BEST_PRACTICES.md). Key points:

1. Player-visible strings must use `__()` / `_()`.
2. Chinese translations must keep all `%s`/`%d`/`[var]` placeholders.
3. Avoid string concatenation; compose complete sentences first, then translate.
4. JSON translatable fields use the `_i18n` suffix.
5. Don't translate internal keys, picture paths, or sound paths.
6. After adding new strings, run `translate --empty` and export/translate/import.

---

## 6. Legacy items and pending optimizations

| Item | Status | Description |
|----|------|------|
| Machine translation quality review | 🚧 Ongoing | ~3,500 dialogue blocks and ~9,000 strings migrated early are machine translations; spot checks at runtime needed |
| Review of core story text | 🚧 Ongoing | chapter1-3 and story_events are recommended for manual polishing |
| Mod content translation | ⏳ To be planned | `game/custom/` content stays in its original language by default; may be supported in the future via a unified string table |
| `tools/translate_sync.py` | ✅ Not implemented (decision on 2026-06-25) | The need to "sync strings.rpy with tl file old/new" is already covered by the existing toolchain: missing detection = `verify_i18n.py` (`translate --count`); placeholder integrity = `audit_placeholders.py`; empty-translation export/import round trip = `export_empty_to_xlsx.py` / `import_translated_empty.py`; stale entries are cleaned when the Ren'Py `translate` command rewrites tl files. No need to reinvent the wheel. |
| i18n_lint developer-facing false positives | 📝 Recorded | `i18n_lint.py` currently reports 17 issues, all in developer-facing text (dev console output, test runner assertion messages, exception messages) — not player-visible strings, so not wrapped with `__()` for now; if needed later, a path whitelist can be added to the tool. |

---

## 7. Related files

| File | Description |
|------|------|
| [`BEST_PRACTICES.md`](BEST_PRACTICES.md) | Coding and translation best practices |
| [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md) | Chinese translation completion log (concluded; historical records + current baseline) |
| [`game/core/i18n/json_i18n.rpy`](../../game/core/i18n/json_i18n.rpy) | JSON i18n registration implementation |
| [`tools/i18n_lint.py`](../../tools/i18n_lint.py) | i18n static audit |
| [`tools/verify_i18n.py`](../../tools/verify_i18n.py) | i18n regression verification |
