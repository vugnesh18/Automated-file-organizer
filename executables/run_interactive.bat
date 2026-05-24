@echo off
REM Automated File Organizer - Windows Batch Launcher
REM This script helps you run the file organizer on Windows

echo.
echo ======================================
echo  Automated File Organizer - Launcher
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

REM Run the CLI with interactive mode
python cli.py --interactive

pause
