# q31_cmac_subkeys.py
# Generate CMAC subkeys K1 and K2 from L = E_K(0^b).
# For block size 64 bits, Rb = 0x1B. For 128 bits, Rb = 0x87.
# The function expects L as bytes of length block_bytes (8 or 16).

def bytes_to_bit_list(b):
    out=[]
    for byte in b:
        for i in range(8):
            out.append((byte >> (7-i)) & 1)
    return out

def bit_list_to_bytes(bits):
    by=[]
    for i in range(0,len(bits),8):
        val=0
        for j in range(8):
            val = (val<<1) | bits[i+j]
        by.append(val)
    return bytes(by)

def left_shift_one_bit(b):
    bits = bytes_to_bit_list(b)
    shifted = bits[1:] + [0]
    return bit_list_to_bytes(shifted)

def xor_bytes(a,b):
    return bytes(x^y for x,y in zip(a,b))

def generate_subkeys(L_bytes):
    n = len(L_bytes)
    if n == 8:
        Rb = 0x1B
    elif n == 16:
        Rb = 0x87
    else:
        raise ValueError("Only block sizes 64 (8 bytes) or 128 (16 bytes) supported in this demo")
    # K1 = L << 1
    msb = (L_bytes[0] >> 7) & 1
    K1 = left_shift_one_bit(L_bytes)
    if msb == 1:
        # XOR the last byte with Rb (i.e., XOR whole block with constant whose low-order byte is Rb)
        const = bytes([0]*(n-1) + [Rb])
        K1 = xor_bytes(K1, const)
    # K2 from K1
    msb2 = (K1[0] >> 7) & 1
    K2 = left_shift_one_bit(K1)
    if msb2 == 1:
        const = bytes([0]*(n-1) + [Rb])
        K2 = xor_bytes(K2, const)
    return K1, K2

if __name__ == "__main__":
    # Example: given L (result of encrypting 0^b under K). Here we use a dummy L for demo.
    # In practice, L = E_K(0^b) where E_K is the block cipher under key K.
    L_demo_128 = bytes.fromhex('6BC1BEE22E409F96E93D7E117393172A')[:16]  # sample 16 bytes (demo)
    K1, K2 = generate_subkeys(L_demo_128)
    print("K1 (hex):", K1.hex())
    print("K2 (hex):", K2.hex())

    print("\nConstants used:")
    print("  For 64-bit block Rb = 0x1B")
    print("  For 128-bit block Rb = 0x87")
    print("\nWhy left-shift + XOR works (brief):")
    print("  Left shift multiplies the polynomial representation by x in GF(2^b).")
    print("  If MSB was 1, the multiplication over the finite field wraps around — implemented by XOR with Rb.")
