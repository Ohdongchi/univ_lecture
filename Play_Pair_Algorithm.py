#Play Pair Algorithm

ArrayCHR = []
ArrayCHRCopy = []

for i in range(0,26):
    ArrayCHR.append(0)

#find frequency
def readFileEncryption(mFile):
    with open(mFile, 'r') as file:
        linebyline = file.readline()
        while linebyline != '':
            for i in linebyline:
                if ord(i.lower()) >= 97 and ord(i.lower()) <= 122:
                    temp = ArrayCHR[ord(i.lower()) - 97 ] + 1
                    del ArrayCHR[ord(i.lower()) - 97]
                    ArrayCHR.insert(ord(i.lower()) - 97, temp)
            linebyline = file.readline()
        ArrayCHRCopy.extend(ArrayCHR)

#frequency save to file:
def make_KEY():
    with open('key.txt', 'w') as file:
        for linebyline in ArrayCHR:
            file.writelines(str[linebyline] + ',')
#frequency sort:
def sort_CHRCNT():
    for i in range(len(ArrayCHRCopy)):
        for j in range(len(ArrayCHRCopy) - 1):
            temp1 = ArrayCHRCopy[j]
            temp2 = ArrayCHRCopy[j + 1]
            if temp1 < temp2: # sort
                del ArrayCHRCopy[j]
                del ArrayCHRCopy[j]
                ArrayCHRCopy.insert(j, temp1)
                ArrayCHRCopy.insert(j, temp2)

#Encrypt
def encrypt(mFile):
    with open(mFile, 'r') as rfile:
        with open('encrypt.txt', 'w') as wfile:
            linebyline = rfile.readline()
            while linebyline != '':
                for i in linebyline:
                    if 97 <= ord(i.lower()) <= 122:
                        find_word = ord(i.lower()) - 97

                        for j in range(len(ArrayCHR)):
                            if ArrayCHR[find_word] == ArrayCHRCopy[j]:
                                wfile.write(chr(j + 97))
                            else:
                                wfile.write(i)
                        linebyline = rfile.readline()

#Decrypt
def decrypt(mFile):
    with open('key.txt', 'r') as kfile:
        line = kfile.readline()
        keyArray = line.split(',')
        for i in range(len(keyArray)):
            if keyArray[i] == '':
                continue
            ArrayCHR[i] = int(keyArray[i])
    ArrayCHRCopy.extend(ArrayCHR)
    sort_CHRCNT()
    with open(mFile, 'r') as rfile:
        with open('decrypt.txt', 'w') as wfile:
            linebyline = rfile.readline()
            while linebyline != '':
                for i in linebyline:
                    if 97 <= ord(i.lower()) <= 122:
                        find_word = ord(i) - 97
                        for j in range(len(ArrayCHRCopy)):
                            if ArrayCHRCopy[find_word] == ArrayCHR[j]:
                                wfile.write(chr(j + 97))
                            else:
                                wfile.write(i)

                        linebyline = rfile.readline()
