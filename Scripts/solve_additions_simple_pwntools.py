from pwn import *
import re

context.log_level = 'error'  # reduce noise

HOST = ''
PORT = 1337

conn = remote(HOST, PORT)

for i in range(500):
    q = conn.recvuntil(b'?').decode(errors='ignore')
    m = re.search(r'(\d+)\s*\+\s*(\d+)', q)
    if not m:
        print(f"Could not parse question: {q!r}")
        break
    a = int(m.group(1)) + int(m.group(2))
    conn.sendline(str(a).encode())
    print(f"Problem {i+1}: {m.group(1)} + {m.group(2)} = {a}")

flag = conn.recvall(timeout=3).decode(errors='ignore')
print(flag)

conn.close()
