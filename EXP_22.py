# q22_cbc_affine256.py
# CBC mode using affine modulo 256 as block cipher on single-byte blocks (educational).
# Note: Affine parameters must be coprime with 256 for invertibility (use odd 'a').

MOD = 256

def modinv(a, m=MOD):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt_byte(b, a, c):
    return (a * b + c) % MOD

def affine_decrypt_byte(x, a, c):
    inv = modinv(a, MOD)
    if inv is None: raise ValueError("a not invertible")
    return (inv * (x - c)) % MOD

def cbc_encrypt(bytes_in, iv, a, c):
    prev = iv
    ct = []
    for b in bytes_in:
        x = b ^ prev
        y = affine_encrypt_byte(x, a, c)
        ct.append(y); prev = y
    return bytes(ct)

def cbc_decrypt(bytes_ct, iv, a, c):
    prev = iv
    pt = []
    for y in bytes_ct:
        x = affine_decrypt_byte(y, a, c)
        p = x ^ prev
        pt.append(p); prev = y
    return bytes(pt)

if __name__ == "__main__":
    # Example with small test
    a,c = 5, 7  # a must be odd for mod256 invertibility
    iv = 0xAA
    plaintext = bytes([0x00,0x01,0x02,0x03])
    ct = cbc_encrypt(plaintext, iv, a, c)
    rec = cbc_decrypt(ct, iv, a, c)
    print("PT:", plaintext)
    print("CT:", ct)
    print("REC:", rec)
