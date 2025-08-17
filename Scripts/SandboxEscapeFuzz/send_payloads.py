import socket
import time

HOST = '94.237.123.87'
PORT = 44123

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
