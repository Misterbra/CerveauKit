@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\windows.ps1" -Action InstallVideo
set "KIT_EXIT=%ERRORLEVEL%"
echo.
pause
exit /b %KIT_EXIT%
