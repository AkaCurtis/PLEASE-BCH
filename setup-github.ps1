# Quick setup script for publishing to GitHub

Write-Host "=== AxeBCH ATH Watcher - GitHub Setup ===" -ForegroundColor Green
Write-Host ""

# Step 1: Rename watcher file
if (Test-Path "watcher..py") {
    Write-Host "[1/5] Renaming watcher..py to watcher.py..." -ForegroundColor Yellow
    Rename-Item "watcher..py" "watcher.py" -ErrorAction SilentlyContinue
    Write-Host "  ✓ Done" -ForegroundColor Green
} else {
    Write-Host "[1/5] watcher.py already exists" -ForegroundColor Green
}

# Step 2: Check git
Write-Host ""
Write-Host "[2/5] Checking git..." -ForegroundColor Yellow
$gitExists = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitExists) {
    Write-Host "  ✗ Git not found! Please install Git first." -ForegroundColor Red
    Write-Host "  Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ Git found" -ForegroundColor Green

# Step 3: Initialize repo
Write-Host ""
Write-Host "[3/5] Initializing git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "  ✓ Repository initialized" -ForegroundColor Green
} else {
    Write-Host "  ✓ Repository already initialized" -ForegroundColor Green
}

# Step 4: Get user info
Write-Host ""
Write-Host "[4/5] Configuration" -ForegroundColor Yellow
Write-Host ""

$username = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter repository name (default: axebch-ath-watcher)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "axebch-ath-watcher"
}

$developerName = Read-Host "Enter your name for umbrel-app.yml (default: $username)"
if ([string]::IsNullOrWhiteSpace($developerName)) {
    $developerName = $username
}

Write-Host ""
Write-Host "  Repository: https://github.com/$username/$repoName" -ForegroundColor Cyan

# Step 5: Update umbrel-app.yml
Write-Host ""
Write-Host "[5/5] Updating umbrel-app.yml..." -ForegroundColor Yellow

$umbrelConfig = Get-Content "umbrel-app.yml" -Raw
$umbrelConfig = $umbrelConfig -replace 'developer: You', "developer: $developerName"
$umbrelConfig = $umbrelConfig -replace 'repo: ""', "repo: `"https://github.com/$username/$repoName`""
$umbrelConfig = $umbrelConfig -replace 'support: ""', "support: `"https://github.com/$username/$repoName/issues`""
Set-Content "umbrel-app.yml" $umbrelConfig
Write-Host "  ✓ Updated" -ForegroundColor Green

# Final instructions
Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Green
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host "   - Name: $repoName" -ForegroundColor Gray
Write-Host "   - Public repository" -ForegroundColor Gray
Write-Host "   - Don't initialize with README" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Run these commands:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Cyan
Write-Host "   git commit -m `"Initial release: AxeBCH ATH Watcher v1.0.0`"" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/$username/$repoName.git" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""

Write-Host "3. Install on Umbrel:" -ForegroundColor White
Write-Host "   - Open Umbrel App Store" -ForegroundColor Gray
Write-Host "   - Click Settings (gear icon)" -ForegroundColor Gray
Write-Host "   - Add App Store" -ForegroundColor Gray
Write-Host "   - Enter: https://github.com/$username/$repoName" -ForegroundColor Cyan
Write-Host "   - Install your app!" -ForegroundColor Gray
Write-Host ""

Write-Host "=== Files Ready ===" -ForegroundColor Green
Write-Host "✓ umbrel-app.yml" -ForegroundColor Gray
Write-Host "✓ docker-compose.yml" -ForegroundColor Gray
Write-Host "✓ backend.py" -ForegroundColor Gray
Write-Host "✓ watcher.py" -ForegroundColor Gray
Write-Host "✓ icon.svg" -ForegroundColor Gray
Write-Host "✓ README.md" -ForegroundColor Gray
Write-Host "✓ LICENSE" -ForegroundColor Gray
Write-Host "✓ INSTALL.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Ready to publish! 🚀" -ForegroundColor Green
