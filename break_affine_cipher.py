# affine_break.py
from collections import Counter
import string

ALPH = string.ascii_uppercase
N = 26

def modinv(a, m):
    a %= m
    for x in range(1,m):
        if (a*x) % m == 1:
            return x
    return None

def solve_for_a_b(c1, p1, c2, p2):
    # (a*p1 + b) ≡ c1 (mod 26)
    # (a*p2 + b) ≡ c2 (mod 26)
    # subtract: a*(p1-p2) ≡ (c1-c2) (mod 26)
    diff_p = (p1 - p2) % N
    diff_c = (c1 - c2) % N
    inv = modinv(diff_p, N)
    if inv is None:
        return None
    a = (diff_c * inv) % N
    b = (c1 - a*p1) % N
    return a, b

def break_affine_by_freq(ciphertext, top_map=[('B','E'),('U','T')]):
    # top_map: list of (cipher_most, plaintext_guess) pairs attempts
    freq = [c for c,_ in Counter(ciphertext).most_common()]
    # Try all pairings of guesses between top ciphertext letters and plaintexts
    for (c1,p1),(c2,p2) in [ (top_map[0], top_map[1]) ]:
        c1i = ALPH.index(c1)
        c2i = ALPH.index(c2)
        p1i = ALPH.index(p1)
        p2i = ALPH.index(p2)
        sol = solve_for_a_b(c1i, p1i, c2i, p2i)
        if sol:
            a,b = sol
            yield a,b

if __name__=="__main__":
    ct = input("Enter ciphertext: ").upper()
    for a,b in break_affine_by_freq(ct):
        from affine import decrypt_affine
        try:
            print("Try a,b:", a,b, "->", decrypt_affine(ct, a, b))
        except Exception as e:
            print("invalid", e)
