@echo off
title Auto-Commit Watcher
cd /d "%~dp0"
echo.
echo  ========================================
echo   Starting Auto-Commit Watcher...
echo  ========================================
echo.
python auto_commit_watcher.py
pause
