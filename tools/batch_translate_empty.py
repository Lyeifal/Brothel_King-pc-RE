#!/usr/bin/env python3
"""
Batch translate empty entries in strings.rpy using deep_translator.
Processes in small batches with progress output.
"""

import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator

NEW_PROJECT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
NEW_STRINGS_RPY = NEW_PROJECT / "game" / "tl" / "chinese_simplified" / "strings.rpy"
BATCH_SIZE = 30


def batch_translate():
    translator = GoogleTranslator(source='en', target='zh-CN')

    with open(NEW_STRINGS_RPY, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = re.compile(
        r'(\s*#\s*[^\n]*\n\s*old\s+)("(?:[^"\\]|\\.)*"|"""[\s\S]*?""")(\s*\n\s*new\s+)""(\s*\n)',
        re.MULTILINE,
    )

    matches = list(pattern.finditer(content))
    print(f"Found {len(matches)} empty translations")
    if not matches:
        return

    # Collect all texts and their positions
    entries = []
    for m in matches:
        old_text = m.group(2)
        if old_text.startswith('"""'):
            raw = old_text[3:-3]
        else:
            raw = old_text[1:-1]
            raw = raw.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
        
        new_start = m.end(3)
        new_end = m.end(3) + 2
        entries.append((raw, new_start, new_end))

    # Batch translate
    all_texts = [e[0] for e in entries]
    all_translations = []
    
    total = len(all_texts)
    for i in range(0, total, BATCH_SIZE):
        batch = all_texts[i:i+BATCH_SIZE]
        print(f"Translating batch {i//BATCH_SIZE + 1}/{(total-1)//BATCH_SIZE + 1} ({i+1}-{min(i+BATCH_SIZE, total)} of {total})...")
        try:
            results = translator.translate_batch(batch)
            all_translations.extend(results)
        except Exception as e:
            print(f"  Batch failed: {e}, trying individually...")
            for text in batch:
                try:
                    t = translator.translate(text)
                    all_translations.append(t)
                except Exception as e2:
                    print(f"    Failed: {text[:40]}... -> {e2}")
                    all_translations.append("")
        time.sleep(0.5)  # Rate limiting

    # Apply translations
    replacements = []
    for (raw, new_start, new_end), trans in zip(entries, all_translations):
        if not trans:
            continue
        if '\n' in raw:
            escaped = trans.replace('"""', '\"\"\"')
            formatted = f'"""{escaped}"""'
        else:
            escaped = trans.replace('"', '\\"')
            formatted = f'"{escaped}"'
        replacements.append((new_start, new_end, formatted))

    if replacements:
        replacements.sort(key=lambda x: x[0], reverse=True)
        content_list = list(content)
        for start, end, new_text in replacements:
            content_list[start:end] = list(new_text)
        content = ''.join(content_list)
        with open(NEW_STRINGS_RPY, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nTranslated {len(replacements)} of {len(entries)} entries")
    else:
        print("No translations applied")


if __name__ == "__main__":
    batch_translate()
