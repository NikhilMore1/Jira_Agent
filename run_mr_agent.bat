@echo off
REM MR Agent Runner - Create GitHub Pull Requests
REM Usage: run_mr_agent.bat --title "Feature: Name" --head feature/name --base develop

cd /d "%~dp0"
python agents/mr_agent.py %*
pause

