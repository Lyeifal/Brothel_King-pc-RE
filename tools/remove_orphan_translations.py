#!/usr/bin/env python3
"""
Remove orphan translation blocks from .rpy translation files.
Pass one or more "file.rpy:translate_id" arguments.
"""
import re
import sys
from pathlib import Path

TL_DIR = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc\game\tl\chinese_simplified")


def remove_block(content, translate_id):
    """Remove a translate block with the given id, including its leading comment."""
    # Match optional comment line, then translate line, then blank line, then indented body
    pattern = re.compile(
        r'^(\s*#.*\n)?'
        r'\s*translate\s+\w+\s+' + re.escape(translate_id) + r'\s*:\s*\n'
        r'(?:\s*\n)*'
        r'((?:[ \t]+.*\n)+)',
        re.MULTILINE,
    )
    return pattern.sub('', content)


def main():
    targets = []
    for arg in sys.argv[1:]:
        if ':' not in arg:
            print(f"Invalid target (expected file.rpy:translate_id): {arg}")
            continue
        file_part, tid = arg.rsplit(':', 1)
        targets.append((file_part, tid))

    if not targets:
        print("Usage: python remove_orphan_translations.py path/to/file.rpy:translate_id ...")
        return

    for file_part, tid in targets:
        fpath = TL_DIR / file_part
        if not fpath.exists():
            print(f"File not found: {fpath}")
            continue
        content = fpath.read_text(encoding='utf-8')
        new_content = remove_block(content, tid)
        if new_content != content:
            fpath.write_text(new_content, encoding='utf-8')
            print(f"Removed {tid} from {fpath}")
        else:
            print(f"Block {tid} not found in {fpath}")


if __name__ == "__main__":
    main()
