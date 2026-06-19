#!/usr/bin/env python3
"""
批量包裹 economy.rpy 中玩家可见的 % 格式化字符串。
只处理 ttip/change_log/budget_ttip/gold_ttip/text1 等已知变量上的简单模式。
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\akxls\Documents\Code\BK\Brothel_King-pc")
FILE = PROJECT_ROOT / "game" / "core" / "framework" / "economy.rpy"

# 变量前缀模式（赋值或 +=）
VAR_PATTERNS = [
    r"ttip",
    r"budget_ttip",
    r"gold_ttip\[[^\]]+\]",
    r"xp_ttip\[[^\]]+\]",
    r"jp_ttip\[[^\]]+\]",
    r"rep_ttip\[[^\]]+\]",
    r"text1",
    r"change_log\.add",
]

# 已知的内部键/不需要翻译的模板
SKIP_TEMPLATES = {
    "%s", "%s %s", "%i", "%i%%", "%s: %s", "%s: %s\\n",
}


def is_translatable_template(tmpl):
    """判断一个 % 模板是否值得翻译。"""
    t = tmpl.strip()
    if not t:
        return False
    if t in SKIP_TEMPLATES:
        return False
    # 必须包含字母
    if not any(c.isalpha() for c in t):
        return False
    return True


def wrap_line(line):
    """尝试包裹一行中的裸 % 格式化字符串。"""
    def repl(m):
        prefix = m.group(1)
        tmpl = m.group(2)
        suffix = m.group(3)
        s = tmpl[1:-1]
        if is_translatable_template(s) and not s.strip().startswith("__"):
            return f'{prefix}__({tmpl}){suffix}'
        return m.group(0)

    for var in VAR_PATTERNS:
        # 赋值
        pattern = rf"(\b{var}\s*=\s*)(\"(?:[^\"\\]|\\.)*\")(\s*%)"
        line = re.sub(pattern, repl, line)

        # +=
        pattern = rf"(\b{var}\s*\+=\s*)(\"(?:[^\"\\]|\\.)*\")(\s*%)"
        line = re.sub(pattern, repl, line)

    return line


def main():
    text = FILE.read_text(encoding="utf-8")
    lines = text.splitlines()
    new_lines = []
    changed = 0

    for lineno, line in enumerate(lines, 1):
        new_line = wrap_line(line)
        if new_line != line:
            changed += 1
        new_lines.append(new_line)

    FILE.write_text("\n".join(new_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    print(f"Modified {changed} lines in {FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
