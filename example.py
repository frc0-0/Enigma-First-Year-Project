import enigma as e

message = "Secretmessage"

machine = e.enigma([2,4,3], "B")

#Encryption
machine.rotorBuffer[0].ringPosition = e.ati("C")
machine.rotorBuffer[0].rotorPosition = e.ati("D")

machine.rotorBuffer[1].ringPosition = e.ati("E")
machine.rotorBuffer[1].rotorPosition = e.ati("S")

machine.rotorBuffer[2].ringPosition = e.ati("Y")
machine.rotorBuffer[2].rotorPosition = e.ati("T")

machine.plugboard.add(e.ati("S"), e.ati("G"))
machine.plugboard.add(e.ati("F"), e.ati("X"))
machine.plugboard.add(e.ati("H"), e.ati("B"))
machine.plugboard.add(e.ati("K"), e.ati("M"))
machine.plugboard.add(e.ati("Q"), e.ati("L"))
machine.plugboard.add(e.ati("R"), e.ati("U"))

enctyptedMessage = machine.op(message)
print(enctyptedMessage)


#Decryption
machine.rotorBuffer[0].ringPosition = e.ati("C")
machine.rotorBuffer[0].rotorPosition = e.ati("D")

machine.rotorBuffer[1].ringPosition = e.ati("E")
machine.rotorBuffer[1].rotorPosition = e.ati("S")

machine.rotorBuffer[2].ringPosition = e.ati("Y")
machine.rotorBuffer[2].rotorPosition = e.ati("T")

decryptedMessage = machine.op(enctyptedMessage)
print(decryptedMessage)
