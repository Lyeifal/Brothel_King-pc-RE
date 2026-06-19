#!/usr/bin/env python3
"""
Mark character names in Character() definitions with _().
"""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = []
    
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith('#'):
            continue
        
        original = line
        # Match Character("..." or DynamicCharacter("..."
        # Replace the first string argument with _("...")
        # But skip if already wrapped
        
        def replacer(m):
            func = m.group(1)
            quote = m.group(2)
            name = m.group(3)
            
            # Skip if already wrapped
            before = m.string[:m.start()]
            if before.rstrip().endswith('_') or before.rstrip().endswith('__'):
                return m.group(0)
            
            # Skip empty or single-char names (likely not real names)
            if not name or len(name.strip()) <= 1:
                return m.group(0)
            
            # Skip names that look like variables
            if name.startswith('[') and name.endswith(']'):
                return m.group(0)
            
            return f'{func}({quote}{name}{quote}'
        
        # Pattern: Character( or DynamicCharacter( followed by quote string
        # But NOT Character(_(
        def char_replacer(m):
            name = m.group(3)
            # Skip variable references (contain . or end with _name or look like identifiers)
            if '.' in name or name.endswith('_name'):
                return m.group(0)
            # Skip if already wrapped
            before = m.string[:m.start()]
            if before.rstrip().endswith('_') or before.rstrip().endswith('__'):
                return m.group(0)
            # Skip empty or single char
            if len(name.strip()) <= 1:
                return m.group(0)
            return f'{m.group(1)}_({m.group(2)}{name}{m.group(4)})'
        
        new_line = re.sub(
            r'(\b(?:Character|DynamicCharacter)\s*\(\s*)(["\'])(.*?)(\2)',
            char_replacer,
            line
        )
        
        if new_line != original:
            changes.append((i, original.rstrip('\n'), new_line.rstrip('\n')))
            lines[i-1] = new_line
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'game/BKdeclarations.rpy')
    changes = process_file(filepath)
    print(f"Processed: {filepath}")
    print(f"Changes: {len(changes)}")
    for line_num, old, new in changes[:20]:
        print(f"  Line {line_num}:")
        print(f"    - {old[:100]}")
        print(f"    + {new[:100]}")
