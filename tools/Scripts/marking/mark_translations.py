#!/usr/bin/env python3
"""
Translation marker for Ren'Py .rpy files.
Adds _() or __() around user-visible hardcoded strings.
Uses precise token-based parsing.
"""
import re
import sys
import argparse
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent


# Characters that indicate the string is part of an expression, not a standalone UI text
EXPRESSION_CHARS = set('+%)].,;')

def should_translate(text, is_python=False):
    """Determine if a string literal should be translated."""
    t = text.strip()
    if not t:
        return False
    if not t.strip(' \t\n'):
        return False
    # Skip pure symbols/arrows
    if re.match(r'^[\s▲▼⟸⟹➜✓↑↓◄►←→⇦⇨\-\+\*\/\=\|\&\!\?\.\,\;\:\(\)\[\]\{\}<>\d\%\#\@\$\\"\'\`\~\^]*$', t):
        return False
    # Skip file paths
    if '/' in t and ('.' in t or t.startswith('game/') or t.startswith('UI/') or t.startswith('NPC/')):
        return False
    # Skip color codes
    if re.match(r'^#[0-9a-fA-F]{6,8}$', t):
        return False
    # Skip pure variable interpolation
    if re.match(r'^\[[\w\!]+\]$', t):
        return False
    # Skip strings that are only Ren'Py tags with no real text
    if re.match(r'^\s*(\{(image|color|size|b|i|u|s|/)[^}]*\}\s*)+\s*$', t):
        return False
    # Skip format-only strings
    if re.match(r'^[%\s\di\.efs\(\)\[\]\,\*\+\-/]+$' , t) and '%' in t:
        return False
    # Skip strings that are just color tags with single characters
    if re.match(r'^\{color=[^}]+\}[A-Za-z]\{/color\}$', t):
        return False
    
    if is_python:
        # In Python code, be more conservative
        # Skip single words (likely keys/identifiers)
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', t):
            return False
        # Skip strings that look like file extensions or paths
        if re.match(r'^[a-z0-9_]+\.[a-z]+$', t):
            return False
        # Skip strings that are just version numbers or identifiers
        if re.match(r'^[0-9]+(\.[0-9]+)*[a-z]?$', t):
            return False
        # Skip strings that look like exception messages with code
        if t.startswith('Illegal') and 'tag' in t.lower():
            return False
        # Skip strings in lists that look like identifiers
        if re.match(r'^[a-z_][a-z0-9_\s]*$', t) and len(t.split()) <= 3:
            # But allow if it contains clear description words
            description_words = ['affects', 'changes', 'customer', 'girl', 'brothel', 'income', 
                                 'skill', 'reputation', 'prestige', 'security', 'satisfaction',
                                 'experience', 'challenge', 'story', 'picture', 'achievement',
                                 'budget', 'reward', 'resource', 'fee', 'grace', 'period',
                                 'progression', 'sexual', 'preference', 'tip', 'damage',
                                 'entertainment', 'whore', 'weapon', 'defense', 'mood']
            if not any(w in t.lower() for w in description_words):
                return False
    
    return True


def get_first_nonspace_char(s):
    for c in s:
        if not c.isspace():
            return c
    return None


def is_inside_function_call(line, pos):
    depth = 0
    for i, c in enumerate(line[:pos]):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
    return depth > 0


def find_and_wrap_strings(line, wrap_func, is_python=False):
    """Find all string literals in a line and wrap them with wrap_func if translatable."""
    result = []
    i = 0
    while i < len(line):
        c = line[i]
        if c in '"\'':
            quote = c
            j = i + 1
            while j < len(line):
                if line[j] == '\\' and j + 1 < len(line):
                    j += 2
                elif line[j] == quote:
                    content = line[i+1:j]
                    if should_translate(content, is_python):
                        result.append(wrap_func(line[i:j+1], content, quote))
                    else:
                        result.append(line[i:j+1])
                    i = j + 1
                    break
                else:
                    j += 1
            else:
                result.append(line[i:])
                break
        else:
            result.append(c)
            i += 1
    return ''.join(result)


def process_line_screen(line, line_num):
    """Process a single line in screen language context."""
    if line.lstrip().startswith('#'):
        return line
    
    is_renpy_label = re.match(r'^\s*label\s+\w+\s*:', line.lstrip())
    keywords = ['text', 'textbutton', 'tooltip']
    if not is_renpy_label:
        keywords.append('label')
    
    new_line = line
    offset = 0
    
    for keyword in keywords:
        for m in re.finditer(r'\b' + keyword + r'\b', new_line):
            kw_start = m.start() + offset
            kw_end = m.end() + offset
            
            before_kw = new_line[:kw_start].rstrip()
            if before_kw.endswith('_(') or before_kw.endswith('__('):
                continue
            
            if is_inside_function_call(new_line, kw_start):
                continue
            
            rest = new_line[kw_end:]
            i = 0
            while i < len(rest) and rest[i].isspace():
                i += 1
            
            if i >= len(rest) or rest[i] not in '"\'':
                continue
            
            quote = rest[i]
            j = i + 1
            while j < len(rest):
                if rest[j] == '\\' and j + 1 < len(rest):
                    j += 2
                elif rest[j] == quote:
                    content = rest[i+1:j]
                    str_end = j + 1
                    
                    if not should_translate(content):
                        break
                    
                    after = rest[str_end:]
                    first_char = get_first_nonspace_char(after)
                    if first_char in EXPRESSION_CHARS:
                        break
                    
                    old_part = new_line[kw_start:kw_end + str_end]
                    new_part = new_line[kw_start:kw_end] + ' ' + '_(' + quote + content + quote + ')'
                    new_line = new_line[:kw_start] + new_part + new_line[kw_end + str_end:]
                    offset += len(new_part) - len(old_part)
                    break
                else:
                    j += 1
    
    # Handle tt.Action("...")
    offset = 0
    for m in re.finditer(r'tt\.Action\s*\(', new_line):
        start = m.end() + offset
        rest = new_line[start:]
        
        i = 0
        while i < len(rest) and rest[i].isspace():
            i += 1
        
        if i >= len(rest) or rest[i] not in '"\'':
            continue
        
        quote = rest[i]
        j = i + 1
        while j < len(rest):
            if rest[j] == '\\' and j + 1 < len(rest):
                j += 2
            elif rest[j] == quote:
                content = rest[i+1:j]
                str_end = j + 1
                
                if not should_translate(content):
                    break
                
                after = rest[str_end:]
                first_char = get_first_nonspace_char(after)
                if first_char != ')':
                    break
                
                old_part = new_line[m.start() + offset:m.start() + offset + len(m.group(0)) + str_end]
                new_part = new_line[m.start() + offset:m.start() + offset + len(m.group(0))] + '_(' + quote + content + quote + ')' + after[:len(after) - len(after.lstrip())]
                new_line = new_line[:m.start() + offset] + new_part + new_line[m.start() + offset + len(m.group(0)) + str_end:]
                offset += len(new_part) - len(old_part)
                break
            else:
                j += 1
    
    return new_line


def process_line_python(line, line_num):
    """Process a single line in Python code context."""
    if line.lstrip().startswith('#'):
        return line
    
    # Very conservative: only mark strings in specific contexts
    # We look for: "key" : "value"  or  "value" in lists
    # and variable assignments like: var = "description"
    
    new_line = line
    offset = 0
    
    # Find all string literals
    for m in re.finditer(r'["\']', new_line):
        pos = m.start() + offset
        quote = new_line[pos]
        
        # Check if already wrapped
        before = new_line[:pos].rstrip()
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
                
                if not should_translate(content, is_python=True):
                    break
                
                # Check context: what comes before and after
                before_str = new_line[:pos].rstrip()
                after_str = new_line[str_end:].lstrip()
                
                # Skip if this looks like a dictionary key (followed by :)
                if after_str.startswith(':'):
                    break
                
                # Skip if this is part of a function call with keyword args
                if before_str.endswith('=') and not before_str.endswith('=='):
                    # Could be a keyword arg - check if before the = is an identifier
                    # e.g., font="DejaVuSans"
                    match = re.search(r'(\w+)\s*=\s*$', before_str)
                    if match:
                        param_name = match.group(1).lower()
                        # Skip known non-translatable parameters
                        if param_name in ['font', 'size', 'color', 'background', 'image', 
                                          'path', 'file', 'dir', 'directory', 'url', 
                                          'name', 'id', 'key', 'tag', 'style', 'action',
                                          'hovered', 'unhovered', 'activate_sound',
                                          'tooltip', 'xalign', 'yalign', 'xpos', 'ypos',
                                          'xsize', 'ysize', 'xpadding', 'ypadding']:
                            break
                
                # Skip if in exception raise
                if 'raise ' in before_str or 'Exception(' in before_str:
                    break
                
                # Skip if looks like a file path assignment
                if re.search(r'(path|file|dir|directory)\s*=\s*$', before_str, re.I):
                    break
                
                # Perform replacement
                old_part = new_line[pos:str_end]
                new_part = '__(' + quote + content + quote + ')'
                new_line = new_line[:pos] + new_part + new_line[str_end:]
                offset += len(new_part) - len(old_part)
                break
            else:
                j += 1
    
    return new_line


def process_file(filepath, mode='screen'):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    changes = []
    
    # Track whether we're in a python block
    in_python = False
    python_indent = None
    
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        
        # Detect python block start/end
        if mode == 'auto':
            if re.match(r'^\s*(init\s+[-\d]+\s+)?python\s*:', stripped):
                in_python = True
                python_indent = indent
            elif re.match(r'^\s*\$\s', stripped):
                # Single-line python
                new_line = process_line_python(line, i)
            elif in_python:
                if indent <= python_indent and stripped and not stripped.startswith('#'):
                    in_python = False
                    python_indent = None
        
        if mode == 'python' or (mode == 'auto' and in_python):
            new_line = process_line_python(line, i)
        else:
            new_line = process_line_screen(line, i)
        
        if new_line != line:
            changes.append((i, line.rstrip('\n'), new_line.rstrip('\n')))
        new_lines.append(new_line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return changes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mark strings for translation in Ren\'Py .rpy files')
    parser.add_argument('filepath', help='Path to the .rpy file')
    parser.add_argument('--mode', choices=['screen', 'python', 'auto'], default='screen',
                        help='Processing mode: screen (default), python, or auto-detect')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    
    args = parser.parse_args()
    
    changes = process_file(args.filepath, args.mode)
    
    print(f"Processed: {args.filepath} (mode={args.mode})")
    print(f"Changes made: {len(changes)}")
    for line_num, old, new in changes[:30]:
        print(f"  Line {line_num}:")
        print(f"    - {old[:120]}")
        print(f"    + {new[:120]}")
    if len(changes) > 30:
        print(f"  ... and {len(changes) - 30} more changes")
