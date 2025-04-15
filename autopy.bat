REM file autopy.bat
@echo off
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please run install.bat first.
    pause
    exit /b
)

python "%~dp0main.py" %*
if %errorlevel% neq 0 (
    echo An error occurred while running the program.
    pause
    exit /b %errorlevel%
)
pause