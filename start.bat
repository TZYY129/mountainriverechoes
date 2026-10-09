@echo off
chcp 65001 >nul
title MountainRiverEchoes
cd /d "C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\mountainriverechoes"

set PY=C:\Users\20318\.workbuddy\binaries\python\envs\default\Scripts\python.exe

echo ================================================================
echo   Shan He Hui Xiang  /  mountainriverechoes  (local WebUI)
echo   URL: http://127.0.0.1:8766
echo   Close this window to stop the service.
echo ================================================================
echo.

start "" http://127.0.0.1:8766

"%PY%" webui\mountainriverechoes.py

echo.
echo [service stopped]
pause
