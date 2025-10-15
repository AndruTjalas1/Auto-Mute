# Stop Auto Mute Script
# This script stops any running auto_mute.py processes

Write-Host "Searching for auto_mute.py processes..." -ForegroundColor Yellow

$processes = Get-Process pythonw -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -like "*Personal*"
}

if ($processes) {
    Write-Host "Found $($processes.Count) process(es). Stopping..." -ForegroundColor Green
    $processes | Stop-Process -Force
    Write-Host "✓ Auto Mute stopped successfully!" -ForegroundColor Green
} else {
    Write-Host "No auto_mute.py processes found running." -ForegroundColor Cyan
}

pause
