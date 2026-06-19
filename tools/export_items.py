import re, json, ast

with open('game/core/data/items.rpy', encoding='utf-8') as f:
    content = f.read()

IT_MAP = {
    'IT_Misc': 'Misc', 'IT_Gift': 'Gift', 'IT_Weapon': 'Weapon',
    'IT_Ring': 'Ring', 'IT_Necklace': 'Necklace', 'IT_Accessory': 'Accessory',
    'IT_Dress': 'Dress', 'IT_Food': 'Food', 'IT_Toy': 'Toy',
    'IT_Supplies': 'Supplies', 'IT_Flower': 'Flower', 'IT_Passive': 'Passive',
    'IT_Story': 'Story',
}

def extract_string(s, start):
    """Extract a quoted string starting at position start. Returns (value, end_pos)."""
    quote = s[start]
    assert quote in '"\''
    i = start + 1
    result = []
    while i < len(s):
        c = s[i]
        if c == '\\':
            i += 1
            if i < len(s):
                result.append(s[i])
                i += 1
            continue
        if c == quote:
            return ''.join(result), i + 1
        result.append(c)
        i += 1
    return ''.join(result), i

def tokenize_args(s):
    """Tokenize function arguments, respecting strings and parens."""
    tokens = []
    cur = []
    depth = 0
    in_str = False
    str_char = None
    i = 0
    while i < len(s):
        c = s[i]
        if in_str:
            cur.append(c)
            if c == '\\':
                i += 1
                if i < len(s):
                    cur.append(s[i])
            elif c == str_char:
                in_str = False
                str_char = None
            i += 1
            continue
        if c in '"\'':
            cur.append(c)
            in_str = True
            str_char = c
            i += 1
            continue
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif c == ',' and depth == 0:
            tokens.append(''.join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    if cur:
        tokens.append(''.join(cur).strip())
    return tokens

def parse_effect(s):
    m = re.match(r"Effect\s*\((.*)\)\s*$", s, re.DOTALL)
    if not m:
        return None
    args = tokenize_args(m.group(1))
    result = {}
    pos_keys = ['type', 'target', 'value', 'chance']
    pos_idx = 0
    for arg in args:
        arg = arg.strip()
        m2 = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$', arg, re.DOTALL)
        if m2:
            k, v = m2.group(1), m2.group(2).strip()
            try:
                result[k] = ast.literal_eval(v)
            except:
                result[k] = v
        else:
            if pos_idx < len(pos_keys):
                try:
                    result[pos_keys[pos_idx]] = ast.literal_eval(arg)
                except:
                    result[pos_keys[pos_idx]] = arg.strip('"\'')
                pos_idx += 1
    return result

def parse_item(item_str):
    m = re.match(r"Item\s*\((.*)\)\s*$", item_str, re.DOTALL)
    if not m:
        return None
    inner = m.group(1)
    # Replace IT_ constants with string literals
    for k, v in IT_MAP.items():
        inner = re.sub(r'\b' + k + r'\b', repr(v), inner)
    # Extract effects first (remove them from inner)
    effects = []
    def repl_eff(m):
        # Find matching closing paren
        start = m.end() - 1  # position of opening paren
        depth = 1
        i = start + 1
        while i < len(inner) and depth > 0:
            if inner[i] == '(':
                depth += 1
            elif inner[i] == ')':
                depth -= 1
            i += 1
        eff_str = inner[m.start():i]
        eff = parse_effect(eff_str)
        if eff:
            effects.append(eff)
        # Replace with spaces to preserve positions
        spaces = ' ' * len(eff_str)
        return spaces
    inner_no_eff = re.sub(r'Effect\s*\(', repl_eff, inner)
    # Parse key=value pairs from inner_no_eff
    result = {}
    i = 0
    while i < len(inner_no_eff):
        # Skip whitespace and commas
        while i < len(inner_no_eff) and inner_no_eff[i] in ' \t\n,':
            i += 1
        if i >= len(inner_no_eff):
            break
        m_key = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*', inner_no_eff[i:])
        if not m_key:
            i += 1
            continue
        key = m_key.group(1)
        i += len(m_key.group(0))
        # Parse value
        val_start = i
        if i < len(inner_no_eff) and inner_no_eff[i] in '"\'':
            val, i = extract_string(inner_no_eff, i)
        else:
            depth = 0
            while i < len(inner_no_eff):
                c = inner_no_eff[i]
                if c in '([{':
                    depth += 1
                elif c in ')]}':
                    depth -= 1
                elif c == ',' and depth == 0:
                    break
                i += 1
            val_str = inner_no_eff[val_start:i].strip()
            try:
                val = ast.literal_eval(val_str)
            except:
                val = val_str
        result[key] = val
    if effects:
        result['effects'] = effects
    return result

def extract_items(section):
    items = []
    idx = 0
    while True:
        m = re.search(r'Item\s*\(', section[idx:])
        if not m:
            break
        start = idx + m.start()
        depth = 1
        i = idx + m.end()
        while i < len(section) and depth > 0:
            if section[i] == '(':
                depth += 1
            elif section[i] == ')':
                depth -= 1
            i += 1
        parsed = parse_item(section[start:i])
        if parsed:
            items.append(parsed)
        idx = i
    return items

template_match = re.search(r'template_items\s*=\s*\[(.*?)\]', content, re.DOTALL)
all_match = re.search(r'all_items\s*=\s*\[(.*?)\]', content, re.DOTALL)

template_items = extract_items(template_match.group(1)) if template_match else []
all_items = extract_items(all_match.group(1)) if all_match else []

for it in template_items:
    it['template'] = True

output = {
    "template_items": template_items,
    "all_items": all_items,
}

with open('game/core/data/items/items.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Exported {len(template_items)} template items and {len(all_items)} regular items")
