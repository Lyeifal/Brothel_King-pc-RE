#!/bin/bash
# BK Evolution - CI Test Suite
# 完整的测试套件，用于CI/CD或本地验证

set -e  # 任何命令失败就退出

echo "========================================="
echo "BK Evolution - Running Test Suite"
echo "========================================="
echo ""

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 辅助函数
run_test() {
    TEST_NAME="$1"
    shift
    COMMAND="$@"

    echo "--------------------------------------"
    echo "Running: $TEST_NAME"
    echo "--------------------------------------"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if $COMMAND; then
        echo -e "${GREEN}✓ PASSED${NC}: $TEST_NAME"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}: $TEST_NAME"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Test 1: Ren'Py Lint
run_test "Ren'Py Lint" \
    python Brothel_King.py . lint

# Test 2: Translation Count (检查翻译覆盖率)
run_test "Translation Count" \
    python Brothel_King.py . translate --count chinese_simplified

# Test 3: Mod API Verification
run_test "Mod API Verification" \
    python tools/verify_mod_api.py

# Test 4: Girl Pack Compatibility
run_test "Girl Pack Compatibility" \
    python tools/test_girl_packs.py

# Test 5: Python Syntax Check (所有Python工具)
run_test "Python Syntax Check" bash -c '
    for file in tools/*.py tools/*/*.py; do
        if [ -f "$file" ]; then
            python -m py_compile "$file" || exit 1
        fi
    done
'

# Test 6: 检查关键文件存在性
run_test "Critical Files Existence" bash -c '
    FILES=(
        "game/core/init/start.rpy"
        "game/core/systems/services/service_container.rpy"
        "game/core/systems/mods/mod_api_v2.rpy"
        "game/core/framework/girlclass.rpy"
        "game/core/tools/test_runner.rpy"
        "docs/project/PROJECT_GUIDE.md"
        "docs/modding/MOD_DEVELOPMENT_GUIDE.md"
        "docs/modding/GIRL_PACK_COMPATIBILITY.md"
    )

    for file in "${FILES[@]}"; do
        if [ ! -f "$file" ]; then
            echo "Missing: $file"
            exit 1
        fi
    done
'

# Test 7: 检查必需目录存在
run_test "Required Directories" bash -c '
    DIRS=(
        "game/core"
        "game/custom/girls"
        "game/custom/mods"
        "game/tl/chinese_simplified"
        "docs"
        "docs_EN"
        "tools"
    )

    for dir in "${DIRS[@]}"; do
        if [ ! -d "$dir" ]; then
            echo "Missing directory: $dir"
            exit 1
        fi
    done
'

# 总结
echo ""
echo "========================================="
echo "Test Suite Complete"
echo "========================================="
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
fi
echo ""

if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}❌ TEST SUITE FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    exit 0
fi
