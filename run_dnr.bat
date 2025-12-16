@echo off
title Daily News Roundup - Workflow
cd /d "%~dp0"

echo.
echo ============================================================
echo   DAILY NEWS ROUNDUP - LAUNCHER
echo ============================================================
echo.
echo   1. Standard workflow (RSS + Airtable)
echo   2. Full workflow (+ Playwright paywalled sites)
echo   3. Full workflow with enrichment (slower)
echo   4. Quick dry-run (just show story counts)
echo   5. Exit
echo.
set /p choice="Select option (1-5): "

if "%choice%"=="1" goto standard
if "%choice%"=="2" goto playwright
if "%choice%"=="3" goto full
if "%choice%"=="4" goto dryrun
if "%choice%"=="5" goto end

echo Invalid choice. Please try again.
pause
goto :eof

:standard
echo.
echo Starting standard workflow...
echo.
"venv\Scripts\python.exe" src/workflow.py
goto done

:playwright
echo.
echo Starting workflow with Playwright sources...
echo.
"venv\Scripts\python.exe" src/workflow.py --playwright
goto done

:full
echo.
echo Starting full workflow with enrichment...
echo.
"venv\Scripts\python.exe" src/workflow.py --playwright --enrich
goto done

:dryrun
echo.
echo Running dry-run...
echo.
"venv\Scripts\python.exe" src/main.py --dry-run --playwright
goto done

:done
echo.
echo ============================================================
pause

:end
