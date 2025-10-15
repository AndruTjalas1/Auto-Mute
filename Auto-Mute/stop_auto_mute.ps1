# Stop Auto Mute Script# Stop Auto Mute Script

# This script stops any running auto_mute.py processes# This script stops any running auto_mute.py processes



Write-Host "======================================" -ForegroundColor CyanWrite-Host "Searching for auto_mute.py processes..." -ForegroundColor Yellow

Write-Host "  Stopping Auto Mute" -ForegroundColor Cyan

Write-Host "======================================" -ForegroundColor Cyan$processes = Get-Process pythonw -ErrorAction SilentlyContinue | Where-Object {

Write-Host ""    $_.Path -like "*Personal*"

}

Write-Host "Searching for auto_mute.py processes..." -ForegroundColor Yellow

if ($processes) {

$processes = Get-Process pythonw,python -ErrorAction SilentlyContinue | Where-Object {    Write-Host "Found $($processes.Count) process(es). Stopping..." -ForegroundColor Green

    $_.Path -like "*Personal*"    $processes | Stop-Process -Force

}    Write-Host "✓ Auto Mute stopped successfully!" -ForegroundColor Green

} else {

if ($processes) {    Write-Host "No auto_mute.py processes found running." -ForegroundColor Cyan

    Write-Host "Found $($processes.Count) process(es). Stopping..." -ForegroundColor Green}

    $processes | Stop-Process -Force

    Write-Host "Auto Mute stopped successfully!" -ForegroundColor Greenpause

} else {
    Write-Host "No auto_mute.py processes found running." -ForegroundColor Cyan
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
pause
