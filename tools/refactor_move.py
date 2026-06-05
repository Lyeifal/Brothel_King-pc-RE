#!/usr/bin/env python3
"""
Brothel King Phase 2 Refactor - File Move Script

Moves .rpy files and resource directories to the new structure,
updates hardcoded paths, and synchronizes translation file locations.

Usage:
    python tools/refactor_move.py [--dry-run]
"""

import shutil
import sys
from pathlib import Path

# Project root is two levels up from this script
ROOT = Path(__file__).parent.parent.resolve()
GAME = ROOT / "game"
TL_CN = GAME / "tl" / "chinese_simplified"
TL_EN = GAME / "tl" / "english"
TL_ZH = GAME / "tl" / "chinese"

DRY_RUN = "--dry-run" in sys.argv


def log(msg: str):
    print(msg)


def mkdir(p: Path):
    if DRY_RUN:
        log(f"[DRY-RUN] mkdir {p.relative_to(ROOT)}")
    else:
        p.mkdir(parents=True, exist_ok=True)


def move(src: Path, dst: Path):
    if not src.exists():
        log(f"[SKIP] Source not found: {src.relative_to(ROOT)}")
        return
    if dst.exists():
        log(f"[SKIP] Destination already exists: {dst.relative_to(ROOT)}")
        return
    mkdir(dst.parent)
    if DRY_RUN:
        log(f"[DRY-RUN] move {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    else:
        shutil.move(str(src), str(dst))
        log(f"[MOVED] {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


# ========================================================================
# 1. Code file moves: old_path (relative to game/) -> new_path (relative to game/)
# ========================================================================
CODE_MOVES = {
    # core/init/
    "BKinit_variables.rpy": "core/init/variables.rpy",
    "BKsettings.rpy": "core/init/settings.rpy",
    "BKdeclarations.rpy": "core/init/declarations.rpy",
    # core/framework/
    "BKfunctions.rpy": "core/framework/functions.rpy",
    "BKclasses.rpy": "core/framework/classes.rpy",
    "BKgirlclass.rpy": "core/framework/girlclass.rpy",
    # core/config/
    "options.rpy": "core/config/options.rpy",
    "gui.rpy": "core/config/gui.rpy",
    "screens.rpy": "core/config/screens.rpy",
    "translations.rpy": "core/config/translations.rpy",
    # systems/
    "BKitems.rpy": "systems/items.rpy",
    "BKtraits.rpy": "systems/traits.rpy",
    "BKperks.rpy": "systems/perks.rpy",
    "BKspells.rpy": "systems/spells.rpy",
    "BKpowers.rpy": "systems/powers.rpy",
    "BKfarm.rpy": "systems/farm.rpy",
    "BKsecurity.rpy": "systems/security.rpy",
    "BKachievements.rpy": "systems/achievements.rpy",
    "BKpostings.rpy": "systems/postings.rpy",
    "BKdist.rpy": "systems/dist.rpy",
    "BKminigame.rpy": "systems/minigame.rpy",
    "BKhelp.rpy": "systems/help.rpy",
    # ui/
    "BKscreens.rpy": "ui/screens.rpy",
    "BKscreen_home.rpy": "ui/screen_home.rpy",
    "BKmain.rpy": "ui/main.rpy",
    "BKcontent_menu.rpy": "ui/content_menu.rpy",
    "notify.rpy": "ui/notify.rpy",
    # gameplay/
    "BKstart.rpy": "gameplay/start.rpy",
    "BKintro.rpy": "gameplay/intro.rpy",
    "BKendday.rpy": "gameplay/endday.rpy",
    "BKevents.rpy": "gameplay/events_dispatcher.rpy",
    "BKdialogue.rpy": "gameplay/dialogue.rpy",
    "BKinteractions.rpy": "gameplay/interactions.rpy",
    "BKinteractions_free.rpy": "gameplay/interactions_free.rpy",
    # content/main_story/
    "BKchapter1.rpy": "content/main_story/chapter1/chapter1.rpy",
    "BKchapter2.rpy": "content/main_story/chapter2/chapter2.rpy",
    "BKchapter3.rpy": "content/main_story/chapter3/chapter3.rpy",
    # content/side_stories/
    "kite_jobgirl_variables.rpy": "content/side_stories/kite_jobgirl/variables.rpy",
    "kite_jobgirl 1_riddle.rpy": "content/side_stories/kite_jobgirl/riddle.rpy",
    "kite_jobgirl 2_beach.rpy": "content/side_stories/kite_jobgirl/beach.rpy",
    # content/other/
    "BKstory_events.rpy": "content/story_events/story_events.rpy",
    "BKcity_events.rpy": "content/city_events/city_events.rpy",
    "BKday_events.rpy": "content/day_events/day_events.rpy",
}

# ========================================================================
# 2. Resource directory moves: old_dir -> new_dir (relative to game/)
# ========================================================================
RESOURCE_MOVES = {
    "backgrounds": "resources/backgrounds",
    "brothels": "resources/brothels",
    "districts": "resources/districts",
    "events": "resources/events",
    "items": "resources/items",
    "perks": "resources/perks",
    "spells": "resources/spells",
    "MC": "resources/characters/mc",
    "NPC": "resources/characters/npc",
    "default": "resources/characters/default",
    "gui": "resources/gui",
    "UI": "resources/ui",
    "music": "resources/music",
    "sounds": "resources/sounds",
    "transitions": "resources/transitions",
}

# ========================================================================
# 3. Custom content moves
# ========================================================================
CUSTOM_MOVES = {
    "girls": "custom/girls",
    "Mods": "custom/mods",
}

# ========================================================================
# 4. Path replacements inside .rpy files
#    Format: (old_str, new_str)
# ========================================================================
PATH_REPLACEMENTS = [
    # girls/mods directories
    ('"girls/', '"custom/girls/'),
    ("'girls/", "'custom/girls/"),
    ('"Mods/', '"custom/mods/'),
    ("'Mods/", "'custom/mods/"),
    # characters
    ('"MC/', '"resources/characters/mc/'),
    ("'MC/", "'resources/characters/mc/"),
    ('"NPC/', '"resources/characters/npc/'),
    ("'NPC/", "'resources/characters/npc/"),
    ('"default/', '"resources/characters/default/'),
    ("'default/", "'resources/characters/default/"),
    # resources
    ('"backgrounds/', '"resources/backgrounds/'),
    ("'backgrounds/", "'resources/backgrounds/"),
    ('"brothels/', '"resources/brothels/'),
    ("'brothels/", "'resources/brothels/"),
    ('"districts/', '"resources/districts/'),
    ("'districts/", "'resources/districts/"),
    ('"events/', '"resources/events/'),
    ("'events/", "'resources/events/"),
    ('"items/', '"resources/items/'),
    ("'items/", "'resources/items/"),
    ('"perks/', '"resources/perks/'),
    ("'perks/", "'resources/perks/"),
    ('"spells/', '"resources/spells/'),
    ("'spells/", "'resources/spells/"),
    ('"gui/', '"resources/gui/'),
    ("'gui/", "'resources/gui/"),
    ('"UI/', '"resources/ui/'),
    ("'UI/", "'resources/ui/"),
    ('"music/', '"resources/music/'),
    ("'music/", "'resources/music/"),
    ('"sounds/', '"resources/sounds/'),
    ("'sounds/", "'resources/sounds/"),
    ('"transitions/', '"resources/transitions/'),
    ("'transitions/", "'resources/transitions/"),
    # config paths
    ('girl_directories = ["girls/", ]', 'girl_directories = ["custom/girls/", ]'),
    ("girl_directories = ['girls/', ]", "girl_directories = ['custom/girls/', ]"),
    # story girl paths (NPC subdirs)
    ('"NPC/Kunoichi/', '"resources/characters/npc/kunoichi/'),
    ("'NPC/Kunoichi/", "'resources/characters/npc/kunoichi/"),
    ('"NPC/Homura/', '"resources/characters/npc/homura/'),
    ("'NPC/Homura/", "'resources/characters/npc/homura/"),
]


def move_code_files():
    log("\n=== Moving code files ===")
    for old, new in CODE_MOVES.items():
        move(GAME / old, GAME / new)


def move_resource_dirs():
    log("\n=== Moving resource directories ===")
    for old, new in RESOURCE_MOVES.items():
        src = GAME / old
        dst = GAME / new
        if not src.exists():
            log(f"[SKIP] Source not found: {src.relative_to(ROOT)}")
            continue
        if dst.exists():
            log(f"[SKIP] Destination already exists: {dst.relative_to(ROOT)}")
            continue
        mkdir(dst.parent)
        if DRY_RUN:
            log(f"[DRY-RUN] move {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        else:
            shutil.move(str(src), str(dst))
            log(f"[MOVED] {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def move_custom_dirs():
    log("\n=== Moving custom content directories ===")
    for old, new in CUSTOM_MOVES.items():
        src = GAME / old
        dst = GAME / new
        if not src.exists():
            log(f"[SKIP] Source not found: {src.relative_to(ROOT)}")
            continue
        if dst.exists():
            log(f"[SKIP] Destination already exists: {dst.relative_to(ROOT)}")
            continue
        mkdir(dst.parent)
        if DRY_RUN:
            log(f"[DRY-RUN] move {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        else:
            shutil.move(str(src), str(dst))
            log(f"[MOVED] {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def move_translation_files():
    log("\n=== Moving translation files ===")
    for old, new in CODE_MOVES.items():
        # Chinese Simplified
        src_tl = TL_CN / old
        dst_tl = TL_CN / new
        if src_tl.exists():
            move(src_tl, dst_tl)
        # English (only strings.rpy usually)
        src_tl_en = TL_EN / old
        dst_tl_en = TL_EN / new
        if src_tl_en.exists():
            move(src_tl_en, dst_tl_en)
        # Chinese (old)
        src_tl_zh = TL_ZH / old
        dst_tl_zh = TL_ZH / new
        if src_tl_zh.exists():
            move(src_tl_zh, dst_tl_zh)


def replace_paths_in_file(filepath: Path):
    """Apply PATH_REPLACEMENTS to a single .rpy file."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        log(f"[ERROR] Cannot read {filepath}: {e}")
        return False

    original = text
    for old, new in PATH_REPLACEMENTS:
        text = text.replace(old, new)

    if text != original:
        if DRY_RUN:
            log(f"[DRY-RUN] update paths in {filepath.relative_to(ROOT)}")
        else:
            filepath.write_text(text, encoding="utf-8")
            log(f"[UPDATED] {filepath.relative_to(ROOT)}")
        return True
    return False


def update_hardcoded_paths():
    log("\n=== Updating hardcoded paths in .rpy files ===")
    updated = 0
    for rpy_file in sorted(GAME.rglob("*.rpy")):
        if replace_paths_in_file(rpy_file):
            updated += 1
    log(f"Updated {updated} files.")


def create_template_dirs():
    log("\n=== Creating template directories ===")
    templates = [
        GAME / "custom" / "templates" / "girl_template",
        GAME / "custom" / "templates" / "mod_template",
    ]
    for t in templates:
        mkdir(t)


def generate_report():
    log("\n=== Refactor Move Report ===")
    log(f"Dry run: {DRY_RUN}")
    log(f"Code files mapped: {len(CODE_MOVES)}")
    log(f"Resource dirs mapped: {len(RESOURCE_MOVES)}")
    log(f"Custom dirs mapped: {len(CUSTOM_MOVES)}")
    log(f"Path replacements defined: {len(PATH_REPLACEMENTS)}")
    log("\nDone.")


def main():
    if DRY_RUN:
        log("*** DRY RUN MODE - No files will be modified ***")

    move_code_files()
    move_translation_files()
    move_resource_dirs()
    move_custom_dirs()
    update_hardcoded_paths()
    create_template_dirs()
    generate_report()


if __name__ == "__main__":
    main()
