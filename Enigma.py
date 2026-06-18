# Converts letter to integer 0-25.
def ati(letter):
    i = ord(letter)

    if i>=65 and i<=90: #A-Z
        return i-65

# Converts numbers 0-25 to A-Z
def ita(num):
    if num>=0 and num <= 25:
        return chr(num+65)

#Note that A=0, B=1, C=2, etc...
class rotor:
    # historicRotorType. If given 1-5, it will populate the rotor class with the appropriate values
    # based off of https://en.wikipedia.org/wiki/Enigma_rotor_details for the Enigma I and M3 Army.
    # Otherwise, it will do nothing.
    def __init__(self, historicRotorType=0):
        self.ringPosition = 0
        self.notchPosition = 0 #Only AFTER encountering the notch will the mechanism rotate the next rotor.
        self.rotorPosition = 0
        self.permutationEnter = [] #This is the permutation used when coming from the ETW(input wheel).
        self.permutationExit = [] #This is the permutation used after reflecting.

        if historicRotorType == 1:
            self.notchPosition = ati("Q")
            self.permutationEnter = [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9]
            self.permutationExit = [20, 22, 24, 6, 0, 3, 5, 15, 21, 25, 1, 4, 2, 10, 12, 19, 7, 23, 18, 11, 17, 8, 13, 16, 14, 9] 
        elif historicRotorType == 2:
            self.notchPosition = ati("E")
            self.permutationEnter = [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]
            self.permutationExit = [0, 9, 15, 2, 25, 22, 17, 11, 5, 1, 3, 10, 14, 19, 24, 20, 16, 6, 4, 13, 7, 23, 12, 8, 21, 18] 
        elif historicRotorType == 3:
            self.notchPosition = ati("V")
            self.permutationEnter = [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]
            self.permutationExit = [19, 0, 6, 1, 15, 2, 18, 3, 16, 4, 20, 5, 21, 13, 25, 7, 24, 8, 23, 9, 22, 11, 17, 10, 14, 12] 

    def rotate(self):
        self.rotorPosition = (self.rotorPosition+1)%26

class plugboard:
    # To connect two letters, call the function add, passing both letters as numbers. To remove this connection, call remove with one of these letters.

    def __init__(self):
        self.connection = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

    def add(self, l1, l2):
        self.connection[ati(l1)] = ati(l2)
        self.connection[ati(l2)] = ati(l1)

    def remove(self, l0):
        self.connection[self.connection[ati(l0)]] = self.connection[ati(l0)]
        self.connection[ati(l0)] = ati(l0)

    def removeAll(self):
        for i in range(26):
            self.connection[i] = i

class enigma:
    # rotorType should be a list of the rotors, from left to right. The rightmost will be connected to the ETW.
    def __init__(self, rotorTypes, rotorRings, rotorPositions):
        self.rotorBuffer = []
        self.reflector = [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19]
        self.plugboard = plugboard()

        for i in range(3):
            self.rotorBuffer.append(rotor(rotorTypes[i]))
            self.rotorBuffer[i].ringPosition = ati([rotorRings, rotorPositions][0][i])
            self.rotorBuffer[i].rotorPosition = ati([rotorRings, rotorPositions][1][i])

    def rotate(self, num):
        for k in range(num):
            hasRotated = False # if rotNext has rotated.

            for i in range(2):
                if hasRotated is True:
                    hasRotated = False
                    continue

                rotCurrent = self.rotorBuffer[i]
                rotNext = self.rotorBuffer[i+1]

                if rotNext.notchPosition == rotNext.rotorPosition:
                    rotCurrent.rotate()  
                    rotNext.rotate()
                    hasRotated = True

            if hasRotated is False:
                self.rotorBuffer[2].rotate()
    def op(self, text):
        newText = []

        for i in text:
            letter = ati(i)

            #Rotate rotor
            self.rotate(1)

            #Plugboard
            letter = self.plugboard.connection[letter]

            #Forward
            for i in range(3):
                rot = self.rotorBuffer[2-i]
                letter = rot.permutationEnter[(letter + (rot.rotorPosition - rot.ringPosition))%26]
                letter -= (rot.rotorPosition - rot.ringPosition)%26

            #Reflect
            letter = self.reflector[letter]

            #Backward
            for i in range(3):
                rot = self.rotorBuffer[i]
                letter = rot.permutationExit[(letter + (rot.rotorPosition - rot.ringPosition))%26]
                letter -= (rot.rotorPosition - rot.ringPosition)%26

            #Plugboard
            letter = self.plugboard.connection[letter]
            newText.append(ita(letter))

        return "".join(newText)