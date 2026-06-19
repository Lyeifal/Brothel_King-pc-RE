import sys, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent

sys.stdout.reconfigure(encoding='utf-8')

with open(str(ROOT / 'game/tl/chinese_simplified/strings.rpy'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

issues = []
for i, line in enumerate(lines):
    if line.strip().startswith('old '):
        m = re.match(r'old "(.*)"', line.strip())
        if m:
            inner = m.group(1)
            if '"' in inner or ' + ' in inner:
                issues.append((i+1, line.strip()))

print(f'Found {len(issues)} problematic old strings:')
for line_num, line_text in issues:
    print(f'{line_num}: {line_text}')
