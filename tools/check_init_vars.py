import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


with open(str(ROOT / 'game/BKinit_variables.rpy'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    for m in re.finditer(r'__\((".*?")\)', line):
        content = m.group(1)
        if len(content) < 4 or content.startswith('"tb ') or content.startswith('"side ') or content.startswith('"bg_'):
            print(f'Line {i}: {content[:60]}')
