#!/usr/bin/env python3
"""Convert translated docx back to translated.txt for import."""
from docx import Document
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


doc = Document(str(ROOT / 'game/tl/chinese_simplified/to_translate_translated.docx'))

with open(str(ROOT / 'game/tl/chinese_simplified/translated.txt'), 'w', encoding='utf-8') as f:
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        # Extract [number] prefix
        m = re.match(r'^\[(\d+)\]\s*(.*)', text)
        if m:
            f.write(f"{m.group(1)}\t{m.group(2)}\n")

print("Saved: game/tl/chinese_simplified/translated.txt")
print("Now run: python tools/import_translation.py")
