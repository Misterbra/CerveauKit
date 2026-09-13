@echo off
chcp 65001 >nul
title Cerveau Kit — traitement des videos
cd /d "%~dp0tools\tubescribe"
if not exist config.toml (
    echo [!] Configuration absente. Double-cliquez d'abord INSTALLER.bat
    pause
    exit /b 1
)
python -m tubescribe watch
echo.
echo Termine. Les notes sont dans raw\youtube\ ^(ouvrez-les avec Obsidian^).
pause
