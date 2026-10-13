# BK Evolution — CI/CD 设置与测试流程

> **版本**: 2026-10-13  
> **目标读者**: 开发者、CI维护者  
> **状态**: 当前稳定版

---

## 📚 目录

1. [测试工具概览](#测试工具概览)
2. [本地测试脚本](#本地测试脚本)
3. [CI集成示例](#ci集成示例)
4. [提交前检查清单](#提交前检查清单)
5. [测试覆盖范围](#测试覆盖范围)
6. [故障排除](#故障排除)

---

## 🔧 测试工具概览

BK Evolution 提供以下测试工具：

| 工具 | 用途 | 位置 | 运行方式 |
|------|------|------|---------|
| **Test Runner** | 游戏内自动化测试套件 | 游戏主界面 "Tests" 按钮 | Ren'Py 内部 |
| **Girl Pack Tester** | 女孩包兼容性验证 | `tools/test_girl_packs.py` | Python 脚本 |
| **Lint** | 代码静态检查 | Ren'Py Launcher | `renpy.sh lint` |
| **Translation Check** | 翻译完整性检查 | `tools/extract_translations.py` | Python 脚本 |
| **Mod API Validator** | Mod API 验证 | `tools/verify_mod_api.py` | Python 脚本 |

---

## 📜 本地测试脚本

### Bash 脚本（Linux/macOS/WSL）

创建 `tools/ci/run_tests.sh`:

```bash
#!/usr/bin/env bash
################################################################################
## BK Evolution - CI Test Runner (Bash)
## Usage: bash tools/ci/run_tests.sh [--quick]
################################################################################

set -euo pipefail  # 错误时立即退出

# 配置
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RENPY_SDK="${RENPY_SDK:-$PROJECT_ROOT/../renpy}"
TEMP_DIR="$PROJECT_ROOT/temp"
LOG_FILE="$TEMP_DIR/ci_test_log.txt"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 创建临时目录
mkdir -p "$TEMP_DIR"

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 测试计数器
TESTS_PASSED=0
TESTS_FAILED=0

# 记录测试结果
record_result() {
    if [ $1 -eq 0 ]; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_info "$2 ✓"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "$2 ✗"
    fi
}

################################################################################
# 测试1: Ren'Py Lint
################################################################################
test_lint() {
    log_info "Running Ren'Py Lint..."
    
    if [ ! -d "$RENPY_SDK" ]; then
        log_warn "Ren'Py SDK not found at $RENPY_SDK, skipping lint"
        return 0
    fi
    
    cd "$PROJECT_ROOT"
    "$RENPY_SDK/renpy.sh" "$PROJECT_ROOT" lint > "$TEMP_DIR/lint_output.txt" 2>&1
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        record_result 0 "Lint check"
    else
        log_error "Lint errors found:"
        tail -n 20 "$TEMP_DIR/lint_output.txt"
        record_result 1 "Lint check"
    fi
    
    return $exit_code
}

################################################################################
# 测试2: Girl Pack 兼容性
################################################################################
test_girl_packs() {
    log_info "Testing Girl Packs..."
    
    cd "$PROJECT_ROOT"
    python3 tools/test_girl_packs.py > "$TEMP_DIR/girl_pack_test.txt" 2>&1
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        record_result 0 "Girl Pack test"
    else
        log_error "Girl Pack errors:"
        tail -n 20 "$TEMP_DIR/girl_pack_test.txt"
        record_result 1 "Girl Pack test"
    fi
    
    return $exit_code
}

################################################################################
# 测试3: 翻译完整性检查
################################################################################
test_translations() {
    log_info "Checking translations..."
    
    cd "$PROJECT_ROOT"
    
    # 检查翻译文件是否存在
    if [ ! -d "game/tl/chinese_simplified" ]; then
        log_warn "Chinese translation directory not found, skipping"
        return 0
    fi
    
    # 统计未翻译条目（简单检查）
    local untranslated_count=$(find game/tl/chinese_simplified -name "*.rpy" -exec grep -c "# TODO" {} + 2>/dev/null | awk '{s+=$1} END {print s}' || echo "0")
    
    if [ "$untranslated_count" -gt 0 ]; then
        log_warn "Found $untranslated_count untranslated entries"
    fi
    
    record_result 0 "Translation check"
    return 0
}

################################################################################
# 测试4: Mod API 验证
################################################################################
test_mod_api() {
    log_info "Validating Mod API..."
    
    cd "$PROJECT_ROOT"
    
    if [ ! -f "tools/verify_mod_api.py" ]; then
        log_warn "Mod API validator not found, skipping"
        return 0
    fi
    
    python3 tools/verify_mod_api.py > "$TEMP_DIR/mod_api_test.txt" 2>&1
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        record_result 0 "Mod API validation"
    else
        log_error "Mod API errors:"
        tail -n 20 "$TEMP_DIR/mod_api_test.txt"
        record_result 1 "Mod API validation"
    fi
    
    return $exit_code
}

################################################################################
# 测试5: Python 语法检查
################################################################################
test_python_syntax() {
    log_info "Checking Python syntax..."
    
    cd "$PROJECT_ROOT"
    
    # 检查所有 .py 文件
    find tools -name "*.py" -exec python3 -m py_compile {} \; 2> "$TEMP_DIR/python_syntax_errors.txt"
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        record_result 0 "Python syntax check"
    else
        log_error "Python syntax errors:"
        cat "$TEMP_DIR/python_syntax_errors.txt"
        record_result 1 "Python syntax check"
    fi
    
    return $exit_code
}

################################################################################
# 主测试流程
################################################################################
main() {
    log_info "========================================="
    log_info "BK Evolution - CI Test Suite"
    log_info "========================================="
    
    # 检查快速模式
    QUICK_MODE=false
    if [ "${1:-}" = "--quick" ]; then
        QUICK_MODE=true
        log_info "Running in QUICK mode (skipping lint)"
    fi
    
    # 执行测试
    test_python_syntax || true
    test_girl_packs || true
    test_translations || true
    test_mod_api || true
    
    if [ "$QUICK_MODE" = false ]; then
        test_lint || true
    fi
    
    # 汇总结果
    log_info "========================================="
    log_info "Test Results:"
    log_info "  Passed: $TESTS_PASSED"
    log_error "  Failed: $TESTS_FAILED"
    log_info "========================================="
    
    # 保存日志
    {
        echo "========================================="
        echo "BK Evolution - CI Test Results"
        echo "Date: $(date)"
        echo "========================================="
        echo "Passed: $TESTS_PASSED"
        echo "Failed: $TESTS_FAILED"
        echo "========================================="
    } > "$LOG_FILE"
    
    log_info "Full log saved to: $LOG_FILE"
    
    # 返回失败状态
    if [ $TESTS_FAILED -gt 0 ]; then
        exit 1
    fi
    
    exit 0
}

# 运行主函数
main "$@"
```

**使用方式**:

```bash
# 完整测试
bash tools/ci/run_tests.sh

# 快速测试（跳过 lint）
bash tools/ci/run_tests.sh --quick
```

---

### PowerShell 脚本（Windows）

创建 `tools/ci/run_tests.ps1`:

```powershell
################################################################################
## BK Evolution - CI Test Runner (PowerShell)
## Usage: powershell -ExecutionPolicy Bypass -File tools/ci/run_tests.ps1 [-Quick]
################################################################################

[CmdletBinding()]
param(
    [switch]$Quick = $false
)

# 配置
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$RenpySDK = if ($env:RENPY_SDK) { $env:RENPY_SDK } else { Join-Path $ProjectRoot "..\renpy" }
$TempDir = Join-Path $ProjectRoot "temp"
$LogFile = Join-Path $TempDir "ci_test_log.txt"

# 创建临时目录
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

# 测试计数器
$TestsPassed = 0
$TestsFailed = 0

# 颜色输出函数
function Write-Info { param([string]$Message) Write-Host "[INFO] $Message" -ForegroundColor Green }
function Write-Warn { param([string]$Message) Write-Host "[WARN] $Message" -ForegroundColor Yellow }
function Write-Err { param([string]$Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }

# 记录测试结果
function Record-Result {
    param([bool]$Success, [string]$TestName)
    if ($Success) {
        $script:TestsPassed++
        Write-Info "$TestName ✓"
    } else {
        $script:TestsFailed++
        Write-Err "$TestName ✗"
    }
}

################################################################################
# 测试1: Ren'Py Lint
################################################################################
function Test-Lint {
    Write-Info "Running Ren'Py Lint..."
    
    $RenpyExe = Join-Path $RenpySDK "renpy.exe"
    if (-not (Test-Path $RenpyExe)) {
        Write-Warn "Ren'Py SDK not found at $RenpySDK, skipping lint"
        return $true
    }
    
    $LintOutput = Join-Path $TempDir "lint_output.txt"
    & $RenpyExe $ProjectRoot lint > $LintOutput 2>&1
    $Success = $LASTEXITCODE -eq 0
    
    if (-not $Success) {
        Write-Err "Lint errors found:"
        Get-Content $LintOutput -Tail 20 | ForEach-Object { Write-Host $_ }
    }
    
    Record-Result -Success $Success -TestName "Lint check"
    return $Success
}

################################################################################
# 测试2: Girl Pack 兼容性
################################################################################
function Test-GirlPacks {
    Write-Info "Testing Girl Packs..."
    
    $TestScript = Join-Path $ProjectRoot "tools\test_girl_packs.py"
    $OutputFile = Join-Path $TempDir "girl_pack_test.txt"
    
    python $TestScript > $OutputFile 2>&1
    $Success = $LASTEXITCODE -eq 0
    
    if (-not $Success) {
        Write-Err "Girl Pack errors:"
        Get-Content $OutputFile -Tail 20 | ForEach-Object { Write-Host $_ }
    }
    
    Record-Result -Success $Success -TestName "Girl Pack test"
    return $Success
}

################################################################################
# 测试3: 翻译完整性检查
################################################################################
function Test-Translations {
    Write-Info "Checking translations..."
    
    $TlDir = Join-Path $ProjectRoot "game\tl\chinese_simplified"
    if (-not (Test-Path $TlDir)) {
        Write-Warn "Chinese translation directory not found, skipping"
        return $true
    }
    
    # 统计未翻译条目
    $TodoCount = (Get-ChildItem $TlDir -Recurse -Filter "*.rpy" | Select-String "# TODO" | Measure-Object).Count
    
    if ($TodoCount -gt 0) {
        Write-Warn "Found $TodoCount untranslated entries"
    }
    
    Record-Result -Success $true -TestName "Translation check"
    return $true
}

################################################################################
# 测试4: Mod API 验证
################################################################################
function Test-ModAPI {
    Write-Info "Validating Mod API..."
    
    $ValidatorScript = Join-Path $ProjectRoot "tools\verify_mod_api.py"
    if (-not (Test-Path $ValidatorScript)) {
        Write-Warn "Mod API validator not found, skipping"
        return $true
    }
    
    $OutputFile = Join-Path $TempDir "mod_api_test.txt"
    python $ValidatorScript > $OutputFile 2>&1
    $Success = $LASTEXITCODE -eq 0
    
    if (-not $Success) {
        Write-Err "Mod API errors:"
        Get-Content $OutputFile -Tail 20 | ForEach-Object { Write-Host $_ }
    }
    
    Record-Result -Success $Success -TestName "Mod API validation"
    return $Success
}

################################################################################
# 测试5: Python 语法检查
################################################################################
function Test-PythonSyntax {
    Write-Info "Checking Python syntax..."
    
    $ToolsDir = Join-Path $ProjectRoot "tools"
    $ErrorFile = Join-Path $TempDir "python_syntax_errors.txt"
    
    $AllSuccess = $true
    Get-ChildItem $ToolsDir -Recurse -Filter "*.py" | ForEach-Object {
        python -m py_compile $_.FullName 2>> $ErrorFile
        if ($LASTEXITCODE -ne 0) {
            $AllSuccess = $false
        }
    }
    
    if (-not $AllSuccess) {
        Write-Err "Python syntax errors:"
        Get-Content $ErrorFile | ForEach-Object { Write-Host $_ }
    }
    
    Record-Result -Success $AllSuccess -TestName "Python syntax check"
    return $AllSuccess
}

################################################################################
# 主测试流程
################################################################################
function Main {
    Write-Info "========================================="
    Write-Info "BK Evolution - CI Test Suite"
    Write-Info "========================================="
    
    if ($Quick) {
        Write-Info "Running in QUICK mode (skipping lint)"
    }
    
    # 执行测试
    Test-PythonSyntax | Out-Null
    Test-GirlPacks | Out-Null
    Test-Translations | Out-Null
    Test-ModAPI | Out-Null
    
    if (-not $Quick) {
        Test-Lint | Out-Null
    }
    
    # 汇总结果
    Write-Info "========================================="
    Write-Info "Test Results:"
    Write-Info "  Passed: $TestsPassed"
    Write-Err "  Failed: $TestsFailed"
    Write-Info "========================================="
    
    # 保存日志
    @"
=========================================
BK Evolution - CI Test Results
Date: $(Get-Date)
=========================================
Passed: $TestsPassed
Failed: $TestsFailed
=========================================
"@ | Out-File -FilePath $LogFile -Encoding UTF8
    
    Write-Info "Full log saved to: $LogFile"
    
    # 返回失败状态
    if ($TestsFailed -gt 0) {
        exit 1
    }
    
    exit 0
}

# 运行主函数
Main
```

**使用方式**:

```powershell
# 完整测试
powershell -ExecutionPolicy Bypass -File tools/ci/run_tests.ps1

# 快速测试
powershell -ExecutionPolicy Bypass -File tools/ci/run_tests.ps1 -Quick
```

---

## 🔗 CI集成示例

### GitHub Actions

创建 `.github/workflows/test.yml`:

```yaml
name: BK Evolution CI

on:
  push:
    branches: [ main, bk-evolution ]
  pull_request:
    branches: [ main, bk-evolution ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Run CI tests
      run: |
        bash tools/ci/run_tests.sh --quick
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: temp/
```

### GitLab CI

创建 `.gitlab-ci.yml`:

```yaml
stages:
  - test

test:
  stage: test
  image: python:3.10
  
  script:
    - python -m pip install --upgrade pip
    - bash tools/ci/run_tests.sh --quick
  
  artifacts:
    when: always
    paths:
      - temp/
    expire_in: 1 week
  
  only:
    - main
    - bk-evolution
```

---

## ✅ 提交前检查清单

在提交代码前，请确保：

### 1. 本地测试通过

```bash
# Linux/macOS/WSL
bash tools/ci/run_tests.sh

# Windows
powershell -ExecutionPolicy Bypass -File tools/ci/run_tests.ps1
```

### 2. 代码格式正确

```bash
# 检查 .rpy 文件缩进（4空格）
grep -rn $'\\t' game/core/  # 不应有 Tab

# 检查 Python 文件格式
python -m flake8 tools/ --max-line-length=120
```

### 3. 翻译文件同步

```bash
# 如果修改了硬编码文本，更新翻译
renpy.sh game/ extract_translations
```

### 4. Girl Pack 兼容性

```bash
python tools/test_girl_packs.py
```

### 5. 存档兼容性

- [ ] 在旧版本创建存档
- [ ] 在新版本读取存档
- [ ] 验证所有功能正常

### 6. Mod 兼容性

- [ ] 测试所有内置 Mod
- [ ] 确认 Mod API 未破坏

---

## 📊 测试覆盖范围

### 当前测试覆盖

| 测试类型 | 覆盖范围 | 状态 |
|---------|---------|------|
| **Lint** | 全部 `.rpy` 文件语法检查 | ✅ 已覆盖 |
| **Girl Pack** | 所有女孩包 `_BK.ini` 完整性 | ✅ 已覆盖 |
| **Translation** | 中文翻译文件存在性检查 | ⚠️ 部分覆盖 |
| **Mod API** | Mod 注册与钩子验证 | ✅ 已覆盖 |
| **Python Syntax** | `tools/` 下所有 Python 脚本 | ✅ 已覆盖 |
| **Unit Tests** | 游戏内 Test Runner | ⚠️ 手动运行 |
| **Save/Load** | 存档兼容性 | ❌ 需手动测试 |

### 未来计划

- [ ] 自动化存档兼容性测试
- [ ] 性能测试（启动时间、读档时间）
- [ ] UI 自动化测试
- [ ] 端到端测试（完整游戏流程）

---

## 🛠️ 故障排除

### 问题1: Lint 报错 "indentation error"

**原因**: 使用了 Tab 而不是空格

**解决**:

```bash
# 查找所有 Tab
grep -rn $'\\t' game/core/

# 转换为空格（使用 sed 或编辑器）
find game/core -name "*.rpy" -exec sed -i 's/\\t/    /g' {} +
```

### 问题2: Girl Pack 测试失败

**原因**: `_BK.ini` 缺少必需字段或格式错误

**解决**: 检查 `temp/girl_pack_test_report.txt`，修复对应的女孩包

### 问题3: Python syntax check 失败

**原因**: Python 脚本有语法错误

**解决**:

```bash
# 手动检查
python -m py_compile tools/your_script.py

# 使用 flake8 检查
pip install flake8
flake8 tools/your_script.py
```

### 问题4: Windows PowerShell 执行策略限制

**错误**: `cannot be loaded because running scripts is disabled`

**解决**:

```powershell
# 临时允许
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 或直接运行
powershell -ExecutionPolicy Bypass -File tools/ci/run_tests.ps1
```

### 问题5: Ren'Py SDK 未找到

**错误**: `Ren'Py SDK not found`

**解决**:

```bash
# 设置环境变量
export RENPY_SDK="/path/to/renpy-sdk"

# 或编辑脚本中的路径
RENPY_SDK="${RENPY_SDK:-$PROJECT_ROOT/../renpy}"
```

---

## 📚 相关文档

- [`../modding/MOD_DEVELOPMENT_GUIDE.md`](../modding/MOD_DEVELOPMENT_GUIDE.md) — Mod 开发指南
- [`MANUAL_TEST_GUIDE.md`](MANUAL_TEST_GUIDE.md) — 手动测试指南
- [`../../tools/test_girl_packs.py`](../../tools/test_girl_packs.py) — Girl Pack 测试器源码
- [Ren'Py Lint 文档](https://www.renpy.org/doc/html/lint.html)

---

**最后更新**: 2026-10-13  
**维护者**: BK Evolution Team
