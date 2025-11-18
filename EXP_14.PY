# q14_one_time_vigenere.py
ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def normalize(s):
    return ''.join([c for c in s.upper() if c.isalpha()])

def encrypt_otv(plaintext, key_stream):
    pt = normalize(plaintext)
    if len(key_stream) < len(pt):
        raise ValueError("Key stream shorter than plaintext")
    ct = []
    for i,ch in enumerate(pt):
        p = ALPH.index(ch)
        k = key_stream[i] % 26
        ct.append(ALPH[(p + k) % 26])
    return ''.join(ct)

def derive_key_from_pt_ct(plaintext, ciphertext):
    pt = normalize(plaintext)
    ct = normalize(ciphertext)
    if len(pt) != len(ct):
        raise ValueError("Lengths differ")
    key = []
    for i in range(len(pt)):
        k = (ALPH.index(ct[i]) - ALPH.index(pt[i])) % 26
        key.append(k)
    return key

if __name__ == "__main__":
    # Part (a)
    plaintext = "send more money"
    key_stream = [9,0,1,7,23,15,21,14,11,11,2,8,9]
    ciphertext = encrypt_otv(plaintext, key_stream)
    print("Part (a) ciphertext:", ciphertext)

    # Part (b) Suppose ciphertext from (a) is to be decrypted to "cash not needed"
    desired_pt = "cash not needed"
    # We already have ciphertext from part (a) (normalized)
    ct = ciphertext
    # derive key that maps ct -> desired_pt: key_i = (pt_i - ct_i) mod26
    # Ensure lengths match by using substring/pad/truncate as needed
    pt_norm = normalize(desired_pt)
    ct_norm = ct[:len(pt_norm)]
    key_for_mapping = derive_key_from_pt_ct(pt_norm, ct_norm)
    print("Part (b) derived key stream (numbers):", key_for_mapping)
    print("Verify decryption (ct -> desired_pt) using derived key:")
    # decrypt: (ct - key) mod26 -> pt
    recovered = []
    for i,ch in enumerate(ct_norm):
        recovered.append(ALPH[(ALPH.index(ch) - key_for_mapping[i]) % 26])
    print("Recovered plaintext:", ''.join(recovered))
