# Auto Alpha Substitution

def apply_substitution(ciphertext, key):
    result = ''
    for char in ciphertext.upper():
        if char in key:
            result += key[char]
        elif char == ' ':
            result += ' '
        else:
            result += '_'
    return result

cipher_text = "MAL TIRRUEZF CR MAL RKZYIOL EX MAL OIY UAE RICF MAL ACWALRM"

# Full substitution key (derived from known plaintext)
substitution_key = {
    'M': 'T',
    'A': 'H',
    'L': 'E',
    'T': 'C',
    'I': 'R',
    'R': 'E',
    'U': 'A',
    'E': 'T',
    'Z': 'U',
    'F': 'R',
    'C': 'O',
    'K': 'K',
    'Y': 'N',
    'O': 'W',
    'X': 'I',
    'N': 'D',
    'D': 'S',
    'W': 'B'
}

decrypted = apply_substitution(cipher_text, substitution_key)
print("Decrypted Message:\n")
print(decrypted)
