#!/usr/bin/env python3
"""
Export remaining English empty translations from all chinese_simplified .rpy files.
Covers:
- strings.rpy
- per-file translate chinese_simplified strings: blocks
- dialogue blocks with empty translations

Skips entries where old text is already Chinese or empty (auto-filled by auto_fill_nonenglish_empty.py).
"""

import re
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("openpyxl not installed. Install with: pip install openpyxl")
    exit(1)

NEW_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
TL_DIR = NEW_PROJECT / "game" / "tl" / "chinese_simplified"

chinese_re = re.compile(r'[\u4e00-\u9fff]')


def parse_quoted_string(s):
    s = s.strip()
    if s.startswith('"""') and s.endswith('"""'):
        return s[3:-3]
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
    return s


def export_string_empty():
    """Export empty string entries from all translate chinese_simplified strings: blocks."""
    entries = []
    pattern = re.compile(
        r'(#\s*([^\n]*)\n\s*old\s+)("(?:[^"\\]|\\.)*"|"""[\s\S]*?""")(\s*\n\s*new\s+)""(\s*\n)',
        re.MULTILINE,
    )

    for fpath in sorted(TL_DIR.rglob('*.rpy')):
        content = fpath.read_text(encoding='utf-8')
        for m in pattern.finditer(content):
            old_val = m.group(3)
            old_text = parse_quoted_string(old_val)

            if not old_text or chinese_re.search(old_text):
                continue  # Already non-English; auto-filled or genuinely empty

            rel_path = fpath.relative_to(TL_DIR)
            comment = m.group(2).strip()
            is_common = rel_path.name == 'common.rpy'

            entries.append({
                'type': 'common' if is_common else 'string',
                'file': str(rel_path),
                'comment': comment,
                'english': old_text,
                'chinese': '',
            })
    return entries


def export_dialogue_empty():
    """Export dialogue blocks with empty translations."""
    entries = []
    pattern = re.compile(
        r'^translate chinese_simplified (\w+):\s*\n'
        r'(?:\s*\n)*'
        r'\s*#\s*(?:(\w+)\s+)?"((?:[^"\\]|\\.)*)"\s*\n'
        r'(\s*(?:(\w+)\s+)?)""\s*\n',
        re.MULTILINE,
    )

    for fpath in TL_DIR.glob("**/*.rpy"):
        content = fpath.read_text(encoding='utf-8')
        for m in pattern.finditer(content):
            hash_id = m.group(1)
            original = m.group(3)
            if not original or chinese_re.search(original):
                continue
            rel_path = fpath.relative_to(TL_DIR)
            entries.append({
                'type': 'dialogue',
                'file': str(rel_path),
                'comment': f'hash={hash_id}',
                'english': original,
                'chinese': '',
            })
    return entries


def main():
    print("Collecting remaining English empty translations...")
    string_entries = export_string_empty()
    dialogue_entries = export_dialogue_empty()

    game_entries = [e for e in string_entries if e['type'] != 'common']

    print(f"Game strings empty: {len(game_entries)}")
    print(f"Common strings empty: {len([e for e in string_entries if e['type'] == 'common'])} (skipped)")
    print(f"Dialogue empty: {len(dialogue_entries)}")

    wb = openpyxl.Workbook()

    # Game strings sheet
    ws1 = wb.active
    ws1.title = "strings"
    ws1.append(["Type", "File", "Context", "English (DO NOT MODIFY)", "Chinese Translation"])
    for e in game_entries:
        ws1.append([e['type'], e['file'], e['comment'], e['english'], e['chinese']])

    # Dialogue sheet
    ws2 = wb.create_sheet("dialogue")
    ws2.append(["Type", "File", "Hash", "English (DO NOT MODIFY)", "Chinese Translation"])
    for e in dialogue_entries:
        ws2.append([e['type'], e['file'], e['comment'], e['english'], e['chinese']])

    output = NEW_PROJECT / "temp" / "translations" / "to_translate_remaining_v3.xlsx"
    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output)
    print(f"\nExported to: {output}")
    print(f"Total entries: {len(game_entries) + len(dialogue_entries)}")


if __name__ == "__main__":
    main()
