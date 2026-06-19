import re

def is_translatable(text):
    if not text or not text.strip():
        return False
    t = text.strip()
    if len(t) <= 1:
        return False
    if not any(c.isalpha() for c in t):
        return False
    return True

def extract_string_literals(line):
    strings = []
    for m in re.finditer(r'"(?:[^"\\]|\\.)*"', line):
        s = m.group(0)[1:-1]
        strings.append((m.start(), m.end(), '"', s))
    for m in re.finditer(r"'(?:[^'\\]|\\.)*'", line):
        s = m.group(0)[1:-1]
        strings.append((m.start(), m.end(), "'", s))
    return sorted(strings, key=lambda x: x[0])

def is_inside_i18n_call(line, start, end, strings):
    prefix = line[:start]
    if re.search(r"(?<![A-Za-z0-9_])__\(\s*$", prefix) or re.search(r"(?<![A-Za-z0-9_])_\(\s*$", prefix):
        return True
    i18n_calls = [(m.start(), m.group(0).startswith("__")) for m in re.finditer(r"(?<![A-Za-z0-9_])(__\(|_\()", line[:start])]
    if not i18n_calls:
        return False
    for call_start, is_double in reversed(i18n_calls):
        depth = 1
        for i in range(call_start + (3 if is_double else 2), start):
            if line[i] == '(':
                depth += 1
            elif line[i] == ')':
                depth -= 1
                if depth <= 0:
                    break
        if depth > 0:
            return True
    return False

line = '        night_late.add(_("Entertainment (served): %s") % (event_color["average"] % served), ttip=_("%i customers were entertained out of %i waiting customers") % (served, len(customers))))'
strings = extract_string_literals(line)
print('Strings:', strings)
for start, end, quote, s in strings:
    print(f'  {s!r}: translatable={is_translatable(s)}, inside_i18n={is_inside_i18n_call(line, start, end, strings)}')

print()
print('=== New percent detection ===')
for start, end, quote, s in strings:
    if '%' not in s or not is_translatable(s) or is_inside_i18n_call(line, start, end, strings):
        continue
    if re.match(r'\s*%', line[end:]):
        print(f'Matched: {s!r}, after={line[end:end+10]!r}')
