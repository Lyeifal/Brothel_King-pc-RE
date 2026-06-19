#!/usr/bin/env python3
"""
Export all untranslated strings and dialogues to an Excel file for manual translation.

Output: temp/translations/to_translate.xlsx
Sheets:
  - strings:     strings.rpy fallback entries
  - chapter1:    BKchapter1.rpy untranslated blocks
  - chapter2:    BKchapter2.rpy untranslated blocks
  - chapter3:    BKchapter3.rpy untranslated blocks
  - story:       BKstory_events.rpy untranslated blocks
  - city:        BKcity_events.rpy untranslated blocks
  - day:         BKday_events.rpy untranslated blocks
  - interact:    BKinteractions.rpy + BKinteractions_free.rpy untranslated blocks
  - other:       All other .rpy translation files

Format per row:
  English (原文) | Chinese (翻译) | Source File | Identifier (hash or old key)
"""

import glob
import os
import re
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

ROOT = Path(__file__).parent.parent.parent.parent
OUTPUT_FILE = ROOT / "temp" / "translations" / "to_translate.xlsx"
STRINGS_PATH = ROOT / 'game/tl/chinese_simplified/strings.rpy'

def unquote_rpy(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == 'n': result.append('\n')
            elif nxt == 'r': result.append('\r')
            elif nxt == 't': result.append('\t')
            elif nxt == '"': result.append('"')
            elif nxt == '\\': result.append('\\')
            else: result.append(nxt)
            i += 2
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)

def extract_strings_todo():
    """Extract fallback entries from strings.rpy"""
    rows = []
    with open(STRINGS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(
        r'^(\s*#(?:\s*TODO)?\s*[^\n]*)\n'
        r'\s*old\s+"(.*?)"\s*\n'
        r'\s*new\s+"(.*?)"\s*$',
        re.MULTILINE | re.DOTALL
    )
    for m in pattern.finditer(content):
        comment = m.group(1).strip()
        old_text = unquote_rpy(m.group(2))
        new_text = unquote_rpy(m.group(3))
        if new_text == old_text:
            rows.append((old_text, "", comment.replace('#', '').strip(), old_text))
    return rows

def extract_dialogue_todo(filepath):
    """Extract untranslated translate blocks from a Ren'Py translation file."""
    rows = []
    if not os.path.exists(filepath):
        return rows
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: find translate blocks
    # Format:
    # # game/file.rpy:123
    # translate chinese_simplified hash:
    #
    #     # character "Original English"
    #     character "Current Text"
    block_pattern = re.compile(
        r'(?:^#\s*(game/[^\n]+)\n)?'
        r'^translate\s+chinese_simplified\s+([a-zA-Z0-9_]+):\s*\n'
        r'\s*\n'
        r'\s*#\s+([^\n]+)\n'
        r'\s+([^\n]+)',
        re.MULTILINE
    )
    
    for m in block_pattern.finditer(content):
        source_file = m.group(1) if m.group(1) else ""
        hash_id = m.group(2)
        comment_line = m.group(3).strip()
        display_line = m.group(4).strip()
        
        # Parse comment line to get original English
        # Format: character "English text"
        comment_match = re.match(r'(\S+)\s+"(.*)"$', comment_line)
        if not comment_match:
            continue
        
        character = comment_match.group(1)
        original = comment_match.group(2)
        
        # Parse display line to get current text
        display_match = re.match(r'(\S+)\s+"(.*)"$', display_line)
        if not display_match:
            continue
        
        current = display_match.group(2)
        
        if current == original:
            rows.append((original, "", f"{source_file} #{hash_id}", hash_id, character))
    
    return rows

def create_sheet(wb, title, headers, rows):
    ws = wb.create_sheet(title=title)
    ws.append(headers)
    for row in rows:
        ws.append(row)
    
    # Style header
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        cell.font = Font(bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 80
    ws.column_dimensions['B'].width = 80
    ws.column_dimensions['C'].width = 40
    ws.column_dimensions['D'].width = 30
    if len(headers) > 4:
        ws.column_dimensions['E'].width = 20
    
    # Freeze header
    ws.freeze_panes = 'A2'
    
    return ws

def main():
    wb = Workbook()
    wb.remove(wb.active)  # Remove default sheet
    
    # 1. strings.rpy
    print("Extracting strings.rpy fallback entries...")
    string_rows = extract_strings_todo()
    print(f"  Found {len(string_rows)} untranslated strings")
    create_sheet(wb, "strings", ["English (原文)", "Chinese (翻译)", "Source", "Old Key"], string_rows)
    
    # 2. Dialogue files
    dialogue_files = {
        "chapter1": str(ROOT / "game/tl/chinese_simplified/BKchapter1.rpy"),
        "chapter2": str(ROOT / "game/tl/chinese_simplified/BKchapter2.rpy"),
        "chapter3": str(ROOT / "game/tl/chinese_simplified/BKchapter3.rpy"),
        "story": str(ROOT / "game/tl/chinese_simplified/BKstory_events.rpy"),
        "city": str(ROOT / "game/tl/chinese_simplified/BKcity_events.rpy"),
        "day": str(ROOT / "game/tl/chinese_simplified/BKday_events.rpy"),
        "interact": str(ROOT / "game/tl/chinese_simplified/BKinteractions.rpy"),
        "interact_free": str(ROOT / "game/tl/chinese_simplified/BKinteractions_free.rpy"),
        "help": str(ROOT / "game/tl/chinese_simplified/BKhelp.rpy"),
        "intro": str(ROOT / "game/tl/chinese_simplified/BKintro.rpy"),
        "main": str(ROOT / "game/tl/chinese_simplified/BKmain.rpy"),
        "minigame": str(ROOT / "game/tl/chinese_simplified/BKminigame.rpy"),
        "powers": str(ROOT / "game/tl/chinese_simplified/BKpowers.rpy"),
        "security": str(ROOT / "game/tl/chinese_simplified/BKsecurity.rpy"),
        "start": str(ROOT / "game/tl/chinese_simplified/BKstart.rpy"),
        "kite1": str(ROOT / "game/tl/chinese_simplified/kite_jobgirl 1_riddle.rpy"),
        "kite2": str(ROOT / "game/tl/chinese_simplified/kite_jobgirl 2_beach.rpy"),
    }
    
    total_dialogue = 0
    for sheet_name, filepath in dialogue_files.items():
        print(f"Extracting {filepath}...")
        rows = extract_dialogue_todo(filepath)
        if rows:
            print(f"  Found {len(rows)} untranslated blocks")
            create_sheet(wb, sheet_name, ["English (原文)", "Chinese (翻译)", "Source", "Hash", "Character"], rows)
            total_dialogue += len(rows)
        else:
            print(f"  No untranslated blocks found")
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUTPUT_FILE)
    print(f"\n{'='*60}")
    print(f"Exported to: {OUTPUT_FILE}")
    print(f"  strings.rpy: {len(string_rows)} entries")
    print(f"  Dialogue files: {total_dialogue} entries")
    print(f"  Total: {len(string_rows) + total_dialogue} entries")
    print(f"  Sheets: {len(wb.sheetnames)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
