#!/usr/bin/env python3
"""Convert to_translate.txt to docx for Google Translate document translation."""
from docx import Document
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent


with open(str(ROOT / 'game/tl/chinese_simplified/to_translate.txt'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

doc = Document()
doc.add_heading('Brothel King - Translation', 0)

for line in lines:
    line = line.rstrip('\n')
    if '\t' in line:
        parts = line.split('\t', 1)
        if len(parts) == 2:
            idx, text = parts
            p = doc.add_paragraph()
            p.add_run(f"[{idx}] ").bold = True
            p.add_run(text)

output_path = str(ROOT / 'game/tl/chinese_simplified/to_translate.docx')
doc.save(output_path)
print(f"Saved: {output_path}")
print("Upload this file to Google Translate (Document translation)")
print("After downloading the translated docx, run docx_to_txt.py")
