# BashSandboxEscape

A Bash payload fuzzing and enumeration tool for restricted shell environments (CTF & sandbox contexts).

## Features
- Regex-aware payload testing
- Modular payload system
- Environment exploration and flag discovery
- CLI interface with output logging

## Usage
```bash
python bash_sandbox_escape.py --host 127.0.0.1 --port 9001 --modules env,flaghunt --verbose
```

## License

MIT
