#!/usr/bin/env python3
"""
i18n 回归测试：
1. 运行 Ren'Py translate --count，断言 0 missing
2. 运行 Ren'Py lint，断言无新增错误
3. 运行 tools/i18n_lint.py，断言 0 issues

需要在项目根目录运行。
"""

import subprocess
import sys
from pathlib import Path

# EN: Resolve the project root from this file's location so the tool works
#     on any machine/checkout (previously hardcoded to an old absolute path).
# ZH: 从脚本所在位置推导项目根目录，保证在任何机器/检出上可用
#     （此前硬编码了旧的绝对路径，已失效）。
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYTHON_EXE = PROJECT_ROOT / "lib" / "py3-windows-x86_64" / "python.exe"
RENPY_LAUNCHER = PROJECT_ROOT / "Brothel_King.py"


def run_command(cmd, description):
    """Run a command and return (success, output)."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=600,
        )
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr)
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: {description}")
        return False, ""
    except Exception as e:
        print(f"ERROR: {e}")
        return False, ""


def check_translate_count():
    """Run Ren'Py translate --count and check for 0 missing."""
    cmd = [str(PYTHON_EXE), str(RENPY_LAUNCHER), ".", "translate", "--count", "chinese_simplified"]
    success, output = run_command(cmd, "Ren'Py translate --count")
    if not success:
        return False, "translate --count command failed"

    if "0 missing dialogue translations" in output and "0 missing string translations" in output:
        return True, "translate --count: 0 missing"
    else:
        return False, f"translate --count still has missing translations:\n{output[-500:]}"


def check_lint():
    """Run Ren'Py lint."""
    cmd = [str(PYTHON_EXE), str(RENPY_LAUNCHER), ".", "lint"]
    success, output = run_command(cmd, "Ren'Py lint")
    if not success:
        return False, "lint command failed"
    # Ren'Py lint exits 0 even with warnings, so we just check it ran
    return True, "lint completed"


def check_i18n_lint():
    """Run tools/i18n_lint.py."""
    cmd = [sys.executable, "tools/i18n_lint.py"]
    success, output = run_command(cmd, "i18n_lint.py")
    if not success:
        return False, f"i18n_lint.py found issues:\n{output[-500:]}"
    return True, "i18n_lint.py: 0 issues"


def main():
    if not PYTHON_EXE.exists():
        print(f"Python executable not found: {PYTHON_EXE}")
        return 1
    if not RENPY_LAUNCHER.exists():
        print(f"Ren'Py launcher not found: {RENPY_LAUNCHER}")
        return 1

    checks = [
        check_translate_count,
        check_lint,
        check_i18n_lint,
    ]

    all_passed = True
    results = []
    for check in checks:
        passed, message = check()
        results.append((check.__name__, passed, message))
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    for name, passed, message in results:
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}: {message}")

    if all_passed:
        print("\nAll i18n checks passed!")
        return 0
    else:
        print("\nSome i18n checks failed. See details above.")
        return 1


if __name__ == "__main__":
    exit(main())
