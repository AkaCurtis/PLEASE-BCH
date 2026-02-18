# Pre-Publishing Checklist

## Required Files
- [x] umbrel-app.yml - App manifest
- [x] docker-compose.yml - Container setup  
- [x] backend.py - Web UI
- [ ] watcher.py - Rename from watcher..py
- [x] icon.svg - App icon (256x256 recommended)
- [x] README.md - Documentation
- [x] .umbrelignore - Exclude unnecessary files

## Update Before Publishing

### umbrel-app.yml
- [ ] Change `developer: You` to your name/org
- [ ] Add `website` URL (optional but recommended)
- [ ] Add `repo` URL (will be your GitHub repo)
- [ ] Add `support` URL or email
- [ ] Consider adding screenshots to `gallery`

### README.md
- [ ] Update any repo-specific URLs
- [ ] Add screenshots of the web UI
- [ ] Test all instructions

### Testing
- [ ] Rename watcher..py to watcher.py
- [ ] Update docker-compose.yml reference if needed
- [ ] Test locally with Docker Compose first
- [ ] Verify all environment variables work
- [ ] Test Discord webhook integration

## Optional Enhancements
- [ ] Add LICENSE file (MIT recommended)
- [ ] Add CHANGELOG.md
- [ ] Create releases/tags for versioning
- [ ] Add app screenshots for gallery

## Security
- [ ] No hardcoded credentials
- [ ] Proper input validation in backend
- [ ] Safe file permissions in containers
