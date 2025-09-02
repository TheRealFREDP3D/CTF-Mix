import argparse
import base64
import dis
import io
import marshal
import sys

try:
    from decompyle3.main import decompile
except ImportError:
    decompile = None
    print("[!] decompyle3 not found. Decompilation will be skipped.\n    Install with: pip install decompyle3")


def load_code_from_pyc(path):
    with open(path, "rb") as f:
        magic = f.read(4)
        
        if sys.version_info >= (3, 7):
            hash_based = int.from_bytes(flags_or_timestamp, "little") & 0x01
            if hash_based:
                f.read(8)  # skip hash
            else:
                f.read(4)  # skip timestamp
        else:
            f.read(4)  # skip timestamp for older versions
            
        # Now read the marshal data
        marshal_data = f.read()
        
        try:
            code_obj = marshal.loads(rest)
            return code_obj
        except Exception as e:
            print(f"[!] Failed to load marshal code object from .pyc: {e}")
            sys.exit(1)


def decode_base64_file(b64_file):
    with open(b64_file, "r") as f:
        b64data = f.read()
    return base64.b64decode(b64data)


def decode_base64_string(b64_string):
    return base64.b64decode(b64_string)


def load_code_object(binary_data):
    try:
        return marshal.loads(binary_data)
    except Exception as e:
        print(f"[!] Failed to unmarshal code object: {e}")
        sys.exit(1)


def disassemble_code(code_obj):
    print("\n=== 🔍 Disassembly ===")
    dis.dis(code_obj)
    with open("disassembly.txt", "w") as f:
        dis_text = io.StringIO()
        dis.dis(code_obj, file=dis_text)
        f.write(dis_text.getvalue())
    print("[+] Disassembly saved to disassembly.txt")


def decompile_code(code_obj, py_version="3.12"):
    if decompile is None:
        print("[!] Skipping decompilation (decompyle3 not installed).")
        return

    major, minor = map(int, py_version.split('.'))
    buf = io.StringIO()
    try:
        decompile((major, minor), code_obj, buf)
        decompiled = buf.getvalue()
        print("\n=== 🧠 Decompiled Source ===")
        print(decompiled)
        with open("decompiled.py", "w") as f:
            f.write(decompiled)
        print("[+] Decompiled source saved to decompiled.py")
    except Exception as e:
        print(f"[!] Decompilation failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Reverse engineer Python .pyc or base64-marshalled bytecode.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Path to base64-encoded file")
    group.add_argument("-s", "--string", help="Base64-encoded string")
    group.add_argument("-p", "--pyc", help="Path to .pyc file")
    parser.add_argument("-v", "--version", default="3.12", help="Python version for decompyle3 (default: 3.12)")

    args = parser.parse_args()

    if args.pyc:
        print(f"[*] Loading .pyc file: {args.pyc}")
        code_obj = load_code_from_pyc(args.pyc)

    elif args.file:
        print(f"[*] Decoding from base64 file: {args.file}")
        binary_data = decode_base64_file(args.file)
        code_obj = load_code_object(binary_data)

    elif args.string:
        print("[*] Decoding base64 string input...")
        binary_data = decode_base64_string(args.string)
        code_obj = load_code_object(binary_data)

    else:
        parser.print_help()
        sys.exit(1)

    disassemble_code(code_obj)
    decompile_code(code_obj, py_version=args.version)


if __name__ == "__main__":
    main()
