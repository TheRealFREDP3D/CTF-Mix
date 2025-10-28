This is a **bash script** that automates the process of assembling and linking x86-64 assembly programs, with an optional debugging mode.

## Line-by-Line Breakdown

**`#!/bin/bash`**
- Shebang line that tells the system to execute this script using the bash shell

**`set -e`**
- Makes the script exit immediately if any command fails (returns non-zero exit status)
- Prevents cascading errors (e.g., trying to link if assembly failed)

**`if [[ -z "$1" ]]; then`**
- Checks if the first argument (`$1`) is empty (`-z` = zero length)
- If no filename was provided, shows usage instructions and exits

**`fileName="${1%%.*}"`**
- Extracts the filename without extension
- `%%.*` removes everything from the last `.` to the end
- Example: `program.s` becomes `program`

**`nasm -f elf64 "${fileName}.s" -o "${fileName}.o"`**
- **nasm**: The Netwide Assembler
- **-f elf64**: Specifies output format as 64-bit ELF (Linux executable format)
- Assembles the `.s` source file into a `.o` object file

**`ld "${fileName}.o" -o "${fileName}"`**
- **ld**: The GNU linker
- Links the object file into an executable binary
- Output has no extension (standard for Linux executables)

**`if [[ "$2" == "-g" ]]; then`**
- Checks if the second argument is `-g` (debug flag)

**Debug mode:** `gdb -q "${fileName}"`
- Launches GDB (GNU Debugger) in quiet mode
- Lets you step through the assembly code

**Normal mode:** `"./${fileName}"`
- Executes the compiled program directly

## Usage Examples

```bash
# Assemble, link, and run
./assembler.sh program.s

# Assemble, link, and debug
./assembler.sh program.s -g
```
