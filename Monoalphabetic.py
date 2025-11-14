def Monoalphabetic_substitution(text):
    substitute_elements = "QWERTYUIOPASDFGHJKLZXCVBNM"
    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    for char in text:
        if char in alphabets:
            res+=substitute_elements[alphabets.index(char)]
        else:
            res+=char
    return res
print(Monoalphabetic_substitution("HELLO"))
