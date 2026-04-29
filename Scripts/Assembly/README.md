# Assembly Script

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

**`base_name="${1%.s}"`**
- Extracts the filename without the `.s` extension
- `%.s` removes only the `.s` extension
- Example: `program.s` becomes `program`

**`as --64 "$1" -o "${base_name}.o"`**
- **as**: The GNU Assembler (GAS)
- **--64**: Specifies 64-bit mode for x86-64 assembly
- Assembles the `.s` source file into a `.o` object file using GAS syntax

**`ld "${base_name}.o" -o "${base_name}"`**
- **ld**: The GNU linker
- Links the object file into an executable binary
- Output has no extension (standard for Linux executables)

**`if [[ "$2" == "-g" ]]; then`**
- Checks if the second argument is `-g` (debug flag)

**Debug mode:** `gdb -q "${base_name}"`
- Launches GDB (GNU Debugger) in quiet mode
- Lets you step through the assembly code

**Normal mode:** `"./${base_name}"`
- Executes the compiled program directly

## Usage Examples

```bash
# Assemble, link, and run
./assembler.sh program.s

# Assemble, link, and debug
./assembler.sh program.s -g
```
