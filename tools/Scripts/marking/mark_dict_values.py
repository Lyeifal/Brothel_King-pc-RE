#!/usr/bin/env python3
"""
Mark dictionary values in specific variables with __().
Only marks values, not keys.
"""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent


TARGET_DICTS = {'diff_name', 'diff_description', 'diff_setting_name', 'diff_setting_description', 'stat_name_dict', 'job_name_dict', 'sex_act_name_dict'}

def should_translate(text):
    t = text.strip()
    if not t or not t.strip(' \t\n'):
        return False
    return True


def wrap_dict_values(line):
    """Wrap string values in a dict line with __()."""
    result = []
    i = 0
    while i < len(line):
        # Look for :
        colon_pos = line.find(':', i)
        if colon_pos == -1:
            result.append(line[i:])
            break
        
        # Add everything up to and including :
        result.append(line[i:colon_pos+1])
        
        # Skip whitespace after :
        j = colon_pos + 1
        while j < len(line) and line[j].isspace():
            result.append(line[j])
            j += 1
        
        # Check if next is a quote
        if j < len(line) and line[j] in '"\'':
            quote = line[j]
            k = j + 1
            while k < len(line):
                if line[k] == '\\' and k + 1 < len(line):
                    k += 2
                elif line[k] == quote:
                    content = line[j+1:k]
                    if should_translate(content):
                        result.append(f'__({quote}{content}{quote})')
                    else:
                        result.append(f'{quote}{content}{quote}')
                    i = k + 1
                    break
                else:
                    k += 1
            else:
                # Unterminated string
                result.append(line[j:])
                break
        else:
            i = j
    
    return ''.join(result)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = []
    in_target = False
    bracket_depth = 0
    
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        
        if not in_target:
            for var in TARGET_DICTS:
                if re.match(rf'^\s*{re.escape(var)}\s*=\s*\{{', stripped):
                    in_target = True
                    bracket_depth = stripped.count('{') - stripped.count('}')
                    break
        
        if in_target:
            original = line
            new_line = wrap_dict_values(line)
            
            if new_line != original:
                changes.append((i, original.rstrip('\n'), new_line.rstrip('\n')))
                lines[i-1] = new_line
            
            bracket_depth += stripped.count('{') - stripped.count('}')
            if bracket_depth <= 0 and '{' in line:
                in_target = False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'game/BKinit_variables.rpy')
    changes = process_file(filepath)
    print(f"Processed: {filepath}")
    print(f"Changes: {len(changes)}")
    for line_num, old, new in changes[:10]:
        print(f"  Line {line_num}:")
        print(f"    - {old[:100]}")
        print(f"    + {new[:100]}")
