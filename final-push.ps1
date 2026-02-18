# Final push to GitHub with template structure
$env:Path += ";C:\Program Files\Git\bin"

Write-Host "=== Pushing Umbrel App Store to GitHub ===" -ForegroundColor Cyan
Write-Host ""

# Add all changes
Write-Host "Adding all files..." -ForegroundColor Yellow
git add .

# Show status
Write-Host ""
Write-Host "Changes to commit:" -ForegroundColor Cyan
git status --short

# Commit
Write-Host ""
Write-Host "Committing..." -ForegroundColor Yellow
git commit -m "Setup Umbrel Community App Store template structure"

# Push
Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "=== Success! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Your app store is live at:" -ForegroundColor Cyan
Write-Host "https://github.com/AkaCurtis/BCH-Umbrel" -ForegroundColor White
Write-Host ""
Write-Host "To install on Umbrel:" -ForegroundColor Yellow
Write-Host "1. Open Umbrel dashboard" -ForegroundColor Gray
Write-Host "2. Go to App Store -> Settings" -ForegroundColor Gray
Write-Host "3. Add Community App Store" -ForegroundColor Gray
Write-Host "4. Enter: https://github.com/AkaCurtis/BCH-Umbrel" -ForegroundColor White
Write-Host "5. Install 'AxeBCH ATH Watcher'" -ForegroundColor Gray
Write-Host ""
Write-Host "App Store Structure:" -ForegroundColor Yellow
Write-Host "  umbrel-app-store.yml           - Store config (ID: akacurtis-apps)" -ForegroundColor Gray
Write-Host "  akacurtis-apps-axebch-watcher/ - Your app" -ForegroundColor Gray
Write-Host "  README.md                      - Documentation" -ForegroundColor Gray
Write-Host "  LICENSE                        - License file" -ForegroundColor Gray
