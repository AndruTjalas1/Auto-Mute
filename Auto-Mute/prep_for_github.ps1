# Quick Setup Script for GitHub Upload

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Auto Mute - GitHub Prep" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
$currentPath = Get-Location
if ($currentPath.Path -ne "C:\Personal") {
    Write-Host "Please run this script from C:\Personal" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Step 1: Replacing README with GitHub version..." -ForegroundColor Yellow
if (Test-Path "README.md") {
    Remove-Item "README.md" -Force
    Write-Host "  Removed local README.md" -ForegroundColor Gray
}
if (Test-Path "README_GITHUB.md") {
    Rename-Item "README_GITHUB.md" "README.md"
    Write-Host "  Renamed README_GITHUB.md to README.md" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Checking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "auto_mute.py",
    "config_gui.py",
    "config.example.json",
    "requirements.txt",
    "LICENSE",
    ".gitignore",
    "CONTRIBUTING.md"
)

$allPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $file" -ForegroundColor Red
        $allPresent = $false
    }
}

if (-not $allPresent) {
    Write-Host ""
    Write-Host "Some required files are missing!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Step 3: Initializing Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "  Git already initialized" -ForegroundColor Gray
} else {
    git init
    Write-Host "  Git initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 4: Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "  Files staged" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Auto Mute application with GUI and hotkey support"
Write-Host "  Commit created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 6: Connecting to GitHub..." -ForegroundColor Yellow
git remote add origin https://github.com/AndruTjalas1/Auto-Mute.git 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Remote already exists, updating..." -ForegroundColor Gray
    git remote set-url origin https://github.com/AndruTjalas1/Auto-Mute.git
}
Write-Host "  Remote configured" -ForegroundColor Green

Write-Host ""
Write-Host "Step 7: Setting main branch..." -ForegroundColor Yellow
git branch -M main
Write-Host "  Branch set to 'main'" -ForegroundColor Green

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Ready to Push!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To push to GitHub, run:" -ForegroundColor Yellow
Write-Host "  git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "If this is your first push, you may need to authenticate." -ForegroundColor Cyan
Write-Host ""

$response = Read-Host "Push to GitHub now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Success! Your project is now on GitHub!" -ForegroundColor Green
        Write-Host "View at: https://github.com/AndruTjalas1/Auto-Mute" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "Push failed. You may need to authenticate or check your connection." -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "Skipped push. Run manually when ready:" -ForegroundColor Yellow
    Write-Host "  git push -u origin main" -ForegroundColor White
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Add a screenshot to screenshots/config_gui.png" -ForegroundColor White
Write-Host "  2. Review your repository on GitHub" -ForegroundColor White
Write-Host "  3. Add topics in repository settings" -ForegroundColor White
Write-Host ""
pause
