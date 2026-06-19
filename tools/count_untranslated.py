import re
import glob

with open('game/tl/chinese_simplified/strings.rpy', 'r', encoding='utf-8') as f:
    content = f.read()

empty_strings = content.count('new ""')
print(f'strings.rpy empty new translations: {empty_strings}')

files = glob.glob('game/tl/chinese_simplified/**/*.rpy', recursive=True)
total_empty = 0
for f in files:
    if 'strings.rpy' in f:
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    empty = re.findall(r'translate chinese_simplified \w+:\s*\n(?:\s*\n|\s*#.*\n)*\s*(?:\w+\s+)?\"\"\s*\n', content)
    if empty:
        total_empty += len(empty)
        print(f'{f}: {len(empty)} empty translations')

print(f'Total empty dialogue translations: {total_empty}')
