# q23_ctr_hill256.py
# CTR mode using a toy Hill 2x2 modulo 256 block cipher on 2-byte blocks.

import numpy as np

MOD = 256

def matrix_mult_mod(A, v, mod=MOD):
    res = [ (A[0][0]*v[0] + A[0][1]*v[1]) % mod,
            (A[1][0]*v[0] + A[1][1]*v[1]) % mod ]
    return res

def ctr_encrypt(plaintext_bytes, key_matrix, counter_start=0):
    # operate on 2-byte blocks
    ct = bytearray()
    cnt = counter_start
    for i in range(0, len(plaintext_bytes), 2):
        block = plaintext_bytes[i:i+2]
        if len(block) < 2: block = block + b'\x00'
        nonce = [ (cnt >> 8) & 0xFF, cnt & 0xFF ]
        keystream = matrix_mult_mod(key_matrix, nonce)
        ks_bytes = bytes([keystream[0] % 256, keystream[1] % 256])
        ct_block = bytes(a ^ b for a,b in zip(block, ks_bytes))
        ct.extend(ct_block)
        cnt += 1
    return bytes(ct)

def ctr_decrypt(ct_bytes, key_matrix, counter_start=0):
    return ctr_encrypt(ct_bytes, key_matrix, counter_start)  # symmetric XOR

if __name__ == "__main__":
    key = [[3,5],[1,7]]  # example
    pt = bytes([0x00,0x01,0x00,0x02,0x00,0x04])
    ct = ctr_encrypt(pt, key, counter_start=0)
    rec = ctr_decrypt(ct, key, counter_start=0)
    print("PT:", pt)
    print("CT:", ct)
    print("REC:", rec)
