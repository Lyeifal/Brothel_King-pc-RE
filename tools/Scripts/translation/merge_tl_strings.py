#!/usr/bin/env python3
"""
Remove duplicate 'translate chinese_simplified strings:' blocks from
tl/chinese_simplified/*.rpy files (except strings.rpy itself) and merge
their translations into strings.rpy.

This fixes the 'A translation for "..." already exists' runtime error.
"""

import glob
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
TL_DIR = ROOT / 'game/tl/chinese_simplified'

def parse_strings_block(text):
    """Parse a strings block into dict: old_text -> new_text"""
    result = {}
    # Match old/new pairs
    pattern = re.compile(
        r'^\s*#(?:\s*TODO)?\s*[^\n]*\n'
        r'\s*old\s+"(.*?)"\s*\n'
        r'\s*new\s+"(.*?)"\s*$',
        re.MULTILINE | re.DOTALL
    )
    for m in pattern.finditer(text):
        old_text = m.group(1).replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
        new_text = m.group(2).replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
        result[old_text] = new_text
    return result

def unquote_rpy(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == 'n':
                result.append('\n')
            elif nxt == 'r':
                result.append('\r')
            elif nxt == 't':
                result.append('\t')
            elif nxt == '"':
                result.append('"')
            elif nxt == '\\':
                result.append('\\')
            else:
                result.append(nxt)
            i += 2
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)

def quote_for_rpy(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')

def parse_strings_rpy(path):
    """Parse strings.rpy into dict: old_text -> (new_text, has_todo, comment)"""
    translations = {}
    if not os.path.exists(path):
        return translations
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(
        r'^(\s*#(?:\s*TODO)?\s*[^\n]*)\n'
        r'\s*old\s+"(.*?)"\s*\n'
        r'\s*new\s+"(.*?)"\s*$',
        re.MULTILINE | re.DOTALL
    )
    for m in pattern.finditer(content):
        comment = m.group(1)
        old_text = unquote_rpy(m.group(2))
        new_text = unquote_rpy(m.group(3))
        has_todo = 'TODO' in comment
        translations[old_text] = (new_text, has_todo, comment)
    return translations

def main():
    strings_rpy = TL_DIR / "strings.rpy"
    backup_rpy = TL_DIR / "strings.rpy.backup"
    
    # Read current strings.rpy
    print(f"Reading {strings_rpy}...")
    main_translations = parse_strings_rpy(strings_rpy)
    print(f"  Current entries: {len(main_translations)}")
    
    # Find all .rpy files in tl/ except strings.rpy
    files = sorted(glob.glob(str(TL_DIR / '*.rpy')))
    files = [f for f in files if not f.endswith('strings.rpy')]
    
    merged_count = 0
    removed_count = 0
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and remove strings blocks
        pattern = re.compile(
            r'^translate chinese_simplified strings:\s*\n'
            r'(.*?)(?=\n^translate chinese_simplified |\Z)',
            re.MULTILINE | re.DOTALL
        )
        
        new_content = content
        for m in pattern.finditer(content):
            block = m.group(0)
            block_translations = parse_strings_block(block)
            
            for old_text, new_text in block_translations.items():
                if old_text in main_translations:
                    # If the existing translation is a fallback (same as old) but
                    # the tl file has a real translation, prefer the real one
                    existing_new, existing_todo, existing_comment = main_translations[old_text]
                    if existing_new == old_text and new_text != old_text:
                        main_translations[old_text] = (new_text, False, f"    # {filepath.replace(chr(92), '/')} (merged)")
                        merged_count += 1
                else:
                    has_todo = new_text == old_text
                    comment = f"    # TODO {filepath.replace(chr(92), '/')} (merged)" if has_todo else f"    # {filepath.replace(chr(92), '/')} (merged)"
                    main_translations[old_text] = (new_text, has_todo, comment)
                    merged_count += 1
            
            removed_count += len(block_translations)
            new_content = new_content.replace(block, '', 1)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Removed strings block from {filepath}")
    
    print(f"\nMerged {merged_count} translations from tl files")
    
    # Rebuild strings.rpy
    output_lines = [
        "# Translation file for chinese_simplified",
        "# Auto-generated by merge_tl_strings.py",
        "",
        "translate chinese_simplified strings:",
        "",
    ]
    
    for old_text, (new_text, has_todo, comment) in sorted(main_translations.items()):
        old_quoted = quote_for_rpy(old_text)
        new_quoted = quote_for_rpy(new_text)
        
        if not comment.strip():
            comment = "    # "
        
        output_lines.append(comment)
        output_lines.append(f'    old "{old_quoted}"')
        output_lines.append(f'    new "{new_quoted}"')
        output_lines.append("")
    
    shutil.copy2(strings_rpy, backup_rpy)
    with open(strings_rpy, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines) + '\n')
    
    print(f"Written {strings_rpy} with {len(main_translations)} entries")
    
    # Count stats
    translated = sum(1 for _, (new, _, _) in main_translations.items() if new != _)
    # Wait, can't use _ as loop variable. Fix:
    translated = sum(1 for new_text, has_todo, comment in main_translations.values() if new_text != old_text)
    # Hmm, I don't have old_text in this loop. Let me fix:
    translated_count = 0
    for old_text, (new_text, has_todo, comment) in main_translations.items():
        if new_text != old_text:
            translated_count += 1
    
    print(f"  Translated: {translated_count}")
    print(f"  Untranslated (fallback): {len(main_translations) - translated_count}")

if __name__ == '__main__':
    main()
