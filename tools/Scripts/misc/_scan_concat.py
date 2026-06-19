import os, re

results = []

for root, dirs, files in os.walk('game'):
    if 'tl' in root.split(os.sep):
        continue
    if 'tools' in root.split(os.sep):
        continue
    if 'data' in root.split(os.sep):
        continue
    for fname in files:
        if not fname.endswith('.rpy'):
            continue
        path = os.path.join(root, fname)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        for i, line in enumerate(lines, 1):
            # Match lines that contain both __() and + in some order
            if ('__' in line or '_(' in line) and '+' in line:
                # Simple heuristic: contains concatenation with translation
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if re.search(r'__\s*\(.*\)\s*\+|\+\s*__\s*\(|_\s*\(.*\)\s*\+|\+\s*_\s*\(', line):
                    results.append((path, i, stripped))

# Group by file
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent

by_file = defaultdict(list)
for path, i, line in results:
    by_file[path].append((i, line))

print(f"Found {len(results)} potential concatenation lines across {len(by_file)} files")
print()

# Show top files by count
sorted_files = sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True)
for path, lines in sorted_files[:15]:
    print(f"{path}: {len(lines)} lines")
    for i, line in lines[:3]:
        print(f"  {i}: {line[:120]}")
    if len(lines) > 3:
        print(f"  ... and {len(lines)-3} more")
    print()

with open('tools/_concat_report.txt', 'w', encoding='utf-8') as f:
    for path, lines in sorted_files:
        f.write(f"{path}\n")
        for i, line in lines:
            f.write(f"  {i}: {line}\n")
        f.write("\n")

print("Full report: tools/_concat_report.txt")
