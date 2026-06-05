@echo off
REM Quick validation script for Chronicle AI
REM This automatically uses the correct Python from the venv

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo Starting Chronicle AI Validation...
echo.

"%CD%\venv\Scripts\python.exe" scripts/validate_startup.py

if errorlevel 1 (
    echo.
    echo ❌ Validation failed!
    exit /b 1
) else (
    echo.
    echo ✅ Validation passed!
    exit /b 0
)
