#!/usr/bin/env python3
"""
Text-level migration: match current dialogue blocks by original English text
(rather than hash) against old _cn translations.
"""

import re
from pathlib import Path
from collections import defaultdict

OLD_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc_cn")
NEW_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
OLD_TL_DIR = OLD_PROJECT / "game" / "tl" / "schinese"
NEW_TL_DIR = NEW_PROJECT / "game" / "tl" / "chinese_simplified"

# ---------------------------------------------------------------------------
# Build old original->translation index
# ---------------------------------------------------------------------------
def build_old_original_index():
    index = {}
    for old_file in OLD_TL_DIR.glob("BK*.rpy"):
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = re.compile(
            r'^translate schinese \w+:\s*\n'
            r'(?:\s*\n)*'
            r'\s*#\s*(?:(\w+)\s+)?"((?:[^"\\]|\\.)*)"\s*\n'
            r'\s*(?:(\w+)\s+)?"((?:[^"\\]|\\.)*)"\s*\n',
            re.MULTILINE,
        )
        for m in pattern.finditer(content):
            original = m.group(2)
            translated = m.group(4)
            if original not in index:
                index[original] = translated
    return index


# ---------------------------------------------------------------------------
# Build current dialogue index per file
# ---------------------------------------------------------------------------
def build_current_file_index(fpath):
    """Return list of (hash, original, trans_start, trans_end, current_trans)"""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(
        r'^translate chinese_simplified (\w+):\s*\n'
        r'(?:\s*\n)*'
        r'\s*#\s*(?:(\w+)\s+)?"((?:[^"\\]|\\.)*)"\s*\n'
        r'(\s*(?:(\w+)\s+)?)"((?:[^"\\]|\\.)*)"\s*\n',
        re.MULTILINE,
    )
    blocks = []
    for m in pattern.finditer(content):
        hash_id = m.group(1)
        original = m.group(3)
        trans_start = m.start(6)
        trans_end = m.end(6)
        trans = m.group(6)
        blocks.append((hash_id, original, trans_start, trans_end, trans))
    return content, blocks


# ---------------------------------------------------------------------------
# Migrate one file
# ---------------------------------------------------------------------------
def migrate_file(fpath, old_original, report):
    content, blocks = build_current_file_index(fpath)
    if not blocks:
        return 0, 0

    replaced = 0
    skipped = 0
    replacements = []

    for hash_id, original, trans_start, trans_end, cur_trans in blocks:
        if original not in old_original:
            continue
        old_trans = old_original[original]
        if cur_trans == old_trans:
            skipped += 1
            continue
        replacements.append((trans_start, trans_end, old_trans))
        replaced += 1

    if replacements:
        replacements.sort(key=lambda x: x[0], reverse=True)
        content_list = list(content)
        for start, end, new_text in replacements:
            content_list[start:end] = list(new_text)
        content = ''.join(content_list)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

    return replaced, skipped


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Building old original text index...")
    old_original = build_old_original_index()
    print(f"Old original texts: {len(old_original)}")

    total_replaced = 0
    total_skipped = 0

    print("\nMigrating by text match...\n")
    for fpath in NEW_TL_DIR.glob("**/*.rpy"):
        if 'strings.rpy' in str(fpath):
            continue
        rep, skip = migrate_file(fpath, old_original, None)
        if rep > 0 or skip > 0:
            rel = fpath.relative_to(NEW_TL_DIR)
            print(f"{str(rel):60s} replaced={rep:4d} skipped={skip:4d}")
        total_replaced += rep
        total_skipped += skip

    print("\n" + "=" * 60)
    print(f"Total replaced: {total_replaced}")
    print(f"Total skipped:  {total_skipped}")

    report_path = NEW_PROJECT / "temp" / "translations" / "text_level_migration_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Text-Level Migration Report\n")
        f.write(f"Total replaced: {total_replaced}\n")
        f.write(f"Total skipped:  {total_skipped}\n")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
