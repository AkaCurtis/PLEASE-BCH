# Installation Guide

## Quick Install (Custom App Store)

### 1. Prepare Repository

First, rename the watcher file:
```powershell
Rename-Item "watcher..py" "watcher.py"
```

Update your info in `umbrel-app.yml`:
- Change `developer` to your name
- Add your `website`, `repo`, and `support` URLs

### 2. Push to GitHub

```powershell
# Initialize git (if not already done)
git init

# Add files
git add .

# Commit
git commit -m "Initial release: AxeBCH ATH Watcher v1.0.0"

# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/axebch-ath-watcher.git
git branch -M main
git push -u origin main
```

### 3. Add to Umbrel

1. Open your Umbrel dashboard
2. Navigate to **App Store**
3. Click the **gear/settings icon** (top right)
4. Select **Add App Store**
5. Enter your repository URL:
   ```
   https://github.com/YOUR_USERNAME/axebch-ath-watcher
   ```
6. Click **Add**
7. Find "AxeBCH ATH Watcher" in your Community App Stores section
8. Click **Install**

### 4. Configure

1. Once installed, open the app
2. Paste your Discord webhook URL
3. Adjust poll interval if desired (default 15 seconds)
4. Click **Save Settings**
5. Watch the status indicator turn green ✅

## Testing Locally First

Before installing on Umbrel, test with Docker Compose:

```powershell
# Set environment variables
$env:APP_DATA_DIR = "${PWD}"
$env:APP_PORT = "3001"
$env:UMBREL_APP_BASE = "http://your-pool-url:port"

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Open browser
Start-Process "http://localhost:3001"

# Stop when done
docker-compose down
```

## Repository Structure

Your GitHub repo should look like:
```
axebch-ath-watcher/
├── umbrel-app.yml          # Required: App manifest
├── docker-compose.yml      # Required: Container config
├── backend.py              # Required: Web UI
├── watcher.py              # Required: Monitoring script
├── icon.svg                # Required: App icon
├── README.md               # Recommended: Documentation
├── INSTALL.md              # This file
├── LICENSE                 # Recommended: MIT or similar
├── .gitignore              # Recommended
└── .umbrelignore           # Required: Package filter
```

## Troubleshooting

### App doesn't show up in Umbrel
- Check repository is public
- Verify `umbrel-app.yml` is valid YAML
- Check Umbrel logs: Settings → Show Debug Info

### Container fails to start
- Check docker-compose.yml syntax
- Verify volume mounts
- Review container logs in Umbrel

### Webhook not working
- Test webhook URL with curl first
- Check watcher container logs
- Verify Discord webhook permissions

### "Import yaml could not be resolved"
- This is just an IDE warning
- The containers install pyyaml at runtime
- Ignore unless you want to install locally

## Need Help?

1. Check container logs in Umbrel UI
2. SSH into Umbrel: `ssh umbrel@umbrel.local`  
3. View logs: `cd ~/umbrel/app-data/axebch-ath-watcher && docker-compose logs`
4. Open an issue on GitHub

## Updating the App

```powershell
# Make changes to your files
git add .
git commit -m "Update: description of changes"
git push

# Increment version in umbrel-app.yml
# Users can update through Umbrel UI
```
