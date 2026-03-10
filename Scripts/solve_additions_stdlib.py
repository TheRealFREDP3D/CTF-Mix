import socket
import re
import time

HOST = 'HOST' # <---
PORT = 1337 # <---

# persistent buffer to avoid over-reading past '?'
_buffer = bytearray()

def recv_until(sock, stop=b'?'):
    global _buffer
    while True:
        idx = _buffer.find(stop)
        if idx != -1:
            # include the stop byte
            out = bytes(_buffer[:idx+1])
            # keep the remainder for next call
            _buffer = _buffer[idx+1:]
            return out
        # need more data
        chunk = sock.recv(4096)
        if not chunk:
            out = bytes(_buffer)
            _buffer.clear()
            return out
        _buffer.extend(chunk)


def main():
    try:
        with socket.create_connection((HOST, PORT), timeout=120.0) as s:
            s.settimeout(120.0)
            # disable Nagle for low-latency small writes
            try:
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            except Exception:
                pass

            for i in range(500):
                # keep reading until we encounter a chunk that actually contains an addition question
                while True:
                    q = recv_until(s, b'?').decode(errors='ignore').strip()
                    m = re.search(r'^(?:.*?)(\d+)\s*\+\s*(\d+)\s*\?\s*$', q)
                    if m:
                        a = int(m.group(1)) + int(m.group(2))
                        s.sendall(f"{a}\r\n".encode())
                        print(f"Problem {i+1}: {m.group(1)} + {m.group(2)} = {a}")
                        break
                    # if not matched, ignore this '?'-terminated chunk and continue reading

            # read the remaining output (e.g., the flag)
            s.settimeout(3.0)
            chunks = []
            try:
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
            except socket.timeout:
                pass

            out = b''.join(chunks).decode(errors='ignore')
            print(out)
    except (TimeoutError, ConnectionResetError) as e:
        print(f"Connection error: {e}")


if __name__ == '__main__':
    main()
