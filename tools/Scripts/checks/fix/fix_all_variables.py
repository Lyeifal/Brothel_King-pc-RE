#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive fix for ALL translated [variable] names in strings.rpy and dialogue files.
This script handles:
1. Same-count pairs: position-based replacement
2. Merged variables (e.g. [thing] [best] → [最好的东西]): intelligent split
3. Dialogue files: comment/translation line pairs
"""

import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

sys.stdout.reconfigure(encoding='utf-8')

def has_cjk(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def is_english_var(text):
    """Check if text looks like an English Ren'Py variable name."""
    return bool(re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_.!]*', text))

def extract_brackets(text):
    """Extract all [...] patterns from text."""
    return re.findall(r'\[[^\]]+\]', text)

def extract_english_vars_from_old(text):
    """Extract variable names from old text (English)."""
    brackets = extract_brackets(text)
    return [b for b in brackets if is_english_var(b[1:-1])]

# --- Special case: merged variable mappings ---
# When Google Translate merges [thing] [best] into [最好的东西]
MERGED_VAR_MAP = {
    '最好的东西': ['[thing]', '[best]'],
    '最糟糕的事': ['[thing]', '[worst]'],
    '最糟糕的情况': ['[thing]', '[worst]'],
    '某某东西': ['[thing]', '[worst]'],
    '最坏的': ['[worst]', '[thing]'],  # "[worst] is a terrible [thing]"
    '最佳': ['[best]', '[thing]'],  # "totally [best] type when it comes to [thing]"
}

# Single-variable Chinese → English mappings (for mismatched count repair)
SINGLE_VAR_MAP = {
    '东西': '[thing]',
    '事物': '[thing]',
    '最好的': '[best]',
    '最佳': '[best]',
    '最坏的': '[worst]',
    '最糟糕的': '[worst]',
    '最差的': '[worst]',
    '那件事': '[thing]',
    '这件事': '[thing]',
    '这件事': '[thing]',
    '某某': '[thing]',
    '某样东西': '[thing]',
    '某事': '[thing]',
    '爱好': '[thing]',
    '最喜欢的': '[best]',
    '女孩名字': '[girl.name]',
    '女孩全名': '[girl.fullname]',
    '女孩.全名': '[girl.fullname]',
    '女孩的名字': '[girl.name]',
    '女孩.名字': '[girl.name]',
    '女孩名': '[girl.name]',
    '女主姓名': '[girl.name]',
    '妓院名称': '[brothel.name]',
    '妓院广告': '[brothel.advertising]',
    '妓院卧室类型名称': '[brothel.bedroom_type.name]',
    '妓院维护': '[brothel.maintenance]',
    '新等级': '[new_rank]',
    '主角玩家职业': '[MC.playerclass]',
    '顾客': '[customer]',
    '资源': '[resource]',
    '精神病院费用': '[asylum_cost]',
    '持续时间': '[duration]',
    '半价': '[half_price]',
    '价格': '[price]',
    '季节': '[season]',
    '索引': '[index]',
    '计数': '[count]',
    '家': '[home]',
    '房子': '[house]',
    '章节，资源成本，额外库存': '[chapter, resource_cost, extra_stock]',
    '最好的东西': '[thing] [best]',
    '那东西': '[thing]',
    '这东西': '[thing]',
    '最爱': '[best]',
    '最糟糕的事': '[thing] [worst]',
    '最糟糕': '[worst]',
    '最差': '[worst]',
    '最糟糕的事情': '[thing] [worst]',
    '最喜欢': '[best]',
    '最糟糕的': '[worst]',
    '最喜欢的东西': '[thing] [best]',
    '最爱好的东西': '[thing] [best]',
    '最讨厌': '[worst]',
    '最爱好的': '[best]',
    '最爱好的事物': '[thing] [best]',
    '最喜爱的东西': '[thing] [best]',
    '最喜欢的事物': '[thing] [best]',
    '最爱好的': '[best]',
    '撒谎': '[lie]',
    '谎言': '[lie]',
    '说谎的人': '[liar]',
    '说谎': '[lying]',
    '某某': '[something]',
    '某种东西': '[something]',
    '某物': '[something]',
}

def fix_mismatched_vars(old_text, new_text, old_vars, new_vars):
    """
    Fix case where old_vars and new_vars have different counts.
    Returns fixed new_text or None if couldn't fix.
    """
    result = new_text
    cjk_vars = [(i, v) for i, v in enumerate(new_vars) if has_cjk(v[1:-1])]
    if not cjk_vars:
        return result

    for idx, cjk_var in cjk_vars:
        inner = cjk_var[1:-1]  # strip brackets
        if inner in MERGED_VAR_MAP:
            # Check if old_vars match the expected merge
            expected = MERGED_VAR_MAP[inner]
            if len(old_vars) == len(expected):
                # Verify each expected var is in old_vars (order may differ)
                if all(ev in old_vars for ev in expected):
                    replacement = ' '.join(expected)
                    result = result.replace(cjk_var, replacement, 1)
                    continue
        
        # Try single var mapping
        if inner in SINGLE_VAR_MAP:
            replacement = SINGLE_VAR_MAP[inner]
            # If replacement is multiple vars but old only has one, check
            replacement_count = len(extract_brackets(replacement))
            if replacement_count <= len(old_vars):
                result = result.replace(cjk_var, replacement, 1)
                continue
        
        # Fallback: try to match by looking at old vars
        # If old has [worst] and [thing], and cjk is "最坏的" → map to [worst]
        # This is a heuristic
        if 'worst' in [v[1:-1] for v in old_vars] and '最' in inner and ('坏' in inner or '糟' in inner or '差' in inner):
            if '[worst]' in old_vars:
                result = result.replace(cjk_var, '[worst]', 1)
                continue
        if 'best' in [v[1:-1] for v in old_vars] and ('好' in inner or '佳' in inner or '爱' in inner):
            if '[best]' in old_vars:
                result = result.replace(cjk_var, '[best]', 1)
                continue
        if 'thing' in [v[1:-1] for v in old_vars] and ('东西' in inner or '事物' in inner or '事' in inner):
            if '[thing]' in old_vars:
                result = result.replace(cjk_var, '[thing]', 1)
                continue
    
    return result

def fix_strings_rpy(filepath):
    """Fix variables in strings.rpy."""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    fixed_count = 0
    mismatch_fixed = 0
    unchanged = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('    old '):
            old_line = line
            old_vars = extract_english_vars_from_old(old_line)
            if i + 1 < len(lines) and lines[i+1].startswith('    new '):
                new_line = lines[i+1]
                new_vars = extract_brackets(new_line)
                
                if not old_vars:
                    i += 2
                    continue
                
                original_new = new_line
                fixed_new = new_line
                
                if len(old_vars) == len(new_vars):
                    # Position-based replacement
                    for oi, (ov, nv) in enumerate(zip(old_vars, new_vars)):
                        inner = nv[1:-1]
                        if has_cjk(inner) and is_english_var(ov[1:-1]):
                            fixed_new = fixed_new.replace(nv, ov, 1)
                            fixed_count += 1
                else:
                    # Mismatched count - try intelligent fix
                    result = fix_mismatched_vars(old_line, new_line, old_vars, new_vars)
                    if result != new_line:
                        fixed_new = result
                        mismatch_fixed += 1
                
                if fixed_new != original_new:
                    lines[i+1] = fixed_new
                else:
                    unchanged += 1
                
                i += 2
                continue
        i += 1
    
    filepath.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Position-based fixes: {fixed_count}")
    print(f"  Mismatch fixes: {mismatch_fixed}")
    print(f"  Unchanged (could not fix): {unchanged}")
    return fixed_count + mismatch_fixed

def fix_dialogue_file(filepath):
    """Fix variables in dialogue translate files."""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    fixed_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('# ') and not stripped.startswith('# old'):
            # This is likely a comment line with original text
            old_line = line
            old_vars = extract_english_vars_from_old(old_line)
            if old_vars and i + 1 < len(lines):
                next_line = lines[i+1]
                # Check if next line is a dialogue line (starts with speaker or indented text)
                if not next_line.strip().startswith('#') and not next_line.strip().startswith('translate') and not next_line.strip().startswith('old '):
                    new_vars = extract_brackets(next_line)
                    if len(old_vars) == len(new_vars):
                        for ov, nv in zip(old_vars, new_vars):
                            inner = nv[1:-1]
                            if has_cjk(inner) and is_english_var(ov[1:-1]):
                                lines[i+1] = next_line.replace(nv, ov, 1)
                                next_line = lines[i+1]
                                fixed_count += 1
                    else:
                        result = fix_mismatched_vars(old_line, next_line, old_vars, new_vars)
                        if result != next_line:
                            lines[i+1] = result
                            fixed_count += 1
        i += 1
    
    filepath.write_text('\n'.join(lines), encoding='utf-8')
    return fixed_count

def main():
    tl_dir = Path('game/tl/chinese_simplified')
    
    total_fixed = 0
    
    # Fix strings.rpy
    strings_file = tl_dir / 'strings.rpy'
    if strings_file.exists():
        print(f"Fixing {strings_file}...")
        total_fixed += fix_strings_rpy(strings_file)
    
    # Fix dialogue files
    for rpy_file in tl_dir.rglob('*.rpy'):
        if rpy_file.name == 'strings.rpy':
            continue
        fixed = fix_dialogue_file(rpy_file)
        if fixed > 0:
            print(f"  Fixed {fixed} in {rpy_file.name}")
            total_fixed += fixed
    
    print(f"\nTotal fixes: {total_fixed}")
    
    # Post-check: count remaining CJK variables
    print("\n--- Post-check: remaining CJK variables ---")
    remaining = 0
    for rpy_file in tl_dir.rglob('*.rpy'):
        content = rpy_file.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if line.startswith('    new ') or (not line.strip().startswith('#') and '[' in line):
                matches = re.findall(r'\[([\u4e00-\u9fff][^\]]*)\]', line)
                for m in matches:
                    print(f"  {rpy_file.name}: [{m}]")
                    remaining += 1
    print(f"Remaining CJK variables: {remaining}")

if __name__ == '__main__':
    main()
