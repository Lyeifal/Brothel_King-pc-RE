#!/usr/bin/env python3
"""
Audit placeholder integrity across all chinese_simplified translation files.

Checks that translated strings preserve the same placeholders as the original:
- printf-style: %s, %d, %i, %f, etc.
- Ren'Py interpolation: [var], [var!t], [var:...]

Reports mismatches without modifying files.
"""
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
TL_DIR = ROOT / "game" / "tl" / "chinese_simplified"

# Regex patterns
PRINTF_RE = re.compile(r"%[+-]?\d*(\.\d+)?[sdif]")
INTERPOLATION_RE = re.compile(r"\[[A-Za-z_][A-Za-z0-9_]*(?:\![A-Za-z]+|:[^\]]+)?\]")


def extract_placeholders(text):
    """Return a sorted list of placeholders in text."""
    printf = [m.group(0) for m in PRINTF_RE.finditer(text)]
    interp = INTERPOLATION_RE.findall(text)
    # Normalize: %s and [var]
    return sorted(printf + interp)


def parse_translation_blocks(content):
    """Yield (old_text, new_text, line_number) from an .rpy translation file."""
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('old '):
            old_match = re.match(r'^\s*old\s+((?:"""[\s\S]*?"""|"(?:[^"\\]|\\.)*"))', line)
            if old_match and i + 1 < len(lines):
                new_match = re.match(r'^\s*new\s+((?:"""[\s\S]*?"""|"(?:[^"\\]|\\.)*"))', lines[i + 1])
                if new_match:
                    old_raw = old_match.group(1)
                    new_raw = new_match.group(1)
                    old_text = unquote(old_raw)
                    new_text = unquote(new_raw)
                    yield old_text, new_text, i + 1
                    i += 1
        i += 1


def unquote(raw):
    """Unquote a Ren'Py string literal (single or triple quoted)."""
    raw = raw.strip()
    if raw.startswith('"""') and raw.endswith('"""'):
        return raw[3:-3]
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1].replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
    return raw


def export_xlsx(mismatches, language):
    try:
        import openpyxl
    except ImportError:
        print("openpyxl not installed; skipping xlsx export.")
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "placeholder_mismatches"
    ws.append(["", "File", "Line", "English (DO NOT MODIFY)", f"{language} Translation (fix placeholders)", "Expected Placeholders", "Actual Placeholders"])
    for m in mismatches:
        ws.append(["", str(m['file']), m['line'], m['old'], m['new'], ", ".join(m['old_ph']), ", ".join(m['new_ph'])])
    output = ROOT / f"placeholder_mismatches_{language}.xlsx"
    wb.save(output)
    print(f"Exported to: {output}")


def main():
    mismatches = []
    checked = 0

    for rpy_file in sorted(TL_DIR.rglob("*.rpy")):
        content = rpy_file.read_text(encoding='utf-8')
        for old_text, new_text, line_no in parse_translation_blocks(content):
            checked += 1
            if not new_text:
                continue  # empty translation, already covered by translate --count
            old_ph = extract_placeholders(old_text)
            new_ph = extract_placeholders(new_text)
            if old_ph != new_ph:
                mismatches.append({
                    'file': rpy_file.relative_to(ROOT),
                    'line': line_no,
                    'old': old_text,
                    'new': new_text,
                    'old_ph': old_ph,
                    'new_ph': new_ph,
                })

    print(f"Checked {checked} translation blocks")
    print(f"Placeholder mismatches: {len(mismatches)}")

    if mismatches:
        export_xlsx(mismatches, "chinese_simplified")
        for m in mismatches[:30]:
            print(f"\n{m['file']}:{m['line']}")
            print(f"  old: {m['old'][:120]!r}")
            print(f"  new: {m['new'][:120]!r}")
            print(f"  old placeholders: {m['old_ph']}")
            print(f"  new placeholders: {m['new_ph']}")
        if len(mismatches) > 30:
            print(f"\n... and {len(mismatches) - 30} more")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
