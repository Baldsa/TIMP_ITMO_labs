s1 = 's8t|296?'
s2 = 'j9qk93n5' 

for i in range(8):
    print(chr(48 + int(ord(s1[i]) ^ (ord(s2[i]) - 48))), end='')