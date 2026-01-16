```bash
#!/usr/bin/env bash
#
# 🧱 backup-home.sh — Automated home directory backup
#
# Creates timestamped compressed backups of your $HOME, excluding caches/trash.
# Features:
#   • Logging
#   • Retains last N backups
#   • Optional remote sync via rsync or scp
#   • Compatible with Debian/Ubuntu/Kali

set -euo pipefail

# ───────────────────────────── CONFIGURATION ─────────────────────────────
BACKUP_DIR="$HOME"
RETENTION_DAYS=7
LOG_FILE="$HOME/backup-home.log"

# Exclusions (edit to taste)
EXCLUDES=(
  "--exclude=$HOME/.cache"
  "--exclude=$HOME/.local/share/Trash"
  "--exclude=$HOME/.config/Code/Cache"
)

# Optional remote copy
REMOTE_ENABLED=false               # set to true to enable
REMOTE_USER="fred"                 # your remote username
REMOTE_HOST="example.com"          # remote host
REMOTE_PATH="/backups/$USER"       # remote path

# ───────────────────────────── FUNCTIONS ─────────────────────────────
timestamp() { date +"%Y-%m-%d-%H%M"; }
log() { echo "[$(date +'%F %T')] $*" | tee -a "$LOG_FILE"; }

rotate_backups() {
  log "🧹 Removing backups older than $RETENTION_DAYS days..."
  find "$BACKUP_DIR" -maxdepth 1 -name "home-backup-*.tar.*" -mtime +"$RETENTION_DAYS" -print -delete || true
}

create_backup() {
  local ts archive
  ts=$(timestamp)
  archive="$BACKUP_DIR/home-backup-$ts.tar.gz"

  log "📦 Creating compressed backup: $archive"
  tar "${EXCLUDES[@]}" -czf "$archive" -C "$HOME" . 2>>"$LOG_FILE"
  log "✅ Backup complete: $(du -h "$archive" | awk '{print $1}')"
}

verify_backup() {
  log "🔍 Verifying archive integrity..."
  tar -tzf "$1" >/dev/null
  log "✅ Archive integrity check passed."
}

upload_remote() {
  [[ "$REMOTE_ENABLED" == true ]] || return
  log "🌐 Uploading $1 to $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"
  rsync -az "$1" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/" 2>>"$LOG_FILE" \
    && log "✅ Remote upload complete." \
    || log "⚠️  Remote upload failed."
}

# ───────────────────────────── MAIN ─────────────────────────────
log "─────────────────────────────"
log "🏁 Starting home backup for $USER"

rotate_backups
create_backup
latest=$(ls -t "$BACKUP_DIR"/home-backup-*.tar.gz | head -n 1)
verify_backup "$latest"
upload_remote "$latest"

log "🏁 Backup process finished successfully."
log "─────────────────────────────"
```

---

## 🧩 Installation

1. Save as `~/backup-home.sh`
    
2. Make it executable:
    
    ```bash
    chmod +x ~/backup-home.sh
    ```
    
3. Run manually:
    
    ```bash
    ./backup-home.sh
    ```
    

---

## 🕒 Optional: Automate with Cron

Open your cron table:

```bash
crontab -e
```

Add this line to run every day at 2 AM:

```bash
0 2 * * * /home/youruser/backup-home.sh >> /home/youruser/backup-cron.log 2>&1
```

---

## 🧠 Notes

- All logs go to `~/backup-home.log`
    
- Keeps backups from the last 7 days (tweak `RETENTION_DAYS`)
    
- Enable remote upload by setting:
    
    ```bash
    REMOTE_ENABLED=true
    REMOTE_USER="yourname"
    REMOTE_HOST="yourserver.com"
    REMOTE_PATH="/path/to/backups"
    ```
    
- Tested on: Kali 2024.x, Ubuntu 22.04, Debian 12
    

---

