@echo off
setlocal EnableDelayedExpansion

REM Get Python versions from Python.org instead of endoflife.date
set "python_version=3.12.2"

echo Checking if Python %python_version% or greater is already installed...
set "current_version="
where python >nul 2>nul && (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "current_version=%%v"
)

if "%current_version%"=="" (
    echo Python is not installed. Proceeding with installation.

    REM Define the URL and file name of the Python installer
    set "url=https://www.python.org/ftp/python/%python_version%/python-%python_version%-amd64.exe"
    set "installer=%temp%\python-%python_version%-amd64.exe"

    REM Download the Python installer using BITS transfer (more reliable)
    echo Downloading Python installer...
    powershell -Command "Start-BitsTransfer -Source '%url%' -Destination '%installer%'"

    REM Install Python
    echo Installing Python...
    start /wait %installer% /passive InstallAllUsers=1 PrependPath=1 Include_test=0
    if errorlevel 1 (
        echo Installation failed!
        exit /b 1
    ) else (
        echo Installation successful!
    )

    REM Cleanup
    del "%installer%"
) else (
    echo Python %current_version% is already installed.
)

REM Refresh environment variables
call refreshenv.cmd 2>nul
if errorlevel 1 (
    echo Refreshing PATH...
    powershell -Command "& {$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')}"
)

echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r "%~dp0requirements.txt"

echo Setting up AutoPY...

REM Create desktop shortcut with icon
echo Creating desktop shortcut...
powershell -Command ^
"$WshShell = New-Object -comObject WScript.Shell; ^
$Shortcut = $WshShell.CreateShortcut($env:USERPROFILE + '\Desktop\AutoPY.lnk'); ^
$Shortcut.TargetPath = '%~dp0autopy.bat'; ^
$Shortcut.WorkingDirectory = '%~dp0'; ^
$Shortcut.IconLocation = '%~dp0assets\icon.ico'; ^
$Shortcut.Save()"

echo.
echo Installation complete! 
echo -----------------------------------------------
echo  Please restart your command prompt, then:
echo  1. Double click AutoPY shortcut on your desktop
echo  2. Type 'autopy' in any terminal
echo -----------------------------------------------
pause