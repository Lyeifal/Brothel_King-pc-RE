# Clean runtime artifacts for Brothel King (Ren'Py)
# Usage: powershell -ExecutionPolicy Bypass -File tools/clean_runtime.ps1

$ErrorActionPreference = "SilentlyContinue"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Write-Host "Cleaning runtime artifacts in: $root" -ForegroundColor Cyan

# 1. Delete all .rpyc cache files
$rpyc = Get-ChildItem -Path "$root\game" -Recurse -Filter "*.rpyc" -File
$rpycCount = $rpyc.Count
$rpyc | Remove-Item -Force
Write-Host "  Deleted $rpycCount .rpyc files" -ForegroundColor Green

# 2. Delete orphan .rpyc (no matching .rpy)
$orphan = Get-ChildItem -Path "$root\game" -Recurse -Filter "*.rpyc" -File | Where-Object { -not (Test-Path ($_.FullName -replace '\.rpyc$', '.rpy')) }
$orphanCount = $orphan.Count
$orphan | Remove-Item -Force
Write-Host "  Deleted $orphanCount orphan .rpyc files" -ForegroundColor Green

# 3. Delete Ren'Py cache directory
if (Test-Path "$root\game\cache") {
    Remove-Item -Recurse -Force "$root\game\cache"
    Write-Host "  Deleted game/cache/" -ForegroundColor Green
}

# 4. Delete runtime log files
$logs = @("errors.txt", "traceback.txt", "log.txt", "lint.txt")
$logCount = 0
foreach ($f in $logs) {
    $path = Join-Path $root $f
    if (Test-Path $path) {
        Remove-Item -Force $path
        $logCount++
    }
}
Write-Host "  Deleted $logCount runtime log files" -ForegroundColor Green

# 5. Delete persistent data (optional - uncomment if needed)
# $persistentPath = Join-Path $env:APPDATA "RenPy\Brothel_King"
# if (Test-Path $persistentPath) {
#     Remove-Item -Recurse -Force $persistentPath
#     Write-Host "  Deleted persistent data at $persistentPath" -ForegroundColor Yellow
# }

Write-Host "Done. You can now restart the game." -ForegroundColor Cyan
