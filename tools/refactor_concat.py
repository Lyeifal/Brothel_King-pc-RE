#!/usr/bin/env python3
"""
Semi-automated script to refactor __() string concatenations.
Handles simple patterns on a single line:
  __("text ") + expr + __(" more")  =>  __("text %s more") % expr
  __("text ") + expr                =>  __("text %s") % expr
  expr + __(" text")                =>  __("%s text") % expr

SAFETY RULES:
- Only processes lines where the resulting format string doesn't already contain '%'
  (unless it's part of an existing format like '%s')
- Only handles single-line concatenations
- Skips lines with nested __() calls in the expression part
- Skips lines where the expression contains '+' operators
- Creates .bak backups before modifying files
"""

import re
import sys
import shutil
import os

def find_matching_paren(s, start):
    """Find matching closing paren for an opening '(' at position start."""
    depth = 1
    in_str = None
    escape = False
    for i in range(start + 1, len(s)):
        c = s[i]
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if in_str:
            if c == in_str:
                in_str = None
            continue
        if c in ('"', "'"):
            in_str = c
            continue
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return i
    return -1


def extract_string_content(s):
    """Extract content from a quoted string literal (single/double quotes)."""
    s = s.strip()
    if (s.startswith('"""') and s.endswith('"""')) or (s.startswith("'''") and s.endswith("'''")):
        return s[3:-3]
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    return None


def split_by_plus(line):
    """
    Split a line by '+' operators, but only outside of strings and parentheses.
    Returns list of text parts.
    """
    parts = []
    i = 0
    current = ""
    in_str = None
    paren_depth = 0
    escape = False
    
    while i < len(line):
        c = line[i]
        
        if escape:
            current += c
            escape = False
            i += 1
            continue
        
        if c == '\\':
            current += c
            escape = True
            i += 1
            continue
        
        if in_str:
            current += c
            if c == in_str:
                in_str = None
            i += 1
            continue
        
        if c in ('"', "'"):
            current += c
            in_str = c
            i += 1
            continue
        
        if c == '(':
            paren_depth += 1
            current += c
            i += 1
            continue
        
        if c == ')':
            paren_depth -= 1
            current += c
            i += 1
            continue
        
        if c == '+' and paren_depth == 0:
            stripped = current.strip()
            if stripped:
                parts.append(stripped)
            current = ""
            i += 1
            continue
        
        current += c
        i += 1
    
    stripped = current.strip()
    if stripped:
        parts.append(stripped)
    
    return parts


def classify_part(part):
    """Classify a part as ('str', content), ('call', content), or ('expr', content)."""
    part = part.strip()
    if part.startswith('__(') and part.endswith(')'):
        inner = part[3:-1].strip()
        content = extract_string_content(inner)
        if content is not None:
            return ('str', content)
        return ('call', inner)
    # Check for plain string literal
    content = extract_string_content(part)
    if content is not None:
        return ('raw_str', content)
    return ('expr', part)


def is_safe_expr(expr):
    """Check if expression is safe to put in a % format (no +, no __() at top level)."""
    if '+' in expr:
        return False
    # Disallow nested __() calls
    if re.search(r'\b__\s*\(', expr):
        return False
    return True


def format_has_unsafe_percent(s):
    """Check if string already has % that isn't a safe format specifier."""
    # Remove safe format specifiers
    temp = re.sub(r'%\([a-zA-Z0-9_]+\)[sdifg]', '', s)
    temp = re.sub(r'%[sdifg%]', '', temp)
    temp = re.sub(r'%\{', '', temp)
    return '%' in temp


def try_refactor_line(line):
    """Try to refactor a single line. Returns new_line or None if no change."""
    original = line
    
    # Only process lines with __() and +
    if '__(' not in line or '+' not in line:
        return None
    
    # Skip comments
    stripped = line.strip()
    if stripped.startswith('#'):
        return None
    
    parts = split_by_plus(line)
    if len(parts) < 2:
        return None
    
    classified = [classify_part(p) for p in parts]
    
    # Pattern 1: str + expr + str  (sandwich)
    if len(classified) == 3:
        if classified[0][0] == 'str' and classified[1][0] == 'expr' and classified[2][0] == 'str':
            left_str = classified[0][1]
            expr = classified[1][1]
            right_str = classified[2][1]
            if not is_safe_expr(expr):
                return None
            new_str = left_str + "%s" + right_str
            if format_has_unsafe_percent(new_str):
                return None
            # Use double quotes for new string
            new_str_lit = '"' + new_str.replace('"', '\\"') + '"'
            pattern = re.escape(parts[0]) + r'\s*\+\s*' + re.escape(parts[1]) + r'\s*\+\s*' + re.escape(parts[2])
            replacement = '__(' + new_str_lit + ') % (' + expr + ')'
            new_line = re.sub(pattern, replacement, line, count=1)
            return new_line if new_line != line else None
    
    # Pattern 2: str + expr  (str at left)
    if len(classified) == 2:
        if classified[0][0] == 'str' and classified[1][0] == 'expr':
            left_str = classified[0][1]
            expr = classified[1][1]
            if not is_safe_expr(expr):
                return None
            new_str = left_str + "%s"
            if format_has_unsafe_percent(new_str):
                return None
            new_str_lit = '"' + new_str.replace('"', '\\"') + '"'
            pattern = re.escape(parts[0]) + r'\s*\+\s*' + re.escape(parts[1])
            replacement = '__(' + new_str_lit + ') % (' + expr + ')'
            new_line = re.sub(pattern, replacement, line, count=1)
            return new_line if new_line != line else None
        
        # Pattern 3: expr + str  (str at right)
        if classified[0][0] == 'expr' and classified[1][0] == 'str':
            expr = classified[0][1]
            right_str = classified[1][1]
            if not is_safe_expr(expr):
                return None
            new_str = "%s" + right_str
            if format_has_unsafe_percent(new_str):
                return None
            new_str_lit = '"' + new_str.replace('"', '\\"') + '"'
            pattern = re.escape(parts[0]) + r'\s*\+\s*' + re.escape(parts[1])
            replacement = '__(' + new_str_lit + ') % (' + expr + ')'
            new_line = re.sub(pattern, replacement, line, count=1)
            return new_line if new_line != line else None
    
    return None


def process_file(filepath, dry_run=True):
    """Process a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = []
    new_lines = []
    for i, line in enumerate(lines):
        new_line = try_refactor_line(line)
        if new_line and new_line != line:
            changes.append((i + 1, line.rstrip('\n'), new_line.rstrip('\n')))
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    if not changes:
        return 0
    
    if not dry_run:
        shutil.copy2(filepath, filepath + '.bak')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    return len(changes)


if __name__ == '__main__':
    files = [
        'game/BKscreens.rpy',
        'game/BKclasses.rpy',
        'game/BKfunctions.rpy',
        'game/BKsecurity.rpy',
        'game/BKinteractions.rpy',
        'game/BKendday.rpy',
        'game/BKevents.rpy',
        'game/BKscreen_home.rpy',
    ]
    
    dry = '--apply' not in sys.argv
    
    total = 0
    for f in files:
        if not os.path.exists(f):
            continue
        n = process_file(f, dry_run=dry)
        if n:
            print(f"{'[DRY-RUN]' if dry else '[APPLIED]'} {f}: {n} changes")
            total += n
    
    print(f"\nTotal: {total} changes")
    if dry and total > 0:
        print("Run with --apply to apply changes.")
