#!/bin/bash
set -e  # Exit on any error

if [[ -z "$1" ]]; then
  echo "Usage: $0 file.s [-g]" >&2
  exit 1
fi

# Ensure file ends with .s and exists
if [[ ! "$1" =~ \.s$ ]]; then
  echo "Error: Input file must have a .s extension" >&2
  exit 1
fi

if [[ ! -f "$1" ]]; then
  echo "Error: File '$1' not found" >&2
  exit 1
fi

# Strip .s extension safely
base_name="${1%.s}"

# Assemble with debug info if -g is requested (helps in GDB)
if [[ "$2" == "-g" ]]; then
  nasm -g -f elf64 "$1" -o "${base_name}.o"
else
  nasm -f elf64 "$1" -o "${base_name}.o"
fi

# Link
ld "${base_name}.o" -o "${base_name}"

# Optional: clean up object file (comment out if you want to keep it)
rm -f "${base_name}.o"

# Run or debug
if [[ "$2" == "-g" ]]; then
  gdb -q "${base_name}"
else
  "./${base_name}"
fi
