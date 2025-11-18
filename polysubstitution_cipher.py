def encrypt(plaintext, key):
    key = key.lower()
    ciphertext = ""
    j = 0  # pointer for key

    for ch in plaintext:
        if ch.isalpha():  # encrypt only letters
            shift = ord(key[j % len(key)]) - ord('a')
            base = ord('a') if ch.islower() else ord('A')
            ciphertext += chr((ord(ch) - base + shift) % 26 + base)
            j += 1
        else:
            ciphertext += ch  # keep spaces
    return ciphertext

plaintext = input("Enter plaintext: ")
key = input("Enter key: ")

print("Encrypted:", encrypt(plaintext, key))