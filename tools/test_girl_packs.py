#!/usr/bin/env python3
"""
BK Evolution - Girl Pack Compatibility Tester
测试 game/custom/girls/ 下所有女孩包的加载兼容性

Usage:
    python tools/test_girl_packs.py
    python tools/test_girl_packs.py --verbose
    python tools/test_girl_packs.py --pack "某个女孩包名"

Output:
    - 兼容性报告（成功/失败/警告）
    - 详细错误日志（temp/girl_pack_test_report.txt）
"""

import os
import sys
import argparse
from pathlib import Path
from configparser import ConfigParser
from collections import defaultdict

# Windows控制台编码修复
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
GIRLS_DIR = PROJECT_ROOT / "game" / "custom" / "girls"
REPORT_FILE = PROJECT_ROOT / "temp" / "girl_pack_test_report.txt"


class GirlPackValidator:
    """女孩包验证器"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.results = {
            "success": [],
            "failed": [],
            "warnings": []
        }

    def validate_all_packs(self, specific_pack=None):
        """验证所有女孩包"""
        if not GIRLS_DIR.exists():
            print(f"❌ 女孩包目录不存在: {GIRLS_DIR}")
            return

        packs = []
        for item in GIRLS_DIR.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if specific_pack and item.name != specific_pack:
                    continue
                packs.append(item)

        if not packs:
            print(f"❌ 未找到女孩包")
            return

        print(f"🔍 找到 {len(packs)} 个女孩包，开始验证...")
        print("=" * 80)

        for pack_dir in sorted(packs):
            self.validate_pack(pack_dir)

        self.print_summary()
        self.save_report()

    def validate_pack(self, pack_dir: Path):
        """验证单个女孩包"""
        pack_name = pack_dir.name
        issues = []
        warnings = []

        # 检查1: _BK.ini 文件存在性
        ini_file = pack_dir / "_BK.ini"
        if not ini_file.exists():
            issues.append("缺少 _BK.ini 文件")
            self.results["failed"].append((pack_name, issues, warnings))
            self._print_result(pack_name, False, issues, warnings)
            return

        # 检查2: 读取 _BK.ini
        try:
            config = ConfigParser(allow_no_value=True)
            config.read(ini_file, encoding='utf-8-sig')  # 处理BOM
        except Exception as e:
            issues.append(f"_BK.ini 解析失败: {e}")
            self.results["failed"].append((pack_name, issues, warnings))
            self._print_result(pack_name, False, issues, warnings)
            return

        # 检查3: 必需字段
        # BK使用的是 [identity] section，不是 [girl]
        required_sections = ["identity"]

        has_identity = config.has_section("identity")
        if not has_identity:
            issues.append("缺少必需section: [identity]")
        else:
            # 检查必需字段
            if not config.has_option("identity", "first_name"):
                issues.append("缺少必需字段: [identity] first_name")
            else:
                first_name = config.get("identity", "first_name").strip(' "')
                if not first_name:
                    issues.append("first_name 字段为空")

        # 检查4: 图片目录
        # BK的图片和_BK.ini在同一目录
        pic_dir = pack_dir
        pic_files = list(pic_dir.glob("*.jpg")) + list(pic_dir.glob("*.png")) + \
                   list(pic_dir.glob("*.webp")) + list(pic_dir.glob("*.avif"))

        if len(pic_files) == 0:
            warnings.append("图片目录为空（没有 jpg/png/webp/avif 文件）")
        elif self.verbose:
            print(f"   📷 找到 {len(pic_files)} 个图片文件")

        # 检查5: 常见字段验证
        if has_identity:
            # 特质 (Traits) - 可能在 [base positive traits] 或 [base negative traits]
            if config.has_section("base positive traits"):
                if config.has_option("base positive traits", "traits"):
                    traits_str = config.get("base positive traits", "traits")
                    # 简单检查格式（应该是逗号分隔）
                    if traits_str and "\n" in traits_str:
                        warnings.append("traits 格式可能不正确（包含换行符）")

            # 初始等级
            if config.has_section("background story"):
                if config.has_option("background story", "init_level"):
                    try:
                        level = int(config.get("background story", "init_level"))
                        if level < 1 or level > 7:
                            warnings.append(f"init_level 超出合理范围: {level} (建议1-7)")
                    except ValueError:
                        warnings.append("init_level 不是有效整数")

        # 检查6: 文件编码（警告级别）
        try:
            with open(ini_file, 'rb') as f:
                raw = f.read()
                # 检查BOM
                if raw[:3] == b'\xef\xbb\xbf':
                    if self.verbose:
                        print(f"   ℹ️  检测到UTF-8 BOM（已正确处理）")
                # 尝试UTF-8解码
                raw.decode('utf-8')
        except UnicodeDecodeError:
            warnings.append("文件编码可能不是UTF-8")

        # 汇总结果
        if issues:
            self.results["failed"].append((pack_name, issues, warnings))
            self._print_result(pack_name, False, issues, warnings)
        elif warnings:
            self.results["warnings"].append((pack_name, warnings))
            self._print_result(pack_name, True, issues, warnings)
        else:
            self.results["success"].append(pack_name)
            self._print_result(pack_name, True, issues, warnings)

    def _print_result(self, pack_name, success, issues, warnings):
        """打印单个验证结果"""
        if success and not warnings:
            print(f"✅ {pack_name}")
        elif success and warnings:
            print(f"⚠️  {pack_name}")
            if self.verbose:
                for w in warnings:
                    print(f"      警告: {w}")
        else:
            print(f"❌ {pack_name}")
            for issue in issues:
                print(f"      错误: {issue}")
            if self.verbose and warnings:
                for w in warnings:
                    print(f"      警告: {w}")

    def print_summary(self):
        """打印汇总报告"""
        total = len(self.results["success"]) + len(self.results["failed"]) + len(self.results["warnings"])
        print("=" * 80)
        print(f"\n📊 验证汇总:")
        print(f"   总计: {total} 个女孩包")
        print(f"   ✅ 完全通过: {len(self.results['success'])}")
        print(f"   ⚠️  有警告: {len(self.results['warnings'])}")
        print(f"   ❌ 失败: {len(self.results['failed'])}")

        if self.results["failed"]:
            print(f"\n❌ 失败的女孩包:")
            for pack_name, issues, warnings in self.results["failed"]:
                print(f"   - {pack_name}")
                for issue in issues:
                    print(f"       {issue}")

    def save_report(self):
        """保存详细报告到文件"""
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("BK Evolution - Girl Pack Compatibility Report\n")
            f.write("=" * 80 + "\n\n")

            total = len(self.results["success"]) + len(self.results["failed"]) + len(self.results["warnings"])
            f.write(f"总计: {total} 个女孩包\n")
            f.write(f"✅ 完全通过: {len(self.results['success'])}\n")
            f.write(f"⚠️  有警告: {len(self.results['warnings'])}\n")
            f.write(f"❌ 失败: {len(self.results['failed'])}\n\n")

            if self.results["success"]:
                f.write("=" * 80 + "\n")
                f.write("✅ 完全通过的女孩包\n")
                f.write("=" * 80 + "\n")
                for pack_name in self.results["success"]:
                    f.write(f"  - {pack_name}\n")
                f.write("\n")

            if self.results["warnings"]:
                f.write("=" * 80 + "\n")
                f.write("⚠️  有警告的女孩包\n")
                f.write("=" * 80 + "\n")
                for pack_name, warnings in self.results["warnings"]:
                    f.write(f"\n📦 {pack_name}\n")
                    for w in warnings:
                        f.write(f"    警告: {w}\n")
                f.write("\n")

            if self.results["failed"]:
                f.write("=" * 80 + "\n")
                f.write("❌ 失败的女孩包\n")
                f.write("=" * 80 + "\n")
                for pack_name, issues, warnings in self.results["failed"]:
                    f.write(f"\n📦 {pack_name}\n")
                    for issue in issues:
                        f.write(f"    ❌ 错误: {issue}\n")
                    if warnings:
                        for w in warnings:
                            f.write(f"    ⚠️  警告: {w}\n")
                f.write("\n")

        print(f"\n📄 详细报告已保存: {REPORT_FILE}")


def main():
    parser = argparse.ArgumentParser(description="BK Evolution Girl Pack Compatibility Tester")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    parser.add_argument("--pack", "-p", type=str, help="只测试指定的女孩包")

    args = parser.parse_args()

    validator = GirlPackValidator(verbose=args.verbose)
    validator.validate_all_packs(specific_pack=args.pack)


if __name__ == "__main__":
    main()
