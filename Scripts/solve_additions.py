# C:\Users\bloga\solve_additions.py
import socket, re, sys, time

HOST = '<TARGET_IP>'
PORT = <TARGET_PORT>
TOTAL = 500

# Configurable timeouts
CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 5.0
QUESTION_TIMEOUT = 30.0

# Progress verbosity
VERBOSE = True

class BufferedReader:
    def __init__(self, sock):
        self.s = sock
        self.buf = b''
    def recv_until(self, delim=b'?', timeout=QUESTION_TIMEOUT, max_bytes=1_000_000):
        end_by = time.time() + timeout
        while True:
            idx = self.buf.find(delim)
            if idx != -1:
                out = self.buf[:idx+1]
                self.buf = self.buf[idx+1:]
                return out
            # Need more data
            now = time.time()
            if now >= end_by:
                raise TimeoutError('Timed out waiting for delimiter')
            try:
                chunk = self.s.recv(4096)
            except socket.timeout:
                continue  # keep looping until overall timeout
            if not chunk:
                raise ConnectionError('Remote closed the connection')
            self.buf += chunk
            if len(self.buf) > max_bytes:
                raise RuntimeError('Buffer exceeded max size; unexpected protocol data')


def main():
    addr = (HOST, PORT)
    with socket.create_connection(addr, timeout=CONNECT_TIMEOUT) as s:
        s.settimeout(READ_TIMEOUT)
        try:
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception:
            pass
        reader = BufferedReader(s)
        solved = 0
        # Consume any banner up to the first '?', if present
        try:
            pre = reader.recv_until(b'?', timeout=QUESTION_TIMEOUT)
        except Exception:
            pre = b''
        while solved < TOTAL:
            # Ensure we have a question ending with '?'
            try:
                qbytes = pre if pre.endswith(b'?') else reader.recv_until(b'?', timeout=QUESTION_TIMEOUT)
            except Exception as e:
                print(f'Error receiving question {solved+1}: {e}', file=sys.stderr)
                return 1
            pre = b''  # reset after first iteration
            q = qbytes.decode('utf-8', errors='ignore')
            m = re.search(r'(\d+)\s*\+\s*(\d+)', q)
            if not m:
                # Not a question; continue scanning until the next '?'
                continue
            a = int(m.group(1)); b = int(m.group(2)); ans = a + b
            try:
                s.sendall(f"{ans}\r\n".encode('ascii'))
                # small pacing to avoid overwhelming the service
                time.sleep(0.005)
            except Exception as e:
                print(f'Error sending answer for {a} + {b}: {e}', file=sys.stderr)
                return 1
            solved += 1
            if VERBOSE:
                print(f'Problem {solved}: {a} + {b} = {ans}')
        # Read trailing output/flag
        flag_chunks = []
        end_by = time.time() + 5.0
        while time.time() < end_by:
            try:
                chunk = s.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            flag_chunks.append(chunk)
        out = b''.join(flag_chunks).decode('utf-8', errors='ignore').strip()
        if out:
            print(out)
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f'Fatal error: {e}', file=sys.stderr)
        sys.exit(1)
