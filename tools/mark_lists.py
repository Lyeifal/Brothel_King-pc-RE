#!/usr/bin/env python3
"""
Mark string items in specific list variables with __().
"""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


TARGET_LISTS = {'random_tips', 'tip_list'}

def should_translate(text):
    t = text.strip()
    if not t or not t.strip(' \t\n'):
        return False
    if re.match(r'^#[0-9a-fA-F]{6,8}$', t):
        return False
    return True


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = []
    in_target = False
    bracket_depth = 0
    
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        
        if not in_target:
            for var in TARGET_LISTS:
                if re.match(rf'^\s*{re.escape(var)}\s*=\s*\[', stripped):
                    in_target = True
                    bracket_depth = stripped.count('[') - stripped.count(']')
                    break
        
        if in_target:
            original = line
            # Match: (whitespace)"string"(optional comma)
            new_line = re.sub(
                r'^(\s+)("[^"]*")(\s*,?\s*)$',
                lambda m: f'{m.group(1)}__({m.group(2)}){m.group(3)}' if should_translate(m.group(2)[1:-1]) else m.group(0),
                line
            )
            
            if new_line != original:
                changes.append((i, original.rstrip('\n'), new_line.rstrip('\n')))
                lines[i-1] = new_line
            
            bracket_depth += stripped.count('[') - stripped.count(']')
            if bracket_depth <= 0 and '[' in line:
                in_target = False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'game/BKinit_variables.rpy')
    changes = process_file(filepath)
    print(f"Processed: {filepath}")
    print(f"Changes: {len(changes)}")
