import os
import json
import re

# Read strings.rpy and build exact old text index
with open('game/tl/chinese_simplified/strings.rpy', 'r', encoding='utf-8') as f:
    strings_content = f.read()

old_pattern = re.compile(r'old "((?:[^"\\]|\\.)*)"')
old_texts = set(old_pattern.findall(strings_content))
print(f'strings.rpy unique old texts: {len(old_texts)}')

# Check JSON _i18n fields
missing = []
for root, dirs, files in os.walk('game/core/data'):
    for file in files:
        if not file.endswith('.json'):
            continue
        filepath = os.path.join(root, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        def scan(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k.endswith('_i18n') and isinstance(v, str) and v:
                        if v not in old_texts:
                            missing.append((os.path.basename(filepath), k, v))
                    elif isinstance(v, (dict, list)):
                        scan(v)
            elif isinstance(obj, list):
                for item in obj:
                    scan(item)
        
        scan(data)

print(f'JSON _i18n texts NOT in strings.rpy: {len(missing)}')
if missing:
    print('\nSample missing (first 30):')
    for fp, k, text in missing[:30]:
        print(f'  {fp} [{k}]: {text[:100]}')

    # Group by file
    by_file = {}
    for fp, k, text in missing:
        by_file.setdefault(fp, []).append(text)
    print('\n\nMissing by file:')
    for fp, texts in sorted(by_file.items(), key=lambda x: -len(x[1])):
        print(f'  {fp}: {len(texts)} missing')
