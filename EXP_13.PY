# q13_hill_known_plaintext.py
# Recover 2x2 Hill cipher key given plaintext-ciphertext pairs (mod 26).
# Usage: run and follow prompts; example provided in comments.

import math

ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = 26

def inv_mod(a, m):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def mat_inv_2x2_mod(mat):
    # mat is [[a,b],[c,d]]
    a,b = mat[0]; c,d = mat[1]
    det = (a*d - b*c) % N
    invdet = inv_mod(det, N)
    if invdet is None:
        return None
    # adjugate matrix [[d, -b], [-c, a]] times invdet
    inv = [[( d * invdet) % N, ((-b) * invdet) % N],
           [((-c) * invdet) % N, ( a * invdet) % N]]
    return inv

def mult_mat_2x2(a, b):
    # multiply 2x2 mats mod N
    return [[(a[0][0]*b[0][0] + a[0][1]*b[1][0]) % N,
             (a[0][0]*b[0][1] + a[0][1]*b[1][1]) % N],
            [(a[1][0]*b[0][0] + a[1][1]*b[1][0]) % N,
             (a[1][0]*b[0][1] + a[1][1]*b[1][1]) % N]]

def text_to_pairs(s):
    s = ''.join([c for c in s.upper() if c.isalpha()])
    if len(s) % 2 == 1:
        s += 'X'
    pairs = []
    for i in range(0, len(s), 2):
        pairs.append([ALPH.index(s[i]), ALPH.index(s[i+1])])
    return pairs


