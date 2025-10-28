# 🛠️ `ctf-setup.sh` – CTF Environment Setup Script

Here's a full **CTF Environment Setup Script** that automates setting up a **Kali Linux or ParrotSec VM** for fast and efficient CTF play. It installs essential tools, sets up useful aliases (including Active Directory tools), and configures your terminal environment for speed.

> ✅ Compatible with Kali Linux / Parrot OS  
> 📦 Installs tools  
> 🔧 Adds aliases  
> 🧠 Optimized for web, binary, pwn, privilege escalation, and Active Directory

---

## 📄 Script

```bash
#!/bin/bash
# ctf-setup.sh – Kali Linux CTF Setup Script
# Author: Frederick Pellerin (TheRealFREDP3D)
# Use: sudo bash ctf-setup.sh

set -e

echo "[+] Updating system..."
apt update && apt upgrade -y

echo "[+] Installing essential CTF tools..."
apt install -y \
  net-tools curl wget git unzip build-essential \
  nmap gobuster ffuf whatweb whois \
  smbclient enum4linux rpcbind \
  python3 python3-pip python3-venv \
  ldap-utils neo4j bloodhound \
  seclists dmitry nbtscan \
  crackmapexec impacket-scripts \
  rlwrap \
  tcpdump wireshark \
  metasploit-framework \
  ipython \
  gdb gdbserver \
  p7zip-full \
  jq

echo "[+] Installing additional tools from GitHub..."
mkdir -p ~/tools && cd ~/tools

# Kerbrute
if [ ! -d kerbrute ]; then
  git clone https://github.com/ropnop/kerbrute
  cd kerbrute && go build -o kerbrute main.go && sudo mv kerbrute /usr/local/bin/ && cd ..
fi

# PEASS-ng
if [ ! -d PEASS-ng ]; then
  git clone https://github.com/carlospolop/PEASS-ng
fi

# Impacket Python virtualenv
if [ ! -d impacket ]; then
  git clone https://github.com/SecureAuthCorp/impacket
  cd impacket && python3 -m venv venv && source venv/bin/activate
  pip install -r requirements.txt .
  deactivate && cd ..
fi

echo "[+] Adding CTF aliases..."
cat << 'EOF' > ~/.ctf_aliases
# === General Recon ===
alias ports='netstat -tuln | grep LISTEN'
  git clone https://github.com/ropnop/kerbrute
  cd kerbrute && go build -o kerbrute main.go && sudo mv kerbrute /usr/local/bin/ && cd ..
fi
alias nmapf='nmap -sC -sV -T4 -oN nmap_full -v'
alias nmapq='nmap -sS -T4 -p- -oN nmap_quick --min-rate=1000 -v'
alias gobusterd='gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt'
alias ffufd='ffuf -u http://TARGET/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200'

# === Shells & Privilege Escalation ===
alias shellz='python3 -c "import pty; pty.spawn(\'/bin/bash\')"'
alias upgrade='python3 -c "import pty; pty.spawn(\'/bin/bash\'); import os; os.system(\'export TERM=xterm\')"'
alias suidbin='find / -perm -4000 -type f 2>/dev/null'
alias linpeas='~/tools/PEASS-ng/linPEAS/linpeas.sh'

# === Networking ===
alias serve='python3 -m http.server 8000'
alias phpserve='php -S 0.0.0.0:8000'
alias sniff='sudo tcpdump -i any -nn'
alias myports='ss -tulwn'

# === SMB & Active Directory ===
alias smbshare='smbclient -L \\\\TARGET\\ -N'
alias enum4='enum4linux -a'
alias smbmap='smbmap -H'
alias crackmap='crackmapexec smb'
alias secretsdump='secretsdump.py DOMAIN/USER:PASSWORD@TARGET'
alias kerbrute='~/tools/kerbrute/kerbrute'

# === Kerberos & BloodHound ===
alias asreproast='GetNPUsers.py DOMAIN/ -usersfile users.txt -no-pass -dc-ip TARGET'
alias kerberoast='GetUserSPNs.py DOMAIN/USER:PASSWORD -dc-ip TARGET -request'
alias bloodhound='bloodhound-python -u USER -p PASSWORD -dc-ip DC_IP -c all'
alias neo4jstart='sudo systemctl start neo4j'
alias neo4jstop='sudo systemctl stop neo4j'

# === Misc ===
alias e='nano'
alias c='clear'
alias cleanup='history -c && history -w && rm -f ~/.bash_history'
EOF

echo '[+] Linking aliases into shell startup...'
grep -qF 'source ~/.ctf_aliases' ~/.bashrc || echo '[ -f ~/.ctf_aliases ] && source ~/.ctf_aliases' >> ~/.bashrc

echo '[+] Setup complete. Reload your shell or run:'
echo 'source ~/.bashrc'
```

---

## ✅ Usage

1. **Save it** to a file:

```bash
curl -O https://example.com/ctf-setup.sh  # (Or save manually)
chmod +x ctf-setup.sh
```

2. **Run it as root**:

```bash
sudo ./ctf-setup.sh
```

3. **Reload shell**:

```bash
source ~/.bashrc
```

---

## 🧊 Optional Snapshot Instructions

After setup, **take a VM snapshot** (e.g., in VirtualBox or VMware) called `CTF-Ready` so you can revert to a clean state any time.

---

## 🧠 Learning Resources

- [HackTricks Book](https://book.hacktricks.xyz/)

- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

- [TryHackMe AD Rooms](https://tryhackme.com/module/active-directory)

- [HTB Starting Point](https://app.hackthebox.com/starting-point)

---

Would you like a downloadable `.zip` or `.tar.gz` of this script and aliases together? Or a version that supports **offline installs**?
