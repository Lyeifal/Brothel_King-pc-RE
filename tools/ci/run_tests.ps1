# BK Evolution - CI Test Suite (PowerShell)
# 完整的测试套件，用于CI/CD或本地验证（Windows）

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "BK Evolution - Running Test Suite"
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 项目根目录
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $ProjectRoot

# 计数器
$TotalTests = 0
$PassedTests = 0
$FailedTests = 0

# 辅助函数
function Run-Test {
    param(
        [string]$TestName,
        [scriptblock]$Command
    )

    Write-Host "--------------------------------------" -ForegroundColor Gray
    Write-Host "Running: $TestName" -ForegroundColor Yellow
    Write-Host "--------------------------------------" -ForegroundColor Gray

    $script:TotalTests++

    try {
        & $Command
        if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
            throw "Command exited with code $LASTEXITCODE"
        }
        Write-Host "PASSED: $TestName" -ForegroundColor Green
        $script:PassedTests++
        return $true
    }
    catch {
        Write-Host "FAILED: $TestName" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Red
        $script:FailedTests++
        return $false
    }
}

# Test 1: Ren'Py Lint
Run-Test "Ren'Py Lint" {
    python Brothel_King.py . lint
}

# Test 2: Translation Count
Run-Test "Translation Count" {
    python Brothel_King.py . translate --count chinese_simplified
}

# Test 3: Mod API Verification
Run-Test "Mod API Verification" {
    python tools\verify_mod_api.py
}

# Test 4: Girl Pack Compatibility
Run-Test "Girl Pack Compatibility" {
    python tools\test_girl_packs.py
}

# Test 5: Python Syntax Check
Run-Test "Python Syntax Check" {
    Get-ChildItem -Path "tools" -Filter "*.py" -Recurse | ForEach-Object {
        python -m py_compile $_.FullName
        if ($LASTEXITCODE -ne 0) {
            throw "Syntax error in $($_.FullName)"
        }
    }
}

# Test 6: 检查关键文件存在性
Run-Test "Critical Files Existence" {
    $Files = @(
        "game\core\init\start.rpy",
        "game\core\systems\services\service_container.rpy",
        "game\core\systems\mods\mod_api_v2.rpy",
        "game\core\framework\girlclass.rpy",
        "game\core\tools\test_runner.rpy",
        "docs\project\PROJECT_GUIDE.md",
        "docs\modding\MOD_DEVELOPMENT_GUIDE.md",
        "docs\modding\GIRL_PACK_COMPATIBILITY.md"
    )

    foreach ($File in $Files) {
        if (-not (Test-Path $File)) {
            throw "Missing file: $File"
        }
    }
}

# Test 7: 检查必需目录存在
Run-Test "Required Directories" {
    $Dirs = @(
        "game\core",
        "game\custom\girls",
        "game\custom\mods",
        "game\tl\chinese_simplified",
        "docs",
        "docs_EN",
        "tools"
    )

    foreach ($Dir in $Dirs) {
        if (-not (Test-Path $Dir -PathType Container)) {
            throw "Missing directory: $Dir"
        }
    }
}

# 总结
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Test Suite Complete"
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Total Tests: $TotalTests"
Write-Host "Passed: $PassedTests" -ForegroundColor Green
if ($FailedTests -gt 0) {
    Write-Host "Failed: $FailedTests" -ForegroundColor Red
}
Write-Host ""

if ($FailedTests -gt 0) {
    Write-Host "TEST SUITE FAILED" -ForegroundColor Red
    exit 1
}
else {
    Write-Host "ALL TESTS PASSED" -ForegroundColor Green
    exit 0
}
