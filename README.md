# CTF-Mixed-Stuff

A comprehensive collection of tools, scripts, and resources for Capture The Flag (CTF) challenges and cybersecurity training. This repository contains materials developed while solving challenges on various platforms including HackTheBox, TryHackMe, pwn.college, WeChall, Root-Me, CryptoHack, PicoCTF, and more.

## 📁 Repository Structure

### Core Directories

- **`Cheatsheets/`** - Quick reference guides and command references
  - `reverse-shell-cheatsheet.md` - Various reverse shell payloads and techniques
  - `privesc.md` - Privilege escalation techniques and commands
  - `web-cheatsheet.md` - Web application testing quick reference

- **`CTF Environment Setup Script + Aliases/`** - Setup scripts and shell configurations
  - Environment setup for different CTF platforms
  - Custom shell aliases for common tasks
  - Tool installation scripts

- **`Guidelines/`** - Best practices and methodologies
  - CTF participation guidelines
  - Ethical hacking principles
  - Reporting templates

- **`Note-Template/`** - Structured note-taking templates
  - Challenge documentation format
  - Solution tracking
  - Methodology documentation

- **`Scripts/`** - Custom tools and exploit scripts
  - Cryptography tools
  - Web exploitation scripts
  - Binary exploitation helpers
  - Network tools
  - *See [Scripts/README.md](Scripts/README.md) for complete details*

- **`Writeup-Guidelines/`** - Templates and standards
  - Writeup structure
  - Documentation standards
  - Reporting best practices

### Quick Start

1. **Setup Environment**:
   - Copy the script from `CTF Environment Setup Script + Aliases/Setup Script.md` to a file named `setup.sh`.
   - Make it executable: `chmod +x setup.sh`
   - Run it as root: `sudo ./setup.sh`

2. **Explore Scripts**:
   ```bash
   # Check available scripts
   cd Scripts
   python3 script_name.py --help
   ```

3. **Use Cheatsheets**:
   ```bash
   # Quick reference during challenges
   cat Cheatsheets/reverse-shell-cheatsheet.md | less
   ```

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
