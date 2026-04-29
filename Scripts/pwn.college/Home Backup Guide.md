
---

# 💾 /home/hacker Backup Guide (for CTF or Lab Environments)

Backups are your safety net — they save you from losing progress on long-running challenges, configs, or notes.  
This guide provides **two simple backup options** and instructions for verifying and restoring your data.

---

## ⚙️ Before You Begin

Decide on the backup type:

|Option|Type|Pros|Cons|
|:--|:--|:--|:--|
|**A**|Compressed `.tar.gz`|Portable, easy to download|Slightly slower|
|**B**|Plain folder copy|Fast, instantly browsable|Takes more space|

Also consider:

- ✅ Include hidden files (dotfiles) — yes, keep them.
    
- 🚫 Exclude caches and trash for smaller backups.
    
- 📦 Backups can stay local or be sent to another system (remote server, local machine, etc.).
    

---

## 🅰️ Option A — Create a Compressed Backup (`.tar.gz`)

This option makes a timestamped archive, e.g. `home-backup-2025-10-24-1530.tar.gz`,  
and saves it in your home directory.

### Run:

```bash
du -sh ~

tar --exclude="$HOME/.cache" \
    --exclude="$HOME/.local/share/Trash" \
    --exclude="$HOME/.config/Code/Cache" \
    -czf "$HOME/home-backup-$(date +%F-%H%M).tar.gz" \
    -C "$HOME" .

ls -lh "$HOME"/home-backup-*.tar.gz
```

### Verify the Archive

```bash
tar -tzf "$HOME"/home-backup-*.tar.gz | head
```

This lists the first few files to confirm the archive structure.

---

## 🅱️ Option B — Make a Plain Folder Copy (via `rsync`)

This creates a direct mirror of your home directory, preserving file permissions and timestamps.  
Useful if you need to browse or selectively restore files.

### Run:

```bash
mkdir -p /tmp/home-backup

rsync -a --exclude='.cache/' \
          --exclude='.local/share/Trash/' \
          --exclude='.config/Code/Cache/' \
          "$HOME"/ /tmp/home-backup/

du -sh /tmp/home-backup
```

---

## 🌐 Optional — Copy Backup Off the VM

Move the backup to safety using `rsync` or `scp`.

**On your local machine terminal**

### With `rsync`:

```bash
# Change filename
rsync -az hacker@dojo.pwn.college:/home/hacker/<enter filename of the backup> "./pwn-college-home-backup.tar.gz"
```

### With `scp`:

```bash


# Change filename
$ scp hacker@dojo.pwn.college:/home/hacker/<enter filename of the backup> ./pwn-college-home-backup.tar.gz

home-backup-2025-10-24-1941.tar.gz                                                    100%   29MB 900.7KB/s   00:32
```

💡 If you’re using a **VSCode Remote Workspace (like pwn.college)**,  
you can also download the `.tar.gz` directly through the file explorer sidebar.

---

## 🧩 Restore Test (Highly Recommended)

Always verify your backup can actually restore:

```bash
mkdir -p ~/restore-test
tar -xzf "$HOME"/home-backup-*.tar.gz -C ~/restore-test
ls -la ~/restore-test | head
```

This extracts the backup into a temporary folder to confirm it’s complete.

---

## 🧠 Quick Reference

|Task|Command|
|---|---|
|Check home size|`du -sh ~`|
|Create compressed backup|`tar -czf ...`|
|List archives|`ls -lh ~/home-backup-*.tar.gz`|
|Browse archive contents|`tar -tzf archive.tar.gz`|
|Restore from backup|`tar -xzf archive.tar.gz -C ~/restore-test`|
|Copy backup remotely|`rsync` or `scp`|

---

## 🚀 Pro Tips

- Automate daily backups with a cron job or systemd timer.
    
- Use `xz` instead of `gzip` for better compression:
    
    ```bash
    tar -cJf "$HOME/home-backup-$(date +%F-%H%M).tar.xz" -C "$HOME" .
    ```
    
- Keep multiple versions:
    
    ```bash
    find "$HOME" -name "home-backup-*.tar.gz" -mtime +7 -delete
    ```
    
    (Deletes backups older than 7 days.)
    

---
