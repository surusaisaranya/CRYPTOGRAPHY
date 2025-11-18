# otp_vigenere.py
import string
ALPH = string.ascii_uppercase

def encrypt_one_time_pad(plaintext, key_stream):
    pt = [c for c in plaintext.upper() if c in ALPH]
    ct = []
    for i,ch in enumerate(pt):
        k = key_stream[i]
        ct.append(ALPH[(ALPH.index(ch) + k) % 26])
    return ''.join(ct)

def decrypt_one_time_pad(ciphertext, key_stream):
    ct = [c for c in ciphertext.upper() if c in ALPH]
    pt = []
    for i,ch in enumerate(ct):
        k = key_stream[i]
        pt.append(ALPH[(ALPH.index(ch) - k) % 26])
    return ''.join(pt)

if __name__=="__main__":
    key = [9,0,1,7,23,15,21,14,11,11,2,8,9]  # example from problem 14
    plaintext = "SEND MORE MONEY"
    print("Cipher:", encrypt_one_time_pad(plaintext, key))
