#!/usr/bin/env python3
import re
import glob
from pathlib import Path
from collections import defaultdict

OLD_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc_cn")
NEW_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
OLD_TL_DIR = OLD_PROJECT / "game" / "tl" / "schinese"
NEW_TL_DIR = NEW_PROJECT / "game" / "tl" / "chinese_simplified"

# ---------------------------------------------------------------------------
# Build old original->translation index from dialogue comments
# ---------------------------------------------------------------------------
def build_old_original_index():
    index = {}
    for old_file in OLD_TL_DIR.glob("BK*.rpy"):
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Match: translate schinese HASH:\n\n    # "original text"\n    "translated text"
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
            index[original] = translated
    return index

# ---------------------------------------------------------------------------
# Build current dialogue index: hash -> (file, start, end, current_translation, original_text)
# ---------------------------------------------------------------------------
def build_current_dialogue_index():
    index = {}
    for fpath in NEW_TL_DIR.glob("**/*.rpy"):
        if 'strings.rpy' in str(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = re.compile(
            r'^translate chinese_simplified (\w+):\s*\n'
            r'(?:\s*\n)*'
            r'\s*#\s*(?:(\w+)\s+)?"((?:[^"\\]|\\.)*)"\s*\n'
            r'(\s*(?:(\w+)\s+)?)"((?:[^"\\]|\\.)*)"\s*\n',
            re.MULTILINE,
        )
        for m in pattern.finditer(content):
            hash_id = m.group(1)
            original = m.group(3)
            trans_start = m.start(6)
            trans_end = m.end(6)
            trans = m.group(6)
            if hash_id not in index:  # keep first occurrence
                index[hash_id] = {
                    'file': str(fpath),
                    'trans_start': trans_start,
                    'trans_end': trans_end,
                    'translation': trans,
                    'original': original,
                    'is_empty': trans == "",
                }
    return index

# ---------------------------------------------------------------------------
# Build old hash->translation index
# ---------------------------------------------------------------------------
def build_old_hash_index():
    index = {}
    for old_file in OLD_TL_DIR.glob("BK*.rpy"):
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = re.compile(
            r'^translate schinese (\w+):\s*\n'
            r'(?:\s*\n|\s*#.*\n)*'
            r'\s*(?:\w+\s+)?"((?:[^"\\]|\\.)*)"\s*\n',
            re.MULTILINE,
        )
        for m in pattern.finditer(content):
            index[m.group(1)] = m.group(2)
    return index

# ---------------------------------------------------------------------------
# Build old strings index
# ---------------------------------------------------------------------------
def build_old_strings_index():
    index = {}
    for old_file in OLD_TL_DIR.glob("BK*.rpy"):
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = re.compile(
            r'^\s*#\s*[^\n]*\n'
            r'\s*old\s+"((?:[^"\\]|\\.)*)"\s*\n'
            r'\s*new\s+"((?:[^"\\]|\\.)*)"\s*\n',
            re.MULTILINE,
        )
        for m in pattern.finditer(content):
            index[m.group(1)] = m.group(2)
    return index

# ---------------------------------------------------------------------------
# Build current strings index
# ---------------------------------------------------------------------------
def build_current_strings_index():
    index = {}
    strings_file = NEW_TL_DIR / "strings.rpy"
    if not strings_file.exists():
        return index
    with open(strings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(
        r'(^\s*#\s*[^\n]*\n\s*old\s+)"((?:[^"\\]|\\.)*)"(\s*\n\s*new\s+)"((?:[^"\\]|\\.)*)"(\s*\n)',
        re.MULTILINE,
    )
    for m in pattern.finditer(content):
        old_text = m.group(2)
        new_text = m.group(4)
        start = m.start(4)
        end = m.end(4)
        if old_text not in index:
            index[old_text] = {
                'translation': new_text,
                'start': start,
                'end': end,
                'is_empty': new_text == "",
            }
    return index

# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------
def main():
    print("Building indexes...")
    old_original = build_old_original_index()
    old_hash = build_old_hash_index()
    old_strings = build_old_strings_index()
    current_dialogue = build_current_dialogue_index()
    current_strings = build_current_strings_index()

    print(f"Old original texts:     {len(old_original)}")
    print(f"Old hash mappings:      {len(old_hash)}")
    print(f"Old strings mappings:   {len(old_strings)}")
    print(f"Current dialogue:       {len(current_dialogue)}")
    print(f"Current strings:        {len(current_strings)}")

    # Dialogue analysis
    dialogue_empty = sum(1 for v in current_dialogue.values() if v['is_empty'])
    dialogue_hash_match = sum(1 for h in current_dialogue if h in old_hash)
    dialogue_hash_mismatch = len(current_dialogue) - dialogue_hash_match

    # Text-level matching for hash mismatches
    text_match_count = 0
    text_mismatch_count = 0
    empty_count = 0
    text_match_examples = []

    for hash_id, info in current_dialogue.items():
        if hash_id in old_hash:
            continue  # Already matched by hash
        original = info['original']
        if info['is_empty']:
            empty_count += 1
        if original in old_original:
            text_match_count += 1
            if len(text_match_examples) < 5:
                text_match_examples.append((original, info['translation'], old_original[original]))
        else:
            text_mismatch_count += 1

    print("\n" + "=" * 70)
    print("DIALOGUE TRANSLATION ANALYSIS")
    print("=" * 70)
    print(f"Total dialogue blocks:              {len(current_dialogue)}")
    print(f"  Empty (need translation):         {dialogue_empty}")
    print(f"  Hash match with old _cn:          {dialogue_hash_match}")
    print(f"  Hash mismatch:                    {dialogue_hash_mismatch}")
    print(f"    - Text-level match possible:    {text_match_count}")
    print(f"    - No match at all:              {text_mismatch_count}")
    print(f"    - Of which are empty:           {empty_count}")

    if text_match_examples:
        print("\nText-level match examples:")
        for orig, cur, old in text_match_examples:
            print(f"  ORIG: {orig[:80]}")
            print(f"  CUR : {cur[:80]}")
            print(f"  OLD : {old[:80]}")
            print()

    # Strings analysis
    strings_empty = sum(1 for v in current_strings.values() if v['is_empty'])
    strings_match = sum(1 for old_text in current_strings if old_text in old_strings)
    strings_mismatch = len(current_strings) - strings_match

    # Text-level for strings mismatches
    strings_text_match = 0
    strings_text_examples = []
    for old_text, info in current_strings.items():
        if old_text in old_strings:
            continue
        if old_text in old_original:
            strings_text_match += 1
            if len(strings_text_examples) < 3:
                strings_text_examples.append((old_text, info['translation'], old_original[old_text]))

    print("=" * 70)
    print("STRINGS.RPY ANALYSIS")
    print("=" * 70)
    print(f"Total strings:                      {len(current_strings)}")
    print(f"  Empty (need translation):         {strings_empty}")
    print(f"  Text match with old _cn strings:  {strings_match}")
    print(f"  Text mismatch:                    {strings_mismatch}")
    print(f"    - Text-level match possible:    {strings_text_match}")

    if strings_text_examples:
        print("\nStrings text-level match examples:")
        for old_text, cur, old in strings_text_examples:
            print(f"  OLD_TEXT: {old_text[:60]}")
            print(f"  CUR_NEW : {cur[:60]}")
            print(f"  OLD_NEW : {old[:60]}")
            print()

    # Write report
    report_path = NEW_PROJECT / "temp" / "translations" / "translation_gap_analysis.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Translation Gap Analysis\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Dialogue blocks:\n")
        f.write(f"  Total:              {len(current_dialogue)}\n")
        f.write(f"  Empty:              {dialogue_empty}\n")
        f.write(f"  Hash match:         {dialogue_hash_match}\n")
        f.write(f"  Hash mismatch:      {dialogue_hash_mismatch}\n")
        f.write(f"    Text match poss:  {text_match_count}\n")
        f.write(f"    No match:         {text_mismatch_count}\n")
        f.write(f"\nStrings:\n")
        f.write(f"  Total:              {len(current_strings)}\n")
        f.write(f"  Empty:              {strings_empty}\n")
        f.write(f"  Text match:         {strings_match}\n")
        f.write(f"  Text mismatch:      {strings_mismatch}\n")
        f.write(f"    Text match poss:  {strings_text_match}\n")
    print(f"\nReport written to: {report_path}")


if __name__ == "__main__":
    main()
