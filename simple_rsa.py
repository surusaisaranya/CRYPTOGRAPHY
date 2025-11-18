# small_rsa_privkey.py
import math

def find_p_q(n):
    for p in range(2, int(math.sqrt(n))+1):
        if n % p == 0:
            return p, n//p
    return None, None

def egcd(a,b):
    if b==0: return (1,0,a)
    x,y,g = egcd(b, a%b)
    return (y, x - (a//b)*y, g)

def modinv(a,m):
    x,y,g = egcd(a,m)
    if g != 1:
        return None
    return x % m

if __name__=="__main__":
    n = 3599; e = 31
    p,q = find_p_q(n)
    print("p,q:", p,q)
    phi = (p-1)*(q-1)
    d = modinv(e, phi)
    print("Private key d =", d)
