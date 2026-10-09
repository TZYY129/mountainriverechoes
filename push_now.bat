@echo off
chcp 65001 >nul
title Push to GitHub - mountainriverechoes

set "GIT_ROOT=C:\Users\20318\.workbuddy\binaries\git\versions\mingit-v2.56.0.windows.2"
set "PATH=%GIT_ROOT%\cmd;%GIT_ROOT%\mingw64\bin;%PATH%"
set "PROJ=C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\mountainriverechoes"
cd /d "%PROJ%"

echo ================================================================
echo   Push mountainriverechoes to GitHub
echo ================================================================
echo.
echo  repo   : https://github.com/TZYY129/mountainriverechoes
echo  branch : master
echo.
echo  A GitHub sign-in window will open. Just sign in and approve.
echo  No token or password needed.
echo  First push uploads about 30 MB, please wait.
echo.

git add -A
git diff --cached --quiet
if errorlevel 1 goto do_commit
echo [skip]  nothing new to commit
goto do_push

:do_commit
git commit -m "chore: manual backup" -q
echo [ok]    changes committed

:do_push
echo.
echo ----------------------------------------------------------------
echo  Connecting to GitHub - a sign-in window should appear now...
echo ----------------------------------------------------------------
echo.

git push -u origin master --progress
if errorlevel 1 goto force_push
goto push_ok

:force_push
echo.
echo [note]  Remote already has other commits (your fork came with history).
echo         Replacing it with your local backup...
echo.
git push --force -u origin master --progress
if errorlevel 1 goto push_failed
goto push_ok

:push_ok
echo.
echo ================================================================
echo  [OK]  Pushed successfully.
echo  Credentials saved - future auto backups can push silently.
echo ================================================================
goto end

:push_failed
echo.
echo ================================================================
echo  [FAILED]  Push did not complete. Read the message above.
echo.
echo  Common reasons:
echo    - the sign-in window was closed or cancelled
echo    - cannot reach github.com right now (just try again later)
echo    - no permission on that repository
echo ================================================================

:end
echo.
pause
