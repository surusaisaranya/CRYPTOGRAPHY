# q30_cbc_mac.py
# CBC-MAC for one-block message using toy block cipher (XOR with key byte)
BLOCK_SIZE = 8

def pad_oneblock(block, bs=BLOCK_SIZE):
    if len(block) != bs:
        raise ValueError("expects one full block")
    return block

def toy_block_encrypt(block, key_byte):
    return bytes(b ^ key_byte for b in block)

def cbc_mac_oneblock(message_block, key_byte, iv=None):
    if iv is None:
        iv = bytes([0]*BLOCK_SIZE)
    # CBC-MAC for one-block T = E_k(M XOR IV)
    x = bytes(a ^ b for a,b in zip(message_block, iv))
    return toy_block_encrypt(x, key_byte)

if __name__ == "__main__":
    M = b'ABCDEFGH'  # 8-byte block
    K = 0x5A
    tag = cbc_mac_oneblock(M, K)
    print("Message:", M)
    print("Tag (hex):", tag.hex())
