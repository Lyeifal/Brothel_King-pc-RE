"""Split game/core/framework/classes.rpy into focused modules.

Splits classes.rpy (init blocks) into:
  - picture.rpy        (init -4)   Picture, ProportionalScale
  - goal.rpy           (init -10)  Goal
  - core_entities.rpy  (init -2)   Game, Main, NPC, Calendar, Log
  - world.rpy          (init -2)   District, Population, Customer, Brothel, Location, Room, Moon
  - character.rpy      (init -2)   Stat, Trait, Perk, PerkArchetype, Effect, Sexact, ItemType, Personality, Fixation
  - interactions.rpy   (init -2)   Event, StoryEvent, Quest, GirlInteractionTopic, GirlInteraction, GirlRecentEvent
  - challenges.rpy     (init -2)   Spell, MC_challenge, Resource, Furniture, Loan, Mod
  - progression.rpy    (init -2)   Achievement, Contract, ContractTask, EnemyBrothel, NGPSetting, MetaUpgrade
"""

import re
from pathlib import Path

SRC = Path("game/core/framework/classes.rpy")
OUT_DIR = Path("game/core/framework")

# Read source
with open(SRC, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find init blocks
init_blocks = []
for i, line in enumerate(lines):
    m = re.match(r"^(init\s+-?\d+\s+python:)", line)
    if m:
        init_blocks.append((i, m.group(1)))

# Determine block boundaries
block_ranges = []
for idx, (start, header) in enumerate(init_blocks):
    if idx + 1 < len(init_blocks):
        end = init_blocks[idx + 1][0]
    else:
        end = len(lines)
    block_ranges.append((start, end, header))

print("Init blocks found:")
for start, end, header in block_ranges:
    print(f"  {header:20s}  lines {start+1:5d}-{end:5d}  ({end-start:5d} lines)")

# Find class boundaries within each block
def find_classes_in_block(block_lines, global_start):
    classes = []
    for i, line in enumerate(block_lines):
        m = re.match(r"^(\s*)class (\w+)", line)
        if m:
            classes.append((i + global_start, m.group(2), len(m.group(1))))
    return classes

all_classes = []
for start, end, header in block_ranges:
    block_classes = find_classes_in_block(lines[start:end], start)
    all_classes.extend([(cls_start, cls_name, indent, start, end, header) for cls_start, cls_name, indent in block_classes])

# Build class line ranges
class_ranges = []
for i, (cls_start, cls_name, indent, block_start, block_end, header) in enumerate(all_classes):
    if i + 1 < len(all_classes):
        next_start = all_classes[i + 1][0]
    else:
        next_start = block_end
    class_ranges.append((cls_name, cls_start, next_start, header, block_start, block_end))

print("\nClasses found:")
for name, s, e, h, bs, be in class_ranges:
    print(f"  {name:25s}  lines {s+1:5d}-{e:5d}  ({e-s:5d} lines)  in {h}")

# Define split groups
# Group names mapped to (output_file, init_header, [class_names])
groups = {
    "picture": (
        "picture.rpy",
        "init -4 python:",
        ["Picture", "ProportionalScale"],
    ),
    "goal": (
        "goal.rpy",
        "init -10 python:",
        ["Goal"],
    ),
    "core_entities": (
        "core_entities.rpy",
        "init -2 python:",
        ["Game", "Main", "NPC", "Calendar", "Log"],
    ),
    "world": (
        "world.rpy",
        "init -2 python:",
        ["District", "Population", "Customer", "Brothel", "Location", "Room", "Moon"],
    ),
    "character": (
        "character.rpy",
        "init -2 python:",
        ["Stat", "Trait", "Perk", "PerkArchetype", "Effect", "Sexact", "ItemType", "Personality", "Fixation"],
    ),
    "interactions": (
        "interactions.rpy",
        "init -2 python:",
        ["Event", "StoryEvent", "Quest", "GirlInteractionTopic", "GirlInteraction", "GirlRecentEvent"],
    ),
    "challenges": (
        "challenges.rpy",
        "init -2 python:",
        ["Spell", "MC_challenge", "Resource", "Furniture", "Loan", "Mod"],
    ),
    "progression": (
        "progression.rpy",
        "init -2 python:",
        ["Achievement", "Contract", "ContractTask", "EnemyBrothel", "NGPSetting", "MetaUpgrade"],
    ),
}

# Collect any comments/imports before the first class in each original init block
# We need to preserve imports that are used by the classes in the group
pre_class_content = {}  # block_start_line -> list of lines before first class
for start, end, header in block_ranges:
    # Find first class in this block
    first_class = None
    for cs, cn, ci, bs, be, h in all_classes:
        if bs == start:
            first_class = cs
            break
    if first_class is not None:
        pre_class_content[start] = lines[start:first_class]
    else:
        pre_class_content[start] = lines[start:end]

# Track which imports are needed by which groups
import_lines = {
    "import hashlib": "picture",  # hashlib used by Picture
    "import datetime": "core_entities",  # datetime used by Game
}

# Build output files
for group_name, (out_file, init_header, class_names) in groups.items():
    out_path = OUT_DIR / out_file
    
    # Header comment
    content = f"#### {group_name.replace('_', ' ').title()} classes ####\n\n"
    content += init_header + "\n"
    
    # Add imports if needed
    if group_name == "picture":
        content += "\n    import hashlib\n"
    elif group_name == "core_entities":
        content += "\n    import datetime\n"
    
    for name in class_names:
        # Find class range
        for cls_name, cls_start, cls_end, header, bs, be in class_ranges:
            if cls_name == name:
                class_lines = lines[cls_start:cls_end]
                # Ensure consistent 4-space indent (classes should already be indented)
                content += "".join(class_lines)
                break
        else:
            print(f"WARNING: Class {name} not found!")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written {out_path} ({len(content.splitlines())} lines)")

print("\nDone. Remember to delete the old classes.rpy after testing!")
