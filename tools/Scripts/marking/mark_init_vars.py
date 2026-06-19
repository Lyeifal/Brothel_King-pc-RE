#!/usr/bin/env python3
"""
Specialized translation marker for BKinit_variables.rpy.
Only marks specific known variables that contain user-visible text.
"""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent


TARGET_VARS = {
    'diff_name',
    'diff_description', 
    'diff_setting_name',
    'diff_setting_description',
    'random_tips',
    'tip_list',
}

def should_translate(text):
    t = text.strip()
    if not t or not t.strip(' \t\n'):
        return False
    if re.match(r'^#[0-9a-fA-F]{6,8}$', t):
        return False
    if '/' in t and ('.' in t or 'game/' in t):
        return False
    if re.match(r'^[%\s\di\.efs\(\)\[\]\,\*\+\-/]+$' , t) and '%' in t:
        return False
    return True


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Process each target variable
    for var in TARGET_VARS:
        # Pattern to find the variable definition and its content
        # We look for: var = { ... } or var = [ ... ]
        pattern = rf'(\b{re.escape(var)}\s*=\s*)([\{{\[])(.*?)([\}}\]])'
        
        def replacer(m):
            prefix = m.group(1)
            open_bracket = m.group(2)
            body = m.group(3)
            close_bracket = m.group(4)
            
            new_body = body
            body_offset = 0
            
            if open_bracket == '{':
                # Dictionary: replace values only
                # Match: "key" : "value" (with possible spaces)
                for vm in re.finditer(r'((?<=:\s)|(?<=:\s{2,}))"([^"]*)"', body):
                    # Actually, simpler: find all occurrences of : "..." or :  "..."
                    pass
                
                # Better approach: find all "..." that come after :
                # Use a loop with offset
                i = 0
                while i < len(new_body):
                    # Look for : followed by optional spaces and a quote
                    colon_pos = new_body.find(':', i)
                    if colon_pos == -1:
                        break
                    
                    j = colon_pos + 1
                    while j < len(new_body) and new_body[j].isspace():
                        j += 1
                    
                    if j < len(new_body) and new_body[j] == '"':
                        # Found a value string
                        quote_start = j
                        k = j + 1
                        while k < len(new_body):
                            if new_body[k] == '\\' and k + 1 < len(new_body):
                                k += 2
                            elif new_body[k] == '"':
                                content = new_body[quote_start+1:k]
                                if should_translate(content):
                                    old_part = new_body[quote_start:k+1]
                                    new_part = '__(' + '"' + content + '"' + ')'
                                    new_body = new_body[:quote_start] + new_part + new_body[k+1:]
                                    body_offset += len(new_part) - len(old_part)
                                i = k + 1 + body_offset
                                break
                            else:
                                k += 1
                        else:
                            break
                    else:
                        i = colon_pos + 1
            
            elif open_bracket == '[':
                # List: replace all string items
                i = 0
                while i < len(new_body):
                    if new_body[i] == '"':
                        quote_start = i
                        k = i + 1
                        while k < len(new_body):
                            if new_body[k] == '\\' and k + 1 < len(new_body):
                                k += 2
                            elif new_body[k] == '"':
                                content = new_body[quote_start+1:k]
                                if should_translate(content):
                                    old_part = new_body[quote_start:k+1]
                                    new_part = '__(' + '"' + content + '"' + ')'
                                    new_body = new_body[:quote_start] + new_part + new_body[k+1:]
                                    body_offset += len(new_part) - len(old_part)
                                i = k + 1
                                break
                            else:
                                k += 1
                        else:
                            break
                    else:
                        i += 1
            
            return prefix + open_bracket + new_body + close_bracket
        
        # We need a different approach: find the variable block and process it
        # Use a simpler method: search for the variable and extract the block
    
    # Simpler approach: process the entire file line by line
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_target = False
    target_started = False
    bracket_depth = 0
    
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        
        # Check if we're starting a target variable
        if not in_target:
            for var in TARGET_VARS:
                if re.match(rf'^\s*{re.escape(var)}\s*=\s*[\{{\[]', stripped):
                    in_target = True
                    target_started = True
                    bracket_depth = 0
                    break
        
        if in_target:
            original_line = line
            new_line = line
            
            # Count brackets to track depth
            bracket_depth += line.count('{') + line.count('[')
            bracket_depth -= line.count('}') + line.count(']')
            
            # If this is the first line, we need to handle the opening bracket
            if target_started:
                # Find the opening bracket position
                bracket_pos = max(line.find('{'), line.find('['))
                if bracket_pos != -1:
                    before = line[:bracket_pos+1]
                    rest = line[bracket_pos+1:]
                else:
                    before = line
                    rest = ''
                target_started = False
            else:
                before = ''
                rest = line
            
            # Process the rest of the line
            if rest:
                offset = 0
                j = 0
                while j < len(rest):
                    # For dict values: look for : "..." or :  "..."
                    if rest[j] == ':':
                        k = j + 1
                        while k < len(rest) and rest[k].isspace():
                            k += 1
                        if k < len(rest) and rest[k] == '"':
                            # Found a value string
                            q_start = k
                            m = k + 1
                            while m < len(rest):
                                if rest[m] == '\\' and m + 1 < len(rest):
                                    m += 2
                                elif rest[m] == '"':
                                    content = rest[q_start+1:m]
                                    if should_translate(content):
                                        old_part = rest[q_start:m+1]
                                        new_part = '__(' + '"' + content + '"' + ')'
                                        rest = rest[:q_start] + new_part + rest[m+1:]
                                        offset += len(new_part) - len(old_part)
                                    j = m + 1
                                    break
                                else:
                                    m += 1
                            else:
                                j = k + 1
                        else:
                            j += 1
                    # For list items: look for "..." at the start or after comma
                    elif rest[j] == '"' and (j == 0 or rest[j-1].isspace() or rest[j-1] == ','):
                        q_start = j
                        m = j + 1
                        while m < len(rest):
                            if rest[m] == '\\' and m + 1 < len(rest):
                                m += 2
                            elif rest[m] == '"':
                                content = rest[q_start+1:m]
                                if should_translate(content):
                                    old_part = rest[q_start:m+1]
                                    new_part = '__(' + '"' + content + '"' + ')'
                                    rest = rest[:q_start] + new_part + rest[m+1:]
                                    offset += len(new_part) - len(old_part)
                                j = m + 1
                                break
                            else:
                                m += 1
                        else:
                            j += 1
                    else:
                        j += 1
                
                if before:
                    new_line = before + rest
                else:
                    new_line = rest
            
            if new_line != original_line:
                changes.append((i, original_line.rstrip('\n'), new_line.rstrip('\n')))
            
            new_lines.append(new_line)
            
            # Check if we've closed the variable definition
            if bracket_depth <= 0:
                in_target = False
        else:
            new_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return changes


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'game/BKinit_variables.rpy')
    changes = process_file(filepath)
    
    print(f"Processed: {filepath}")
    print(f"Changes made: {len(changes)}")
    for line_num, old, new in changes[:30]:
        print(f"  Line {line_num}:")
        print(f"    - {old[:120]}")
        print(f"    + {new[:120]}")
    if len(changes) > 30:
        print(f"  ... and {len(changes) - 30} more changes")
