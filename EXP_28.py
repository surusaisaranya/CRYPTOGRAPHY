# q28_diffie_hellman_demo.py
import random

def dh_key(p, g):
    a = random.randint(2, p-2)
    A = pow(g, a, p)
    return a, A

def compute_shared(their, my_secret, p):
    return pow(their, my_secret, p)

if __name__ == "__main__":
    p = 23; g = 5  # small demo prime and generator
    a, A = dh_key(p, g)
    b, B = dh_key(p, g)
    shared1 = compute_shared(B, a, p)
    shared2 = compute_shared(A, b, p)
    print("Shared keys equal:", shared1, shared2)

    # If participants send x^a for public a (i.e., send a^x) this generally fails:
    print("If they send x^a instead of g^a, protocol breaks unless design adjusted; must use generator-based approach.")

    # Can Eve break it? For small p yes via discrete log; for large p properly chosen, discrete log is believed hard.
