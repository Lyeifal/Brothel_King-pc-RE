import re
import pathlib

root = pathlib.Path('C:/Users/akxls/Documents/Code/BK/Brothel_King-pc/game')
files = [
    root / 'core/config/gui.rpy',
    root / 'core/config/screens.rpy',
    root / 'core/init/declarations.rpy',
    root / 'core/ui/screens.rpy',
]

changed = 0
for f in files:
    text = f.read_text(encoding='utf-8')
    # Replace both "gui/ and "GUI/ with "resources/gui/ and "resources/GUI/
    new_text = re.sub(r'"gui/', '"resources/gui/', text)
    new_text = re.sub(r'"GUI/', '"resources/GUI/', new_text)
    if new_text != text:
        count = text.count('"gui/') + text.count('"GUI/')
        print(f'Updated {f.relative_to(root.parent)}: {count} replacements')
        f.write_text(new_text, encoding='utf-8')
        changed += 1

print(f'Done. Changed {changed} files.')
