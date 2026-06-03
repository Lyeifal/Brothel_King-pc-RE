import os

errors = []
for root, dirs, files in os.walk('game'):
    for f in files:
        if f.endswith('.rpy'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            for i, line in enumerate(content.split('\n'), 1):
                if '__(' in line:
                    depth = 0
                    in_str = None
                    escape = False
                    for c in line:
                        if escape:
                            escape = False
                            continue
                        if c == '\\':
                            escape = True
                            continue
                        if in_str:
                            if c == in_str:
                                in_str = None
                            continue
                        if c in ('"', "'"):
                            in_str = c
                            continue
                        if c == '(':
                            depth += 1
                        elif c == ')':
                            depth -= 1
                    if depth != 0:
                        errors.append(f'{path}:{i}')
                        print(f'{path}:{i}: {line.strip()[:80]}')

if errors:
    print(f'Found {len(errors)} potential issues')
else:
    print('No obvious unmatched parentheses found in __() calls')
