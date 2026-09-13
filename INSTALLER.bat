@echo off
chcp 65001 >nul
title Installation du Cerveau Kit
echo ============================================
echo    Installation du Cerveau Kit
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [!] Python introuvable.
    echo     Installez Python 3.11+ depuis https://python.org
    echo     ^(cochez "Add Python to PATH" pendant l'installation^), puis relancez ce fichier.
    pause
    exit /b 1
)

echo [1/3] Installation des dependances Python...
python -m pip install --quiet -r "%~dp0tools\tubescribe\requirements.txt"
if errorlevel 1 (
    echo [!] L'installation des dependances a echoue. Verifiez votre connexion internet.
    pause
    exit /b 1
)

where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo [2/3] ffmpeg introuvable — installation via winget...
    winget install -e --id Gyan.FFmpeg
    echo     Si ffmpeg vient d'etre installe, fermez cette fenetre et relancez INSTALLER.bat
    echo     pour que le systeme le trouve. Sinon, continuez.
) else (
    echo [2/3] ffmpeg : OK
)

echo [3/3] Configuration...
python "%~dp0tools\setup.py"
if errorlevel 1 (
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Installation terminee !
echo  1. Collez vos liens YouTube dans youtube.md
echo  2. Double-cliquez TRAITER-VIDEOS.bat
echo ============================================
pause
