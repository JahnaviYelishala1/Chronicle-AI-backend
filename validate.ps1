# Quick validation script for Chronicle AI
# This automatically uses the correct Python from the venv

$venvPython = "$PSScriptRoot\venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "❌ Virtual environment not found at: $venvPython" -ForegroundColor Red
    exit 1
}

Write-Host "Starting Chronicle AI Validation..." -ForegroundColor Cyan
Write-Host ""

& $venvPython "$PSScriptRoot\scripts\validate_startup.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Validation passed! Ready for deployment." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Validation failed! Fix issues before deploying." -ForegroundColor Red
    exit 1
}
