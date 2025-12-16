@echo off
title Daily News Roundup
cd /d "%~dp0"
"venv\Scripts\python.exe" src/workflow.py
pause
