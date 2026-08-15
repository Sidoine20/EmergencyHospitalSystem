@echo off
title Emergency Hospital DSA System Hub
cd /d "%~dp0"

echo ======================================================================
echo    Starting Emergency Hospital Patient Management System
echo ======================================================================

if exist .venv\Scripts\python.exe (
    .\.venv\Scripts\python.exe app.py
) else (
    python app.py
)

pause
