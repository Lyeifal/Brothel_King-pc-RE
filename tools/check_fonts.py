import re
import pathlib

root = pathlib.Path('C:/Users/akxls/Documents/Code/BK/Brothel_King-pc/game')
all_refs = {}

for f in root.rglob('*.rpy'):
    text = f.read_text(encoding='utf-8')
    for match in re.finditer(r'font\s*=\s*"([^"]+)"', text):
        ref = match.group(1)
        all_refs.setdefault(ref, []).append(str(f))
    for match in re.finditer(r'text_font\s*"([^"]+)"', text):
        ref = match.group(1)
        all_refs.setdefault(ref, []).append(str(f))

for ref in sorted(all_refs.keys()):
    print(f'{ref}: {len(all_refs[ref])} refs')
