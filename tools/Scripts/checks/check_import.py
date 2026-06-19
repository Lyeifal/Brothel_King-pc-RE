import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent

sys.stdout.reconfigure(encoding='utf-8')

with open(str(ROOT / 'game/tl/chinese_simplified/strings.rpy'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

filled = 0
empty = 0
for line in lines:
    if 'new ' in line:
        if 'new ""' in line:
            empty += 1
        else:
            filled += 1

print(f'Filled: {filled}, Empty: {empty}')
