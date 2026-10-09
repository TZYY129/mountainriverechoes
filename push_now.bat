@echo off
chcp 65001 >nul
title Push to GitHub - mountainriverechoes

set "GIT_ROOT=C:\Users\20318\.workbuddy\binaries\git\versions\mingit-v2.56.0.windows.2"
set "PATH=%GIT_ROOT%\cmd;%GIT_ROOT%\mingw64\bin;%GIT_ROOT%\ucrt64\bin;%PATH%"
set "PROJ=C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\mountainriverechoes"
set "LOGDIR=C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\.workbuddy\logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
set "GCM_TRACE=%LOGDIR%\gcm_push.log"
set "GIT_TERMINAL_PROMPT=1"
set "GCM_INTERACTIVE=true"
cd /d "%PROJ%"

echo ================================================================
echo   Push mountainriverechoes to GitHub
echo ================================================================
echo.
echo  repo   : https://github.com/TZYY129/mountainriverechoes
echo  branch : master
echo.
echo  HOW TO SIGN IN  (needed only the first time):
echo    1. A code like ABCD-1234 will appear below.
echo    2. Open this page in your browser:  https://github.com/login/device
echo    3. Type the code and click the green Authorize button.
echo    4. Come back here - the upload starts by itself.
echo.

git add -A
git diff --cached --quiet
if errorlevel 1 goto do_commit
echo [skip]  nothing new to commit
goto auth

:do_commit
git commit -m "chore: manual backup" -q
echo [ok]    changes committed

:auth
echo.
echo ----------------------------------------------------------------
echo   Connecting to GitHub - a sign-in code will appear below
echo ----------------------------------------------------------------
echo.
echo   >>> COPY the code shown below, then open: https://github.com/login/device
echo.
git ls-remote --heads origin
if errorlevel 1 goto auth_failed
echo.
echo [ok]    GitHub login succeeded - credentials saved on this computer.
goto do_push

:auth_failed
echo.
echo [warn]  login not finished or GitHub unreachable - will still try to push

:do_push
echo.
echo ----------------------------------------------------------------
echo   Uploading (about 30 MB the first time, please wait)...
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
echo  Credentials are saved - future pushes will NOT ask for a code.
echo ================================================================
goto end

:push_failed
echo.
echo ================================================================
echo  [FAILED]  Push did not complete. Read the message above.
echo.
echo  A log file was saved here:
echo    %GCM_TRACE%
echo  Send that file to WorkBuddy for a check.
echo ================================================================

:end
echo.
pause
