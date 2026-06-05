import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


filepath = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'game/BKdialogue.rpy')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
screens = len(re.findall(r'^\s*screen\s+\w+', content, re.M))
menus = len(re.findall(r'^\s*menu\s*:', content, re.M))
descs = len(re.findall(r'description\s*=\s*["\']', content))
print(f'screens: {screens}, menus: {menus}, descriptions: {descs}')
