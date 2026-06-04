#!/usr/bin/env python3
"""Remove empty-string entries from strings.rpy."""

import re

with open('game/tl/chinese_simplified/strings.rpy', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(
    r'^(\s*#(?:\s*TODO)?\s*[^\n]*)\n'
    r'\s*old\s+""\s*\n'
    r'\s*new\s+""\s*\n',
    re.MULTILINE
)

matches = list(pattern.finditer(content))
print(f"Found {len(matches)} empty-string entries")

new_content = pattern.sub('', content)

if new_content != content:
    with open('game/tl/chinese_simplified/strings.rpy', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Removed empty-string entries")
else:
    print("No empty-string entries to remove")
