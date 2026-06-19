import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
STRINGS_PATH = ROOT / 'game/tl/chinese_simplified/strings.rpy'

with open(STRINGS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
fixed = 0
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    if stripped.startswith('old '):
        old_val = stripped[4:].strip().strip('"')
        if i+1 < len(lines) and lines[i+1].strip().startswith('new '):
            new_val = lines[i+1].strip()[4:].strip().strip('"')
            
            old_s = old_val.count('%s')
            new_s = new_val.count('%s')
            
            old_fmt = len(re.findall(r'%[sdif]', old_val))
            new_fmt = len(re.findall(r'%[sdif]', new_val))
            
            if old_fmt != new_fmt or old_s != new_s:
                indent = len(lines[i+1]) - len(lines[i+1].lstrip())
                lines[i+1] = ' ' * indent + f'new "{old_val}"'
                fixed += 1
                if fixed <= 10:
                    print(f'Fixed: {repr(old_val[:60])}...')
        i += 1
    i += 1

with open(STRINGS_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Fixed {fixed} placeholder mismatches')
