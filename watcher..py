import os
import time
import json
import requests
from typing import Any, Dict, List, Optional
import yaml


def load_settings():
    """Load settings from the settings file"""
    try:
        with open("/data/settings.yml", "r") as f:
            return yaml.safe_load(f) or {}
    except:
        return {}

def get_webhook():
    """Get Discord webhook from settings"""
    return load_settings().get("discord_webhook", "")

def get_poll_seconds():
    """Get poll interval from settings, fallback to env var"""
    settings = load_settings()
    if "poll_seconds" in settings:
        return int(settings["poll_seconds"])
    return int(os.getenv("POLL_SECONDS", "15"))

def get_base_url():
    """Get base URL from settings, fallback to env var"""
    settings = load_settings()
    if "umbrel_app_base" in settings and settings["umbrel_app_base"]:
        return settings["umbrel_app_base"].rstrip("/")
    return os.getenv("UMBREL_APP_BASE", "http://umbrel.local:21212").rstrip("/")


BASE = get_base_url()
PROXY_TOKEN = os.getenv("UMBREL_PROXY_TOKEN", "").strip()

STATE_FILE = os.getenv("STATE_FILE", "/data/state.json")

# Note: PROXY_TOKEN check removed - will work without it
# Webhook is checked dynamically via get_webhook()
# BASE URL and POLL_SECONDS can be overridden in settings


def get_pool_url():
    """Get pool URL dynamically"""
    return f"{get_base_url()}/api/pool"

def get_workers_url():
    """Get workers URL dynamically"""
    return f"{get_base_url()}/api/pool/workers"


def load_state() -> Dict[str, Any]:
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def save_state(state: Dict[str, Any]) -> None:
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_FILE)


def get_json(url: str) -> Dict[str, Any]:
    cookies = {"UMBREL_PROXY_TOKEN": PROXY_TOKEN} if PROXY_TOKEN else None

    r = requests.get(
        url,
        cookies=cookies,
        headers={"Accept": "application/json"},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, dict) else {"_raw": data}



def format_mining_number(value: int) -> str:
    try:
        num = float(value)
    except Exception:
        return str(value)

    units = ["", "K", "M", "G", "T", "P", "E"]
    index = 0

    while num >= 1000 and index < len(units) - 1:
        num /= 1000.0
        index += 1

    if index == 0:
        return f"{int(num)}"
    return f"{num:.2f}{units[index]}"

def progress_bar(ratio: float, width: int = 16) -> str:
    """
    ratio: 0.0 to 1.0+
    returns: bar like █████░░░░░ plus percent
    """
    if ratio < 0:
        ratio = 0.0
    filled = int(min(ratio, 1.0) * width)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    pct = min(ratio, 1.0) * 100
    return f"`{bar}` **{pct:.2f}%**"


from datetime import datetime, timezone

def discord_post_ath(display, bestever, worker_data, pool_data):
    embed_color = 706958  # BCH green

    best_formatted = format_mining_number(bestever)

    net_diff = pool_data.get("network_difficulty")
    diff_int = None
    diff_formatted = "—"

    try:
        if net_diff is not None:
            diff_int = int(float(net_diff))
            diff_formatted = format_mining_number(diff_int)
    except Exception:
        diff_int = None

    # Progress = best share / difficulty
    ratio = 0.0
    if diff_int and diff_int > 0:
        ratio = float(bestever) / float(diff_int)

    bar_text = progress_bar(ratio, width=18)

    height = pool_data.get("network_height")
    eta_text = pool_data.get("eta_text")

    fields = [
        {"name": "🏷 Worker", "value": f"**{display}**", "inline": True},
        {"name": "🎯 Best Share", "value": f"`{best_formatted}`", "inline": True},
        {"name": "⛏ Block Diff", "value": f"`{diff_formatted}`", "inline": True},
        {"name": "📈 Progress to Block", "value": bar_text, "inline": False},
    ]

    if height is not None:
        fields.append({"name": "📏 Height", "value": f"`{height}`", "inline": True})

    if eta_text:
        fields.append({"name": "⏳ ETA", "value": f"`{eta_text}`", "inline": True})

    if worker_data.get("lastshare_ago_s") is not None:
        fields.append({
            "name": "⏱ Last Share Ago",
            "value": f"`{worker_data.get('lastshare_ago_s')}s`",
            "inline": True
        })

    payload = {
        "username": "AxeBCH",
        "embeds": [{
            "title": "🔥 NEW WORKER ATH!",
            "description": f"**{display}** just hit a new best share!",
            "color": embed_color,
            "thumbnail": {"url": "https://cryptologos.cc/logos/bitcoin-cash-bch-logo.png"},
            "fields": fields,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "footer": {"text": "AxeBCH Solo Node"},
        }]
    }

    webhook = get_webhook()
    if not webhook:
        return

    r = requests.post(webhook, json=payload, timeout=15)
    r.raise_for_status()



def pretty_worker_name(workername: str) -> str:
    # Take substring after the first dot, trim, normalize spaces, title-case
    if not workername:
        return "Unknown"
    suffix = workername.split(".", 1)[1] if "." in workername else workername
    suffix = " ".join(suffix.strip().split())
    return suffix.title() if suffix else "Unknown"


def main():
    state = load_state()

    # Persisted map: { "<raw workername>": bestever_int }
    last_bestever: Dict[str, int] = state.get("last_bestever", {})
    if not isinstance(last_bestever, dict):
        last_bestever = {}
    
    print("[watcher] Starting AxeBCH ATH Watcher...")
    print(f"[watcher] Base URL: {get_base_url()}")
    print(f"[watcher] State file: {STATE_FILE}")

    while True:
        try:
            # Get dynamic settings
            poll_seconds = get_poll_seconds()
            webhook = get_webhook()
            
            if not webhook:
                print("[watcher] No Discord webhook configured. Waiting...")
                time.sleep(30)
                continue
            
            # Fetch both workers and pool data
            data = get_json(get_workers_url())
            details = data.get("workers_details", [])
            if not isinstance(details, list):
                details = []

            pool_data = get_json(get_pool_url())

            # Track updates, then save once per loop
            changed = False

            for w in details:
                if not isinstance(w, dict):
                    continue

                raw_name = str(w.get("workername", "")).strip()
                if not raw_name:
                    continue

                # bestever might be null; ignore if missing
                bestever = w.get("bestever", None)
                if bestever is None:
                    continue

                try:
                    bestever_int = int(bestever)
                except Exception:
                    continue

                prev = last_bestever.get(raw_name)

                # First time seeing this worker: record but don't notify (prevents spam on first run)
                if prev is None:
                    last_bestever[raw_name] = bestever_int
                    changed = True
                    continue

                # Notify ONLY when it increases
                if bestever_int > int(prev):
                    display = pretty_worker_name(raw_name)

                    # Send Discord notification
                    discord_post_ath(display, bestever_int, w, pool_data)

                    last_bestever[raw_name] = bestever_int
                    changed = True

            if changed:
                save_state({"last_bestever": last_bestever})

            print(f"[poll] workers={len(details)} state_saved={changed} webhook_configured={bool(webhook)}")

        except Exception as e:
            print(f"[poll] error: {e}")
            poll_seconds = get_poll_seconds()

        time.sleep(poll_seconds)


if __name__ == "__main__":
    main()
