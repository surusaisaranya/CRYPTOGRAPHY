def create_matrix(key):
    matrix = ""
    key = key.upper().replace("J","I")
    for char in key + "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if char not in matrix:
            matrix+=char
    return [list(matrix[i:i+5])for i in range(0,25,5)]
def finding_position(matrix,ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j]==ch:
                return i,j
def play_cipher(text,key):
    text = text.upper().replace("J","I").replace(" ","")
    matrix = create_matrix(key)
    result = ""
    i=0
    while (i < len(text)):
        a = text[i]
        b = 'X'
        if (i+1) < len(text) and text[i]!=text[i+1]:
            b = text[i+1]
            i+=2
        else:
            i+=1
        
        r1 , c1 = finding_position(matrix,a)
        r2 , c2 = finding_position(matrix,b)

        if r1==r2:
            result+=matrix[r1][(c1+1)%5]
            result+=matrix[r2][(c2+1)%5]
        
        elif c1==c2:
            result+=matrix[(r1+1)%5][c1]
            result+=matrix[(r2+1)%5][c2]

        else:
            result+=matrix[r1][c1]
            result+=matrix[r2][c2]
        
    return result

print(play_cipher("BALLOON","MONARCHY")) 
