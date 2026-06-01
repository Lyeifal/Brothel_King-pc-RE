#!/usr/bin/env python3
"""
Mark string values in specific function keyword arguments with __().
Targets: description=, name=, caption=, title= etc.
"""
import re
import sys
import glob
import os

# Keyword arguments to mark
TARGET_KWARGS = {'description', 'name', 'caption', 'title', 'message', 'label'}

def should_translate(text):
    t = text.strip()
    if not t or not t.strip(' \t\n'):
        return False
    if re.match(r'^#[0-9a-fA-F]{6,8}$', t):
        return False
    if '/' in t and ('.' in t or t.startswith('game/') or t.startswith('UI/')):
        return False
    if re.match(r'^[%\s\di\.efs\(\)\[\]\,\*\+\-/]+$' , t) and '%' in t:
        return False
    return True


def process_line(line):
    if line.lstrip().startswith('#'):
        return line
    
    new_line = line
    offset = 0
    
    for kw in TARGET_KWARGS:
        # Match: kw="..." or kw = "..." or kw= '...'
        pattern = rf'\b{kw}\s*=\s*(["\'])'
        
        for m in re.finditer(pattern, new_line):
            pos = m.end() - 1 + offset
            quote = m.group(1)
            
            # Check if already wrapped
            before = new_line[:m.start() + offset].rstrip()
            if before.endswith('__') or before.endswith('_'):
                continue
            
            # Parse string
            j = pos + 1
            while j < len(new_line):
                if new_line[j] == '\\' and j + 1 < len(new_line):
                    j += 2
                elif new_line[j] == quote:
                    content = new_line[pos+1:j]
                    str_end = j + 1
                    
                    if not should_translate(content):
                        break
                    
                    old_part = new_line[m.start() + offset:str_end]
                    new_part = new_line[m.start() + offset:m.end() + offset - 1] + '__(' + quote + content + quote + ')'
                    new_line = new_line[:m.start() + offset] + new_part + new_line[str_end:]
                    offset += len(new_part) - len(old_part)
                    break
                else:
                    j += 1
    
    return new_line


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = []
    for i, line in enumerate(lines, 1):
        new_line = process_line(line)
        if new_line != line:
            changes.append((i, line.rstrip('\n'), new_line.rstrip('\n')))
            lines[i-1] = new_line
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


if __name__ == '__main__':
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = glob.glob('game/*.rpy')
    
    total = 0
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        changes = process_file(filepath)
        if changes:
            print(f"{filepath}: {len(changes)} changes")
            total += len(changes)
    print(f"Total: {total}")
