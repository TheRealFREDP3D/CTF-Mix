from pwn import *
import re

# -------------------------
target = "127.0.0.1"  # <----- Change to target IP
port = 9999           # <----- Change to target port
# -------------------------

def parse_addition_problem(line):
    """Extract numbers from addition problem using regex"""
    # Match patterns like "What is 123 + 456?" or "Problem 1: 123 + 456 = ?"
    match = re.search(r'(\d+)\s*\+\s*(\d+)', line)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

try:
    # Connect to the server
    conn = remote(target, port)
    
    # Read welcome messages
    print(conn.recvuntil(b'?').decode())
    
    # Solve 500 addition problems
    for i in range(500):
        # Receive the question
        line = conn.recvline().decode().strip()
        print(f"Received: {line}")
        
        # Parse the addition problem
        num1, num2 = parse_addition_problem(line)
        
        if num1 is not None and num2 is not None:
            answer = num1 + num2
            
            # Send the answer
            conn.sendline(str(answer).encode())
            print(f"Problem {i+1}: {num1} + {num2} = {answer}")
        else:
            print(f"[!] Failed to parse problem {i+1}: {line}")
            break
    
    # Receive and print the flag
    flag = conn.recvall().decode()
    print(f"[+] Flag: {flag}")
    
except Exception as e:
    print(f"[!] Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
