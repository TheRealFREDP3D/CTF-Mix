import argparse
import socket
import os
import re

def load_payloads(modules, payloads_dir="payloads"):
    """Loads payloads from specified module files."""
    all_payloads = []
    for module in modules:
        file_path = os.path.join(payloads_dir, f"{module}.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                all_payloads.extend([line.strip() for line in f if line.strip()])
        else:
            print(f"Warning: Payload module '{module}' not found.")
    return all_payloads

def filter_payloads(payloads, regex):
    """Filters payloads based on the allowed character regex."""
    if not regex:
        return payloads
    
    allowed_chars_pattern = re.compile(regex)
    filtered_payloads = [p for p in payloads if allowed_chars_pattern.fullmatch(p)]
    return filtered_payloads

def main():
    parser = argparse.ArgumentParser(description="BashSandboxEscape: Restricted shell fuzzer and enumerator.")
    parser.add_argument("--host", required=True, help="Target host IP or hostname.")
    parser.add_argument("--port", required=True, type=int, help="Target port.")
    parser.add_argument("--regex", help="Regex for allowed characters in payloads.")
    parser.add_argument("--modules", default="env,files", help="Comma-separated list of payload modules to use (e.g., env,files,redir).")
    parser.add_argument("--log", help="Log results to a file.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

    args = parser.parse_args()

    print(f"[*] Loading payloads from modules: {args.modules}")
    payload_modules = args.modules.split(',')
    payloads = load_payloads(payload_modules)

    if args.regex:
        print(f"[*] Filtering payloads using regex: {args.regex}")
        payloads = filter_payloads(payloads, args.regex)
        print(f"[*] {len(payloads)} payloads remaining after filtering.")

    if not payloads:
        print("[!] No payloads to send. Exiting.")
        return

    print(f"[*] Connecting to {args.host}:{args.port}")
    try:
        # Basic socket connection (pwntools alternative)
        with socket.create_connection((args.host, args.port), timeout=5) as s:
            print("[+] Connected.")
            # Placeholder for initial interaction if needed
            # initial_output = s.recv(4096).decode()
            # if args.verbose:
            #     print(f"[<] Initial output:\n{initial_output}")

            for payload in payloads:
                try:
                    if args.verbose:
                        print(f"[>] Sending payload: {payload}")
                    s.sendall((payload + '\n').encode())
                    
                    # Basic receive (may need adjustment based on target behavior)
                    response = s.recv(4096).decode()
                    if args.verbose:
                         print(f"[<] Received:\n{response}")
                    else:
                         print(f"[*] Payload: {payload}\n[+] Response:\n{response.strip()}")

                except socket.timeout:
                    print(f"[!] Timeout sending/receiving for payload: {payload}")
                except Exception as e:
                    print(f"[!] Error sending/receiving for payload {payload}: {e}")

    except ConnectionRefusedError:
        print(f"[!] Connection refused to {args.host}:{args.port}")
    except socket.gaierror:
        print(f"[!] Hostname resolution failed for {args.host}")
    except socket.timeout:
        print(f"[!] Connection timed out to {args.host}:{args.port}")
    except Exception as e:
        print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    main()
