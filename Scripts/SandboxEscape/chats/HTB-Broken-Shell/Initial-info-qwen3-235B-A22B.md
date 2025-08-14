# HTB: Broken Shell

## Initial Information - Qwen3-235B-A22B

CHALLENGE DESCRIPTION
We've built a secure sandbox environment that only allows specific symbols and numbers. It's designed to be inescapable—security at its best!

```bash
❯ nc -nv 94.237.120.71 34065
Connection to 94.237.120.71 34065 port [tcp/*] succeeded!
TERM environment variable not set.      

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⣀⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡴⠦⣤⣴⡟⠉⠉⡗⠚⡇⠀⠈⡷⢤⠖⠒⠲⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣀⡇⠀⠀⢸⠀⡇⠀⠀⠇⠀⡇⠀⠀⡇⢸⠀⠀⢠⠋⡝⠉⠓⢦⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠊⠁⢣⢰⠀⠀⠈⡆⢳⠀⠀⠀⠀⡇⠀⢸⠀⡇⠀⠀⡜⢰⠃⠀⠀⡜⢦⢤⣀⠀⠀⠀⠀⠀
⠀⠀⠀⡠⢴⠻⡀⠀⠈⡎⡇⠀⠀⢃⢸⠀⠀⢸⠀⡇⠀⢸⢀⡇⠀⢠⠃⡎⠀⠀⡼⢡⠃⠀⠙⡆⠀⠀⠀⠀
⠀⠀⢸⠁⠀⢣⢱⡀⠀⢸⣸⡀⠀⢸⠈⡄⠀⢸⠀⡇⠀⠘⢸⠀⠀⡸⢰⠁⠀⢰⢡⠏⠀⠀⡜⡿⢤⡀⠀⠀
⠀⣠⠞⣷⡄⠀⢣⢣⠀⠀⢧⢇⠀⠈⡆⡇⠀⢸⠀⡇⠀⡇⡼⠀⢀⠇⡏⠀⢠⢇⠎⠀⢀⡜⡜⠁⠀⢳⠀⠀
⢸⡁⠀⠈⢻⣦⠀⢫⢧⠀⠘⡾⡄⠀⣇⢡⠀⢸⠀⡇⠀⡇⡇⠀⣸⢸⠀⢀⠏⡜⠀⢀⢎⠞⠀⢀⡴⡻⡄⠀
⣰⠻⣆⠀⠀⠻⣷⡀⢻⣇⠀⢹⢧⠀⢸⢸⠀⢸⠀⡇⢠⢿⠃⠀⡇⡇⠀⡜⡾⠀⢠⢾⠎⠀⡰⢫⠞⠀⡟⠀
⢹⣅⠙⢷⣄⠀⠙⣷⡀⢻⡄⠈⣿⡄⠘⡞⡆⢸⠀⡇⢸⢸⠀⢸⣸⠀⡸⡽⠁⢠⣯⠋⣠⣾⡖⢁⡠⠚⣿⡄
⠘⣏⠳⣄⠙⣦⡀⠘⢧⠀⢻⡄⠸⣧⠀⠇⡇⢸⠀⡇⢸⡌⠀⣇⠇⢰⣱⠁⣠⡻⢃⡴⡷⢋⡴⢋⡤⣺⠇⠀
⠀⢹⡕⢄⠑⢌⠛⢦⠈⢣⡀⢻⡀⢳⠀⢸⢳⢸⠀⡇⣎⡇⢸⠽⢠⠇⠁⣰⡿⢡⣾⢞⣴⣯⡔⣫⢴⠟⠀⠀
⠀⠀⠙⢦⣝⢦⡑⢄⠳⣌⠳⡈⢧⠈⡆⠸⣼⠸⡀⡇⡏⠁⡏⢀⠎⠀⡰⠉⡱⠋⡡⣫⣞⣽⣋⣴⠟⠀⠀⠀
⠀⠀⠀⠀⠉⠻⢿⣮⡳⣌⢦⡱⡌⣆⢸⠀⡟⡆⡇⡇⡇⢸⠁⡜⠀⡼⠁⡜⠁⣪⠞⣿⡵⠟⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⡾⣾⣷⣵⡜⡜⡄⠇⢣⡇⡇⢳⠁⡎⠀⠀⡼⢁⠞⠠⢾⡵⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣷⠈⠛⢿⣾⣾⣾⠘⠈⠁⠇⠀⠀⠁⠀⠾⠁⢀⣤⠞⢫⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢧⣄⠀⠙⠿⣟⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⣡⡴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠒⠦⠬⠷⢄⡀⠀⠀⠀⣠⠴⠟⠚⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


[*] Allowed characters: ^[0-9${}/?"[:space:]:&>_=()]+$

Broken@Shell$
```

---

## Answer

# Solving the Secure Sandbox Challenge

This is a restricted shell environment that only allows specific characters. Let's analyze what we have:

## Allowed Characters
The regex `^[0-9${}/?"[:space:]:&>_=()]+$` tells us we can use:
- Digits (0-9)
- `${}/?"` special characters
- Whitespace
- Colon `:`, ampersand `&`, greater-than `>`, equals `_=` 
- Parentheses `()`

## Observations
1. This is a restricted shell with a custom prompt `Broken@Shell$`
2. We're seeing an ASCII art logo/banner
3. The connection drops after some inactivity, suggesting there's a script running

## Strategy for Escaping the Sandbox

With these kinds of restricted shells, we want to:
1. Check basic command execution
2. Try to access environment variables
3. Look for ways to execute commands using allowed characters
4. Attempt to spawn a proper shell

### First Tests
I would try these commands first to see what works:
```bash
echo $PATH
env
set
which sh
which bash
```

### Exploitation Approaches

#### 1. Using allowed characters to execute commands
We can try to execute commands using the allowed characters. Some possibilities:
```bash
${IFS} - acts as whitespace
; can be used to separate commands
> to redirect output
() to create subshells
```

#### 2. Using environment variables
We might try manipulating environment variables to get more functionality:
```bash
IFS=$' \t\n'
export IFS
```

#### 3. Trying to spawn a shell
Given the allowed characters, I might try:
```bash
sh${IFS}-c${IFS}"exec${IFS}sh"
bash${IFS}-c${IFS}"exec${IFS}bash"
```

#### 4. Using redirection and file descriptors
Since `>&=` are allowed, we could try:
```bash
sh 1>&2 2>&1  # Redirect stdin/stdout
```

#### 5. Looking for command injection vectors
If any commands are available, we might try:
```bash
echo ${PATH}
cat /etc/passwd
```

Without direct access to test, my recommendation would be to first check what commands are available by trying to list files or print environment variables. Then use that information to craft an appropriate escape.

Did you have a specific question about this challenge or was there a particular error you encountered when trying to solve it?