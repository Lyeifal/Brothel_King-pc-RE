#!/usr/bin/env python3
"""
Translation marker for Ren'Py .rpy files.
Adds _() around user-visible hardcoded strings in UI screens.
Uses precise token-based parsing.
"""
import re
import sys

# Characters that indicate the string is part of an expression, not a standalone UI text
EXPRESSION_CHARS = set('+%)].,;')

def should_translate(text):
    """Determine if a string literal should be translated."""
    t = text.strip()
    if not t:
        return False
    if not t.strip(' \t\n'):
        return False
    if re.match(r'^[\s▲▼⟸⟹➜✓↑↓◄►←→⇦⇨\-\+\*\/\=\|\&\!\?\.\,\;\:\(\)\[\]\{\}<>\d\%\#\@\$\\"\'\`\~\^]*$', t):
        return False
    if '/' in t and ('.' in t or t.startswith('game/') or t.startswith('UI/') or t.startswith('NPC/')):
        return False
    if re.match(r'^#[0-9a-fA-F]{6,8}$', t):
        return False
    if re.match(r'^\[[\w\!]+\]$', t):
        return False
    if re.match(r'^\s*(\{(image|color|size|b|i|u|s|/)[^}]*\}\s*)+\s*$', t):
        return False
    if re.match(r'^[%\s\di\.efs\(\)\[\]\,\*\+\-/]+$' , t) and '%' in t:
        return False
    if re.match(r'^\{color=[^}]+\}[A-Za-z]\{/color\}$', t):
        return False
    return True


def get_first_nonspace_char(s):
    """Get first non-whitespace character of a string, or None."""
    for c in s:
        if not c.isspace():
            return c
    return None


def is_inside_function_call(line, pos):
    """Check if position is inside a function call (after '(' but before matching ')')."""
    # Simple heuristic: if there's an unmatched '(' before pos, we're inside a function call
    depth = 0
    for i, c in enumerate(line[:pos]):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
    return depth > 0


def process_line(line, line_num):
    """Process a single line, adding _() where appropriate."""
    
    # Skip comment lines
    stripped = line.lstrip()
    if stripped.startswith('#'):
        return line
    
    # Check for Ren'Py label statement (e.g., "label start:")
    is_renpy_label = re.match(r'^\s*label\s+\w+\s*:', stripped)
    
    keywords = ['text', 'textbutton', 'tooltip']
    if not is_renpy_label:
        keywords.append('label')
    
    new_line = line
    offset = 0
    
    for keyword in keywords:
        # Find all occurrences of keyword as a whole word
        for m in re.finditer(r'\b' + keyword + r'\b', new_line):
            kw_start = m.start() + offset
            kw_end = m.end() + offset
            
            # Check if already wrapped: look back for _( or __(
            before_kw = new_line[:kw_start].rstrip()
            if before_kw.endswith('_(') or before_kw.endswith('__('):
                continue
            
            # Skip if inside a function call (e.g., GetFocusRect("tooltip"))
            if is_inside_function_call(new_line, kw_start):
                continue
            
            # Find the next token after the keyword
            rest = new_line[kw_end:]
            
            # Skip whitespace
            i = 0
            while i < len(rest) and rest[i].isspace():
                i += 1
            
            if i >= len(rest):
                continue
            
            # Check if next token is a string literal
            quote = rest[i]
            if quote not in '"\'':
                continue
            
            # Parse string literal
            j = i + 1
            while j < len(rest):
                if rest[j] == '\\' and j + 1 < len(rest):
                    j += 2
                elif rest[j] == quote:
                    content = rest[i+1:j]
                    str_end = j + 1  # Position after closing quote
                    
                    if not should_translate(content):
                        break
                    
                    # Check what comes after the string
                    after = rest[str_end:]
                    first_char = get_first_nonspace_char(after)
                    
                    # If followed by expression operator, skip
                    if first_char in EXPRESSION_CHARS:
                        break
                    
                    # Perform replacement
                    old_part = new_line[kw_start:kw_end + str_end]
                    new_part = new_line[kw_start:kw_end] + ' ' + '_(' + quote + content + quote + ')'
                    
                    new_line = new_line[:kw_start] + new_part + new_line[kw_end + str_end:]
                    
                    # Update offset for subsequent replacements
                    offset += len(new_part) - len(old_part)
                    break
                else:
                    j += 1
    
    # Handle tt.Action("...")
    offset = 0
    for m in re.finditer(r'tt\.Action\s*\(', new_line):
        start = m.end() + offset
        rest = new_line[start:]
        
        # Skip whitespace
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
                
                # Check what comes after - should be ) for tt.Action()
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


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    changes = []
    for i, line in enumerate(lines, 1):
        new_line = process_line(line, i)
        if new_line != line:
            changes.append((i, line.rstrip('\n'), new_line.rstrip('\n')))
        new_lines.append(new_line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return changes


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <rpy_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    changes = process_file(filepath)
    
    print(f"Processed: {filepath}")
    print(f"Changes made: {len(changes)}")
    for line_num, old, new in changes[:30]:
        print(f"  Line {line_num}:")
        print(f"    - {old[:120]}")
        print(f"    + {new[:120]}")
    if len(changes) > 30:
        print(f"  ... and {len(changes) - 30} more changes")
