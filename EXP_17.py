# q17_des_subkeys_decryption.py
# Produces 16 DES subkeys in decryption order (K16..K1) from a 64-bit hex key.
# Note: This code implements the DES key schedule (PC-1, left shifts, PC-2).

PC1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

# number of left shifts per round
SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def hex_to_bitlist(hexkey):
    val = int(hexkey, 16)
    bits = [(val >> i) & 1 for i in reversed(range(64))]
    return bits

def permute(bits, table):
    return [bits[i-1] for i in table]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_subkeys_decryption(hexkey):
    bits64 = hex_to_bitlist(hexkey)
    # apply PC-1 -> 56 bits
    key56 = permute(bits64, PC1)
    C = key56[:28]
    D = key56[28:]
    subkeys = []
    for i,sh in enumerate(SHIFTS):
        C = left_shift(C, sh)
        D = left_shift(D, sh)
        CD = C + D
        K = permute(CD, PC2)  # 48-bit subkey
        subkeys.append(K)
    # subkeys now K1..K16; for decryption, use reversed order
    subkeys_decrypt_order = list(reversed(subkeys))
    return subkeys_decrypt_order

def bits_to_hex(bits):
    val = 0
    for b in bits:
        val = (val << 1) | b
    # return hex string padded
    hx = hex(val)[2:].upper()
    hx = hx.zfill(len(bits)//4)
    return hx

if __name__ == "__main__":
    sample_key = input("Enter 64-bit key in hex (16 hex chars), e.g. 133457799BBCDFF1 :\n").strip()
    subkeys = generate_subkeys_decryption(sample_key)
    print("16 subkeys in decryption order (K16 .. K1) (hex 48-bit each):")
    for i,k in enumerate(subkeys, start=16):
        print(f"K{i:2d} =", bits_to_hex(k))
    print("\nNote: These are subkeys for DES used in reverse for decryption (K16..K1).")
