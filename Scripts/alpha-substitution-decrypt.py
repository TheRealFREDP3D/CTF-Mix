# =========================================
#    Monoalphabetic Substitution Solver 
# -----------------------------------------
# Author: Frederick Pellerin
# Github: https://github.com/therealfredp3d
# X: @TheRealFREDP3D
# =========================================

from collections import Counter

def frequency_analysis(text):
    text = text.replace(" ", "").upper()
    return Counter(text)

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

# -------------------------------------------------------------------------
# Cipher text input
cipher_text = "MAL TIRRUEZF CR MAL RKZYIOL EX MAL OIY UAE RICF MAL ACWALRM"
# --------------------------------------------------------------------------

# Analyze frequency
freq = frequency_analysis(cipher_text)
print("Letter Frequency Analysis:")
for letter, count in freq.most_common():
    print(f"{letter}: {count}")

# You can update this manually based on guesses or frequency
# For example: let's start with M -> T, A -> H, L -> E (guessing MAL = THE)
substitution_key = {
    'M': 'T',
    'A': 'H',
    'L': 'E',
    # Add more guesses here
    # 'T': 'C', etc.
}

# Show current decryption
decrypted = apply_substitution(cipher_text, substitution_key)
print("\nPartial Decryption:")
print(decrypted)
