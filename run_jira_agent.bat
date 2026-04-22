@echo off
REM Run Jira Agent to fetch your stories
REM This script loads configuration from .env and fetches your Jira stories

echo.
echo ========================================
echo  🔍 Jira Agent - Story Fetcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Solution:
    echo 1. Download Python from https://www.python.org/downloads/
    echo 2. During installation, check "Add Python to PATH"
    echo 3. Restart your terminal
    echo.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo ❌ ERROR: .env file not found!
    echo.
    echo Expected location: %cd%\.env
    echo.
    echo Please run "python test_env.py" first to verify setup.
    echo.
    pause
    exit /b 1
)

REM Check if required modules are installed
python -m pip show requests >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Installing required dependencies...
    python -m pip install requests python-dotenv
    echo.
)

REM Run the Jira Agent
echo 🚀 Running Jira Agent...
echo.
python agents/jira_agent.py %*
pause

