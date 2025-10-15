# Create Desktop Shortcut for Auto Mute Configuration GUI

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Creating Desktop Shortcut" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Get desktop path
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "Auto Mute Config.lnk"

# VBS launcher path
$vbsPath = "C:\Personal\configure_schedule.vbs"

# Check if VBS exists
if (-not (Test-Path $vbsPath)) {
    Write-Host "Error: configure_schedule.vbs not found!" -ForegroundColor Red
    pause
    exit 1
}

try {
    # Create shortcut
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $vbsPath
    $Shortcut.WorkingDirectory = "C:\Personal"
    $Shortcut.Description = "Configure Auto Mute Schedule"
    $Shortcut.IconLocation = "shell32.dll,165"  # Settings gear icon
    $Shortcut.Save()
    
    Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Location: $shortcutPath" -ForegroundColor White
    Write-Host ""
    Write-Host "You can now double-click 'Auto Mute Config' on your desktop!" -ForegroundColor Cyan
    
} catch {
    Write-Host "Error creating shortcut: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
pause
