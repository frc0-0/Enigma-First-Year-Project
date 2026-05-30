import enigma as e
from itertools import permutations

cipher = "ESXOQJRWNDOGCQFPLTILCTCAJWSKVROOHHDFPKQPLWXPTFWAKLZJPUCFLCQRCCDTHXVHOISBLOTBAGEXXESPLFVCOQDCBYTKKXBZWADAUYHNEVZYSVPAVWZBNZUHVUTSBODDEYDSCVTKJHDJDCVURNXGODJQOHAUBWRQWWWZAUACDIGMVD"
cribWord="REGULATION"
cribLen = len(cribWord)

possibleInitialSettings = []

def getInitialSettings(corr, order, rp):
    # Index of the first letter of corr
    index = -1
    for i in range(len(cipher)-len(cribWord)):
        index = i
        for j in range(len(cribWord)):
            if cipher[i+j] != corr[j]:
                index = -1
                break
        if index != -1:
            break

    window = [0,0,0]
    ring   = [0,0,0]
    window[2] = (rp[2] - index) % 26 #There is one rotation of the right rotor each time.

    # The right rotor goes over its notch at most (index//26)+1 times
    # The middle rotor goes over its notch at most (index//26*26)+1 times
    # So the initial position could be from rp[1] to rp[1]-2-(index//26)-(index//26*26)

    #Meanwhile, the left rotor could have rotated at most (index//26*26)+1
    # So the initial position could be from rp[0] to rp[0]-1-(index//26*26)
    machine = e.enigma(order, ["A","A","A"], ["A","A","A"])
    for i in range(26**2):
        ring = [0, (i//26)%26, i%26]

        for r in range(3):
            machine.rotorBuffer[r].ringPosition = ring[r]

        for leftPos in range(rp[0]-1-(index//(26*26)), rp[0]+1):
            for middlePos in range(rp[1]-2-(index//26)-(index//(26*26)), rp[1]+1):
                 
                machine.rotorBuffer[0].rotorPosition = (ring[0] + leftPos)%26
                machine.rotorBuffer[1].rotorPosition = (ring[1] + middlePos)%26
                machine.rotorBuffer[2].rotorPosition = (ring[2] + window[2])%26 

                machine.rotate(index)
                dec = machine.op(corr, -1, -1)
                if dec == cribWord:
                    window[0] = (ring[0] + leftPos)%26
                    window[1] = (ring[1] + middlePos)%26
                    possibleInitialSettings.append([order,ring,[window[0],window[1],(ring[2] + window[2])%26]])
                # Check if its the same as the settings we recieved.


def decrypt():
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

    corrSol = ""
    windowSol = [0,0,0]
    orderSol = [0,0,0]

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
                    print("Match found!")
                    getInitialSettings(corr,order,rp)
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
                    print("Match found!")
                    getInitialSettings(corr,order,rp)
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
                        print("Match found!")
                        getInitialSettings(corr,order,rp)
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
                    print("Match found!")
                    getInitialSettings(corr,order,rp)
                    done = True
                    break
                elif differenceIndex4>0:#Maybe there is an m after lm
                    machine.rotorBuffer[1].rotate(1)
                    machine.rotorBuffer[2].rotate(differenceIndex4)
                    dec = machine.op(corr,differenceIndex4,cribLen,True,True)
                    differenceIndex5 = -1
                    for l in range(cribLen-differenceIndex4):
                        if cribWord[l+differenceIndex4] != dec[l]:
                            differenceIndex5 = l
                            break
                    if differenceIndex5 == -1:
                        print("Match found!")
                        getInitialSettings(corr,order,rp)
                        done = True
                        break
            if done == True:
                break;
        if done == True:
            break;


def main():
    decrypt()
    print(len(possibleInitialSettings))
    for i in possibleInitialSettings:
        print("Current settings: ", i)
        machine = e.enigma(i[0],i[1],i[2],True)
        print(machine.op(cipher,-1,-1))
main()
