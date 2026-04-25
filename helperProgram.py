def ati(letter):
    i = ord(letter)
    if i>=97 and i<=122: #a-z
        return i-97
    elif i>=65 and i<=90: #A-Z
        return i-65


def orderLists():
    t1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    t2 = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
    l1 = []
    l2 = []
    for l in t1:
        l1.append(l)

    for l in t2:
        l2.append(l)

    print("l2 before: ", l2)
    exit
    i = 0
    while i < 25:
        if ati(l2[i])>ati(l2[i+1]):
            temp = l2[i+1]
            l2[i+1] = l2[i]
            l2[i] = temp

            temp = l1[i+1]
            l1[i+1] = l1[i]
            l1[i] = temp
            i = -1
        i += 1

    print("\nl2 after: ", l1)

def convertListToInt():
    l = ['F', 'V', 'P', 'J', 'I', 'A', 'O', 'Y', 'E', 'D', 'R', 'Z', 'X', 'W', 'G', 'C', 'T', 'K', 'U', 'Q', 'S', 'B', 'N', 'M', 'H', 'L']
    nl = []
    for i in l:
        nl.append(ati(i))
    print(nl)

convertListToInt()
