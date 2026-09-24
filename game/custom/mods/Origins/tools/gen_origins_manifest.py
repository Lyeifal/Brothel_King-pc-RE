# -*- coding: utf-8 -*-
"""Generate tl_manifest.rpy for the Origins mod from data/origins.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.load(open(str(ROOT / "data" / "origins.json"), encoding="utf-8"))

lines = []
seen = set()


def add(s):
    if s and s not in seen:
        seen.add(s)
        esc = s.replace("\\", "\\\\").replace('"', '\\"')
        lines.append('    __("%s")' % esc)


for o in data:
    add(o.get("name_i18n"))
    add(o.get("description_i18n"))
    cd = o.get("class_def", {})
    add(cd.get("name_i18n"))
    add(cd.get("description_i18n"))
    for s in cd.get("spellbook", []):
        add(s.get("name_i18n"))
        add(s.get("description_i18n"))
    for t in o.get("talents", []):
        add(t.get("name_i18n"))
        add(t.get("description_i18n"))

header = '''################################################################################
##  Origins Mod — Translation Manifest
##  EN: Static string manifest for the data-driven origins.json content.
##      The translation extractor only sees LITERAL __() calls, so every
##      name/description in data/origins.json is listed here to enter the
##      translate pipeline. Keep in sync when editing the JSON (or rerun
##      tools/gen_origins_manifest.py).
##  ZH: \u6570\u636e\u9a71\u52a8\u5185\u5bb9\uff08origins.json\uff09\u7684\u9759\u6001\u5b57\u7b26\u4e32\u6e05\u5355\u3002\u7ffb\u8bd1\u63d0\u53d6\u5668\u53ea\u80fd
##      \u8bc6\u522b\u5b57\u9762\u91cf __() \u8c03\u7528\uff0c\u56e0\u6b64 JSON \u4e2d\u7684\u6bcf\u6761\u540d\u79f0/\u63cf\u8ff0\u90fd\u5728\u6b64\u5217\u51fa\u4ee5
##      \u8fdb\u5165\u7ffb\u8bd1\u7ba1\u7ebf\u3002\u7f16\u8f91 JSON \u65f6\u8bf7\u540c\u6b65\u7ef4\u62a4\u672c\u6587\u4ef6\uff08\u6216\u91cd\u8dd1
##      tools/gen_origins_manifest.py\uff09\u3002
################################################################################

init python:
'''

out = ROOT / "tl_manifest.rpy"
out.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
print("manifest strings:", len(lines))
