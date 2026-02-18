# Setup Without Git Command Line

If you don't have git installed, use **GitHub Desktop** instead!

## Step 1: Install GitHub Desktop

1. Download: https://desktop.github.com/
2. Install and sign in with your GitHub account

## Step 2: Create Repository

In GitHub Desktop:
1. Click **File** → **New Repository**
2. Name: `axebch-ath-watcher`
3. Local Path: Browse to `D:\BCH dash`
4. Click **Create Repository**

## Step 3: Publish

1. Review the files in the left sidebar
2. Add commit message: "Initial release: AxeBCH ATH Watcher v1.0.0"
3. Click **Commit to main**
4. Click **Publish repository** button at top
5. Make sure "Keep this code private" is **unchecked** (needs to be public)
6. Click **Publish**

## Step 4: Get Your Repo URL

Your repository will be at:
```
https://github.com/YOUR_USERNAME/axebch-ath-watcher
```

## Step 5: Install on Umbrel

1. Open Umbrel dashboard
2. Go to **App Store** → **Settings** (gear icon)
3. Click **Add App Store**
4. Enter your repo URL: `https://github.com/YOUR_USERNAME/axebch-ath-watcher`
5. Find and install your app!

---

## Alternative: Upload Files via GitHub Web

If you don't want to install anything:

1. Go to https://github.com/new
2. Create repository: `axebch-ath-watcher` (public)
3. Click **uploading an existing file**
4. Drag and drop these files:
   - umbrel-app.yml
   - docker-compose.yml
   - backend.py
   - watcher.py (rename from watcher..py first!)
   - icon.svg
   - README.md
   - LICENSE
   - .umbrelignore
5. Commit files
6. Use the repo URL in Umbrel

**Note**: If using web upload, manually rename `watcher..py` to `watcher.py` first!
