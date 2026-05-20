import enigma as e

message = "CURRENTTIMEISEIGHTOCLOCKXWEATHERINTHEENGLISHCHANNELISCALMYWITHLIGHTRAINANDSMALLWAVESNEARTHECOASTXHEILHITLERX"

#There will be a rotation of the left rotor!
machine = e.enigma([2,1,3], ["T", "L", "G"], ["C", "O", "E"])
encryptedMessage = machine.op(message,-1,-1,True,False)
rp = [2,14,4]
for i in range(len(message)):
    machine.rotate(1)
    if machine.rotorBuffer[0].rotorPosition == rp[0]+1:
        rp[0] += 1
        rp[1] += 1
        print("_lm_ at", i, "; context:", message[i:])
    elif machine.rotorBuffer[1].rotorPosition == rp[1]+1:
        rp[1] += 1
        print("_m_ at", i, "; context:", message[i:])
    rp[2] = (rp[2]+1)%26
#print(machine.rotorBuffer[0].rotorPosition,machine.rotorBuffer[1].rotorPosition,machine.rotorBuffer[2].rotorPosition)

machine = e.enigma([2,1,3], ["T", "L", "G"], ["C", "O", "E"])
decryptedMessage = machine.op(encryptedMessage,-1,-1)



'''
print("Encrypted text:", encryptedMessage)
print()
print("Decrypted text:", decryptedMessage)
'''
