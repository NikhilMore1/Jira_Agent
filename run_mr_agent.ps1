# MR Agent Runner - Create GitHub Pull Requests
# Usage: .\run_mr_agent.ps1 -Title "Feature: Name" -Head "feature/name" -Base "develop"

param(
    [string]$Title,
    [string]$Head,
    [string]$Base,
    [string]$Description = "",
    [string]$Labels = "",
    [string]$Assignees = "",
    [string]$Reviewers = "",
    [string]$JiraIssue = "",
    [string]$Changes = "",
    [switch]$Draft = $false
)

# Verify arguments
if (-not $Title -or -not $Head -or -not $Base) {
    Write-Host "❌ Error: Title, Head, and Base branches are required" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host '  .\run_mr_agent.ps1 -Title "Feature: Name" -Head "feature/name" -Base "develop"'
    Write-Host ""
    Write-Host "Optional Parameters:"
    Write-Host "  -Description `"PR description`""
    Write-Host "  -Labels `"feature,auth`""
    Write-Host "  -Assignees `"reviewer1,reviewer2`""
    Write-Host "  -Reviewers `"reviewer1,reviewer2`""
    Write-Host "  -JiraIssue `"PROJ-123`""
    Write-Host "  -Changes `"Change 1,Change 2`""
    Write-Host "  -Draft"
    exit 1
}

# Build arguments for Python script
$args = @(
    "--title", "`"$Title`"",
    "--head", "`"$Head`"",
    "--base", "`"$Base`""
)

if ($Description) { $args += "--description", "`"$Description`"" }
if ($Labels) { $args += "--labels", "`"$Labels`"" }
if ($Assignees) { $args += "--assignees", "`"$Assignees`"" }
if ($Reviewers) { $args += "--reviewers", "`"$Reviewers`"" }
if ($JiraIssue) { $args += "--jira-issue", "`"$JiraIssue`"" }
if ($Changes) { $args += "--changes", "`"$Changes`"" }
if ($Draft) { $args += "--draft" }

# Run MR Agent
Write-Host "🔀 Starting GitHub MR Agent..." -ForegroundColor Cyan
python agents/mr_agent.py @args

