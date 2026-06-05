import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


with open(str(ROOT / 'game/BKscreens.rpy'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

errors = []
for i, line in enumerate(lines, 1):
    # Check for double quotes after _()
    if re.search(r'_\(["\'].*?["\']\)\s*["\']', line):
        errors.append((i, 'double quote', line.strip()[:100]))
    # Check for text _(...) % pattern
    if re.search(r'^\s*text\s+_\(["\'].*?["\']\)\s*%', line):
        errors.append((i, 'text _() %', line.strip()[:100]))

print(f'Found {len(errors)} potential issues')
for e in errors[:20]:
    print(f'Line {e[0]} ({e[1]}): {e[2]}')
