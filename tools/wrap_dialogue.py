#!/usr/bin/env python3
"""
Wrap all string literals in add_dialogue() calls with __() in BKdialogue.rpy.

This script processes game/BKdialogue.rpy line by line. For each add_dialogue() call,
it wraps every string literal in the 3rd argument (the 'lines' parameter) with __().

Example transformations:
  add_dialogue("topic", "key", "Hello") 
    → add_dialogue("topic", "key", __("Hello"))
  
  add_dialogue("topic", "key", ("A", "B"))
    → add_dialogue("topic", "key", (__("A"), __("B")))
  
  add_dialogue("topic", "key", ["g: A", "mc: B"], multiple=True)
    → add_dialogue("topic", "key", [__("g: A"), __("mc: B")], multiple=True)
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUT_FILE = ROOT / "game/BKdialogue.rpy"
BACKUP_FILE = ROOT / "game/BKdialogue.rpy.phase2backup"


def wrap_strings_in_expr(expr: str) -> str:
    """
    Wrap every string literal in expr with __().
    
    Handles single-quoted and double-quoted strings, respecting escapes.
    Does NOT handle triple-quoted strings (confirmed none exist in add_dialogue calls).
    """
    result = []
    i = 0
    n = len(expr)
    
    while i < n:
        c = expr[i]
        
        if c in ('"', "'"):
            quote = c
            j = i + 1
            while j < n:
                if expr[j] == '\\':
                    j += 2
                    continue
                if expr[j] == quote:
                    break
                j += 1
            else:
                # Unterminated string - shouldn't happen in valid source
                result.append(expr[i:])
                break
            
            # expr[i:j+1] is the full string literal including quotes
            string_lit = expr[i:j+1]
            result.append(f'__({string_lit})')
            i = j + 1
        else:
            result.append(c)
            i += 1
    
    return ''.join(result)


def process_line(line: str) -> str:
    """Process a single line, wrapping strings in add_dialogue() calls."""
    stripped = line.lstrip()
    if not stripped.startswith('add_dialogue('):
        return line
    
    # Find the matching closing parenthesis for add_dialogue(
    start_idx = line.index('add_dialogue(')
    paren_idx = start_idx + len('add_dialogue(')
    
    # Walk to find the closing paren at depth 0
    depth = 1
    in_string = None
    escape = False
    end_idx = paren_idx
    
    while end_idx < len(line) and depth > 0:
        ch = line[end_idx]
        
        if escape:
            escape = False
            end_idx += 1
            continue
        
        if ch == '\\':
            escape = True
            end_idx += 1
            continue
        
        if in_string:
            if ch == in_string:
                in_string = None
            end_idx += 1
            continue
        
        if ch in ('"', "'"):
            in_string = ch
            end_idx += 1
            continue
        
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        
        end_idx += 1
    
    if depth != 0:
        # Malformed - shouldn't happen
        return line
    
    # The call spans line[start_idx:end_idx]
    call_content = line[start_idx:end_idx]  # e.g. add_dialogue("a", "b", "c", d=1)
    prefix = line[:start_idx]
    suffix = line[end_idx:]
    
    # Extract arguments string (between first ( and last ))
    args_start = len('add_dialogue(')
    args_str = call_content[args_start:-1]  # remove trailing )
    
    # Parse arguments: find comma positions at depth 0
    args = []
    arg_start = 0
    depth = 0
    in_string = None
    escape = False
    
    for idx, ch in enumerate(args_str):
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if in_string:
            if ch == in_string:
                in_string = None
            continue
        if ch in ('"', "'"):
            in_string = ch
            continue
        if ch in '([{':
            depth += 1
            continue
        if ch in ')]}':
            depth -= 1
            continue
        if ch == ',' and depth == 0:
            args.append(args_str[arg_start:idx])
            arg_start = idx + 1
    
    args.append(args_str[arg_start:])
    
    if len(args) < 3:
        return line
    
    # Wrap strings in the 3rd argument (index 2)
    args[2] = wrap_strings_in_expr(args[2])
    
    new_call = 'add_dialogue(' + ','.join(args) + ')'
    return prefix + new_call + suffix


def main():
    shutil.copy2(INPUT_FILE, BACKUP_FILE)
    print(f"Backup created: {BACKUP_FILE}")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = 0
    new_lines = []
    
    for line in lines:
        new_line = process_line(line)
        if new_line != line:
            modified += 1
        new_lines.append(new_line)
    
    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Modified {modified} lines in {INPUT_FILE}")
    
    # Quick sanity check: verify every add_dialogue line has __() in the 3rd arg
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    import re
    total_calls = 0
    wrapped_calls = 0
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('add_dialogue('):
            total_calls += 1
            if '__(' in line:
                wrapped_calls += 1
            else:
                print(f"WARNING: Line {i} has no __(): {line.strip()[:120]}")
    
    print(f"Total add_dialogue calls: {total_calls}")
    print(f"Calls with __(): {wrapped_calls}")
    
    if total_calls != wrapped_calls:
        print("ERROR: Not all calls were wrapped! Restoring backup...")
        shutil.copy2(BACKUP_FILE, INPUT_FILE)
        sys.exit(1)
    
    print("SUCCESS: All add_dialogue() calls now have wrapped strings.")


if __name__ == '__main__':
    main()
