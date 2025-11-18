# playfair.py
import string

def build_playfair_matrix(keyword):
    keyword = keyword.upper().replace('J','I')  # merge J into I
    seen = []
    for ch in keyword:
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    for ch in string.ascii_uppercase:
        if ch == 'J': continue
        if ch not in seen:
            seen.append(ch)
    # 5x5 matrix
    mat = [seen[i*5:(i+1)*5] for i in range(5)]
    pos = {mat[r][c]:(r,c) for r in range(5) for c in range(5)}
    return mat, pos

def prepare_text(s):
    s = ''.join([c for c in s.upper() if c.isalpha()]).replace('J','I')
    res = []
    i=0
    while i < len(s):
        a = s[i]
        b = 'X' if i+1==len(s) else s[i+1]
        if a==b:
            res.append(a+'X'); i+=1
        else:
            res.append(a+b); i+=2
    if len(res[-1])==1:
        res[-1] += 'X'
    return res

def encrypt_playfair(plaintext, keyword):
    mat,pos = build_playfair_matrix(keyword)
    pairs = prepare_text(plaintext)
    out = []
    for pair in pairs:
        r1,c1 = pos[pair[0]]
        r2,c2 = pos[pair[1]]
        if r1==r2:
            out.append(mat[r1][(c1+1)%5] + mat[r2][(c2+1)%5])
        elif c1==c2:
            out.append(mat[(r1+1)%5][c1] + mat[(r2+1)%5][c2])
        else:
            out.append(mat[r1][c2] + mat[r2][c1])
    return ''.join(out)

if __name__=="__main__":
    key = "CIPHER"
    pt = "Must see you over Cadogan West Coming at once"
    print("Matrix and encryption:")
    mat,pos = build_playfair_matrix(key)
    for row in mat:
        print(' '.join(row))
    print("Cipher:", encrypt_playfair(pt, key))
