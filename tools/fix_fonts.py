import re
import pathlib

root = pathlib.Path('C:/Users/akxls/Documents/Code/BK/Brothel_King-pc/game')
files = list(root.rglob('*.rpy'))
changed = 0

for f in files:
    text = f.read_text(encoding='utf-8')
    new_text = re.sub(
        r'(?i)(?<!resources/fonts/)"vivaldii\.TTF"',
        '"resources/fonts/VIVALDII.TTF"',
        text
    )
    if new_text != text:
        f.write_text(new_text, encoding='utf-8')
        changed += 1
        print(f'Updated: {f.relative_to(root.parent)}')

print(f'Done. Changed {changed} files.')
