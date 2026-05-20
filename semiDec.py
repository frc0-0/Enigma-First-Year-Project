import enigma as e
from itertools import permutations
cipher = "EKZUZCNOBOZOXLJISABTFAKTBMDEFLDQAFKZALTOPDFSDSWXYBNWPRQCXCNDWFUXMLCZDRPDDMXZQBEZPIUIUDVUXCSODUKOYMLHVGOXOFCZ"
print(len(cipher))
cribWord="ENGLISH"
cribLen = len(cribWord)

# This part finds possible parts of cipher that decrypt to cribword, and stores them in cribCorr
def findCorr():
    cribCorr = []
    foundPossible = True
    for start in range(len(cipher)-len(cribWord)):
        for letter in range(len(cribWord)):
            if cipher[start+letter] == cribWord[letter]:
                foundPossible = False
                break;
        if foundPossible == True:
            cribCorr.append(cipher[start:start+len(cribWord)])
        else:
            foundPossible = True
    return cribCorr

def decrypt(cribCorr):
    machine = e.enigma([1,2,3],["A","A","A"],["A","A","A"])
    corrIndex = 1 #Keep track of progress. Not necessary 
    permIndex = 1 #Keep track of progress. Not necessary
    done=False
    for order in permutations([1,2,3]):
        print("PERMUTATION", permIndex,",", order)
        permIndex += 1
        index = 1
        for corr in cribCorr:
            print(index,"out of",len(cribCorr))
            index += 1
            for i in range(26**3):

                #Rotor position
                rp = [i // 676, (i // 26) % 26, i % 26]

                #Set up Enigma settings:
                for rotor in range(3):
                    machine.rotorBuffer[rotor].setPermutation(order[rotor])
                    machine.rotorBuffer[rotor].rotorPosition = rp[rotor]
    
                #After decryption, look for the first letter that differs.
                dec1 = machine.op(corr,-1,-1,True,True)
                differenceIndex = -1
                for l in range(cribLen):
                    if cribWord[l] != dec1[l]:
                        differenceIndex = l
                        break
                
                #Case1: NULL(no middle,no left rotation)
                if differenceIndex == -1:
                    print("Match found!\nCipher:",corr," Window:",rp)
                    done = True
                    break

                
                #Case2: Only middle: m
                #Since m, only rotate the middle buffer manually
                machine.rotorBuffer[1].rotate(1)
                machine.rotorBuffer[2].rotate(differenceIndex)
                dec = machine.op(corr,differenceIndex,cribLen,True,True)
                differenceIndex2 = -1
                for l in range(cribLen-differenceIndex):
                    if cribWord[l+differenceIndex] != dec[l]:
                        differenceIndex2 = l
                        break
                if differenceIndex2 == -1:
                    print("Match found!\nCipher:",corr," Window:",rp)
                    done = True
                    break
                elif differenceIndex2 == 1: #If differenceIndex2=0, then m at the beginning must be wrong, otherwise we should get at least one correct letter. Recall that it has to be 1, since m lm are right next to each other.
                    #Case3: middle, then leftmiddle: m,lm
                    machine.rotorBuffer[0].rotate(1)
                    machine.rotorBuffer[1].rotate(1)
                    machine.rotorBuffer[2].rotate(differenceIndex2)
                    dec = machine.op(corr,differenceIndex+differenceIndex2,cribLen,True,True)

                    differenceIndex3 = -1
                    for l in range(cribLen-differenceIndex-differenceIndex2):
                        if cribWord[l+differenceIndex+differenceIndex2] != dec[l]:
                            differenceIndex3 = l
                            break
                    if differenceIndex3 == -1:
                        print("Match found!\nCipher:",corr," Window:",rp)
                        done = True
                        break

                #Case4:leftmiddle, then possibly middle: lm...m
                #Note that lm must be first
                if differenceIndex != 0:
                    continue
                machine.rotorBuffer[0].rotate(1)
                #Already rotated [1] from Case 2
                machine.rotorBuffer[2].rotorPosition = rp[2]
                dec = machine.op(corr,-1,-1,True,True)
                differenceIndex4 = -1
                for l in range(cribLen):
                    if cribWord[l] != dec[l]:
                        differenceIndex4 = l
                        break
                if differenceIndex4 == -1:
                    print("Match found!\nCipher:",corr," Window:",rp)
                    done = True
                    break
                elif differenceIndex4>0:#Maybe there is an m after lm
                    machine.rotorBuffer[1].rotate(1)
                    machine.rotorBuffer[2].rotate(differenceIndex4)
                    dec = machine.op(corr,differenceIndex4,cribLen,True,True)
                    differenceIndex5 = -1
                    for l in range(cribLen):
                        if cribWord[l] != dec[l]:
                            differenceIndex5 = l
                            break
                    if differenceIndex5 == -1:
                        print("Match found!\nCipher:",corr," Window:",rp)
                        done = True
                        break
            if done == True:
                break;
        if done == True:
            break;
def main():
    cribCorr = findCorr()
    decrypt(cribCorr)
    
main()
