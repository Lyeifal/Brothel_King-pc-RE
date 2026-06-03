import os, re

errors = []
for root, dirs, files in os.walk('game'):
    for f in files:
        if f.endswith('.rpy'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            for i, line in enumerate(content.split('\n'), 1):
                # Find each __() call
                idx = 0
                while True:
                    pos = line.find('__(', idx)
                    if pos == -1:
                        break
                    # Check it's not __init__ or similar
                    if pos > 0 and line[pos-1].isalnum():
                        idx = pos + 1
                        continue
                    # Find matching paren for this __()
                    depth = 1
                    in_str = None
                    escape = False
                    matched = False
                    for j in range(pos + 3, len(line)):
                        c = line[j]
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
                            if depth == 0:
                                matched = True
                                idx = j + 1
                                break
                    if not matched:
                        errors.append(f'{path}:{i}')
                        print(f'{path}:{i}: {line.strip()[:100]}')
                        break
                    idx = pos + 1

if errors:
    print(f'Found {len(errors)} unmatched __() calls')
else:
    print('All __() calls appear balanced')
