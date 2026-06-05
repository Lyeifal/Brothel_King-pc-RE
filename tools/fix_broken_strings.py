import sys, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

sys.stdout.reconfigure(encoding='utf-8')

with open(str(ROOT / 'game/tl/chinese_simplified/strings.rpy'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find broken old strings and remove those entry pairs
broken_lines = [954, 5988, 8952, 8955, 8958, 8961, 8964, 8973, 9036, 10368]

new_lines = []
i = 0
while i < len(lines):
    if i + 1 < len(lines) and lines[i].strip().startswith('old '):
        line_num = i + 1
        if line_num in broken_lines:
            # Skip this old line and the next new line
            i += 2
            continue
    new_lines.append(lines[i])
    i += 1

with open(str(ROOT / 'game/tl/chinese_simplified/strings.rpy'), 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Removed {len(broken_lines)} broken entries")
