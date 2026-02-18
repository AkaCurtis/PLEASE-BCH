from flask import Flask, request, jsonify, send_from_directory
import yaml
import os
import time

app = Flask(__name__)

SETTINGS_PATH = "/data/settings.yml"
STATE_PATH = "/data/state.json"

def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {"discord_webhook": "", "poll_seconds": 15, "umbrel_app_base": ""}
    with open(SETTINGS_PATH, "r") as f:
        data = yaml.safe_load(f) or {}
        # Ensure defaults
        data.setdefault("discord_webhook", "")
        data.setdefault("poll_seconds", 15)
        data.setdefault("umbrel_app_base", "")
        return data

def save_settings(data):
    with open(SETTINGS_PATH, "w") as f:
        yaml.dump(data, f)

@app.route("/api/settings", methods=["GET"])
def get_settings():
    return jsonify(load_settings())

@app.route("/api/settings", methods=["POST"])
def update_settings():
    data = request.json
    settings = load_settings()
    settings["discord_webhook"] = data.get("discord_webhook", "").strip()
    settings["poll_seconds"] = int(data.get("poll_seconds", 15))
    settings["umbrel_app_base"] = data.get("umbrel_app_base", "").strip()
    save_settings(settings)
    return jsonify({"status": "ok", "message": "Settings saved! Watcher will use new settings on next poll."})

@app.route("/api/status", methods=["GET"])
def get_status():
    """Check if watcher is working by looking at state file modification time"""
    try:
        if os.path.exists(STATE_PATH):
            mtime = os.path.getmtime(STATE_PATH)
            age_seconds = int(time.time() - mtime)
            return jsonify({
                "state_file_exists": True,
                "last_update_seconds_ago": age_seconds,
                "status": "running" if age_seconds < 60 else "possibly_stalled"
            })
        else:
            return jsonify({
                "state_file_exists": False,
                "status": "waiting_for_first_run"
            })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"})

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title>AxeBCH ATH Watcher - Settings</title>
        <style>
            * { box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                max-width: 600px;
                width: 100%;
            }
            h1 {
                margin: 0 0 8px 0;
                color: #1a202c;
                font-size: 28px;
                font-weight: 700;
            }
            .subtitle {
                color: #718096;
                margin: 0 0 32px 0;
                font-size: 14px;
            }
            .form-group {
                margin-bottom: 24px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #2d3748;
                font-weight: 600;
                font-size: 14px;
            }
            input, select {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
                transition: all 0.2s;
                font-family: inherit;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            .help-text {
                margin-top: 6px;
                font-size: 13px;
                color: #718096;
            }
            button {
                width: 100%;
                padding: 14px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            button:active {
                transform: translateY(0);
            }
            .alert {
                padding: 12px 16px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-size: 14px;
                display: none;
            }
            .alert-success {
                background: #c6f6d5;
                color: #22543d;
                border: 1px solid #9ae6b4;
            }
            .alert-error {
                background: #fed7d7;
                color: #742a2a;
                border: 1px solid #fc8181;
            }
            .status-badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                margin-top: 8px;
            }
            .status-running { background: #c6f6d5; color: #22543d; }
            .status-waiting { background: #feebc8; color: #7c2d12; }
            .status-error { background: #fed7d7; color: #742a2a; }
            .card {
                background: #f7fafc;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 24px;
            }
            .card h3 {
                margin: 0 0 12px 0;
                font-size: 16px;
                color: #2d3748;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ AxeBCH ATH Watcher</h1>
            <p class="subtitle">Configure Discord webhook alerts for worker all-time high shares</p>
            
            <div id="alert" class="alert"></div>
            
            <div class="card">
                <h3>📊 Watcher Status</h3>
                <div id="status">Checking...</div>
            </div>
            
            <form id="settingsForm" onsubmit="return false;">
                <div class="form-group">
                    <label for="webhook">Discord Webhook URL *</label>
                    <input 
                        type="url" 
                        id="webhook" 
                        placeholder="https://discord.com/api/webhooks/..." 
                        required
                    />
                    <div class="help-text">
                        📌 <a href="https://support.discord.com/hc/en-us/articles/228383668" target="_blank" style="color: #667eea;">How to create a Discord webhook</a>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="poll_seconds">Poll Interval (seconds)</label>
                    <input 
                        type="number" 
                        id="poll_seconds" 
                        min="5" 
                        max="300" 
                        value="15"
                    />
                    <div class="help-text">How often to check for new worker records (5-300 seconds)</div>
                </div>
                
                <div class="form-group">
                    <label for="umbrel_app_base">Pool API Base URL (optional)</label>
                    <input 
                        type="url" 
                        id="umbrel_app_base" 
                        placeholder="http://umbrel.local:21212"
                    />
                    <div class="help-text">Leave empty to use default. Only change if you know what you're doing.</div>
                </div>
                
                <button type="submit" onclick="save()">💾 Save Settings</button>
            </form>
        </div>
        
        <script>
            function showAlert(message, type) {
                const alert = document.getElementById('alert');
                alert.className = 'alert alert-' + type;
                alert.textContent = message;
                alert.style.display = 'block';
                setTimeout(() => { alert.style.display = 'none'; }, 5000);
            }
            
            async function loadSettings() {
                try {
                    const res = await fetch('/api/settings');
                    const data = await res.json();
                    document.getElementById('webhook').value = data.discord_webhook || '';
                    document.getElementById('poll_seconds').value = data.poll_seconds || 15;
                    document.getElementById('umbrel_app_base').value = data.umbrel_app_base || '';
                } catch (e) {
                    showAlert('Failed to load settings: ' + e.message, 'error');
                }
            }
            
            async function loadStatus() {
                try {
                    const res = await fetch('/api/status');
                    const data = await res.json();
                    const statusDiv = document.getElementById('status');
                    
                    if (data.status === 'running') {
                        statusDiv.innerHTML = `
                            <span class="status-badge status-running">✅ Running</span>
                            <div class="help-text" style="margin-top: 8px;">Last activity: ${data.last_update_seconds_ago}s ago</div>
                        `;
                    } else if (data.status === 'waiting_for_first_run') {
                        statusDiv.innerHTML = `
                            <span class="status-badge status-waiting">⏳ Waiting for first poll</span>
                            <div class="help-text" style="margin-top: 8px;">Watcher is starting up...</div>
                        `;
                    } else if (data.status === 'possibly_stalled') {
                        statusDiv.innerHTML = `
                            <span class="status-badge status-error">⚠️ Possibly Stalled</span>
                            <div class="help-text" style="margin-top: 8px;">Last activity: ${data.last_update_seconds_ago}s ago. Check logs.</div>
                        `;
                    } else {
                        statusDiv.innerHTML = `<span class="status-badge status-error">❌ Unknown</span>`;
                    }
                } catch (e) {
                    document.getElementById('status').innerHTML = 
                        '<span class="status-badge status-error">❌ Error loading status</span>';
                }
            }
            
            async function save() {
                const webhook = document.getElementById('webhook').value.trim();
                const poll_seconds = parseInt(document.getElementById('poll_seconds').value);
                const umbrel_app_base = document.getElementById('umbrel_app_base').value.trim();
                
                if (!webhook) {
                    showAlert('Discord webhook URL is required!', 'error');
                    return;
                }
                
                if (!webhook.startsWith('https://discord.com/api/webhooks/')) {
                    showAlert('Invalid Discord webhook URL format!', 'error');
                    return;
                }
                
                try {
                    const res = await fetch('/api/settings', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            discord_webhook: webhook,
                            poll_seconds: poll_seconds,
                            umbrel_app_base: umbrel_app_base
                        })
                    });
                    const data = await res.json();
                    showAlert(data.message || '✅ Settings saved successfully!', 'success');
                    loadStatus();
                } catch (e) {
                    showAlert('Failed to save: ' + e.message, 'error');
                }
            }
            
            // Load on page load
            loadSettings();
            loadStatus();
            
            // Refresh status every 10 seconds
            setInterval(loadStatus, 10000);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)
