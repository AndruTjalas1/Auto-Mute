# Install Task Bar Icon Dependencies
# This script installs the required packages for the task bar icon feature

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Auto-Mute Task Bar Icon - Dependency Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check if pip is available
Write-Host "Checking pip installation..." -ForegroundColor Yellow
$pipVersion = pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip is not installed" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "Found: $pipVersion" -ForegroundColor Green
Write-Host ""

# Install new dependencies
Write-Host "Installing task bar icon dependencies..." -ForegroundColor Yellow
Write-Host "This will install: pystray and Pillow" -ForegroundColor Cyan
Write-Host ""

$confirm = Read-Host "Continue with installation? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "Installation cancelled." -ForegroundColor Yellow
    pause
    exit 0
}

Write-Host ""
Write-Host "Installing pystray..." -ForegroundColor Yellow
pip install pystray

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install pystray" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Installing Pillow..." -ForegroundColor Yellow
pip install Pillow

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install Pillow" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
$packages = pip list | Select-String -Pattern "pystray|Pillow"
if ($packages) {
    Write-Host "Installed packages:" -ForegroundColor Green
    Write-Host $packages -ForegroundColor Green
} else {
    Write-Host "WARNING: Could not verify package installation" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Run Auto-Mute with tray icon:" -ForegroundColor White
Write-Host "   python auto_mute.py --tray" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Or run in console mode (original):" -ForegroundColor White
Write-Host "   python auto_mute.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. For more information, see:" -ForegroundColor White
Write-Host "   - TASK_BAR_ICON_GUIDE.md (User guide)" -ForegroundColor Yellow
Write-Host "   - TASK_BAR_ICON_DOCS.md (Technical docs)" -ForegroundColor Yellow
Write-Host ""

pause
