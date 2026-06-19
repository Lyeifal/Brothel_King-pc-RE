#!/usr/bin/env python3
"""
Wrap bare string literals in renpy.call_screen("yes_no", ...) and 
call_screen("yes_no", ...) calls with __() for translation.

Only wraps plain string literals; leaves existing __()/_() and 
non-string expressions alone.
"""

import re
from pathlib import Path

GAME_DIR = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc\game")

# Match call_screen("yes_no", "...") or call_screen("yes_no", '...')
# The string may contain escaped quotes.
PATTERN = re.compile(
    r'(renpy\.)?call_screen\s*\(\s*["\']yes_no["\']\s*,\s*'
    r'((?:["\'](?:[^"\'\\]|\\.)*["\'])|\+\s*)'
    r'(?=\s*\))',
    re.MULTILINE,
)

# More precise: match the literal part only, leave existing __() alone
PATTERN_LITERAL = re.compile(
    r'(?<![_\w])call_screen\s*\(\s*["\']yes_no["\']\s*,\s*'
    r'(?P<q>["\'])(?P<text>(?:[^"\'\\]|\\.)*)(?P=q)'
)

def wrap_file(fpath):
    content = fpath.read_text(encoding='utf-8')
    original = content
    
    def repl(m):
        q = m.group('q')
        text = m.group('text')
        # Skip if text is empty
        if not text:
            return m.group(0)
        # Skip if already wrapped by looking behind (simple check)
        prefix = content[:m.start()]
        # Check the 10 chars before match for __(_ or _(_
        if prefix[-10:].rstrip().endswith(('__(', '_(')):
            return m.group(0)
        return m.group(0).replace(
            f'{q}{text}{q}',
            f'__("{text.replace(chr(92), chr(92)+chr(92)).replace(chr(34), chr(92)+chr(34))}")'
        )
    
    new_content = PATTERN_LITERAL.sub(repl, content)
    if new_content != original:
        fpath.write_text(new_content, encoding='utf-8')
        return True
    return False


def main():
    changed = []
    for fpath in sorted(GAME_DIR.rglob('*.rpy')):
        if wrap_file(fpath):
            changed.append(str(fpath.relative_to(GAME_DIR)))
    
    print(f'Modified {len(changed)} files:')
    for p in changed:
        print(f'  {p}')


if __name__ == "__main__":
    main()
