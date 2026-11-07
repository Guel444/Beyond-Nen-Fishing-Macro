@echo off
title Gerar EXE - Beyond Nen Fishing
cd /d "%~dp0"
py -m pip install opencv-python mss numpy pyautogui keyboard pillow pyinstaller
if errorlevel 1 (
    echo Erro ao instalar dependencias.
    pause
    exit /b 1
)
py -m PyInstaller --onefile --noconsole --name BeyondNenFishing --collect-all cv2 --collect-all mss beyond_nen_app.py
echo.
echo O executavel, se criado, ficara na pasta dist.
pause
