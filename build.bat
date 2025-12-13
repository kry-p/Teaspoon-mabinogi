@echo off

:: Remove venv if it exists
if exist "venv" (
    rmdir /s /q "venv"
)

:: Remove executable if it exists
if exist "dist\Spoon.exe" (
    del /q "dist\Spoon.exe"
)

:: Create venv
python -m venv ./venv

:: Activate venv
if exist "./venv/Scripts/activate.bat" (
    call "./venv/Scripts/activate.bat"
) else (
    echo "Warning: Could not find activate.bat"
)

:: Install requirements
pip install -r requirements.txt

:: Run PyInstaller
pyinstaller Spoon.spec
