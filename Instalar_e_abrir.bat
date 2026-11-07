@echo off
title Beyond Nen Fishing
cd /d "%~dp0"
echo Instalando dependencias...
py -m pip install opencv-python mss numpy pyautogui keyboard pillow
if errorlevel 1 (
    echo.
    echo Erro ao instalar dependencias. Instale Python 3 para Windows e tente novamente.
    pause
    exit /b 1
)
echo Abrindo Beyond Nen Fishing...
py beyond_nen_app.py
pause
