# -*- mode: python ; coding: utf-8 -*-
# One-file Windows build. The fishing logic remains in beyond_nen_app.py.

from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = [
    "pyautogui._pyautogui_win",
    "mouseinfo",
    "pyscreeze",
    "pymsgbox",
    "pytweening",
    "keyboard",
    "mss",
    "PIL",
]

for package in ("cv2", "mss", "pyautogui", "keyboard", "PIL"):
    package_datas, package_binaries, package_hiddenimports = collect_all(package)
    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_hiddenimports

a = Analysis(
    ["beyond_nen_app.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="BeyondNenFishing",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
)
