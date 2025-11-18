# caesar_bruteforce.py
import string

ALPH = string.ascii_uppercase

def caesar_shift(text, shift):
    res = []
    for ch in text.upper():
        if ch in ALPH:
            res.append(ALPH[(ALPH.index(ch)-shift) % 26])  # decrypt with shift
        else:
            res.append(ch)
    return ''.join(res)

def top_k_caesar(ciphertext,k=10):
    results = []
    for s in range(26):
        results.append((s, caesar_shift(ciphertext, s)))
    return results[:k]

if __name__=="__main__":
    ct = input("Ciphertext: ")
    for s,pt in top_k_caesar(ct,26):
        print(f"Shift {s}: {pt}")
