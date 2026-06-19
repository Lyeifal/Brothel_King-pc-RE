#!/usr/bin/env python3
"""
Export hardcoded Achievements, Difficulty, and NG+ settings to JSON.
Run from project root: python tools/export_meta_data.py
"""

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT / "game"
DATA_DIR = GAME / "custom" / "data"


def _eval_node(node):
    """Evaluate an AST node safely for the values we expect (range, list comps)."""
    code = ast.unparse(node)
    # Restrict to safe builtins
    safe_globals = {"__builtins__": {}}
    safe_locals = {"range": range, "list": list, "tuple": tuple, "len": len}
    return eval(code, safe_globals, safe_locals)


def parse_call_args(args_text):
    """Parse positional and keyword args from an Achievement/NGPSetting call."""
    code = "f(" + args_text + ")"
    tree = ast.parse(code)
    call = tree.body[0].value

    def convert(node):
        try:
            return ast.literal_eval(node)
        except ValueError:
            return _eval_node(node)

    args = [convert(a) for a in call.args]
    kwargs = {kw.arg: convert(kw.value) for kw in call.keywords}
    return args, kwargs


def parse_nested_calls(text, class_name):
    """Find all ClassName(...) calls in text, handling nested parens."""
    items = []
    i = 0
    while True:
        idx = text.find(class_name + "(", i)
        if idx == -1:
            break
        start = idx + len(class_name) + 1
        depth = 1
        j = start
        while j < len(text) and depth > 0:
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
            j += 1
        args_text = text[start : j - 1]
        items.append(args_text)
        i = j
    return items


def export_achievements():
    path = GAME / "core" / "systems" / "achievements.rpy"
    text = path.read_text(encoding="utf-8")

    m = re.search(r"achievement_list\s*=\s*\[(.*?)\n\s*\]", text, re.DOTALL)
    if not m:
        raise RuntimeError("achievement_list not found")

    list_text = m.group(1)
    # Replace runtime expression with its literal value
    list_text = list_text.replace("license_dict[1][1]", '"license1.webp"')

    data = {}
    for args_text in parse_nested_calls(list_text, "Achievement"):
        args, kwargs = parse_call_args(args_text)
        # Achievement signature:
        # (title, description, pic=..., pic_path=..., level_nb=1, target="",
        #  requirements="default", requirements2=None, custom_titles=None, multi=1)
        entry = {}
        entry["title"] = args[0] if len(args) > 0 else kwargs.get("title", "")
        entry["description"] = args[1] if len(args) > 1 else kwargs.get("description", "")
        entry["pic"] = kwargs.get("pic", "misc.webp")
        entry["pic_path"] = kwargs.get("pic_path", "resources/ui/achievements/")
        entry["level_nb"] = kwargs.get("level_nb", 1)
        entry["target"] = kwargs.get("target", "")
        entry["requirements"] = kwargs.get("requirements", "default")
        entry["requirements2"] = kwargs.get("requirements2", None)
        entry["custom_titles"] = kwargs.get("custom_titles", None)
        entry["multi"] = kwargs.get("multi", 1)

        target = entry["target"]
        if not target:
            continue
        # Convert requirements default marker to real dict for JSON
        if entry["requirements"] == "default":
            entry["requirements"] = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

        data[target] = entry

    out = DATA_DIR / "achievements" / "achievements.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported {len(data)} achievements to {out}")


def export_difficulty():
    path = GAME / "core" / "init" / "variables.rpy"
    text = path.read_text(encoding="utf-8")

    # diff_list
    m = re.search(r'diff_list\s*=\s*(\[.*?\])', text, re.DOTALL)
    diff_list = ast.literal_eval(m.group(1)) if m else []

    # diff_settings_range
    m = re.search(r'diff_settings_range\s*=\s*(\{.*?\})\n\n', text, re.DOTALL)
    # Need careful parsing because diff_dict follows. Use regex to extract balanced braces.
    # Re-do with a more robust approach
    m = re.search(r'diff_settings_range\s*=\s*\{', text)
    start = m.end() - 1
    depth = 1
    i = start + 1
    while i < len(text) and depth > 0:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    diff_settings_range = ast.literal_eval(text[start:i])

    # diff_dict
    m = re.search(r'diff_dict\s*=\s*\{', text)
    start = m.end() - 1
    depth = 1
    i = start + 1
    while i < len(text) and depth > 0:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    diff_dict = ast.literal_eval(text[start:i])

    data = {
        "diff_list": diff_list,
        "diff_settings_range": diff_settings_range,
        "diff_dict": diff_dict,
    }

    out = DATA_DIR / "difficulty" / "difficulty.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported difficulty settings to {out}")


def export_ngp():
    path = GAME / "core" / "gameplay" / "start.rpy"
    text = path.read_text(encoding="utf-8")

    m = re.search(r"\$ NGP_settings\s*=\s*\[(.*?)\n\s*\]", text, re.DOTALL)
    if not m:
        raise RuntimeError("NGP_settings not found")

    list_text = m.group(1)
    data = []
    category_map = {
        "resources": ["starting chapter", "starting gold", "starting resources", "extractors Mk I", "extractors Mk II"],
        "girls": ["farm", "carpenter", "minion merchants", "item merchants", "all trainers", "girl"],
        "MC": ["strength", "spirit", "charisma", "speed", "good alignment", "evil alignment"],
    }

    for args_text in parse_nested_calls(list_text, "NGPSetting"):
        args, kwargs = parse_call_args(args_text)
        entry = {}
        entry["name"] = args[0] if len(args) > 0 else kwargs.get("name", "")
        entry["type"] = args[1] if len(args) > 1 else kwargs.get("type", "")
        entry["label"] = kwargs.get("label", entry["name"].capitalize())
        entry["values"] = kwargs.get("values", None)
        entry["cost"] = kwargs.get("cost", 0)
        entry["ttip"] = kwargs.get("ttip", "")

        # Determine category
        cat = "misc"
        for c, names in category_map.items():
            if entry["name"] in names:
                cat = c
                break
        entry["category"] = cat

        # Convert range to list for JSON serialisation
        if isinstance(entry["values"], range):
            entry["values"] = list(entry["values"])

        data.append(entry)

    out = DATA_DIR / "ngp" / "ngp_settings.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported {len(data)} NG+ settings to {out}")


def export_meta_template():
    """Create a starter meta-progression JSON template."""
    data = {
        "meta_upgrades": [
            {
                "id": "crystal_cap",
                "name_i18n_key": "Crystal Cap",
                "description_i18n_key": "Increase maximum crystals carried across runs by 50.",
                "max_rank": 5,
                "cost_per_rank": [10, 25, 50, 100, 200],
                "effects": [{"type": "change", "target": "crystal cap", "value": 50}],
                "unlock_condition": "newgame+"
            },
            {
                "id": "starting_crystals",
                "name_i18n_key": "Starting Crystals",
                "description_i18n_key": "Begin each New Game+ with extra crystals.",
                "max_rank": 3,
                "cost_per_rank": [20, 50, 100],
                "effects": [{"type": "change", "target": "starting crystals", "value": 10}],
                "unlock_condition": "newgame+"
            }
        ]
    }
    out = DATA_DIR / "meta" / "meta_progression.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported meta-progression template to {out}")


if __name__ == "__main__":
    export_achievements()
    export_difficulty()
    export_ngp()
    export_meta_template()
