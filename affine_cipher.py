# affine.py
# Encrypt/decrypt using affine cipher C = (a*p + b) mod 26
# Also shows which 'a' values are allowed (must be coprime with 26)

from math import gcd
import string

ALPH = string.ascii_uppercase
N = 26

def allowed_a_values():
    return [a for a in range(1, N) if gcd(a, N) == 1]

def modinv(a, m):
    # multiplicative inverse of a mod m (returns None if not invertible)
    a = a % m
    for x in range(1, m):
        if (a*x) % m == 1:
            return x
    return None

def encrypt_affine(plaintext, a, b):
    res = []
    for ch in plaintext.upper():
        if ch in ALPH:
            p = ALPH.index(ch)
            c = (a * p + b) % N
            res.append(ALPH[c])
        else:
            res.append(ch)
    return ''.join(res)

def decrypt_affine(ciphertext, a, b):
    inv = modinv(a, N)
    if inv is None:
        raise ValueError(f"a={a} is not invertible mod {N}")
    res = []
    for ch in ciphertext.upper():
        if ch in ALPH:
            c = ALPH.index(ch)
            p = (inv * (c - b)) % N
            res.append(ALPH[p])
        else:
            res.append(ch)
    return ''.join(res)

if __name__ == "__main__":
    print("Allowed 'a' values (coprime with 26):", allowed_a_values())
    # Example
    pt = "HELLO"
    a, b = 5, 8
    ct = encrypt_affine(pt, a, b)
    print("Plain:", pt, "-> Cipher:", ct)
    print("Decrypt:", decrypt_affine(ct, a, b))
