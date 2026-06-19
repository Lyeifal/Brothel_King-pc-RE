#!/usr/bin/env python3
"""
Migrate high-quality manual translations from the old _cn version
to the current project by matching Ren'Py translation hashes.

Supports speaker tags:    speaker "text"
as well as plain:        "text"
"""

import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OLD_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc_cn")
NEW_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
OLD_TL_DIR = OLD_PROJECT / "game" / "tl" / "schinese"
NEW_TL_DIR = NEW_PROJECT / "game" / "tl" / "chinese_simplified"
NEW_STRINGS_RPY = NEW_TL_DIR / "strings.rpy"

DIALOGUE_FILE_MAP = {
    "BKstory_events.rpy":      "core/content/story_events/story_events.rpy",
    "BKchapter1.rpy":          "core/content/main_story/chapter1/chapter1.rpy",
    "BKchapter2.rpy":          "core/content/main_story/chapter2/chapter2.rpy",
    "BKchapter3.rpy":          "core/content/main_story/chapter3/chapter3.rpy",
    "BKinteractions.rpy":      "core/gameplay/interactions.rpy",
    "BKinteractions_free.rpy": "core/gameplay/interactions_free.rpy",
    "BKday_events.rpy":        "core/content/day_events/day_events.rpy",
    "BKcity_events.rpy":       "core/content/city_events/city_events.rpy",
    "BKevents.rpy":            "core/gameplay/events_dispatcher.rpy",
    "BKintro.rpy":             "core/gameplay/intro.rpy",
    "BKhelp.rpy":              "core/systems/help.rpy",
    "BKscreens.rpy":           "core/ui/screens.rpy",
    "BKscreen_home.rpy":       "core/ui/screens.rpy",  # merged
    "BKmain.rpy":              "core/ui/main.rpy",
    "BKendday.rpy":            "core/gameplay/endday.rpy",
    "BKstart.rpy":             "core/gameplay/start.rpy",
    "common.rpy":              "common.rpy",
    "options.rpy":             "common.rpy",  # merged
}

STRINGS_BULK_FILES = [
    "BKitems.rpy", "BKclasses.rpy", "BKfunctions.rpy", "BKsecurity.rpy",
    "BKpostings.rpy", "BKpowers.rpy", "BKspells.rpy", "BKtraits.rpy",
    "BKperks.rpy", "BKachievements.rpy", "BKminigame.rpy", "BKgirlclass.rpy",
    "BKdeclarations.rpy", "BKinit_variables.rpy",
]

# ---------------------------------------------------------------------------
# Regex
# ---------------------------------------------------------------------------

# Speaker tag is optional: (?:\w+\s+)?"..."
# Handles both:  "text"   and   speaker "text"
DIALOGUE_BLOCK_RE = re.compile(
    r'^translate schinese (\w+):\s*\n'
    r'(?:\s*\n|\s*#.*\n)*'
    r'\s*(?:\w+\s+)?"((?:[^"\\]|\\.)*)"\s*\n',
    re.MULTILINE,
)

CURRENT_DIALOGUE_RE = re.compile(
    r'^translate chinese_simplified (\w+):\s*\n'
    r'(?:\s*\n|\s*#.*\n)*'
    r'(\s*(?:\w+\s+)?)"((?:[^"\\]|\\.)*)"(\s*\n)',
    re.MULTILINE,
)

STRINGS_ENTRY_RE = re.compile(
    r'^\s*#\s*[^\n]*\n'
    r'\s*old\s+"((?:[^"\\]|\\.)*)"\s*\n'
    r'\s*new\s+"((?:[^"\\]|\\.)*)"\s*\n',
    re.MULTILINE,
)

STRINGS_OLD_RE = re.compile(
    r'(\s*#\s*[^\n]*\n\s*old\s+)"((?:[^"\\]|\\.)*)"(\s*\n\s*new\s+)"((?:[^"\\]|\\.)*)"(\s*\n)',
    re.MULTILINE,
)


def extract_dialogue_blocks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = {}
    for m in DIALOGUE_BLOCK_RE.finditer(content):
        blocks[m.group(1)] = m.group(2)
    return blocks


def extract_strings_bulk(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    pairs = {}
    for m in STRINGS_ENTRY_RE.finditer(content):
        pairs[m.group(1)] = m.group(2)
    return pairs


def build_dialogue_index(content):
    """hash -> (start, end, current_translation)"""
    index = {}
    for m in CURRENT_DIALOGUE_RE.finditer(content):
        hash_id = m.group(1)
        start = m.start(3)
        end = m.end(3)
        trans = m.group(3)
        if hash_id not in index:
            index[hash_id] = (start, end, trans)
    return index


def migrate_dialogue_file(old_path, new_path):
    if not new_path.exists():
        return 0, 0, 0, f"target not found: {new_path}"

    old_blocks = extract_dialogue_blocks(old_path)
    if not old_blocks:
        return 0, 0, 0, None

    with open(new_path, 'r', encoding='utf-8') as f:
        new_content = f.read()

    index = build_dialogue_index(new_content)

    replaced = 0
    skipped_same = 0
    not_found = 0
    replacements = []

    for hash_id, old_trans in old_blocks.items():
        if hash_id not in index:
            not_found += 1
            continue
        start, end, cur_trans = index[hash_id]
        if cur_trans == old_trans:
            skipped_same += 1
            continue
        replacements.append((start, end, old_trans))
        replaced += 1

    if replacements:
        replacements.sort(key=lambda x: x[0], reverse=True)
        content_list = list(new_content)
        for start, end, new_text in replacements:
            content_list[start:end] = list(new_text)
        new_content = ''.join(content_list)
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return replaced, skipped_same, not_found, None


def migrate_strings_bulk(all_old_pairs):
    if not NEW_STRINGS_RPY.exists():
        return 0, 0, 0, "strings.rpy not found"

    with open(NEW_STRINGS_RPY, 'r', encoding='utf-8') as f:
        content = f.read()

    replaced = 0
    skipped_same = 0
    not_found = 0
    replacements = []

    for old_text, new_text in all_old_pairs.items():
        old_escaped = re.escape(old_text)
        pattern = re.compile(
            r'(\s*#\s*[^\n]*\n\s*old\s+)"' + old_escaped + r'"(\s*\n\s*new\s+)"((?:[^"\\]|\\.)*)"(\s*\n)',
            re.MULTILINE,
        )
        m = pattern.search(content)
        if m:
            cur_new = m.group(3)
            if cur_new == new_text:
                skipped_same += 1
            else:
                start = m.start(3)
                end = m.end(3)
                replacements.append((start, end, new_text))
                replaced += 1
        else:
            not_found += 1

    if replacements:
        replacements.sort(key=lambda x: x[0], reverse=True)
        content_list = list(content)
        for start, end, new_text in replacements:
            content_list[start:end] = list(new_text)
        content = ''.join(content_list)
        with open(NEW_STRINGS_RPY, 'w', encoding='utf-8') as f:
            f.write(content)

    return replaced, skipped_same, not_found, None


def main():
    total_replaced = 0
    total_skipped = 0
    total_not_found = 0

    print("=" * 70)
    print("Translation Migration: _cn -> chinese_simplified")
    print("=" * 70)

    print("\n--- Dialogue Block Migration ---\n")
    for old_name, new_rel in DIALOGUE_FILE_MAP.items():
        old_path = OLD_TL_DIR / old_name
        new_path = NEW_TL_DIR / new_rel
        if not old_path.exists():
            print(f"[SKIP] Old file not found: {old_name}")
            continue
        rep, skip, nf, err = migrate_dialogue_file(old_path, new_path)
        if err:
            print(f"{old_name:30s} -> ERROR: {err}")
        else:
            print(f"{old_name:30s} -> replaced={rep:5d} skipped={skip:5d} not_found={nf:5d}")
        total_replaced += rep
        total_skipped += skip
        total_not_found += nf

    print("\n--- Strings Bulk Migration ---\n")
    all_old_pairs = {}
    for old_name in STRINGS_BULK_FILES:
        old_path = OLD_TL_DIR / old_name
        if not old_path.exists():
            print(f"[SKIP] Old file not found: {old_name}")
            continue
        pairs = extract_strings_bulk(old_path)
        print(f"{old_name:30s} | extracted {len(pairs):5d} pairs")
        all_old_pairs.update(pairs)

    print(f"\nTotal unique old/new pairs: {len(all_old_pairs)}")
    rep, skip, nf, err = migrate_strings_bulk(all_old_pairs)
    if err:
        print(f"strings.rpy -> ERROR: {err}")
    else:
        print(f"strings.rpy                    -> replaced={rep:5d} skipped={skip:5d} not_found={nf:5d}")
    total_replaced += rep
    total_skipped += skip
    total_not_found += nf

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total replaced:   {total_replaced}")
    print(f"Total skipped:    {total_skipped} (already identical)")
    print(f"Total not found:  {total_not_found} (hash/old text mismatch)")

    report_path = NEW_PROJECT / "temp" / "translations" / "translation_migration_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Translation Migration Report\n")
        f.write(f"Total replaced:   {total_replaced}\n")
        f.write(f"Total skipped:    {total_skipped}\n")
        f.write(f"Total not found:  {total_not_found}\n")
    print(f"\nReport: {report_path}")


if __name__ == "__main__":
    main()
