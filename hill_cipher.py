# hill2.py
import numpy as np
import string

ALPH = string.ascii_uppercase
N = 26

def text_to_vec(text):
    text = ''.join([c for c in text.upper() if c in ALPH])
    if len(text) % 2 == 1:
        text += 'X'
    pairs = [ [ALPH.index(text[i]), ALPH.index(text[i+1])] for i in range(0,len(text),2) ]
    return np.array(pairs).T  # shape 2 x m

def vec_to_text(mat):
    s = ''
    for col in mat.T:
        s += ALPH[int(col[0])%26] + ALPH[int(col[1])%26]
    return s

def inv_mod_matrix(mat, mod):
    det = int(round(np.linalg.det(mat))) % mod
    inv_det = None
    for i in range(mod):
        if (det * i) % mod == 1:
            inv_det = i; break
    if inv_det is None:
        raise ValueError("Matrix not invertible mod {}".format(mod))
    # adjugate matrix
    adj = np.array([[mat[1,1], -mat[0,1]], [-mat[1,0], mat[0,0]]])
    inv = (inv_det * adj) % mod
    return inv

def encrypt(pt, key):
    P = text_to_vec(pt)
    C = (key.dot(P)) % N
    return vec_to_text(C)

def decrypt(ct, key):
    C = text_to_vec(ct)
    Kinv = inv_mod_matrix(key, N)
    P = (Kinv.dot(C)) % N
    return vec_to_text(P)

if __name__=="__main__":
    key = np.array([[9,4],[5,7]])
    pt = "MEETMEATTHEUSUALPLACEATTENRATHERTHANEIGHTOCLOCK"
    ct = encrypt(pt, key)
    print("Ciphertext:", ct)
    print("Decrypted:", decrypt(ct, key))
