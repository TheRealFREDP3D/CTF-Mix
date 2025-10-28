#!/bin/bash
set -e

if [[ -z "$1" ]]; then
  echo "Usage: $0 file.s [-g]" >&2
  exit 1
fi

if [[ ! -f "$1" ]]; then
  echo "Error: File '$1' not found" >&2
  exit 1
fi

base_name="${1%.s}"

# Assemble with GNU as (supports .intel_syntax)
as --64 "$1" -o "${base_name}.o"

# Link
ld "${base_name}.o" -o "${base_name}"

# Clean up
rm -f "${base_name}.o"

if [[ "$2" == "-g" ]]; then
  gdb -q "${base_name}"
else
  "./${base_name}"
fi
