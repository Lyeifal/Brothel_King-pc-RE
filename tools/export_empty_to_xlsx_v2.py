#!/usr/bin/env python3
"""
Export all empty string translations to an Excel file for manual translation.
Scans all .rpy files under game/tl/chinese_simplified/ for:
- translate chinese_simplified strings: blocks with empty `new ""`
- Per-file string translation blocks

Does NOT export dialogue blocks (those are handled separately if needed).
"""

import re
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("openpyxl not installed. Install with: pip install openpyxl")
    exit(1)

NEW_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
NEW_TL_DIR = NEW_PROJECT / "game" / "tl" / "chinese_simplified"


def parse_string_literal(s):
    """Parse a Ren'Py string literal (double or triple quoted)."""
    s = s.strip()
    if s.startswith('"""') and s.endswith('"""'):
        return s[3:-3]
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
        s = s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\\\", "\\")
        return s
    return s


def export_empty_string_entries():
    entries = []

    # Pattern matches:
    #     old "..."
    #     new ""
    # including optional comment lines and leading whitespace
    pattern = re.compile(
        r'^\s*(#.*\n)?\s*old\s+("(?:[^"\\]|\\.)*"|"""[\s\S]*?""")\s*\n\s*new\s+""\s*$',
        re.MULTILINE,
    )

    for fpath in NEW_TL_DIR.rglob('*.rpy'):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        for m in pattern.finditer(content):
            comment = m.group(1) or ''
            comment = comment.strip().lstrip('#').strip() if comment else ''
            raw = parse_string_literal(m.group(2))
            rel_path = fpath.relative_to(NEW_PROJECT)
            entries.append({
                'file': str(rel_path),
                'comment': comment,
                'english': raw,
                'chinese': '',
            })

    return entries


def main():
    print("Collecting empty string translations...")
    entries = export_empty_string_entries()

    print(f"Total empty string entries: {len(entries)}")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "strings"
    # Match import_translated_remaining_v3.py column layout (col B=file, C=context, D=english, E=chinese)
    ws.append(["", "File", "Context", "English (DO NOT MODIFY)", "Chinese Translation"])

    for e in entries:
        ws.append(["", e['file'], e['comment'], e['english'], e['chinese']])

    output = NEW_PROJECT / "temp" / "translations" / "to_translate_phase1.xlsx"
    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output)
    print(f"\nExported to: {output}")


if __name__ == "__main__":
    main()
