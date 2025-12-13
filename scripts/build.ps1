# Create venv if it doesn't exist (re-creating it is cleaner but let's follow the simple shell script style of just running it)
python -m venv ./venv

# Activate venv
# In PowerShell, activation script is in venv/Scripts/Activate.ps1
if (Test-Path "./venv/Scripts/Activate.ps1") {
    & "./venv/Scripts/Activate.ps1"
} elseif (Test-Path "./venv/bin/Activate.ps1") {
    # Non-standard or POSIX-like layout on Windows? usually Scripts
    & "./venv/bin/Activate.ps1"
} else {
    Write-Host "Could not find activation script. Continuing with system python might fail."
}

# Install requirements
pip install -r ../requirements.txt

# Run PyInstaller
pyinstaller ../Spoon.spec
