#!/usr/bin/env python3
"""Scan game/core/**/*.rpy for menu options that are not literal strings."""

import re
from pathlib import Path

ROOT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
CORE = ROOT / "game" / "core"


def get_indent(line):
    return len(line) - len(line.lstrip())


def is_literal_option(text):
    """Check if menu option text is a literal string (possibly with condition)."""
    stripped = text.strip()
    if stripped.endswith(':'):
        stripped = stripped[:-1].strip()

    # If starts with quote, find matching closing quote
    if stripped.startswith('"') or stripped.startswith("'"):
        quote = stripped[0]
        # Find closing quote not escaped
        end = 1
        while end < len(stripped):
            if stripped[end] == '\\':
                end += 2
                continue
            if stripped[end] == quote:
                # Check for condition after closing quote
                after = stripped[end+1:].strip()
                return after == '' or after.startswith('if ')
            end += 1
        return False
    return False


def is_control_or_nested(line):
    """Skip non-option lines inside menu blocks."""
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith('#'):
        return True
    if stripped.startswith('$'):
        return True
    if stripped.startswith(('if ', 'elif ', 'else:', 'python:', 'try:', 'except', 'show ', 'label ', 'while ', 'for ', 'jump ', 'call ', 'return', 'pass', 'with ', 'scene ', 'play ', 'stop ', 'window ', 'nvl ')):
        return True
    return False


def scan_file(fpath):
    issues = []
    lines = fpath.read_text(encoding='utf-8').splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect menu start (not menu caption like "menu caption:")
        if re.match(r'^\s*menu\s*:', stripped):
            menu_indent = get_indent(line)
            i += 1

            # Find option indent (first non-empty, non-control line inside menu)
            option_indent = None
            j = i
            while j < len(lines):
                inner = lines[j]
                if not inner.strip():
                    j += 1
                    continue
                inner_indent = get_indent(inner)
                if inner_indent <= menu_indent:
                    break  # exited menu
                # Skip comments when determining option indent
                if inner.strip().startswith('#'):
                    j += 1
                    continue
                option_indent = inner_indent
                break

            if option_indent is None:
                continue

            # Scan options at option_indent level
            while i < len(lines):
                inner = lines[i]
                if not inner.strip():
                    i += 1
                    continue
                inner_indent = get_indent(inner)
                if inner_indent <= menu_indent:
                    break  # exited menu

                if inner_indent == option_indent:
                    if inner.strip().endswith(':'):
                        if not is_control_or_nested(inner) and not is_literal_option(inner):
                            issues.append((i + 1, inner.strip()))
                    # else: could be a multi-line option start, ignore

                i += 1
            continue

        i += 1

    return issues


def main():
    total_issues = 0
    for fpath in sorted(CORE.rglob('*.rpy')):
        issues = scan_file(fpath)
        if issues:
            total_issues += len(issues)
            print(f"\n=== {fpath.relative_to(ROOT)} ({len(issues)} issues) ===")
            for lineno, text in issues[:20]:
                print(f"  line {lineno}: {text[:120]}")
            if len(issues) > 20:
                print(f"  ... and {len(issues) - 20} more")

    print(f"\nTotal non-literal menu options: {total_issues}")


if __name__ == "__main__":
    main()
