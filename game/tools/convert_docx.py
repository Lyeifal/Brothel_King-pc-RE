#!/usr/bin/env python3
"""Convert translated docx back to translated.txt for import."""
from docx import Document
import re

doc = Document('game/tl/chinese_simplified/to_translated.docx')

count = 0
with open('game/tl/chinese_simplified/translated.txt', 'w', encoding='utf-8') as f:
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        # Extract [number] prefix
        m = re.match(r'^\[(\d+)\]\s*(.*)', text)
        if m:
            f.write(f"{m.group(1)}\t{m.group(2)}\n")
            count += 1

print(f"Saved {count} translations to: game/tl/chinese_simplified/translated.txt")
print("Now run: python game/tools/import_translation.py")
