#!/usr/bin/env python3
"""
Brothel King Phase 2 Refactor - Verification Script

Scans the game/ directory for:
1. Any remaining hardcoded old paths that should have been updated
2. Directory structure compliance with the new layout
3. Missing or orphaned translation files

Usage:
    python tools/refactor_verify.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
GAME = ROOT / "game"

# Patterns that indicate an OLD path still present in code
OLD_PATH_PATTERNS = [
    '"girls/',
    "'girls/",
    '"Mods/',
    "'Mods/",
    '"MC/',
    "'MC/",
    '"NPC/',
    "'NPC/",
    '"default/',
    "'default/",
    '"backgrounds/',
    "'backgrounds/",
    '"brothels/',
    "'brothels/",
    '"districts/',
    "'districts/",
    '"events/',
    "'events/",
    '"items/',
    "'items/",
    '"perks/',
    "'perks/",
    '"spells/',
    "'spells/",
    '"UI/',
    "'UI/",
    '"music/',
    "'music/",
    '"sounds/',
    "'sounds/",
    '"transitions/',
    "'transitions/",
    'girl_directories = ["girls/"]',
    "girl_directories = ['girls/']",
]

# Expected new directories (should exist after refactor)
EXPECTED_DIRS = [
    GAME / "core" / "init",
    GAME / "core" / "framework",
    GAME / "core" / "config",
    GAME / "systems",
    GAME / "ui",
    GAME / "gameplay",
    GAME / "content" / "main_story",
    GAME / "content" / "side_stories",
    GAME / "content" / "story_events",
    GAME / "content" / "city_events",
    GAME / "content" / "day_events",
    GAME / "resources",
    GAME / "custom" / "girls",
    GAME / "custom" / "mods",
]

# Files that should NO LONGER exist in game/ root
FORBIDDEN_ROOT_FILES = [
    "BKinit_variables.rpy",
    "BKsettings.rpy",
    "BKdeclarations.rpy",
    "BKfunctions.rpy",
    "BKclasses.rpy",
    "BKgirlclass.rpy",
    "BKitems.rpy",
    "BKtraits.rpy",
    "BKperks.rpy",
    "BKspells.rpy",
    "BKpowers.rpy",
    "BKfarm.rpy",
    "BKsecurity.rpy",
    "BKachievements.rpy",
    "BKpostings.rpy",
    "BKdist.rpy",
    "BKminigame.rpy",
    "BKhelp.rpy",
    "BKscreens.rpy",
    "BKscreen_home.rpy",
    "BKmain.rpy",
    "BKcontent_menu.rpy",
    "BKstart.rpy",
    "BKintro.rpy",
    "BKendday.rpy",
    "BKevents.rpy",
    "BKdialogue.rpy",
    "BKinteractions.rpy",
    "BKinteractions_free.rpy",
    "BKchapter1.rpy",
    "BKchapter2.rpy",
    "BKchapter3.rpy",
    "BKstory_events.rpy",
    "BKcity_events.rpy",
    "BKday_events.rpy",
    "kite_jobgirl_variables.rpy",
    "kite_jobgirl 1_riddle.rpy",
    "kite_jobgirl 2_beach.rpy",
]


def log(msg: str):
    print(msg)


def check_old_paths():
    log("\n=== Checking for old hardcoded paths ===")
    issues = []
    for rpy_file in sorted(GAME.rglob("*.rpy")):
        try:
            text = rpy_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for pattern in OLD_PATH_PATTERNS:
            if pattern in text:
                # Try to report line number
                lines = text.splitlines()
                for i, line in enumerate(lines, 1):
                    if pattern in line:
                        issues.append((rpy_file.relative_to(ROOT), i, pattern.strip("'\"")))
                        break
                else:
                    issues.append((rpy_file.relative_to(ROOT), "?", pattern.strip("'\"")))
                break  # one report per file per pattern is enough

    if issues:
        log(f"[WARN] Found {len(issues)} old path references:")
        for filepath, line, pattern in issues[:50]:
            log(f"  {filepath}:{line} -> {pattern}")
        if len(issues) > 50:
            log(f"  ... and {len(issues) - 50} more")
    else:
        log("[PASS] No old hardcoded paths found.")
    return len(issues)


def check_directory_structure():
    log("\n=== Checking directory structure ===")
    missing = 0
    for d in EXPECTED_DIRS:
        if d.exists():
            log(f"[PASS] {d.relative_to(ROOT)}")
        else:
            log(f"[FAIL] Missing: {d.relative_to(ROOT)}")
            missing += 1
    return missing


def check_root_files():
    log("\n=== Checking for leftover files in game/ root ===")
    leftover = []
    for name in FORBIDDEN_ROOT_FILES:
        p = GAME / name
        if p.exists():
            leftover.append(name)
    if leftover:
        log(f"[FAIL] {len(leftover)} files still in game/ root:")
        for name in leftover:
            log(f"  {name}")
    else:
        log("[PASS] No forbidden files left in game/ root.")
    return len(leftover)


def check_translation_sync():
    log("\n=== Checking translation file sync ===")
    issues = 0
    # Find all .rpy files in tl/chinese_simplified that don't have a corresponding source file
    tl_cn = GAME / "tl" / "chinese_simplified"
    if tl_cn.exists():
        for tl_file in sorted(tl_cn.rglob("*.rpy")):
            rel = tl_file.relative_to(tl_cn)
            src = GAME / rel
            if not src.exists():
                log(f"[WARN] Orphaned translation: {tl_file.relative_to(ROOT)} (no source {src.relative_to(ROOT)})")
                issues += 1
    if not issues:
        log("[PASS] No orphaned translation files.")
    return issues


def generate_stats():
    log("\n=== Directory statistics ===")
    for subdir in sorted(GAME.iterdir()):
        if subdir.is_dir() and subdir.name not in ("cache", "saves"):
            rpy_count = len(list(subdir.rglob("*.rpy")))
            total_lines = 0
            for rpy in subdir.rglob("*.rpy"):
                try:
                    total_lines += len(rpy.read_text(encoding="utf-8").splitlines())
                except Exception:
                    pass
            log(f"  {subdir.name:20s} | .rpy files: {rpy_count:3d} | total lines: {total_lines:6d}")


def main():
    log("Brothel King Phase 2 Refactor Verification")
    log("=" * 50)

    errs = 0
    errs += check_old_paths()
    errs += check_directory_structure()
    errs += check_root_files()
    errs += check_translation_sync()
    generate_stats()

    log("\n" + "=" * 50)
    if errs:
        log(f"[RESULT] {errs} issue(s) found. Please review above.")
        sys.exit(1)
    else:
        log("[RESULT] All checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
