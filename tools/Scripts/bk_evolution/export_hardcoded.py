#!/usr/bin/env python3
"""
EN: Export hardcoded Trait/Perk definitions from .rpy files to JSON.
    This is a one-time migration tool for BK Evolution.
ZH: 将 .rpy 文件中的硬编码特质/天赋定义导出为 JSON。
    这是 BK Evolution 的一次性迁移工具。

Usage: python tools/Scripts/bk_evolution/export_hardcoded.py
Output:
  - game/core/data/traits/traits.json
  - game/core/data/perks/perks.json
"""

import json
import os
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Stub classes for safe eval() — mirroring the in-game class signatures
# ---------------------------------------------------------------------------

class Effect:
    def __init__(self, type, target=None, value=0, chance=1.0, scales_with=None, scope=None, dice=False, change_cap=True, duration=-1, source=None):
        self.type = type
        self.target = target
        self.value = value
        self.chance = chance
        self.scales_with = scales_with
        self.scope = scope
        self.dice = dice
        self.change_cap = change_cap
        self.duration = duration
        self.source = source

    def to_dict(self):
        d = {
            "type": self.type,
            "target": self.target,
            "value": self.value,
            "chance": self.chance,
            "scales_with": self.scales_with,
            "scope": self.scope,
            "dice": self.dice,
            "change_cap": self.change_cap,
            "duration": self.duration,
            "source": self.source,
        }
        # Remove None / default values to keep JSON clean
        return {k: v for k, v in d.items() if v not in (None, False, 1.0, -1, True) or k in ("type",)}


class Trait:
    def __init__(self, name, verb="be", eff1=None, eff2=None, eff3=None, effects=None, opposite=None, archetype=None, base_description="", public=True):
        self.name = name
        self.verb = verb
        self.effects = []
        if effects:
            self.effects.extend(make_list(effects))
        for eff in (eff1, eff2, eff3):
            if eff:
                self.effects.append(eff)
        self.opposite = opposite if opposite else None
        self.archetype = archetype
        self.base_description = base_description
        self.public = public

    def to_dict(self):
        d = {
            "name": self.name,
            "verb": self.verb,
            "effects": [e.to_dict() for e in self.effects],
            "opposite": self.opposite,
            "archetype": self.archetype,
            "base_description": self.base_description,
            "public": self.public,
        }
        return {k: v for k, v in d.items() if v not in (None, "", True) or k in ("name",)}


class Perk:
    def __init__(self, name, type, effects, archetype=None, pic=None, perk_level=0, min_rank=0, base_description=""):
        self.name = name
        self.type = type
        self.effects = make_list(effects)
        self.archetype = archetype
        self.pic = pic
        self.level = perk_level
        self.min_rank = min_rank
        self.base_description = base_description

    def to_dict(self):
        d = {
            "name": self.name,
            "type": self.type,
            "effects": [e.to_dict() for e in self.effects],
            "archetype": self.archetype,
            "pic": self.pic,
            "perk_level": self.level,
            "min_rank": self.min_rank,
            "base_description": self.base_description,
        }
        return {k: v for k, v in d.items() if v not in (None, "", 0) or k in ("name", "type")}


def make_list(obj, cls=Effect):
    if isinstance(obj, list):
        return obj
    return [obj]


# Eval environment — must include all referenced free variables
_EVAL_ENV = {
    "Effect": Effect,
    "Trait": Trait,
    "Perk": Perk,
    "make_list": make_list,
    "bis_chance": 0.5,
    "group_chance": 0.5,
}


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def extract_calls(text, prefix):
    """
    EN: Extract all calls like 'Prefix(...)' from text, handling nested parens.
    ZH: 从文本中提取所有 'Prefix(...)' 调用，处理嵌套括号。
    """
    results = []
    i = 0
    while True:
        idx = text.find(prefix + "(", i)
        if idx == -1:
            break
        start = idx + len(prefix) + 1  # after '('
        depth = 1
        j = start
        while j < len(text) and depth > 0:
            if text[j] == '(':
                depth += 1
            elif text[j] == ')':
                depth -= 1
            j += 1
        # j is now one past the matching ')'
        inner = text[start:j - 1]
        results.append(inner)
        i = j
    return results


def parse_trait_or_perk(text, cls_name):
    """
    EN: Safely eval a Trait/Perk call argument string.
    ZH: 安全地 eval Trait/Perk 调用的参数字符串。
    """
    # Handle dict key syntax: "Key" : Trait(...)
    # We only want the inner part after the colon
    if ":" in text and not text.strip().startswith("name="):
        # It's likely a dict entry like "Name" : Trait(...)
        # Find the first unquoted colon
        colon_idx = text.index(":")
        text = text[colon_idx + 1:].strip()
    
    # If text starts with Trait( or Perk(, skip the wrapper
    for prefix in ("Trait(", "Perk("):
        if text.startswith(prefix):
            text = text[len(prefix):]
            if text.endswith(")"):
                text = text[:-1]
            break

    # Build eval expression
    expr = f"{cls_name}({text})"
    try:
        obj = eval(expr, {"__builtins__": {}}, _EVAL_ENV)
        return obj
    except Exception as e:
        print(f"  [WARN] Failed to parse: {expr[:120]}... -> {e}")
        return None


def parse_file(filepath, cls_name, cls_prefix):
    """
    EN: Parse all Trait or Perk definitions from a .rpy file.
    ZH: 从 .rpy 文件中解析所有 Trait 或 Perk 定义。
    """
    text = Path(filepath).read_text(encoding="utf-8")
    # Remove comments to simplify parsing
    text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)
    
    calls = extract_calls(text, cls_prefix)
    objects = []
    for call_text in calls:
        obj = parse_trait_or_perk(call_text, cls_name)
        if obj:
            objects.append(obj)
    return objects


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = Path(__file__).parent.parent.parent.parent
    data_dir = root / "game" / "custom" / "data"
    
    print("=" * 60)
    print("BK Evolution — Hardcoded Data Exporter")
    print("=" * 60)

    # --- Export Traits ---
    print("\n[1/2] Exporting Traits from game/core/systems/traits.rpy ...")
    trait_objs = parse_file(root / "game" / "core" / "systems" / "traits.rpy", "Trait", "Trait")
    print(f"       Found {len(trait_objs)} Trait definitions")
    
    traits_data = []
    seen_names = set()
    for t in trait_objs:
        if t.name in seen_names:
            print(f"       [SKIP] Duplicate: {t.name}")
            continue
        seen_names.add(t.name)
        d = t.to_dict()
        # Infer category from the original .rpy file (gold/pos/neg)
        # For now, we leave it out — the DataLoader will categorize by effects
        traits_data.append(d)
    
    traits_file = data_dir / "traits" / "traits.json"
    traits_file.parent.mkdir(parents=True, exist_ok=True)
    with open(traits_file, "w", encoding="utf-8") as f:
        json.dump(traits_data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"       Saved {len(traits_data)} traits -> {traits_file}")

    # --- Export Perks ---
    print("\n[2/2] Exporting Perks from game/core/data/perks.rpy ...")
    perk_objs = parse_file(root / "game" / "core" / "data" / "perks.rpy", "Perk", "Perk")
    print(f"       Found {len(perk_objs)} Perk definitions")
    
    perks_data = []
    seen_names = set()
    for p in perk_objs:
        if p.name in seen_names:
            print(f"       [SKIP] Duplicate: {p.name}")
            continue
        seen_names.add(p.name)
        perks_data.append(p.to_dict())
    
    perks_file = data_dir / "perks" / "perks.json"
    perks_file.parent.mkdir(parents=True, exist_ok=True)
    with open(perks_file, "w", encoding="utf-8") as f:
        json.dump(perks_data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"       Saved {len(perks_data)} perks -> {perks_file}")

    print("\n" + "=" * 60)
    print("Export complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
