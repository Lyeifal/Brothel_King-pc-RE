import re
import pathlib

root = pathlib.Path('C:/Users/akxls/Documents/Code/BK/Brothel_King-pc/game')
font_files = [f.name for f in (root / 'resources/fonts').glob('*') if f.is_file()]
print('Fonts on disk:', font_files)

for f in root.rglob('*.rpy'):
    text = f.read_text(encoding='utf-8')
    for match in re.finditer(r'font\s*=\s*"([^"]+)"', text):
        ref = match.group(1)
        if not ref.startswith('resources/fonts/'):
            print(f'BARE font= : {ref} in {f}')
    for match in re.finditer(r'text_font\s*"([^"]+)"', text):
        ref = match.group(1)
        if not ref.startswith('resources/fonts/'):
            print(f'BARE text_font: {ref} in {f}')
