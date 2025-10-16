# Remove Auto Mute from Windows startup

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Auto Mute - Remove from Startup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Get the Startup folder path
$startupFolder = [System.IO.Path]::Combine([Environment]::GetFolderPath('Startup'))
$shortcutPath = [System.IO.Path]::Combine($startupFolder, "Auto Mute.lnk")

# Check if shortcut exists
if (Test-Path $shortcutPath) {
    try {
        Remove-Item $shortcutPath -Force
        Write-Host "✓ Successfully removed Auto Mute from startup!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Auto Mute will no longer run automatically on login." -ForegroundColor Yellow
        Write-Host "You can still run it manually by double-clicking run_auto_mute.vbs" -ForegroundColor White
    } catch {
        Write-Host "✗ Error removing shortcut: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Auto Mute is not currently in startup folder." -ForegroundColor Yellow
    Write-Host "Nothing to remove." -ForegroundColor White
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
pause
