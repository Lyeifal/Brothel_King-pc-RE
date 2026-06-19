import re
from pathlib import Path

def wrap_notify_in_file(fpath):
    lines = Path(fpath).read_text(encoding='utf-8').splitlines(keepends=True)
    new_lines = []
    changed = False

    for line in lines:
        original = line
        # Match renpy.notify( "..." ) or renpy.notify( "..." % (...))
        # Avoid lines already containing __( or _(
        if re.search(r'renpy\.notify\(\s*["\']', line) and not re.search(r'renpy\.notify\(\s*(?:__\(|_\()', line):
            # Wrap the first string literal after renpy.notify(
            line = re.sub(
                r'(renpy\.notify\(\s*)(["\'])(.*?)(?:\2)',
                lambda m: f'{m.group(1)}__({m.group(2)}{m.group(3)}{m.group(2)})',
                line,
                count=1
            )
            # If there was a trailing ) without formatting, we now have renpy.notify(__("..."))
            # which is correct.
            # If there was "..." % (...), after wrapping it becomes renpy.notify(__("...") % (...))
            # because the rest of the line is preserved.
            if line != original:
                changed = True
        new_lines.append(line)

    if changed:
        Path(fpath).write_text(''.join(new_lines), encoding='utf-8')
        print(f"Updated {fpath}")
    else:
        print(f"No changes {fpath}")

if __name__ == "__main__":
    import sys
    for f in sys.argv[1:]:
        wrap_notify_in_file(f)
