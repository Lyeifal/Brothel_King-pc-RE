#!/usr/bin/env python3
"""
Mark menu option texts with _() in Ren'Py .rpy files.
"""
import re
import sys
import glob
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent


def should_translate(text):
    t = text.strip()
    if not t or not t.strip(' \t\n'):
        return False
    # Skip pure format strings
    if re.match(r'^[%\s\di\.efs\(\)\[\]\,\*\+\-/]+$' , t) and '%' in t:
        return False
    return True


def process_line(line, line_num):
    if line.lstrip().startswith('#'):
        return line
    
    # Match menu option: (indent)"Option text":
    # But not already wrapped, not inside python expressions
    stripped = line.lstrip()
    if not stripped.startswith('"'):
        return line
    
    # Check if this is a menu option (ends with :)
    # Menu options are typically indented and followed by a colon
    # But the colon might be on the same line or next line
    
    # Simple pattern: indented quote string at start of line
    # This catches most menu options
    m = re.match(r'^(\s+)(".*?")(\s*):', line)
    if m:
        indent = m.group(1)
        quote = m.group(2)
        rest = m.group(3)
        colon = line[m.end()-1:]
        
        # Extract content from quotes
        content = quote[1:-1]
        if not should_translate(content):
            return line
        
        # Check if already wrapped
        if line[:len(indent)].rstrip().endswith('_'):
            return line
        
        return f'{indent}_({quote}){rest}:'
    
    return line


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = []
    in_menu = False
    
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        
        # Detect menu block
        if re.match(r'^\s*menu\s*:', stripped):
            in_menu = True
            continue
        
        if in_menu:
            # Check if we've exited the menu block
            # (line with same or less indent as menu that's not empty/comment)
            if stripped and not stripped.startswith('#') and not line.startswith(' ' * (len(line) - len(stripped) + 4)):
                if not re.match(r'^\s*"', stripped):
                    in_menu = False
            
            if in_menu:
                original = line
                new_line = process_line(line, i)
                if new_line != original:
                    changes.append((i, original.rstrip('\n'), new_line.rstrip('\n')))
                    lines[i-1] = new_line
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


if __name__ == '__main__':
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = glob.glob(str(ROOT / 'game/*.rpy'))
    
    total_changes = 0
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        changes = process_file(filepath)
        if changes:
            print(f"{filepath}: {len(changes)} changes")
            total_changes += len(changes)
    
    print(f"\nTotal changes: {total_changes}")
