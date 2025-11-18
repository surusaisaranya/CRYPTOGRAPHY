# q20_ecb_cbc_error_simulation.py
from copy import deepcopy

BLOCK_SIZE = 8

def split_blocks(data, block_size=BLOCK_SIZE):
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    return blocks

def ecb_encrypt_blocks(plaintext_blocks, key):
    # toy block cipher: XOR with key byte
    return [bytes(b ^ key for b in blk) for blk in plaintext_blocks]

def ecb_decrypt_blocks(cipher_blocks, key):
    return [bytes(b ^ key for b in blk) for blk in cipher_blocks]

def cbc_encrypt_blocks(plaintext_blocks, key, iv):
    ct_blocks = []
    prev = iv
    for blk in plaintext_blocks:
        xored = bytes(a ^ b for a,b in zip(blk, prev))
        ct = bytes(b ^ key for b in xored)
        ct_blocks.append(ct)
        prev = ct
    return ct_blocks

def cbc_decrypt_blocks(cipher_blocks, key, iv):
    pt_blocks = []
    prev = iv
    for ct in cipher_blocks:
        x = bytes(b ^ key for b in ct)
        pt = bytes(a ^ b for a,b in zip(x, prev))
        pt_blocks.append(pt)
        prev = ct
    return pt_blocks

def flip_bit(bytes_obj, block_index, byte_index, bit_index=0):
    ba = bytearray(bytes_obj)
    pos = block_index*BLOCK_SIZE + byte_index
    ba[pos] ^= (1 << bit_index)
    return bytes(ba)

if __name__ == "__main__":
    key = 0xAA
    iv = bytes([0]*BLOCK_SIZE)
    plaintext = b"Block000Block111Block222Block333"  # 4 blocks of 8 bytes each
    p_blocks = split_blocks(plaintext)

    # ECB encrypt
    ct_ecb = ecb_encrypt_blocks(p_blocks, key)
    # CBC encrypt
    ct_cbc = cbc_encrypt_blocks(p_blocks, key, iv)

    # Simulate corruption in transmitted C1 (first ciphertext block) for CBC
    ct_cbc_corrupt = deepcopy(ct_cbc)
    # flip a bit in first ciphertext block
    corrupted_first = bytearray(ct_cbc_corrupt[0])
    corrupted_first[0] ^= 0x01
    ct_cbc_corrupt[0] = bytes(corrupted_first)

    # Decrypt corrupted CBC
    pt_cbc_after = cbc_decrypt_blocks(ct_cbc_corrupt, key, iv)
    print("CBC decrypted blocks after corrupting C1:")
    for i,blk in enumerate(pt_cbc_after):
        print(i, blk)

    print("\nAnalysis Q20:")
    print("a) If C1 is corrupted in transmission, CBC decryption: P1 and P2 get corrupted, but blocks beyond P2 are not affected.")
    print("   Reason: P1 uses corrupted C1 directly; P2 uses C1 XOR step to recover and thus affected. P3 uses C2 (which was received correctly), so not affected.")
    print("b) If a bit error is in source plaintext P1 (before encryption), how many ciphertext blocks are changed?")
    print("   - In ECB: only C1 changes (one block affected).")
    print("   - In CBC encryption: due to chaining, C1 changes because it is encryption of (P1 XOR IV).")
    print("     Also since C1 changed, during transmission this altered C1 will affect P2 on decryption (propagation). But source plaintext bit error does not further propagate beyond C1 during encryption phase (only C1 changes).")
    print("\nDetailed effect at receiver:")
    print("- Error in transmitted C1 => P1 and P2 corrupted, beyond P2 ok.")
    print("- Bit error in source P1 (before encryption) => only C1 differs; when ciphertext transmitted, if C1 is correct but original P1 was different, receiver recovers that different P1; no further blocks corrupted unless transmission errors occur.")
