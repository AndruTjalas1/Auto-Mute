# Check Auto Mute Status
# Shows if auto_mute.py is currently running

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Auto Mute - Status Check" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check for running processes
$pythonProcesses = Get-Process python* -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -like "*Personal*"
}

if ($pythonProcesses) {
    Write-Host "Status: RUNNING" -ForegroundColor Green
    Write-Host ""
    foreach ($proc in $pythonProcesses) {
        Write-Host "  Process ID: $($proc.Id)" -ForegroundColor White
        Write-Host "  Process Name: $($proc.ProcessName)" -ForegroundColor White
        Write-Host "  Started: $($proc.StartTime)" -ForegroundColor White
        Write-Host ""
    }
    Write-Host "Hotkey: Ctrl+Shift+M = Toggle ON/OFF" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To stop: Run stop_auto_mute.ps1" -ForegroundColor Cyan
} else {
    Write-Host "Status: NOT RUNNING" -ForegroundColor Red
    Write-Host ""
    Write-Host "To start: Double-click run_auto_mute.vbs" -ForegroundColor Yellow
    Write-Host "Auto-start: It will run automatically on next login" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
pause
