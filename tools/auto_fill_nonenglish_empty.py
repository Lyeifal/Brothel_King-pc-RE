#!/usr/bin/env python3
"""
Auto-fill empty translations where the source (old) text is already non-English
(typically Chinese hardcoded in source). This avoids requiring translators to
fill entries that don't need translation.
"""

import re
from pathlib import Path

TL_DIR = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc\game\tl\chinese_simplified")

def parse_quoted_string(s):
    s = s.strip()
    if s.startswith('"""') and s.endswith('"""'):
        return s[3:-3]
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
    return s

def format_quoted_string(text):
    if '\n' in text or '\r' in text:
        safe = text.replace('"""', '\\"""')
        return f'"""{safe}"""'
    else:
        safe = text.replace('"', '\\"').replace('\\', '\\\\')
        return f'"{safe}"'

chinese_re = re.compile(r'[\u4e00-\u9fff]')

filled = 0
english_empty = 0

for fpath in sorted(TL_DIR.rglob('*.rpy')):
    content = fpath.read_text(encoding='utf-8')
    original = content
    
    pattern = re.compile(
        r'(#\s*[^\n]*\n\s*old\s+)("(?:[^"\\]|\\.)*"|"""[\s\S]*?""")(\s*\n\s*new\s+)""(\s*\n)',
        re.MULTILINE
    )
    
    def repl(m, counters={'filled': 0, 'english_empty': 0}):
        old_val = m.group(2)
        old_text = parse_quoted_string(old_val)
        
        if not old_text or chinese_re.search(old_text):
            # Non-English or empty source: fill with source text
            counters['filled'] += 1
            return m.group(1) + old_val + m.group(3) + format_quoted_string(old_text) + m.group(4)
        else:
            counters['english_empty'] += 1
            return m.group(0)
    
    new_content = pattern.sub(repl, content)
    filled += repl.__defaults__[0]['filled']
    english_empty += repl.__defaults__[0]['english_empty']
    if new_content != original:
        fpath.write_text(new_content, encoding='utf-8')

print(f'Auto-filled non-English empty entries: {filled}')
print(f'Remaining English empty entries: {english_empty}')
