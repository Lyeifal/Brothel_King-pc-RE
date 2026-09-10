#!/usr/bin/env python3
"""
i18n 审计脚本：扫描 game/core/**/*.rpy，找出不符合 i18n 最佳实践的代码模式。

检测项：
1. call_screen/renpy.say/renpy.notify 中的裸字符串
2. Screen text/button/label 中的裸字符串
3. 玩家可见的 + 拼接
4. 未包裹 __() 的 % 格式化

输出：按文件分组的问题列表（含行号、类型、原文）。
"""

import re
from pathlib import Path

# EN: Resolve the project root from this file's location so the tool works
#     on any machine/checkout (previously hardcoded to an old absolute path).
# ZH: 从脚本所在位置推导项目根目录，保证在任何机器/检出上可用
#     （此前硬编码了旧的绝对路径，已失效）。
PROJECT_ROOT = Path(__file__).resolve().parent.parent
GAME_DIR = PROJECT_ROOT / "game" / "core"

# 不需要翻译的字符串集合
SKIP_STRINGS = {
    "", " ", "\n", "\t",
    "-", "+", "=", "*", "/", "<", ">",
    "{", "}", "[", "]", "(", ")",
    ":", ";", ",", ".", "?", "!",
}


def is_translatable(text):
    """判断一个字符串是否可能是需要翻译的玩家可见文本。"""
    if not text or not text.strip():
        return False
    t = text.strip()
    if t in SKIP_STRINGS:
        return False
    if len(t) <= 1:
        return False
    # 跳过纯图片/音频标签
    if re.fullmatch(r"\{image=[^}]+\}|\{sound=[^}]+\}|\{movie=[^}]+\}", t):
        return False
    # 跳过纯 Ren'Py 样式标签
    if re.fullmatch(r"\{/?[a-zA-Z_]+(=[^}]+)?\}", t):
        return False
    # 跳过纯颜色代码
    if re.fullmatch(r"#[0-9A-Fa-f]{3,8}", t):
        return False
    # 跳过纯数字
    try:
        float(t)
        return False
    except ValueError:
        pass
    # 跳过文件路径
    if any(t.lower().endswith(ext) for ext in [".webp", ".png", ".jpg", ".jpeg", ".ogg", ".wav", ".mp3"]):
        return False
    # 跳过图片/资源路径片段
    if t.startswith("resources/") or "/" in t:
        return False
    # 跳过纯代码 key（只含小写、下划线、数字）
    if re.fullmatch(r"[a-z_][a-z0-9_]*", t):
        return False
    # 跳过看起来像调试/代码标识符的字符串
    if t.startswith(("Effect(", "BK_", "img_", "IT_", "bg ", "weird_pet", "falling_pet", "explode_pet", "pets_on_fire")):
        return False
    # 跳过已知的内部对话键/图片键模式
    if re.fullmatch(r"[a-z][a-z0-9_ ]*(?:chat|hunt|locked|well_being|feelings)[a-z0-9_ ]*%s[a-z0-9_ ]*", t):
        return False
    if re.fullmatch(r"%s canister %i", t):
        return False
    # 必须包含至少一个字母
    if not any(c.isalpha() for c in t):
        return False
    return True


def extract_string_literals(line):
    """从一行代码中提取双引号和单引号字符串字面量（不含三引号）。
    返回 [(start, end, quote, content), ...]
    使用单次遍历避免单引号与双引号字符串互相穿透匹配。
    """
    strings = []
    for m in re.finditer(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', line):
        quote = m.group(0)[0]
        s = m.group(0)[1:-1]
        if quote == '"':
            s = s.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
        else:
            s = s.replace("\\'", "'").replace('\\n', '\n').replace('\\\\', '\\')
        strings.append((m.start(), m.end(), quote, s))
    return sorted(strings, key=lambda x: x[0])


def mask_strings(line, strings):
    """将字符串字面量替换为占位符，便于检测字符串外的操作符。"""
    result = []
    last_end = 0
    for i, (start, end, quote, content) in enumerate(strings):
        result.append(line[last_end:start])
        result.append(f"__STR{i}__")
        last_end = end
    result.append(line[last_end:])
    return "".join(result)


def is_inside_i18n_call(line, start, end, strings):
    """判断字符串是否已经在 __() 或 _() 调用内部（考虑括号嵌套）。"""
    prefix = line[:start]
    # 简单情况：字符串前面紧邻 __( 或 _(
    if re.search(r"(?<![A-Za-z0-9_])__\(\s*$", prefix) or re.search(r"(?<![A-Za-z0-9_])_\(\s*$", prefix):
        return True

    # 复杂情况：检查是否在 __( ... ) 内部
    # 从字符串位置向前扫描，找到最近的未闭合的 __( 或 _(
    # 简化：使用正则查找所有 __( 和 _( 的位置，然后检查字符串是否在对应的括号内
    i18n_calls = [(m.start(), m.group(0).startswith("__")) for m in re.finditer(r"(?<![A-Za-z0-9_])(__\(|_\()", line[:start])]
    if not i18n_calls:
        return False

    # 从最靠近字符串的 i18n call 开始，检查括号是否闭合
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


def scan_file(fpath):
    """扫描单个文件，返回问题列表。"""
    issues = []
    content = fpath.read_text(encoding='utf-8')
    lines = content.splitlines()

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()

        # 跳过注释和空行
        if not stripped or stripped.startswith('#'):
            continue

        strings = extract_string_literals(line)
        masked = mask_strings(line, strings)

        # 跳过调试日志/调试通知/断言消息中的字符串
        if re.search(r'\bdebug_notify\s*\(|\bgame\.func_time_log|\braise\s+AssertionError\s*\(|\bBkLog\.|_debug\s*\+=|\bprint\s*\(', stripped):
            continue

        # 1. yes_no 确认框裸字符串
        for m in re.finditer(r'(?:renpy\.)?call_screen\s*\(\s*["\']yes_no["\']\s*,\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', line):
            s = m.group(1)[1:-1]
            if is_translatable(s) and not is_inside_i18n_call(line, m.start(1), m.end(1), strings):
                issues.append((lineno, 'yes_no_bare_string', s[:80]))

        # 2. renpy.say 裸字符串（简化检测：第二个参数是字符串）
        for m in re.finditer(r'renpy\.say\s*\([^,]+,\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', line):
            s = m.group(1)[1:-1]
            if is_translatable(s) and not is_inside_i18n_call(line, m.start(1), m.end(1), strings):
                issues.append((lineno, 'renpy.say_bare_string', s[:80]))

        # 3. renpy.notify 裸字符串
        for m in re.finditer(r'renpy\.notify\s*\(\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', line):
            s = m.group(1)[1:-1]
            if is_translatable(s) and not is_inside_i18n_call(line, m.start(1), m.end(1), strings):
                issues.append((lineno, 'renpy.notify_bare_string', s[:80]))

        # 4. Screen text/button/label 裸字符串
        # 匹配 text "..." / button "..." / label "..." 但前面没有 _(
        for keyword in ['text', 'button', 'label']:
            pattern = rf'\b{keyword}\s+(?:action\s+[^"\']+\s+)?("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
            for m in re.finditer(pattern, line):
                s = m.group(1)[1:-1]
                # 跳过已翻译的 Ren'Py 插值表达式，如 [config.name!t]
                if re.search(r'\[[^\]]*!t[^\]]*\]', s):
                    continue
                if is_translatable(s) and not is_inside_i18n_call(line, m.start(1), m.end(1), strings):
                    issues.append((lineno, f'screen_{keyword}_bare_string', s[:80]))

        # 5. + 拼接可见文本
        # 只在字符串字面量外检查 + 操作符
        if re.search(r'["\']\s*\+\s*[^"\']|\+\s*["\']', masked):
            strings_in_line = [s for _, _, _, s in strings if is_translatable(s)]
            if strings_in_line:
                # 只报告包含完整句子的拼接（至少一个字符串包含空格或标点）
                has_sentence = any(re.search(r'[\s.!?,:;]', s) for s in strings_in_line)
                if has_sentence:
                    # 跳过已知的非玩家可见拼接模式
                    if re.search(r'resources/|declare\(|was_seen\(|condition\(|No dialogue found for|__STR\d+__\s*\+\s*[a-zA-Z_]+\s*\+\s*__STR\d+__', masked):
                        pass
                    else:
                        issues.append((lineno, 'string_concatenation', stripped[:120]))

        # 6. % 格式化未包裹 __()
        # 只在字符串字面量外检查 % 操作符，基于 extract_string_literals 的位置避免跨字符串贪婪匹配
        for start, end, quote, s in strings:
            if '%' not in s or not is_translatable(s) or is_inside_i18n_call(line, start, end, strings):
                continue
            # 检查字符串闭引号后是否紧跟 %（允许空白）
            m = re.match(r'\s*%\s*\(', line[end:])
            if not m:
                continue
            # 跳过字典键格式化，如 dict["key %s" % (x)]
            paren_start = end + m.end() - 1
            depth = 1
            paren_end = None
            for i in range(paren_start + 1, len(line)):
                if line[i] == '(':
                    depth += 1
                elif line[i] == ')':
                    depth -= 1
                    if depth == 0:
                        paren_end = i
                        break
            if paren_end is not None and re.match(r'\s*\]', line[paren_end+1:]):
                continue
            # 要求模板包含完整单词（至少两个词或明显是句子）
            if len(s.split()) >= 2 or re.search(r'[.!?]', s):
                issues.append((lineno, 'unwrapped_percent_format', s[:80]))

    return issues


def main():
    print("Scanning game/core/**/*.rpy for i18n issues...\n")

    total_issues = 0
    file_counts = {}

    for fpath in sorted(GAME_DIR.rglob('*.rpy')):
        issues = scan_file(fpath)
        if issues:
            rel = fpath.relative_to(PROJECT_ROOT)
            print(f"=== {rel} ({len(issues)} issues) ===")
            file_counts[rel] = len(issues)
            for lineno, issue_type, text in issues:
                print(f"  line {lineno:5d} [{issue_type:30s}] {text!r}")
            print()
            total_issues += len(issues)

    print("=" * 60)
    print(f"Total files with issues: {len(file_counts)}")
    print(f"Total issues: {total_issues}")

    if file_counts:
        print("\nTop files by issue count:")
        for rel, count in sorted(file_counts.items(), key=lambda x: -x[1])[:15]:
            print(f"  {count:4d}  {rel}")

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    exit(main())
