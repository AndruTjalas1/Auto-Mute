# Setup Auto Mute to run on Windows startup
# This script creates a shortcut in the Windows Startup folder

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Auto Mute - Startup Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Get the Startup folder path
$startupFolder = [System.IO.Path]::Combine([Environment]::GetFolderPath('Startup'))
Write-Host "Startup folder: $startupFolder" -ForegroundColor Yellow

# Path to the VBS script
$vbsScriptPath = "C:\Personal\run_auto_mute.vbs"
$shortcutPath = [System.IO.Path]::Combine($startupFolder, "Auto Mute.lnk")

# Check if VBS file exists
if (-not (Test-Path $vbsScriptPath)) {
    Write-Host "Error: run_auto_mute.vbs not found!" -ForegroundColor Red
    Write-Host "  Expected location: $vbsScriptPath" -ForegroundColor Red
    pause
    exit 1
}

# Create shortcut
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $vbsScriptPath
    $Shortcut.WorkingDirectory = "C:\Personal"
    $Shortcut.Description = "Auto Mute - Automatically mutes system audio on schedule"
    $Shortcut.Save()
    
    Write-Host "Successfully created startup shortcut!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Auto Mute will now run automatically when you log in to Windows." -ForegroundColor Green
    Write-Host ""
    Write-Host "Shortcut location:" -ForegroundColor Yellow
    Write-Host "  $shortcutPath" -ForegroundColor White
    Write-Host ""
    Write-Host "To disable autostart:" -ForegroundColor Yellow
    Write-Host "  1. Press Win+R" -ForegroundColor White
    Write-Host "  2. Type: shell:startup" -ForegroundColor White
    Write-Host "  3. Delete the Auto Mute shortcut" -ForegroundColor White
    Write-Host ""
    Write-Host "Or run: remove_autostart.ps1" -ForegroundColor Cyan
    
} catch {
    Write-Host "Error creating shortcut: $_" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
pause
