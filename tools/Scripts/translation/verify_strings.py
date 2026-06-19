import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
STRINGS_PATH = ROOT / 'game/tl/chinese_simplified/strings.rpy'

with open(STRINGS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []
lines = content.split('\n')
for i, line in enumerate(lines):
    if line.strip().startswith('old ') and i+1 < len(lines):
        if not lines[i+1].strip().startswith('new '):
            errors.append(f'Line {i+1}: old without new: {line.strip()[:50]}')
    if line.strip().startswith('new '):
        val = line.strip()[4:].strip()
        if val and not (val.startswith('"') and val.endswith('"')):
            if val != '""':
                errors.append(f'Line {i+1}: suspicious new line: {line.strip()[:50]}')

print(f'Checked {len(lines)} lines')
if errors:
    print(f'Found {len(errors)} errors:')
    for e in errors[:10]:
        print(' ', e)
else:
    print('No obvious syntax errors found')

mismatches = 0
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith('old '):
        old_val = line[4:].strip().strip('"')
        if i+1 < len(lines) and lines[i+1].strip().startswith('new '):
            new_val = lines[i+1].strip()[4:].strip().strip('"')
            old_fmt = len(re.findall(r'%[sdif]', old_val))
            new_fmt = len(re.findall(r'%[sdif]', new_val))
            if old_fmt != new_fmt:
                mismatches += 1
                if mismatches <= 3:
                    print('STILL BAD:', repr(old_val[:60]))
        i += 1
    i += 1

if mismatches:
    print(f'WARNING: {mismatches} placeholder mismatches remain')
else:
    print('All placeholder counts match')
