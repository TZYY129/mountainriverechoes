@echo off
chcp 65001 >nul
title MountainRiverEchoes - Auto Backup

set "GIT_ROOT=C:\Users\20318\.workbuddy\binaries\git\versions\mingit-v2.56.0.windows.2"
set "PATH=%GIT_ROOT%\cmd;%GIT_ROOT%\mingw64\bin;%GIT_ROOT%\ucrt64\bin;%PATH%"
set "PROJ=C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\mountainriverechoes"
cd /d "%PROJ%"

echo ================================================================
echo   Auto backup  -  mountainriverechoes
echo ================================================================
echo.

git add -A
git diff --cached --quiet
if errorlevel 1 goto do_commit
echo [skip]  no changes since last backup
goto try_push

:do_commit
git commit -m "chore: auto backup" -q
if errorlevel 1 goto commit_failed
echo [ok]    changes committed
goto try_push

:commit_failed
echo [warn]  commit failed

:try_push
set GIT_TERMINAL_PROMPT=0
git push origin master >nul 2>&1
if errorlevel 1 goto push_skip
echo [ok]    pushed to GitHub
goto done

:push_skip
echo [note]  cannot reach GitHub right now - local backup is saved

:done
echo.
echo Done.
exit /b 0
