#!/usr/bin/env python3
"""Fix remaining syntax errors:
1. Missing comma after __() in lists (BKinit_variables.rpy)
2. Merged menu items with 'if' condition (BKinteractions.rpy, BKstory_events.rpy)
"""
import re

# Fix 1: BKinit_variables.rpy - add missing comma after __()) where next line starts with __()
with open('game/BKinit_variables.rpy', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    stripped = line.rstrip()
    # Check if current line ends with __("...") (no comma) and next line starts with __(
    if i + 1 < len(lines):
        next_line = lines[i + 1]
        if stripped.endswith(')') and not stripped.endswith('),') and next_line.strip().startswith('__'):
            # Check if this looks like a __() call at end of line
            if re.search(r'__\(["\'].*["\']\)$', stripped):
                line = line.rstrip() + ',\n'
    new_lines.append(line)

with open('game/BKinit_variables.rpy', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

# Fix 2: Split menu items with 'if condition' that have code on same line
def fix_merged_if_menus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed = False
    new_lines = []
    in_menu = False
    menu_indent = 0
    
    for line in lines:
        original = line
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        
        if re.match(r'^\s*menu\s*:', stripped):
            in_menu = True
            menu_indent = indent
            new_lines.append(line)
            continue
        
        if in_menu:
            if stripped and not stripped.startswith('#') and not stripped.startswith('"') and not re.match(r'^\s*\$', stripped):
                if indent <= menu_indent:
                    in_menu = False
                    new_lines.append(line)
                    continue
            
            # Pattern: "Text" if condition:    code
            m = re.match(r'^(\s+)("[^"]+"\s+if\s+[^:]+:)(\s+\S.*)$', line.rstrip('\n'))
            if m:
                menu_indent_str = m.group(1)
                option = m.group(2)
                code = m.group(3).lstrip()
                new_lines.append(f'{menu_indent_str}{option}\n')
                new_lines.append(f'{menu_indent_str}    {code}\n')
                fixed = True
                continue
        
        new_lines.append(line)
    
    if fixed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

for filepath in ['game/BKinteractions.rpy', 'game/BKstory_events.rpy']:
    if fix_merged_if_menus(filepath):
        print(f"Fixed: {filepath}")

print("Done.")
