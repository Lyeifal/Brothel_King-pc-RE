#!/usr/bin/env python3
"""
Export untranslated strings to a text file for external translation.
Format: one string per line, numbered.
Translator can use Google Translate, DeepL, etc. on the output file,
then run import_translation.py to merge back.
"""
import re

with open('game/tl/chinese_simplified/strings.rpy', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
pairs = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith('old '):
        m = re.match(r'old\s+"(.*)"', line)
        if m:
            old_text = m.group(1)
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('new '):
                if lines[i + 1].strip() == 'new ""':
                    pairs.append(old_text)
                i += 2
                continue
    i += 1

output_path = 'game/tl/chinese_simplified/to_translate.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    for idx, text in enumerate(pairs, 1):
        f.write(f"{idx}\t{text}\n")

print(f"Exported {len(pairs)} strings to {output_path}")
print("Next steps:")
print("1. Open to_translate.txt")
print("2. Translate the second column (tab-separated)")
print("3. Save as translated.txt in the same folder")
print("4. Run import_translation.py")
