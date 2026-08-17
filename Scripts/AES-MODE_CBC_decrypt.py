"""
* ======================================= *
| This script performs AES-CBC decryption |
* ======================================= *

What it does:

1. Imports AES from the PyCryptodome library (Crypto.Cipher)
2. Converts hex strings to bytes for the key, IV (Initialization Vector), and ciphertext
3. Creates an AES cipher in CBC mode with the provided key and IV
4. Decrypts the ciphertext to reveal the plaintext
5. Prints the result in three formats: hex, raw bytes, and ASCII
6. Voila!
"""

from Crypto.Cipher import AES

# AES decryption key (32 bytes = 256-bit key)
key = bytes.fromhex('4ec8484ac58b0916f8bf135ddcf6c0bace79ea6000b67d5ff0d3c891eebaf1c9')

# Initialization Vector for CBC mode (16 bytes = 128-bit block size)
iv  = bytes.fromhex('7a4a50567b051898ccbe5f6830dc15d9')

# Ciphertext to decrypt (encrypted data)
ct  = bytes.fromhex('00e59455d01901d305f56d004837da914f3c812a3a84c8362b7b0af885e68af3')

# Create AES cipher object in CBC (Cipher Block Chaining) mode
# CBC mode requires both key and IV for proper decryption
cipher = AES.new(key, AES.MODE_CBC, iv=iv)

# Decrypt the ciphertext to get plaintext
pt = cipher.decrypt(ct)

# Output the decrypted plaintext in different formats
print("Plaintext hex:", pt.hex())          # Hexadecimal representation
print("Plaintext raw:", pt)                # Raw bytes
print("Plaintext ascii:", pt.decode('ascii', errors='replace'))  # ASCII string (replace invalid chars)