Remove-Item -Path "venv" -Recurse -Force -ErrorAction SilentlyContinue # Remove venv if it exists
Remove-Item -Path "dist\Spoon.exe" -Force -ErrorAction SilentlyContinue # Remove executable if it exists

python -m venv ./venv # Create venv

# Activate venv
# In PowerShell, activation script is in venv/Scripts/Activate.ps1
if (Test-Path "./venv/Scripts/Activate.ps1") {
    & "./venv/Scripts/Activate.ps1"
} elseif (Test-Path "./venv/bin/Activate.ps1") {
    # Non-standard or POSIX-like layout on Windows usually Scripts
    & "./venv/bin/Activate.ps1"
} else {
    Write-Host "Could not find activation script. Continuing with system python might fail."
}


pip install -r requirements.txt # Install requirements
pyinstaller Spoon.spec # Run PyInstaller
