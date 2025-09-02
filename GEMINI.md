# GEMINI Context for CTF-Mix Directory

This directory, `CTF-Mix`, serves as a collection of resources, tools, guidelines, and templates related to Capture The Flag (CTF) competitions and cybersecurity training. It's designed to aid in learning, practicing, and participating in CTFs on various platforms.

## Directory Overview

- **`README.md`**: Provides a brief introduction to the repository's purpose, mentioning its use for CTF challenges and training on platforms like HackTheBox, TryHackMe, etc.
- **`listener.py`**: A Python script implementing a basic TCP socket listener, useful for receiving reverse shells during CTF challenges.
- **`Cheatsheets/`**: Contains markdown files with quick-reference information.
  - **`reverse-shell-cheatsheet.md`**: A comprehensive list of reverse shell commands in various languages (Bash, Python, Perl, PHP, etc.) and listener commands. Crucial for exploitation phases in CTFs.
- **`Guidelines/`**: Houses documents outlining best practices.
  - **`CTFs-Guidelines.md`**: Offers a list of tips and best practices for effective CTF participation.
- **`Note-Template/`**: Provides structured templates for documenting CTF progress and solutions.
  - **`DRAFT-CTFs-Notes-Template-Obsidian.md`**: A detailed Markdown template for note-taking, especially suited for Obsidian, covering sections like Information Gathering, Exploitation, Privilege Escalation, and TODOs.
- **`Scripts/`**: Likely intended for custom scripts (currently empty).
- **`Writeup-Guidelines/`**: Presumably contains guidelines for writing CTF challenge solutions (currently empty).

## Key Files and Their Purpose

1.  **`listener.py`**: This is a core utility script. It sets up a TCP server that listens on a specified port. When a connection is made (e.g., from a reverse shell payload), it allows the user to send commands and receive output interactively. This is a fundamental tool for the exploitation phase of many CTF challenges.
2.  **`Cheatsheets/reverse-shell-cheatsheet.md`**: This is an essential reference. It provides numerous one-liners to establish reverse shells from a compromised target back to the attacker's machine. It also lists commands for setting up listeners on the attacker side (e.g., with `netcat`, `socat`) and tips for stabilizing shells. This file is directly applicable when exploiting vulnerabilities.
3.  **`Note-Template/DRAFT-CTFs-Notes-Template-Obsidian.md`**: This template is vital for organizing thoughts and documenting the process during a CTF. It provides a structured format for recording findings from information gathering, steps taken during exploitation and privilege escalation, flags obtained, and post-CTF tasks. Using this helps in writing clear writeups and learning from past challenges.

## Usage

This directory is intended to be a personal or shared resource hub for CTF players. The Python listener script can be run directly to catch reverse shells. The cheatsheets provide quick access to common commands needed during challenges. The note-taking template should be copied and filled out for each CTF box or challenge attempted, ensuring a consistent and thorough documentation process.