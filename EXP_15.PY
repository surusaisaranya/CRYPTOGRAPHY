# q15_additive_freq_attack.py
import math
import re
from collections import Counter

ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
COMMON_WORDS = {"THE","BE","TO","OF","AND","A","IN","THAT","HAVE","I","IT","FOR","NOT","ON","WITH","HE","AS","YOU","DO","AT"}

def caesar_decrypt(ct, shift):
    res = []
    ct = ct.upper()
    for ch in ct:
        if ch.isalpha():
            res.append(ALPH[(ALPH.index(ch) - shift) % 26])
        else:
            res.append(ch)
    return ''.join(res)

def score_text(txt):
    # simple scoring: count known english words occurrences + word-like token ratio
    words = re.findall(r"[A-Z]+", txt.upper())
    if not words:
        return 0
    word_matches = sum(1 for w in words if w in COMMON_WORDS)
    # also penalize non-letter characters ratio
    letter_count = sum(c.isalpha() for c in txt)
    score = word_matches * 10 + letter_count / (len(txt)+1)
    return score

def top_k_shifts(ciphertext, k=10):
    candidates = []
    for s in range(26):
        pt = caesar_decrypt(ciphertext, s)
        sc = score_text(pt)
        candidates.append((sc, s, pt))
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[:k]

if __name__ == "__main__":
    ct = input("Enter ciphertext (additive/Caesar):\n")
    top = top_k_shifts(ct, k=10)
    print("\nTop candidates:")
    for sc,s,pt in top:
        print(f"Shift={s:2d}  score={sc:.2f}  -> {pt}")
