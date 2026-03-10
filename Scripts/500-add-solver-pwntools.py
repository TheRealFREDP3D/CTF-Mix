from pwn import *

# -------------------------
target = TARGET_IP # <-----
port = TARGET_PORT # <-----
# -------------------------

# onnect to the server
> conn = remote(target, port)
>
> # Read welcome messages
> print(conn.recvuntil(b'?').decode())
500 addition pro>
> # Solve 500 addition problems
> for i in range(500):
>     # Receive the question
 conn.recvline()>     line = conn.recvline().decode().strip()
se the addition >
>     # Parse the addition problem
>     parts = line.split()
>     if len(parts) >= 5 and parts[4] == '+':
>         num1 = int(parts[3])
>         num2 = int(parts[5].rstrip('?'))
>         answer = num1 + num2
>
>         # Send the answer
>         conn.sendline(str(answer).encode())
>         print(f"Problem {i+1}: {num1} + {num2} = {answer}")
>
> # Receive and print the flag
> flag = conn.recvall().decode()
> print(flag)
>
> conn.close()
