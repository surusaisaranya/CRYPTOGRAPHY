# q26_rsa_key_leak_demo.py
# Demonstrates that if Bob leaks private key d but keeps modulus n, creating new (e2,d2) with same n is dangerous.

def demonstrate(n, leaked_d, new_e):
    # Without factoring n we cannot compute private key directly,
    # but leaking old d allows computation of phi(n) if gcd(e, new_e) relationships exist.
    # This demo simply shows concept: with leaked d you can compute k such that e*d = 1 + k*phi(n)
    # thus phi(n) divides (e*d - 1). If e is known, we can find multiples revealing phi(n).
    print("If the old (e,d) pair is known (or d leaked), attacker can derive phi(n) and factor n.")
    print("Conclusion: generating new keys with same modulus is unsafe; must generate new modulus.")

if __name__ == "__main__":
    demonstrate(3599,  d=0, new_e=7)
