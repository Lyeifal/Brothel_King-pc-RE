#!/usr/bin/env python3
"""
Audit the translation directory structure against the source directory.
- Identify .rpy translation files without corresponding source files.
- Identify source .rpy files without corresponding translation files (informational).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "game" / "core"
TL_DIR = ROOT / "game" / "tl" / "chinese_simplified" / "core"


def collect_rpy_files(directory):
    return {p.relative_to(directory) for p in directory.rglob("*.rpy")}


def main():
    src_files = collect_rpy_files(SRC_DIR)
    tl_files = collect_rpy_files(TL_DIR)

    # Translation files without source
    stale = sorted(tl_files - src_files)
    # Source files without translation (informational, excluding declarations/options)
    missing_tl = sorted(src_files - tl_files)

    print(f"Source .rpy files: {len(src_files)}")
    print(f"Translation .rpy files: {len(tl_files)}")
    print()

    print(f"Stale translation files (no corresponding source): {len(stale)}")
    for f in stale:
        print(f"  {f}")

    print()
    print(f"Source files without translation file: {len(missing_tl)}")
    for f in missing_tl[:50]:
        print(f"  {f}")
    if len(missing_tl) > 50:
        print(f"  ... and {len(missing_tl) - 50} more")


if __name__ == "__main__":
    main()
