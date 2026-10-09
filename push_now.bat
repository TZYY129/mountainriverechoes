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
echo  (first push uploads about 30 MB of data, please wait)
echo.

git add -A
git diff --cached --quiet
if errorlevel 1 goto do_commit
echo [skip]  nothing new to commit
goto do_push

:do_commit
git commit -m "chore: manual backup" -q
if errorlevel 1 (
  echo [warn]  commit failed
) else (
  echo [ok]    changes committed
)

:do_push
echo.
echo ----------------------------------------------------------------
echo  git will now ask for credentials:
echo      Username :  TZYY129
echo      Password :  paste your GitHub token (starts with ghp_) and press Enter
echo  NOTE: when typing the password nothing appears on screen. That is normal.
echo ----------------------------------------------------------------
echo.

git config credential.helper store
git push -u origin master

if errorlevel 1 goto push_failed

echo.
echo ================================================================
echo  [OK]  Pushed successfully.
echo  Credentials saved - next time it will not ask again.
echo ================================================================
goto end

:push_failed
echo.
echo ================================================================
echo  [FAILED]  Push did not complete. Read the message above.
echo.
echo  Common reasons:
echo    - token copied wrongly (should start with ghp_ and be one line)
echo    - no network access to github.com
echo    - token missing the "repo" scope
echo ================================================================

:end
echo.
pause
