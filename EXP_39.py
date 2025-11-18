# q39_additive_freq_topN.py
import re
ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
COMMON = {"THE","AND","TO","OF","A","IN","IS"}

def decrypt_shift(ct, s):
    out=[]
    for ch in ct.upper():
        if ch.isalpha():
            out.append(ALPH[(ALPH.index(ch)-s)%26])
        else:
            out.append(ch)
    return ''.join(out)

def score(txt):
    words = re.findall(r"[A-Z]+", txt)
    return sum(1 for w in words if w in COMMON)

def top_shifts(ct, k=10):
    candidates=[]
    for s in range(26):
        pt = decrypt_shift(ct,s)
        sc = score(pt)
        candidates.append((sc, s, pt))
    candidates.sort(reverse=True)
    return candidates[:k]

if __name__ == "__main__":
    ciphertext = input("Enter Caesar ciphertext:\n")
    res = top_shifts(ciphertext, k=10)
    for sc,s,pt in res:
        print(f"Shift {s:2d} score={sc} -> {pt}")
