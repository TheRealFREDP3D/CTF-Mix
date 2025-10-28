# Scripts Directory

This directory contains various scripts for automating tasks, testing, or other utility purposes related to CTFs and cybersecurity challenges.

## Contents

### Core Scripts (Root Directory):
- **`alpha-auto-substitution.py`**: Automates the process of solving simple substitution ciphers using frequency analysis.
- **`alpha-substitution-decrypt.py`**: Decrypts text using a provided substitution cipher key.
- **`bash-send-payload.py`**: Sends a bash command payload to a target system (use responsibly and ethically).
- **`lfi-nginx-log-poisoning.py`**: Exploits Local File Inclusion vulnerabilities by poisoning Nginx access logs.
- **`listener.py`**: A simple network listener for receiving connections and data.

### Subdirectories:

#### `Assembly/`
- **`assembler.sh`**: Bash script for assembling assembly code (architecture specific).

#### `Full-Auto/Hackthebox/`
- **`Phantom-exploit.py`**: Automated exploit script for a HackTheBox challenge (Phantom box).

#### `LFI/`
- **`lfi_fuzzer.py`**: Advanced fuzzer for testing Local File Inclusion vulnerabilities with various path traversal payloads.

#### `pyc-reverse-tool/`
- **`py-reverse-tool.py`**: Tool for reverse engineering Python bytecode (.pyc files) - can disassemble and attempt to decompile.

#### `Testing-Input-Sanitization/`
- **`Input-Sanitization-Testing.py`**: Tests web application input handling by sending various payloads to detect sanitization issues.
- **`README.md`**: Documentation for the input sanitization testing framework.

#### `XSS-Cookie-Stealer/`
- **`cookie-stealer.py`**: Proof-of-concept for demonstrating XSS cookie stealing vulnerabilities.

#### `quantum/`
- **`quantum_teleport.py`**: Quantum computing example demonstrating quantum teleportation (educational purposes).

## Usage

Each script includes a help message that can be accessed by running it with the `-h` or `--help` flag. For detailed usage instructions, refer to the individual script's documentation or comments.

## Note

These scripts are intended for educational and authorized testing purposes only. Always ensure you have proper authorization before testing any systems.

Refer to the `README.md` within each subdirectory for more detailed information about the specific scripts and their functionalities.