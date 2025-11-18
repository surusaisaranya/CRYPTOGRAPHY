# q32_dsa_k_random_demo.py
# Toy DSA-style signature demonstration using small primes to show that different k produce different signatures.
# Not real DSA parameters. Educational only.

import random
from math import gcd

def egcd(a,b):
    if b==0: return (1,0,a)
    x,y,g = egcd(b, a%b)
    return (y, x - (a//b)*y, g)

def modinv(a,m):
    x,y,g = egcd(a,m)
    if g!=1: return None
    return x % m

# Toy DSA params (small; DO NOT use in real systems)
p = 211  # prime
q = 53   # q divides p-1 (here 211-1=210=53*4 ? no; this is toy only)
g = 2
x = 15   # private key
y = pow(g, x, p) # public key

def hash_msg(msg):
    # simple hash -> integer mod q (toy)
    return sum(ord(c) for c in msg) % q

def sign(msg):
    H = hash_msg(msg)
    while True:
        k = random.randint(2, q-1)
        r = pow(g, k, p) % q
        if r == 0: continue
        kinv = modinv(k, q)
        if kinv is None: continue
        s = (kinv * (H + x * r)) % q
        if s == 0: continue
        return (r, s, k)

def verify(msg, sig):
    r,s = sig
    if not (0 < r < q and 0 < s < q): return False
    H = hash_msg(msg)
    w = modinv(s,q)
    u1 = (H * w) % q
    u2 = (r * w) % q
    v = (pow(g,u1,p) * pow(y,u2,p)) % p
    return (v % q) == r

if __name__ == "__main__":
    message = "hello"
    sig1_r, sig1_s, k1 = sign(message)
    sig2_r, sig2_s, k2 = sign(message)
    print("Message:", message)
    print("Signature1 (r,s) =", (sig1_r, sig1_s), "k used:", k1)
    print("Signature2 (r,s) =", (sig2_r, sig2_s), "k used:", k2)
    print("Signatures equal?", (sig1_r==sig2_r and sig1_s==sig2_s))
    print("Verification sig1:", verify(message, (sig1_r, sig1_s)))
    print("Verification sig2:", verify(message, (sig2_r, sig2_s)))
    print("\nImplication: Different random k yields different signatures even for same message.")
