import enigma as e

message = "THECREWISYINGENERALYINGOODORDERXSIGNSOFFATIGUEAFTEREXTENDEDWATCHCYCLESWERENOTEDYWITHNOINCREASEDDISCIPLINARYINCIDENTSXBRIEFINGSANDRESTPERIODSAREBEINGOBSERVEDACCORDINGTOREGULATIONX"

#There will be a rotation of the left rotor!
machine = e.enigma([3,2,1], ["J", "K", "M"], ["T", "V", "R"])
encryptedMessage = machine.op(message,-1,-1,True,False)

machine = e.enigma([3,2,1], ["J", "K", "M"], ["T", "V", "R"])
decryptedMessage = machine.op(encryptedMessage,-1,-1)


print()
print("Encrypted text:", encryptedMessage)
print("Decrypted text:", decryptedMessage)
