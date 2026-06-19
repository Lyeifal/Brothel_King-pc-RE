#!/usr/bin/env python3
from pathlib import Path

p = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc\game\core\ui\screens.rpy")
text = p.read_text(encoding='utf-8')

old = '                                                tooltip "Use this setting to change your customers\' preference for " + pref + " up to +" + str(50*brothel.get_effect("allow", pref + " preference")) + "%" + "."'
new = '                                                tooltip __("Use this setting to change your customers\' preference for ") + __(pref.capitalize()) + __(" up to +") + str(50*brothel.get_effect("allow", pref + " preference")) + "%" + __(".")'

if old in text:
    text = text.replace(old, new)
    p.write_text(text, encoding='utf-8')
    print("Replaced.")
else:
    print("Not found.")
