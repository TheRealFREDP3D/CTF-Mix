# Scripts Directory

A personal collection of Python and Bash scripts built while working through CTF challenges and cybersecurity exercises. Each script targets a specific attack category or utility need encountered during real challenges.

## Directory Structure
Scripts/
├── README.md
├── listener.py
├── bash-send-payload.py
├── lfi-nginx-log-poisoning.py
├── shellcode_optimized.py
├── shell.s
├── alpha-auto-substitution.py
├── alpha-substitution-decrypt.py
├── solve_additions.py
├── solve_additions_simple_pwntools.py
├── solve_additions_stdlib.py
├── 500-add-solver-pwntools.py
│
├── Assembly/
│   ├── README.md
│   └── assembler.sh
│
├── Full-Auto/
│   └── Hackthebox/
│       └── Phantom-exploit.py
│
├── LFI/
│   └── lfi_fuzzer.py
│
├── MSSQL-user-enumeration-multi/
│   ├── mssql_enum_methods.md
│   └── mssql_user_enum.py
│
├── Powershell/
│   ├── chisel_setup.ps1
│   ├── PowerShell TCP forwarding.ps1
│   └── test_tunnels.ps1
│
├── pyc-reverse-tool/
│   └── py-reverse-tool.py
│
├── pwn.college/
│   ├── Autobackup.md
│   └── Home Backup Guide.md
│
├── quantum/
│   ├── quantum teleport guide.md
│   └── quantum_teleport.py
│
├── Testing-Input-Sanitization/
│   ├── README.md
│   └── Input-Sanitization-Testing.py
│
└── XSS-Cookie-Stealer/
└── cookie-stealer.py

---

## Scripts Reference

### Root Directory

| Script | Category | Description |
|--------|----------|-------------|
| `listener.py` | Networking | TCP listener that accepts connections and provides an interactive shell session over the socket. |
| `bash-send-payload.py` | Exploitation | Connects to a target shell prompt and sends a wildcard-based payload to read files (e.g. `flag.txt`). |
| `lfi-nginx-log-poisoning.py` | Web / LFI | Poisons Nginx access logs with a PHP payload via the User-Agent header, then triggers execution via LFI. |
| `shellcode_optimized.py` | PWN | Sends optimized 42-byte x86-64 shellcode to read `/flag.txt` on a remote target using pwntools. |
| `shell.s` | PWN | Raw x86-64 assembly source for the `/flag.txt` shellcode — companion to `shellcode_optimized.py`. |
| `alpha-substitution-decrypt.py` | Cryptography | Frequency analysis tool for monoalphabetic substitution ciphers; builds a partial key interactively. |
| `alpha-auto-substitution.py` | Cryptography | Applies a completed substitution key to decrypt a ciphertext in one shot. |
| `solve_additions.py` | Networking | Robust stdlib-only solver for 500-question addition challenges; includes buffered reading and timeouts. |
| `solve_additions_simple_pwntools.py` | Networking | Clean pwntools-based solver for the same challenge type — simpler and more concise. |
| `solve_additions_stdlib.py` | Networking | Alternative stdlib solver with persistent buffer management and TCP_NODELAY optimization. |
| `500-add-solver-pwntools.py` | Networking | Early pwntools solver for addition challenges — kept as a reference for the original approach. |

---

### `Assembly/`

| File | Description |
|------|-------------|
| `assembler.sh` | Bash script that assembles and links x86-64 `.s` files using GNU `as` and `ld`. Supports optional `-g` flag to drop into GDB after building. |
| `README.md` | Line-by-line breakdown of `assembler.sh` explaining each flag and step. |

---

### `Full-Auto/Hackthebox/`

| Script | Description |
|--------|-------------|
| `Phantom-exploit.py` | Automated XSS exploit for the HackTheBox Phantom challenge. Uses Socket.IO to listen for a flag callback after injecting a payload via the `/search` endpoint. |

---

### `LFI/`

| Script | Description |
|--------|-------------|
| `lfi_fuzzer.py` | Advanced LFI fuzzer that generates combinatorial path traversal payloads using `itertools.product`. Tests raw, URL-encoded, and double-slash variants across multiple traversal depths. |

---

### `MSSQL-user-enumeration-multi/`

| File | Description |
|------|-------------|
| `mssql_user_enum.py` | Enumerates valid Windows domain users against an MSSQL server by analysing authentication error message differences. Requires `pymssql`. |
| `mssql_enum_methods.md` | Reference guide covering 8 distinct MSSQL/AD user enumeration techniques: Nmap NSE, Metasploit, error-based, SMB, LDAP, Kerberos, NTLM capture, and ASREPRoasting. |

---

### `Powershell/`

| Script | Description |
|--------|-------------|
| `PowerShell TCP forwarding.ps1` | Sets up bidirectional TCP port forwarders in PowerShell for LDAP (389), Kerberos (88), and WinRM (5985) — useful for pivoting through a compromised Windows host. |
| `chisel_setup.ps1` | Downloads `chisel.exe` to a target and starts a reverse tunnel client, forwarding LDAP, Kerberos, and WinRM back to the attacker machine. |
| `test_tunnels.ps1` | Verifies that the forwarded tunnel ports are reachable and reports their status. |

---

### `pyc-reverse-tool/`

| Script | Description |
|--------|-------------|
| `py-reverse-tool.py` | Reverse engineers Python bytecode from `.pyc` files, base64-encoded files, or base64 strings. Disassembles via `dis` and optionally decompiles via `decompyle3`. |

---

### `pwn.college/`

| File | Description |
|------|-------------|
| `Home Backup Guide.md` | Step-by-step guide for backing up `/home/hacker` in pwn.college lab environments. Covers compressed archives, rsync mirrors, remote copy, and restore testing. |
| `Autobackup.md` | Production-ready automated backup script with logging, retention policy, optional remote sync, and cron setup instructions. |

---

### `quantum/`

| File | Description |
|------|-------------|
| `quantum teleport guide.md` | Beginner-friendly guide to quantum teleportation covering qubits, gates, Bell pairs, and the full teleportation protocol with a correction table. |
| `quantum_teleport.py` | pwntools-based solver for a quantum teleportation CTF challenge. Reads leaked qubit measurements, applies Pauli corrections, and recovers the encoded flag bit by bit. |

---

### `Testing-Input-Sanitization/`

| File | Description |
|------|-------------|
| `Input-Sanitization-Testing.py` | Sends a battery of test payloads (variable expansion, command substitution, Shellshock, file descriptors) to a remote service to probe its input sanitization. |
| `README.md` | Detailed line-by-line breakdown of the sanitization tester, including a payload reference table and links to relevant concepts. |

---

### `XSS-Cookie-Stealer/`

| Script | Description |
|--------|-------------|
| `cookie-stealer.py` | Registers an account, logs in, and submits a bug report containing an XSS payload that exfiltrates the admin cookie to a listener. |

---

## Dependencies

Install Python dependencies with:

```bash
pip install pwntools requests python-socketio pymssql python-dotenv decompyle3
```

> **Note:** `decompyle3` is optional — `py-reverse-tool.py` degrades gracefully if it is not installed.

---

## Disclaimer

These scripts are intended for **educational purposes and authorized testing only**. Always ensure you have explicit permission before testing any system you do not own.