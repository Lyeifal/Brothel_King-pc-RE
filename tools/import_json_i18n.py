#!/usr/bin/env python3
"""
Import missing JSON _i18n texts into strings.rpy.
Handles multiline strings using triple quotes.
Deduplicates by old text.
Correctly handles escape sequences (\\n -> real newline).
"""

import os
import json
import re
from pathlib import Path

NEW_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
NEW_TL_DIR = NEW_PROJECT / "game" / "tl" / "chinese_simplified"
NEW_STRINGS_RPY = NEW_TL_DIR / "strings.rpy"


def collect_json_i18n():
    texts = []
    for root, dirs, files in os.walk('game/core/data'):
        for file in files:
            if not file.endswith('.json'):
                continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def scan(obj, path=''):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if k.endswith('_i18n') and isinstance(v, str) and v:
                            texts.append((os.path.basename(filepath), path + '.' + k, v))
                        elif isinstance(v, (dict, list)):
                            scan(v, path + '.' + k)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        scan(item, path + f'[{i}]')
            
            scan(data)
    return texts


def unescape_renpy_string(text):
    """Convert Ren'Py escape sequences to real characters."""
    result = []
    i = 0
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text):
            nxt = text[i + 1]
            if nxt == 'n':
                result.append('\n')
                i += 2
            elif nxt == 't':
                result.append('\t')
                i += 2
            elif nxt == '"':
                result.append('"')
                i += 2
            elif nxt == '\\':
                result.append('\\')
                i += 2
            else:
                result.append(text[i])
                i += 1
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


def get_existing_old_texts():
    with open(NEW_STRINGS_RPY, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Single-quoted strings
    single = re.findall(r'old "((?:[^"\\]|\\.)*)"', content)
    # Triple-quoted strings
    triple = re.findall(r'old """([\s\S]*?)"""', content)
    
    all_texts = single + triple
    # Unescape Ren'Py escape sequences
    return set(unescape_renpy_string(t) for t in all_texts)


def escape_renpy_string(text):
    if '\n' in text or '\r' in text:
        escaped = text.replace('"""', '\"\"\"')
        return f'"""{escaped}"""'
    else:
        escaped = text.replace('"', '\\"')
        return f'"{escaped}"'


def main():
    print("Collecting JSON _i18n texts...")
    json_texts = collect_json_i18n()
    print(f"Total _i18n texts in JSON: {len(json_texts)}")
    
    existing = get_existing_old_texts()
    print(f"Existing old texts in strings.rpy: {len(existing)}")
    
    seen = set()
    missing = []
    for fp, path, text in json_texts:
        if text in existing or text in seen:
            continue
        seen.add(text)
        missing.append((fp, path, text))
    
    print(f"Missing from strings.rpy (deduped): {len(missing)}")
    
    if not missing:
        print("Nothing to import.")
        return
    
    lines = ['\n', '# Auto-imported JSON _i18n texts\n', 'translate chinese_simplified strings:\n\n']
    
    for fp, path, text in missing:
        formatted = escape_renpy_string(text)
        lines.append(f'    # {fp}: {path}\n')
        lines.append(f'    old {formatted}\n')
        lines.append(f'    new ""\n\n')
    
    import_block = ''.join(lines)
    
    with open(NEW_STRINGS_RPY, 'a', encoding='utf-8') as f:
        f.write(import_block)
    
    print(f"\nAppended {len(missing)} entries to strings.rpy")
    
    list_path = NEW_PROJECT / "temp" / "translations" / "json_i18n_to_translate.txt"
    list_path.parent.mkdir(parents=True, exist_ok=True)
    with open(list_path, 'w', encoding='utf-8') as f:
        for fp, path, text in missing:
            f.write(f"[{fp}] {text[:200]}\n")
    print(f"Translation list: {list_path}")


if __name__ == "__main__":
    main()
