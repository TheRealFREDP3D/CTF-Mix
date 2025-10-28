#!/bin/bash
set -e  # stop on first error

if [[ -z "$1" ]]; then
  echo "Usage: $0 file.s [-g]"
  exit 1
fi

fileName="${1%%.*}"

nasm -f elf64 "${fileName}.s" -o "${fileName}.o"
ld "${fileName}.o" -o "${fileName}"

if [[ "$2" == "-g" ]]; then
  gdb -q "${fileName}"
else
  "./${fileName}"
  "./${fileName}"
fi
