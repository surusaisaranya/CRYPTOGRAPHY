# q25_rsa_gcd_demo.py
# If a plaintext block shares a non-trivial gcd with n, that gcd reveals a factor of n.

import math

def demo(n, plaintext_block):
    g = math.gcd(plaintext_block, n)
    return g

if __name__ == "__main__":
    # Example: n = p*q where p=59,q=61 -> n=3599
    n = 3599
    # Suppose one plaintext block equals p (59) or multiple thereof
    pt_block = 59
    g = demo(n, pt_block)
    print("gcd(pt_block, n) =", g)
    if 1 < g < n:
        print("Non-trivial factor found:", g)
    else:
        print("No factor found.")
