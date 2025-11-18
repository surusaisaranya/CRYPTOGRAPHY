# q27_rsa_perchar_demo.py
# Shows that encrypting single letters 0..25 separately is insecure: small plaintext space -> brute force.

def encrypt_block(m, e, n):
    return pow(m, e, n)

def brute_force_single_char(ct, e, n):
    # try all 0..25
    for m in range(26):
        if pow(m, e, n) == ct:
            return m
    return None

if __name__ == "__main__":
    # small demo with small key (educational)
    e = 3; p=61; q=59; n = p*q
    msg = "HELLO"
    ct_blocks = [encrypt_block(ord(ch)-65, e, n) for ch in msg]
    print("Cipher blocks:", ct_blocks)
    recovered = [brute_force_single_char(c, e, n) for c in ct_blocks]
    print("Recovered numeric letters:", recovered)
    print("Recovered text:", ''.join(chr(r+65) for r in recovered))
