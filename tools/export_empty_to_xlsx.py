#!/usr/bin/env python3
"""
Export all empty translations to an Excel file for manual translation.
Exports:
1. strings.rpy empty entries
2. Dialogue blocks with empty translations
"""

import re
import glob
from pathlib import Path

try:
    import openpyxl
    from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
except ImportError:
    print("openpyxl not installed. Install with: pip install openpyxl")
    exit(1)

NEW_PROJECT = Path(__file__).resolve().parent.parent
NEW_TL_DIR = NEW_PROJECT / "game" / "tl" / "chinese_simplified"
NEW_STRINGS_RPY = NEW_TL_DIR / "strings.rpy"


def clean(text):
    return ILLEGAL_CHARACTERS_RE.sub("", text)


def export_strings_empty():
    pattern = re.compile(
        r'(\s*#\s*[^\n]*\n\s*old\s+)("(?:[^"\\]|\\.)*"|"""[\s\S]*?""")(\s*\n\s*new\s+)""(\s*\n)',
        re.MULTILINE,
    )
    
    entries = []
    for fpath in NEW_TL_DIR.glob("**/*.rpy"):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Only scan blocks inside translate chinese_simplified strings:
        strings_block_pattern = re.compile(
            r'translate\s+chinese_simplified\s+strings:\s*\n'
            r'((?:\s*#.*\n|\s*old\s+.*?\n\s*new\s+.*?\n)+)',
            re.MULTILINE,
        )
        
        for block_match in strings_block_pattern.finditer(content):
            block = block_match.group(1)
            for m in pattern.finditer(block):
                old_text = m.group(2)
                if old_text.startswith('"""'):
                    raw = old_text[3:-3]
                else:
                    raw = old_text[1:-1]
                    raw = raw.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
                
                # Get comment
                comment_match = re.search(r'#\s*([^\n]*)', m.group(1))
                comment = comment_match.group(1) if comment_match else ""
                
                rel_path = fpath.relative_to(NEW_TL_DIR)
                entries.append({
                    'type': 'string',
                    'file': str(rel_path),
                    'comment': comment,
                    'english': raw,
                    'chinese': '',
                })
    return entries


def export_dialogue_empty():
    entries = []
    pattern = re.compile(
        r'^translate chinese_simplified (\w+):\s*\n'
        r'(?:\s*\n)*'
        r'\s*#\s*(?:(\w+)\s+)?"((?:[^"\\]|\\.)*)"\s*\n'
        r'(\s*(?:(\w+)\s+)?)""\s*\n',
        re.MULTILINE,
    )
    
    for fpath in NEW_TL_DIR.glob("**/*.rpy"):
        if 'strings.rpy' in str(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for m in pattern.finditer(content):
            hash_id = m.group(1)
            original = m.group(3)
            rel_path = fpath.relative_to(NEW_TL_DIR)
            entries.append({
                'type': 'dialogue',
                'file': str(rel_path),
                'comment': f'hash={hash_id}',
                'english': original,
                'chinese': '',
            })
    return entries


def main():
    print("Collecting empty translations...")
    strings_empty = export_strings_empty()
    dialogue_empty = export_dialogue_empty()
    
    print(f"strings.rpy empty: {len(strings_empty)}")
    print(f"dialogue empty: {len(dialogue_empty)}")
    
    # Create workbook
    wb = openpyxl.Workbook()
    
    # Strings sheet
    ws1 = wb.active
    ws1.title = "strings"
    ws1.append(["Type", "File", "Context", "English (DO NOT MODIFY)", "Chinese Translation"])
    for e in strings_empty:
        ws1.append([e['type'], e['file'], clean(e['comment']), clean(e['english']), e['chinese']])
    
    # Dialogue sheet
    ws2 = wb.create_sheet("dialogue")
    ws2.append(["Type", "File", "Hash", "English (DO NOT MODIFY)", "Chinese Translation"])
    for e in dialogue_empty:
        ws2.append([e['type'], e['file'], e['comment'], clean(e['english']), e['chinese']])
    
    output = NEW_PROJECT / "temp" / "translations" / "to_translate_empty.xlsx"
    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output)
    print(f"\nExported to: {output}")
    print(f"Total entries: {len(strings_empty) + len(dialogue_empty)}")


if __name__ == "__main__":
    main()
