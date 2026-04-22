# Run Jira Agent to fetch your stories
# This script loads configuration from .env and fetches your Jira stories

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " 🔍 Jira Agent - Story Fetcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solution:" -ForegroundColor Yellow
    Write-Host "1. Download Python from https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. During installation, check 'Add Python to PATH'" -ForegroundColor White
    Write-Host "3. Restart your terminal" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if .env exists
$envPath = Join-Path (Get-Location) ".env"
if (-not (Test-Path $envPath)) {
    Write-Host "❌ ERROR: .env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected location: $envPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please ensure .env file exists in the project root." -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Configuration file found: .env" -ForegroundColor Green
Write-Host ""

# Check if required modules are installed
Write-Host "📦 Checking Python dependencies..." -ForegroundColor Cyan
$requiredModules = @("requests", "dotenv")

foreach ($module in $requiredModules) {
    try {
        python -m pip show $module >$null 2>&1
        Write-Host "  ✅ $module installed" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  Installing $module..." -ForegroundColor Yellow
        python -m pip install $module >$null
    }
}

Write-Host ""
Write-Host "🚀 Running Jira Agent..." -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Run the Jira Agent
python agents/jira_agent.py @args

Write-Host ""
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Read-Host "Press Enter to exit"

