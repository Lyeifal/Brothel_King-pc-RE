#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Audit JSON _i18n strings for missing translations.

Scans game/core/data/**/*.json using the same rules as json_i18n.rpy,
then checks game/tl/<language>/strings.rpy for existing translations.
Outputs an Excel file with all missing JSON i18n strings.
"""
from __future__ import print_function
import json
import os
import re
import sys
from collections import OrderedDict
from pathlib import Path

try:
    import openpyxl
except ImportError:
    openpyxl = None

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "game" / "core" / "data"
TL_DIR = ROOT / "game" / "tl"

SKIP_EXTS = (
    ".webp", ".png", ".jpg", ".jpeg",
    ".ogg", ".wav", ".mp3", ".mp4", ".webm",
)
SKIP_PREFIXES = (
    "Effect(", "BK_", "img_", "IT_",
)


def is_i18n_value(value):
    if not isinstance(value, str) or not value.strip():
        return False
    v = value.strip()
    if len(v) <= 1:
        return False
    if any(v.lower().endswith(ext) for ext in SKIP_EXTS):
        return False
    if v.startswith("#") and len(v) in (4, 7, 9):
        hex_body = v[1:]
        if all(c in "0123456789ABCDEFabcdef" for c in hex_body):
            return False
    try:
        float(v)
        return False
    except ValueError:
        pass
    if v.startswith(SKIP_PREFIXES):
        return False
    if v.startswith(("{image=", "{sound=", "{movie=")):
        return False
    return True


def scan_i18n_strings(obj, collected, parent_key=None):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(key, str) and key.endswith("_i18n") and is_i18n_value(value):
                collected.add(value)
            elif parent_key and parent_key.endswith("_i18n") and is_i18n_value(value):
                collected.add(value)
            scan_i18n_strings(value, collected, key)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, str) and parent_key and parent_key.endswith("_i18n") and is_i18n_value(item):
                collected.add(item)
            scan_i18n_strings(item, collected, parent_key)


def load_existing_translations(language):
    strings_file = TL_DIR / language / "strings.rpy"
    translations = {}  # old -> new
    if not strings_file.exists():
        return translations
    text = strings_file.read_text(encoding="utf-8")
    pattern = re.compile(
        r'^\s*old\s+"((?:[^"\\]|\\.)*)"\s*\n\s*new\s+"((?:[^"\\]|\\.)*)"',
        re.MULTILINE,
    )
    for old, new in pattern.findall(text):
        translations[old] = new
    return translations


def main():
    language = sys.argv[1] if len(sys.argv) > 1 else "chinese_simplified"

    collected = set()
    file_count = 0
    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            if not f.endswith(".json"):
                continue
            if ".schema.json" in f or "_schemas" in root:
                continue
            path = Path(root) / f
            try:
                with path.open("r", encoding="utf-8") as fp:
                    data = json.load(fp)
                scan_i18n_strings(data, collected)
                file_count += 1
            except Exception as e:
                print(f"Warning: failed to scan {path}: {e}", file=sys.stderr)

    translations = load_existing_translations(language)
    # A translation is "missing" only if the new string is empty.
    # Translations identical to English are a quality issue, not a missing issue.
    missing = [s for s in sorted(collected) if s in translations and translations[s] == ""]
    translated_count = len(collected) - len(missing)

    print(f"Scanned {file_count} JSON files")
    print(f"Total JSON _i18n strings: {len(collected)}")
    print(f"Already translated: {translated_count}")
    print(f"Missing translations: {len(missing)}")

    if not missing:
        print("All JSON _i18n strings are translated!")
        return

    if openpyxl is None:
        print("openpyxl not installed; cannot write xlsx. Missing strings:")
        for s in missing[:50]:
            print(" -", s)
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "strings"
    ws.append(["", "File", "Context", "English (DO NOT MODIFY)", f"{language} Translation"])
    strings_file = f"game/tl/{language}/strings.rpy"
    for s in missing:
        ws.append(["", strings_file, "", s, ""])

    output = ROOT / f"json_i18n_missing_{language}.xlsx"
    wb.save(output)
    print(f"Exported missing strings to: {output}")
    print("Format is compatible with tools/import_translated_remaining_v3.py")


if __name__ == "__main__":
    main()
