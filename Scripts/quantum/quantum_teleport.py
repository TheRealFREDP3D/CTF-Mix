# solve_pwntools.py
#!/usr/bin/env python3
from pwn import remote, context
import re

context.log_level = "info"  # switch to "debug" for verbose

HOST = "<Enter instance IP here>"
PORT = <Enter instance port here>

# Pauli correction lookup - use X:0 as no-op since qubit 0 is already measured
corr = {
    (0, 0): "X:0",      # no correction needed, use dummy gate
    (0, 1): "X:2",      # apply X to qubit 2
    (1, 0): "Z:2",      # apply Z to qubit 2
    (1, 1): "Z:2;X:2"   # apply Z then X to qubit 2
}

# Correct decoding: measurement result directly indicates the encoded state
decode = {
    ("Z", 0): "00",  # 0 measurement in Z basis -> |0⟩ -> "00"
    ("Z", 1): "01",  # 1 measurement in Z basis -> |1⟩ -> "01"
    ("X", 0): "10",  # 0 measurement in X basis -> |+⟩ -> "10"
    ("X", 1): "11"   # 1 measurement in X basis -> |-⟩ -> "11"
}

def recover_pair(basis: str, q0: int, q1: int, meas: int) -> str:
    """Return the original two-bit string."""
    return decode[(basis, meas)]

def solve():
    io = remote(HOST, PORT)
    
    flag_bits = ""
    pair_cnt = 0
    
    while True:
        # --- wait for server banners -------------------------------------------------
        line = io.recvline_regex(rb"Qubit \d+/\d+")
        pair_cnt += 1
        print(f"[*] Qubit {pair_cnt}/???")
        
        # --- Basis -------------------------------------------------------------------
        line = io.recvline_contains(b"Basis :")
        basis = line.decode().split(":")[1].strip()  # "Z" or "X"
        print(f"[*] basis = {basis}")
        
        # --- leaked measurements -----------------------------------------------------
        line = io.recvline_contains(b"Measurement of qubit 0 :")
        q0 = int(line.decode().split(":")[1].strip())
        line = io.recvline_contains(b"Measurement of qubit 1 :")
        q1 = int(line.decode().split(":")[1].strip())
        print(f"[*] leaked (q0,q1) = ({q0},{q1})")
        
        # --- send correction gates ---------------------------------------------------
        gates = corr[(q0, q1)]
        io.sendlineafter(b"Specify the instructions :", gates.encode())
        print(f"[*] sent gates: {gates}")
        
        # --- choose measurement basis ------------------------------------------------
        io.sendlineafter(b"Specify the measurement basis :", basis.encode())
        print(f"[*] sent basis: {basis}")
        
        # --- read back final measurement ---------------------------------------------
        line = io.recvline_contains(b"Measurement of qubit 2 :")
        meas = int(line.decode().split(":")[1].strip())
        print(f"[*] meas q2 = {meas}")
        
        # --- recover original two-bit pair ------------------------------------------
        two_bit = recover_pair(basis, q0, q1, meas)
        flag_bits += two_bit
        print(f"[+] recovered pair #{pair_cnt}: {two_bit}  (flag so far: {flag_bits})")
        
        # --- check if we have a complete flag ---------------------------------------
        if len(flag_bits) % 8 == 0 and len(flag_bits) >= 32:
            try:
                flag = bytes(int(flag_bits[i:i+8], 2) for i in range(0, len(flag_bits), 8))
                flag_str = flag.decode('ascii', errors='ignore')
                print(f"[*] Current decoded: {flag_str}")
                if flag.endswith(b"}") and flag.startswith(b"HTB{"):
                    print(f"[+] Flag recovered: {flag.decode()}")
                    break
            except (ValueError, UnicodeDecodeError):
                pass
    
    io.close()

if __name__ == "__main__":
    solve()