#!/usr/bin/env python3
"""
Split ALL merged menu items back into proper two-line format.
Ren'Py requires menu options to end with ':' at end-of-line.
"""
import glob
import re

def fix_file(filepath):
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
        
        # Detect menu block
        if re.match(r'^\s*menu\s*:', stripped):
            in_menu = True
            menu_indent = indent
            new_lines.append(line)
            continue
        
        if in_menu:
            # Check if we've exited the menu block
            if stripped and not stripped.startswith('#') and not stripped.startswith('"') and not re.match(r'^\s*\$', stripped):
                if indent <= menu_indent:
                    in_menu = False
                    new_lines.append(line)
                    continue
            
            # Pattern: "Text":    <code>
            # Split into:
            # "Text":
            #     <code>
            # Must match: quote text quote colon whitespace code
            m = re.match(r'^(\s+)("[^"]+"):(\s+\S.*)$', line.rstrip('\n'))
            if m:
                menu_indent_str = m.group(1)
                option = m.group(2)
                code = m.group(3).lstrip()
                new_lines.append(f'{menu_indent_str}{option}:\n')
                new_lines.append(f'{menu_indent_str}    {code}\n')
                fixed = True
                continue
        
        new_lines.append(line)
    
    if fixed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False


if __name__ == '__main__':
    files = glob.glob('game/**/*.rpy', recursive=True)
    fixed_count = 0
    for f in files:
        if fix_file(f):
            print(f"Fixed: {f}")
            fixed_count += 1
    print(f"Total files fixed: {fixed_count}")
