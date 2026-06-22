# CTF-Mixed-Stuff

A comprehensive collection of tools, scripts, and resources for Capture The Flag (CTF) challenges and cybersecurity training. This repository contains materials developed while solving challenges on various platforms including HackTheBox, TryHackMe, pwn.college, WeChall, Root-Me, CryptoHack, PicoCTF, and more.

## � Table of Contents

- [CTF-Mixed-Stuff](#ctf-mixed-stuff)
  - [� Table of Contents](#-table-of-contents)
  - [�📁 Repository Structure](#-repository-structure)
    - [Core Directories](#core-directories)
    - [Quick Start](#quick-start)
  - [🛠️ Usage](#️-usage)
  - [⚠️ Legal \& Ethical Considerations](#️-legal--ethical-considerations)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)

## 📁 Repository Structure

### Core Directories

- **`Cheatsheets/`** - Quick reference guides and command references
  - `reverse-shell-cheatsheet.md` - Various reverse shell payloads and techniques

- **`CTF Environment Setup Script + Aliases/`** - Environment setup and configuration
  - Setup scripts for CTF environments
  - Custom shell aliases and configurations

- **`Guidelines/`** - Best practices and methodologies
  - CTF participation guidelines
  - Ethical hacking principles

- **`Scripts/`** - Custom tools and exploit scripts
  - **Cryptography & Ciphers**: `alpha-substitution-decrypt.py`, `alpha-auto-substitution.py`
  - **Binary Exploitation**: `shell.s`, `shellcode_optimized.py`, `500-add-solver-pwntools.py`
  - **Web Security**: `lfi-nginx-log-poisoning.py`, `bash-send-payload.py`, `XSS-Cookie-Stealer/`
  - **Network Tools**: `listener.py`, `pass-spraying-domain-users.py`
  - **Assembly**: `Assembly/assembler.sh` with GAS syntax support
  - **Python Tools**: `pyc-reverse-tool/` for .pyc reverse engineering
  - **CTF Platform Tools**: `pwn.college/` backup solutions
  - **Testing**: `Testing-Input-Sanitization/` for web app testing
  - *See [Scripts/README.md](Scripts/README.md) for complete details*

- **`Writeup-Guidelines/`** - Templates and standards
  - Writeup structure and documentation standards

### Quick Start

1. **Setup Environment**:
   - Navigate to `CTF Environment Setup Script + Aliases/` for setup scripts
   - Follow the installation instructions for your platform

2. **Explore Scripts**:
   ```bash
   # Check available scripts
   cd Scripts
   python3 script_name.py --help
   # For assembly:
   ./Assembly/assembler.sh program.s
   ```

3. **Use Cheatsheets**:
   ```bash
   # Quick reference during challenges
   cat Cheatsheets/reverse-shell-cheatsheet.md | less
   ```

4. **Common Use Cases**:
   - **Binary Exploitation**: Use `500-add-solver-pwntools.py` for CTF math challenges
   - **Cryptography**: Try `alpha-substitution-decrypt.py` for substitution ciphers
   - **Web Testing**: Use `Testing-Input-Sanitization/` for web app security testing
   - **Reverse Engineering**: Use `pyc-reverse-tool/` for Python bytecode analysis

## 🛠️ Usage

This repository is designed to be both a personal knowledge base and a collection of reusable tools. Feel free to:
- Use the scripts and tools in your CTF challenges
- Reference the cheatsheets during competitions
- Follow the guidelines for structured note-taking and writeups

## ⚠️ Legal & Ethical Considerations

- All tools and scripts are for educational and authorized testing purposes only
- Only use these resources on systems you own or have explicit permission to test
- Always comply with applicable laws and regulations
- Respect the terms of service of all platforms and challenges

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This repository serves as a personal knowledge base and toolkit for CTF challenges.
