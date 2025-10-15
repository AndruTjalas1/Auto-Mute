# Restart Auto Mute Script
# Stops any running instances and starts a fresh one

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Restarting Auto Mute" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Stop any running instances
Write-Host "Step 1: Stopping existing processes..." -ForegroundColor Yellow
$processes = Get-Process pythonw,python -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -like "*Personal*"
}

if ($processes) {
    $processes | Stop-Process -Force
    Write-Host "  Stopped $($processes.Count) process(es)" -ForegroundColor Green
    Start-Sleep -Seconds 1
} else {
    Write-Host "  No existing processes found" -ForegroundColor Gray
}

# Start new instance
Write-Host ""
Write-Host "Step 2: Starting Auto Mute with admin rights..." -ForegroundColor Yellow

# Check if VBS launcher exists
if (Test-Path "C:\Personal\run_auto_mute_admin.vbs") {
    Start-Process -FilePath "C:\Personal\run_auto_mute_admin.vbs" -Verb RunAs
    Write-Host "  Auto Mute started with admin rights!" -ForegroundColor Green
    Write-Host "  Hotkey (Ctrl+Shift+M) will work" -ForegroundColor Cyan
} elseif (Test-Path "C:\Personal\run_auto_mute.vbs") {
    Start-Process -FilePath "C:\Personal\run_auto_mute.vbs"
    Write-Host "  Auto Mute started (without admin rights)" -ForegroundColor Green
    Write-Host "  Note: Hotkey may not work without admin" -ForegroundColor Yellow
} else {
    Write-Host "  Error: Could not find launcher script" -ForegroundColor Red
    Write-Host "  Try running manually: python auto_mute.py" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Restart Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The script is now running in the background." -ForegroundColor White
Write-Host "Press Ctrl+Shift+M to toggle Auto Mute ON/OFF" -ForegroundColor Cyan
Write-Host ""
pause
