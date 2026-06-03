#!/usr/bin/env python3
"""
Import translated strings back into strings.rpy.
Expects translated.txt with format: number\ttranslated_text
"""
import re

# Read original strings.rpy
with open('game/tl/chinese_simplified/strings.rpy', 'r', encoding='utf-8') as f:
    content = f.read()

# Read translations
with open('game/tl/chinese_simplified/translated.txt', 'r', encoding='utf-8') as f:
    translations = {}
    for line in f:
        line = line.rstrip('\n')
        if '\t' in line:
            parts = line.split('\t', 1)
            if len(parts) == 2:
                try:
                    idx = int(parts[0])
                    translations[idx] = parts[1]
                except ValueError:
                    pass

lines = content.split('\n')
idx = 0
i = 0
imported = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith('old '):
        m = re.match(r'old\s+"(.*)"', line)
        if m:
            idx += 1
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('new '):
                if idx in translations:
                    safe = translations[idx].replace('"', '\\"')
                    lines[i + 1] = f'    new "{safe}"'
                    imported += 1
                else:
                    # Clear existing translation if no new translation available
                    lines[i + 1] = '    new ""'
            i += 2
            continue
    i += 1

with open('game/tl/chinese_simplified/strings.rpy', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Imported {imported} translations, cleared {idx - imported}, total old strings: {idx}")
