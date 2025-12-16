@echo off
title Daily News Roundup (Full)
cd /d "%~dp0"
"venv\Scripts\python.exe" src/workflow.py --playwright
pause
