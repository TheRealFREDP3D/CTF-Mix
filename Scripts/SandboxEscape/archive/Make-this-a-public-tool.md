# Bashpoke: Tool Design Notes & Reference

## Project Overview

**Bashpoke** (working title) is a lightweight fuzzing and enumeration tool designed to interact with restricted shell environments commonly found in CTF challenges or sandboxed systems. The goal is to identify useful environment variables, hidden files, and potential breakout paths using Bash-compatible syntax under character constraints.

---

## ✅ Core Goals

* **Automate** the process of sending restricted Bash payloads.
* **Explore** system internals using only allowed characters (e.g., via regex filters).
* **Assist CTF players** or red-teamers working in limited shell environments.

---

## 🔍 Source Script Review

### Original Strengths

* A variety of exploratory payloads.
* Coverage for:

  * Environment variables
  * Directory probing
  * Substitution/expansion
  * Redirection
  * Arithmetic operations
  * Flag discovery attempts
* Built using `pwntools`, a standard CTF-friendly library.
* Handles initial response, sends payloads in sequence, and captures output.

### Original Weaknesses

* Hardcoded character set (specific regex).
* No payload modularity or filtering.
* No output parsing/flag detection.
* Monolithic code structure.
* Assumes POSIX shell.

---

## 🔁 Reusability Analysis

| Factor              | Score (1–10) | Comments                                           |
| ------------------- | ------------ | -------------------------------------------------- |
| Regex Flexibility   | 5            | Static regex awareness. Needs dynamic handling.    |
| Payload Coverage    | 9            | Well-rounded for restricted Bash use cases.        |
| Shell Compatibility | 8            | Strong POSIX/Bash support. Not usable elsewhere.   |
| Code Modularity     | 4            | Monolithic script. Needs CLI interface and config. |
| Output Analysis     | 6            | No parsing or filtering. Raw output only.          |
| Target Agnosticism  | 7            | Useful across typical Linux shell targets.         |

---

## 📦 Planned Features

### CLI Options

```bash
bashpoke.py \
  --host 127.0.0.1 \
  --port 1337 \
  --regex "^[0-9${}/?:&>_=()[:space:]]+$" \
  --modules env,files,redir \
  --log results.json \
  --verbose
```

### Modular Payload System

```
payloads/
├── env.txt
├── files.txt
├── arith.txt
├── redir.txt
├── flaghunt.txt
```

### Output Filtering

* Detect potential flags (`flag`, `CTF{`, `ROOT`, `key`, etc.)
* Option to save interesting output

### Logging

* Support JSON or plain text logs

### Retry and Reconnect Logic

* Graceful handling of broken pipe, EOF, or timeout

---

## 📚 Useful Resources

### pwntools

* [Docs](https://docs.pwntools.com/en/stable/)
* [GitHub](https://github.com/Gallopsled/pwntools)

### Bash Reference

* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
* [Bash Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)

### Regex & Input Sanitization

* [Regex101](https://regex101.com/) — for testing character filters
* [OWASP Command Injection Guide](https://owasp.org/www-community/attacks/Command_Injection)

### CTF Tools & Examples

* [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
* [CTF Field Guide](https://trailofbits.github.io/ctf/)

---

## 🏷️ Name Ideas

| Functional  | Descriptive    | Hacker-Style    |
| ----------- | -------------- | --------------- |
| `shellfuzz` | `PayloadProbe` | `bashwreck`     |
| `bashpoke`  | `FlagHunter`   | `$$` (stylized) |
| `shfuzz`    | `EscapePlan`   | `ghostsh`       |

---

## 📄 README.md Outline

````markdown
# bashpoke

A Bash payload fuzzing and enumeration tool for restricted shell environments (CTF & sandbox contexts).

## Features
- Regex-aware payload testing
- Modular payload system
- Environment exploration and flag discovery
- CLI interface with output logging

## Usage
```bash
python bashpoke.py --host 127.0.0.1 --port 9001 --modules env,flaghunt --verbose
````

## License

MIT

```

---

## ✍️ Next Steps
1. Refactor current script into modular functions.
2. Build payload loader from directory.
3. Add `argparse` CLI interface.
4. Create GitHub repo and write full README.
5. Expand payload library.

Let me know if you'd like help generating the GitHub repo, README content, or if you want this turned into a `pip`-installable package!
```
