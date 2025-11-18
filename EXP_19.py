# q19_cbc_3des_simulation.py
# Illustrative CBC mode using a toy block cipher (not real DES/3DES).
# Demonstrates how CBC works and answers security/performance questions.

from typing import List

BLOCK_SIZE = 8  # bytes

def pad_pkcs7(data, block_size=BLOCK_SIZE):
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len])*pad_len

def unpad_pkcs7(data):
    pad_len = data[-1]
    return data[:-pad_len]

def toy_des_block_encrypt(block: bytes, key: int) -> bytes:
    # VERY SIMPLE toy block cipher: XOR with key bytes (illustrative only)
    return bytes((b ^ (key & 0xFF)) for b in block)

def toy_des_block_decrypt(block: bytes, key: int) -> bytes:
    # symmetric XOR
    return bytes((b ^ (key & 0xFF)) for b in block)

def cbc_encrypt(plaintext: bytes, iv: bytes, keys: List[int]) -> bytes:
    # keys: list of round keys (for 3DES you'd have 3 keys)
    pt = pad_pkcs7(plaintext)
    prev = iv
    ciphertext = b''
    # Emulate 3DES by encrypting with key1, decrypt with key2, encrypt with key3 (EDE)
    for i in range(0, len(pt), BLOCK_SIZE):
        block = bytes(a ^ b for a,b in zip(pt[i:i+BLOCK_SIZE], prev))
        # apply toy 3-stage: E(k1), D(k2), E(k3)
        y = toy_des_block_encrypt(block, keys[0])
        y = toy_des_block_decrypt(y, keys[1])
        y = toy_des_block_encrypt(y, keys[2])
        ciphertext += y
        prev = y
    return ciphertext

def cbc_decrypt(ciphertext: bytes, iv: bytes, keys: List[int]) -> bytes:
    prev = iv
    plaintext = b''
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        # reverse 3DES: D(k3), E(k2), D(k1)
        x = toy_des_block_decrypt(block, keys[2])
        x = toy_des_block_encrypt(x, keys[1])
        x = toy_des_block_decrypt(x, keys[0])
        pt_block = bytes(a ^ b for a,b in zip(x, prev))
        plaintext += pt_block
        prev = block
    return unpad_pkcs7(plaintext)

if __name__ == "__main__":
    keys = [0x1A, 0x2B, 0x3C]  # toy keys (just bytes)
    iv = b'\x00'*BLOCK_SIZE
    message = b"Attack at dawn! Meet at 10."
    ct = cbc_encrypt(message, iv, keys)
    print("Ciphertext (hex):", ct.hex())
    recovered = cbc_decrypt(ct, iv, keys)
    print("Recovered plaintext:", recovered)

    print("\nAnswers:")
    print("a) For security: 3DES is more secure than DES (3DES uses multiple DES ops).")
    print("b) For performance: DES is faster (single DES) — 3DES is roughly ~3x slower.")
    print("\nNote: This script uses a toy block cipher to illustrate CBC mechanics. For real 3DES use a crypto library.")
