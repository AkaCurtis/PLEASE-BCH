# AxeBCH ATH Watcher - Umbrel App

Discord webhook notifications when mining workers hit new all-time high shares!

## 🚀 What This Does

This Umbrel app monitors your AxeBCH mining pool workers and automatically sends a beautiful Discord notification whenever any worker achieves a new all-time best share. 

## 📦 Installation

1. Copy this entire folder to your Umbrel app directory or app store
2. Install the app through Umbrel's interface
3. Open the app and configure your Discord webhook URL

## ⚙️ Configuration

### Getting a Discord Webhook URL

1. Open Discord and go to your server
2. Go to **Server Settings** → **Integrations** → **Webhooks**
3. Click **New Webhook** or edit an existing one
4. Copy the **Webhook URL**
5. Paste it into the AxeBCH ATH Watcher configuration page

### Settings Explained

- **Discord Webhook URL** (Required): Where notifications will be sent
- **Poll Interval**: How often to check for new records (5-300 seconds, default: 15)
- **Pool API Base URL**: Only change if your pool API is at a custom location

## 📊 Features

- ✅ **Web-based Configuration** - No need to edit config files or environment variables
- ✅ **Live Status Monitoring** - See if the watcher is running properly
- ✅ **Beautiful Discord Embeds** - Rich notifications with progress bars and stats
- ✅ **Smart Detection** - Only notifies on NEW all-time highs, not every share
- ✅ **Multi-Worker Support** - Tracks all workers independently
- ✅ **Persistent State** - Remembers records across restarts

## 🐳 Docker Services

The app runs two containers:

1. **backend** - Flask web server for the configuration UI (port 3001)
2. **watcher** - Python script that polls the pool API and sends Discord notifications

## 📁 File Structure

```
.
├── umbrel-app.yml          # App manifest
├── docker-compose.yml      # Container configuration
├── backend.py              # Web UI and API
├── watcher.py              # Main monitoring script
├── icon.svg                # App icon
└── README.md              # This file
```

## 🔧 Environment Variables (Optional)

You can override these in `docker-compose.yml` if needed:

- `UMBREL_APP_BASE` - Pool API base URL (default: http://umbrel.local:21212)
- `UMBREL_PROXY_TOKEN` - Auth token for pool API (if required)
- `POLL_SECONDS` - Fallback poll interval if not set in web UI
- `STATE_FILE` - Where to store worker records (default: /data/state.json)

## 🐛 Troubleshooting

### "Webhook not configured" in logs

- Open the web UI and enter your Discord webhook URL
- Click Save and wait up to 30 seconds

### "Possibly Stalled" status

- Check the Docker logs: `docker logs axebch-ath-watcher_watcher_1`
- Verify your pool API URL is correct
- Ensure the pool API is accessible from the container

### No notifications being sent

- Test your Discord webhook URL directly with curl
- Check that workers are actually mining and setting new records
- Review watcher logs for errors

## 📝 Notes

- The first time a worker is seen, its current best share is recorded but no notification is sent
- Notifications are only sent when a worker IMPROVES their personal best
- State is persisted in `/data/state.json` and shared between container restarts

## 💚 BCH Green

Made for Bitcoin Cash (BCH) solo mining enthusiasts! 

---

**Need help?** Check the logs or open an issue in the repository.
