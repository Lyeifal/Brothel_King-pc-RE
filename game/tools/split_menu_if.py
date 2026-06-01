#!/usr/bin/env python3
"""
Split merged menu items that have 'if' statements back into two lines.
This fixes Indentation mismatch errors caused by if/else blocks on the same line as menu options.
"""
import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed = False
    new_lines = []
    in_menu = False
    
    for line in lines:
        original = line
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        
        # Detect menu block
        if re.match(r'^\s*menu\s*:', stripped):
            in_menu = True
            new_lines.append(line)
            continue
        
        if in_menu:
            # Check if we've exited the menu block
            if stripped and not stripped.startswith('#') and not stripped.startswith('"') and not re.match(r'^\s*\$', stripped):
                if indent <= 4:
                    in_menu = False
                    new_lines.append(line)
                    continue
            
            # Pattern: "Text":    if condition:
            # Split into:
            # "Text":
            #     if condition:
            m = re.match(r'^(\s+)("[^"]+"):(\s+if\s+.+:)$', line.rstrip('\n'))
            if m:
                menu_indent = m.group(1)
                option = m.group(2)
                code = m.group(3).lstrip()  # Remove leading whitespace from code
                # New format: option on its own line, code indented +4
                new_lines.append(f'{menu_indent}{option}:\n')
                new_lines.append(f'{menu_indent}    {code}\n')
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
